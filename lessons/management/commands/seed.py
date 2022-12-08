'''A command for seeding the database'''
from django.core.management.base import BaseCommand
from django.forms import ValidationError
from django.db.models import Model
from faker import Faker
from datetime import timedelta

from lessons.models import *
from msms.models import *


def exists(model:type[Model], **kwargs):
    '''Returns first record matching query if at least one exists.
    Else returns None'''
    
    result = model.objects.filter(**kwargs)
    if result.exists():
        return result.first()
    
    return None
    

class Command(BaseCommand):
    '''A class responsible for seeding the database'''
    
    def __init__(self):
        BaseCommand.__init__(self)
        self.faker = Faker("en_GB")
        
        
    def handle(self, *args, **options):
        '''Adds all default users and some random ones'''
        
        print("Seeding")    
        self.add_default_members()
        
        # fill_database adds 4 students so 25 loops required to reach the requested 100
        for fill_num in range(25):
            print(f"Fill {fill_num + 1}/25")
            self.fill_database()
        print("Finished Seeding")
        
    
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
        
        try:
            object.full_clean()
            object.save()
            print(f"Saved object {object}")
            return object
        except ValidationError as e:
            print(e.messages)
            return None
           
            
    def persistently_save_user(self, model:type[Model], level=10, **kwargs,):
        '''Will attempt to save a user with random details, accepts kwargs such as school.
        Stops attempting to save if saving fails 10 times, likely there is another issue.'''
        
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
        '''Adds the users required by the Assignment, a school and also a teacher account
        includes Default School, John Doe (St), Bob Benson (T),  Petra Pickles (A),
        and Marty Major (SA)'''
        
        school = exists(School, name="Default School")
        if not school:
            school = School(name="Default School")
            self.save_object(school)
        else:
            print("Using existing school")
        
        #check if student account already exists
        if exists(User, email="john.doe@example.org"):
            print("default student already exists")
        else:
            # new student created
            student = Student.create(first_name="John", last_name="Doe", password="Password123", email="john.doe@example.org")
            self.save_object(student)
            
        #check if teacher account already exists
        user = exists(User, email="benson@benson.com")
        if user:
            print("Updating school for default teacher")
            user.teacher.school = school
            self.save_object(user.teacher)
        else:
            # new teacher created
            teacher = Teacher.create(first_name="Bob", last_name="Benson", password="abcdefghijk123", email="benson@benson.com", school=school)
            self.save_object(teacher)
        
        # check if admin account already exists
        user = exists(User, email="petra.pickles@example.org")
        if user:
            print("Updating school for default admin")
            admin = exists(Admin, user=user)
            admin.school = school
            self.save_object(admin) 
        else:
            # new admin created
            admin = Admin.create(first_name="Petra", last_name="Pickles", password="Password123", email="petra.pickles@example.org", school=school)
            self.save_object(admin)
        
        
        # check if admin account already exists
        user = exists(User, email="marty.major@example.org")
        if user:
            print("Updating school for default director")
            admin = exists(Admin, user=user)
            admin.school = school
            self.save_object(admin)
        else:
            # new admin created
            director = Admin.create(first_name="Marty", last_name="Major", password="Password123", email="marty.major@example.org", school=school)
            self.save_object(director)
    
             
    def fill_database(self):
        '''Adds to the database a random school and some random users including 4 students and 4 teachers
        Also creates 6 lessons, 4 of which are booked, 2 of which has a transfer associated
        with it'''
        
        school = exists(School, name="Default School")
        name = f"{faker.word()} School".capitalize()
        while exists(School, name=name):
            name = f"{faker.word()} School".capitalize()
        school = School(name=name)
        school.save()
        
        # add an admin to the school
        admin = self.persistently_save_user(Admin, school=school)        

        # make a teacher and student, make a lesson request with both of them. Save all to database
        teacher = self.persistently_save_user(Teacher, school=school)
        student = self.persistently_save_user(Student)
        lesson = Lesson(num_lessons=3, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        
        # make a another student, make a lesson request with student and previous teacher. Save all to database
        # then turn the lesson request into a booking
        student = self.persistently_save_user(Student)
        lesson = Lesson(num_lessons=4, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        lesson.make_booking()
        
        # make a another teacher, make a lesson request with teacher and previous student. Save all to database
        # then turn the lesson request into a booking, and get the invoice
        teacher = self.persistently_save_user(Teacher, school=school)
        lesson = Lesson(num_lessons=5, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        invoice:Invoice = lesson.make_booking()
        
        # make a transfer based on the invoice
        transfer = Transfer.create_from_invoice(invoice)
        self.save_object(transfer)
        
        
        # make a teacher and student, make a lesson request with both of them. Save all to database
        teacher = self.persistently_save_user(Teacher, school=school)
        student = self.persistently_save_user(Student)
        lesson = Lesson(num_lessons=3, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        
        # make a another student, make a lesson request with student and previous teacher. Save all to database
        # then turn the lesson request into a booking
        student = self.persistently_save_user(Student)
        lesson = Lesson(num_lessons=4, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        lesson.make_booking()
        
        # make a another teacher, make a lesson request with teacher and previous student. Save all to database
        # then turn the lesson request into a booking, and get the invoice
        teacher = self.persistently_save_user(Teacher, school=school)
        lesson = Lesson(num_lessons=5, interval=1, student=student, teacher=teacher, duration=timedelta(minutes=30))
        self.save_object(lesson)
        invoice = lesson.make_booking()
        
        # make a transfer based on the invoice
        transfer = Transfer.create_from_invoice(invoice)
        self.save_object(transfer)