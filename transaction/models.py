from django.db import models
from user.models import User,Farms,Warehouse,FoodGrain


# Create your models here.
"""
Add an image field
"""

#add default date
class Produce(models.Model):
    type=models.ForeignKey(FoodGrain,on_delete=models.CASCADE)
    farmer=models.ForeignKey(User,on_delete=models.CASCADE)
    grade=models.CharField(max_length=50)
    quantity=models.FloatField()
    price=models.FloatField()
    date=models.DateField()

    def __str__(self):
        return self.farmer.name

#add default date
class StorageTransaction(models.Model):
    transno=models.CharField(max_length=50,unique=True)
    warehouse=models.OneToOneField(Warehouse,on_delete=models.CASCADE)
    produce=models.OneToOneField(Produce,on_delete=models.CASCADE)
    quantity = models.FloatField()
    cost = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.transno


class TransactionSale(models.Model):
    CHOICES = (
        ("1", "Own"),
        ("2", "Warehouse"),
    )
    transno = models.CharField(max_length=50,unique=True)
    approved=models.BooleanField(default=False)
    type=models.CharField(max_length=1,choices = CHOICES)
    seller=models.ForeignKey(Farms,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    produce=models.ForeignKey(Produce, blank=True, null=True, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, blank=True, null=True, on_delete=models.CASCADE)
    quantity=models.FloatField()
    price=models.FloatField()
    # dprice=models.FloatField()

    def __str__(self):
        return self.transno

"""
Add a completely new delivery model, with a new user role.
"""
# class Delivery(models.Model):
#     name=models.CharField(max_length=50)
#     cont = models.CharField(max_length=50)
#     cost=models.FloatField()
#     loc=models.ForeignKey(Location,on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


class Bid(models.Model):
    transno=models.CharField(max_length=50,unique=True)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.ForeignKey(FoodGrain,on_delete=models.CASCADE)
    quantity=models.FloatField()
    description=models.TextField()
    deadline=models.DateField()

    def __str__(self):
        return self.buyer

class PlaceBid(models.Model):
    bid=models.ForeignKey(Bid,on_delete=models.CASCADE)
    farmer=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.FloatField()
    description=models.TextField()

    def __str__(self):
        return self.bid