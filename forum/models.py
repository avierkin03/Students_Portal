from django.db import models
from django.conf import settings


# Create your models here.
# тема для обговорення 
class Topic(models.Model):
    name = models.CharField(max_length=200, verbose_name = "topic name")
    title = models.TextField(verbose_name="title")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner_topic")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="create_date")

    def __str__(self):
        return self.name
    

# пост/повідомлення окнкретного юзера
class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(verbose_name="title-post")
    owner_post = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner_post")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="create_date")

    def __str__(self):
        return f"Post in topic: {self.topic.name} from {self.owner_post.username}"

