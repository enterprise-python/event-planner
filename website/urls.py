from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import DetailView, TemplateView

from eventplanner import settings
from . import views
from website.models import Business


app_name = 'website'

urlpatterns = [
    path('',
         TemplateView.as_view(template_name="website/pages/index.html"),
         name='index'),
    path('register-client/',
         views.ClientRegistrationView.as_view(),
         name='register_client'),
    path('register-contractor/',
         views.ContractorRegistrationView.as_view(),
         name='register_contractor'),

    path('login/',
         auth_views.LoginView.as_view(template_name='website/pages/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='website/pages/login.html'),
         name='logout'),

    path('profile/',
         login_required(TemplateView.as_view(
             template_name="website/pages/profile.html")),
         name='profile'),
    path('profile/edit/',
         login_required(views.ProfileEditView.as_view()),
         name='edit'),
    path('main/',
         login_required(views.MainPageView.as_view()),
         name='main'),

    path('add-business/',
         login_required(views.AddBusinessView.as_view()),
         name='add_business'),
    path('businesses/', views.BusinessesListView.as_view(),
         name='businesses'),
    path('ranking/',
         views.RankingView.as_view(),
         name='ranking'),
    path('business/<int:pk>/',
         DetailView.as_view(
             model=Business,
             template_name='website/pages/business.html'
         ),
         name='business'),
    path('business/<int:pk>/edit/',
         login_required(views.EditBusinessView.as_view()),
         name='edit_business'),

    path('business/<int:pk>/add-opinion/',
         login_required(views.AddOpinionView.as_view()),
         name='add_opinion'),
    path('business/<int:pk>/opinions/',
         views.OpinionsListView.as_view(),
         name='opinion'),

    path('events/',
         login_required(views.EventsListView.as_view()),
         name='events'),
    path('add-event/',
         login_required(views.AddEventView.as_view()),
         name='add_event'),
    path('event/<int:pk>/',
         login_required(views.EventDetailView.as_view()),
         name='event'),
    path('event/<int:pk>/edit/',
         login_required(views.EditEventView.as_view()),
         name='edit_event'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
