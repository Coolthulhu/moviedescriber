from django.test import TestCase, SimpleTestCase, Client
from movies.models import Movie
from comments.models import Comment
from comments.views import get_ranked_movies

class TestAddComment(TestCase):
    def setUp(self):
        self.client = Client()

    def testInvalidMovieId(self):
        response = self.client.post('/comments/', {"movie": "", "text": "aaa"}, follow=True)
        self.assertEqual(404, response.status_code)

    def testAddComment(self):
        Movie().save()
        response = self.client.post('/comments/', {"movie": "1", "text": "aaa"}, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Comment.objects.all().count())

class TestListComments(TestCase):
    def setUp(self):
        self.client = Client()

    def testListUnfilteredComments(self):
        movie = Movie(title="1")
        movie.save()
        Comment.objects.bulk_create([Comment(movie=movie, date="2000-01-01") for i in range(3)])
        response = self.client.get('/comments/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json()))

    def testListFilteredComments(self):
        movie1 = Movie(title="1")
        movie1.save()
        movie2 = Movie(title="2")
        movie2.save()
        Comment.objects.bulk_create([Comment(movie=movie1, date="2000-01-01") for i in range(2)])
        Comment.objects.bulk_create([Comment(movie=movie2, date="2000-01-01") for i in range(3)])
        response = self.client.get('/comments/', {"id": 1})
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json()))

class TestTopCommented(TestCase):
    def setUp(self):
        self.client = Client()

    def testCorrectRankOrder(self):
        movies = [Movie(title=str(i)) for i in range(4)]
        for m in movies:
            m.save()
        Comment.objects.bulk_create([Comment(movie=movies[0], date="2000-01-02") for j in range(1)])
        Comment.objects.bulk_create([Comment(movie=movies[1], date="2000-01-02") for j in range(2)])
        Comment.objects.bulk_create([Comment(movie=movies[2], date="2000-01-02") for j in range(2)])
        Comment.objects.bulk_create([Comment(movie=movies[3], date="2000-01-02") for j in range(3)])
        ranked = get_ranked_movies("2000-01-01", "2000-01-03")
        self.assertEqual(1, ranked[0]['rank'])
        self.assertEqual(2, ranked[1]['rank'])
        self.assertEqual(2, ranked[2]['rank'])
        self.assertEqual(3, ranked[3]['rank'])
        self.assertEqual(4, ranked[0]['movie_id'])
        self.assertEqual(1, ranked[3]['movie_id'])

    def testCommentsOutsideRangeDontCount(self):
        movies = [Movie(title=str(i)) for i in range(4)]
        for m in movies:
            m.save()
        Comment.objects.bulk_create([Comment(movie=movies[0], date="2000-01-02") for j in range(1)])
        Comment.objects.bulk_create([Comment(movie=movies[1], date="2000-01-04") for j in range(2)])
        Comment.objects.bulk_create([Comment(movie=movies[2], date="2000-01-04") for j in range(2)])
        Comment.objects.bulk_create([Comment(movie=movies[3], date="2000-01-04") for j in range(3)])
        ranked = get_ranked_movies("2000-01-01", "2000-01-03")
        self.assertEqual(1, ranked[0]['movie_id'])
