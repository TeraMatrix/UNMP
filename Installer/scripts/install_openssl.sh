#!/bin/sh

######################################################
#
#	$1	$Temp/32-bit	The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Openssl and Openssl-devel.."
echo ""

cd $1

rpm -Uvh --nodeps openssl-0.9.8e-7.el5.i386.rpm
rpm -Uvh --nodeps openssl-devel-0.9.8e-7.el5.i386.rpm
