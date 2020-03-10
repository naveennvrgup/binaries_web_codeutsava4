from django.contrib import admin
from .models import Produce,StorageTransaction,TransactionSale,Bid,PlaceBid, DeliveryService, TempDeliveryTransaction, Notification
# Register your models here.
#class ProductAdmin(admin.ModelAdmin):
 #   list_display = ('id', 'name', 'venue', 'date','time')
 #   search_fields = ('id', 'name','venue','date', 'time')

#admin.site.register(Prodict, ProductAdmin)


admin.site.register(DeliveryService)
admin.site.register(TempDeliveryTransaction)
admin.site.register(Notification)

class ProduceAdmin(admin.ModelAdmin):
    list_display = ('id','grade', 'date', 'quantity', 'price')
admin.site.register(Produce,ProduceAdmin)

class StorageTransactionAdmin(admin.ModelAdmin):
    list_display = ('transno', 'date', 'quantity', 'cost')
admin.site.register(StorageTransaction,StorageTransactionAdmin)

class TransactionSaleAdmin(admin.ModelAdmin):
    list_display = ('approved', 'quantity', 'price')
admin.site.register(TransactionSale,TransactionSaleAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ( 'transno', 'description', 'deadline')
admin.site.register(Bid,BidAdmin)

class PlaceBidAdmin(admin.ModelAdmin):
    list_display = ( 'price', 'description')
admin.site.register(PlaceBid,PlaceBidAdmin)
