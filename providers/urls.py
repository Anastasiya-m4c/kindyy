"""
URL patterns for the blog application.

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create/', views.create_post, name='create_post'),
    path('manage/', views.my_posts, name='my_posts'),
    path('search/', views.post_search, name='post_search'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
