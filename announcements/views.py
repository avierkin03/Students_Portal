from django.views.generic import CreateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, EmojiReaction, AnnouncementPhoto, AnnouncementComment
from django.contrib.auth.decorators import login_required


class AnnouncementListView(View):
    def get(self, request):
        announcements = Announcement.objects.all()
        user_reactions = {}
        emoji_counts = {}
        emoji_choices = dict(EmojiReaction.EMOJI_CHOICES)

        if request.user.is_authenticated:
            for announcement in announcements:
                user_reactions[announcement.pk] = announcement.reactions.filter(user=request.user).first()
                emoji_counts[announcement.pk] = {
                    emoji: announcement.reactions.filter(emoji=emoji).count()
                    for emoji, _ in emoji_choices.items()
                }
        else:
            for announcement in announcements:
                emoji_counts[announcement.pk] = {
                    emoji: announcement.reactions.filter(emoji=emoji).count()
                    for emoji, _ in emoji_choices.items()
                }

        return render(request, "announcements/announcement_list.html", {
            'announcement_list': announcements,
            'user_reactions': user_reactions,
            'emoji_counts': emoji_counts,
            'emoji_choices': emoji_choices
        })


class AnnouncementInfoView(View):
    def get(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        comments = AnnouncementComment.objects.filter(announcement=pk)
        user_reaction = None
        emoji_counts = {}
        emoji_choices = dict(EmojiReaction.EMOJI_CHOICES)

        if request.user.is_authenticated:
            reaction = announcement.reactions.filter(user=request.user).first()
            user_reaction = reaction.emoji if reaction else None

        emoji_counts = {
            emoji: announcement.reactions.filter(emoji=emoji).count()
            for emoji, _ in emoji_choices.items()
        }

        return render(request, "announcements/announcements_info.html", {
            "announcement": announcement,
            "user_reactions": [user_reaction],
            "emoji_counts": emoji_counts,
            "emoji_choices": emoji_choices,
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
        return reverse("announcements:announcements_router", kwargs={"pk": self.object.announcement.pk})
    


class AnnouncementAddComment(View):
    def post(self, request, *args, **kwargs):
        announcement_id = kwargs.get("pk")
        comment_text = request.POST.get("comment")
        if comment_text:
            announcement = get_object_or_404(Announcement, pk=announcement_id)
            AnnouncementComment.objects.create(
                announcement=announcement,
                creator=request.user,
                text=comment_text
            )
        return redirect(f"/announcements/{announcement_id}/")
    

class AnnouncementRouterView(View):
    def dispatch(self, request, *args, **kwargs):
        action = request.GET.get("action") or request.POST.get("action")

        if action == "comment":
            view = AnnouncementAddComment.as_view()
        else:
            view = AnnouncementInfoView.as_view()

        return view(request, *args, **kwargs)

@login_required
def add_reaction(request, pk, emoji):
    announcement = get_object_or_404(Announcement, pk=pk)
    if emoji not in dict(EmojiReaction.EMOJI_CHOICES).keys():
        return redirect('announcements:announcements_router', pk=pk)
    
    # Видаляємо попередню реакцію користувача, якщо є
    EmojiReaction.objects.filter(user=request.user, announcement=announcement).delete()
    
    # Додаємо нову реакцію
    EmojiReaction.objects.create(
        user=request.user,
        announcement=announcement,
        emoji=emoji
    )
    
    # Перенаправляємо назад до сторінки оголошення
    return redirect('announcements:announcements_router', pk=pk)