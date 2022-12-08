from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from numpy import isin
from msms.form import StudentSignUpForm
from msms.models import Student, User
from helpers import LogInTester

class StudentSignUpViewTestCase(TestCase, LogInTester):
    
    def setUp(self):
        self.url = reverse('student_sign_up')
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password1': 'signupform123',
            'password2': 'signupform123'
        }
    
    def test_student_sign_up_url(self):
        self.assertEqual(self.url, '/student_sign_up/')
        
    def test_get_student_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_sign_up.html')
        form = response.content['form']
        self.assertTrue(isinstance(form, StudentSignUpForm))
        self.assertFalse(form.is_bound)
        
    def test_unsuccessful_student_sign_up(self):
        self.form_input['first_name'] = 'BAD_NAME'
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_sign_up.html')
        form = response.content['form']
        self.assertTrue(isinstance(form, StudentSignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
        
    def test_successful_student_sign_up(self):
        before_count = Student.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Student.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        user = User.objects.get(first_name='Jane')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        is_password_correct = check_password('signupform123', user.password1)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())