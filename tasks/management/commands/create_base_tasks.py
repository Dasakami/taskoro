from django.core.management.base import BaseCommand
from users.models import CharacterClass
from tasks.models import BaseTask

class Command(BaseCommand):
    help = 'Creates default character classes and base tasks'

    def handle(self, *args, **kwargs):
        # Create character classes
        warrior, created = CharacterClass.objects.get_or_create(
            name="Воин",
            defaults={
                "description": "Физические задачи и тренировки",
                "icon": "⚔️",
                "color": "#ff3366"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created character class: {warrior.name}'))
        
        sage, created = CharacterClass.objects.get_or_create(
            name="Мудрец",
            defaults={
                "description": "Задачи, связанные с обучением и знаниями",
                "icon": "📚",
                "color": "#3366ff"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created character class: {sage.name}'))
        
        strategist, created = CharacterClass.objects.get_or_create(
            name="Стратег",
            defaults={
                "description": "Планирование, организация, продуктивность",
                "icon": "🧠",
                "color": "#33ff99"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created character class: {strategist.name}'))
        
        merchant, created = CharacterClass.objects.get_or_create(
            name="Купец",
            defaults={
                "description": "Финансы и материальное благополучие",
                "icon": "💰",
                "color": "#ffcc33"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created character class: {merchant.name}'))
        
        socialist, created = CharacterClass.objects.get_or_create(
            name="Социалист",
            defaults={
                "description": "Общение, социальные связи и поддержка",
                "icon": "👥",
                "color": "#ff66cc"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created character class: {socialist.name}'))
        
        creator, created = CharacterClass.objects.get_or_create(
            name="Творец",
            defaults={
                "description": "Креативность, самовыражение, хобби",
                "icon": "🎨",
                "color": "#9966ff"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created character class: {creator.name}'))
        
        # Create base tasks
        
        # Warrior tasks
        warrior_tasks = [
            {
                "title": "Тренировка силы",
                "description": "Выполнить силовую тренировку (отжимания, приседания, подтягивания)",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 45,
                "xp_reward": 40
            },
            {
                "title": "Пробежка",
                "description": "Пробежать минимум 3 км",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 30,
                "xp_reward": 30
            },
            {
                "title": "Растяжка",
                "description": "Выполнить комплекс растяжки утром или вечером",
                "difficulty": "easy",
                "task_type": "habit",
                "estimated_minutes": 15,
                "xp_reward": 20
            },
            {
                "title": "10,000 шагов",
                "description": "Пройти минимум 10,000 шагов за день",
                "difficulty": "medium",
                "task_type": "daily",
                "estimated_minutes": 90,
                "xp_reward": 35
            },
            {
                "title": "Эпическая тренировка",
                "description": "Выполнить полноценную тренировку в спортзале по всем группам мышц",
                "difficulty": "hard",
                "task_type": "one_time",
                "estimated_minutes": 90,
                "xp_reward": 80
            }
        ]
        
        # Sage tasks
        sage_tasks = [
            {
                "title": "Чтение книги",
                "description": "Прочитать минимум 30 страниц книги по саморазвитию или профессиональной тематике",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 45,
                "xp_reward": 40
            },
            {
                "title": "Изучение языка",
                "description": "Потратить 20 минут на изучение иностранного языка",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 20,
                "xp_reward": 30
            },
            {
                "title": "Прослушать подкаст",
                "description": "Прослушать образовательный подкаст",
                "difficulty": "easy",
                "task_type": "one_time",
                "estimated_minutes": 30,
                "xp_reward": 25
            },
            {
                "title": "Решение задач",
                "description": "Решить минимум 3 интеллектуальные задачи или головоломки",
                "difficulty": "medium",
                "task_type": "daily",
                "estimated_minutes": 30,
                "xp_reward": 35
            },
            {
                "title": "Онлайн-курс",
                "description": "Пройти один урок онлайн-курса по интересующей теме",
                "difficulty": "hard",
                "task_type": "habit",
                "estimated_minutes": 60,
                "xp_reward": 50
            }
        ]
        
        # Strategist tasks
        strategist_tasks = [
            {
                "title": "Планирование дня",
                "description": "Составить план на день с приоритетами и временными рамками",
                "difficulty": "easy",
                "task_type": "habit",
                "estimated_minutes": 15,
                "xp_reward": 25
            },
            {
                "title": "Еженедельный обзор",
                "description": "Проанализировать прошедшую неделю и составить план на следующую",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 45,
                "xp_reward": 50
            },
            {
                "title": "Техника Помодоро",
                "description": "Поработать в режиме 25 минут работы, 5 минут отдыха (минимум 4 цикла)",
                "difficulty": "medium",
                "task_type": "daily",
                "estimated_minutes": 120,
                "xp_reward": 40
            },
            {
                "title": "Организация рабочего места",
                "description": "Навести порядок на рабочем столе и организовать документы",
                "difficulty": "medium",
                "task_type": "one_time",
                "estimated_minutes": 45,
                "xp_reward": 35
            },
            {
                "title": "Стратегическое планирование",
                "description": "Составить план достижения важной цели на ближайшие 3 месяца",
                "difficulty": "hard",
                "task_type": "one_time",
                "estimated_minutes": 90,
                "xp_reward": 75
            }
        ]
        
        # Merchant tasks
        merchant_tasks = [
            {
                "title": "Учет расходов",
                "description": "Записать все расходы за день и категоризировать их",
                "difficulty": "easy",
                "task_type": "habit",
                "estimated_minutes": 10,
                "xp_reward": 20
            },
            {
                "title": "Финансовый обзор",
                "description": "Проанализировать финансы за месяц и составить бюджет на следующий",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 60,
                "xp_reward": 45
            },
            {
                "title": "Исследование инвестиций",
                "description": "Изучить одну потенциальную инвестиционную возможность",
                "difficulty": "medium",
                "task_type": "one_time",
                "estimated_minutes": 45,
                "xp_reward": 40
            },
            {
                "title": "Дополнительный заработок",
                "description": "Потратить час на развитие источника пассивного дохода",
                "difficulty": "hard",
                "task_type": "habit",
                "estimated_minutes": 60,
                "xp_reward": 50
            },
            {
                "title": "Оптимизация расходов",
                "description": "Найти способ сэкономить на регулярных расходах",
                "difficulty": "medium",
                "task_type": "one_time",
                "estimated_minutes": 30,
                "xp_reward": 35
            }
        ]
        
        # Socialist tasks
        socialist_tasks = [
            {
                "title": "Связь с близкими",
                "description": "Позвонить или написать родственнику или другу, с которым давно не общались",
                "difficulty": "easy",
                "task_type": "habit",
                "estimated_minutes": 15,
                "xp_reward": 20
            },
            {
                "title": "Нетворкинг",
                "description": "Познакомиться с новым человеком или укрепить профессиональный контакт",
                "difficulty": "medium",
                "task_type": "one_time",
                "estimated_minutes": 30,
                "xp_reward": 35
            },
            {
                "title": "Групповое мероприятие",
                "description": "Посетить мероприятие, где можно встретить единомышленников",
                "difficulty": "hard",
                "task_type": "one_time",
                "estimated_minutes": 120,
                "xp_reward": 60
            },
            {
                "title": "Помощь другим",
                "description": "Сделать что-то полезное для другого человека",
                "difficulty": "easy",
                "task_type": "daily",
                "estimated_minutes": 20,
                "xp_reward": 25
            },
            {
                "title": "Активное слушание",
                "description": "Практиковать активное слушание в разговоре без перебивания",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 30,
                "xp_reward": 30
            }
        ]
        
        # Creator tasks
        creator_tasks = [
            {
                "title": "Творческая практика",
                "description": "Уделить время своему хобби или творческому проекту",
                "difficulty": "medium",
                "task_type": "habit",
                "estimated_minutes": 45,
                "xp_reward": 40
            },
            {
                "title": "Новая техника",
                "description": "Попробовать новую технику или подход в своем творчестве",
                "difficulty": "medium",
                "task_type": "one_time",
                "estimated_minutes": 60,
                "xp_reward": 50
            },
            {
                "title": "Завершение проекта",
                "description": "Довести творческий проект до завершения",
                "difficulty": "hard",
                "task_type": "one_time",
                "estimated_minutes": 120,
                "xp_reward": 80
            },
            {
                "title": "Творческий дневник",
                "description": "Записать идеи и мысли в творческий дневник",
                "difficulty": "easy",
                "task_type": "habit",
                "estimated_minutes": 15,
                "xp_reward": 20
            },
            {
                "title": "Изучение работ мастера",
                "description": "Изучить работы признанного мастера в вашей творческой области",
                "difficulty": "medium",
                "task_type": "daily",
                "estimated_minutes": 30,
                "xp_reward": 35
            }
        ]
        
        # Create all tasks
        for task_data in warrior_tasks:
            BaseTask.objects.get_or_create(
                title=task_data["title"],
                character_class=warrior,
                defaults={
                    "description": task_data["description"],
                    "difficulty": task_data["difficulty"],
                    "task_type": task_data["task_type"],
                    "estimated_minutes": task_data["estimated_minutes"],
                    "xp_reward": task_data["xp_reward"]
                }
            )
        
        for task_data in sage_tasks:
            BaseTask.objects.get_or_create(
                title=task_data["title"],
                character_class=sage,
                defaults={
                    "description": task_data["description"],
                    "difficulty": task_data["difficulty"],
                    "task_type": task_data["task_type"],
                    "estimated_minutes": task_data["estimated_minutes"],
                    "xp_reward": task_data["xp_reward"]
                }
            )
        
        for task_data in strategist_tasks:
            BaseTask.objects.get_or_create(
                title=task_data["title"],
                character_class=strategist,
                defaults={
                    "description": task_data["description"],
                    "difficulty": task_data["difficulty"],
                    "task_type": task_data["task_type"],
                    "estimated_minutes": task_data["estimated_minutes"],
                    "xp_reward": task_data["xp_reward"]
                }
            )
        
        for task_data in merchant_tasks:
            BaseTask.objects.get_or_create(
                title=task_data["title"],
                character_class=merchant,
                defaults={
                    "description": task_data["description"],
                    "difficulty": task_data["difficulty"],
                    "task_type": task_data["task_type"],
                    "estimated_minutes": task_data["estimated_minutes"],
                    "xp_reward": task_data["xp_reward"]
                }
            )
        
        for task_data in socialist_tasks:
            BaseTask.objects.get_or_create(
                title=task_data["title"],
                character_class=socialist,
                defaults={
                    "description": task_data["description"],
                    "difficulty": task_data["difficulty"],
                    "task_type": task_data["task_type"],
                    "estimated_minutes": task_data["estimated_minutes"],
                    "xp_reward": task_data["xp_reward"]
                }
            )
        
        for task_data in creator_tasks:
            BaseTask.objects.get_or_create(
                title=task_data["title"],
                character_class=creator,
                defaults={
                    "description": task_data["description"],
                    "difficulty": task_data["difficulty"],
                    "task_type": task_data["task_type"],
                    "estimated_minutes": task_data["estimated_minutes"],
                    "xp_reward": task_data["xp_reward"]
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created all base tasks!'))