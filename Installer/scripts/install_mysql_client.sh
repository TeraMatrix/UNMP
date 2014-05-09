#!/bin/sh

######################################################
#
#	It installs MySQL Client before actual installation
#	to check database connectivity
#
#	$1	$Temp/32-bit	The path where RPM resides
#
######################################################

cd $1

rpm -e --nodeps mysql-5.0.77-4.el5_4.2.i386
rpm -Uvh --nodeps MySQL-client-community-5.1.60-1.rhel5.i386.rpm
