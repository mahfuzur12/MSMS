from django.shortcuts import render
from django.views.generic import CreateView
from msms.form import StudentSignUpForm, TeacherSignUpForm, AdminSignUpForm

from msms.models import User, Student, Teacher, Admin

def home(request):
    return render(request, 'home.html')

class student_sign_up(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student_sign_up.html'

