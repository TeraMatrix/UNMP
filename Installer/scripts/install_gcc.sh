#!/bin/sh

######################################################
#
#	$1	$Temp/32-bit	The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing GCC.."
echo ""

cd $1

rpm -Uvh --nodeps kernel-headers-2.6.18-128.el5.i386.rpm
rpm -Uvh --nodeps glibc-headers-2.5-34.i386.rpm
rpm -Uvh --nodeps glibc-devel-2.5-34.i386.rpm
rpm -Uvh --nodeps libgomp-4.3.2-7.el5.i386.rpm
rpm -Uvh --nodeps "gcc-4.1.2-44.el5.i386.rpm"

