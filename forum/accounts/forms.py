from allauth.account.forms import SignupForm
from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import User
from .utils import CodeManager


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.is_active = False
        code = CodeManager.generate(user)
        user.save()
        send_mail(
            subject=f'Activation code',
            message=f'Activation account code: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user
