# Generated by Django 4.1.13 on 2024-02-04 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vehiculos', '0002_alter_vehiculo_fecha_baja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='Fecha_Baja',
            field=models.DateTimeField(),
        ),
    ]
