from rest_framework import serializers
from .models import Post, Comment, Tag, Reply


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'caption', 'tags',
                  'created_at', 'modified_at', 'likes_count', 'comments_count')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        post = Post.objects.create(**validated_data)
        if tags_data:
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data["name"])
                post.tags.add(tag)

        post.save()
        return post

    def update(self, instance, validated_data):
        instance.caption = validated_data.get("caption")
        tags_data = validated_data.pop('tags', None)

        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data["name"])
                instance.tags.add(tag)

        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "content", "created_at",
                  "modified_at", "likes_count", "replies_count")


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Reply
        fields = ("id", "author", "replied_to", "content", "created_at",
                  "modified_at", "likes_count")
