from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create/', login_required(views.create_post), name='create_post'),  # New path for post creation
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
