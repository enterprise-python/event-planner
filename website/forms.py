from django import forms
from django.core.exceptions import ValidationError

from .models import Client


class ClientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmed_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'confirmed_password']

    def clean(self):
        data = super().clean()
        password = data['password']
        confirmed_password = data['confirmed_password']

        if password != confirmed_password:
            raise ValidationError('Passwords must match')

        return data
