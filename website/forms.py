from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Client, Contractor


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ()


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ()
