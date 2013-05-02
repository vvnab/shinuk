#  -*- coding: utf-8 -*- 

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext, Context
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from accounts.models import Profile, Address
from models import *
from orders.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import tools, settings, urllib, urllib2

@login_required
def auth(request):
  order = request.session.get('order', None)
  if not order: redirect('/')
  order = get_object_or_404(Order, id = order)

  AMOUNT = str(order.totalcost) + '.00'
  CURRENCY = settings.CURRENCY
  ORDER = order.ordernum()
  DESC = order.desc
  MERCH_NAME = settings.MERCH_NAME
  MERCH_URL = settings.MERCH_URL
  MERCHANT = settings.MERCHANT
  TERMINAL = settings.TERMINAL
  EMAIL = settings.EMAIL
  TRTYPE = '0'
  COUNTRY = settings.COUNTRY
  MERCH_GMT = settings.MERCH_GMT
  TIMESTAMP = tools.timestamp()
  NONCE = tools.nonce(32)
  BACKREF = settings.BACKREF
  
  temp = tools.prepstr([AMOUNT, CURRENCY, ORDER, DESC, MERCH_NAME, MERCH_URL, MERCHANT, TERMINAL, EMAIL, TRTYPE, COUNTRY, MERCH_GMT, TIMESTAMP, NONCE, BACKREF])
  P_SIGN = tools.mac(temp, settings.KEY)

  GATEWAY_URL = settings.GATEWAY_URL

  return render_to_response('ecommerce/auth.html', locals(), context_instance = RequestContext(request))

@csrf_exempt
def reply(request):
  if request.method == 'POST':
    order = request.POST.get('ORDER', '')
    order = get_object_or_404(Order, id = int(order))
    action =  request.POST.get('ACTION', '')
    aproval = request.POST.get('APPROVAL', '')
    int_ref = request.POST.get('IRN', '')
    rc = request.POST.get('RC', '')
    rrn = request.POST.get('RRN', '')
    timestamp = request.POST.get('TIMESTAMP', '')
    nonce = request.POST.get('NONCE', '')
    mac = request.POST.get('P_SIGN', '')
    rr = ResponseRequest(order = order, aproval = aproval, int_ref = int_ref, rc = rc, rrn = rrn)
    rr.save()
    return HttpResponse('ok')
  else:
    return HttpResponse('error')

@csrf_exempt
def accept(request):
  data = {}
  url_values = urllib.urlencode(data)
  return HttpResponse('ok')

@csrf_exempt
def reject(request):
  return HttpResponse('ok')

def backref(request):
  order = request.session.get('order', None)
  if not order: redirect('/')
  order = get_object_or_404(Order, id = order)
  rr = get_list_or_404(ResponseRequest, order = order)[0]
  return render_to_response('ecommerce/complete.html', locals(), context_instance = RequestContext(request))
  