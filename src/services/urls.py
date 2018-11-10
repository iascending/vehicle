from django.urls import path, include
from services import views

app_name = 'services'

urlpatterns = [
    path('new-service/', views.NewService.as_view(), name='new_service'),
    path('service-list/', views.ServiceList.as_view(), name='service_list'),
    path('new-tyre-service/', views.NewTyreService.as_view(), name='new_tyre_service'),
    path('tyre-service-list/', views.TyreServiceList.as_view(), name='tyre_service_list')
]
