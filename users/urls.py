from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileViewSet, UserViewSet

# A ProfileViewSet agora terá as suas rotas definidas manualmente
profile_view = ProfileViewSet.as_view({
    'get': 'list',      # GET /api/users/me/ -> list (ver perfil)
    'patch': 'partial_update' # PATCH /api/users/me/ -> partial_update (atualizar perfil)
})

password_view = ProfileViewSet.as_view({
    'post': 'set_password' # POST /api/users/me/change-password/ -> set_password
})

# O router continua a ser usado para a UserViewSet (listar e seguir utilizadores)
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    # NOVAS ROTAS MANUAIS
    path('me/', profile_view, name='my-profile'),
    path('me/change-password/', password_view, name='change-password'),

    # A rota do router vem no final
    path('', include(router.urls)),
]