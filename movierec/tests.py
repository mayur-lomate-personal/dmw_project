from django.test import TestCase, Client
from . import views
from movierec.views import forlike

# Create your tests here.
class TestViews(TestCase):

    def test_a(self):
        self.assertEqual(1,1)

    def test_mytest1(self):
        response = Client().get('/creator/')
        self.assertEqual(response.status_code, 200)

    def test_mytes2(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'login.html')

    def test_mytest3(self):
        response = Client().get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_mytest4(self):
        self.assertEqual(len(forlike()), 10)



