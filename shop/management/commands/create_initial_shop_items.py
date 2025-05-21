from django.core.management.base import BaseCommand
from shop.models import ShopItem, Chest
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates initial shop items for the store'

    def handle(self, *args, **options):
        # Create titles
        titles = [
            {
                'name': 'Легенда',
                'description': 'Титул "Легенда" для настоящих героев.',
                'price': 1000,
                'currency': 'coins',
                'title_text': 'Легенда',
                'title_color': '#FFD700',
            },
            {
                'name': 'Мастер',
                'description': 'Титул "Мастер" для тех, кто достиг совершенства.',
                'price': 800,
                'currency': 'coins',
                'title_text': 'Мастер',
                'title_color': '#3B82F6',
            },
            {
                'name': 'Тень',
                'description': 'Таинственный титул "Тень" для самых скрытных.',
                'price': 50,
                'currency': 'gems',
                'title_text': 'Тень',
                'title_color': '#6B21A8',
            },
            {
                'name': 'Непобедимый',
                'description': 'Титул "Непобедимый" для тех, кто никогда не сдается.',
                'price': 75,
                'currency': 'gems',
                'title_text': 'Непобедимый',
                'title_color': '#DC2626',
            },
        ]
        
        for title_data in titles:
            ShopItem.objects.get_or_create(
                name=title_data['name'],
                defaults={
                    'description': title_data['description'],
                    'price': title_data['price'],
                    'currency': title_data['currency'],
                    'category': 'title',
                    'title_text': title_data['title_text'],
                    'title_color': title_data['title_color'],
                }
            )
        
        # Create avatar frames
        frames = [
            {
                'name': 'Золотая рамка',
                'description': 'Роскошная золотая рамка для вашего аватара.',
                'price': 1500,
                'currency': 'coins',
                'frame_style': 'gold',
            },
            {
                'name': 'Огненная рамка',
                'description': 'Пылающая рамка для самых горячих аватаров.',
                'price': 100,
                'currency': 'gems',
                'frame_style': 'fire',
            },
            {
                'name': 'Ледяная рамка',
                'description': 'Морозная рамка для холодных профессионалов.',
                'price': 100,
                'currency': 'gems',
                'frame_style': 'ice',
            },
            {
                'name': 'Электрическая рамка',
                'description': 'Рамка с электрическими разрядами для самых энергичных.',
                'price': 120,
                'currency': 'gems',
                'frame_style': 'electric',
            },
        ]
        
        for frame_data in frames:
            ShopItem.objects.get_or_create(
                name=frame_data['name'],
                defaults={
                    'description': frame_data['description'],
                    'price': frame_data['price'],
                    'currency': frame_data['currency'],
                    'category': 'avatar_frame',
                    'frame_style': frame_data['frame_style'],
                }
            )
        
        # Create background themes
        backgrounds = [
            {
                'name': 'Ночное небо',
                'description': 'Фон с красивым звездным небом для вашего профиля.',
                'price': 1200,
                'currency': 'coins',
            },
            {
                'name': 'Городской пейзаж',
                'description': 'Стильный городской фон для вашего профиля.',
                'price': 1000,
                'currency': 'coins',
            },
            {
                'name': 'Космическая станция',
                'description': 'Футуристический фон космической станции.',
                'price': 85,
                'currency': 'gems',
            },
            {
                'name': 'Магический лес',
                'description': 'Таинственный фон с магическим лесом.',
                'price': 90,
                'currency': 'gems',
            },
        ]
        
        for bg_data in backgrounds:
            ShopItem.objects.get_or_create(
                name=bg_data['name'],
                defaults={
                    'description': bg_data['description'],
                    'price': bg_data['price'],
                    'currency': bg_data['currency'],
                    'category': 'background',
                }
            )
        
        # Create visual effects
        effects = [
            {
                'name': 'Огненный след',
                'description': 'Оставляет огненный след при навигации по сайту.',
                'price': 2000,
                'currency': 'coins',
            },
            {
                'name': 'Сверкающие частицы',
                'description': 'Добавляет сверкающие частицы вокруг вашего аватара.',
                'price': 150,
                'currency': 'gems',
            },
        ]
        
        for effect_data in effects:
            ShopItem.objects.get_or_create(
                name=effect_data['name'],
                defaults={
                    'description': effect_data['description'],
                    'price': effect_data['price'],
                    'currency': effect_data['currency'],
                    'category': 'effect',
                }
            )
        
        # Create boosters
        boosters = [
            {
                'name': 'Ускоритель опыта x2',
                'description': 'Удваивает получаемый опыт на 24 часа.',
                'price': 500,
                'currency': 'coins',
                'boost_multiplier': 2.0,
                'boost_duration': 24,
            },
            {
                'name': 'Ускоритель опыта x3',
                'description': 'Утраивает получаемый опыт на 12 часов.',
                'price': 50,
                'currency': 'gems',
                'boost_multiplier': 3.0,
                'boost_duration': 12,
            },
            {
                'name': 'Ускоритель монет x2',
                'description': 'Удваивает получаемые монеты на 24 часа.',
                'price': 500,
                'currency': 'coins',
                'boost_multiplier': 2.0,
                'boost_duration': 24,
            },
            {
                'name': 'Ускоритель монет x3',
                'description': 'Утраивает получаемые монеты на 12 часов.',
                'price': 50,
                'currency': 'gems',
                'boost_multiplier': 3.0,
                'boost_duration': 12,
            },
        ]
        
        for boost_data in boosters:
            ShopItem.objects.get_or_create(
                name=boost_data['name'],
                defaults={
                    'description': boost_data['description'],
                    'price': boost_data['price'],
                    'currency': boost_data['currency'],
                    'category': 'boost',
                    'boost_multiplier': boost_data['boost_multiplier'],
                    'boost_duration': boost_data['boost_duration'],
                }
            )
        
        # Create chests
        chests = [
            {
                'name': 'Сундук новичка',
                'description': 'Базовый сундук с небольшим количеством ресурсов.',
                'rarity': 'common',
                'price_coins': 200,
                'price_gems': 0,
                'min_coins_reward': 100,
                'max_coins_reward': 300,
                'min_gems_reward': 1,
                'max_gems_reward': 5,
            },
            {
                'name': 'Сундук странника',
                'description': 'Сундук с хорошими наградами для опытных игроков.',
                'rarity': 'rare',
                'price_coins': 500,
                'price_gems': 5,
                'min_coins_reward': 300,
                'max_coins_reward': 700,
                'min_gems_reward': 5,
                'max_gems_reward': 15,
            },
            {
                'name': 'Эпический сундук',
                'description': 'Редкий сундук с отличными наградами.',
                'rarity': 'epic',
                'price_coins': 1000,
                'price_gems': 20,
                'min_coins_reward': 700,
                'max_coins_reward': 1500,
                'min_gems_reward': 15,
                'max_gems_reward': 35,
            },
            {
                'name': 'Легендарный сундук',
                'description': 'Самый ценный сундук с невероятными наградами.',
                'rarity': 'legendary',
                'price_coins': 2000,
                'price_gems': 50,
                'min_coins_reward': 1500,
                'max_coins_reward': 3000,
                'min_gems_reward': 40,
                'max_gems_reward': 100,
            },
        ]
        
        for chest_data in chests:
            Chest.objects.get_or_create(
                name=chest_data['name'],
                defaults={
                    'description': chest_data['description'],
                    'rarity': chest_data['rarity'],
                    'price_coins': chest_data['price_coins'],
                    'price_gems': chest_data['price_gems'],
                    'min_coins_reward': chest_data['min_coins_reward'],
                    'max_coins_reward': chest_data['max_coins_reward'],
                    'min_gems_reward': chest_data['min_gems_reward'],
                    'max_gems_reward': chest_data['max_gems_reward'],
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created initial shop items'))