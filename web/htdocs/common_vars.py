"""
common function and variables used often in UNMP,
those dosen't require any import from python base/external libraries
"""

#@TODO:
# device_type_dict = {'ap25': 'AP25', 'odu16': 'RM18', 'odu100': 'RM'}
# host_status_dic
# object_model_di
# errorStatus
# extract variables from common_controller and common_bll to this file

make_list = lambda x: [" - " if i is None or i == '' else str(i) for i in x]

device_type_dict = {'ap25': 'AP25',
                    'odu16': 'RM18',
                    'odu100': 'RM',
                    'idu4': 'IDU'}

device_name_dict = {'odu16': 'RM18',
                    'odu100': 'RM',
                    'idu4': 'IDU',
                    'ap25': 'Access Point',
                    'ccu': 'CCU'}

object_model_di = {
    'odu100': {
        '7.2.20': '7.2.20',
        '7.2.25': '7.2.25',
        '7.2.29': '7.2.29',
        '7.2.30': '7.2.29'
    },
    'odu16': {
        '7.2.10': '7.2.10',
    },
    'ap25': {
        '1.2.12': '1.2.12',
    },
    'idu4': {
        '2.0.5': '2.0.5',
    }
}

# SNMP error status code
errorStatus = {0: 'noError',
               1: 'Device Unresponsive',
               2: 'Parameter is out of range',
               3: 'Bad Value Parameter',
               4: 'Read Only Parameter',
               5: 'General Error. Device Unresponsive',
               6: 'Read Only Parameter',
               7: 'Wrong Type',
               8: 'Wrong Length',
               9: 'Wrong Encoding',
               10: 'Channel Ineffective',
               11: 'No Creation',
               12: 'Inconsistent Value',
               13: 'Resource Unavailable',
               14: 'Commit Failed',
               15: 'Undo Failed',
               16: 'Authorization Error',
               17: 'Not Writable',
               21: 'Invalid radio index',
               22: 'Invalid timeslot index',
               23: 'Invalid MAC address',
               24: 'RU admin state needs to be locked',
               '24': 'Device is not responding',
               25: 'Parameter can not be modified for sync source radio',
               26: 'Sync admin state needs to be locked',
               27: 'Raster time, timer adjust , percentDlTxTime can be specified only when sync source is internal.',
               28: 'RA admin state needs to be locked',
               29: 'Site survey inprogress, can"t do another operation.',
               30: 'Pass phrase not allowed if encryption is not enabled, UNLOCK failed',
               31: 'Blank passphrase is not allowed, UNLOCK failed.',
               32: 'Value specified for mcsindex is not valid for antenna port, UNLOCK failed.',
               33: 'Configured channel is unavailable in RAChannelList, UNLOCK failed',
               34: 'Can not support configured guaranteed bw for specified configuration, UNLOCK failed.',
               38: 'Radio Access admin state needs to be locked',
               39: 'Another O&M operation already in progress.',
               40: 'Two values should be non-zero and one value should be zero in bw calculator.',
               41: 'Error in IP configuration, check IP address, netmask and default gateway are correctly entered.',
               44: 'Numslaves one is not valid if guaranteed broadcast bandwidth is non zero or DBA enabled.',
               49: 'Invalid oid received',
               50: 'On master if aggregate of uplink guaranteedBW found greater than the node bandwidth',
               51: 'On master if aggregate of downlink guaranteedBW found greater than the node bandwidth',
               52: 'Max uplink bw is not in range within guaranteedUplinkBW to nodeBandwidth',
               53: 'Max downlinklink bw is not in range within guaranteedUplinkBW to nodeBandwidth',
               54: 'All timeslots for which MAC is not specified should have same set of values for all attributes',
               18: 'inconsistentName',
               50: 'On master if aggregate of uplink guaranteedBW found greater than the node bandwidth',
               551: 'Network is Unreachable',
               553: 'Request Timeout.Please Wait and Retry Again Later',
               55: 'Configuration Failed.Please try again later',
               91: 'Arguments are not proper',
               96: 'Configuration Failed.Please try again later',
               97: 'ip-port-community_not_passed',
               98: 'otherException',
               99: 'SNMP agent unknownn error',
               102: 'Unkown Error Occured',
               553: 'Device Unreachable'}

host_status_di = {0: 'No operation',
                  1: 'Firmware download',
                  2: 'Firmware upgrade',
                  3: 'Restore default config',
                  4: 'Flash commit',
                  5: 'Reboot',
                  6: 'Site survey',
                  7: 'Calculate BW',
                  8: 'Uptime service',
                  9: 'Statistics gathering',
                  10: 'Reconciliation',
                  11: 'Table reconciliation',
                  12: 'Set operation',
                  13: 'Live monitoring',
                  14: 'Status capturing',
                  #15: 'AP Scaning',
                  15: 'Refreshing Site Survey',
                  16: 'Refreshing RA Channel List'}
