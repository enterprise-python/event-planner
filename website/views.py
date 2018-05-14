from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from website.models import Role
from .forms import ClientCreationForm, UserCreationForm, ContractorCreationForm


class ClientRegistrationView(View):
    user_form = UserCreationForm
    client_form = ClientCreationForm
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
            user.role = Role.CLIENT.value
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            return HttpResponseRedirect(reverse('website:login'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'client_form': client_form
        })


class ContractorRegistrationView(View):
    user_form = UserCreationForm
    contractor_form = ContractorCreationForm
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
            user.role = Role.CONTRACTOR.value
            user.save()

            contractor = contractor_form.save(commit=False)
            contractor.user = user
            contractor.save()

            return HttpResponseRedirect(reverse('website:login'))

        return render(request, self.template_name, {
            'user_form': user_form,
            'contractor_form': contractor_form
        })
