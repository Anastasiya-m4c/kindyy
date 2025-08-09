"""
Views for the blog application.

This module handles the display and management of blog posts,
including listing, searching, creating, editing, and deleting posts.

It uses Django's class-based and function-based views, and integrates with
PostForm, Post model, and the SWANSEA_AREAS dropdown.

"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.core.paginator import Paginator
from .forms import PostForm
from .models import Post
from .choices import SWANSEA_AREAS


def post_detail(request, slug):
    """
    Display an individual published post by slug.
    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the post to retrieve.

    Returns:
        HttpResponse: Rendered detail view of the post.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    return render(
        request,
        "kindyy/post_detail.html",
        {"post": post},
    )


class PostList(generic.ListView):
    """
    Display a paginated list of published posts.
    """
    queryset = Post.objects.filter(status=1)
    template_name = 'kindyy/index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        """
        Add Swansea area choices to the context for filtering.
        """
        context = super().get_context_data(**kwargs)
        context['swansea_areas'] = SWANSEA_AREAS
        return context


def post_search(request):
    """
    Display posts filtered by selected Swansea area.

    Supports pagination and a dropdown list of areas.

    Args:
        request (HttpRequest): The request object containing GET parameters.

    Returns:
        HttpResponse: Rendered list view of filtered posts.
    """
    selected_area = request.GET.get('area')

    areas = [area[0] for area in SWANSEA_AREAS]

    if selected_area:
        posts = Post.objects.filter(area=selected_area)
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    return render(request, 'kindyy/post_search.html', {
        'page_obj': page_obj,
        'paginator': paginator,
        'posts': posts,
        'areas': areas,
        'selected_area': selected_area,
        'is_paginated': is_paginated,
        'swansea_areas': SWANSEA_AREAS
    })


@login_required
def create_post(request):
    """
    Allow a logged-in user to create a new post.

    On successful POST, redirects to homepage.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'kindyy/post_form.html', {'form': form})


@login_required
def my_posts(request):
    """
    Display all posts created by the logged-in user.
    """
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'kindyy/my_posts.html', {'posts': user_posts})


@login_required
def edit_post(request, slug):
    """
    Allow the user to edit their own post.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the post to edit.

    Returns:
        HttpResponse: Rendered form view for editing.
    """
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)
    return render(
        request, 'kindyy/post_form.html', {'form': form, 'edit': True})


@login_required
def delete_post(request, slug):
    """
    Allow the user to delete their own post.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the post to delete.

    Returns:
        HttpResponse: Confirmation page or redirect.
    """
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('my_posts')

    return render(request, 'kindyy/confirm_delete.html', {'post': post})
