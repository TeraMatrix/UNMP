#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing mod_python.."
echo ""

cd $1

tar -xvf "mod_python-3.3.1.tgz" 
cd mod_python-3.3.1
chmod +x configure
./configure --with-apxs=/usr/sbin/apxs --with-python=/usr/local/bin/python2.6
make
cp ./src/mod_python.so /etc/httpd/modules/
make install

service httpd restart

chcon -t textrel_shlib_t '/usr/lib/httpd/modules/mod_python.so'

	

