from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form labels and help text
        self.fields['username'].label = 'Имя охотника'
        self.fields['username'].help_text = 'Имя, которое будут видеть другие игроки.'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя охотника')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'theme_preference']
        labels = {
            'avatar': 'Аватар',
            'bio': 'О себе',
            'theme_preference': 'Тема интерфейса'
        }