# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import UserAccountManager

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = UserAccountManager
        fields = ('email', 'first_name', 'last_name', 'mobile', 'address')

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = UserAccountManager
        fields = ('email', 'first_name', 'last_name', 'mobile', 'address')
