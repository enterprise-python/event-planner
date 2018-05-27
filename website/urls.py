from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView, DetailView

from website.models import Business
from . import views

app_name = 'website'
urlpatterns = [
    path('', TemplateView.as_view(template_name="website/pages/index.html"),
         name='index'),
    path('register-client/', views.ClientRegistrationView.as_view(),
         name='register_client'),
    path('register-contractor/', views.ContractorRegistrationView.as_view(),
         name='register_contractor'),

    path('login/',
         auth_views.LoginView.as_view(template_name='website/pages/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='website/pages/login.html'),
         name='logout'),

    path('profile/', login_required(TemplateView.as_view(
        template_name="website/pages/profile.html")),
         name='profile'),
    path('profile/edit/', login_required(views.ProfileEditView.as_view()),
         name='edit'),
    path('main/', login_required(TemplateView.as_view(
        template_name="website/pages/main_page.html")),
         name='main'),

    path('add-business/', login_required(views.AddBusinessView.as_view()),
         name='add_business'),
    path('business/<int:pk>/', DetailView.as_view(
        model=Business, template_name='website/pages/business.html'),
         name='business'),
    path('business/<int:pk>/edit/', login_required(views.EditBusinessView.as_view()),
         name='edit_business'),

    path('events/', login_required(views.EventsListView.as_view()),
         name='events'),
    path('add-event/', login_required(views.AddEventView.as_view()),
         name='add_event'),
    path('events/<int:pk>/', login_required(views.EventDetailView.as_view()),
         name='event'),
    path('events/<int:pk>/edit/', login_required(views.EditEventView.as_view()),
         name='edit_event'),
]
