from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # Список активних опитувань
    path('', views.PollListView.as_view(), name='poll_list'),
    # Деталі опитування
    path('<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
]