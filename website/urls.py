from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'website'
urlpatterns = [
    path('', TemplateView.as_view(template_name="website/index.html"),
         name='index'),
    path('register-client/', views.ClientFormView.as_view(),
         name='register_client'),
    path('register-contractor/', views.ContractorFormView.as_view(),
         name='register_contractor'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout')
]
