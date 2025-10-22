from django.db import models
from django.contrib.auth.models import User

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
