from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Avg
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from .forms import (BusinessForm, ClientCreationForm, ClientEditForm,
                    ContractorCreationForm, ContractorEditForm, EventForm,
                    UserCreationForm, UserEditForm)
from website.models import Role, Business, Event


class ClientRegistrationView(View):
    user_form = UserCreationForm
    client_form = ClientCreationForm
    template_name = 'website/pages/register_client.html'

    def get(self, request):
        return render(request, self.template_name, {
            'user_form': self.user_form(None),
            'client_form': self.client_form(None)
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
        return render(request, self.template_name, {
            'user_form': self.user_form(None),
            'contractor_form': self.contractor_form(None)
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
    password_change_form = PasswordChangeForm
    template_name = "website/pages/edit_profile.html"

    def get(self, request):
        if request.user.is_client():
            return self._get_client(request)
        elif request.user.is_contractor():
            return self._get_contractor(request)

    def _get_client(self, request):
        user_edit_form = self.user_edit_form(instance=request.user)
        client_edit_form = self.client_edit_form(instance=request.user)
        change_password_form = self.password_change_form(user=request.user)

        return render(request, self.template_name, {
            'user_edit_form': user_edit_form,
            'client_edit_form': client_edit_form,
            'change_password_form': change_password_form
        })

    def _get_contractor(self, request):
        user_edit_form = self.user_edit_form(instance=request.user)
        contractor_edit_form = self.contractor_edit_form(instance=request.user)
        change_password_form = self.password_change_form(request.user)

        return render(request, self.template_name, {
            'user_edit_form': user_edit_form,
            'contractor_edit_form': contractor_edit_form,
            'change_password_form': change_password_form
        })

    def post(self, request):
        if request.user.is_client():
            return self._post_client(request)
        elif request.user.is_contractor():
            return self._post_contractor(request)

    def _post_client(self, request):
        user_edit_form = self.user_edit_form(request.POST,
                                             instance=request.user)
        client_edit_form = self.client_edit_form(request.POST,
                                                 instance=request.user)
        change_password_form = self.password_change_form(request.user,
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

        return render(request, self.template_name, {
            'user_edit_form': user_edit_form,
            'client_edit_form': client_edit_form,
            'change_password_form': change_password_form
        })

    def _post_contractor(self, request):
        user_edit_form = self.user_edit_form(request.POST,
                                             instance=request.user)
        contractor_edit_form = self.contractor_edit_form(request.POST,
                                                         instance=request.user)
        change_password_form = self.password_change_form(request.user,
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
        return render(request, self.template_name, {
            'user_edit_form': user_edit_form,
            'contractor_edit_form': contractor_edit_form,
            'change_password_form': change_password_form
        })


class EventsListView(ListView):
    context_object_name = 'events_list'
    template_name = 'website/pages/events_list.html'

    def get_queryset(self):
        if not self.request.user.is_client():
            raise Http404()

        return Event.objects.filter(owner=self.request.user.client).order_by(
            '-date_from')


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'website/pages/event.html'

    def get_object(self, queryset=None):
        event = super().get_object(queryset)

        if (not self.request.user.is_client()
                or not self.request.user.client.event_set.filter(pk=event.pk)):
            raise Http404()

        return event


class AddEventView(View):
    event_form = EventForm
    template_name = 'website/pages/add_event.html'

    def get(self, request):
        if not request.user.is_client():
            raise Http404()

        return render(request, self.template_name, {
            'event_form': self.event_form(None)
        })

    def post(self, request):
        if not request.user.is_client():
            raise Http404

        event_form = self.event_form(request.POST)

        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.owner = request.user.client
            event.save()

            return HttpResponseRedirect(reverse('website:events'))

        return render(request, self.template_name, {
            'event_form': event_form
        })


class EditEventView(View):
    event_form = EventForm
    template_name = 'website/pages/edit_event.html'

    @staticmethod
    def _check_event_owner(user, pk):
        if not (user.is_client()
                and Event.objects.get(pk=pk) in user.client.event_set):
            raise Http404()

    def get(self, request, pk):
        self._check_event_owner(request.user, pk)
        return render(request, self.template_name, {
            'event_form': self.event_form(instance=Event.objects.get(pk=pk))
        })

    def post(self, request, pk):
        self._check_event_owner(request.user, pk)
        event_form = self.event_form(request.POST,
                                     instance=Event.objects.get(pk=pk))
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Your event was successfully updated!')

            return HttpResponseRedirect(reverse('website:events'))

        messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {
            'event_form': event_form
        })


class BusinessesListView(ListView):
    template_name = 'website/pages/businesses_list.html'
    context_object_name = 'businesses_list'

    def get_queryset(self):
        return Business.objects.all()


class RankingView(ListView):
    template_name = 'website/pages/ranking.html'
    context_object_name = 'businesses_list'

    def get_queryset(self):
        return Business.objects.all().annotate(
            avg_rating=Avg('opinion__rating')).order_by('-avg_rating')[:10]


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
    def _check_business_owner(user, pk):
        if not (user.is_contractor()
                and Business.objects.get(pk=pk)
                in user.contractor.business_set):
            raise Http404()

    def get(self, request, pk):
        self._check_business_owner(request.user, pk)

        business_form = self.business_form(instance=Business.objects.get(pk=pk))
        return render(request, self.template_name, {
            'business_form': business_form
        })

    def post(self, request, pk):
        self._check_business_owner(request.user, pk)

        business_form = self.business_form(request.POST,
                                           instance=Business.objects.get(pk=pk))
        if business_form.is_valid():
            business_form.save()
            messages.success(request, 'Your business was successfully updated!')

            return HttpResponseRedirect(reverse('website:main'))

        messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {
            'business_form': business_form
        })
