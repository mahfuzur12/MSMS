'''A command for unseeding the database'''
from django.core.management.base import BaseCommand
from lessons.models import School
from msms.models import User


class Command(BaseCommand):
    '''A class responsible for removing all records except non admin accounts from the database'''
    
    def handle(self, *args, **options):
        print("Unseeding")
        User.objects.exclude(is_admin=True).exclude(is_staff=True).delete()
                            
        School.objects.all().delete()
        print("Finished")