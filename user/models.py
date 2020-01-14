from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FoodGrain(models.Model):
    type=models.CharField(max_length=50)
    life=models.IntegerField()

    def __str__(self):
        return self.type

class Location(models.Model):
    xloc=models.FloatField()
    yloc=models.FloatField()
    centre = models.ForeignKey('Centre',on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return str(self.xloc)+','+str(self.yloc)

class AppUser(models.Model):
    name=models.CharField(max_length=300)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact=models.CharField(max_length=12)
    address=models.TextField()
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
    role=models.CharField(max_length=3,choices=CHOICES)

    def __str__(self):
        return self.name


class Farms(models.Model):
    farmer=models.ForeignKey('AppUser',on_delete=models.CASCADE, related_name='farms')
    location=models.OneToOneField(Location,on_delete=models.CASCADE, related_name='farms')

    def __str__(self):
        return self.farmer.name

class Warehouse(models.Model):
    owner=models.ForeignKey('AppUser',on_delete=models.CASCADE, related_name='warehouses')
    CHOICES=(
                ('PVT','Private'),
                ('PUB','Public'),
    )

    sect=models.CharField(max_length=3,choices=CHOICES )
    foodgrain=models.ForeignKey(FoodGrain,on_delete=models.CASCADE, related_name='warehouses')
    location=models.OneToOneField(Location,on_delete=models.CASCADE)
    free=models.FloatField()
    total=models.FloatField()

    def __str__(self):
        return self.owner.name

class Centre(models.Model):
    cid = models.CharField(max_length=200)
    admin = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    #area --> ????
    #derived-> deficit fg, stats, profit
    @property
    def farms(self):
        locations = self.locations
        farms = [loc.farms for farms in locations]
        # for loc in locations:
        #     farms.append(loc.farms[0])
        return farms


    def __str__(self):
        return self.cid

class Demand(models.Model):
    foodgrain = models.ForeignKey(FoodGrain, on_delete=models.CASCADE)
    quantity = models.FloatField()
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.centre.cid)+'->'+str(self.foodgrain.type)+': '+str(self.quantity)