#!/bin/sh

######################################################
#
#	It installs MySQL Client before actual installation
#	to check database connectivity
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

cd $1

rpm -e --nodeps mysql-5.0.77-4.el5_4.1.i386
rpm -e --nodeps mysql-5.0.77-4.el5_4.1.x86_64
rpm -Uvh --nodeps MySQL-client-community-5.1.60-1.rhel5.x86_64.rpm
