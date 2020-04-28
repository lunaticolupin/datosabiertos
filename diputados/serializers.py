from rest_framework import serializers
from django.db.models import Q
from .models import *


class DistritoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Distrito
		fields = ('numero', 'nombre')


class PartidoPoliticoSerializer(serializers.ModelSerializer):
	class Meta:
		model = PartidoPolitico
		fields = ('nombre', 'siglas', 'logo')


class DiputadoSerializer(serializers.ModelSerializer):
	partido = PartidoPoliticoSerializer()
	distrito = DistritoSerializer()
	electo_por = serializers.ReadOnlyField()
	direccion = serializers.ReadOnlyField()

	class Meta:
		model = Diputado
		fields = ('__all__')


class ComisionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comision
		fields = ('id', 'nombre')


class DiputadoComisionSerializer(serializers.ModelSerializer):
	comision = ComisionSerializer()
	cargo = serializers.ReadOnlyField()

	class Meta:
		model = ComisionDiputado
		fields = ('cargo', 'tipo_cargo', 'comision')


class ComisionDiputadoSerializer(serializers.ModelSerializer):
	diputado = DiputadoSerializer()
	cargo = serializers.ReadOnlyField()

	class Meta:
		model = ComisionDiputado
		fields = ('__all__')


class ComisionSerializer(serializers.ModelSerializer):
	diputados = ComisionDiputadoSerializer(source="comisiondiputado_set", read_only=True, many=True)

	class Meta:
		model = Comision
		fields = ('__all__')


class SesionPlenoSerializer(serializers.ModelSerializer):
	tipo_sesion = serializers.ReadOnlyField()

	class Meta:
		model = SesionPleno
		fields = ('__all__')
		depth = 2


class SesionComisionSerializer(serializers.ModelSerializer):
	comision: ComisionSerializer()

	class Meta:
		model = SesionComision
		fields = ('__all__')
		depth = 1


class SesionSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		if isinstance(instance, SesionPleno):
			return SesionPlenoSerializer(instance=instance).data

		if isinstance(instance, SesionComision):
			return SesionComisionSerializer(instance=instance).data

	class Meta:
		model = Sesion
		fields = ('__all__')


class AsistenciaSerializer(serializers.ModelSerializer):
	tipo = serializers.ReadOnlyField()
	sesion = SesionSerializer()

	class Meta:
		model = Asistencia
		fields = ('__all__')


class SesionAsistenciaSerializer(serializers.ModelSerializer):
	tipo = serializers.ReadOnlyField()
	diputado = DiputadoSerializer()

	class Meta:
		model = Asistencia
		fields = ('__all__')


class DiputadoDetalleSerializer(serializers.ModelSerializer):
	partido = PartidoPoliticoSerializer()
	distrito = DistritoSerializer()
	comisiones = DiputadoComisionSerializer(source="comisiondiputado_set", read_only=True, many=True)
	asistencias = AsistenciaSerializer(many=True)
	total_asistencias = serializers.SerializerMethodField()
	total_inasistencias = serializers.SerializerMethodField()
	electo_por = serializers.ReadOnlyField()
	direccion = serializers.ReadOnlyField()

	class Meta:
		model = Diputado
		fields = ('__all__')

	def get_total_asistencias(self, obj):
		return obj.asistencias.filter(Q(tipo_asistencia=1) | Q(tipo_asistencia=4) | Q(tipo_asistencia=5)).count()

	def get_total_inasistencias(self, obj):
		return obj.asistencias.exclude(tipo_asistencia=1).count()
