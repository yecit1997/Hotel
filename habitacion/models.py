from django.db import models
import uuid

# Create your models here.


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