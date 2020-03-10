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
from collections import defaultdict, Counter
import math




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
    serializer_class = WarehouseDetailSerializer



class FoodGrainListView(generics.ListCreateAPIView):

    queryset = FoodGrain.objects.all()
    serializer_class = FoodGrainSerializer



@api_view(['get'])
def FoodGrainDetailView(req,pk):
    foodgrains = []
    produces = []
    warehouses = []
    farmers = []
    res_quantity=defaultdict(int)
    res_price=defaultdict(int)
    res_farmers = {}
    
    currfoodgrain = FoodGrain.objects.get(id=pk)
    produces = Produce.objects.filter(type = currfoodgrain)
    # warehouses = Warehouse.objects.filter(foodgrain=currfoodgrain)

    result = []

    for produce in produces:
        temp = {}
        farmer = produce.farmer
        quantity = produce.quantity
        farmerwarehouse = StorageTransaction.objects.filter(produce = produce)
        for fw in farmerwarehouse:
            quantity+= fw.quantity
        price = produce.price
        temp['farmer'] = UserSerializer(farmer).data
        temp['quantity'] = quantity
        temp['price'] = price
        temp['produce_id'] = produce.pk
        result.append(temp)

    return Response(result)


    
    # for x in produces:
    #     for y in x:
    #         key=str(y.farmer.contact)
    #         res_quantity[key]+=y.quantity
    #         res_quantity[key]=y.price
    #         res_farmers[key]=UserSerializer(y.farmer).data
    
    # return Response([{
    #     'farmer':res_farmers[x],
    #     'quantity':res_quantity[x],
    #     'price':res_price[x]
    # }for x in res_quantity])




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
        quantity = int(quantity)
        produceid = int(produceid)
        produce = Produce.objects.get(id=produceid)
        foodgrain = produce.type
        src = produce.location 
        warehouse = Warehouse.objects.filter(foodgrain=foodgrain).filter(free_space__gte=quantity)
        
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
            predicted_dis=round(math.sqrt(d),2)
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
                'availstorage':predicted_avail_storage,
                'centre':predicted_centre,
                'owner':predicted_owner,
                'sector':predicted_sector,
            }
            result.append(temp)

        if len(distances)>0:
            ispresent = True

        res = {'data':result,'ispresent':ispresent}
        return Response(res)

class FarmerAI(APIView):
    def get(self, request):
        farmer = request.user
        print('a',farmer.farms.all())
        loc = farmer.farms.all()[0].location
        print('adarsh')
        rec_crops = Centre.objects.get(locations = loc).rec_crops
        def_crops = Centre.objects.get(locations = loc).def_crops
        # print(rec_crops)

        return Response({'rec_crops' : [i.type for i in rec_crops.all()], 'def_crops' : [i.type for i in def_crops.all()]})

    

@api_view(['get'])
def ListNotfications(req):
    queryset = Notifications.objects.filter(user = req.user)
    obj = NotificationSerializer(queryset,many=True)

    return Response(obj.data)
    

@api_view(['get'])
def delayView(req):
    import time
    time.sleep(3)
    return Response("something")


@api_view(['get'])
def GraphyView(req):
    users = User.objects.filter(role = "FAR")
    centres = Centre.objects.all()
    warehouses = Warehouse.objects.all()
    farms = Farms.objects.all()

    farms_list = []
    user_list = []
    centre_list = []
    warehouse_list = []
    # print('a')

    for i in users:
        user_list.append(i.name)
    for i in centres:
        centre_list.append("Center : " + str(i.id))
    for i in warehouses:
        warehouse_list.append(i.name)
    for i in farms:
        farms_list.append("Farm : "+str(i.id))

    # print('a')
    
    labels = set(user_list + centre_list + warehouse_list + farms_list)

    conn =[]
    farm_farmer = []
    centre_farmer = []
    farmer_warehouse = []
    # print('a')
    for centre in centres:
        dic = {'farms' : [], 'farmers' : [], 'warehouses' : [] }
        far_list =[]
        # print('a')
        loc = Location.objects.filter(centre = centre)
        farms_ = []
        # print('b')
        for loc_i in loc:
            f = []
            for i in farms:
                if i.location in loc:
                    f.append(i)
            for ff in f:
                farms_.append(ff)
                # print('d')
        farmers_ = []
        for farm in farms_:
            farmers_.append(farm.farmer.name)
            farm_farmer.append((farm.farmer.name, "Farm : "+str(farm.id)))
            centre_farmer.append(("Centre : " + str(centre.id), farm.farmer.name))

        for trans in StorageTransaction.objects.all():
            farmer_warehouse.append((trans.farmer.name, trans.warehouse.name)) 

    conn = list(set(farm_farmer + centre_farmer + farmer_warehouse))
    return Response({"labels":labels, "connections": conn})

        
            


class PotentialBuyers(APIView):
    def get(self, request, foodgrain):
        type = FoodGrain.objects.get(type = foodgrain)
        print(type)
        trans = TransactionSale.objects.filter(foodgrain = type)
        users = []
        for tran in trans:
            users.append(tran.buyer)
        print(users)
        cnt = Counter(users)
        users = list(set(users))
        users.sort(key = lambda i : cnt[i], reverse = True)
        users = [{'name':user.name, "contact": user.contact} for user in users]
        return Response(users)
        








    
        






















# @api_view(['get'])
# def GraphyView(req):
#     centres = [x for x in Centre.objects.all()]
#     farmers = []
#     labels = set(['server'])
#     connections = []

#     black='#000000'
#     green='#00ff00'
#     blue='#0000ff'
#     red='#ff0000'

#     for x in centres:
#         for y in x.user_set.all():
#             if y.role=='FAR':
#                 labels.add(y.name+' '+y.dob)
#                 farmers.append(y)
#                 connections.append([x.cid,y.name,green])
    
#     for x in farmers:
#         i=1
#         for y in x.farms:
#             farmname=x.name+' farm '+str(i)
#             labels.add(farmname)
#             connections.append([x.name,farmname,blue])
#             i+=1

#         for y in x.warehouses:
#             labels.add(y.name)
#             connections.append([x.name,y.name,black])

#     for x in centres:

#     return Response({
#         'connections': connections,
#         'labels': list(labels)
#     })
#         labels.add(x.cid)
#         connections.append(['server',x.cid,red])
        

#     return Response({
#         'connections': connections,
#         'labels': list(labels)
#     })