from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # Список активних опитувань
    path('', views.PollListView.as_view(), name='poll_list'),
    # Деталі опитування
    path('<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    # Обробка голосування в опитуванні
    path('<int:pk>/vote/', views.PollVoteView.as_view(), name='poll_vote'),
    # Створення нового опитування (лише для адмінів/модераторів)
    path('create/', views.PollCreateView.as_view(), name='poll_create'),
]