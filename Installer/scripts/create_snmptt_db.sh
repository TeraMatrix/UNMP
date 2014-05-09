#!/bin/sh

######################################################
#
#	Setting first time configuration for root user
#
#	$1	<%DBName%>
#	$2	<%DBIP%>
#	$3	<%DBPort%>
#	$4	<%DBUsername%>
#	$5	<%DBPassword%>
#	$6	<%Temp%>
#
#	Example:
#
#	mysql -hlocalhost -P3306 -uroot -Dnms -proot
#
######################################################

echo ""
echo "Creating SNMPTT database.."
echo ""

mysql -h$2 -P$3 -u$4 -p$5 -e "create database snmptt";
#mysql -hlocalhost -P3306 -uroot -proot -e "create database snmptt";

echo ""
echo "Firing SNMPTT database script.."
echo ""

mysql snmptt -h$2 -P$3 -u$4 -p$5 < "$6/snmptt.sql";
#mysql snmptt -hlocalhost -P3306 -uroot -proot < "./snmptt.sql";

