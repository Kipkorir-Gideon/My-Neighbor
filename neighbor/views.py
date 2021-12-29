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
    if request.method == 'POST':
        form = NeighborhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighborhood = form.save(commit=False)
            neighborhood.admin = request.user.profile
            neighborhood.save()
            messages.success(request,'Neighborhood created successfully.')
            return redirect('neighborhood')
    else:
        form = NeighborhoodForm()
    return render(request, 'neighborhood.html', {'form': form})


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
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance = request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile information updated successfully.')
        return redirect('profile')
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'profile_form': profile_form})



@login_required
def my_neighborhood(request, neighborhood_id):
    neighborhood = Neighborhood.objects.get(id=neighborhood_id)
    if request.method == 'POST':
        business_form = BusinessForm(request.POST, request.FILES)
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.neighborhood = neighborhood
            business.user = request.user
            business.save()
            return redirect('my_neighborhood', neighborhood_id)
    else:
        business_form = BusinessForm()
        current_user = request.user
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        business = Business.objects.filter(neighborhood=neighborhood)
        users = Profile.objects.filter(neighborhood=neighborhood)
        posts = Post.objects.filter(neighborhood=neighborhood)
    return render(request, 'my_hood.html', {'business_form': business_form, 'users':users,'current_user':current_user, 'neighborhood':neighborhood,'business':business,'posts':posts})