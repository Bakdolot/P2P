from django.contrib import admin

from .models import Category, Service
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'api_id', 'order_id')
    list_display_links = list_display


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display

