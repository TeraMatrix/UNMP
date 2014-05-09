#!/usr/bin/python2.6
"""
@ Author			:	Rajendra Sharma
@ Project			:	UNMP
@ Version			:	0.1
@ File Name			:	walk1.py
@ Creation Date			:	1-September-2011
@ Purpose			:	This plugin insert the data in multipal table.
@ Organisation                  :       Code Scape Consultants Pvt. Ltd.
@ Copyright (c) 2011 Codescape Consultant Private Limited
"""

#####################################################################################################
#
# exit from program using sys.exit() with error code[0,1,2,3]
# 0 for OK
# 1 for Warning
# 2 for Critical
# 3 for Unknown
#
##########################################################################

# import the packages
try:
    import os
    import math
    import sys
    import re
    import shlex
    import subprocess
    import commands
    from compiler.pycodegen import EXCEPT
    from datetime import datetime
    import time
except ImportError as e:
    print str(e[-1])
    raise SlefCreatedException("pakcege Import Error ")
    sys.exit(2)
# take argument by command line
arg = sys.argv
# function for error messages


def plugin_message(message=""):
    if message == "":
        print "you are passing bad arguments."
    else:
        print message


# default data insert function
def defult_data_insert(table_name, ip_address):
    try:
        site = __file__.split("/")[3]
        execfile(
            '/omd/sites/%s/share/check_mk/web/htdocs/mysql_exception.py' % site)
        db, cursor = mysql_connection('nmsp')
        if db == 1:
            raise SelfException(cursor)
        sql = "SELECT host_id from hosts where ip_address = '%s'" % ip_address
        if cursor.execute(sql) == 0 or cursor.execute(sql) == None:
            plugin_message("host_id dosn't exists in hosts table")
            sys.exit(1)
        else:
            result = cursor.fetchone()[0]
        if table_name.strip() == 'get_odu16_peer_node_status_table':
            ins_query = "INSERT INTO `get_odu16_peer_node_status_table`(`host_id`,`index`,`timeslot_index`,`link_status`,`tunnel_status`,`sig_strength`,`peer_mac_addr`,`ssidentifier`,`peer_node_status_raster_time`,`peer_node_status_num_slaves`,`peer_node_status_timer_adjust`,`peer_node_status_rf_config`,`timestamp`) values('%s','1','%s',' ',' ','0',' ',' ','0','0','0','0','%s')" % (result, '-1', datetime.now())
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip() == 'odu100_peerNodeStatusTable':
            ins_query = "INSERT INTO `odu100_peerNodeStatusTable` (`%s`, `raIndex`, `timeSlotIndex`, `linkStatus`, `tunnelStatus`, `sigStrength1`, `peerMacAddr`, `ssIdentifier`, `peerNodeStatusNumSlaves`, `peerNodeStatusrxRate`, `peerNodeStatustxRate`, `allocatedTxBW`, `allocatedRxBW`, `usedTxBW`, `usedRxBW`, `txbasicRate`, `sigStrength2`, `rxbasicRate`, `txLinkQuality`, `peerNodeStatustxTime`, `peerNodeStatusrxTime`, `timestamp`) VALUES ('%s', '1', '%s',' ',' ',0, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%s')" % (
                result, '-1', datetime.now())
            cursor.execute(ins_query)
            db.commit()
        # close the connection
        cursor.close()
        db.close()
    except MySQLdb.Error as e:
        print "MySQLdb Exception    " + str(e[-1])
        if db.open:
            cursor.close()
            db.close()
        sys.exit(1)
    except SlefCreatedException as e:
        if db.open:
            cursor.close()
            db.close()
        pass
        sys.exit(2)
    except Exception as e:
        print str(e[-1])
        if db.open:
            cursor.close()
            db.close()
        sys.exit(2)
    finally:
        if db.open:
            cursor.close()
            db.close()

# -- 	default data instert close


def snmp_walk(ip, port, oid, option, mib_path, table_name):
    # arg=["snmpwalk","-Le","-Ln","-v",version,"-c",community,(ip+":"+port),oid,option]
    # SS=subprocess.Popen(arg, stdout=subprocess.PIPE).communicate()
    myCommand = "snmpwalk -Le -Ln -v 2c -c public " + ip + ":" + port + " " + \
        oid + " " + option + " -m " + mib_path
    walk_result = commands.getstatusoutput(myCommand)
    if walk_result[0] != 0:
        if walk_result[-1] == None or walk_result[-1] == "":
            defult_data_insert(table_name, ip)
            raise SlefCreatedException(
                "Host Unrechable / Device not connected to network.")
            sys.exit(1)
        else:
            defult_data_insert(table_name, ip)
            plugin_message(str(walk_result[-1]))
            sys.exit(2)
    else:
        split_result = walk_result[-1].split('\n')
        count_interface = 0
        values = []
        total_index = len(split_result[0].split('.'))
        for col_value in split_result:
            sub_part = re.split("[.=]", col_value)
            values.append(sub_part[len(sub_part) - 1])
            if (col_value.split('.'))[0] == (split_result[0].split('.'))[0]:
                count_interface += 1
    return values, count_interface, total_index, split_result


# Exception class
class SlefCreatedException(Exception):
    def __init__(self, msg):
        print msg
        pass


# check the validation for command line argument
try:
    # import mySQL module
    import MySQLdb
    # Open database connection
    site = __file__.split("/")[3]
    execfile(
        '/omd/sites/%s/share/check_mk/web/htdocs/mysql_exception.py' % site)
    db, cursor = mysql_connection('nmsp')
    if db == 1:
        raise SelfException(cursor)

    if len(arg) > 1:
        if "--help" in arg or "-h" in arg:
            print """
MONITOR ODU16_NETWORK_INTERFACE_STATISTICS:
--------------------------------
This plugin gives you interface and tx/rx values

For Inserting the value of ODU16 tx/rx into mySQL database:
\t./%s -i 192.168.1.1 -o .1.3.6 odu_get_nw_statistics_table

\t-i\t Ip Address
\t-o\tOID [e.g. .1.3.6.-----]
\t-p\tPort_no
\t-t\t table name
\t -m\t mibs path

""" % (arg[0])
            sys.exit(2)
        else:
            if ("-i" in arg) and ("-o" in arg) and (len(arg) == 11) and ("-t" in arg) and ("-p" in arg) and ("-m" in arg):
                ip_address = arg[arg.index("-i") + 1]
                                           # receive the ip address
                oid_value = arg[arg.index("-o") + 1]       # receive oid value
                port_no = arg[arg.index("-p") + 1]       # receive port number
                table_name = arg[arg.index("-t") + 1]      # recive table name
                mib_path = arg[arg.index("-m") + 1]      # recive mib_path
                site = __file__.split("/")[3]		# site instance
                values, count_interface, total_index, split_result = snmp_walk(
                    ip_address, port_no, oid_value, "-OsQ", mib_path, table_name)
                # select the host)id form hosts table
                sql = "SELECT host_id from hosts where ip_address = '%s'" % ip_address
                if cursor.execute(sql) == 0 or cursor.execute(sql) == None:
                    plugin_message("host_id dosn't exists in hosts table")
                    sys.exit(1)
                else:
                    result = cursor.fetchone()[0]
                    # create sql query for insertion in table
                    for nw in range(count_interface):
                        if (values[int(nw)].strip() == 'notAssigned' or str(values[int(nw)]).strip() == '0') and (str(values[int(nw) + int(count_interface)]).strip() == '0' or values[int(nw) + int(count_interface)].strip() == 'notAvailable' or values[int(nw) + int(count_interface)].strip() == 'disabled'):
                            pass
                        else:
                            sql = "INSERT INTO %s values(null,'%s'" % (
                                table_name, result)
                            for index_val in range(total_index - 1):
                                sub_part_results = (
                                    re.split("[.=]", split_result[nw]))
                                sql += ",'%s'" % sub_part_results[
                                    index_val + 1]
                            for value in range((len(values)) / count_interface):
                                sql += ",'%s'" % values[nw + (
                                    value * count_interface)].replace('"', '').strip()
                            sql += ",'%s')" % (datetime.now())
                            time.sleep(1)
                            cursor.execute(sql)  # execute the query
                            db.commit()  # save the value in data base
                    print "SNMP OK"
                    cursor.close()  # close database and cursor
                    db.close()
                    sys.exit(0)
            else:
                plugin_message()
                sys.exit(1)
                if db.open:
                    cursor.close()
                    db.close()
    else:
        plugin_message('-------->>>> Please pass the arguments and you can also check the passing argumnets by [python] [file name] --help or -h.')
        sys.exit(1)
        if db.open:
            cursor.close()
            db.close()

except ImportError as e:
    print "Import Error   " + str(e[-1])
    if db.open:
        cursor.close()
        db.close()
    sys.exit(2)
except MySQLdb.Error as e:
    print "MySQLdb Exception    " + str(e[-1])
    if db.open:
        cursor.close()
        db.close()
    sys.exit(1)
except SlefCreatedException as e:
    if db.open:
        cursor.close()
        db.close()
    pass
    sys.exit(2)
except Exception as e:
    print str(e[-1])
    if db.open:
        cursor.close()
        db.close()
    sys.exit(2)
finally:
    if db.open:
        cursor.close()
        db.close()



#			if values[int(nw)].strip()=='notAssigned' and (values[int(nw)+int(count_interface)].strip()=='notAvailable' or values[int(nw)+int(count_interface)].strip()=='disabled'):
#				if table_name.strip()=='get_odu16_peer_node_status_table':
#					ins_query="INSERT INTO `get_odu16_peer_node_status_table`(`host_id`,`index`,`timeslot_index`,`link_status`,`tunnel_status`,`sig_strength`,`peer_mac_addr`,`ssidentifier`,`peer_node_status_raster_time`,`peer_node_status_num_slaves`,`peer_node_status_timer_adjust`,`peer_node_status_rf_config`,`timestamp`) values('%s','1','1','notAssigned','notAvailable','0',' ','%s','0','0','0','0','%s')"%(result,'-2',datetime.now())
#					print ins_query
#					cursor.execute(ins_query)
#					db.commit()
#				elif table_name.strip()=='odu100_peerNodeStatusTable':
#					ins_query="INSERT INTO `odu100_peerNodeStatusTable` (`%s`, `raIndex`, `timeSlotIndex`, `linkStatus`, `tunnelStatus`, `sigStrength1`, `peerMacAddr`, `ssIdentifier`, `peerNodeStatusNumSlaves`, `peerNodeStatusrxRate`, `peerNodeStatustxRate`, `allocatedTxBW`, `allocatedRxBW`, `usedTxBW`, `usedRxBW`, `txbasicRate`, `sigStrength2`, `rxbasicRate`, `txLinkQuality`, `peerNodeStatustxTime`, `peerNodeStatusrxTime`, `timestamp`) VALUES ('%s', '1', '1','notAssigned','notAvailable',0, ' ', '%s', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '%s')"%(result,'-2',datetime.now())
#			else:
