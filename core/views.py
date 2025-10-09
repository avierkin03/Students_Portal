# Імпорити
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from core.models import UserProfile, Group, GroupProfile
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import User_Login_Form, User_Register_Form, User_Profile_Form, Group_Form, Group_Profile_Form

# ------------------ ЛОГІН ТА РЕЄСТРАЦІЯ ------------------
# Функція авторізації
def logins_user(request):
    if request.method == 'POST':
        form = User_Login_Form(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вхід виконано успішно!')
            return redirect('home')
    else:
        form = User_Login_Form()
    return render(request, 'login.html', {'form': form})

# Функція реєстрації
def register_user(request):
    if request.method == 'POST':
        form = User_Register_Form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')
            return redirect('home')
    else:
        form = User_Register_Form()
    return render(request, 'register.html', {'form': form})

# Функція вихода
def logout_user(request):
    logout(request)
    messages.info(request, 'Ви вийшли із системи.')
    return redirect('home')


# ------------------ КОРИСТУВАЧ ------------------
# Функція перегляд особистого профілю користувача
@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile})

# Функція редагування профілю користувача
@login_required
def edit_user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = User_Profile_Form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = User_Profile_Form(instance=profile)

    return render(request, 'edit_user_profile.html', {'form': form})


# ------------------ ГРУПИ ------------------
# Список усіх груп
class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'

# Деталі групи
class GroupDetail(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'group_detail.html'
    context_object_name = 'group'

# Створення нової групи
class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    form_class = Group_Form
    template_name = 'group_form.html'
    success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.add(self.request.user) # Додавання користувача до групи
        return response


# ------------------ ПРОФІЛЬ ГРУПИ ------------------
# Перегляд профілю групи
class GroupProfileDetail(LoginRequiredMixin, DetailView):
    model = GroupProfile
    template_name = 'group_profile.html'
    context_object_name = 'profile'

# Редагування профілю групи
class GroupProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GroupProfile
    form_class = Group_Profile_Form
    template_name = 'group_profile_form.html'

    def test_func(self):
        group_profile = self.get_object()
        return self.request.user in group_profile.group.members.all()

    def get_success_url(self):
        return reverse_lazy('group_profile', kwargs={'pk': self.object.pk})