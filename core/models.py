from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User



class Log_User(AbstractUser):
    # Авторизація та Реєстрація(та перевірка на ролі)
    class Roles(models.TextChoices):
        USER = "user", "Користувач"
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Адміністратор"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name="Роль"
    )

    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser
    
class UserProfile(models.Model):
    # Особистий кабінет користувача
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True, verbose_name="Біографія")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Профіль {self.user.username}"


class Group(models.Model):
    # Група користувачів (наприклад, навчальна група, команда тощо)
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name="groups")

    def __str__(self):
        return self.name


class GroupProfile(models.Model):
    # Особистий кабінет групи
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="group_logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Кабінет групи {self.group.name}"
