from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from forum import models 
# Create your views here.

class ClassForumList(ListView):
    model = models.Topic
    context_object_name = "forum_list"
    template_name = "forum_list.html"


class ClassForumDetail(DetailView):
    model = models.Post
    context_object_name = "forum_detail"
    template_name = "forum_detail.html"





