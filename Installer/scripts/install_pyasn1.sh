#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing PyASN1.."
echo ""

cd $1

tar -xvf "pyasn1-0.1.1.tar.gz" 
cd pyasn1-0.1.1
python2.6 setup.py install

