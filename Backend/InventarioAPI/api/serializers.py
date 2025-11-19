from rest_framework import serializers
from .models import (
    Sede, Servicio, Responsable, Equipo, RegistroHistorico,
    DocumentoEquipo, MetrologiaAdmin, MetrologiaTecnica, CondicionesFuncionamiento
)

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    sede_nombre = serializers.CharField(source='sede.nombre', read_only=True)
    
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'sede', 'sede_nombre']

class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'

class RegistroHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHistorico
        fields = '__all__'

class DocumentoEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoEquipo
        fields = '__all__'

class MetrologiaAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetrologiaAdmin
        fields = '__all__'

class MetrologiaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetrologiaTecnica
        fields = '__all__'

class CondicionesFuncionamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionesFuncionamiento
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    sede_nombre = serializers.CharField(source='sede.nombre', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.nombre', read_only=True)
    
    # Relaciones anidadas opcionales
    historico = RegistroHistoricoSerializer(read_only=True)
    documentos = DocumentoEquipoSerializer(read_only=True)
    metrologia_admin = MetrologiaAdminSerializer(read_only=True)
    metrologia_tecnica = MetrologiaTecnicaSerializer(read_only=True)
    condiciones = CondicionesFuncionamientoSerializer(read_only=True)
    
    class Meta:
        model = Equipo
        fields = [
            'id', 'proceso', 'nombre_equipo', 'codigo_inventario', 'codigo_ips', 'codigo_ecri',
            'ubicacion_fisica', 'marca', 'modelo', 'serie', 'clasificacion_misional',
            'clasificacion_ips', 'clasificacion_riesgo', 'registro_invima', 'estado',
            'descripcion_baja', 'fecha_baja', 'sede', 'servicio', 'responsable',
            'sede_nombre', 'servicio_nombre', 'responsable_nombre',
            'historico', 'documentos', 'metrologia_admin', 'metrologia_tecnica', 'condiciones'
        ]