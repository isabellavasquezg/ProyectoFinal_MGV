# api/models.py
from django.db import models

class Usuario(models.Model):
    """Modelo para usuarios del sistema basado en tabla api_usuario"""
    nombreusuario = models.CharField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('viewer', 'Viewer')])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'api_usuario'
    
    def __str__(self):
        return f"{self.nombreusuario} ({self.rol})"

class Equipo(models.Model):
    """Modelo para equipos basado en tabla api_equipo"""
    proceso = models.CharField(max_length=100)
    nombre_equipo = models.TextField()
    codigo_interno = models.CharField(max_length=40, blank=True, null=True)
    codigo_ips = models.CharField(max_length=15, blank=True, null=True)
    codigo_ecri = models.CharField(max_length=15, blank=True, null=True)
    responsable = models.TextField(blank=True, null=True)
    ubicacion = models.TextField(blank=True, null=True)
    marca = models.TextField(blank=True, null=True)
    modelo = models.TextField(blank=True, null=True)
    serie = models.TextField(blank=True, null=True)
    clasificacion_misional = models.TextField(blank=True, null=True)
    clasificacion_ips = models.CharField(max_length=10, blank=True, null=True)
    clasificacion_riesgo = models.CharField(max_length=10, blank=True, null=True)
    registro_invima = models.TextField(blank=True, null=True)
    tiempo_vida_util = models.TextField(blank=True, null=True)
    fecha_adquisicion = models.TextField(blank=True, null=True)
    propietario = models.CharField(max_length=40, blank=True, null=True)
    fecha_fabricacion = models.CharField(max_length=20, blank=True, null=True)
    nit = models.CharField(max_length=30, blank=True, null=True)
    proveedor = models.TextField(blank=True, null=True)
    en_garantia = models.CharField(max_length=20, blank=True, null=True)
    fecha_fin_garantia = models.CharField(max_length=20, blank=True, null=True)
    forma_adquisicion = models.CharField(max_length=30, blank=True, null=True)
    tipo_documento = models.TextField(blank=True, null=True)
    numero_documento = models.CharField(max_length=30, blank=True, null=True)
    hoja_vida = models.CharField(max_length=20, blank=True, null=True)
    registro_importacion = models.TextField(blank=True, null=True)
    manual_operacion = models.CharField(max_length=30, blank=True, null=True)
    manual_mantenimiento = models.TextField(blank=True, null=True)
    guia_rapida = models.CharField(max_length=20, blank=True, null=True)
    instructivo = models.CharField(max_length=30, blank=True, null=True)
    protocolo_mto = models.TextField(blank=True, null=True)
    frecuencia_metrologica = models.CharField(max_length=30, blank=True, null=True)
    mantenimiento = models.CharField(max_length=20, blank=True, null=True)
    frecuencia_mantenimiento = models.CharField(max_length=10, blank=True, null=True)
    calibracion = models.CharField(max_length=20, blank=True, null=True)
    frecuencia_calibracion = models.CharField(max_length=30, blank=True, null=True)
    magnitud = models.TextField(blank=True, null=True)
    rango = models.TextField(blank=True, null=True)
    resolucion = models.TextField(blank=True, null=True)
    rango_trabajo = models.TextField(blank=True, null=True)
    error_maximo = models.TextField(blank=True, null=True)
    voltaje = models.TextField(blank=True, null=True)
    corriente = models.CharField(max_length=100, blank=True, null=True)
    humedad = models.TextField(blank=True, null=True)
    temperatura = models.CharField(max_length=50, blank=True, null=True)
    peso = models.TextField(blank=True, null=True)
    otros = models.TextField(blank=True, null=True)
    sede = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    dimensiones = models.TextField(blank=True, null=True)
    valor_compra = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        db_table = 'api_equipo'
    
    def __str__(self):
        return f"{self.nombre_equipo} - {self.proceso}"

class EdicionEquipo(models.Model):
    """Modelo para historial de ediciones de equipos"""
    fecha = models.DateField()
    justificacion = models.TextField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    responsable_anterior = models.CharField(max_length=100, blank=True, null=True)
    responsable_nuevo = models.CharField(max_length=100, blank=True, null=True)
    sede_anterior = models.CharField(max_length=100, blank=True, null=True)
    sede_nueva = models.CharField(max_length=100, blank=True, null=True)
    servicio_anterior = models.CharField(max_length=100, blank=True, null=True)
    servicio_nuevo = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'api_edicionequipo'

class DesactivacionEquipo(models.Model):
    """Modelo para equipos desactivados"""
    fecha_desactivacion = models.DateField()
    responsable_desactivacion = models.CharField(max_length=100)
    justificacion = models.TextField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'api_desactivacionequipo'

class TrasladoEquipo(models.Model):
    """Modelo para gestionar traslados de equipos"""
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_traslado = models.DateField(blank=True, null=True)
    usuario_solicitante = models.CharField(max_length=100)
    
    # Ubicación origen
    sede_origen = models.CharField(max_length=100, blank=True, null=True)
    ubicacion_origen = models.TextField(blank=True, null=True)
    responsable_origen = models.CharField(max_length=100, blank=True, null=True)
    
    # Ubicación destino
    sede_destino = models.CharField(max_length=100)
    ubicacion_destino = models.TextField(blank=True, null=True)
    responsable_destino = models.CharField(max_length=100, blank=True, null=True)
    
    justificacion = models.TextField()
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('ejecutado', 'Ejecutado'),
        ('rechazado', 'Rechazado')
    ], default='pendiente')
    
    # Campos para aprobación
    fecha_aprobacion = models.DateTimeField(blank=True, null=True)
    aprobado_por = models.CharField(max_length=100, blank=True, null=True)
    observaciones_aprobacion = models.TextField(blank=True, null=True)
    
    # Campos para ejecución
    fecha_ejecucion = models.DateTimeField(blank=True, null=True)
    ejecutado_por = models.CharField(max_length=100, blank=True, null=True)
    observaciones_ejecucion = models.TextField(blank=True, null=True)
    
    # Campos para rechazo
    fecha_rechazo = models.DateTimeField(blank=True, null=True)
    rechazado_por = models.CharField(max_length=100, blank=True, null=True)
    motivo_rechazo = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'api_trasladoequipo'
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"Traslado {self.equipo.nombre_equipo} - {self.estado}"

# Alias para mantener compatibilidad con las vistas
Traslado = TrasladoEquipo