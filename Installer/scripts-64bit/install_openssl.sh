#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing Openssl and Openssl-devel.."
echo ""

cd $1

rpm -Uvh --nodeps openssl-0.9.8e-12.el5_4.6.x86_64.rpm
rpm -Uvh --nodeps openssl-devel-0.9.8e-12.el5_4.6.x86_64.rpm
