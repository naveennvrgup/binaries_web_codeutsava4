from transaction.models import *
from user.models import *
from django.core.management.base import BaseCommand, CommandError
from random import random
import math

class Command(BaseCommand):
    help = 'Creates the dummy data for the project'

    def handle(self, *args, **options):
        users = [
            ['rushi', ,]
        ]
        
        for  x in users:
            User.objects.create_user(
                
            )        