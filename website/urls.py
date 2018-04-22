from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'website'
urlpatterns = [
    path('', TemplateView.as_view(template_name="website/index.html"), name='index'),
    path('register/', views.ClientFormView.as_view(), name='register'),
]
