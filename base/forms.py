from xml.etree.ElementInclude import include
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import  Film, Review, User






class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class FilmForm(ModelForm):
    image = forms.ImageField(label="Image", required=False)
    class Meta:
        model = Film
        fields = "__all__"
        exclude = ["host", "participants", "average_rating", "category"]



class ReviewForm(ModelForm):
    rating = forms.ChoiceField(
        initial=1,
        label="Rating",
        widget=forms.RadioSelect(),
        choices=(
            (1, "1 star"),
            (2, "2 stars"),
            (3, "3 stars"),
            (4, "4 stars"),
            (5, "5 stars"),
        )
    )
    class Meta:
        model = Review
        fields = ("rating", "body",)