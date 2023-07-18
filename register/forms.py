from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    #add different models

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]