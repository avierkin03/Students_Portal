from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name = 'event-list'), 
    path('<uuid:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.EventCreateView.as_view(), name='event-create'), 
    path('<uuid:pk>/update', views.EventUpdateView.as_view(), name='event-update'), 
    path('<uuid:pk>/delete', views.EventDeleteView.as_view(), name='event-delete'), 
    path("<uuid:pk>/register/", views.register_for_event, name="event-register"),
    path("confirm-registration/<str:token>/", views.confirm_registration, name="confirm-registration"),
]