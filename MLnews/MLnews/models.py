from django import forms
from django.db import models

class BotResponse(forms.Form):
    bot_res = forms.CharField(max_length=1000)
