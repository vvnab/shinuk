#  -*- coding: utf-8 -*- 

from models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext, Context
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Max, Min, Q
from django.utils import simplejson as json
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from decimal import *
import re, urllib
from templatetags.ssort import cmp_size
from datetime import datetime
from lxml import etree

#@login_required
def bag(request):
  try:
    bag = json.loads(urllib.unquote(request.COOKIES.get('bag', '[]')))
  except Exception:
    bag = ''
  try:
    wishList = json.loads(urllib.unquote(request.COOKIES.get('wishList', '[]')))
    for k, i in wishList.items():
      model = Model.objects.get(art = i['art'])
      i['name'] = model.name
  except Exception:
    wishList = ''
  return render_to_response('shop/bag.html', locals(), context_instance = RequestContext(request))

def goods_view(request):
  models = Model.objects.select_related().distinct()
  return render_to_response('shop/all.html', locals(), context_instance = RequestContext(request))

def group_view(request, group):
  group = get_object_or_404(Group, name = group)
  return render_to_response('shop/group.html', locals(), context_instance = RequestContext(request))

def all_brand(request, group):
  if group != 'all':
    group = get_object_or_404(Group, name = group)
    brands = Brand.objects.filter(model__category__group = group).distinct().order_by('name')
  else:
    brands = Brand.objects.filter(model__thing__present = True).distinct().order_by('name')
  groups = Group.objects.select_related().order_by('-name')
  return render_to_response('shop/brands.html', locals(), context_instance = RequestContext(request))

def brand_view(request, brand, group):
  brand = get_object_or_404(Brand, name = brand)
  group = get_object_or_404(Group, name = group)
  things = Thing.objects.filter(model__brand = brand, model__category__group = group, present = True).distinct().order_by()
  subcategorys = Category.objects.filter(model__thing__in = things).distinct()
  groups = Group.objects.exclude(id = group.id).filter(category__model__brand = brand).distinct()

  if things.count(): 
    price_max = {'ru': things.order_by('-price')[0].price_ru(), 'en': things.order_by('-price')[0].price}
    price_min = {'ru': things.order_by('price')[0].price_ru(), 'en': things.order_by('price')[0].price}
    sizes = list(Size.objects.filter(thing__in = things).values('size_ru').distinct().annotate(size = Max('size')))
    sizes = sorted(sizes, cmp = cmp_size)
    brands = Brand.objects.filter(model__thing__in = things).values('name').distinct()
    colors = Color.objects.filter(thing__in = things).values('base').order_by('base').distinct()
  else:
    price_max = {'ru': 0, 'en': 0}
    price_min = {'ru': 0, 'en': 0}
  return render_to_response('shop/brand.html', locals(), context_instance = RequestContext(request))

def category_view(request, group, category, subcategory):
  group = get_object_or_404(Group, name = group)
  category = get_object_or_404(Category, group = group, parent = None, name = category)
  if (subcategory):
    subcategory = get_object_or_404(Category, parent = category, name = subcategory)
    query = Q(model__category = subcategory, size__gt = 0)
    things = Thing.objects.filter(query).distinct().order_by()
    subcategorys = Category.objects.filter(parent = category, model__thing__in = things).exclude(name = subcategory.name).distinct()
  else:
    subcategorys = Category.objects.filter(parent = category).distinct()
    query = Q(model__category = category, size__gt = 0) | Q(model__category__parent = category, size__gt = 0)
    things = Thing.objects.filter(query).distinct().order_by()
  if things.count(): 
    price_max = {'ru': things.order_by('-price')[0].price_ru(), 'en': things.order_by('-price')[0].price}
    price_min = {'ru': things.order_by('price')[0].price_ru(), 'en': things.order_by('price')[0].price}
    sizes = list(Size.objects.filter(thing__in = things).values('size_ru').distinct().annotate(size = Max('size')))
    sizes = sorted(sizes, cmp = cmp_size)
    brands = Brand.objects.filter(model__thing__in = things).values('name', 'id').distinct().order_by('name')
    colors = Color.objects.filter(thing__in = things).values('base').distinct().order_by('base')
  else:
    price_max = {'ru': 0, 'en': 0}
    price_min = {'ru': 0, 'en': 0}
  return render_to_response('shop/list.html', locals(), context_instance = RequestContext(request))

def model_view(request, art):
  sPage = int(request.GET.get('page', 0))
  things = Thing.objects.filter(model__art = art, size__gt = 0).distinct().order_by()
  if len(things) == 0:
    things = Thing.objects.filter(model__art = art).distinct().order_by()
    if len(things) == 0: raise Http404 
    model = things[0].model
    category = model.category.all()
    sex = model.category.all()[0].group.name
    sizeguide = FlatPage.objects.get(url='/info/sizeguide/%s/' % sex)
    model_not_exist = True
    return render_to_response('shop/model.html', locals(), context_instance = RequestContext(request))
  model = things[0].model
  category = model.category.all()
  sex = model.category.all()[0].group.name
  sizeguide = FlatPage.objects.get(url='/info/sizeguide/%s/' % sex)
  return render_to_response('shop/model.html', locals(), context_instance = RequestContext(request))

def get_goods(request):
  position = int(request.GET.get('position', 0))
  page = int(request.GET.get('page', 0))
  group = request.GET.get('group', None)
  category = request.GET.get('category', None)
  category = re.sub('&amp;', '&', category)
  subcategory = request.GET.get('subcategory', None)
  subcategory = re.sub('&amp;', '&', subcategory)

  fSort = request.GET.get('fSort')

  if (fSort == 'new'):
    fSort = '-date_of_add'
  elif (fSort == 'up'):
    fSort = '-thing__price'
  elif (fSort == 'down'):
    fSort = 'thing__price'
  else:
    fSort = '-date_of_add'

  query = Q(thing__present = True)

  fSubcategory = request.GET.getlist('fSubcategory[]')
  if fSubcategory: 
    query = query & Q(category__id__in = fSubcategory)

  fBrand = request.GET.getlist('fBrand[]')
  if fBrand:
    query = query & Q(brand__id__in = fBrand)

  fSize = request.GET.getlist('fSize[]')
  if fSize:
    size = []
    for s in fSize:
      size_ru = get_object_or_404(Size, size = s)
      size.append(size_ru.size_ru)
    query = query & Q(thing__size__size_ru__in = size)

  fColor = request.GET.getlist('fColor[]')
  if fColor:
    query = query & Q(thing__color__base__in = fColor)

  fPrice = request.GET.getlist('fPrice[]')
  if fPrice:
    query = query & Q(thing__price__gte = fPrice[0], thing__price__lte = fPrice[1])

  if (subcategory):
    category = get_object_or_404(Category, group__name = group, name = category)
    subcategory = get_object_or_404(Category, parent = category, name = subcategory)
    if not fSubcategory:
      query = query & Q(category = subcategory)
      models = Model.objects.filter(query).distinct().order_by(fSort)
    if fSubcategory:
      models = Model.objects.filter(query)
      models = models.filter(category = subcategory).distinct().order_by(fSort)
  elif (category):
    category = get_object_or_404(Category, group__name = group, name = category)
    query = query & (Q(category__parent = category) | Q(category = category))
    models = Model.objects.filter(query).distinct().order_by(fSort)
  elif (group):
    query = query & Q(category__group__name = group)
    models = Model.objects.filter(query).distinct().order_by(fSort)
  else:
    models = Model.objects.filter(query).distinct().order_by(fSort)
  quantity = models.count()
  models = models[position:position + page]
  goods = {'count': quantity, 'items': []}

  for m in models:
    things = Thing.objects.filter(model = m, present = True).distinct().order_by('color__name_ru')
    if not things: continue
    colors = things.values_list('color__name_ru', 'color__rgb').distinct().order_by('color__name_ru')
    good = {'name': m.name}
    imgs = []
    for t in things:
      try:
        imgs.append(t.image_set.all()[0].thumb)
      except IndexError:
        pass
    price = int(things[0].price_ru())
    oldprice = int(things[0].old_price_ru())
    good.update({'imgs': list(imgs), 'price': price, 'oldprice': oldprice, 'colors': list(colors), 'art': m.art})
    goods['items'].append(good)
  return HttpResponse(json.dumps(goods, indent = 2, ensure_ascii = False))

def get_goods2(request):
  page = int(request.GET.get('page', 0))
  page_size = int(request.GET.get('page_size', 0))
  position = page * page_size
  category = int(request.GET.get('category', 0))
  models = Model.objects.filter(category = category, thing__present = True).distinct().order_by('-date_of_add')
  quantity = models.count()
  models = models[position:position + page_size]
  goods = {'count': quantity, 'items': []}
  for m in models:
    brand = m.brand.title if m.brand.title else m.brand.name
    good = {'name': brand}
    things = Thing.objects.filter(model = m, present = True)
    imgs = [things[0].image_set.all()[0].small]
    price = int(things[0].price_ru())
    oldprice = int(things[0].old_price_ru())
    good.update({'imgs': list(imgs), 'price': price, 'oldprice': oldprice, 'art': m.art})
    goods['items'].append(good)
  return HttpResponse(json.dumps(goods, indent = 2, ensure_ascii = False))

def yml(request):
  root = etree.Element('yml_catalog', date = unicode(datetime.now()))
  shop = etree.SubElement(root, 'shop')
  etree.SubElement(shop, 'name').text = u'ShinUK'
  etree.SubElement(shop, 'company').text = u'ShinUK LLC'
  etree.SubElement(shop, 'url').text = u'http://shinuk.ru'
  currencies = etree.SubElement(shop, 'currencies')
  etree.SubElement(currencies, 'currency', id = 'RUR', rate = '1')
  etree.SubElement(currencies, 'currency', id = 'UAH', rate = 'CBRF')
  etree.SubElement(currencies, 'currency', id = 'KZT', rate = 'CBRF')
  etree.SubElement(currencies, 'currency', id = 'BYR', rate = 'CBRF')
  categories = etree.SubElement(shop, 'categories')
  category = Category.objects.all()
  group = Group.objects.all()
  for g in group:
    etree.SubElement(categories, 'category', id = unicode(g.id)).text = unicode(g.name_ru).capitalize()
  for c in category:
    if c.parent:
      etree.SubElement(categories, 'category', id = unicode(c.id), parentId = unicode(c.parent.id)).text = unicode(c.name_ru).capitalize()
    else:
      etree.SubElement(categories, 'category', id = unicode(c.id), parentId = unicode(c.group.id)).text = unicode(c.name_ru).capitalize()
  offers = etree.SubElement(shop, 'offers')
  thing = Thing.objects.select_related('model', 'color', 'image_set').filter(present = True).distinct().order_by('id')
  for t in thing:
    offer = etree.SubElement(offers, 'offer', id = unicode(t.id), available = u'false')
    etree.SubElement(offer, 'url').text = unicode('http://shinuk.ru/shop/model/%s/#color=%s' % (t.model.art, t.color.name))
    etree.SubElement(offer, 'price').text = unicode(t.price_ru())
    etree.SubElement(offer, 'currencyId').text = u'RUR'
    t_id = t.model.art
    etree.SubElement(offer, 'categoryId').text = unicode(t.model.category.all()[0].id)
    etree.SubElement(offer, 'picture').text = t.image_set.all()[0].medium
    etree.SubElement(offer, 'delivery').text = u'true'
    if t.price_ru() > 5000: 
      etree.SubElement(offer, 'local_delivery_cost').text = u'0'
    else:
      etree.SubElement(offer, 'local_delivery_cost').text = u'500'
    etree.SubElement(offer, 'name').text = t.model.name
    etree.SubElement(offer, 'description').text = t.model.description
    etree.SubElement(offer, 'sales_notes').text = u'Необходима предоплата.'
    etree.SubElement(offer, 'param', name = u'Цвет').text = t.color.name_ru
  return HttpResponse(etree.tostring(root, pretty_print = True, encoding = 'utf-8', xml_declaration = True, doctype = '<!DOCTYPE yml_catalog SYSTEM "shops.dtd">'), mimetype = 'text/xml')
