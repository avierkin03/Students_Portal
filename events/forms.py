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

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError("Дата події не може бути в минулому.")
        return date

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        date = self.cleaned_data.get('date')

        if due_date and due_date < timezone.now():
            raise forms.ValidationError("Кінцева дата не може бути в минулому.")
        if due_date and date and due_date < date:
            raise forms.ValidationError("Кінцева дата не може бути раніше початку події.")
        return due_date

class CommentForm(forms.ModelForm):

    class Meta:
        model = EventComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 2, "placeholder": "Write here..."}),
        }