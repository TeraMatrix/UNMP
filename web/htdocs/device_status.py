#!/usr/bin/python2.6


# import the packages

try:
    import socket
    # importing pysnmp library
    import pysnmp
    from pysnmp.entity.rfc3413.oneliner import cmdgen
    from pysnmp.proto.api import v2c
    #from common_bll import agent_start
    from datetime import datetime
    # import mySQL module
    import MySQLdb
    from copy import deepcopy
    import traceback    #from unmp_config import SystemConfig    #from commom_controller import logme
    # from unmp_config import SystemConfig
except ImportError as e:
    print str(e[-1])

########################## NOTE
# Please Remember : when you add oid of table please add .1 at last
# like if table oid is '.1.3.6.1.4.1.26149.2.2.11.2' then add .1 at last so new oid is '.1.3.6.1.4.1.26149.2.2.11.2.1'
# thats it
odu16_table_dict = {
    'get_odu16_synch_statistics_table': '.1.3.6.1.4.1.26149.2.2.11.2.1',
    'get_odu16_nw_interface_statistics_table': '.1.3.6.1.4.1.26149.2.2.12.3.1',
    'get_odu16_ra_tdd_mac_statistics_entry': '.1.3.6.1.4.1.26149.2.2.13.7.3.1',
    'get_odu16_peer_node_status_table': '.1.3.6.1.4.1.26149.2.2.13.9.2.1'
}

idu4_table_dict = {'idu_linkStatusTable': '.1.3.6.1.4.1.26149.2.1.3.1.1',
                   'idu_e1PortStatusTable': '.1.3.6.1.4.1.26149.2.1.3.2.1',
                   'idu_linkStatisticsTable': '.1.3.6.1.4.1.26149.2.1.4.2.1',
                   'idu_tdmoipNetworkInterfaceStatisticsTable': '.1.3.6.1.4.1.26149.2.1.4.1.1',
                   'idu_iduNetworkStatisticsTable': '.1.3.6.1.4.1.26149.2.1.4.3.1',
                   'idu_portstatisticsTable': '.1.3.6.1.4.1.26149.2.1.6.9.1',
                   'idu_swPrimaryPortStatisticsTable': '.1.3.6.1.4.1.26149.2.1.4.4.1',
                   'idu_portSecondaryStatisticsTable': '.1.3.6.1.4.1.26149.2.1.4.5.1'
}

odu100_table_dict = {
    'odu100_peerNodeStatusTable': '.1.3.6.1.4.1.26149.2.2.13.9.2.1',
    'odu100_raTddMacStatisticsTable': '.1.3.6.1.4.1.26149.2.2.13.7.3.1',
    'odu100_nwInterfaceStatisticsTable': '.1.3.6.1.4.1.26149.2.2.12.3.1',
    'odu100_synchStatisticsTable': '.1.3.6.1.4.1.26149.2.2.11.2.1',
    'odu100_peerTunnelStatisticsTable': '1.3.6.1.4.1.26149.2.2.13.9.3.1',
    'odu100_peerLinkStatisticsTable': '1.3.6.1.4.1.26149.2.2.13.9.4.1',
    'odu100_peerConfigTable': '1.3.6.1.4.1.26149.2.2.13.9.1.1',
    'odu100_raStatusTable': '1.3.6.1.4.1.26149.2.2.13.2.1',
    'odu100_nwInterfaceStatusTable': '1.3.6.1.4.1.26149.2.2.12.2.1',
    'odu100_synchStatusTable': '1.3.6.1.4.1.26149.2.2.11.3.1',
}

main_dict = {'odu16': odu16_table_dict,
             'odu100': odu100_table_dict,
             'idu4': idu4_table_dict
}
############################ Please read NOTE before addition of new table


class DeviceStatus():
    """
    Get the Device Status
    """

    def __init__(self):
        self.db = 1
        self.host_id = None
        self.error = ''

    def defult_data_insert(self, table_name, ip_address, is_disable=1):
        """

        @param table_name:
        @param ip_address:
        @param is_disable:
        @raise:
        """
        try:
            exit_status = 1
            timestamp = datetime.now()
            # print " de ",table_name
            # if is_disable:
            nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            # idu_portstatisticsTable
            softwarestatportnum, framerx, frametx, indiscards, ingoodoctets, inbadoctet, outoctets = 0, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            ## for idu table idu_e1PortStatusTable
            portNum, opstate, los, lof, ais, rai, rxFrameSlip, txFrameSlip, adptClkState, holdOverStatus, bpv = 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            ## for idu table idu_linkStatusTable
            bundleNum, portNum, operationalStatus, minJBLevel, maxJBLevel, underrunOccured, overrunOccured = 1, 1, 1111111, 1111111, 1111111, 1111111, 1111111
            ## for idu_swPrimaryPortStatisticsTable
            swportnumber, framesRx, framesTx, inDiscard, inGoodOctets, inBadOctets, outOctets = 0, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            ## idu_portSecondaryStatisticsTable
            switchPortNum, inUnicast, outUnicast, inBroadcast, outBroadcast, inMulticast, outMulricast, inUndersizeRx, inFragmentsRx, inOversizeRx, inJabberRx, inMacRcvErrorRx, inFCSErrorRx, outFCSErrorTx, deferedTx, collisionTx, lateTx, exessiveTx, singleTx, multipleTx = 0, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            ## idu_linkStatisticsTable
            bundlenumber, portNum, goodFramesToEth, goodFramesRx, lostPacketsAtRx, discardedPackets, reorderedPackets, underrunEvents = 1, 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            ## idu_tdmoipNetworkInterfaceStatisticsTable
            indexid, bytesTransmitted, bytesReceived, framesTransmittedOk, framesReceivedOk, goodClassifiedFramesRx, checksumErrorPackets = 0, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            ## idu_iduNetworkStatisticsTable
            interfaceName, rxPackets, txPackets, rxBytes, txBytes, rxErrors, txErrors, rxDropped, txDropped, multicasts, collisions = 0, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111
            # nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, -110, 123456789

            if self.db == 1:
                raise SelfCreatedException(' can not connect to database ')
            result = self.host_id
            cursor = self.db.cursor()
            if table_name.strip() == 'get_odu16_nw_interface_statistics_table':
                for j in range(3):
                    ins_query = "INSERT INTO `get_odu16_nw_interface_statistics_table`(`host_id`,`index`,`rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_multicast`,`colisions`,`timestamp`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        result, j + 1, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop,
                        rx_multicast, colisions, datetime.now())
                    cursor.execute(ins_query)
                    self.db.commit()
            elif table_name.strip() == 'get_odu16_synch_statistics_table':
                ins_query = "INSERT INTO `get_odu16_synch_statistics_table`(`host_id`, `index`, `sysc_lost_counter`, `timestamp`) values('%s','1','%s','%s')" % (
                    result, sync_lost, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'get_odu16_ra_tdd_mac_statistics_entry':
                ins_query = "INSERT INTO `get_odu16_ra_tdd_mac_statistics_entry`(`host_id`,`index`,`rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_crc_errors`,`rx_phy_error`,`timestamp`) values('%s','1','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    result, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_crc_err,
                    rx_phy_err, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'get_odu16_peer_node_status_table':
                ins_query = "INSERT INTO `get_odu16_peer_node_status_table`(`host_id`,`index`,`timeslot_index`,`link_status`,`tunnel_status`,`sig_strength`,`peer_mac_addr`,`ssidentifier`,`peer_node_status_raster_time`,`peer_node_status_num_slaves`,`peer_node_status_timer_adjust`,`peer_node_status_rf_config`,`timestamp`) values('%s','1', '1', NULL, NULL, '%s', NULL, NULL, '1111111', '0', '1111111', NULL,'%s')" % (
                    result, sig_strength, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'odu100_nwInterfaceStatisticsTable':
                for j in range(2):
                    ins_query = "INSERT INTO `odu100_nwInterfaceStatisticsTable`(`host_id`,`nwStatsIndex`,`rxPackets`,`txPackets`,`rxBytes`,`txBytes`,`rxErrors`,`txErrors`,`rxDropped`,`txDropped`,`timestamp`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        result, j + 1, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop,
                        datetime.now())
                    cursor.execute(ins_query)
                    self.db.commit()
            elif table_name.strip() == 'odu100_raTddMacStatisticsTable':
                ins_query = "INSERT INTO `odu100_raTddMacStatisticsTable`(`host_id`, `raIndex`, `rxpackets`, `txpackets`, `rxerrors`, `txerrors`, `rxdropped`, `txdropped`, `rxCrcErrors`, `rxPhyError`, `timestamp`) values('%s','1','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    result, rx_packets, tx_packets, rx_err, tx_err, rx_drop, tx_drop, rx_crc_err, rx_phy_err,
                    datetime.now())
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'odu100_synchStatisticsTable':
                ins_query = "INSERT INTO `odu100_synchStatisticsTable`(`host_id`,`syncConfigIndex`,`syncLostCounter`,`timestamp`) values('%s','1','%s','%s')" % (
                    result, sync_lost, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'odu100_peerNodeStatusTable':
                ins_query = "INSERT INTO `odu100_peerNodeStatusTable` (`host_id`, `raIndex`, `timeSlotIndex`, `linkStatus`, `tunnelStatus`, `sigStrength1`, `peerMacAddr`, `ssIdentifier`, `peerNodeStatusNumSlaves`, `peerNodeStatusrxRate`, `peerNodeStatustxRate`, `allocatedTxBW`, `allocatedRxBW`, `usedTxBW`, `usedRxBW`, `txbasicRate`, `sigStrength2`, `rxbasicRate`, `txLinkQuality`, `peerNodeStatustxTime`, `peerNodeStatusrxTime`,`negotiatedMaxUplinkBW`,`negotiatedMaxDownlinkBW`,`peerNodeStatuslinkDistance` ,`timestamp`) VALUES ( '%s', '1', '1', '1111111', '1111111', '%s', '1111111', '1111111', '0', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '%s', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '%s')" % (
                    result, sig_strength, sig_strength, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()

            elif table_name.strip() == 'odu100_peerTunnelStatisticsTable':
                ins_query = "INSERT INTO `odu100_peerTunnelStatisticsTable` (`host_id`, `raIndex`,`tsIndex`,`rxPacket`,`txPacket`,`rxBundles`,`txBundles`, `timestamp`) VALUES ('%s', 1, 1, 1111111, 1111111, 1111111,1111111, '%s')" % (
                    result, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'odu100_peerLinkStatisticsTable':
                ins_query = "INSERT INTO `odu100_peerLinkStatisticsTable` (`host_id`, `raIndex`, `timeslotindex`, `txdroped`, `rxDataSubFrames`, `txDataSubFrames`, `signalstrength1`, `txRetransmissions5`, `txRetransmissions4`, `txRetransmissions3`, `txRetransmissions2`, `txRetransmissions1`, `txRetransmissions0`, `rxRetransmissions5`, `rxRetransmissions4`, `rxRetransmissions3`, `rxRetransmissions2`, `rxRetransmissions1`, `rxRetransmissions0`, `rxBroadcastDataSubFrames`, `rateIncreases`, `rateDecreases`, `emptyRasters`, `rxDroppedTpPkts`, `rxDroppedRadioPkts`, `signalstrength2`, `timestamp`) VALUES ('%s', 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, '%s')" % (
                result, datetime.now())
                cursor.execute(ins_query)
                self.db.commit()

            elif table_name.strip() == 'odu100_nwInterfaceStatusTable':
                ins_query = "INSERT INTO `odu100_nwInterfaceStatusTable` ( `host_id` ,`nwStatusIndex` ,`nwInterfaceName`, `operationalState` ,`macAddress` ,`timestamp`) \
    VALUES ('%s', '1', '1111111', '1111111', '1111111', '%s')" % (result, timestamp)
                cursor.execute(ins_query)
                self.db.commit()

            elif table_name.strip() == 'odu100_synchStatusTable':
                ins_query = "INSERT INTO `odu100_synchStatusTable` (`host_id`, `syncConfigIndex`,`timerAdjust`,`syncoperationalState`, `syncpercentageDownlinkTransmitTime`,`syncrasterTime`, `timestamp`) VALUES (%s,'1','1111111','1111111','1111111','1111111','%s')" % (
                    result, timestamp)
                cursor.execute(ins_query)
                self.db.commit()

            elif table_name.strip() == 'odu100_raStatusTable':
                ins_query = "INSERT INTO `odu100_raStatusTable` (`host_id`, `raIndex`, `currentTimeSlot`,`raMacAddress`,`unusedTxTimeUL`,`unusedTxTimeDL`, `raoperationalState`,  `timestamp`) VALUES ('%s', '1', '1111111', '1111111', '1111111', '1111111','1111111','%s')" % (
                result, timestamp)
                cursor.execute(ins_query)
                self.db.commit()

                # elif table_name.strip()=='':
                #    ins_query=""

                ###################### idu
            elif table_name.strip() == 'idu_e1PortStatusTable':
                ins_query = "INSERT INTO `idu_e1PortStatusTable` ( `host_id`, `portNum`, `opStatus`, `los`, `lof`, `ais`, `rai`, `rxFrameSlip`, `txFrameSlip`, `bpv`, `adptClkState`, `holdOverStatus`, `timestamp`) VALUES \
    ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  %s  ,  %s  ,  %s  ,  %s  , '%s' );" % (
                result, portNum, opstate, los, lof, ais, rai, rxFrameSlip, txFrameSlip, bpv, adptClkState,
                holdOverStatus, timestamp)
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'idu_linkStatusTable':
                ins_query = "INSERT INTO `idu_linkStatusTable` (`host_id`, `bundleNum`, `portNum`, `operationalStatus`, `minJBLevel`, `maxJBLevel`, `underrunOccured`, `overrunOccured`, `timestamp`) VALUES ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  '%s' );" % (
                    result, bundleNum, portNum, operationalStatus, minJBLevel, maxJBLevel, underrunOccured,
                    overrunOccured, timestamp)
                cursor.execute(ins_query)
                self.db.commit()

            elif table_name.strip() == 'idu_portstatisticsTable':
                ins_query = " INSERT INTO `idu_portstatisticsTable` (`host_id`, `softwarestatportnum`, `framerx`, `frametx`, `indiscards`, `ingoodoctets`, `inbadoctet`, `outoctets`, `timestamp`) VALUES ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  '%s' );" % (
                    result, softwarestatportnum, framerx, frametx, indiscards, ingoodoctets, inbadoctet, outoctets,
                    timestamp)
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'idu_swPrimaryPortStatisticsTable':
                ins_query = "INSERT INTO `idu_swPrimaryPortStatisticsTable` (`host_id`, `swportnumber`, `framesRx`, `framesTx`, `inDiscard`, `inGoodOctets`, `inBadOctets`, `outOctets`, `timestamp`) VALUES ( %s, %s,  %s  ,  %s  ,  %s  ,  %s  ,  %s  ,  %s ,  '%s' );" % (
                    result, swportnumber, framesRx, framesTx, inDiscard, inGoodOctets, inBadOctets, outOctets,
                    timestamp)
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'idu_portSecondaryStatisticsTable':
                ins_query = "INSERT INTO `idu_portSecondaryStatisticsTable` ( `host_id`, `switchPortNum`, `inUnicast`, `outUnicast`, `inBroadcast`, `outBroadcast`, `inMulticast`, `outMulricast`, `inUndersizeRx`, `inFragmentsRx`, `inOversizeRx`, `inJabberRx`, `inMacRcvErrorRx`, `inFCSErrorRx`, `outFCSErrorTx`, `deferedTx`, `collisionTx`, `lateTx`, `exessiveTx`, `singleTx`, `multipleTx`, `timestamp`) VALUES ( %s,%s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s' );" % (
                    result, switchPortNum, inUnicast, outUnicast, inBroadcast, outBroadcast, inMulticast, outMulricast,
                    inUndersizeRx, inFragmentsRx, inOversizeRx, inJabberRx, inMacRcvErrorRx, inFCSErrorRx,
                    outFCSErrorTx, deferedTx, collisionTx, lateTx, exessiveTx, singleTx, multipleTx, timestamp)
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'idu_linkStatisticsTable':
                ins_query = "INSERT INTO `idu_linkStatisticsTable` (`host_id`, `bundlenumber`, `portNum`, `goodFramesToEth`, `goodFramesRx`, `lostPacketsAtRx`, `discardedPackets`, `reorderedPackets`, `underrunEvents`, `timestamp`) VALUES \
    ( %s,  %s , %s , %s,  %s,  %s,  %s , %s , %s ,'%s');" % (
                result, bundlenumber, portNum, goodFramesToEth, goodFramesRx, lostPacketsAtRx, discardedPackets,
                reorderedPackets, underrunEvents, timestamp)
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'idu_tdmoipNetworkInterfaceStatisticsTable':
                ins_query = "INSERT INTO `idu_tdmoipNetworkInterfaceStatisticsTable` (`host_id`, `indexid`, `bytesTransmitted`, `bytesReceived`, `framesTransmittedOk`, `framesReceivedOk`, `goodClassifiedFramesRx`, `checksumErrorPackets`, `timestamp`) VALUES \
    ( %s, %s ,%s ,%s ,%s ,%s ,%s ,%s,'%s');" % (
                result, indexid, bytesTransmitted, bytesReceived, framesTransmittedOk, framesReceivedOk,
                goodClassifiedFramesRx, checksumErrorPackets, timestamp)
                cursor.execute(ins_query)
                self.db.commit()
            elif table_name.strip() == 'idu_iduNetworkStatisticsTable':
                ins_query = "INSERT INTO `idu_iduNetworkStatisticsTable` (`host_id`, `interfaceName`, `rxPackets`, `txPackets`, `rxBytes`, `txBytes`, `rxErrors`, `txErrors`, `rxDropped`, `txDropped`, `multicasts`, `collisions`, `timestamp`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'%s');" % (
                    result, interfaceName, rxPackets, txPackets, rxBytes, txBytes, rxErrors, txErrors, rxDropped,
                    txDropped, multicasts, collisions, timestamp)
                cursor.execute(ins_query)
                self.db.commit()

            exit_status = 1
            # print ins_query
            # close the connection
        except MySQLdb.Error as e:
            print "MySQLdb Exception in ddb " + table_name + " : " + str(e[-1])
            exit_status = 2
        except SelfCreatedException as e:
            print str(e)
            exit_status = 2
        except Exception as e:
            print str(e[-1])
            exit_status = 2
        finally:
            if self.db != 1:
                cursor.close()

    # --     default data insert close
    def is_filled(self, table_list=[]):
        """

        @param table_list:
        @return: @raise:
        """
        try:
            return_value = 0
            if self.db == 1:
                raise SelfCreatedException(' can not connect to database ')
            result = self.host_id
            sel_query = None
            cursor = self.db.cursor()
            temp_list = deepcopy(table_list)
            # print " is_filled ",table_list
            try:
                for table_name in temp_list:
                    return_value = 0
                    if table_name.strip() == 'get_odu16_nw_interface_statistics_table':
                        sel_query = "SELECT `rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_multicast`,`colisions` FROM `get_odu16_nw_interface_statistics_table` WHERE get_odu16_nw_interface_statistics_table_id = (SELECT max(get_odu16_nw_interface_statistics_table_id) FROM get_odu16_nw_interface_statistics_table where host_id = '%s')" % (
                            result)

                    elif table_name.strip() == 'get_odu16_synch_statistics_table':
                        sel_query = "SELECT `sysc_lost_counter` FROM get_odu16_synch_statistics_table WHERE get_odu16_synch_statistics_table_id = (SELECT max(get_odu16_synch_statistics_table_id) FROM get_odu16_synch_statistics_table WHERE host_id = '%s')" % (
                            result)

                    elif table_name.strip() == 'get_odu16_ra_tdd_mac_statistics_entry':
                        sel_query = "SELECT `rx_packets`,`tx_packets`,`rx_bytes`,`tx_bytes`,`rx_errors`,`tx_errors`,`rx_dropped`,`tx_dropped`,`rx_crc_errors`,`rx_phy_error` FROM get_odu16_ra_tdd_mac_statistics_entry WHERE get_odu16_ra_tdd_mac_statistics_entry_id = (SELECT max(get_odu16_ra_tdd_mac_statistics_entry_id) FROM get_odu16_ra_tdd_mac_statistics_entry WHERE host_id = '%s')" % (
                            result)

                    elif table_name.strip() == 'get_odu16_peer_node_status_table':
                        sel_query = "SELECT `sig_strength` FROM get_odu16_peer_node_status_table WHERE get_odu16_peer_node_status_table_id = (SELECT max(get_odu16_peer_node_status_table_id) FROM get_odu16_peer_node_status_table WHERE host_id='%s')" % (
                            result)

                    elif table_name.strip() == 'odu100_nwInterfaceStatisticsTable':
                        sel_query = "SELECT `rxPackets`,`txPackets`,`rxBytes`,`txBytes`,`rxErrors`,`txErrors`,`rxDropped`,`txDropped` FROM odu100_nwInterfaceStatisticsTable WHERE odu100_nwInterfaceStatisticsTable_id = (SELECT max(odu100_nwInterfaceStatisticsTable_id) FROM odu100_nwInterfaceStatisticsTable WHERE host_id='%s')" % (
                            result)

                    elif table_name.strip() == 'odu100_raTddMacStatisticsTable':
                        sel_query = "SELECT `txpackets`, `rxpackets` FROM `odu100_raTddMacStatisticsTable` where `odu100_raTddMacStatisticsTable_id` = (SELECT max(`odu100_raTddMacStatisticsTable_id`) FROM `odu100_raTddMacStatisticsTable` where `host_id` = '%s')" % (
                        result)

                    elif table_name.strip() == 'odu100_synchStatisticsTable':
                        sel_query = "SELECT `syncLostCounter` FROM odu100_synchStatisticsTable WHERE odu100_synchStatisticsTable_id = (SELECT max(odu100_synchStatisticsTable_id) FROM odu100_synchStatisticsTable WHERE host_id='%s')" % (
                            result)

                    elif table_name.strip() == 'odu100_peerTunnelStatisticsTable':
                        sel_query = "SELECT `rxPacket`,`txPacket`,`rxBundles`,`txBundles` FROM odu100_peerTunnelStatisticsTable WHERE odu100_peerTunnelStatisticsTable_id = (SELECT max(odu100_peerTunnelStatisticsTable_id) FROM odu100_peerTunnelStatisticsTable WHERE host_id='%s')" % (
                            result)

                    elif table_name.strip() == 'odu100_peerLinkStatisticsTable':
                        sel_query = "SELECT `timeslotindex`, `txdroped`, `rxDataSubFrames`, `txDataSubFrames`, `signalstrength1` FROM odu100_peerLinkStatisticsTable WHERE odu100_peerLinkStatisticsTable_id = (SELECT max(odu100_peerLinkStatisticsTable_id) FROM odu100_peerLinkStatisticsTable WHERE host_id='%s')" % (
                        result)

                    elif table_name.strip() == 'odu100_nwInterfaceStatusTable':
                        sel_query = "SELECT `operationalState` ,`macAddress` from `odu100_nwInterfaceStatusTable` where `odu100_nwInterfaceStatusTable_id` = (select max(`odu100_nwInterfaceStatusTable_id`) from `odu100_nwInterfaceStatusTable` WHERE host_id = '%s')" % (
                            result)

                    elif table_name.strip() == 'odu100_synchStatusTable':
                        sel_query = "SELECT   `syncoperationalState`, `syncpercentageDownlinkTransmitTime`,syncrasterTime from `odu100_synchStatusTable` where `odu100_synchStatusTable_id` = ( select max(`odu100_synchStatusTable_id`) from `odu100_synchStatusTable` WHERE host_id = '%s')" % (
                        result)

                    elif table_name.strip() == 'odu100_raStatusTable':
                        sel_query = "SELECT  `currentTimeSlot`, `unusedTxTimeUL`,`unusedTxTimeDL` from `odu100_raStatusTable` where `odu100_raStatusTable_id` = ( SELECT max(`odu100_raStatusTable_id`) from `odu100_raStatusTable` WHERE host_id = '%s')" % (
                            result)

                    elif table_name.strip() == 'odu100_peerNodeStatusTable':
                        sel_query = "SELECT `sigStrength1`, `sigStrength2` FROM odu100_peerNodeStatusTable WHERE odu100_peerNodeStatusTable_id = (SELECT max(odu100_peerNodeStatusTable_id) FROM odu100_peerNodeStatusTable WHERE host_id='%s')" % (
                            result)

                    elif table_name.strip() == 'idu_e1PortStatusTable':
                        sel_query = "SELECT `opStatus` FROM idu_e1PortStatusTable WHERE idu_e1PortStatusTable_id = (SELECT max(idu_e1PortStatusTable_id) FROM idu_e1PortStatusTable WHERE host_id='%s')" % (
                            result)
                    elif table_name.strip() == 'idu_linkStatusTable':
                        sel_query = "SELECT `operationalStatus` FROM idu_linkStatusTable WHERE idu_linkStatusTable_id = (SELECT max(idu_linkStatusTable_id) FROM idu_linkStatusTable WHERE host_id='%s')" % (
                            result)
                    elif table_name.strip() == 'idu_portstatisticsTable':
                        sel_query = "SELECT `framerx` FROM idu_portstatisticsTable WHERE idu_portstatisticsTable_id = (SELECT max(idu_portstatisticsTable_id) FROM idu_portstatisticsTable WHERE host_id='%s')" % (
                            result)
                    elif table_name.strip() == 'idu_swPrimaryPortStatisticsTable':
                        sel_query = "SELECT `framesRx` FROM idu_swPrimaryPortStatisticsTable WHERE idu_swPrimaryPortStatisticsTable_id = (SELECT max(idu_swPrimaryPortStatisticsTable_id) FROM idu_swPrimaryPortStatisticsTable WHERE host_id='%s')" % (
                        result)
                    elif table_name.strip() == 'idu_portSecondaryStatisticsTable':
                        sel_query = "SELECT `inUnicast` FROM idu_portSecondaryStatisticsTable WHERE idu_portSecondaryStatisticsTable_id = (SELECT max(idu_portSecondaryStatisticsTable_id) FROM idu_portSecondaryStatisticsTable WHERE host_id='%s')" % (
                            result)
                    elif table_name.strip() == 'idu_linkStatisticsTable':
                        sel_query = "SELECT `goodFramesToEth` FROM idu_linkStatisticsTable WHERE idu_linkStatisticsTable_id = (SELECT max(idu_linkStatisticsTable_id) FROM idu_linkStatisticsTable WHERE host_id='%s')" % (
                            result)
                    elif table_name.strip() == 'idu_tdmoipNetworkInterfaceStatisticsTable':
                        sel_query = "SELECT `bytesTransmitted` FROM idu_tdmoipNetworkInterfaceStatisticsTable WHERE idu_tdmoipNetworkInterfaceStatisticsTable_id = (SELECT max(idu_tdmoipNetworkInterfaceStatisticsTable_id) FROM idu_tdmoipNetworkInterfaceStatisticsTable WHERE host_id='%s')" % (
                            result)
                    elif table_name.strip() == 'idu_iduNetworkStatisticsTable':
                        sel_query = "SELECT `rxPackets` FROM idu_iduNetworkStatisticsTable WHERE idu_iduNetworkStatisticsTable_id = (SELECT max(idu_iduNetworkStatisticsTable_id) FROM idu_iduNetworkStatisticsTable WHERE host_id='%s')" % (
                            result)

                    if sel_query:
                        cursor.execute(sel_query)
                        sel_result = cursor.fetchall()
                        if len(sel_result) > 0:
                            if len(sel_result[0]) == map(str, sel_result[0]).count('1111111'):
                                return_value = 1
                            if return_value:
                                table_list.remove(table_name)
            # close the connection
            except MySQLdb.Error as e:
                print "MySQLdb Exception in filling " + table_name + " : " + str(e[-1])
                # return_value = 2
            except Exception as e:
                print " filler : ", str(e[-1])
        except SelfCreatedException as e:
            print str(e)
            return_value = 2
        except Exception as e:
            print str(e[-1])
            return_value = 2
        finally:
            if self.db != 1:
                cursor.close()
            table_list.append(return_value)
            return table_list

    def bulktable(self, oid, ip_address, port, community, max_value=15):
        """

        @param oid:
        @param ip_address:
        @param port:
        @param community:
        @param max_value:
        @return:
        """
        err_dict = {}
        success = 1
        try:
            if isinstance(ip_address, str) and isinstance(oid, str) and isinstance(community, str) and isinstance(port,
                                                                                                                  int):
                try:
                    make_tuple = lambda x: tuple(int(i) for i in x.split('.'))
                    oid = oid.strip('.')
                    # print oid
                    first_value = 0
                    errorIndication, errorStatus, errorIndex, \
                    varBindTable = cmdgen.CommandGenerator().bulkCmd(
                        cmdgen.CommunityData('device-agent', community), cmdgen.UdpTransportTarget((ip_address, port)),
                        first_value, max_value, make_tuple(oid))

                    var_dict = {}

                    if errorIndication and len(varBindTable) < 1:
                        success = 1
                        err_dict[53] = str(errorIndication)
                        return
                        # handle

                    else:
                        if errorStatus:
                            err_dict[int(errorStatus)] = str(errorStatus)
                            success = 1
                            return
                            # print '%s at %s\n' % (
                            # errorStatus.prettyPrint(),errorIndex and
                            # varBindTable[-1][int(errorIndex)-1] or '?')
                        else:
                            success = 0
                            oid_li = []
                            var_dict = {}
                            # print varBindTable
                            for varBindTableRow in varBindTable:
                                for name, val in varBindTableRow:
                                    # print '%s = %s' % (name.prettyPrint(),
                                    # val.prettyPrint())
                                    temp_split = name.prettyPrint().split(oid)
                                    if len(temp_split) > 1:
                                        pass
                                    else:
                                        return
                                        # print name.prettyPrint()
                                    oid_values_list = name.prettyPrint(
                                    ).split(oid)[1].strip('.').split('.')
                                    # print oid_values_list
                                    if len(oid_values_list) > 0:
                                        oid_no = oid_values_list.pop(0)
                                    else:
                                        success = 1
                                        return
                                    if isinstance(val, v2c.IpAddress):
                                        value = str(val.prettyPrint())
                                    else:
                                        value = str(
                                            val)  # val.prettyPrint() #str(val)
                                    if oid_li.count(oid_no) == 0:
                                        oid_li.append(oid_no)
                                        count = 0
                                        flag = 1
                                        if len(oid_li) == 1:
                                            flag = 0

                                    if flag == 0:
                                        count += 1
                                        li = []
                                        # oid_values_list.pop(0)
                                        # print oid_values_list
                                        for i in oid_values_list:
                                            li.append(i)
                                            # print " li ",li
                                        li.append(value)
                                        # print " li 2",li
                                        var_dict[count] = li
                                        # print var_dict
                                    else:
                                        count += 1
                                        li = var_dict[count]
                                        li.append(value)
                                        var_dict[count] = li
                                        # print li,count
                                        # print "li,count",li,count,var_dict,oid_li

                except socket.error as sock_err:
                    success = 1
                    err_dict[51] = str(sock_err)
                except pysnmp.proto.error.ProtocolError as err:
                    success = 1
                    err_dict[99] = 'pyproto err ' + str(err)
                except TypeError as err:
                    success = 1
                    err_dict[99] = 'type err ' + str(err)
                except Exception as e:
                    # print traceback.print_exc(e)
                    success = 1
                    err_dict[99] = 'pysnmp exception ' + str(e)

            else:
                success = 1
                err_dict[
                    96] = "Arguments_are_not_proper : oid as str ( don't include first dot as .1.3 must be 1.3),ip_address as str ,port as int,community as str"
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

    def db_connect(self):
        """
        Used to connect to the database :: return database object assigned in global_self.db variable
        """
        self.db = 1
        try:
            #self.db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            self.db = MySQLdb.connect("localhost", "root", "root", "nms")
        except MySQLdb.Error as e:
            print str(e)
        except Exception as e:
            print "Exception in database connection " + str(e)

    def host_status(self, status, host_ip=None, prev_status=0):
        """



        @param status:
        @param host_ip:
        @param prev_status:
        @note: Used to update host operation status and varify it
        @dict: {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring', 14:'Status capturing'}
        """
        value = 0
        try:
            self.db_connect()
            if self.hostid:
                sel_query = """select status from host_status  where host_id = '%s'""" % (
                    str(self.hostid))
            elif host_ip:
                sel_query = """select status from host_status  where host_ip = '%s'""" % (
                    host_ip)
            else:
                value = 0  # error 100
                return
            if status == None:
                value = 0  # error 100
                return
            cursor = self.db.cursor()
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                if int(result[0][0]) == prev_status or int(result[0][0]) == int(status):
                    if self.hostid:
                        up_query = """update host_status set status='%s' where host_id = '%s'""" % (
                            status, str(self.hostid))
                    elif host_ip:
                        up_query = """update host_status set status='%s' where host_ip = '%s'""" % (
                            status, host_ip)
                    cursor.execute(up_query)
                    self.db.commit()
                    value = 0
                else:
                    value = int(result[0][0])
            else:
                value = 0  # value = 100 no row found
            cursor.close()

        except MySQLdb.Error:
            pass
        except Exception:
            pass
        finally:
            return value

    ###### @@@ device_status program starts from here

    def get_columns(self, firmware_id, table_name):
        """

        @param firmware_id:
        @param table_name:
        @return:
        """
        result = ''
        query = """SELECT indexes_name, coloumn_name FROM odu100_%s_oids WHERE table_name = '%s'""" % (
        firmware_id.replace('.', '_'), table_name.split('_')[-1])
        #print query
        try:
            cur = self.db.cursor()
            if cur.execute(query):
                result = cur.fetchall()
                result = """(host_id, %s %s, timestamp) \
                            """ % (
                    result[0][0] + ',',
                    # '' if result[0][0] == 'NULL' else result[0][0]+',',
                    ', '.join([t[1] for t in result])
                )
            cur.close()
        except Exception:
            import traceback

            print traceback.format_exc()
        finally:
            return result

    def insert_db(self, result_dict, table_name, device_type_id=None, firmware_id=None):
        """

        @param result_dict:
        @param table_name:
        @param device_type_id:
        @param firmware_id:
        @return:
        """
        success = 1
        if device_type_id == 'odu100':
            ins_query = "INSERT INTO %s %s values " % (
                table_name, self.get_columns(firmware_id, table_name))
        else:
            ins_query = "INSERT INTO %s values " % (table_name)

        flag = 1
        ins_str = ""
        date_time = datetime.now()
        for i in result_dict:
            if flag == 1:
                ins_query += "('%s'" % (self.host_id)
                ins_len = len(result_dict[i])
                for ln in xrange(ins_len):
                    ins_str += " ,'%s'"
                flag = 0
            else:
                ins_query += ", ('%s'" % (self.host_id)

            ins_query += ins_str % tuple(result_dict[i])
            ins_query += ", '%s')" % (date_time)
            #logme(table_name + ' ' + ins_query)
        #print ins_query

        cursor = self.db.cursor()
        try:
            cursor.execute(ins_query)  # execute the query
            self.db.commit()                # save the value in data base
        except Exception, e:
            self.error = " insert_db %s %s" % (table_name, traceback.format_exc())
            #print str(e)
            success = 0
            #print table_name, ":", e[1]
        cursor.close()
        return success

    def insert_status(self, host_id, ip_address, port_no, community, device_type, single_table_name=None,
                      firmware_id=None):
        """

        @param host_id:
        @param ip_address:
        @param port_no:
        @param community:
        @param device_type:
        @param single_table_name:
        @param firmware_id:
        @return: @raise:
        """
        try:
            # Open database connection
            self.db = 1
            cursor = None
            is_db_connect = 1
            self.host_id = host_id
            exit_status = -1
            is_exception = 1
            table_dict = {}
            if device_type is not None:
                table_dict = main_dict.get(device_type, {})
                if len(table_dict) < 1:
                    return
            is_table = 0
            if single_table_name is not None:
                is_table = 1
                single_table = single_table_name

            table_list = []

            if is_table:
                table_list.append(single_table)
            else:
                table_list = table_dict.keys()
                # print table_list
            host_state = self.host_status(14)

            if host_state == 0:
                for table_name in table_dict:
                    # print table_name
                    if is_table:
                        table_name = single_table
                        # print table_name
                    snmp_result_dict = self.bulktable(str(table_dict[table_name].strip(
                        '.')), str(ip_address), int(port_no), community)
                    print str(table_dict[table_name].strip('.'))
                    # opening self.db connection
                    print snmp_result_dict
                    if is_db_connect:
                        self.db_connect()
                        is_db_connect = 0
                        if self.db == 1:
                            raise SelfCreatedException(
                                ' db connection failed ')

                    if snmp_result_dict['success'] == 0:
                        result_dict = snmp_result_dict['result']

                        if len(result_dict) > 0:
                            is_exception = self.insert_db(result_dict, table_name, device_type, firmware_id)
                        table_list.remove(table_name)
                        exit_status = -1
                        if is_exception:
                            is_exception = 0
                            exit_status = 0
                    else:
                        # print snmp_result_dict['result'].values()[0]
                        # print table_name,", remain:
                        # ",len(table_list)
                        self.host_status(0, None, 14)
                        agent_start(str(ip_address))
                        return_value = 0
                        if len(table_list) > 0:
                            table_list = self.is_filled(table_list)
                            return_value = table_list.pop()

                        if return_value < 2:
                            for table_name in table_list:
                                exit_status = self.defult_data_insert(
                                    table_name, ip_address)
                        else:
                            exit_status = return_value
                        exit_status = -1
                        return

                    if is_table:
                        break
            else:
                exit_status = host_state

        except MySQLdb.Error:
            self.error = "MySQLdb Exception   %s " % (traceback.format_exc())
            exit_status = 22
        except SelfCreatedException:
            self.error = " self %s " % (traceback.format_exc())
            exit_status = 22
        except Exception as e:
            self.error = "IN MAIN :  " % (traceback.format_exc())
            exit_status = 22
        finally:
            self.host_status(0, None, 14)
            if isinstance(self.db, MySQLdb.connection):
                if self.db.open:
                    if cursor:
                        cursor.close()
                    self.db.close()
            return exit_status

# Exception class


class SelfCreatedException(Exception):
    """

    @param msg:
    """

    def __init__(self, msg):
        print msg

# How to use
# dd = DeviceStatus()
# print dd.insert_status('4','172.22.0.120', 161, 'public','odu100','odu100_synchStatusTable', '7.2.29')
# query for getting
# sql="SELECT host_id,snmp_port,snmp_read_community,device_type_id from
# hosts where ip_address = '%s'"%ip_address
