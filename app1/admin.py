from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)

class OrderAdmin(admin.ModelAdmin):
  list_display = ('user','created_at','total_price')
  
admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
  list_display = ('order','product','quantity','price')
  
admin.site.register(OrderItem, OrderItemAdmin)