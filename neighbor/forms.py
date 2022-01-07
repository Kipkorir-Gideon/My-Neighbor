from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name', 'username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio', 'email', 'neighborhood')


class NeighborhoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        exclude = ('admin',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description','photo', 'neighborhood','user')


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 'email','photo', 'description', 'owner', 'neighborhood_id')