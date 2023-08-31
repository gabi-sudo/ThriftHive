from django.contrib import admin

from store.models import Cart, Item, Order, Store

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Store)