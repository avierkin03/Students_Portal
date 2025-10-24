from django import forms
from forum.models import Post, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name","title","owner"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введіть ваше повідомлення'}),
        }
        