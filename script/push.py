import urllib
import json
def token(appid, secret):
    query = {}
    query['grant_type'] = 'client_credential'
    query['appid'] = appid
    query['secret'] = secret
    addr = 'https://api.weixin.qq.com/cgi-bin/token'
    rep = urllib.urlopen(addr + '?' + urllib.urlencode(query))
    if 200 == rep.getcode():
        return json.loads(rep.read())['access_token']
    return None


def upload_media():
    pass #push_thumbnail

def push_article():
    pass


if __name__ == '__main__':
    import sys
    token = token(sys.argv[1], sys.argv[2])
