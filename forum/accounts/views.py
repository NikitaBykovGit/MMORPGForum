from django.contrib.auth import get_user_model

from django.views.generic import DetailView, UpdateView

from .forms import UserForm

User = get_user_model()


class ProfileDetail(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'


class ProfileUpdate(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'accounts/profile_edit.html'
