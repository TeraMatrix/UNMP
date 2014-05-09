#!/usr/bin/python2.6
"""
@ Author            :    Rajendra Sharma
@author: Modified by Rahul Gautam
@ Project            :    UNMP
@ Version            :    0.1
@ File Name            :    walk1.py
@ Creation Date            :    1-September-2011
@date: 4-June-2012
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
    from pysnmp.entity import engine, config
    from pysnmp.entity.rfc3413 import cmdgen
    from pysnmp.carrier.asynsock.dgram import udp
    from pysnmp.proto.api import v2c
    import time
    from datetime import datetime
# extra for get_table
    from pysnmp.entity.rfc3413.oneliner import cmdgen as pycmdgen
    import MySQLdb
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
         
main_dict = {'odu16':odu16_table_dict,
           'odu100':odu100_table_dict,    
           'idu4':idu4_table_dict
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
                       51:'networkUnreachable',
                       52:'typeError',
                       53:'Request Timeout.Please Wait and Retry Again',
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

class Bulk():
    def __init__(self,ip_address,port=161,community='public'):
        self.ip_address = ip_address
        self.port = port
        self.community = community
        self.bulk_result = {}
        self.var_binds = 20
        self.main_oid = ''
        self.agent = 'test-agent'
        self.timeout = 5
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
            err_dict[99] = 'Exception : snmp Engine is not able to bind '
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
                err_dict[53] = str(errorIndication)
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
            err_dict[51] = str(sock_err)               
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
                snmp_result['result'] = {'24':'Unable to get error string'}
            return snmp_result
        


def defult_data_insert(table_name,ip_address,is_disable=1):
    try:
        exit_status = 1
        timestamp=datetime.now()
        #print " de ",table_name
        #if is_disable:
        nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
        # idu_portstatisticsTable
        softwarestatportnum, framerx, frametx, indiscards, ingoodoctets, inbadoctet, outoctets= 0 ,1111111 ,1111111 ,1111111 ,1111111 ,1111111 , 1111111
        ## for idu table idu_e1PortStatusTable 
        portNum,opstate,los,lof,ais,rai,rxFrameSlip,txFrameSlip,adptClkState,holdOverStatus,bpv = 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111 ,1111111
        ## for idu table idu_linkStatusTable
        bundleNum, portNum, operationalStatus, minJBLevel, maxJBLevel, underrunOccured, overrunOccured=1, 1, 1111111, 1111111, 1111111, 1111111, 1111111
        ## for idu_swPrimaryPortStatisticsTable
        swportnumber, framesRx, framesTx, inDiscard, inGoodOctets, inBadOctets, outOctets= 0, 1111111 ,1111111 ,1111111 ,1111111 ,1111111 ,1111111
        ## idu_portSecondaryStatisticsTable
        switchPortNum, inUnicast, outUnicast, inBroadcast, outBroadcast, inMulticast, outMulricast, inUndersizeRx, inFragmentsRx, inOversizeRx, inJabberRx, inMacRcvErrorRx, inFCSErrorRx, outFCSErrorTx, deferedTx, collisionTx, lateTx, exessiveTx, singleTx, multipleTx = 0 , 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
        ## idu_linkStatisticsTable
        bundlenumber ,  portNum ,  goodFramesToEth ,  goodFramesRx ,  lostPacketsAtRx ,  discardedPackets ,  reorderedPackets ,  underrunEvents =1 ,1 ,1111111, 1111111, 1111111, 1111111 ,1111111 ,1111111
        ## idu_tdmoipNetworkInterfaceStatisticsTable
        indexid, bytesTransmitted, bytesReceived, framesTransmittedOk, framesReceivedOk, goodClassifiedFramesRx, checksumErrorPackets = 0 ,1111111 ,1111111 ,1111111 ,1111111 ,1111111 ,1111111
        ## idu_iduNetworkStatisticsTable
        interfaceName, rxPackets, txPackets, rxBytes, txBytes, rxErrors, txErrors, rxDropped, txDropped, multicasts, collisions= 0, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111 ,1111111 ,1111111 ,1111111 ,1111111 
            #nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, -110, 123456789
#        else:
#            nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, 987654321, -111, 987654321
        global db,host_id    
        if db ==1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        cursor = db.cursor()  
        if table_name.strip()=='get_odu16_nw_interface_statistics_table':
            for j in range(3):
                ins_query="INSERT INTO `get_odu16_nw_interface_statistics_table`(`host_id`,`index`,`rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_multicast`,`colisions`,`timestamp`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(result,j+1,rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions,datetime.now())        
                cursor.execute(ins_query)
                db.commit()
        elif table_name.strip()=='get_odu16_synch_statistics_table':
            ins_query="INSERT INTO `get_odu16_synch_statistics_table`(`host_id`, `index`, `sysc_lost_counter`, `timestamp`) values('%s','1','%s','%s')"%(result,sync_lost,datetime.now())        
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip()=='get_odu16_ra_tdd_mac_statistics_entry':
            ins_query="INSERT INTO `get_odu16_ra_tdd_mac_statistics_entry`(`host_id`,`index`,`rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_crc_errors`,`rx_phy_error`,`timestamp`) values('%s','1','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(result,rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_crc_err, rx_phy_err,datetime.now())        
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip()=='get_odu16_peer_node_status_table':
            ins_query="INSERT INTO `get_odu16_peer_node_status_table`(`host_id`,`index`,`timeslot_index`,`link_status`,`tunnel_status`,`sig_strength`,`peer_mac_addr`,`ssidentifier`,`peer_node_status_raster_time`,`peer_node_status_num_slaves`,`peer_node_status_timer_adjust`,`peer_node_status_rf_config`,`timestamp`) values('%s','1', '1', NULL, NULL, '%s', NULL, NULL, '1111111', '0', '1111111', NULL,'%s')"%(result,sig_strength,datetime.now())    
            cursor.execute(ins_query)
            db.commit()            
        elif table_name.strip()=='odu100_nwInterfaceStatisticsTable':
            for j in range(2):
                ins_query="INSERT INTO `odu100_nwInterfaceStatisticsTable`(`host_id`,`nwStatsIndex`,`rxPackets`,`txPackets`,`rxBytes`,`txBytes`,`rxErrors`,`txErrors`,`rxDropped`,`txDropped`,`timestamp`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(result,j+1, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, datetime.now())        
                cursor.execute(ins_query)
                db.commit()
        elif table_name.strip()=='odu100_raTddMacStatisticsTable':
            ins_query="INSERT INTO `odu100_raTddMacStatisticsTable`(`host_id`, `raIndex`, `rxpackets`, `txpackets`, `rxerrors`, `txerrors`, `rxdropped`, `txdropped`, `rxCrcErrors`, `rxPhyError`, `timestamp`) values('%s','1','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(result,rx_packets, tx_packets, rx_err, tx_err, rx_drop, tx_drop, rx_crc_err, rx_phy_err, datetime.now())        
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip()=='odu100_synchStatisticsTable':
            ins_query="INSERT INTO `odu100_synchStatisticsTable`(`host_id`,`synchStatsIndex`,`syncLostCounter`,`timestamp`) values('%s','1','%s','%s')"%(result,sync_lost,datetime.now())    
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip()=='odu100_peerNodeStatusTable':
            ins_query="INSERT INTO `odu100_peerNodeStatusTable` (`host_id`, `raIndex`, `timeSlotIndex`, `linkStatus`, `tunnelStatus`, `sigStrength1`, `peerMacAddr`, `ssIdentifier`, `peerNodeStatusNumSlaves`, `peerNodeStatusrxRate`, `peerNodeStatustxRate`, `allocatedTxBW`, `allocatedRxBW`, `usedTxBW`, `usedRxBW`, `txbasicRate`, `sigStrength2`, `rxbasicRate`, `txLinkQuality`, `peerNodeStatustxTime`, `peerNodeStatusrxTime`,`negotiatedMaxUplinkBW`,`negotiatedMaxDownlinkBW`,`peerNodeStatuslinkDistance` ,`timestamp`) VALUES ( '%s', '1', '1', '1111111', '1111111', '%s', '1111111', '1111111', '0', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '%s', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '%s')"%(result,sig_strength,sig_strength,datetime.now())    
            cursor.execute(ins_query)
            db.commit()
            
        elif table_name.strip()=='odu100_peerTunnelStatisticsTable':
            ins_query="INSERT INTO `odu100_peerTunnelStatisticsTable` (`host_id`, `raIndex`,`tsIndex`,`rxPacket`,`txPacket`,`rxBundles`,`txBundles`, `timestamp`) VALUES ('%s', 1, 1, 1111111, 1111111, 1111111,1111111, '%s')"%(result,datetime.now())
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip()=='odu100_peerLinkStatisticsTable':
            ins_query="INSERT INTO `odu100_peerLinkStatisticsTable` (`host_id`, `raIndex`, `timeslotindex`, `txdroped`, `rxDataSubFrames`, `txDataSubFrames`, `signalstrength1`, `txRetransmissions5`, `txRetransmissions4`, `txRetransmissions3`, `txRetransmissions2`, `txRetransmissions1`, `txRetransmissions0`, `rxRetransmissions5`, `rxRetransmissions4`, `rxRetransmissions3`, `rxRetransmissions2`, `rxRetransmissions1`, `rxRetransmissions0`, `rxBroadcastDataSubFrames`, `rateIncreases`, `rateDecreases`, `emptyRasters`, `rxDroppedTpPkts`, `rxDroppedRadioPkts`, `signalstrength2`, `timestamp`) VALUES ('%s', 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, '%s')"%(result,datetime.now())
            cursor.execute(ins_query)
            db.commit()            

        elif table_name.strip()=='odu100_nwInterfaceStatusTable':
            ins_query="INSERT INTO `odu100_nwInterfaceStatusTable` ( `host_id` ,`nwStatusIndex` ,`nwInterfaceName`, `operationalState` ,`macAddress` ,`timestamp`) \
VALUES ('%s', '1', '1111111', '1111111', '1111111', '%s')"%(result,timestamp)
            cursor.execute(ins_query)
            db.commit()

        elif table_name.strip()=='odu100_synchStatusTable':
            ins_query="INSERT INTO `odu100_synchStatusTable` (`host_id`, `synchStatsIndex`,`timerAdjust`,`syncoperationalState`, `syncpercentageDownlinkTransmitTime`, `syncrasterTime`,`timestamp`) VALUES (%s,'1','1111111','1111111','1111111','1111111','%s')"%(result,timestamp)
            cursor.execute(ins_query)
            db.commit()
            
        elif table_name.strip()=='odu100_raStatusTable':
            ins_query="INSERT INTO `odu100_raStatusTable` (`host_id`, `raIndex`, `currentTimeSlot`,`raMacAddress`,`unusedTxTimeUL`,`unusedTxTimeDL`, `raoperationalState`,  `timestamp`) VALUES ('%s', '1', '1111111', '1111111', '1111111', '1111111','1111111','%s')"%(result,timestamp)
            cursor.execute(ins_query)
            db.commit()
            
        #elif table_name.strip()=='':
        #    ins_query=""                                    
            
            ###################### idu
        elif table_name.strip()=='idu_e1PortStatusTable':
            ins_query="INSERT INTO `idu_e1PortStatusTable` ( `host_id`, `portNum`, `opStatus`, `los`, `lof`, `ais`, `rai`, `rxFrameSlip`, `txFrameSlip`, `bpv`, `adptClkState`, `holdOverStatus`, `timestamp`) VALUES \
( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  %s  ,  %s  ,  %s  ,  %s  , '%s' );"%(result,portNum,opstate,los,lof,ais,rai,rxFrameSlip,txFrameSlip,bpv,adptClkState,holdOverStatus,timestamp)
            cursor.execute(ins_query)
            db.commit()    
        elif table_name.strip()=='idu_linkStatusTable':
            ins_query="INSERT INTO `idu_linkStatusTable` (`host_id`, `bundleNum`, `portNum`, `operationalStatus`, `minJBLevel`, `maxJBLevel`, `underrunOccured`, `overrunOccured`, `timestamp`) VALUES ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  '%s' );"%(result,bundleNum, portNum, operationalStatus, minJBLevel, maxJBLevel, underrunOccured, overrunOccured, timestamp)
            cursor.execute(ins_query)
            db.commit()        
        
        elif table_name.strip()=='idu_portstatisticsTable':
            ins_query=" INSERT INTO `idu_portstatisticsTable` (`host_id`, `softwarestatportnum`, `framerx`, `frametx`, `indiscards`, `ingoodoctets`, `inbadoctet`, `outoctets`, `timestamp`) VALUES ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  '%s' );"%(result, softwarestatportnum, framerx, frametx, indiscards, ingoodoctets, inbadoctet, outoctets, timestamp)
            cursor.execute(ins_query)
            db.commit()    
        elif table_name.strip()=='idu_swPrimaryPortStatisticsTable':
            ins_query="INSERT INTO `idu_swPrimaryPortStatisticsTable` (`host_id`, `swportnumber`, `framesRx`, `framesTx`, `inDiscard`, `inGoodOctets`, `inBadOctets`, `outOctets`, `timestamp`) VALUES ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  '%s' );"%(result,swportnumber, framesRx, framesTx, inDiscard, inGoodOctets, inBadOctets, outOctets, timestamp)
            cursor.execute(ins_query)
            db.commit()                                                
        elif table_name.strip()=='idu_portSecondaryStatisticsTable':
            ins_query="INSERT INTO `idu_portSecondaryStatisticsTable` ( `host_id`, `switchPortNum`, `inUnicast`, `outUnicast`, `inBroadcast`, `outBroadcast`, `inMulticast`, `outMulricast`, `inUndersizeRx`, `inFragmentsRx`, `inOversizeRx`, `inJabberRx`, `inMacRcvErrorRx`, `inFCSErrorRx`, `outFCSErrorTx`, `deferedTx`, `collisionTx`, `lateTx`, `exessiveTx`, `singleTx`, `multipleTx`, `timestamp`) VALUES ( %s,%s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s' );"%(result,switchPortNum, inUnicast, outUnicast, inBroadcast, outBroadcast, inMulticast, outMulricast, inUndersizeRx, inFragmentsRx, inOversizeRx, inJabberRx, inMacRcvErrorRx, inFCSErrorRx, outFCSErrorTx, deferedTx, collisionTx, lateTx, exessiveTx, singleTx, multipleTx, timestamp)
            cursor.execute(ins_query)
            db.commit()                                                
        elif table_name.strip()=='idu_linkStatisticsTable':
            ins_query="INSERT INTO `idu_linkStatisticsTable` (`host_id`, `bundlenumber`, `portNum`, `goodFramesToEth`, `goodFramesRx`, `lostPacketsAtRx`, `discardedPackets`, `reorderedPackets`, `underrunEvents`, `timestamp`) VALUES \
( %s,  %s , %s , %s,  %s,  %s,  %s , %s , %s ,'%s');"%(result, bundlenumber ,  portNum ,  goodFramesToEth ,  goodFramesRx ,  lostPacketsAtRx ,  discardedPackets ,  reorderedPackets ,  underrunEvents ,timestamp)
            cursor.execute(ins_query)
            db.commit()                                                
        elif table_name.strip()=='idu_tdmoipNetworkInterfaceStatisticsTable':
            ins_query="INSERT INTO `idu_tdmoipNetworkInterfaceStatisticsTable` (`host_id`, `indexid`, `bytesTransmitted`, `bytesReceived`, `framesTransmittedOk`, `framesReceivedOk`, `goodClassifiedFramesRx`, `checksumErrorPackets`, `timestamp`) VALUES \
( %s, %s ,%s ,%s ,%s ,%s ,%s ,%s,'%s');"%(result,indexid, bytesTransmitted, bytesReceived, framesTransmittedOk, framesReceivedOk, goodClassifiedFramesRx, checksumErrorPackets,timestamp)
            cursor.execute(ins_query)
            db.commit()                
        elif table_name.strip()=='idu_iduNetworkStatisticsTable':
            ins_query="INSERT INTO `idu_iduNetworkStatisticsTable` (`host_id`, `interfaceName`, `rxPackets`, `txPackets`, `rxBytes`, `txBytes`, `rxErrors`, `txErrors`, `rxDropped`, `txDropped`, `multicasts`, `collisions`, `timestamp`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'%s');"%(result,interfaceName, rxPackets, txPackets, rxBytes, txBytes, rxErrors, txErrors, rxDropped, txDropped, multicasts, collisions, timestamp)
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
        #print " is_filled ",table_list
        try:              
            for table_name in temp_list:
                return_value = 0
                if table_name.strip()=='get_odu16_nw_interface_statistics_table':
                    sel_query = "SELECT `rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_multicast`,`colisions` FROM `get_odu16_nw_interface_statistics_table` WHERE get_odu16_nw_interface_statistics_table_id = (SELECT max(get_odu16_nw_interface_statistics_table_id) FROM get_odu16_nw_interface_statistics_table where host_id = '%s')"%(result)
                    
                elif table_name.strip()=='get_odu16_synch_statistics_table':
                    sel_query = "SELECT `sysc_lost_counter` FROM get_odu16_synch_statistics_table WHERE get_odu16_synch_statistics_table_id = (SELECT max(get_odu16_synch_statistics_table_id) FROM get_odu16_synch_statistics_table WHERE host_id = '%s')"%(result)
        
                elif table_name.strip()=='get_odu16_ra_tdd_mac_statistics_entry':
                    sel_query = "SELECT `rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_crc_errors`,`rx_phy_error` FROM get_odu16_ra_tdd_mac_statistics_entry WHERE get_odu16_ra_tdd_mac_statistics_entry_id = (SELECT max(get_odu16_ra_tdd_mac_statistics_entry_id) FROM get_odu16_ra_tdd_mac_statistics_entry WHERE host_id = '%s')"%(result)

                elif table_name.strip()=='get_odu16_peer_node_status_table':
                    sel_query = "SELECT `sig_strength` FROM get_odu16_peer_node_status_table WHERE get_odu16_peer_node_status_table_id = (SELECT max(get_odu16_peer_node_status_table_id) FROM get_odu16_peer_node_status_table WHERE host_id='%s')"%(result)

        
                elif table_name.strip()=='odu100_nwInterfaceStatisticsTable':
                    sel_query = "SELECT `rxPackets`,`txPackets`,`rxBytes`,`txBytes`,`rxErrors`,`txErrors`,`rxDropped`,`txDropped` FROM odu100_nwInterfaceStatisticsTable WHERE odu100_nwInterfaceStatisticsTable_id = (SELECT max(odu100_nwInterfaceStatisticsTable_id) FROM odu100_nwInterfaceStatisticsTable WHERE host_id='%s')"%(result)
                    
                elif table_name.strip()=='odu100_raTddMacStatisticsTable':
                    sel_query = "SELECT `txpackets`, `rxpackets` FROM `odu100_raTddMacStatisticsTable` where `odu100_raTddMacStatisticsTable_id` = (SELECT max(`odu100_raTddMacStatisticsTable_id`) FROM `odu100_raTddMacStatisticsTable` where `host_id` = '%s')"%(result)
                    
                elif table_name.strip()=='odu100_synchStatisticsTable':
                    sel_query = "SELECT `syncLostCounter` FROM odu100_synchStatisticsTable WHERE odu100_synchStatisticsTable_id = (SELECT max(odu100_synchStatisticsTable_id) FROM odu100_synchStatisticsTable WHERE host_id='%s')"%(result)
                    
                elif table_name.strip()=='odu100_peerTunnelStatisticsTable':
                    sel_query = "SELECT `rxPacket`,`txPacket`,`rxBundles`,`txBundles` FROM odu100_peerTunnelStatisticsTable WHERE odu100_peerTunnelStatisticsTable_id = (SELECT max(odu100_peerTunnelStatisticsTable_id) FROM odu100_peerTunnelStatisticsTable WHERE host_id='%s')"%(result)
                    
                elif table_name.strip()=='odu100_peerLinkStatisticsTable':
                    sel_query = "SELECT `timeslotindex`, `txdroped`, `rxDataSubFrames`, `txDataSubFrames`, `signalstrength1` FROM odu100_peerLinkStatisticsTable WHERE odu100_peerLinkStatisticsTable_id = (SELECT max(odu100_peerLinkStatisticsTable_id) FROM odu100_peerLinkStatisticsTable WHERE host_id='%s')"%(result)
                    
                elif table_name.strip()=='odu100_nwInterfaceStatusTable':
                    sel_query="SELECT `operationalState` ,`macAddress` from `odu100_nwInterfaceStatusTable` where `odu100_nwInterfaceStatusTable_id` = (select max(`odu100_nwInterfaceStatusTable_id`) from `odu100_nwInterfaceStatusTable` WHERE host_id = '%s')"%(result)      
                    
                elif table_name.strip()=='odu100_synchStatusTable':
                    sel_query="SELECT   `syncoperationalState`, `syncpercentageDownlinkTransmitTime`,syncrasterTime from `odu100_synchStatusTable` where `odu100_synchStatusTable_id` = ( select max(`odu100_synchStatusTable_id`) from `odu100_synchStatusTable` WHERE host_id = '%s')"%(result)
                          
                elif table_name.strip()=='odu100_raStatusTable':
                    sel_query="SELECT  `currentTimeSlot`, `unusedTxTimeUL`,`unusedTxTimeDL` from `odu100_raStatusTable` where `odu100_raStatusTable_id` = ( SELECT max(`odu100_raStatusTable_id`) from `odu100_raStatusTable` WHERE host_id = '%s')"%(result)                          
                    
                elif table_name.strip()=='odu100_peerNodeStatusTable':
                    sel_query = "SELECT `sigStrength1`, `sigStrength2` FROM odu100_peerNodeStatusTable WHERE odu100_peerNodeStatusTable_id = (SELECT max(odu100_peerNodeStatusTable_id) FROM odu100_peerNodeStatusTable WHERE host_id='%s')"%(result)
                                        
                elif table_name.strip()=='idu_e1PortStatusTable':
                    sel_query = "SELECT `opStatus` FROM idu_e1PortStatusTable WHERE idu_e1PortStatusTable_id = (SELECT max(idu_e1PortStatusTable_id) FROM idu_e1PortStatusTable WHERE host_id='%s')"%(result)
                elif table_name.strip()=='idu_linkStatusTable':
                    sel_query = "SELECT `operationalStatus` FROM idu_linkStatusTable WHERE idu_linkStatusTable_id = (SELECT max(idu_linkStatusTable_id) FROM idu_linkStatusTable WHERE host_id='%s')"%(result)
                elif table_name.strip()=='idu_portstatisticsTable':
                    sel_query = "SELECT `framerx` FROM idu_portstatisticsTable WHERE idu_portstatisticsTable_id = (SELECT max(idu_portstatisticsTable_id) FROM idu_portstatisticsTable WHERE host_id='%s')"%(result)
                elif table_name.strip()=='idu_swPrimaryPortStatisticsTable':
                    sel_query = "SELECT `framesRx` FROM idu_swPrimaryPortStatisticsTable WHERE idu_swPrimaryPortStatisticsTable_id = (SELECT max(idu_swPrimaryPortStatisticsTable_id) FROM idu_swPrimaryPortStatisticsTable WHERE host_id='%s')"%(result)
                elif table_name.strip()=='idu_portSecondaryStatisticsTable':
                    sel_query = "SELECT `inUnicast` FROM idu_portSecondaryStatisticsTable WHERE idu_portSecondaryStatisticsTable_id = (SELECT max(idu_portSecondaryStatisticsTable_id) FROM idu_portSecondaryStatisticsTable WHERE host_id='%s')"%(result)
                elif table_name.strip()=='idu_linkStatisticsTable':
                    sel_query = "SELECT `goodFramesToEth` FROM idu_linkStatisticsTable WHERE idu_linkStatisticsTable_id = (SELECT max(idu_linkStatisticsTable_id) FROM idu_linkStatisticsTable WHERE host_id='%s')"%(result)  
                elif table_name.strip()=='idu_tdmoipNetworkInterfaceStatisticsTable':
                    sel_query = "SELECT `bytesTransmitted` FROM idu_tdmoipNetworkInterfaceStatisticsTable WHERE idu_tdmoipNetworkInterfaceStatisticsTable_id = (SELECT max(idu_tdmoipNetworkInterfaceStatisticsTable_id) FROM idu_tdmoipNetworkInterfaceStatisticsTable WHERE host_id='%s')"%(result)  
                elif table_name.strip()=='idu_iduNetworkStatisticsTable':
                    sel_query = "SELECT `rxPackets` FROM idu_iduNetworkStatisticsTable WHERE idu_iduNetworkStatisticsTable_id = (SELECT max(idu_iduNetworkStatisticsTable_id) FROM idu_iduNetworkStatisticsTable WHERE host_id='%s')"%(result)                                                        
                
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
    



def pysnmp_get_table(oid,ip_address,port,community):
    err_dict = {}
    success = 1
    try:
        if isinstance(ip_address,str) and isinstance(oid,str) and isinstance(community,str) and isinstance(port,int):
            try:
                make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                oid = oid.strip('.')
                errorIndication, errorStatus, errorIndex, \
                             varBindTable = pycmdgen.CommandGenerator().nextCmd(
                pycmdgen.CommunityData('table1-agent', community),pycmdgen.UdpTransportTarget((ip_address, port)),make_tuple(oid))
                             
                var_dict = {}
                
                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[53] = str(errorIndication)
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
            
            #bulk_obj = Bulk(ip_address,port_no,'public')
            #obj_result = bulk_obj.engine()
            obj_result = {}
            obj_result['success'] = 0
            if obj_result['success'] == 0:
                #time.sleep(60)
                host_state, plugin_state = host_status(None,9,ip_address)
                if host_state == 0:
                    if is_db_connect:
                       db = db_connect()
                       if db == 1:
                           raise SelfCreatedException(' db connection failed ')
                       else:
                           # select the host)id form hosts table
                           is_db_connect = 0
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
                            
                        snmp_result_dict = pysnmp_get_table(str(table_dict[table_name]).strip('.'),str(ip_address),int(port_no),'public')
#bulk_obj.bulkget(str(table_dict[table_name].strip('.')))
                        time.sleep(10)
                        #print snmp_result_dict
                        if is_db_connect:
                           db = db_connect()
                           if db == 1:
                               raise SelfCreatedException(' db connection failed ')
                                                              
                        if snmp_result_dict['success'] == 0:    
                            result_dict = snmp_result_dict['result']
                            if len(result_dict) > 0:
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
                                try:
                                    cursor.execute(ins_query) # execute the query 
                                    db.commit()               # save the value in data base
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
                            #print snmp_result_dict['result']
                            host_status(None,0,ip_address,9)
                            temp_exit = 0
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
                    hstatus_dict = {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring',14:'Status capturing'}
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
                print " Execution stop: SNMP ENGINE initiation fail ",ip_address,obj_result['result']
                
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
                \t./%s -i 192.168.1.1 -p 161 -d odu16
                \t-i\t Ip Address
                \t-p\t Port_no
                \t-d\t Device_type
                \t for single table -t Table_Name
                """ % (arg[0])
        sys.exit(2)
        
  else:
    plugin_message('-------->>>> Please pass right arguments.\n               for HELP type # python2.6 %s --help or -h.'%(arg[0]))
    sys.exit(2)



