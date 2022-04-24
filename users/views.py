from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from posts.models import Post, Comment
from .models import CustomUser
from .serializers import CustomUserSerializer
from .pagination import CursorPagination
from .permissions import IsUserOrReadOnly, BlockAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CursorPagination
    lookup_field = 'username'

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsUserOrReadOnly]
        elif self.action in ["follow", "unfollow"]:
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [BlockAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        post_id = self.request.GET.get('post_id')
        comment_id = self.request.GET.get('comment_id')
        user_followers = self.request.GET.get('user_followers')
        user_following = self.request.GET.get('user_following')
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                queryset = queryset.filter(id__in=post.likes.all())
            except Post.DoesNotExist:
                return

        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
                queryset = queryset.filter(id__in=comment.likes.all())
            except Comment.DoesNotExist:
                return

        if user_following:
            try:
                user = CustomUser.objects.get(username=user_following)
                queryset = queryset.filter(id__in=user.following.all())
            except CustomUser.DoesNotExist:
                return

        if user_followers:
            try:
                user = CustomUser.objects.get(username=user_followers)
                queryset = queryset.filter(id__in=user.followers.all())
            except CustomUser.DoesNotExist:
                return

        return queryset

    @action(detail=True)
    def follow(self, request, username):
        user = self.get_object()
        request.user.following.add(user)
        return Response({'message': 'You followed user successfully'}, status=status.HTTP_200_OK)

    @action(detail=True)
    def unfollow(self, request, username):
        user = self.get_object()
        request.user.following.remove(user)
        return Response({'message': 'You unfollowed user successfully'}, status=status.HTTP_200_OK)
