from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm

from .models import Business, Client, Contractor, Event, Opinion, User


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


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class UserEditAvatarForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'avatar',
        )


class ClientEditForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ()


class ContractorEditForm(forms.ModelForm):

    class Meta:
        model = Contractor
        fields = ()


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'title',
            'date_from',
            'date_to',
            'businesses'
        )


class BusinessForm(forms.ModelForm):

    class Meta:
        model = Business
        fields = (
            'name',
            'business_type',
            'description'
        )


class CreateOpinionForm(forms.ModelForm):

    class Meta:
        model = Opinion
        fields = (
            'text',
            'rating'
        )
