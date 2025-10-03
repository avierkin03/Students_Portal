from django.urls import path
from .views import AnnouncementListView, AnnouncementInfoView, AnnouncementCreateView
app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path("<int:pk>/", AnnouncementInfoView.as_view(), name="announcement_detail"),
    path("create/", AnnouncementCreateView.as_view(), name="announcement_create"),
]