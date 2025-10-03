from django.views.generic import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import Announcement

class AnnouncementListView(View):
    def get(self, request):
        announcement = Announcement.objects.all()
        return render(request, "announcements/announcement_list.html", {'announcement_list': announcement})
    

class AnnouncementInfoView(View):
    def get(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        return render(request, "announcements/announcements_info.html", {"announcement": announcement})


class AnnouncementCreateView(CreateView):
    model = Announcement
    template_name = "announcements/announcement_create.html"
    fields = ["title", "text"]
    success_url = reverse_lazy("announcements:announcement_list")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

