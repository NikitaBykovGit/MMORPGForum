from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Response


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
        }


class FilterSupporter:
    @staticmethod
    def get_user_posts(request):
        if request is None:
            return Post.objects.none()
        user = request.user
        return Post.objects.filter(author=user)


class ResponseFilter(FilterSet):
    post = ModelChoiceFilter(queryset=FilterSupporter.get_user_posts)

    class Meta:
        model = Response
        fields = [
            'post',
        ]
