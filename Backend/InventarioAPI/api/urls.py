from django.urls import path
from .views import Equipos,Registros,MetrologiaA,MetrologiaT,documentos,condicion

urlpatterns = [
    path('equipos/', Equipos.as_view(), name='equipos_general'),
    path('registros/', Registros.as_view(), name='registros_general'),
    path('metrologiaT/', MetrologiaT.as_view(), name='metrologiaT_general'),
    path('metrologiaA/', MetrologiaA.as_view(), name='metrologiaA_general'),
    path('documentos/', documentos.as_view(), name='documentos_general'),
    path('condicion/', condicion.as_view(), name='condicion_general'),
]