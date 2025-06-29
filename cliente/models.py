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


