from django.test import TestCase
from apps.runlog.models import Run
from django.core.exceptions import ValidationError
from django.test.client import Client

class ModelTest(TestCase):
    def test_run_minutes_errors_if_invalid(self):
        """
        Test that we raise a ValidationError if minutes greater than 60.
        """
        aRun = Run(date = "2011-7-21", hours = 0, minutes = "61", seconds = 17, distance = 4)
        self.assertRaises(ValidationError, aRun.save())

    def test_run_seconds_errors_if_invalid(self):
        """"
        Test that seconds less than 60
        """
        aRun = Run(date = "2011-7-22", hours = 0, minutes = "19", seconds = 61, distance = 4)
        self.assertRaises(ValidationError, aRun.save())

class ViewsTest(TestCase):
    #TODO use reverse()
    def setUp(self):
        self.c = Client()

    def test_index(self):
        """"
        Make sure the index returns 200 status code
        """
        status = self.c.get('/').status_code
        self.assertEquals(status, 200)

    def test_delete(self):
        """
        Make sure the delete view returns 200 status code
        """
        status = self.c.post('/delete/1').status_code
        self.assertEquals(status, 302)

    def test_add(self):
        """
        Make sure the addd view returns 200 status code
        """
        status = self.c.get('/add/').status_code
        self.assertEquals(status, 200)

