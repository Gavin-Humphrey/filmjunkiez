from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_follow.forms import FollowForm
from user_follow.models import UserFollows
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView

from base.models import User


@login_required
def follows_page(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    ####

    if request.method == "POST":
        form = FollowForm(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST["followed_user"])
                if request.user == followed_user:
                    messages.error(request, "You can't follow yourself!")
                else:
                    try:
                        UserFollows.objects.create(
                            user=request.user, followed_user=followed_user
                        )
                        messages.success(
                            request, f"You are now following {followed_user} !"
                        )
                    except IntegrityError:
                        messages.error(
                            request, f"You are already following {followed_user} !"
                        )
            except User.DoesNotExist:
                messages.error(
                    request,
                    f'A user with username: {form.data["followed_user"]} does not exist.',
                )
    else:
        form = FollowForm()

    user_follows = UserFollows.objects.filter(
        user=request.user, followed_user__username__icontains=q
    ).order_by("followed_user")
    followed_by = UserFollows.objects.filter(
        followed_user=request.user, user__username__icontains=q
    ).order_by("user")
    context = {
        "form": form,
        "user_follows": user_follows,
        "followed_by": followed_by,
        "title": "follows",
    }
    return render(request, "user_follow/follow_page.html", context)


class UnfollowUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserFollows
    success_url = "/follow-page"
    context_object_name = "unfollow"

    def test_func(self):
        unfollow = self.get_object()
        if self.request.user == unfollow.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(
            self.request,
            f"You have stopped following {self.get_object().followed_user}.",
        )
        return super(UnfollowUser, self).delete(request, *args, **kwargs)
