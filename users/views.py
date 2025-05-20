from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from .models import Profile, Medal
from django.http import Http404
from django.contrib.auth.models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('main')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in after registration
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Welcome, Охотник {username}! Your account has been created.')
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    user_profile = request.user.profile
    medals = user_profile.medals.all()
    
    context = {
        'profile': user_profile,
        'medals': medals,
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile:profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'profile_form': profile_form,
    }
    
    return render(request, 'users/edit_profile.html', context)

@login_required
def view_other_profile(request, username):
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Пользователь не найден.")

    user_profile = other_user.profile
    medals = user_profile.medals.all()
    
    context = {
        'profile': user_profile,
        'medals': medals,
        'is_self': other_user == request.user
    }

    return render(request, 'users/profile.html', context)