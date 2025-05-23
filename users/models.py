from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CharacterClass(models.Model):
    """Character classes that users can select"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="⚔️")
    color = models.CharField(max_length=7, default="#6633ff")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Character Classes"

class Profile(models.Model):
    THEME_CHOICES = [
        ('dark_blue', 'Dark Blue'),
        ('shadow_purple', 'Shadow Purple'),
        ('blood_red', 'Blood Red'),
        ('neon_green', 'Neon Green'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    experience_needed = models.IntegerField(default=100)
    streak = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    gems = models.IntegerField(default=0)
    bio = models.TextField(max_length=500, blank=True)
    title = models.CharField(max_length=100, blank=True)
    theme_preference = models.CharField(max_length=20, choices=THEME_CHOICES, default='dark_blue')
    character_classes = models.ManyToManyField(CharacterClass, related_name='profiles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_experience_percentage(self):
        return (self.experience / self.experience_needed) * 100
    
    def add_experience(self, amount):
        self.experience += amount
        # Check if level up is needed
        while self.experience >= self.experience_needed:
            self.level_up()
        self.save()
    
    def level_up(self):
        self.experience -= self.experience_needed
        self.level += 1
        self.experience_needed = int(self.experience_needed * 1.5)
        self.gems += 5  # Reward for level up
        self.save()
        self.check_and_award_medals()

    
    def check_and_award_medals(self):
        from .models import Medal  # Import here to avoid circular imports
        
        # Example of awarding medals by level
        if self.level >= 10:
            Medal.objects.get_or_create(
                profile=self,
                name='Level 10 Achiever',
                defaults={
                    'description': 'Достиг 10 уровня',
                    'medal_type': 'bronze',
                }
            )
        if self.level >= 20:
            Medal.objects.get_or_create(
                profile=self,
                name='Level 20 Achiever',
                defaults={
                    'description': 'Достиг 20 уровня',
                    'medal_type': 'silver',
                }
            )
        if self.level >= 30:
            Medal.objects.get_or_create(
                profile=self,
                name='Level 30 Achiever',
                defaults={
                    'description': 'Достиг 30 уровня',
                    'medal_type': 'gold',
                }
            )
    
    # Get equipped items methods
    def get_equipped_avatar_frame(self):
        from shop.models import Purchase, ShopItem
        try:
            purchase = Purchase.objects.get(
                user=self.user, 
                item__category='avatar_frame',
                is_equipped=True
            )
            return purchase.item
        except Purchase.DoesNotExist:
            return None
    
    def get_equipped_title(self):
        from shop.models import Purchase, ShopItem
        try:
            purchase = Purchase.objects.get(
                user=self.user, 
                item__category='title',
                is_equipped=True
            )
            return purchase.item
        except Purchase.DoesNotExist:
            return None
    
    def get_equipped_background(self):
        from shop.models import Purchase, ShopItem
        try:
            purchase = Purchase.objects.get(
                user=self.user, 
                item__category='background',
                is_equipped=True
            )
            return purchase.item
        except Purchase.DoesNotExist:
            return None
    
    def get_equipped_effect(self):
        from shop.models import Purchase, ShopItem
        try:
            purchase = Purchase.objects.get(
                user=self.user, 
                item__category='effect',
                is_equipped=True
            )
            return purchase.item
        except Purchase.DoesNotExist:
            return None
    
    def get_active_boosts(self):
        from shop.models import ActiveBoost
        return ActiveBoost.objects.filter(
            user=self.user,
            expires_at__gt=models.functions.Now()
        )

class Medal(models.Model):
    MEDAL_TYPES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('legendary', 'Legendary'),
    ]
    
    profile = models.ForeignKey(Profile, related_name='medals', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    medal_type = models.CharField(max_length=20, choices=MEDAL_TYPES)
    acquired_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} ({self.medal_type})'

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
