from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ImageGenerationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='Nick',
            password='password',
            is_active=True
        )
        self.client.login(email='testuser@example.com', password='password')

    def test_generate_image_page_access(self):
        response = self.client.get(reverse('image_generator:generate_image'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
