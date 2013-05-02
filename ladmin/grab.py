#  -*- coding: utf-8 -*- 

#from scrapy.selector import HtmlXPathSelector
from pyquery import PyQuery as pq
from django.contrib.flatpages.models import FlatPage
import re, yaml, logging
from datetime import datetime

logger = logging.getLogger('logger')

class DoesNotExist(Exception):
  def __init__(self, val):
    self.val = val
  def __str__(self):
    return self.val

class Asos:
  def __init__(self, url):
    d = pq(url)
    
    self.vendor = u'asos'
    self.group = d('meta[name="DCSext.pg_n"]').attr('content')
    self.category = d('meta[name="DCSext.pg_s"]').attr('content')
    self.subcategory = d('meta[name="DCSext.cg_sec"]').attr('content')
    self.brand = d('meta[name="DCSext.brand"]').attr('content')
    self.url = d('link[rel="canonical"]').attr('href')
    if self.url:
      self.art = re.findall('iid=(\d*)', self.url)
    else:
      self.art = None
    if self.art:
        self.art = self.art[0]
    else:
      raise DoesNotExist('Not Exist')

    self.name = d('#ctl00_ContentMainPage_ctlSeparateProduct_lblProductTitle').text()
    self.name = re.sub('mp_trans_seo_url_title_start|mp_trans_seo_url_title_end', '', self.name)
    self.description = d('#ctl00_ContentMainPage_ctlSeparateProduct_divInvLongDescription').text()
    self.info = self.get_info('%s \n %s' % (d('#ctl00_ContentMainPage_lblAdditionalInfo').html(), d('#ctl00_ContentMainPage_lblCareInfo').html()))
    script1 = d('body form script').eq(1).text()
    script2 = d('body form script').eq(2).text()
    script3 = d('body form script').eq(3).text()
    ritems = re.findall(r'new Array\((.+)\)', script1)
    self.flashurl = d('#VideoPath').attr('value')
    if self.flashurl == '/Video/blank.swf' or not self.flashurl:
      self.flashurl = None

    items = {}

    for i in ritems:
      params = i.split(',')
      size = int(params[0])
      size_en = re.sub('^"|"$', '', params[1])
      color = re.sub('^"|"$', '', params[2]).lower()
      present = re.sub('^"|"$', '', params[3])
      if present == 'True': 
        present = True
      else:
        present = False
      price = float(re.sub(u'^"|\xa3|"$', '', params[5]))
      oldprice = float(re.sub(u'^"|\xa3|"$', '', params[8]))
      if oldprice == 0:
        oldprice = float(re.sub(u'^"|\xa3|"$', '', params[6]))
      try:
        items[color].append({'size': size, 'size_en': size_en, 'size_ru': '', 'present': present, 'price': price, 'oldprice': oldprice})
      except KeyError:
        items[color] = [{'size': size, 'size_en': size_en, 'size_ru': '', 'present': present, 'price': price, 'oldprice': oldprice}]

#    self.items = items

    rimages_color = re.findall(r'arrSepImage_ctl00_ContentMainPage_ctlSeparateProduct\[\d+\] = new Array(\(.+)\)', script2)
    rimages_all = re.findall(r'arrThumbImage_ctl00_ContentMainPage_ctlSeparateProduct\[\d+\] = new Array(\(.+)\)', script3)
    images = {}

    for i in rimages_color:
      params = i.split(',')
      color = re.sub('^"|"$', '', params[3].strip()).lower()
      
      keys = items.keys()
      for key in keys:
        match = re.match(key, color)
        if match:
          if match.group(0) != color:
            val = items.pop(key)
            items.update({color: val})
      
      small = re.sub('^\("|"$', '', params[0].strip())
      medium = re.sub('^"|"$', '', params[1].strip())
      lage = re.sub('^"|"$', '', params[2].strip())
      thumb = re.sub('1xl.jpg', '1l.jpg', medium)
      try:
        images[color].update({'small': small, 'medium': medium, 'lage': lage, 'thumb': thumb})
      except KeyError:
        images[color.lower()] = {'small': small, 'medium': medium, 'lage': lage, 'thumb': thumb}
    for i in rimages_all:
      params = i.split(',')
      small = re.sub('^\("|"$', '', params[0].strip())
      medium = re.sub('^"|"$', '', params[1].strip())
      lage = re.sub('^"|"$', '', params[2].strip())
      thumb = re.sub('1xl.jpg', '1l.jpg', medium)
      try:
        images['all'].append({'small': small, 'medium': medium, 'lage': lage, 'thumb': thumb})
      except KeyError:
        images['all'] = [{'small': small, 'medium': medium, 'lage': lage, 'thumb': thumb}]
    self.images = images
    self.items = items
      
  def get(self):
    obj = {}
    obj['vendor'] = self.vendor
    obj['url'] = self.url
    obj['group'] = self.group
    obj['category'] = self.category
    obj['subcategory'] = self.subcategory
    obj['brand'] = self.brand
    obj['art'] = self.art
    obj['name'] = self.name
    obj['description'] = self.description
    obj['flashurl'] = self.flashurl
    obj['info'] = self.info
    obj['items'] = self.items
    obj['images'] = self.images
    return obj

  def get_info(self, html):
    html = re.sub('<span class="product">', '', html)
    html = re.sub('<span class="care">', '', html)
    html = re.sub('</span>', '\n', html)
    html = re.sub('<strong>', '', html)
    html = re.sub('</strong>', '\n', html)
    html = re.sub('<br />', '', html)
    html = re.sub('<br/>', '', html)
    html = re.sub('ABOUT ME', u'СОСТАВ', html)
    html = re.sub('SIZE &amp; FIT\n', u'\n\nРАЗМЕР МОДЕЛИ НА ФОТО', html)
    html = re.sub('LOOK AFTER ME', u'\nУХОД', html)

    html = re.sub('Shell', u'Верх', html)
    html = re.sub('Main', u'Верх', html)
    html = re.sub('Upper', u'Верх', html)
    html = re.sub('Outer', u'Верх', html)
    html = re.sub('Trim', u'Отделка', html)
    html = re.sub('Height', u'Высота', html)
    html = re.sub('Width', u'Ширина', html)
    html = re.sub('Depth', u'Глубина', html)
    html = re.sub('Inner', u'Стелька', html)
    html = re.sub('Sole', u'Подошва', html)
    html = re.sub('Textile', u'текстиль', html)
    html = re.sub('Rubber', u'резина', html)
    html = re.sub('Backing', u'Основа', html)
    html = re.sub('Lining', u'Подклад', html)
    html = re.sub('Polyurethane', u'полиуретан', html)
    html = re.sub('Polyester', u'полиэстер', html)
    html = re.sub('Cotton', u'хлопок', html)
    html = re.sub('Viscose', u'вискоза', html)
    html = re.sub('Silk', u'шёлк', html)
    html = re.sub('Leather', u'кожа', html)
    html = re.sub('Acrylic', u'акрил', html)
    html = re.sub('Nylon', u'нейлон', html)
    html = re.sub('Wool', u'шерсть', html)
    html = re.sub('Linen', u'лён', html)
    html = re.sub('Polyamide', u'полиамид', html)
    html = re.sub('Specialist clean only', u'только химчистка', html)
    html = re.sub('Sleeve Lining', u'Подклад рукавов', html)
    html = re.sub('Sleeve lining', u'Подклад рукавов', html)
    html = re.sub('Dry clean', u'сухая чистка', html)
    html = re.sub('Dry clean only', u'Только сухая чистка', html)
    html = re.sub('Hand wash only', u'Только ручная стирка', html)
    html = re.sub('40 degree Machine Wash', u'Машинная стирка при 40º', html)
    html = re.sub('40 degree machine wash', u'Машинная стирка при 40º', html)
    html = re.sub('Machine wash at 40 degrees', u'Машинная стирка при 40º', html)
    html = re.sub('Hand wash', u'Ручная стирка', html)
    html = re.sub('Elastane', u'эластан', html)
    html = re.sub('Model wears', u'Размер модели', html)
    html = re.sub('Model\'s height', u'Рост модели', html)
    html = re.sub('To maintain appearance &amp; condition avoid contact with liquid &amp; perfume', u'Чтобы сохранить внешний вид и состояние, избегать контакта с жидкостью и духами.', html)
    html = re.sub('To maintain appearance and condition, avoid contact with liquid and perfume', u'Чтобы сохранить внешний вид и состояние, избегать контакта с жидкостью и духами.', html)
    html = re.sub('To maintain appearance and condition avoid contact with liquids and perfume', u'Чтобы сохранить внешний вид и состояние, избегать контакта с жидкостью и духами.', html)
    html = re.sub('To maintain appearance and condition, avoid contact with liquids or perfume', u'Чтобы сохранить внешний вид и состояние, избегать контакта с жидкостью и духами.', html)
    html = re.sub('To maintain appearance and condition, avoid contact with liquids and perfume', u'Чтобы сохранить внешний вид и состояние, избегать контакта с жидкостью и духами.', html)
    html = re.sub('Base metal', u'металл', html)
    html = re.sub('Base Metal', u'металл', html)
    html = re.sub('To maintain appearance and condition, remove light marks with a clean damp sponge', u'Чтобы сохранить внешний вид и состояние - протирать влажной губкой', html)
    html = re.sub('Wipe with a damp cloth or sponge', u'Протирать влажной тканью или губкой', html)
    html = re.sub('To maintain appearance, wipe clean with a damp cloth', u'Чтобы сохранить внешний вид и состояние - протирать влажной губкой', html)
    html = re.sub('To remove any marks we recommend cleaning with a clean damp cloth', u'Чтобы сохранить внешний вид и состояние - протирать влажной губкой', html)
    html = re.sub('To maintain appearance we recommend treating with a suitable leather protector', u'Чтобы сохранить внешний вид рекомендуется обрабатывать подходящим защитным средством для кожи', html)
    html = re.sub('To maintain appearance and condition, treat with a suitable leather protector', u'Чтобы сохранить внешний вид рекомендуется обрабатывать подходящим защитным средством для кожи', html)
    html = re.sub('Wipe clean with a damp cloth or sponge', u'Протирать влажной тканью или губкой', html)
    html = re.sub('To maintain appearance and condition, wipe light marks with a damp cloth', u'Для поддержания внешнего вида и состояния, протирать влажной тканью', html)
    html = re.sub('To remove light marks wipe with a clean damp cloth', u'Чтобы удалить загрязнения, протрите чистой влажной тканью', html)
    html = re.sub('Machine wash according to instructions on care label', u'Машинная стирка в соответствии с инструкциями на этикетке', html)
    html = re.sub('Avoid contact with liquids', u'Избегать контакта с жидкостями', html)
    html = re.sub('avoid contact with liquids', u'Избегать контакта с жидкостями', html)
    html = re.sub("Model's chest", u'Обхват груди модели', html)
    html = re.sub("model's chest", u'Обхват груди модели', html)
    html = re.sub("Model is wearing", u'Размер модели', html)
    html = re.sub("model is wearing", u'Размер модели', html)
    html = re.sub("Model wearing", u'Размер модели', html)
    html = re.sub("model wearing", u'Размер модели', html)
    html = re.sub(" cm ", u' см ', html)
    html = re.sub("Wipe clean with a damp cloth", u'Протирать влажной тканью', html)
    html = re.sub("wipe clean with a damp cloth", u'Протирать влажной тканью', html)
    html = re.sub("Size UK 8/ EU 36/ US 4 side neck to hem measures", u'Размеру 42 соответствует длина', html)
    html = re.sub("size UK 8/ EU 36/ US 4 side neck to hem measures", u'Размеру 42 соответствует длина', html)
    html = re.sub("Wipe light marks with a soft cloth", u'Протирать мягкой тканью', html)
    html = re.sub("wipe light marks with a soft cloth", u'Протирать мягкой тканью', html)
    html = re.sub("To maintain appearance and condition treat with a suitable leather protector", u'Чтобы сохранить внешний вид - использовать специальные средства по уходу за кожей', html)
    html = re.sub("to maintain appearance and condition treat with a suitable leather protector", u'Чтобы сохранить внешний вид - использовать специальные средства по уходу за кожей', html)
    html = re.sub('UK 8/ EU 36/ US 4 side neck to hem measures', u'Размеру 42 соответствует длина', html)
    html = re.sub('Polyvinylchloride', u'поливинилхлорид', html)
    html = re.sub('polyvinylchloride', u'поливинилхлорид', html)
    html = re.sub('Modacrylic', u'модакрил', html)
    
    try:
      replace = yaml.load(FlatPage.objects.get(url = '/').content)['replace']
    except:
      replace = ''
    if replace:
      for i in replace:
        try:
          html = re.sub(r'(?i){0}'.format(i[0]), u'{0}'.format(i[1]), html)
        except:
          pass

    return html
