#  -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
import views 

urlpatterns = patterns('',
    url(r'^$', views.profile),
    url(r'^register/$', views.register),
#    url(r'^register/profile/$', views.register_profile),
#    url(r'^register/address/$', views.register_address),
    url(r'^profile/$', views.profile),
    url(r'^order/(\d+)/$', views.order),
    url(r'^userexists/$', views.userexists),
    url(r'^partnership/$', views.partnership),
    url(r'^send_password/$', views.send_password),
)

