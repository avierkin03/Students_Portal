from django.contrib import admin
from .models import Events, EventComment, EventRegistration

admin.site.register(Events)
admin.site.register(EventComment)
admin.site.register(EventRegistration)
