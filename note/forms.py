from django import forms
from .models import Note, NoteCategory

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'category', 'task', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'id': 'markdown-editor'}),
        }

class NoteCategoryForm(forms.ModelForm):
    class Meta:
        model = NoteCategory
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Краткое описание категории (не обязательно)',
                'rows': 3,
            }),
        }