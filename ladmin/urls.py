#  -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
import views 

urlpatterns = patterns('',
    url(r'^$', views.main),
    url(r'^search/$', views.search),
    url(r'^goods_add/$', views.goods_add),
    url(r'^model_fetch/$', views.fetch),
    url(r'^get_categorys/$', views.get_categorys),
    url(r'^orders/$', views.orders),
    url(r'^order/(\d+)/$', views.order),
    url(r'^order/delete/$', views.order_delete),
    url(r'^users/$', views.users),
    url(r'^email/$', views.email),
)