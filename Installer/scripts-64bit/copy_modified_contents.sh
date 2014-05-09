#!/bin/sh

######################################################
#
#	$1	check_mk_temp path
#	$2	conf.d_temp path
#
######################################################

mv -fv $1/web $1/../check_mk/
mv -fv $2/conf.d/* $2/../conf.d/

rm -rfv $1
rm -rfv $2
	

