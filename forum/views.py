from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from forum import models 
from forum.form import TopicForm, PostForm
from forum.mixings import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

class ClassForumList(ListView):
    model = models.Topic
    context_object_name = "topics"
    template_name = "forum/forum_list.html"


class ClassForumDetail(DetailView, UserPassesTestMixin):
    model = models.Topic
    context_object_name = "topic"
    template_name = "forum/forum_detail.html"




class TopicCreateView(LoginRequiredMixin, CreateView):
    model = models.Topic
    form_class = TopicForm
    template_name = "forum/forum_create.html"
    success_url = reverse_lazy("forum:forum_list")


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Topic
    context_object_name = "topic_delete"
    template_name = "forum/forum_delete.html"
    success_url = reverse_lazy("forum:forum_list")


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Topic
    context_object_name = "topic"
    template_name = "forum/forum_update.html"
    success_url = reverse_lazy("forum:forum_list")


class PostCreateView(CreateView):
    model = models.Post
    form_class = PostForm
    template_name = "forum/post_create.html"
    success_url = reverse_lazy('forum:forum_list')

class PostDeleteView(LoginRequiredMixin, DeleteView ):
    model = models.Post
    template_name = "forum/post_delete.html"

