from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Task, TaskCategory, BaseTask
from users.models import CharacterClass
from .forms import TaskForm, TaskCategoryForm, HabitForm, DailyForm
from django.db.models import Count


@login_required
def task_list(request):
    # Get filter parameters from request
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    status = request.GET.get('status')
    task_type = request.GET.get('type', 'all')
    
    # Get user's character classes
    user_classes = request.user.profile.character_classes.all()
    
    # Get base tasks related to user's classes
    base_tasks = []
    if user_classes.exists():
        # Find which base tasks have already been created for this user
        user_base_task_ids = Task.objects.filter(
            user=request.user, 
            base_task__isnull=False
        ).values_list('base_task_id', flat=True)
        
        # Get base tasks for the user's classes that haven't been created yet
        available_base_tasks = BaseTask.objects.filter(
            character_class__in=user_classes
        ).exclude(
            id__in=user_base_task_ids
        )
        
        if task_type != 'all':
            available_base_tasks = available_base_tasks.filter(task_type=task_type)
            
        base_tasks = available_base_tasks
    
    # Get user's custom tasks
    user_tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    # Apply type filter if provided
    if task_type != 'all':
        user_tasks = user_tasks.filter(task_type=task_type)
    
    # Apply category filter if provided
    if category_id:
        user_tasks = user_tasks.filter(category_id=category_id)
    
    # Apply difficulty filter if provided
    if difficulty:
        user_tasks = user_tasks.filter(difficulty=difficulty)
    
    # Apply status filter if provided
    if status:
        if status == 'overdue':
            user_tasks = user_tasks.filter(
                deadline__lt=timezone.now(),
                is_completed=False
            )
        else:
            user_tasks = user_tasks.filter(status=status)
    
    # Get all categories for filter dropdown
    categories = TaskCategory.objects.filter(user=request.user)
    
    # Get all character classes for display
    character_classes = CharacterClass.objects.all()
    
    context = {
        'base_tasks': base_tasks,
        'user_tasks': user_tasks,
        'categories': categories,
        'character_classes': character_classes,
        'difficulty_choices': Task.DIFFICULTY_CHOICES,
        'status_choices': Task.STATUS_CHOICES,
        'task_type_choices': Task.TASK_TYPE_CHOICES,
        'selected_category': category_id,
        'selected_difficulty': difficulty,
        'selected_status': status,
        'selected_type': task_type,
    }
    
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Задача "{task.title}" создана!')
            return redirect('tasks:tasks')
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'is_create': True})

@login_required
def create_from_base_task(request, base_task_id):
    base_task = get_object_or_404(BaseTask, id=base_task_id)
    
    # Check if user has the required character class
    if not request.user.profile.character_classes.filter(id=base_task.character_class.id).exists():
        messages.error(request, f'У вас нет доступа к заданиям класса "{base_task.character_class.name}"')
        return redirect('tasks:tasks')
    
    # Create a new task from the base task
    task = Task(
        title=base_task.title,
        description=base_task.description,
        user=request.user,
        base_task=base_task,
        character_class=base_task.character_class,
        difficulty=base_task.difficulty,
        task_type=base_task.task_type,
        estimated_minutes=base_task.estimated_minutes
    )
    
    # Set deadline and target date for daily goals
    if base_task.task_type == 'daily':
        task.target_date = timezone.now().date()
    
    task.save()
    messages.success(request, f'Задача "{task.title}" добавлена в ваш список!')
    return redirect('tasks:tasks')

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Задача "{task.title}" обновлена!')
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task, 'is_create': False})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, f'Задача "{task.title}" удалена!')
        return redirect('tasks:tasks')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    experience = task.complete_task()
    
    if experience > 0:
        messages.success(request, f'Задача "{task.title}" выполнена! Получено {experience} XP.')
    else:
        messages.info(request, 'Эта задача уже была выполнена ранее.')
    
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)  # redirect to relative URL from next parameter
    else:
        return redirect('tasks:tasks')  # example: redirect to task list page

@login_required
def habit_complete(request, habit_id):
    habit = get_object_or_404(Task, id=habit_id, user=request.user, task_type='habit')
    
    if habit.last_completed == timezone.now().date():
        messages.info(request, "Эта привычка уже была выполнена сегодня.")
        return redirect('tasks:habits_list')

    experience = habit.complete_task()

    if experience > 0:
        messages.success(request, f'Привычка "{habit.title}" выполнена! Получено {experience} XP.')
    else:
        messages.warning(request, 'Не удалось завершить привычку.')

    return redirect('tasks:habits_list')

@login_required
def daily_goals(request):
    today = timezone.now().date()
    selected_date = request.GET.get('date')
    
    if selected_date:
        try:
            selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today
    
    # Get daily goals for the selected date
    daily_goals = Task.objects.filter(
        user=request.user,
        task_type='daily',
        target_date=selected_date
    )
    
    # Get habits that should be tracked today
    habits = Task.objects.filter(
        user=request.user,
        task_type='habit'
    )
    
    context = {
        'daily_goals': daily_goals,
        'habits': habits,
        'today': today,
        'selected_date': selected_date,
    }
    
    return render(request, 'tasks/daily_goals.html', context)

@login_required
def habits_list(request):
    habits = Task.objects.filter(
        user=request.user,
        task_type='habit'
    ).order_by('-streak', 'title')
    
    context = {
        'habits': habits,
    }
    
    return render(request, 'tasks/habits_list.html', context)

def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            # Нужно добавить user
            habit.user = request.user
            habit.save()
            return redirect('tasks:habits_list')
    else:
        form = HabitForm()
    return render(request, 'tasks/habit_form.html', {'form': form})

def daily_create(request):
    if request.method == 'POST':
        form = DailyForm(request.POST)
        if form.is_valid():
            daily_goal = form.save(commit=False)
            daily_goal.user = request.user  # Обязательно укажи текущего пользователя
            daily_goal.save()
            return redirect('tasks:daily_goals')
    else:
        form = DailyForm()
    return render(request, 'tasks/daily_form.html', {'form': form})


@login_required
def habits_detail(request, habit_id):
    habit = get_object_or_404(Task, id=habit_id, user=request.user, task_type='habit')
    
    # Calculate completion rate for the last 30 days
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    completion_history = habit.completions.filter(
        completed_at__date__gte=thirty_days_ago
    ).order_by('completed_at__date')
    
    # Create a calendar of the last 30 days
    calendar_days = []
    current_date = thirty_days_ago
    while current_date <= timezone.now().date():
        calendar_days.append({
            'date': current_date,
            'completed': completion_history.filter(completed_at__date=current_date).exists()
        })
        current_date += timezone.timedelta(days=1)
    
    context = {
        'habit': habit,
        'calendar_days': calendar_days,
        'completion_rate': (len([day for day in calendar_days if day['completed']]) / 30) * 100
    }
    
    return render(request, 'tasks/habits_detail.html', context)


@login_required
def category_list(request):
    categories = TaskCategory.objects.filter(user=request.user).annotate(tasks_count=Count('tasks'))
    return render(request, 'tasks/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f'Категория "{category.name}" создана!')
            return redirect('tasks:categories')
    else:
        form = TaskCategoryForm()
    
    return render(request, 'tasks/category_form.html', {'form': form, 'is_create': True})

@login_required
def category_edit(request, category_id):
    category = get_object_or_404(TaskCategory, id=category_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Категория "{category.name}" обновлена!')
            return redirect('tasks:categories')
    else:
        form = TaskCategoryForm(instance=category)
    
    return render(request, 'tasks/category_form.html', {'form': form, 'category': category, 'is_create': False})

@login_required
def category_delete(request, category_id):
    category = get_object_or_404(TaskCategory, id=category_id, user=request.user)
    
    if request.method == 'POST':
        # Check if category has tasks
        tasks_count = category.tasks.count()
        
        category.delete()
        messages.success(request, f'Категория "{category.name}" удалена{f" вместе с {tasks_count} задачами" if tasks_count else ""}!')
        return redirect('tasks:categories')
    
    return render(request, 'tasks/category_confirm_delete.html', {'category': category})