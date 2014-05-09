#!/bin/sh

######################################################
#
#	$1	path 1
#	$2	path 2
#	..	..
#	..	..
#
######################################################

echo ""
echo "The UNMP installer is removing the original files.."
echo ""

rm -fRv $1
rm -fRv $2
