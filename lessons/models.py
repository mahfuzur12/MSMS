from datetime import timedelta

from django.db import models
from django.utils import timezone

from msms.models import Student, Teacher
from lessons.schoolmodel import School

    
class Transfer(models.Model):
    reference = models.CharField(max_length=30)
    state = models.CharField(max_length=20, choices=[("I","incoming"),("P","processed")], default="I")
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    date_transferred = models.DateField(default=timezone.now)
    
    
COST_PER_LESSON = 20
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def num_to_day():
    return DAYS[timezone.now().weekday()]

class Lesson(models.Model):
    '''A model which represents a group of lessons.
    They are assumed to be one a week'''
    
    # choices from 1-10
    num_lessons = models.IntegerField(choices=[(num, num) for num in range(1, 11)], default=1)
    interval = models.IntegerField(choices=[(1, 1),(2, 2)], default=1)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    # choices from 30mins, 45mins, 1hr
    duration = models.DurationField(choices=[(timedelta(minutes=mins), timedelta(minutes=mins)) for mins in [30, 45, 60]], default=30)
    state = models.CharField(max_length=20, choices=[("R","request"),("B","booking"),("C","cancelled")], default="R")
    first_lesson_date = models.DateField(default=timezone.now)
    day = models.CharField(max_length=10, choices=[(day, day) for day in DAYS], default=num_to_day)
      
    def make_booking(self):
        if self.state == "B":
            return
        
        self.state = "B"
        invoice = Invoice.create(
            amount=COST_PER_LESSON,
            remaining_cost=COST_PER_LESSON * self.num_lessons,
            student=self.student,
            lesson=self)
        try:
            self.save()
            invoice.save()
            return invoice
        except:
            self.state = "R"
            self.save()
            return None
    
    
    def cancel(self):
        if self.state == "C":
            return
        
        invoice = Invoice.objects.filter(lesson=self)
        if invoice.exists():
            invoice.delete()
        
        self.state = "C"
        self.save()
    
    
    def __str__(self):
        return f"Lesson({self.pk}) {self.student} - {self.teacher}"
    
    
class Invoice(models.Model):   
    # amount per lesson
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    remaining_cost = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    number = models.IntegerField()
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)   
    
    def create(student, **kwargs):
        # get the next available invoice number
        number = Invoice.objects.filter(student=student).__len__() + 1
        return Invoice(student=student, number=number,**kwargs)
    
    
    def __str__(self):
        return f"Invoice {self.ref()}"
    
    
    def ref(self):
        return f"{self.student.user.pk}-{self.number}"