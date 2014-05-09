#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Report Lab Daily Unix.."
echo ""

cd $1

tar -xvf "reportlab-daily-unix.tar.gz" 
cd reportlab-20111118203602
python2.6 setup.py install

	

