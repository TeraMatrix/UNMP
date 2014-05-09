#!/bin/sh

######################################################
#
#	$1	Default Site Name
#
#	Example:
#
#	passwd -S $site_name
#
######################################################

echo ""
echo "The UNMP installer is checking whether the User already exists or not.."
echo ""

tmp=$(passwd -S "$1")

if [ "$tmp" == "passwd: Unknown user name '$1'." ] 
then

	echo "User does not exist"

else

	echo "User do exists"

fi
