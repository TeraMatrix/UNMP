#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing PySNMP.."
echo ""

cd $1

tar -xvf "pysnmp-4.1.16d.tar.gz" 
cd pysnmp-4.1.16d
python2.6 setup.py install

	

