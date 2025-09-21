# users/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class UserAuthTests(APITestCase):
    def test_register_user(self):
        """
        Garante que um novo utilizador pode ser criado.
        """
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post("/api/users/register/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login_user(self):
        """
        Garante que um utilizador pode fazer login e receber um token.
        """
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
        """
        Garante que um utilizador pode seguir outro.
        """
        # Autentica como user1
        self.client.force_authenticate(user=self.user1)
        
        # CORREÇÃO: Ação é para /follow/
        response = self.client.post(f"/api/users/{self.user2.id}/follow/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.profile.following.filter(id=self.user2.id).exists())

    def test_unfollow_user(self):
        """
        Garante que um utilizador pode deixar de seguir outro.
        """
        # user1 primeiro segue user2
        self.user1.profile.following.add(self.user2)
        
        # Autentica como user1
        self.client.force_authenticate(user=self.user1)
        
        # CORREÇÃO: Ação é para deixar de seguir user2, não user1
        response = self.client.post(f"/api/users/{self.user2.id}/unfollow/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.profile.following.filter(id=self.user2.id).exists())

    def test_get_profile_with_follow_info(self):
        """
        Garante que as informações de seguidores/seguindo estão corretas em ambos os perfis.
        """
        # user1 segue user2
        self.user1.profile.following.add(self.user2)
        
        # Testa o perfil do user1 (quem segue)
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['following']), 1)
        self.assertEqual(response.data['following'][0]['username'], 'user2')
        self.assertEqual(len(response.data['followers']), 0)

        # Testa o perfil do user2 (quem é seguido)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['followers']), 1)
        self.assertEqual(response.data['followers'][0]['username'], 'user1')
        self.assertEqual(len(response.data['following']), 0)