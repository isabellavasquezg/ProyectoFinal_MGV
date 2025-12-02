from django.urls import path
from .views import (
    EquiposView, 
    RegistroHistoricoView, 
    MetrologiaAdminView, 
    MetrologiaTecnicaView, 
    DocumentoEquipoView, 
    CondicionesFuncionamientoView,
    ResponsablesView,
    SedeView,
    ServiciosView,
    EstadoEquipoView
)

urlpatterns = [
    # Vistas de listado y filtro general
    path('General/', EquiposView.as_view(), name='equipos_general'),
    path('General/<id_equipo>/', EquiposView.as_view(), name='equipos_especifico'),
    path('General/Estado/', EstadoEquipoView.as_view(), name='equipos_estado'),
    path('Registro/', RegistroHistoricoView.as_view(), name='registros_historicos_general'),
    path('Registro/<id_historico>/', RegistroHistoricoView.as_view(), name='registros_historicos_especifico'),
    path('MetrologiaA/', MetrologiaAdminView.as_view(), name='metrologia_tecnica_general'),
    path('MetrologiaA/<id_admin>/', MetrologiaAdminView.as_view(), name='metrologia_tecnica_especifica'),
    path('MetrologiaT/', MetrologiaTecnicaView.as_view(), name='metrologia_admin_general'),
    path('MetrologiaT/<id_tecnica>/', MetrologiaTecnicaView.as_view(), name='metrologia_admin_especifica'),
    path('Documentacion/', DocumentoEquipoView.as_view(), name='documentos_general'),
    path('Documentacion/<id_doc>/', DocumentoEquipoView.as_view(), name='documentos_especifico'),
    path('Condicion/', CondicionesFuncionamientoView.as_view(), name='condiciones_funcionamiento_general'),
    path('Condicion/<id_cond>/', CondicionesFuncionamientoView.as_view(), name='condiciones_funcionamiento_especifico'),
    path('Responsables/', ResponsablesView.as_view(), name='Responsables_general'),
    path('Sedes/', SedeView.as_view(), name='Sedes_general'),
    path('Servicios/', ServiciosView.as_view(), name='Servicios_general'),
]