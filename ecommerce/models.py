#  -*- coding: utf-8 -*- 

from django.db import models
from orders.models import Order

class ResponseRequest(models.Model):
  order = models.ForeignKey(Order, verbose_name = u'заказ')
  datetime = models.DateTimeField(u'дата/время формирования', auto_now_add = True)
  rc = models.CharField(u'код ответа', max_length = 3, blank = True, null = True)
  aproval = models.CharField(u'код подтверждения банка', max_length = 6, blank = True, null = True)
  rrn = models.CharField(u'RRN', max_length = 12, blank = True, null = True)
  int_ref = models.CharField(u'IRN', max_length = 32, blank = True, null = True)
  def __unicode__(self):
    return u'%s::%s::%s::%s' % (self.rc, self.rrn, self.int_ref, self.datetime.strftime('%Y.%m.%d %H:%M'))
  class Meta:
    verbose_name = u'ответ'
    verbose_name_plural = u'ответы'
    ordering = ['order', 'datetime']
  

