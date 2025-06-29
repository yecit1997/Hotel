from rest_framework.views import APIView

# from django.http import Http404

from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import NotFound 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
 
from .models import Cliente
from .serializer import ClienteSerializer



class ClienteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly] # Personal autenticado puede enviar informacion, sino esta autenticado solo puede ver
    
    def get(self, request):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClienteViewDetail(APIView):
    
    permission_classes = [IsAuthenticated] # Solo personal autenticado puede manipular los clientes
    
    def get_objet(self, pk):
        try:
            return Cliente.objects.get(id=pk)
        except:
            return NotFound("Los datos ingresados para el cliente no son validos")
        
    def get(self, reques, pk):
        cliente = self.get_objet(pk)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        cliente = self.get_objet(pk)
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, pk):
        cliente = self.get_objet(pk)
        serializer = ClienteSerializer(cliente, data=request.data, partial=True) # Agregamos partial=True para poder actualizar el modelo parcialmente
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        cliente = self.get_objet(pk)
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    






