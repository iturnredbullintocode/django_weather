from django.test import TestCase
from django.urls import reverse

from .forms import ZipcodeForm, RegexZipcodeForm




class HomeViewTests(TestCase):

    def test_home(self):
        """
        Making sure regular home view works.
        """
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)





class ZipcodeFormTests(TestCase):

    def test_zipcode_works(self):
        """
        making sure zipcode works fine despite a throwaway form field, gets cast to string
        """
        data = {"zipcode": "10019",
                "extra_throwaway_field": "test",   }
        form = ZipcodeForm(data)
        self.assertIs(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['zipcode'], '10019')

    def test_zipcode_too_high(self):
        """
        zipcode can't be too high
        """
        data = {"zipcode": "99999999",
                "extra_throwaway_field": "test",   }
        form = ZipcodeForm(data)
        self.assertIs(form.is_valid(), False)



class RegexZipcodeFormTests(TestCase):

    def test_regex_zipcode_format(self):
        """
        making sure the regex version of the zipcode is fine
        """
        form = RegexZipcodeForm({"zipcode": "10019"})
        self.assertIs(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['zipcode'], '10019')
        form = RegexZipcodeForm({"zipcode": "058843737272"})
        self.assertIs(form.is_valid(), False)
        form = RegexZipcodeForm({"zipcode": "1oo19"})
        self.assertIs(form.is_valid(), False)
        form = RegexZipcodeForm({"zipcode": "1"})
        self.assertIs(form.is_valid(), False)




