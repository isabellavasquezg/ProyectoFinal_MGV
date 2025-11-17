from django.db import models

# -----------------------------
# 1. SEDES
# -----------------------------
class Sede(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -----------------------------
# 2. SERVICIOS (vinculados a una sede)
# -----------------------------
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='servicios')

    def __str__(self):
        return f"{self.nombre} - {self.sede.nombre}"


# -----------------------------
# 3. RESPONSABLES
# -----------------------------
class Responsable(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


# -----------------------------
# 4. EQUIPO (INFORMACIÓN GENERAL)
# -----------------------------
class Equipo(models.Model):
    # Relación con sede y servicio
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    responsable = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True)

    # Información general del equipo
    proceso = models.CharField(max_length=200)
    nombre_equipo = models.CharField(max_length=200)
    codigo_inventario = models.CharField(max_length=100)
    codigo_ips = models.CharField(max_length=100, null=True, blank=True)
    codigo_ecri = models.CharField(max_length=100, null=True, blank=True)

    ubicacion_fisica = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=150)

    clasificacion_misional = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_ips = models.CharField(max_length=100, null=True, blank=True)
    clasificacion_riesgo = models.CharField(max_length=100, null=True, blank=True)

    registro_invima = models.CharField(max_length=200, null=True, blank=True)

    # Estado del equipo (activo/inactivo)
    estado = models.CharField(max_length=20, default="activo")  # activo / inactivo
    descripcion_baja = models.TextField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_equipo} - {self.codigo_inventario}"


# -----------------------------
# 5. REGISTRO HISTÓRICO
# -----------------------------
class RegistroHistorico(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, related_name='historico')

    tiempo_vida_util = models.CharField(max_length=50, null=True, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    propietario = models.CharField(max_length=100)
    fecha_fabricacion = models.CharField(max_length=50, null=True, blank=True)
    nit = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=200)

    en_garantia = models.BooleanField(default=False)
    fecha_fin_garantia = models.CharField(max_length=100, null=True, blank=True)

    forma_adquisicion = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=100)

    def __str__(self):
        return f"Histórico - {self.equipo.nombre_equipo}"


# -----------------------------
# 6. INVENTARIO DE DOCUMENTOS
# -----------------------------
class DocumentoEquipo(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, related_name='documentos')

    hoja_vida = models.BooleanField(default=False)
    registro_importacion = models.BooleanField(default=False)
    manual_operacion = models.BooleanField(default=False)
    manual_mantenimiento = models.CharField(max_length=200, null=True, blank=True)
    guia_rapida = models.BooleanField(default=False)
    instructivo_manejo = models.BooleanField(default=False)
    protocolo_mantenimiento = models.BooleanField(default=False)
    frecuencia_metrologica = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Documentos - {self.equipo.nombre_equipo}"


# -----------------------------
# 7. INFORMACIÓN METROLÓGICA ADMINISTRATIVA
# -----------------------------
class MetrologiaAdmin(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, related_name='metrologia_admin')

    mantenimiento = models.BooleanField(default=False)
    frecuencia_mantenimiento = models.IntegerField(default=0)

    calibracion = models.BooleanField(default=False)
    frecuencia_calibracion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Metrología Adm - {self.equipo.nombre_equipo}"


# -----------------------------
# 8. INFORMACIÓN METROLÓGICA TÉCNICA
# -----------------------------
class MetrologiaTecnica(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, related_name='metrologia_tecnica')

    magnitud = models.CharField(max_length=150)
    rango_equipo = models.CharField(max_length=200)
    resolucion = models.CharField(max_length=100, null=True, blank=True)
    rango_trabajo = models.CharField(max_length=200)
    error_maximo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Metrología Técnica - {self.equipo.nombre_equipo}"


# -----------------------------
# 9. CONDICIONES DE FUNCIONAMIENTO
# -----------------------------
class CondicionesFuncionamiento(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, related_name='condiciones')

    voltaje = models.CharField(max_length=50)
    corriente = models.CharField(max_length=50, null=True, blank=True)
    humedad = models.CharField(max_length=50, null=True, blank=True)
    temperatura = models.CharField(max_length=100, null=True, blank=True)

    dimensiones = models.CharField(max_length=200)
    peso = models.CharField(max_length=50)
    otros = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Condiciones - {self.equipo.nombre_equipo}"
