from datetime import timedelta
from django.forms import ValidationError
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.db.models import Model
from faker import Faker
from lessons.models import Lesson
from django.utils import timezone

from msms.models import Admin, School, Student, Teacher, User


class ViewTestCase(TestCase):
    '''A test case base class used to test pages are being visited and loaded properly
    This class should be subclassed to define url_name, expected_url, and expected_template file'''
    
    url_name = ""
    expected_url = ""
    expected_template = ""
    
    def setUp(self):
        self.url = reverse(self.url_name)
        self.user:User = User.objects.create(email="bob@bob.com")
        self.user.set_password("forkedeggs30")
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username="bob@bob.com", password="forkedeggs30")
        self.studentify()

    def userify(self):
        '''turns user into basic user'''
        self.user.is_superuser,
        self.user.is_teacher,
        self.user.is_admin,
        self.user.is_student = False
        
    def studentify(self):
        self.userify()
        self.user.is_student = True
        self.user.save()
        
    def teacherify(self):
        self.userify()
        self.user.is_teacher = True
        self.user.save()
        
    def adminify(self):
        self.userify()
        self.user.is_admin = True
        self.user.save()
    
    def superuserify(self):
        self.userify()
        self.user.is_superuser = True
        self.user.save()   
        
    
    def test_url(self):
        self.assertEqual(self.url, self.expected_url)
        
        
    def test_get_page(self):
        response = self.client.get(self.url)
        self.check_response(response)
        
        
    def check_response(self, response:HttpResponse):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expected_template)


class FormViewTestCase(TestCase):
    '''A test case base class used to test pages are being visited and loaded properly,
    and that the forms on these pages work properly
    This class should be subclassed to define: 
    expected_form_class, url_name, expected_url, response_url_name,
    expected_template file, model[optional] and form_input'''
    
    url_name = ""
    expected_url = ""
    success_url_name = ""
    fail_url_name = ""
    expected_template = ""
    next_template = ""
    model:type[Model] = None
    form_input = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker("en_GB")
    
    def setUp(self):
        self.url = reverse(self.url_name)
        self.user:User = User.objects.create(email="bob@bob.com")
        self.user.set_password("forkedeggs30")
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username="bob@bob.com", password="forkedeggs30")

    def userify(self):
        '''turns user into basic user'''
        self.user.is_superuser,
        self.user.is_teacher,
        self.user.is_admin,
        self.user.is_student = False
        if Student.objects.filter(user=self.user).exists():
            self.user.student.delete()
        
        if Teacher.objects.filter(user=self.user).exists():
            self.user.teacher.delete()
        
        if Admin.objects.filter(user=self.user).exists():
            self.user.admin.delete()
        
    def studentify(self):
        self.userify()
        self.user.is_student = True
        self.user.save()
        Student(user=self.user).save()
        
    def teacherify(self):
        self.userify()
        self.user.is_teacher = True
        self.user.save()
        school = School("bob")
        Teacher(user=self.user, school=school).save()
        
    def adminify(self):
        self.userify()
        self.user.is_admin = True
        self.user.save()
        school = School("bob")
        Admin(user=self.user, school=school).save()
    
    def superuserify(self):
        self.userify()
        self.user.is_superuser = True
        self.user.save()
        
    
    def random_user(self):
        '''Creates a dictionary of random user details'''
        
        email = self.faker.email()
        # username field is required, 
        # just make it the same as email
        return {
                "username":email,
                "first_name":self.faker.first_name(),
                "last_name":self.faker.last_name(),
                "password":self.faker.word(),
                "email":email
                }
            
            
    def save_object(self, object:Model):
        '''Tries to save an object. Prints 'Saved object' and returns object if successful.
        Else returns none and prints error meesage'''
        
        object.full_clean()
        object.save()
        return object
           
            
    def save_random_user(self, model:type[Model], level=10, **kwargs):
        '''Will attempt to save a user with random details, accepts kwargs such as school.
        Since there is a small chance details are not unique (very unlikely), we will try to save multiple times
        Stops attempting to save if saving fails 10 times, likely there is another issue.'''
        
        if level <= 0:
            print("Couldn't save user")
            # don't try this forever, very unlikely it will need more than 10 tries
            return None
        
        try:
            # can fail if email already exists
            return self.save_object(model.create(**self.random_user(), **kwargs))
        except ValidationError as e:
            # try to save again with new details
            print(e.message)
            return self.save_random_user(model, level=level-1, **kwargs)
          
    
    def test_url(self):
        self.assertEqual(self.url, self.expected_url)
        
        
    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        
    def check_response(self, response:HttpResponse):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expected_template)
        return response
    
        
    def check_unsuccessful_form_submit(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.check_response(response) 
        
          
    def check_successful_form_submit(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.check_response(response)
        
        

class AvailabilityViewTestCase(FormViewTestCase):
    url_name = "availability"
    expected_url = "/lesson/availability/"
    success_url_name = "availability"
    fail_url_name = "availability"
    expected_template = "availability.html"
    next_template = "availability.html"
    
    def setUp(self):
        super().setUp()
        self.studentify()
        self.form_input = {
            'monday': True,
            'tuesday': True,
            'wednesday': True,
            'thursday': True,
            'friday': True,
            'saturday': True,
            'sunday': True,
        }
        
        
    def test_successful_submit(self):
        self.check_successful_form_submit()


class OptionsViewTestCase(ViewTestCase):
    url_name = "lesson_options"
    expected_url = "/lesson/options/"
    expected_template = "lessonoptions.html"


class RequestStudentTestCase(FormViewTestCase):
    url_name = "student_request_lesson"
    expected_url = "/lesson/request/student/"
    success_url_name = "view_lessons"
    expected_template = "requestlesson.html"
    next_template = "viewlessons.html"
    
    
    def setUp(self):
        super().setUp()
        school = School(name="bob")
        school.save()
        self.form_input = {
            'num_lessons': 3,
            'interval': 2,
            'teacher':self.save_random_user(Teacher,school=school),
            'duration': timedelta(minutes=30),
            'first_lesson_date': timezone.now()
        }
        
    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
     
    def test_successful_submit(self):
        self.check_successful_form_submit()

        
    