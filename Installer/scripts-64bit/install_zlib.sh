#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Zlib and Zlib-devel.."
echo ""

cd $1

rpm -Uvh --nodeps zlib-1.2.3-3.x86_64.rpm
rpm -Uvh --nodeps zlib-devel-1.2.3-3.x86_64.rpm
