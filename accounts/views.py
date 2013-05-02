#  -*- coding: utf-8 -*- 

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404,  get_list_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required
import simplejson as json
from django.contrib import auth
from orders.models import *
from models import *
from orders.models import *
from forms import *
from accounts.models import Message
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['username'] = data['email']
        if User.objects.filter(username = data['username']):
            return HttpResponseRedirect('/accounts/userexists/')
        password = User.objects.make_random_password(length = 8)
        userform = UserForm(data)
        addressform = AddressForm(data)
        if userform.is_valid():
            user = User.objects.create_user(data['email'], data['email'], password)
            user.first_name = userform.cleaned_data['first_name']
            user.last_name = userform.cleaned_data['last_name']
            user.save()
            user = auth.authenticate(username = user.username, password = password)
            auth.login(request, user)
            send_mail(u'Ваш логин/пароль на сайте ShinUK', u'Вы успешно зарегестрированы на сайте ShinUK.Ru\n Ваш логин: %s\nВаш пароль: %s' % (user.username, password), 'info@shinuk.ru', [user.email], fail_silently = True)
            profileform = ProfileForm(data)
            if profileform.is_valid():
                profile = Profile(user = user)
                UIN = request.COOKIES.get('UIN', None)
                if UIN:
                  try:
                    partner = Partner.objects.get(key = UIN)
                    profile.invite = partner.user
                  except ObjectDoesNotExist:
                    pass
                profileform = ProfileForm(data, instance = profile)
                profileform.save()
                addressform = AddressForm(data)
                if addressform.is_valid():
                    address = Address(user = user)
                    addressform = AddressForm(data, instance = address)
                    addressform.save()
                    return HttpResponseRedirect('/order/checkout/')
    else:
        userform = UserForm()
        profileform = ProfileForm()
        addressform = AddressForm()
    return render_to_response('accounts/register.html', locals(), context_instance=RequestContext(request))

@login_required
def profile(request):
  user = request.user
  profile = user.get_profile()
  address = get_list_or_404(Address, user = user)
  if request.method == 'POST':
    data = request.POST.copy()
    if request.POST.get('last_name', None):
      user.last_name = data['last_name']
      user.first_name = data['first_name']
      profile.middlename = data['middlename']
      profile.phone = data['phone']
      user.save()
      profile.save()
    addressform = AddressForm(data, instance = address[0])
    if request.POST.get('zip', None) and addressform.is_valid():
      addressform.save()
  address = get_list_or_404(Address, user = user)
  addressform = AddressForm(instance = address[0])
  profile = user.get_profile()
  orders = Order.objects.filter(user = user)
  return render_to_response('accounts/profile.html', locals(), context_instance=RequestContext(request))

@login_required
def order(request, id):
  order = get_object_or_404(Order, id = id)
  if order.user != request.user:
    return redirect('/accounts/profile/')
  if request.method == 'POST':
    if request.POST.get('action') == 'reject':
      status = OrderStatus.objects.get(title = u'отказ клиента')
      statusList = OrderStatusList(order = order, status = status)
      statusList.save()
      order.status = statusList
      order.save()
    return redirect(request.path)
  return render_to_response('accounts/order.html', locals(), context_instance=RequestContext(request))

def userexists(request):
    return render_to_response('accounts/userexists.html', locals(), context_instance=RequestContext(request))

def send_password(request):
    email = request.GET.get('email')
    try:
        user = User.objects.get(email = email)
        password = User.objects.make_random_password(length = 8)
        user.set_password(password)
        user.save()
        send_mail(u'Пароль на ShinUK.RU', u'Здравствуйте {0}\nВаш новый пароль для входа в личный кабинет: {2}\nВаш логин: {1}'.format(user.get_full_name(), user.username, password), 'no-reply@shinuk.ru', [email], fail_silently = True)
        return HttpResponse('ok')
    except:
        return HttpResponse('error')

@login_required
def partnership(request):
  user = request.user
  profile = user.get_profile()
  try:
    partner = Partner.objects.get(user = user)
    key = partner.key
  except ObjectDoesNotExist:
    key = User.objects.make_random_password(length = 10, allowed_chars = '123456789')
    while Partner.objects.filter(key = key).exists():
      key = User.objects.make_random_password(length = 10, allowed_chars = '123456789')
    partner = Partner(user = user, key = key)
    partner.save()
  pcount = Profile.objects.filter(invite = user).count()
  return render_to_response('accounts/partnership.html', locals(), context_instance=RequestContext(request))

import string, re
@permission_required('goods.can_add', login_url='/admin/')
def users(request):
  response = u''
  users = User.objects.all()
  for user in users:
    profile = user.get_profile()
    name = u'{0} {1}'.format(user.first_name, profile.middlename)
    name = string.capwords(name)
    name = re.sub(r' +', ' ', name.strip())
    if profile.gender == 'men':
      use = u'Уважаемый'
    else:
      use = u'Уважаемая'
    response += u'{0},{1},{2},{3}\r\n'.format(user.email, name, string.capwords(user.last_name).strip(), use)
  return HttpResponse(response, mimetype = 'text/plain')
