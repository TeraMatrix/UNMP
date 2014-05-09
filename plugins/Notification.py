#!/usr/bin/python
# import all the usefull modules.
import sys
# from mod_python import util,apache


# exit from program using sys.exit() with error code[0,1,2,3]
# 0 for OK
# 1 for Warning
# 2 for Critical
# 3 for Unknown


# get all the command line arguments
arg = sys.argv


# error message for this plugin
def plugin_message(message=""):
    if message == "":
        print "you are passing bad arguments."
    else:
        print message


try:
    # import mySQL module
    import MySQLdb

    if len(arg) > 1:
        if "--help" in arg or "-h" in arg:
            print """


ALARM NOTIFICATION:
----------------------------------
This plugin for check the alarm current table

For all alarm

	Example :   %s -i <172.22.0.110> -a <alarm> -o <all>

For Selected alaem

	Example :  %s -i <172.22.0.110> -a <alarm> -o <'13002|13015|13012'>
--------------------------------------

""" % (arg[0], arg[0])

        else:
            if ("-i" in arg) and ("-a" in arg) and ("-o" in arg) and (len(arg) == 7):
                ip_address = arg[arg.index("-i") + 1]
                                           # receive the ip address
                alarm_event_option = arg[arg.index(
                    "-a") + 1]        # receive alarm type
                option = arg[arg.index(
                    "-o") + 1]  # recive option for alarm and event ex all or pipe sepreated
                # site_name= __file__.split("/")[3]
                db = MySQLdb.connect(
                    "172.22.0.95", "root", "root", "nms_sample")
                cursor = db.cursor()
                if alarm_event_option == "alarm":
                    if option == "all":
                    # sql="Select
                    # trap_receive_date,trap_event_type,trap_event_id,manage_obj_name
                    # from trap_alarm_current where agent_id='%s' and
                    # alarm_event_type='%s'" %(ip_address,alarm)
                        sql = "Select trap_receive_date,trap_event_type,trap_event_id,manage_obj_name from trap_alarm_current where agent_id='%s' " % (ip_address)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if result == None or result == "" or result == ():
                            plugin_message("Alarm dose not exists")
                            cursor.close()
                            db.close()
                            sys.exit(0)
#			     return 2
                        else:
                            print "Alarm Exists  "
#                            print result
                            cursor.close()
                            db.close()
                            sys.exit(2)
                    else:
                        alarm_ids = option.split("|")
                        i = 1
                        sql = "SELECT trap_receive_date,trap_event_type,trap_event_id,manage_obj_name from trap_alarm_current where trap_event_id IN ("
                        for count in alarm_ids:
                            if i < len(alarm_ids):
                                sql += "'" + count + "',"
                            else:
                                sql += "'" + count + "'"
                            i += 1
                        sql += ")"
#			print sql
                        cursor.execute(sql)
                        result = cursor.fetchall()
#			print result
                        cursor.close()
                        db.close()
                        print "Alarm Exists "
                        sys.exit(2)

# This is for event Notification

            elif ("-i" in arg) and ("-e" in arg) and ("-o" in arg) and (len(arg) == 7):
                ip_address = arg[arg.index("-i") + 1]
                                           # receive the ip address
                alarm_event_option = arg[arg.index(
                    "-e") + 1]        # receive alarm type
                option = arg[arg.index(
                    "-o") + 1]  # recive option for alarm and event ex all or pipe sepreated
                # site_name= __file__.split("/")[3]
#		print "option"+str(option)
                db = MySQLdb.connect(
                    "172.22.0.95", "root", "root", "nms_sample")
                cursor = db.cursor()
                if alarm_event_option == "event":
                    if option == "all":
                    # sql="Select
                    # trap_receive_date,trap_event_type,trap_event_id,manage_obj_name
                    # from trap_alarm_current where agent_id='%s' and
                    # alarm_event_type='%s'" %(ip_address,alarm)
                        sql = "Select trap_receive_date,trap_event_type,trap_event_id,manage_obj_name from trap_alarms where agent_id='%s' and timestamp BETWEEN  (now() - interval 1 minute) and now()  " % (
                            ip_address)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if result == None or result == "" or result == ():
                            plugin_message("Events dose not exists")
                            cursor.close()
                            db.close()
                            sys.exit(0)
#			     return 2
                        else:
                            print "Events Exists \n "
#                            print result
                            cursor.close()
                            db.close()
                            sys.exit(2)
                    else:
                        event_names = option.split("|")
                        i = 1
                        sql = "SELECT trap_receive_date,trap_event_type,trap_event_id,manage_obj_name from trap_alarms where  timestamp BETWEEN  (now() - interval 1 minute) and now()  and trap_event_type IN ("
                        for count in event_names:
                            if i < len(event_names):
                                sql += "'" + count + "',"
                            else:
                                sql += "'" + count + "'"
                            i += 1
                        sql += ")"
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if result == None or result == "" or result == ():
                            plugin_message("Events dose not exists  ")
                            cursor.close()
                            db.close()
                            sys.exit(0)
                        else:
                            print "Events Exists \n "
#                            print result
                            cursor.close()
                            db.close()
                            sys.exit(2)

            else:
                plugin_message()
                sys.exit(1)


except MySQLdb.Error, e:
    if db.open:
        cursor.close()
        db.close()
    plugin_message("Schema or Table does not exist")
    print (str(e))
    sys.exit(2)
except ImportError:
    plugin_message("MySQL Module not exist in Python")
    sys.exit(2)
except Exception, e:
    if db.open:
        cursor.close()
        db.close()
    plugin_message()
    print str(e[-1])
    sys.exit(2)
finally:
    if db.open:
        cursor.close()
        db.close()
