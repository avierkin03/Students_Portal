from django.urls import path
from .views import AnnouncementListView

app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
]