from abc import ABC

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery, Count
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Post, Response
from .forms import PostForm, ResponseForm
from .filters import PostFilter, ResponseFilter


class FindResponseMixin(ABC):
    def get_object(self, queryset=None):
        return Response.objects.get(post_id=self.kwargs['pk'], author=self.request.user)


class AuthorRequiredMixin(ABC):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseForbidden("Forbidden")
        return super().dispatch(request, *args, **kwargs)


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
        response = Response.objects.filter(post_id=OuterRef('pk'), author_id=self.request.user.id)
        queryset = queryset.annotate(response_exists=Count(Subquery(response.only('id'))))
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'billboard/post_edit.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.post_id = self.kwargs['pk']
        response.author = self.request.user
        return super().form_valid(form)


class PostUpdate(AuthorRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'


class ResponseUpdate(FindResponseMixin, AuthorRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'billboard/post_edit.html'


class PostDelete(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')


class ResponseDelete(FindResponseMixin, AuthorRequiredMixin, DeleteView):
    model = Response
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')


class ResponseDeny(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('response_list')


class ResponseAccept(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        Response.objects.filter(pk=self.kwargs['pk']).update(status=True)
        return HttpResponseRedirect(reverse_lazy('response_list'))


class ResponseUserPostsList(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-time'
    template_name = 'billboard/responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, request=self.request, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
