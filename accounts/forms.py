from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'image',)


class CustomUserChangeForm(UserChangeForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = ('image',)


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password',)
