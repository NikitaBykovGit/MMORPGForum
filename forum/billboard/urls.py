from django.urls import path
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseCreate, ResponseUpdate,
                    ResponseDelete)
urlpatterns = [
    path('', PostList.as_view(), name='main_page'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/response/create', ResponseCreate.as_view(), name='response_create'),
    path('<int:pk>/response/update', ResponseUpdate.as_view(), name='response_update'),
    path('<int:pk>/response/delete', ResponseDelete.as_view(), name='response_delete'),
]