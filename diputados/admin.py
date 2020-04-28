from django.contrib import admin
from .models import *

# register your models here.
''' admin.site.register(PartidoPolitico)
admin.site.register(Legislatura)
admin.site.register(Diputado)
admin.site.register(DiputadoSuplente)
admin.site.register(DiputadoIndependiente)
admin.site.register(Distrito)
admin.site.register(CV)
admin.site.register(RedesSociales)
admin.site.register(CasaGestion)
admin.site.register(Licencia)
admin.site.register(OrganoLegislativo)
admin.site.register(DiputadoOrganoLegislativo)
admin.site.register(Sesion)
admin.site.register(Asistencia)
admin.site.register(SesionPleno)
admin.site.register(Comision)
admin.site.register(SesionComision)
admin.site.register(ComisionDiputado)
admin.site.register(Tema)
admin.site.register(Votacion)
admin.site.register(VotoDiputado)
admin.site.register(VotacionSecreta)
admin.site.register(Documento)
admin.site.register(DocumentoComision)
admin.site.register(DocumentoDiputado)
admin.site.register(DocumentoSesion)  '''


@admin.register(PartidoPolitico)
class PartidoPoliticoAdmin(admin.ModelAdmin):
	pass


@admin.register(Diputado)
class DiputadoAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'tipo', 'partido')
	list_filter = ('tipo', 'partido')
	search_fields = ['nombre', 'apellidos']


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
	pass


class AsistenciaInLine(admin.TabularInline):
	model = Asistencia


@admin.register(SesionPleno)
class SesionPlenoAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'fecha')
	list_filter = ('tipo', 'fecha')
	search_fields = ['tipo', 'fecha']
	inlines = [AsistenciaInLine]


@admin.register(SesionComision)
class SesionComisionAdmin(admin.ModelAdmin):
	list_display = ('comision', 'fecha')
	list_filter = ('comision', 'fecha')
	search_fields = ['comision', 'fecha']
	inlines = [AsistenciaInLine]


class ComisionDiputadoInLine(admin.TabularInline):
	model = ComisionDiputado


@admin.register(Comision)
class ComisionAdmin(admin.ModelAdmin):
	inlines = [ComisionDiputadoInLine]
	search_fields = ['nombre']
