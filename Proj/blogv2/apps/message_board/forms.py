from django import forms
from .models import MessageBoardModel

class MessageBoardModelForm(forms.ModelForm):
    class Meta:
        model = MessageBoardModel
        fields = ['email', 'content']
        