#coding:utf8
import sys
import os
sys.path.append(os.path.dirname(__file__))
import web
import hashlib
import xml.etree.ElementTree
import time
import tianqi
try:
    import conf
    token = conf.token
    ico_path = conf.icon_path
    res_path = conf.res_path
except:
    token = 'test token'
    ico_path = './'
    res_path = './res'
errmsg ='''无效的输入。
获取天气信息：请尝试输入： 城市名+天气，如，北京天气
'''
def check_signature(signature, timestamp, nonce):
    sha1 = hashlib.sha1()
    l = [token, timestamp, nonce]
    l.sort()
    map(sha1.update, l)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        return True
    else:
        return False

class favicon:
    def GET(self):
        content = None
        with open(os.path.join(ico_path, 'favicon.ico'), 'rb') as f:
            content = f.read()
        web.header('content-type', 'image/x-icon')
        return content

class image:
    def GET(self, name, ext):
        content = None
        with open(os.path.join(res_path, name + '.' + ext), 'rb') as f:
            content = f.read()
        web.header('content-type', 'image/%s' % ext)
        return content

class index():
    def GET(self, query=''):
        return web.template.render(os.path.join(os.path.dirname(__file__), 'templates')).index(None)

class server:
    def GET(self):
        get_data = web.input()
        if len(get_data) == 0:
            raise web.seeother('/index')
        signature = get_data.signature
        timestamp = get_data.timestamp
        nonce = get_data.nonce
        echo = get_data.echostr
        if check_signature(signature, timestamp, nonce):
            return echo

    def POST(self):
        pass
        req = xml.etree.ElementTree.fromstring(web.data())
        content = req.find("Content").text
        msgType = req.find("MsgType").text
        fromUser = req.find("FromUserName").text
        toUser = req.find("ToUserName").text
        content = content.encode('utf8')
        if -1 != content.find('天气'):
            city = content.replace('天气', '')
            w = tianqi.baidu(city)
            today = w['data']['weather']['content']['today']
            tomorrow = w['data']['weather']['content']['tomorrow']
            reply = u'【%s】%s，天气%s，风力%s，温度%s，PM2.5:%s。%s，天气%s，风力%s，气温%s。http://app.codepongo.com/weather' %(
                    w['data']['weather']['content']['city'],
                    today['date'],
                    today['condition'],
                    today['wind'],
                    today['temp'],
                    today['pm25'],
                    tomorrow['date'],
                    tomorrow['condition'],
                    tomorrow['wind'],
                    tomorrow['temp'],
                    )
            return web.template.render(os.path.join(os.path.dirname(__file__), 'templates')).replytext(fromUser,toUser,int(time.time()),reply)
        else:
            return web.template.render(os.path.join(os.path.dirname(__file__), 'templates')).replytext(fromUser,toUser,int(time.time()), errmsg)

        

urls = (
    '/server', server,
    '/favicon.ico', favicon,
    '/(.*).(jpg)', image,
    '/(.*)', index,

)
app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
else:
    application = app.wsgifunc()
