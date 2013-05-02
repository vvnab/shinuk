#  -*- coding: utf-8 -*- 

from django.db import models
import datetime
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core.mail import send_mail
from accounts.models import Address
from goods.models import Thing, Size

def sendmessage(status, order):
  if order.email:
    try:
      send_mail(status.title, status.emailmsg, 'info@shinuk.ru', [order.email])
    except ValueError:
      pass

class Delivery(models.Model):
  method = models.CharField(u'способ доставки', max_length = 255, unique = True)
  cost = models.IntegerField(u'стоимость')
  description = models.TextField(u'описание', blank = True, null = True)
  def __unicode__(self):
    return self.method
  class Meta:
    verbose_name = u'способ доставки'
    verbose_name_plural = u'способы доставки'
    ordering = ['method',]

class Pay(models.Model):
  method = models.CharField(u'способ оплаты', max_length = 255, unique = True)
  priority = models.IntegerField(u'порядок сортировки', default = 0)
  nick = models.CharField(u'имя (nickname)', max_length = 255, unique = True)
  cost = models.IntegerField(u'комиссия', default = 0)
  description = models.TextField(u'описание', blank = True, null = True)
  available = models.BooleanField(u'доступен', default = False)
  def __unicode__(self):
    return u'%s : %s' % (self.available, self.nick)
  class Meta:
    verbose_name = u'способ оплаты'
    verbose_name_plural = u'способы оплаты'
    ordering = ['priority',]

class ParcelStatus(models.Model):
  title = models.CharField(u'наименование', max_length = 255)
  sendmessage = models.BooleanField(u'отправлять ли уведомление', default = False, blank = True)
  emailmsg = models.TextField(u'текст почтового уведомления', blank = True, null = True)
  smsmsg = models.TextField(u'текст SMS уведомления', blank = True, null = True)
  def __unicode__(self):
    return u'%s' % self.title
  class Meta:
    verbose_name = u'статус отправления'
    verbose_name_plural = u'статусы отправлений'

class ParcelStatusList(models.Model):
  parcel = models.ForeignKey('Parcel', verbose_name = u'отправление')
  status = models.ForeignKey('ParcelStatus', verbose_name = u'статус')
  datetime = models.DateTimeField(u'дата/время формирования', auto_now_add = True)
  def __unicode__(self):
    return u'%s::%s::%s' % (self.order, self.status, self.datetime.strftime('%Y.%m.%d %H:%M'))
  class Meta:
    verbose_name = u'список статусов отправления'
    verbose_name_plural = u'списки статусов отправлений'
    ordering = ['parcel',]

class Parcel(models.Model):
  code = models.CharField(u'код отправления', max_length = 20, unique = True)
  status = models.ForeignKey('ParcelStatusList', verbose_name = u'список статусов отправления', related_name = 'statuslist_set', blank = True, null = True)
  def __unicode__(self):
    return u'%s' % self.code
  class Meta:
    verbose_name = u'отправление'
    verbose_name_plural = u'отправления'

class OrderStatus(models.Model):
  title = models.CharField(u'наименование', max_length = 255)
  sendmessage = models.BooleanField(u'отправлять ли уведомление', default = False, blank = True)
  emailmsg = models.TextField(u'текст почтового уведомления', blank = True, null = True)
  smsmsg = models.TextField(u'текст SMS уведомления', blank = True, null = True)
  def __unicode__(self):
    return u'%s' % self.title
  class Meta:
    verbose_name = u'статус заказа'
    verbose_name_plural = u'статусы заказов'

class OrderStatusList(models.Model):
  order = models.ForeignKey('Order', verbose_name = u'заказ')
  status = models.ForeignKey('OrderStatus', verbose_name = u'статус')
  datetime = models.DateTimeField(u'дата/время формирования', auto_now_add = True)
  def __unicode__(self):
    return u'%s::%s::%s' % (self.order, self.status, self.datetime.strftime('%Y.%m.%d %H:%M'))
  class Meta:
    verbose_name = u'список статусов заказа'
    verbose_name_plural = u'списки статусов заказов'
    ordering = ['order', 'datetime']

class Order(models.Model):
  user = models.ForeignKey(User, verbose_name = u'пользователь')
  address = models.ForeignKey(Address, verbose_name = u'адрес доставки')
  parcel = models.ForeignKey('Parcel', verbose_name = u'отправление', blank = True, null = True)
  delivery = models.ForeignKey('Delivery', verbose_name = u'способ доставки')
  deliverycost = models.IntegerField(u'стоимость доставки', null = True, blank = True)
  totalcost = models.IntegerField(u'общая стоимость отправления', null = True, blank = True)
  datetime = models.DateTimeField(u'дата/время формирования', auto_now_add = True)
  pay = models.ForeignKey('Pay', verbose_name = u'способ оплаты')
  status = models.ForeignKey('OrderStatusList', verbose_name = u'статус заказа', related_name = 'statuslist_set', blank = True, null = True)
  text = models.TextField(u'комментарии к заказу', blank = True, null = True)
  info = models.TextField(u'дополнительная информация', blank = True, null = True)
  desc = models.CharField(u'описание', max_length = 50, default = u'Order from ShinUK.ru')
  def parcelcost(self):
    return int(self.totalcost) - int(self.deliverycost)
  def ordernum(self):
    return str(self.id).zfill(9)
  def __unicode__(self):
    return u'№ %s | %s  | %s руб. | %s' % (self.id, self.status.status, self.totalcost, self.user)
  class Meta:
    verbose_name = u'заказ'
    verbose_name_plural = u'заказы'
    ordering = ['id',]


class OrderItem(models.Model):
  order = models.ForeignKey(Order, verbose_name = u'заказ')
  thing = models.ForeignKey(Thing, verbose_name = u'элемент заказа')
  size = models.ForeignKey(Size, verbose_name = u'размер вещи')
  quantity = models.IntegerField(u'кол-во в заказе', default = 1)
  price = models.IntegerField(u'цена', null = True, blank = True)
  def cost(self):
    return self.price * self.quantity
  def __unicode__(self):
    return u'%s:%s %s (%s) [%s шт.] - %s р.' % (self.order.id, self.thing.model.art, self.thing.color.name_ru, self.size.size_ru, self.quantity, self.cost())
  class Meta:
    verbose_name = u'элемент заказа'
    verbose_name_plural = u'элементы заказа'
    ordering = ['order',]

class PromoCode(models.Model):
  code = models.CharField(u'код', max_length = 10)
  discount = models.IntegerField(u'скидка', default = 5)
  start = models.DateField(u'дата начала акции')
  expire = models.DateField(u'дата окончания')
  active = models.BooleanField(u'активен', default = True)
  def __unicode__(self):
    return '%s::%s::%s' % (self.code, self.discount, self.expire)
  class Meta:
    verbose_name = u'код промоакции'
    verbose_name_plural = u'коды промоакций'

class DiscountCode(models.Model):
  code = models.CharField(u'код', max_length = 10)
  discount = models.IntegerField(u'скидка', default = 5)
  start = models.DateField(u'дата создания')
  expire = models.DateField(u'дата окончания')
  active = models.BooleanField(u'активен', default = True)
  order = models.ForeignKey(Order, verbose_name = u'заказ')
  def __unicode__(self):
    return '%s::%s::%s' % (self.code, self.discount, self.start)
  class Meta:
    verbose_name = u'код скидки'
    verbose_name_plural = u'коды скидок'
