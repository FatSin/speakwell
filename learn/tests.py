from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Language

# Create your tests here.

class TestRoutes(TestCase):
    """Test the views of 'learn' app."""
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_voc(self):
        response = self.client.get(reverse('voc'))
        self.assertEqual(response.status_code, 302)

    def test_stats(self):
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 302)

    def test_quizz(self):
        response = self.client.get(reverse('quizz'))
        self.assertEqual(response.status_code, 302)



class TestRegistration(TestCase):
    def setUp(self):
        self.username = "usertest"
        self.password = "12345678"
        self.email = "usertest@mail.com"
        self.lang = 'Japanese'
        self.lang_dis = "English"

        Language.objects.create(NameEng=self.lang, Code='code1')
        Language.objects.create(NameEng=self.lang_dis, Code='code2')

    def test_registration(self):

        response = self.client.post(reverse('submit_form_html'),{
            'username':self.username,
            'password':self.password,
            'email':self.email,
            'lang':self.lang,
            'lang-display':self.lang_dis,
            'create-user':True
        })
        check_user = User.objects.filter(username=self.username).count()
        self.assertEqual(check_user, 1)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('voc'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('quizz'))
        self.assertEqual(response.status_code, 200)
