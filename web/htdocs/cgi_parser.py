#! /usr/bin/python2.6

from copy import deepcopy
import socket
import urllib2


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

# Reconcilation data
url_dict['odu100_ruConfTable'] = 'ruconfig.shtml'
url_dict['odu100_ruStatusTable'] = ['rustatus.shtml', 'eweb_index.shtml']
url_dict['odu100_swStatusTable'] = 'index.shtml'
url_dict['odu100_omcConfTable'] = 'omcconfiguration.shtml'
url_dict['odu100_ipConfigTable'] = 'ipconfiguration.shtml'
url_dict['odu100_hwDescTable'] = 'index.shtml'
url_dict['odu100_syncConfigTable'] = 'syncclockconfig.shtml'
url_dict['odu100_raConfTable'] = ['aclconfig.shtml', 'raaccessconfig.shtml']
url_dict['odu100_raChannelListTable'] = 'rachannellist.shtml'
url_dict['odu100_raAclConfigTable'] = 'cgi-bin/getaclmacaddress.sh'
url_dict['odu100_raLlcConfTable'] = 'llcconfig.shtml'
url_dict['odu100_raTddMacConfigTable'] = 'raaccessconfig.shtml'
url_dict['odu100_raTddMacStatusTable'] = 'raaccess.shtml'
url_dict['odu100_raPreferredRFChannelTable'] = 'preferredchannellist.shtml'
url_dict['odu100_peerConfigTable'] = 'peerconfig.shtml'


############################################################## monitoring

def odu100_peerNodeStatusTable(data):
    """

    @param data:
    @return:
    """
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
            'linkStatus', 'tunnelStatus', 'sigStrength1', 'macAddress', 'ssid', 'numSlaves', 'rxRate', 'txRate',
            'allocatedTxBW', 'allocatedRxBW', 'usedTxBW',
            'usedRxBW', 'txBasicRate', 'sigStrength2', 'rxBasicRate', 'txLinkQuality', 'txTime', 'rxTime',
            'negotiatedMaxUplinkBW', 'negotiatedMaxDownlinkBW', 'linkDistance']
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
    """

    @param data:
    @return:
    """
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
    """

    @param data:
    @return:
    """
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
    """

    @param data:
    @return:
    """
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
    """

    @param data:
    @return:
    """
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
    """

    @param data:
    @return:
    """
    success = 0
    try:
        s = data
        main_str_list = ["Sync Operational State", "Raster Time",
                         "Time Adjust", "Percentage Downlink Transmit Time"]
        find_string_list = [
            '<td align="left"><div id="operationalstate">', '<td align="left"><div id="rastertime">',
            '<td align="left">',
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
    """

    @param data:
    @return:
    """
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


############################################ Status tables

def odu100_raStatusTable(data):
    """

    @param data:
    @return:
    """
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
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}


def odu100_synchStatusTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ["Sync Operational State", "Raster Time",
                         "Time Adjust", "Percentage Downlink Transmit Time"]
        find_string_list = [
            '<td align="left"><div id="operationalstate">', '<td align="left"><div id="rastertime">',
            '<td align="left">',
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
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}


def odu100_nwInterfaceStatusTable(data):
    """

    @param data:
    @return:
    """
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
            temp_status = [count, i['name'], opstate, i['macAddress'], count]
            interface_status[count] = temp_status
            count = count + 1
        success = 0
    except Exception, e:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': interface_status}
        else:
            return {'success': success, 'result': {}}


####################################### reconcilation Tables
def odu100_ruConfTable(data):
    """

    @param data:
    @return:
    """
    try:
        s = data
        main_str_list = [
            '** Update RU admin state drop-down listbox.', '** Update Tier drop-down listbox.',
            '** Update channel bandwidth drop-down listbox.',
            '** Update synchSource drop-down listbox.', 'm** Update country code drop-down listbox.',
            '** Update poe state drop-down listbox.',
            'RU.RUConfTable.alignmentControl']

        find_string_list = [
            'var synchSource = ', 'var nodeType = ', 'var channelBandwidth = ',
            'var synchSource = ', 'var countryCode = ', 'var poeState = ',
            'onBlur="checkField(this)" value="']
        end_string_list = [";", ";", ";", ";", ";", ";", '"']
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
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_ruStatusTable(data_ru_op_state, data):  # view-source:http://172.22.0.120/eweb_index.shtml
    """

    @param data_ru_op_state:
    @param data:
    @return:
    """
    try:
        s = data_ru_op_state
        find_str = '<div id="opstate">'
        ind = s.find(find_str)
        ind2 = s.find("</div>", ind + 1)
        ru_op_state = s[ind + len(find_str):ind2].strip()
        s = data
        main_str_list = ['Last Reboot Reason', 'Config Commited', 'Uptime(seconds)',
                         'POE State', 'CPU ID',
                         'BW Capability(kbps)']

        find_string_list = [
            '<div id="rebootreason">', '<div id="yesnostate">', '<div id="status_value">',
            '<div id="opstate">', '<div id="status_value">',
            '<div id="status_value">']
        end_string_list = ["</div>", "</div>", "</div>",
                           "</div>", "</div>",
                           '</div>']
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
        list_data.insert(6, ru_op_state)
        # list_data.append(data.strip())
        # return {1:[list_data]}
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}


def odu100_swStatusTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['Active Version Number',
                         'Passive Version Number', 'Boot Loader Version']
        find_string_list = ['<td align="left">',
                            '<td align="left">', '<td align="left">']
        end_string_list = ['</td>', '</td>', '</td>']
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
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_omcConfTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['OMC IP Address', 'Periodic Statistics Timer']
        find_string_list = ['onBlur="checkField(this)" value="',
                            'onBlur="checkField(this)" value="']
        end_string_list = ['" ', '" ']
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
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_ipConfigTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = [
            '** Update IP admin state drop-down listbox.', '<td align="left">IP Address<br/>',
            '<td align="left">IP Netmask</td>',
            '<td align="left">IP Default Gateway</td>', '** Update DHCP state drop-down listbox.', 'var manState',
            'name="RU.IPConfigTable.managementVlanTag" onBlur="checkField(this)" id="managementVlanTag']
        find_string_list = [
            'var ipAdminState = ', 'id="ru.np.ip.ipAddress" value="', 'id="ru.np.ip.ipNetworkMask" value="',
            'id="ru.np.ip.ipDefaultGateway" value="', 'var dhcpState = ', '=', 'value="']
        end_string_list = [';', '" size="20"></td>',
                           '" size="20"></td>', '" size="20"></td>', ';', ';', '"']
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
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_hwDescTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['Hardware Version', 'Hardware Serial Number']
        find_string_list = ['<td align="left">', '<td align="left">']
        end_string_list = ['</td>', '</td>']
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
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_syncConfigTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['** Update sync admin state drop-down listbox.', 'Raster Time (RW_LO:SYNC)',
                         'Sync Loss Threshold',
                         'Leaky bucket Timer', 'Sync loss Timeout', 'Sync Timer Adjust (RW_LO:SYNC)',
                         'Percentage Downlink Transmit Time (RW_LO:SYNC)']
        find_string_list = ['var syncAdminState = ',
                            'name="RU.SyncClock.SyncConfigTable.rasterTime" onBlur="checkField(this)" value="',
                            'name="RU.SyncClock.SyncConfigTable.syncLossThreshold" onBlur="checkField(this)" value="',
                            'name="RU.SyncClock.SyncConfigTable.leakyBucketTimer" onBlur="checkField(this)" value="',
                            'name="RU.SyncClock.SyncConfigTable.syncLostTimeout" onBlur="checkField(this)" value="',
                            'name="RU.SyncClock.SyncConfigTable.timerAdjust" onBlur="checkField(this)" id="ru.np.synch.timerAdjust" value="',
                            'name="RU.SyncClock.SyncConfigTable.percentageDownlinkTransmitTime" onBlur="checkField(this)" value="']
        end_string_list = [';', '" size="15"', '" size="15">', '" size="15">',
                           '" size="15"></td>', '" size="3">', '" size="15">']
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
            if i == 1:
                list_data.append('1')
            list_data.append(data.strip())
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_raConfTable(data_acl, data_ra_config):
    """

    @param data_acl:
    @param data_ra_config:
    @return:
    """
    success = 1
    try:
        s = data_acl
        find_str = "var ra1ACLMode = "
        ind = s.find(find_str)
        ind2 = s.find(";", ind + 1)
        acl_mode = s[ind + len(find_str):ind2].strip()
        # print acl_mode
        s = data_ra_config
        main_str_list = ['** Update radio admin state drop-down listbox.', '<td align="left">SSID (RW_LO:RA)</td>',
                         'Guaranteed Broadcast BW(RW_LO:RA)', '** Update dba state drop-down listbox.',
                         '** Update acm state drop-down listbox.',
                         '** Update acs state drop-down listbox.', '** Update dfs state drop-down listbox',
                         '** Update numSlaves drop-down listbox.', '/*** Update dfs state drop-down listbox */',
                         'var linkdistance']
        find_string_list = ['var raAdminState = ', 'name="RU.RA.1.RAConfTable.ssId" onBlur="checkField(this)" value="',
                            'name="RU.RA.1.RAConfTable.guaranteedBroadcastBW" onBlur="checkField(this)" value="',
                            'var raDba = ', 'var raAcm = ',
                            'var raAcs = ', 'var raDfs = ', 'var numSlaves = ', 'var raantennaport = ', '=']
        end_string_list = [';', '" size="15"></td>',
                           '" size="15"></td>', ';', ';', ';', ';', ';', ';', ';']
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
            if i == 1:
                list_data.append(acl_mode)
            list_data.append(data.strip())
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:[list_data]}


def odu100_raLlcConfTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['<td align="left">Retransmit Window Size(Low)</td>',
                         '<td align="left">Retransmit Window Size(High)</td>',
                         '<td align="left">Frame Loss Threshold</td>', '<td align="left">Leaky Bucket Timer</td>',
                         '<td align="left">Frame Loss Timeout</td>']
        find_string_list = ['name="RU.RA.1.LLC.RALLCConfTable.arqWinLow" onBlur="checkField(this)" value="',
                            'name="RU.RA.1.LLC.RALLCConfTable.arqWinHigh" onBlur="checkField(this)" value="',
                            'name="RU.RA.1.LLC.RALLCConfTable.frameLossThreshold" onBlur="checkField(this)" value="',
                            'name="RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer" onBlur="checkField(this)" value="',
                            'name="RU.RA.1.LLC.RALLCConfTable.frameLossTimeout" onBlur="checkField(this)" value="']
        end_string_list = ['" size="15"></td>', '" size="15"></td>',
                           '" size="15"></td>', '" size="15"></td>', '" size="15"></td>']
        list_data = []
        for i in range(len(main_str_list)):
            main_str = main_str_list[i]
            find_string = find_string_list[i]
            end_string = end_string_list[i]
            data_index = s.find(main_str)
            data_index_start = s.find(find_string, data_index + len(main_str))
            data_index_start = data_index_start + len(find_string)
            data_index_end = s.find(end_string, data_index_start)
            data = s[data_index_start:data_index_end]
            # dict_data[count]=data.strip()
            list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:list_data}


def odu100_raTddMacConfigTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['<td align="left">Pass Phrase (RW_LO:RA)</td>', '** Update numSlaves drop-down listbox.',
                         "var oSelect = document.getElementById('txPower');", '<td align="left">Max CRC Errors</td>',
                         '<td align="left">Leaky Bucket Timer</td>',
                         '** Update radio encryptionType drop-down listbox.']
        find_string_list = ['name="RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase" onBlur="checkField(this)" value="',
                            'var x ="',
                            'var max_Power= "',
                            'name="RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors" onBlur="checkField(this)" value="',
                            'name="RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer" onBlur="checkField(this)" value="',
                            'var raEncryptionType =']
        end_string_list = ['" size="15"></td>', '";', '";',
                           '" size="15"></td>', '" size="15"></td>', ';']
        list_data = []
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
            # list_data.append(data.strip())
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:list_data}


def odu100_raTddMacStatusTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['<td align="left">Current Frequency</td>']
        find_string_list = ['<td align="left">']
        end_string_list = ["</td>"]
        list_data = []
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
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': {1: list_data}}
        else:
            return {'success': success, 'result': {}}
            # return {1:list_data}


def odu100_raPreferredRFChannelTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['function selectFreq()', '$("#Freq1").val(rfChannel);', '$("#Freq2").val(rfChannel);',
                         '$("#Freq3").val(rfChannel);',
                         '$("#Freq4").val(rfChannel);', '$("#Freq5").val(rfChannel);', '$("#Freq6").val(rfChannel);',
                         '$("#Freq7").val(rfChannel);', '$("#Freq8").val(rfChannel);', '$("#Freq9").val(rfChannel);']
        find_string_list = [
            'var rfChannel = ', 'rfChannel = ', 'rfChannel = ', 'rfChannel = ',
            'rfChannel = ', 'rfChannel = ', 'rfChannel = ',
            'rfChannel = ', 'rfChannel = ', 'rfChannel = ']
        end_string_list = [";", ";", ";", ";", ";", ";", ";", ";", ";", ";"]
        list_data = []
        dict_data = {}
        count = 1
        for i in range(len(main_str_list)):
            main_str = main_str_list[i]
            find_string = find_string_list[i]
            end_string = end_string_list[i]
            data_index = s.find(main_str)
            data_index_start = s.find(find_string, data_index + len(main_str))
            data_index_start = data_index_start + len(find_string)
            data_index_end = s.find(end_string, data_index_start)
            data = s[data_index_start:data_index_end]
            temp_list = [count, data.strip()]
            list_data.append(temp_list)
            dict_data[count] = temp_list
            count = count + 1
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': dict_data}
        else:
            return {'success': success, 'result': {}}

            # return dict_data


def odu100_raChannelListTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str = 'var x1,x2,x3,x4,x5,x6,x7,x8;'
        find_string = 'var finalString= "'
        end_string = '";'
        # list_data=[]
        dict_data = {}
        count = 1
        data_index = s.find(main_str)
        data_index_start = s.find(find_string, data_index + len(main_str))
        data_index_start = data_index_start + len(find_string)
        data_index_end = s.find(end_string, data_index_start)
        data = s[data_index_start:data_index_end].split(' ')
        i = 0
        while i in range(len(data) - 1):
            temp_list = [count, data[i].strip(), data[i + 1].strip()]
            # list_data.append(temp_list)
            dict_data[count] = temp_list
            count = count + 1
            i = i + 2
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': dict_data}
        else:
            return {'success': success, 'result': {}}

            # return dict_data


def odu100_raAclConfigTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        num = 'num'
        acl = 'acl'
        macAddress = 'macAddress'
        di = eval(s)
        count = 1
        temp_list = []
        list_data = []
        dict_data = {}
        count_dict = 1
        for i in di['acl']:
            if i['macAddress'] != "":
                temp_list = [count, i['macAddress'], '1']
                dict_data[count_dict] = temp_list
                count_dict = count_dict + 1
                # list_data.append(temp_list)
            count = count + 1

        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': dict_data}
        else:
            return {'success': success, 'result': {}}


def odu100_peerConfigTable1(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = ['function convertIntoArray(checkOrNot)', ' peerConfigArray[0] =',
                         'peerConfigArray[1] = ', 'peerConfigArray[2] =', 'peerConfigArray[3] =',
                         'peerConfigArray[4] =', 'peerConfigArray[5] =', 'peerConfigArray[6] =',
                         'peerConfigArray[7] =', 'peerConfigArray[8] =', 'peerConfigArray[9] =',
                         'peerConfigArray[10] =', 'peerConfigArray[11] =', 'peerConfigArray[12] =',
                         'peerConfigArray[13] =', 'peerConfigArray[14] =']
        find_string_list = [
            'mac= "', 'guaranteedDownlinkBW= "', 'guaranteedUplinkBW= "', 'maxDownlinkBW= "',
            'maxUplinkBW= "', 'basicRateMCSIndex= "']
        end_string_list = ['";', '";', '";', '";', '";', '";']
        list_data = []
        dict_data = {}
        count = 1
        for i in range(len(main_str_list)):
            main_str = main_str_list[i]
            temp_list = [count]
            for j in range(len(find_string_list)):
                find_string = find_string_list[j]
                end_string = end_string_list[j]
                data_index = s.find(main_str)
                data_index_start = s.find(
                    find_string, data_index + len(main_str))
                data_index_start = data_index_start + len(find_string)
                data_index_end = s.find(end_string, data_index_start)
                data = s[data_index_start:data_index_end]
                # if j==0 and data.strip()=='':
                #   data="new empty"
                temp_list.append(data.strip())
                # list_data.append(temp_list)
            dict_data[count] = temp_list
            count = count + 1
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': dict_data}
        else:
            return {'success': success, 'result': {}}
            # return dict_data


def odu100_peerConfigTable(data):
    """

    @param data:
    @return:
    """
    success = 1
    try:
        s = data
        main_str_list = [
            '<td align ="left"><b>1</b></td>', '<td align ="left"><b>2</b></td>',
            '<td align ="left"><b>3</b></td>', '<td align ="left"><b>4</b></td>',
            '<td align ="left"><b>5</b></td>', '<td align ="left"><b>6</b></td>',
            '<td align ="left"><b>7</b></td>', '<td align ="left"><b>8</b></td>',
            '<td align ="left"><b>9</b></td>', '<td align ="left"><b>10</b></td>',
            '<td align ="left"><b>11</b></td>', '<td align ="left"><b>12</b></td>',
            '<td align ="left"><b>13</b></td>', '<td align ="left"><b>14</b></td>',
            '<td align ="left"><b>15</b></td>', '<td align ="left"><b>16</b></td>']
        find_string_list = [
            'PEER1MAC" value="', 'guaranteedDownlinkBW" value="', 'guaranteedUplinkBW" value="',
            'maxDownlinkBW" value="',
            'maxUplinkBW" value="', 'basicRateMCSIndex" value="']
        end_string_list = ['" size="', '" size="', '" size="',
                           '" size="', '" size="', '" size="']
        list_data = []
        dict_data = {}
        count = 1
        for i in range(len(main_str_list)):
            main_str = main_str_list[i]
            temp_list = [count]
            for j in range(len(find_string_list)):
                find_string = find_string_list[j]
                end_string = end_string_list[j]
                data_index = s.find(main_str)
                data_index_start = s.find(
                    find_string, data_index + len(main_str))
                data_index_start = data_index_start + len(find_string)
                data_index_end = s.find(end_string, data_index_start)
                data = s[data_index_start:data_index_end]
                temp_list.append(data.strip())
            temp_list.insert(4, temp_list[6])
            temp_list.pop()
            check = 1
            for l in temp_list:
                if l == '':
                    check = check + 1
            if check != len(temp_list):
                dict_data[count] = temp_list
            count = count + 1
        success = 0
    except:
        success = 1
    finally:
        if success == 0:
            return {'success': success, 'result': dict_data}
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

# Reconcilation data
function_dict['odu100_ruConfTable'] = odu100_ruConfTable
function_dict['odu100_ruStatusTable'] = odu100_ruStatusTable
function_dict['odu100_swStatusTable'] = odu100_swStatusTable
function_dict['odu100_omcConfTable'] = odu100_omcConfTable
function_dict['odu100_ipConfigTable'] = odu100_ipConfigTable
function_dict['odu100_hwDescTable'] = odu100_hwDescTable
function_dict['odu100_syncConfigTable'] = odu100_syncConfigTable
function_dict['odu100_raConfTable'] = odu100_raConfTable
function_dict['odu100_raChannelListTable'] = odu100_raChannelListTable
function_dict['odu100_raAclConfigTable'] = odu100_raAclConfigTable
function_dict['odu100_raLlcConfTable'] = odu100_raLlcConfTable
function_dict['odu100_raTddMacConfigTable'] = odu100_raTddMacConfigTable
function_dict['odu100_raTddMacStatusTable'] = odu100_raTddMacStatusTable
function_dict[
    'odu100_raPreferredRFChannelTable'] = odu100_raPreferredRFChannelTable
function_dict['odu100_peerConfigTable'] = odu100_peerConfigTable
# print function_dict.keys()


def cgi_opener(ip, username, password, table_list):
    """

    @param ip:
    @param username:
    @param password:
    @param table_list:
    @return:
    """
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
                        elif table == 'odu100_ruStatusTable':
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
                    result_dict['51'] = str(sock_err)
                    break
                except urllib2.URLError, e:
                    success = 1
                    errno, str_err = e.args[0]
                    if errno == 113:
                        result_dict[51] = " " + str_err
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
        errno, str_err = e.args[0]
        if errno == 113:
            result_dict[51] = " Error " + str_err
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

# table_list=['odu100_raStatusTable', 'odu100_raPreferredRFChannelTable', 'odu100_raAclConfigTable', 'odu100_syncConfigTable', 'odu100_swStatusTable', 'odu100_nwInterfaceStatusTable', 'odu100_nwInterfaceStatisticsTable', 'odu100_peerNodeStatusTable', 'odu100_raConfTable', 'odu100_omcConfTable', 'odu100_ruStatusTable', 'odu100_raTddMacStatisticsTable', 'odu100_ruConfTable', 'odu100_raTddMacConfigTable', 'odu100_peerConfigTable', 'odu100_raLlcConfTable', 'odu100_synchStatisticsTable', 'odu100_raTddMacStatusTable', 'odu100_ipConfigTable', 'odu100_synchStatusTable', 'odu100_raChannelListTable', 'odu100_hwDescTable']
#
# tabel_res=['odu100_raStatusTable', # done
#'odu100_raPreferredRFChannelTable',
#'odu100_raAclConfigTable',
#'odu100_syncConfigTable',
#'odu100_swStatusTable',
#'odu100_nwInterfaceStatusTable',
#'odu100_nwInterfaceStatisticsTable',
#'odu100_peerNodeStatusTable',
#'odu100_raConfTable',
#'odu100_omcConfTable',
#'odu100_ruStatusTable',
#'odu100_raTddMacStatisticsTable',
#'odu100_ruConfTable',
#'odu100_raTddMacConfigTable',
#'odu100_peerConfigTable',
#'odu100_raLlcConfTable',
#'odu100_synchStatisticsTable',
#'odu100_raTddMacStatusTable',
#'odu100_ipConfigTable',
#'odu100_synchStatusTable',
#'odu100_raChannelListTable',
#'odu100_hwDescTable',]

table_oid_dict = {
    '1.3.6.1.4.1.26149.2.2.11.2.1': 'odu100_synchStatisticsTable',
    '1.3.6.1.4.1.26149.2.2.12.3.1': 'odu100_nwInterfaceStatisticsTable',
    '1.3.6.1.4.1.26149.2.2.13.7.3.1': 'odu100_raTddMacStatisticsTable',
    '1.3.6.1.4.1.26149.2.2.13.9.2.1': 'odu100_peerNodeStatusTable',
    '1.3.6.1.4.1.26149.2.2.1.1': 'odu100_ruConfTable',
    '1.3.6.1.4.1.26149.2.2.10.1': 'odu100_hwDescTable',
    '1.3.6.1.4.1.26149.2.2.11.1': 'odu100_syncConfigTable',
    '1.3.6.1.4.1.26149.2.2.11.3.1': 'odu100_synchStatusTable',
    '1.3.6.1.4.1.26149.2.2.12.2.1': 'odu100_nwInterfaceStatusTable',
    '1.3.6.1.4.1.26149.2.2.13.1.1': 'odu100_raConfTable',
    '1.3.6.1.4.1.26149.2.2.13.2.1': 'odu100_raStatusTable',
    '1.3.6.1.4.1.26149.2.2.13.3.1': 'odu100_raChannelListTable',
    '1.3.6.1.4.1.26149.2.2.13.5.1': 'odu100_raAclConfigTable',
    '1.3.6.1.4.1.26149.2.2.13.6.1': 'odu100_raLlcConfTable',
    '1.3.6.1.4.1.26149.2.2.13.7.1': 'odu100_raTddMacConfigTable',
    '1.3.6.1.4.1.26149.2.2.13.7.2': 'odu100_raTddMacStatusTable',
    '1.3.6.1.4.1.26149.2.2.13.7.4': 'odu100_raPreferredRFChannelTable',
    '1.3.6.1.4.1.26149.2.2.13.9.1': 'odu100_peerConfigTable',
    '1.3.6.1.4.1.26149.2.2.3.1': 'odu100_ruStatusTable',
    '1.3.6.1.4.1.26149.2.2.6.1': 'odu100_swStatusTable',
    '1.3.6.1.4.1.26149.2.2.7.1': 'odu100_omcConfTable',
    '1.3.6.1.4.1.26149.2.2.9.1': 'odu100_ipConfigTable'}


def cgi_recon(ip, table_oid, username='root', password='public'):
    """

    @param ip:
    @param table_oid:
    @param username:
    @param password:
    @return:
    """
    try:
        success = 1
        result_dict = {}
        table_list = [table_oid_dict[table_oid]
        ] if table_oid in table_oid_dict else []
        url = "http://" + ip + "/"
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
                        elif table == 'odu100_ruStatusTable':
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
                            result_dict = response_data['result']

                        temp_list.remove(table)
                        success = 0
                except socket.error as sock_err:
                    success = 1
                    result_dict['51'] = str(sock_err)
                    break
                except urllib2.URLError, e:
                    success = 1
                    errno, str_err = e.args[0]
                    if errno == 113:
                        result_dict[51] = " " + str_err
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
        errno, str_err = e.args[0]
        if errno == 113:
            result_dict[51] = " Error " + str_err
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

# cgi_opener("172.22.0.120","admin","public",table_list)

# print cgi_recon("172.22.0.123",'1.3.6.1.4.1.26149.2.2.9.1')
