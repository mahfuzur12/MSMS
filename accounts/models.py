from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from accounts.managers import UserManager


ROLE_CHOICES = [("student", "student"),
                ("teacher", "teacher"),
                ("admin","admin"),
                ("superadmin","superadmin"),
                ("director","director"),
                ("siteadmin","siteadmin")]


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return f"({self.pk}){self.email}"
