from django.test import TestCase
from django.urls import reverse




class HomeViewTests(TestCase):

    def test_home(self):
        """
        Making sure regular home view works.
        """
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

