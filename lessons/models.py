from datetime import timedelta

from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from msms.models import Student, Teacher
 
    
COST_PER_LESSON = 20
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def current_day():
    '''A function which converts the current day of the week index into a word'''
    return DAYS[timezone.now().weekday()]

class Lesson(models.Model):
    '''A model which represents a group of lessons.
    They are assumed to be one a week, on the same day and same duration'''
    
    # choices from 1-10
    num_lessons = models.IntegerField(choices=[(num, num) for num in range(1, 11)], default=1)
    interval = models.IntegerField(choices=[(1, 1),(2, 2)], default=1)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    # choices from 30mins, 45mins, 1hr
    duration = models.DurationField(choices=[(timedelta(minutes=mins), timedelta(minutes=mins)) for mins in [30, 45, 60]], default=30)
    state = models.CharField(max_length=20, choices=[("R","request"),("B","booking"),("C","cancelled")], default="R")
    first_lesson_date = models.DateField(default=timezone.now)
    day = models.CharField(max_length=10, choices=[(day, day) for day in DAYS], default=current_day)
      
    def make_booking(self):
        '''Converts this lesson into a booking. Creates a corresponding invoice too'''
        if self.state == "B":
            return
                
        
        self.state = "B"
        invoice = Invoice.create(
            amount=COST_PER_LESSON * self.num_lessons,
            student=self.student,
            lesson=self)
        try:
            self.save()
            invoice.save()
            return invoice
        except ValidationError as e:
            print(e.messages)
            self.state = "R"
            self.save()
            return None

    def save_booking(self, num_of_lessons):
        if self.state == "B":
            # If the lesson is already booked, then it must be edited
            # So the amount in the invoice will change depending on the lesson edit
            invoice = Invoice.objects.get(lesson=self)
            invoice.amount = COST_PER_LESSON * num_of_lessons
            try:
                self.save()
                invoice.save()
                return invoice
            except ValidationError as e:
                print(e.messages)
                self.save()
                return None
    
    
    def cancel(self):
        '''Cancels this lesson, removing a related invoice if applicable'''
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
    '''A model which represents the invoice of a lesson. 
    This details how much is remaining to be paid, the invoice number.
    There is also a method to get the unique reference number'''
    
    # total amount to be paid
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    number = models.CharField(max_length=60)
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)   
    
    def create(student, **kwargs):
        '''Creates an invoice automatically generating the correct invoice number'''
        
        # get the next available invoice number
        number = f"{student.user.pk}-{Invoice.objects.filter(student=student).__len__() + 1}"
        return Invoice(student=student, number=number,**kwargs)
    
    
    def __str__(self):
        return f"Invoice {self.ref()}"
    
    
    def ref(self):
        '''Unique invoice reference number'''
        return f"{self.student.user.pk}-{self.number}"


class Transfer(models.Model):
    '''Represents a bank transfer:
    Includes reference number which should be in the form (stud.id-inv.num)'''

    # Each transfer is related to a student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reference = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    date_transferred = models.DateField(default=timezone.now)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, null = True) 

    def create(student, **kwargs):
        '''Creates an invoice automatically generating the correct invoice number'''
        
        # get the next available invoice number
        number = f"{student.user.pk}-{Invoice.objects.filter(student=student).__len__() + 1}"
        return Invoice(student=student, number=number,**kwargs)