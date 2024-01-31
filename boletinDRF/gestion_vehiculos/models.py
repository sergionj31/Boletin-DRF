from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Marcas"
