# Generated by Django 5.2.3 on 2025-06-29 04:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0003_delete_reserva'),
        ('habitacion', '0005_remove_habitacion_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_entrada', models.DateField()),
                ('fecha_salida', models.DateField()),
                ('precio_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cantidad_noches', models.IntegerField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('CONFIRMADA', 'Confirmada'), ('CANCELADA', 'Cancelada'), ('COMPLETADA', 'Completada')], default='PENDIENTE', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='cliente.cliente')),
                ('habitacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservas_habitacion', to='habitacion.habitacion')),
            ],
            options={
                'verbose_name': 'reserva',
                'verbose_name_plural': 'reservas',
                'ordering': ['-fecha_entrada', 'estado'],
                'unique_together': {('habitacion', 'fecha_entrada', 'fecha_salida')},
            },
        ),
    ]
