from rest_framework import serializers
from .models import Usuario, Rol


# Serializamos los models


class RolSerializer(serializers.ModelSerializer):
    """
    Serializamos el modelo Rol juntamente con todos sus campos
    """

    class Meta:
        model = Rol
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializamos el modelo Usuario juntamente con todos sus campos
    """
    
    '''Mostramos el valor del metodo str del campo rol'''
    rol = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Rol
        fields = [
            "id",
            "dni",
            "username",
            "email",
            "password",
            "first_name",
            "telefono",
            "rol",
            "fecha_creacion",
            "fecha_modificacion",
        ]
