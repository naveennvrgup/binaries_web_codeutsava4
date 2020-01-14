from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.response import Response
import random

class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = "__all__"
 