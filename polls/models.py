from django.db import models
from django.conf import settings

# Модель "Опитування"
class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'


# Модель "Варіант відповіді для опитування"
class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.poll.title}: {self.text}"

    class Meta:
        verbose_name = 'Poll Option'
        verbose_name_plural = 'Poll Options'


# Модель "Голос користувача"
class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='poll_votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} voted in {self.poll.title}"

    class Meta:
        verbose_name = 'Poll Vote'
        verbose_name_plural = 'Poll Votes'
        unique_together = ['poll', 'user']  # Один голос на користувача для опитування