# -*- coding: utf-8 -*- 

import os
import sys
import MySQLdb

nombre=(sys.argv[1])
tipo=(sys.argv[2])
password=(sys.argv[3])



def cambia_mysql():
	base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="mysql")
	cursor = base.cursor()
	consulta = "select user from user where user='%s';" % (nombre)
	cursor.execute(consulta)
	resultado = cursor.fetchone()
	if resultado == None:
		print "No se puede cambiar las contraseña, el usuario %s no exite" % (nombre)
	else:
		print "La nueva contraseña para MySQL del usuario %s es %s" % (nombre,password)
        consulta = "update user set password=PASSWORD('%s') where user='%s';" % (password,nombre)
        cursor.execute(consulta)
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        base.commit()


def cambia_ftp():
	base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="proftpd")
	cursor = base.cursor()
	consulta = "select usuario from usuarios where usuario='%s';" % (nombre)
	cursor.execute(consulta)
	resultado = cursor.fetchone()
	if resultado == None:
		print "No se puede cambiar las contraseña, el usuario %s no exite" % (nombre)
	else:
		print "La nueva contraseña para Proftpd del usuario %s es %s" % (nombre,password)
        consulta = "update usuarios set password=PASSWORD('%s') where username='%s';" % (password,nombre)
        cursor.execute(consulta)
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        base.commit()


case = {"-sql" : cambia_mysql(),
        "-ftp" : cambia_ftp(),
        }


if tipo in ('-sql','-ftp'):
	case [tipo]  
else:
	print "El segundo argumento ha de ser -sql o -ftp"



















