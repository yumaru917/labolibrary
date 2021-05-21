from django.forms import ModelForm, CharField, TextInput, Textarea
from django import forms

from chat.models import ChatMessageBetweenUserAndUser


class SendMessageForUserForm(forms.ModelForm):
    class Meta:
        model = ChatMessageBetweenUserAndUser
        # fields = '__all__'
        fields = ('text',)
