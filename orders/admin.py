#  -*- coding: utf-8 -*- 

from django.contrib import admin
from models import *

admin.site.register(Delivery)
admin.site.register(Pay)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)
admin.site.register(OrderStatusList)
admin.site.register(Parcel)
admin.site.register(ParcelStatus)
admin.site.register(ParcelStatusList)
admin.site.register(PromoCode)
admin.site.register(DiscountCode)

