from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client

from apps.runlog.models import Run
from apps.runlog.models import UserProfile


class ModelTest(TestCase):
    """Class for testing models in the runlog app."""

    def setUp(self):
        """Create a test user before running tests."""
        self.user = User.objects.create_user("user")

    def test_run_minutes_errors_if_invalid(self):
        """Test that we raise a ValidationError if minutes > 59."""
        aRun = Run(user=self.user, date="2011-7-21", hours=0,
                minutes=61, seconds=17, distance=4)
        self.assertRaises(ValidationError, aRun.full_clean)
        aRun = Run(user=self.user, date="2011-7-21", hours=0,
                minutes=60, seconds=17, distance=4)
        self.assertRaises(ValidationError, aRun.full_clean)

    def test_run_seconds_errors_if_invalid(self):
        """"Test that we raise a Validation Error if minutes > 59."""
        aRun = Run(user=self.user, date="2011-7-22", hours=0,
                minutes=19, seconds=61, distance=4)
        self.assertRaises(ValidationError, aRun.full_clean)
        aRun = Run(user=self.user, date="2011-7-22", hours=0,
                minutes=19, seconds=60, distance=4)
        self.assertRaises(ValidationError, aRun.full_clean)

    def tearDown(self):
        """Destroy any created db objects."""
        User.objects.all().delete()
        Run.objects.all().delete()
        UserProfile.objects.all().delete()


class ViewsTest(TestCase):
    """Class for testing views in the runlog app."""

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user("user", password="pass")

    def test_index_not_logged_in(self):
        """"Index should return 200 status code if not authenticated."""
        status = self.c.get('/').status_code
        self.assertEquals(status, 200)

    def test_index_logged_in(self):
        """Index should redirect to dashboard if logged in."""
        self.c.login(username='user', password='pass')
        status = self.c.get('/').status_code
        self.assertEquals(status, 302)

    def test_dashboard_not_logged_in(self):
        """"Dashboard should return 302 status code if not authenticated."""
        status = self.c.get('/dashboard/').status_code
        self.assertEquals(status, 302)

    def test_dashboard_logged_in(self):
        """Dashboard should return 200 if authenticated"""
        self.c.login(username='user', password='pass')
        status = self.c.get('/dashboard/').status_code
        self.assertEquals(status, 200)

    def test_calculates_six_week_avg_properly(self):
        """Dashboard view should calculate the 6 week average properly."""
        #Create a bunch of runs to average
        NOW = datetime.now()
        Run1 = Run(user=self.user, date=NOW, hours=0, minutes=19,
                seconds=1, distance=7)
        Run1.save()
        Run2 = Run(user=self.user, date=NOW - timedelta(days=7),
                hours=0, minutes=19, seconds=1, distance=11)
        Run2.save()
        Run3 = Run(user=self.user, date=NOW - timedelta(days=14),
                hours=0, minutes=19, seconds=1, distance=23)
        Run3.save()
        Run4 = Run(user=self.user, date=NOW - timedelta(days=21),
                hours=0, minutes=19, seconds=1, distance=1)
        Run4.save()
        Run5 = Run(user=self.user, date=NOW - timedelta(days=28),
                hours=0, minutes=19, seconds=21, distance=18)
        Run5.save()
        Run6 = Run(user=self.user, date=NOW - timedelta(days=42),
                hours=0, minutes=19, seconds=38, distance=6)
        Run6.save()
        #Create a run that shouldn't be averaged.
        Run7 = Run(user=self.user, date=NOW - timedelta(days=43),
                hours=0, minutes=19, seconds=49, distance=400)
        Run7.save()
        self.c.login(username='user', password='pass')
        response = self.c.get('/dashboard/')
        self.assertEquals(response.context['six_week_avg'], 11)

    def test_delete_works_if_authorized(self):
        """Make sure the delete view returns 200 status code."""
        aRun = Run(user=self.user, date="2011-7-22", hours=0, minutes=19,
                seconds=59, distance=4)
        aRun.save()
        self.c.login(username='user', password='pass')
        status = self.c.post('/delete/1').status_code
        self.assertEquals(status, 302)
        self.assertEquals(0, Run.objects.count())

    def test_delete_fails_if_unauthorized(self):
        """If you don't own a run you should not be able to delete it."""
        self.user2 = User.objects.create_user("user2", password="pass")
        aRun = Run(user=self.user2, date="2011-7-22", hours=0, minutes=19,
                seconds=59, distance=4)
        aRun.save()
        self.c.login(username='user', password='pass')
        status = self.c.post('/delete/' + str(aRun.id)).status_code
        self.assertEquals(status, 302)
        self.assertEquals(1, Run.objects.count())

    def test_delete_invalid_id_404s(self):
        """If we try to delete an invalid ID, we should fail and 404."""
        self.c.login(username='user', password='pass')
        status = self.c.post('/delete/1000000').status_code
        self.assertEquals(status, 404)

    def test_get_add_view_if_authenticated(self):
        """Add view should return 200 if authenticated."""
        self.c.login(username='user', password='pass')
        status = self.c.get('/add/').status_code
        self.assertEquals(status, 200)

    def test_get_add_view_if_unauthenticated(self):
        """Add view should return redirect if unauthenticated."""
        status = self.c.get('/add/').status_code
        self.assertEquals(status, 302)

    def test_add_a_new_run(self):
        """Add a new run through the view."""
        self.c.login(username='user', password='pass')
        self.c.post('/add/', {'user': self.user, 'date': '2011-7-22',
            'hours': 0, 'minutes': 19, 'seconds': 59, 'distance': 4})
        self.assertEquals(Run.objects.count(), 1)

    def test_unvalid_add_returns_errors(self):
        self.c.login(username='user', password='pass')
        response = self.c.post('/add/', {'user': self.user,
            'date': '2011-7-22', 'hours': 0, 'minutes': 19, 'distance': 4})
        self.assertEquals(Run.objects.count(), 0)
        #The second field should be listed as a key in the form errors dict
        #becuase the second's field was missing from the post request.
        self.assertTrue('seconds' in response.context['form'].errors.keys())

    def tearDown(self):
        """Destroy any created db objects."""
        User.objects.all().delete()
        Run.objects.all().delete()
        UserProfile.objects.all().delete()
        self.c.logout()
