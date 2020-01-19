from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('name','contact', 'address', 'city','state', 'dob','adhaar','role')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('name','contact', 'address', 'city','state', 'dob','adhaar','role')