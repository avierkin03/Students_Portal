from django.shortcuts import render
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django import forms

import uuid


class Portfolio(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_bio = models.CharField(max_length=500, blank=True)
    projects = models.JSONField(default=list, blank=True)
    cover_image = models.ImageField(upload_to='portfolio/covers/%Y/%m/%d/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Портфоліо'
        verbose_name_plural = 'Портфоліо'

    def __str__(self):
        return f"{self.title} — {self.owner}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'portfolio'
            unique = f"{base}-{uuid.uuid4().hex[:6]}"
            self.slug = unique
        super().save(*args, **kwargs)



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



@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'updated_at')
    search_fields = ('title', 'owner__username', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_public', 'created_at')

    fieldsets = (
        (None, {'fields': ('owner', 'title', 'slug', 'short_bio', 'cover_image', 'is_public')}),
        ('Проєкти (JSON)', {'fields': ('projects',)}),
        ('Часові мітки', {'fields': ('created_at', 'updated_at')}),
    )

