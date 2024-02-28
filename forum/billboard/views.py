from django.db.models import Value, F, OuterRef, Subquery
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import PostForm, ResponseForm
from .models import Post, Response


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
        responce = Response.objects.get(post_id=OuterRef('id'), user_id=self.request.user.id)
        queryset = queryset.annotate(response_exists=Subquery(responce.values(F('id'))))
        print(self.request.user.id)
        print(queryset[1].response_exists)
        print(queryset[1].id)
        return queryset


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


class ResponseUpdate(UpdateView):
    form_class = ResponseForm
    model = Response
    template_name = 'billboard/post_edit.html'

    def get_object(self, queryset=None):
        return Response.objects.get(post_id=self.kwargs['pk'], user_id=self.request.user.id)


class PostDelete(DeleteView):
    model = Post
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')


class Responser(View):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        if Response.objects.filter(post_id=post_id, user_id=self.request.user.id).exists():
            return HttpResponseRedirect(reverse('response_update', args=[post_id]))
        else:
            return HttpResponseRedirect(reverse('response_create', args=[post_id]))
