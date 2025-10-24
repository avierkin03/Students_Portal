from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AnnouncementListView, AnnouncementCreateView, AnnouncementDeleteView, AnnouncementAddImage, AnnouncementRouterView

app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path("add/<int:pk>/", AnnouncementAddImage.as_view(), name="announcement_add_image"),
    path("<int:announcement_id>/", AnnouncementRouterView.as_view(), name="announcements_router"),
    path("create/", AnnouncementCreateView.as_view(), name="announcement_create"),
    path("<int:pk>/delete/", AnnouncementDeleteView.as_view(), name="announcement_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
