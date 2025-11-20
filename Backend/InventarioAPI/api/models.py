from django.db import models

# =============================
# 1. SERVICIOS y SEDES
# =============================

class Sede(models.Model):
    # Nombre de la sede (ej: Sede Principal, Laboratorio Norte)
    nombre = models.CharField(max_length=100)

    # Dirección o ubicación física de la sede
    ubicacion = models.CharField(max_length=200)

    # Teléfono de contacto general de la sede
    telefono = models.CharField(max_length=50)

    # Tipo de sede (ej: Hospital, Clínica, Laboratorio, Centro Médico)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    # Servicio pertenece a una sede específica
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='servicios')

    # Nombre del servicio (ej: Radiología, Laboratorio Clínico, Urgencias)
    nombre = models.CharField(max_length=150)

    # Descripción opcional del servicio (espacios, funciones, detalles)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.sede.nombre}"


# =============================
# 2. RESPONSABLES
# =============================

class Responsable_Servicios(models.Model):
    # Datos personales del responsable del servicio/equipo
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    correo_electronico = models.EmailField()
    documento = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    # Cargo del responsable (ej: Ingeniero Biomédico, Técnico, Coordinador)
    cargo = models.CharField(max_length=100)

    # Servicio al que pertenece el responsable
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# =============================
# 3. EQUIPO (INFORMACIÓN GENERAL)
# =============================

class Equipo(models.Model):
    # Relación del equipo con sede y servicio
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='equipos_sede')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)

    # Responsable asignado al equipo
    responsable = models.ForeignKey(Responsable_Servicios, on_delete=models.SET_NULL, null=True)

    # Información técnica y administrativa del equipo
    nombre_equipo = models.CharField(max_length=200)       # Nombre del dispositivo
    codigo_inventario = models.CharField(max_length=100)   # Código interno/inventario
    codigo_ips = models.CharField(max_length=100, null=True, blank=True)  # Código interno de IPS (si aplica)
    codigo_ecri = models.CharField(max_length=100, null=True, blank=True) # Código ECRI (clasificación técnica)
    ubicacion_fisica = models.CharField(max_length=200)    # Lugar exacto donde está el equipo

    # Información técnica del fabricante
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=150)

    # Clasificaciones según IPS y riesgo biomédico
    clasificacion_misional = models.CharField(max_length=200, null=True, blank=True)
    clasificacion_ips = models.CharField(max_length=100, null=True, blank=True)
    clasificacion_riesgo = models.CharField(max_length=100, null=True, blank=True)

    # Registro sanitario INVIMA (si es equipo médico)
    registro_invima = models.CharField(max_length=200, null=True, blank=True)

    # Estado administrativo
    estado = models.CharField(max_length=20, default="activo")  # activo / inactivo / de baja
    descripcion_baja = models.TextField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_equipo} - {self.codigo_inventario}"


# =============================
# 4. REGISTRO HISTÓRICO DEL EQUIPO
# =============================

class RegistroHistorico(models.Model):
    # Relación con sede, servicio y equipo
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='registros_historicos_sede')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)

    # Equipo asociado
    serie = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='registros_historicos', null=True)

    # Información de adquisición y vida útil
    tiempo_vida_util = models.CharField(max_length=50, null=True, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    propietario = models.CharField(max_length=100)
    fecha_fabricacion = models.CharField(max_length=50, null=True, blank=True)

    # Información del proveedor
    nit = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=200)

    # Garantía
    en_garantia = models.BooleanField(default=False)
    fecha_fin_garantia = models.CharField(max_length=100, null=True, blank=True)

    # Información del documento de compra
    forma_adquisicion = models.CharField(max_length=100)  # compra, donación, leasing, etc.
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=100)

    def __str__(self):
        return f"Histórico - {self.serie.nombre_equipo}"


# =============================
# 5. INVENTARIO DE DOCUMENTOS
# =============================

class DocumentoEquipo(models.Model):
    # Relación con sede, servicio y equipo
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='documentos_equipos_sede')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    serie = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='documentos_equipo', null=True)

    # Documentos asociados al equipo
    hoja_vida = models.BooleanField(default=False)
    registro_importacion = models.BooleanField(default=False)
    manual_operacion = models.BooleanField(default=False)
    manual_mantenimiento = models.CharField(max_length=200, null=True, blank=True)
    guia_rapida = models.BooleanField(default=False)
    instructivo_manejo = models.BooleanField(default=False)
    protocolo_mantenimiento = models.BooleanField(default=False)

    # Frecuencia de calibración o revisión metrológica
    frecuencia_metrologica = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Documentos - {self.serie.nombre_equipo}"


# =============================
# 6. INFORMACIÓN METROLÓGICA ADMINISTRATIVA
# =============================

class MetrologiaAdmin(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='metrologia_admin_sede')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    serie = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='metrologia_admin', null=True)

    # Información administrativa de mantenimiento y calibración
    mantenimiento = models.BooleanField(default=False)
    frecuencia_mantenimiento = models.IntegerField(default=0)
    calibracion = models.BooleanField(default=False)
    frecuencia_calibracion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Metrología Adm - {self.serie.nombre_equipo}"


# =============================
# 7. INFORMACIÓN METROLÓGICA TÉCNICA
# =============================

class MetrologiaTecnica(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='metrologia_tecnica_sede')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    serie = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='metrologia_tecnica', null=True)

    # Parámetros técnicos propios del equipo medible
    magnitud = models.CharField(max_length=150, null=True)
    rango_equipo = models.CharField(max_length=200, null=True)
    resolucion = models.CharField(max_length=100, null=True, blank=True)
    rango_trabajo = models.CharField(max_length=200, null=True)
    error_maximo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Metrología Técnica - {self.serie.nombre_equipo}"


# =============================
# 8. CONDICIONES DE FUNCIONAMIENTO DEL EQUIPO
# =============================

class CondicionesFuncionamiento(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, related_name='condiciones_funcionamiento_sede')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    serie = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, related_name='condiciones_funcionamiento')

    # Condiciones físicas de operación del equipo
    voltaje = models.CharField(max_length=50)
    corriente = models.CharField(max_length=50, null=True, blank=True)
    humedad = models.CharField(max_length=50, null=True, blank=True)
    temperatura = models.CharField(max_length=100, null=True, blank=True)
    dimensiones = models.CharField(max_length=200, null=True)
    peso = models.CharField(max_length=50, null=True)
    otros = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Condiciones - {self.serie.nombre_equipo}"
