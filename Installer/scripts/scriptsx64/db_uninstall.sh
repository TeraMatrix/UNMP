#!/bin/sh

######################################################
#
#	Uninstalls UNMP Database Only
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

rpm -ev --nodeps MySQL-community-debuginfo-5.1.60-1.rhel5.x86_64
rpm -ev --nodeps MySQL-shared-compat-5.1.60-1.rhel5.x86_64
rpm -ev --nodeps MySQL-devel-community-5.1.60-1.rhel5.x86_64
rpm -ev --nodeps MySQL-client-community-5.1.60-1.rhel5.x86_64
rpm -ev --nodeps MySQL-server-community-5.1.60-1.rhel5.x86_64

# rpm -ev --nodeps MySQL-shared-compat-5.6.10-1.rhel5
# rpm -ev --nodeps MySQL-shared-5.6.10-1.rhel5
# rpm -ev --nodeps MySQL-devel-5.6.10-1.rhel5
# rpm -ev --nodeps MySQL-client-5.6.10-1.rhel5
# rpm -ev --nodeps MySQL-server-5.6.10-1.rhel5



