from django.db import models
from django.utils import timezone

# Категории — например, "Учебники", "Статьи", "Видео"
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Материал — это основная сущность (запись)
class Material(models.Model):
    title = models.CharField(max_length=100)  # Название материала
    description = models.TextField()          # Текст или описание
    resource = models.TextField()             # Источник
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='materials')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# Комментарий к материалу
class Comment(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author}'