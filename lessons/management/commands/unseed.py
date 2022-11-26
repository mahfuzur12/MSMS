'''A command for unseeding the database'''
from django.core.management.base import BaseCommand
from lessons.lesson_models.accounts import *


class Command(BaseCommand):
    '''A class responsible for removing all records except non admin accounts from the database'''
    def handle(self, *args, **options):
        print("Unseeding")
        User.objects.exclude(role="admin"
                            ).exclude(role="superadmin"
                            ).exclude(role="director").delete()
                            
        School.objects.all().delete()
        print("Finished")