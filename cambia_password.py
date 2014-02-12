# -*- coding: utf-8 -*- 

import os
import sys
import MySQLdb



def cambia_mysql(nombre,password):
	base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="mysql")
	cursor = base.cursor()
	consulta = "select user from user where user='%s';" % nombre
	cursor.execute(consulta)
	resultado = cursor.fetchone()
	if resultado == None:
		print "No se puede cambiar la contraseña, el usuario %s no exite" % nombre
	else:
		print "La nueva contraseña para MySQL del usuario %s es %s" % (nombre,password)
		consulta = "update user set password=PASSWORD('%s') where user='%s';" % (password,nombre)
		cursor.execute(consulta)
		basereload = "FLUSH PRIVILEGES;"
		cursor.execute(basereload)
		base.commit()

def cambia_ftp(nombre,password):
	base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="proftpd")
	cursor = base.cursor()
	consulta = "select usuario from usuarios where usuario='%s';" % nombre
	cursor.execute(consulta)
	resultado = cursor.fetchone()
	if resultado == None:
		print "No se puede cambiar la contraseña, el usuario %s no exite" % nombre
	else:
		print "La nueva contraseña para Proftpd del usuario %s es %s" % (nombre,password)
		consulta = "update usuarios set password=PASSWORD('%s') where usuario='%s';" % (password,nombre)
		cursor.execute(consulta)
		basereload = "FLUSH PRIVILEGES;"
		cursor.execute(basereload)
		base.commit()


nombre=(sys.argv[1])
tipo=(sys.argv[2])
password=(sys.argv[3])


print tipo
if tipo == '-sql':
	cambia_mysql(nombre,password)
else:
	if tipo == '-ftp':
		cambia_ftp(nombre,password)		
	else:
		print "El segundo argumento ha de ser -sql o -ftp"



















