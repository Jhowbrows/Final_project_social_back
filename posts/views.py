from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self): return {'request': self.request}
    def perform_create(self, serializer): serializer.save(author=self.request.user)
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id: queryset = queryset.filter(author__id=user_id)
        return queryset
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"status": "Post descurtido"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"status": "Post curtido"}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self): return {'request': self.request}
    def get_queryset(self):
        user = self.request.user
        following_users_ids = user.profile.following.values_list('id', flat=True)
        all_ids = list(following_users_ids) + [user.id]
        return Post.objects.filter(author__id__in=all_ids)