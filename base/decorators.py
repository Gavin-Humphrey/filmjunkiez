from functools import wraps
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import user_passes_test




def is_superuser(user):
    return user.is_superuser


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is a staff member
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have the permission to add films for review. Contact us for a 'Host privilege'")
    return _wrapped_view


def user_not_authenticated(view_func):
    """
    Decorator to redirect authenticated users away from the signup page.
    """
    @user_passes_test(lambda user: not user.is_authenticated, login_url='home')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return wrapper
