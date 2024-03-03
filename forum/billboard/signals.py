from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response


@receiver(post_save, sender=Response)
def response_to_post(instance, **kwargs):
    send_mail(
        subject=f'Response to your post',
        message=f'Your post {settings.SITE_URL}{instance.post.get_absolute_url()} get response from '
                f'{instance.author}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.post.author.email]
    )
