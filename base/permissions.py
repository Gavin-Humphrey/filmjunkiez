from functools import wraps
from django.http import HttpResponseForbidden




def is_superuser(user):
    return user.is_superuser



def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is a staff member
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to create films.")
    return _wrapped_view

