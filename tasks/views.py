from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Task, TaskCategory, BaseTask, BaseTaskCompletion
from .forms import TaskForm, TaskCategoryForm, DailyForm, HabitForm
from history.models import ActivityLog
from tournaments.models import TournamentParticipant



@login_required
def task_list(request):
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    status = request.GET.get('status')
    task_type = request.GET.get('type', 'all')
    
    user_tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    if task_type != 'all':
        user_tasks = user_tasks.filter(task_type=task_type)
    
    if category_id:
        user_tasks = user_tasks.filter(category_id=category_id)

    if difficulty:
        user_tasks = user_tasks.filter(difficulty=difficulty)

    if status:
        if status == 'overdue':
            user_tasks = user_tasks.filter(
                deadline__lt=timezone.now(),
                is_completed=False
            )
        else:
            user_tasks = user_tasks.filter(status=status)
    

    categories = TaskCategory.objects.filter(user=request.user)
    
    context = {
        'user_tasks': user_tasks,
        'categories': categories,
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
def class_tasks_list(request):
    user_classes = request.user.profile.character_classes.all()

    task_type = request.GET.get('type', 'all')
    difficulty = request.GET.get('difficulty')
    character_class = request.GET.get('class')
    
    base_tasks = BaseTask.objects.filter(character_class__in=user_classes)
    
    if task_type != 'all':
        base_tasks = base_tasks.filter(task_type=task_type)
    
    if difficulty:
        base_tasks = base_tasks.filter(difficulty=difficulty)
    
    if character_class:
        base_tasks = base_tasks.filter(character_class_id=character_class)
    
    today = timezone.now().date()
    completed_tasks = request.user.completed_base_tasks.filter(
        completed_at__date=today
    ).values_list('base_task_id', flat=True)
    
    context = {
        'base_tasks': base_tasks,
        'character_classes': user_classes,
        'completed_tasks': completed_tasks,
        'difficulty_choices': BaseTask.DIFFICULTY_CHOICES,
        'task_type_choices': BaseTask.TASK_TYPE_CHOICES,
        'selected_type': task_type,
        'selected_difficulty': difficulty,
        'selected_class': character_class,
    }
    
    return render(request, 'tasks/class_tasks_list.html', context)

@login_required
def class_task_detail(request, task_id):
    base_task = get_object_or_404(BaseTask, id=task_id)
    
    if not request.user.profile.character_classes.filter(id=base_task.character_class.id).exists():
        messages.error(request, f'У вас нет доступа к заданиям класса "{base_task.character_class.name}"')
        return redirect('tasks:class_tasks')
    
    completion_history = BaseTaskCompletion.objects.filter(
        user=request.user,
        base_task=base_task
    ).order_by('-completed_at')

    today = timezone.now().date()
    completed_today = completion_history.filter(completed_at__date=today).exists()
    
    streak = 0
    last_date = None
    
    for completion in completion_history:
        completion_date = completion.completed_at.date()
        
        if last_date is None:
            streak = 1
        elif (last_date - completion_date).days == 1:
            streak += 1
        else:
            break
            
        last_date = completion_date
    
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    completions_last_30_days = completion_history.filter(
        completed_at__date__gte=thirty_days_ago
    ).values_list('completed_at__date', flat=True).distinct().count()
    
    completion_rate = (completions_last_30_days / 30) * 100 if completions_last_30_days > 0 else 0
    
    context = {
        'task': base_task,
        'completion_history': completion_history[:10],  
        'completed_today': completed_today,
        'streak': streak,
        'completion_rate': completion_rate,
        'completions_last_30_days': completions_last_30_days
    }
    
    return render(request, 'tasks/class_task_detail.html', context)

@login_required
def class_task_completed(request):
    character_class = request.GET.get('class')
    difficulty = request.GET.get('difficulty')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    user_classes = request.user.profile.character_classes.all()
    
    completions = BaseTaskCompletion.objects.filter(
        user=request.user
    ).select_related('base_task', 'base_task__character_class').order_by('-completed_at')
    
    if character_class:
        completions = completions.filter(base_task__character_class_id=character_class)
    
    if difficulty:
        completions = completions.filter(base_task__difficulty=difficulty)
    
    if date_from:
        try:
            date_from = timezone.datetime.strptime(date_from, '%Y-%m-%d').date()
            completions = completions.filter(completed_at__date__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = timezone.datetime.strptime(date_to, '%Y-%m-%d').date()
            completions = completions.filter(completed_at__date__lte=date_to)
        except ValueError:
            pass
    

    completion_dates = {}
    for completion in completions:
        date = completion.completed_at.date()
        if date not in completion_dates:
            completion_dates[date] = []
        
        completion_dates[date].append(completion)
    
    context = {
        'completion_dates': completion_dates,
        'character_classes': user_classes,
        'difficulty_choices': BaseTask.DIFFICULTY_CHOICES,
        'selected_class': character_class,
        'selected_difficulty': difficulty,
        'date_from': date_from if date_from else '',
        'date_to': date_to if date_to else '',
    }
    
    return render(request, 'tasks/class_task_completed.html', context)

@login_required
def complete_class_task(request, task_id):
    base_task = get_object_or_404(BaseTask, id=task_id)
    
    if not request.user.profile.character_classes.filter(id=base_task.character_class.id).exists():
        messages.error(request, f'У вас нет доступа к заданиям класса "{base_task.character_class.name}"')
        return redirect('tasks:class_tasks')
    
    today = timezone.now().date()
    if request.user.completed_base_tasks.filter(
        base_task=base_task,
        completed_at__date=today
    ).exists():
        messages.info(request, 'Эта задача уже была выполнена сегодня.')
        return redirect('tasks:class_tasks')
    

    completion = BaseTaskCompletion.objects.create(
        user=request.user,
        base_task=base_task,
        completed_at=timezone.now()
    )
    

    profile = request.user.profile
    experience = base_task.xp_reward
    profile.add_experience(experience)
    profile.coins += int(experience / 4)
    profile.save()
    
    ActivityLog.objects.create(
        user=request.user,
        activity_type='class_task_complete',
        description=f'Выполнил задачу класса: {base_task.title}',
        experience_gained=experience,
        coins_gained=int(experience / 4),
        gems_gained=0
    )
    
    messages.success(
        request,
        f'Задача "{base_task.title}" выполнена! Получено {experience} XP и {int(experience/4)} монет.'
    )
    
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect('tasks:class_tasks')

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
        task_type = request.GET.get('type', 'one_time')
        form = TaskForm(user=request.user, initial={'task_type': task_type})
    
    return render(request, 'tasks/task_form.html', {'form': form, 'is_create': True})

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
        ActivityLog.objects.create(
            user=request.user,
            activity_type='task_complete',
            description=f'Выполнил задачу: {task.title}',
            experience_gained=experience,
            coins_gained=task.coins if hasattr(task, 'coins') else 0,
            gems_gained=task.gems if hasattr(task, 'gems') else 0,
            task=task
        )

        active_participations = TournamentParticipant.objects.filter(
            user=request.user,
            tournament__start_date__lte=timezone.now(),
            tournament__end_date__gte=timezone.now()
        )
        
        for participation in active_participations:
            participation.update_score(new_task_count=1)
        
    else:
        messages.info(request, 'Эта задача уже была выполнена ранее.')
    
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url) 
    else:
        return redirect('tasks:tasks') 

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

    daily_goals = Task.objects.filter(
        user=request.user,
        task_type='daily',
        target_date=selected_date
    )
    
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
        tasks_count = category.tasks.count()
        
        category.delete()
        messages.success(request, f'Категория "{category.name}" удалена{f" вместе с {tasks_count} задачами" if tasks_count else ""}!')
        return redirect('tasks:categories')
    
    return render(request, 'tasks/category_confirm_delete.html', {'category': category})


@login_required
def habits_detail(request, habit_id):
    habit = get_object_or_404(Task, id=habit_id, user=request.user, task_type='habit')
    
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    completion_history = habit.completions.filter(
        completed_at__date__gte=thirty_days_ago
    ).order_by('completed_at__date')
    
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

def daily_create(request):
    if request.method == 'POST':
        form = DailyForm(request.POST)
        if form.is_valid():
            daily_goal = form.save(commit=False)
            daily_goal.user = request.user 
            daily_goal.save()
            return redirect('tasks:daily_goals')
    else:
        form = DailyForm()
    return render(request, 'tasks/daily_form.html', {'form': form})

def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('tasks:habits_list')
    else:
        form = HabitForm()
    return render(request, 'tasks/habit_form.html', {'form': form})

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


