#!/usr/bin/python2.6

#==============================================================================
#
# Author: Yogesh Kumar (ccpl)
#
# Purpose:
# This plugin gives you the number of connected clients
# through device cgi script.
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
# Insert total number of user which are connected with Access point
# into database
# Display Number of Connected User
# Return Status [0,1,2,3]
#
#==============================================================================

# import all the usefull modules.
import sys, subprocess, urllib2, base64, socket, xml.dom.minidom

# get all the command line arguments
arg = sys.argv

# constant variable which stores total VAP in an Access Point
VAP = 8

# 
socket.setdefaulttimeout(1)

# error message for this plugin
def plugin_message(message = ""):
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

# function to return XML tag text
def getText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

# call the cgi script to get connected user
def get_connected_user(ip,vap,auth_string):
	mac_list = []
	try:
		url = "http://%s/cgi-bin/ServerFuncs?Method=DisplayConnectedClients&VapId=%s" % (ip,vap)	# url for calling Access Point CGI command
		req = urllib2.Request(url)
		req.add_header("Authorization", "Basic %s" % auth_string)
		f = urllib2.urlopen(req)
		response = f.read()
		if response.find("No Connected Clients") == -1:
			#response ="<TABLE cellpadding='3' cellspacing='0' border='1'><TR><TD align='center' class='header'>SlNo</TD><TD align='center' class='header'>ADDR</TD><TD align='center' class='header'>AID</TD><TD align='center' class='header'>CHAN</TD><TD align='center' class='header'>TxRATE</TD><TD align='center' class='header'>RxRATE</TD><TD align='center' class='header'>RSSI</TD><TD align='center' class='header'>IDLE</TD><TD align='center' class='header'>TXSEQ</TD><TD align='center' class='header'>RXSEQ</TD><TD align='center' class='header'>CAPS</TD></TR><TR><TD class='header' align='center'>1</TD><TD align='center' class='header'>20:7c:8f:2e:80:42</TD><TD align='center' class='header'>1</TD><TD align='center' class='header'>6</TD><TD align='center' class='header'>11M</TD><TD align='center' class='header'>11M</TD><TD align='center' class='header'>68</TD><TD align='center' class='header'>120</TD><TD align='center' class='header'>63016</TD><TD align='center' class='header'>48480</TD><TD align='center' class='header'>ESs</TD></TR><TR><TD class='header' align='center'>1</TD><TD align='center' class='header'>10:7c:8f:2e:80:42</TD><TD align='center' class='header'>1</TD><TD align='center' class='header'>6</TD><TD align='center' class='header'>11M</TD><TD align='center' class='header'>11M</TD><TD align='center' class='header'>68</TD><TD align='center' class='header'>120</TD><TD align='center' class='header'>63016</TD><TD align='center' class='header'>48480</TD><TD align='center' class='header'>ESs</TD></TR><TR><TD class='header' align='center'>1</TD><TD align='center' class='header'>00:7c:8f:2e:80:42</TD><TD align='center' class='header'>1</TD><TD align='center' class='header'>6</TD><TD align='center' class='header'>11M</TD><TD align='center' class='header'>11M</TD><TD align='center' class='header'>68</TD><TD align='center' class='header'>120</TD><TD align='center' class='header'>63016</TD><TD align='center' class='header'>48480</TD><TD align='center' class='header'>ESs</TD></TR><TR>"
			response += "</TR></TABLE>"
			dom = xml.dom.minidom.parseString(response)
			td = dom.getElementsByTagName("TD")
			for i in range(12,len(td),11):
                		mac_list.append(getText(td[i].childNodes))
		return mac_list
	except xml.parsers.expat.ExpatError:
        	return mac_list
	except:
		return mac_list

# validate command line argument
# print help
try:
	# import mySQL module
	import MySQLdb

	if len(arg)>1:
		if "--help" in arg:
			print """
MONITOR NUMBER OF CONNECTED USER WITH ACCESS POINT:
---------------------------------------------------
This plugin gives you number of connected user with particular access point

For Inserting the number of connected user into mySQL database:
\t./%s -i 192.168.1.1 -s nms

\t-i\tAccess Point Ip Address
\t-s\tSite Name [e.g. nms]

""" % (arg[0])
			exit(2)
		else:

			if ("-i" in arg) and ("-s" in arg) and (len(arg) == 5):
				ip_address = arg[arg.index("-i") + 1]		# receive the ip address
				site_name = arg[arg.index("-s") + 1]		# receive site name
				execfile('/omd/sites/%s/share/check_mk/web/htdocs/nms_config.py' % site_name)
				# Open database connection
				db = open_database_connection()
				# prepare a cursor object using cursor() method
				cursor = db.cursor()

				# get the device_id,username and password from ip address
				sql = "SELECT id,username,password from nms_devices \
					WHERE ipaddress = '%s'" % (ip_address)
				cursor.execute(sql)
				result = cursor.fetchone()

				# check device exist or not in the database
				if result == None:
					plugin_message("Device does not exist in Database");
					exit(1)
				else:
					device_id = result[0]			# get device_id
					device_user_name = result[1]		# get device_user_name
					device_password = result[2]		# get device_password
					connected_user = 0			# set initially connected user

					# create authentication string
					auth_string = base64.encodestring("%s:%s" % (device_user_name,device_password))
					
					connected_user = 0
					for v in range(VAP):
						mac = get_connected_user(ip_address,(v+1),auth_string)
						connected_user += len(mac)
						for m in mac:
							sql = "SELECT count(*) FROM nms_devices_connected_user WHERE deviceid = %s AND mac = '%s' AND vap = %s" % (device_id,m,(v+1))
							cursor.execute(sql)
							count = cursor.fetchone()[0]
							if count == 0:
								sql = "INSERT INTO nms_devices_connected_user(create_timestamp,deviceid,mac,vap) VALUES(now(),%s,'%s',%s);" % (device_id,m,(v+1))
							else:
								sql = "UPDATE nms_devices_connected_user SET timestamp = now(), create_timestamp = create_timestamp WHERE deviceid = %s AND mac = '%s' AND vap = %s" % (device_id,m,(v+1))
							cursor.execute(sql)
					db.commit()
					# display plugin message
					plugin_message("Connected User: %s" % connected_user)
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
except :
	#print sys.exc_info()
	plugin_message()
	exit(2)
