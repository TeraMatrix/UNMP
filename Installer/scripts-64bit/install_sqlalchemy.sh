#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing sqlalchemy.."
echo ""

cd $1

tar -xvf "SQLAlchemy-0.7.1.tar.gz" 
cd SQLAlchemy-0.7.1
python2.6 setup.py install
	

