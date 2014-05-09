#!/bin/sh

######################################################
#
#	$1		<%Temp%>/scripts-64bit			The path where scripts reside
#	$2		/opt/omd/versions/0.48/share/nbi/bin	The path where jaco resides
#
######################################################

echo ""
echo "Replacing jaco.."
echo ""

rm -f $2/jaco

cp $1/jaco $2/
