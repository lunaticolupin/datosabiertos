from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    url(r'^diputados/$', views.diputado_list),
    url(r'^diputados/export/$', views.diputado_export),
    url(r'^comisiones/$', views.comisiones_list),
    url(r'^sesiones/$', views.sesiones_list),
    url(r'^diputados/(?P<pk>[0-9]+)/$', views.diputado_detail),
    url(r'^sesiones/(?P<pk>[0-9]+)/asistencias/$', views.sesiones_asistencia),
    url(r'^asistencias/(?P<pk>[0-9]+)/$', views.asistencias_detail)
]
