import django_filters

from .models import Movie, Genre, Person, Review


class MovieFilter(django_filters.FilterSet):
    release_date_start = django_filters.IsoDateTimeFilter(field_name="release_date", lookup_expr='gte')
    release_date_end = django_filters.IsoDateTimeFilter(field_name="release_date", lookup_expr='lte')
    actor = django_filters.ModelMultipleChoiceFilter(
        field_name='actors__name',
        to_field_name='name',
        queryset=Person.objects.all()
    )
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre__genre_name',
        to_field_name='genre_name',
        queryset=Genre.objects.all()
    )
    budget = django_filters.RangeFilter(field_name="budget", lookup_expr='range')

    class Meta:
        model = Movie
        fields = ['release_date_start', 'release_date_end', 'actor', 'genre', 'budget']


class ReviewFilter(django_filters.FilterSet):
    movie = django_filters.ModelMultipleChoiceFilter(
        field_name='movie__slug',
        to_field_name='slug',
        queryset=Movie.objects.all()
    )

    class Meta:
        model = Review
        fields = ['movie']
