from rest_framework import serializers
from user.models import Location,FoodGrain,AppUser,Farms,Warehouse

class FoodGrainSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodGrain
        fields=['type','life']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['xloc','yloc']


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppUser
        fields=['name','user','contact','address','city','state','dob','adhaar','role']


class WarehouseSerilazer(serializers.ModelSerializer):
    class Meta:
        model=Warehouse
        fields=['owner','sect','foodgrain','location','total','free']

    class Meta:
        models=Farms
        fields=['farmer','location']
