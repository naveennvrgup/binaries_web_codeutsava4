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
    path('placebid/', views.PlaceBidListView.as_view()),
    path('produce/', views.ProduceListView.as_view()),
    path('storage_transaction/', views.StorageTransactionListView.as_view()),
    path('transaction_sale/', views.TransactionSaleListView.as_view()),
    
    
    

]