from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.GroupProfileDetail.as_view(), name='group_profile'),

    path('register/', views.register_user, name='register'),
    path('login/', views.logins_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.user_profile_forms, name='user_profile_forms'),

    path('groups/', views.GroupList.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreate.as_view(), name='group_create'),
    path('groups/edit/', views.GroupDetail.as_view(), name='group_detail'),

    path('profile/', views.GroupProfileDetail.as_view(), name='group_profile'),
    path('profile/edit/', views.GroupProfileUpdate.as_view(), name='group_profile_edit'),
]