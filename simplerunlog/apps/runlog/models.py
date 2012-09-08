from django.db import models
from django.core.exceptions import ValidationError

class Run(models.Model):
    """Stores information about a particular run.

    :attr date date: The date of the run
    :attr float distance: The length of the run
    :attr int hours: The number of hours the run took.
    :attr int minutes: The number of minutes the run took.
    :attr int seconds: The number of secondst the run took.
    """

    date = models.DateField('Date of Run')
    distance = models.FloatField('Distance')
    hours = models.IntegerField('Hours')
    minutes = models.IntegerField('Minutes')
    seconds = models.IntegerField('Seconds')

    def clean(self):
        """Provides basic validation that minutes and seconds must be less than
        60.

        :raises ValidationError: Error occurs if minutes or seconds > 60.
        """

        if self.seconds >= 60:
            raise ValidationError("Seconds must be less than 60")
        if self.minutes >= 60:
            raise ValidationError("Minutes must be less than 60")

