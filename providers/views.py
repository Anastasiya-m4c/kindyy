from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .choices import SWANSEA_AREAS


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

# List of areas for the dropdown in the search form
def post_search(request):
    # Get the selected area from the form submission
    selected_area = request.GET.get('area')

    # Make a list of just the area names
    areas = []
    for area in SWANSEA_AREAS:
        areas.append(area[0])

    # If a user selected an area, filter the posts by that area
    if selected_area:
        posts = Post.objects.filter(area=selected_area)
    else:
        posts = Post.objects.all()  # no filter, show all posts

    # Send the data to the template
    return render(request, post_search, {
        'posts': posts,                 # the posts to show
        'areas': areas,                 # list of all areas for the dropdown
        'selected_area': selected_area  # so we know what was selected
    })


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

