'''A command for unseeding the database'''
from django.core.management.base import BaseCommand
from lessons.models import Transfer
from msms.models import User, School


class Command(BaseCommand):
    '''A class responsible for removing all records except admin accounts from the database'''
    
    def handle(self, *args, **options):
        '''Removes every record except admin accounts from the database''' 
          
        print("Unseeding")
        # due to referential integrity lessons and invoices implicitly removed
        User.objects.exclude(is_staff=True).delete()
                            
        School.objects.all().delete()
        Transfer.objects.all().delete()
        print("Finished")