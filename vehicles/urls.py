from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('vehicle_list', views.vehicle_list, name='vehicle_list'),
    path('vehicle/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicle/update/<str:pk>/', views.vehicle_update, name='vehicle_update'),

    path('driver_list', views.driver_list, name='driver_list'),
    path('driver/add/', views.driver_add, name='driver_add'),
    path('driver/update/<str:pk>/', views.driver_update, name='driver_update'),

    path('trip_create', views.trip_create, name='trip_create'),
    path("select2/", include("django_select2.urls")),
    
    path('api/get_driver_details/<str:driver_id>/', views.get_driver_details, name='get_driver_details'),
    path('api/get_vehicle_details/<str:vehicle_number>/', views.get_vehicle_details, name='get_vehicle_details'),
]