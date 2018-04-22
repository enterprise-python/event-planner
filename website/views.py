from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

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
            user = user_form.save(commit=False)
            client = client_form.save(commit=False)
            user_data = user_form.clean()

            username = user_data['username']
            password = user_data['password']
            user.set_password(password)
            user.save()
            client.save()

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('website:index'))

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
            user = user_form.save(commit=False)
            contractor = contractor_form.save(commit=False)
            user_data = user_form.clean()

            username = user_data['username']
            password = user_data['password']
            user.set_password(password)
            user.save()
            contractor.save()

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('website:index'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'contractor_form': contractor_form
        })
