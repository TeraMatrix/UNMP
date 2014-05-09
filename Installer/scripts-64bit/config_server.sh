#!/bin/sh

######################################################
#
#	$1	<%WebServerMode%>
#	$2	<%SharedPort%>
#
######################################################

omd create UNMP

omd config UNMP set APACHE_MODE $1

if [ "$1" == "own" ]
then

	omd config UNMP set APACHE_TCP_PORT $2

else

	omd config UNMP set APACHE_TCP_PORT 80

fi

omd config UNMP set MySQL off

omd config UNMP set DEFAULT_GUI check_mk

service httpd restart
service mysql restart

#omd start UNMP
