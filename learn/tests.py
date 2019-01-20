from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class Routetesting(TestCase):
    """Test the views of 'learn' app."""
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
"""
    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class TestRegistration(TestCase):
    #Test registration
    def create_user(self):
        user = ""
        self.user = user

    def signin(self):
        new_user = new_user(self.user)

        # assert new_user[0][0].ProductName == "Test-comte"
        # assert new_user[1] == Product.objects.get(ProductName="Comté AOP (34% MG)").id
        # assert new_user[2] == self.sub.id
        # assert new_user[3] == self.sub.ImageLink
        # assert new_user[4] == self.sub.Grade.upper()

class TestLogin(TestCase):
    #Test Login in, but might be redundant!

"""