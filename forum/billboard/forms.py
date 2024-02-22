from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'
