from django.contrib.auth.models import User
from django import forms
from .models import *

class UserForm(forms.ModelForm):
    username = forms.CharField(required = True, widget = forms.TextInput(attrs = {
        'placeholder' : 'Username', 
        'class': 'gray form-button'
    }))
    email = forms.EmailField(required = True, widget = forms.EmailInput(attrs = {
        'placeholder' : 'Email', 
        'class': 'gray form-button'
    }))
    password = forms.CharField(required = True, widget = forms.PasswordInput(attrs = {
        'placeholder' : 'Password', 
        'class': 'gray form-button',
        'id': 'password'
    }))
    reenter = forms.CharField(required = True, widget = forms.PasswordInput(attrs = {
        'placeholder' : 'Re-Enter Password', 
        'class': 'gray form-button',
        'id': 'confirm'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    fname = forms.CharField(required = True, widget = forms.TextInput(attrs = {
        'placeholder' : 'First Name', 
        'class': 'gray form-button'
    }))
    lname = forms.CharField(widget = forms.TextInput(attrs = {
        'placeholder' : 'Last Name', 
        'class': 'gray form-button'
    }))

    class Meta:
        model = Profile
        fields = ('fname', 'lname')

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required = True, widget = forms.TextInput(attrs = {
        'placeholder' : 'Username', 
        'class': 'gray form-button'
    }))
    email = forms.EmailField(required = True, widget = forms.EmailInput(attrs = {
        'placeholder' : 'Email', 
        'class': 'gray form-button'
    }))

    class Meta:
        model = User
        fields = ('username', 'email')

class UpdateProfileForm(forms.ModelForm):
    fname = forms.CharField(required = True, widget = forms.TextInput(attrs = {
        'placeholder' : 'First Name', 
        'class': 'gray form-button'
    }))
    lname = forms.CharField(widget = forms.TextInput(attrs = {
        'placeholder' : 'Last Name', 
        'class': 'gray form-button'
    }))

    class Meta:
        model = Profile
        fields = ('fname', 'lname', 'avatar')