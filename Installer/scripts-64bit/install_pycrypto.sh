#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing PyCrypto.."
echo ""

cd $1

tar -xvf "pycrypto-2.0.1.tar.gz" 
cd pycrypto-2.0.1
python2.6 setup.py install

