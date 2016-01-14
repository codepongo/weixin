import urllib
import urllib2
import cookielib
def login():
    urllib2.install_opener(urllib2.build_opner(urllib2.HTTPCookieProcessor(cookielib.MozillaCookieJar(cookie.txt))))

    
