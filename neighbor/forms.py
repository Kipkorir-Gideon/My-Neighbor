from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio', 'email', 'neighborhood', 'location')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description')


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'email')