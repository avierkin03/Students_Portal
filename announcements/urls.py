from django.urls import path
from .views import AnnouncementListView, AnnouncementInfoView, AnnouncementCreateView, AnnouncementDeleteView, add_reaction, AnnouncementAddImage, AnnouncementRouterView
app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path("add/<int:pk>/", AnnouncementAddImage.as_view(), name="announcement_add_image"),
    path("<int:announcement_id>/", AnnouncementRouterView.as_view(), name="announcements_router"),
    path("create/", AnnouncementCreateView.as_view(), name="announcement_create"),
    path("<int:pk>/delete/", AnnouncementDeleteView.as_view(), name="announcement_delete"),
    path("<int:pk>/react/<str:emoji>/", add_reaction, name="add_reaction"),
]