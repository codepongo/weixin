import urllib
import urllib2
import cookielib
import json
import hashlib
def login(email, password):
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.MozillaCookieJar('cookie.txt'))))

    req = urllib2.Request('https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN', urllib.urlencode({'username': email, 'pwd':hashlib.md5(password).hexdigest(), 'imgcode':'', 'f':'json'}))
    req.add_header('Referer', 'https://mp.weixin.qq.com')
    rep = urllib2.urlopen(req).read()
    
    result = json.loads(rep)
    print result

    if 'base_resp' in result and result['base_resp']['ret'] == 0:
        return result['redirect_url'].split("=")[-1]

def upload_image_as_cover():
    pass

def send_message_to_all():
    pass

if __name__ ==  '__main__':
    import sys
    print login(sys.argv[0], sys.argv[1])

    
