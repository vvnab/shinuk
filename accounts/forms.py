#  -*- coding: utf-8 -*- 

from django import forms
from models import *

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('email', 'last_name', 'first_name')

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ('user', 'invite', 'deposit')
        
class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    exclude = ('user', 'default')
