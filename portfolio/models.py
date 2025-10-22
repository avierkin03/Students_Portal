from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid


class Portfolio(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_bio = models.CharField(max_length=500, blank=True)

    # проєкти: список словників (див. схему в docstring)
    projects = models.JSONField(default=list, blank=True)
    cover_image = models.ImageField(default=True, upload_to="portdolio_img")

    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Портфоліо'
        verbose_name_plural = 'Портфоліо'


    def __str__(self):
        return f"{self.title} — {self.owner}"


    def clean(self):
        # Перевірка, що projects є списком і кожен елемент має необхідні ключі
        if not isinstance(self.projects, list):
            raise ValidationError({'projects': 'Поле projects повинно бути списком.'})
        for p in self.projects:
            if not isinstance(p, dict):
                raise ValidationError({'projects': 'Кожен проєкт має бути словником.'})
            if 'id' not in p:
                raise ValidationError({'projects': 'Кожен проєкт повинен мати поле "id" (рекомендовано uuid).'})
            if 'title' not in p:
                raise ValidationError({'projects': 'Кожен проєкт повинен мати поле "title".'})


    def save(self, *args, **kwargs):
        # Автоматична генерація slug при створенні, якщо не вказано
        if not self.slug:
            base = slugify(self.title) or 'portfolio'
            unique = f"{base}-{uuid.uuid4().hex[:6]}"
            self.slug = unique
        super().save(*args, **kwargs)


    # Допоміжні методи для роботи з JSON проєкт
    def add_project(self, title, description='', links=None, screenshots=None, files=None, tags=None):
        links = links or []
        screenshots = screenshots or []
        files = files or []
        tags = tags or []
        proj = {
            'id': uuid.uuid4().hex,
            'title': title,
            'description': description,
            'links': links,
            'screenshots': screenshots,
            'files': files,
            'tags': tags,
        }
        self.projects.append(proj)
        self.save(update_fields=['projects', 'updated_at'])
        return proj


    def remove_project(self, project_id):
        before = len(self.projects)
        self.projects = [p for p in self.projects if p.get('id') != project_id]
        if len(self.projects) != before:
            self.save(update_fields=['projects', 'updated_at'])
            return True
        return False

    def update_project(self, project_id, **changes):
        updated = False
        for p in self.projects:
            if p.get('id') == project_id:
                for k, v in changes.items():
                    p[k] = v
                updated = True
                break
        if updated:
            self.save(update_fields=['projects', 'updated_at'])
        return updated


from django.contrib import admin


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'updated_at')
    search_fields = ('title', 'owner__username', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_public', 'created_at')

    fieldsets = (
        (None, {'fields': ('owner', 'title', 'slug', 'short_bio', 'cover_image', 'is_public')}),
        ('Projects (JSON)', {'fields': ('projects',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

