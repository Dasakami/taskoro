from django import forms
from .models import Task, TaskCategory
from users.models import CharacterClass

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'category', 'character_class',
            'difficulty',  'deadline', 'estimated_minutes',
            # 'frequency', 'target_date'  # убираем эти поля
        ]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            # 'target_date': forms.DateInput(attrs={'type': 'date'}), # убрали
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['category'].queryset = TaskCategory.objects.filter(user=user)
            self.fields['character_class'].queryset = user.profile.character_classes.all()
        
        # Удаляем frequency и target_date, чтобы не показывать
        self.fields.pop('frequency', None)
        self.fields.pop('target_date', None)

class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['name', 'description', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CharacterClassForm(forms.Form):
    character_classes = forms.ModelMultipleChoiceField(
        queryset=CharacterClass.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Выберите классы, которые наиболее соответствуют вашим интересам"
    )

class HabitForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'category', 'character_class',
            'difficulty', 'estimated_minutes', 'frequency'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(HabitForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['category'].queryset = TaskCategory.objects.filter(user=user)
            self.fields['character_class'].queryset = user.profile.character_classes.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.task_type = 'habit'
        if commit:
            instance.save()
        return instance

class DailyForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'category', 'character_class',
            'difficulty', 'estimated_minutes', 'target_date'
        ]
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DailyForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['category'].queryset = TaskCategory.objects.filter(user=user)
            self.fields['character_class'].queryset = user.profile.character_classes.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.task_type = 'daily'
        if commit:
            instance.save()
        return instance
