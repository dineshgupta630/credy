from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'all_genres', views.GenreViewSet)
router.register(r'all_actors', views.ActorViewSet)
router.register(r'movie', views.MovieDetailViewSet)
router.register(r'reviews', views.ReviewCurrentUserViewSet, basename='reviews')
router.register(r'all_reviews', views.ReviewsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]