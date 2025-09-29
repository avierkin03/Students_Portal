from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from forum import models 
from forum.form import TopicForm, PostForm
from forum.mixings import UserPassesTestMixin
# Create your views here.

class ClassForumList(ListView):
    model = models.Topic
    context_object_name = "topics"
    template_name = "forum/forum_list.html"


class ClassForumDetail(DetailView, UserPassesTestMixin):
    model = models.Topic
    context_object_name = "topic"
    template_name = "forum/forum_detail.html"




class TopicCreateView(CreateView):
    model = models.Topic
    form_class = TopicForm
    template_name = "forum/forum_create.html"


class TopicDeleteView(DeleteView):
    model = models.Topic
    template_name = "forum/forum_delete.html"


class TopicUpdateView(UpdateView):
    model = models.Topic
    template_name = "forum/forum_update.html"


class PostCreateView(CreateView):
    model = models.Post
    form_class = PostForm
    template_name = "forum/post_create.html"

class PostDeleteView(DeleteView):
    model = models.Post
    template_name = "forum/post_delete.html"

