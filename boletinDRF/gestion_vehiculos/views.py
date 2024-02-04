from django.shortcuts import render
from rest_framework import viewsets
from .models import Marca, vehiculo
from .serializers import MarcaSerializer, VehiculoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = vehiculo.objects.all().order_by('Fecha_Matriculacion')
    serializer_class = VehiculoSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def vehiculos_por_marca(self, request):
        nombre_marca = request.query_params.get('Nombre', None)

        try:
            marca = Marca.objects.get(Nombre__iexact=nombre_marca)
            vehiculos = vehiculo.objects.filter(Marca=marca)

            if vehiculos.exists():
                serializer = VehiculoSerializer(vehiculos, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'No hay vehículos asociados a esta marca'}, status=status.HTTP_404_NOT_FOUND)

        except Marca.DoesNotExist:
            return Response({'error': 'La marca no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def list_ordenados_por_fecha(self, request):
        vehiculos_ordenados = vehiculo.objects.all().order_by('Fecha_Matriculacion')
        serializer = VehiculoSerializer(vehiculos_ordenados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def vehiculos_filtrados(self, request):
        nombre_marca = request.query_params.get('Marca', None)
        modelo_param = request.query_params.get('Modelo', None)
        color_param = request.query_params.get('Color', None)

        try:
            marca = Marca.objects.get(Nombre__iexact=nombre_marca)

            # Inicializar las variables modelo y color
            modelo = None
            color = None

            # Verificar si se proporcionaron los parámetros de modelo y color
            if modelo_param:
                try:
                    modelo = vehiculo.objects.get(Modelo__iexact=modelo_param, Marca=marca)
                except vehiculo.DoesNotExist:
                    return Response({'error': 'El modelo no existe'}, status=status.HTTP_404_NOT_FOUND)

            if color_param:
                try:
                    color = vehiculo.objects.get(Color__iexact=color_param, Marca=marca)
                except vehiculo.DoesNotExist:
                    return Response({'error': 'El color no existe'}, status=status.HTTP_404_NOT_FOUND)

            # Filtrar vehículos por marca
            vehiculos = vehiculo.objects.filter(Marca=marca)

            # Filtrar por modelo si se proporcionó
            if modelo:
                vehiculos = vehiculos.filter(Modelo=modelo.Modelo)

            # Filtrar por color si se proporcionó
            if color:
                vehiculos = vehiculos.filter(Color=color.Color)

            if vehiculos.exists():
                serializer = VehiculoSerializer(vehiculos, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'No hay vehículos asociados a esta marca'}, status=status.HTTP_404_NOT_FOUND)

        except Marca.DoesNotExist:
            return Response({'error': 'La marca no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
