#  -*- coding: utf-8 -*- 

from django import forms
from goods.models import *

class ModelForm(forms.ModelForm):
  class Meta:
    model = Model
    fields = ('vendor', 'category', 'brand', 'url', 'art', 'name', 'description', 'info', 'flashurl')
#    category = forms.ModelMultipleChoiceField(queryset = Category.objects.all(), label=u'Категории')
#    brand = forms.ModelChoiceField(queryset = Brand.objects.all(), label=u'Бренд')

class ThingForm(forms.ModelForm):
  class Meta:
    model = Thing
    fields = ('color', 'size', 'price', 'oldprice')

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ('group',)
        

