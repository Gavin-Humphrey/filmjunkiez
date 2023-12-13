from base.models import User
from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()



def assert_common_elements(self, markup, expected_elements):
    for element in expected_elements:
        assert element in markup


class BaseFilmJunkiezTestCase(TestCase):
    def setUp(self):
        self.client = Client()  # Use self.client instead of creating a local variable
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.url = reverse('modify-user')


    
       