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
        if tag == 'td' and len(attrs) == 1 and attrs[0] == ('height', '24'):
            self.flag = 'issue'
            return
        if tag == 'font' and len(attrs) == 1 and attrs[0] == ('class', 'FontRed'):
            self.flag = 'red'
            return
        if tag == 'font' and len(attrs) == 1 and attrs[0] == ('class', 'FontBlue'):
            self.flag = 'blue'
            return
        if tag == 'td' and len(attrs) == 0 and self.item.has_key('blue'):
            self.flag = 'publish'
            return
    def handle_data(self, data):
        d = data.strip()
        if self.flag == None or d == '':
            self.flag = None
            return
        self.item[self.flag] = d
        self.flag = None
        if self.item.has_key('publish'):
            self.result.append(self.item)
class Found(BaseException):
    pass
class ParserForLast(Parser):
    def handle_data(self, data):
        Parser.handle_data(self, data)
        if len(self.result) == 1:
            raise Found, self.result

class DLT():
    def last(self):
        url = 'http://www.lottery.gov.cn/lottery/dlt/History.aspx'
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
    print r
    numbers = r['red'] + ' + ' + r['blue']
    reply = '%s第%s期%s' % (r['publish'], r['issue'], numbers)
    print reply.decode('utf8')

