from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'time'
    template_name = 'billboard/posts.html'
    context_object_name = 'Posts'
