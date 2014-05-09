#!/bin/sh


cp $1/auth.conf $2/version/0.48/skel/etc/apache/conf.d/
cp $1/session.py /usr/local/lib/python2.6/site-packages/mod_python/
cp $1/multisite.mk $2/version/0.48/skel/etc/check_mk/
