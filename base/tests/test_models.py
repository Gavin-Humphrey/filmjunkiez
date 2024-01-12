from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from base.models import User, Category, Film, Review
import os



class UserModelTest(TestCase):
    def test_str_representation(self):
        # Test that the string representation of the User model is the user's name
        user = User(username="testuser", email="test@example.com", name="Test User")
        self.assertEqual(str(user), "Test User")

    def test_user_creation(self):
        # Test the creation of a user using the create_user method
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        # Check if the user is an instance of the User model and if the count of users is 1
        self.assertTrue(isinstance(user, User))
        self.assertEqual(User.objects.count(), 1)

class CategoryModelTest(TestCase):
    def test_str_representation(self):
        # Test that the string representation of the Category model is the category's title
        category = Category(title="Action")
        self.assertEqual(str(category), "Action")

class FilmModelTest(TestCase):
    def setUp(self):
        # Set up a user and a category for testing
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.category = Category.objects.create(title="Action")

    def test_str_representation(self):
        # Test that the string representation of the Film model is the film's title
        film = Film(title="Test Film", host=self.user, category=self.category)
        self.assertEqual(str(film), "Test Film")

    def test_average_rating_calculation(self):
        # Test the calculation of the average rating for a film
        film = Film.objects.create(title="Test Film", host=self.user, category=self.category)
        review1 = Review.objects.create(user=self.user, film=film, rating=4, body="Good movie")
        review2 = Review.objects.create(user=self.user, film=film, rating=2, body="Average movie")

        # Calculate the average rating and check if it matches the expected value
        film.calculate_average_rating()
        self.assertEqual(film.average_rating, 3.0)

  
    def test_save_method_with_image(self):
        # Test the save method of the Film model when an image is provided
        image_path = os.path.join("media", "film_img", "knowledge.jpg")
        image_file = SimpleUploadedFile(name="test_image.jpg", content=open(image_path, "rb").read(), content_type="image/jpeg")
        film = Film.objects.create(title="Test Film", host=self.user, category=self.category, image=image_file)

        # Save the film
        film.save()
        #img = Image.open(film.image.path)

    def test_save_method_without_image(self):
        # Test the save method of the Film model when no image is provided
        film = Film.objects.create(title="Test Film", host=self.user, category=self.category)

        # Save the film and check if no image is assigned (no image provided)
        film.save()

        try:
            # Attempt to access the image URL
            image_url = film.image.url
           # _ = film.image.url
            # If we reach here, there's an image, and the test should fail
            self.fail("Image should not be present")
        except ValueError:
            # If a ValueError is raised, there's no image, and the test passes
            pass

   

class ReviewModelTest(TestCase):
    def setUp(self):
        # Set up a user, a category, and a film for testing
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.category = Category.objects.create(title="Action")
        self.film = Film.objects.create(title="Test Film", host=self.user, category=self.category)

    def test_str_representation(self):
        # Test that the string representation of the Review model is the beginning of the review body
        review = Review(user=self.user, film=self.film, rating=4, body="Good movie")
        self.assertEqual(str(review), "Good movie")

    def test_review_creation(self):
        # Test the creation of a review
        review = Review.objects.create(user=self.user, film=self.film, rating=4, body="Good movie")
        # Check if the review is an instance of the Review model and if the count of reviews is 1
        self.assertTrue(isinstance(review, Review))
        self.assertEqual(Review.objects.count(), 1)
