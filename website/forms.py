from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Client, Contractor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmed_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirmed_password']

    def clean(self):
        data = super().clean()
        password = data['password']
        confirmed_password = data['confirmed_password']

        if password != confirmed_password:
            raise ValidationError('Passwords must match')

        return data


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = []


class ContractorForm(forms.ModelForm):

    class Meta:
        model = Contractor
        fields = []
