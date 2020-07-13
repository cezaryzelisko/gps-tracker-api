from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

OBTAIN_TOKEN_URL = reverse('jwt_auth:token_obtain')
REFRESH_TOKEN_URL = reverse('jwt_auth:token_refresh')


class CustomJWTTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_can_obtain_custom_token(self):
        res = self.get_access_token()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertIn('accessExpiresAt', res.data)
        self.assertIn('refreshExpiresAt', res.data)

    def test_can_refresh_custom_token(self):
        access_res = self.get_access_token()

        refresh_res = self.client.post(REFRESH_TOKEN_URL, {'refresh': access_res.data['refresh']})

        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_res.data)
        self.assertIn('accessExpiresAt', refresh_res.data)

    def get_access_token(self):
        credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        user = User(username=credentials['username'])
        user.set_password(credentials['password'])
        user.save()

        res = self.client.post(OBTAIN_TOKEN_URL, credentials)

        return res
