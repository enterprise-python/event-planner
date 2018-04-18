from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'website'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', TemplateView.as_view(template_name="website/index.html"), name='index'),
]