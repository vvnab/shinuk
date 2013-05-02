#  -*- coding: utf-8 -*- 

from django.db import models
from django.db.models.signals import *
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.core.exceptions import ObjectDoesNotExist
import datetime, pytils
from thumbs import ImageWithThumbsField
from django.template.defaultfilters import safe
import yaml
from django.contrib.flatpages.models import FlatPage

PRICE_INTERVALS = yaml.load(FlatPage.objects.get(url = '/').content)['price']

class Vendor(models.Model):
    name = models.CharField(u'наименование магазина', max_length = 200)
    title = models.CharField(u'наименование магазина', max_length = 200, null = True, blank = True)
    def __unicode__(self):
        return unicode(self.name)
    class Meta:
        verbose_name = u'магазин'
        verbose_name_plural = u'магазины'
        ordering = ['name',]

class Group(models.Model):
    name = models.CharField(u'наименование группы товаров EN', max_length = 200)
    name_ru = models.CharField(u'наименование группы товаров RU', max_length = 200, null = True, blank = True)
    def url(self):
        return pytils.translit.slugify(self.name)
    def __unicode__(self):
        return unicode(self.name)
    class Meta:
        verbose_name = u'группа товаров'
        verbose_name_plural = u'группы товаров'
        ordering = ['name',]

class Category(models.Model):
    name = models.CharField(u'тип товара EN', max_length = 200)
    name_ru = models.CharField(u'тип товара RU', max_length = 200, null = True, blank = True)
    group = models.ForeignKey(Group, verbose_name = u'группа товаров')
    parent = models.ForeignKey('self', verbose_name = u'родительская категория', null = True, blank = True)
    description = models.TextField(u'описание категории', null = True, blank = True)
    def url(self):
        return pytils.translit.slugify(self.name)
    def __unicode__(self):
        if self.parent:
            return u'%s → %s' % (self.parent, self.name)
        else:
            return u'%s → %s' % (self.group, self.name)
    class Meta:
        verbose_name = u'категория товаров'
        verbose_name_plural = u'категории товаров'
        ordering = ['group', 'parent__name', 'name']

class Size(models.Model):
    size = models.IntegerField(u'размер')
    size_en = models.CharField(u'размер_EN', max_length = 50)
    size_ru = models.CharField(u'размер_RU', max_length = 50, null = True, blank = True)
    def __unicode__(self):
        return u'%s - %s' % (self.size, self.size_en)
    class Meta:
        verbose_name = u'размер'
        verbose_name_plural = u'размеры'
        ordering = ['size_ru',]

class Color(models.Model):
    name = models.CharField(u'наименование цвета EN', max_length = 255, db_index = True)
    name_ru = models.CharField(u'наименование цвета RU', max_length = 255, default = '')
    base = models.CharField(u'базовый цвет', max_length = 255, default = '', db_index = True)
    rgb = models.CharField(u'HEX код', max_length = 6, default = '000000')
    def __unicode__(self):
        return unicode(self.name)
    def get_color(self):
        return '<div class="colorbox vtip" title="%s" style="background-color:%s"></div>' % (self.name, self.rgb,)
    get_color.allow_tags = True
    get_color.short_description = u'цвет'
    class Meta:
        verbose_name = u'цвет'
        verbose_name_plural = u'цвета'
        ordering = ['name_ru',]


class Brand(models.Model):
    name = models.CharField(u'имя', max_length = 50, db_index = True)
    title = models.CharField(u'заголовок', max_length = 50, null = True, blank = True)
    description = models.TextField(u'описание', null = True, blank = True)
    url = models.URLField(u'ссылка на сайт производителя', null = True, blank = True)
    def getTitle(self):
        if self.title:
            return unicode(self.title)
        else:
            return unicode(self.name)
    def get_href(self):
        if self.url: html = u'<a href="%s">&laquo;%s&raquo;</a>' % (self.url, self.name)
        else: html = unicode(u'&laquo;%s&raquo;' % self.name)
        return safe(html)
    def __unicode__(self):
        return unicode(self.name)
    class Meta:
        verbose_name = u'бренд'
        verbose_name_plural = u'бренды'
        ordering = ['name',]

class Model(models.Model):
    vendor = models.ForeignKey(Vendor, verbose_name = u'магазин')
    category = models.ManyToManyField(Category, verbose_name = u'тип товара')
    art = models.CharField(u'артикул', max_length = 200, unique = True, db_index = True)
    brand = models.ForeignKey(Brand, verbose_name = u'производитель')
    name = models.CharField(u'наименование товара', max_length = 200)
    info = models.TextField(u'информация', null = True, blank = True)
    description = models.TextField(u'описание', null = True, blank = True)
    url = models.URLField(u'ссылка на модель', verify_exists = False)
    flashurl = models.URLField(u'ссылка на flash', verify_exists = False, null = True, blank = True)
    stars = models.FloatField(u'рейтинг', default = 0)
    date_of_add = models.DateField(u'дата внесения', auto_now_add = True)
    date_of_last_change = models.DateField(u'дата последнего изменения', auto_now = True)
    def __unicode__(self):
        return u'%s | %s %s' % (self.art, self.brand.name, self.name)
    def print_stars(self):
        html = ''
        if self.stars: stars = int(round(float(self.stars) * 4))
        else: stars = 0
        for i in range(1, 21):
            if i == stars: html += '<input name="st_%s" type="radio" class="star" disabled="disabled" checked="checked"/>\n' % self.article
            else: html += '<input name="st_%s" type="radio" class="star {split:4}" disabled="disabled"/>\n' % self.article
        return safe(html)
    class Meta:
        verbose_name = u'модель'
        verbose_name_plural = u'модели'
        ordering = ['category__group', 'art', 'brand', 'name']

class Thing(models.Model):
    model = models.ForeignKey(Model, verbose_name = u'модель', db_index = True)
    color = models.ForeignKey(Color, verbose_name = u'цвет', db_index = True)
    price = models.DecimalField(u'цена', max_digits = 8, decimal_places = 2, null = True, blank = True)
    oldprice = models.DecimalField(u'начальная цена', max_digits = 8, decimal_places = 2, null = True, blank = True)
    size = models.ManyToManyField(Size, verbose_name = u'размеры', null = True, blank = True, db_index = True)
    present = models.BooleanField(u'наличие', default = True)
    def price_ru(self):
      price = float(self.price)
      _price = 0
      for i in PRICE_INTERVALS:
        if price > i[0]:
          _price = price * i[1]
      return int(_price)
    def old_price_ru(self):
      price = float(self.oldprice)
      _price = 0
      for i in PRICE_INTERVALS:
        if price > i[0]:
          _price = price * i[1]
      return int(_price)
    def __unicode__(self):
        return u'%s %s' % (self.model.name, self.color)
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'
        ordering = ['model', 'color']

class Image(models.Model):
    thing = models.ForeignKey(Thing, verbose_name = u'товар', null = True, blank = True, db_index = True)
    model = models.ForeignKey(Model, verbose_name = u'модель', null = True, blank = True, db_index = True)
    small = models.URLField(verify_exists = False)
    thumb = models.URLField(verify_exists = False)
    medium = models.URLField(verify_exists = False)
    lage = models.URLField(verify_exists = False)
    def __unicode__(self):
        if self.thing:
          return u'%s | %s' % (unicode(self.thing.model.name), unicode(self.thing.color))
        else:
          return u'%s | base' % unicode(self.model.name)
    class Meta:
        verbose_name = u'изображение товара'
        verbose_name_plural = u'изображения товаров'
        ordering = ['model', 'thing']
