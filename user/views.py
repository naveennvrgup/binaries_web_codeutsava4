from django.shortcuts import render
from rest_framework import viewsets, permissions,generics
from user.models import *
from transaction.models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  

class UserListView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['get'])
@permission_classes([IsAuthenticated])
def FarmerDetailView(req):
    # import pdb; pdb.set_trace()
    print(req.user.id)
    return Response("hello")
        



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



class getProduce(APIView):
    #returns list of id of produce of each farmer

    def get(self, request, pk):
        farmer = User.objects.get(id = pk)
        queryset = Produce.objects.filter(farmer = farmer)
        return Response({'produce':[produce.id for produce in queryset]})



class getUser(APIView):
    #return list of ids of each role
    def get(self, request, role):
        queryset = User.objects.filter(role = role)
        return Response({'users':[f.id for f in queryset]})


class getWarehouse(APIView):
    def get(self, request, pk):
        farmer = User.objects.get(id = pk)
        queryset = StorageTransaction.objects.filter(farmer = farmer)
        return Response({'warehouses':[f.warehouse.id for f in queryset]})

    

class getWarehouseUser(APIView):
    def get(self, request, pk):
        warehouse = Warehouse.objects.get(id = pk)
        queryset = StorageTransaction.objects.filter(warehouse=warehouse)
        return Response({'users':list(set([obj.farmer.id for obj in queryset]))})









