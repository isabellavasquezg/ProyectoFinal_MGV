from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SedeViewSet, ServicioViewSet, ResponsableViewSet, EquipoViewSet,
    RegistroHistoricoViewSet, DocumentoEquipoViewSet, MetrologiaAdminViewSet,
    MetrologiaTecnicaViewSet, CondicionesFuncionamientoViewSet
)

# Crear el router para las APIs REST
router = DefaultRouter()
router.register(r'sedes', SedeViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'responsables', ResponsableViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'registros-historicos', RegistroHistoricoViewSet)
router.register(r'documentos', DocumentoEquipoViewSet)
router.register(r'metrologia-admin', MetrologiaAdminViewSet)
router.register(r'metrologia-tecnica', MetrologiaTecnicaViewSet)
router.register(r'condiciones', CondicionesFuncionamientoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]