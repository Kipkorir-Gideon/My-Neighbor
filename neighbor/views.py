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
    form = NeighborhoodForm(request.POST, request.FILES)
    if request.method == 'POST':
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
    form = RegisterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to = [to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration.')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_request(request):
    form = AuthenticationForm(request, data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('neighborhood')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')



def logout_request(request):
    logout(request)
    messages.info(request, "Logout successfully")
    return redirect('login')


@login_required
def profile(request):
    profile_form = ProfileForm(request.POST, instance = request.user.profile)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile information updated successfully.')
        return redirect('profile')
    profile_form = ProfileForm(instance=request.user.profile)
    form = NeighborhoodForm()
    return render(request, 'profile.html', {'form': form, 'profile_form': profile_form})



@login_required
def join_hood(request, neighborhood_id):
    neighborhood = get_object_or_404(Neighborhood, id=neighborhood_id)
    request.user.profile.neighborhood = neighborhood
    request.user.profile.save()
    return redirect('my_neighborhood', neighborhood_id = neighborhood.id)



@login_required
def my_neighborhood(request, neighborhood_id):
    neighborhood = Neighborhood.objects.get(id=neighborhood_id)
    post_form = PostForm(request.POST, request.FILES)
    business_form = BusinessForm(request.POST, request.FILES)
    form = NeighborhoodForm(request.POST, request.FILES)
    users = Profile.objects.filter(neighborhood=neighborhood)
    business = Business.objects.filter(neighborhood_id=neighborhood)
    posts = Post.objects.filter(neighborhood=neighborhood)
    current_user = request.user
    if request.method == 'POST':
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
        form = NeighborhoodForm()
        post_form = PostForm()
        business_form = BusinessForm()
        current_user = request.user
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        business = Business.objects.filter(neighborhood_id=neighborhood)
        users = Profile.objects.filter(neighborhood=neighborhood)
        posts = Post.objects.filter(neighborhood=neighborhood)
    return render(request, 'my_hood.html', {'form': form, 'post_form':post_form, 'business_form': business_form, 'users':users,'current_user':current_user, 'neighborhood':neighborhood,'business':business,'posts':posts})



@login_required
def leave_hood(request, neighborhood_id):
    neighborhood = get_object_or_404(Neighborhood, id=neighborhood_id)
    request.user.profile.neighborhood = None
    request.user.profile.save()
    return redirect('neighborhood')



@login_required
def search(request):
    if 'name' in request.GET and request.GET['name']:
        search_term = request.GET.get('name')
        search_buzz = Business.search_by_business_name(search_term)
        message = f"{search_term}"
        form = NeighborhoodForm()
        return render(request, 'search.html', {'message': message, 'buzz': search_buzz, "form":form})

    else:
        form = NeighborhoodForm()
        message = "You have not search for any business."
        return render(request, 'search.html', {'message': message, "form":form})
