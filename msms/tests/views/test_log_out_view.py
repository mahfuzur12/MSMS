from django.test import TestCase
from django.urls import reverse
from msms.models import User
from helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):
    
    def setUp(self):
        self.url = reverse('logout')
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
        
    def test_log_out_url(self):
        self.assertEqual(self.url, '/logout/')
        
    def test_get_log_out(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())