from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import NotFound 
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
 
from .models import Cliente, Reserva
from .serializer import ClienteSerializer, HabitacionSerializerForReserva, ReservaSerializer





