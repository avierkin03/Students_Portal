from django.contrib import admin
from .models import Voting, Option, Vote

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active']
    inlines = [OptionInline]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'voting', 'option', 'voted_at']