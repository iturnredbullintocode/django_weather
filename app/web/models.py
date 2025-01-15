import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone



# not in use, don't want to litter the DB with zipcodes since we have em in cache
# unless we need to do more operations on them
'''
class Zipcode(models.Model):
    zipcode = models.IntegerField(label="5 digit US zipcode", max_value=99999, min_value=1)
    scraped_date = models.DateTimeField("date scraped from api")

    def __str__(self):
        return self.zipcode

    # decorates specifically the was_updated_recently method
    # changes how this model is displayed on the admin console
    @admin.display(
        # the default display shows "False" or "True,
        # this changes it to checkmarks or crosses
        boolean=True,
        ordering="scraped_date",
        # the default display would show `was_updated_recently` without underscores
        # this changes it to more humanly understandable words
        description="Updated recently?",    )
    def was_updated_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
'''

