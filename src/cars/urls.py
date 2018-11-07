from django.urls import path, include
from cars.views import (NewCar, ListCars, SingleCar,
                        NewDriver, ListDriver, SingleDriver,
                        NewDrivingRecord, ListDrivingRecord,
                        DrivingRecordUpdate, DrivingRecordDelete)

app_name = 'cars'

urlpatterns = [
    # path('create-new-car/', NewCar, name='new_car'),
    path('create-new-car/', NewCar.as_view(), name='new_car'),
    path('create-new-driver/', NewDriver.as_view(), name='new_driver'),
    path('new-driving-record/', NewDrivingRecord.as_view(), name='new_driving_record'),
    path('car-list/', ListCars.as_view(), name='car_list'),
    # path('driver-list/', ListDriver.as_view(), name='driver_list'),
    path('driving-records-list/', ListDrivingRecord.as_view(), name='drivingrecord_list'),
    path('cars/<int:pk>/', SingleCar.as_view(), name='single_car'),
    path('drivers/<int:pk>/', SingleDriver.as_view(), name='single_driver'),
    path('drivingrecords/<int:pk>/', DrivingRecordUpdate.as_view(), name='update_drivingrecord'),
    path('drivingrecords-delete/<int:pk>/', DrivingRecordDelete.as_view(), name='delete_drivingrecord'),
]
