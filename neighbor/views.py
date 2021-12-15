from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
@ login_required
def neighborhood(request):
    return render(request, 'neighborhood.html')


@login_required
def profile(request, pk):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance = request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        user = User.objects.get(pk=pk)
        current_user = request.user
        profile_form = ProfileForm()
        return render(request, 'profile.html', {'user': user, 'current_user': current_user, 'profile_form': profile_form})