from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client

from apps.runlog.models import Run

class ModelTest(TestCase):
    """Class for testing models in the runlog app."""

    def setUp(self):
        """Create a test user before running tests."""
        self.user = User.objects.create_user("user")

    def test_run_minutes_errors_if_invalid(self):
        """Test that we raise a ValidationError if minutes greater than 60."""
        aRun = Run(user = self.user, date = "2011-7-21", hours = 0, minutes = 61, seconds = 17, distance = 4)
        self.assertRaises(ValidationError, aRun.save())

    def test_run_seconds_errors_if_invalid(self):
        """"Test that seconds less than 60."""
        aRun = Run(user = self.user, date = "2011-7-22", hours = 0, minutes = 19, seconds = 61, distance = 4)
        self.assertRaises(ValidationError, aRun.save())

    def tearDown(self):
        """Destroy any created db objects."""
        User.objects.all().delete()
        Run.objects.all().delete()

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

    def test_delete_works_if_authorized(self):
        """Make sure the delete view returns 200 status code."""
        aRun = Run(user = self.user, date = "2011-7-22", hours = 0, minutes =
                19, seconds = 59, distance = 4)
        aRun.save()
        self.c.login(username='user', password='pass')
        status = self.c.post('/delete/1').status_code
        self.assertEquals(status, 302)
        self.assertEquals(0, Run.objects.count())

    def test_delete_fails_if_unauthorized(self):
        """If you don't own a run you should not be able to delete it."""
        self.user2 = User.objects.create_user("user2", password="pass")
        aRun = Run(user = self.user2, date = "2011-7-22", hours = 0, minutes =
                19, seconds = 59, distance = 4)
        aRun.save()
        self.c.login(username='user', password='pass')
        status = self.c.post('/delete/' + str(aRun.id)).status_code
        self.assertEquals(status, 302)
        self.assertEquals(1, Run.objects.count())

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
        self.c.post('/add/', {'user': self.user, 'date' : '2011-7-22', 'hours' :
            0, 'minutes': 19, 'seconds': 59, 'distance':4})
        self.assertEquals(1, Run.objects.count())

    def tearDown(self):
        """Destroy any created db objects."""
        User.objects.all().delete()
        Run.objects.all().delete()
        self.c.logout()
