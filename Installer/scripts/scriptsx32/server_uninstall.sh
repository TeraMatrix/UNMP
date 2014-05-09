#!/bin/sh

######################################################
#
#	Uninstalls UNMP Server
#
######################################################

echo ""
echo "Uninstalling the UNMP server.."
echo ""

#service mysql restart

# params must be dynamic here..
#mysql -h@@@DBIP@@@ -P@@@DBPort@@@ -u@@@DBUsername@@@ -p@@@DBPassword@@@ -e "drop database if exists snmptt";

# params must be dynamic here..
#mysql -h@@@DBIP@@@ -P@@@DBPort@@@ -u@@@DBUsername@@@ -p@@@DBPassword@@@ -e "drop database if exists @@@DBName@@@";

omd stop
service httpd stop
service mysql stop

a=$(fuser -m /omd/sites/UNMP/tmp | awk '{ print $1 }'); for i in $a; do kill -9 $i; done;

omd -f rm UNMP

userdel -rf UNMP
echo -e "\n" | passwd UNMP
groupdel omd

service snmptt stop
snmptrapd -Off
service snmptrapd stop
service snmpd stop
service ndo2db stop

iptables -F

crontab -r

chkconfig --del vsftpd
chkconfig --del ndo2db
chkconfig --del snmptt
chkconfig --del snmptrapd
chkconfig --del snmpd

rm -rf /var/spool/snmptt
rm -rf /var/log/snmptt

userdel -rf snmptt
groupdel snmptt

rm -rf /etc/snmp
mv -f /etc/snmp.bak /etc/snmp

rm -rf /usr/share/snmp/mibs/IDU_1.3.smi
rm -rf /usr/share/snmp/mibs/IDU_1.7.smi
rm -rf /usr/share/snmp/mibs/RU_1.24.smi
rm -rf /usr/share/snmp/mibs/RU_1.62.smi

rm -rf /etc/sysconfig/iptables-config
mv -f /etc/sysconfig/iptables-config.bak /etc/sysconfig/iptables-config

rm -rf /etc/vsftpd/user_list
mv -f /etc/vsftpd/user_list.bak /etc/vsftpd/user_list

rm -rf /etc/vsftpd/vsftpd.conf
mv -f /etc/vsftpd/vsftpd.conf.bak /etc/vsftpd/vsftpd.conf

rm -rf /etc/httpd/conf/httpd.conf
mv -f /etc/httpd/conf/httpd.conf.bak /etc/httpd/conf/httpd.conf

# here /opt/omd must be dynamic
#rm -rf /opt/omd/versions/0.48/skel/etc/init.d/nagios
#mv -f /opt/omd/versions/0.48/skel/etc/init.d/nagios.bak /opt/omd/versions/0.48/skel/etc/init.d/nagios

rpm -ev --nodeps vsftpd-2.0.5-12.el5.i386
rpm -ev --nodeps omd-0.48-rh55-23.i386
rpm -ev --nodeps lm_sensors-2.10.7-4.el5.i386
rpm -ev --nodeps libtool-ltdl-1.5.22-6.1.i386
#rpm -ev --nodeps openldap-devel-2.3.43-3.el5.i386
a=$( rpm -qa | grep openldap-devel | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
#rpm -ev --nodeps expat-devel-1.95.8-8.2.1.i386
a=$( rpm -qa | grep expat-devel | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
#rpm -ev --nodeps db4-devel-4.3.29-9.fc6.i386
a=$( rpm -qa | grep db4-devel | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps apr-util-devel-1.2.7-7.el5.i386
#rpm -ev --nodeps apr-util-1.2.7-7.el5.i386
a=$( rpm -qa | grep apr-util-1.2.7 | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps apr-devel-1.2.7-11.i386
#rpm -ev --nodeps apr-1.2.7-11.i386
a=$( rpm -qa | grep apr-1.2.7 | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps php-gd-5.1.6-23.el5.i386
#rpm -ev --nodeps php-cli-5.1.6-23.el5.i386
a=$( rpm -qa | grep php-cli | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps php-mbstring-5.1.6-23.el5.i386
rpm -ev --nodeps php-pdo-5.1.6-23.el5.i386
#rpm -ev --nodeps php-common-5.1.6-23.el5.i386
a=$( rpm -qa | grep php-common | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps mod_fcgid-2.2-11.el5.i386
rpm -ev --nodeps libmcrypt-devel-2.5.7-1.2.el5.rf.i386
rpm -ev --nodeps libmcrypt-2.5.7-1a.i386
rpm -ev --nodeps graphviz-gd-2.14-1.el5.i386
rpm -ev --nodeps gmp-4.1.4-10.el5.i386
#rpm -ev --nodeps uuid-1.5.1-3.el5.src
a=$( rpm -qa | grep uuid | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps net-snmp-utils-5.3.2.2-5.el5.i386
rpm -ev --nodeps net-snmp-perl-5.3.2.2-5.el5.i386
rpm -ev --nodeps net-snmp-5.3.2.2-5.el5.i386
rpm -ev --nodeps graphviz-2.14-1.el5.i386
rpm -ev --nodeps perl-DBI-1.52-2.el5.i386
rpm -ev --nodeps perl-DBD-MySQL-3.0007-2.el5.i386
rpm -ev --nodeps perl-Config-IniFiles-2.68-1.el5.noarch
rpm -ev --nodeps perl-modules-5.8.8-10.i386
#rpm -ev --nodeps perl-Net-UPnP-1.41-3.el5.src
a=$( rpm -qa | grep perl-Net-UPnP | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
#rpm -ev --nodeps perl-5.8.8-18.el5.i386
a=$( rpm -qa | grep perl-5.8.8 | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
#rpm -ev --nodeps MySQL-community-debuginfo-5.1.60-1.rhel5.i386
#rpm -ev --nodeps MySQL-shared-compat-5.1.60-1.rhel5.i386
#rpm -ev --nodeps MySQL-devel-community-5.1.60-1.rhel5.i386
rpm -ev --nodeps MySQL-client-community-5.1.60-1.rhel5.i386
#rpm -ev --nodeps MySQL-server-community-5.1.60-1.rhel5.i386
#rpm -ev --nodeps postgresql-libs-8.1.11-1.el5_1.1.i386
a=$( rpm -qa | grep postgresql-libs | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
#rpm -ev --nodeps php-5.1.6-23.el5.i386
a=$( rpm -qa | grep php-5.1.6 | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rpm -ev --nodeps httpd-devel-2.2.3-22.el5.i386
#rpm -ev --nodeps httpd-2.2.3-22.el5.i386
a=$( rpm -qa | grep httpd-2.2.3 | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;

#rpm -ev --nodeps jdk-7-linux-i586
a=$( rpm -qa | grep jdk-7 | awk '{ print $1 }' ); for i in $a; do rpm -ev --nodeps $i; done;
rm -rf /usr/bin/java
mv -f /usr/bin/java.bak /usr/bin/java

chkconfig --del unmp-alarm
chkconfig --del unmp-ds
chkconfig --del unmp-local

#rm -rf /etc/init.d/unmp-nbi-naming /etc/init.d/unmp-nbi-notify /etc/init.d/unmp-nbi-supplier /var/lib/UNMP-NBI-Naming /var/lib/UNMP-NBI-Notify /var/lib/UNMP-NBI-Supplier /etc/init.d/unmp-ds /etc/init.d/unmp-local /etc/init.d/unmp-alarm /etc/init.d/unmp-clearAlarm /root/orb.properties

rm -rf /etc/init.d/unmp*
rm -rf /etc/init.d/snmptt*
rm -rf /usr/sbin/snmptt*
