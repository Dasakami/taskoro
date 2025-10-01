from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from .models import CharacterClass

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    selected_class = forms.ModelChoiceField(
        queryset=CharacterClass.objects.all(),
        label='Выберите класс персонажа',
        help_text='Выберите класс, который будет определять ваши способности и стиль игры.',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'selected_class']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя охотника'
        self.fields['username'].help_text = 'Имя, которое будут видеть другие игроки.'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['selected_class'].label = 'Класс персонажа'

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