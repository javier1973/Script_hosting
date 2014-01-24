#!/bin/bash

echo 'zone "'$1'" {' >> /var/cache/bind/$2
echo '        type master;' >> /var/cache/bind/$2
echo '      file "'$2'";' >> /var/cache/bind/$2
echo '};' >> /var/cache/bind/$2


echo 'zone "'$3'.in-addr.arpa"{'>> /var/cache/bind/'inv_'$2
echo '        type master;'>> /var/cache/bind/'inv_'$2
echo '        file "inv_"$2;'>> /var/cache/bind/'inv_'$2
echo '	};' >> /var/cache/bind/$2
