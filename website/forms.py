from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, \
    UserChangeForm
from .models import User, Client, Contractor


class UserCreationForm(AuthUserCreationForm):
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


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ()


class ContractorCreationForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ()


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ()


class ContractorEditForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ()