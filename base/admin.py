from django.contrib import admin

from .models import User, Category, Film, Review


admin.site.register(User)
admin.site.register(Film)
admin.site.register(Category)
admin.site.register(Review)
