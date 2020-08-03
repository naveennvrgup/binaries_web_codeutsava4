from django.views.generic import View
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
from .sms import send_sms
from django.core.files import File
from django.template.response import TemplateResponse


from rest_framework import status
import traceback
import http 
from decouple import config


from django.db.models.signals import post_save
from django.dispatch import receiver


invoice_html = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>A simple, clean, and responsive HTML invoice template</title>
    
    <style>
    .invoice-box {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
        font-size: 16px;
        line-height: 24px;
        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        color: #555;
    }
    
    .invoice-box table {
        width: 100%;
        line-height: inherit;
        text-align: left;
    }
    
    .invoice-box table td {
        padding: 5px;
        vertical-align: top;
    }
    
    .invoice-box table tr td:nth-child(2) {
        text-align: right;
    }
    
    .invoice-box table tr.top table td {
        padding-bottom: 20px;
    }
    
    .invoice-box table tr.top table td.title {
        font-size: 45px;
        line-height: 45px;
        color: #333;
    }
    
    .invoice-box table tr.information table td {
        padding-bottom: 40px;
    }
    
    .invoice-box table tr.heading td {
        background: #eee;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
    }
    
    .invoice-box table tr.details td {
        padding-bottom: 20px;
    }
    
    .invoice-box table tr.item td{
        border-bottom: 1px solid #eee;
    }
    
    .invoice-box table tr.item.last td {
        border-bottom: none;
    }
    
    .invoice-box table tr.total td:nth-child(2) {
        border-top: 2px solid #eee;
        font-weight: bold;
    }
    
    @media only screen and (max-width: 600px) {
        .invoice-box table tr.top table td {
            width: 100%;
            display: block;
            text-align: center;
        }
        
        .invoice-box table tr.information table td {
            width: 100%;
            display: block;
            text-align: center;
        }
    }
    
    /** RTL **/
    .rtl {
        direction: rtl;
        font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    }
    
    .rtl table {
        text-align: right;
    }
    
    .rtl table tr td:nth-child(2) {
        text-align: left;
    }
    </style>
</head>

<body>
    <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">
            <tr class="top">
                <td colspan="2">
                    <table>
                        <tr>
                            <td class="title">
                                <h4>Invoice </h4>
                                <p>[ TEAM BINARIES ]</p>
                            </td>
                            
                            <td>
                                Invoice #: {{}}<br>
                                Created: {{}}<br>
                                Due: {{}}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            
            <tr class="information">
                <td colspan="2">
                    <table>
                        <tr>
                            <td>
                                Mr./Mrs. {{}}<br>
                                {{}}
                                Contact: {{}}
                            </td>
                            
                            <td>
                                Mr./Mrs. {{}}<br>
                                {{}}<br>
                                Contact: {{}}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            
            <tr class="heading">
                <td>
                    Payment Method
                </td>
                
                <td>
                    Check #
                </td>
            </tr>
            
            <tr class="details">
                <td>
                    Cash 
                </td>
                
                <td>
                    Rs. {{}}
                </td>
            </tr>
            
            <tr class="heading">
                <td>
                    Item
                </td>
                
                <td>
                    Price
                </td>
            </tr>
            
            <tr class="item">
                <td>
                    {{}}
                </td>
                
                <td>
                    Rs. {{}}
                </td>
            </tr>
            
            
            <tr class="total">
                <td></td>
                
                <td>
                   Total: Rs. {{}}
                </td>
            </tr>
        </table>
        <div style='text-align:center'>This is a machine generated invoice</div>
    </div>
</body>
</html>
"""


@receiver(post_save, sender=TransactionSale)
def save_profile(sender, instance, **kwargs):
    import pdfkit 
    import datetime
    if instance.approved:
        global invoice_html
        temp = invoice_html.split('{{}}')
        
        transno = instance.transno
        created_date = datetime.datetime.now().strftime("%d/%m/%Y")
        seller = instance.seller.name
        seller_address = instance.seller.address +','+instance.seller.city+','+instance.seller.state
        seller_contact = instance.seller.contact
        buyer = instance.buyer.name
        buyer_address = instance.buyer.address +','+instance.buyer.city+','+instance.buyer.state
        buyer_contact =instance.buyer.contact
        total_amount = instance.price
        foodgrain = instance.foodgrain.type


        data = [transno, created_date, created_date, seller, seller_address, seller_contact,
        buyer, buyer_address, buyer_contact, total_amount, foodgrain,total_amount,total_amount] 
        data = [str(x) for x in data]

        final_html_str = temp[0]

        for i in range(len(data)):
            final_html_str +=data[i]
            final_html_str +=temp[i+1]

        storage_url = 'invoices/tsale{}.pdf'.format(transno)
        pdfkit.from_string(final_html_str,storage_url.format(transno)) 
        instance.invoice.save('new', File(open(storage_url)))
        # instance.invoice


        
        



@api_view(['post'])
def PlaceOrderView(req):
    print("foodgrainid",req.data['foodgrain_id'])
    print(req.data)
    foodgrain = FoodGrain.objects.get(id=req.data['foodgrain_id'])
    buyer = req.user
    print(req.data)
    farmer = User.objects.filter(contact=req.data['farmer_contact'])[0]
    quantity = req.data['quantity']
    prod_id = req.data['produce_id']
    prod = Produce.objects.get(id=prod_id)

    price = prod.price

    

    ts = TransactionSale.objects.create(
        type= '1',
        seller= farmer,
        buyer = buyer,
        quantity = quantity,
        foodgrain = foodgrain,
        price = price,
        order_details = OrderDetails.objects.create(),
    )
    obj = TransactionSaleSerializer(ts).data
    message = buyer.name+ " wants to buy "+str(ts.quantity)+"kg of "+foodgrain.type+" from you. Contact- "+str(buyer.contact) +". Order id is : "+str(ts.id)

    send_sms(farmer.contact, message)

    return Response(obj)


class OrderDetailsUpdateView(generics.UpdateAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer



class TotalBidListView(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

class ActiveBidListView(generics.ListAPIView):
    queryset = Bid.objects.filter(isActive = True)
    serializer_class = BidSerializer


class BidDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

@api_view(['post'])
def CreateBidView(req):
    print(req.data)
    type = FoodGrain.objects.get(type=req.data['foodgrain'].lower())
    quantity = req.data['quantity']
    description = req.data['description']
    deadline = datetime.datetime(2020,2,2)

    queryset = PlaceBid.objects.create(
        buyer = req.user,
        type = type,
        quantity= int(quantity),
        nbids=0,
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
    old_produce = Produce.objects.filter(farmer=farmer,type=foodgrain)
    if old_produce:
        old_produce = old_produce[0]
        old_produce.quantity += quantity
        old_produce.save()
        poduceserializer = ProduceSerializer(old_produce).data
    else:
        produce = Produce.objects.create(farmer=farmer,type=foodgrain,grade=grade,quantity=quantity,location=location,price=price)
        produce.save()
        poduceserializer = ProduceSerializer(produce).data
    send_sms(farmer.contact, "Your produce has been Reported")
    return Response(poduceserializer)

class StorageTransactionListView(generics.ListCreateAPIView):
    queryset = StorageTransaction.objects.filter(valid = True)
    serializer_class = StorageTransactionSerializer

@api_view(['post'])
def createStorageTransaction(request):
    warehouse = Warehouse.objects.get(id=request.data['warehouse'])
    produce = Produce.objects.get(id=request.data['produce'])
    farmer = request.user
    quantity = request.data['quantity']
    cost = warehouse.price
    if quantity <= produce.quantity and quantity <= warehouse.free_space:

    # transno = random.randint(1,1000000)
        storagetransaction = StorageTransaction.objects.create(
            warehouse = warehouse,
            produce = produce,
            farmer = farmer,
            quantity = quantity,
            cost = cost,
            farmerprice = produce.price,
            foodgrain = produce.type
        )
        storagetransaction.save()

        produce.quantity -= quantity
        produce.save()

        warehouse.free_space -= quantity
        warehouse.save()
        print('saved')

        # data = StorageTransactionSerializer(storagetransaction).data
        # print(data)

        return Response({"flag":True,}, status=status.HTTP_200_OK)
    else:
        return Response({"flag":False, "message":"Not enough produce or insufficient space in warehouse"})

@api_view(['get'])
@permission_classes([IsAuthenticated])
def TransactionSaleListView(req):
    queryset = TransactionSale.objects.filter(buyer=req.user)
    data = TransactionSaleSerializer(queryset,many=True).data

    return Response(data)


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
        data[i]['foodgraintype']=queryset[i].foodgrain.type
        data[i]['seller']=queryset[i].seller.name
        data[i]['buyer']=queryset[i].buyer.name
    print(data)
    return Response(data)


@api_view(['get'])
def FarmerOrdersListView(req):
    queryset = [x for x in req.user.sale_seller.all()]
    data =TransactionSaleSerializer(queryset,many=True).data

    for i in range(len(queryset)):
        data[i]['foodgraintype']=queryset[i].foodgrain.type
        data[i]['seller']=queryset[i].seller.name
        data[i]['buyer']=queryset[i].buyer.name
        data[i]['price']=queryset[i].price
        data[i]['quantity']=queryset[i].quantity

    print(data)
    return Response(data)

@api_view(['post'])
def ApproveFarmerOrderView(req,id):

    tsale = req.user.sale_seller.get(id=int(id))
    get_from = req.data['get_from']
    quantity_to_delete = tsale.quantity
    print(req)
    produce = Produce.objects.filter(type = tsale.foodgrain)
    if produce:
        produce = produce[0]
    else:
        produce = None  

    
    strans = StorageTransaction.objects.filter(farmer=tsale.seller, foodgrain = tsale.foodgrain)
    print(strans)
    if strans:
        strans = strans[0]
    else:
        strans = None


    if get_from=='produce':
        if produce:
            if produce.quantity >= quantity_to_delete:
                produce.quantity -= quantity_to_delete
                produce.save()
            else:
                quantity_to_delete -= produce.quantity
                produce.quantity = 0
                produce.save()
                produce.delete()
                if strans.quantity >= quantity_to_delete:
                    strans.quantity -= quantity_to_delete
                    strans.save()
                else:
                    return Response({"message": "Not enough grain available", "flag":False})
        else:
            
            if strans.quantity >= quantity_to_delete:
                strans.quantity -= quantity_to_delete
                strans.save()
                if strans.quantity == 0:
                    strans.delete()
            else:
                return Response({"message": "Not enough grain available", "flag":False})

    else:
        if strans.quantity >= quantity_to_delete:
            strans.quantity -= quantity_to_delete
            strans.save()
        else:
            quantity_to_delete -= strans.quantity
            strans.delete()
            if produce and produce.quantity >= quantity_to_delete:
                produce.quantity -= quantity_to_delete
                produce.save()
                if produce.quantity == 0:
                    produce.delete()


            else:
                return Response({"message":"Not enough available"})


    tsale.approved=True
    tsale.save()

    #send_sms(tsale.buyer.contact, "Your Order has been approved")


    return Response(True)


@api_view(['get'])
def RejectFarmerOrderView(req,id):
    req.user.sale_seller.get(id=int(id)).delete()
    #send_sms(req.user.sale_buyer.contact, "Your Order has been approved")
    return Response(True)


def gen_mess(user, arr):
    print(arr)
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
            message+="Name : " +i.name +"\\n"+"Free Space : " + str(i.free_space)+"\\n"+"Total Space"+str(i.total_space)+""  

    elif arr[0] == 'approve' or arr[0] == 'decline':
        order = TransactionSale.objects.get(transno = int(arr[1]))
        if arr[0] == 'approve':
            order.approve = True
            message = "Order number "+arr[1]+" Approved"
        else:
            order.approve = False
            message = "Order number "+arr[1]+" Decline"
        order.save()

    elif arr[0]=="getbid" or arr[0] =="किसान":
            queryset = Bid.objects.all()
            message = ''
            for i in queryset:
                message += "Bid no : "+str(i.transno) + "//n" + "FoodGrain : "+i.type.type + "//n"+"Quantity : "+str(i.quantity) +"//n"+"Description : "+i.description

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

    elif arr[0] == "weather":
            message = "Weather report for following Month : Mostly Sunny , Expected light showers on 5,6 and 7 February"
    else:
        message = "PLease follow the standard format"

    print(message)
    return message

from transaction.sms import send_sms

@api_view(['POST'])
def message(request):
    contact = request.data['contact']
    message = request.data['message']+" "
    newcontact = contact[3:]
    print(contact, message)
    message=message.lower()
    try:
        user = User.objects.get(contact = newcontact)
    except:
        message = "Rishabh's private message"
        print("Rishabh's private message")
    else:
        arr = message.split(' ')
        mess = gen_mess(user,arr)
        #send_sms(newcontact,mess)
        print(user)
        print(mess)
    return Response({'message':message})


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


@api_view(['get'])
def farmerDashboardGraphView(req):
    import random
    result = []
    one = 34
    two = 44
    three=59

    months = ['jan','feb','mar','apr','jun','jul','aug','sep','oct','nov','dec']
    for month in months:
        change = 5

        one_diff = change*(random.random())/100
        two_diff = change*(random.random())/100
        three_diff = change*(random.random())/100

        if random.randint(0,10)>5:
            one-=one*one_diff
        else:
            one+=one*one_diff

        if random.randint(0,10)>5:
            two-=two*two_diff
        else:
            two+=two*two_diff

        if random.randint(0,10)>5:
            three-=three*three_diff
        else:
            three+=three*three_diff

        result.append([month,one,two,three])
    
    return Response(result)



@api_view(['get'])
def PastBidList(req):
    user = req.user
    bids = Bid.objects.filter(buyer = user)
    bids = BidSerializer(bids,many=True).data
    return Response(bids)

@api_view(['get'])
def FarmerPlacedbids(request,id):
    user = request.user
    placedbids = PlaceBid.objects.filter(bid = Bid.objects.get(id=id))
    obj = [{
        "bid":x.id,
        'farmer':x.farmer.name,
        'price':x.price,
        'description':x.description
    } for x in placedbids]
    return Response(obj)



@api_view(['get'])
def FarmerActiveBidList(request):
    user = request.user
    activeplacedbids = Bid.objects.filter(isActive = True)
    obj = BidSerializer(activeplacedbids,many=True).data
    return Response(obj)


@api_view(['GET', 'POST'])
def FarmerPlaceBid(request):    
    farmer = request.user
    bid = Bid.objects.get(id=int(request.data['bidno']))
    PlaceBid(bid = bid, 
    farmer = farmer, 
    price = int(request.data['price']), 
    description = request.data['description']).save()
    return Response(True)
    

@api_view(['GET'])
def FarmerResponseBidList(request, pk):    
    bid = Bid.objects.get(id = pk)
    pbids = bid.placebid_set.all()
    pbids = PlaceBidSerializer(pbids,many=True).data
    print(pbids)
    return Response(pbids)


@api_view(['GET'])
def ApproveBid(request, pk):  
    import random
    print('a', pk)
    print(PlaceBid.objects.all())
    placedBid = PlaceBid.objects.get(id = int(pk))  

    bid = placedBid.bid

    transno = random.randint(1, 10**6)
    approved = True
    type = bid.type.type
    seller = placedBid.farmer
    buyer = bid.buyer
    foodgrain = bid.type
    quantity = placedBid.bid.quantity
    price = placedBid.price
    TransactionSale(
        transno = transno, 
        approved =approved, 
        type = type, 
        seller =seller, 
        buyer = buyer, 
        foodgrain = foodgrain, 
        quantity = quantity, 
        price = price).save()
    
    bid.isActive=False
    bid.save()

    return Response("Transaction Done")

@api_view(['post'])
def createBid(req):
    bid = Bid.objects.create(
        buyer=req.user,
        type=FoodGrain.objects.get(type=req.data['foodgrain'].lower()),
        quantity=int(req.data['quantity']),
        description=req.data['description'],
        deadline='2020-02-01'
    )
    obj = BidSerializer(bid).data
    return Response(obj)

@api_view(['get'])
def get_farmer_storage_warehouse(request):
    farmer = request.user
    print(farmer.name)
    storagetransactions = StorageTransaction.objects.filter(farmer=farmer)
    print(storagetransactions)
    # warehouses = [st.warehouse.id for st in storagetransactions]
    # queryset = Warehouse.objects.filter(pk__in = warehouses)
    data = StorageTransactionSerializer(storagetransactions,many=True).data
    return Response(data)


class DefCentreView(APIView):
    def get(self, request):
        id_ = 1
        centre = Centre.objects.get(cid = id_)
        loc = Location.objects.filter(centre = centre)
        farms = [farm.id for farm in Farms.objects.all() if farm.location in loc]
        farmers = [Farms.objects.get(id = i).farmer.contact for i in farms]
        print(centre.def_crops)
        message = "Centre : "+str(id_)+" is facing a shortage of " + ', '.join([i.type for i in centre.def_crops.all()])+" \\n Your potential buyers are : Buyer23 contact : 9867543421 \\n Buyer56 contact :9876540981"
        for num in farmers:
            send_sms(num, message)
            print(num, message)
        return Response(message)
    # obj = BidSerializer(bid)

    # return Response(obj.data)




####################################### Delivery Views ######################################



class CreateDeliveryRequest(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class CreateDeliveryService(generics.ListCreateAPIView):
    queryset = DeliveryService.objects.all()
    serializer_class = DeliveryServiceSerializer



"""
@api_view(['post'])
def createTempDeliveryTransaction(req):
    print(req.data)
    del_ord = Delivery.objects.get(id=req.data['del_id'])
    print("adarsh")
    del_serv = DeliveryService.objects.get(id=req.data['del_serv_id'])
    print("adarsh")
    cost = req.data['cost']
    print("adarsh")

    #send sms to farmer  Senedrnum = Farmernum
    if del_ord.type == 'SD':
        sender_num = del_ord.order_storage.farmer.contact
        receiver_num = del_ord.order_storage.warehouse.owner.contact
        print(sender_num, receiver_num)
    else:
        sender_num = del_ord.order_sale.seller.contact
        reciever_num = del_ord.order_sale.buyer.contact
        print(sender_num, reciever_num)
    
    obj = TempDeliveryTransaction.objects.create(delivery_ord=del_ord, delivery_service=del_serv,cost =cost)
    res = TempDeliveryTransationSerializer(obj).data
    return Response(res)

"""



def get_distance(loc1, loc2):
    return ((loc1.xloc-loc2.xloc)**2 + (loc1.yloc-loc2.yloc)**2)**0.5


@api_view(['POST'])
def get_delivery_list(req):
    choice = req.data['choice']
    dest = req.data['destinationId']
    farmerContact = req.data['farmerContact']
    print(choice, dest)
    if choice == 'TD':
        src = req.user
        print(src)
        dest = User.objects.get(contact=farmerContact)#farmer
        dest_loc = dest.farms.all()[0].location
        src_loc = src.location
        req.data['destinationId'] = dest.id
    else:
        src = req.user#farnmer
        dest = Warehouse.objects.get(id = int(dest))
        src_loc = src.farms.all()[0].location
        dest_loc = dest.location
    dist = get_distance(src_loc, dest_loc)

    delv_serv = DeliveryService.objects.all()
    print(delv_serv)
    res = []
    for i in delv_serv:
        res.append({
            "deliveryServiceId":i.id,
            "deliveryServiceName":i.name,
            "owner":i.owner.name,
            "basePrice":i.base_price,
            "totalPrice":i.base_price*dist,

        })
    
    res.sort(key = lambda i:i['totalPrice'])
    print({"deliveryServiceList":res, "choice":choice, "destinationId":req.data['destinationId']})
    return Response({"deliveryServiceList":res, "choice":choice, "destinationId":req.data['destinationId']})

@api_view(['POST'])
def request_delivery(req):
    print(req.data)
    choice = req.data['choice']
    src = req.user
    dest = req.data['destinationId']
    cost = float(req.data['cost'])
    del_id = int(req.data['serviceId'])
    del_srv = DeliveryService.objects.get(id = del_id)
    print(choice, src, dest)
    if choice == 'TD':
        
        dest = User.objects.get(id = int(dest))
        deliv = Delivery.objects.create(type = choice, cost = cost, delivery_service = del_srv, source_farmer = dest, destination_buyer = src)
        deliv.save()
        print("success")
    else:
        dest = Warehouse.objects.get(id = int(dest))
        deliv = Delivery.objects.create(type = choice, cost = cost, delivery_service = del_srv, source_farmer = src, destination_warehouse = dest)
        deliv.save()
        print("success")
    return Response({"message":"successful", "choice":choice})

    







@api_view(['get'])
def lockDelivery(req, id):
    temp = Delivery.objects.get(id = id)
    temp.locked = True
    temp.save()    
    print("Your delivery prposal has been approb=ved", temp.delivery_service.owner.contact)
    return Response("Delivery Locked")





@api_view(['get'])
def getNonLockedDelivery(req, id):
    del_serv = DeliveryService.objects.get(id = id)
    queryset = Delivery.objects.filter(locked = False, delivery_service = del_serv)
    res = DeliverySerializer(queryset, many = True).data
    return Response(res)



@api_view(['get'])
def getLockedDelivery(req, id):
    del_serv = DeliveryService.objects.get(id = id)
    queryset = Delivery.objects.filter(locked = True, delivery_service = del_serv)
    res = DeliverySerializer(queryset, many = True).data
    return Response(res)


@api_view(['get'])
def getWarehouseFromOwner(req, id):
    user = User.objects.get(id=id)
    query = Warehouse.objects.filter(owner = user)
    res = WarehouseDetailSerializer(query, many=True).data
    return Response(res)




class CreateNotification(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

@api_view(['get'])
def getNotification(req):
    user = req.user
    if 'timestamp' in req.data:
        tm = req.data['timestamp']
        query = Notification.objects.filter(timestamp__gte=str(tm))
    else:
        query = Notification.objects.all().order_by("-timestamp")
       
    
    res = NotificationSerializer(query, many = True).data
    return Response(res)





"""
@api_view(['get'])
def lockDelivery(req, id):
    obj = Delivery.objects.get(id = id)
    obj.locked = True
    obj.save()
"""




"""

@api_view(['post'])
def createDeliveryRequest(request):
    delivery_service = request.data['delivery_service']
    type = request.data['type']
    order_storage = request.data['order_storage']
    order_sale = request.data['order_sale']
    obj = Delivery.objects.create(delivery_service=delivery_service, 
                                  type = type,
                                  order_storage = order_storage,
                                  order_sale = order_sale)
    res = DeliverySerializer(obj).data
    return Response(res)



@api_view(['post'])
def createDeliveryService(request):
    loc = request.data['loc']
    name = request.data['name']
    branches = request.data['branches']
    obj = Delivery.objects.create(loc = loc,
                                  name = name,
                                  branches = branches)
    res = DeliveryServiceSerializer(obj).data
    return Response(res)

"""




def delivery_admin(request, pk):
    return TemplateResponse(request, 'mytemplate.html', dict({"pk":pk}))

@api_view(["POST"])
def update_detail(req, pk):
    obj = OrderDetails.objects.get(pk = pk)
    obj.verified = 1 if req.data['verified']=='1' else 0
    obj.in_transit = True if req.data['in_transit']=='1' else False
    obj.delivered = True if req.data['delivered']=='1' else False
    obj.reached = True if req.data['reached']=='1' else False

    obj.save()
    if obj.reached:
        otp = random.randint(1001, 9999)
        obj.otp = otp
        obj.save()
        send_sms("7024901272", "OTP is" + str(otp))
        return TemplateResponse(req, 'otp_delv.html', dict({"pk":pk}))
    else:
        return TemplateResponse(req, 'success.html', dict({"pk":pk}))


@api_view(["POST"])
def match_otp(req, pk):
    obj = OrderDetails.objects.get(pk = pk)
    if obj.otp == int(req.data['otp']):
        obj.delivered = True
        obj.save()
        return TemplateResponse(req, 'success.html', dict({"pk":pk}))
    else:
        return TemplateResponse(req, 'failure.html', dict({"pk":pk}))



def enter_otp(req, pk):
    return TemplateResponse(req, 'otp.html', dict({"pk":pk}))

@api_view(["GET"])
def order_details(req, pk):
    tsale = TransactionSale.objects.get(pk = pk)
    obj = tsale.order_details
    print(obj)
    data = OrderDetailsSerializer(obj).data
    print(data)
    return Response(data)

