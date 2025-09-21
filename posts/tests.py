from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post

class PostAndFeedAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.user3 = User.objects.create_user(username="user3", password="password")
        self.user1.profile.following.add(self.user2)
        self.post_by_user1 = Post.objects.create(author=self.user1, content="Post do user1")
        self.post_by_user2 = Post.objects.create(author=self.user2, content="Post do user2")
        self.post_by_user3 = Post.objects.create(author=self.user3, content="Post do user3")
    def test_create_post(self):
        self.client.force_authenticate(user=self.user1)
        data = {"content": "Meu novo post de teste."}
        response = self.client.post("/api/posts/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 4)
    def test_feed_shows_followed_and_own_posts(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contents = [post['content'] for post in response.data['results']]
        self.assertIn("Post do user1", contents)
        self.assertIn("Post do user2", contents)
        self.assertNotIn("Post do user3", contents)
    def test_like_post(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f"/api/posts/{self.post_by_user2.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post_by_user2.likes.count(), 1)
        response = self.client.post(f"/api/posts/{self.post_by_user2.id}/like/")
        self.assertEqual(self.post_by_user2.likes.count(), 0)
    def test_comment_on_post(self):
        self.client.force_authenticate(user=self.user1)
        data = {"text": "Ótimo post!"}
        response = self.client.post(f"/api/posts/{self.post_by_user2.id}/comment/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post_by_user2.comments.count(), 1)