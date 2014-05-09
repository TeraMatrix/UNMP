#!/bin/sh

######################################################
#
#	$1		<%InstallType%>
#
######################################################

if [ "$1" == "UNMP Server" ]
then

	mv -fv $2/server_uninstall.sh $2/omd_uninstall.sh

elif [ "$1" == "UNMP Database" ]
then

	mv -fv $2/db_uninstall.sh $2/omd_uninstall.sh

else

	echo "The selected Installation Mode '$1' is wrongly read.."

fi


