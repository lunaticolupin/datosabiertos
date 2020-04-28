from django.db import models
from model_utils.managers import InheritanceManager

# Create your models here.


class Estado(models.IntegerChoices):
    ACTIVO = (1, 'Activo')
    INACTIVO = (2, 'Inactivo')


class PartidoPolitico(models.Model):

    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10, null=True, blank=True)
    logo = models.ImageField(upload_to='partidos/logos', null=True, blank=True)

    def __str__(self):
        try:
            return self.siglas
        except PartidoPolitico.ObjectDoesNotExist:
            return ''
        except PartidoPolitico.DoesNotExist:
            return ''

    class Meta:
        verbose_name_plural = "Partidos Políticos"


class Legislatura(models.Model):

    nombre = models.CharField(max_length=20)
    inicio = models.DateField("Fecha de inicio")
    fin = models.DateField("Fecha de termino")
    status = models.IntegerField("Estado", choices=Estado.choices, default=Estado.ACTIVO)

    def __str__(self):
        return self.nombre


class Diputado(models.Model):

    class EstadoDip(models.IntegerChoices):
        ACTIVO = (1, 'Activo')
        INACTIVO = (2, 'Inactivo')
        LICENCIA_TEMPORAL = (3, 'Licencia menor a 30 días')
        LICENCIA_INDEFINIDA = (4, 'Licencia por tiempo indefinido')

    class Sede(models.IntegerChoices):
        SEDE1 = (1, '5 poniente')
        SEDE2 = (2, 'Mesón del Cristo')

    class Sexo(models.IntegerChoices):
        HOMBRE = (1, 'Hombre')
        MUJER = (2, 'Mujer')

    class TipoEleccion(models.IntegerChoices):
        MAYORIA = (1, 'Mayoría Relativa')
        PROPORCIONAL = (2, 'Representación Proporcional')

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    sexo = models.IntegerField(choices=Sexo.choices, default=0)
    tipo = models.IntegerField("Tipo de elección", choices=TipoEleccion.choices, default=TipoEleccion.MAYORIA)
    fotografia = models.ImageField(upload_to='diputados/fotos', null=True, blank=True)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=25)
    sede = models.IntegerField(choices=Sede.choices, default=Sede.SEDE1)
    status = models.IntegerField("Estado", choices=EstadoDip.choices, default=EstadoDip.ACTIVO)
    partido = models.ForeignKey(PartidoPolitico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Partido Político", related_name="integrantes")
    legislatura = models.ForeignKey(Legislatura, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos

    @property
    def electo_por(self):
        return self.TipoEleccion.choices[self.tipo - 1][1]

    @property
    def direccion(self):
        if (self.sede == self.Sede.SEDE1):
            return "Av. 5 poniente No. 128 Centro Histórico C.P. 72000 Puebla, Pue"

        if (self.sede == self.Sede.SEDE2):
            return "Edificio Alterno \"Mesón del Cristo\" Centro Histórico C.P. 72000 Puebla, Pue"


class DiputadoSuplente(models.Model):
    diputado_propietario = models.OneToOneField(Diputado, on_delete=models.SET_NULL, null=True, related_name="propietario")
    diputado_suplente = models.OneToOneField(Diputado, on_delete=models.CASCADE, related_name="suplente")
    fecha_inicio = models.DateField()


class DiputadoIndependiente(Diputado):
    es_independiente = models.BooleanField()


class Distrito (models.Model):
    numero = models.IntegerField(default=0)
    nombre = models.CharField(max_length=50)
    diputado = models.OneToOneField(Diputado, on_delete=models.SET_NULL, null=True, verbose_name="Representante", related_name='distrito')
    status = models.IntegerField("Estado", choices=Estado.choices, default=Estado.ACTIVO)

    def __str__(self):
        try:
            return str(self.numero) + ' ' + self.nombre
        except Distrito.ObjectDoesNotExist:
            return ''
        except Distrito.DoesNotExist:
            return ''


class CV (models.Model):
    datos_academicos = models.TextField("Datos Académicos")
    datos_laborales = models.TextField("Datos Laborales")
    otros_datos = models.TextField("Otros datos")
    diputado = models.OneToOneField(Diputado, on_delete=models.CASCADE)


class RedesSociales(models.Model):
    nombre = models.CharField(max_length=25)
    url = models.URLField()
    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE)


class CasaGestion(models.Model):
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE)


class Licencia(models.Model):
    class Tipo(models.IntegerChoices):
        TEMPORAL = (1, 'Menor a 30 días')
        INDEFINIDA = (2, 'Tiempo Indefinido')

    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE)
    inicio = models.DateField("Inicio de licencia")
    fin = models.DateField("Termino de licencia", null=True, blank=True)
    tipo = models.IntegerField("Tipo de licencia", choices=Tipo.choices)


class OrganoLegislativo(models.Model):

    class Tipo(models.IntegerChoices):
        JUGOCOPO = (1, 'Junta de Gobierno y Coordinación Política')
        MESA = (2, 'Mesa Directiva')
        PERMANENTE = (3, 'Comisión Permanente')

    nombre = models.CharField(max_length=50)
    tipo = models.IntegerField(choices=Tipo.choices)
    status = models.IntegerField("Estado", choices=Estado.choices, default=Estado.ACTIVO)
    inicio = models.DateField("Fecha de inicio")
    fin = models.DateField("Fecha de termino")
    legislatura = models.ForeignKey(Legislatura, on_delete=models.SET_NULL, null=True)
    integrantes = models.ManyToManyField(Diputado, through='DiputadoOrganoLegislativo')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Órganos Legislativos"


class DiputadoOrganoLegislativo(models.Model):
    class Cargo(models.IntegerChoices):
        PRESIDENTE = (1, 'PRESIDENTE(A)')
        VICE_PRESIDENTE = (2, 'VICEPRESIDENTE(A)')
        SECRETARIO = (3, 'SECRETARIO(A)')
        PROSECRETARIO = (4, 'PROSECRETARIO(A)')
        VOCAL = (5, 'VOCAL')
        COORDINADOR = (6, 'COORDINADOR(A)')
        REPRESENTANTE = (7, 'REPRESENTANTE LEGISLATIVO')

    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE)
    organo = models.ForeignKey(OrganoLegislativo, on_delete=models.CASCADE)
    tipo_cargo = models.IntegerField("Cargo", choices=Cargo.choices)
    status = models.IntegerField("Estado", choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        verbose_name_plural = "Integrantes"


class SesionManager(InheritanceManager):
    def get_queryset(self):
        return super(SesionManager, self).get_queryset().select_subclasses()


class Sesion (models.Model):
    fecha = models.DateField("Fecha de sesión")
    url_acta_sesion = models.FileField("Acta de la sesión", upload_to='sesiones/actas', null=True, blank=True)
    url_orden_dia = models.FileField("Orden del día", upload_to='sesiones/orden_dia', null=True, blank=True)
    # objects = InheritanceManager()
    objects = SesionManager()

    class Meta:
        base_manager_name = 'objects'


class Asistencia(models.Model):

    class Tipo(models.IntegerChoices):
        ASISTENCIA = (1, 'ASISTENCIA')
        INASISTENCIA_J = (2, 'INASISTENCIA JUSTIFICADA')
        INASISTENCIA_I = (3, 'INASISTENCIA INJUSTIFICADA')
        RETARDO_J = (4, 'RETARDO JUSTIFICADO')
        RETARDO_I = (5, 'RETARDO INJUSTIFICADO')
        NO_APLICA = (6, 'NO APLICA')
        LICENCIA = (7, 'CON LICENCIA')

    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE, related_name="asistencias")
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    tipo_asistencia = models.IntegerField("Tipo de asistencia", choices=Tipo.choices, default=Tipo.ASISTENCIA)

    def __str__(self):
        return ''

    @property
    def tipo(self):
        return self.Tipo.choices[self.tipo_asistencia - 1][1]

    class Meta:
        verbose_name_plural = "Asistencias"
        ordering = ['sesion__fecha']


class SesionPleno(Sesion):

    class Tipo(models.IntegerChoices):
        PREVIA = (0, 'PREVÍA')
        ORDINARIA = (1, 'PÚBLICA ORDINARIA')
        EXTRA = (2, 'EXTRAORDINARIA')
        PERMANENTE = (3, 'COMISIÓN PERMANENTE')
        SOLEMNE = (4, 'SOLEMNE')
        OTRA = (5, 'OTRA')

    def sesion_directorio(instance, filename):
        return 'sesiones/{0}/version_estenografica/{1}'.format(instance.id, filename)

    tipo = models.IntegerField("Tipo de sesión", choices=Tipo.choices, default=Tipo.ORDINARIA)
    url_version_estenografica = models.FileField("Versión estenográfica", upload_to=sesion_directorio, null=True, blank=True)

    def __str__(self):
        nombre = self.Tipo.choices[self.tipo][1]
        return nombre + ' del ' + format(self.fecha.strftime("%d/%m/%Y"))

    @property
    def tipo_sesion(self):
        return self.Tipo.choices[self.tipo][1]

    class Meta:
        verbose_name = "Sesión de Pleno"
        verbose_name_plural = "Sesiones de Pleno"


class Comision(models.Model):
    nombre = models.CharField(max_length=100)
    diputados = models.ManyToManyField(Diputado, through='ComisionDiputado', related_name='comisiones')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Comisión/Comité"
        verbose_name_plural = "Comisiones y Comités"
        ordering = ['nombre']


class SesionComision(Sesion):
    url_comunicado = models.FileField("Comunicado", upload_to='comisiones/comunicados', null=True, blank=True)
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)

    def __str__(self):
        return self.comision.nombre + ' del ' + format(self.fecha.strftime("%d/%m/%Y"))

    class Meta:
        verbose_name_plural = "Sesiones de Comisión"


class ComisionDiputado(models.Model):
    class Cargo(models.IntegerChoices):
        PRESIDENTE = (1, 'PRESIDENTE(A)')
        SECRETARIO = (2, 'SECRETARIO(A)')
        VOCAL = (3, 'VOCAL')

    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE, limit_choices_to={'status': 1})
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)
    tipo_cargo = models.IntegerField("Cargo", choices=Cargo.choices)
    status = models.IntegerField(choices=Estado.choices, default=Estado.ACTIVO)

    def __str__(self):
        return ''

    @property
    def cargo(self):
        temp = self.Cargo.choices[self.tipo_cargo - 1][1]
        temp = temp.replace("(A)", "")

        if (self.diputado.sexo == 2 and self.tipo_cargo != 3):
            temp = temp[0:len(temp) - 1] + 'A'

        return temp

    class Meta:
        verbose_name_plural = "Ingrantes de la Comisión"
        ordering = ['tipo_cargo']


class Tema (models.Model):
    descripcion = models.TextField()
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)

    def __str(self):
        return self.descripcion


class Votacion(models.Model):

    class Resultado (models.IntegerChoices):
        APROBADA = (1, 'Abrobada')
        NO_APROBADA = (2, 'No aprobada')

    class Tipo(models.IntegerChoices):
        NOMINAL = (1, 'Nominal')
        ECONOMICA = (2, 'Economica')
        SECRETA = (3, 'Secreta')

    resultado = models.IntegerField(choices=Resultado.choices)
    tipo = models.IntegerField("Tipo de votación", choices=Tipo.choices)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    diputado = models.ManyToManyField(Diputado, through='VotoDiputado')


class VotoDiputado(models.Model):

    class Tipo(models.IntegerChoices):
        FAVOR = (1, 'A FAVOR')
        CONTRA = (2, 'EN CONTRA')
        ABSTENCION = (3, 'EN ABSTENCION')
        SECRETO = (4, 'SECRETA')

    votacion = models.ForeignKey(Votacion, on_delete=models.CASCADE)
    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE, limit_choices_to={'status': 1})
    tipo_voto = models.IntegerField("Tipo de voto", choices=Tipo.choices)


class VotacionSecreta(Votacion):
    votos_favor = models.IntegerField("Votos a favor", default=0)
    votos_contra = models.IntegerField("Votos en contra", default=0)
    abstenciones = models.IntegerField("Abstenciones", default=0)


class Documento(models.Model):

    class Tipo(models.IntegerChoices):
        INFORME = (1, 'INFORME')
        PLAN = (2, 'PLAN DE TRABAJO')
        INICIATIVA = (3, 'INICIATIVA')
        ACUERDO = (4, 'PUNTO DE ACUERDO')
        DICTAMEN = (5, 'DICTAMEN')
        OTRO = (6, 'OTRO')

    nombre = models.CharField(max_length=150)
    tipo = models.IntegerField("Tipo de documento", choices=Tipo.choices)

    def __str__(self):
        return self.nombre


class DocumentoDiputado(Documento):
    diputado = models.ForeignKey(Diputado, on_delete=models.CASCADE)
    url_documento = models.FileField("Documento", upload_to='diputados/' + str(diputado) + '/documento')


class DocumentoComision(Documento):
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)
    url_documento = models.FileField("Documento", upload_to='comisiones/' + str(comision) + '/documento')


class DocumentoSesion(Documento):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    url_documento = models.FileField("Documento", upload_to='sesiones/' + str(tema) + '/documento')
