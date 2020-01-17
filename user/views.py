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
from collections import defaultdict

class UserListView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['get'])
@permission_classes([IsAuthenticated])
def FarmerDetailView(req):

    userObj=UserSerializer(req.user).data
    userObj.pop("password")
    return Response(userObj)
        



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



@api_view(['get'])
def FoodGrainDetailView(req,pk):
    foodgrains = []
    produces = []
    farmers = []
    res_quantity=defaultdict(int)
    res_price=defaultdict(int)
    res_farmers = {}
    
    for x in FoodGrain.objects.all():
        produces.append(x.produce.all())

    
    for x in produces:
        for y in x:
            key=str(y.farmer.contact)
            res_quantity[key]+=y.quantity
            res_quantity[key]=y.price
            res_farmers[key]=UserSerializer(y.farmer).data
    
    return Response([{
        'farmer':res_farmers[x],
        'quantity':res_quantity[x],
        'price':res_price[x]
    }for x in res_quantity])




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

class findWareHouse(APIView):
    def get(self, request, quantity, produceid):
        produce = Produce.objects.get(id=produceid)
        foodgrain = produce.type
        src = produce.location 
        warehouse = Warehouse.objects.filter(foodgrain=foodgrain).filter(total_space__gte=quantity)
        
        #Euclidean
        distances = []
        i=0
        for w in warehouse:
            distances.append((w.location.xloc**2+w.location.yloc**2,i))
            i+=1
        distances.sort()

        #top 5
        maxl = 5
        predicted_whid = []
        predicted_whname = []
        predicted_dis = []
        predicted_price = []
        predicted_avail_storage = []
        predicted_locx = []
        predicted_locy = []
        predicted_centre = []
        predicted_owner = []
        predicted_sector = []
        ispresent = False
        count=0
        result = []
        for d,i in distances:
            if count>=maxl:
                break
            count+=1
            predicted_whid=warehouse[i].pk
            predicted_whname=warehouse[i].name
            predicted_dis=d
            predicted_price=warehouse[i].price
            predicted_avail_storage=warehouse[i].free_space
            predicted_owner=warehouse[i].owner.name
            predicted_sector=warehouse[i].sector
            predicted_locx=warehouse[i].location.xloc
            predicted_locy=warehouse[i].location.yloc
            predicted_centre=warehouse[i].location.centre.id
            temp = {
                'whid':predicted_whid,
                'whname':predicted_whname,
                'distance':predicted_dis,
                'price':predicted_price,
                'locx':predicted_locx,
                'locy':predicted_locy,
                'avail_storage':predicted_avail_storage,
                'centre':predicted_centre,
                'owner':predicted_owner,
                'sector':predicted_sector,
            }
            result.append(temp)

        if len(distances)>0:
            ispresent = True

        res = {'data':result,'ispresent':ispresent}
        return Response(res)


@api_view(['get'])
def ListNotfications(req):
    queryset = Notifications.objects.filter(user = req.user)
    obj = NotificationSerializer(queryset,many=True)

    return Response(obj.data)
    