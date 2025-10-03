from django.shortcuts import render
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django import forms

from .models import Portfolio



class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'short_bio', 'cover_image', 'is_public']


@login_required
def my_portfolios(request):
    portfolios = Portfolio.objects.filter(owner=request.user)
    return render(request, 'portfolio/my_portfolio_list.html', {'portfolios': portfolios})


@login_required
def portfolio_detail(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug)
    if portfolio.owner != request.user and not portfolio.is_public:
        return HttpResponseForbidden("У вас немає доступу до цього портфоліо.")
    return render(request, 'portfolio/portfolio_detail.html', {'portfolio': portfolio})


@login_required
def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.owner = request.user
            portfolio.save()
            return redirect('portfolio_detail', slug=portfolio.slug)
    else:
        form = PortfolioForm()
    return render(request, 'portfolio/portfolio.html', {'form': form})


@login_required
def portfolio_edit(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('portfolio_detail', slug=portfolio.slug)
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'portfolio/portfolio.html', {'form': form})


@login_required
def portfolio_delete(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug, owner=request.user)
    if request.method == 'POST':
        portfolio.delete()
        return redirect('my_portfolios')
    return render(request, 'portfolio/portfolio_confirm_delete.html', {'portfolio': portfolio})


