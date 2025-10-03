from django import forms
from django.forms import inlineformset_factory
from .models import Poll, PollOption

# Форма для створення/редагування опитування
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Formset для створення кількох PollOption, пов’язаних із Poll
PollOptionFormSet = inlineformset_factory(
    Poll,
    PollOption,
    fields=['text'],
    extra=3,  # Кількість порожніх форм за замовчуванням (3 варіанти)
    can_delete=False,
    widgets={'text': forms.TextInput()},
)