from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import PostForm
from django.shortcuts import render, get_object_or_404
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
    queryset = Post.objects.filter(status=1)
    template_name = 'kindyy/index.html'
    paginate_by = 6

@login_required
def create_post(request):
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

