from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post


class PostDetail(DetailView):
    model = Post
    template_name = 'billboard/post.html'
    context_object_name = 'post'


class PostList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'billboard/posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')


class Response(View):
    pass