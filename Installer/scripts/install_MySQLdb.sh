#!/bin/sh

######################################################
#
#	$1	$Temp/32-bit	The path where RPM resides
#	$2	$Temp/scripts/site.cfg	The path where scripts resides (here, site.cfg)
#
######################################################

echo ""
echo "The UNMP installer is installing MySQLdb for Python2.6.."
echo ""

cd $1

tar -xvf "MySQL-python-1.2.3.tar.gz" 
cd MySQL-python-1.2.3
rm site.cfg
cp $2 .
python2.6 setup.py install
	

