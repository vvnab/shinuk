#  -*- coding: utf-8 -*- 

from django import forms
from models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('status', 'code', 'postdatetime', 'partner', 'user')

        

