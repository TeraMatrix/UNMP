#!/usr/bin/python2.6

import socket,sys
from signal import signal, SIGTERM
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
def pysnmp_get_table(oid,ip_address,port,community,agent):
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address,str) and isinstance(oid,str) and isinstance(community,str) and isinstance(port,int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                errorIndication, errorStatus, errorIndex, \
                             varBindTable = cmdgen.CommandGenerator().nextCmd(
                cmdgen.CommunityData(agent, community),cmdgen.UdpTransportTarget((ip_address, port)),make_tuple(oid))
                             
                var_dict = {}
                
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
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
                                oid_values_list = name.prettyPrint().split(oid)[1][1:].split('.')
                                if len(oid_values_list) == 3:
                                    oid_no,oid2, oid3 = oid_values_list
                                    is_oid2 = 1
                                elif len(oid_values_list) == 2:
                                    oid_no,oid3 = oid_values_list
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
        agent = 'a'+ip_address.replace('.','')
        
        table_dict1 = {'table1_name':{'row1':'1','col1':'1','oid':'1','file':''}}
        if len(table_dict) < 1:
            round_param = 0
            return
        for table in table_dict:
            default = 0
            oid_value = table_dict[table]['oid']
            row = table_dict[table]['row']
            col = table_dict[table]['col']
            row_count = table_dict[table].get('row_count',False)
            unreachable = table_dict[table].get('unreachable_value',-1)
            rrd_path = table_dict[table]['file']        
            snmp_result = pysnmp_get_table(oid_value,ip_address,int(port),community,agent)
            rrd_insert_list = []
            if snmp_result['success'] == 0:
                temp_result = snmp_result['result']
                if not row_count:
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
                    rrd_insert_list.append(len(temp_result))
            else:
                for item in row:
                    for temp_col in col:
                        rrd_insert_list.append(unreachable) 
            if os.path.isfile(rrd_path):
                insert_data(rrd_path,'N',rrd_insert_list)
            # call sirs function(rrd_insert_list) # first import your func in file
        
    except Exception,e:
        pass


url_dict={}
# monitoring data
url_dict['rssi']='peerstats.shtml'
url_dict['sync_loss']='syncclock.shtml'
url_dict['crc_phy']='cgi-bin/gettddmac.sh'
url_dict['interface']='cgi-bin/getstat.sh'


# status data
url_dict['odu100_raStatusTable']='raaccess.shtml'
url_dict['odu100_synchStatusTable']='syncstatus.shtml'
url_dict['odu100_nwInterfaceStatusTable']='cgi-bin/getstat.sh'

def odu100_peerNodeStatusTable(data):
    success = 1
    #print data
    dict_data={}
    try:
        s=data
        function_str="function GetPeerInfo(peer)";
        find_string="macAddress, linkStatus, ssid, tunnelStatus, numSlaves, rxRate, txRate, allocatedTxBW, allocatedRxBW, usedTxBW, usedRxBW, txBasicRate, rxBasicRate, sigStrength1, sigStrength2, txTime, rxTime, txLinkQuality, negotiatedMaxUplinkBW, negotiatedMaxDownlinkBW, linkDistance"
        left_hand_str="peernodestats"
        list_data=[]
        dict_data={}
        list_index=0
        count=1
        index=s.find(function_str)
        given=find_string.split(', ')
        req=['linkStatus', 'tunnelStatus', 'sigStrength1', 'macAddress', 'ssid', 'numSlaves', 'rxRate','txRate', 'allocatedTxBW', 'allocatedRxBW', 'usedTxBW',
 'usedRxBW', 'txBasicRate', 'sigStrength2', 'rxBasicRate', 'txLinkQuality', 'txTime', 'rxTime', 'negotiatedMaxUplinkBW', 'negotiatedMaxDownlinkBW', 'linkDistance']
        while 1:
            to_be_matched="case %s:"%(list_index+1)
            index_data=s.find(to_be_matched,index+1)
            #print index_data
            index_data_start=s.find(left_hand_str,index_data+1)
            index_data_end= s.find("break;",index_data_start+1)
            temp_str=s[index_data_start:index_data_end]
            #print temp_str
            temp_index=temp_str.find(find_string)
            li = []
            if temp_index!=-1:
                list_temp=temp_str[temp_index+1+len(find_string):].split(", ")
                list_temp[-1]=list_temp[-1].strip().replace('";',"")
                list_temp[2]=list_temp[2] if list_temp[2]!='<null>' else ''
                temp_dict = dict(zip(given,list_temp))
                for i in req:
                    li.append(temp_dict.get(i,""))                
                li.insert(0,list_index+1)
                li.insert(0,1)
                dict_data[count]=li
                li = []
                temp_dict = {}
            list_index=list_index+1
            count=count+1
            if list_index==15:
                break
        success = 0
        #print dict_data
    except Exception,e:
        print str(e)
        success = 1
    finally:
        return {'success':success,'result':dict_data} #list_data


def odu100_synchStatisticsTable(data):
    success = 1
    try:
        s=data
        function_str="Sync Lost Counter"
        find_string='<td align="left">'
        data_index=s.find(function_str)
        data_index_start=s.find(find_string,data_index+len(function_str))
        data_index_start=data_index_start+len(find_string)
        data_index_end=s.find("</td>",data_index_start)
        data= s[data_index_start:data_index_end]
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success':success,'result':{1:[1,data.strip()]}}
        else:
            return {'success':success,'result':{}}


def odu100_nwInterfaceStatisticsTable(data):
    success = 1
    try:
        num='num'
        nwifaces='nwifaces'
        name='name'
        rxPackets='rxPackets'
        txPackets='txPackets'
        rxBytes='rxBytes'
        txBytes='txBytes'
        rxErrors='rxErrors'
        txErrors='txErrors'
        rxDropped='rxDropped'
        txDropped='txDropped'
        macAddress='macAddress'
        operationalState='operationalState'
    
        di=eval(data)
        interface_statistics={}
        li=di['nwifaces']
        count=1
        for i in li:
            temp_statistics=[count,i['rxPackets'], i['txPackets'], i['rxBytes'], i['txBytes'], i['rxErrors'],i['txErrors'], i['rxDropped'], i['txDropped']]
            interface_statistics[count]=temp_statistics
            count=count+1
        #return {'interface_statistics':interface_statistics,"interface_status":interface_status}
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success':success,'result':interface_statistics}
        else:
            return {'success':success,'result':{}}        


def odu100_raTddMacStatisticsTable(data):
    success = 1
    try:
        num='num'
        tddmacs='tddmacs'
        rfChannelFrequency='rfChannelFrequency'
        rxPackets='rxPackets'
        txPackets='txPackets'
        rxErrors='rxErrors'
        txErrors='txErrors'
        rxDropped='rxDropped'
        txDropped='txDropped'
        rxCrcErrors='rxCrcErrors'
        rxPhyErrors='rxPhyErrors'
        di=eval(data)
        tdd_mac_statistics={}
        li=di['tddmacs']
        count=1
        for i in li:
            temp_tdd_mac=[1,i['rxPackets'], i['txPackets'], i['rxErrors'], i['txErrors'], i['rxDropped'], i['txDropped'], i['rxCrcErrors'], i['rxPhyErrors']]
            tdd_mac_statistics[count]=temp_tdd_mac
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success':success,'result':tdd_mac_statistics}
        else:
            return {'success':success,'result':{}}       


############################################ Status tables

def odu100_raStatusTable(data):
    success = 1
    try:
        s=data
        main_str_list=["Current Time Slot","Radio MAC Address","Radio Operational State","Unused Tx Time UL","Unused Tx Time DL"]
        find_string_list=['<td align="left">','<td align="left">','<td align="left"><div id="opstate">',   '<td align="left">', '<td align="left">']
        end_string_list=["</td>","</td>","</div></td>","</td>","</td>"]
        list_data=[1]
        for i in range(len(main_str_list)):
            main_str=main_str_list[i]
            find_string=find_string_list[i]
            end_string=end_string_list[i]
            data_index=s.find(main_str)
            data_index_start=s.find(find_string,data_index+len(main_str))
            data_index_start=data_index_start+len(find_string)
            data_index_end=s.find(end_string,data_index_start)
            data= s[data_index_start:data_index_end]
            list_data.append(data.strip())
        success = 0
    except Exception,e:
        #print str(e)
        success = 1
    finally:
        if success == 0:
            return {'success':success,'result':{1:list_data}}
        else:
            return {'success':success,'result':{}}

def odu100_synchStatusTable(data):
    success = 0
    try:
        s=data
        main_str_list=["Sync Operational State","Raster Time","Time Adjust","Percentage Downlink Transmit Time"]
        find_string_list=['<td align="left"><div id="operationalstate">', '<td align="left"><div id="rastertime">', '<td align="left">', '<td align="left"><div id="percentagedownlinktransmittime">']
        end_string_list=["</td>","</div></td>","</div></td>","</div></td>"]
        list_data=[1]
        for i in range(len(main_str_list)):
            main_str=main_str_list[i]
            find_string=find_string_list[i]
            end_string=end_string_list[i]
            data_index=s.find(main_str)
            data_index_start=s.find(find_string,data_index+len(main_str))
            data_index_start=data_index_start+len(find_string)
            data_index_end=s.find(end_string,data_index_start)
            data= s[data_index_start:data_index_end]
            list_data.append(int(data.strip()))
    except:
        success = 1
    finally:
        if success == 0:
            return {'success':success,'result':{1:list_data}}
        else:
            return {'success':success,'result':{}}

def odu100_nwInterfaceStatusTable(data):
    success = 1
    try:
        num='num'
        nwifaces='nwifaces'
        name='name'
        rxPackets='rxPackets'
        txPackets='txPackets'
        rxBytes='rxBytes'
        txBytes='txBytes'
        rxErrors='rxErrors'
        txErrors='txErrors'
        rxDropped='rxDropped'
        txDropped='txDropped'
        macAddress='macAddress'
        operationalState='operationalState'
        di=eval(data)
        interface_statistics=[]
        interface_status={}
        li=di['nwifaces']
        count=1
        for i in li:
            temp_statistics=[count, i['rxPackets'], i['txPackets'], i['rxBytes'], i['txBytes'], i['rxErrors'],i['txErrors'], i['rxDropped'], i['txDropped']]
            interface_statistics.append(temp_statistics)
            opstate=1 if i['operationalState']=='Enabled' else 0
            temp_status=[count, i['name'], opstate, i['macAddress']]
            interface_status[count]=temp_status
            count=count+1
        success = 0
    except Exception,e:
        #print " nw ",str(e)
        success = 1
    finally:
        if success == 0:
            return {'success':success,'result':interface_status}
        else:
            return {'success':success,'result':{}}






function_dict={}
# monitoring data
function_dict['rssi']=odu100_peerNodeStatusTable
function_dict['sync_loss']=odu100_synchStatisticsTable
function_dict['crc_phy']=odu100_raTddMacStatisticsTable
function_dict['interface']=odu100_nwInterfaceStatisticsTable

# status data
function_dict['odu100_raStatusTable']=odu100_raStatusTable
function_dict['odu100_synchStatusTable']=odu100_synchStatusTable
function_dict['odu100_nwInterfaceStatusTable']=odu100_nwInterfaceStatusTable



def cgi_opener(ip,username,password,table_list):
    try:
        success = 1
        url="http://"+ip+"/"
        result_dict={}
        if isinstance(url, str) and isinstance(username, str) and isinstance(password, str):
            loop = len(table_list)
            temp_list = deepcopy(table_list)
            while loop:
                table_list = deepcopy(temp_list)
                
                flag=1
                try:
                    for table in table_list:
                        if table=="odu100_raConfTable": # special case for odu100_raConfTable
                            #data_acl=url+"aclconfig.shtml"
                            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                            top_level_url = url
                            password_mgr.add_password(None, top_level_url, username, password)
                            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
                            opener = urllib2.build_opener(handler)
                            url_table=url+url_dict[table][0]
                            f = opener.open(url_table, None, 10)    
                            data_acl = f.read()
                            url_table=url+url_dict[table][1]
                            f = opener.open(url_table, None, 10)    
                            data_ra_access = f.read()
                            response_data=function_dict[table](data_acl,data_ra_access)
                            
                        else:
                            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                            top_level_url = url
                            password_mgr.add_password(None, top_level_url, username, password)
                            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
                            opener = urllib2.build_opener(handler)
                            url_table=url+url_dict[table]
                            f = opener.open(url_table, None, 10)    
                            data = f.read()
                            response_data=function_dict[table](data)
                        if response_data['success'] == 0:                             
                            result_dict[table]=response_data['result']
                        
                        temp_list.remove(table)
                        success=0
                except socket.error as sock_err:
                    success = 1
                    #print str(sock_err)
                    result_dict=str(sock_err)
                    break
                except urllib2.URLError,e:
                    success = 1
                    #print " URL Error "+str(e)
                    result_dict=str(e)
                    break        
                    #if str(e)=="<urlopen error [Errno 113] No route to host>":
                    #    success=0
                    #    break
                    
                except Exception,e:
                    #print str(e)
                    success=0
                    #pass
                loop -= 1
                if len(temp_list) < 1:
                    break
                
        else:
            success = 1
            #print " arguments are not proper : (url , username, password) all arguments should be as String"
            result_dict="arguments are not proper : (url , username, password) all arguments should be as String"
    except urllib2.URLError,e:
        success = 1
        result_dict=" URL Error "+str(e)         
    except Exception,e:
        success = 1
        result_dict="EXCEPTION : "+str(e)
    finally:
        response_dict = {}
        response_dict['success'] = success
        response_dict['result'] = result_dict
        return response_dict
    

def live_cgi():
    global snmp_param,table_dict,round_param
    try:
        ip_address = snmp_param.keys()[0]
        
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
            #snmp_result1 = pysnmp_get_table(oid_value,ip_address,int(port),community,agent)
            cgi_result = cgi_opener(ip_address,"admin","public",[table_name])
            rrd_insert_list = []
            if cgi_result['success'] == 0 and cgi_result['result'].has_key(table) and len(cgi_result['result'][table]) > 0:
                temp_result = cgi_result['result'][table]
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
            sleeptime = 60
            while(round_param):
                statn = os.stat(file_path).st_mtime
                if mstat != statn:
                    mstat = statn
                    round_param = 15
                    execfile(file_path,globals())        
                round_param -= 1
                
                live_snmp()  # or live_cgi
                
                global timeout
                try:
                    if timeout:
                        sleeptime = timeout
                except:
                    pass
                if round_param:
                    time.sleep(sleeptime)
                else:
                    statn = os.stat(file_path).st_mtime
                    if mstat != statn:
                        mstat = statn
                        round_param = 15
                        execfile(file_path,globals())
                    if round_param:
                        time.sleep(sleeptime)
                    else:
                        os.unlink(file_path)
                        break
            
            
        except Exception,e:
            print "Exception in current clear alarm :",str(e[-1])
        finally:
            if os.path.isfile(file_path):
                os.unlink(file_path)

root_pid_path = '/omd/daemon/tmp/rrd_pids'

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        file_path = sys.argv[2]

        if os.path.isfile(file_path):
            pass
        else:
            print 'file not found'
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

