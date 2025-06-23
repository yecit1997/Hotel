from rest_framework import serializers
from .models import Habitacion, Cama, Servicio, Piso

# Asegúrate de que estos serializadores auxiliares existan para la lectura
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'detalle']

class CamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cama
        fields = ['id', 'tipo', 'detalle']

class PisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piso
        fields = ['id', 'numero']


class HabitacionSerializer(serializers.ModelSerializer):
    # Campo para ESCRIBIR los servicios (lista de UUIDs)
    servicios = serializers.PrimaryKeyRelatedField(
        queryset=Servicio.objects.all(),
        many=True,
        required=False
    )

    # Campo de SOLO LECTURA para mostrar los nombres de los servicios en la respuesta GET
    servicios_nombres = serializers.StringRelatedField(source='servicios', many=True, read_only=True)

    # Serializadores para mostrar los detalles de Cama y Piso en la respuesta GET
    cama_detalle = CamaSerializer(source='cama', read_only=True)
    piso_hotel_detalle = PisoSerializer(source='piso_hotel', read_only=True)
    
    # Campos para la escritura de Cama y Piso (requeridos si no son null=True, blank=True en el modelo)
    cama = serializers.PrimaryKeyRelatedField(queryset=Cama.objects.all(), required=False, allow_null=True)
    piso_hotel = serializers.PrimaryKeyRelatedField(queryset=Piso.objects.all())
    
    descripcion = serializers.CharField(source='descripcion_adicional', required=False, allow_blank=True) # Para escritura
    # Luego, un campo read_only para la descripción completa:
    full_descripcion = serializers.CharField(source='descripcion', read_only=True) # Usa el @property del modelo

    class Meta:
        model = Habitacion
        fields = [
            'id', 
            'tamano', 
            'piso_hotel',           
            'piso_hotel_detalle',   
            'numero_dentro_piso', 
            'servicios',            
            'servicios_nombres',    
            'cama',                 
            'cama_detalle',         
            'precio_por_noche', 
            'disponibilidad', 
            'descripcion',          # Incluimos 'descripcion' aquí para que el usuario pueda enviarla
            'full_descripcion',
            'fecha_creacion',
            'fecha_modificacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
        
        extra_kwargs = {
            # 'tamano': {'required': T},
            # 'precio_por_noche': {'required': False},
            'descripcion': {'required': False}, # Asegúrate que sea opcional para que no lo pida siempre
        }

     # No necesitas modificar create/update para la descripción, solo para los servicios
    def create(self, validated_data):
        servicios_data = validated_data.pop('servicios', [])
        habitacion = Habitacion.objects.create(**validated_data)
        habitacion.servicios.set(servicios_data)
        return habitacion

    def update(self, instance, validated_data):
        servicios_data = validated_data.pop('servicios', None)
        # ... actualizar otros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if servicios_data is not None:
            instance.servicios.set(servicios_data)
        return instance
    
    
    
    