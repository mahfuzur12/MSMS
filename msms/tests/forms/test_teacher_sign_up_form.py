from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from msms.form import TeacherSignUpForm
from msms.models import Teacher


class TeacherSignUpFormTestCase(TestCase):
    
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password1': 'signupform123',
            'password2': 'signupform123'
        }
        
    def test_valid_teacher_sign_up_form(self):
        form = TeacherSignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_teacher_sign_up_form(self):
        response = self.client.post(reverse('teacher_sign_up'), data={
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password2
        })
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)