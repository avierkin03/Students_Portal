from django.contrib import admin
from .models import Announcement, AnnouncementPhoto, AnnouncementComment

admin.site.register([Announcement, AnnouncementPhoto, AnnouncementComment])
