
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ShopItem, Purchase, Chest, ChestOpening
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
    }
    
    return render(request, 'shop/shop_category.html', context)

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id, is_available=True)
    
    context = {
        'item': item,
    }
    
    return render(request, 'shop/item_detail.html', context)

@login_required
def purchase_item(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id, is_available=True)
    
    # Check if user can afford the item
    profile = request.user.profile
    if item.currency == 'coins' and profile.coins < item.price:
        messages.error(request, 'Недостаточно монет для покупки.')
        return redirect('shop:item_detail', item_id=item.id)
    elif item.currency == 'gems' and profile.gems < item.price:
        messages.error(request, 'Недостаточно кристаллов для покупки.')
        return redirect('shop:item_detail', item_id=item.id)
    
    # Process purchase
    if item.currency == 'coins':
        profile.coins -= item.price
    else:
        profile.gems -= item.price
    profile.save()
    
    Purchase.objects.create(
        user=request.user,
        item=item,
        total_price=item.price
    )
    
    messages.success(request, f'Вы приобрели {item.name}!')
    return redirect('shop:user_inventory')

@login_required
def chest_list(request):
    chests = Chest.objects.all()
    
    context = {
        'chests': chests,
    }
    
    return render(request, 'shop/chest_list.html', context)

@login_required
def open_chest(request, chest_id):
    chest = get_object_or_404(Chest, id=chest_id)
    profile = request.user.profile
    
    # Check if user can afford the chest
    if profile.coins < chest.price_coins or profile.gems < chest.price_gems:
        messages.error(request, 'Недостаточно средств для открытия сундука.')
        return redirect('shop:chest_list')
    
    # Deduct cost
    profile.coins -= chest.price_coins
    profile.gems -= chest.price_gems
    
    # Generate rewards
    coins_reward = random.randint(chest.min_coins_reward, chest.max_coins_reward)
    gems_reward = random.randint(chest.min_gems_reward, chest.max_gems_reward)
    
    # Add rewards
    profile.coins += coins_reward
    profile.gems += gems_reward
    profile.save()
    
    # Record opening
    opening = ChestOpening.objects.create(
        user=request.user,
        chest=chest,
        coins_reward=coins_reward,
        gems_reward=gems_reward
    )
    
    messages.success(
        request,
        f'Вы получили {coins_reward} монет и {gems_reward} кристаллов из {chest.name}!'
    )
    return redirect('shop:chest_list')

@login_required
def user_inventory(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    
    context = {
        'purchases': purchases,
    }
    
    return render(request, 'shop/user_inventory.html', context)
