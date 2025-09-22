from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileViewSet, UserViewSet


profile_view = ProfileViewSet.as_view({
    'get': 'list',      
    'patch': 'partial_update' 
})

password_view = ProfileViewSet.as_view({
    'post': 'set_password' 
})

delete_picture_view = ProfileViewSet.as_view({
    'post': 'delete_picture'
})

change_username_view = ProfileViewSet.as_view({
    'post': 'set_username'
})


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),


    path('me/', profile_view, name='my-profile'),
    path('me/change-password/', password_view, name='change-password'),
    path('me/delete-picture/', delete_picture_view, name='delete-picture'),
    path('me/change-username/', change_username_view, name='change-username'),
    path('', include(router.urls)),
]