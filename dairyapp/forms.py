from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')


class LoginForm(forms.Form):
    username = forms.EmailField(label="email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)




