#!/usr/bin/python2.6

#=====================================================================================
#
# Author: Yogesh Kumar (ccpl)
#
# Purpose:
# This plugin gives you the value of each interfaces and tx/rx
# through snmp get (snmp.pl file).
#
# Arguments:
# --help	:	prints all arguments and use of arguments
# -i		:	Access point ip address
# -s		:	site name [e.g: nms]
#
# Requirement:
# Nagios
# Python 2.x or higher (with MySQLdb package)
# mySQL (with nms database schema and usefull tables)
#
# Output:
# Insert all the interfaces, tx/rx and uptime details into database
# Display Uptime of Device
# Return Status [0,1,2,3]
#
#=========================================================================

# import all the usefull modules.
import sys
import subprocess

# get all the command line arguments
arg = sys.argv

# constant variable which stores default status of device
STATE = "down"

# error message for this plugin


def plugin_message(message=""):
    if message == "":
        print "you are passing bad arguments."
    else:
        print message

# exit from program using sys.exit() with error code[0,1,2,3]
# 0 for OK
# 1 for Warning
# 2 for Critical
# 3 for Unknown


def exit(message_code):
    try:
        sys.exit(message_code)
    except SystemExit:
        pass

# validate command line argument
# print help
try:
    # import mySQL module
    import MySQLdb

    if len(arg) > 1:
        if "--help" in arg:
            print """
MONITOR ACCESS POINT BANDWIDTH:
--------------------------------
This plugin gives you interface and tx/rx values

For Inserting the value of Access Point tx/rx into mySQL database:
\t./%s -i 192.168.1.1 -s nms

\t-i\tAccess Point Ip Address
\t-s\tSite Name [e.g. nms]

""" % (arg[0])
            exit(2)
        else:

            if ("-i" in arg) and ("-s" in arg) and (len(arg) == 5):
                ip_address = arg[arg.index("-i") + 1]		# receive the ip address
                site_name = arg[arg.index("-s") + 1]		# receive site name
                execfile(
                    '/omd/sites/%s/share/check_mk/web/htdocs/nms_config.py' % site_name)
                # Open database connection
                db = open_database_connection()
                # prepare a cursor object using cursor() method
                cursor = db.cursor()
                command = ["/omd/deamon/snmp.pl", ip_address]
                # call the perl file which gives you interface, tx/rx values
                # and uptime using snmp get
                pipe = subprocess.Popen(
                    command, stdout=subprocess.PIPE).communicate()[0]
                command_result = pipe.split("\n")
                interface_name = []
                    # create a list variable to store interface name
                interface_tx = []
                    # create a list variable to store tx values
                interface_rx = []
                    # create a list variable to store rx values
                sys_uptime = STATE				# create a variable to store system uptime

                # get the device_id from ip address
                sql = "SELECT id from nms_devices \
					WHERE ipaddress = '%s'" % (ip_address)
                cursor.execute(sql)
                result = cursor.fetchone()

                # check device exist or not in the database
                if result == None:
                    plugin_message("Device does not exist in Database")
                    exit(1)
                else:
                    device_id = result[0]  # get device_id

                    if len(command_result) == 5:			#
                        interface_name = command_result[1].split(",")
                        interface_tx = command_result[2].split(",")
                        interface_rx = command_result[3].split(",")
                        sys_uptime = command_result[4]

                        # insert tx rx values in the database
                        for i in range(len(interface_name)):
                            sql = "INSERT INTO nms_devices_bandwidth(deviceid,interface,tx,rx) VALUES(%s,'%s',%s,%s)" % (
                                device_id, interface_name[i], interface_tx[i], interface_rx[i])
                            cursor.execute(sql)
                    # insert uptime values in database
                    sql = "SELECT COUNT(*) FROM nms_devices_uptime WHERE deviceid = %s" % (
                        device_id)
                    cursor.execute(sql)
                    countDevices = cursor.fetchone()[0]
                    if countDevices == 0:
                        # Insert Uptime details when last details not exist
                        sql = "INSERT INTO nms_devices_uptime(deviceid,uptime) VALUES(%s,'%s')" % (
                            device_id, sys_uptime)
                    else:
                        # Update Uptime details when last details exist
                        sql = "UPDATE nms_devices_uptime SET uptime = '%s' WHERE deviceid = %s" % (
                            sys_uptime, device_id)
                    cursor.execute(sql)
                    db.commit()

                    # display plugin message
                    plugin_message("System Uptime: " + sys_uptime)
                    if sys_uptime == STATE:
                        plugin_message(
                            "Device Not Connected or SNMP not Enable")
                        exit(1)
                    else:
                        exit(0)
                close_connection(db)
            else:
                plugin_message()
                exit(2)
    else:
        plugin_message()
        exit(2)
except MySQLdb.Error:
    plugin_message("Schema or Table does not exist")
    exit(2)
except ImportError:
    plugin_message("MySQL Module not exist in Python")
    exit(2)
except:
    # print sys.exc_info()
    plugin_message()
    exit(2)
