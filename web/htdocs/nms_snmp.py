#!/usr/bin/python2.6

# import the package
import os
import math
import sys
import re
import MySQLdb
import shlex
import subprocess
import commands

"""
nms_snmp: All Snmp Functions For NMS

Author : Anuj Samaria

(CodeScape Consultants Pvt. Ltd.)
"""


##################################################
##                                              ##
##           Author- Anuj Samariya              ##
##                                              ##
##             Nms_snmp                         ##
##                                              ##
##                                              ##
##          CodeScape Consultants Pvt. Ltd.     ##
##                                              ##
##################################################
###############################################################################
#  Author- Anuj Samariya
# This function is used to get the value of device parameter.
def snmp_get(version, community, ip, port, oid):
    arg = ["snmpget", "-Le", "-Ln", "-v", version, "-c", community, (
        ip + ":" + port), oid]
    SS = subprocess.Popen(arg, stdout=subprocess.PIPE).communicate()[0]
    return SS


def snmp_set(version, community, ip, port, oid, type, val):
    arg = ["snmpset", "-OsQ", "-Le", "-Ln", "-v", version, "-c",
           community, (ip + ":" + port), oid, type, val]
    SS = subprocess.Popen(arg, stdout=subprocess.PIPE).communicate()[0]
    return SS


def snmp_setmultiple(version, community, ip, port, oid, type, val, oid1, type1, val1):
    arg = ["snmpset", "-Le", "-Ln", "-v", version, "-c", community, (
        ip + ":" + port), oid, type, val, oid1, type1, val1]
    SS = subprocess.Popen(arg, stdout=subprocess.PIPE).communicate()[0]
    return SS


def snmp_walk(version, community, ip, port, oid, option, option1):
    arg = ["snmpwalk", "-Le", "-Ln", "-v", version, "-c", community, (
        ip + ":" + port), oid, option, option1]
    SS = subprocess.Popen(
        arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    row = re.split("[\n=]", SS[0])
    dictarr = []
    dict = {}
    for i in range(0, (len(row) - 1), 2):
        ii = i + 1
        dict[str(row[i].strip())] = str(row[ii].strip())
    return dict

##    arg=["snmpwalk","-Le","-Ln","-v",version,"-c",community,(ip+":"+port),oid,option,option1]
##    SS=subprocess.Popen(arg, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
##    row=re.split("[\n=]",SS)
##    dictarr=[]
##    dict={}
##    for i in range(0,(len(row)-1),2):
##        ii = i + 1
##        dict[str(row[i].strip())]=str(row[ii].strip())
##    return dict




# ss = snmp_walk('2c','public','172.22.0.110','161','.1.3.6.1.4.1.26149.2','-On','-OQ')
# print ss


# ss=snmp_setmultiple('2c','private','172.22.0.110','161','.1.3.6.1.4.1.26149.2.2.13.5.1.3.1.12','i','4','.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.12','s',"                  ")
# print ss
# ss={}
