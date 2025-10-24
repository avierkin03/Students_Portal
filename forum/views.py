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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо форму для створення повідомлення
        context['form'] = PostForm()
        context['posts'] = self.object.posts.all()
        return context



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

    def form_valid(self, form):
        form.instance.topic = models.Topic.objects.get(pk=self.kwargs['pk'])
        form.instance.owner_post = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:forum_detail', kwargs={'pk': self.kwargs['pk']})
    

class PostDeleteView(LoginRequiredMixin, DeleteView ):
    model = models.Post
    template_name = "forum/post_delete.html"

