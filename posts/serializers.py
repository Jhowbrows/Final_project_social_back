from rest_framework import serializers
from .models import Post, Comment
from users.serializers import PublicProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = PublicProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at', 'post']

class PostSerializer(serializers.ModelSerializer):
    author = PublicProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'created_at', 'likes_count', 'is_liked', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'likes_count', 'is_liked', 'comments']
    def get_likes_count(self, obj): return obj.likes.count()
    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(id=user.id).exists()