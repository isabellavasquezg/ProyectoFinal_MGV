from django.urls import path
from .views import Equipos,Registros,MetrologiaA,MetrologiaT

urlpatterns = [
    path('equipos/', Equipos.as_view(), name='equipos_general'),
    path('registros/', Registros.as_view(), name='registros_general'),
    path('metrologiaT/', MetrologiaT.as_view(), name='metrologiaT_general'),
    path('metrologiaA/', MetrologiaA.as_view(), name='metrologiaA_general'),
]