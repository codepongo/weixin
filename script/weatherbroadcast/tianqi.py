#coding:utf8
import json
import urllib
key = ''
try:
    import cfg
    key = cfg.key
except:
    pass

def baidu(where=''):
    url = 'https://www.baidu.com/home/other/data/weatherInfo'
    if where != '':
        url = '%s?city=%s' % (url, urllib.quote(where))
    print url
    info = json.loads(urllib.urlopen(url).read())
    r = {
            'location' : '',
            'date' : '',
            'today': {
                'weather' : '', 
                'wind' : '',
                'temp' : '',
                'pm25' : '',
                'index': ''
            },
            'tomorrow' : {
                'date' : '',
                'weather' : '',
                'wind' : '',
                'temp' : ''
            }
    }
    if not info['data']['weather'].has_key('content'):
        return r
    r['location'] = info['data']['weather']['content']['city']
    today = info['data']['weather']['content']['today']
    tomorrow = info['data']['weather']['content']['tomorrow']
    r['date'] = today['date']
    r['today']['weather'] = today['condition']
    r['today']['wind'] = today['wind']
    r['today']['temp'] = today['temp']
    r['today']['pm25'] = today['pm25']
    r['today']['index'] = ''
    r['tomorrow']['date'] = tomorrow['date']
    r['tomorrow']['weather'] = tomorrow['condition']
    r['tomorrow']['wind'] = tomorrow['wind']
    r['tomorrow']['temp'] = tomorrow['temp']
    return r


def baiduapi(where):
    url = 'http://api.map.baidu.com/telematics/v3/weather?output=json&ak=%s&location=%s' %(key, urllib.quote(where))
    print url
    r = {
            'location' : '',
            'date' : '',
            'today': {
                'weather' : '', 
                'wind' : '',
                'temp' : '',
                'pm25' : '',
                'index': ''
            },
            'tomorrow' : {
                'date' : '',
                'weather' : '',
                'wind' : '',
                'temp' : ''
            }
    }
    info = json.loads(urllib.urlopen(url).read())
    if info.has_key('error') and info['error'] != 0:
        return r
    now = info['results'][0]['weather_data'][0]['date']
    temp = info['results'][0]['weather_data'][0]['temperature'] + now[now.find('('):]
    index = ''
    for idx in info['results'][0]['index']:
        if idx['title'] == u'穿衣':
            index += u'气温' + idx['zs'] +', '
        else:
            index += '%s%s, ' % (idx['zs'], idx['title'])
    r['location'] = info['results'][0]['currentCity']
    r['date'] = info['date']
    r['today']['weather'] = info['results'][0]['weather_data'][0]['weather']
    r['today']['wind'] = info['results'][0]['weather_data'][0]['wind']
    r['today']['temp'] = temp
    r['today']['pm25'] = info['results'][0]['pm25']
    r['today']['index'] = index
    r['tomorrow']['date'] = u'明天'
    r['tomorrow']['weather'] = info['results'][0]['weather_data'][1]['weather']
    r['tomorrow']['wind'] = info['results'][0]['weather_data'][1]['wind']
    r['tomorrow']['temp'] = info['results'][0]['weather_data'][1]['temperature']
    return r

def print_weather(r):
    print r['location']
    print r['date']
    print r['today']['weather']
    print r['today']['wind']
    print r['today']['temp']
    print r['today']['pm25']
    print r['today']['index']
    print r['tomorrow']['date']
    print r['tomorrow']['weather']
    print r['tomorrow']['wind']
    print r['tomorrow']['temp']


if __name__ == '__main__':
    print_weather(baiduapi('北京'))
    print_weather(baiduapi('佳木斯'))
    print_weather(baiduapi('哈尔滨'))

    print_weather(baidu())
    print_weather(baidu('北京'))
    print_weather(baidu('佳木斯'))
    print_weather(baidu('哈尔滨'))
