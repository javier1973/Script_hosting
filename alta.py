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

def crea_bd(mynombre,dominio):	
	## creamos Base de datos para el cliente ##
	pass_mysql=gen_passw()
	print "A continuación se va a generar la contraseña para mysql"
#	print "Dicha contraseña se guardara en el fichero contraseñas_mysql"
	print "la contraseña para %s es: %s" % (nombre,pass_mysql)
	#creamos una bas de datos para el usuario
	crearbase=" create database %s" % (nombre)
	cursor.execute(crearbase)
    #creamos el usuario y le damos todos los permisos sobre la base de datos creada antes
	permisosql= "grant all privileges on %s.* to"% (nombre)+ " %s@localhost"% (mynombre)+ " identified by "+"'%s'" % (pass_mysql)
	cursor.execute(permisosql)
	#guardamos y salimos
	basereload = "FLUSH PRIVILEGES;"
	cursor.execute(basereload)
	base.commit()


def crea_carpetas (nombre,dominio):
	## CARPETAS PERSONALES y VIRTUAL HOST##
    os.system("mkdir /usr/www/%s" % nombre)
    os.system("echo Pagina del dominio %s en construccion > /usr/www/%s/index.html" %(dominio,nombre))
    #creamos vitual host y guardamos en /etc/apache/sites-avaible
    vhost=open("virtualhosts","r")
    lista=vhost.read()
    vhost.close()
    lista=lista.replace("@dominio@","%s" % dominio)
    lista=lista.replace("@nombre@","%s" % nombre)
    #abrimos el modo escritura y crea un nuevo fichero con lo introducido anteriormente
    s_avaible=open("/etc/apache2/sites-available/%s" % dominio,"w")
    s_avaible.write(lista)
    s_avaible.close()
    vhost=open("phpmyadmin_vh","r")
    lista=vhost.read()
    vhost.close()
    lista=lista.replace("@dominio@","%s" % dominio)
    #abrimos el modo escritura y crea un nuevo fichero con lo introducido anteriormente
    s_avaible=open("/etc/apache2/sites-available/mysql.%s" % dominio,"w")
    s_avaible.write(lista)
    s_avaible.close()    
    os.system("chmod -R 755 /usr/www")
    os.system("a2ensite %s >/dev/null" % dominio)
    os.system("service apache2 restart >/dev/null ")

def crea_proftpd(nombre,dominio):    
	# PROFTPD ##
    #con pwgen obtenemos una contrasena aleatoria de 12 letras y la guardamos en un fichero
    pas=gen_passw()
    consulta = "select max(uid) from proftpd.usuarios"
    cursor.execute(consulta)
    uids = cursor.fetchone()   
    uid = 4000
    if (uids != None):
        uid = uids[0]
        uid= int(uid) + 1

	
    #Insetamos al nuevo usuario en la tabla usuarios con la clave encriptada
    print "La contraseña de Proftpd para el usuario %s es : %s" % (nombre,pas)
    addusuario = "insert into usuarios values ('%s', PASSWORD('%s'), '%s', '%s', '/usr/www/%s','/bin/false',1,'%s');" % (nombre,pas,uid,uid,nombre,dominio)
    addgrupo = "insert into grupos values ('%s',%s)" % (nombre,uid)
    cursor.execute(addusuario)
    cursor.execute(addgrupo)
    basereload = "FLUSH PRIVILEGES;"
    cursor.execute(basereload)
    base.commit()
    os.system("chmod -R 755 /usr/www/%s" % nombre)
    os.system("chown -R %s:%s /usr/www/%s" % (uid, uid, nombre))
    

def crea_dns(nombre,dominio):        
    ## CREAR DNS ##
    # llemos plantilla nombre zona
    nombre_zona=open("named.conf.local","r")
    lista_nombre=nombre_zona.read()
    nombre_zona.close()
	#leemos plantilla zona directa
    zona_directa=open("db.dominio","r")
    lista_db=zona_directa.read()
    zona_directa.close()
        
    #reemplazamos en el fichero el dominio introducido
    lista_nombre=lista_nombre.replace("@dominio@","%s" % dominio)  
    #abrimos el fichero en modo añadir y agregamos la nueva zona
    nombre_zona=open("/etc/bind/named.conf.local","a")
    nombre_zona.write(lista_nombre)
    nombre_zona.close()
        
    #reemplazamos en el fichero el dominio introducido
    lista_db=lista_db.replace("@dominio@","%s" % dominio)
    #abrimos el fichero en modo escritura y lo guardamos con lo modificado antes
    z_directa=open("/var/cache/bind/db.%s" % (dominio),"w")
    z_directa.write(lista_db)
    z_directa.close()
    os.system("service bind9 restart >/dev/null")




#recogemos los parámetros nombre y dominio
nombre=(sys.argv[1])
dominio=(sys.argv[2])
mynombre='my'+nombre


#Realizamo una conexión a la base de datos
base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="proftpd")
cursor = base.cursor()

#realizaremos consulta para comprobar que no existe usuario 
consulta = "select usuario from usuarios where usuario='%s';" % (nombre)
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
		crea_bd(nombre,dominio)
		crea_carpetas(nombre,dominio)
		crea_proftpd(nombre,dominio)
		crea_dns(nombre,dominio)        
     
        
        
