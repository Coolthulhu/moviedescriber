from django.test import TestCase, SimpleTestCase, Client
from movies.models import Movie
from unittest.mock import patch

class TestAddMovie(TestCase):
    def setUp(self):
        self.client = Client()

    def testInvalidRequest(self):
        response = self.client.post('/movies/', follow=True)
        self.assertNotEqual(200, response.status_code)

    def mock_movie_getter(self, title, *args, **kwargs):
        return Movie(title=title)

    @patch('movies.omdb_interface.get_movie_from_omdbapi', side_effect=mock_movie_getter)
    def testValidRequest(self, movie_getter):
        response = self.client.post('/movies/', {"title": "hello world"}, follow=True)
        self.assertEqual(200, response.status_code)

class TestPutMovie(TestCase):
    def setUp(self):
        self.client = Client()
        Movie.objects.all().delete()

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


class TestOMDBInterface(TestCase):
    def testEmptyInput(self):
        pass
