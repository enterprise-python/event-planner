from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from eventplanner import settings
from .forms import ClientForm, UserForm, ContractorForm


class ClientFormView(View):
    user_form = UserForm
    client_form = ClientForm
    template_name = 'website/register_client.html'

    def get(self, request):
        user_form = self.user_form(None)
        client_form = self.client_form(None)

        return render(request, self.template_name, {
            'user_form': user_form,
            'client_form': client_form
        })

    def post(self, request):
        user_form = self.user_form(request.POST)
        client_form = self.client_form(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)

            client.user = user
            client.save()

            return HttpResponseRedirect(reverse('website:login'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'client_form': client_form
        })


class ContractorFormView(View):
    user_form = UserForm
    contractor_form = ContractorForm
    template_name = 'website/register_contractor.html'

    def get(self, request):
        user_form = self.user_form(None)
        contractor_form = self.contractor_form(None)

        return render(request, self.template_name, {
            'user_form': user_form,
            'contractor_form': contractor_form
        })

    def post(self, request):
        user_form = self.user_form(request.POST)
        contractor_form = self.contractor_form(request.POST)

        if user_form.is_valid() and contractor_form.is_valid():
            user = user_form.save()
            contractor = contractor_form.save(commit=False)

            contractor.user = user
            contractor.save()

            return HttpResponseRedirect(reverse('website:login'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'contractor_form': contractor_form
        })


class LoginFormView(View):
    template_name = 'website/login.html'
    login_form = AuthenticationForm

    def get(self, request):
        login_form = self.login_form(None)
        return render(request, self.template_name, {'login_form': login_form})

    def post(self, request):
        login_form = self.login_form(request, data=request.POST)
        if login_form.is_valid():
            if login_form.user_cache:
                login(request, login_form.user_cache)
                return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))

        return render(request, self.template_name, {'login_form': login_form})


@login_required
def user_logout(request):
    logout(request)
    HttpResponseRedirect(reverse('website:index'))
