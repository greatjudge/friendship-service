from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class TestRegister(TestCase):
    def test_success_register(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        resp = self.client.post(reverse('register_user'), data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['username'], data['username'])
        user_id = int(resp.data['id'])
        user = User.objects.get(id=user_id)
        self.assertEqual(user.username, data['username'])

    def test_unique_username(self):
        user = User.objects.create(username='testuser_unique')
        data = {
            'username': 'testuser_unique',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        resp = self.client.post(reverse('register_user'), data)
        self.assertEqual(resp.status_code, 400)
