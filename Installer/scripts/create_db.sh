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
echo "Starting MySQL Server.."
echo ""

service mysql start

echo ""
echo "Settring default password for root.."
echo ""

mysqladmin -u root password $5
#mysqladmin -u root -h localhost.localdomain password root

echo ""
echo "Creating database.."
echo ""

mysql -h$2 -P$3 -u$4 -p$5 -e "create database $1";

echo ""
echo "Firing database script [Main].."
echo ""

mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/structure.sql";
mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/partitioning_dump.sql";
mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/defaultdata.sql";
mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/default_device.sql";

echo ""
echo "Firing database script [Stored Procedures].."
echo ""

mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/StoredProcedure/ap_interface_graph.sql";
mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/StoredProcedure/dashboard_ap_graph.sql";
mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/StoredProcedure/dashboard_sp.sql";
mysql $1 -h$2 -P$3 -u$4 -p$5 < "$6/StoredProcedure/get_overall_bandwidth.sql";

#echo ""
#echo "Creating default user for UNMP.."
#echo ""

#mysql -uroot -proot -sN -e "CREATE USER '$4'@'$2' IDENTIFIED BY '$5'"

echo ""
echo "Granting permissions to the created users.."
echo ""

mysql -uroot -proot -sN -e "GRANT ALL ON $1.* TO '$4'@'$2'"
cp $6/auth.conf /opt/omd/versions/0.48/skel/etc/apache/conf.d/
cp $6/Session.py /usr/local/lib/python2.6/site-packages/mod_python/
cp $6/multisite.mk /opt/omd/versions/0.48/skel/etc/check_mk/
