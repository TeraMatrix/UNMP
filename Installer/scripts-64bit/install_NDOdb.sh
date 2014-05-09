#!/bin/sh

######################################################
#
#	$1		<%Temp%>/64-bit		The path where RPM resides
#	$2		<%Temp%>/scripts/ndo_conf_files		The path where scripts resides (here, ndo_conf_files)
#
######################################################

echo ""
echo "The UNMP installer is installing NDO2db.."
echo "" 

omd stop

cd $2
rm -rf /opt/omd/sites/UNMP/etc/nagios/nagios.cfg
cp ndomod.cfg ndo2db.cfg nagios.cfg /opt/omd/sites/UNMP/etc/nagios/

cd $1
tar -xvzf ndoutils-1.4b9.tar.gz 
cd ndoutils-1.4b9
chmod +x configure
./configure
make
cd src
cp ndomod-3x.o ndo2db-3x log2ndo file2sock /opt/omd/versions/0.48/bin/
cd ..
make install-init
