#  -*- coding: utf-8 -*- 

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.log import ERROR
# from scrapy.selector import HtmlXPathSelector

import psycopg2, re
from models import Asos, DoesNotExist
from shinuk_update.items import ShinukUpdateItem

class AsosSpider(BaseSpider):
  name = "asos.com"
  allowed_domains = ["asos.com"]
  start_urls = []
  goods = {}
  def __init__(self, *args, **kwargs):
    conn = psycopg2.connect('dbname=shinuk user=shinuk')
    cur = conn.cursor()
    cur.execute("SELECT * FROM goods_model;")
    for rec in cur:
      url = str(rec[7])
      art = str(rec[2])
      pk = str(rec[0])
      self.start_urls.append(url)
      self.goods.update({art: pk})
    cur.close()
    conn.close()
    super(BaseSpider, self).__init__()

  def make_requests_from_url(self, url):
    return Request(url = url, cookies = {'asos': 'currencyid=1'}, callback = self.parse)

  def parse(self, response):
    item = ShinukUpdateItem()
    try:
      i = Asos(response)
    except DoesNotExist:
      url = response.meta['redirect_urls'][0]
      art = re.findall('iid=(\d*)', url)[0]
      item['art'] = art
      item['pk'] = self.goods[art]
      item['name'] = None
      return item
    i = i.get()
    item['name'] = i['name']
    item['items'] = i['items']
    item['art'] = i['art']
    item['pk'] = self.goods[i['art']]
    return item
