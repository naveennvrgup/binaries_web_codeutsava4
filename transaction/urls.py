from django.urls import include, path
# from rest_framework import routers
# # from .views import UserListView,UserDetailView
# from .views import UserViewSet
#
# router = routers.DefaultRouter()
# router.register('users', UserViewSet)
#
# urlpatterns = [
#     # path("",UserListView.as_view(),name='list'),
#     # path('<int:pk>',UserDetailView.as_view(),name='detail')
#      path("", include(router.urls)),
#      path('auth',include('rest_framework.urls',namespace='rest_framework'))
# ]

from . import views
urlpatterns = [
    path('active_bid/', views.ActiveBidListView.as_view()),
    path('total_bid/', views.TotalBidListView.as_view()),
    path('bid/<int:pk>/', views.BidDetailView.as_view()),
    path('placebid/', views.CreateBidView),
    path('placeOrder/',views.PlaceOrderView),
    path('buyerOrders/',views.BuyerOrdersListView),
    path('farmerOrders/',views.FarmerOrdersListView),
    path('approveOrder/<id>/',views.ApproveFarmerOrderView),
    path('rejectOrder/<id>/',views.RejectFarmerOrderView),
    path('produce/', views.ProduceListView),
    path('storage_transaction/', views.StorageTransactionListView.as_view()),
    path('transaction_sale/', views.TransactionSaleListView),
    path('produce_filter/', views.ProduceListFilter.as_view()),
    path('message/', views.message),
    path('getCenterDetails/<int:pk>', views.GetCenterDetails.as_view()),
    path('report_produce/',views.report_produce),
    path('storagetransaction/',views.createStorageTransaction),
    path('farmerDashboardGraph/',views.farmerDashboardGraphView),
    ###############

    path('createBid/',views.createBid),
    path('pastBidsList/', views.PastBidList),
    path('farmerActiveBidList/', views.FarmerActiveBidList),
    path('farmerPlacedBids/<int:id>/', views.FarmerPlacedbids),
    path('farmerPlaceBid/', views.FarmerPlaceBid),
    path('approveBid/<int:pk>/', views.ApproveBid),
    path('farmerResponseBidList/<int:pk>/',views.FarmerResponseBidList),

    ##############
    path('getFarmerStoredWarehouse/', views.get_farmer_storage_warehouse),
    path('DefCentreView/',views.DefCentreView.as_view()),

    #########################################

    path('getDeliveryServiceList/', views.get_delivery_list),
    path('createDeliveryService/', views.CreateDeliveryService.as_view()),
    path('requestDelivery/', views.request_delivery ),
    path('getNonLockedDelivery/<int:id>', views.getNonLockedDelivery),
    path('getLockedDelivery/<int:id>', views.getLockedDelivery),
    path('lockDelivery/<int:id>', views.lockDelivery),


    ########################################
    path('getWarehouseFromOwner/<int:id>', views.getWarehouseFromOwner),


    #################################################

    path('notifications/', views.getNotification),
    path('createNotification/', views.CreateNotification.as_view())

    
]
