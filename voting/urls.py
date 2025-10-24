from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('', views.voting_list, name='voting_list'),
    path('my/', views.my_votings, name='my_votings'),
    path('<int:pk>/', views.voting_detail, name='voting_detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('create/', views.voting_create, name='voting_create'),
    path('<int:pk>/edit/', views.voting_edit, name='voting_edit'),
    path('<int:pk>/delete/', views.voting_delete, name='voting_delete'),
]