from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm
from .models import CustomUser


# Create your views here.

def registration_view(request):
    if request.POST:
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
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

    form = CustomUserLoginForm(request.POST or None, data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['username']  # JAKO USERNAME, BO TAK WYNIKA Z AuthenticationForm
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('index')

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_data_change_view(request):
    user = CustomUser.objects.get(username=request.user)
    form = CustomUserChangeForm(request.POST or None, request.FILES)
    if request.POST:
        user.image = request.FILES['image']
        user.save()
        return redirect('index')

    return render(request, 'accounts/change.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')
