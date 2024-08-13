from django.urls import path
from . import views


urlpatterns = [
    path("login", views.loginPage, name="login"),
    path("register-user", views.registerUser, name="register-user"),
    path("profile/<str:pk>", views.userProfile, name="user-profile"),
    path("modify-user", views.modifyUser, name="modify-user"),
    path("logout", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("film/<str:pk>/", views.film, name="film"),
    path("film-details/<str:pk>/", views.filmDetails, name="film-details"),
    path("create-film", views.createFilm, name="create-film"),
    path("update-film/<str:pk>/", views.updateFilm, name="update-film"),
    path("delete-film/<str:pk>/", views.deleteFilm, name="delete-film"),
    path("categories", views.categoriesPage, name="categories"),
    path("delete-review/<str:pk>/", views.deleteReview, name="delete-review"),
    path("activity", views.activityPage, name="activity"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path("contact/", views.contact, name="contact"),
]
