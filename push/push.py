#coding:utf8
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
        if type(post) == dict:
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
    field = {'file': open(path, 'rb'), 'filename':'test.jpg'}
    post, header = poster.encode.multipart_encode(field)
    rep = transfer(url, get, post, header)
    return rep['content']


def add_message(cover, title, content, digest='', author='', url=''):
    url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg'
    post = {
            'AppMsgId': '', 
            'count': 1, 
            'sub': 'create',
            'type': 10,
            'title0':title,
            'content0':content,
            'digest0':digest,
            'author0':author,
            'fileid0':cover,
            'sourceurl0':url,
            'show_cover_pic0':0,
            'shortvideofileid0':'',
            'copyright_type0':0,
            'releasefirst0':0,
            'can_reward0':0,
            'reward_wording0':'',
            'reprint_permit_type0':0,
            'original_article_type0':'',
            'need_open_comment0':1,

            }
    rep = transfer(url, post=post)
    return rep['appMsgId']
def send_mass_message(msg_id, gender=0, group_id=-1):
    url = 'https://mp.weixin.qq.com/cgi-bin/masssendpage'
    get = {
            't':'mass/send',
    }
    rep = transfer(url, get)
    op = rep['operation_seq']
    #administractor's certification 

def image_path(image_id):
    image_list_cache = 'image_list.txt'
    image_list = ''
    if os.path.isfile(image_list_cache):
        with open(image_list_cache, 'rb') as f:
            lines = f.readlines()
        if len(lines) != 0:
            for line in lines:
                [id, url] = line.split('\t')
                if int(id) == int(image_id):
                    return url
    url = 'https://mp.weixin.qq.com/cgi-bin/filepage'
    get = {
            'type':2, 
            't':'media/img_list',
    }
    rep = transfer(url, get)
    with open(image_list_cache, 'ab+') as f:
        for image in rep['page_info']['file_item']:
            print type(image['file_id']), type(image_id)
            if image['file_id'] == int(image_id):
                f.write('%d\t%s\n' %(image['file_id'], image['cdn_url'].replace('\/', '/')))
                return image['cdn_url'].replace('\/', '/')
    return None


title = '''hello, wechat's gong zhong hao'''
content = '''
这个是猪火腿的公众号第一条消息。用于测试程序。
<br />
代码可以在https://github.com/codepongo/weixin可以找到。
<br />
目前，程序只能完成：
<ul>
 <li>登陆，登出</li>
 <li>上传图片</li>
 <li>增加图文消息</li>
</ul>
<b>无法自动推送消息:(</b>
<br />
<br />
Hi, this message is the first message from Codepongo's Gong Zhong Hao, and it is for testing the program.
<br />
The source code is hosted in https://github.com/codepongo/weixin.
<br />
now, the function of it:
<ul>
  <li>login and logout</li>
  <li>upload image resource</li>
  <li> add message with image to wechat's platform</li>
</ul>
<b>but, it has not publish the message yet. :(</b>
'''

if __name__ ==  '__main__':
    import sys
    token = login(sys.argv[1], sys.argv[2])
    result = {}
    result['cover'] = upload_image_as_cover(os.path.join('res', 'qrcode_for_gh_de3d190f1f61_258.jpg'))
    result['appMsgId'] = add_message(result['cover'], title, content)
    print image_path(result['cover'])
    print result
    logout()

