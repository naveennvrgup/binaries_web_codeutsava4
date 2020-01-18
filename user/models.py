from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class FoodGrain(models.Model):
    type=models.CharField(max_length=50)
    life=models.IntegerField()
    price=models.IntegerField(default=17) 

    def __str__(self):
        return self.type

class Location(models.Model):
    xloc=models.FloatField()
    yloc=models.FloatField()
    centre = models.ForeignKey('Centre',on_delete=models.CASCADE, related_name='locations', null = True)

    def __str__(self):
        return str(self.xloc)+','+str(self.yloc)

class User(AbstractUser):
    name=models.CharField(max_length=300)
    contact=models.CharField(max_length=12)
    address=models.TextField()
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    dob=models.DateField(null = True)
    adhaar=models.CharField(unique=True,max_length=16, null = True)
    CHOICES = (
        ('FAR', 'Farmer'),
        ('BUY', 'Buyer'),
        ('WHO', 'Warehouse Owner'),
        ('NGO', 'NGO'),
        ('ADM', 'Admin'),
        ('DVR', 'Delivery Partner'),
    )
    role=models.CharField(max_length=3,choices=CHOICES)

    def __str__(self):
        return self.name



class Farms(models.Model):
    farmer=models.ForeignKey('User',on_delete=models.CASCADE, related_name='farms')
    location=models.OneToOneField(Location,on_delete=models.CASCADE, related_name='farms')

    def __str__(self):
        return self.farmer.name

class Warehouse(models.Model):
    name = models.CharField(max_length = 50,default="")
    owner=models.ForeignKey('User',on_delete=models.CASCADE, related_name='warehouses')
    CHOICES=(
                ('PVT','Private'),
                ('PUB','Public'),
    )

    sector=models.CharField(max_length=3,choices=CHOICES )
    price = models.FloatField(default=20000)
    foodgrain=models.ForeignKey(FoodGrain,on_delete=models.CASCADE)
    location=models.ForeignKey(Location,on_delete=models.CASCADE)
    free_space=models.FloatField()
    total_space=models.FloatField()

    def __str__(self):
        return self.owner.name

class Centre(models.Model):
    cid = models.CharField(max_length=200)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    def_crops = models.ManyToManyField(FoodGrain, related_name="d_centre")
    rec_crops = models.ManyToManyField(FoodGrain, related_name="r_centre")
    #area --> ????
    #derived-> deficit fg, stats, profit
    @property
    def farms(self):
        locations = self.locations
        farms = [loc.farms for loc in locations]
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


class Notifications(models.Model):
    msg = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {} {} '.format( user,msg,seen)
