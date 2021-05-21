from django import forms
from django.core.mail import EmailMessage


class ContactForm(forms.Form):
    inquiry = forms.CharField(label='ベータ版へのフィードバック', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_email(self):
        inquiry = self.cleaned_data['inquiry']

        message = EmailMessage(subject="ユーザーからベータ版へのフィードバックが届きました。",
                               body=inquiry,
                               from_email="lablib2021@gmail.com",
                               to=["lablib2021@gmail.com"],
                               )
        message.send()
