from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from msms.form import StudentSignUpForm
from msms.models import Student


class StudentSignUpFormTestCase(TestCase):
    
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password': 'signupform123'
        }
        
    def test_valid_student_sign_up_form(self):
        form = StudentSignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_student_sign_up_form(self):
        response = self.client.post(reverse('student_sign_up'), data={
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)