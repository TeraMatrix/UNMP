#!/bin/sh

######################################################
#
#	$1	<%InstallType%>
#	$2	$Temp/32-bit	The path where RPM resides
#
######################################################

cd $2

tmp=$(uname -a | grep -c ubuntu)

if [ $tmp -gt 0 ] 
then

	sudo dpkg -i alien_8.81_all.deb

	if [ "$1" == "Typical - UNMP Server & DB" ] 
	then

		sudo alien -d jdk-7-linux-i586.rpm
	
		sudo dpkg -i jdk-7-linux-i586.deb
	
	elif [ "$1" == "UNMP Server" ]
	then

		sudo alien -d jdk-7-linux-i586.rpm
	
		sudo dpkg -i jdk-7-linux-i586.deb

	elif [ "$1" == "UNMP Database" ] 
	then


		sudo alien -d postgresql-libs-8.1.11-1.el5_1.1.i386.rpm

		sudo dpkg -i postgresql-libs-8.1.11-1.el5_1.1.i386.deb

	else
		echo "else part"
	fi

else

	if [ "$1" == "Typical - UNMP Server & DB" ] 
	then

		echo ""
		echo "The UNMP installer is installing the UNMP server and Database.."
		echo ""

		rpm -Uvh --nodeps jdk-7-linux-i586.rpm
		mv -f /usr/bin/java /usr/bin/java.bak
		ln -s "/usr/java/jdk1.7.0/bin/java" /usr/bin/
		
		rpm -Uvh --nodeps httpd-2.2.3-22.el5.i386.rpm
		rpm -Uvh --nodeps httpd-devel-2.2.3-22.el5.i386.rpm
		rpm -Uvh --nodeps php-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps postgresql-libs-8.1.11-1.el5_1.1.i386.rpm
		rpm -e --nodeps mysql-5.0.45-7.el5.i386
		rpm -e --nodeps mysql-server-5.0.45-7.el5.i386
		rpm -e --nodeps mysql-devel-5.0.45-7.el5.i386
		rpm -Uvh --nodeps MySQL-server-community-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-client-community-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-devel-community-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-shared-compat-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-community-debuginfo-5.1.60-1.rhel5.i386.rpm
		rpm -ev --nodeps perl-base-2.14-1.el5.rf.noarch
		rpm -Uvh --nodeps perl-5.8.8-18.el5.i386.rpm
		rpm -Uvh --nodeps perl-Net-UPnP-1.41-3.el5.src.rpm
		rpm -Uvh --nodeps perl-modules-5.8.8-10.i386.rpm
		rpm -Uvh --nodeps perl-Config-IniFiles-2.68-1.el5.noarch.rpm
		rpm -Uvh --nodeps --force perl-base-2.14-1.el5.rf.noarch.rpm
		rpm -Uvh --nodeps perl-DBD-MySQL-3.0007-2.el5.i386.rpm
		rpm -Uvh --nodeps perl-DBI-1.52-2.el5.i386.rpm
		rpm -Uvh --nodeps graphviz-2.14-1.el5.i386.rpm
		rpm -Uvh --nodeps net-snmp-5.3.2.2-5.el5.i386.rpm
		rpm -Uvh --nodeps net-snmp-perl-5.3.2.2-5.el5.i386.rpm
		rpm -Uvh --nodeps net-snmp-utils-5.3.2.2-5.el5.i386.rpm
#		rpm -Uvh --nodeps snmptt-0.9-1.i586.rpm
		rpm -Uvh --nodeps uuid-1.5.1-3.el5.src.rpm
		rpm -Uvh --nodeps gmp-4.1.4-10.el5.i386.rpm
		rpm -Uvh --nodeps graphviz-gd-2.14-1.el5.i386.rpm
		rpm -Uvh --nodeps libmcrypt-2.5.7-1a.i386.rpm
		rpm -Uvh --nodeps libmcrypt-devel-2.5.7-1.2.el5.rf.i386.rpm
		rpm -Uvh --nodeps mod_fcgid-2.2-11.el5.i386.rpm
		rpm -Uvh --nodeps php-common-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-pdo-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-mbstring-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-cli-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-gd-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps apr-1.2.7-11.i386.rpm
		rpm -Uvh --nodeps apr-devel-1.2.7-11.i386.rpm
		rpm -Uvh --nodeps apr-util-1.2.7-7.el5.i386.rpm
		rpm -Uvh --nodeps apr-util-devel-1.2.7-7.el5.i386.rpm
		rpm -Uvh --nodeps db4-devel-4.3.29-9.fc6.i386.rpm
		rpm -Uvh --nodeps expat-devel-1.95.8-8.2.1.i386.rpm
		rpm -Uvh --nodeps openldap-devel-2.3.43-3.el5.i386.rpm
		rpm -Uvh --nodeps libtool-ltdl-1.5.22-6.1.i386.rpm
		rpm -Uvh --nodeps lm_sensors-2.10.7-4.el5.i386.rpm
		rpm -Uvh --nodeps omd-0.48-rh55-23.i386.rpm
		rpm -Uvh --nodeps vsftpd-2.0.5-12.el5.i386.rpm

		echo ""
		echo "The UNMP installer has finished installing the UNMP server and UNMP Database.."
		echo ""

	elif [ "$1" == "UNMP Server" ]
	then

		echo ""
		echo "The UNMP installer is installing the UNMP server.."
		echo ""

		rpm -Uvh --nodeps jdk-7-linux-i586.rpm
		mv -f /usr/bin/java /usr/bin/java.bak
		ln -s "/usr/java/jdk1.7.0/bin/java" /usr/bin/

		rpm -Uvh --nodeps httpd-2.2.3-22.el5.i386.rpm
		rpm -Uvh --nodeps httpd-devel-2.2.3-22.el5.i386.rpm
		rpm -Uvh --nodeps php-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps postgresql-libs-8.1.11-1.el5_1.1.i386.rpm
		rpm -ev --nodeps perl-base-2.14-1.el5.rf.noarch
		rpm -Uvh --nodeps perl-5.8.8-18.el5.i386.rpm
		rpm -Uvh --nodeps perl-Net-UPnP-1.41-3.el5.src.rpm
		rpm -Uvh --nodeps perl-modules-5.8.8-10.i386.rpm
		rpm -Uvh --nodeps perl-Config-IniFiles-2.68-1.el5.noarch.rpm
		rpm -Uvh --nodeps --force perl-base-2.14-1.el5.rf.noarch.rpm
		rpm -Uvh --nodeps perl-DBD-MySQL-3.0007-2.el5.i386.rpm
		rpm -Uvh --nodeps perl-DBI-1.52-2.el5.i386.rpm
		rpm -Uvh --nodeps graphviz-2.14-1.el5.i386.rpm
		rpm -Uvh --nodeps net-snmp-5.3.2.2-5.el5.i386.rpm
		rpm -Uvh --nodeps net-snmp-perl-5.3.2.2-5.el5.i386.rpm
		rpm -Uvh --nodeps net-snmp-utils-5.3.2.2-5.el5.i386.rpm
#		rpm -Uvh --nodeps snmptt-0.9-1.i586.rpm
		rpm -Uvh --nodeps uuid-1.5.1-3.el5.src.rpm
		rpm -Uvh --nodeps gmp-4.1.4-10.el5.i386.rpm
		rpm -Uvh --nodeps graphviz-gd-2.14-1.el5.i386.rpm
		rpm -Uvh --nodeps libmcrypt-2.5.7-1a.i386.rpm
		rpm -Uvh --nodeps libmcrypt-devel-2.5.7-1.2.el5.rf.i386.rpm
		rpm -Uvh --nodeps mod_fcgid-2.2-11.el5.i386.rpm
		rpm -Uvh --nodeps php-common-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-pdo-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-mbstring-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-cli-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps php-gd-5.1.6-23.el5.i386.rpm
		rpm -Uvh --nodeps apr-1.2.7-11.i386.rpm
		rpm -Uvh --nodeps apr-devel-1.2.7-11.i386.rpm
		rpm -Uvh --nodeps apr-util-1.2.7-7.el5.i386.rpm
		rpm -Uvh --nodeps apr-util-devel-1.2.7-7.el5.i386.rpm
		rpm -Uvh --nodeps db4-devel-4.3.29-9.fc6.i386.rpm
		rpm -Uvh --nodeps expat-devel-1.95.8-8.2.1.i386.rpm
		rpm -Uvh --nodeps openldap-devel-2.3.43-3.el5.i386.rpm
		rpm -Uvh --nodeps libtool-ltdl-1.5.22-6.1.i386.rpm
		rpm -Uvh --nodeps lm_sensors-2.10.7-4.el5.i386.rpm
		rpm -Uvh --nodeps omd-0.48-rh55-23.i386.rpm
		rpm -Uvh --nodeps vsftpd-2.0.5-12.el5.i386.rpm

		echo ""
		echo "The UNMP installer has finished installing the UNMP server.."
		echo ""

	elif [ "$1" == "UNMP Database" ]
	then

		echo ""
		echo "The UNMP installer is installing the UNMP Database.."
		echo ""

		rpm -Uvh --nodeps postgresql-libs-8.1.11-1.el5_1.1.i386.rpm
		rpm -e --nodeps mysql-5.0.45-7.el5.i386
		rpm -e --nodeps mysql-server-5.0.45-7.el5.i386
		rpm -e --nodeps mysql-devel-5.0.45-7.el5.i386
		rpm -Uvh --nodeps MySQL-server-community-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-client-community-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-devel-community-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-shared-compat-5.1.60-1.rhel5.i386.rpm
		rpm -Uvh --nodeps MySQL-community-debuginfo-5.1.60-1.rhel5.i386.rpm

		echo ""
		echo "The UNMP installer has finished installing the UNMP Database.."
		echo ""

	else

		echo ""
		echo "The selected Installation Mode '$1' is wrongly choosen.."
		echo ""

	fi

	### for RHEL Only ###
	setsebool -P httpd_can_network_connect=1

fi

