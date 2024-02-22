from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


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
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = RichTextUploadingField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)

