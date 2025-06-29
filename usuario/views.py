from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .serializers import RolSerializer, UsuarioSerializer, UsuarioTokenObtainPairSerializer
from .models import Usuario, Rol


'''
Vistas basadas en clases para Usuario
'''
class RolesView(APIView):
    
    def get(self, request):
        '''
        Consultamos todos los roles
        '''
        roles = Rol.objects.all()
        if not roles:
            return Response({'Error': 'No se encontraron roles'}, status=status.HTTP_204_NO_CONTENT)
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        '''
        Creamos un roles
        '''
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolViewDetail(APIView):
    
    '''
    Consultamos el ID del Rol, si este no existe lanzamos un 404.
    
    Esta misma funcion es la que usaremos en las otras funcionas, ya que en esta contamos con el 
    ID del rol solicitado
    '''
    def get_rol(self, pk):
        try:
            return Rol.objects.get(id=pk)
        except Rol.DoesNotExist:
            raise Http404
    
    
    def get(self, request, pk):
        rol = self.get_rol(pk)
        serializer = RolSerializer(rol)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        rol = self.get_rol(pk)
        serializer = RolSerializer(rol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, pk):
        rol = self.get_rol(pk)
        serializer = RolSerializer(rol, data=request.data, partial=True) # Agregamos partial=True para poder actualizar el modelo parcialmente
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
       rol = self.get_rol(pk)
       rol.delete()
       return Response({'OK': 'Rol eliminado correctamente'}, status=status.HTTP_200_OK)
       

'''
Vistas basadas en clases para Usuario
'''
class UsuariosView(APIView):
    
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


class UsuariosViewDetail(APIView):
    
    def get_usuario(self, pk):
        '''
        Consultamos un usuario por PK para usar esta busqueda en los demas metodos.
        '''
        try:
            return Usuario.objects.get(id=pk)
        except Usuario.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        usuario = self.get_usuario(pk)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        usuario = self.get_usuario(pk)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
    def patch(self, request, pk):
        usuario = self.get_usuario(pk)
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, pk):
        usuario = self.get_usuario(pk)
        usuario.delete()
        return Response({'OK': 'El usuario se elimino correctamente'}, status=status.HTTP_200_OK)
          
    
'''
Creamos el metodo de login
'''

class LoginAPIView(TokenObtainPairView):
    
    serializer_class = UsuarioTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        # Si es válido, obtener la respuesta estándar (tokens)
        response_data = serializer.validated_data

        # Obtener el objeto de usuario (simplejwt lo adjunta al serializador)
        user = serializer.user
        
        # Serializar el objeto de usuario y añadirlo a la respuesta
        user_serializer = UsuarioSerializer(user)
        response_data['user'] = user_serializer.data

        return Response(response_data, status=status.HTTP_200_OK)
        
        


