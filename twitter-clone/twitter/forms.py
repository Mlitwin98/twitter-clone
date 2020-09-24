from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(ModelForm):
    username = forms.CharField(max_length=50, widget= forms.TextInput
                                                (attrs={'class': 'form-control mb-2',
                                                        'placeholder': 'Username'}))
    email = forms.EmailField(max_length=254, widget= forms.TextInput
                                                (attrs={'class': 'form-control mb-2',
                                                        'id':'email',
                                                        'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput
                                                (attrs={'class': 'form-control mb-2',
                                                        'id':'pwd',
                                                        'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')