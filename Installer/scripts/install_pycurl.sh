#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is installing PyCurl.."
echo ""

cd $1

tar -xvf "pycurl.tar.gz"
cd pycurl
sh pycurl_install.sh

chmod -R 755 /opt/omd/daemon
