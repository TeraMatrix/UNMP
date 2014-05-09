#!/usr/bin/python2.6
"""
@ Author            :    Rahul Gautam
@ Project           :    UNMP
@ Version           :    0.1, 0.9
@ File Name         :    odu100walk1.py
@ Creation Date     :    1-September-2011
@date: 4-June-2012
@date: 11-Jan-2012
@ Purpose           :    This plugin insert the data in multipal table for RM/UBRe type device.
@ Organisation      :    CodeScape Consultants Pvt. Ltd.
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
##########################################################################

##-------------------- fixme -------------------##
##
##  Now when insert to database table i also take care of column names
##  but i am afraid that we are no longer in support for CGI base pooling
##  of monitoring data for firmware > 7.2.20
##
##--------------------   ~   -------------------##


# import the pack
try:
    # import traceback
    import socket
    import os
    import sys
    # importing pysnmp library
    # from pysnmp.entity import engine, config
    # from pysnmp.entity.rfc3413 import cmdgen
    # from pysnmp.carrier.asynsock.dgram import udp
    from pysnmp.proto.api import v2c
    import pysnmp
    from datetime import datetime
    # extra for get_table
    from pysnmp.entity.rfc3413.oneliner import cmdgen as pycmdgen
    import MySQLdb
    from copy import deepcopy
    # import tempfile
    # import paramiko
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import paramiko
    import urllib2
except ImportError as e:
    print str(e[-1])
    sys.exit(2)


# Exception class
class SelfCreatedException(Exception):
    pass


url_dict = {}
# monitoring data
url_dict['odu100_peerNodeStatusTable'] = 'peerstats.shtml'
url_dict['odu100_synchStatisticsTable'] = 'syncclock.shtml'
url_dict['odu100_raTddMacStatisticsTable'] = 'cgi-bin/gettddmac.sh'
url_dict['odu100_nwInterfaceStatisticsTable'] = 'cgi-bin/getstat.sh'


# status data
url_dict['odu100_raStatusTable'] = 'raaccess.shtml'
url_dict['odu100_synchStatusTable'] = 'syncstatus.shtml'
url_dict['odu100_nwInterfaceStatusTable'] = 'cgi-bin/getstat.sh'


############################################################## monitoring
def odu100_peerNodeStatusTable(data):
    success = 1
    # print data
    dict_data = {}
    try:
        s = data
        function_str = "function GetPeerInfo(peer)"
        find_string = "macAddress, linkStatus, ssid, tunnelStatus, numSlaves, rxRate, txRate, allocatedTxBW, allocatedRxBW, usedTxBW, usedRxBW, txBasicRate, rxBasicRate, sigStrength1, sigStrength2, txTime, rxTime, txLinkQuality, negotiatedMaxUplinkBW, negotiatedMaxDownlinkBW, linkDistance"
        left_hand_str = "peernodestats"
        list_data = []
        dict_data = {}
        list_index = 0
        count = 1
        index = s.find(function_str)
        given = find_string.split(', ')
        req = [
            'linkStatus', 'tunnelStatus', 'sigStrength1', 'macAddress', 'ssid', 'numSlaves', 'rxRate', 'txRate', 'allocatedTxBW', 'allocatedRxBW', 'usedTxBW',
            'usedRxBW', 'txBasicRate', 'sigStrength2', 'rxBasicRate', 'txLinkQuality', 'txTime', 'rxTime', 'negotiatedMaxUplinkBW', 'negotiatedMaxDownlinkBW', 'linkDistance']
        while 1:
            to_be_matched = "case %s:" % (list_index + 1)
            index_data = s.find(to_be_matched, index + 1)
            # print index_data
            index_data_start = s.find(left_hand_str, index_data + 1)
            index_data_end = s.find("break;", index_data_start + 1)
            temp_str = s[index_data_start:index_data_end]
            # print temp_str
            temp_index = temp_str.find(find_string)
            li = []
            if temp_index != -1:
                list_temp = temp_str[temp_index + 1 + len(
                    find_string):].split(", ")
                list_temp[-1] = list_temp[-1].strip().replace('";', "")
                list_temp[2] = list_temp[2] if list_temp[2] != '<null>' else ''
                temp_dict = dict(zip(given, list_temp))
                for i in req:
                    li.append(temp_dict.get(i, ""))
                li.insert(0, list_index + 1)
                li.insert(0, 1)
                dict_data[count] = li
                li = []
                temp_dict = {}
            list_index = list_index + 1
            count = count + 1
            if list_index == 15:
                break
        success = 0
        # print dict_data
    except Exception, e:
        print str(e)
        success = 1
    finally:
        return {'success': success, 'result': dict_data}  # list_data


def odu100_synchStatisticsTable(data):
    success = 1
    try:
        s = data
        function_str = "Sync Lost Counter"
        find_string = '<td align="left">'
        data_index = s.find(function_str)
        data_index_start = s.find(find_string, data_index + len(function_str))
        data_index_start = data_index_start + len(find_string)
        data_index_end = s.find("</td>", data_index_start)
        data = s[data_index_start:data_index_end]
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: [1, data.strip()]}}
        else:
            return {'success': success, 'result': {}}


def odu100_nwInterfaceStatisticsTable(data):
    success = 1
    try:
        num = 'num'
        nwifaces = 'nwifaces'
        name = 'name'
        rxPackets = 'rxPackets'
        txPackets = 'txPackets'
        rxBytes = 'rxBytes'
        txBytes = 'txBytes'
        rxErrors = 'rxErrors'
        txErrors = 'txErrors'
        rxDropped = 'rxDropped'
        txDropped = 'txDropped'
        macAddress = 'macAddress'
        operationalState = 'operationalState'

        di = eval(data)
        interface_statistics = {}
        li = di['nwifaces']
        count = 1
        for i in li:
            temp_statistics = [count, i['rxPackets'], i['txPackets'], i['rxBytes'], i[
                'txBytes'], i['rxErrors'], i['txErrors'], i['rxDropped'], i['txDropped']]
            interface_statistics[count] = temp_statistics
            count = count + 1
        # return
        # {'interface_statistics':interface_statistics,"interface_status":interface_status}
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': interface_statistics}
        else:
            return {'success': success, 'result': {}}


def odu100_raTddMacStatisticsTable(data):
    success = 1
    try:
        num = 'num'
        tddmacs = 'tddmacs'
        rfChannelFrequency = 'rfChannelFrequency'
        rxPackets = 'rxPackets'
        txPackets = 'txPackets'
        rxErrors = 'rxErrors'
        txErrors = 'txErrors'
        rxDropped = 'rxDropped'
        txDropped = 'txDropped'
        rxCrcErrors = 'rxCrcErrors'
        rxPhyErrors = 'rxPhyErrors'
        di = eval(data)
        tdd_mac_statistics = {}
        li = di['tddmacs']
        count = 1
        for i in li:
            temp_tdd_mac = [1, i['rxPackets'], i['txPackets'], i['rxErrors'], i[
                'txErrors'], i['rxDropped'], i['txDropped'], i['rxCrcErrors'], i['rxPhyErrors']]
            tdd_mac_statistics[count] = temp_tdd_mac
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': tdd_mac_statistics}
        else:
            return {'success': success, 'result': {}}


############################################ Status tables

def odu100_raStatusTable(data):
    success = 1
    try:
        s = data
        main_str_list = ["Current Time Slot", "Radio MAC Address",
                         "Radio Operational State", "Unused Tx Time UL", "Unused Tx Time DL"]
        find_string_list = ['<td align="left">', '<td align="left">',
                            '<td align="left"><div id="opstate">', '<td align="left">', '<td align="left">']
        end_string_list = ["</td>", "</td>", "</div></td>", "</td>", "</td>"]
        list_data = [1]
        for i in range(len(main_str_list)):
            main_str = main_str_list[i]
            find_string = find_string_list[i]
            end_string = end_string_list[i]
            data_index = s.find(main_str)
            data_index_start = s.find(find_string, data_index + len(main_str))
            data_index_start = data_index_start + len(find_string)
            data_index_end = s.find(end_string, data_index_start)
            data = s[data_index_start:data_index_end]
            list_data.append(data.strip())
        success = 0
    except Exception, e:
        # print str(e)
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}


def odu100_synchStatusTable(data):
    success = 0
    try:
        s = data
        main_str_list = ["Sync Operational State", "Raster Time",
                         "Time Adjust", "Percentage Downlink Transmit Time"]
        find_string_list = [
            '<td align="left"><div id="operationalstate">', '<td align="left"><div id="rastertime">', '<td align="left">',
            '<td align="left"><div id="percentagedownlinktransmittime">']
        end_string_list = ["</td>", "</div></td>", "</div></td>",
                           "</div></td>"]
        list_data = [1]
        for i in range(len(main_str_list)):
            main_str = main_str_list[i]
            find_string = find_string_list[i]
            end_string = end_string_list[i]
            data_index = s.find(main_str)
            data_index_start = s.find(find_string, data_index + len(main_str))
            data_index_start = data_index_start + len(find_string)
            data_index_end = s.find(end_string, data_index_start)
            data = s[data_index_start:data_index_end]
            list_data.append(int(data.strip()))
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}


def odu100_nwInterfaceStatusTable(data):
    success = 1
    try:
        num = 'num'
        nwifaces = 'nwifaces'
        name = 'name'
        rxPackets = 'rxPackets'
        txPackets = 'txPackets'
        rxBytes = 'rxBytes'
        txBytes = 'txBytes'
        rxErrors = 'rxErrors'
        txErrors = 'txErrors'
        rxDropped = 'rxDropped'
        txDropped = 'txDropped'
        macAddress = 'macAddress'
        operationalState = 'operationalState'
        di = eval(data)
        interface_statistics = []
        interface_status = {}
        li = di['nwifaces']
        count = 1
        for i in li:
            temp_statistics = [count, i['rxPackets'], i['txPackets'], i['rxBytes'], i[
                'txBytes'], i['rxErrors'], i['txErrors'], i['rxDropped'], i['txDropped']]
            interface_statistics.append(temp_statistics)
            opstate = 1 if i['operationalState'] == 'Enabled' else 0
            temp_status = [count, i['name'], opstate, i['macAddress']]
            interface_status[count] = temp_status
            count = count + 1
        success = 0
    except Exception, e:
        # print " nw ",str(e)
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': interface_status}
        else:
            return {'success': success, 'result': {}}


function_dict = {}
# monitoring data
function_dict['odu100_peerNodeStatusTable'] = odu100_peerNodeStatusTable
function_dict['odu100_synchStatisticsTable'] = odu100_synchStatisticsTable
function_dict[
    'odu100_raTddMacStatisticsTable'] = odu100_raTddMacStatisticsTable
function_dict[
    'odu100_nwInterfaceStatisticsTable'] = odu100_nwInterfaceStatisticsTable

# status data
function_dict['odu100_raStatusTable'] = odu100_raStatusTable
function_dict['odu100_synchStatusTable'] = odu100_synchStatusTable
function_dict['odu100_nwInterfaceStatusTable'] = odu100_nwInterfaceStatusTable


def cgi_opener(ip, username, password, table_list):
    try:
        success = 1
        url = "http://" + ip + "/"
        result_dict = {}
        if isinstance(url, str) and isinstance(username, str) and isinstance(password, str):
            loop = len(table_list)
            temp_list = deepcopy(table_list)
            while loop:
                table_list = deepcopy(temp_list)

                flag = 1
                try:
                    for table in table_list:
                        if table == "odu100_raConfTable":  # special case for odu100_raConfTable
                            # data_acl=url+"aclconfig.shtml"
                            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm(
                            )
                            top_level_url = url
                            password_mgr.add_password(
                                None, top_level_url, username, password)
                            handler = urllib2.HTTPBasicAuthHandler(
                                password_mgr)
                            opener = urllib2.build_opener(handler)
                            url_table = url + url_dict[table][0]
                            f = opener.open(url_table, None, 10)
                            data_acl = f.read()
                            url_table = url + url_dict[table][1]
                            f = opener.open(url_table, None, 10)
                            data_ra_access = f.read()
                            response_data = function_dict[
                                table](data_acl, data_ra_access)

                        else:
                            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm(
                            )
                            top_level_url = url
                            password_mgr.add_password(
                                None, top_level_url, username, password)
                            handler = urllib2.HTTPBasicAuthHandler(
                                password_mgr)
                            opener = urllib2.build_opener(handler)
                            url_table = url + url_dict[table]
                            f = opener.open(url_table, None, 10)
                            data = f.read()
                            response_data = function_dict[table](data)
                        if response_data['success'] == 0:
                            result_dict[table] = response_data['result']

                        temp_list.remove(table)
                        success = 0
                except socket.error as sock_err:
                    success = 1
                    # print str(sock_err)
                    result_dict[551] = str(sock_err)
                    break
                except urllib2.URLError, e:
                    success = 1
                    errno, str_err = e.args[0] if len(
                        e.args) > 0 else (0, str(e))
                    if errno == 113:
                        result_dict[551] = " " + str_err
                    else:
                        result_dict[99] = " URL Error " + str_err
                    break

                except Exception, e:
                    success = 0

                loop -= 1
                if len(temp_list) < 1:
                    break

        else:
            success = 1
            result_dict[
                96] = "arguments are not proper : (url , username, password) all arguments should be as String"

    except urllib2.URLError, e:
        success = 1
        # errno, str_err = e.args[0]
        errno, str_err = e.args[0] if len(e.args) > 0 else (0, str(e))
        if errno == 113:
            result_dict[551] = " Error " + str_err
        else:
            result_dict[99] = " URL Error " + str_err

    except Exception, e:
        success = 1
        result_dict[98] = "EXCEPTION : " + str(e)
    finally:
        response_dict = {}
        response_dict['success'] = success
        response_dict['result'] = result_dict
        return response_dict


class Connection(object):
    """Connects and logs into the specified hostname.
    Arguments that are not given are guessed from the environment."""

    def __init__(self,
                 host,
                 username=None,
                 private_key=None,
                 password=None,
                 port=22,
                 ):
        self._sftp_live = False
        self._sftp = None
        self.ok = True
        if not username:
            username = os.environ['LOGNAME']

        # Log to a temporary file.
        # templog = tempfile.mkstemp('.txt', 'ssh-')[1]
        # paramiko.util.log_to_file(templog)

        # Begin the SSH transport.
        try:
            self._transport = paramiko.Transport((host, port))
            self._tranport_live = True
            # Authenticate the transport.
            if password:
                    # Using Password.
                self._transport.connect(
                    username=username, password=password)
            else:
                # Use Private Key.
                if not private_key:
                        # Try to use default key.
                    if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                        private_key = '~/.ssh/id_rsa'
                    elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                        private_key = '~/.ssh/id_dsa'
                    else:
                        raise TypeError(
                            "You have not specified a password or key.")

                private_key_file = os.path.expanduser(private_key)
                rsa_key = paramiko.RSAKey.from_private_key_file(
                    private_key_file)
                self._transport.connect(username=username, pkey=rsa_key)

        except Exception, e:
            self.ok = False
            pass

    def _sftp_connect(self):
        """Establish the SFTP connection."""
        if self.ok:
            if not self._sftp_live:
                self._sftp = paramiko.SFTPClient.from_transport(
                    self._transport)
                self._sftp_live = True

    def get(self, remotepath, localpath=None):
        """Copies a file between the remote host and the local host."""
        if self.ok:
            if not localpath:
                localpath = os.path.split(remotepath)[1]
            self._sftp_connect()
            self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath=None):
        """Copies a file between the local host and the remote host."""
        if self.ok:
            if not remotepath:
                remotepath = os.path.split(localpath)[1]
            self._sftp_connect()
            self._sftp.put(localpath, remotepath)

    def execute(self, command):
        """Execute the given commands on a remote machine."""
        if self.ok:
            channel = self._transport.open_session()
            channel.exec_command(command)
            output = channel.makefile('rb', -1).readlines()
            if output:
                return output
            else:
                return channel.makefile_stderr('rb', -1).readlines()

    def run(self, command):
        """Execute the given commands on a remote machine."""
        if self.ok:
            channel = self._transport.open_session()
            channel.exec_command(command)

    def close(self):
        """Closes the connection and cleans up."""
        # Close SFTP Connection.
        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False
        # Close the SSH Transport.
        if self._tranport_live:
            self._transport.close()
            self._tranport_live = False

    def __del__(self):
        """Attempt to clean up if not explicitly closed."""
        self.close()


def sshmain(ip_address):
    """Little test when called directly."""
    # Set these to your own details.
    try:
        myssh = Connection(ip_address, 'root', None, 'public')
        # myssh.put('myssh.py')
        myssh.run(
            "a=$( ps | grep snmpagent | grep -v grep | awk '{print $1}');c=1;for i in $a;do if [ $c -gt 1 ];then kill $i;fi;c=`expr ${c} + 1`;done;")
        myssh.run('/stureplan/sbin/snmpagent &')
        myssh.close()
        print " ;; "
    except Exception, e:
        pass
        # print " IN SEXCEPTION ",str(e[-1])


## for printing better name at output
name_table_dict = {'get_odu16_synch_statistics_table': 'SYNC_STATISTICS',
                   'get_odu16_nw_interface_statistics_table': 'NW_IFACE_STATISTICS',
                   'get_odu16_ra_tdd_mac_statistics_entry': 'TDD_STATISTICS',
                   'get_odu16_peer_node_status_table': 'PEER_NODE_STATUS',
                   'idu_linkStatusTable': 'LINK_STATUS',
                   'idu_e1PortStatusTable': 'E1_PORT_STATUS',
                   'idu_linkStatisticsTable': 'LINK_STATISTICS',
                   'idu_tdmoipNetworkInterfaceStatisticsTable': 'TDMOIP_STATISTICS',
                   'idu_iduNetworkStatisticsTable': 'NETWORK_STATISTICS',
                   'idu_portstatisticsTable': 'PORT_STATISTICS',
                   'idu_swPrimaryPortStatisticsTable': 'SW_PORT_STATISTICS',
                   'idu_portSecondaryStatisticsTable': 'PORT_SEC_STATISTICS',
                   'odu100_peerNodeStatusTable': 'PEER_NODE_STATUS',
                   'odu100_raTddMacStatisticsTable': 'TDD_MAC_STATISTICS',
                   'odu100_nwInterfaceStatisticsTable': 'NW_IFACE_STATISTICS',
                   'odu100_synchStatisticsTable': 'SYNC_STATISTICS',
                   'odu100_peerTunnelStatisticsTable': 'PEER_TUNNEL_STATISTICS',
                   'odu100_peerLinkStatisticsTable': 'PEER_LINK_STATISTICS',
                   'odu100_peerConfigTable': 'PEER_CONFIG_STATISTICS',
                   'odu100_raStatusTable': 'RA_STATUS',
                   'odu100_nwInterfaceStatusTable': 'NW_IFACE_STATISTICS',
                   'odu100_synchStatusTable': 'SYNC_STATUS',
                   }


########################## NOTE
# Please Remember : when you add oid of table please add .1 at last
# like if table oid is '.1.3.6.1.4.1.26149.2.2.11.2' then add .1 at last so new oid is '.1.3.6.1.4.1.26149.2.2.11.2.1'
# thats it
odu16_table_dict = {
}

idu4_table_dict = {
}

odu100_table_dict = {
    'odu100_peerNodeStatusTable': '.1.3.6.1.4.1.26149.2.2.13.9.2.1',
    'odu100_raTddMacStatisticsTable': '.1.3.6.1.4.1.26149.2.2.13.7.3.1',
    'odu100_nwInterfaceStatisticsTable': '.1.3.6.1.4.1.26149.2.2.12.3.1',
    'odu100_synchStatisticsTable': '.1.3.6.1.4.1.26149.2.2.11.2.1',
    #'odu100_peerTunnelStatisticsTable':'1.3.6.1.4.1.26149.2.2.13.9.3.1',
    #'odu100_peerLinkStatisticsTable':'1.3.6.1.4.1.26149.2.2.13.9.4.1',
    'odu100_raStatusTable': '1.3.6.1.4.1.26149.2.2.13.2.1',
    'odu100_nwInterfaceStatusTable': '1.3.6.1.4.1.26149.2.2.12.2.1',
    'odu100_synchStatusTable': '1.3.6.1.4.1.26149.2.2.11.3.1',
}

main_dict = {'odu16': odu16_table_dict,
             'odu100': odu100_table_dict,
             'idu4': idu4_table_dict
             }
############################ Please read NOTE before addition of new table

error_dict = {0: 'noError',
              1: 'tooBig packet',
              2: 'noSuchName',
              3: 'badValue',
              4: 'readOnly',
              # 5:'genErr',
              6: 'noAccess',
              7: 'wrongType',
              8: 'wrongLength',
              9: 'wrongEncoding',
              10: 'wrongValue',
              11: 'noCreation',
              12: 'inconsistentValue',
              13: 'resourceUnavailable',
              14: 'commitFailed',
              15: 'undoFailed',
              16: 'authorizationError',
              17: 'notWritable',
              18: 'inconsistentName',
              50: 'unKnown',
              551: 'networkUnreachable',
              52: 'typeError',
              553: 'Request Timeout.Please Wait and Retry Again',
              54: '0active_state_notAble_to_lock',
              55: '1active_state_notAble_to_Unlock',
              91: 'Arguments are not proper',
              96: 'InternalError',
              97: 'ip-port-community_not_passed',
              98: 'otherException',
              99: 'pysnmpException',
              102: 'Unkown Error Occured'}

global db, host_id
# take argument by command line
arg = sys.argv


def defult_data_insert(table_name, ip_address, is_disable=1):
    try:
        exit_status = 1
        timestamp = datetime.now()

        nwStatsIndex, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, rx_multicast, colisions, rx_crc_err, rx_phy_err, sig_strength, sync_lost = 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111

        global db, host_id
        if db == 1:
            raise SelfCreatedException(' can not connect to database ')
        result = host_id
        cursor = db.cursor()

        if table_name.strip() == 'odu100_nwInterfaceStatisticsTable':
            for j in range(2):
                ins_query = "INSERT INTO `odu100_nwInterfaceStatisticsTable`(`host_id`,`nwStatsIndex`,`rxPackets`,`txPackets`,`rxBytes`,`txBytes`,`rxErrors`,`txErrors`,`rxDropped`,`txDropped`,`timestamp`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    result, j + 1, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_err, tx_err, rx_drop, tx_drop, datetime.now())
                cursor.execute(ins_query)
                db.commit()
        elif table_name.strip() == 'odu100_raTddMacStatisticsTable':
            ins_query = "INSERT INTO `odu100_raTddMacStatisticsTable`(`host_id`, `raIndex`, `rxpackets`, `txpackets`, `rxerrors`, `txerrors`, `rxdropped`, `txdropped`, `rxCrcErrors`, `rxPhyError`, `timestamp`) values('%s','1','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                result, rx_packets, tx_packets, rx_err, tx_err, rx_drop, tx_drop, rx_crc_err, rx_phy_err, datetime.now())
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip() == 'odu100_synchStatisticsTable':
            ins_query = "INSERT INTO `odu100_synchStatisticsTable`(`host_id`,`syncConfigIndex`,`syncLostCounter`,`timestamp`) values('%s','1','%s','%s')" % (
                result, sync_lost, datetime.now())
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip() == 'odu100_peerNodeStatusTable':
            ins_query = "INSERT INTO `odu100_peerNodeStatusTable` (`host_id`, `raIndex`, `timeSlotIndex`, `linkStatus`, `tunnelStatus`, `sigStrength1`, `peerMacAddr`, `ssIdentifier`, `peerNodeStatusNumSlaves`, `peerNodeStatusrxRate`, `peerNodeStatustxRate`, `allocatedTxBW`, `allocatedRxBW`, `usedTxBW`, `usedRxBW`, `txbasicRate`, `sigStrength2`, `rxbasicRate`, `txLinkQuality`, `peerNodeStatustxTime`, `peerNodeStatusrxTime`,`negotiatedMaxUplinkBW`,`negotiatedMaxDownlinkBW`,`peerNodeStatuslinkDistance` ,`timestamp`) VALUES ( '%s', '1', '1', '1111111', '1111111', '%s', '1111111', '1111111', '0', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '%s', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '1111111', '%s')" % (
                result, sig_strength, sig_strength, datetime.now())
            cursor.execute(ins_query)
            db.commit()

        elif table_name.strip() == 'odu100_peerTunnelStatisticsTable':
            ins_query = "INSERT INTO `odu100_peerTunnelStatisticsTable` (`host_id`, `raIndex`,`tsIndex`,`rxPacket`,`txPacket`,`rxBundles`,`txBundles`, `timestamp`) VALUES ('%s', 1, 1, 1111111, 1111111, 1111111,1111111, '%s')" % (result, datetime.now())
            cursor.execute(ins_query)
            db.commit()
        elif table_name.strip() == 'odu100_peerLinkStatisticsTable':
            ins_query = "INSERT INTO `odu100_peerLinkStatisticsTable` (`host_id`, `raIndex`, `timeslotindex`, `txdroped`, `rxDataSubFrames`, `txDataSubFrames`, `signalstrength1`, `txRetransmissions5`, `txRetransmissions4`, `txRetransmissions3`, `txRetransmissions2`, `txRetransmissions1`, `txRetransmissions0`, `rxRetransmissions5`, `rxRetransmissions4`, `rxRetransmissions3`, `rxRetransmissions2`, `rxRetransmissions1`, `rxRetransmissions0`, `rxBroadcastDataSubFrames`, `rateIncreases`, `rateDecreases`, `emptyRasters`, `rxDroppedTpPkts`, `rxDroppedRadioPkts`, `signalstrength2`, `timestamp`) VALUES ('%s', 1, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, 1111111, '%s')" % (
                result, datetime.now())
            cursor.execute(ins_query)
            db.commit()

        elif table_name.strip() == 'odu100_nwInterfaceStatusTable':
            ins_query = "INSERT INTO `odu100_nwInterfaceStatusTable` ( `host_id` ,`nwStatusIndex` ,`nwInterfaceName`, `operationalState` ,`macAddress` ,`timestamp`) \
VALUES ('%s', '1', '1111111', '1111111', '1111111', '%s')" % (result, timestamp)
            cursor.execute(ins_query)
            db.commit()

        elif table_name.strip() == 'odu100_synchStatusTable':
            ins_query = "INSERT INTO `odu100_synchStatusTable` (`host_id`, `syncConfigIndex`,`timerAdjust`,`syncoperationalState`, `syncpercentageDownlinkTransmitTime`, `syncrasterTime`,`timestamp`) VALUES (%s,'1','1111111','1111111','1111111','1111111','%s')" % (result, timestamp)
            cursor.execute(ins_query)
            db.commit()

        elif table_name.strip() == 'odu100_raStatusTable':
            ins_query = "INSERT INTO `odu100_raStatusTable` (`host_id`, `raIndex`, `currentTimeSlot`,`raMacAddress`,`unusedTxTimeUL`,`unusedTxTimeDL`, `raoperationalState`,  `timestamp`) VALUES ('%s', '1', '1111111', '1111111', '1111111', '1111111','1111111','%s')" % (
                result, timestamp)
            cursor.execute(ins_query)
            db.commit()

        exit_status = 1
        # print ins_query
        # close the connection
    except MySQLdb.Error as e:
        # print ins_query
        print "MySQLdb Exception in ddb " + name_table_dict[
            table_name] + " : " + st
        # print traceback.format_exc()
        exit_status = 2
    except SelfCreatedException as e:
        print str(e)
        exit_status = 2
    except Exception as e:
        print str(e[-1])
        exit_status = 2
    finally:
        if db != 1:
            cursor.close()
        return exit_status


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
        # print " is_filled ",table_list
        try:
            for table_name in temp_list:
                return_value = 0
                if table_name.strip() == 'odu100_nwInterfaceStatisticsTable':
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

                if sel_query:
                    # print sel_query
                    cursor.execute(sel_query)
                    sel_result = cursor.fetchall()
                    # print sel_result
                    if len(sel_result) > 0:
                        if len(sel_result[0]) == map(str, sel_result[0]).count('1111111'):
                            return_value = 1
                        if return_value:
                            table_list.remove(table_name)
        # close the connection
        except MySQLdb.Error as e:
            print "MySQLdb Exception in filling " + \
                name_table_dict[table_name] + " : " + str(e[-1])
            # print sel_query
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
        if db != 1:
            cursor.close()
        table_list.append(return_value)
        return table_list


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
                        pycmdgen.CommunityData('tableodu-agent', community), pycmdgen.UdpTransportTarget((ip_address, port), timeout, retries), make_tuple(oid))

                var_dict = {}

                if errorIndication and len(varBindTable) < 1:
                    success = 1
                    err_dict[553] = str(errorIndication)
                    # handle

                else:
                    if errorStatus:
                        err_dict[int(errorStatus)] = str(errorStatus)
                        success = 1
                        # print '%s at %s\n' % (
                        # errorStatus.prettyPrint(),errorIndex and
                        # varBindTable[-1][int(errorIndex)-1] or '?')
                    else:
                        success = 0
                        oid_li = []
                        var_dict = {}
                        is_oid2 = 0
                        # print varBindTable
                        # print
                        # print
                        for varBindTableRow in varBindTable:
                            for name, val in varBindTableRow:
                                # print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                                # print name.prettyPrint()
                                oid_values_list = name.prettyPrint(
                                ).split(oid)[1][1:].split('.')
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
                success = 2
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


def db_connect():
    """
    Used to connect to the database :: return database object assigned in global_db variable
    """
    try:
        return MySQLdb.connect(hostname, username, password, schema)
        # db_obj = MySQLdb.connect("172.22.0.95","root","root","nms_p")
    except MySQLdb.Error as e:
        print str(e)
        raise
    except Exception as e:
        print "Exception in database connection " + str(e)
        raise


def host_status(hostid, status, host_ip=None, prev_status=0):
    """
    @note: Used to update host operation status and varify it
    """
    value = 0
    plugin_status = 0
    try:
        db = db_connect()
        if hostid:
            sel_query = """select status,plugin_status from host_status  where host_id = '%s'""" % (
                str(hostid))
        elif host_ip:
            sel_query = """select status,plugin_status from host_status  where host_ip = '%s'""" % (host_ip)
        else:
            value = 0  # error 100
            return
        if status is None:
            value = 0  # error 100
            return
        cursor = db.cursor()
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if len(result) > 0:
            if int(result[0][0]) == prev_status or int(result[0][0]) == int(status):
                if hostid:
                    up_query = """update host_status set status='%s', plugin_status = 0 where host_id = '%s'""" % (
                        status, hostid)
                elif host_ip:
                    up_query = """update host_status set status='%s', plugin_status = 0 where host_ip = '%s'""" % (
                        status, host_ip)
                cursor.execute(up_query)
                db.commit()
                value = 0
            else:
                value = result[0][0]
            plugin_status = result[0][1]
        else:
            value = 0  # value = 100 no row found
        cursor.close()

    except MySQLdb.Error as e:
        pass
    except Exception as e:
        pass
    finally:
        return int(value), int(plugin_status)


def update_plugin_state(state, host_ip):
    """
    @note: Used to update host operation status and varify it
    """
    global db
    try:
        up_query = """update host_status set plugin_status = %s  where host_ip = '%s'""" % (
            state, host_ip)
        cursor = db.cursor()
        cursor.execute(up_query)
        cursor.close()
        db.commit()
    except MySQLdb.Error as e:
        pass
    except Exception as e:
        pass


def get_columns(firmware_id, table_name):
    global db
    result = ''

    try:
        query = """SELECT indexes_name, coloumn_name FROM odu100_%s_oids WHERE table_name = '%s'""" % (
            firmware_id.replace('.', '_'), table_name.split('_')[-1])
        # print query
        cur = db.cursor()
        if cur.execute(query):
            result = cur.fetchall()
            result = """(host_id, %s %s, timestamp) \
                        """ % (
                result[0][0] + ',',
                # '' if result[0][0] == 'NULL' else result[0][0]+',',
                ', '.join([t[1] for t in result])
            )
        cur.close()
    except Exception, e:
        print " get_columns ", str(e)
        # print traceback.format_exc()
    finally:
        return result


def insert_db(result_dict, table_name, firmware_id):
    global db, host_id
    success = 1
    ins_query = "INSERT INTO %s %s values " % (
        table_name, get_columns(firmware_id, table_name))
    # print ins_query
    flag = 1
    ins_str = ""
    date_time = datetime.now()
    for i in result_dict:
        if flag == 1:
            ins_query += "('%s'" % (host_id)
            ins_len = len(result_dict[i])
            for ln in xrange(ins_len):
                ins_str += " ,'%s'"
            flag = 0
        else:
            ins_query += ", ('%s'" % (host_id)

        ins_query += ins_str % tuple(result_dict[i])
        ins_query += ", '%s')" % (date_time)
    # print ins_query

    cursor = db.cursor()
    try:
        cursor.execute(ins_query)  # execute the query
        db.commit()               # save the value in data base
    except Exception, e:
        success = 0
        print name_table_dict[table_name], ":", e[1]
    cursor.close()
    return success


###### @@@ main program starts from here

def main():
    global db, host_id
    ip_address, db, cursor = None, None, None
    try:
        exit_status = 1
        if arg.count('-i') and arg.count('-p'):
            # receive the ip address
            ip_address = arg[arg.index("-i") + 1]

            # receive port number
            port_no = arg[arg.index("-p") + 1]

            run_loop = 0
            device_type = 'odu100'

            table_dict = main_dict[device_type]

            is_table = 0
            big_result_dict = {}
            cgi_list = []
            if arg.count('-t'):
                is_table = 1
                single_table = arg[arg.index("-t") + 1]

            if is_table:
                table_list = [single_table]
            else:
                table_list = table_dict.keys()

            # open a db connection and make it global
            db = db_connect()

            # Get host details
            cursor = db.cursor()
            sql = "SELECT host_id, snmp_read_community, firmware_mapping_id \
                    FROM hosts WHERE ip_address = '%s' and is_deleted = 0" % ip_address
            if cursor.execute(sql):
                host_id, snmp_read, firmware_id = cursor.fetchone()
            else:
                plugin_message(
                    "host data dosn't exists in hosts table")
                exit_status = 1
                return
            cursor.close()

            host_state, plugin_state = host_status(None, 9, ip_address)

            if host_state == 0:
                db.close()
                # SNMP main for loop begin
                for table_name in table_dict:
                    snmp_result_dict = pysnmp_get_table(
                        str(table_dict[table_name]).strip('.'),
                        str(ip_address), int(port_no), snmp_read)

                    # print snmp_result_dict
                    if snmp_result_dict['success'] == 0:
                        result_dict = snmp_result_dict['result']
                        if len(result_dict) > 0:
                            big_result_dict[table_name] = result_dict
                        table_list.remove(table_name)
                    else:
                        temp_exit = 0
                        if int(snmp_result_dict['result'].keys()[0]) in error_dict:
                            print " No Response,", snmp_result_dict[
                                'result'].values()[0]
                        else:
                            print "For %s No Response, Unknown Error : %s " % (
                                name_table_dict.get(table_name, 'table_name'),
                                str(snmp_result_dict['result'].values()[0]))
                            temp_exit = 2

                        if snmp_result_dict['success'] == 2:
                            break

                        if not run_loop:
                            cgi_list.extend(table_list)
                            break
                        else:
                            run_loop -= 1
                            cgi_list.append(table_name)

                        # agent start
                        sshmain(ip_address)

                    if is_table:
                        break

                db = db_connect()
                host_status(None, 0, ip_address, 9)
                db.close()

            else:
                hstatus_dict = {
                    0: 'No operation', 1: 'Firmware download', 2: 'Firmware upgrade',
                    3: 'Restore default config', 4: 'Flash commit', 5: 'Reboot', 6: 'Site survey',
                    7: 'Calculate BW', 8: 'Uptime service', 9: 'Statistics gathering',
                    10: 'Reconciliation', 11: 'Table reconciliation', 12: 'Set operation',
                    13: 'Live monitoring', 14: 'Status capturing', 15: 'Refreshing Site Survey',
                    16: 'Refreshing RA Channel List'}

                schedule_round = 3
                if plugin_state > schedule_round:
                    cursor = db.cursor()
                    up_query = """UPDATE host_status SET plugin_status = 0 WHERE host_ip = '%s'""" % (
                        ip_address)
                    cursor.execute(up_query)
                    db.commit()
                    cursor.close()
                    db.close()
                    cgi_list.extend(table_list)
                    print " Device is busy, Device %s is in progress." % hstatus_dict.get(int(host_state), "other operation")
                else:
                    print "Service rescheduled"
                    print " Device is busy, Device %s is in progress." % hstatus_dict.get(int(host_state), "other operation")
                    update_plugin_state(plugin_state + 1, ip_address)
                    db.close()
                    return

            if len(table_list):
                cgi_result = cgi_opener(
                    ip_address, "admin", "public", table_list)

                if cgi_result['success'] == 0:
                    print " Additional Response OK "
                    for table_name in cgi_result['result']:
                        if len(cgi_result['result'][table_name]) > 0:
                            big_result_dict[
                                table_name] = cgi_result['result'][table_name]
                            table_list.remove(table_name)
                    exit_status = 0
                else:
                    print "  Addtional result : ", cgi_result[
                        'result']
            else:
                print " Response OK "

            db = db_connect()

            if len(table_list) > 0:
                print name_table_dict.get(table_list[0], table_list[0]), " remain: ", len(table_list), " cause: ", cgi_result['result']
                table_list = is_filled(table_list)
                return_value = table_list.pop()

                if return_value < 2:
                    for table_name in table_list:
                        big_result_dict[table_name] = None
                else:
                    exit_status = return_value

                if temp_exit:
                    exit_status = temp_exit

            # print big_result_dict
            for table_name in big_result_dict:
                if big_result_dict.get(table_name):
                    try:
                        insert_db(big_result_dict[
                                  table_name], table_name, firmware_id)
                        exit_status = 0
                    except Exception, e:
                        exit_status = 1
                        print '%s : Exception > %s during insert db' % (table_name, str(e))
                else:
                    exit_status = defult_data_insert(table_name, ip_address)
        else:
            plugin_message()
            exit_status = 1

    except MySQLdb.Error as e:
        print "MySQLdb Exception    " + str(e[-1])
        exit_status = 2
    except SelfCreatedException as e:
        print str(e)
        exit_status = 2
    except Exception as e:
        print "IN MAIN :  ", str(e[-1])
        exit_status = 2
    finally:
        if ip_address:
            host_status(None, 0, ip_address, 9)
        if isinstance(db, MySQLdb.connection):
            if db.open:
                if cursor:
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
                MONITOR ODU100_STATISTICS_OF_DEVICES:
                --------------------------------
                How to use:
                \t./%s -i 192.168.1.1 -p 161
                \t-i\t Ip Address
                \t-p\t Port_no
                \t for single table -t Table_Name
                """ % (arg[0])
        sys.exit(2)

    else:
        plugin_message(
            '-------->>>> Please pass right arguments.\n               for HELP type # python2.6 %s --help or -h.' % (arg[0]))
        sys.exit(2)
