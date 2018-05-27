from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
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
    path('profile/', login_required(TemplateView.as_view(
        template_name="website/pages/profile.html")),
         name='profile'),
    path('profile/edit/', login_required(views.ProfileEditView.as_view()), name='edit'),
    path('main/', login_required(TemplateView.as_view(
        template_name="website/pages/main_page.html")),
         name='main'),
    path('businesses/', views.BusinessesListView.as_view(),
         name='businesses'),
    path('ranking/', views.RankingView.as_view(),
         name='ranking')
]
