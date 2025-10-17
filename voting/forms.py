from django import forms
from .models import Voting, Option, Vote

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['title', 'description', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']

OptionFormSet = forms.inlineformset_factory(
    Voting, Option, form=OptionForm, extra=2, can_delete=True
)

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['option']

    def __init__(self, *args, **kwargs):
        voting = kwargs.pop('voting', None)
        super().__init__(*args, **kwargs)
        if voting:
            self.fields['option'].queryset = Option.objects.filter(voting=voting)