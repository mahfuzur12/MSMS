from django.http import request
from django.shortcuts import render
from django.views.generic import CreateView
from msms.form import StudentSignUpForm, TeacherSignUpForm, AdminSignUpForm

from msms.models import User, Student, Teacher, Admin

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

class student_sign_up(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student_sign_up.html'
    
class teacher_sign_up(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'teacher_sign_up.html'
    
class admin_sign_up(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'admin_sign_up.html'

