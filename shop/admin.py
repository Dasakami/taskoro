from django.contrib import admin
from .models import ShopItem, Purchase, Chest, ChestOpening, ActiveBoost

class ShopItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'currency', 'is_available')
    list_filter = ('category', 'currency', 'is_available')
    search_fields = ('name', 'description')

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'total_price', 'purchased_at', 'is_equipped')
    list_filter = ('is_equipped', 'purchased_at')
    search_fields = ('user__username', 'item__name')

class ChestAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'price_coins', 'price_gems')
    list_filter = ('rarity',)

class ChestOpeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'chest', 'coins_reward', 'gems_reward', 'opened_at')
    list_filter = ('opened_at',)
    search_fields = ('user__username',)

class ActiveBoostAdmin(admin.ModelAdmin):
    list_display = ('user', 'boost_item', 'multiplier', 'activated_at', 'expires_at', 'is_active')
    list_filter = ('activated_at', 'expires_at')
    search_fields = ('user__username', 'boost_item__name')

admin.site.register(ShopItem, ShopItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Chest, ChestAdmin)
admin.site.register(ChestOpening, ChestOpeningAdmin)
admin.site.register(ActiveBoost, ActiveBoostAdmin)