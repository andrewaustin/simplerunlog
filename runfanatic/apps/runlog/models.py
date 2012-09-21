from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Run(models.Model):
    """Stores information about a particular run.

    :attr User User: The user who performed the run.
    :attr date date: The date of the run.
    :attr float distance: The length of the run.
    :attr int hours: The number of hours the run took.
    :attr int minutes: The number of minutes the run took.
    :attr int seconds: The number of secondst the run took.
    """

    user = models.ForeignKey(User)
    date = models.DateField('Date of Run')
    distance = models.FloatField('Distance')
    hours = models.IntegerField('Hours')
    minutes = models.IntegerField('Minutes')
    seconds = models.IntegerField('Seconds')

    def clean(self):
        """Provides basic validation that minutes and seconds must be less than
        60.

        :raises ValidationError: Error occurs if minutes or seconds > 59.
        """
        if self.seconds >= 60:
            raise ValidationError("Seconds must be less than 60")
        if self.minutes >= 60:
            raise ValidationError("Minutes must be less than 60")


class UserProfile(models.Model):
    """Stores user profile information and settings.

    :attr User User: The user who is associated with the profile.
    :attr day_week_starts String: The start of the week for the user.
    """

    user = models.OneToOneField(User)

    day_week_starts = models.CharField(
            max_length=6,
            choices=(
                ('Sunday', 'Sunday'),
                ('Monday', 'Monday'),
            ),
            default='Sunday'
            )
    units = models.CharField(
            max_length=2,
            choices=(
                ('mi', 'Miles'),
                ('km', 'Kilometers'),
            ),
            default='mi'
            )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
