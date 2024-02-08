from django.test import TestCase, Client
from django.urls import reverse
from base.models import User
from base.models import Film, Category, Review


class HomeViewTest(TestCase):
    def setUp(self):
        # Create test data (categories, films, etc.)
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(title="Test Category")
        self.film = Film.objects.create(
            title="Test Film",
            description="Film description",
            category=self.category,
            host=self.user,
        )
        self.review = Review.objects.create(
            user=self.user, film=self.film, rating=5, body="Great film!"
        )

        # Initialize the Django test client
        self.client = Client()

    def test_home_view(self):
        # Simulate a GET request to the home view
        response = self.client.get(reverse("home"))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template is correct
        self.assertTemplateUsed(response, "base/home.html")

        # Check if the context contains the expected data
        self.assertIn("films", response.context)
        self.assertIn("categories", response.context)
        self.assertIn("film_count", response.context)
        self.assertIn("film_reviews", response.context)
