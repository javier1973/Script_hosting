import os
import sys
import MySQLdb

nombre=(sys.argv[1])
subdom=(sys.argv[2])

base = MySQLdb.connect(host="localhost", user="root", passwd="javi", db="proftpd")
cursor = base.cursor()
#Consultamos dominio del usuario
consulta = "select dominio from proftpd.usuarios where usuario='%s';" % (nombre)
cursor.execute(consulta)
dmn = cursor.fetchone()
dominio=dmn[0]
#Obtendremos None si no existe el dominio
if dominio == None:
    print "No se puede incluir el subdominio, el usuario %s no existe" % (dominio)
else:
   #creamos carpetas
    os.system("mkdir /usr/www/%s/subdominio" % (nombre))
    os.system("mkdir /usr/www/%s/subdominio/%s" % (nombre,subdom))
    os.system("chmod -R 755 /usr/www/%s/subdominio/%s" % (nombre,subdom))
    #copiamos index
    os.system("echo Pagina de %s en construccion  > /usr/www/%s/subdominio/%s/index.html" %(nombre,nombre,subdom))
    #creamos vitual host
    vhost=open("sub_virtualhosts","r")
    lista=vhost.read()
    vhost.close()
    url=subdom+'.'+dominio
    lista=lista.replace("@dominio@","%s" % url)
    lista=lista.replace("@nombre@","%s" % nombre)
    lista=lista.replace("@nombre@","%s" % subdom)
    s_avaible=open("/etc/apache2/sites-available/%s" % url,"w")
    s_avaible.write(lista)
    s_avaible.close()
    os.system("a2ensite %s" % url)
    os.system("service apache2 restart ")
    #modificamos DNS
    zona_directa=open("/var/cache/bind/db.%s" % (dominio,"a"))
    zona_directa.write("%s IN CNAME www\n" % subdom)
    zona_directa.close()
    os.system("service bind9 restart >/dev/null")
    
