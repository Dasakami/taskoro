from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add magic-themed classes to the form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control magic-input'
            
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add magic-themed classes to the form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control magic-input'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'title', 'theme_preference']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add magic-themed classes to the form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control magic-input'