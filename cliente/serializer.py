from rest_framework import serializers
from .models import Cliente
from habitacion.models import Habitacion


# Serializadores auxiliares (pueden estar en otro archivo si prefieres)
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "dni", "nombre", "apellido", "correo", "telefono"]


class HabitacionSerializerForReserva(serializers.ModelSerializer):
    # Aquí solo incluimos los campos necesarios para la reserva, como precio_por_noche
    class Meta:
        model = Habitacion
        fields = [
            "id",
            "precio_por_noche",
        ]  # Necesitas precio_por_noche para el cálculo
        read_only_fields = ["precio_por_noche"]  # No debe ser editable por el cliente


