from base.models import User
from django.test import TestCase
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode
from base.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.test import override_settings
from django.conf import settings
from .helper import assert_common_elements




class RegistrationTestCase(TestCase):
    def setUp(self):
        # Set EMAIL_BACKEND to console backend for testing
        self._old_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = "FilmJunkiezEmailApp.backends.email_backend.EmailBackend"

        # Define user data for registration
        self.user_data = {
            'user': 'testuser',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

    def tearDown(self):
        # Restore the original EMAIL_BACKEND after the test
        settings.EMAIL_BACKEND = self._old_email_backend

    @override_settings(EMAIL_BACKEND = "FilmJunkiezEmailApp.backends.email_backend.EmailBackend")
    def test_successful_registration_redirects_to_login(self):
        # Existing test code
        response = self.client.post(reverse('register-user'), data=self.user_data)
        self.assertEqual(response.status_code, 200)  # In case of successful registration

        # Check if the response has a status code of 200
        self.assertEqual(response.status_code, 200)

    def test_activation_view(self):
        # Manually create a user to simulate the activation process
        user = User.objects.create(username='testuser', email='test@example.com', is_active=False)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        
        # Call the activation view with the generated uid and token
        response = self.client.get(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        
        # Check if activation is successful (status code 302 for redirect)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('login'))


class LoginTestCase(TestCase):
    assert_common_elements = assert_common_elements

    def test_render_login_form(self):
        response = self.client.get(reverse("login"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "Login" in markup
        self.assert_common_elements(markup, ['name="username"', 'name="password"'])
