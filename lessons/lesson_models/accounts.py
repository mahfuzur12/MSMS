from django.db import models
from django.contrib.auth.hashers import make_password


ROLE_CHOICES = [("student", "student"),
                ("teacher", "teacher"),
                ("admin","admin"),
                ("superadmin","superadmin"),
                ("director","director"),
                ("siteadmin","siteadmin")]


# Create your models here.
class User(models.Model):
    URN = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=40, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")


class UserMaker():
    def create(cls, first_name, last_name, password, email, role, **kwargs):
        user = User(first_name=first_name, last_name=last_name, password=make_password(password), email=email, role=role)
        user.full_clean()
        user.save()
        return cls(user=user, **kwargs)


class School(models.Model):
    schoolID = models.AutoField(primary_key=True, default=1)
    name = models.CharField(max_length=20)
    

class Admin(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    
    def create(**kwargs):
        return UserMaker.create(Admin, **kwargs)
    
    
class Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    availability = models.CharField(max_length=10, default="NA")
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    
    def create(**kwargs):
        return UserMaker.create(Teacher, role="teacher", **kwargs)
    
    
class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    availability = models.CharField(max_length=10, default="NA")
    balance = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    
    def create(**kwargs):
        return UserMaker.create(Student, role="student", **kwargs)
    
    