from .models import Reserva
from .serializer import ReservaSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
 



# lista y creacion de reservas
class ReservaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Solo visualizar si no esta autenticado
    
# Editar, actualizar y eliminar reservas
class ReservaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated] # Vistas solo para usuarios autenticados
    






