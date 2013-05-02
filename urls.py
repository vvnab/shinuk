from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()
import goods.views, accounts.views

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$',  login, {'template_name': 'accounts/login.html'}),
    (r'^accounts/logout/$', logout, {'next_page': '/accounts/login/'}),
    (r'^accounts/', include('accounts.urls')),
    (r'^bag/$', goods.views.bag),
    (r'^ladmin/', include('ladmin.urls')),
    (r'^shop/', include('goods.urls')),
    (r'^order/', include('orders.urls')),
    (r'^ecommerce/', include('ecommerce.urls')),
    (r'^yml/$', goods.views.yml),
    (r'^users/$', accounts.views.users)
)
