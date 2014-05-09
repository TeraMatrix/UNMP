#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing GCC.."
echo ""

cd $1

rpm -Uvh --nodeps kernel-headers-2.6.18-194.el5.x86_64.rpm
rpm -Uvh --nodeps glibc-headers-2.5-49.x86_64.rpm
rpm -Uvh --nodeps glibc-devel-2.5-49.x86_64.rpm
rpm -Uvh --nodeps libgomp-4.4.0-6.el5.x86_64.rpm
rpm -Uvh --nodeps "gcc-4.1.2-48.el5.x86_64.rpm"

