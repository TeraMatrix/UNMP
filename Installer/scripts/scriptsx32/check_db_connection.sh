#!/bin/sh

######################################################
#
#	$1	<%InstallDir%>
#	$2	<%Temp%>
#
#	$3	<%DBIP%>
#	$4	<%DBPort%>
#	$5	<%DBUsername%>
#	$6	<%DBPassword%>
#	$7	<%DBName%>
#
######################################################

echo ""
echo "Changing Permissions to 777 of Install Directory and Temp.."
echo ""

chmod -R 777 $1 $2 

cd $2/ThirdParty

echo ""
echo "Uninstalling old version of MySQL-Client.."
echo ""
rpm -e --nodeps mysql-5.0.77-4.el5_4.2.i386

echo ""
echo "Installing new version of MySQL-Client.."
echo ""
rpm -Uvh --nodeps MySQL-client-community-5.1.60-1.rhel5.i386.rpm

result=$(rpm -qa | grep MySQL-client-community-5.1.60-1.rhel5)

if [ "$result" != "" ]
then
	echo ""
	echo "Checking whether database server running.."
	echo ""

	tmp=$(mysql -h$3 -P$4 -u$5 -p$6 -e "SHOW DATABASES LIKE '$7'")

	if [ "$tmp" == "" ] 
	then
		echo "Database does not exists"
	else
		echo "Database do exists"
	fi
else
	echo "Database is not installed"
fi
