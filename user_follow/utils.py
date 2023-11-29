from .models import UserFollows



def get_follows(user):

    follows = UserFollows.objects.filter(user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.followed_user)

    return followed_users