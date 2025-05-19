from django.contrib import admin
from .models import Chest,ChestOpening,ShopItem,Purchase
admin.site.register(ShopItem)
admin.site.register(Purchase)
admin.site.register(Chest)
admin.site.register(ChestOpening)

# Register your models here.
