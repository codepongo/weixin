import urllib
import urllib2
import cookielib
import json
import hashlib
import os
import poster
import random
import time

token = None

def login(email, password):
    poster.streaminghttp.register_openers()
    cookie = cookielib.LWPCookieJar('cookie.txt')
### poster.streaminghttp.register_openers() ###
### http://oldj.net/article/python-upload-file-via-form-post/
#from poster.encode import multipart_encode
#from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
#handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
#opener = urllib2.build_opener(*handlers)
#urllib2.install_opener(opener)
###
    opener = poster.streaminghttp.register_openers()
    opener.add_handler(urllib2.HTTPCookieProcessor(cookie))

    req = urllib2.Request('https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN', urllib.urlencode({'username': email, 'pwd':hashlib.md5(password).hexdigest(), 'imgcode':'', 'f':'json'}))
    req.add_header('Referer', 'https://mp.weixin.qq.com')
    rep = urllib2.urlopen(req).read()
    cookie.save()
    
    result = json.loads(rep)

    if 'base_resp' in result and result['base_resp']['ret'] == 0:
        return result['redirect_url'].split("=")[-1]
def logout():
    urllib2.urlopen('https://mp.weixin.qq.com/cgi-bin/logout?t=wxm-logoout')

def transfer(url, get = None, post = None, header = None):
    time.sleep(1)
    query = {'lang':'zh_CN', 'token':token} 
    if get != None:
        get.update(query)
        get.update({'f':'json'})
        url = url + '?' + urllib.urlencode(get)

    if post != None:
        if type(post) == 'dict':
            post.update(query)
            post.update({'ajax':1, 'random':random.random()})
            if 't' not in post.keys():
                post['t'] = 'ajax-response'
            post = urllib.urlencode(post)
        req = urllib2.Request(url, post)
    else:
        req = urllib2.Request(url)
    req.add_header('Referer', 'https://mp.weixin.qq.com')

    if header != None:
        for k,v in header.items():
            req.add_header(k, v)
    rep = urllib2.urlopen(req).read()
    rep = json.loads(rep)
    if rep['base_resp']['ret'] != 0:
        print url, '->', rep
        return None
    return rep


def ticket():
    rep = transfer('https://mp.weixin.qq.com/cgi-bin/message', get={'t':'message/list', 'count':20, 'day':0})
    if rep == None:
        return None, None
    user = rep['user_info']['user_name']
    media = rep['base_resp']['media_ticket']
    return user, media



def upload_image_as_cover(path):
    user, media = ticket()
    if user == None:
        return None
    url = 'https://mp.weixin.qq.com/cgi-bin/filetransfer'
    get = {
        'action':'upload_material',
        'f':'json',
        'writetype':'doublewrite',
        'groupid':1,
        'ticket_id':user,
        'ticket':media,
        'token':token,
    }
    field = {'file': open(path, 'rb')}
    post, header = poster.encode.multipart_encode(field)
    rep = transfer(url, get, post, header)
    return rep['content']

def send_message_to_all():
    pass

if __name__ ==  '__main__':
    import sys
    token = login(sys.argv[1], sys.argv[2])
    media_id = upload_image_as_cover(os.path.join('res', 'qrcode_for_gh_de3d190f1f61_258.jpg'))
   # if media_id == None:
   # sys.exit(0)
    logout()


    
