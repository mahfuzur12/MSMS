from django.test import TestCase

from lessons.forms import *


class AvailabilityTestCase(TestCase):
    form_class = AvailabilityForm
    
    def setUp(self):
        self.form_input = {
            'monday': True,
            'tuesday': True,
            'wednesday': True,
            'thursday': True,
            'friday': True,
            'saturday': True,
            'sunday': True,
        }
    
    
    def test_valid_availability_details(self):
        form = self.form_class(data=self.form_input)
        self.assertTrue(form.is_valid())