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
                'id_sede': e.sede.id if e.sede else None,
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
    def put_estado(self, request):
        """
        Actualiza el estado de uno o varios equipos a 0 (desactivado).
        Espera un JSON con: {"ids": [1, 5, 8], "estado_equipo": 0}
        """
        try:
            data = json.loads(request.body)
            ids_a_actualizar = data.get('ids', [])
            nuevo_estado = data.get('estado_equipo', 0) # Por defecto, 0 (desactivado)

            if not ids_a_actualizar or not isinstance(ids_a_actualizar, list):
                return JsonResponse({'error': 'Se requiere una lista de IDs de equipos para actualizar.'}, status=400)

            if nuevo_estado not in [0, 1]:
                 return JsonResponse({'error': 'Estado de equipo inválido. Debe ser 0 o 1.'}, status=400)

            # 1. Ejecutar la actualización masiva
            # Esto es más eficiente que hacer un bucle de Equipo.objects.get().save()
            equipos_actualizados = Equipo.objects.filter(id__in=ids_a_actualizar)
            conteo_actualizado = equipos_actualizados.update(estado_equipo=nuevo_estado)

            if conteo_actualizado == 0:
                return JsonResponse({'message': 'Ningún equipo encontrado con los IDs proporcionados. No se realizaron cambios.'}, status=200)

            return JsonResponse({
                'message': f'{conteo_actualizado} equipo(s) actualizados a estado {nuevo_estado} (Desactivado).',
                'updated_count': conteo_actualizado
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido en el cuerpo de la solicitud'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def put(self, request, id_equipo=None):
        """
        """
        if id_equipo is None:
            return JsonResponse({'error': 'Se requiere el ID del equipo para actualizar'}, status=400)

        try:
            # 1. Obtener el equipo a actualizar por su ID
            equipo = Equipo.objects.get(id=id_equipo)
            data = json.loads(request.body)
            
            # Campos a validar y actualizar
            codigo_inventario_nuevo = data.get('codigo_inventario')
            serie_equipo_nuevo = data.get('serie_equipo')

            # 2. **Verificación de Unicidad**
            # Buscamos otros equipos (excluyendo el actual) que ya tengan el nuevo código o serie.
            
            # Q1: ¿Existe otro equipo con el mismo codigo_inventario?
            if codigo_inventario_nuevo:
                if Equipo.objects.exclude(id=id_equipo).filter(codigo_inventario=codigo_inventario_nuevo).exists():
                    return JsonResponse({'error': 'Equipo ya existente: El código de inventario ya está en uso por otro equipo.'}, status=409)

            # Q2: ¿Existe otro equipo con la misma serie_equipo?
            if serie_equipo_nuevo:
                if Equipo.objects.exclude(id=id_equipo).filter(serie_equipo=serie_equipo_nuevo).exists():
                    return JsonResponse({'error': 'Equipo ya existente: El número de serie ya está en uso por otro equipo.'}, status=409)
            
            # 3. Actualizar los campos del equipo
            
            # Ejemplo de actualización de campos. Debes listar todos los campos que pueden ser actualizados.
            if 'sede' in data: 
                equipo.sede = data['sede']
            if 'servicio' in data: 
                equipo.servicio = data['servicio']
            if 'responsable_servicio' in data: 
                equipo.responsable_servicio = data['responsable_servicio']
                
            # 2. Actualizar los campos validados (codigo_inventario y serie_equipo)
            if codigo_inventario_nuevo: 
                equipo.codigo_inventario = codigo_inventario_nuevo
            if serie_equipo_nuevo: 
                equipo.serie_equipo = serie_equipo_nuevo

            # 3. Actualizar Datos del Equipo (Equipo Base)
            if 'nombre_equipo' in data: 
                equipo.nombre_equipo = data['nombre_equipo']
            if 'marca_equipo' in data: 
                equipo.marca_equipo = data['marca_equipo']
            if 'modelo_equipo' in data: 
                equipo.modelo_equipo = data['modelo_equipo']
            if 'estado_equipo' in data: 
                equipo.estado_equipo = data['estado_equipo']
            if 'codigo_ips' in data: 
                equipo.codigo_ips = data['codigo_ips']
            if 'codigo_ecri' in data: 
                equipo.codigo_ecri = data['codigo_ecri']
            if 'ubicacion_fisica' in data: 
                equipo.ubicacion_fisica = data['ubicacion_fisica']
            if 'clasificacion_misional' in data: 
                equipo.clasificacion_misional = data['clasificacion_misional']
            if 'clasificacion_ips' in data: 
                equipo.clasificacion_ips = data['clasificacion_ips']
            if 'clasificacion_riesgo' in data: 
                equipo.clasificacion_riesgo = data['clasificacion_riesgo']
            if 'registro_invima' in data: 
                equipo.registro_invima = data['registro_invima']
            if 'descripcion_baja' in data: 
                equipo.descripcion_baja = data['descripcion_baja']
            if 'fecha_baja_equipo' in data: # Usar el nombre del campo del modelo (e.fecha_baja_equipo)
                equipo.fecha_baja_equipo = data['fecha_baja_equipo']
            
            equipo.save()

            return JsonResponse({'message': f'Equipo con ID {id_equipo} actualizado exitosamente'}, status=200)

        except Equipo.DoesNotExist:
            return JsonResponse({'error': f'Equipo con ID {id_equipo} no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido en el cuerpo de la solicitud'}, status=400)
        except Exception as e:
            # Capturar otros errores como problemas de base de datos o campos faltantes/inválidos
            return JsonResponse({'error': str(e)}, status=500)

    # ---------------------------------------------------------------------
    # --- Nuevo Método POST: Crear Equipo con Verificación de Unicidad ---
    # ---------------------------------------------------------------------
    def post(self, request):
        """
        Crea un nuevo equipo y verifica la unicidad de 
        codigo_inventario y serie_equipo.
        """
        try:
            data = json.loads(request.body)
            
            codigo_inventario_nuevo = data.get('codigo_inventario')
            serie_equipo_nuevo = data.get('serie_equipo')

            # 1. Verificación de Unicidad (Para la creación)
            # No es necesario usar .exclude() aquí, ya que el equipo no existe todavía.
            
            # Verificar codigo_inventario
            if codigo_inventario_nuevo and Equipo.objects.filter(codigo_inventario=codigo_inventario_nuevo).exists():
                return JsonResponse({'error': 'Equipo ya existente: El código de inventario ya está en uso.'}, status=409)

            # Verificar serie_equipo
            if serie_equipo_nuevo and Equipo.objects.filter(serie_equipo=serie_equipo_nuevo).exists():
                return JsonResponse({'error': 'Equipo ya existente: El número de serie ya está en uso.'}, status=409)

            # 2. Creación del equipo
            Equipo.objects.create(
                # --- Campos Directos ---
                nombre_equipo=data.get('nombre_equipo'), 
                marca_equipo=data.get('marca_equipo'), 
                modelo_equipo=data.get('modelo_equipo'),
                # Los campos validados ya están en variables
                codigo_inventario=codigo_inventario_nuevo,
                serie_equipo=serie_equipo_nuevo,
                
                estado_equipo=data.get('estado_equipo'), 
                codigo_ips=data.get('codigo_ips'), 
                codigo_ecri=data.get('codigo_ecri'), 
                ubicacion_fisica=data.get('ubicacion_fisica'), 
                clasificacion_misional=data.get('clasificacion_misional'), 
                clasificacion_ips=data.get('clasificacion_ips'), 
                clasificacion_riesgo=data.get('clasificacion_riesgo'), 
                registro_invima=data.get('registro_invima'),
                descripcion_baja=data.get('descripcion_baja'),
                fecha_baja_equipo=data.get('fecha_baja_equipo'), # Usar el nombre del campo del modelo

                # --- Foreign Keys (Relaciones) ---
                # Usamos la notación '_id' para asignar los IDs numéricos recibidos del cliente.
                # Usamos .get() para que si el campo no viene en el JSON, se asigne None.
                sede_id=data.get('sede'), 
                servicio_id=data.get('servicio'),
                responsable_servicio_id=data.get('responsable_servicio'),
            )

            return JsonResponse({'message': 'Equipo creado exitosamente'}, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except KeyError as e:
            # Esto captura si falta un campo obligatorio en el JSON (ej. 'nombre_equipo')
            return JsonResponse({'error': f'Campo obligatorio faltante: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
# views.py (Añade esta clase)
class EstadoEquipoView(View):
    """
    Vista dedicada para la actualización masiva del estado de los equipos.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def put(self, request):
        # Llama a la lógica de actualización de estado ya existente en EquiposView
        return EquiposView().put_estado(request)
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
    def put(self, request, id_historico=None):
        """
        Actualiza un registro histórico existente.
        Requiere el ID del registro en la URL.
        """
        if id_historico is None:
            return JsonResponse({'error': 'Se requiere el ID del registro histórico para actualizar'}, status=400)

        try:
            registro = RegistroHistorico.objects.get(id=id_historico)
            data = json.loads(request.body)
            
            # 2. Actualizar Campos Propios
            if 'tiempo_vida_util' in data: registro.tiempo_vida_util = data['tiempo_vida_util']
            if 'fecha_adquisicion' in data: registro.fecha_adquisicion = data['fecha_adquisicion'] 
            if 'propietario' in data: registro.propietario = data['propietario']
            if 'fecha_fabricacion' in data: registro.fecha_fabricacion = data['fecha_fabricacion']
            if 'nit' in data: registro.nit = data['nit']
            if 'proveedor' in data: registro.proveedor = data['proveedor']
            if 'en_garantia' in data: registro.en_garantia = data['en_garantia'] 
            if 'fecha_fin_garantia' in data: registro.fecha_fin_garantia = data['fecha_fin_garantia']
            if 'forma_adquisicion' in data: registro.forma_adquisicion = data['forma_adquisicion']
            if 'tipo_documento' in data: registro.tipo_documento = data['tipo_documento']
            if 'numero_documento' in data: registro.numero_documento = data['numero_documento']
            
            registro.save()

            return JsonResponse({'message': f'Registro Histórico con ID {id_historico} actualizado exitosamente'}, status=200)

        except RegistroHistorico.DoesNotExist:
            return JsonResponse({'error': f'Registro Histórico con ID {id_historico} no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido en el cuerpo de la solicitud'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def post(self, request):
        """
        Crea un nuevo registro histórico.
        """
        try:
            data = json.loads(request.body)
            equipo_id = data.get('equipo_id')
            
            if not equipo_id:
                return JsonResponse({'error': 'Campo obligatorio faltante: equipo_id'}, status=400)
                
            # Verificar si el Equipo existe
            try:
                equipo = Equipo.objects.get(id=equipo_id)
            except Equipo.DoesNotExist:
                return JsonResponse({'error': f'Equipo con ID {equipo_id} no encontrado. No se puede crear el registro.'}, status=404)

            # Opcional: Podrías validar unicidad si un Equipo solo debe tener un RegistroHistorico
            # if RegistroHistorico.objects.filter(equipo=equipo).exists():
            #     return JsonResponse({'error': f'El equipo con ID {equipo_id} ya tiene un Registro Histórico asociado.'}, status=409)

            RegistroHistorico.objects.create(
                equipo_id=equipo_id,
                tiempo_vida_util=data.get('tiempo_vida_util'),
                fecha_adquisicion=data.get('fecha_adquisicion'), 
                propietario=data.get('propietario'),
                fecha_fabricacion=data.get('fecha_fabricacion'),
                nit=data.get('nit'),
                proveedor=data.get('proveedor'), 
                en_garantia=data.get('en_garantia', False), # Asignar False por defecto
                fecha_fin_garantia=data.get('fecha_fin_garantia'),
                forma_adquisicion=data.get('forma_adquisicion'),
                tipo_documento=data.get('tipo_documento'),
                numero_documento=data.get('numero_documento'),
            )

            return JsonResponse({'message': 'Registro Histórico creado exitosamente'}, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
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
    def post(self, request):
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")

            if not equipo_id:
                return JsonResponse({'error': 'Campo obligatorio faltante: equipo_id'}, status=400)

            try:
                equipo = Equipo.objects.get(id=equipo_id)
            except Equipo.DoesNotExist:
                return JsonResponse({'error': f'Equipo con ID {equipo_id} no existe'}, status=404)

            MetrologiaAdmin.objects.create(
                equipo_id=equipo_id,
                mantenimiento=data.get("mantenimiento"),
                tipo_mantenimiento=data.get("tipo_mantenimiento"),
                frecuencia_mantenimiento=data.get("frecuencia_mantenimiento"),
                calibracion=data.get("calibracion", False),
                tipo_calibracion=data.get("tipo_calibracion"),
                frecuencia_calibracion=data.get("frecuencia_calibracion"),
            )

            return JsonResponse({'message': 'Metrología Administrativa creada exitosamente'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # ---------------------- ACTUALIZAR ----------------------
    def put(self, request, id_admin=None):

        if id_admin is None:
            return JsonResponse({'error': 'Se requiere ID para actualizar'}, status=400)

        try:
            registro = MetrologiaAdmin.objects.get(id=id_admin)
            data = json.loads(request.body)

            # Campos editables
            if "mantenimiento" in data: registro.mantenimiento = data["mantenimiento"]
            if "tipo_mantenimiento" in data: registro.tipo_mantenimiento = data["tipo_mantenimiento"]
            if "frecuencia_mantenimiento" in data: registro.frecuencia_mantenimiento = data["frecuencia_mantenimiento"]
            if "calibracion" in data: registro.calibracion = data["calibracion"]
            if "tipo_calibracion" in data: registro.tipo_calibracion = data["tipo_calibracion"]
            if "frecuencia_calibracion" in data: registro.frecuencia_calibracion = data["frecuencia_calibracion"]

            registro.save()
            return JsonResponse({'message': f'Metrología Administrativa {id_admin} actualizada'}, status=200)

        except MetrologiaAdmin.DoesNotExist:
            return JsonResponse({'error': 'No existe el registro'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
    def post(self, request):
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")

            if not equipo_id:
                return JsonResponse({'error': 'Campo obligatorio faltante: equipo_id'}, status=400)

            try:
                equipo = Equipo.objects.get(id=equipo_id)
            except Equipo.DoesNotExist:
                return JsonResponse({'error': f'Equipo con ID {equipo_id} no existe'}, status=404)

            MetrologiaTecnica.objects.create(
                equipo_id=equipo_id,
                magnitud=data.get("magnitud"),
                rango_equipo=data.get("rango_equipo"),
                resolucion=data.get("resolucion"),
                rango_trabajo=data.get("rango_trabajo"),
                error_maximo=data.get("error_maximo")
            )

            return JsonResponse({'message': 'Metrología Técnica creada exitosamente'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # ---------------------- ACTUALIZAR ----------------------
    def put(self, request, id_tecnica=None):

        if id_tecnica is None:
            return JsonResponse({'error': 'Se requiere ID para actualizar'}, status=400)

        try:
            registro = MetrologiaTecnica.objects.get(id=id_tecnica)
            data = json.loads(request.body)

            if "magnitud" in data: registro.magnitud = data["magnitud"]
            if "rango_equipo" in data: registro.rango_equipo = data["rango_equipo"]
            if "resolucion" in data: registro.resolucion = data["resolucion"]
            if "rango_trabajo" in data: registro.rango_trabajo = data["rango_trabajo"]
            if "error_maximo" in data: registro.error_maximo = data["error_maximo"]

            registro.save()
            return JsonResponse({'message': f'Metrología Técnica {id_tecnica} actualizada'}, status=200)

        except MetrologiaTecnica.DoesNotExist:
            return JsonResponse({'error': 'Registro no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
    def post(self, request):
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")

            if not equipo_id:
                return JsonResponse({'error': 'Campo obligatorio faltante: equipo_id'}, status=400)

            try:
                equipo = Equipo.objects.get(id=equipo_id)
            except Equipo.DoesNotExist:
                return JsonResponse({'error': f'Equipo con ID {equipo_id} no existe'}, status=404)

            DocumentoEquipo.objects.create(
                equipo_id=equipo_id,
                hoja_vida=data.get("hoja_vida", False),
                registro_importacion=data.get("registro_importacion", False),
                manual_operacion=data.get("manual_operacion"),
                manual_mantenimiento=data.get("manual_mantenimiento"),
                guia_rapida=data.get("guia_rapida"),
                instructivo_manejo=data.get("instructivo_manejo", False),
                protocolo_mantenimiento=data.get("protocolo_mantenimiento"),
                frecuencia_metrologica=data.get("frecuencia_metrologica"),
            )

            return JsonResponse({'message': 'Documento creado'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # ---------------------- ACTUALIZAR ----------------------
    def put(self, request, id_doc=None):

        if id_doc is None:
            return JsonResponse({'error': 'Se requiere ID para actualizar'}, status=400)

        try:
            doc = DocumentoEquipo.objects.get(id=id_doc)
            data = json.loads(request.body)

            for campo in [
                "hoja_vida", "registro_importacion", "manual_operacion",
                "manual_mantenimiento", "guia_rapida", "instructivo_manejo",
                "protocolo_mantenimiento", "frecuencia_metrologica"
            ]:
                if campo in data:
                    setattr(doc, campo, data[campo])

            doc.save()
            return JsonResponse({'message': f'Documento {id_doc} actualizado'}, status=200)

        except DocumentoEquipo.DoesNotExist:
            return JsonResponse({'error': 'Documento no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
    def post(self, request):
        try:
            data = json.loads(request.body)
            equipo_id = data.get("equipo_id")

            if not equipo_id:
                return JsonResponse({'error': 'Campo obligatorio faltante: equipo_id'}, status=400)

            try:
                equipo = Equipo.objects.get(id=equipo_id)
            except Equipo.DoesNotExist:
                return JsonResponse({'error': f'Equipo con ID {equipo_id} no existe'}, status=404)

            CondicionesFuncionamiento.objects.create(
                equipo_id=equipo_id,
                voltaje=data.get("voltaje"),
                corriente=data.get("corriente"),
                humedad=data.get("humedad"),
                temperatura=data.get("temperatura"),
                dimensiones=data.get("dimensiones"),
                peso=data.get("peso"),
                otros=data.get("otros_requerimientos"),
            )

            return JsonResponse({'message': 'Condiciones creadas'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # ---------------------- ACTUALIZAR ----------------------
    def put(self, request, id_cond=None):

        if id_cond is None:
            return JsonResponse({'error': 'Se requiere ID para actualizar'}, status=400)

        try:
            con = CondicionesFuncionamiento.objects.get(id=id_cond)
            data = json.loads(request.body)

            for campo in [
                "voltaje", "corriente", "humedad",
                "temperatura", "dimensiones", "peso", "otros"
            ]:
                if campo in data:
                    setattr(con, campo, data[campo])

            con.save()
            return JsonResponse({'message': f'Condición {id_cond} actualizada'}, status=200)

        except CondicionesFuncionamiento.DoesNotExist:
            return JsonResponse({'error': 'Registro no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class ResponsablesView(View): 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        responsables = Responsable.objects.select_related('sede').all()

        data = [
            {
                'id': resp.id,
                'nombre_responsable': resp.nombre_responsable,   
                'nombre_sede': resp.sede.nombre_sede,
            }
            for resp in responsables
        ]

        return JsonResponse({"result": data}, status=200)


class ServiciosView(View): 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        servicios = Servicio.objects.select_related('sede').all()

        data = [
            {
                'id': serv.id,
                'nombre_servicio': serv.nombre_servicio,  
                'nombre_sede': serv.sede.nombre_sede 
            }
            for serv in servicios
           
        ]

        return JsonResponse({"result": data}, status=200)



class SedeView(View): 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):

        sedes = Sede.objects.all()
        # Si no se encontró ningún equipo
        if not sedes.exists():
            # Devolver una lista vacía con status 200 (OK)
            return JsonResponse({"result": []}, status=200)

        # 3. Serialización de la Data
        data = [
            {
                'id': sed.id,
                'nombre_sede': sed.nombre_sede,   
            }
            for sed in sedes
        ]

        # Devolver la respuesta en formato JSON
        # safe=False si se devuelve un objeto que no es un diccionario (aquí no es necesario, pero es buena práctica si la lista 'data' fuera la respuesta principal)
        return JsonResponse({"result": data}, status=200)       
