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
    path('', views.UserListView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    
    path('rest-auth/', include('rest_auth.urls')), #/login and /logout
    
    path('farms/', views.FarmsListView.as_view()),
    path('farms/<int:pk>/', views.FarmsDetailView.as_view()),

    path('foodgrains/', views.FoodGrainListView.as_view()),
    path('foodgrains/<int:pk>/', views.FoodGrainDetailView.as_view()),

    path('warehouse/', views.WarehouseListView.as_view()),
    path('warehouse/<int:pk>/', views.WarehouseDetailView.as_view()),

    path('location/', views.LocationListView.as_view()),
    

]