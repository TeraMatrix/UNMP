#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Python.."
echo ""

cd $1

rm -rf /usr/bin/python
tar -xvf Python-2.6.6.tgz 
cd Python-2.6.6
chmod +x configure
./configure --enable-shared
make
make install
ln -s "/usr/local/bin/python" /usr/bin/
	

