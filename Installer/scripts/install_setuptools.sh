#!/bin/sh

######################################################
#
#	$1	$Temp/32-bit	The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing setuptools.."
echo ""

cd $1

tar -xvf "setuptools-0.6c11.tar.gz" 
cd setuptools-0.6c11
python2.6 setup.py install
	

