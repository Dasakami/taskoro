from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ShopItem(models.Model):
    CURRENCY_CHOICES = [
        ('coins', 'Монеты'),
        ('gems', 'Кристаллы'),
    ]
    
    CATEGORY_CHOICES = [
        ('avatar_frame', 'Рамка аватара'),
        ('title', 'Титул'),
        ('background', 'Фон профиля'),
        ('effect', 'Визуальный эффект'),
        ('boost', 'Ускоритель'),
        ('chest', 'Сундук'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='shop_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    title_text = models.CharField(max_length=100, blank=True, null=True, help_text="For title items")
    title_color = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color for title")
    frame_style = models.CharField(max_length=100, blank=True, null=True, help_text="For avatar frames")
    background_url = models.CharField(max_length=255, blank=True, null=True, help_text="For background items")
    effect_class = models.CharField(max_length=100, blank=True, null=True, help_text="CSS class for visual effect")
    boost_multiplier = models.FloatField(default=1.0, help_text="For boost items")
    boost_duration = models.IntegerField(default=0, help_text="Duration in hours for boosts")
    
    def __str__(self):
        return self.name
    
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES)[self.category]

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_equipped = models.BooleanField(default=False, help_text="Whether this item is currently equipped")
    
    def __str__(self):
        return f"{self.user.username} - {self.item.name}"

class ActiveBoost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='active_boosts')
    boost_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, limit_choices_to={'category': 'boost'})
    multiplier = models.FloatField()
    activated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.boost_item.name}"
    
    @property
    def is_active(self):
        return timezone.now() < self.expires_at
    
    @property
    def remaining_time(self):
        if not self.is_active:
            return "Истёк"
        
        now = timezone.now()
        remaining = self.expires_at - now
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}д {hours}ч"
        elif hours > 0:
            return f"{hours}ч {minutes}м"
        else:
            return f"{minutes}м {seconds}с"

class Chest(models.Model):
    RARITY_CHOICES = [
        ('common', 'Обычный'),
        ('rare', 'Редкий'),
        ('epic', 'Эпический'),
        ('legendary', 'Легендарный'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    price_coins = models.IntegerField()
    price_gems = models.IntegerField()
    min_coins_reward = models.IntegerField()
    max_coins_reward = models.IntegerField()
    min_gems_reward = models.IntegerField()
    max_gems_reward = models.IntegerField()
    image = models.ImageField(upload_to='chest_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_rarity_display()} {self.name}"
        
    def get_rarity_display(self):
        return dict(self.RARITY_CHOICES)[self.rarity]

class ChestOpening(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chest_openings')
    chest = models.ForeignKey(Chest, on_delete=models.CASCADE)
    coins_reward = models.IntegerField()
    gems_reward = models.IntegerField()
    opened_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} opened {self.chest.name}"