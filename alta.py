# -*- coding: utf-8 -*- 
import os
import sys
import MySQLdb

#generador de calves aleatorias
def gen_passw():
	from random import choice
 	longitud = 10
	valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"
 	passw = ""
	passw = passw.join([choice(valores) for i in range(longitud)])
	return passw

#recogemos los parámetros nombre y dominio
nombre=(sys.argv[1])
dominio=(sys.argv[2])

#Realizamo una conexión a la base de datos
base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="proftpd")
cursor = base.cursor()

#realizaremos consulta para comprobar que no existe usuario 
consulta = "select usuario from proftpd.usuarios where usuario='%s' or dominio='%s';" % (nombre,dominio)
cursor.execute(consulta)
devolucion = cursor.fetchone()
if devolucion != None:
    print "Introduzca otro usuario, el usuario %s ya existe" % (nombre)
else:
	#realizaremos consulta para comprobar que no existe dominio
	consulta = "select usuario from proftpd.usuarios where dominio='%s';" % (dominio)
	cursor.execute(consulta)
	devolucion = cursor.fetchone()
	if devolucion != None:
		print "Introduzca otro dominio, el dominio %s ya existe" % (dominio)
	else:
		## creamos Base de datos para el cliente ##
		pass_mysql=gen_passw()
		print "A continuación se va a generar la contraseña para mysql"
#		print "Dicha contraseña se guardara en el fichero contraseñas_mysql"
		print "la contraseña para %s es: %s" % (nombre,pass_mysql)
		#creamos una bas de datos para el usuario
		crearbase=" create database %s" % (nombre)
        cursor.execute(crearbase)
        #creamos el usuario y le damos todos los permisos sobre la base de datos creada antes
        permisosql= "grant all privileges on %s.* to"% (nombre)+ " %s@localhost"% (nombre)+ " identified by "+"'%s'" % (pass_mysql)
        cursor.execute(permisosql)
		#guardamos y salimos
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        base.commit()
        
        ##  ##
        
