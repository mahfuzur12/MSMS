import json
from django.contrib.auth.hashers import make_password
from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from faker import Faker

from msms.managers import UserManager


class School(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return f"({self.pk}) {self.name}"
    

class User(AbstractUser):

    URN = models.AutoField(primary_key=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=False)  
    
    objects = UserManager()
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"({self.pk}){self.email}"
    
    def str__2(self, prefix=""):
        return f"{prefix}{self.first_name} {self.last_name}"
    

DEF_AVAILABILITY = [True for _ in range(7)]

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.CharField(max_length=70, default=json.dumps(DEF_AVAILABILITY))
    balance = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    
    def create(**kwargs):
        return UserMaker.create(Student, is_student=True, **kwargs)
    
    def __str__(self):
        return self.user.str__2("Stud. ")
    
    
    def get_availability(self):
        return json.loads(self.availability)
    
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.CharField(max_length=70, default=json.dumps(DEF_AVAILABILITY))
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    
    def create(**kwargs):
        return UserMaker.create(Teacher, is_teacher=True, **kwargs)
    
    def __str__(self):
        school = ""
        if self.school:
            school = f"({self.school.name})"
        return f"{self.user.str__2()} {school}"
    
    def get_availability(self):
        return json.loads(self.availability)
    
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    
    def create(**kwargs):
        return UserMaker.create(Admin, is_admin=True, **kwargs)
    
    def __str__(self):
        return self.user.str__2("Admin. ")
    

faker = Faker()
class UserMaker():
    def create(cls, first_name, last_name, password, email, username=None, is_admin=False, is_student=False, is_teacher=False, **kwargs):
        if not username:
            username = email
            while User.objects.filter(username=username).exists():
                username = faker.user_name()
                
        user = User(username=username, first_name=first_name, last_name=last_name, password=make_password(password), email=email, 
                    is_student=is_student, is_admin=is_admin, is_teacher=is_teacher)
        user.full_clean()
        user.save()
        return cls(user=user, **kwargs)

