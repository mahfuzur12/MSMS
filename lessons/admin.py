from django.contrib import admin
from lessons.models import *


# Registered models.

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'name']
    
    
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'num_lessons',
                    'student',
                    'teacher',
                    'duration',
                    'state',
                    'first_lesson_date']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'amount',
                    'number',
                    'date',
                    'student',
                    'lesson']
    

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'reference',
                    'state',
                    'amount',
                    'date_transferred']