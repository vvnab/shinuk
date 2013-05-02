#  -*- coding: utf-8 -*- 

from django.contrib import admin
from models import *

admin.site.register(Vendor)
admin.site.register(Group)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('__unicode__', 'name_ru')
  list_display_links = ('__unicode__',)
  list_filter = ('group',)
  list_editable = ('name_ru',)

admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
  list_display = ('name', 'title')
  list_display_links = ('name',)
  list_editable = ('title',)

admin.site.register(Brand, BrandAdmin)

class ColorAdmin(admin.ModelAdmin):
  list_display = ('name', 'name_ru', 'base')
  list_display_links = ('name',)
  list_editable = ('name_ru', 'base')
  list_filter = ('base',)
admin.site.register(Color, ColorAdmin)

admin.site.register(Size)

class ModelAdmin(admin.ModelAdmin):
  filter_horizontal = ('category',)
  search_fields = ('art', 'name')

admin.site.register(Model, ModelAdmin)

class ThingAdmin(admin.ModelAdmin):
  search_fields = ('model__art', 'model__name')

admin.site.register(Thing, ThingAdmin)
admin.site.register(Image)

