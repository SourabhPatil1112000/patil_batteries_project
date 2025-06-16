from django.contrib import admin
from .models import Product, ChatPrompt

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'battery_type', 'capacity', 'price', 'in_stock')
    list_filter = ('battery_type', 'in_stock')
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)
admin.site.register(ChatPrompt)