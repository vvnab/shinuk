#  -*- coding: utf-8 -*- 

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField


class Profile(models.Model):
  GENDER_CHOICES = (
    ('men', 'мужской'),
    ('women', 'женский'),
  )
  user = models.ForeignKey(User, verbose_name = u'пользователь', unique = True)
  middlename = models.CharField(u'отчество', max_length = 255, blank = True, null = True)
  gender = models.CharField(u'пол', max_length = 5, choices = GENDER_CHOICES)
  phone = models.CharField(u'номер телефона', max_length = 17, null = True, blank = True)
  deposit = models.IntegerField(u'сумма депозита', default = 0)
  invite = models.ForeignKey(User, verbose_name = u'пригласивший', related_name = 'invite_set', null = True, blank = True)
  def __unicode__(self):
    return unicode(self.user)
  def get_full_name(self):
    return u'%s %s %s' % (self.user.last_name, self.user.first_name, self.middlename)
  class Meta:
    verbose_name = u'дополнительные данные пользователя'
    verbose_name_plural = u'дополнительные данные пользователей'

class Address(models.Model):
  user = models.ForeignKey(User, verbose_name = u'пользователь', blank = True, null = True)
  default = models.BooleanField(u'адрес по умолчанию', default = True)
  zip = models.CharField(u'почтовый индекс', max_length = 6, blank = True, null = True)
  subject = models.CharField(u'регион', max_length = 255, blank = True, null = True)
  county = models.CharField(u'район', max_length = 255, blank = True, null = True)
  city = models.CharField(u'нас. пункт', max_length = 255, blank = True, null = True)
  place = models.CharField(u'место', max_length = 255, blank = True, null = True)
  street = models.CharField(u'улица', max_length = 255, blank = True, null = True)
  house = models.CharField(u'дом', max_length = 255, blank = True, null = True)
  flat = models.CharField(u'квартира', max_length = 255, blank = True, null = True)
  def __unicode__(self):
    adr = u'%s' % self.subject
    if self.county: adr += u', %s' % self.county
    if self.city: adr += u', %s' % self.city
    if self.place: adr += u', %s' % self.place
    if self.street: adr += u', %s' % self.street
    if self.house: adr += u', дом %s' % self.house
    if self.flat: adr += u', кв %s' % self.flat
    return adr
  def getadds(self):
    adr = u'%s' % self.subject
    if self.county: adr += u', %s' % self.county
    if self.city: adr += u', %s' % self.city
    if self.place: adr += u', %s' % self.place
    if self.street: adr += u', %s' % self.street
    if self.house: adr += u', дом %s' % self.house
    if self.flat: adr += u', кв %s' % self.flat
    return adr
  class Meta:
    verbose_name = u'адрес'
    verbose_name_plural = u'адреса'

class Partner(models.Model):
  user = models.ForeignKey(User, verbose_name = u'пользователь', unique = True)
  key = models.CharField(u'ключ', max_length = 255, unique = True)
  count = models.IntegerField(u'кол-во приглашённых', default = 0)
  def __unicode__(self):
    return unicode(self.user)
  class Meta:
    verbose_name = u'данные партнёра'
    verbose_name_plural = u'данные партнёров'

class Message(models.Model):
    TARGET_CHOICES = (
    ('reg', u'Регистрация'),
    ('chp', u'Смена пароля'),
    ('chk', u'Размещение заказа'),
    ('pay', u'Оплата заказа'),
    ('can', u'Отмена заказа'),
    ('shp', u'Отправка заказа'),
    )
    target = models.CharField(u'событие', max_length = 3, choices = TARGET_CHOICES, unique = True)
    subject = models.CharField(u'тема письма', max_length = 255)
    mail = models.TextField(u'текст письма', help_text = 'В тексте можно использовать переменные. <a class="popuhelp">?</a>')
    sms = models.TextField(u'текст смс', help_text = 'В тексте можно использовать переменные. <a class="popuhelp">?</a>')
    def __unicode__(self):
        return unicode(self.subject)
    class Meta:
        verbose_name = u'сообщение'
        verbose_name_plural = u'сообщения'
