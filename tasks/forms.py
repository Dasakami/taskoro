from django import forms
from .models import Task, TaskCategory

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'difficulty', 'deadline', 'estimated_minutes']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add magic-themed classes to the form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control magic-input'
        
        # Filter categories by user if provided
        if user:
            self.fields['category'].queryset = TaskCategory.objects.filter(user=user)

class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['name', 'description', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add magic-themed classes to the form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control magic-input'