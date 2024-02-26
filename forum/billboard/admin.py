from django.contrib import admin
from .models import Category, Post, Response
from .forms import PostAdminForm


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Response)
