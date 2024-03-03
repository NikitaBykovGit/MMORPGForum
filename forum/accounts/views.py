from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import DetailView, UpdateView

from .forms import UserForm
from .models import Code

User = get_user_model()


class ProfileDetail(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'


class ProfileUpdate(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'accounts/profile_edit.html'


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = Code.objects.filter(code=request.POST['code'])
            if code.exists():
                User.objects.filter(id=code[0].user.id).update(is_active=True)
                code.delete()
            else:
                return render(self.request, 'accounts/invalid_code.html')
        return HttpResponseRedirect(reverse_lazy('account_login'))
