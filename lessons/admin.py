from django.contrib import admin
from lessons.models import *


# Registered models.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['URN',
                   'first_name',
                   'last_name',
                   'email',
                   'role',
                   'password']
    
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user',
                   'availability',
                   'balance']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['user',
                   'school']
    
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'school',
                   'availability']
    

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['schoolID',
                    'name']