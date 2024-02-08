from django.test import TestCase
from django.urls import reverse
from base.models import User, Category, Film, Review

# from base.forms import FilmForm
from django.utils import timezone
from django.template.defaultfilters import timesince


class FilmViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(
            username="hostuser", email="hostuser@example.com", password="testpassword"
        )

        # Create a sample category
        self.category = Category.objects.create(title="Test Category")

        self.duration = "30"

        # Create a sample participant
        participant = User.objects.create(username="Test Participant")

        # Create the film object
        self.film = Film.objects.create(
            title="Test Film",
            description="Test Description",
            director="Test Director",
            lead="Test Lead",
            average_rating="4",
            host=self.user,
            image="film_img",
            video="film_videos",
            category=self.category,
            release_date=timezone.now(),  # You can use a naive datetime field, 2023-12-12
            duration=self.duration,
        )

        # Use the set() method to assign participants to the film
        self.film.participants.set([participant])

        # Create a sample review
        self.review = Review.objects.create(
            user=self.user,
            film=self.film,
            rating="4",
            body="Nice Film!",
            created=timezone.now(),
        )

    def test_film_view(self):
        # Log in the user
        # self.client.login(email='hostuser@example.com', password='testpassword')
        self.client.force_login(self.user)

        response = self.client.get(reverse("film", args=[self.film.id]))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        expected_host = self.user
        expected_average_rating = "4"
        expected_date = timesince(self.review.created)

        # Check that the film details are present in the response
        self.assertContains(response, "Test Film")
        self.assertContains(response, "Test Director")
        self.assertContains(response, f"<span>@{expected_host}</span>")
        self.assertContains(response, f"{expected_average_rating}")
        self.assertContains(
            response, '<span class="film__categories">Test Category</span>'
        )
        self.assertContains(
            response, f'<span class="thread__date">{expected_date} ago</span>'
        )
        self.assertContains(response, "film_img")

    def test_film_details(self):
        # self.client.login(username='hostuser@example.com', password='testpassword')
        self.client.force_login(self.user)

        response = self.client.get(reverse("film-details", args=[self.film.id]))
        # markup = response.content.decode("utf-8")

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        expected_release_date = timezone.now().strftime("%Y-%m-%d")

        self.assertContains(response, "Test Film")
        self.assertContains(response, "<h3>Test Description</h3>")
        self.assertContains(response, "film_videos")
        self.assertContains(response, "film_img")
        self.assertContains(response, "Test Director")
        self.assertContains(response, "Test Lead")
        self.assertContains(response, f"Release Date: {expected_release_date}")
        self.assertContains(response, self.duration)

    def test_updates_film(self):
        # Get the initial film instance
        # initial_film = Film.objects.get(id=self.film.id)
        # initial_title = initial_film.title

        updated_title = "Updated Film Title"
        updated_director = "Updated Film Director"
        updated_lead = "Updated Film Lead"
        updated_img = "Updated film_img"
        updated_description = "Updated Film Description"
        updated_category = "Updated Film Category"

        # Test updating with empty fields
        response = self.client.post(
            reverse("update-film", args=[self.film.id]),
            {
                "title": "",
                "director": "",
                "lead": "",
                "film_img": "",
                "description": "",
                "category": self.category,
            },
            follow=True,
        )

        self.assertNotContains(response, "required.", html=True)

        response = self.client.post(
            reverse("update-film", args=[self.film.id]),
            {
                "title": updated_title,
                "director": updated_director,
                "lead": updated_lead,
                "film_img": updated_img,
                "description": updated_description,
                "category": updated_category,
            },
            follow=True,
        )

        # Assert that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

    def test_film_delete(self):
        # Log in with a user
        self.client.login(email="hostuser@example.com", password="testpassword")
        self.client.force_login(self.user)

        # Get the initial count of films
        initial_film_count = Film.objects.count()

        # Make a POST request to delete the film
        response = self.client.post(
            reverse("delete-film", args=[self.film.id]), follow=True
        )
        # Check that the response redirects to the "home" page
        self.assertRedirects(response, reverse("home"))
        # Check that the film is no longer present in the database
        self.assertEqual(Film.objects.count(), initial_film_count - 1)
        self.assertFalse(
            Film.objects.filter(id=self.film.id).exists(), "Film should be deleted"
        )
