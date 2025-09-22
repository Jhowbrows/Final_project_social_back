from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
import tempfile
from PIL import Image
from django.conf import settings
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

class UserAuthTests(APITestCase):
    def test_register_user(self):
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post("/api/users/register/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
    def test_login_user(self):
        User.objects.create_user(username="testuser", password="testpassword123")
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post("/api/login/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class FollowSystemTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
    def test_follow_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f"/api/users/{self.user2.id}/follow/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.profile.following.filter(id=self.user2.id).exists())
    def test_unfollow_user(self):
        self.user1.profile.following.add(self.user2)
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f"/api/users/{self.user2.id}/unfollow/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.profile.following.filter(id=self.user2.id).exists())
    def test_get_profile_with_follow_info(self):
        self.user1.profile.following.add(self.user2)
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['following']), 1)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['followers']), 1)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ProfileInteractionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="old_password")
        self.client.force_authenticate(user=self.user)

    def _create_temp_image(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def test_change_password_successfully(self):
        
        data = {"old_password": "old_password", "new_password": "new_secure_password"}
        response = self.client.post("/api/users/me/change-password/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_secure_password"))

    def test_change_password_with_wrong_old_password(self):
        
        data = {"old_password": "wrong_password", "new_password": "new_password"}
        response = self.client.post("/api/users/me/change-password/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_profile_picture(self):
        """
        Garante que o utilizador pode fazer o upload de uma foto de perfil.
        """
        tmp_file = self._create_temp_image()
        data = {'profile.profile_picture': tmp_file}
        response = self.client.patch("/api/users/me/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.profile_picture.url.endswith('.jpg'))

    
    def test_delete_profile_picture(self):
        """
        Garante que o utilizador pode apagar a sua foto de perfil.
        """
        # Primeiro, fazemos o upload de uma imagem
        tmp_file = self._create_temp_image()
        self.user.profile.profile_picture = SimpleUploadedFile(tmp_file.name, tmp_file.read())
        self.user.profile.save()

        # Verificamos se a imagem existe
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.profile_picture)

        # Agora, chamamos o endpoint para apagar
        response = self.client.post("/api/users/me/delete-picture/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificamos se a imagem foi removida do perfil
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.profile_picture)