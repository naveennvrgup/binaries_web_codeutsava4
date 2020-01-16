from django.shortcuts import render
from datetime import date
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import viewsets, permissions,generics
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import status
import traceback

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



@api_view(['get'])
@permission_classes([IsAuthenticated])
def ProduceListView(req):

    queryset = req.user.produce.all()
    obj = ProduceSerializer(queryset,many=True).data

    return Response(obj)



class StorageTransactionListView(generics.ListCreateAPIView):
    queryset = StorageTransaction.objects.filter(valid = True)
    serializer_class = StorageTransactionSerializer


@api_view(['get'])
@permission_classes([IsAuthenticated])
def TransactionSaleListView(req):
    queryset = TransactionSale.objects.filter(buyer=req.user)
    data = TransactionSaleSerializer(queryset,many=True).data

    return Response(data)

@api_view(['post'])
def CreateTransactionView(req):
    
    try:
        foodgrain_id=int(req.data['foodgrain_id'])
        from_produce=int(req.data['from_produce'])
        from_warehouse = int(req.data['from_warehouse'])

        foodgrain = FoodGrain.objects.get(pk=foodgrain_id)
        produce = foodgrain.produce.all()[0]
        price = foodgrain.price * (from_produce + from_warehouse)

        warehouse = foodgrain.warehouse_set.all()
        warehouse = warehouse[0] if warehouse else None

        produce.quantity -= from_produce
        produce.save()

        if warehouse:
            warehouse.quantity -= from_warehouse
            warehouse.save()

        deal_type=None
        if from_produce and from_warehouse:
            deal_type='3'
        elif from_produce:
            deal_type='1'
        else:
            deal_type='2'


        farmer = None
        if produce.farmer:
            farmer = produce.farmer
        else:
            farmer = warehouse.owner


        ts = TransactionSale.objects.create(
            type = deal_type,
            seller = farmer,
            buyer = req.user,
            produce = produce,
            warehouse = warehouse,
            quantity= from_produce +from_warehouse,
            price = price
        )

        data = TransactionSaleSerializer(ts).data

        return Response(data, status=status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return Response('something went bad',status=status.HTTP_400_BAD_REQUEST)
    

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

    

    

    
    



        