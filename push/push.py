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
import subprocess

token = ''

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
        
        #buy ticket
        def assistant():
            get = { 
                    '1':'1'
            }
            post = {
                    'action':'get_ticket',
                    'auth':'ticket'
            }
            rep = transfer('https://mp.weixin.qq.com/misc/safeassistant', get, post, None)
            return rep['ticket']
        ticket = assistant()
        if ticket == None:
            return None
        
        # change the card
        def qrconnect(t):
            url = 'https://mp.weixin.qq.com/safe/safeqrconnect'
            get = { 
                    '1':'1'
            }
            post = {
                    'appid':'wx3a432d2dbe2442ce',
                    'scope':'snsapi_contact',
                    'state':'0',
                    'redirect_uri':'https://mp.weixin.qq.com',
                    'login_type':'safe_center',
                    'type':'json',
                    'ticket':ticket,
            }
            def uuid(url, rep):
                rep = json.loads(rep)
                if rep.has_key('uuid'):
                    return rep
                return None

            rep = transfer(url , get, post, None, uuid)
            if rep == None:
                return None
            return rep['uuid']
        uuid = qrconnect(ticket)
        if uuid == None:
            return None
        #sequential number
        #i don't know how to make it, but it must be made in client.
        msgid = '407438052'
        
        #print the card
        def qrcode(ticket, uuid):
            url = 'https://mp.weixin.qq.com/safe/safeqrcode'
            get = {
                    'ticket':ticket,
                    'uuid':uuid,
                    'action':'check',
                    'type':'login',
                    'auth':'ticket',
                    'msgid':msgid,
            }
            def qrcode(url, rep):
                img = 'qr.jpg'
                with open(img, 'wb') as qr:
                    qr.write(rep)
                return img
            return transfer(url, get, None, None, qrcode)
        img = qrcode(ticket, uuid)

        #checking the card
        def safeuuid(uuid):
            url = 'https://mp.weixin.qq.com/safe/safeuuid'
            get = {
                    'timespam':str(time.time()).replace('.', ''),
                    'token':'',
                    }
            post = {
                    'token':'',
                    'uuid':uuid,
                    'action':'json',
                    'type':'json',
                    }                    
            def pass_ack(url, resp):
                resp = json.loads(resp)
                if resp.has_key('code'):
                    return resp['code']
                return None

            return transfer(url , get, post, None, pass_ack)
        if sys.platform == 'win32':
            subprocess.Popen('mspaint %s' % img)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', img])
        else:
            print 'could not open the qr image.'
            sys.exit(0)
        code = None
        while code == None:
            code = safeuuid(uuid)

        os.remove(img)

        #verify the account
        def verify(email, msgid, code):
            url = 'https://mp.weixin.qq.com/cgi-bin/securewxverify'
            post = {
                'token':'',
                'code':code,
                'account':email,
                'operation_seq':msgid
            }

            def verify_ack(url, r):
                return r
            return transfer(url , None, post, None)
        result = verify(email, msgid, code)
        return result['redirect_url'].split("=")[-1]

def logout():
    urllib2.urlopen('https://mp.weixin.qq.com/cgi-bin/logout?t=wxm-logoout')

def transfer(url, get = None, post = None, header = None, ack = None):
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
    if ack == None:
        def ack(url, rep):
            rep = json.loads(rep)
            if rep['base_resp']['ret'] != 0:
                print url, '->', rep
                return None
            return rep
    return ack(url, rep)

def ticket():
    rep = transfer('https://mp.weixin.qq.com/cgi-bin/message', get={'t':'message/list', 'count':20, 'day':0})
    if rep == None:
        return None, None
    user = rep['user_info']['user_name']
    media = rep['base_resp']['media_ticket']
    return user, media

def upload_image(path):
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


def add_message(cover, title, content, digest='', author='', source=''):
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
            'sourceurl0':source,
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
def image_path():
    url = 'https://mp.weixin.qq.com/cgi-bin/filepage'
    get = {
            'type':2, 
            't':'media/img_list',
    }
    rep = transfer(url, get)
    id_path = {}
    for image in rep['page_info']['file_item']:
            id_path[image['file_id']] = image['cdn_url'].replace('\/', '/')
    return id_path


if __name__ ==  '__main__':
    import sys
    import re
    import markdown2
    import anydbm
    token = login(sys.argv[1], sys.argv[2])
    if token == None:
        print 'failure to login'
        sys.exit(0)
    imgs = anydbm.open('cache.db', 'c')
    root = sys.argv[3]
    if sys.argv[3].find('cook') == -1:
        source = 'http://note.codepongo.com/article/' + sys.argv[4][:-len('.md')]
    else:
        source = 'http://cook.codepongo.com/' + sys.argv[4][:-len('.md')]

    with open(os.path.join(root, sys.argv[4])) as f:
        title = f.readline()[:-1]
        f.readline()
        content = f.read()
    cover = None
    for img in re.findall(re.compile(r"\!\[.*\]\((.*)\)"), content):
        # if the image is already in server, path is the image id
        # the code does not process this situation :(
        # i will fix it later.
        imgs[img] = upload_image(os.path.join(root, img))
        if cover == None:
            cover = imgs[img]

    server = image_path()
    # improve compatibility
    if sys.platform == 'darwin':
        for k in imgs.keys():
            local_path = k
            local_id = imgs[k]
            for server_id, server_path in server.items():
                if server_id == int(local_id):
                    imgs[local_path] = server_path
        for k in imgs.keys():
            v = imgs[k]
            content = content.replace(k, v)
    else:
        for local_path, local_id in imgs.items():
            for server_id, server_path in server.items():
                if server_id == int(local_id):
                    imgs[local_path] = server_path
    
        for k, v in imgs.items():
            content = content.replace(k, v)
    content = markdown2.markdown(content).replace('<h2>', '<br /><br /><h2><b>').replace('</h2>', '</b></h2><br /><br />').encode('utf8')
    add_message(cover, title, content, author='Zuo Haitao(codepongo)', source=source)
    logout()
    if sys.platform == 'darwin':
        os.remove('cache.db.db')
    else:
        os.remove('cache.db')

