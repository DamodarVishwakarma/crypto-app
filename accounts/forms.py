from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        return user

class AdminUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin_user = True
        user.is_staff = True
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']