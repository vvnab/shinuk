#  -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
import views 

urlpatterns = patterns('',
    url(r'^checkout/$', views.checkout),
    url(r'^pay/$', views.pay),
    url(r'^complete/$', views.complete),
    url(r'^qiwi/success/$', views.complete),
    url(r'^promocode/$', views.promocode)
)

