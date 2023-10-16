from django import forms
from django.db import models

class BotResponse(forms.Form):
    bot_res = forms.CharField(max_length=1000)

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}"