from django.db import models

# =============================
# 1. SEDE (Ubicación física principal)
# =============================
class Sede(models.Model):
    nombre_sede = models.CharField(max_length=150, unique=True)
    ubicacion_sede = models.CharField(max_length=250, null=True, blank=True) # Ubicación física de la sede

    class Meta:
        verbose_name_plural = "Sedes"    
    def __str__(self):
        return self.nombre_sede

# =============================
# 1. SERVICIO (Departamento/Área funcional)
# =============================
class Servicio(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, related_name='sede_en_servicio')
    nombre_servicio = models.CharField(max_length=150)
    
    class Meta:
        verbose_name_plural = "Servicios"
        # Restricción: No puede haber dos servicios con el mismo nombre en la misma sede
        unique_together = ('sede', 'nombre_servicio')
        
    def __str__(self):
        return f"{self.nombre_servicio} ({self.sede.nombre_sede})"

class Responsable(models.Model):
    nombre_responsable = models.CharField(max_length=150)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, related_name='sede_en_responsable')
    def __str__(self):
        return self.nombre_responsable
# =============================
# 2. EQUIPO (INFORMACIÓN GENERAL)
# =============================
class Equipo(models.Model):
    # Ubicación actual del equipo
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='sede_en_equipos')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, related_name='servicio_en_equipos')
    responsable_servicio = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, related_name='responsable_en_equipos')

    # Información técnica y administrativa del equipo
    nombre_equipo = models.CharField(max_length=200, null=True, blank=True) 
    codigo_inventario = models.CharField(max_length=100, unique=True) # Generalmente único
    codigo_ips = models.CharField(max_length=100, null=True, blank=True)
    codigo_ecri = models.CharField(max_length=100, null=True, blank=True)
    ubicacion_fisica = models.CharField(max_length=200, null=True, blank=True) 

    # Información técnica del fabricante
    marca_equipo = models.CharField(max_length=100, null=True, blank=True)
    modelo_equipo = models.CharField(max_length=100, null=True, blank=True)
    serie_equipo = models.CharField(max_length=150, unique=True) # La serie debe ser única

    # Clasificaciones según IPS y riesgo biomédico
    clasificacion_misional = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_ips = models.CharField(max_length=100, null=True, blank=True)
    clasificacion_riesgo = models.CharField(max_length=100, null=True, blank=True)
    # Registro sanitario INVIMA (si es equipo médico)
    registro_invima = models.CharField(max_length=200, null=True, blank=True)
    # Estado administrativo
    estado_equipo = models.BooleanField(default=False) # activo / inactivo / de baja
    descripcion_baja = models.TextField(null=True, blank=True) # Motivo de baja si aplica
    fecha_baja_equipo=models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_equipo} - {self.codigo_inventario} (S/N: {self.serie_equipo})"

# =============================
# 3. MANTENIENTOS DE EQUIPOS
# =============================
class Mantenimiento(models.Model):
    equipo=models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name='equipo_en_mantenimiento')
    fecha_mantenimiento = models.DateField()
    tipo_mantenimiento = models.CharField(max_length=150) # Preventivo, Correctivo, etc.
    estado_mantenimiento = models.BooleanField(default=False) # Realizado, Pendiente, Cancelado
    def __str__(self):
        return f"Mantenimiento {self.equipo.serie_equipo} - {self.fecha_mantenimiento}"

# =============================
# 4. TRASLADOS DE EQUIPOS ENTRE SEDES
# =============================
class TrasladoEquipo(models.Model):
    equipo =  models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name='equipo_en_traslado')
    sede_origen = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='sede_en_traslado')
    servicio_origen = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, related_name='servicio_en_traslado')
    fecha_traslado = models.DateField()
    descripcion_traslado = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Traslado {self.equipo.nombre_equipo} de {self.sede_origen} a {self.equipo.sede}"

# =============================
# 5. REGISTRO HISTÓRICO DEL EQUIPO (Información de Adquisición/Proveedor)
# =============================
class RegistroHistorico(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_en_registro') 

    # Información de adquisición y vida útil
    tiempo_vida_util = models.CharField(max_length=50, null=True, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    propietario = models.CharField(max_length=100, null=True, blank=True)
    fecha_fabricacion = models.DateField(null=True, blank=True)

    # Información del proveedor
    nit = models.CharField(max_length=50, null=True, blank=True)
    proveedor = models.CharField(max_length=200, null=True, blank=True)

    # Garantía
    en_garantia = models.BooleanField(default=False)
    fecha_fin_garantia = models.DateField(null=True, blank=True)

    # Información del documento de compra
    forma_adquisicion = models.CharField(max_length=100, null=True, blank=True) 
    tipo_documento = models.CharField(max_length=50, null=True, blank=True)
    numero_documento = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Histórico - {self.equipo.serie_equipo}"

# =============================
# 6. INVENTARIO DE DOCUMENTOS
# =============================
class DocumentoEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_en_documento')  

    # Documentos asociados al equipo
    hoja_vida = models.BooleanField(default=False)
    registro_importacion = models.BooleanField(default=False)
    manual_operacion = models.BooleanField(default=False)
    manual_mantenimiento = models.BooleanField(default=False) 
    guia_rapida = models.BooleanField(default=False)
    instructivo_manejo = models.BooleanField(default=False)
    protocolo_mantenimiento = models.BooleanField(default=False)
    # Frecuencia de calibración o revisión metrológica
    frecuencia_metrologica = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"Documentos - {self.equipo.serie_equipo}"

# =============================
# 7. INFORMACIÓN METROLÓGICA ADMINISTRATIVA
# =============================
class MetrologiaAdmin(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_en_metrologiaA')  
    # Información administrativa de mantenimiento y calibración
    mantenimiento = models.BooleanField(default=False)
    tipo_mantenimiento = models.CharField(max_length=250,null=True, blank=True)
    frecuencia_mantenimiento = models.IntegerField(default=0) # Frecuencia en meses o días
    calibracion = models.BooleanField(default=False)
    tipo_calibracion = models.CharField(max_length=250, null=True, blank=True)
    frecuencia_calibracion = models.IntegerField(default=0)
    def __str__(self):
        return f"Metrología Adm - {self.equipo.serie_equipo}"

# =============================
# 8. INFORMACIÓN METROLÓGICA TÉCNICA
# =============================
class MetrologiaTecnica(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_en_metrologiaT')  

    # Parámetros técnicos propios del equipo medible
    magnitud = models.CharField(max_length=150, null=True)
    rango_equipo = models.CharField(max_length=200, null=True)
    resolucion = models.CharField(max_length=100, null=True, blank=True)
    rango_trabajo = models.CharField(max_length=200, null=True)
    error_maximo = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"Metrología Técnica - {self.equipo.serie_equipo}"

# =============================
# 9. CONDICIONES DE FUNCIONAMIENTO DEL EQUIPO
# =============================
class CondicionesFuncionamiento(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_en_condicion')   

    # Condiciones físicas de operación del equipo
    voltaje = models.CharField(max_length=50)
    corriente = models.CharField(max_length=50, null=True, blank=True)
    humedad = models.CharField(max_length=50, null=True, blank=True)
    temperatura = models.CharField(max_length=100, null=True, blank=True)
    dimensiones = models.CharField(max_length=200, null=True)
    peso = models.CharField(max_length=50, null=True)
    otros = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"Condiciones - {self.equipo.serie_equipo}"
