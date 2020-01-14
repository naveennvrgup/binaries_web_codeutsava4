from django.shortcuts import render
from rest_framework import viewsets, permissions,generics
from user.models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  

class UserListView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class FarmsListView(generics.CreateAPIView):

    queryset = Farms.objects.all()
    serializer_class = FarmsSerializer



class FarmsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Farms.objects.all()
    serializer_class = FarmsSerializer




class WarehouseListView(generics.ListCreateAPIView):

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer



class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer



class FoodGrainListView(generics.ListCreateAPIView):

    queryset = FoodGrain.objects.all()
    serializer_class = FoodGrainSerializer



class FoodGrainDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodGrain.objects.all()
    serializer_class = FoodGrainSerializer


class LocationListView(generics.ListCreateAPIView):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# Create your views here.
