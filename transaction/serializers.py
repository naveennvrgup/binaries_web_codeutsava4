from rest_framework import serializers
from .models import *
from user.serializers import *
from rest_framework import status
from rest_framework.response import Response
import random

class BidSerializer(serializers.ModelSerializer):
    type=FoodGrainSerializer()
    buyer=UserSerializer()

    class Meta:
        model = Bid
        fields = "__all__"

class PlaceBidSerializer(serializers.ModelSerializer):

    def create(self, valid_data):
        placebid = PlaceBid(
            price = valid_data['price'],
            description = valid_data['description'],
            bid = valid_data["bid"],
            farmer = valid_data["farmer"]

        )
        placebid.save()
        bid = valid_data["bid"]
        bid.nbids+=1
        bid.save()

        return placebid

    class Meta:
        model = PlaceBid
        fields = "__all__"
 
 

class StorageTransactionSerializer(serializers.ModelSerializer):

    def create(self, valid_data):
        trans = StorageTransaction(
            warehouse=valid_data['warehouse'],
            farmer = valid_data['farmer'],
            produce=valid_data['produce'],
            quantity = valid_data['quantity'],
            cost = valid_data['cost'],

        )
        produce=valid_data['produce']
        trans.transno = random.randint(1,1000000)
        quantity = valid_data['quantity']
        if produce.quantity >= quantity:
            produce.quantity-=quantity
            produce.save() 
        else:
            trans.valid = False           
        trans.save()
        return trans



    class Meta:
        model = StorageTransaction
        fields = ['warehouse','farmer','produce','quantity','cost']
 
 


class TransactionSaleSerializer(serializers.ModelSerializer):

    def create(self, valid_data):
        trans = TransactionSale(
            type=valid_data["type"],
            seller=valid_data["seller"],
            buyer=valid_data["buyer"],
            produce=valid_data["produce"],
            warehouse = valid_data["warehouse"],
            quantity=valid_data["quantity"],
            price=valid_data["price"],

        )
        trans.transno = random.randint(1,1000000)           
        trans.save()
        return trans
    

    class Meta:
        model = TransactionSale
        fields='__all__'
 



class ProduceSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    type=FoodGrainSerializer()

    class Meta:
        model = Produce
        fields = "__all__"



