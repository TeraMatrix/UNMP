#!/usr/bin/python2.6
"""
@ Author            :    Rajendra Sharma
@author: Modified by Rahul Gautam
@ Project            :    UNMP
@ Version            :    0.1
@ File Name          :    walk_v1.py 
@ Creation Date      :    1-September-2011
@date: 4-June-2012
@ Purpose            :    This plugin insert the data in multipal table. version 1 devices
@ Organisation       :       Code Scape Consultants Pvt. Ltd.
@ Copyright (c) 2011 Codescape Consultant Private Limited 
"""

#####################################################################################################
#
#
## walk for version 1 devices
#
# exit from program using sys.exit() with error code[0,1,2,3]
# 0 for OK
# 1 for Warning
# 2 for Critical
# 3 for Unknown
#
#####################################################################################################

# import the packages

try:
	import socket
	import random
	import os
	import sys
	# importing pysnmp library 
	from pysnmp.entity import engine, config
	from pysnmp.entity.rfc3413 import cmdgen
	from pysnmp.carrier.asynsock.dgram import udp
	from pysnmp.proto.api import v2c
	# extra for get_table
	from pysnmp.entity.rfc3413.oneliner import cmdgen as pycmdgen
	import time
	from datetime import datetime	
	import traceback
	import MySQLdb
	from copy import deepcopy
except ImportError as e:
    print str(e[-1])
    sys.exit(2)


#Exception class
class SelfCreatedException(Exception):
    pass
        

## for printing better name at output
name_table_dict = {'ccu_ccuRealTimeStatusTable':'CCU_REAL_TIME_STATUS',
                }


########################## NOTE
# Please Remember : when you add oid of table please add .1 at last 
# like if table oid is '.1.3.6.1.4.1.26149.2.2.11.2' then add .1 at last so new oid is '.1.3.6.1.4.1.26149.2.2.11.2.1'
# thats it 
ccu_table_dict = {'ccu_ccuRealTimeStatusTable':'1.3.6.1.4.1.26149.3.9.1'
          }

main_dict = {'ccu':ccu_table_dict,
        }
############################ Please read NOTE before addition of new table

error_dict = {0:'noError',
                       1:'tooBig packet',
                       2:'noSuchName',
                       3:'badValue',
                       4:'readOnly',
                       #5:'genErr',
                       6:'noAccess',
                       7:'wrongType',
                       8:'wrongLength',
                       9:'wrongEncoding',
                       10:'wrongValue',
                       11:'noCreation',
                       12:'inconsistentValue',
                       13:'resourceUnavailable',
                       14:'commitFailed',
                       15:'undoFailed',
                       16:'authorizationError',
                       17:'notWritable',
                       18:'inconsistentName',
                       50:'unKnown',
                       551:'networkUnreachable',
                       52:'typeError',
                       553:'Request Timeout.Please Wait and Retry Again',
                       54:'0active_state_notAble_to_lock',
                       55:'1active_state_notAble_to_Unlock',
                       91:'Arguments are not proper',
                       96:'InternalError',
                       97:'ip-port-community_not_passed',
                       98:'otherException',
                       99:'pysnmpException',
                       102:'Unkown Error Occured'}

global db, host_id
# take argument by command line 
arg = sys.argv


def pysnmp_get_table(oid, ip_address, port, community):
    err_dict = {}
    success = 1
    timeout = 20
    retries = 3
    try:
        if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port, int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                oid = oid.strip('.')
                errorIndication, errorStatus, errorIndex, \
                             varBindTable = pycmdgen.CommandGenerator().nextCmd(
                pycmdgen.CommunityData('tablev1-agent', community, 0), pycmdgen.UdpTransportTarget((ip_address, port), timeout, retries), make_tuple(oid))
                             
                var_dict = {}
                
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
                    # handle 
                    
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1
                        #print '%s at %s\n' % ( errorStatus.prettyPrint(),errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        is_oid2 = 0
                        #print varBindTable
                        #print
                        #print
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                #print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                                #print name.prettyPrint()      
                                oid_values_list = name.prettyPrint().split(oid)[1][1:].split('.')
                                if len(oid_values_list) == 3:
                                    oid_no, oid2, oid3 = oid_values_list
                                    is_oid2 = 1
                                elif len(oid_values_list) == 2:
                                    oid_no, oid3 = oid_values_list
                                else: 
                                    success = 1
                                    return
                                if isinstance(val, v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(val) #val.prettyPrint() #str(val)
                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0
                                                                                
                                if flag == 0:
                                    count += 1                      
                                    li = []
                                    if is_oid2:
                                        li.append(oid2)
                                    li.append(oid3)
                                    li.append(value)
                                    var_dict[count] = li
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    li.append(value)
                                    var_dict[count] = li
                            
            except socket.error as sock_err:
                success = 1
                err_dict[551] = str(sock_err)               
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err ' + str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err ' + str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception ' + str(e)
        else:
            success = 1
            err_dict[96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception as e:
        success = 1
        err_dict[98] = 'outer Exception ' + str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = var_dict
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        return result_dict
        

def defult_data_insert(table_name, ip_address, is_disable=1):
    try:
        exit_status = 1
        timestamp = datetime.now()
        
        ## ccu default data
        
        global db, host_id    
        if db == 1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        cursor = db.cursor()
        
        ## ccu  
        if table_name.strip() == 'ccu_ccuRealTimeStatusTable':
            ins_query = "INSERT INTO `ccu_ccuRealTimeStatusTable` (`host_id`, `ccuRTSIndex`, `ccuRTSSystemVoltage`, `ccuRTSSolarCurrent`, `ccuRTSSMPSCurrent`, `ccuRTSBatteryCurrent`, `ccuRTSLoadCurrent`, `ccuRTSBatterySOC`, `ccuRTSInternalTemperature`, `ccuRTSBatteryAmbientTemperature`, `ccuRTSSMPSTemperature`, `ccuRTSACVoltageReading`, `ccuRTSAlarmStatusByte`, `timestamp`) VALUES ('%s', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111','%s');" % (result, timestamp)      
            cursor.execute(ins_query)
            db.commit()
        ## eidu
        elif table_name.strip() == 'table_name':
			pass
            
        #elif table_name.strip()=='':
        #    ins_query=""                                    

        exit_status = 1
        #print ins_query
        # close the connection
    except MySQLdb.Error as e:
        #print ins_query
        print "MySQLdb Exception in ddb " + name_table_dict[table_name] + " : " + str(e[-1])
        exit_status = 2        
    except SelfCreatedException as e:
        print " DDB ",str(e)
        exit_status = 2
    except Exception as e:
        print " DDB ",str(e[-1])
        exit_status = 2
    finally :
        if db != 1:
            cursor.close()
        return exit_status


#fill_check_di = {} an idea

# --     default data insert close

def is_filled(table_list=[]):
    try:
        return_value = 0
        
        global db, host_id
        if db == 1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        sel_query = None
        cursor = db.cursor()
        temp_list = deepcopy(table_list)
        #print " is_filled ",table_list
        try:              
            #fill_di = {'table_name':'', 'host':''} #an idea
            for table_name in temp_list:
                return_value = 0
                
                ## ccu
                if table_name.strip() == 'ccu_ccuRealTimeStatusTable':                	
                    sel_query = "SELECT `ccuRTSIndex`, `ccuRTSSystemVoltage`, `ccuRTSSolarCurrent`, `ccuRTSSMPSCurrent`, `ccuRTSBatteryCurrent`, `ccuRTSLoadCurrent`, `ccuRTSBatterySOC`, `ccuRTSInternalTemperature`, `ccuRTSBatteryAmbientTemperature`, `ccuRTSSMPSTemperature`, `ccuRTSACVoltageReading`, `ccuRTSAlarmStatusByte` \
                    FROM `ccu_ccuRealTimeStatusTable` WHERE  ccu_ccuRealTimeStatusTable_id = (SELECT max(ccu_ccuRealTimeStatusTable_id) FROM ccu_ccuRealTimeStatusTable where host_id = '%s')" % (result)
                
                if sel_query:
                    cursor.execute(sel_query)
                    sel_result = cursor.fetchall()
                    #print sel_result
                    if len(sel_result) > 0:
                        if len(sel_result[0]) == map(str, sel_result[0]).count('1111111'):
                            return_value = 1
                        if return_value:
                            table_list.remove(table_name)
        # close the connection
        except MySQLdb.Error as e:
            print "MySQLdb Exception in filling " + name_table_dict[table_name] + " : " + str(e[-1])
            #print sel_query
            #return_value = 2
        except Exception as e:
            print " filler : ", str(e[-1])        
    except SelfCreatedException as e:
        print " Filler: ",str(e)
        return_value = 2
    except Exception as e:
        print " Filler: ",str(e[-1])
        return_value = 2
    finally :
        if db != 1:
            cursor.close()
        table_list.append(return_value)
        return table_list
    


#Exception class
class SelfCreatedException(Exception):
    pass
        
def db_connect():
    """
    Used to connect to the database :: return database object assigned in global_db variable
    """
    db_obj = 1
    try:
        db_obj = MySQLdb.connect(hostname, username, password, schema)        
        #db_obj = MySQLdb.connect("172.22.0.95","root","root","nms_p")        
    except MySQLdb.Error as e:
        print str(e)
    except Exception as e:
        print "Exception in database connection " + str(e)
    finally:
        return db_obj


def host_status(hostid, status, host_ip=None, prev_status=0):
    """
    @note: Used to update host operation status and varify it
    """
    value = 0
    plugin_status = 0
    try:
        db = db_connect()
        if hostid:
            sel_query = """select status,plugin_status from host_status  where host_id = '%s'""" % (str(hostid))
        elif host_ip:
            sel_query = """select status,plugin_status from host_status  where host_ip = '%s'""" % (host_ip)
        else:
            value = 0 # error 100 
            return
        if status == None:
            value = 0 # error 100
            return 
        cursor = db.cursor()
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if len(result) > 0:
            if int(result[0][0]) == prev_status or int(result[0][0]) == int(status):
                if hostid:
                    up_query = """update host_status set status='%s', plugin_status = 0 where host_id = '%s'""" % (status, hostid)
                elif host_ip:
                    up_query = """update host_status set status='%s', plugin_status = 0 where host_ip = '%s'""" % (status, host_ip)
                cursor.execute(up_query)
                db.commit()
                value = 0
            else:
                value = result[0][0]
            plugin_status = result[0][1]              
        else:
            value = 0 #value = 100 no row found
        cursor.close()
        db.close()
    except MySQLdb.Error as e:
        db.close()    
    except Exception as e:
        db.close()
    finally:
        return int(value), int(plugin_status)


def update_plugin_state(state, host_ip):
    """
    @note: Used to update host operation status and varify it
    """
    try:
        db = db_connect()
        up_query = """update host_status set plugin_status = %s  where host_ip = '%s'""" % (state, host_ip)
        cursor = db.cursor()
        cursor.execute(up_query)
        cursor.close()
        db.commit()
    except MySQLdb.Error as e:
        pass    
    except Exception as e:
        pass
    finally:
        db.close()
        

###### @@@ main program starts from here 

def main():
    try:
        ip_address = None
        # Open database connection
        exit_status = 1
        global db, host_id
        db = 1
        is_db_connect = 1
        if arg.count('-i') and  arg.count('-p') and arg.count('-d') :
            ip_address = arg[arg.index("-i") + 1]        # receive the ip address
            port_no = arg[arg.index("-p") + 1]           # receive port number
            device_type = arg[arg.index("-d") + 1]       # receive device type
            snmp_flag = 0
            is_exception = 1
            run_loop = 1
            table_dict = main_dict[device_type]
            is_table = 0
            if arg.count('-t'):
                is_table = 1
                single_table = arg[arg.index("-t") + 1]
            
            table_list = []
            is_fill_flag = 1
            if is_table:
                table_list.append(single_table)
            else:
                table_list = table_dict.keys()
            #print table_list
            
            #time.sleep(60)
            snmp_read = 'public'
            host_state, plugin_state = host_status(None, 9, ip_address)
            if host_state == 0:
                if is_db_connect:
                   db = db_connect()
                   if db == 1:
                       raise SelfCreatedException(' db connection failed ')
                   else:
                       # select the host)id form hosts table
                       is_db_connect = 0
                       cursor = db.cursor()
                       sql = "SELECT host_id,snmp_read_community from hosts where ip_address = '%s' and is_deleted = 0" % ip_address
                       if cursor.execute(sql) == 0 or cursor.execute(sql) == None:
                           plugin_message("host_id dosn't exists in hosts table")
                           exit_status = 1
                           return
                       else:
                           host_data = cursor.fetchall()
                           if len(host_data[0]) > 1:
                               host_id = str(host_data[0][0])
                               snmp_read = host_data[0][1]
                           else:
                               plugin_message("host_id dosn't exists in hosts table")
                               exit_status = 1
                               return
                           
                           #print host_id
                       cursor.close()

                for table_name in table_dict:
                    if is_db_connect == 0:
                        is_db_connect = 1
                        db.close()
                        
                    snmp_result_dict = pysnmp_get_table(str(table_dict[table_name]).strip('.'), str(ip_address), int(port_no), snmp_read) 
                    time.sleep(5)
                    #print snmp_result_dict
                    if is_db_connect:
                       db = db_connect()
                       if db == 1:
                           raise SelfCreatedException(' db connection failed ')
                                                          
                    if snmp_result_dict['success'] == 0:    
                        result_dict = snmp_result_dict['result']
                        if len(result_dict) > 0:
                            ins_query = "INSERT INTO %s values " % (table_name)
                            flag = 1
                            ins_str = ""
                            date_time = datetime.now()
                
                            for i in result_dict:
    
                                if flag == 1:
                                    ins_query += "(null, '%s'" % (host_id)
                                    ins_len = len(result_dict[i])
                                    for ln in xrange(ins_len):
                                        ins_str += " ,'%s'"
                                    flag = 0
                                else:
                                    ins_query += ", (null, '%s'" % (host_id)
                                     
                                ins_query += ins_str % tuple(result_dict[i])
                                ins_query += ", '%s')" % (date_time)
                            #print ins_query
                            cursor = db.cursor()                            
                            try:
                                cursor.execute(ins_query) # execute the query 
                                db.commit()               # save the value in data base
                            except Exception, e:
                                is_exception = 0
                                print name_table_dict[table_name], ":", e[1]                          
                            cursor.close()
                        table_list.remove(table_name)
                        if is_exception:
                            is_exception = 0
                            print "  RESPONSE : OK "
                        exit_status = 0
                        #sys.exit(0)
                    else:
                        #print snmp_result_dict['result']
                        host_status(None, 0, ip_address, 9)
                        temp_exit = 0
                        if error_dict.has_key(int(snmp_result_dict['result'].keys()[0])):
                            print " No Response,", snmp_result_dict['result'].values()[0]
                        else:
                            print " No Response, Unknown Error : ", snmp_result_dict['result'].values()[0]
                            temp_exit = 2
                        
                        snmp_flag = 1
                        return_value = 0
                        if not run_loop:
                            print name_table_dict[table_name], ", remain: ", len(table_list)
                            if len(table_list) > 0:
                                table_list = is_filled(table_list)
                                return_value = table_list.pop()
                                    
                            if return_value < 2:
                                for table_name in table_list:
                                    exit_status = defult_data_insert(table_name, ip_address)
                            else:
                                exit_status = return_value                            
                                
                            if temp_exit:
                                exit_status = temp_exit
                            return
                        else:
                            run_loop -= 1
                            #print name_table_dict[table_name]
                            t_list = is_filled([table_name])
                            #print t_list
                            table_list.remove(table_name)
                            return_value = t_list.pop()
                            if return_value < 2 and len(t_list) > 0:
                                exit_status = defult_data_insert(table_name, ip_address)
                            
                            
                    
                    if is_table:
                        host_status(None, 0, ip_address, 9)
                        break

            else:
                hstatus_dict = {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring', 14:'Status capturing', 15:'Refreshing Site Survey'}
                schedule_round = 3
                if plugin_state > schedule_round:
                    print " Not able to gather deivce statistics. "
                    print " Device is busy, Device %s is in progress." % hstatus_dict.get(int(host_state), "other operation")
                    db = db_connect()
                    is_db_connect = 0
                    if db == 1:
                        raise SelfCreatedException(' db connection failed ')
                    else:
                        # select the host)id form hosts table
                        cursor = db.cursor()
                        sql = "SELECT host_id from hosts where ip_address = '%s' and is_deleted = 0" % ip_address
                        if cursor.execute(sql) == 0 or cursor.execute(sql) == None:
                            plugin_message("host_id dosn't exists in hosts table")
                            exit_status = 1
                            return
                        else:
                            host_id = cursor.fetchone()[0]
                                                        
                        up_query = """update host_status set plugin_status = 0 where host_ip = '%s'""" % (ip_address)
                        cursor.execute(up_query)
                        db.commit()

                            #print host_id
                        cursor.close()
                    
                        return_value = 1
                        if len(table_list) > 0:
                            table_list = is_filled(table_list)
                            return_value = table_list.pop()
                                
                        if return_value < 2:
                            for table_name in table_list:
                                exit_status = defult_data_insert(table_name, ip_address)
                        else:
                            exit_status = return_value                            
                        
                        return
                else:
                    print "Service rescheduled"
                    print " Device is busy, Device %s is in progress." % hstatus_dict.get(int(host_state), "other operation")
                    update_plugin_state(plugin_state + 1, ip_address)    
            

                
        else:
            plugin_message()
            exit_status = 1
            #sys.exit(1)
        
    except MySQLdb.Error as e:
        print "MySQLdb Exception    " + str(e[-1])
        exit_status = 2
    except SelfCreatedException as e:
        exit_status = 2
    except Exception as e:
        print traceback.format_exc()
        print "IN MAIN :  ", str(e[-1])
        exit_status = 2
    finally:
        if ip_address:
            host_status(None, 0, ip_address, 9)
        if isinstance(db, MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()
        sys.exit(exit_status)

# function for error messages
def plugin_message(message=""):
    if message == "":
        print " BAD ARGUMENT PASSED TO PLUGIN "
    else:
        print message

# check the validation for command line argument
if len(arg) > 4:
    mysql_file = '/omd/daemon/config.rg'
    if(os.path.isfile(mysql_file)):       # getting variables from config file
        execfile(mysql_file)
        main()
    else:
        print 'config.rg file not found on /omd/daemon path'
        print ' So not able to connect to database '
        sys.exit(2)
    
else:
  if "--help" in arg or "-h" in arg:
        print """
                MONITOR DIFFERENT_STATISTICS_OF_DEVICES:
                --------------------------------
                How to use:
                \t./%s -i 192.168.1.1 -p 161 -d odu16
                \t-i\t Ip Address
                \t-p\t Port_no
                \t-d\t Device_type
                \t for single table -t Table_Name
                """ % (arg[0])
        sys.exit(2)
        
  else:
    plugin_message('-------->>>> Please pass right arguments.\n               for HELP type # python2.6 %s --help or -h.' % (arg[0]))
    sys.exit(2)



