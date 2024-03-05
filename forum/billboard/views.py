from abc import ABC

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import OuterRef, Subquery, Count, Exists, F, Value, Sum
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Post, Response, Category, Subscription
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
        user = self.request.user.id
        responses = Response.objects.filter(post_id=OuterRef('pk'), author_id=user)
        queryset = queryset.annotate(response_exists=Exists(responses))
        queryset = queryset.annotate(response_accepted=Sum(responses.values('status')))
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['title'] = 'Post'
        return context


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'billboard/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['title'] = 'Response'
        return context

    def form_valid(self, form):
        response = form.save(commit=False)
        response.post_id = self.kwargs['pk']
        response.author = self.request.user
        return super().form_valid(form)


class PostUpdate(AuthorRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'billboard/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['title'] = 'Post edit'
        context['text'] = f'Post {Post.objects.get(id=self.kwargs["pk"]).title} edit'
        return context


class ResponseUpdate(FindResponseMixin, AuthorRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'billboard/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['title'] = 'Response edit'
        context['text'] = f'Response to post {Post.objects.get(id=self.kwargs["pk"]).title} edit'
        return context


class PostDelete(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['title'] = 'Post'
        context['text'] = f'Do you want to delete your post {Post.objects.get(id=self.kwargs["pk"]).title}'
        return context


class ResponseDelete(FindResponseMixin, AuthorRequiredMixin, DeleteView):
    model = Response
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['title'] = 'Response'
        context['text'] = f'Do you want to delete your response to post {Post.objects.get(id=self.kwargs["pk"]).title}'
        return context


class ResponseDeny(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'billboard/post_delete.html'
    success_url = reverse_lazy('response_list')


class ResponseAccept(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        response = Response.objects.filter(pk=self.kwargs['pk'])
        response.update(status=True)
        send_mail(
            subject=f'Your response accepted',
            message=f'Your response to post {settings.SITE_URL}{response[0].post.get_absolute_url()} has been accepted',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.first().author.email]
        )
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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'billboard/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
