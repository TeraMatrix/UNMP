#!/bin/sh

## run at last after all python modules and packages installed 
##
echo " pylink change script "
cp /usr/local/bin/python2.6 /usr/bin/
mv /usr/bin/python /usr/bin/python_bak
mv /usr/local/bin/python /usr/local/bin/python_bak
ln -s /usr/bin/python2.4 /usr/bin/python
ln -s /usr/bin/python2.4 /usr/local/bin/python
echo " pylink change : done"
