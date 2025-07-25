from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),  # Create a new post
    path('manage/', views.manage_posts, name='manage_posts'), # Manage existing posts
]

