'''A command for seeding the database'''
from django.core.management.base import BaseCommand, CommandError
from django.forms import ValidationError
from django.db.models import Model
from faker import Faker

from lessons.lesson_models.accounts import *


class Command(BaseCommand):
    '''A class responsible for seeding the database'''
    
    def __init__(self):
        self.faker = Faker("en_GB")
        
        
    def handle(self, *args, **options):
        print("Seeding")    
        self.add_default_members()
            
            
    def save_object(self, object:Model):
        try:
            object.full_clean()
            object.save()
            print("Saved object")
        except ValidationError:
            print("Error in saving object.")
    
    
    def add_default_members(self):
        if 0 == School.objects.filter(name="Default School").__len__():
            school = School(name="Default School")
            self.save_object(school)
        else:
            print("Using existing school")
            school = School.objects.filter(name="Default School").first()
        
        try:
            student = Student.create(first_name="John", last_name="Doe", password="Password123", email="john.doe@example.org")
            self.save_object(student)
        except ValidationError as e:
            print(e.messages)
        
        try: 
            admin = Admin.create(first_name="Petra", last_name="Pickles", password="Password123", email="petra.pickles@example.org", role="admin", school=school)
            self.save_object(admin)
        except ValidationError as e:
            user = User.objects.get(email="petra.pickles@example.org")
            admin = Admin.objects.get(user=user)
            admin.school = school
            self.save_object(admin)
            print("updated school for default admin")
        
        try:
            director = Admin.create(first_name="Marty", last_name="Major", password="Password123", email="marty.major@example.org", role="director", school=school)
            self.save_object(director)
        except ValidationError as e:
            user = User.objects.get(email="marty.major@example.org")
            admin = Admin.objects.get(user=user)
            admin.school = school
            self.save_object(admin)
            print("updated school for default director")