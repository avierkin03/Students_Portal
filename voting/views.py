from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator
from .models import Voting, Option, Vote
from .forms import VotingForm, OptionFormSet, VoteForm

def voting_list(request):
    votings = Voting.objects.filter(is_active=True)
    return render(request, 'voting/vote_list.html', {'votings': votings})

def voting_detail(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(user=request.user, voting=voting).first()
    options = voting.options.all()
    results = {option: option.votes.count() for option in options}
    total_votes = sum(results.values())
    return render(request, 'voting/vote_detail.html', {
        'voting': voting,
        'user_vote': user_vote,
        'results': results,
        'total_votes': total_votes
    })

@login_required
def vote(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    if not voting.is_active:
        return redirect('voting:voting_detail', pk=pk)

    Vote.objects.filter(user=request.user, voting=voting).delete()

    if request.method == 'POST':
        form = VoteForm(request.POST, voting=voting)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.voting = voting
            vote.save()
            return redirect('voting:voting_detail', pk=pk)
    else:
        form = VoteForm(voting=voting)
    return render(request, 'voting/vote_options.html', {'form': form, 'voting': voting})

@login_required
def voting_create(request):
    if request.method == 'POST':
        form = VotingForm(request.POST)
        formset = OptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            voting = form.save(commit=False)
            voting.created_by = request.user
            voting.save()
            formset.instance = voting
            formset.save()
            return redirect('voting:voting_list')
    else:
        form = VotingForm()
        formset = OptionFormSet()
    return render(request, 'voting/vote_form.html', {'form': form, 'formset': formset})

@login_required
def voting_edit(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    if voting.created_by != request.user:
        raise Http404("Ви не маєте права редагувати це голосування")
    
    if request.method == 'POST':
        form = VotingForm(request.POST, instance=voting)
        formset = OptionFormSet(request.POST, instance=voting)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('voting:voting_list')
    else:
        form = VotingForm(instance=voting)
        formset = OptionFormSet(instance=voting)
    return render(request, 'voting/vote_form.html', {'form': form, 'formset': formset, 'voting': voting})

@login_required
def voting_delete(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    if voting.created_by != request.user:
        raise Http404("Ви не маєте права видаляти це голосування")
    
    if request.method == 'POST':
        voting.delete()
        return redirect('voting:my_votings')
    return render(request, 'voting/vote_delete_confirm.html', {'voting': voting})

@login_required
def my_votings(request):
    # Получаем голосования текущего пользователя
    votings_list = Voting.objects.filter(created_by=request.user).order_by('-start_date')
    
    # Пагинация
    paginator = Paginator(votings_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Считаем статистику
    for voting in page_obj:
        voting.options_count = voting.options.count()
        voting.votes_count = voting.votes.count()
        voting.is_currently_active = voting.is_active
    
    context = {
        'page_obj': page_obj,
        'votings_count': votings_list.count(),
        'active_votings_count': votings_list.filter(is_active=True).count(),
    }
    return render(request, 'voting/my_votings.html', context)