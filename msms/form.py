from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from django.db import transaction
from .models import Student, Teacher, Admin, User

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
    email = forms.EmailField(max_length=40)
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def data_save(self):
        user_password = self.cleaned_data.get('new_password')
        user_password_confirmation = self.cleaned_data.get('password_confirmation')
        if user_password != user_password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')
            
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.password = self.cleaned_data.get('new_password')
        user.save()
        student = Student.objects.create(user=user)
        student.availability = self.cleaned_data.get('availability')
        student.balance = self.cleaned_data.get('balance')
        return student
    
class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
    email = forms.EmailField(max_length=40)
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def data_save(self):
        user_password = self.cleaned_data.get('new_password')
        user_password_confirmation = self.cleaned_data.get('password_confirmation')
        if user_password != user_password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')
            
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.password = self.cleaned_data.get('new_password')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.availability = self.cleaned_data.get('availability')
        return teacher
    
class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
    email = forms.EmailField(max_length=40)
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def data_save(self):
        user_password = self.cleaned_data.get('new_password')
        user_password_confirmation = self.cleaned_data.get('password_confirmation')
        if user_password != user_password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')
            
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.password = self.cleaned_data.get('new_password')
        user.save()
        admin = Admin.objects.create(user=user)
        return admin