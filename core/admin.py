from django.contrib import admin
from .models import Person, Movie, Review, Genre

admin.site.register(Person)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
