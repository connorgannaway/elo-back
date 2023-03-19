from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Genders(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')

class College(models.Model):
    name = models.CharField(max_length=200)
    rating = models.FloatField(default=0)
    gender = models.CharField( 
        max_length=1,
        choices=Genders.choices
        )
    def __str__(self):
        return f"({self.gender}) {self.name}"

class Item(models.Model):
    name = models.CharField(max_length=60)
    votes = models.BigIntegerField(default=0)
    rating = models.FloatField(default=1500)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    gender = models.CharField( 
        max_length=1,
        choices=Genders.choices
        )

    def __str__(self):
        return f"({self.gender}) {self.name}"

class Vote(models.Model):
    item1 = models.ForeignKey(Item, related_name='first_item', on_delete=models.CASCADE)
    item2 = models.ForeignKey(Item,related_name='second_item', on_delete=models.CASCADE)
    item1win = models.BooleanField()
    time = models.DateTimeField(default=timezone.now)
    ipaddress = models.GenericIPAddressField(blank=True ,null=True)
    gender = models.CharField( 
        max_length=1,
        choices=Genders.choices
        )

    def __str__(self):
        if(self.item1win == True):
            return f"{self.item1} vs {self.item2}"
        else:
            return f"{self.item2} vs {self.item1}"
        