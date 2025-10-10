from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Events, EventComment
from .forms import EventForm, CommentForm
from .mixins import UserIsOwnerMixin

# from .forms import EventCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

class EventListView(ListView):
    model = Events
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class EventDetailView(DetailView):
    model = Events
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        # context["comments"] = self.object.comments.select_related("author")
        context["form"] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.event = self.object

            # викликаємо утиліту
            # comment.content = process_mentions(comment, request.user)

            comment.save()
            return redirect("events:event-detail", pk=self.object.pk)

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

    
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Events
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class EventUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Events
    form_class = EventForm
    template_name = 'events/event_update.html'
    def get_success_url(self):
        return reverse_lazy('events:event-detail', kwargs={'pk': self.object.pk})
    
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Events
    success_url = reverse_lazy('events:event-list')
    template_name = 'events\event_delete_confirmation.html'
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by or self.request.user.is_staff
