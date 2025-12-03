from django.contrib import admin
from .models import Usuario, Equipo, EdicionEquipo, DesactivacionEquipo

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombreusuario', 'rol', 'activo', 'fecha_creacion']
    list_filter = ['rol', 'activo']
    search_fields = ['nombreusuario']

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_equipo', 'proceso', 'sede', 'activo']
    list_filter = ['proceso', 'sede', 'activo']
    search_fields = ['nombre_equipo', 'codigo_interno', 'marca', 'modelo']

@admin.register(EdicionEquipo)
class EdicionEquipoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'equipo', 'responsable_anterior', 'responsable_nuevo']
    list_filter = ['fecha']

@admin.register(DesactivacionEquipo)
class DesactivacionEquipoAdmin(admin.ModelAdmin):
    list_display = ['fecha_desactivacion', 'equipo', 'responsable_desactivacion']
    list_filter = ['fecha_desactivacion']