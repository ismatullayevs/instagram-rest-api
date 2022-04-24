from django.urls import path, include
from users.views import UserViewSet
from posts.views import PostViewSet, ReplyViewSet, CommentViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)
router.register('replies', ReplyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
