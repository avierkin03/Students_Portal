from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path("", views.ClassForumList.as_view(), name="forum_list"),
    path("detail/<int:pk>", views.ClassForumDetail.as_view(), name="forum_detail"),
    path("create/", views.TopicCreateView.as_view(), name="forum_create"),
    path("delete/<int:pk>", views.TopicDeleteView.as_view(), name="forum_delete"),
    path("update/<int:pk>", views.TopicUpdateView.as_view(), name="forum_update"),
    path("delete_post/<int:pk>", views.PostDeleteView.as_view(), name="post_delete"),
    path("create_post/", views.PostCreateView.as_view(), name="post_create"),
    
]