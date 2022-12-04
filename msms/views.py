from django.http import request
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from msms.form import StudentSignUpForm, TeacherSignUpForm, AdminSignUpForm
from msms.models import User, Student, Teacher, Admin
<<<<<<< HEAD
from django.contrib.auth.forms import AuthenticationForm
=======
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
>>>>>>> parent of dd8a856 (Change password works)
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

class student_sign_up(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student_sign_up.html'
    
    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.INFO, "Successfully signed up!")
        return redirect('home')
    
class teacher_sign_up(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'teacher_sign_up.html'
    
    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.INFO, "Successfully signed up!")
        return redirect('home')
    
class admin_sign_up(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'admin_sign_up.html'
    
    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.INFO, "Successfully signed up!")
        return redirect('home')  
    
def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user:User = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        else:
            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    return render(request, 'login.html', context={'form':AuthenticationForm()})


def feed(request):
    '''A page for school admins'''
    return render(request, 'feed.html')

def logout_view(request):
    logout(request)
<<<<<<< HEAD
    return redirect('home')
=======
    return redirect('home')

def view_profile(request):
    args = {'user': request.user}
    return render(request, 'profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)

>>>>>>> parent of dd8a856 (Change password works)
