from django.contrib import admin
from .models import Usuario, Rol

# Register your models here.

admin.site.register(Rol)
admin.site.register(Usuario)
