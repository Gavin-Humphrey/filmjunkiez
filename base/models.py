from django.db import models
#from django.contrib.auth.models import User
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Just added for the test. Can remove if affecting user functioning
    def __str__(self):
        return self.name or self.username


class Category(models.Model):
    title = models.CharField(max_length=200)
    

    def __str__(self) -> str:
        return self.title


class Film(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=200, default='Unknown')
    lead = models.CharField(max_length=200, default='Unknown')
    release_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to="film_img")
    video = models.FileField(blank=True, null=True, upload_to="film_videos", help_text="Upload an MP4 video file")
    average_rating = models.FloatField(null=True, blank=True)


    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self) -> str:
        return self.title

    def calculate_average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
        else:
            self.average_rating = None

    if image is True:
        def save(self, *args, **kwargs):
            super().save()
            img = ImageOps.contain(Image.open(self.image.path), (200, 200), method=3)
            img.save(self.image.path)

            if not self.pk and self.video:
            # Will handle video processing or validation, here later, if needed
                pass

            super().save(*args, **kwargs)
    
       

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    null=True, blank=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self) -> str:
        return self.body[0:50]




"""

class Film(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=200, default='Unknown')
    lead = models.CharField(max_length=200, default='Unknown')
    release_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to="film_img")
    video = models.FileField(blank=True, null=True, upload_to="film_videos", help_text="Upload an MP4 video file")
    average_rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["-updated", "-created"]

"""