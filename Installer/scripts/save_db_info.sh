#!/bin/sh

########################################################
#
# 	$1 		represents to 	DBName
# 	$2 		represents to 	DBIP
# 	$3 		represents to 	DBPort
# 	$4 		represents to 	DBUsername
# 	$5 		represents to 	DBPassword
# 	$6 		represents to 	<%Temp%>/scripts/config_db.py 
# 	$7 		represents to 	<%InstallDir%>/versions/0.48/share/check_mk/web/htdocs/xml/config.xml
# 	$8 		represents to 	<%InstallDir%>/versions/0.48/share/check_mk/web/htdocs/xml/config_.xml
#
########################################################

py="python"

arguments=8

if [ $# -eq $arguments ] 

then
	
	pyScript_path="$6"

	config_path="$7"

	$py $pyScript_path $1 $2 $3 $4 $5 $config_path
	
	config_path="$8"

	$py $pyScript_path $1 $2 $3 $4 $5 $config_path
	
fi

cp $9/auth.conf $10/versions/0.48/skel/etc/apache/conf.d/
cp $9/Session.py /usr/local/lib/python2.6/site-packages/mod_python/
cp $9/multisite.mk $10/versions/0.48/skel/etc/check_mk/
