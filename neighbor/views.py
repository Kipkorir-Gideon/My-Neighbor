from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
@ login_required
def neighborhood(request):
    return render(request, 'neighborhood.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('neighborhood')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm
    return render(request, 'registration/register.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('neighborhood')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logout successfully")
    return redirect('login')


@login_required
def profile(request, pk):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance = request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        user = User.objects.get(pk=pk)
        current_user = request.user
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profile.html', {'user': user, 'current_user': current_user, 'profile_form': profile_form})