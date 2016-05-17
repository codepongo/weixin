#coding:utf8
import json
import urllib
def baidu(where=''):
    url = 'https://www.baidu.com/home/other/data/weatherInfo'
    if where != '':
        url = '%s?city=%s' % (url, urllib.quote(where))
    return json.loads(urllib.urlopen(url).read())


def print_weather(info):
    today = info['data']['weather']['content']['today']
    print info['data']['weather']['content']['city']
    print today['date']
    print today['condition']
    print today['wind']
    print today['temp']
    print today['pm25']
    tomorrow = info['data']['weather']['content']['tomorrow']
    print tomorrow['date']
    print tomorrow['condition']
    print tomorrow['wind']
    print tomorrow['temp']
if __name__ == '__main__':
    print_weather(baidu())
    print_weather(baidu('北京'))
    print_weather(baidu('佳木斯'))
    print_weather(baidu('哈尔滨'))

