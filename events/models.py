import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Events(models.Model):
    CATEGORY_CHOICES = [
        ('MEETING', 'Зустріч'),
        ('WORKSHOP', 'Воркшоп'),
        ('SEMINAR', 'Семінар'),
        ('CONFERENCE', 'Конференція'),
        ('SOCIAL', 'Соціальна подія'),
        ('VACATION', 'Відпочинок'),
        ('OTHER', 'Інше'),
    ]
    TYPE_CHOICES = [
        ('ONLINE', 'Онлайн'),
        ('OFFLINE', 'Офлайн'),
        ('HYBRID', 'Гібридний'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='OTHER')
    location = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField()
    due_date = models.DateTimeField(blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    people_registered = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='OFFLINE')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')

    event_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
# class EventCalendar(models.Model):
#     CALENDAR_TYPES = [
#         ("PUBLIC", "Public calendar"),
#         ("PERSONAL", "Personal calendar"),
#         ("GROUP", "Group calendar"),
#         ("CUSTOM", "Custom calendar"),
#     ]

#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     type = models.CharField(max_length=20, choices=CALENDAR_TYPES, default="CUSTOM")

#     owner = models.ForeignKey(
#         'auth.User',
#         on_delete=models.CASCADE,
#         related_name="calendars",
#         null=True, blank=True
#     )

#     members = models.ManyToManyField(
#         'auth.User',
#         related_name="shared_calendars",
#         blank=True
#     )

#     events = models.ManyToManyField(Event, blank=True, related_name="calendars")

#     def __str__(self):
#         return f"{self.name} ({self.type})"
    
class EventComment(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.event}'
    
class EventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)

    def generate_token(self):
        self.confirmation_token = uuid.uuid4().hex
        self.save()

    def __str__(self):
        return f'{self.user} registration for {self.event}'
