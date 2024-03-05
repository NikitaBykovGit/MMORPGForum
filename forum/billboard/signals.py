from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response, Post, Subscription


@receiver(post_save, sender=Response)
def response_to_post(instance, **kwargs):
    send_mail(
        subject=f'Response to your post',
        message=f'Your post {settings.SITE_URL}{instance.post.get_absolute_url()} get response from '
                f'{instance.author}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.post.author.email]
    )


@receiver(post_save, sender=Post)
def post_created(instance, **kwargs):
    for subscription in Subscription.objects.filter(category_id=instance.category.id):
        if instance.author != subscription.user:
            send_mail(
                subject=f'New post',
                message=f'New post {settings.SITE_URL}{instance.get_absolute_url()} in category '
                        f'{instance.category} you are subscribed to',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email]
            )
