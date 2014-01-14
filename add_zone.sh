#!/bin/bash

echo 'zone "'$1'" {' >> /var/cache/bind/$2
echo '        type master;' >> /var/cache/bind/$2
echo '      file "'$2'";' >> /var/cache/bind/$2
echo '};' >> /var/cache/bind/$2

zone "0.0.10.in-addr.arpa"{
        type master;
        file "inversa_javihost";

