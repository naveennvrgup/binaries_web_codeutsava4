from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, permissions,generics
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
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


class ProduceListView(generics.ListCreateAPIView):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer

class StorageTransactionListView(generics.ListCreateAPIView):
    queryset = StorageTransaction.objects.filter(valid = True)
    serializer_class = StorageTransactionSerializer


class TransactionSaleListView(generics.ListCreateAPIView):
    queryset = TransactionSale.objects.all()
    serializer_class = TransactionSaleSerializer
