from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from website.models import Role, Business
from .forms import ClientCreationForm, UserCreationForm, ContractorCreationForm, \
    UserEditForm, ClientEditForm, ContractorEditForm, BusinessForm


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


class ProfileEditView(View):
    user_edit_form = UserEditForm
    client_edit_form = ClientEditForm
    contractor_edit_form = ContractorEditForm
    change_password_form = PasswordChangeForm
    template_name = "website/pages/edit_profile.html"

    def get(self, request):
        if request.user.is_client():
            return self.get_client(request)
        elif request.user.is_contractor():
            return self.get_contractor(request)

    def get_client(self, request):
        user_edit_form = self.user_edit_form(instance=request.user)
        client_edit_form = self.client_edit_form(instance=request.user)
        change_password_form = self.change_password_form(request.user)

        return render(request, self.template_name,
                      {
                          'user_edit_form': user_edit_form,
                          'client_edit_form': client_edit_form,
                          'change_password_form': change_password_form
                      })

    def get_contractor(self, request):
        user_edit_form = self.user_edit_form(instance=request.user)
        contractor_edit_form = self.contractor_edit_form(instance=request.user)
        change_password_form = self.change_password_form(request.user)

        return render(request, self.template_name,
                      {
                          'user_edit_form': user_edit_form,
                          'contractor_edit_form': contractor_edit_form,
                          'change_password_form': change_password_form
                      })

    def post(self, request):
        if request.user.is_client():
            return self.post_client(request)
        elif request.user.is_contractor():
            return self.post_contractor(request)

    def post_client(self, request):
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

    def post_contractor(self, request):
        user_edit_form = self.user_edit_form(request.POST,
                                             instance=request.user)
        contractor_edit_form = self.contractor_edit_form(request.POST,
                                                         instance=request.user)
        change_password_form = self.change_password_form(request.user,
                                                         request.POST)

        if user_edit_form.is_valid() and contractor_edit_form.is_valid():
            user_edit_form.save()
            contractor_edit_form.save()
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
                          'contractor_edit_form': contractor_edit_form,
                          'change_password_form': change_password_form
                      })


class AddBusinessView(View):
    business_form = BusinessForm
    template_name = 'website/pages/add_business.html'

    def get(self, request):
        if not request.user.is_contractor():
            raise Http404()

        return render(request, self.template_name, {
            'business_form': self.business_form(None)
        })

    def post(self, request):
        if not request.user.is_contractor():
            raise Http404()

        business_form = self.business_form(request.POST)

        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.owner = request.user.contractor
            business.save()

            return HttpResponseRedirect(reverse('website:main'))

        return render(request, self.template_name, {
            'business_form': business_form
        })


class EditBusinessView(View):
    business_form = BusinessForm
    template_name = 'website/pages/edit_business.html'

    @staticmethod
    def _check_business_owner(request, pk):
        if not request.user.is_contractor():
            raise Http404()

        for business in Business.objects.filter(owner=request.user.client):
            if business.pk == pk:
                break
        else:
            raise Http404()

    def get(self, request, pk):
        self._check_business_owner(request, pk)

        return render(request, self.template_name, {
            'business_form': self.business_form(
                instance=Business.objects.filter(pk=pk))
        })

    def post(self, request, pk):
        self._check_business_owner(request, pk)

        business_form = self.business_form(request.POST,
                                           instance=Business.objects.filter(
                                               pk=pk))
        if business_form.is_valid():
            business_form.save()
            messages.success(request, 'Your business was successfully updated!')

            return HttpResponseRedirect(reverse('website:main'))

        messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {
            'business_form': business_form
        })
