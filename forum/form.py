from django import forms
from forum.models import Post, Topic



class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name","title","owner","date_create"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text","topic","owner_post","date_create"]
        