from django.core.management.base import BaseCommand
from vote.models import College, Item

class Command(BaseCommand):

    def update_college_ratings(self):
        colleges = College.objects.all()
        for college in colleges:
            items = Item.objects.filter(college=college)
            rating = 0
            for item in items:
                rating += item.rating
            rating = rating / items.count()
            college.rating = rating
            college.save()
            print(f"Updated college {college.name} ({college.gender}) with rating {college.rating}")

            
    def handle(self, *args, **options):
        self.update_college_ratings()