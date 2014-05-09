#!/usr/bin/python2.6
"""
@author: Rahul Gautam
"""
try:
    import socket
    # importing pysnmp library
    import pysnmp
    import os
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    import sys
    from datetime import datetime,timedelta
    # import mySQL module
    import MySQLdb
except ImportError as e:
    print str(e[-1])
    raise SelfCreatedException("package Import Error ")
    sys.exit(2)


class SelfCreatedException(Exception):
    pass

def timetick_convert(value):
    sec = timedelta(seconds=int(int(value)/100))
    d = datetime(1,1,1) + sec
    return ("%d Days, %d Hours, %d Mins, %d Secs" % (d.day-1, d.hour, d.minute, d.second))


def get(ip_address,port,community='public'):
    try:
        if isinstance(ip_address,str) and isinstance(community,str) and isinstance(port,int):
            args = [
        cmdgen.CommunityData('test-agent', community),
        cmdgen.UdpTransportTarget((ip_address, port)),
    ]

            klass = cmdgen.CommandGenerator().getCmd
            #args.append(
            #        tuple(map(int, name.prettyPrint().split('.')))
            #    )
            args.append((1, 3, 6, 1, 2, 1, 1, 3, 0))
            success = 0
            response_dict = {}
            try:
                errorIndication, errorStatus, errorIndex, varBinds = klass(*args)

                if errorIndication:
                    response_dict[553] = str(errorIndication)
                    success = 1
                    return
                else:

                    if errorStatus > 0 and errorIndex != None:
                        response_dict[name.prettyPrint()] =  int(errorStatus) if errorStatus.isdigit() else str(errorStatus)
                        return

                    elif errorStatus == 0:
                        for name, val in varBinds:

                            if val != '' and val != None:   # if needed put that and val != 'No Such Instance currently exists at this OID'
                                response_dict[name.prettyPrint()] = timetick_convert(str(val))
                                return
                            else:
                                response_dict[102] = 'No Value present'
                                return


            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[551] = sock_errstr
            except pysnmp.proto.error.ProtocolError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'pyproto err '+str(err)
            except TypeError as err:
                response_dict = {}
                success = 1
                response_dict[99] = 'type err '+str(err)
            except Exception as e:
                response_dict = {}
                success = 1
                response_dict[99] = 'pysnmp err '+str(e)
        else:

            response_dict = {}
            success = 1
            response_dict[101] = 'parameters are not correct '

    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer '+str(e)

    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success
        final_responce_dict['result'] = response_dict
        return final_responce_dict



def db_connect():
    """
    Used to connect to the database :: return database object assigned in global_db variable
    """
    db_obj = 1
    try:
        db_obj = MySQLdb.connect(hostname,username,password,schema)
    except MySQLdb.Error as e:
        print str(e)
    except Exception as e:
        print "Exception in database connection "+str(e)
    finally:
        return db_obj




###### @@@ main program starts from here
# take argument by command line
arg=sys.argv

def main():
    try:

        # Open database connection
        exit_status = 1
        db,cursor = 1,1
        if arg.count('-i') and  arg.count('-p') :
            ip_address = arg[arg.index("-i") + 1]        # receive the ip address
            port_no = arg[arg.index("-p") + 1]       # receive port number
            snmp_flag = 1
            snmp_result_dict = get(ip_address,int(port_no))
            if snmp_result_dict['success'] == 0:
                snmp_flag = 0
                print " RESPONSE : OK "
                print "  Host Uptime - ",snmp_result_dict['result'].values()[0]
                exit_status = 0
            else:
                snmp_flag = 1
                exit_status = 2
                print " No response received before timeout "
                print "  ",snmp_result_dict['result'].values()[0]
            db = db_connect()
            if db == 1:
                raise SelfCreatedException(' db connection failed ')
                return
            else:
                cursor = db.cursor()
                
                # this is provide the host_id of ip_address
                status=0 # default value
                host_id=0
                sel_query="SELECT host_id from hosts WHERE ip_address='%s' and is_deleted = 0"%(ip_address)
                cursor.execute(sel_query)
                host_result=cursor.fetchall()
                if len(host_result)>0:
                    host_id=host_result[0][0]
                else:
                    raise SelfCreatedException(' host_id does not exist ')
                    return 
                
                # trap_event_id = 50001
                sel_query = "SELECT * FROM `trap_alarm_current` WHERE agent_id = '%s' and trap_event_id = 50001"%(ip_address)
                cursor.execute(sel_query)
                current_info=cursor.fetchall()
                now_dt = datetime.now()

                # this is provide the last event_id of ip_address from system alarm
                sel_query="SELECT trap_event_id from system_alarm_table WHERE agent_id='%s' order by timestamp desc limit 1"%(ip_address)
                cursor.execute(sel_query)
                result=cursor.fetchall()
                
                if len(result)>0:
                    status=result[0][0]

                if snmp_flag:
                    if len(current_info) > 0:
                        del_query = "DELETE FROM `trap_alarm_current` WHERE agent_id = '%s' and trap_event_id = 50001"%(ip_address)
                        cursor.execute(del_query)
                        db.commit()
                    ins_query = """INSERT INTO `trap_alarm_current` (`trap_alarm_current_id`, `event_id`, `trap_id`, `agent_id`, `trap_date`, `trap_receive_date`, `serevity`, `trap_event_id`, `trap_event_type`, `manage_obj_id`, `manage_obj_name`, `component_id`, `trap_ip`, `description`) VALUES (NULL, 'unmpSystemTrap', '.1.3.6.1.2.1.1.1.0','%s', '%s', '%s', 4, 50001, 'DEVICE_UNREACHABLE', 601, 'device', 701, '%s:%s', 'No response received from device before timeout')"""%(ip_address,now_dt,datetime.strftime(now_dt,'%a %b %d %H:%M:%S %Y'),ip_address,port_no)
                    cursor.execute(ins_query)
                    db.commit()
                    print " UPTIME  Trap Sent Successfully "
                    if (int(status)!=50001 or int(status)==0) and host_id!=0:
                        ins_query = """INSERT INTO `system_alarm_table` (`system_alarm_id`, `host_id`,`event_id`, `trap_id`, `agent_id`, `trap_date`, `trap_receive_date`, `serevity`, `trap_event_id`, `trap_event_type`, `manage_obj_id`, `manage_obj_name`, `component_id`, `trap_ip`, `description`) VALUES (NULL,%s,'unmpSystemTrap', '.1.3.6.1.2.1.1.1.0','%s', '%s', '%s', 4, 50001, 'DEVICE_UNREACHABLE', 601, 'device', 701, '%s:%s', 'No response received from device before timeout')"""%(host_id,ip_address,now_dt,datetime.strftime(now_dt,'%a %b %d %H:%M:%S %Y'),ip_address,port_no)
                        print ins_query
                        cursor.execute(ins_query)
                        db.commit()

                else:
                    if len(current_info) > 0:
                        del_query = "DELETE FROM `trap_alarm_current` WHERE agent_id = '%s' and trap_event_id = 50001"%(ip_address)
                        del_query2 = "DELETE FROM `trap_alarm_clear` WHERE agent_id = '%s' and trap_event_id = 50002"%(ip_address)
                        cursor.execute(del_query)
                        cursor.execute(del_query2)
                        db.commit()
                        ins_query = """INSERT INTO `trap_alarm_clear` (`trap_alarm_clear_id`, `event_id`, `trap_id`, `agent_id`, `trap_date`, `trap_receive_date`, `serevity`, `trap_event_id`, `trap_event_type`, `manage_obj_id`, `manage_obj_name`, `component_id`, `trap_ip`, `description`) VALUES (NULL, 'unmpSystemTrap', '.1.3.6.1.2.1.1.1.0','%s', '%s', '%s', 0, 50002, 'DEVICE_REACHABLE', 601, 'device', 701, '%s:%s', 'NOW response is OK')"""%(ip_address,now_dt,datetime.strftime(now_dt,'%a %b %d %H:%M:%S %Y'),ip_address,port_no)
                        cursor.execute(ins_query)
                        db.commit()
                        print " UPTIME  Trap Cleared Successfully "
                    
                    if (int(status)!=50002 or int(status)==0) and host_id!=0:
                        ins_query = """INSERT INTO `system_alarm_table` (`system_alarm_id`, `host_id`,`event_id`, `trap_id`, `agent_id`, `trap_date`, `trap_receive_date`, `serevity`, `trap_event_id`, `trap_event_type`, `manage_obj_id`, `manage_obj_name`, `component_id`, `trap_ip`, `description`) VALUES (NULL,%s,'unmpSystemTrap', '.1.3.6.1.2.1.1.1.0','%s', '%s', '%s', 4, 50002, 'DEVICE_REACHABLE', 601, 'device', 701, '%s:%s', 'NOW response is OK')"""%(host_id,ip_address,now_dt,datetime.strftime(now_dt,'%a %b %d %H:%M:%S %Y'),ip_address,port_no)
                        cursor.execute(ins_query)
                        db.commit()

        else:
            plugin_message()
            exit_status = 1
            #sys.exit(1)

    except ImportError as e:
        print "Import Error   "+str(e[-1])
        exit_status = 2 #sys.exit(2)
    except MySQLdb.Error as e:
        print "MySQLdb Exception    "+str(e[-1])
        exit_status = 2#sys.exit(1)
    except SelfCreatedException as e:
        print str(e)
        exit_status = 1#sys.exit(2)
    except Exception as e:
        print "main",str(e[-1])
        exit_status = 2#sys.exit(2)
    finally :
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()
        sys.exit(exit_status)

# function for error messages
def plugin_message(message = ""):
    if message == "":
        print "you are passing bad arguments."
    else:
        print message

# check the validation for command line argument
if len(arg)>2:
    MySql_file = '/omd/daemon/config.rg'
    if(os.path.isfile(MySql_file)):       # getting variables from config file
        execfile(MySql_file)
        main()
    else:
        print 'Not able to connect database'
        print ' > config.rg file not found on /omd/daemon path'
        sys.exit(2)

else:
    if "--help" in arg or "-h" in arg:
        print """
                SNMP UPTIME PLUGIN - NAGIOS
                --------------------------------
                This plugin checks snmp uptime for host

                \t./%s -i 192.168.1.1 -p 161
                \t-i\t Ip Address
                \t-p\tPort_no
                """ % (arg[0])
        sys.exit(2)

    else:
        plugin_message('-------->>>> Please pass the arguments and you can also check the passing argumnets by [python] [file name] --help or -h.')
        sys.exit(2)
