from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class Category(models.Model):
    CATEGORY = (
        ('TK', 'Tanks'),
        ('HL', 'Healers'),
        ('DD', 'DDs'),
        ('SL', 'Sellers'),
        ('GM', 'Guildmasters'),
        ('QG', 'Questgivers'),
        ('BS', 'Blacksmiths'),
        ('TN', 'Tanners'),
        ('PM', 'Potionmasters'),
        ('SM', 'Spellmasters')
    )
    name = models.CharField(max_length=2, choices=CATEGORY, unique=True, default='TK')

    def __str__(self):
        for category in self.CATEGORY:
            if category[0] == self.name:
                return category[1]


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = RichTextUploadingField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def preview(self):
        position_tag = self.content[1:-1].find('<')
        if position_tag == -1:
            return self.content[:20] + '...'
        else:
            return self.content[3:position_tag] + '...'


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'post'], name='unique response to a post from each user'),
        ]

    def get_absolute_url(self):
        return reverse('main_page')

    def save(self, *args, **kwargs):
        if self.author == self.post.author:
            raise ValidationError('You can not response to your post')
        super().save(*args, **kwargs)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
