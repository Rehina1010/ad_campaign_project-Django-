from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='Nick',
            password='password',
            is_active=True
        )
        self.client.login(email='testuser@example.com', password='password')

    def test_register_page_access(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_login_page_access(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_profile_page_access(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')

    def test_edit_profile_page_access(self):
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')
