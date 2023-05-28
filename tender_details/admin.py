from django.contrib import admin
from .models import Tender, Category, Keywords, Province

@admin.register(Tender)
class tenderAdmin(admin.ModelAdmin):
    list_display = ['refNum', 'issueDate', 'closingDate', 'kw_assigned']
    # list_filter = ('kw_assigned',)
    filter_horizontal = ('tenderCategory', 'tenderProvince')
    search_fields = ['refNum', 'summary']
    raw_id_fields = ('assigned_keywords',)


@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ['catDescription']


@admin.register(Keywords)
class keywordsAdmin(admin.ModelAdmin):
    list_display = ['keyword']
    search_fields = ['keyword']

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['province_name']