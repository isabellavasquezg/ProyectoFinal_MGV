# api/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django import forms
from django.utils import timezone
from datetime import date
from .models import Usuario, Equipo, DesactivacionEquipo, EdicionEquipo, TrasladoEquipo
from .forms import EquipoForm, TrasladoForm

def login_view(request):
    """Vista para página de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Usuario.objects.get(nombreusuario=username, contraseña=password, activo=True)
            # Guardar sesión
            request.session['user_id'] = user.id
            request.session['username'] = user.nombreusuario
            request.session['rol'] = user.rol
            return redirect('dashboard')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    request.session.flush()
    return redirect('login')

def dashboard_view(request):
    """Vista para dashboard principal con estadísticas"""
    # Verificar si usuario está logueado
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Calcular estadísticas
    total_equipos = Equipo.objects.count()
    equipos_activos = Equipo.objects.filter(activo=True).count()
    equipos_inactivos = Equipo.objects.filter(activo=False).count()
    
    # Estadísticas por sede
    stats_por_sede = Equipo.objects.values('sede').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Estadísticas por proceso
    stats_por_proceso = Equipo.objects.values('proceso').annotate(
        total=Count('id')
    ).order_by('-total')[:5]  # Top 5
    
    # Equipos que requieren mantenimiento
    equipos_mantenimiento = Equipo.objects.filter(
        Q(mantenimiento__icontains='Si') | Q(calibracion__icontains='Si')
    ).count()
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'stats': {
            'total_equipos': total_equipos,
            'equipos_activos': equipos_activos,
            'equipos_inactivos': equipos_inactivos,
            'equipos_mantenimiento': equipos_mantenimiento,
            'por_sede': list(stats_por_sede),
            'por_proceso': list(stats_por_proceso),
        }
    }
    
    return render(request, 'dashboard.html', context)

def equipos_view(request):
    """Vista para tabla de equipos ACTIVOS únicamente"""
    # Verificar si usuario está logueado
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Obtener filtros de la URL (sin filtro de estado)
    proceso_filter = request.GET.get('proceso', '')
    sede_filter = request.GET.get('sede', '')
    search = request.GET.get('search', '')
    
    # Consulta base - SOLO EQUIPOS ACTIVOS
    equipos = Equipo.objects.filter(activo=True)
    
    # Aplicar filtros
    if proceso_filter:
        equipos = equipos.filter(proceso__icontains=proceso_filter)
    if sede_filter:
        equipos = equipos.filter(sede__icontains=sede_filter)
    if search:
        equipos = equipos.filter(
            Q(nombre_equipo__icontains=search) |
            Q(codigo_interno__icontains=search) |
            Q(marca__icontains=search) |
            Q(modelo__icontains=search)
        )
    
    # Obtener listas únicas para filtros (solo de equipos activos)
    procesos = Equipo.objects.filter(activo=True).values_list('proceso', flat=True).distinct()
    sedes = Equipo.objects.filter(activo=True).values_list('sede', flat=True).distinct().exclude(sede__isnull=True)
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'equipos': equipos,
        'filtros': {
            'procesos': procesos,
            'sedes': sedes,
            'proceso_actual': proceso_filter,
            'sede_actual': sede_filter,
            'search_actual': search,
        },
        'total_equipos': equipos.count()
    }
    
    return render(request, 'equipos.html', context)

def equipos_inactivos_view(request):
    """Vista para lista de equipos INACTIVOS con registro de desactivación"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Obtener filtros de la URL
    proceso_filter = request.GET.get('proceso', '')
    sede_filter = request.GET.get('sede', '')
    search = request.GET.get('search', '')
    
    # Consulta base - EQUIPOS INACTIVOS con sus registros de desactivación
    equipos_inactivos = Equipo.objects.filter(activo=False).select_related()
    
    # Obtener registros de desactivación
    registros_desactivacion = DesactivacionEquipo.objects.filter(
        equipo__activo=False
    ).select_related('equipo').order_by('-fecha_desactivacion')
    
    # Aplicar filtros a los registros
    if proceso_filter:
        registros_desactivacion = registros_desactivacion.filter(equipo__proceso__icontains=proceso_filter)
    if sede_filter:
        registros_desactivacion = registros_desactivacion.filter(equipo__sede__icontains=sede_filter)
    if search:
        registros_desactivacion = registros_desactivacion.filter(
            Q(equipo__nombre_equipo__icontains=search) |
            Q(equipo__codigo_interno__icontains=search) |
            Q(equipo__marca__icontains=search) |
            Q(equipo__modelo__icontains=search)
        )
    
    # Obtener listas únicas para filtros (solo de equipos inactivos)
    procesos = Equipo.objects.filter(activo=False).values_list('proceso', flat=True).distinct()
    sedes = Equipo.objects.filter(activo=False).values_list('sede', flat=True).distinct().exclude(sede__isnull=True)
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'registros': registros_desactivacion,
        'filtros': {
            'procesos': procesos,
            'sedes': sedes,
            'proceso_actual': proceso_filter,
            'sede_actual': sede_filter,
            'search_actual': search,
        },
        'total_registros': registros_desactivacion.count()
    }
    
    return render(request, 'equipos_inactivos.html', context)

def desactivar_equipo(request, equipo_id):
    """Vista para desactivar un equipo"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        equipo = Equipo.objects.get(id=equipo_id, activo=True)
    except Equipo.DoesNotExist:
        messages.error(request, 'El equipo no existe o ya está inactivo.')
        return redirect('equipos')
    
    if request.method == 'POST':
        justificacion = request.POST.get('justificacion', '').strip()
        
        if not justificacion:
            messages.error(request, 'La justificación es obligatoria.')
            return redirect('equipos')
        
        # Desactivar el equipo
        equipo.activo = False
        equipo.save()
        
        # Crear registro de desactivación
        from datetime import date
        DesactivacionEquipo.objects.create(
            fecha_desactivacion=date.today(),
            responsable_desactivacion=request.session.get('username', 'Sistema'),
            justificacion=justificacion,
            equipo=equipo
        )
        
        messages.success(request, f'Equipo "{equipo.nombre_equipo}" desactivado exitosamente.')
        return redirect('equipos')
    
    # Si es GET, retornar error
    messages.error(request, 'Método no válido.')
    return redirect('equipos')

def activar_equipo(request, equipo_id):
    """Vista para reactivar un equipo inactivo"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        equipo = Equipo.objects.get(id=equipo_id, activo=False)
    except Equipo.DoesNotExist:
        messages.error(request, 'El equipo no existe o ya está activo.')
        return redirect('equipos_inactivos')
    
    if request.method == 'POST':
        # Reactivar el equipo
        equipo.activo = True
        equipo.save()
        
        messages.success(request, f'Equipo "{equipo.nombre_equipo}" reactivado exitosamente.')
        return redirect('equipos')
    
    # Si es GET, retornar error
    messages.error(request, 'Método no válido.')
    return redirect('equipos_inactivos')

def equipo_inactivo_detalle(request, equipo_id):
    """Vista de solo lectura para equipos inactivos"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        equipo = Equipo.objects.get(id=equipo_id, activo=False)
        registro_desactivacion = DesactivacionEquipo.objects.filter(equipo=equipo).first()
    except Equipo.DoesNotExist:
        messages.error(request, 'El equipo no existe o no está inactivo.')
        return redirect('equipos_inactivos')
    
    # Obtener pestaña activa (por defecto 'general')
    tab = request.GET.get('tab', 'general')
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'equipo': equipo,
        'registro_desactivacion': registro_desactivacion,
        'tab_activa': tab,
        'solo_lectura': True  # Flag para indicar que es solo lectura
    }
    
    return render(request, 'equipo_detalle.html', context)

def api_stats(request):
    """API endpoint para estadísticas del dashboard (para gráficas)"""
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    # Estadísticas por sede para gráfica
    stats_sede = list(Equipo.objects.values('sede').annotate(
        count=Count('id')
    ).exclude(sede__isnull=True))
    
    # Estadísticas por proceso para gráfica
    stats_proceso = list(Equipo.objects.values('proceso').annotate(
        count=Count('id')
    ))
    
    return JsonResponse({
        'por_sede': stats_sede,
        'por_proceso': stats_proceso
    })

def crear_equipo(request):
    """Vista para crear nuevo equipo"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()
            messages.success(request, f'Equipo "{equipo.nombre_equipo}" creado exitosamente.')
            return redirect('equipos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = EquipoForm()
    
    return render(request, 'crear_equipo.html', {
        'form': form,
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        }
    })

def equipo_detalle(request, equipo_id):
    """Vista para página de detalle del equipo con pestañas"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'El equipo no existe.')
        return redirect('equipos')
    
    # Obtener pestaña activa (por defecto 'general')
    tab = request.GET.get('tab', 'general')
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'equipo': equipo,
        'tab_activa': tab
    }
    
    return render(request, 'equipo_detalle.html', context)

def editar_equipo_seccion(request, equipo_id, seccion):
    """Vista para editar una sección específica del equipo"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'El equipo no existe.')
        return redirect('equipos')
    
    # Mapeo de secciones y sus campos
    secciones_campos = {
        'general': [
            'sede', 'proceso', 'serie', 'marca', 'modelo', 'nombre_equipo',
            'responsable', 'codigo_interno', 'codigo_ips', 'codigo_ecri',
            'ubicacion', 'clasificacion_misional', 'clasificacion_ips',
            'clasificacion_riesgo', 'registro_invima'
        ],
        'historico': [
            'tiempo_vida_util', 'fecha_adquisicion', 'propietario',
            'fecha_fabricacion', 'nit', 'proveedor', 'en_garantia',
            'fecha_fin_garantia', 'forma_adquisicion', 'tipo_documento',
            'numero_documento'
        ],
        'metrologia_admin': [
            'mantenimiento', 'frecuencia_mantenimiento', 'calibracion',
            'frecuencia_calibracion'
        ],
        'metrologia_tecnica': [
            'magnitud', 'rango', 'resolucion', 'rango_trabajo', 'error_maximo'
        ],
        'documentacion': [
            'hoja_vida', 'registro_importacion', 'manual_operacion',
            'manual_mantenimiento', 'guia_rapida', 'instructivo',
            'protocolo_mto', 'frecuencia_metrologica'
        ],
        'funcionamiento': [
            'voltaje', 'corriente', 'humedad', 'temperatura',
            'dimensiones', 'peso', 'otros'
        ]
    }
    
    if seccion not in secciones_campos:
        messages.error(request, 'Sección no válida.')
        return redirect('equipo_detalle', equipo_id=equipo_id)
    
    # Crear formulario dinámico solo con los campos de la sección
    class SeccionForm(forms.ModelForm):
        class Meta:
            model = Equipo
            fields = ['proceso', 'serie'] + secciones_campos[seccion]  # Siempre incluir proceso y serie
            
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Aplicar estilos Bootstrap a todos los campos
            for field_name, field in self.fields.items():
                if field_name in ['proceso', 'serie']:
                    field.widget.attrs['readonly'] = True
                    field.widget.attrs['class'] = 'form-control bg-light'
                else:
                    field.widget.attrs['class'] = 'form-control'
    
    if request.method == 'POST':
        form = SeccionForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sección {seccion.replace("_", " ").title()} actualizada exitosamente.')
            return redirect('equipo_detalle', equipo_id=equipo_id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = SeccionForm(instance=equipo)
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'equipo': equipo,
        'form': form,
        'seccion': seccion,
        'seccion_titulo': seccion.replace('_', ' ').title()
    }
    
    return render(request, 'editar_seccion.html', context)

def debug_equipos_inactivos(request):
    """Vista temporal para debuggear equipos inactivos"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Obtener todos los equipos inactivos
    equipos_inactivos = Equipo.objects.filter(activo=False)
    
    # Obtener todos los registros de desactivación
    registros_desactivacion = DesactivacionEquipo.objects.all()
    
    # Encontrar equipos inactivos SIN registro de desactivación
    equipos_sin_registro = []
    for equipo in equipos_inactivos:
        tiene_registro = DesactivacionEquipo.objects.filter(equipo=equipo).exists()
        if not tiene_registro:
            equipos_sin_registro.append(equipo)
    
    # Estadísticas para debug
    debug_info = {
        'total_equipos': Equipo.objects.count(),
        'equipos_activos': Equipo.objects.filter(activo=True).count(),
        'equipos_inactivos_total': equipos_inactivos.count(),
        'registros_desactivacion': registros_desactivacion.count(),
        'equipos_sin_registro': len(equipos_sin_registro),
    }
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'equipos_inactivos': equipos_inactivos,
        'registros_desactivacion': registros_desactivacion,
        'equipos_sin_registro': equipos_sin_registro,
        'debug_info': debug_info
    }
    
    return render(request, 'debug_inactivos.html', context)

def listar_traslados_view(request):
    """Vista para listar todos los traslados"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Filtros de búsqueda
    estado = request.GET.get('estado', '')
    equipo_busqueda = request.GET.get('equipo', '')
    
    traslados = TrasladoEquipo.objects.select_related('equipo').all()
    
    if estado:
        traslados = traslados.filter(estado=estado)
    
    if equipo_busqueda:
        traslados = traslados.filter(
            Q(equipo__nombre_equipo__icontains=equipo_busqueda) |
            Q(equipo__codigo_interno__icontains=equipo_busqueda)
        )
    
    # Ordenar por fecha de solicitud más reciente
    traslados = traslados.order_by('-fecha_solicitud')
    
    context = {
        'traslados': traslados,
        'estados': [
            ('pendiente', 'Pendiente'),
            ('aprobado', 'Aprobado'),
            ('ejecutado', 'Ejecutado'),
            ('cancelado', 'Cancelado')
        ],
        'estado_actual': estado,
        'equipo_busqueda': equipo_busqueda,
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'user_rol': request.session.get('rol'),
        'username': request.session.get('username')
    }
    
    return render(request, 'traslados_lista.html', context)

def crear_traslado_view(request):
    """Vista para crear una nueva solicitud de traslado"""
    # Verificar autenticación
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Verificar si se ha pasado un equipo específico
    equipo_id = request.GET.get('equipo_id')
    equipo_seleccionado = None
    
    if (equipo_id):
        try:
            equipo_seleccionado = Equipo.objects.get(id=equipo_id, activo=True)
        except Equipo.DoesNotExist:
            messages.error(request, "El equipo especificado no existe o no está activo")
            return redirect('equipos')
    
    if request.method == 'POST':
        form = TrasladoForm(request.POST)
        if form.is_valid():
            traslado = form.save(commit=False)
            # Establecer campos obligatorios
            traslado.usuario_solicitante = request.session.get('username', 'Sistema')
            traslado.estado = 'pendiente'
            traslado.fecha_solicitud = timezone.now().date()
            
            # Capturar información de origen del equipo
            equipo = traslado.equipo
            traslado.sede_origen = equipo.sede or ''
            traslado.ubicacion_origen = equipo.ubicacion or ''
            traslado.responsable_origen = equipo.responsable or ''
            
            try:
                traslado.save()
                messages.success(request, f'Solicitud de traslado creada exitosamente para el equipo {traslado.equipo.nombre_equipo}')
                return redirect('detalle_traslado', traslado_id=traslado.id)
            except Exception as e:
                messages.error(request, f'Error al guardar el traslado: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request, f'{field_name}: {error}')
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, f'Error general: {error}')
    else:
        form = TrasladoForm()
        # Si hay equipo preseleccionado, configurar el formulario
        if equipo_seleccionado:
            form.fields['equipo'].initial = equipo_seleccionado
    
    # Obtener datos para el template
    equipos_activos = Equipo.objects.filter(activo=True).order_by('nombre_equipo')
    
    # Obtener lista única de sedes disponibles
    sedes_disponibles = Equipo.objects.filter(activo=True).values_list('sede', flat=True).distinct().exclude(sede__isnull=True, sede__exact='')
    
    context = {
        'form': form,
        'equipos': equipos_activos,
        'sedes': sedes_disponibles,  # Agregar sedes disponibles
        'equipo_seleccionado': equipo_seleccionado,
        'username': request.session.get('username'),
        'user_rol': request.session.get('rol'),
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        }
    }
    return render(request, 'crear_traslado.html', context)

def detalle_traslado_view(request, traslado_id):
    """Vista para ver detalles de un traslado específico"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    traslado = get_object_or_404(TrasladoEquipo, id=traslado_id)
    
    context = {
        'traslado': traslado,
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'user_rol': request.session.get('rol'),
        'username': request.session.get('username')
    }
    
    return render(request, 'detalle_traslado.html', context)

def aprobar_traslado_view(request, traslado_id):
    """Vista para aprobar un traslado (solo administradores)"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'admin':
        messages.error(request, 'No tienes permisos para aprobar traslados.')
        return redirect('listar_traslados')
    
    traslado = get_object_or_404(TrasladoEquipo, id=traslado_id)
    
    if traslado.estado != 'pendiente':
        messages.error(request, 'Solo se pueden aprobar traslados pendientes.')
        return redirect('detalle_traslado', traslado_id=traslado_id)
    
    traslado.estado = 'aprobado'
    traslado.save()
    
    messages.success(request, f'Traslado aprobado para {traslado.equipo.nombre_equipo}')
    return redirect('detalle_traslado', traslado_id=traslado_id)

def ejecutar_traslado_view(request, traslado_id):
    """Vista para ejecutar un traslado aprobado (solo administradores)"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.session.get('rol') != 'admin':
        messages.error(request, 'No tienes permisos para ejecutar traslados.')
        return redirect('listar_traslados')
    
    traslado = get_object_or_404(TrasladoEquipo, id=traslado_id)
    
    if traslado.estado != 'aprobado':
        messages.error(request, 'Solo se pueden ejecutar traslados aprobados.')
        return redirect('detalle_traslado', traslado_id=traslado_id)
    
    if request.method == 'POST':
        # Actualizar información del equipo
        equipo = traslado.equipo
        equipo.sede = traslado.sede_destino
        equipo.ubicacion = traslado.ubicacion_destino
        equipo.responsable = traslado.responsable_destino
        equipo.save()
        
        # Actualizar estado del traslado
        traslado.estado = 'ejecutado'
        traslado.fecha_traslado = date.today()
        traslado.ejecutado_por = request.session.get('username')
        traslado.save()
        
        # Crear registro en EdicionEquipo para auditoría
        EdicionEquipo.objects.create(
            fecha=date.today(),
            justificacion=f'Traslado ejecutado: {traslado.justificacion}',
            equipo=equipo,
            responsable_anterior=traslado.responsable_origen,
            responsable_nuevo=traslado.responsable_destino,
            sede_anterior=traslado.sede_origen,
            sede_nueva=traslado.sede_destino,
            servicio_anterior=traslado.ubicacion_origen,
            servicio_nuevo=traslado.ubicacion_destino
        )
        
        messages.success(request, f'Traslado ejecutado exitosamente para {equipo.nombre_equipo}')
        return redirect('detalle_traslado', traslado_id=traslado_id)
    
    context = {
        'traslado': traslado,
        'user_rol': request.session.get('rol'),
        'username': request.session.get('username')
    }
    
    return render(request, 'ejecutar_traslado.html', context)

def cancelar_traslado_view(request, traslado_id):
    """Vista para cancelar un traslado"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    traslado = get_object_or_404(TrasladoEquipo, id=traslado_id)
    user_rol = request.session.get('rol')
    username = request.session.get('username')
    
    # Solo admins pueden cancelar cualquier traslado, usuarios normales solo los suyos pendientes
    if user_rol != 'admin' and (traslado.usuario_solicitante != username or traslado.estado != 'pendiente'):
        messages.error(request, 'No tienes permisos para cancelar este traslado.')
        return redirect('listar_traslados')
    
    if traslado.estado == 'ejecutado':
        messages.error(request, 'No se puede cancelar un traslado ya ejecutado.')
        return redirect('detalle_traslado', traslado_id=traslado_id)
    
    if request.method == 'POST':
        motivo_cancelacion = request.POST.get('motivo_cancelacion', '')
        
        traslado.estado = 'cancelado'
        if motivo_cancelacion:
            traslado.observaciones = f"{traslado.observaciones}\n\nCancelado por {username}: {motivo_cancelacion}".strip()
        traslado.save()
        
        messages.success(request, f'Traslado cancelado para {traslado.equipo.nombre_equipo}')
        return redirect('listar_traslados')
    
    context = {
        'traslado': traslado,
        'user_rol': user_rol,
        'username': username
    }
    
    return render(request, 'cancelar_traslado.html', context)

def solicitar_traslado_desde_equipo(request, equipo_id):
    """Vista para crear traslado directamente desde la página del equipo"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    equipo = get_object_or_404(Equipo, id=equipo_id, activo=True)
    
    # Verificar si ya existe un traslado pendiente o aprobado
    traslado_activo = TrasladoEquipo.objects.filter(
        equipo=equipo,
        estado__in=['pendiente', 'aprobado']
    ).first()
    
    if traslado_activo:
        messages.warning(request, f'Este equipo ya tiene un traslado {traslado_activo.estado}.')
        return redirect('detalle_traslado', traslado_id=traslado_activo.id)
    
    if request.method == 'POST':
        try:
            traslado = TrasladoEquipo.objects.create(
                equipo=equipo,
                usuario_solicitante=request.session.get('username'),
                sede_origen=equipo.sede or '',
                ubicacion_origen=equipo.ubicacion or '',
                responsable_origen=equipo.responsable or '',
                sede_destino=request.POST.get('sede_destino'),
                ubicacion_destino=request.POST.get('ubicacion_destino'),
                responsable_destino=request.POST.get('responsable_destino'),
                justificacion=request.POST.get('justificacion'),
                observaciones=request.POST.get('observaciones', ''),
            )
            
            messages.success(request, f'Solicitud de traslado creada exitosamente.')
            return redirect('detalle_traslado', traslado_id=traslado.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear la solicitud: {str(e)}')
    
    sedes_disponibles = ['Prado', 'San Vicente', 'SIU']
    
    context = {
        'equipo': equipo,
        'sedes': sedes_disponibles,
        'user_rol': request.session.get('rol'),
        'username': request.session.get('username')
    }
    
    return render(request, 'solicitar_traslado_equipo.html', context)

def historial_traslados_equipo(request, equipo_id):
    """Vista para ver historial de traslados de un equipo específico"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    equipo = get_object_or_404(Equipo, id=equipo_id)
    traslados = TrasladoEquipo.objects.filter(equipo=equipo).order_by('-fecha_solicitud')
    
    context = {
        'equipo': equipo,
        'traslados': traslados,
        'user': {
            'username': request.session.get('username'),
            'rol': request.session.get('rol')
        },
        'user_rol': request.session.get('rol'),
        'username': request.session.get('username')
    }
    
    return render(request, 'historial_traslados_equipo.html', context)