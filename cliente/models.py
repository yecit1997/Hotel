from django.db import models
import uuid

from habitacion.models import Habitacion


# --- Nuevo Modelo para la lógica de Cliente ---
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dni = models.CharField(
        max_length=20, unique=True, help_text="Número de identificación del cliente"
    )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documentos = models.ImageField(
        upload_to="documentos_clientes/", blank=True, null=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["apellido", "nombre"]  # Ordenar por apellido y luego nombre


# --- Nuevo Modelo para la lógica de Reserva ---
class Reserva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name="reservas",
    )
    
    habitacion = models.ForeignKey(
        Habitacion, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="reservas_habitacion",
    )
    
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()

    # Nuevo: Agrega blank=True y null=True
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 

    # 'cantidad_noches' también debería ser no editable si se calcula.
    cantidad_noches = models.IntegerField(blank=True, null=True) # Permitir null si no se puede calcular inmediatamente

    ESTADO_RESERVA_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA", "Cancelada"),
        ("COMPLETADA", "Completada"),
    ]
    estado = models.CharField(
        max_length=20, choices=ESTADO_RESERVA_CHOICES, default="PENDIENTE"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Asegúrate de que 'cantidad_noches' se calcule aquí
        if self.fecha_entrada and self.fecha_salida:
            self.cantidad_noches = (self.fecha_salida - self.fecha_entrada).days
            if self.cantidad_noches < 0:
                raise ValueError("La fecha de salida no puede ser anterior a la fecha de entrada.")
        else:
            self.cantidad_noches = None # Si fechas no están, cantidad_noches es nulo
                
        # Calcula el precio total solo si la habitación está asignada y cantidad_noches es válida
        if self.habitacion and self.cantidad_noches is not None and self.cantidad_noches >= 0:
            self.precio_total = self.habitacion.precio_por_noche * self.cantidad_noches
        else:
            self.precio_total = None # Si no se puede calcular, el precio total es nulo

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        id_reserva = str(self.id)[:8]
        cliente_info = f"{self.cliente.nombre} {self.cliente.apellido}" if self.cliente else "Cliente desconocido"
        
        habitacion_info = "Hab: Sin asignar"
        if self.habitacion:
            habitacion_info = f"Hab: {self.habitacion.piso_hotel.numero}{self.habitacion.numero_dentro_piso:02d}"

        # Usar self.precio_total directamente del objeto Reserva
        precio_total_info = f"Total: {self.precio_total}" if self.precio_total is not None else "Total: N/A"

        return (
            f"Reserva {id_reserva} - Cliente: {cliente_info} - "
            f"{habitacion_info} - {precio_total_info} - "
            f"Entrada: {self.fecha_entrada} Salida: {self.fecha_salida}"
        )

    class Meta:
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
        ordering = ["-fecha_entrada", "estado"]
        unique_together = (('habitacion', 'fecha_entrada', 'fecha_salida'),) # Una habitación no puede estar reservada en las mismas fechas por dos reservas
        



