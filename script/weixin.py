#coding:utf-8
import sys
import os
sys.path.append(os.path.dirname(__file__))
import web
import hashlib
try:
    import conf
    token = conf.token
except:
    token = 'test token'

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
    def GET(self, name):
        content = None
        with open(os.path.join(ico_path, name), 'rb') as f:
            content = f.read()
        web.header('content-type', 'image/x-icon')
        return f.read()

#class image:
#    def GET(self, name):
#        ext = os.path.splitext(name)
#        content = None
#        with open(os.path.join(ico_path, name), 'rb') as f:
#            content = f.read()
#        web.header('content-type', 'image/x-icon')
#        return f.read()

class index():
    def GET(self, query=''):
        return web.template.render(os.path.join(os.path.dirname(__file__), 'templates')).index(None)

class authentication:
    def GET(self):
        get_data = web.input()
        signature = get_data.signature
        timestamp = get_data.timestamp
        nonce = get_data.nonce
        echo = get_data.echostr
        if check_signature(signature, timestamp, nonce):
            return echo

urls = (
    '/authentication', authentication,
    '/favicon.ico', favicon,
    '/(.*)', index,

)
app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
else:
    application = app.wsgifunc()
