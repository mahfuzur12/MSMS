from django.core.exceptions import ValidationError
from django.test import TestCase
from msms.models import User, Student

class StudentModelTestCase(TestCase):
    
    def setUp(self):
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
        student = Student.objects.create(user=self.user)
        
    def test_valid_user(self):
        self._assert_user_is_valid()
        
    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()
        
    def test_first_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()
        
    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()
        
    def test_last_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()
        
    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()
        
    def test_email_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.email = second_user.email
        self._assert_user_is_invalid()
        
    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()
    
    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()
        
    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()
        
    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()
        
    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()
        
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')
            
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
            
    def _create_second_user(self):
        user = User.objects.create_user(
            is_student = True,
            is_teacher = False,
            is_admin = False,
            first_name = 'Jane',
            last_name = 'Doe',
            email = 'janedoe@example.org',
            password1 = 'Password123',
            password2 = 'Password123',
            is_active = True,
        )