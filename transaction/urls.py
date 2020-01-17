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
    path('create_transaction_sale/', views.CreateTransactionView),
    path('produce_filter/', views.ProduceListFilter.as_view()),
    path('approveOrder/<int:pk>/', views.ApproveOrder.as_view()),
    path('message/', views.message),
    path('getCenterDetails/<int:pk>', views.GetCenterDetails.as_view())
    path('report_produce/',views.report_produce),
    
]