from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.translation import ugettext_lazy as _


# Create your views here.

def registration_view(request):
    if request.POST:
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            # username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:

        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.POST:
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']  # JAKO USERNAME, BO TAK WYNIKA Z AuthenticationForm
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_data_change_view(request):
    user = CustomUser.objects.get(username=request.user)
    if request.POST:
        form = CustomUserChangeForm(request.POST, request.FILES)
        if form.is_valid():
            for field in form:
                print(field)
            print(make_password(form.password))
            user.password = make_password(form.password)
            user.save()
    else:
        form = CustomUserChangeForm()

    return render(request, 'accounts/change.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')
