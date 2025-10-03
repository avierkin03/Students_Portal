from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View
from .models import Poll, PollOption, PollVote
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import PollForm, PollOptionFormSet

# Список активних опитувань
class PollListView(ListView):
    model = Poll
    template_name = 'polls/poll_list.html'
    context_object_name = 'polls'

    def get_queryset(self):
        return Poll.objects.filter(is_active=True)


# Деталі опитування, включаючи перевірку, чи голосував користувач
class PollDetailView(DetailView):
    model = Poll
    template_name = 'polls/poll_detail.html'
    context_object_name = 'poll'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо інформацію, чи голосував користувач
        if self.request.user.is_authenticated:
            context['has_voted'] = PollVote.objects.filter(poll=self.object, user=self.request.user).exists()
        return context
    

# Обробка голосування, із захистом від повторного голосування
class PollVoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        option_id = request.POST.get('option')
        option = get_object_or_404(PollOption, pk=option_id, poll=poll)
        
        # Перевірка, чи користувач уже голосував
        if PollVote.objects.filter(poll=poll, user=request.user).exists():
            messages.error(request, 'Ви вже проголосували в цьому опитуванні!')
            return HttpResponseRedirect(reverse_lazy('polls:poll_detail', kwargs={'pk': pk}))
        
        # Створюємо голос
        PollVote.objects.create(poll=poll, option=option, user=request.user)
        option.vote_count += 1
        option.save()
        messages.success(request, 'Ваш голос зараховано!')
        return HttpResponseRedirect(reverse_lazy('polls:poll_detail', kwargs={'pk': pk}))
    

# Створення опитувань 
class PollCreateView(LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/poll_form.html'
    success_url = reverse_lazy('polls:poll_list')

    # додаємо PollOptionFormSet до контексту шаблону
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PollOptionFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PollOptionFormSet(instance=self.object)
        return context

    # перевіряємо валідність formset і зберігаємо варіанти відповідей після збереження опитування
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            # Встановлюємо created_by як поточного користувача
            form.instance.created_by = self.request.user
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Опитування та варіанти відповідей успішно створено!')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))