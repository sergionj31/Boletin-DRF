from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Marca, vehiculo
from .serializers import MarcaSerializer, VehiculoSerializer

# Create your views here.


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Marca', 'Modelo', 'Color']
    ordering_fields = ['Fecha_Fabricacion']

    @extend_schema(
        parameters=[
            OpenApiParameter(name='Nombre', description="Nombre de la marca", required=True, type=str)
        ]
    )
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

    @extend_schema(
        parameters=[
            OpenApiParameter(name='Marca', description="Nombre de la marca", required=True, type=str),
            OpenApiParameter(name='Modelo', description="Nombre del modelo", required=False, type=str),
            OpenApiParameter(name='Color', description="Color del vehículo", required=False, type=str),
        ],
        responses={200: VehiculoSerializer(many=True)}
    )
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