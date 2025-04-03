from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import LoggedInUser, UserTextData
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()

class ModelTests(TestCase):
    def test_logged_in_user_str(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        logged_in = LoggedInUser.objects.create(user=user)
        self.assertEqual(str(logged_in), 'testuser')

    def test_user_text_data_str(self):
        user = User.objects.create_user(username='testuser2', password='testpass')
        data = UserTextData.objects.create(user=user, name='Note', text_data='Some text')
        self.assertIn('testuser2', str(data))

class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_demo_view(self):
        response = self.client.get(reverse("demo"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, world!"})