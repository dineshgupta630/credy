from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework import serializers

from .models import Movie, Person, Genre, Review

UserModel = get_user_model()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Movie
        fields = (
            'title', 'plot', 'release_date', 'budget', 'genre', 'rating', 'actors', 'release_date', 'slug', 'movie_poster')


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','username']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    slug = serializers.CharField(source='movie.slug')

    class Meta:
        depth = 2
        model = Review
        fields = ('rating_value', 'review', 'slug', 'user')

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            rating = validated_data.pop('rating_value')
            review = validated_data.pop('review')
            slug = validated_data.pop('movie').pop('slug')
            movie_obj = Movie.objects.filter(slug=slug).first()
            review_obj = Review.objects.filter(user=user, movie=movie_obj)
            if review_obj:
                review_obj.update(rating_value=rating, review=review)
            else:
                review_obj.create(rating_value=rating, review=review, movie=movie_obj, user=user)
            return review_obj.first()
