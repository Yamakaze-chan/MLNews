from django import forms
from django.db import models
from .models import BotResponse

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = BotResponse
        # exclude = ['author', 'updated', 'created', ]
        fields = ['bot_res']
        widgets = {
            'bot_res': forms.TextInput(attrs={
                'id': 'post-text', 
                'required': True, 
                'placeholder': 'Say something...'
            })
        }