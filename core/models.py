import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def get_user_profile_img_upload_path(instance, orig_filename):
    upload_folder = 'movie_poster'
    filename = '{}_{}'.format(instance.release_date.strftime("%d_%B_%Y"), orig_filename)
    return os.path.join(upload_folder, filename)


class TimeModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    edited_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True


class Person(TimeModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)


class Movie(TimeModel):
    RATINGS = (
        (0, 'NR - Not Rated'),
        (1,
         'U - Unrestricted public exhibition'),
        (2,
         'U/A - Parental Guidance Suggested'),
        (3, 'A - Restricted'),
    )
    slug = models.CharField(max_length=140, unique=True)
    title = models.CharField(max_length=140)
    plot = models.TextField()
    release_date = models.DateField()
    budget = models.PositiveIntegerField()
    rating = models.IntegerField(
        choices=RATINGS,
        default=0)
    website = models.URLField(blank=True)
    actors = models.ManyToManyField(to='Person', related_name='acting_credits', blank=True)
    genre = models.ManyToManyField(to='Genre', related_name='genre')
    movie_poster = models.ImageField(verbose_name='Photo', upload_to=get_user_profile_img_upload_path,
                                     storage=default_storage, max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('release_date', 'title')

    def __str__(self):
        return '{} ({})'.format(self.title, self.release_date)


class Review(TimeModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, )
    rating_value = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.CharField(max_length=1024, blank=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return '{} ({}) {}'.format(self.user, self.rating_value, self.movie.title)


class Genre(TimeModel):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.genre_name)

