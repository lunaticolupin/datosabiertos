from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
# from rest_framework.parsers import JSONParser
import django_excel as excel
# from django.core.exceptions import ObjectDoesNotExist
from diputados.models import *
from diputados.serializers import *


class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def diputado_list(request):
	if request.method == 'GET':
		diputados = Diputado.objects.filter(status=1).order_by('tipo', 'distrito__numero', 'id')
		serializer = DiputadoSerializer(diputados, many=True)
		return JSONResponse(serializer.data)

	return HttpResponse(status=404)


def diputado_export(request):
	export = []
	diputados = Diputado.objects.values_list(
		'id',
		'nombre',
		'apellidos',
		'email',
		'telefono',
		'tipo',
		'distrito__numero',
		'distrito__nombre',
		'partido__nombre',
		named=True).filter(status=1).order_by('tipo', 'distrito__numero', 'id')

	for d in diputados:
		distrito = ''
		partido = 'Sin Partido'

		if (d.distrito__nombre is not None):
			distrito = str(d.distrito__numero) + ' ' + d.distrito__nombre

		if (d.partido__nombre is not None):
			partido = d.partido__nombre

		export.append([
			d.nombre + ' ' + d.apellidos,
			d.email, d.telefono,
			distrito,
			partido
		])

	sheet = excel.pe.Sheet(export)

	return excel.make_response(sheet, 'csv', file_name='diputados.csv')


def diputado_detail_export(request, pk):
	try:
		# diputado = Diputado.objects.get(pk=pk)
		pass
	except Diputado.DoesNotExist:
		return HttpResponse(status=404)

	pass


def diputado_detail(request, pk):
	try:
		diputado = Diputado.objects.get(pk=pk)
	except Diputado.DoesNotExist:
		return HttpResponse(status=404)

	if (request.method == 'GET'):
		serializer = DiputadoDetalleSerializer(diputado)
		return JSONResponse(serializer.data)

	return HttpResponse(status=404)


@csrf_exempt
def comisiones_list(request):
	comisiones = Comision.objects.all()
	serializer = ComisionSerializer(comisiones, many=True)

	return JSONResponse(serializer.data)


def sesiones_list(request):
	if (request.GET.get('tipo')):
		tipo_sesion = request.GET.get('tipo')
		sesiones = SesionPleno.objects.filter(tipo=tipo_sesion).order_by('-fecha')
	elif (request.GET.get('fecha')):
		fecha_sesion = request.GET.get('fecha')
		sesiones = SesionPleno.objects.filter(fecha=fecha_sesion)
	else:
		sesiones = SesionPleno.objects.all().order_by('-fecha')

	serializer = SesionPlenoSerializer(sesiones, many=True)
	return JSONResponse(serializer.data)


def sesiones_asistencia(request, pk):
	try:
		asistencias = Asistencia.objects.filter(sesion_id=pk)
	except Asistencia.DoesNotExist:
		return HttpResponse(status=404)

	serializer = SesionAsistenciaSerializer(asistencias, many=True)
	total_asistencia = asistencias.filter(Q(tipo_asistencia=1) | Q(tipo_asistencia=4) | Q(tipo_asistencia=5)).count()
	total_inasistencia = asistencias.exclude(Q(tipo_asistencia=1) | Q(tipo_asistencia=4) | Q(tipo_asistencia=5)).count()
	json = {'asistencias': serializer.data, 'total_asistencia': total_asistencia, 'total_inasistencia': total_inasistencia}

	return JSONResponse(json)


def asistencias_detail(request, pk):
	try:
		asistencias = Asistencia.objects.get(pk=pk)
	except Asistencia.DoesNotExist:
		return HttpResponse(status=404)

	serializer = AsistenciaSerializer(asistencias)
	return JSONResponse(serializer.data)


# Create your views here.
def index(request):
	return HttpResponde("Inicio")
