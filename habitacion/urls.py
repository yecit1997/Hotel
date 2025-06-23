from django.urls import path

from .views import (    
        CamasView, CamaViewDetail, 
        ServicioListCreateAPIView, ServicioRetrieveUpdateDestroyAPIView,
        PisoListCreateAPIView, PisoRetrieveUpdateDestroyAPIView,
        HabitacionListCreateAPIView, HabitacionRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('camas/', CamasView.as_view(), name='camas-list-create'),
    path('camas/<uuid:pk>/', CamaViewDetail.as_view(), name='camas-detail'),
    
    path('servicios/', ServicioListCreateAPIView.as_view(), name='servicio-list-create'),
    path('servicios/<uuid:pk>/', ServicioRetrieveUpdateDestroyAPIView.as_view(), name='servicio-detail'),
    
    path('pisos/', PisoListCreateAPIView.as_view(), name='pisos-list-create'),
    path('pisos/<uuid:pk>/', PisoRetrieveUpdateDestroyAPIView.as_view(), name='pisos-detail'),
    
    path('habitaciones/', HabitacionListCreateAPIView.as_view(), name='habitaciones-list-create'),
    path('habitaciones/<uuid:pk>/', HabitacionRetrieveUpdateDestroyAPIView.as_view(), name='habitaciones-detail'),

]
