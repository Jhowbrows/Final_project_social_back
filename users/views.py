from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer, PublicProfileSerializer
from rest_framework.decorators import action

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return User.objects.filter(id=self.request.user.id)
    def get_object(self): return self.request.user
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    def list(self, request, *args, **kwargs): return Response(self.get_serializer(self.request.user).data)
    def destroy(self, request, *args, **kwargs): return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = PublicProfileSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        current_user = request.user
        if user_to_follow == current_user: return Response({"error": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)
        current_user.profile.following.add(user_to_follow)
        return Response({"status": f"Você agora está seguindo {user_to_follow.username}"}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        current_user = request.user
        current_user.profile.following.remove(user_to_unfollow)
        return Response({"status": f"Você deixou de seguir {user_to_unfollow.username}"}, status=status.HTTP_200_OK)