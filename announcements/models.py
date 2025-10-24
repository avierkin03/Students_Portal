from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    poster = models.ImageField(upload_to="announcements/posters", default="announcements/posters/default.jpg")

    class Meta():
        ordering = ["-create_time"]

    def __str__(self):
        return f"{self.title} creator: ..."
    

class AnnouncementPhoto(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="announcements/images/", default="default.jpg")


class EmojiLibrary(models.Model):
    image = models.ImageField(upload_to="announcements/reactions/")
    name = models.CharField(max_length=50, blank=True)
    

class AnnouncementUserReaction(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.ImageField(upload_to="announcements/reactions/", default="announcements/posters/default.jpg")
    reactions_mum = models.IntegerField()


class AnnouncementComment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now=True)
