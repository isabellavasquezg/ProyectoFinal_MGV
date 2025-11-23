from django.http import JsonResponse
from django.views import View
from .models import Sede, Servicio, Equipo, RegistroHistorico, MetrologiaAdmin, MetrologiaTecnica, DocumentoEquipo, CondicionesFuncionamiento, Mantenimiento, TrasladoEquipo,Responsable,Sede,Servicio
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# ================================================
# VISTA: Equipos (Listado y Filtro por GET)
# ================================================

class EquiposView(View): # Renombrado a EquiposView para claridad

    # Desactiva la protección CSRF para esta clase/método (útil para APIs)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Maneja peticiones GET para listar y filtrar equipos dinámicamente.
        Los parámetros de filtro se esperan en la URL (Query Params).
        """
        filtros = {}

        filtros["estado_equipo"] = 1
        # 1. FILTROS DE RELACIONES (Acceso a través de FK con __nombre)
        # Filtro por Nombre de Sede (Búsqueda parcial, case-insensitive)
        sede = request.GET.get("sede")
        if sede:
            filtros["sede__nombre_sede__icontains"] = sede

        # Filtro por Nombre de Servicio
        servicio = request.GET.get("servicio")
        if servicio:
            filtros["servicio__nombre_servicio__icontains"] = servicio
        
        # Filtro por Número de Serie
        serie = request.GET.get("serie")
        if serie:
            filtros["serie_equipo__icontains"] = serie

        # 2. FILTROS DE PROPIEDADES DIRECTAS (Equipo)
        
        # Filtro por Marca
        marca = request.GET.get("f1")
        if marca:
            filtros["marca_equipo__icontains"] = marca

        # Filtro por Modelo
        modelo = request.GET.get("f2")
        if modelo:
            filtros["modelo_equipo__icontains"] = modelo

        # Filtro por Estado (activo, inactivo, de baja)
        codigo_inventario = request.GET.get("f3")
        if codigo_inventario:
            filtros["codigo_inventario__icontains"] = codigo_inventario

        # Ejecutar filtro dinámico en la base de datos
        # Usa select_related() para optimizar la consulta de las FK (sede y servicio)
        equipos = Equipo.objects.select_related('sede', 'servicio').filter(**filtros)

        # Si no se encontró ningún equipo
        if not equipos.exists():
            # Devolver una lista vacía con status 200 (OK)
            return JsonResponse({"result": []}, status=200)

        # 3. Serialización de la Data
        data = [
            {
                # 3.1. Datos de Relaciones y Responsable
                'id': e.id, # Incluir el ID siempre es útil
                'nombre_sede': e.sede.nombre_sede if e.sede else None, 
                # CORRECCIÓN: Usa e.servicio.nombre si e.servicio existe
                'nombre_servicio': e.servicio.nombre_servicio if e.servicio else None,
                'nombre_responsable': e.responsable_servicio.nombre_responsable if e.responsable_servicio else None, # Campo CharField  
                # 3.2. Datos del Equipo (Equipo Base)
                'nombre_equipo': e.nombre_equipo, 
                'marca_equipo': e.marca_equipo, 
                'modelo_equipo': e.modelo_equipo,
                'serie_equipo': e.serie_equipo, 
                'estado_equipo': e.estado_equipo, 
                'codigo_inventario': e.codigo_inventario, 
                'codigo_ips': e.codigo_ips, 
                'codigo_ecri': e.codigo_ecri, 
                'ubicacion_fisica': e.ubicacion_fisica, 
                'clasificacion_misional': e.clasificacion_misional, 
                'clasificacion_ips': e.clasificacion_ips, 
                'clasificacion_riesgo': e.clasificacion_riesgo, 
                'registro_invima': e.registro_invima,
                'descripcion_baja':e.descripcion_baja,
                'fecha_baja':e.fecha_baja_equipo,
            }
            for e in equipos
        ]

        # Devolver la respuesta en formato JSON
        # safe=False si se devuelve un objeto que no es un diccionario (aquí no es necesario, pero es buena práctica si la lista 'data' fuera la respuesta principal)
        return JsonResponse({"result": data}, status=200)
    
# ================================================
# VISTA: RegistroHistorico (Adquisición, Proveedor)
# ================================================

class RegistroHistoricoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        filtros = {}
        filtros["equipo__estado_equipo"] = 1
        # Filtro por SERIE del Equipo relacionado
        serie = request.GET.get("serie")
        if serie:
            filtros["equipo__serie_equipo__icontains"] = serie 
        
        # Filtro por Nombre de Sede (Búsqueda parcial, case-insensitive)
        sede = request.GET.get("sede")
        if sede:
            filtros["equipo__sede__nombre_sede__icontains"] = sede

        # Filtro por Nombre de Servicio
        servicio = request.GET.get("servicio")
        if servicio:
            filtros["equipo__servicio__nombre_servicio__icontains"] = servicio

        # 2. NUEVOS FILTROS ESPECÍFICOS DE HISTÓRICO (Adquisición/Proveedor)

        # Filtro por PROVEEDOR
        proveedor = request.GET.get("f1")
        if proveedor:
            filtros["proveedor__icontains"] = proveedor

        # Filtro por FORMA DE ADQUISICIÓN (compra, donación, leasing, etc.)
        forma_adquisicion = request.GET.get("f2")
        if forma_adquisicion:
            filtros["forma_adquisicion__icontains"] = forma_adquisicion

        # Filtro por GARANTÍA (Booleano)
        en_garantia = request.GET.get("f3")
        if en_garantia in ('True', 'true', '1'):
            filtros["en_garantia"] = True
        elif en_garantia in ('False', 'false', '0'):
            filtros["en_garantia"] = False

        # Ejecutar filtro dinámico
        # Usamos select_related('equipo') para optimizar el acceso a los datos del equipo
        registros = RegistroHistorico.objects.select_related('equipo').filter(**filtros)

        # Si no se encontró nada
        if not registros.exists():
            return JsonResponse({"result": []}, status=200)

        # Convertir queryset en lista JSON
        data = [
            {
                'id': r.id,
                # Datos del Equipo (obtenidos a través de la relación)
                'serie_equipo': r.equipo.serie_equipo if r.equipo else None,
                'nombre_sede': r.equipo.sede.nombre_sede if r.equipo else None,
                'nombre_servicio':r.equipo.servicio.nombre_servicio if r.equipo else None,
                'estado_equipo':r.equipo.estado_equipo if r.equipo else None,
                
                # Información de adquisición y vida útil
                'tiempo_vida_util': r.tiempo_vida_util,
                'fecha_adquisicion': r.fecha_adquisicion, 
                'propietario': r.propietario,
                'fecha_fabricacion': r.fecha_fabricacion,

                # Información del proveedor
                'nit': r.nit,
                'proveedor': r.proveedor, 

                # Garantía
                'en_garantia': r.en_garantia, 
                'fecha_fin_garantia': r.fecha_fin_garantia,

                # Información del documento de compra
                'forma_adquisicion': r.forma_adquisicion,
                'tipo_documento': r.tipo_documento,
                'numero_documento': r.numero_documento,
            }
            for r in registros
        ]

        # safe=False ya no es necesario aquí porque la respuesta es un diccionario con la clave "result"
        return JsonResponse({"result": data}, status=200)
    
# ================================================
# VISTA: MetrologiaAdmin (Mantenimiento y Calibración)
# ================================================

class MetrologiaAdminView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """
        Maneja peticiones GET para listar y filtrar datos de Metrología Administrativa.
        Los filtros se aplican a través de la relación FK al modelo Equipo.
        """
        filtros = {}
        filtros["equipo__estado_equipo"] = 1
        # Filtro por SERIE del Equipo relacionado
        serie = request.GET.get("serie")
        if serie:
            filtros["equipo__serie_equipo__icontains"] = serie 
        
        # Filtro por Nombre de Sede (Búsqueda parcial, case-insensitive)
        sede = request.GET.get("sede")
        if sede:
            filtros["equipo__sede__nombre_sede__icontains"] = sede

        # Filtro por Nombre de Servicio
        servicio = request.GET.get("servicio")
        if servicio:
            filtros["equipo__servicio__nombre_servicio__icontains"] = servicio
        
        # Filtro por Marca del Equipo
        frecuenciaM = request.GET.get("f1")
        if frecuenciaM:
            # Acceso directo al campo 'marca' del objeto Equipo
            filtros["frecuencia_mantenimiento__icontains"] = frecuenciaM 

        # Filtro por Modelo del Equipo
        frecuenciaC = request.GET.get("f2")
        if frecuenciaC:
            filtros["frecuencia_calibracion__icontains"] = frecuenciaC

        # Filtro por Requisito de Calibración (Booleano)
        calibracion_req = request.GET.get("f3")
        if calibracion_req in ('True', 'true', '1'):
            filtros["calibracion"] = True
        elif calibracion_req in ('False', 'false', '0'):
            filtros["calibracion"] = False
            
        # Ejecutar filtro dinámico
        metrologias = MetrologiaAdmin.objects.select_related('equipo').filter(**filtros)

        # Si no se encontró nada
        if not metrologias.exists():
            return JsonResponse({"result": []}, status=200)

        # Convertir queryset en lista JSON
        data = [
            {
                'id': ma.id,
                # --- 1. DATOS DEL EQUIPO RELACIONADO ---
                'serie_equipo': ma.equipo.serie_equipo if ma.equipo else None,
                'nombre_sede': ma.equipo.sede.nombre_sede if ma.equipo else None,
                'nombre_servicio':ma.equipo.servicio.nombre_servicio if ma.equipo else None,
                'estado_equipo':ma.equipo.estado_equipo if ma.equipo else None,
                
                # --- 2. INFORMACIÓN ADMINISTRATIVA ---
                'mantenimiento_requerido': ma.mantenimiento,
                'tipo_mantenimiento':ma.tipo_mantenimiento,
                'frecuencia_mantenimiento': ma.frecuencia_mantenimiento,
                'calibracion_requerida': ma.calibracion,
                'tipo_calibracion':ma.tipo_calibracion,
                'frecuencia_calibracion': ma.frecuencia_calibracion,
            }
            for ma in metrologias
        ]

        return JsonResponse({"result": data}, status=200)

# ================================================
# VISTA: MetrologiaTecnica (Parámetros Técnicos)
# ================================================

class MetrologiaTecnicaView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """
        Maneja peticiones GET para listar y filtrar datos de Metrología Técnica.
        Los filtros se aplican a través de la relación FK al modelo Equipo.
        """
        filtros = {}
        filtros["equipo__estado_equipo"] = 1
        # Filtro por SERIE del Equipo relacionado
        serie = request.GET.get("serie")
        if serie:
            filtros["equipo__serie_equipo__icontains"] = serie 
        
        # Filtro por Nombre de Sede (Búsqueda parcial, case-insensitive)
        sede = request.GET.get("sede")
        if sede:
            filtros["equipo__sede__nombre_sede__icontains"] = sede

        # Filtro por Nombre de Servicio
        servicio = request.GET.get("servicio")
        if servicio:
            filtros["equipo__servicio__nombre_servicio__icontains"] = servicio
        
        # Filtro por Estado del Equipo
        rangoE = request.GET.get("f2")
        if rangoE:
            filtros["rango_equipo__icontains"] = rangoE

        # 2. FILTROS PROPIOS DE METROLOGIA TÉCNICA
        
        # Filtro por Magnitud de Medida
        magnitud = request.GET.get("f1")
        if magnitud:
            filtros["magnitud__icontains"] = magnitud
        
        # Filtro por Rango de Equipo
        rangoT = request.GET.get("f3")
        if rangoT:
            # Usamos __icontains para buscar valores parciales en el rango (si es un CharField)
            filtros["rango_trabajo__icontains"] = rangoT 
            

        # Ejecutar filtro dinámico
        # Usamos select_related para optimizar la consulta
        metrologias = MetrologiaTecnica.objects.select_related('equipo').filter(**filtros)

        # Si no se encontró nada
        if not metrologias.exists():
            return JsonResponse({"result": []}, status=200)

        # Convertir queryset en lista JSON
        data = [
            {
                'id': mt.id,
                 # --- 1. DATOS DEL EQUIPO RELACIONADO ---
                'serie_equipo': mt.equipo.serie_equipo if mt.equipo else None,
                'nombre_sede': mt.equipo.sede.nombre_sede if mt.equipo else None,
                'nombre_servicio':mt.equipo.servicio.nombre_servicio if mt.equipo else None,
                'estado_equipo':mt.equipo.estado_equipo if mt.equipo else None,
                
                # --- 2. INFORMACIÓN TÉCNICA DE METROLOGÍA ---
                'magnitud': mt.magnitud,
                'rango_equipo': mt.rango_equipo,
                'resolucion': mt.resolucion,
                'rango_trabajo': mt.rango_trabajo,
                'error_maximo': mt.error_maximo,
            }
            for mt in metrologias
        ]

        return JsonResponse({"result": data}, status=200)

# ================================================
# VISTA: DocumentoEquipo (Documentos y Manuales)
# ================================================

class DocumentoEquipoView(View): # Renombrado a DocumentoEquipoView
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """
        Maneja peticiones GET para listar y filtrar documentos asociados a equipos.
        Los filtros de ubicación y propiedades del equipo se aplican a través de 'equipo__'.
        """
        filtros = {}
        filtros["equipo__estado_equipo"] = 1
        # Filtro por SERIE del Equipo relacionado
        serie = request.GET.get("serie")
        if serie:
            filtros["equipo__serie_equipo__icontains"] = serie 
        
        # Filtro por Nombre de Sede (Búsqueda parcial, case-insensitive)
        sede = request.GET.get("sede")
        if sede:
            filtros["equipo__sede__nombre_sede__icontains"] = sede

        # Filtro por Nombre de Servicio
        servicio = request.GET.get("servicio")
        if servicio:
            filtros["equipo__servicio__nombre_servicio__icontains"] = servicio
          
        # 2. FILTROS PROPIOS DE DOCUMENTO EQUIPO
        
        # Filtro por si tiene Hoja de Vida (Booleano)
        hoja_vida = request.GET.get("f1")
        if hoja_vida in ('True', 'true', '1'):
            filtros["hoja_vida"] = True
        elif hoja_vida in ('False', 'false', '0'):
            filtros["hoja_vida"] = False

        registro_importacion = request.GET.get("f2")
        if registro_importacion in ('True', 'true', '1'):
            filtros["registro_importacion"] = True
        elif registro_importacion in ('False', 'false', '0'):
            filtros["registro_importacion"] = False
        
        instructivo_manejo = request.GET.get("f3")
        if instructivo_manejo in ('True', 'true', '1'):
            filtros["instructivo_manejo"] = True
        elif instructivo_manejo in ('False', 'false', '0'):
            filtros["instructivo_manejo"] = False

        # Ejecutar filtro dinámico
        # Optimización: Cargar Equipo, Sede y Servicio en una sola consulta
        documentos = DocumentoEquipo.objects.select_related('equipo').filter(**filtros)

        # Si no se encontró nada
        if not documentos.exists():
            return JsonResponse({"result": []}, status=200)

        # Convertir queryset en lista JSON
        data = [
            {
                'id': doc.id,
                # --- 1. DATOS DEL EQUIPO RELACIONADO ---
                'serie_equipo': doc.equipo.serie_equipo if doc.equipo else None,
                'nombre_sede': doc.equipo.sede.nombre_sede if doc.equipo else None,
                'nombre_servicio':doc.equipo.servicio.nombre_servicio if doc.equipo else None,
                'estado_equipo':doc.equipo.estado_equipo if doc.equipo else None,
                
                # --- 2. DOCUMENTACIÓN DISPONIBLE (Propios de DocumentoEquipo) ---
                'hoja_vida': doc.hoja_vida, 
                'registro_importacion': doc.registro_importacion, 
                'manual_operacion': doc.manual_operacion, 
                'manual_mantenimiento': doc.manual_mantenimiento, # String (Manual de Servicio)
                'guia_rapida': doc.guia_rapida, 
                'instructivo_manejo': doc.instructivo_manejo, 
                'protocolo_mantenimiento': doc.protocolo_mantenimiento,
                'frecuencia_metrologica': doc.frecuencia_metrologica, 
            }
            for doc in documentos
        ]

        return JsonResponse({"result": data}, status=200)

# ================================================
# VISTA: CondicionesFuncionamiento (Requisitos Ambientales/Eléctricos)
# ================================================

class CondicionesFuncionamientoView(View): # Renombrado a CondicionesFuncionamientoView
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """
        Maneja peticiones GET para listar y filtrar los requisitos de funcionamiento de los equipos.
        """
        filtros = {}
        filtros["equipo__estado_equipo"] = 1
        # Filtro por SERIE del Equipo relacionado
        serie = request.GET.get("serie")
        if serie:
            filtros["equipo__serie_equipo__icontains"] = serie 
        
        # Filtro por Nombre de Sede (Búsqueda parcial, case-insensitive)
        sede = request.GET.get("sede")
        if sede:
            filtros["equipo__sede__nombre_sede__icontains"] = sede

        # Filtro por Nombre de Servicio
        servicio = request.GET.get("servicio")
        if servicio:
            filtros["equipo__servicio__nombre_servicio__icontains"] = servicio
        
        # 2. FILTROS PROPIOS DE CONDICIONES DE FUNCIONAMIENTO
        
        # Filtro por Voltaje
        voltaje = request.GET.get("f1")
        if voltaje:
            # Filtro exacto o parcial, dependiendo de cómo se guarde el voltaje (ej. "120V")
            filtros["voltaje__icontains"] = voltaje 

        # Filtro por Peso (asumiendo que es un campo de texto/número)
        peso = request.GET.get("f2")
        if peso:
            # Usamos icontains para ser flexibles, pero para números podrías usar __gte, __lte
            filtros["peso__icontains"] = peso 

        # Filtro por Rango de Temperatura
        temperatura = request.GET.get("f3")
        if temperatura:
            filtros["temperatura__icontains"] = temperatura

        # Ejecutar filtro dinámico
        # Optimización: Cargar Equipo, Sede y Servicio en una sola consulta
        condiciones = CondicionesFuncionamiento.objects.select_related('equipo').filter(**filtros)

        # Si no se encontró nada
        if not condiciones.exists():
            return JsonResponse({"result": []}, status=200)

        # Convertir queryset en lista JSON
        data = [
            {
                'id': con.id,
                # --- 1. DATOS DEL EQUIPO RELACIONADO ---
                'serie_equipo': con.equipo.serie_equipo if con.equipo else None,
                'nombre_sede': con.equipo.sede.nombre_sede if con.equipo else None,
                'nombre_servicio':con.equipo.servicio.nombre_servicio if con.equipo else None,
                'estado_equipo':con.equipo.estado_equipo if con.equipo else None,
                
                # --- 2. REQUISITOS DE FUNCIONAMIENTO ---
                'voltaje': con.voltaje,
                'corriente': con.corriente,
                'humedad': con.humedad,
                'temperatura': con.temperatura,
                'dimensiones': con.dimensiones,
                'peso': con.peso,
                'otros_requerimientos': con.otros,
            }
            for con in condiciones
        ]

        return JsonResponse({"result": data}, status=200)
class ResponsablesView(View): 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, codigo_interno=None):
        if codigo_interno:
            try:
                responsable = Responsable.objects.get(codigo_interno=codigo_interno)
                data = {
                    'nombre': responsable.nombre_responsable,
                    'sede': responsable.sede.nombre_sede,
                }
                return JsonResponse(data, status=200)
            except Responsable.DoesNotExist:
                return JsonResponse({'error': 'Laborresponsable no encontrado'}, status=404)
            except Responsable.MultipleObjectsReturned:
                return JsonResponse({'error': 'Múltiples responsables encontrados con el mismo código'}, status=400)
        else:
            responsables=list(Responsable.objects.values('nombre_responsable','sede__nombre_sede'))
            data={'message':'Success','result':responsables}
            return JsonResponse(data, status=200)

class SedeView(View): 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, codigo_interno=None):
        if codigo_interno:
            try:
                sede = Sede.objects.get(codigo_interno=codigo_interno)
                data = {
                    'nombre': sede.nombre_sede,
                    'ubicacion': sede.ubicacion_sede,
                }
                return JsonResponse(data, status=200)
            except Sede.DoesNotExist:
                return JsonResponse({'error': 'Sede no encontrado'}, status=404)
            except Sede.MultipleObjectsReturned:
                return JsonResponse({'error': 'Múltiples responsables encontrados con el mismo código'}, status=400)
        else:
            sedes=list(Sede.objects.values('nombre_sede','ubicacion_sede'))
            data={'message':'Success','result':sedes}
            return JsonResponse(data, status=200)        
