#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing PIL.."
echo ""

cd $1

tar -xvf "Imaging-1.1.7.tar.gz" 
cd Imaging-1.1.7
python2.6 setup.py install

	

