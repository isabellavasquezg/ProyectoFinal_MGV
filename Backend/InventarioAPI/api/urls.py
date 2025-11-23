from django.urls import path
from .views import (
    EquiposView, 
    RegistroHistoricoView, 
    MetrologiaAdminView, 
    MetrologiaTecnicaView, 
    DocumentoEquipoView, 
    CondicionesFuncionamientoView
)

urlpatterns = [
    # Vistas de listado y filtro general
    path('General/', EquiposView.as_view(), name='equipos_general'),
    path('Registro/', RegistroHistoricoView.as_view(), name='registros_historicos_general'),
    path('MetrologiaA/', MetrologiaTecnicaView.as_view(), name='metrologia_tecnica_general'),
    path('MetrologiaT/', MetrologiaAdminView.as_view(), name='metrologia_admin_general'),
    path('Documentacion/', DocumentoEquipoView.as_view(), name='documentos_general'),
    path('Condicion/', CondicionesFuncionamientoView.as_view(), name='condiciones_funcionamiento_general'),
]