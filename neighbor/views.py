from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
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
        neighborhoods = Neighborhood.objects.all()
        neighborhoods = neighborhoods[::-1]
    return render(request, 'neighborhood.html', {'form': form, 'neighborhoods': neighborhoods})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('to_email')
            email = EmailMessage(email_subject, message, to = [to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration.')
    else:
        form = RegisterForm()
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
def join_hood(request, neighborhood_id):
    neighborhood = get_object_or_404(Neighborhood, id=neighborhood_id)
    request.user.profile.neighborhood = neighborhood
    request.user.profile.save()
    return redirect('my_neighborhood', neighborhood_id = neighborhood.id)



@login_required
def my_neighborhood(request, neighborhood_id):
    neighborhood = Neighborhood.objects.get(id=neighborhood_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        business_form = BusinessForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.neighborhood = neighborhood
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been added successfully.')
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.neighborhood = neighborhood
            business.user = request.user
            business.save()
            messages.success(request, 'Business added successfully.')
            return redirect('my_neighborhood', neighborhood_id)
    else:
        post_form = PostForm()
        business_form = BusinessForm()
        current_user = request.user
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        business = Business.objects.filter(neighborhood_id=neighborhood)
        users = Profile.objects.filter(neighborhood=neighborhood)
        posts = Post.objects.filter(neighborhood=neighborhood)
    return render(request, 'my_hood.html', {'post_form':post_form, 'business_form': business_form, 'users':users,'current_user':current_user, 'neighborhood':neighborhood,'business':business,'posts':posts})



@login_required
def leave_hood(request, neighborhood_id):
    neighborhood = get_object_or_404(Neighborhood, id=neighborhood_id)
    request.user.profile.neighborhood = None
    request.user.profile.save()
    return redirect('neighborhood')