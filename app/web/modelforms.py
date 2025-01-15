from django.forms import ModelForm
from .models import Zipcode


# not in use, don't want to litter the DB with zipcodes since we have em in cache
# unless we need to do more operations on them
'''
class ZipcodeForm(ModelForm):
    class Meta:
        model = Zipcode
        fields = ["zipcode"] # not including 'scraped_date'


# creating an empty form - can be used to add zipcode to database
form = ZipcodeForm()

# creating a semi-populated form - can be used to update zipcode in database
a_zipcode = Zipcode.object.get(pk='10019')
form = ZipcodeForm(instance=a_zipcode)
'''