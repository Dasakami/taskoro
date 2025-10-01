from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import ShopItem, Purchase, Chest, ChestOpening, ActiveBoost
from history.models import ActivityLog
import random

def shop_home(request):
    featured_items = ShopItem.objects.filter(is_available=True).order_by('?')[:4]
    new_items = ShopItem.objects.filter(is_available=True).order_by('-created_at')[:4]
    
    categories = ShopItem.CATEGORY_CHOICES
    
    context = {
        'featured_items': featured_items,
        'new_items': new_items,
        'categories': categories,
    }
    
    return render(request, 'shop/shop_home.html', context)

@login_required
def shop_category(request, category):
    items = ShopItem.objects.filter(
        category=category,
        is_available=True
    ).order_by('-created_at')
    
    context = {
        'items': items,
        'category': dict(ShopItem.CATEGORY_CHOICES)[category],
        'category_slug': category,
        'shop_item_categories': ShopItem.CATEGORY_CHOICES,
    }
    
    return render(request, 'shop/shop_category.html', context)

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id, is_available=True)
    
    already_purchased = Purchase.objects.filter(user=request.user, item=item).exists()
    is_equipped = False
    if already_purchased:
        is_equipped = Purchase.objects.filter(user=request.user, item=item, is_equipped=True).exists()
    
    context = {
        'item': item,
        'already_purchased': already_purchased,
        'is_equipped': is_equipped,
    }
    
    return render(request, 'shop/item_detail.html', context)

@login_required
def purchase_item(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id, is_available=True)
    
    if Purchase.objects.filter(user=request.user, item=item).exists():
        messages.info(request, f'Вы уже приобрели {item.name}.')
        return redirect('shop:item_detail', item_id=item.id)

    profile = request.user.profile
    if item.currency == 'coins' and profile.coins < item.price:
        messages.error(request, 'Недостаточно монет для покупки.')
        return redirect('shop:item_detail', item_id=item.id)
    elif item.currency == 'gems' and profile.gems < item.price:
        messages.error(request, 'Недостаточно кристаллов для покупки.')
        return redirect('shop:item_detail', item_id=item.id)
    
    if item.currency == 'coins':
        profile.coins -= item.price
    else:
        profile.gems -= item.price
    profile.save()
    
    purchase = Purchase.objects.create(
        user=request.user,
        item=item,
        total_price=item.price
    )
    
    if item.category in ['title', 'avatar_frame', 'background']:
        equip_item(request, item.id)
    
    messages.success(request, f'Вы приобрели {item.name}!')
    return redirect('shop:user_inventory')

@login_required
def equip_item(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id)
    
    purchase = get_object_or_404(Purchase, user=request.user, item=item)
    
    Purchase.objects.filter(
        user=request.user, 
        item__category=item.category,
        is_equipped=True
    ).update(is_equipped=False)
    
    purchase.is_equipped = True
    purchase.save()
    
    profile = request.user.profile
    
    if item.category == 'title':
        profile.title = item.title_text
        profile.save()
        
    elif item.category == 'boost':
        end_time = timezone.now() + timedelta(hours=item.boost_duration)
        
        ActiveBoost.objects.create(
            user=request.user,
            boost_item=item,
            multiplier=item.boost_multiplier,
            expires_at=end_time
        )
    
    messages.success(request, f'Вы экипировали {item.name}.')
    
    if request.method == 'POST':
        return redirect('shop:item_detail', item_id=item.id)
    return redirect('shop:user_inventory')

@login_required
def unequip_item(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id)
    
    purchase = get_object_or_404(Purchase, user=request.user, item=item)
    purchase.is_equipped = False
    purchase.save()
    
    profile = request.user.profile
    
    if item.category == 'title':
        profile.title = ''
        profile.save()
    
    messages.success(request, f'Вы сняли {item.name}.')
    
    if request.method == 'POST':
        return redirect('shop:item_detail', item_id=item.id)
    return redirect('shop:user_inventory')

@login_required
def chest_list(request):
    chests = Chest.objects.all()
    
    context = {
        'chests': chests,
        'shop_item_categories': ShopItem.CATEGORY_CHOICES,
    }
    
    return render(request, 'shop/chest_list.html', context)

@login_required
def open_chest(request, chest_id):
    chest = get_object_or_404(Chest, id=chest_id)
    profile = request.user.profile
    
    if profile.coins < chest.price_coins or profile.gems < chest.price_gems:
        messages.error(request, 'Недостаточно средств для открытия сундука.')
        return redirect('shop:chest_list')
    
    profile.coins -= chest.price_coins
    profile.gems -= chest.price_gems
    
    coins_reward = random.randint(chest.min_coins_reward, chest.max_coins_reward)
    gems_reward = random.randint(chest.min_gems_reward, chest.max_gems_reward)
    
    profile.coins += coins_reward
    profile.gems += gems_reward
    profile.save()
    
    opening = ChestOpening.objects.create(
        user=request.user,
        chest=chest,
        coins_reward=coins_reward,
        gems_reward=gems_reward
    )

    ActivityLog.objects.create(
            user=request.user,
            activity_type='chest_open',
            description=f'Вы открыли сундук: {chest.name}',
            
            
        )
    
    messages.success(
        request,
        f'Вы получили {coins_reward} монет и {gems_reward} кристаллов из {chest.name}!'
    )
    return redirect('shop:chest_list')

@login_required
def user_inventory(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    
    equipped_items = Purchase.objects.filter(
        user=request.user,
        is_equipped=True
    ).select_related('item')
    
    equipped_by_category = {purchase.item.category: purchase.item.id for purchase in equipped_items}
    
    active_boosts = ActiveBoost.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now()
    ).select_related('boost_item')
    
    context = {
        'purchases': purchases,
        'equipped_by_category': equipped_by_category,
        'active_boosts': active_boosts,
        'shop_item_categories': ShopItem.CATEGORY_CHOICES,
    }
    
    return render(request, 'shop/user_inventory.html', context)