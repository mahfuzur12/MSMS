from django.contrib import admin
from .models import User, Teacher, Student, Admin

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
