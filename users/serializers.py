from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'avatar_thumbnail', 'bio', 'website', 'gender', 'is_verified',
                  'following_count', 'followers_count', 'posts_count']
