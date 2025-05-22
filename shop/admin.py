from django.contrib import admin
from .models import ShopItem, Purchase, ActiveBoost, Chest, ChestOpening

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'currency', 'is_available']
    list_filter = ['category', 'currency', 'is_available']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'currency', 'category', 'image', 'is_available')
        }),
        ('Title Settings', {
            'fields': ('title_text', 'title_color'),
            'classes': ('collapse',),
        }),
        ('Frame Settings', {
            'fields': ('frame_style',),
            'classes': ('collapse',),
        }),
        ('Background Settings', {
            'fields': ('background_url',),
            'classes': ('collapse',),
        }),
        ('Effect Settings', {
            'fields': ('effect_class',),
            'classes': ('collapse',),
        }),
        ('Boost Settings', {
            'fields': ('boost_multiplier', 'boost_duration'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'purchased_at', 'is_equipped']
    list_filter = ['is_equipped', 'purchased_at']
    search_fields = ['user__username', 'item__name']

@admin.register(ActiveBoost)
class ActiveBoostAdmin(admin.ModelAdmin):
    list_display = ['user', 'boost_item', 'multiplier', 'activated_at', 'expires_at', 'is_active']
    list_filter = ['activated_at', 'expires_at']
    search_fields = ['user__username', 'boost_item__name']
    readonly_fields = ['is_active', 'remaining_time']

    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    
    def remaining_time(self, obj):
        return obj.remaining_time

@admin.register(Chest)
class ChestAdmin(admin.ModelAdmin):
    list_display = ['name', 'rarity', 'price_coins', 'price_gems']
    list_filter = ['rarity']
    search_fields = ['name']

@admin.register(ChestOpening)
class ChestOpeningAdmin(admin.ModelAdmin):
    list_display = ['user', 'chest', 'coins_reward', 'gems_reward', 'opened_at']
    list_filter = ['opened_at', 'chest']
    search_fields = ['user__username']