from django.contrib import admin
from .models import Packages

@admin.register(Packages)
class Packages_Admin(admin.ModelAdmin):
    list_display = ['package', 'price']