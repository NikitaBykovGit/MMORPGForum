from abc import ABC

from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, Count
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Post, Response
from .forms import PostForm, ResponseForm
from .filters import PostFilter


class FindResponseMixin(ABC):
    def get_object(self, queryset=None):
        return Response.objects.get(post_id=self.kwargs['pk'], user_id=self.request.user.id)


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

    def get_queryset(self):
        queryset = super().get_queryset()
        response = Response.objects.filter(post_id=OuterRef('pk'), user_id=self.request.user.id)
        queryset = queryset.annotate(response_exists=Count(Subquery(response.only('id'))))
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class ResponseCreate(CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'billboard/post_edit.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.post_id = self.kwargs['pk']
        response.user_id = self.request.user.id
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'


class ResponseUpdate(FindResponseMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'billboard/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')


class ResponseDelete(FindResponseMixin, DeleteView):
    model = Response
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')


class ProfileDetail(DetailView):
    model = User
    template_name = 'billboard/profile.html'
    context_object_name = 'user'