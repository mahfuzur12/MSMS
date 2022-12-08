from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from msms.models import User
from helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):
    
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(
            is_student = True,
            is_teacher = False,
            is_admin = False,
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.org',
            password1 = 'Password123',
            password2 = 'Password123',
            is_active = True,
        )
    
    def test_log_in_url(self):
        self.assertEqual(self.url, '/login/')
        
    def test_get_log_in(self):
        form = AuthenticationForm()
        self.assertTrue(isinstance(form, AuthenticationForm()))
        self.assertFalse(form.is_bound)
        
    def test_unsuccessful_log_in(self):
        form_input = {'email': 'johndoe@example.org', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AuthenticationForm()))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        
    def test_successful_log_in(self):
        form_input = {'email': 'johndoe@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        
    def test_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'email': 'johndoe@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AuthenticationForm()))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())