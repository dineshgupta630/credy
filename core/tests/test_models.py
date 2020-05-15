from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Movie, Genre

User = get_user_model()


class CreateUserMixin(APITestCase):
    url = reverse('obtain_jwt_token')

    def setUp(self):
        self.username = "user"
        self.email = "user@outlook.com"
        self.password = "password"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        resp = self.client.post(self.url, {'username': 'user', 'password': 'password'}, format='json')
        self.token = resp.data['token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)


class MovieAPIViewTestCase(CreateUserMixin):
    """
    Testing the Movie API
    """

    def test_movie_api(self):
        resp = self.client.get('/movies/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_movie_api_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + 'wrong-token')
        resp = self.client.get('/movies/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_movie_object_filtering(self):
        Movie.objects.create(
            title='Casper', release_date=datetime.now(), slug='casper',
            plot='Casper is a 1995 American fantasy comedy film directed by Brad Silberling, in his feature directorial',
            budget=65000000,
        )
        resp = self.client.get('/movies/?budget_min=60000000&budget_max=75000000')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['count'], 1)


class ReviewAPIViewTestCase(CreateUserMixin):
    """
    Testing the Review API
    """

    def test_review_api(self):
        resp = self.client.get('/reviews/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_review_api_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + 'wrong-token')
        resp = self.client.get('/reviews/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_creation(self):
        movie_obj = Movie(
            title='Casper', release_date=datetime.now(), slug='casper',
            plot='Casper is a 1995 American fantasy comedy film directed by Brad Silberling, in his feature directorial',
            budget=65000000,
        )
        movie_obj.save()
        data = {
            "rating_value": "5",
            "review": "A must see movie for children",
            "slug": "casper"
        }
        post_resp = self.client.post('/reviews/', data)
        self.assertEqual(post_resp.status_code, status.HTTP_201_CREATED)

        get_resp = self.client.get('/reviews/')
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(get_resp.json()['count'], 1)


class GenreAPIViewTestCase(CreateUserMixin):
    """
    Testing the Genre API
    """

    def test_genre_api(self):
        resp = self.client.get('/all_genres/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_genre_api_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + 'wrong-token')
        resp = self.client.get('/all_genres/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_genre_creation(self):
        genre_obj = Genre(genre_name='Action')
        genre_obj.save()
        get_resp = self.client.get('/all_genres/')
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(get_resp.json()['count'], 1)
