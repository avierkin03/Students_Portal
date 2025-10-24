from django.views.generic import CreateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, AnnouncementPhoto
from django.urls import reverse
from .models import Announcement, AnnouncementPhoto, AnnouncementComment, AnnouncementUserReaction

class AnnouncementListView(View):
    def get(self, request):
        announcement = Announcement.objects.all()
        return render(request, "announcements/announcement_list.html", {'announcement_list': announcement})


class AnnouncementInfoView(View):
    def get(self, request, *args, **kwargs):
        announcement_id = kwargs.get("announcement_id")
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        comments = AnnouncementComment.objects.filter(announcement=announcement).order_by("create_time")
        return render(request, "announcements/announcements_info.html", {
            "announcement": announcement,
            "comments": comments
        })


class AnnouncementCreateView(CreateView):
    model = Announcement
    template_name = "announcements/announcement_create.html"
    fields = ["title", "text", "poster"]
    success_url = reverse_lazy("announcements:announcement_list")
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = "announcements/announcement_confirm_delete.html"
    success_url = reverse_lazy("announcements:announcement_list")


class AnnouncementAddImage(CreateView):
    model = AnnouncementPhoto
    template_name = "announcements/announcement_add_image.html"
    fields = ["image"]

    def form_valid(self, form):
        announcement = get_object_or_404(Announcement, pk=self.kwargs["pk"])
        form.instance.announcement = announcement
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("announcements:announcements_router", kwargs={"announcement_id": self.object.announcement.pk})
    


class AnnouncementAddComment(View):
    def post(self, request, *args, **kwargs):
        announcement_id = kwargs.get("announcement_id")
        comment_text = request.POST.get("comment")
        if comment_text:
            announcement = get_object_or_404(Announcement, pk=announcement_id)
            AnnouncementComment.objects.create(
                announcement=announcement,
                creator=request.user,
                text=comment_text
            )
        return redirect(f"/announcements/{announcement_id}/")
    

class AnnouncementAddReaction(CreateView):
    pass


class AnnouncementRouterView(View):
    def dispatch(self, request, *args, **kwargs):
        action = request.GET.get("action") or request.POST.get("action")

        if action == "comment":
            view = AnnouncementAddComment.as_view()
        elif action == "react":
            view = AnnouncementAddReaction.as_view()
        else:
            view = AnnouncementInfoView.as_view()

        return view(request, *args, **kwargs)
