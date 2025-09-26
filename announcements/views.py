from django.views import View
from django.shortcuts import render
from .models import Announcement

class AnnouncementListView(View):
    def get(self, request):
        announcement = Announcement.objects.all()
        return render(request, "announcements/announcement_list.html", {'announcement_list': announcement})
