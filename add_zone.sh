#!/bin/bash

echo 'zone "'$1'" {' >> /var/cache/bind/$2
echo '        type master;' >> /var/cache/bind/$2
echo '      file "'$2'";' >> /var/cache/bind/$2
echo '};' >> /var/cache/bind/$2

echo 'zone "0.0.10.in-addr.arpa"{'
        type master;
        file "inversa_javihost";
	};

echo 'zone "'$1'" {' >> $2
echo '        type master;' >> $2
echo '      file "'$2'";' >> $2
echo '};' >> $2

echo 'zone "'$3'.in-addr.arpa"{'>> 'inv_'$2
echo '        type master;'>> 'inv_'$2
echo '        file "inv_"$2;'>> 'inv_'$2
echo '	};' >> $2
