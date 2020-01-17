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
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from collections import defaultdict

from rest_framework import status
import traceback

@api_view(['post'])
def PlaceOrderView(req):
    
    foodgrain = FoodGrain.objects.get(id=req.data['foodgrain_id'])
    buyer = req.user
    farmer = User.objects.get(contact=req.data['farmer_contact'])
    quantity = req.data['quantity']

    ts = TransactionSale.objects.create(
        type= '1',
        seller= farmer,
        buyer = buyer,
        quantity = quantity,
        foodgrain = foodgrain,
        price = foodgrain.price,
    )
    obj = TransactionSaleSerializer(ts).data

    return Response(obj)

class TotalBidListView(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

class ActiveBidListView(generics.ListCreateAPIView):
    queryset = Bid.objects.filter(isActive = True)
    serializer_class = BidSerializer


class BidDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

@api_view(['post'])
def CreateBidView(req):
    type = FoodGrain.objects.filter(id=req.data['foodgrain_id'])
    quantity = FoodGrain.objects.filter(id=req.data['quantity'])
    nbids = FoodGrain.objects.filter(id=req.data['price'])
    description = FoodGrain.objects.filter(id=req.data['description'])
    deadline = datetime.datetime.now()

    queryset = PlaceBid.objects.create(
        buyer = req.user,
        type = type,
        quantity= quantity,
        nbids=nbids,
        description=description,
        deadline=deadline
    )

    return Response(BidSerializer(queryset).data)
    


@api_view(['get'])
@permission_classes([IsAuthenticated])
def ProduceListView(req):

    queryset = req.user.produce.all()
    obj = ProduceSerializer(queryset,many=True).data

    return Response(obj)

@permission_classes([IsAuthenticated])
@api_view(['post'])
def report_produce(request):
    farmer = request.user
    foodgrain = FoodGrain.objects.get(id=request.data['fid'])
    grade = request.data['grade']
    quantity= request.data['quantity']
    price= request.data['price']

    location = farmer.farms.all()[0].location
    print('reached')

    produce = Produce.objects.create(farmer=farmer,type=foodgrain,grade=grade,quantity=quantity,location=location,price=price)
    produce.save()
    poduceserializer = ProduceSerializer(produce).data
    return Response(poduceserializer)



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


@api_view(['get'])
def BuyerOrdersListView(req):
    queryset = [x for x in req.user.sale_buyer.all()]
    data =TransactionSaleSerializer(queryset,many=True).data

    for i in range(len(queryset)):
        data[i]['foodgraintype']=queryset[0].foodgrain.type
        data[i]['seller']=queryset[0].seller.name
        data[i]['buyer']=queryset[0].buyer.name

    return Response(data)


@api_view(['get'])
def FarmerOrdersListView(req):
    queryset = [x for x in req.user.sale_seller.all()]
    data =TransactionSaleSerializer(queryset,many=True).data

    for i in range(len(queryset)):
        data[i]['foodgraintype']=queryset[0].foodgrain.type
        data[i]['seller']=queryset[0].seller.name
        data[i]['buyer']=queryset[0].buyer.name

    return Response(data)

@api_view(['get'])
def ApproveFarmerOrderView(req,id):
    obj = req.user.sale_seller.get(id=int(id))
    obj.approved=True
    obj.save()
    return Response(True)


@api_view(['get'])
def RejectFarmerOrderView(req,id):
    obj = req.user.sale_seller.get(id=int(id))
    obj.approved=False
    obj.save()
    return Response(True)


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


        