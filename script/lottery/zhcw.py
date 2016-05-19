import HTMLParser
import urllib
import copy

class Parser(HTMLParser.HTMLParser):
    def feed(self, c):
        HTMLParser.HTMLParser.feed(self, c)
        return self.result
    def __init__(self):
        self.result = []
        self.item = {}
        self.valuable = False
        HTMLParser.HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'td' and len(attrs) == 1 and attrs[0] == ('align', 'center'):
            self.valuable = True
            return
        if tag == 'em':
            self.valuable = True
            return
        if tag == 'strong' and len(attrs) == 1 and attrs[0] == ('class', 'rc'):
            self.valuable = False
            return
    def handle_data(self, data):
        if not self.valuable:
            return
        if not self.item.has_key('publish'):
            if data.strip() != '':
                self.item['publish'] = data
        elif not self.item.has_key('issue'):
            self.item['issue'] = data
        else:
            if not self.item.has_key('numbers'):
                self.item['numbers'] = []
            if data.strip() != '':
                self.item['numbers'].append(data)
            if len(self.item['numbers']) == 7:
                self.result.append(copy.deepcopy(self.item))
                self.item.clear()
        self.valuable = False

class FirstPageParser(Parser):
    def __init__(self):
        self.cn = None
        Parser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if cn == None and tag == 'p' and len(attrs) == 1 and attrs[0] == ('class', 'pg'):
            cn = 0
            return
        return Parser.handle_starttag(self, tag, attrs)
    def handle_data(self, data):
        if cn == 0:
            try:
                cn = int(data)
            except:
                pass
            return
        return Parser.handle_data(self, data)


def save(result):
    import db
    count = len(result)
    i = 0.00
    db.open()
    db.begin()
    for r in result:
        print '\b' * 8, '%2.2f%%' % (i * 100 / count),
        r['numbers'] = ''.join(r['numbers'])
        r['numbers'] = r['numbers'][:-2] + '+' + r['numbers'][-2:]
        db.tinsert('ssq', r)
        i += 1
    db.commit()
    print '\b' * 8, '100.00%'
    db.close()

def snatch():
    import time
    import json
    import base64
    import os
    url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list.html'
    if True:
        html = urllib.urlopen(url).read()
    else:
        html = ''
        with open('t.html', 'rb') as f:
            html = f.read()
    result = []
    result.append(FirstPageParser().feed(html))
    url_ = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_%s.html'
    for i in range(2, cn+1):
        url = url_ % (i)
        cache = base64.b64encode(url)
        html = ''
        if not os.path.isfile(cache):
            html = urllib.urlopen(url).read()
            time.sleep(5)
            with open(cache, 'wb') as f:
                f.write(html)
        with open(cache, 'rb') as f:
            html = f.read()
        result.append(Parser().feed(html))
    return result

class SSQ():
    def last(self):
        url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list.html'
        html = urllib.urlopen(url).read()
        r = Parser().feed(html)
        if r != None and isinstance(r, list) and len(r) >=1 and r[0].has_key('numbers'):
            return r[0]['numbers']
        else:
            return None
if __name__ == '__main__':
#    issues = snatch()
#    save(issues)
    print SSQ().last()


