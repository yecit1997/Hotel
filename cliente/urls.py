from django.urls import path

from .views import (ClienteView, ClienteViewDetail, 
                    ReservaListCreateAPIView, ReservaRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('clientes/', ClienteView.as_view(), name='clientes-list-create'),
    path('clientes/<uuid:pk>/', ClienteViewDetail.as_view(), name='clientes-detail'),
    
    path('reservas/', ReservaListCreateAPIView.as_view(), name='reservas-list-create'),
    path('reservas/<uuid:pk>/', ReservaRetrieveUpdateDestroyAPIView.as_view(), name='reservas-detail'),


]
