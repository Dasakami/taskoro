
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, NoteCategory
from .forms import NoteForm, NoteCategoryForm
from django.contrib import messages
from django.db.models import Q

@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'note/notes_list.html', {'notes': notes})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'note/note_detail.html', {'note': note})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note:notes_list')
    else:
        form = NoteForm()
    return render(request, 'note/note_form.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note:notes_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note/note_form.html', {'form': form})

@login_required
def create_note_category(request):
    if request.method == 'POST':
        form = NoteCategoryForm(request.POST)
        if form.is_valid():
            note_category = form.save(commit=False)
            note_category.user = request.user
            note_category.save()
            return redirect('note:category_list')  # или куда надо после создания
    else:
        form = NoteCategoryForm()

    return render(request, 'note/create_category.html', {'form': form})

def category_list(request):
    categories = NoteCategory.objects.filter(user=request.user)
    return render(request, 'note/category_list.html', {'categories': categories})