from django.urls import path
from .views import AnnouncementListView, AnnouncementInfoView, AnnouncementCreateView, AnnouncementDeleteView
app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path("<int:pk>/", AnnouncementInfoView.as_view(), name="announcement_detail"),
    path("create/", AnnouncementCreateView.as_view(), name="announcement_create"),
    path("<int:pk>/delete/", AnnouncementDeleteView.as_view(), name="announcement_delete"),
]