from django.urls import path
from .views import AnnouncementListView, AnnouncementInfoView, AnnouncementCreateView, AnnouncementDeleteView, add_reaction
app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path("<int:pk>/", AnnouncementInfoView.as_view(), name="announcement_detail"),
    path("create/", AnnouncementCreateView.as_view(), name="announcement_create"),
    path("<int:pk>/delete/", AnnouncementDeleteView.as_view(), name="announcement_delete"),
    path("<int:pk>/react/<str:emoji>/", add_reaction, name="add_reaction"),
]