#!/usr/bin/python2.6
"""
@ Author            :    Rajendra Sharma
@author: Modified by Rahul Gautam
@ Project            :    UNMP
@ Version            :    0.1
@ File Name            :    walk1.py
@ Creation Date            :    1-September-2011
@date: 7-Jan-2012
@ Purpose            :    This plugin insert the data in multipal table.
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
#####################################################################################################

# import the packages

try:
    import socket,random
    # importing pysnmp library 
    import pysnmp
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto.api import v2c
    import os,math
    import sys
    import re
    import shlex, subprocess
    import commands
    from datetime import datetime
    import time
    # import mySQL module
    import MySQLdb
    from copy import deepcopy
except ImportError as e:
    print str(e[-1])
    raise SelfCreatedException("package Import Error ")
    sys.exit(2)


########################## NOTE
# Please Remember : when you add oid of table please add .1 at last 
# like if table oid is '.1.3.6.1.4.1.26149.2.2.11.2' then add .1 at last so new oid is '.1.3.6.1.4.1.26149.2.2.11.2.1'
# thats it 


ap25_table_dict = {'ap25_statisticsTable':'.1.3.6.1.4.1.26149.10.4.1.1.1',
                   'ap25_vapClientStatisticsTable':'.1.3.6.1.4.1.26149.10.4.3.1.1'}

main_dict = {
           'ap25':ap25_table_dict
        }
############################ Please read NOTE before addition of new table



global db,host_id
# take argument by command line 
arg=sys.argv


def ap25_vapclient(host_id,main_result_dict):
    try:
        exit_status = 0
        flag = 1
        global db
        if db ==1:
            raise SelfCreatedException(' can not connect to database ')
        f_cursor = db.cursor()
        dt = datetime.now()
        for vap in main_result_dict:
            result_dict = main_result_dict[vap]
            for k in result_dict:
                if flag:
                    exit_status = 1
                    flag = 0
                result_list = result_dict[k]
                result_list.append(dt)
                result_list.append(host_id)
                result_list.append(vap)
                result_list.append(result_list[1])
                
                result_tuple = tuple(result_list)
                try:
                    sql = "UPDATE ap25_vapClientStatisticsTable set `slNum` = '%s', `addressMAC`= '%s',  `aid`= '%s',  `chan`= '%s',  `txRate`= '%s', \
                    `rxRate` = '%s', `rssi` = '%s', `idle` = '%s', `txSEQ` = '%s', `rxSEQ` = '%s', `caps` = '%s', timestamp = '%s' \
                     WHERE `host_id` = '%s' and vap_id = '%s' and `addressMAC` = '%s' "%result_tuple
                    
                    if f_cursor.execute(sql) == 0:
                        #print " inserting "
                        result_list.pop()
                        result_tuple = tuple(result_list)
                        #print result_tuple
                        sql = "INSERT INTO `ap25_vapClientStatisticsTable` (`ap25_vapClientStatisticsTable_id`, `slNum`, `addressMAC`, `aid`, `chan`, `txRate`, `rxRate`, `rssi`, `idle`, `txSEQ`, `rxSEQ`, `caps`, timestamp, `host_id`, `vap_id`) \
                        VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%result_tuple
                        #print sql
                        f_cursor.execute(sql)
                    db.commit()
                    exit_status = 0
            
                except TypeError, e:
                    exit_status = 1
                    print "type Error in ap"    
    except MySQLdb.Error as e:
        print "MySQLdb Exception    "+str(e[-1])
        exit_status = 2        
    except SelfCreatedException as e:
        print str(e)
        exit_status = 2
    except Exception as e:
        print str(e[-1])
        exit_status = 2
    finally:
        if db != 1:
                f_cursor.close()
        return exit_status


def defult_data_insert(table_name,ip_address):
    try:
        exit_status = 1
        rx_packets, tx_packets, rx_err, tx_err = 1, 1, 1, 1

        global db,host_id
        if db ==1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        cursor = db.cursor()  
        
        if table_name.strip()=='ap25_statisticsTable':
            ins_query="INSERT INTO  `ap25_statisticsTable` (`ap25_systemInfo_id` ,`host_id` ,`index` ,`statisticsInterface` ,`statisticsRxPackets` ,`statisticsTxPackets` ,`statisticsRxError` ,`statisticsTxError` ,`timestamp`)VALUES (NULL , '%s', '0', 'eth0', '%s', '%s', '%s', '%s', '%s')"%(result, rx_packets, tx_packets, rx_err, tx_err, datetime.now())    
            cursor.execute(ins_query) 
            db.commit()                        
        exit_status = 1
        # close the connection
    except MySQLdb.Error as e:
        print "MySQLdb Exception    "+str(e[-1])
        exit_status = 2        
    except SelfCreatedException as e:
        print str(e)
        exit_status = 2
    except Exception as e:
        print str(e[-1])
        exit_status = 2
    finally :
        if db != 1:
            cursor.close()
        return exit_status

# --     default data insert close

def is_filled(table_list = []):
    try:
        return_value = 0
        
        global db,host_id
        if db ==1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        sel_query = None
        cursor = db.cursor()
        temp_list = deepcopy(table_list)
        
        try:              
            for table_name in temp_list:
                return_value = 0

                if table_name.strip()=='ap25_statisticsTable':
                    sel_query = "SELECT `statisticsRxPackets` ,`statisticsTxPackets` ,`statisticsRxError` ,`statisticsTxError` FROM `ap25_statisticsTable` WHERE ap25_systemInfo_id = (SELECT max(ap25_systemInfo_id) FROM `ap25_statisticsTable` WHERE host_id='%s')"%(result)
                    #print sel_query         
                if sel_query:
                    cursor.execute(sel_query)
                    sel_result = cursor.fetchall()
                    #print sel_result
                    if len(sel_result) > 0:
                        if len(sel_result[0]) == sel_result[0].count(1L):
                            return_value = 1
                        if return_value:
                            table_list.remove(table_name)
        # close the connection
        except MySQLdb.Error as e:
            print "MySQLdb Exception    "+str(e[-1])
            #return_value = 2
        except Exception as e:
            print " filler : ",str(e[-1])        
    except SelfCreatedException as e:
        print str(e)
        return_value = 2
    except Exception as e:
        print str(e[-1])
        return_value = 2
    finally :
        if db != 1:
            cursor.close()
        table_list.append(return_value)
        return table_list
    


def pysnmp_get_table(oid,ip_address,port,community):
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address,str) and isinstance(oid,str) and isinstance(community,str) and isinstance(port,int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                
                errorIndication, errorStatus, errorIndex, \
                             varBindTable = cmdgen.CommandGenerator().nextCmd(
                cmdgen.CommunityData('table-agent', community),cmdgen.UdpTransportTarget((ip_address, port)),make_tuple(oid))
                             
                var_dict = {}
                
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[53] = "NO SNMP RESPONSE RECEIVED BEFORE TIMEOUT"
                    return
                    # handle 
                    
                else:
                    if errorStatus:
                        err_dict[int(errorIndex)] = str(errorStatus)
                        success = 1
                        #print '%s at %s\n' % ( errorStatus.prettyPrint(),errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        is_oid2 = 0
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                #print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                                oid_values_list = name.prettyPrint().split(oid)[1][1:].split('.')
                                #print oid_values_list
                                if len(oid_values_list) == 3:
                                    oid_no,oid2, oid3 = oid_values_list
                                    is_oid2 = 1
                                #print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                                elif len(oid_values_list) == 2:
                                    oid_no,oid3 = oid_values_list
                                else: 
                                    success = 1
                                    return
                              

                                if isinstance(val,v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    if str(val).find('<null>'):
                                        value = str(val) #val.prettyPrint() #str(val) 
                                    else:
                                        value = 'NULL'

                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0
                                                                                
                                if flag == 0:
                                    count += 1                      
                                    li = []
                                    value = str(val) #val.prettyPrint() #str(val)
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
                                
                            
            except socket.error as (sock_errno, sock_errstr):
                success = 1
                err_dict[51] = sock_errstr                
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err '+str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err '+str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception '+str(e)
        else:
            success = 1
            err_dict[96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception as e:
        success = 1
        err_dict[98] = 'outer Exception '+str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = var_dict
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        #print var_dict
        return result_dict

def pysnmp_get_node(oid,ip_address,port,community):
    err_dict = {}
    success = 1
    var_dict = {}
    try:
        if isinstance(ip_address,str) and isinstance(oid,str) and isinstance(community,str) and isinstance(port,int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                
                errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('table-agent', community),cmdgen.UdpTransportTarget((ip_address, port)),make_tuple(oid))
                if errorIndication:
                    success = 1
                    err_dict[53] = "NO SNMP RESPONSE RECEIVED BEFORE TIMEOUT"
                    return
                    # handle 
                    
                else:
                    if errorStatus:
                        err_dict[int(errorIndex)] = "NO SNMP RESPONSE RECEIVED BEFORE TIMEOUT"
                        success = 1
                        #print '%s at %s\n' % ( errorStatus.prettyPrint(),errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                #print '%s = %s' % (name.prettyPrint(), val.prettyPrint())                                
                                oid_no = name.prettyPrint().split(oid)[1][1:].split('.')[0]
                                
                                if oid_li.count(oid_no) == 0:
                                    oid_li.append(oid_no)
                                    count = 0
                                    flag = 1
                                    if len(oid_li) == 1:
                                        flag = 0

                                if isinstance(val,v2c.IpAddress):
                                    value = str(val.prettyPrint())
                                else:
                                    value = str(val) #val.prettyPrint() #str(val)
                                                                                                                    
                                if flag == 0:
                                    count += 1                      
                                    li = []
                                    li.append(value)
                                    var_dict[count] = li
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    li.append(value)
                                    var_dict[count] = li
                                
            except socket.error as sock_err:
                success = 1
                err_dict[51] = str(sock_err)            
            except pysnmp.proto.error.ProtocolError as err:
                success = 1
                err_dict[99] = 'pyproto err '+str(err)
            except TypeError as err:
                success = 1
                err_dict[99] = 'type err '+str(err)
            except Exception as e:
                success = 1
                err_dict[99] = 'pysnmp exception '+str(e)
        else:
            success = 1
            err_dict[96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
    except Exception as e:
        success = 1
        err_dict[98] = 'outer Exception '+str(e)
    finally:
        result_dict = {}
        if success == 0:
            result_dict['success'] = success
            result_dict['result'] = var_dict
        else:
            result_dict['success'] = success
            result_dict['result'] = err_dict
        return result_dict

def single_set(ip_address,port,community,received_list):
    try:
        make_tuple = lambda x: tuple(int(i) for i in x.split('.'))      #@note: this lambda function used to convert a oid string to oid tuple (in a format required by pysnmp)  
        success = 0
        if isinstance(ip_address,str) and isinstance(community,str) and port != None and len(received_list) == 3:
            datatypes_dict = {'Integer32':v2c.Integer32,'Unsigned32':v2c.Unsigned32,'OctetString':v2c.OctetString,'DisplayString':v2c.OctetString,'Gauge32':v2c.Gauge32,'IpAddress':v2c.IpAddress,'Counter32':v2c.Counter32,'Counter64':v2c.Counter64}
            
            response_dict = {}
           
            oid_str,datatype,value = received_list
            
            snmp_args = [cmdgen.CommunityData('single-set', community),
                         cmdgen.UdpTransportTarget((ip_address, int(port))),
                         ]
            
            cmdClass = cmdgen.CommandGenerator().setCmd
            
            snmp_args.append((make_tuple(oid_str),datatypes_dict[datatype](value)))
            #print snmp_args
            try:
                
                errorIndication, errorStatus, errorIndex, varBinds = cmdClass(*snmp_args)
                                
                if errorIndication:
                    success = 1
                    response_dict[53] = "NO SNMP RESPONSE RECEIVED BEFORE TIMEOUT"  
                else:
                    if errorStatus > 0 and errorIndex != None:
                        success = 1
                        response_dict[str(errorStatus)] = errorStatus.prettyPrint()   
                        return                  
                        
                    elif errorStatus == 0:
                        #print " no error >>>>>>>>>"
                        #response_dict[0] = 'all_field_set_sucessfully' 
                        for name, val in varBinds:
                            response_dict[oid_str] = str(val)
                        return
            
            except socket.error as (sock_errno, sock_errstr):
                response_dict = {}
                success = 1
                response_dict[51] = sock_errstr                
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
                response_dict[99] = 'pysnmp exception '+str(e)
        else:
            response_dict = {}
            success = 1
            response_dict[97] = 'IP or Port or community not present'
    except Exception as e:
        response_dict = {}
        success = 1
        response_dict[98] = 'outer err '+str(e)
    finally:
        final_responce_dict = {}
        final_responce_dict['success'] = success 
        final_responce_dict['result'] = response_dict
        return final_responce_dict

def special_ap_walk(ip_address,port):
    get_community = 'public'
    set_community = 'private'
    vap_dict = {}
    vap_data_list = [] 
    vapSelection_oid = '1.3.6.1.4.1.26149.10.2.3.1'
    selectVap_oid =  '1.3.6.1.4.1.26149.10.2.3.1.2.0'
    vapClient_oid = '1.3.6.1.4.1.26149.10.4.3.1.1'
    success = 0 
    final_result_dict = {}
    try:
        vap_selc_dict = pysnmp_get_node(vapSelection_oid, ip_address, port, get_community)
        #print vap_selc_dict
        if vap_selc_dict['success'] == 0:
            vap_selc_list = vap_selc_dict['result'][1] if len(vap_selc_dict['result']) > 0 else []  
            
            if len(vap_selc_list) > 1:
                total_vap = int(vap_selc_list[0])
                select_vap = vap_selc_list[1]
                
                for vap in range(1,total_vap+1):
                    vap_data_list = []
                    #print " vap to set is ",vap
                    set_dict = single_set(ip_address, port,set_community,[selectVap_oid,'Integer32',vap])
                    
                    #print "set_dict",set_dict
                    
                    if set_dict['success'] == 0:
                        time.sleep(1)
                        result2_dict = pysnmp_get_table(vapClient_oid, ip_address, port, get_community) # basicVapSetup
                        #print "1",result2_dict
                        if result2_dict['success'] == 0:
                            #vap_data_list = result2_dict['result'][1] if len(result2_dict['result']) > 0 else []
                            #vap_dict[vap]=vap_data_list
                            vap_dict[vap]= result2_dict['result']
                                    
                        else:
                            return
                    else:
                        return
            else:
                success = 1
                final_result_dict = " No vap Selection Found "                                        
        else:
            success = 1
            final_result_dict = vap_selc_dict['result']
    except Exception,e:
        success = 1
        final_result_dict = str(e)
    finally:
        di = {}
        di['success']=success
        if success == 0:
            final_result_dict = vap_dict
        di['result'] = final_result_dict
        return di
    
    
#Exception class
class SelfCreatedException(Exception):
    def __init__(self,msg):
        print msg
        
def db_connect():
    """
    Used to connect to the database :: return database object assigned in global_db variable
    """
    db_obj = 1
    try:
        db_obj = MySQLdb.connect(hostname,username,password,schema)        
        #db_obj = MySQLdb.connect("172.22.0.95","root","root","nms_p")        
    except MySQLdb.Error as e:
        print str(e)
    except Exception as e:
        print "Exception in database connection "+str(e)
    finally:
        return db_obj


###### @@@ main program starts from here 

def main():
    try:
        # Open database connection
        exit_status = 1
        global db,host_id
        db = 1
        is_db_connect = 1
        if arg.count('-i') and  arg.count('-p') :
                ip_address = arg[arg.index("-i") + 1]        # receive the ip address
                port_no = arg[arg.index("-p") + 1]           # receive port number
                device_type =  'ap25'  #arg[arg.index("-d") + 1]       # receive device type
                snmp_flag = 0
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
                                                        
                for table_name in table_dict:
                    #print table_name
#                    if is_table:
#                        table_name = single_table
                        #print table_name
                    if table_name == 'ap25_vapClientStatisticsTable':
                        snmp_result_dict = special_ap_walk(str(ip_address),int(port_no))
                    else:
                        snmp_result_dict = pysnmp_get_table(str(table_dict[table_name][1:]),str(ip_address),int(port_no),'public')
                    # opening db connection
                    #print snmp_result_dict
                    if is_db_connect:
                           db = db_connect()
                           is_db_connect = 0
                           if db == 1:
                               raise SelfCreatedException(' db connection failed ')
                           else:
                               # select the host)id form hosts table
                               cursor = db.cursor()
                               sql="SELECT host_id from hosts where ip_address = '%s'"%ip_address
                               if cursor.execute(sql) == 0 or cursor.execute(sql) == None:
                                   plugin_message("host_id dosn't exists in hosts table")
                                   exit_status = 1
                                   return
                               else:
                                   host_id=cursor.fetchone()[0]
                               cursor.close()    
                    if snmp_result_dict['success'] == 0:    
                        #create sql query for insertion in table
                        result_dict = snmp_result_dict['result']
                        
                        if table_name == 'ap25_vapClientStatisticsTable':
                            if len(result_dict) > 0:
                                exit_status = ap25_vapclient(host_id,result_dict)
                                if exit_status == 0:
                                    table_list.remove(table_name)
                                    print "   SNMP RESPONSE : OK  "
                            else:
                                print "   SNMP RESPONSE : OK  "
                        else:
                            #sql="INSERT INTO %s values(null,'%s'"%(table_name,result)
                            ins_query = "INSERT INTO %s values "%(table_name)
                            flag = 1
                            ins_str = ""
                            date_time = datetime.now()
                            for i in result_dict:
                            
                                if flag == 1:
                                    ins_query += "(null, '%s'"%(host_id)
                                    ins_len = len(result_dict[i])
                                    for ln in xrange(ins_len):
                                        ins_str += " ,'%s'"
                                    flag = 0
                                else:
                                    ins_query += ", (null, '%s'"%(host_id)
                                     
                                ins_query += ins_str%tuple(result_dict[i])
                                ins_query += ", '%s')"%(date_time)
                            #print ins_query
                            cursor = db.cursor()                            
                            cursor.execute(ins_query) # execute the query 
                            db.commit()    # save the value in data base
                            cursor.close()
                            table_list.remove(table_name)
                            print "   SNMP RESPONSE : OK  "
                            exit_status = 0
                            #sys.exit(0)
                    else:
                        print snmp_result_dict['result'].values()[0]#,table_name
                        snmp_flag = 1
                        return_value = 0
                        if len(table_list) > 0:
                            table_list = is_filled(table_list)
                            return_value = table_list.pop()
                                
                        if return_value < 2:
                            for table_name in table_list:
                                exit_status = defult_data_insert(table_name,ip_address)
                        else:
                            exit_status = return_value                            
                        
                        return
                    
                    if is_table:
                        break
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
        exit_status = 2#sys.exit(2)
    except Exception as e:
        print "IN MAIN :  ",str(e[-1])
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
if len(arg)>3:
    MySql_file = '/omd/daemon/config.rg'
    if(os.path.isfile(MySql_file)):       # getting variables from config file
        execfile(MySql_file)
        main()
    else:
        print 'can not connect to database'
        print 'config.rg file not found on /omd/daemon path'
        sys.exit(2)
    
else:
  if "--help" in arg or "-h" in arg:
        print """
                MONITOR ODU16_NETWORK_INTERFACE_STATISTICS:
                --------------------------------
                This plugin gives you interface and tx/rx values
                
                For Inserting the value of ODU16 tx/rx into mySQL database:
                \t./%s -i 192.168.1.1 -p 161 -t table_name
                \t-i\t Ip Address
                \t-p\t Port_no
                \t for single table -t Table_Name
                """ % (arg[0])
        sys.exit(2)
        
  else:
    plugin_message('-------->>>> Please pass the arguments and you can also check the passing argumnets by [python] [file name] --help or -h.')
    sys.exit(2)


