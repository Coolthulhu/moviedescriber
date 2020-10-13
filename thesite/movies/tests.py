from django.test import TestCase, SimpleTestCase, Client
from movies.models import Movie

class TestAddMovie(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def testInvalidRequest(self):
        response = self.client.post('/movies/', follow=True)
        self.assertNotEqual(200, response.status_code)

    def testValidRequest(self):
        response = self.client.post('/movies/', {"title": "hello world"})
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
        new_movie = Movie("TestMovie").save()
        new_title = 'NewTitle'
        response = self.client.put(new_movie.get_absolute_url(), {'title': new_title}, follow=True)
        self.assertEqual(200, response.status_code)
        movie_from_db = Movies.objects.get(id=new_movie.id)
        self.assertEqual(new_title, movie_from_db.title)


class TestOMDBInterface(TestCase):
    def testEmptyInput(self):
        pass
