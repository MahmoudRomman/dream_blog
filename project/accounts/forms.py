from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models
from accounts import models


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['name', 'username', 'email', 'avatar']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = ['name', 'username', 'avatar']