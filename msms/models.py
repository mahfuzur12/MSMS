from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=40, unique=True)

class School(models.Model):
    schoolID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.CharField(max_length=10, default="NA")
    balance = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    availability = models.CharField(max_length=10, default="NA")
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
