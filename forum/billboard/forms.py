from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post, Response


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
        ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'content',
        ]
