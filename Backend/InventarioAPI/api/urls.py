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
    ServiciosView
)

urlpatterns = [
    # Vistas de listado y filtro general
    path('General/', EquiposView.as_view(), name='equipos_general'),
    path('Registro/', RegistroHistoricoView.as_view(), name='registros_historicos_general'),
    path('MetrologiaA/', MetrologiaAdminView.as_view(), name='metrologia_tecnica_general'),
    path('MetrologiaT/', MetrologiaTecnicaView.as_view(), name='metrologia_admin_general'),
    path('Documentacion/', DocumentoEquipoView.as_view(), name='documentos_general'),
    path('Condicion/', CondicionesFuncionamientoView.as_view(), name='condiciones_funcionamiento_general'),
    path('Responsables/', ResponsablesView.as_view(), name='Responsables_general'),
    path('Sedes/', SedeView.as_view(), name='Sedes_general'),
    path('Servicios/', ServiciosView.as_view(), name='Servicios_general'),
]