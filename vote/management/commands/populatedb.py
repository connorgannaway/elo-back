from django.core.management.base import BaseCommand
from vote.models import Item, College
import os
from vote import constants

os.system('color')
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Command(BaseCommand):
    def populate(self):
        

        try:
            for gender in constants.genders:
                for college in constants.items:
                    print(f"{bcolors.OKCYAN} ({gender}) Creating college {college}...{bcolors.ENDC}", end='')
                    c = College(name=college, gender=gender)
                    c.save()
                    print(f"{bcolors.OKGREEN}Done!{bcolors.ENDC}")
                    for item in constants.items[college]:
                        print(f"{bcolors.ENDC}    -    Creating item {item}...{bcolors.ENDC}", end='')
                        Item.objects.create(name=item, college=c, gender=gender).save()
                        print(f"{bcolors.OKGREEN}Done!{bcolors.ENDC}")
                        
        except Exception as e:
            print(bcolors.FAIL + "\nError populating database: " + bcolors.WARNING + str(e) + bcolors.ENDC)
        else:
            print(f"{bcolors.OKGREEN}Success.{bcolors.ENDC}")

    def handle(self, *args, **options):
        print("Running Item population script... ")
        self.populate()
        