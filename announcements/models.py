from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    title = models.TextField()
    text = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now=True)
    #creator = models.creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    class Meta():
        ordering = ["-create_time"]

    def __str__(self):
        return f"{self.title} creator: ..."
