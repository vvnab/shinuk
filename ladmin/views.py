#  -*- coding: utf-8 -*- 

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect 
from django.template import Template, RequestContext, Context
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Max, Min, Q
from django.utils import simplejson as json
from goods.models import *
from orders.models import *
from ecommerce.models import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from forms import *
from grab import Asos, DoesNotExist
from django.contrib.flatpages.models import FlatPage
import ecommerce.tools, settings, urllib, urllib2
from datetime import datetime
from accounts.models import Profile
from django.contrib import messages
from templated_email import send_templated_mail

@permission_required('goods.can_add', login_url='/admin/')
def main(request):
    flatpage = get_object_or_404(FlatPage, url = '/ladmin/')
    t = get_template('ladmin/main.html')
    html = t.render(Context(locals()))
    response = HttpResponse(html)
    response.set_cookie('IAmAdmin', 'true', max_age = 31536000)
    return response

@permission_required('goods.can_add', login_url='/admin/')
def search(request):
    search = request.GET.get('search')
    if search:
        q = Q(art__contains = search) | Q(name__icontains = search)
        items = Model.objects.filter(q).distinct()
    return render_to_response('ladmin/search.html', locals(), context_instance = RequestContext(request))

@permission_required('goods.can_add', login_url='/admin/')
def goods_add(request):
    count = Model.objects.filter(date_of_add = datetime.now()).count()
    if request.method == 'POST':
        post = request.POST.copy()
        art = post.get('art')
        try:
            model = Model.objects.get(art = art)
            modelform = ModelForm(post, instance = model)
        except ObjectDoesNotExist:
            modelform = ModelForm(post)
        if modelform.is_valid():
            model = modelform.save()
        else:
            return render_to_response('ladmin/goods_add.html', locals(), context_instance = RequestContext(request))

        images_all = post.getlist('images_all')

        for i in range(0, len(images_all), 4):
            small, thumb, medium, lage = images_all[i:i + 4]
            img, cr = Image.objects.get_or_create(small = small, thumb = thumb, medium = medium, lage = lage, model = model)

        colors = post.getlist('colors')

        for c in colors:
            ru, base, rgb = post.getlist('color_' + c)
            color, cr = Color.objects.get_or_create(name = c)
            color.name_ru, color.base, color.rgb = ru, base, rgb
            color.save()
            
            price, oldprice = post.getlist('price_' + c)
            thing, cr = Thing.objects.get_or_create(model = model, color = color)
            thing.price, thing.oldprice = price, oldprice
            if thing.price == 0:
                thing.present = False
            thing.save()

            try:
                small, thumb, medium, lage = post.getlist('images_' + c)
                img, cr = Image.objects.get_or_create(small = small, thumb = thumb, medium = medium, lage = lage, thing = thing)
            except ValueError:
                pass
            sizes = post.getlist('sizes_' + c)
            sss = []
            for s in sizes:
                size = post.get('size_%s_%s' % (s, c))
                ss, cr = Size.objects.get_or_create(size = s)
                ss.size_ru = size
                ss.save()
                sss.append(ss)
            if not sss:
                thing.present = False
            thing.size = sss
            thing.save()
        return HttpResponseRedirect('/ladmin/goods_add/')
    else:
        art = request.GET.get('art', None)
        if art:
            try:
                model = Model.objects.get(art = art)
            except ObjectDoesNotExist:
                pass
        groupform = CategoryForm()
        modelform = ModelForm()
    return render_to_response('ladmin/goods_add.html', locals(), context_instance = RequestContext(request))

def fetch(request):
    url = request.GET.get('url')
    try:
        thing = Asos(url)
    except DoesNotExist, err:
        return HttpResponse(json.dumps({'error': str(err)}, indent = 2, ensure_ascii = False))
    thing = thing.get()
    created = {}
    selcats = []
    try:
        model = Model.objects.get(art = thing['art'])
        thing['info'] = model.info
        thing['description'] = model.description
        thing['group'] = model.category.all()[0].group.name
        selcats = list(model.category.all().values_list('id', flat = True))
    except ObjectDoesNotExist:
        pass
    if thing['brand']:    
        brand, cb = Brand.objects.get_or_create(name = thing['brand'])
        if cb: created.update(brand = {'name': str(brand), 'id': brand.id})
    if thing['group']: 
        group, cg = Group.objects.get_or_create(name = thing['group'])
        if cg: created.update(group = {'name': str(group), 'id': group.id})
    if thing['category']: 
        category, cc = Category.objects.get_or_create(name = thing['category'], group = group, defaults = {'group': group})
        if cc: created.update(category = {'name': str(category), 'id': category.id})
    if thing['subcategory']: 
        subcategory, cs = Category.objects.get_or_create(name = thing['subcategory'], parent = category, defaults = {'group': group, 'parent': category})
        if cs: created.update(subcategory = {'name': str(subcategory), 'id': subcategory.id})
    categorys = {}
    group = Group.objects.all()
    for g in group:
        c = Category.objects.filter(group = g)
        categorys[g.name] = []
        for i in c:
            categorys[g.name].append({'id': i.id, 'name': str(i)})
    col = {}
    for color in thing['items']:
        c, cr = Color.objects.get_or_create(name = color)
        if not cr: 
            col[color] = {'name_ru': c.name_ru, 'base': c.base, 'rgb': c.rgb}
        else:
            col[color] = {'name_ru': '', 'base': '', 'rgb': ''}
        for item in thing['items'][color]:
            size = item['size']
            size_en = item['size_en']
            s, cr = Size.objects.get_or_create(size = size, defaults={'size_en': size_en})
            if not cr: item.update({'size_ru': s.size_ru})
    baseColors = Color.objects.values_list('base', flat = True).distinct().order_by('base')
    return HttpResponse(json.dumps({'url': thing, 'created': created, 'categorys': categorys, 'colors': col, 'baseColors': list(baseColors), 'selcats': selcats}, indent = 2, ensure_ascii = False))

def get_categorys(request):
    group = request.GET.get('group')
    if group:
        categorys = Category.objects.filter(group__id = group)
    else:
        categorys = Category.objects.all()
    cats = []
    for i in categorys:
        cats.append({'id': i.id, 'name': str(i)})
    return HttpResponse(json.dumps({'categorys': cats}, indent = 2))

@permission_required('goods.can_add', login_url='/admin/')
def orders(request):
    orders = Order.objects.all().order_by('-datetime')
    return render_to_response('ladmin/orders.html', locals(), context_instance = RequestContext(request))

@permission_required('goods.can_add', login_url='/admin/')
def order(request, order_id):
    order = Order.objects.get(id = order_id)
    orderstatus = OrderStatus.objects.all()
    if request.method == 'POST':
        post = request.POST.copy()
        if post.get('action') == 'add_status':
            status = OrderStatus.objects.get(pk = post.get('status'))
            status_list = OrderStatusList( order = order, status = status)
            status_list.save()
            order.status = status_list
            order.save()
        if post.get('action') == 'set_parcel_code':
            parcel = Parcel(code = post.get('parcel_code'))
            parcel.save()
            order.parcel = parcel
            order.save()
        return redirect(request.path)
    try:
        rr = ResponseRequest.objects.filter(order = order)[0]
        ORDER = order.ordernum()
        AMOUNT = str(order.totalcost) + '.00'
        CURRENCY = settings.CURRENCY
        RRN = rr.rrn
        INT_REF = rr.int_ref
        TRTYPE_ACCEPT = '21' # accept
        TRTYPE_REJECT = '24' # accept
        TERMINAL = settings.TERMINAL
        TIMESTAMP = ecommerce.tools.timestamp()
        NONCE = ecommerce.tools.nonce(32)
        temp_accept = ecommerce.tools.prepstr([ORDER, AMOUNT, CURRENCY, RRN, INT_REF, TRTYPE_ACCEPT, TERMINAL, TIMESTAMP, NONCE])
        P_SIGN_ACCEPT = ecommerce.tools.mac(temp_accept, settings.KEY)
        temp_reject = ecommerce.tools.prepstr([ORDER, AMOUNT, CURRENCY, RRN, INT_REF, TRTYPE_REJECT, TERMINAL, TIMESTAMP, NONCE])
        P_SIGN_REJECT = ecommerce.tools.mac(temp_reject, settings.KEY)
        GATEWAY_URL = settings.GATEWAY_URL
    except IndexError:
        pass
    return render_to_response('ladmin/order.html', locals(), context_instance = RequestContext(request))

@permission_required('goods.can_add', login_url='/admin/')
def order_delete(request):
    order_id = request.POST.get('order')
    order = get_object_or_404(Order, id = order_id)
    order.delete()
    return redirect('/ladmin/orders')

@permission_required('users.can_add', login_url='/admin/')
def users(request):
    users = Profile.objects.all()
    return render_to_response('ladmin/users.html', locals(), context_instance = RequestContext(request))

import logging
logger = logging.getLogger('logger')

@permission_required('users.can_add', login_url='/admin/')
def email(request):
    users = User.objects.all()
    if request.method == 'POST':
        emailUsers = User.objects.filter(id__in = request.POST.getlist('emailUsers'))
        for i in emailUsers:
            logger.info('Send email to - {0}'.format(i.email))
            try:
                template = request.POST.get('emailUrl')
                send_templated_mail(
                    template_name = template,
                    from_email = u'Магазин ShinUK <ingo@shinuk.ru>',
                    recipient_list = [i.email],
                    context = {
                        'text': request.POST.get('emailText', ''),
                        'user': i
                    }
                )
                logger.info('Ok sended email to - {0}'.format(i.email))
            except:
                logger.info('Errror!!! send email to - {0}'.format(i.email))
                messages.error(request, u'Ошибка при отправке письма с уведомлением!')
        return redirect('/ladmin/email/')
    else:
        pass
    return render_to_response('ladmin/email.html', locals(), context_instance = RequestContext(request))
