from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Sede, Servicio, Responsable, Equipo, RegistroHistorico,
    DocumentoEquipo, MetrologiaAdmin, MetrologiaTecnica, CondicionesFuncionamiento
)
from .serializers import (
    SedeSerializer, ServicioSerializer, ResponsableSerializer, EquipoSerializer,
    RegistroHistoricoSerializer, DocumentoEquipoSerializer, MetrologiaAdminSerializer,
    MetrologiaTecnicaSerializer, CondicionesFuncionamientoSerializer
)

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.select_related('sede').all()
    serializer_class = ServicioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sede']
    search_fields = ['nombre', 'sede__nombre']

class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.select_related(
        'sede', 'servicio', 'responsable'
    ).prefetch_related(
        'historico', 'documentos', 'metrologia_admin', 
        'metrologia_tecnica', 'condiciones'
    ).all()
    serializer_class = EquipoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sede', 'servicio', 'responsable', 'estado', 'marca', 'modelo']
    search_fields = [
        'nombre_equipo', 'codigo_inventario', 'codigo_ips', 'codigo_ecri',
        'marca', 'modelo', 'serie', 'ubicacion_fisica'
    ]
    ordering_fields = ['nombre_equipo', 'codigo_inventario', 'marca', 'modelo']
    ordering = ['nombre_equipo']

    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """Obtener registro histórico de un equipo específico"""
        equipo = self.get_object()
        if hasattr(equipo, 'historico'):
            serializer = RegistroHistoricoSerializer(equipo.historico)
            return Response(serializer.data)
        return Response({'detail': 'No se encontró registro histórico'}, 
                       status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def documentos(self, request, pk=None):
        """Obtener documentos de un equipo específico"""
        equipo = self.get_object()
        if hasattr(equipo, 'documentos'):
            serializer = DocumentoEquipoSerializer(equipo.documentos)
            return Response(serializer.data)
        return Response({'detail': 'No se encontró documentación'}, 
                       status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def metrologia_admin(self, request, pk=None):
        """Obtener información metrológica administrativa"""
        equipo = self.get_object()
        if hasattr(equipo, 'metrologia_admin'):
            serializer = MetrologiaAdminSerializer(equipo.metrologia_admin)
            return Response(serializer.data)
        return Response({'detail': 'No se encontró información metrológica administrativa'}, 
                       status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def metrologia_tecnica(self, request, pk=None):
        """Obtener información metrológica técnica"""
        equipo = self.get_object()
        if hasattr(equipo, 'metrologia_tecnica'):
            serializer = MetrologiaTecnicaSerializer(equipo.metrologia_tecnica)
            return Response(serializer.data)
        return Response({'detail': 'No se encontró información metrológica técnica'}, 
                       status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def condiciones(self, request, pk=None):
        """Obtener condiciones de funcionamiento"""
        equipo = self.get_object()
        if hasattr(equipo, 'condiciones'):
            serializer = CondicionesFuncionamientoSerializer(equipo.condiciones)
            return Response(serializer.data)
        return Response({'detail': 'No se encontraron condiciones de funcionamiento'}, 
                       status=status.HTTP_404_NOT_FOUND)

class RegistroHistoricoViewSet(viewsets.ModelViewSet):
    queryset = RegistroHistorico.objects.select_related('equipo').all()
    serializer_class = RegistroHistoricoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['equipo', 'propietario', 'en_garantia', 'forma_adquisicion']
    search_fields = ['equipo__nombre_equipo', 'propietario', 'proveedor', 'numero_documento']

class DocumentoEquipoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoEquipo.objects.select_related('equipo').all()
    serializer_class = DocumentoEquipoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'equipo', 'hoja_vida', 'registro_importacion', 'manual_operacion',
        'guia_rapida', 'instructivo_manejo', 'protocolo_mantenimiento'
    ]

class MetrologiaAdminViewSet(viewsets.ModelViewSet):
    queryset = MetrologiaAdmin.objects.select_related('equipo').all()
    serializer_class = MetrologiaAdminSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['equipo', 'mantenimiento', 'calibracion']

class MetrologiaTecnicaViewSet(viewsets.ModelViewSet):
    queryset = MetrologiaTecnica.objects.select_related('equipo').all()
    serializer_class = MetrologiaTecnicaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['equipo']
    search_fields = ['magnitud', 'rango_equipo', 'rango_trabajo']

class CondicionesFuncionamientoViewSet(viewsets.ModelViewSet):
    queryset = CondicionesFuncionamiento.objects.select_related('equipo').all()
    serializer_class = CondicionesFuncionamientoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['equipo']
    search_fields = ['voltaje', 'dimensiones', 'peso']
