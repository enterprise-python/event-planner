from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from . import views

app_name = 'website'
urlpatterns = [
    path('', TemplateView.as_view(template_name="website/index.html"),
         name='index'),
    path('register-client/', views.ClientRegistrationView.as_view(),
         name='register_client'),
    path('register-contractor/', views.ContractorRegistrationView.as_view(),
         name='register_contractor'),
    path('login/',
         auth_views.LoginView.as_view(template_name='website/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='website/login.html'),
         name='logout'),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='website/change_password.html',
             success_url=reverse_lazy('website:password_change_done')),
         name='change_password'),
    path('change-password/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='website/password_change_done.html'),
         name='password_change_done'),
]
