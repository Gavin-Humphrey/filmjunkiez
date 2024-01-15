from django.shortcuts import render
from django.http import HttpResponse
from sentry_sdk import capture_exception


def index(request):
    return render(request, "home.html")


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


def trigger_error(request):
    try:
        # This will trigger a division by zero exception
        division_by_zero = 1 / 0
    except Exception as e:
        # Capture the exception and send it to Sentry
        capture_exception(e)
        return HttpResponse("An error occurred. Check your Sentry dashboard for details.")


