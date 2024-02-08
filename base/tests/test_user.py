from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# from django.contrib.auth.forms import AuthenticationForm

from unittest.mock import patch
from django.contrib.auth import get_user_model


class TestViews(TestCase):

    def test_register_user_view(self):
        with patch("base.views.RegisterForm") as mock_register_form:
            mock_form_instance = mock_register_form.return_value
            mock_form_instance.is_valid.return_value = True
            user_data = {"email": "testuser@example.com", "password": "testpassword"}
            mock_form_instance.save.return_value = get_user_model()(**user_data)

            response = self.client.post(reverse("register-user"))

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, expected_url=reverse("login"))

    @patch("django.contrib.auth.forms.AuthenticationForm")
    def test_login_page_view(self, mock_auth_form):
        mock_form_instance = mock_auth_form.return_value
        mock_form_instance.is_valid.return_value = True
        mock_form_instance.get_user.return_value = User(
            email="testuser@example.com", password="testpassword"
        )

        response = self.client.post(reverse("login"))

        # more assertions soon

    def test_logout_view(self):
        with patch("base.views.logout") as mock_logout:
            response = self.client.get(reverse("logout"))

        # more assertions soon

    def test_user_profile_view(self):
        with patch("base.views.User.objects.get") as mock_get_user:
            mock_user_instance = mock_get_user.return_value
            mock_user_instance.film_set.all.return_value = []
            mock_user_instance.review_set.all.return_value = []

            response = self.client.get(reverse("user-profile", kwargs={"pk": 1}))

        # more assertions soon

    def test_modify_user_view(self):
        with patch("base.views.UserForm") as mock_user_form:
            mock_form_instance = mock_user_form.return_value
            mock_form_instance.is_valid.return_value = True
            mock_form_instance.save.return_value = User(
                email="testuser@example.com", password="testpassword"
            )

            response = self.client.post(reverse("modify-user"))

        # more assertions soon
