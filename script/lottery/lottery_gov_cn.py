#coding:utf8
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
        self.flag = None
        HTMLParser.HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'td' and len(attrs) == 3 and attrs[0] == ('height', '23'):
            self.flag = 'issue'
            return
        if tag == 'td' and len(attrs) == 3 and attrs[2] == ('class', 'red'):
            self.flag = 'red'
            return
        if tag == 'td' and len(attrs) == 4 and attrs[3] == ('class', 'blue'):
            self.flag = 'blue'
            return
        if tag == 'td' and len(attrs) == 2:
            self.flag = 'publish'
            return
    def handle_endtag(self, tag):
        if tag == 'tr' and len(self.item.keys()) == 4:
            self.result.append(self.item)

    def handle_data(self, data):
        d = data.strip()
        if self.flag == None or d == '':
            self.flag = None
            return
        if self.flag == 'publish' or self.flag == 'issue':
            self.item[self.flag] = d
            return
        if not self.item.has_key(self.flag):
            self.item[self.flag] = ''
        self.item[self.flag] += d + ' '
        self.flag = None
class Found(BaseException):
    pass
class ParserForLast(Parser):
    def handle_data(self, data):
        Parser.handle_data(self, data)
        if len(self.result) == 1:
            raise Found, self.result

class DLT():
    def last(self):
        url = 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=dlt'
        html = urllib.urlopen(url).read()
        r = None
        try:
            r = ParserForLast().feed(html)
        except Found, result:
            return result[0][0]
        if r != None and isinstance(r, list) and len(r) >=1 and r[0].has_key('numbers'):
            return r[0]
        else:
            return None

if __name__ == '__main__':
    r = DLT().last()
    numbers = r['red'] + ' + ' + r['blue']
    reply = '%s第%s期%s' % (r['publish'], r['issue'], numbers)
    print reply.decode('utf8')

