from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Announcement(models.Model):
    title = models.TextField()
    text = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now=True)
    #creator = models.creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    poster = models.ImageField(upload_to="announcements/posters", default="announcements/posters/default.jpg")

    class Meta():
        ordering = ["-create_time"]

    def __str__(self):
        return f"{self.title} creator: ..."
    

class AnnouncementPhoto(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="announcements/images/", default="default.jpg")

    def get_emoji_counts(self):
        return self.EmojiReaction.EMOJI_CHOICES
    
    # метод який повертатиме кількість реакцій для кожного емодзі
    def get_reaction_count(self, emoji):
        return self.reactions.filter(emoji=emoji).count()


# реакція користувача на оголошення
class EmojiReaction(models.Model):
    EMOJI_CHOICES = [
        ('😊', 'Smile'),
        ('❤️', 'Heart'),
        ('👍', 'Thumbs Up'),
        ('🔥', 'Fire'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reactions")
    # дозволяє отримувати всі реакції для оголошення через announcement.reactions
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="reactions")
    emoji = models.CharField(max_length=10, choices=EMOJI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')  # Один користувач може поставити лише одну реакцію на оголошення

    def __str__(self):
        return f"{self.user.username} reacted with {self.emoji} to {self.announcement.title}"