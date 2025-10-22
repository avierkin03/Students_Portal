from django.db import models
from django.contrib.auth.models import User

class Voting(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва голосування")
    description = models.TextField(verbose_name="Опис")
    start_date = models.DateTimeField(verbose_name="Початок голосування")
    end_date = models.DateTimeField(verbose_name="Кінець голосування")
    is_active = models.BooleanField(default=True, verbose_name="Активне")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_votings")

    def __str__(self):
        return self.title

    def user_can_edit(self, user):
        return self.created_by == user

class Option(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200, verbose_name="Варіант відповіді")

    def __str__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="votes")
    voted_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'voting'], name='unique_user_voting')
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.option.text}"