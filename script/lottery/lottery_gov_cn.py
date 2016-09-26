#coding:utf8
import lottery_gov_cn_dlthistory_aspx
import lottery_gov_cn_historykj_history_jspx
class DLT():
    def last(self):
        r = lottery_gov_cn_historykj_history_jspx.DLT().last()
        if r != None:
            return r
        r = lottery_gov_cn_dlthistory_aspx.DLT().last()
        return r

if __name__ == '__main__':
    r = DLT().last()
    print r
    numbers = r['red'] + ' + ' + r['blue']
    reply = '%s第%s期%s' % (r['publish'], r['issue'], numbers)
    print reply.decode('utf8')
