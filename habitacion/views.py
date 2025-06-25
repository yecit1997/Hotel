from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# from django.http import Http404

from rest_framework.exceptions import NotFound 
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly


from .serializer import CamaSerializer, ServicioSerializer, PisoSerializer, HabitacionSerializer
from .models import Cama, Servicio, Piso, Habitacion


'''
Creamos las vistas para el CRUD de las camas
'''
class CamasView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly] # Cualquiera puede leer, pero solo los usuarios autenticados pueden modificar
    
    def get(self, request):
        camas = Cama.objects.all()
        serializer = CamaSerializer(camas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = CamaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): # raise_exception=True para manejar automaticamente la respuesta 404 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class CamaViewDetail(APIView):
    '''
    Cramos estas vistas con APIView, para practicar y visualizar la manera en la que Django maneja la informacion al gestionar un modelo
    '''
    # queryset = Cama.objects.all()
    # serializer_class = CamaSerializer
    # # Permisos: Solo autenticados pueden ver, actualizar o eliminar
    # permission_classes = [IsAuthenticated] 

    # def retrieve(self, request, *args, **kwargs):
    #     # Puedes sobrescribir retrieve si necesitas lógica personalizada para el detalle
    #     instance = self.get_object() # get_object ya maneja 404 automáticamente
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados
    
    def get_objet(self, pk):
        try:
            return Cama.objects.get(id=pk)
        except Cama.DoesNotExist:
            raise NotFound('Cama no encontrada')
        
        
    def get(self, request, pk):
        cama = self.get_objet(pk)
        serializer = CamaSerializer(cama)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        cama = self.get_objet(pk)
        serializer = CamaSerializer(cama, data=request.data)
        if serializer.is_valid(raise_exception=True): # raise_exception=True para manejar automaticamente la respuesta 404 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, pk):
        cama = self.get_objet(pk)
        serializer = CamaSerializer(cama, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True): # raise_exception=True para manejar automaticamente la respuesta 404 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        cama = self.get_objet(pk)
        cama.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
Creamos las vistas para el CRUD de los servicios
'''
class ServicioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServicioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]


'''
Creamos las vistas para el CRUD de los pisos
'''
class PisoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Piso.objects.all()
    serializer_class = PisoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
class PisoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Piso.objects.all()
    serializer_class = PisoSerializer
    permission_classes = [IsAuthenticated]


'''
Creamos las vistas para el CRUD de las habitaciones
'''

class HabitacionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class HabitacionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer
    permission_classes = [IsAuthenticated]
    
    
    
    