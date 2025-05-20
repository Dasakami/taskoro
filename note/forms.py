from django import forms
from .models import Note, NoteCategory
from django_ckeditor_5.widgets import CKEditor5Widget

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'category', 'task', 'content']
        widgets = {
              "content": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="content"
              )
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