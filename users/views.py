from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer, PublicProfileSerializer, ChangePasswordSerializer, ChangeUsernameSerializer

from rest_framework.decorators import action

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       
        return User.objects.select_related('profile').filter(id=self.request.user.id)

    def get_object(self):
       
        return self.get_queryset().get()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        
        return Response(self.get_serializer(self.get_object()).data)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

    @action(detail=False, methods=['post'], url_path='delete-picture')
    def delete_picture(self, request):
        """
        Ação para apagar a foto de perfil do utilizador.
        """
        user = request.user
        profile = user.profile

        if not profile.profile_picture:
            return Response({"status": "Nenhuma foto de perfil para apagar."}, status=status.HTTP_400_BAD_REQUEST)

        
        profile.profile_picture.delete(save=False)
        profile.profile_picture = None
        profile.save()

        return Response({"status": "Foto de perfil apagada com sucesso."}, status=status.HTTP_200_OK)
    


    action(detail=False, methods=['post'], url_path='change-username')
    def set_username(self, request):
        user = request.user
        serializer = ChangeUsernameSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data['password']
            if not user.check_password(password):
                return Response({"password": ["Senha incorreta."]}, status=status.HTTP_400_BAD_REQUEST)

            new_username = serializer.validated_data['new_username']
            user.username = new_username
            user.save()
            return Response({"status": "Nome de utilizador alterado com sucesso"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='change-password')
    def set_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if not user.check_password(old_password):
                return Response({"old_password": ["Senha antiga incorreta."]}, status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"status": "Senha alterada com sucesso"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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