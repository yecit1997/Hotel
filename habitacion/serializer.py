# crud/serializer.py (o donde tengas tus serializadores para Habitacion y Servicio)
from rest_framework import serializers
from .models import Habitacion, Cama, Servicio, Piso

# Asegúrate de tener un Serializer para Servicio si necesitas representarlo completamente
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'detalle'] # O los campos que quieras mostrar

class CamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cama
        fields = ['id', 'tipo']

class PisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piso
        fields = ['id', 'numero']


class HabitacionSerializer(serializers.ModelSerializer):
    # Para la escritura: permite una lista de UUIDs de servicios
    servicios = serializers.PrimaryKeyRelatedField(
        queryset=Servicio.objects.all(),
        many=True,      # ¡Importante! Indica que es una relación de muchos
        required=False  # Si una habitación puede crearse sin servicios iniciales
    )

    # Para la lectura: puedes usar un serializador anidado o StringRelatedField
    # Opción A: Serializador anidado para mostrar detalles completos de los servicios
    # servicios_detalles = ServicioSerializer(source='servicios', many=True, read_only=True)
    
    # Opción B (más simple): StringRelatedField para mostrar solo el nombre de los servicios
    servicios_nombres = serializers.StringRelatedField(source='servicios', many=True, read_only=True)

    # Serializador para cama y piso_hotel si quieres una representación más detallada en la salida
    cama_detalle = CamaSerializer(source='cama', read_only=True)
    piso_hotel_detalle = PisoSerializer(source='piso_hotel', read_only=True)
    
    # Si quieres enviar el UUID de cama y piso_hotel para escritura
    cama = serializers.PrimaryKeyRelatedField(queryset=Cama.objects.all(), required=False, allow_null=True)
    piso_hotel = serializers.PrimaryKeyRelatedField(queryset=Piso.objects.all()) # Generalmente obligatorio

    class Meta:
        model = Habitacion
        fields = [
            'id', 
            'tamano', 
            'piso_hotel',            # Para escritura (UUID del Piso)
            'piso_hotel_detalle',    # Para lectura (detalles del Piso)
            'numero_dentro_piso', 
            'servicios',             # Para escritura (lista de UUIDs de servicios)
            'servicios_nombres',     # Para lectura (lista de nombres de servicios)
            'cama',                  # Para escritura (UUID de la Cama)
            'cama_detalle',          # Para lectura (detalles de la Cama)
            'precio_por_noche', 
            'disponibilidad', 
            'descripcion',
            'fecha_creacion',
            'fecha_modificacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
        
        extra_kwargs = {
            # Puedes añadir extra_kwargs para hacer algunos campos no requeridos en POST/PATCH
            'tamano': {'required': False},
            'precio_por_noche': {'required': False},
            'descripcion': {'required': False},
            # ... otros campos que no sean obligatorios
        }