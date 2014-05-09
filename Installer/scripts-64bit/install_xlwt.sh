#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Xlwt (Excel library for Python).."
echo ""

cd $1

tar -xvf "xlwt-0.7.2.tar.gz" 
cd xlwt-0.7.2
python2.6 setup.py install

	

