from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Log_User, UserProfile, Group, GroupProfile

# Логін форма
class User_Login_Form(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

# Форма реєстрації
class User_Register_Form(UserCreationForm):
    email = forms.EmailField(required=True) #Перевірка на правельність email

    class Meta:
        model = Log_User # Підключення моделі для реєстрації
        fields = ['username', 'email', 'password1', 'password2', 'role'] # Список данних для реєстрації

# Форма для профіля користувачя
class User_Profile_Form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'phone', 'birthday']

# Форма для групи
class Group_Form(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

# Форма для профіля групи
class Group_Profile_Form(forms.ModelForm):
    class Meta:
        model = GroupProfile
        fields = ['description', 'logo']