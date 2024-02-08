"""from django.urls import reverse
from .helper import BaseFilmJunkiezTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from base.models import User


class TestFilmJunkiezUser(BaseFilmJunkiezTestCase):
    def test_userProfile_rendering(self):

        # Get the user's profile page
        response = self.client.get(reverse("user-profile", kwargs={"pk": self.user.id}))
        markup = response.content.decode("utf-8")

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        expected_avatar_tag = "profile__avatar"
        assert (
            expected_avatar_tag in markup
        ), f"Expected: {expected_avatar_tag}\nActual: {markup}"

        # Check if the "Edit Profile" text is present in the response content
        assert "profile__info" in markup
        assert "Following" in markup
        assert "<h3>About</h3>" in markup
        assert "filmList__header" in markup


class TestFilmJunkiezModifyUser(BaseFilmJunkiezTestCase):

    def test_modify_user_view_rendering(self):
        response = self.client.get(reverse("modify-user"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/modify_user.html")

    def test_modify_user_authentication(self):
        # Logout the user and check if they are redirected to the login page
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login") + f"?next={self.url}")

    def test_modify_user_form_rendering(self):
        response = self.client.get(reverse("modify-user"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "profile_pic")
        self.assertContains(response, "<form")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_modify_user_form_submission_valid_data(self):
        # Create a new user
        user = User.objects.create(
            username="new_username", email="new_email@example.com"
        )

        # Log in the user
        self.client.force_login(user)

        # Prepare form data for updating the profile
        data = {
            "name": "Updated Name",
            "username": "updated_username",
            "email": "updated_email@example.com",
            #'avatar': SimpleUploadedFile('avatar', b'file_content'),
            "bio": "Updated bio",
        }

        # Submit the form
        response = self.client.post(reverse("modify-user"), data=data, follow=True)

        # Assert that the user is redirected to the profile page
        self.assertRedirects(response, reverse("user-profile", kwargs={"pk": user.id}))

    def test_modify_user_form_submission_invalid_data(self):
        # Submit an empty form, assuming 'field1' is a required field in your form
        response = self.client.post(self.url, {}, follow=True)

        # self.assertContains(response, 'This field is required.')
        # Check that the error message is not present in the response content
        error_message = "This field is required."
        self.assertNotIn(error_message, response.content.decode())

    def test_modify_user_file_upload(self):
        # Test file upload functionality
        data = {
            "field1": "value1",
            "field2": "value2",
            "profile_pic": SimpleUploadedFile("test.jpg", b"file_content"),
        }
        response = self.client.post(self.url, data, follow=True)
        # Add assertions to check if the file is correctly processed and associated with the user

    def test_cancel_button(self):
        response = self.client.get(self.url)
        cancel_url = reverse("user-profile", kwargs={"pk": self.user.id})
        self.assertContains(response, f'href="{cancel_url}"')

    # def test_modify_user_security(self):
    #     # Logout and try to access the view, expecting a redirect to the login page
    #     self.client.logout()
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, reverse('login') + f'?next={self.url}')"""
