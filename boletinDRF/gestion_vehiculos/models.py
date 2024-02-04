from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Usuario(AbstractUser):
    es_editor = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='usuarios')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='usuarios')

class Marca(models.Model):
    Nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.Nombre

    class Meta:
        verbose_name_plural = "Marcas"

class vehiculo(models.Model):
    TIPO_VEHICULO = (
        ('Coche', 'Coche'),
        ('Ciclomotor', 'Ciclomotor'),
        ('Motocicleta', 'Motocicleta'),
    )

    COLOR = (
        ('Blanco', 'Blanco'),
        ('Negro', 'Negro'),
        ('Gris', 'Gris'),
    )

    Tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO, null=False)
    Chasis = models.IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(10)
        ]
    )
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=False)
    Modelo = models.CharField(max_length=50, null=False)
    Matricula = models.CharField(max_length=7, null=False, unique=True)
    Color = models.CharField(max_length=10, choices=COLOR, null=False)
    Fecha_Fabricacion = models.DateTimeField(blank=False)
    Fecha_Matriculacion = models.DateTimeField(blank=False)
    Fecha_Baja = models.DateTimeField(null=True, blank=True)
    Suspendido = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.Chasis

    class Meta:
        verbose_name_plural = "Vehiculos"
