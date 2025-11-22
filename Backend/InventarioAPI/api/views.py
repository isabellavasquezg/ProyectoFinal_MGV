# from django.http import JsonResponse
# from django.views import View
# from .models import Equipo, RegistroHistorico,MetrologiaAdmin,MetrologiaTecnica,CondicionesFuncionamiento,DocumentoEquipo,Sede,Servicio,Responsable_Servicios
# import json
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# class Equipos(View): 
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         filtros = {}
#         sede = request.GET.get("sede")
#         if sede:
#             filtros["sede__nombre__icontains"] = sede

#         servicio = request.GET.get("servicio")
#         if servicio:
#             filtros["servicio__nombre__icontains"] = servicio

#         marca = request.GET.get("marca")
#         if marca:
#             filtros["marca__icontains"] = marca

#         modelo = request.GET.get("modelo")
#         if modelo:
#             filtros["modelo__icontains"] = modelo

#         serie = request.GET.get("serie")
#         if serie:
#             filtros["serie__icontains"] = serie

#         estado = request.GET.get("estado")
#         if estado:
#             filtros["estado__icontains"] = estado

#         # Ejecutar filtro dinámico
#         equipos = Equipo.objects.filter(**filtros)

#         # Si no se encontró nada
#         if not equipos.exists():
#             return JsonResponse({"result": []}, status=200)

#         # Convertir queryset en lista JSON
#         data = [
#             {
#                 # Datos de Relaciones
#                 'sede': e.sede.nombre if e.sede else None,                 # Corresponde a <td>{{ eq.sede }}</td>
#                 'servicio': e.servicio.nombre if e.sede else None,         # Corresponde a <td>{{ eq.servicio }}</td>
#                 'responsable': f"{e.responsable.nombre} {e.responsable.apellido}" if e.responsable else None, # ASUMIDO: Necesitas el responsable
                
#                 # Datos del Equipo (Equipo Base)
#                 'nombre_equipo': e.nombre_equipo,      # Corresponde a <td>{{ eq.nombre_equipo }}</td>
#                 'marca': e.marca,                      # Corresponde a <td>{{ eq.marca }}</td>
#                 'modelo': e.modelo,                    # Corresponde a <td>{{ eq.modelo }}</td>
#                 'serie': e.serie,                      # Corresponde a <td>{{ eq.serie }}</td>
#                 'estado': e.estado,                    # Corresponde a <td>{{ eq.estado }}</td>
                
#                 # Campos que faltan en tu consulta inicial, pero están en la tabla
#                 'codigo_inventario': e.codigo_inventario, # Corresponde a <td>{{ eq.codigo_inventario }}</td>
#                 'codigo_ips': e.codigo_ips,              # Corresponde a <td>{{ eq.codigo_ips }}</td>
#                 'codigo_ecri': e.codigo_ecri,            # Corresponde a <td>{{ eq.codigo_ecri }}</td>
#                 'ubicacion_fisica': e.ubicacion_fisica,  # Corresponde a <td>{{ eq.ubicacion_fisica }}</td>
#                 'clasificacion_misional': e.clasificacion_misional, # Corresponde a <td>{{ eq.clasificacion_misional }}</td>
#                 'clasificacion_ips': e.clasificacion_ips,          # Corresponde a <td>{{ eq.clasificacion_ips }}</td>
#                 'clasificacion_riesgo': e.clasificacion_riesgo,    # Corresponde a <td>{{ eq.clasificacion_riesgo }}</td>
#                 'registro_invima': e.registro_invima,
#             }
#             for e in equipos
#         ]

#         return JsonResponse({"result": data}, status=200, safe=False)
# class Registros(View): 
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         filtros = {}
#         sede = request.GET.get("sede")
#         if sede:
#             filtros["sede__nombre__icontains"] = sede

#         servicio = request.GET.get("servicio")
#         if servicio:
#             filtros["servicio__nombre__icontains"] = servicio

#         marca = request.GET.get("marca")
#         if marca:
#             filtros["marca__icontains"] = marca

#         modelo = request.GET.get("modelo")
#         if modelo:
#             filtros["modelo__icontains"] = modelo

#         serie = request.GET.get("serie")
#         if serie:
#             filtros["serie__icontains"] = serie

#         estado = request.GET.get("estado")
#         if estado:
#             filtros["estado__icontains"] = estado

#         # Ejecutar filtro dinámico
#         registros = RegistroHistorico.objects.filter(**filtros)

#         # Si no se encontró nada
#         if not registros.exists():
#             return JsonResponse({"result": []}, status=200)

#         # Convertir queryset en lista JSON
#         data = [
#             {
#                 # Datos de Relaciones (provenientes del modelo 'RegistroHistorico')
#                 # NOTA: La relación 'serie' en RegistroHistorico apunta al modelo Equipo.
#                 'sede': r.sede.nombre if r.sede else None,  
#                 'servicio': r.servicio.nombre if r.servicio else None,
#                 'serie_equipo': r.serie.serie if r.serie else None, # Se renombra a 'serie_equipo' para evitar conflicto con 'serie' (FK)
#                 'tiempo_vida_util': r.tiempo_vida_util,
#                 'fecha_adquisicion': r.fecha_adquisicion.strftime('%Y-%m-%d') if r.fecha_adquisicion else None, # Formatear la fecha
#                 'propietario': r.propietario,
#                 'fecha_fabricacion': r.fecha_fabricacion,

#                 # Información del proveedor
#                 'nit': r.nit,
#                 'proveedor': r.proveedor,

#                 # Garantía
#                 'en_garantia': r.en_garantia, # Será True/False
#                 'fecha_fin_garantia': r.fecha_fin_garantia,

#                 # Información del documento de compra
#                 'forma_adquisicion': r.forma_adquisicion,
#                 'tipo_documento': r.tipo_documento,
#                 'numero_documento': r.numero_documento,
#             }
#             for r in registros
#         ]

#         return JsonResponse({"result": data}, status=200, safe=False)
# class MetrologiaA(View): 
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         filtros = {}
#         sede = request.GET.get("sede")
#         if sede:
#             filtros["sede__nombre__icontains"] = sede

#         servicio = request.GET.get("servicio")
#         if servicio:
#             filtros["servicio__nombre__icontains"] = servicio

#         marca = request.GET.get("marca")
#         if marca:
#             filtros["marca__icontains"] = marca

#         modelo = request.GET.get("modelo")
#         if modelo:
#             filtros["modelo__icontains"] = modelo

#         serie = request.GET.get("serie")
#         if serie:
#             filtros["serie__icontains"] = serie

#         estado = request.GET.get("estado")
#         if estado:
#             filtros["estado__icontains"] = estado

#         # Ejecutar filtro dinámico
#         metrologiasa= MetrologiaAdmin.objects.filter(**filtros)

#         # Si no se encontró nada
#         if not metrologiasa.exists():
#             return JsonResponse({"result": []}, status=200)

#         # Convertir queryset en lista JSON
#         data = [
#             {
#                 # --- 1. DATOS DE RELACIONES (Modelo MetrologiaAdmin) ---
#                 # NOTA: La relación 'serie' en MetrologiaAdmin apunta al modelo Equipo.
#                 'sede': ma.sede.nombre if ma.sede else None,  
#                 'servicio': ma.servicio.nombre if ma.servicio else None,
#                 # Se extrae la serie del Equipo asociado
#                 'serie_equipo': ma.serie.serie if ma.serie else None, 
                
#                 # --- 2. INFORMACIÓN ADMINISTRATIVA DE MANTENIMIENTO Y CALIBRACIÓN (Campos propios de MetrologiaAdmin) ---
#                 'mantenimiento': ma.mantenimiento,
#                 'frecuencia_mantenimiento': ma.frecuencia_mantenimiento,
#                 'calibracion': ma.calibracion,
#                 'frecuencia_calibracion': ma.frecuencia_calibracion,
#             }
#             for ma in metrologiasa
#         ]

#         return JsonResponse({"result": data}, status=200, safe=False)
# class MetrologiaT(View): 
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         filtros = {}
#         sede = request.GET.get("sede")
#         if sede:
#             filtros["sede__nombre__icontains"] = sede

#         servicio = request.GET.get("servicio")
#         if servicio:
#             filtros["servicio__nombre__icontains"] = servicio

#         marca = request.GET.get("marca")
#         if marca:
#             filtros["marca__icontains"] = marca

#         modelo = request.GET.get("modelo")
#         if modelo:
#             filtros["modelo__icontains"] = modelo

#         serie = request.GET.get("serie")
#         if serie:
#             filtros["serie__icontains"] = serie

#         estado = request.GET.get("estado")
#         if estado:
#             filtros["estado__icontains"] = estado

#         # Ejecutar filtro dinámico
#         metrologiast= MetrologiaTecnica.objects.filter(**filtros)

#         # Si no se encontró nada
#         if not metrologiast.exists():
#             return JsonResponse({"result": []}, status=200)

#         # Convertir queryset en lista JSON
#         data = [
#             {
#                 # --- 1. DATOS DE RELACIONES (Modelo MetrologiaTecnica) ---
#                 # NOTA: La relación 'serie' en MetrologiaTecnica apunta al modelo Equipo.
#                 'sede': mt.sede.nombre if mt.sede else None,  
#                 'servicio': mt.servicio.nombre if mt.servicio else None,
#                 # Se extrae la serie del Equipo asociado
#                 'serie_equipo': mt.serie.serie if mt.serie else None, 
                
#                 # --- 2. PARÁMETROS TÉCNICOS PROPIOS DEL EQUIPO (Campos propios de MetrologiaTecnica) ---
#                 'magnitud': mt.magnitud,
#                 'rango_equipo': mt.rango_equipo,
#                 'resolucion': mt.resolucion,
#                 'rango_trabajo': mt.rango_trabajo,
#                 'error_maximo': mt.error_maximo,
#             }
#             for mt in metrologiast
#         ]

#         return JsonResponse({"result": data}, status=200, safe=False)
# class documentos(View): 
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         filtros = {}
#         sede = request.GET.get("sede")
#         if sede:
#             filtros["sede__nombre__icontains"] = sede

#         servicio = request.GET.get("servicio")
#         if servicio:
#             filtros["servicio__nombre__icontains"] = servicio

#         marca = request.GET.get("marca")
#         if marca:
#             filtros["marca__icontains"] = marca

#         modelo = request.GET.get("modelo")
#         if modelo:
#             filtros["modelo__icontains"] = modelo

#         serie = request.GET.get("serie")
#         if serie:
#             filtros["serie__icontains"] = serie

#         estado = request.GET.get("estado")
#         if estado:
#             filtros["estado__icontains"] = estado

#         # Ejecutar filtro dinámico
#         documentos= DocumentoEquipo.objects.filter(**filtros)

#         # Si no se encontró nada
#         if not documentos.exists():
#             return JsonResponse({"result": []}, status=200)

#         # Convertir queryset en lista JSON
#         data = [
#             {
               
#                 # ...
#                 'sede': doc.sede.nombre if doc.sede else None,
#                 'servicio': doc.servicio.nombre if doc.servicio else None,
#                 'serie_equipo': doc.serie.serie if doc.serie else None, 
#                 'hoja_vida': doc.hoja_vida, # Booleano
#                 'registro_importacion': doc.registro_importacion, # Booleano
#                 'manual_operacion': doc.manual_operacion, # Booleano
#                 'manual_mantenimiento': doc.manual_mantenimiento, # String (Manual de Servicio)
#                 'guia_rapida': doc.guia_rapida, # Booleano
#                 'instructivo_manejo': doc.instructivo_manejo, # Booleano
#                 'protocolo_mantenimiento': doc.protocolo_mantenimiento, # Booleano
#                 'frecuencia_metrologica': doc.frecuencia_metrologica, # String
#                 # ...
#             }
            
#             for doc in documentos
#         ]

#         return JsonResponse({"result": data}, status=200, safe=False)
# class condicion(View): 
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     def get(self, request):
#         filtros = {}
#         sede = request.GET.get("sede")
#         if sede:
#             filtros["sede__nombre__icontains"] = sede

#         servicio = request.GET.get("servicio")
#         if servicio:
#             filtros["servicio__nombre__icontains"] = servicio

#         marca = request.GET.get("marca")
#         if marca:
#             filtros["marca__icontains"] = marca

#         modelo = request.GET.get("modelo")
#         if modelo:
#             filtros["modelo__icontains"] = modelo

#         serie = request.GET.get("serie")
#         if serie:
#             filtros["serie__icontains"] = serie

#         estado = request.GET.get("estado")
#         if estado:
#             filtros["estado__icontains"] = estado

#         # Ejecutar filtro dinámico
#         condiciones= CondicionesFuncionamiento.objects.filter(**filtros)

#         # Si no se encontró nada
#         if not condiciones.exists():
#             return JsonResponse({"result": []}, status=200)

#         # Convertir queryset en lista JSON
#         data = [
#             {
#                 # ...
#                 'sede': con.sede.nombre if con.sede else None,
#                 'servicio': con.servicio.nombre if con.servicio else None,
#                 'serie_equipo': con.serie.serie if con.serie else None, 
#                 'voltaje': con.voltaje,
#                 'corriente': con.corriente,
#                 'humedad': con.humedad,
#                 'temperatura': con.temperatura,
#                 'dimensiones': con.dimensiones,
#                 'peso': con.peso,
#                 'otros': con.otros,
#                 # ...
#             }
                        
#             for con in condiciones
#         ]

#         return JsonResponse({"result": data}, status=200, safe=False)