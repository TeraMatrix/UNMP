#!/bin/sh

######################################################
#
#	Uninstalls UNMP Database
#
######################################################

echo ""
echo "The UNMP installer is uninstalling the UNMP Database.."
echo ""

service mysql restart

# params must be dynamic here..
mysql -h@@@DBIP@@@ -P@@@DBPort@@@ -u@@@DBUsername@@@ -p@@@DBPassword@@@ -e "drop database if exists snmptt";

# params must be dynamic here..
mysql -h@@@DBIP@@@ -P@@@DBPort@@@ -u@@@DBUsername@@@ -p@@@DBPassword@@@ -e "drop database if exists @@@DBName@@@";

service mysql stop

rpm -ev --nodeps MySQL-community-debuginfo-5.1.60-1.rhel5.i386
rpm -ev --nodeps MySQL-shared-compat-5.1.60-1.rhel5.i386
rpm -ev --nodeps MySQL-devel-community-5.1.60-1.rhel5.i386
rpm -ev --nodeps MySQL-client-community-5.1.60-1.rhel5.i386
rpm -ev --nodeps MySQL-server-community-5.1.60-1.rhel5.i386
#rpm -ev --nodeps postgresql-libs-8.1.11-1.el5_1.1.i386
a=$( rpm -qa | grep postgresql-libs | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;


