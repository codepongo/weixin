#coding:utf8
import requests
import time
url = 'http://127.0.0.1:8080/server'
msg = '''<xml>
 <ToUserName><![CDATA[%s]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName> 
 <CreateTime>%d</CreateTime>
 <MsgType><![CDATA[%s]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 <MsgId>%d</MsgId>
 </xml>'''

def authentication():
    requests.get(url, params={
        'signature':'f36141c4c275d2216c9269cf13232308c384f946',
        'timestamp':'',
        'nonce':'',
        'echostr':''
        })

def post_text(content):
    r = requests.post(url, data = msg % ('zhuhuotui', 'codepongo', int(time.time()), 'text', content, 1)) 
    print r.text
if __name__ == '__main__':
    #authentication()
    post_text('北京天气')
#    post_text('天气天气')
#    post_text(u'manual天气'.encode('utf8'))
#    post_text('天气热')



