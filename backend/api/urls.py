# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('equipos/', views.equipos_view, name='equipos'),
    path('equipos/crear/', views.crear_equipo, name='crear_equipo'),
    path('equipos/inactivos/', views.equipos_inactivos_view, name='equipos_inactivos'),
    path('equipos/<int:equipo_id>/', views.equipo_detalle, name='equipo_detalle'),
    path('equipos/<int:equipo_id>/editar/<str:seccion>/', views.editar_equipo_seccion, name='editar_equipo_seccion'),
    path('equipos/<int:equipo_id>/desactivar/', views.desactivar_equipo, name='desactivar_equipo'),
    path('equipos/<int:equipo_id>/activar/', views.activar_equipo, name='activar_equipo'),
    path('equipos/inactivos/<int:equipo_id>/', views.equipo_inactivo_detalle, name='equipo_inactivo_detalle'),
    
    # URLs para traslados
    path('traslados/', views.listar_traslados_view, name='listar_traslados'),
    path('traslados/crear/', views.crear_traslado_view, name='crear_traslado'),
    path('traslados/<int:traslado_id>/', views.detalle_traslado_view, name='detalle_traslado'),
    path('traslados/<int:traslado_id>/aprobar/', views.aprobar_traslado_view, name='aprobar_traslado'),
    path('traslados/<int:traslado_id>/ejecutar/', views.ejecutar_traslado_view, name='ejecutar_traslado'),
    path('traslados/<int:traslado_id>/cancelar/', views.cancelar_traslado_view, name='cancelar_traslado'),
    path('equipos/<int:equipo_id>/solicitar-traslado/', views.solicitar_traslado_desde_equipo, name='solicitar_traslado_desde_equipo'),
    path('equipos/<int:equipo_id>/historial-traslados/', views.historial_traslados_equipo, name='historial_traslados_equipo'),
    
    path('debug/inactivos/', views.debug_equipos_inactivos, name='debug_inactivos'),
    path('api/stats/', views.api_stats, name='api_stats'),
]