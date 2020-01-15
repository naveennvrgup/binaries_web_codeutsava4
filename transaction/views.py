from django.shortcuts import render

# Create your views here.
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

