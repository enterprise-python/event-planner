from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView

from website.models import Role
from .forms import ClientCreationForm, UserCreationForm, ContractorCreationForm, \
    UserEditForm, ClientEditForm


class ClientRegistrationView(View):
    user_form = UserCreationForm
    client_form = ClientCreationForm
    template_name = 'website/pages/register_client.html'

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
    template_name = 'website/pages/register_contractor.html'

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


@method_decorator(login_required, name='dispatch')
class ClientEditView(UpdateView):
    user_edit_form = UserEditForm
    client_edit_form = ClientEditForm
    change_password_form = PasswordChangeForm
    template_name = "website/pages/edit_profile.html"

    def get(self, request, **kwargs):
        user_edit_form = self.user_edit_form(instance=request.user)
        client_edit_form = self.client_edit_form(instance=request.user)
        change_password_form = self.change_password_form(request.user)

        return render(request, self.template_name,
                      {
                          'user_edit_form': user_edit_form,
                          'client_edit_form': client_edit_form,
                          'change_password_form': change_password_form
                      })

    def post(self, request, **kwargs):
        user_edit_form = self.user_edit_form(request.POST,
                                             instance=request.user)
        client_edit_form = self.client_edit_form(request.POST,
                                                 instance=request.user)
        change_password_form = self.change_password_form(request.user,
                                                         request.POST)

        if user_edit_form.is_valid() and client_edit_form.is_valid():
            user_edit_form.save()
            client_edit_form.save()
            messages.success(request, 'Your profile was successfully updated!')

            return HttpResponseRedirect(reverse('website:edit'))

        elif change_password_form.is_valid():
            user = change_password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')

            return HttpResponseRedirect(reverse('website:edit'))

        messages.error(request, 'Please correct the error below.')

        return render(request, self.template_name,
                      {
                          'user_edit_form': user_edit_form,
                          'client_edit_form': client_edit_form,
                          'change_password_form': change_password_form
                      })
