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
    import socket
    import random
    import os
    import sys
    # importing pysnmp library 
#    import pysnmp
    from pysnmp.entity import engine, config
    from pysnmp.entity.rfc3413 import cmdgen
    from pysnmp.carrier.asynsock.dgram import udp
#    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto.api import v2c
    from datetime import datetime
    # import mySQL module
    import MySQLdb
    import time
    from copy import deepcopy
except ImportError as e:
    print str(e[-1])
    sys.exit(2)


## for printing better name at output
name_table_dict = {'get_odu16_synch_statistics_table':'SYNC_STATISTICS',
                   'get_odu16_nw_interface_statistics_table':'NW_IFACE_STATISTICS',
                   'get_odu16_ra_tdd_mac_statistics_entry':'TDD_STATISTICS',
                   'get_odu16_peer_node_status_table':'PEER_NODE_STATUS',
                   'idu_linkStatusTable':'LINK_STATUS',
                   'idu_e1PortStatusTable':'E1_PORT_STATUS',
                   'idu_linkStatisticsTable':'LINK_STATISTICS',
                   'idu_tdmoipNetworkInterfaceStatisticsTable':'TDMOIP_STATISTICS',
                   'idu_iduNetworkStatisticsTable':'NETWORK_STATISTICS',
                   'idu_portstatisticsTable':'PORT_STATISTICS',
                   'idu_swPrimaryPortStatisticsTable':'SW_PORT_STATISTICS',
                   'idu_portSecondaryStatisticsTable':'PORT_SEC_STATISTICS',
                   'odu100_peerNodeStatusTable':'PEER_NODE_STATUS',
                   'odu100_raTddMacStatisticsTable':'TDD_MAC_STATISTICS',
                   'odu100_nwInterfaceStatisticsTable':'NW_IFACE_STATISTICS',
                   'odu100_synchStatisticsTable':'SYNC_STATISTICS',
                   'odu100_peerTunnelStatisticsTable':'PEER_TUNNEL_STATISTICS',
                   'odu100_peerLinkStatisticsTable':'PEER_LINK_STATISTICS',
                   'odu100_peerConfigTable':'PEER_CONFIG_STATISTICS',
                   'odu100_raStatusTable':'RA_STATUS',
                   'odu100_nwInterfaceStatusTable':'NW_IFACE_STATISTICS',
                   'odu100_synchStatusTable':'SYNC_STATISTICS',
                   'ap25_vapClientStatisticsTable':'VAP_CLIENT_STATISTICS',
             	   'ap25_statisticsTable':'AP_STATISTICS'
                }


########################## NOTE
# Please Remember : when you add oid of table please add .1 at last 
# like if table oid is '.1.3.6.1.4.1.26149.2.2.11.2' then add .1 at last so new oid is '.1.3.6.1.4.1.26149.2.2.11.2.1'
# thats it 
odu16_table_dict = {'get_odu16_synch_statistics_table':'.1.3.6.1.4.1.26149.2.2.11.2.1',
          'get_odu16_nw_interface_statistics_table':'.1.3.6.1.4.1.26149.2.2.12.3.1',
          'get_odu16_ra_tdd_mac_statistics_entry':'.1.3.6.1.4.1.26149.2.2.13.7.3.1',
          'get_odu16_peer_node_status_table':'.1.3.6.1.4.1.26149.2.2.13.9.2.1'
          }

idu4_table_dict = {'idu_linkStatusTable':'.1.3.6.1.4.1.26149.2.1.3.1.1',
            'idu_e1PortStatusTable':'.1.3.6.1.4.1.26149.2.1.3.2.1',
            'idu_linkStatisticsTable':'.1.3.6.1.4.1.26149.2.1.4.2.1',
            'idu_tdmoipNetworkInterfaceStatisticsTable':'.1.3.6.1.4.1.26149.2.1.4.1.1',
            'idu_iduNetworkStatisticsTable':'.1.3.6.1.4.1.26149.2.1.4.3.1' ,
            'idu_portstatisticsTable':'.1.3.6.1.4.1.26149.2.1.6.9.1',
            'idu_swPrimaryPortStatisticsTable':'.1.3.6.1.4.1.26149.2.1.4.4.1',
            'idu_portSecondaryStatisticsTable':'.1.3.6.1.4.1.26149.2.1.4.5.1'
        }

odu100_table_dict = {'odu100_peerNodeStatusTable':'.1.3.6.1.4.1.26149.2.2.13.9.2.1',
            'odu100_raTddMacStatisticsTable':'.1.3.6.1.4.1.26149.2.2.13.7.3.1',
            'odu100_nwInterfaceStatisticsTable':'.1.3.6.1.4.1.26149.2.2.12.3.1',
            'odu100_synchStatisticsTable':'.1.3.6.1.4.1.26149.2.2.11.2.1',
            #'odu100_peerTunnelStatisticsTable':'1.3.6.1.4.1.26149.2.2.13.9.3.1',
            #'odu100_peerLinkStatisticsTable':'1.3.6.1.4.1.26149.2.2.13.9.4.1',
            'odu100_raStatusTable':'1.3.6.1.4.1.26149.2.2.13.2.1',
            'odu100_nwInterfaceStatusTable':'1.3.6.1.4.1.26149.2.2.12.2.1',
            'odu100_synchStatusTable':'1.3.6.1.4.1.26149.2.2.11.3.1',
         }

ap25_table_dict = {'ap25_vapClientStatisticsTable':'.1.3.6.1.4.1.26149.10.4.3.1.1',
          'ap25_statisticsTable':'.1.3.6.1.4.1.26149.10.4.1.1.1'
          }

main_dict = {'odu16':odu16_table_dict,
           'odu100':odu100_table_dict,    
           'idu4':idu4_table_dict,
           'ap25':ap25_table_dict
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

global db,host_id
# take argument by command line 
arg=sys.argv

import MySQLdb
#client_details=((1, 0, '20:7c:8f:2e:80:44', 1, 6, '11M', '11M', 9, 8, 500, 1500, '22877'),)

#client_info=(1, 0, '20:7c:8f:2e:80:00', 1, 6, '11M', '11M', 9, 8, 50, 200, '22877')
#ap_id = 10

#now=datetime.datetime.now()
mac_index=2
tx_index=9
rx_index=10
rssi_index=7
vap_index=0
table_client_tx_index=3 #8 # table ap_client_details
table_client_rx_index=4 #9 # table ap_client_details
table_ap_tx_index=12 # table ap_client_ap_data
table_ap_rx_index=13 # table ap_client_ap_data
now=datetime.now()
#client_mac=client_info[mac_index]


##################### add functions

def add_new_client(client,ap_id,now):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="INSERT INTO `ap_client_details` (`client_id`, `client_name`, `mac`, `total_tx`, `total_rx`, `first_seen_time`, `first_seen_ap_id`, `last_seen_time`, `last_seen_ap_id`) \
		    VALUES (NULL, '', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(client[mac_index],client[tx_index],client[rx_index],now,ap_id,now,ap_id)
		cursor.execute(sql)
		lastrow=cursor.lastrowid
		db.commit()
		sql="UPDATE ap_client_details set client_name='client_%s' where client_id = '%s '"%(str(lastrow),str(lastrow))
		cursor.execute(sql)
		db.commit()
		cursor.close()
#		db.close()
		result_dict={"success":0}
		result_dict["result"]=[lastrow,client[mac_index]]
		result_dict["message"]="new client inserted"
		return result_dict
    except Exception,e:
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict
	    

def add_ap_connected_client(client_id,client_mac,ap_id,now):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
#		db=db_connect()
		cursor=db.cursor()
		sql="UPDATE ap_connected_client SET state='0' where client_id='%s' and client_mac='%s' "%(client_id,client_mac)
		cursor.execute(sql)
		db.commit()
		sql="INSERT INTO `ap_connected_client` (`ap_connected_client_id`, `host_id`, `client_id`, `client_mac`, `state`) VALUES (NULL, %s, %s, '%s', '1')" %(ap_id,client_id,client_mac)
		cursor.execute(sql)
		db.commit()
#		db.close()
		#print "ap connected client added"
		result_dict={"success":0}
		result_dict["result"]=[client_id,client_mac]
		result_dict["message"]="ap connected client added"
		return result_dict
    except Exception,e:
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict
		
		
def add_ap_client_ap_data(client_id,client_info,ap_id,now):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="INSERT INTO `ap_client_ap_data` (`ap_client_ap_data_id`, `host_id`, `client_id`, `client_mac`, `vap_id`, `slNum`, `aid`, `chan`, `txRate`, `rxRate`, `rssi`, `idle`, `total_tx`, `total_rx`, `caps`, `timestamp`) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(ap_id, client_id, client_info[mac_index], client_info[0], client_info[1], client_info[3],client_info[4],client_info[5],client_info[6],client_info[7],client_info[8],client_info[9],client_info[10],client_info[11],now)
		cursor.execute(sql)
		db.commit()
		#db.close()
		#print "ap client ap data added"
		result_dict={"success":0}
		result_dict["result"]=[client_id,client_mac]
		result_dict["message"]="ap client ap data added"
		return result_dict
    except Exception,e:
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict		
		
		
##################### update functions		

def clear_clients(ap_id):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="UPDATE ap_connected_client SET state='0' where host_id='%s' "%(ap_id)
		cursor.execute(sql)
		db.commit()
		cursor.close()
		#db.close()
		#print "ap connected client set to default values"
		result_dict={"success":0}
		result_dict["result"]=[0,0]
		result_dict["message"]="ap connected client set to default values"
		return result_dict
    except Exception,e:
	    #print str(e)
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict
		






def update_ap_connected_client(client_id,client_mac,ap_id,now):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="UPDATE ap_connected_client SET state='0' where client_id='%s' and client_mac='%s' "%(client_id,client_mac)
		cursor.execute(sql)
		db.commit()
		sql="UPDATE `ap_connected_client` set  state ='1' where host_id='%s' and client_id='%s' and client_mac='%s' " %(ap_id,client_id,client_mac)
		cursor.execute(sql)
		db.commit()
		cursor.close()
		#db.close()
		#print "ap connected client updated"
		result_dict={"success":0}
		result_dict["result"]=[client_id,client_mac]
		result_dict["message"]="ap connected client updated"
		return result_dict
    except Exception,e:
	    #print str(e)
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict
		
def update_client(client_info,ap_id,now,client_id):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="SELECT * FROM ap_client_details where client_id = '%s' " %(client_id)
		cursor.execute(sql)
		result = cursor.fetchall()
		if len(result)>0:
			result=result[0]
			old_tx = result[table_client_tx_index]
			old_rx = result[table_client_rx_index]
			new_tx = int(client_info[tx_index])
			new_rx = int(client_info[rx_index])
			diff_tx = int(new_tx)-int(old_tx)
			diff_rx = int(new_rx)-int(old_rx)
			if diff_tx>0:
				new_tx = old_tx + diff_tx
			elif diff_tx<0:
				new_tx = old_tx + new_tx
	
	
			if diff_rx>0:
				new_rx = old_rx + diff_rx
			elif diff_rx<0:
				new_rx = old_rx + new_rx

			sql="UPDATE ap_client_details set  total_tx=%s, total_rx=%s, last_seen_time='%s', last_seen_ap_id=%s where client_id = '%s'"%(new_tx,new_rx,now,ap_id,client_id)
			cursor.execute(sql)
			db.commit()
			cursor.close()
			#db.close()
			#print "client updated"
			result_dict={"success":0}
			result_dict["result"]=[]#[client_id,client_mac]
			result_dict["message"]="details of  client updated"
			return result_dict
		else:
			result_dict = add_new_client(client,ap_id,now)
			cursor.close()
			db.close()
			return result_dict
    except Exception,e:
	    #print str(e)
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict

				
def update_ap_client_ap_data(client_info,ap_id,now,client_id):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="SELECT * FROM ap_client_ap_data where client_id = '%s' and host_id='%s' " %(client_id,ap_id)
		cursor.execute(sql)
		result = cursor.fetchall()
		if len(result)>0:
			result=result[0]
			old_tx = result[table_ap_tx_index]
			old_rx = result[table_ap_rx_index]
			new_tx = int(client_info[tx_index])
			new_rx = int(client_info[rx_index])
			diff_tx = int(new_tx)-int(old_tx)
			diff_rx = int(new_rx)-int(old_rx)
			if diff_tx>0:
				new_tx = old_tx + diff_tx
			elif diff_tx<0:
				new_tx = old_tx + new_tx

			if diff_rx>0:
				new_rx = old_rx + diff_rx
			elif diff_rx<0:
				new_rx = old_rx + new_rx

			sql="UPDATE ap_client_ap_data set  vap_id='%s' , slNum='%s' , aid='%s' , chan='%s' , txRate='%s' , rxRate='%s' , rssi='%s' , idle='%s' , total_tx='%s' , total_rx='%s' , caps='%s' , timestamp ='%s' where client_id = '%s' and host_id='%s' "%(client_info[0], client_info[1], client_info[3],client_info[4],client_info[5],client_info[6],client_info[7],client_info[8],new_tx,new_rx,client_info[11],now,client_id,ap_id)
			cursor.execute(sql)
			db.commit()
			cursor.close()
			#db.close()
			#print "ap client ap data updated"
			result_dict={"success":0}
			result_dict["result"]=[]#[client_id,client_mac]
			result_dict["message"]="ap client ap data updated"
			return result_dict
		else:
			cursor.close()
			#db.close()
			result_dict=add_ap_client_ap_data(client_id,client_info,ap_id,now)
			return result_dict
    except Exception,e:
	    #print str(e)
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict
		        
def is_new_client(client_mac):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="SELECT client_id FROM ap_client_details where mac = '%s' " %(client_mac)
		cursor.execute(sql)
		result=cursor.fetchall()
		cursor.close()
		#db.close()
		result_dict={"success":0}
		if len(result)>0:
			result_dict["result"]=result[0][0]
		else:
			result_dict["result"]=-1
		result_dict["message"]=""
		return result_dict
    except Exception,e:
        result_dict={"success":1,"result":str(e),"message":""}
        return result_dict

def is_new_ap_client(client_mac,ap_id):
    global db
    try:
		#db=MySQLdb.connect("localhost","root","root","nmsp")
		#db=db_connect()
		cursor=db.cursor()
		sql="SELECT client_id FROM ap_connected_client where client_mac = '%s' and host_id='%s' " %(client_mac,ap_id)
		cursor.execute(sql)
		result=cursor.fetchall()
		cursor.close()
		#db.close()
		result_dict={"success":0}
		if len(result)>0:
			result_dict["result"]=result[0][0]
		else:
			result_dict["result"]=-1
		result_dict["message"]=""
		return result_dict
    except Exception,e:
	    print str(e)
	    result_dict={"success":1,"result":str(e),"message":""}
	    return result_dict



def insert_ap_client_data(client_info,ap_id,now):
	client_mac=client_info[mac_index]
	result_dict=is_new_client(client_mac)		
	if result_dict["success"]==0:
		client_id=result_dict["result"]
		if client_id==-1:        # it doesn't exists ie new client
			client_dict=add_new_client(client_info,ap_id,now)  
			if client_dict["success"]==0:
				client_list=client_dict["result"] 
				client_id=client_list[0]
				#print client_dict
				ap_connected_client_dict=add_ap_connected_client(client_id,client_mac,ap_id,now)
				#print ap_connected_client_dict
				ap_client_ap_data=add_ap_client_ap_data(client_id,client_info,ap_id,now)
				#print ap_client_ap_data
			else:
				#print result_dict["result"]	
				pass

		else:
			#print update_client(client_info,ap_id,now,client_id)
			update_client(client_info,ap_id,now,client_id)
			new_ap_client_dict = is_new_ap_client(client_mac,ap_id)
			#print new_ap_client_dict
			if new_ap_client_dict["success"] == 0:
				new_ap_client=new_ap_client_dict["result"]
				#print "new_ap_client",new_ap_client
				if new_ap_client !=-1: # it doesn't exists in this table ie new client for this table
					update_ap_connected_client(client_id,client_mac,ap_id,now)
					update_ap_client_ap_data(client_info,ap_id,now,client_id)
				else:
					ap_connected_client_dict=add_ap_connected_client(client_id,client_mac,ap_id,now)
					#print ap_connected_client_dict
					
					ap_client_ap_data=add_ap_client_ap_data(client_id,client_info,ap_id,now)
					#print ap_client_ap_data
			else:
				#print new_ap_client_dict["result"]
				pass
	else:
		#print result_dict["result"]
		pass
		
def ap_walk_for_clients(ap_id,client_data,now):
	clear_clients(ap_id)
	for client in client_data:
		insert_ap_client_data(client_data[client],ap_id,now)
#insert_ap_client_data(client_mac,client_info,ap_id,now)

######################################################### end of mahipal's code



def defult_data_insert(table_name,ip_address,is_disable=1):
    try:
        exit_status = 1
        timestamp=datetime.now()
        #print " de ",table_name
        #if is_disable:
        #nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111

        global db,host_id    
        if db ==1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        cursor = db.cursor()        
        if table_name.strip()=='ap25_vapClientStatisticsTable':
            ins_query="INSERT INTO `ap25_vapClientStatisticsTable` (`ap25_vapClientStatisticsTable_id`, `host_id`, `vap_id`, `slNum`, `addressMAC`, `aid`, `chan`, `txRate`, `rxRate`, `rssi`, `idle`, `txSEQ`, `rxSEQ`, `caps`, `timestamp`) VALUES ( NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');"%(result,1,0,'','1111111','1111111','1111111','1111111','1111111','1111111','1111111','1111111','1111111',timestamp)
            cursor.execute(ins_query)
            db.commit()  
            clear_clients(result)
        elif table_name.strip()=='ap25_statisticsTable':
            ins_query="INSERT INTO `ap25_statisticsTable` (`ap25_systemInfo_id`, `host_id`, `index`, `statisticsInterface`, `statisticsRxPackets`, `statisticsTxPackets`, `statisticsRxError`, `statisticsTxError`, `timestamp`) VALUES ( NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');"%(result,0,'eth0','1111111','1111111','1111111','1111111', timestamp)
            cursor.execute(ins_query)
            db.commit()                                                            
        exit_status = 1
        #print ins_query
        # close the connection
    except MySQLdb.Error as e:
        #print ins_query
        print "MySQLdb Exception in ddb "+name_table_dict[table_name]+" : "+str(e[-1])
        exit_status = 2        
    except SelfCreatedException as e:
        print str(e)
        exit_status = 2
    except Exception as e:
        print "Exception ddb "+name_table_dict[table_name]+" "+str(e[-1])
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
        #print " is_filled ",table_list
        try:              
            for table_name in temp_list:
                return_value = 0
                if table_name.strip()=='ap25_vapClientStatisticsTable':
                    sel_query = "SELECT `rxSEQ`,`txSEQ` FROM ap25_vapClientStatisticsTable WHERE ap25_vapClientStatisticsTable_id = (SELECT max(ap25_vapClientStatisticsTable_id) FROM ap25_vapClientStatisticsTable WHERE host_id='%s')"%(result)                 
                elif table_name.strip()=='ap25_statisticsTable':
                    sel_query = "SELECT `statisticsRxPackets`,`statisticsTxPackets` FROM ap25_statisticsTable WHERE ap25_systemInfo_id = (SELECT max(ap25_systemInfo_id) FROM ap25_statisticsTable WHERE host_id='%s')"%(result) 
                if sel_query:
                    #print sel_query
                    cursor.execute(sel_query)
                    sel_result = cursor.fetchall()
                    #print sel_result
                    if len(sel_result) > 0:
                        if len(sel_result[0]) == map(str,sel_result[0]).count('1111111'):
                            return_value = 1
                        if return_value:
                            table_list.remove(table_name)
        # close the connection
        except MySQLdb.Error as e:
            print "MySQLdb Exception in filling "+name_table_dict[table_name]+" : "+str(e[-1])
            #print sel_query
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
    
class Bulk():
    def __init__(self,ip_address,port=161,community='public'):
        self.ip_address = ip_address
        self.port = port
        self.community = community
        self.bulk_result = {}
        self.var_binds = 20
        self.main_oid = ''
        self.agent = 'apbulk-agent'
        self.timeout = 3
        self.make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
        
    def engine(self):
        err_dict = {}
        try:
            success = 1
            port = int(self.port)
            self.snmpEngine = engine.SnmpEngine()
            config.addV1System(self.snmpEngine, self.agent, self.community)
            
            config.addTargetParams(self.snmpEngine, 'myParams', self.agent, 'noAuthNoPriv', 1)
        
            config.addTargetAddr(
                self.snmpEngine, 'myRouter', config.snmpUDPDomain,
                (self.ip_address, port), 'myParams'    
                )
            config.addSocketTransport(
                self.snmpEngine,
                config.snmpUDPDomain,
                udp.UdpSocketTransport().openClientMode()
                )
            success = 0
        except pysnmp.proto.error.ProtocolError as err:
            success = 1
            err_dict[99] = 'pyproto err '+str(err)            
        except Exception,e:
            success = 1
            err_dict[99] = ' : '+str(e)
        finally:
            result = {}
            result['success'] = success
            result['result'] = err_dict
            return result

    def cbFun(self,sendRequesthandle, errorIndication, errorStatus, errorIndex,
              varBindTable, cbCtx):
        bulk_list = self.bulk_result['result']
        success = 3
        err_dict = {}
        try:
            if errorIndication:
                err_dict[553] = str(errorIndication)
                success = 1
                return
            if errorStatus:
                err_dict[str(errorStatus)] = errorStatus.prettyPrint()
                success = 1
                #print " :: ",errorIndex,int(errorStatus),errorStatus.prettyPrint()
                return
            success = 0
            for varBindRow in varBindTable:
                for oid, val in varBindRow:
                    temp_split = oid.prettyPrint().split(self.main_oid)      
                    if len(temp_split) > 1:
                        pass
                    else:
                        #print " table finished "
                        success = 2
                        return
                    if isinstance(val,v2c.IpAddress):
                        value = str(val.prettyPrint())
                    else:
                        value = str(val) #val.prettyPrint() #str(val)
                    bulk_list.append((oid.prettyPrint(),value))
            
            for oid, val in varBindTable[-1]:
                if val is not None:
                    #print " break NONE "
                    break
            else:
                #print " else "
                return # stop on end-of-table
            #print " bulk request "
            time.sleep(self.timeout)
            return 1 # continue walking
        finally:
            self.bulk_result = {}
            self.bulk_result['success'] = success
            if success == 1:
                self.bulk_result['result'] = err_dict
            else:
                self.bulk_result['result'] = bulk_list

    def bulkget(self,oid):
        err_dict = {}
        try:
            snmp_result = {}
            self.bulk_result = {}
            self.bulk_result['result'] = []
            self.bulk_result['success'] = 1
            success = 1
            self.main_oid = oid.strip(".")
            #print " running"
            time.sleep(self.timeout)
            cmdgen.BulkCommandGenerator().sendReq(
                self.snmpEngine, 'myRouter', 0, self.var_binds, ((self.make_tuple(self.main_oid), None),), self.cbFun, None
                )
            
            self.snmpEngine.transportDispatcher.runDispatcher()
            
            #print " exit "
            
            if len(self.bulk_result) > 0:
                #print self.bulk_result
                if self.bulk_result['success'] == 2 or self.bulk_result['success'] == 3 or self.bulk_result['success'] == 0:
                    success = 0
                    oid_li = []
                    var_dict = {}
                    oid_values_list = []
                    varBindTable = self.bulk_result['result']
                    for name, value in varBindTable:
                        #print '%s = %s' % (name, value)
                        oid_values_list = name.split(self.main_oid)[1].strip('.').split('.')
                        if len(oid_values_list) > 0:
                            oid_no = oid_values_list.pop(0)
                        else: 
                            success = 1
                            return
    
                        if oid_li.count(oid_no) == 0:
                            oid_li.append(oid_no)
                            count = 0
                            flag = 1
                            if len(oid_li) == 1:
                                flag = 0
                                                                        
                        if flag == 0:
                            count += 1                      
                            li = []
                            for i in oid_values_list:
                                li.append(i)
                            li.append(value)
                            var_dict[count] = li
                            
                        else:
                            count += 1
                            li = var_dict[count]
                            li.append(value)
                            var_dict[count] = li
                    snmp_result['success'] = success
                    snmp_result['result'] = var_dict
                    #print snmp_result
                elif self.bulk_result['success'] == 1:
                    snmp_result = self.bulk_result 
                self.bulk_result = {}
                
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
            print " Exception BULK ",str(e)
            #print traceback.print_exc(e)
            success = 1
            err_dict[99] = 'pysnmp exception '+str(e)
        finally:
            if len(err_dict) > 1:
                snmp_result['success'] = success
                snmp_result['result'] = err_dict
            if len(snmp_result) < 1:
                snmp_result['success'] = 1
                snmp_result['result'] = {'24':'Unable to get Error '}
            return snmp_result



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


def host_status(hostid,status,host_ip=None,prev_status = 0):
    """
    @note: Used to update host operation status and varify it
    """
    value = 0
    plugin_status = 0
    try:
        db = db_connect()
        if hostid:
            sel_query = """select status,plugin_status from host_status  where host_id = '%s'"""%(str(hostid))
        elif host_ip:
            sel_query = """select status,plugin_status from host_status  where host_ip = '%s'"""%(host_ip)
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
                    up_query = """update host_status set status='%s', plugin_status = 0 where host_id = '%s'"""%(status,hostid)
                elif host_ip:
                    up_query = """update host_status set status='%s', plugin_status = 0 where host_ip = '%s'"""%(status,host_ip)
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
        return int(value),int(plugin_status)


def update_plugin_state(state,host_ip):
    """
    @note: Used to update host operation status and varify it
    """
    try:
        db = db_connect()
        up_query = """update host_status set plugin_status = %s  where host_ip = '%s'"""%(state,host_ip)
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
        # Open database connection
        exit_status = 1
        global db,host_id
        db = 1
        is_db_connect = 1
        if arg.count('-i') and  arg.count('-p') :
            ip_address = arg[arg.index("-i") + 1]        # receive the ip address
            port_no = arg[arg.index("-p") + 1]           # receive port number
            #time.sleep(60)
            #device_type = arg[arg.index("-d") + 1]       # receive device type
            snmp_flag = 0
            run_loop = 1
            is_exception = 1
            table_dict = ap25_table_dict #main_dict[device_type]
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
            bulk_obj = Bulk(ip_address,port_no,'public')
            obj_result = bulk_obj.engine()
            if obj_result['success'] == 0:            
                host_state, plugin_state = host_status(None,9,ip_address)
                if host_state == 0:
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
                               #print host_id
                           cursor.close()    
                    for table_name in table_dict:
                        if is_db_connect == 0:
                            is_db_connect = 1
                            db.close()
                            
                        snmp_result_dict = bulk_obj.bulkget(str(table_dict[table_name].strip('.')))
                        time.sleep(1)
                        #print snmp_result_dict
                        if is_db_connect:
                           db = db_connect()
                           if db == 1:
                               raise SelfCreatedException(' db connection failed ')


                        if snmp_result_dict['success'] == 0:    
                            #create sql query for insertion in table
                            result_dict = snmp_result_dict['result']
                            #sql="INSERT INTO %s values(null,'%s'"%(table_name,result)
                            #print result_dict
                            if len(result_dict) > 0:
                                #ap_walk_for_clients(host_id,{1:['1', '1', 'd4:10:ed:4e:0d:3c', '1', '6', '19M', '19M', '45', '120', '57', '229', 'ESs']},now)
                                    # mahipal
                                    # client_info is the data of walk
                                    # host_id is the host_id of the ap
                                    # now is the time of insert query
                                    # insert_ap_client_data(client_mac,client_info,ap_id,now)
                                #ap_client_details    pass
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
                                    #print result_dict[i]
                                #print ins_query
                                cursor = db.cursor()                            
                                try:
                                    cursor.execute(ins_query) # execute the query 
                                    db.commit()               # save the value in data base
                                    if table_name=="ap25_vapClientStatisticsTable":
                                        ap_walk_for_clients(host_id,result_dict,now)
                                except Exception,e:
                                    is_exception = 0
                                    print name_table_dict[table_name],":",e[1]                          
                                cursor.close()
                            table_list.remove(table_name)
                            if is_exception:
                                is_exception = 0
                                print "  RESPONSE : OK "
                            exit_status = 0
                            #sys.exit(0)
                        else:
                            host_status(None,0,ip_address,9)
                            temp_exit = 0
                            print host_id
                            print snmp_result_dict,"  <> "
                            if error_dict.has_key(int(snmp_result_dict['result'].keys()[0])):
                                print " No Response,",snmp_result_dict['result'].values()[0]
                            else:
                                print " No Response, Unknown Error : ",snmp_result_dict['result'].values()[0]
                                temp_exit = 2
                            snmp_flag = 1
                            return_value = 0
                            if not run_loop:
                                print name_table_dict[table_name],", remain: ",len(table_list)
                                if len(table_list) > 0:
                                    table_list = is_filled(table_list)
                                    return_value = table_list.pop()
                                        
                                if return_value < 2:
                                    for table_name in table_list:
                                        exit_status = defult_data_insert(table_name,ip_address)
                                else:
                                    exit_status = return_value                            
                                    
                                if temp_exit:
                                    exit_status = temp_exit
                                return
                            else:
                                run_loop -= 1
                                table_list.remove(table_name)
                                print name_table_dict[table_name]
                                t_list = is_filled([table_name])
                                return_value = t_list.pop()
                                if return_value < 2:
                                    exit_status = defult_data_insert(table_name,ip_address)                            
                            
                        
                        if is_table:
                            host_status(None,0,ip_address,9)
                            break
                    host_status(None,0,ip_address,9)
                else:
                    hstatus_dict = {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring',14:'Status capturing',15:'Refreshing Site Survey'}
                    schedule_round = 3
                    if plugin_state > schedule_round:
                        print " Not able to gather deivce statistics. "
                        print " Device is busy, Device %s is in progress."%hstatus_dict.get(int(host_state),"other operation")
                        db = db_connect()
                        is_db_connect = 0
                        if db == 1:
                            raise SelfCreatedException(' db connection failed ')
                        else:
                            # select the host)id form hosts table
                            cursor = db.cursor()
                            up_query = """update host_status set plugin_status = 0 where host_ip = '%s'"""%(ip_address)
                            cursor.execute(up_query)
                            db.commit()
                            sql="SELECT host_id from hosts where ip_address = '%s'"%ip_address
                            if cursor.execute(sql) == 0 or cursor.execute(sql) == None:
                                plugin_message("host_id dosn't exists in hosts table")
                                exit_status = 1
                                return
                            else:
                                host_id=cursor.fetchone()[0]
                                #print host_id
                            cursor.close()
                        
                            return_value = 1
                            if len(table_list) > 0:
                                table_list = is_filled(table_list)
                                return_value = table_list.pop()
                                    
                            if return_value < 2:
                                for table_name in table_list:
                                    exit_status = defult_data_insert(table_name,ip_address)
                            else:
                                exit_status = return_value                            
                            
                            return
                    else:
                        print "Service rescheduled"
                        print " Device is busy, Device %s is in progress."%hstatus_dict.get(int(host_state),"other operation")
                        update_plugin_state(plugin_state+1,ip_address)    
            else:
                print " Execution stop: SNMP ENGINE could not initialise ",ip_address,obj_result['result']
        else:
            plugin_message()
            exit_status = 1
            #sys.exit(1)
        
    except MySQLdb.Error as e:
        print "MySQLdb Exception    "+str(e[-1])
        host_status(None,0,ip_address,9)
        exit_status = 2
    except SelfCreatedException as e:
        exit_status = 2
        host_status(None,0,ip_address,9)
    except Exception as e:
        print "IN MAIN :  ",str(e[-1])
        host_status(None,0,ip_address,9)
        exit_status = 2
    finally :
        if isinstance(db,MySQLdb.connection):
            if db.open:
                cursor.close()
                db.close()
        sys.exit(exit_status)

# function for error messages
def plugin_message(message = ""):
    if message == "":
        print " BAD ARGUMENT PASSED TO PLUGIN "
    else:
        print message

# check the validation for command line argument
if len(arg)>4:
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
                \t./%s -i 192.168.1.1 -p 161
                \t-i\t Ip Address
                \t-p\t Port_no
                \t-d\t Device_type
                \t for single table -t Table_Name
                """ % (arg[0])
        sys.exit(2)
        
  else:
    plugin_message('-------->>>> Please pass right arguments.\n               for HELP type # python2.6 %s --help or -h.'%(arg[0]))
    sys.exit(2)



