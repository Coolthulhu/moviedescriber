import json
from django.test import TestCase, SimpleTestCase, Client
from movies.models import Movie
from unittest.mock import patch, MagicMock
from movies import omdb_interface
from movies.views import update_ratings_from_json

class TestAddMovie(TestCase):
    def setUp(self):
        self.client = Client()

    def testInvalidRequest(self):
        response = self.client.post('/movies/', follow=True)
        self.assertNotEqual(200, response.status_code)

    def make_movie(self):
        movie = Movie(title="Hello World")
        movie.save()
        return movie

    @patch('movies.views.get_movie_from_omdbapi', side_effect=make_movie)
    def testValidRequest(self, movie_getter):
        response = self.client.post('/movies/', {"title": "hello world"}, follow=True)
        self.assertEqual(200, response.status_code)

class TestPutMovie(TestCase):
    def setUp(self):
        self.client = Client()

    def testNonexistentMovie(self):
        unused_id = 2
        self.assertFalse(Movie.objects.filter(id=unused_id).exists())
        response = self.client.put('/movies/{}/'.format(unused_id), {}, follow=True)
        self.assertNotEqual(200, response.status_code)

    def testTitleChange(self):
        new_movie = Movie(title="TestMovie")
        new_movie.save()
        new_title = 'NewTitle'
        payload = '{{"title": "{}"}}'.format(new_title)
        response = self.client.put(new_movie.get_absolute_url(), payload, follow=True)
        self.assertEqual(200, response.status_code)
        movie_from_db = Movie.objects.get(id=new_movie.id)
        self.assertEqual(new_title, movie_from_db.title)

    def testInvalidValueChanged(self):
        new_movie = Movie(title="TestMovie")
        new_movie.save()
        response = self.client.put(new_movie.get_absolute_url(), {"bad": "true"}, follow=True)
        self.assertEqual(400, response.status_code)

    def testRatingsChange(self):
        new_movie = Movie(title="TestMovie")
        new_movie.save()
        ratings_array = json.loads('[{"source": "s", "value": "v"}]')
        update_ratings_from_json(new_movie.id, ratings_array)
        ratings = Movie.objects.get(id=new_movie.id).rating_set.all()
        self.assertEqual(1, len(ratings))
        self.assertEqual("s", ratings.first().source)
        self.assertEqual("v", ratings.first().value)

    def testRatingsChangeThroughPut(self):
        new_movie = Movie(title="TestMovie")
        new_movie.save()
        payload = json.dumps({"ratings": '[{"source": "s", "value": "v"}]'})
        response = self.client.put(new_movie.get_absolute_url(), payload, follow=True)
        self.assertEqual(200, response.status_code)
        ratings = Movie.objects.get(id=new_movie.id).rating_set.all()
        self.assertEqual(1, len(ratings))
        self.assertEqual("s", ratings.first().source)
        self.assertEqual("v", ratings.first().value)

class TestDeleteMovie(TestCase):
    def setUp(self):
        self.client = Client()

    def testDeleteInvalidMovie(self):
        response = self.client.delete('/movies/1', follow=True)
        self.assertNotEqual(200, response.status_code)

    def testDeleteExistingMovie(self):
        movie = Movie()
        movie.save()
        self.assertTrue(Movie.objects.filter(id=1).exists())
        response = self.client.delete('/movies/1/', follow=True)
        self.assertEqual(200, response.status_code)
        self.assertFalse(Movie.objects.filter(id=1).exists())

    def testDeleteMovieTwice(self):
        movie = Movie()
        movie.save()
        self.assertTrue(Movie.objects.filter(id=1).exists())
        response = self.client.delete('/movies/1/', follow=True)
        self.assertEqual(200, response.status_code)
        self.assertFalse(Movie.objects.filter(id=1).exists())
        response = self.client.delete('/movies/1/', follow=True)
        self.assertNotEqual(200, response.status_code)

class TestOMDBInterface(TestCase):
    def testEmptyInput(self):
        omdb_interface.omdb_to_model({})

    def testInvalidRatings(self):
        self.assertRaises(TypeError, omdb_interface.omdb_to_model, json={"Ratings": "not an array"})

    def testUnusedValue(self):
        self.assertRaises(KeyError, omdb_interface.omdb_to_model, json={"bad": "true"})

    def testValidValue(self):
        valid_value = {'Title': 'Title','Ratings': [{'Source': 's', 'Value': 'v'}, {'Source': 's2', 'Value': 'v2'}], 'Response': 'True'}
        omdb_interface.omdb_to_model(valid_value)
