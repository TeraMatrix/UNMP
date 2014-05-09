#!/bin/sh

tmp=$(omd status | grep -c "Overall state:  running")

if [ $tmp -gt 0 ] 
then
	echo ""
	echo "Stoping UNMP..........................."
	echo ""
	echo "Stopping OMD.."
	omd stop
	echo ""
	echo "Stopping ndo2db service.."
	service ndo2db stop
	echo ""
	echo "Stopping mysql service.."
	service mysql stop
	echo ""
	echo "Stopping apache web server.."
	service httpd stop
	echo ""
	echo "Stopping FTP server.."
	service vsftpd stop
	echo ""
	echo "Stopping snmptt service.."
	service snmptt stop
	echo ""
	echo "Stopping snmptrapd service.."
	service snmptrapd stop
	echo ""
	echo "Stopping snmpd service.."
	service snmpd stop
	echo ""
	echo "Stopping unmp-alarm Daemon.."
	service unmp-alarm stop
	echo ""
	echo "Stopping unmp-ds Daemon.."
	service unmp-ds stop
	echo ""
	echo "Stopping unmp-local Daemon.."
	service unmp-local stop
	echo ""
else
	echo ""
	echo "Starting UNMP..........................."
	echo ""
	echo "Starting FTP server.."
	service vsftpd restart
	echo ""
	echo "Starting apache web server.."
	service httpd restart
	echo ""
	echo "Starting mysql service.."
	service mysql restart
	echo ""
	echo "Starting ndo2db service.."
	service ndo2db restart
	echo ""
	echo "Starting OMD.."
	omd restart
	echo ""
	echo "Starting snmpd service.."
	service snmpd restart
	echo ""
	echo "Starting snmptrapd service.."
	service snmptrapd restart
	snmptrapd udp:162
	snmptrapd -On
	echo ""
	echo "Starting snmptt service.."
	service snmptt restart
	echo ""
	echo "Starting unmp-alarm Daemon.."
	service unmp-alarm restart
	echo ""
	echo "Starting unmp-ds Daemon.."
	service unmp-ds restart
	echo ""
	echo "Starting unmp-local Daemon.."
	service unmp-local restart
	echo ""
fi

echo ""
echo "The terminal will automatically be closed.."
sleep 5

