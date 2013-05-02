# -*- coding: utf-8 -*-

from mechanize import Browser
from lxml.html import fromstring
import simplejson as json, re, urllib2
 
class StatusError(Exception):
    pass

class Status:
    status = []
    start_url = 'http://www.russianpost.ru/rp/servise/ru/home/postuslug/trackingpo'
    form_name = 'F1'
    headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/20.0.1131.0 Safari/537.1')]
    bar_code = ''
    error = False
    html = u''
    def get_status(self):
        return self.status
    def set_status(self, barCode = ''):
        self.status = []
        self.bar_code = barCode
        br = Browser()
        br.addheaders = self.headers
        br.set_handle_robots(False)
        try:
            br.open(self.start_url)
        except urllib2.URLError, e:
            self.error = True
            self.html = u'ОШИБКА<br/>Соединение с сервисом сброшено. <br/>%s' % e
            return

        try:
          br.select_form(name = 'myform')
          br.submit()
        except:
          pass
        br.select_form(name = self.form_name)
        br.set_all_readonly(False)
        br['BarCode'] = self.bar_code
        br['searchsign'] = '1'
        page = br.submit()
        page = page.read()
        page = page.decode('utf-8')
        if (re.search(r'page_ERROR', page)):
            self.error = True
            self.html = u'ОШИБКА<br/>Почтовый идентификатор неправильного формата.'
        if (re.search(ur'не найдена', page)):
            self.error = True
            self.html = u'К сожалению, информация о почтовом отправлении с данным номером не найдена.'
        result = fromstring(page)
        trs = result.xpath('//body//table[4]/tbody/tr')
        for tr in trs:
            td = tr.xpath('td')
            for t in td:
              if t.text == None:
                t.text = ''
            operation, date, index1, OPC, attr, weight, price, cost, index2, address = td
            self.status.append({
                           'operation': operation.text,
                           'date': date.text,
                           'index1': index1.text,
                           'OPC': OPC.text,
                           'attr': attr.text,
                           'weight': weight.text,
                           'price': price.text,
                           'cost': cost.text,
                           'index2': index2.text,
                           'address': address.text
                           }) 
        for s in self.status:
            self.html += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (unicode(s['operation']), unicode(s['date']), unicode(s['index1']), unicode(s['OPC']), unicode(s['attr']))
    def __init__(self, barCode = ''):
        self.set_status(barCode)
    def __repr__(self):
        return self.get_status()
    def __getitem__(self, i):
        return self.status[i]
    def __str__(self):
        ss = ''
        for s in self.get_status():
            ss += unicode(s)
        return ss
    def get_json(self):
        if self.error:
            return json.dumps({'status': 'error', 'desc': self.html}, ensure_ascii = False)
        else:
            return json.dumps({'status': 'ok', 'list': self.status}, ensure_ascii = False)
    def get_html(self):
        return self.html
        