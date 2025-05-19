
from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path('', views.shop_home, name='shop'),
    path('category/<str:category>/', views.shop_category, name='shop_category'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('purchase/<int:item_id>/', views.purchase_item, name='purchase_item'),
    path('chests/', views.chest_list, name='chest_list'),
    path('chests/<int:chest_id>/open/', views.open_chest, name='open_chest'),
    path('inventory/', views.user_inventory, name='user_inventory'),
]
