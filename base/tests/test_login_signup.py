from django import setup
from base.models import User
from django.test import TestCase
from django.urls import reverse
from .helper import assert_common_elements




# The 3 test functions behave as expected, it now depends on individual choice
# 1
"""class LoginSignupTestCase(TestCase):
    def setUp(self):
        user_info = User.objects.create(
            username= "FakeUser",
            email= "fakeusermail@user.com",
            password= "Fake1234",

        )  
        User.objects.get_or_create(user_info)
    def test_render_login_form(self):
        response = self.client.get(reverse("login"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "<h3>Login</h3>" in markup



    def test_render_register_user_form(self):
        response = self.client.get(reverse("register-user"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "<h3>Register</h3>" in markup"""



# 2
"""class LoginSignupTestCase(TestCase):
    def test_render_login_form(self):
        response = self.client.get(reverse("login"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "Login" in markup
        # Check for the presence of the form fields in the login form
        assert 'name="username"' in markup
        assert 'name="password"' in markup

    def test_render_register_user_form(self):
        response = self.client.get(reverse("register-user"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "Register" in markup
        # Check for the presence of the form fields in the register user form
        assert 'name="name"' in markup
        assert 'name="username"' in markup
        assert 'name="email"' in markup
        assert 'name="password1"' in markup
        assert 'name="password2"' in markup"""


# 3
class LoginSignupTestCase(TestCase):
    assert_common_elements = assert_common_elements

    def test_render_login_form(self):
        response = self.client.get(reverse("login"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "Login" in markup
        self.assert_common_elements(markup, ['name="username"', 'name="password"'])

    def test_render_register_user_form(self):
        response = self.client.get(reverse("register-user"))
        markup = response.content.decode("utf-8")
        assert response.status_code == 200
        assert "Register" in markup
        expected_elements = [
            'name="name"',
            'name="username"',
            'name="email"',
            'name="password1"',
            'name="password2"',
        ]
        self.assert_common_elements(markup, expected_elements)


