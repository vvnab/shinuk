#  -*- coding: utf-8 -*- 

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext, Context
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum, Count, Avg, Max, Min, Q
from django.utils import simplejson
from django.contrib import auth, messages
from pytils.translit import translify
from accounts.models import Profile, Address, Message
from models import *
from forms import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime, re

def sendmessage(fullname, username, password, email):
  try:
    message = Message.objects.get(target = 'rg')
  except ObjectDoesNotExist:
    return
  try:
    send_mail(message.subject, message.text.format(fullname = unicode(fullname), username = username, password = password), 'info@shinuk.ru', [email])
  except:
    pass

def discount(total):
  if total >= 10000:
    return -1500
  elif total >= 5000:
    return -750
  else:
    return 0

@csrf_exempt
def checkout(request):
  '''
  выбор адреса доставки и способа оплаты
  '''
  pays = Pay.objects.filter(available = True)
  if request.method == 'POST':
    bag = request.POST
    request.session['bag'] = bag
  else:
    bag = request.session.get('bag', None)
    if not bag:
      # корзина пуста
      return redirect('/bag/')
  user = request.user
  if not user.is_authenticated(): return redirect('/accounts/login/?next=/order/checkout/')
  T = []
  total = 0
  for i, art in enumerate(bag.getlist('art')):
    color = bag.getlist('color')[i]
    size = bag.getlist('size')[i]
    quantity = int(bag.getlist('quantity')[i])
    thing = get_object_or_404(Thing, model__art = art, color__name = color)
    total += thing.price_ru() * quantity
    T.append({'thing': thing, 'price': thing.price_ru(), 'size': get_object_or_404(Size, size = size), 'quantity': quantity, 'total': quantity * int(thing.price_ru())})
  request.session['T'] = T
  address = get_list_or_404(Address, user = user)
  profile = user.get_profile()
  delivery = Delivery.objects.all()
  for d in delivery:
    d.cost += discount(total)
    if d.cost < 0: d.cost = 0
  return render_to_response('order/checkout.html', locals(), context_instance = RequestContext(request))

@login_required
def pay(request):
  if request.method == 'POST':
    user = request.user
    profile = user.get_profile()
    address = get_object_or_404(Address, user = user, default = True)
    devmethod = request.POST.get('delivery')
    paymethod = request.POST.get('paymethod')
    delivery = get_object_or_404(Delivery, id = devmethod)
    pay = get_object_or_404(Pay, id = paymethod)
    order = Order(user = user, address = address, delivery = delivery, pay = pay)
    order.save()
    try:
        send_mail(u'Новый заказ №%s' % (order.id), u'Новый заказ http://shinuk.ru/ladmin/order/%s/' % (order.id), 'neworder@shinuk.ru', ['info@shinuk.ru', 'admin@shinuk.ru'])
    except:
        pass
    T = request.session.get('T', None)
    total = 0
    for t in T:
      total += t['total']
      orderItem = OrderItem(order = order, thing = t['thing'], size = t['size'], price = t['price'], quantity = t['quantity'])
      orderItem.save()
    order.deliverycost = delivery.cost + discount(total)
    if order.deliverycost < 0: order.deliverycost = 0
    order.totalcost = total + order.deliverycost
    orderstatuslist = OrderStatusList(order = order, status = OrderStatus.objects.get(title = u'новый'))
    orderstatuslist.save()
    order.status = orderstatuslist
    order.save()
    request.session['order'] = order.id
    if pay.nick == 'card':
      return redirect('/ecommerce/auth/')
    elif pay.nick == 'check':
      pass
    elif pay.nick == 'yandex':
      pass
    elif pay.nick == 'qiwi':
      client_phone = re.sub(r'\+\d \(|\) |-', '', profile.phone)
      amount = float(order.totalcost)
      lifetime = datetime.datetime.now() + datetime.timedelta(3)
      comment = u'Заказ №%s в интернет магазине ShinUK от %s' % (order.id, order.datetime)
      txn = order.id
      return redirect('http://w.qiwi.ru/setInetBill_utf.do?from=14671&to=%s&summ=%s&com=%s&txn_id=%s&lifetime=%s' % (client_phone, amount, comment, txn, lifetime))
    elif pay.nick == 'other':
      pass
    return redirect('/order/complete/')
  else:
    return redirect('/bag/')

def complete(request):
  order = request.session.get('order', None)
  if not order: 
    return redirect('/')
  else:
    pass
#    del request.session['order']
  order = get_object_or_404(Order, id = order)
  return render_to_response('order/complete.html', locals(), context_instance = RequestContext(request))

@login_required
@csrf_exempt
def promocode(request):
  code = request.POST.get('promocode')
  try:
    promo = PromoCode.objects.filter(active = True, code = code, expire__gte = datetime.datetime.now(), start__lte = datetime.datetime.now())[0]
  except IndexError:
    return HttpResponse('error')
  T = request.session.get('T', [])
  for t in T:
    t['price'] = t['price'] - ( t['price'] * promo.discount ) / 100
    t['total'] = t['total'] - ( t['total'] * promo.discount ) / 100
  request.session['T'] = T
  return HttpResponse(u'%s' % promo.discount)
