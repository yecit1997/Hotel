from rest_framework import serializers
from .models import Cliente, Reserva
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


class ReservaSerializer(serializers.ModelSerializer):
    # Para la escritura: permite enviar el UUID del cliente y la habitación
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), required=True
    )
    habitacion = serializers.PrimaryKeyRelatedField(
        queryset=Habitacion.objects.all(),
        required=False,  # Si una reserva puede crearse sin habitación inicialmente
        allow_null=True,  # Debe coincidir con null=True en el modelo
    )

    # Para la lectura: muestra los detalles del cliente y la habitación
    cliente_detalle = ClienteSerializer(source="cliente", read_only=True)
    habitacion_detalle = HabitacionSerializerForReserva(
        source="habitacion", read_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "cliente",
            "cliente_detalle",
            "habitacion",
            "habitacion_detalle",
            "fecha_entrada",
            "fecha_salida",
            "cantidad_noches",
            "precio_total",
            "estado",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        read_only_fields = [
            "id",
            "cantidad_noches",
            "precio_total",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        # 'cantidad_noches' y 'precio_total' son de solo lectura porque los calculamos nosotros.


    # def validate(self, data):
    #     """
    #     Valida que la fecha de salida no sea anterior a la fecha de entrada
    #     y que la habitación no esté ya reservada para esas fechas.
    #     """
    #     fecha_entrada = data.get("fecha_entrada")
    #     fecha_salida = data.get("fecha_salida")
    #     habitacion = data.get(
    #         "habitacion"
    #     )  # Esto será una instancia de Habitacion si es válido

    #     if fecha_entrada and fecha_salida:
    #         if fecha_salida < fecha_entrada:
    #             raise serializers.ValidationError(
    #                 "La fecha de salida no puede ser anterior a la fecha de entrada."
    #             )

    #         # Validación de solapamiento de reservas (lógica más robusta)
    #         if habitacion:
    #             # Comprobar si hay reservas existentes para esta habitación que se solapen
    #             # Excluir la reserva actual si es una actualización (self.instance)
    #             qs = Reserva.objects.filter(
    #                 habitacion=habitacion,
    #                 fecha_entrada__lt=fecha_salida,  # La reserva existente empieza antes de que la nueva termine
    #                 fecha_salida__gt=fecha_entrada,  # Y la reserva existente termina después de que la nueva empiece
    #             )
    #             if self.instance:  # Si estamos actualizando una reserva existente
    #                 qs = qs.exclude(pk=self.instance.pk)

    #             if qs.exists():
    #                 raise serializers.ValidationError(
    #                     "Esta habitación ya está reservada para las fechas seleccionadas."
    #                 )

    #     return data

    def create(self, validated_data):
        # La habitación ya es una instancia de Habitacion validada
        habitacion_instance = validated_data.get("habitacion")
        fecha_entrada = validated_data.get("fecha_entrada")
        fecha_salida = validated_data.get("fecha_salida")

        # Calcular cantidad_noches
        if fecha_entrada and fecha_salida:
            validated_data["cantidad_noches"] = (fecha_salida - fecha_entrada).days
            if validated_data["cantidad_noches"] < 0:
                # Esto ya debería haber sido atrapado por validate(), pero es una seguridad
                raise serializers.ValidationError(
                    "La cantidad de noches no puede ser negativa."
                )
        else:
            validated_data["cantidad_noches"] = None

        # Calcular precio_total
        if (
            habitacion_instance
            and validated_data["cantidad_noches"] is not None
            and validated_data["cantidad_noches"] >= 0
        ):
            validated_data["precio_total"] = (
                habitacion_instance.precio_por_noche * validated_data["cantidad_noches"]
            )
        else:
            validated_data["precio_total"] = (
                None  # Si no se puede calcular, dejarlo nulo
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Similar a create, recalcular en update
        habitacion_instance = validated_data.get(
            "habitacion", instance.habitacion
        )  # Usar nuevo o el existente
        fecha_entrada = validated_data.get("fecha_entrada", instance.fecha_entrada)
        fecha_salida = validated_data.get("fecha_salida", instance.fecha_salida)

        # Recalcular cantidad_noches
        if fecha_entrada and fecha_salida:
            instance.cantidad_noches = (fecha_salida - fecha_entrada).days
            if instance.cantidad_noches < 0:
                raise serializers.ValidationError(
                    "La cantidad de noches no puede ser negativa."
                )
        else:
            instance.cantidad_noches = None

        # Recalcular precio_total
        if (
            habitacion_instance
            and instance.cantidad_noches is not None
            and instance.cantidad_noches >= 0
        ):
            instance.precio_total = (
                habitacion_instance.precio_por_noche * instance.cantidad_noches
            )
        else:
            instance.precio_total = None

        # Llamar al update original de ModelSerializer para guardar el resto de los campos
        return super().update(instance, validated_data)
