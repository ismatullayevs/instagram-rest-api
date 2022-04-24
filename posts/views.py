from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from api.pagination import CursorPagination
from .models import Post, Comment, Tag, Reply
from .serializers import PostSerializer, CommentSerializer, ReplySerializer
from .permissions import IsAuthorOrReadOnly


class LikeUnlikeMixin():
    @action(detail=True)
    def like(self, request, pk):
        obj = self.get_object()
        obj.likes.add(request.user)
        return Response({'message': 'You successfully liked this object'}, status=status.HTTP_200_OK)

    @action(detail=True)
    def unlike(self, request, pk):
        obj = self.get_object()
        obj.likes.remove(request.user)
        return Response({'message': 'You successfully unliked this object'}, status=status.HTTP_200_OK)


class CommonPermissionsMixin():
    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["list", "create"]:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthorOrReadOnly]
        elif self.action in ["like", "unlike"]:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class PostViewSet(LikeUnlikeMixin, CommonPermissionsMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = CursorPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        recommended = self.request.GET.get('recommended')
        username = self.request.GET.get('username')
        if recommended == "True":
            queryset = queryset.filter(
                author__in=self.request.user.following.all())

        if username:
            queryset = queryset.filter(author__username=username)

        return queryset


class CommentViewSet(LikeUnlikeMixin, CommonPermissionsMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = CursorPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.GET.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset


class ReplyViewSet(LikeUnlikeMixin, CommonPermissionsMixin, viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    pagination_class = CursorPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Reply.objects.all()
        comment_id = self.request.GET.get('comment_id')
        if comment_id:
            queryset = queryset.filter(replied_to=comment_id)

        return queryset
