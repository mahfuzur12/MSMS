'''A command for seeding the database'''
from django.core.management.base import BaseCommand
from django.forms import ValidationError
from django.db.models import Model
from faker import Faker
from datetime import timedelta

from lessons.models import *
from msms.models import *


def exists(model:type[Model], **kwargs):
        result = model.objects.filter(**kwargs)
        if result.__len__() == 0:
            return None
        return result.first()


class Command(BaseCommand):
    '''A class responsible for seeding the database'''
    
    def __init__(self):
        self.faker = Faker("en_GB")
        
        
    def handle(self, *args, **options):
        print("Seeding")    
        self.add_default_members()
        self.fill_database()
        print("Finished Seeding")
        
    
    def random_user(self):
        return {"first_name":self.faker.first_name(),
                "last_name":self.faker.last_name(),
                "password":self.faker.word(),
                "email":self.faker.email()
                }
            
            
    def save_object(self, object:Model):
        try:
            object.full_clean()
            object.save()
            print(f"Saved object {object}")
            return object
        except ValidationError as e:
            print(e.messages)
            return None
           
            
    def persistently_save_user(self, model:type[Model], level=10, **kwargs,):
        '''Will attempt to save a user with random details, accepts kwargs such as school'''
        if level <= 0:
            print("Couldn't save user")
            # don't try this forever, very unlikely it will need more than 10 tries
            return None
        
        try:
            # can fail if email already exists
            return self.save_object(model.create(**self.random_user(), **kwargs))
        except ValidationError as e:
            print(e.messages)
            # try to save again with new details
            return self.persistently_save_user(model, level=level-1, **kwargs)
    
    
    def add_default_members(self):
        school = exists(School, name="Default School")
        if not school:
            school = School(name="Default School")
            self.save_object(school)
        else:
            print("Using existing school")
        
        
        if exists(User, email="john.doe@example.org"):
            print("default student already exists")
        else:
            student = Student.create(first_name="John", last_name="Doe", password="Password123", email="john.doe@example.org")
            self.save_object(student)
        
        
        user = exists(User, email="petra.pickles@example.org")
        if user:
            print("Updating school for default admin")
            admin = Admin.objects.get(user=user)
            admin.school = school
            self.save_object(admin) 
        else:
            admin = Admin.create(first_name="Petra", last_name="Pickles", password="Password123", email="petra.pickles@example.org", school=school)
            self.save_object(admin)
        
        
        user = exists(User, email="marty.major@example.org")
        if user:
            print("Updating school for default director")
            admin = exists(Admin, user=user)
            admin.school = school
            self.save_object(admin)
        else:
            director = Admin.create(first_name="Marty", last_name="Major", password="Password123", email="marty.major@example.org", school=school)
            self.save_object(director)
    
             
    def fill_database(self):
        school = exists(School, name="Default School")
        if not school:
            school = School(name="Default School")
            self.save_object(school)
              
        teacher = self.persistently_save_user(Teacher, school=school)
        student = self.persistently_save_user(Student)
        lesson = Lesson(num_lessons=3, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        
        student = self.persistently_save_user(Student)
        lesson = Lesson(num_lessons=4, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        lesson.make_booking()
        
        teacher = self.persistently_save_user(Teacher, school=school)
        lesson = Lesson(num_lessons=5, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        invoice = lesson.make_booking()
        
        transfer = Transfer(reference=invoice.ref(), amount=invoice.amount)
        self.save_object(transfer)