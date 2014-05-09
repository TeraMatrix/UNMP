#!/bin/sh

######################################################
#
#	$1	$Temp/32-bit	The path where RPM resides
#
######################################################

echo ""
echo "Including the python's shared library in ldconfig.."
echo ""

ldconfig
