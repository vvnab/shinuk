#  -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
import views 

urlpatterns = patterns('',
    url(r'^auth/$', views.auth),
    url(r'^reply/$', views.reply),
    url(r'^backref/$', views.backref),
    url(r'^callback/$', views.reply),
)

