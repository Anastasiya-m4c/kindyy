from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post


# Create your views here.

def post_detail(request, slug):
    # Display an individual :model:`blog.Post`.
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    return render(
        request,
        "kindyy/post_detail.html",
        {"post": post},
    )

class PostList(generic.ListView):
    # List all published posts
    queryset = Post.objects.filter(status=1)
    template_name = 'kindyy/index.html'
    paginate_by = 6

@login_required
def create_post(request):
    # Create a new post
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Automatically set the post author
            post.save()
            return redirect('home')  # Redirect to your homepage or post detail
    else:
        form = PostForm()
    return render(request, 'kindyy/post_form.html', {'form': form})

@login_required
def my_posts(request):
    # Display posts created by the logged-in user
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'kindyy/my_posts.html', {'posts': user_posts})


@login_required
def edit_post(request, slug):
    # Edit an existing post
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'kindyy/post_form.html', {'form': form, 'edit': True})

@login_required
def delete_post(request, slug):
    # Delete a post
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('my_posts')

    return render(request, 'kindyy/confirm_delete.html', {'post': post})

