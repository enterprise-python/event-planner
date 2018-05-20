from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

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
    path('profile/', TemplateView.as_view(
        template_name="website/pages/profile.html"),
         name='profile'),
    path('profile/edit/', views.ClientEditView.as_view(), name='edit')
]
