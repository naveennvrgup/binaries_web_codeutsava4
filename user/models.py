from django.db import models
from transaction.models import FoodGrain
# Create your models here.
class Location(models.Model):
    xloc=models.FloatField()
    yloc=models.FloatField()
    def __str__(self):
        return self.xloc



class User(models.Model):
    name=models.CharField(max_length=300)
    contact=models.CharField(max_length=12)
    addr=models.TextField()
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    dob=models.DateField()
    adhaar=models.CharField(unique=True,max_length=16)
    CHOICES = (
        ('FAR', 'Farmer'),
        ('BUY', 'Buyer'),
        ('WHO', 'Warehouse Owner'),
        ('NGO', 'NGO'),
    )
    role=models.CharField(max_length=1,choices=CHOICES)

    def __str__(self):
        return self.name


class Farms(models.Model):
    farmer=models.ForeignKey('User',on_delete=models.CASCADE)
    loc=models.ForeignKey(Location,on_delete=models.CASCADE)

    def __str__(self):
        return self.far

class Warehouse(models.Model):
    owner=models.ForeignKey('User',on_delete=models.CASCADE)
    CHOICES=(
                ('PRI','Private'),
                ('PUB','Public'),)

    sect=models.CharField(max_length=1,choices=CHOICES )
    fg=models.ForeignKey(FoodGrain,on_delete=models.CASCADE)
    Loc=models.ForeignKey(Location,on_delete=models.CASCADE)
    free=models.FloatField()
    total=models.FloatField()

    def __str__(self):
        return self.owner
