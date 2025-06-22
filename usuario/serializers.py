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
    rol = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), # Importante: Define el queryset para la validación
        allow_null=True,            # Si el campo 'rol' en Usuario puede ser null (como en tu modelo)
        required=False              # Si el campo 'rol' no es obligatorio al crear/actualizar (como en tu modelo)
    )
    nombre_rol = serializers.CharField(source='rol.nombre', read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            "id",
            "dni",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "telefono",
            "rol",
            "nombre_rol",
            "fecha_creacion",
            "fecha_modificacion",
        ]
    
    # extra_kwargs = {
    #         'password': {'write_only': True, 'required': False},
    #         'username': {'required': False},
    #         'email': {'required': False},
    #         'dni': {'required': False},
    #         'fecha_creacion': {'read_only': True},
    #         'fecha_modificacion': {'read_only': True},
    #     }

    def create(self, validated_data):
        '''
        Creamos el metodo CREATE para manejar el password hasheado correctamente al crear/actualizar usuarios.
        '''
        password = validated_data.pop('password', None)
        user = Usuario.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
