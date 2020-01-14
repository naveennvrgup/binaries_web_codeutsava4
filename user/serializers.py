from rest_framework import serializers
from user.models import User, Farms, Warehouse, Location , FoodGrain
from rest_framework import status
from rest_framework.response import Response
import random

class UserSerializer(serializers.ModelSerializer):
    def create(self, valid_data):
        user = User(name = valid_data['name'],
                    contact = valid_data['contact'],
                    address = valid_data['address'],
                    city = valid_data['city'],
                    state = valid_data['state'],
                    dob = valid_data['dob'],
                    adhaar = valid_data['adhaar'],
                    role = valid_data['role'],
                    )
        user.username = user.contact
        user.set_password(valid_data['password'])
        print(user.username, user.password)
        user.save()
        return user


    class Meta:
        model = User
        fields = ['name','password', 'contact','address','city','state','dob','adhaar', 'role']
       



class FarmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farms
        fields = "__all__"
 

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
 



class FoodGrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodGrain
        fields = "__all__"
 
