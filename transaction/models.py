from django.db import models
from user.models import Location,User,Farms,Warehouse


# Create your models here.
class FoodGrain(models.Model):
    type=models.CharField(max_length=50)
    life=models.IntegerField()

    def __str__(self):
        return self.type


class Produce(models.Model):
    type=models.ForeignKey(FoodGrain,on_delete=models.CASCADE)
    sec=models.ForeignKey(User,on_delete=models.CASCADE)
    grade=models.CharField(max_length=50)
    quan=models.FloatField()
    price=models.FloatField()
    dop=models.DateField()


    def __str__(self):
        return self.sec

class StorageTransaction(models.Model):
    transno=models.CharField(max_length=50,unique=True)
    war=models.OneToOneField(Warehouse,on_delete=models.CASCADE)
    produce=models.OneToOneField(Produce,on_delete=models.CASCADE)
    quant =models.FloatField()

    def __str__(self):
        return self.war


class TransactionSale(models.Model):
    CHOICES = (
        ("1", "Buyer"),
        ("2", "E-Commerce"),
    )
    tran_no = models.CharField(max_length=50,unique=True)
    app=models.BooleanField(default=False)
    type=models.CharField(max_length=1,choices = CHOICES)
    seller=models.ForeignKey(Farms,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    prod=models.ForeignKey(Produce,on_delete=models.CASCADE)
    quant=models.FloatField()
    price=models.FloatField()
    dprice=models.FloatField()


    def __str__(self):
        return self.app


class Delivery(models.Model):
    name=models.CharField(max_length=50)
    cont = models.CharField(max_length=50)
    cost=models.FloatField()
    loc=models.ForeignKey(Location,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bid(models.Model):
    transno=models.CharField(max_length=50,unique=True)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.ForeignKey(FoodGrain,on_delete=models.CASCADE)
    quant=models.FloatField()
    desc=models.TextField()
    deadline=models.DateField()

    def __str__(self):
        return self.buyer

class PlaceBid(models.Model):
    bid=models.ForeignKey(Bid,on_delete=models.CASCADE)
    farmer=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.FloatField()
    desc=models.TextField()

    def __str__(self):
        return self.bid