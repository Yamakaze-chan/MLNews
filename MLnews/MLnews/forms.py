from django import forms
from django.db import models
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class Watch_later_info(models.Model):
    title = models.CharField(max_length=1000)
    guid = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    image_content = models.CharField(max_length=1000)
    published_date = models.DateTimeField(default=timezone.now)
    save_account = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-published_date']

class Watch_later(forms.ModelForm):
    class Meta:
        model = Watch_later_info
        fields = '__all__'

