# -*- coding: utf-8 -*- 
import os
import sys
import MySQLdb

def borra_db(nombre,mynombre):
	borrabase=" drop database %s" % (nombre)
	cursor.execute(borrabase)
	borrausua=" drop user %s@localhost" % (mynombre)
	cursor.execute(borrausua)
	basereload = "FLUSH PRIVILEGES;"
	cursor.execute(basereload)
	base.commit()

def borra_proftpd(dominio):
	#eliminamos de la tabla usuarios la linea que tenga el dominio introducido
    borra_dom="delete from proftpd.usuarios where dominio='%s';" % (dominio)
    cursor.execute(borra_dom)
    basereload = "FLUSH PRIVILEGES;"
    cursor.execute(basereload)
    base.commit()

def borra_carpeta(nombre,dominio):
	#borramos las carpetas del usuario
    os.system("rm -r /usr/www/%s" % nombre)
    os.system("a2dissite %s > /dev/null" % dominio)
    os.system("rm -r /etc/apache2/sites-available/%s" % dominio)
    os.system("service apache2 restart > /dev/null")
    #~ os.system("rm -r /etc/apache2/sites-available/phpmyadmin%s" % nombre)
    os.system("rm -r /var/cache/bind/db.%s" % dominio)
    #eliminamos del fichero la linea que coincide y las sif¡guiente hasta el segundo contenido que coincide 
    os.system("sed '/zone " + '"%s"'% dominio + "/,/};/d' /etc/bind/named.conf.local > temporal")
    os.system("mv temporal /etc/bind/named.conf.local")




#creamos un objeto con las opciones


dominio=(sys.argv[1])
#MySQL
#Conexion con la base de datos
base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="proftpd")
cursor = base.cursor()
#Consultamos nombre del propietario del dominio
consulta = "select usuario from proftpd.usuarios where dominio='%s';" % (dominio)
cursor.execute(consulta)
name = cursor.fetchone()
nombre= name[0]
mynombre='my'+nombre
#Obtendremos None si no existe el dominio
if name == None:
	print "No se puede borrar el dominio, el dominio %s no existe" % (dominio)
else:
    borra_db(nombre,mynombre)
    borra_proftpd(dominio)
    borra_carpeta(nombre,dominio)
    print "el usuario %s con dominio %s se elimino correctamente" % (nombre,dominio)
