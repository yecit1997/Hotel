from django.urls import path

from .views import  ReservaListCreateAPIView, ReservaRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('reservas/', ReservaListCreateAPIView.as_view(), name='reservas-list-create'),
    path('reservas/<uuid:pk>/', ReservaRetrieveUpdateDestroyAPIView.as_view(), name='reservas-detail'),
]
