#  -*- coding: utf-8 -*- 

from goods.models import *
from django.db.models import Count
import yaml
from django.contrib.flatpages.models import FlatPage

PRICE_INTERVALS = yaml.load(FlatPage.objects.get(url = '/').content)['price']

def context(request):
    w_categorys = Category.objects.filter(group__name = 'women', parent = None).order_by('name_ru')
    m_categorys = Category.objects.filter(group__name = 'men', parent = None).order_by('name_ru')
    w_brands = Brand.objects.filter(model__category__group__name = 'women').annotate(count = Count('model')).order_by('-count')[:w_categorys.count() * 2 - 1]
    m_brands = Brand.objects.filter(model__category__group__name = 'men').annotate(count = Count('model')).order_by('-count')[:m_categorys.count() * 2 - 1]
    url = request.path.split('/')
    if len(url[1]):
        url = '/' + url[1]+'/'
    else:
        url = '/'
    return {'request': request, 'url': url, 'w_categorys': w_categorys, 'm_categorys': m_categorys, 'w_brands': w_brands, 'm_brands': m_brands, 'PRICE_INTERVALS': PRICE_INTERVALS}
