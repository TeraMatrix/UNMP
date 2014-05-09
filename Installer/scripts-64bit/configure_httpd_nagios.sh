#!/bin/sh

######################################################
#
#	$1	<%InstallDir%>
#	$2	$Temp/64-bit	The path where RPM resides
#
######################################################

echo ""
echo "The UNMP installer is configuring nagios.."
echo "" 

cd $2
cd ..
mv -f $1/versions/0.48/skel/etc/init.d/nagios $1/versions/0.48/skel/etc/init.d/nagios.bak
cp ${PWD}/nagios $1/versions/0.48/skel/etc/init.d/

echo ""
echo "The UNMP installer is configuring apache.."
echo "" 

cd scripts-64bit
mv -f /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
cp ${PWD}/httpd.conf /etc/httpd/conf/
