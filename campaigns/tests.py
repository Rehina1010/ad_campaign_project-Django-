from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Campaign

User = get_user_model()


class CampaignTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='Nick', password='password',
                                             is_active=True)
        self.client.login(email='testuser@example.com', password='password')

        self.campaign = Campaign.objects.create(
            title='Test Campaign',
            owner=self.user,
            budget=100,
            description='Test Description',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30)
        )

    def test_campaign_list_access(self):
        response = self.client.get(reverse('campaigns:campaign_list'))
        self.assertEqual(response.status_code, 200)
