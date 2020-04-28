# import csv
import wget
import MySQLdb


def get_tipo_sesion(tipo_sesion):

	# Extraordinaria
	if (tipo_sesion == 154 or tipo_sesion == 151 or tipo_sesion == 165):
		return 2

	# Comisión Permanente
	if (tipo_sesion == 155 or tipo_sesion == 152 or tipo_sesion == 166 or tipo_sesion == 1):
		return 3

	# Pública Ordinaria
	if (tipo_sesion == 156 or tipo_sesion == 149 or tipo_sesion == 167):
		return 1

	# Previa
	if (tipo_sesion == 157 or tipo_sesion == 153 or tipo_sesion == 164):
		return 0

	# Solemne
	if (tipo_sesion == 158 or tipo_sesion == 150 or tipo_sesion == 168):
		return 4

	return 5


def actualiza_tabla(items, tipo_documento):
	documento = [['orden_dia', 'url_orden_dia'], ['actas', 'url_acta_sesion'], ['versiones_estenograficas', 'url_version_estenografica']]
	temp_doc = documento[tipo_documento][0]

	for item in items:
		url = "http://congresopuebla.gob.mx/index.php?option=com_k2&view=item&task=download&id="
		repo = "/srv/http/dev.congresopuebla.mx/uploads/sesiones/"
		uploads = "sesiones/"

		id = item[0]
		tipo_sesion = item[1]
		nombre_archivo = item[3]
		fecha = formato_fecha(item[2])
		temp_url = url + str(id)
		temp_nombre_archivo = str(tipo_sesion) + "_" + fecha + "_" + nombre_archivo
		temp_archivo = repo + temp_doc + "/" + temp_nombre_archivo

		descarga_archivo(temp_url, temp_archivo)

		url = uploads + temp_doc + "/" + temp_nombre_archivo
		campo = documento[tipo_documento][1]

		actualiza_campo(campo, tipo_sesion, fecha, url)


def formato_fecha(cadena):
	print(cadena)
	meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
	fecha = ''
	temp = cadena.lower().replace('.', '')

	for index, item in enumerate(meses):
		if (temp.find(item) >= 0):
			inicio = temp.find(item) - 6

			if (inicio < 0):
				inicio = 0

			fin = len(temp)
			fecha = temp[inicio:fin]

			fecha = fecha.split(' de ')

			fecha[1] = str(index + 1) if index > 9 else '0' + str(index + 1)
			return ("-".join(fecha[::-1]))


def descarga_archivo(url, repo):
	print("Descargando " + url)

	try:
		wget.download(url, repo)
		return True
	except Exception:
		print("Error al descargar " + url)
		return False


def actualiza_campo(campo, tipo_sesion, fecha_sesion, url_archivo):
	db_temp = MySQLdb.connect(host='localhost', user='admin', passwd='alohomora', db='congreso')
	sql = "update diputados_sesion set {} = '{}' where fecha = '{}' and id in (select sesion_ptr_id from diputados_sesionpleno where tipo = {})"
	sql_versiones_esteno = "update diputados_sesionpleno set url_version_estenografica = '{}' where tipo = {} and sesion_ptr_id in (select id from diputados_sesion where fecha = '{}')"
	tipo = get_tipo_sesion(tipo_sesion)

	sql = sql.format(campo, url_archivo, fecha_sesion, tipo)

	if (campo == 'url_version_estenografica'):
		sql = sql_versiones_esteno.format(url_archivo, tipo, fecha_sesion)

	print(sql)

	try:
		cursor_temp = db_temp.cursor()
		cursor_temp.execute(sql)
		db_temp.commit()
	except Exception:
		print(Exception.__str__)


mydb = MySQLdb.connect(host='localhost', user='admin', passwd='alohomora', db='lx_plantilla')
cursor = mydb.cursor()

sql_orden_dia = "select a.id, catid, i.title, a.filename from cng_k2_items as i join cng_k2_attachments as a on a.itemid = i.id where catid in (select id from cng_k2_categories where parent in (select id from cng_k2_categories where name like '%orden%'))"
sql_actas = "select a.id, catid, i.title, a.filename from cng_k2_items as i join cng_k2_attachments as a on a.itemid = i.id where catid in (select id from cng_k2_categories where parent in (select id from cng_k2_categories where name like '%actas%'))"
sql_esteno = "select a.id, catid, i.title, a.filename from cng_k2_items as i join cng_k2_attachments as a on a.itemid = i.id where catid in (select id from cng_k2_categories where parent in (select id from cng_k2_categories where name like '%esteno%'))"
consultas = [sql_orden_dia, sql_actas, sql_esteno]

for index, sql in enumerate(consultas):
	cursor.execute(sql)
	items = cursor.fetchall()

	# actualiza_tabla(items, index)

sql_sesiones = "select * from cng_dip_sesiones"
cursor.execute(sql_sesiones)

sesiones = cursor.fetchall()

for sesion in sesiones:
	insert_sesion = "insert into diputados_sesion(id,fecha) values ({},'{}')"
	insert_sesion_pleno = "insert into diputados_sesionpleno(sesion_ptr_id, tipo)"
	tipo_sesion = get_tipo_sesion(sesion[2])
	print(insert_sesion.format(sesion[0], sesion[1]))
