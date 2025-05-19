from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Task, TaskCategory
from .forms import TaskForm, TaskCategoryForm
from django.db.models import Count

def task_list(request):
    # Get filter parameters from request
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    status = request.GET.get('status')
    
    # Start with all user's tasks
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    # Apply filters if provided
    if category_id:
        tasks = tasks.filter(category_id=category_id)
    
    if difficulty:
        tasks = tasks.filter(difficulty=difficulty)
    
    if status:
        if status == 'overdue':
            tasks = tasks.filter(
                deadline__lt=timezone.now(),
                is_completed=False
            )
        else:
            tasks = tasks.filter(status=status)
    
    # Get all categories for filter dropdown
    categories = TaskCategory.objects.filter(user=request.user)
    
    context = {
        'tasks': tasks,
        'categories': categories,
        'difficulty_choices': Task.DIFFICULTY_CHOICES,
        'status_choices': Task.STATUS_CHOICES,
        'selected_category': category_id,
        'selected_difficulty': difficulty,
        'selected_status': status,
    }
    
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    return render(request, 'tasks/task_detail.html', {'task': task})

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


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, f'Задача "{task.title}" удалена!')
        return redirect('tasks:tasks')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    experience = task.complete_task()
    
    if experience > 0:
        messages.success(request, f'Задача "{task.title}" выполнена! Получено {experience} XP.')
    else:
        messages.info(request, 'Эта задача уже была выполнена ранее.')
    
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)  # редирект по относительному URL из параметра next
    else:
        return redirect('tasks:list')  # пример: редирект на страницу списка задач



def category_list(request):
    categories = TaskCategory.objects.filter(user=request.user).annotate(tasks_count=Count('tasks'))
    return render(request, 'tasks/category_list.html', {'categories': categories})


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


def category_delete(request, category_id):
    category = get_object_or_404(TaskCategory, id=category_id, user=request.user)
    
    if request.method == 'POST':
        # Check if category has tasks
        tasks_count = category.tasks.count()
        
        category.delete()
        messages.success(request, f'Категория "{category.name}" удалена{f" вместе с {tasks_count} задачами" if tasks_count else ""}!')
        return redirect('tasks:categories')
    
    return render(request, 'tasks/category_confirm_delete.html', {'category': category})