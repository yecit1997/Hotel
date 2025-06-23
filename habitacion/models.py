from django.db import models
import uuid


class Cama(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=50)
    detalle = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.tipo
    
    class Meta:
        verbose_name = 'cama'
        verbose_name_plural = 'camas'
        ordering = ['-tipo']
        
        
class Servicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    detalle = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ['-nombre']
        
    
class Piso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.IntegerField(unique=True) # Va a contener el numero del piso, ejemplo 4
    # habitacion = models.IntegerField(max_length=4, unique=True) # Va a contener el numero de la habitacion, ejemplo 403
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Piso: {self.numero}"
    
    class Meta:
        verbose_name = 'piso'
        verbose_name_plural = 'pisos'
        ordering = ['numero']
    

class Habitacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tamano = models.CharField(max_length=20,)
    piso_hotel = models.ForeignKey(
        Piso,
        on_delete=models.CASCADE,
        related_name='habitaciones_en_piso',
    ) # Aqui debe ir el numero de piso , ejemplo 4
    
    numero_dentro_piso = models.IntegerField()
    servicios = models.ManyToManyField(Servicio, related_name='habitaciones_con_servicio')
    cama = models.ForeignKey(Cama, on_delete=models.SET_NULL, null=True, blank=True, related_name='cama_habitacion')
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    descripcion_adicional = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    @property
    def _descripcion(self):
        servicios_nombres = [servicio.nombre for servicio in self.servicios.all()]
        servicios_str = ", ".join(servicios_nombres)

        full_desc = self.descripcion_adicional if self.descripcion_adicional else ""

        if servicios_str:
            if full_desc:
                full_desc += f". Servicios incluidos: {servicios_str}."
            else:
                full_desc = f"Servicios incluidos: {servicios_str}."
        return full_desc
    
    
    def __str__(self) -> str:
        return f"Habitación {self.piso_hotel.numero}{self.numero_dentro_piso:02d}" \
               f" - {self.tamano} - {'Disponible' if self.disponibilidad else 'No disponible'}"
        # ':02d' formatea el número a dos dígitos, rellenando con cero si es necesario (ej. 1 -> 01)
    
    class Meta:
        verbose_name = 'habitacion'
        verbose_name_plural = 'habitaciones'
        ordering = ['-piso_hotel']
        unique_together = ('piso_hotel', 'numero_dentro_piso')



    