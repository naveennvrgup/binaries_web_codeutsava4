from django.shortcuts import render
from datetime import date
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import viewsets, permissions,generics
from .models import *
from user.models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from collections import defaultdict


class TotalBidListView(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

class ActiveBidListView(generics.ListCreateAPIView):
    queryset = Bid.objects.filter(isActive = True)
    serializer_class = BidSerializer


class BidDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class PlaceBidListView(generics.ListCreateAPIView):
    queryset = PlaceBid.objects.all()
    serializer_class = PlaceBidSerializer


class ProduceListView(generics.ListCreateAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer

class StorageTransactionListView(generics.ListCreateAPIView):
    queryset = StorageTransaction.objects.filter(valid = True)
    serializer_class = StorageTransactionSerializer


class TransactionSaleListView(generics.ListCreateAPIView):
    queryset = TransactionSale.objects.all()
    serializer_class = TransactionSaleSerializer


class ProduceListFilter(APIView):
    
    
    def get(self, request):
        num = request.GET['num']
        type = request.GET['type']
        type = FoodGrain.objects.get(id = type)
        queryset = Produce.objects.filter(type = type)
        ans = []
        for i in queryset:
            if i.quantity>int(num):
                ans.append(i.id)
        return Response({'produce':ans})

class ApproveOrder(APIView):
    def get(self, request, pk):
        id_ = pk
        obj = TransactionSale.objects.get(id = id_)
        if obj.produce.quantity >= obj.quantity:
            obj.approved = True
            obj.produce.quantity-=obj.quantity
            obj.produce.save()
            mess = "Order Approved"
        else:
            obj.valid = False
            mess = "Not Enough Produce"
        obj.save()        
        return Response({'message':mess})




def gen_mess(user, arr):
        
        
        if arr[0]=='report':    # type quant price grade
            loc = Location(xloc = 0, yloc = 0)
            loc.save()
            type = FoodGrain.objects.get(type = arr[1])
            prdc = Produce(
                type = type,
                farmer=user,
                grade=arr[4],
                quantity=int(arr[2]),
                price=int(arr[3]),
                location = loc,
                date=date.today()
            )
            prdc.save()
            message = "Produce saved"

        elif arr[0] == 'store':
            type = FoodGrain.objects.get(type = arr[1])
            queryset = Warehouse.objects.filter(foodgrain = type , free_space__gt = int(arr[2]))
            message=""
            for i in queryset:
                message+=i.name +"\n"+str(i.free_space)+"\n"+str(i.total_space)+"\n\n"

        elif arr[0] == 'approve' or arr[0] == 'decline':
            order = TransactionSale.objects.get(transno = int(arr[1]))
            if arr[0] == 'approve':
                order.approve = True
                message = "Order Approved"
            else:
                order.approve = False
                message = "Order Declined"
            order.save()
        return message


@api_view(['GET', 'POST', ])
def message(request):
    contact = request.GET['contact']
    message = request.GET['message']
    message=message.lower()
    user = User.objects.get(contact = contact)
    arr = message.split(' ')
    mess = gen_mess(user,arr)
    print(message)
    return Response({'message':mess})

    


    

    
    



class GetCenterDetails(APIView):
    def get(self, request, pk):
        id_ = pk
        centre = Centre.objects.get(id = id_)
        loc = Location.objects.filter(centre = centre)
        farms = [farm.id for farm in Farms.objects.all() if farm.location in loc]
        farmers = [Farms.objects.get(id = i).farmer.id for i in farms]
        produce = [prdc.id for prdc in Produce.objects.all() if prdc.location in loc]
        warehouses = [warehouse.id for warehouse in Warehouse.objects.all() if warehouse.location in loc]
        storage_transactions = [st for st in StorageTransaction.objects.all() if st.warehouse.location in loc]
        sale_transactions = [st for st in TransactionSale.objects.all() if st.seller.id in farmers]
        quant = defaultdict(lambda : 0)
        storage_revenue = defaultdict(lambda : 0)
        sale_revenue = defaultdict(lambda : 0)
        print(produce, storage_transactions, sale_transactions)
        for i in produce:
            quant[Produce.objects.get(id = i).type.id]+=Produce.objects.get(id = i).quantity
            
        for i in storage_transactions:
            quant[i.produce.type.id]+=i.quantity
            storage_revenue[i.produce.type.id] += i.cost
        for i in sale_transactions:
            sale_revenue[i.produce.type.id] += i.price



        
            


        
        return Response({'farms' : farms, 'farmers' : farmers, 'produce' : produce , 'warehouses':  warehouses, 'quant' : quant, 'storage_revenue': storage_revenue, 'sale_revenue':sale_revenue})


        