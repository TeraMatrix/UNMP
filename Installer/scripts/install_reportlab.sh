#!/bin/sh

######################################################
#
#	$1	$Temp/32-bit	The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Report Lab.."
echo ""

cd $1

tar -xvf "reportlab-2.5.tar.gz" 
cd reportlab-2.5
python2.6 setup.py install

	

