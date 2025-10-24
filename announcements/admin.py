from django.contrib import admin
from .models import Announcement, AnnouncementPhoto, AnnouncementComment, AnnouncementUserReaction

admin.site.register([Announcement, AnnouncementPhoto, AnnouncementComment, AnnouncementUserReaction])
