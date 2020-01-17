from django.views.generic import View
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
from transaction.utils import render_to_pdf
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse


class GeneratePdf(View): #function to GeneratePdf
    def get(self, request, *args, **kwargs):
        data={  #fake datas

               'id':1234,
               'buyer':'XYZ',
               'seller':'ABC',
               'today':datetime.date.today(),
               'price':10000,
               'quant':100,
               'grain':'wheat',
            }
        pdf = render_to_pdf('transaction/invoice.html', data)
        return pdf







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

@permission_classes([IsAuthenticated])
@api_view(['get'])
def ProduceListView(req):

    queryset = req.user.produce.all()
    obj = ProduceSerializer(queryset,many=True).data

    return Response(obj)



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
                quantity=float(arr[2]),
                price=float(arr[3]),
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

        elif arr[0]=="bid":
            transno=Bid.objects.get(transno=arr[1])
            bidval=PlaceBid(
                        bid=transno,
                        farmer=user,
                        price=float(arr[2]),
                        description=arr[3],


            )
            bidval.save()
            message="Bid Placed Successfully"

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
