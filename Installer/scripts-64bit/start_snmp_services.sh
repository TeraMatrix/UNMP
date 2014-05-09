#!/bin/sh

######################################################
#
#	Replacing customized configuration for snmp (tt, d, trapd, fmt)
#
#	$1		<%Temp%>/scripts-64bit/snmp_conf_files	source location of the configuration files
#
######################################################

#rm -rf /etc/snmp/snmp*
mv -f /etc/snmp /etc/snmp.bak
mkdir /etc/snmp

cp $1/snmp* /etc/snmp/

groupadd snmptt
useradd -g snmptt snmptt
mkdir /var/log/snmptt
chmod -R 777 /var/log/snmptt

touch /var/log/snmptt/snmptt.log
touch /var/log/snmptt/snmptt.debug
touch /var/log/snmptt/snmpttsystem.log
touch /var/log/snmptt/snmpttunknown.log

mkdir /var/spool/snmptt
chmod -R 777 /var/spool/snmptt
chmod 777 /etc/init.d/snmptt*

iptables -F

chkconfig --add snmpd
chkconfig --level 03456 snmpd on

chkconfig --add snmptrapd
chkconfig --level 03456 snmptrapd on

chkconfig --add snmptt
chkconfig --level 03456 snmptt on

service snmpd restart
service snmptrapd stop
snmptrapd -On
service snmptrapd restart
service snmptt restart

chkconfig --add vsftpd
chkconfig --level 03456 vsftpd on

chkconfig --add ndo2db
chkconfig --level 03456 ndo2db on

service ndo2db restart

