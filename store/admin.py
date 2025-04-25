from django.contrib import admin

# Register your models here.

from .models import Category, Product, Customer, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)