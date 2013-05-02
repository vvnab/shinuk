#  -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
import views 

urlpatterns = patterns('',
    url(r'^get_goods/$', views.get_goods),
    url(r'^get_goods2/$', views.get_goods2),
    url(r'^$', views.goods_view),
    url(r'^model/(\w+)/$', views.model_view),
    url(r'^brand/(men|women|all)/$', views.all_brand),
    url(r'^brand/([\'\’\w&\.\- ]+)/(\w+)/$', views.brand_view),
    url(r'^(\w+)/$', views.group_view),
    url(r'^(\w+)/([\'\w&\- ]+)/$', views.category_view, {'subcategory': None}),
    url(r'^(\w+)/([\'\w&\- ]+)/([\'\w&\- ]+)/$', views.category_view),
)

