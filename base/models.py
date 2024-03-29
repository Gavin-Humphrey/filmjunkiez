from django.db import models
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import AbstractUser

from cloudinary.models import CloudinaryField
from django.conf import settings
import os


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.name or self.username

    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return f"{settings.STATIC_URL}img/avatar.svg"

    class Meta:
        db_table = "auth_user"


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title


class Film(models.Model):
    # host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=200, default="Unknown")
    lead = models.CharField(max_length=200, default="Unknown")
    release_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to="film_img")

    if "CI" in os.environ or settings.DEBUG:
        video = models.FileField(
            blank=True,
            null=True,
            upload_to="film_videos",
            help_text="Upload an MP4 video file",
        )
    else:
        video = CloudinaryField(
            blank=True,
            null=True,
            help_text="Upload an MP4 video file",
            resource_type="video",
        )

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

    def save(self, *args, **kwargs):
        # Check if image field is not None
        if self.image:
            # Check if image has been modified
            if (
                hasattr(self, "_original_image")
                and self.image.name != self._original_image
            ):
                img = Image.open(self.image.path)
                img.save(self.image.path)

            # Store the original image filename after the save
            self._original_image = self.image.name  # Store filename

        # Call the parent save method to save other fields
        super().save(*args, **kwargs)

        # Check if video field is not None
        if not self.pk and self.video:
            pass


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True
    )
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self) -> str:
        return self.body[0:50]
