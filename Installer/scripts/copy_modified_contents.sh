#!/bin/sh

######################################################
#
#	$1	check_mk_temp path
#	$2	conf.d_temp path
#
######################################################

mv -fv $1/web $1/../check_mk/
mv -fv $2/conf.d/* $2/../conf.d/

chmod 777 -R $1/../check_mk/web/htdocs

rm -rfv $1
rm -rfv $2
	

