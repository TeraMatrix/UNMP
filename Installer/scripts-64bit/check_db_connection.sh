#!/bin/sh

######################################################
#
#	$1	hostname
#	$2	port
#	$3	username
#	$4	password
#	$5	schema_name
#
#	Example:
#
#	mysql -hlocalhost -P3306 -uroot -Dnms -proot
#
######################################################

echo ""
echo "The UNMP installer is checking for database server running.."
echo ""

#mysql -h$1 -P$2 -u$3 -D$5 -p$4

tmp=$(mysql -h$1 -P$2 -u$3 -p$4 -e "SHOW DATABASES LIKE '$5'")

if [ "$tmp" == "" ] 
then

	echo "Database does not exists"

else

	echo "Database do exists"

fi
