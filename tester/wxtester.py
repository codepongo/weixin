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
    return r.text
if __name__ == '__main__':
    #authentication()
    case = [
            '北京天气',
            u'manual天气'.encode('utf8'),
            '天气热',
            '双色球', 
            '双色球天气', 
            '大乐透',
    ]
    for c in case:
        print c.decode('utf8')
        print post_text(c)
        print '-----'



