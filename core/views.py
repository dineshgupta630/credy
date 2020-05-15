import django_filters.rest_framework as filters
from django.db.models import Sum, F, Avg
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .filters import MovieFilter, ReviewFilter
from .models import Movie, Genre, Person, Review
from .serializers import MovieSerializer, GenreSerializer, ActorSerializer, ReviewSerializer


class MovieViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer
    filter_class = MovieFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Person.objects.all()
    serializer_class = ActorSerializer


class MovieDetailViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class PaginationWithAggregates(LimitOffsetPagination):
    """
    Custom Pagination class which overrides the default, used for showing the aggregate of Rating.
    """

    def paginate_queryset(self, queryset, request, view=None):
        self.average_rating = queryset.annotate(subtotal=Sum('rating_value')).aggregate(total=Avg(F('subtotal')))
        return super(PaginationWithAggregates, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        paginated_response = super(PaginationWithAggregates, self).get_paginated_response(data)
        paginated_response.data['average_rating'] = self.average_rating['total']
        return paginated_response


class ReviewCurrentUserViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PaginationWithAggregates

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter()
    filter_class = ReviewFilter
    pagination_class = PaginationWithAggregates
