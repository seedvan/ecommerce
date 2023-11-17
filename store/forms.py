from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create and associate a customer instance
            customer = Customer(user=user, name=user.username, email=user.email)
            customer.save()

        return user


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')


