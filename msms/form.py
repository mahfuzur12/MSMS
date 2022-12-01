from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import transaction
from .models import Student, Teacher, Admin, User

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(max_length=40)
    availability = forms.CharField(max_length=10, required=True)
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return self.cleaned_data['email']
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user:User = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user)
        student.availability = self.cleaned_data.get('availability')
        return student
    
class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(max_length=40)
    availability = forms.CharField(max_length=10, required=True)
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return self.cleaned_data['email']
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user:User = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.availability = self.cleaned_data.get('availability')
        return teacher
    
class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(max_length=40)
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return self.cleaned_data['email']
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user:User = super().save(commit=False)
        user.is_admin = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        admin = Admin.objects.create(user=user)
        return admin