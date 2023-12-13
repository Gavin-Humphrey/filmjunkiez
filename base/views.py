import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Film, Review, User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, FilmForm, UserForm #, ReviewForm
#from user_follow.utils import get_follows
from user_follow.models import UserFollows
from django.contrib.auth.forms import AuthenticationForm 
from .permissions import is_superuser, staff_required
from django.shortcuts import get_object_or_404
from django.db.models import Avg




logger = logging.getLogger(__name__)



def registerUser(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_signup.html', {'form': form})


def loginPage(request):
    page = "login"
    
    if request.user.is_authenticated:
        return redirect("home")

    try:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect("home")
            else:
                raise ValueError("Invalid username or password")
        else:
            form = AuthenticationForm()

    except Exception as e:
        logger.error(f"An error occurred in loginPage view: {e}")
        messages.error(request, "Invalid username or password.")

    context = {"page": page, "form": form}
    return render(request, "base/login_signup.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    #films = Film.objects.filter(host=user) # Fetches all films associated with the user, by filtering the Film objects where the host field matches the specific user object
    films = user.film_set.all()# Fetches all films associated with the user using the reverse relation
    #film_posts = Review.objects.filter(user=user)
    film_posts = user.review_set.all()
    categories = Category.objects.all()  
    context = {"user": user, "films": films, "film_posts": film_posts, "categories": categories}
    return render(request, "base/profile.html", context)


@login_required(login_url='login')
def modifyUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/modify_user.html', {'form': form})


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else "" # The line below makes this search query a bit more concise, by using the second argument, "", to specify the default value to use if "q" is not present in the URL. 
    #q = request.GET.get("q", "")
    films = Film.objects.filter(
        Q(category__title__icontains=q) | 
        Q(title__icontains=q) |
        Q(description__icontains=q)
        ) # We then provide the film queryset with q, which is the search. Remember queryset is the way of retirving data from the database
    categories = Category.objects.all()#[:3]
    film_count = films.count()
    film_reviews = Review.objects.filter(Q(film__category__title__icontains=q))
    context = {
        "films": films,
        "categories": categories,
        "film_count": film_count,
        "film_reviews": film_reviews
    }
    return render(request, "base/home.html", context)


def film(request, pk):
    film = get_object_or_404(Film, id=pk)
    reviews = film.review_set.all()
    participants = film.participants.all()


    # Check if the user is following the host
    following_host = request.user.is_authenticated and request.user != film.host \
                     and UserFollows.objects.filter(followed_user=film.host, user=request.user).exists()
    
    # Check if the user has already rated the film
    #user_rated = Review.objects.filter(user=request.user, film=film).exists()
    user_rated = Review.objects.filter(user=request.user if request.user.is_authenticated else None, film=film).exists()

    if request.method == "POST":
        if following_host:
            rating = request.POST.get("rating")
            body = request.POST.get("body")

            if rating and body:
                if not user_rated:
                    review = Review.objects.create(
                        user=request.user,
                        film=film,
                        rating=rating,
                        body=body
                    )
                    film.participants.add(request.user)
                    # Recalculate average rating and update the film model
                    film.calculate_average_rating()
                    film.save()

                    messages.success(request, "Review successfully added!")
                    return redirect("film", pk=film.id)
                else:
                    messages.error(request, "You have already rated this film.")
            elif user_rated:
                # If the user has already rated, allow submitting a review without a rating
                review = Review.objects.create(
                    user=request.user,
                    film=film,
                    rating=None,  # or any default value for rating
                    body=body
                )
                messages.success(request, "Review successfully added!")
                return redirect("film", pk=film.id)
            else:
                messages.error(request, "Both rating and review are required.")
        else:
            messages.error(request, "You need to follow the film's host to submit a review.")
            
    # Recalculate average rating
    average_rating = Review.objects.filter(film=film).aggregate(Avg('rating'))['rating__avg']

    # If the user has not rated, show a prompt message
    #if not user_rated:
        #messages.info(request, "You haven't rated this film yet. Please rate it below.")

    context = {
        "film": film, 
        "film_reviews": reviews, 
        "participants": participants, 
        "average_rating": average_rating, 
        "video_url": film.video.url if film.video else None 
        }
    return render(request, "base/film.html", context)


def filmDetails(request, pk):
    film = get_object_or_404(Film, id=pk)
    context = {"film": film}
    return render(request, "base/film_details.html", context)


@login_required(login_url="login")
@staff_required
def createFilm(request):
    form = FilmForm(request.POST, request.FILES)
    categories = Category.objects.all()

    if request.method == "POST":
        category_title = request.POST.get("category")
        category, created = Category.objects.get_or_create(title=category_title)
        image = request.FILES.get("image", None)

        film = Film(
            host=request.user,
            category=category,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            director=request.POST.get("director"),
            lead=request.POST.get("lead"),
            release_date=request.POST.get("release_date"),
            duration=request.POST.get("duration"),
            image=image
        )
        film.save()

        return redirect("home")

    context = {"form": form, "categories": categories}
    return render(request, "base/film_form.html", context)


def updateFilm(request, pk):
    film = Film.objects.get(id=pk)
    form = FilmForm(request.POST or None, request.FILES or None, instance=film)
    categories = Category.objects.all()

    if request.user != film.host:
        #return HttpResponse("You do not have the permission to do this")
        messages.error(request, "You do not have the permission to do this")
        return redirect("film", pk=film.id)

    if request.method == "POST":
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            category_title = request.POST.get("category")
            category, created = Category.objects.get_or_create(title=category_title)

            # Update film instance with form data
            film = form.save(commit=False)
            film.category = category
            film.save()
            messages.success(request, "Film updated successfully.")
            return redirect("film", pk=film.id)

    context = {"form": form, "categories": categories, "film": film}
    return render(request, "base/film_form.html", context)
###########

"""def updateFilm(request, pk):
    film = Film.objects.get(id=pk)
    form = FilmForm(request.POST or None, request.FILES or None, instance=film)
    categories = Category.objects.all()

    if request.user != film.host:
        messages.error(request, "You do not have the permission to do this")
        return redirect("film", pk=film.id)

    if request.method == "POST":
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            # Update film instance with form data
            film = form.save(commit=False)

            # Get or create the category based on the form data
            category_title = request.POST.get("category")
            category, created = Category.objects.get_or_create(title=category_title)

            film.category = category
            film.save()

            return redirect("film", pk=film.id)

    context = {"form": form, "categories": categories, "film": film}
    return render(request, "base/film_form_update.html", context)"""

#######

@login_required(login_url="login")
def deleteFilm(request, pk):
    film = Film.objects.get(id=pk)
    if request.user != film.host and not request.user.is_superuser:
        return HttpResponse("You do not have the permission to do this")
    if request.method == "POST":
        film.delete()
        return redirect("home")
    context = {"obj": film}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    film = review.film  # Get the film associated with the review
    if request.user != review.user and not request.user.is_superuser:
        return HttpResponse("You do not have the permission to do this")
    if request.method == "POST":
        review.delete()
        return redirect("film",  film.id)
    context = {"obj": review}
    return render(request, "base/delete.html", context)


def categoriesPage(request):
    q = request.GET.get("q", "")
    categories = Category.objects.filter(title__icontains=q)
    context = {"categories": categories}
    return render(request, "base/categories.html", context)


def activityPage(request):
    film_reviews = Review.objects.all()
    context = {"film_reviews": film_reviews} 
    return render(request, "base/activity.html", context)
