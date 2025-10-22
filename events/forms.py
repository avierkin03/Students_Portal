from django import forms
from .models import Events, EventComment

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'description', 'category', 'type', 'location', 'date', 'due_date', 'capacity', 'event_link']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = EventComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 2, "placeholder": "Write here..."}),
        }