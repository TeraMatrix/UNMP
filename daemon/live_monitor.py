#!/usr/bin/python2.6

import socket,sys
from signal import signal, SIGTERM
import random
# importing pysnmp library 
import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.api import v2c
import time
import sys
import os
from daemon import Daemon
import rrdtool
import traceback
#import logging
#logging.basicConfig(filename='/omd/daemon/log/live_mon.log',format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)


def bulktable(oid,ip_address,port,community,agent='live-agent',max_value=20):
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address,str) and isinstance(oid,str) and isinstance(community,str) and isinstance(port,int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                oid = oid.strip('.')
                #print oid
                first_value = 0
                errorIndication, errorStatus, errorIndex, \
                     varBindTable = cmdgen.CommandGenerator().bulkCmd(
        cmdgen.CommunityData(str(agent), community),cmdgen.UdpTransportTarget((ip_address, port)), first_value, max_value, make_tuple(oid))
                             
                var_dict = {}
                
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[53] = str(errorIndication)
                    return
                    # handle 
                    
                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = errorStatus.prettyPrint()
                        success = 1
                        return
                        #print '%s at %s\n' % ( errorStatus.prettyPrint(),errorIndex and varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        #print varBindTable
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                #print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                                temp_split = name.prettyPrint().split(oid)      
                                if len(temp_split) > 1:
                                    pass
                                else:
                                    return
                                #print name.prettyPrint()      
                                oid_values_list = name.prettyPrint().split(oid)[1].strip('.').split('.')
                                #print oid_values_list
                                if len(oid_values_list) > 0:
                                    oid_no = oid_values_list.pop(0)
                                else: 
                                    success = 1
                                    return
                                if isinstance(val,v2c.IpAddress):
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
                                    #oid_values_list.pop(0)
                                    #print oid_values_list
                                    for i in oid_values_list:
                                        li.append(i)
                                    #print " li ",li
                                    li.append(value)
                                    #print " li 2",li
                                    var_dict[count] = li
                                    #print var_dict
                                else:
                                    count += 1
                                    li = var_dict[count]
                                    li.append(value)
                                    var_dict[count] = li
                                #print li,count
                                #print "li,count",li,count,var_dict,oid_li
                            
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
                #print traceback.print_exc(e)
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


def host_status(hostid,status,host_ip=None,prev_status = 0):
    """
    @note: Used to update host operation status and varify it
    """
    value = 0
    plugin_status = 0
    try:
        db = db_connect()
        if hostid:
            sel_query = """select status from host_status  where host_id = '%s'"""%(str(hostid))
        elif host_ip:
            sel_query = """select status from host_status  where host_ip = '%s'"""%(host_ip)
        else:
            value = 0 # error 100 
            return
        if status==None:
            value = 0 # error 100
            return 
        cursor = db.cursor()
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if len(result) > 0:
            if int(result[0][0]) == prev_status or int(result[0][0]) == int(status):
                if hostid:
                    up_query = """update host_status set status='%s' where host_id = '%s'"""%(status,hostid)
                elif host_ip:
                    up_query = """update host_status set status='%s' where host_ip = '%s'"""%(status,host_ip)
                cursor.execute(up_query)
                db.commit()
                value = 0
            else:
                value = result[0][0]
             
        else:
            value = 0 #value = 100 no row found
        cursor.close()
        db.close()
    except MySQLdb.Error as e:
        db.close()    
    except Exception as e:
        db.close()
    finally:
        return int(value)



        
        

mstat = 0
round_param = 15

def insert_data(file_name,timestamp,data):
    try:
        rrdtool.update(file_name,'%s:%s' % (timestamp,":".join(map(str,data))))
    except Exception,e:
        pass

def live_snmp():
    global snmp_param,table_dict,round_param
    try:
        ip_address = snmp_param.keys()[0]
        community =  snmp_param[ip_address][0]
        port =  snmp_param[ip_address][1]
        #agent = 'a'+ip_address.replace('.','')
        agent = 'a'+str(random.randint(2,1000))
        
        table_dict1 = {'table1_name':{'row1':'1','col1':'1','oid':'1','file':''}}
        if len(table_dict) < 1:
            round_param = 0
            return
        for table in table_dict:
            default = 0
            oid_value = table_dict[table]['oid']
            row = table_dict[table]['row']
            col = table_dict[table]['col']
            rrd_path = table_dict[table]['file']        
            time.sleep(1)
            snmp_result = bulktable(oid_value,ip_address,int(port),community,agent)
            rrd_insert_list = []
            if snmp_result['success'] == 0:
                temp_result = snmp_result['result']
                for item in row:
                    for temp_col in col:
                        if temp_result.get(item):
                            if len(temp_result[item]) > temp_col:
                                rrd_insert_list.append(temp_result[item][temp_col])
                            else:
                                rrd_insert_list.append(default)    
                        else:
                            rrd_insert_list.append(default)
            else:
                for item in row:
                    for temp_col in col:
                        rrd_insert_list.append(1)
            if os.path.isfile(rrd_path):
                insert_data(rrd_path,'N',rrd_insert_list)
            # call sirs function(rrd_insert_list) # first import your func in file
        
    except Exception,e:
        pass


class MyDaemon(Daemon):
    """
    this Class is calling main() and Daemonizing my current_clear_alarm daemon
    it extends Daemon class and provides start stop functionality for daemon
    """
    def run(self):
        try:
            global round_param,mstat
            signal(SIGTERM, lambda signum, stack_frame: exit(1))
            while(round_param):
                statn = os.stat(file_path).st_mtime
                if mstat != statn:
                    mstat = statn
                    round_param = 15
                    execfile(file_path,globals())        
                round_param -= 1
                global snmp_param
                ip_address = snmp_param.keys()[0]
                status_round = 5
                while status_round > 0:
                    status_round -= 1
                    param = host_status(None,13,ip_address)                    
                    if param == 0:
                        live_snmp()
                        host_status(None,0,ip_address,13)
                        break
                    else:
                        time.sleep(10)
                if round_param:
                    time.sleep(59)
                else:
                    statn = os.stat(file_path).st_mtime
                    if mstat != statn:
                        mstat = statn
                        round_param = 15
                        execfile(file_path,globals())
                    if round_param:
                        time.sleep(59)
                    else:
                        os.unlink(file_path)
                        break
            
            
        except Exception,e:
            print "Exception in current clear alarm :",str(e[-1])
        finally:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            host_status(None,0,ip_address,13)

root_pid_path = '/omd/daemon/tmp/rrd_pids'
mysql_file = '/omd/daemon/config.rg'

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        file_path = sys.argv[2]

        if os.path.isfile(file_path):
            pass
        else:
            print 'file not found'
            if 'stop' == sys.argv[1]:
                pass
            else:
                sys.exit(1)
        if(os.path.isfile(mysql_file)):       # getting variables from config file
            execfile(mysql_file)
        else:
            print " mysql file not exits : ",mysql_file
            sys.exit(1)
        live_daemon = MyDaemon(root_pid_path+"/"+file_path.split('/')[-1].split('.')[0]+'.pid')
        if 'start' == sys.argv[1]:
            live_daemon.start()
        elif 'stop' == sys.argv[1]:
            live_daemon.stop()
        elif 'restart' == sys.argv[1]:
            live_daemon.restart()
        elif 'status' == sys.argv[1]:
            live_daemon.status()
        else:
            print " Unknown command"
            print " Usage: unmp-clearAlarm status | start | stop | restart | help | log \n     Please use help option if you are using it first time" 
            sys.exit(2)
        sys.exit(0)

#def main():
#    
#    global round_param,mstat
#    
#    while(round_param):
#        statn = os.stat(file_path).st_mtime
#        if mstat != statn:
#            statm = statn
#            round_param = 12
#            execfile(file_path,globals())        
#        round_param -= 1
#        live_snmp()
#        time.sleep(10)
#    os.unlink(file_path)
#    
#main()    
