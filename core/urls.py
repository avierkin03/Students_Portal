from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path(' ', views.base, name='base' ),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_user_profile, name='edit_user_profile'),

    path('groups/', views.GroupList.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreate.as_view(), name='group_create'),
    path('groups/<int:pk>/', views.GroupDetail.as_view(), name='group_detail'),

    path('profile/<int:pk>/', views.GroupProfileDetail.as_view(), name='group_profile'),
    path('profile/<int:pk>/edit/', views.GroupProfileUpdate.as_view(), name='group_profile_edit'),
]