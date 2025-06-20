# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404

from .serializers import RolSerializer, UsuarioSerializer
from .models import Usuario, Rol


class Usuarios(APIView):
    
    def get(self, request):
        '''
        Metodo para obtener todos los usuarios
        '''
        usuarios = Usuario.objects.all()
        if not usuarios:
            return Response({'Error': 'No se encontraron usuarios'}, status=status.HTTP_204_NO_CONTENT)
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        '''
        Metodo para controlar el envio de la informacion del usuario
        '''
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UsuariosDetail(APIView):
    
    def get_usuario(self, pk):
        '''
        Consultamos un usuario por PK
        '''
        try:
            # usuario = get_object_or_404(Usuario, id=pk)
            # return get_object_or_404(Usuario, id=pk)
            return Usuario.objects.get(id=pk)
        except Usuario.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        usuario = self.get_usuario(pk)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    def put_usuario(self, pk):
        '''
        Actualizamos un usuario por PK
        '''
        try:
            usuario = get_object_or_404(Usuario, id=pk)
            
        except Usuario.DoesNotExist:
            raise Http404
        
        
    def delete_usuario(self, pk):
        '''
        Eliminamos un usuario por PK
        '''
        try:
            usuario = get_object_or_404(Usuario, id=pk)
            
        except Usuario.DoesNotExist:
            raise Http404
          
    





