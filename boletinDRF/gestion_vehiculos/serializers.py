from rest_framework import serializers
from .models import Marca, vehiculo

class MarcaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Marca
        fields = ['Nombre']

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehiculo
        fields = ['Tipo_vehiculo', 'Chasis', 'Marca', 'Modelo', 'Matricula', 'Color', 'Fecha_Fabricacion', 'Fecha_Matriculacion', 'Fecha_Baja', 'Suspendido']