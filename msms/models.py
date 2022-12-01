from django.contrib.auth.hashers import make_password
from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

from msms.managers import UserManager


class User(AbstractUser):
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
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.CharField(max_length=10, default="NA")
    balance = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    
    def create(**kwargs):
        return UserMaker.create(Student, is_student=True, **kwargs)
    
    def __str__(self):
        return self.user.__str__()
    
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.CharField(max_length=10, default="NA")
    
    def create(**kwargs):
        return UserMaker.create(Teacher, is_teacher=True, **kwargs)
    
    def __str__(self):
        return self.user.__str__()
    
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def create(**kwargs):
        return UserMaker.create(Admin, is_admin=True, **kwargs)
    
    def __str__(self):
        return self.user.__str__()
    
    
class UserMaker():
    def create(cls, first_name, last_name, password, email, is_admin=False, is_student=False, is_teacher=False, **kwargs):
        user = User(first_name=first_name, last_name=last_name, password=make_password(password), email=email, 
                    is_student=is_student, is_admin=is_admin, is_teacher=is_teacher)
        user.full_clean()
        user.save()
        return cls(user=user, **kwargs)
