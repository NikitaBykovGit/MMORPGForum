from django.urls import path
from .views import ProfileDetail, ProfileUpdate


urlpatterns = [
    path('<int:pk>', ProfileDetail.as_view(), name='profile'),
    path('<int:pk>/update', ProfileUpdate.as_view(), name='profile_update'),
]
