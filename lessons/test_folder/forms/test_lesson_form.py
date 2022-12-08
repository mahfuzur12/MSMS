from datetime import timedelta

from django.db.models import Model
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from faker import Faker

from lessons.forms import *
from msms.models import *


class LessonFormTC(TestCase):
    form_class = LessonForm
    
    def __init__(self, *args, **kwargs):
        self.faker = Faker("en_GB")
        super().__init__(*args, **kwargs)
    
    
    def setUp(self):
        self.form_input = {
            'num_lessons': 3,
            'interval': 2,
            'duration': timedelta(minutes=30),
            'first_lesson_date': timezone.now()
        }
        
      
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
            return self.save_random_user(model, level=level-1, **kwargs)
    
    
    def form_valid(self):
        form = self.form_class(data=self.form_input)
        self.assertTrue(form.is_valid())
      
        
    def form_invalid(self):
        form = self.form_class(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    
    def test_valid_lesson_details(self):
        self.form_valid()
       
        
    def test_invalid_num_lessons_details(self):
        self.form_input['num_lessons'] = "e"
        self.form_invalid()
    
    
    def test_invalid_interval_details(self):
        self.form_input['interval'] = 0
        self.form_invalid()


    def test_invalid_duration_details(self):
        self.form_input['duration'] = timedelta(microseconds=20)
        self.form_invalid()
    
    
    def test_invalid_lesson_date_details(self):
        self.form_input['first_lesson_date'] = "25"
        self.form_invalid()


class LessonStudentFormTestCase(LessonFormTC):
    form_class = LessonStudentForm
    
    def setUp(self):
        super().setUp()
        school = School(name="School")
        school.save()
        user = self.save_random_user(Teacher, school=school)
        self.form_input['teacher'] = user
    
    
    def test_invalid_teacher(self):
        user = self.save_random_user(Student)
        self.form_input['teacher'] = user
        self.form_invalid()
 

class LessonTeacherFormTestCase(LessonFormTC):
    form_class = LessonTeacherForm
    
    def setUp(self):
        super().setUp()
        user = self.save_random_user(Student)
        self.form_input['student'] = user
    
    
    def test_invalid_student(self):
        school = School(name="School")
        school.save()
        user = self.save_random_user(Teacher, school=school)
        self.form_input['student'] = user
        self.form_invalid()
        

class LessonAdminFormTestCase(LessonFormTC):
    form_class = LessonAdminForm
    
    def setUp(self):
        super().setUp()
        student = self.save_random_user(Student)
        self.form_input['student'] = student
        
        school = School(name="School")
        school.save()
        teacher = self.save_random_user(Teacher, school=school)
        self.form_input['teacher'] = teacher
        
        
    def test_invalid_student(self):
        school = School(name="School")
        school.save()
        user = self.save_random_user(Teacher, school=school)
        self.form_input['student'] = user
        self.form_invalid()
       
        
    def test_invalid_teacher(self):
        user = self.save_random_user(Student)
        self.form_input['teacher'] = user
        self.form_invalid()
