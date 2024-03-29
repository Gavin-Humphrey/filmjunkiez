from django.urls import path
from . import views


urlpatterns = [
    path("follow-page", views.follows_page, name="follow-page"),
    path(
        "confirm-delete/<int:pk>/",
        views.UnfollowUser.as_view(),
        name="confirm-unfollow",
    ),
]
