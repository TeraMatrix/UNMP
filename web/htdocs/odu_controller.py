#!/usr/bin/python2.6

####################### import the packages ###################################
from datetime import datetime
import time
import traceback

from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *

from common_bll import EventLog, Essential, agent_start
from common_controller import *
from nms_config import *
from nms_snmp import *
from py_module import pysnmp_setAcl, pysnmp_geter, snmp_ping, pysnmp_acl_reconcile, pysnmp_get_table, pysnmp_set1
from pysnmp_ap import pysnmp_get, odubulk as bulktable
from pysnmp_ap import pysnmp_get_table as pysnmp_get_table_ap
from pysnmp_ap import pysnmp_seter as pysnmp_seter_ap
from pysnmp_module import pysnmp_set
from unmp_config import SystemConfig
from unmp_model import *
from utility import UNMPDeviceType



# from create_class_structure import  rename_tablename
###############################################################################

#-------------------------Author and file Information--------------------------

###############################################################################
"""
Odu Controller : This is used for making functions for getting result from database and set the data on device and get back the result
                 that the device is set or not set

Author : Anuj Samariya

(CodeScape Consultants Pvt. Ltd.)

"""

###############################################################################
##                                                                           ##
##                     Author- Anuj Samariya                                 ##
##                                                                           ##
##                         ODU Controller                                    ##
##                                                                           ##
##                 CodeScape Consultants Pvt. Ltd.                           ##
##                                                                           ##
##                     Dated:27 August 2011                                  ##
##                                                                           ##
###############################################################################

###############################################################################


# Creating Session#####################################
# session=session_db()
global sqlalche_obj


def check_connection():
    """


    @return:
    """
    global sqlalche_obj
    return sqlalche_obj.error

###############################################################################

# Defining Exception Classs and Exception function##################


class Set_exception(Exception):
    """
    Defining Exception Classs and Exception function
    """
    pass


def error_odu16(result, param, err1):
    """

    @param result:
    @param param:
    @param err1:
    @return:
    """
    err = ''
    for i in range(len(param)):
        val = result.find(param[i])
        if val == -1:
            err1[i] = 0
            err += param[i] + ' is not set.Please Retry Again'
        else:
            err1[i] = 1
            err += param[i] + ' is set'
    return err
# ########################################################################

essential_obj = Essential()
# Oid name declare with its numerical values##########
oid_name = {'RU.OMCConfTable.omcIPAddress': '.1.3.6.1.4.1.26149.2.2.7.1.2.1',
            'RU.OMCConfTable.periodicStatisticsTimer': '.1.3.6.1.4.1.26149.2.2.7.1.3.1',
            'RU.RUConfTable.channelBandwidth': '.1.3.6.1.4.1.26149.2.2.1.1.7.1',
            'RU.RUConfTable.synchSource': '.1.3.6.1.4.1.26149.2.2.1.1.8.1',
            'RU.RUConfTable.countryCode': '.1.3.6.1.4.1.26149.2.2.1.1.9.1',
            'RU.RUConfTable.adminState': '.1.3.6.1.4.1.26149.2.2.9.1.2.1',
            'RU.RUDateTimeTable.Year': '.1.3.6.1.4.1.26149.2.2.2.1.2.1',
            'RU.RUDateTimeTable.Month': '.1.3.6.1.4.1.26149.2.2.2.1.3.1',
            'RU.RUDateTimeTable.Day': '.1.3.6.1.4.1.26149.2.2.2.1.4.1',
            'RU.RUDateTimeTable.Hour': '1.3.6.1.4.1.26149.2.2.2.1.5.1',
            'RU.RUDateTimeTable.Minutes': '1.3.6.1.4.1.26149.2.2.2.1.6.1',
            'RU.RUDateTimeTable.Seconds': '1.3.6.1.4.1.26149.2.2.2.1.7.1',
            'RU.NetworkInterface.1.NetworkInterfaceConfigTable.ssId': '.1.3.6.1.4.1.26149.2.2.12.1.1.3.1',
            'RU.NetworkInterface.2.NetworkInterfaceConfigTable.ssId': '.1.3.6.1.4.1.26149.2.2.12.1.1.3.2',
            'ru.np.ra.1.tddmac.rfChannel': '.1.3.6.1.4.1.26149.2.2.13.7.1.1.1.1',
            'RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase': '.1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1',
            'ru.np.ra.1.tddmac.rfCoding': '.1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1',
            'ru.np.ra.1.tddmac.txPower': '.1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1',
            'RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors': '.1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1',
            'RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer': '.1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1',
            'RU.RA.1.LLC.RALLCConfTable.llcArqEnable': '.1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1',
            'RU.RA.1.LLC.RALLCConfTable.arqWin': '.1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1',
            'RU.RA.1.LLC.RALLCConfTable.frameLossThreshold': '.1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1',
            'RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer': '.1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1',
            'RU.RA.1.LLC.RALLCConfTable.frameLossTimeout': '.1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr': '.1.3.6.1.4.1.26149.2.2.8.1.2.1',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson': '.1.3.6.1.4.1.26149.2.2.8.1.3.1',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile': '.1.3.6.1.4.1.26149.2.2.8.1.4.1',
            'RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont': '.1.3.6.1.4.1.26149.2.2.8.1.5.1',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail': '.1.3.6.1.4.1.26149.2.2.8.1.6.1',
            'RU.SyncClock.SyncConfigTable.rasterTime': '.1.3.6.1.4.1.26149.2.2.11.1.1.4.1',
            'RU.SyncClock.SyncConfigTable.numSlaves': '.1.3.6.1.4.1.26149.2.2.11.1.1.5.1',
            'RU.SyncClock.SyncConfigTable.syncLossThreshold': '.1.3.6.1.4.1.26149.2.2.11.1.1.6.1',
            'RU.SyncClock.SyncConfigTable.leakyBucketTimer': '.1.3.6.1.4.1.26149.2.2.11.1.1.7.1',
            'RU.SyncClock.SyncConfigTable.syncLostTimeout': '.1.3.6.1.4.1.26149.2.2.11.1.1.8.1',
            'RU.SyncClock.SyncConfigTable.timerAdjust': '.1.3.6.1.4.1.26149.2.2.11.1.1.9.1',
            'RU.SyncClock.SyncConfigTable.broadcastEnable': '.1.3.6.1.4.1.26149.2.2.11.1.1.10.1',
            'RU.RA.1.RAConfTable.aclMode': '.1.3.6.1.4.1.26149.2.2.13.1.1.4.1',
            'RU.RA.1.RAConfTable.ssId': '.1.3.6.1.4.1.26149.2.2.13.1.1.5.1',
            'ru.np.ra.1.peer.1.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.1',
            'ru.np.ra.1.peer.2.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.2',
            'ru.np.ra.1.peer.3.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.3',
            'ru.np.ra.1.peer.4.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.4',
            'ru.np.ra.1.peer.5.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.5',
            'ru.np.ra.1.peer.6.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.6',
            'ru.np.ra.1.peer.7.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.7',
            'ru.np.ra.1.peer.8.config.macAddress': '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.8',
            'RU.RA.1.RAACLConfig.1.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.1',
            'RU.RA.1.RAACLConfig.2.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.2',
            'RU.RA.1.RAACLConfig.3.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.3',
            'RU.RA.1.RAACLConfig.4.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.4',
            'RU.RA.1.RAACLConfig.5.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.5',
            'RU.RA.1.RAACLConfig.6.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.6',
            'RU.RA.1.RAACLConfig.7.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.7',
            'RU.RA.1.RAACLConfig.8.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.8',
            'RU.RA.1.RAACLConfig.9.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.9',
            'RU.RA.1.RAACLConfig.10.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.10',
            'RU.RA.1.RAACLConfig.#.macAddress': '.1.3.6.1.4.1.26149.2.2.13.5.1.2.1.#',
            'RU.RUOMOperationsTable.omOperationsReq': '.1.3.6.1.4.1.26149.2.2.5.1.2.1'
}
###############################################################################

# Oid Name declare with its type####################

oid_type = {'RU.OMCConfTable.omcIPAddress': 'a',
            'RU.OMCConfTable.periodicStatisticsTimer': 'u',
            'RU.RUConfTable.channelBandwidth': 'i',
            'RU.RUConfTable.synchSource': 'i',
            'RU.RUConfTable.countryCode': 'u',
            'RU.RUConfTable.adminState': 'i',
            'RU.RUDateTimeTable.Year': 'i',
            'RU.RUDateTimeTable.Month': 'i',
            'RU.RUDateTimeTable.Day': 'i',
            'RU.RUDateTimeTable.Hour': 'i',
            'RU.RUDateTimeTable.Minutes': 'i',
            'RU.RUDateTimeTable.Seconds': 'i',
            'RU.NetworkInterface.1.NetworkInterfaceConfigTable.ssId': 's',
            'RU.NetworkInterface.2.NetworkInterfaceConfigTable.ssId': 's',
            'ru.np.ra.1.tddmac.rfChannel': 'i',
            'RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase': 's',
            'ru.np.ra.1.tddmac.rfCoding': 'i',
            'ru.np.ra.1.tddmac.txPower': 'u',
            'RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors': 'u',
            'RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer': 'u',
            'RU.RA.1.LLC.RALLCConfTable.llcArqEnable': 'i',
            'RU.RA.1.LLC.RALLCConfTable.arqWin': 'u',
            'RU.RA.1.LLC.RALLCConfTable.frameLossThreshold': 'u',
            'RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer': 'u',
            'RU.RA.1.LLC.RALLCConfTable.frameLossTimeout': 'i',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr': 's',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson': 's',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile': 's',
            'RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont': 's',
            'RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail': 's',
            'RU.SyncClock.SyncConfigTable.rasterTime': 'i',
            'RU.SyncClock.SyncConfigTable.numSlaves': 'i',
            'RU.SyncClock.SyncConfigTable.syncLossThreshold': 'u',
            'RU.SyncClock.SyncConfigTable.leakyBucketTimer': 'u',
            'RU.SyncClock.SyncConfigTable.syncLostTimeout': 'u',
            'RU.SyncClock.SyncConfigTable.timerAdjust': 'i',
            'RU.SyncClock.SyncConfigTable.broadcastEnable': 'i',
            'RU.RA.1.RAConfTable.aclMode': 'i',
            'RU.RA.1.RAConfTable.ssId': 's',
            'ru.np.ra.1.peer.1.config.macAddress': 's',
            'ru.np.ra.1.peer.2.config.macAddress': 's',
            'ru.np.ra.1.peer.3.config.macAddress': 's',
            'ru.np.ra.1.peer.4.config.macAddress': 's',
            'ru.np.ra.1.peer.5.config.macAddress': 's',
            'ru.np.ra.1.peer.6.config.macAddress': 's',
            'ru.np.ra.1.peer.7.config.macAddress': 's',
            'ru.np.ra.1.peer.8.config.macAddress': 's',
            'RU.RA.1.RAACLConfig.1.macAddress': 's',
            'RU.RA.1.RAACLConfig.2.macAddress': 's',
            'RU.RA.1.RAACLConfig.3.macAddress': 's',
            'RU.RA.1.RAACLConfig.4.macAddress': 's',
            'RU.RA.1.RAACLConfig.5.macAddress': 's',
            'RU.RA.1.RAACLConfig.6.macAddress': 's',
            'RU.RA.1.RAACLConfig.7.macAddress': 's',
            'RU.RA.1.RAACLConfig.8.macAddress': 's',
            'RU.RA.1.RAACLConfig.9.macAddress': 's',
            'RU.RA.1.RAACLConfig.10.macAddress': 's',
            'RU.RA.1.RAACLConfig.#.macAddress': '#'
}

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
               11: 'Channel Ineffective',
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
               553: 'Request Timeout.Please Wait and Retry Again',
               55: 'Configuration Failed.Please try again later',
               91: 'Arguments are not proper',
               96: 'Configuration Failed.Please try again later',
               97: 'ip-port-community_not_passed',
               98: 'otherException',
               99: 'SNMP agent unknownn error',
               102: 'Unkown Error Occured'}

preferred_channel_dic = {}
###############################################################################
host_status_dic = {
    0: 'No operation', 1: 'Firmware download', 2: 'Firmware upgrade', 3: 'Restore default config', 4: 'Flash commit',
                   5: 'Reboot', 6: 'Site survey', 7: 'Calculate BW', 8: 'Uptime service', 9: 'Statistics gathering', 10: 'Reconciliation', 11: 'Table reconciliation', 12: 'Set operation', 13: 'Live monitoring', 14: 'Status capturing', 15: 'Refreshing Site Survey', 16: 'Refreshing RA Channel List'}

time_diff = 0
# Author - Anuj Samariya
# This function is used to get the data of device list
# host_id -this id is used to get the specific device parameters e.g
# ipaddress,macaddressmdevcietypeid,configprofileid


def get_device_param(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of device list
    host_id -this id is used to get the specific device parameters e.g ipaddress,macaddressmdevcietypeid,configprofileid
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    device_list_param = []
    device_list_param = sqlalche_obj.session.query(
        Hosts.ip_address, Hosts.mac_address, Hosts.device_type_id, Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    if device_list_param == None:
        device_list_param = []
    sqlalche_obj.sql_alchemy_db_connection_close()
    return device_list_param

# Author - Anuj Samariya
# This function is used to get the data of omc configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the omc configuration table data and config profile id


def omc_conf_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    # session=session_db()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    odu16_omc_conf_table = sqlalche_obj.session.query(SetOdu16OmcConfTable).filter(
        SetOdu16OmcConfTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return odu16_omc_conf_table, odu16_profile_id

# Author - Anuj Samariya
# omc_fields - these are the collection of form fields which are going to set on the device and store in the database
# omc_config - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def omc_conf_set(host_id, omc_fields, omc_config, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    omc_fields - these are the collection of form fields which are going to set on the device and store in the database
    omc_config- these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param omc_fields:
    @param omc_config:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    err1 = [0, 0]
    result = ""
    param = []
    resultarray = {}
    param.append('omcIpAddress.1')
    param.append('periodicStatsTimer.1')
    form_name = ['OMC IP address', 'Periodic Statistics Timer']
    dictarr = []
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    odu16_omc_conf_table = sqlalche_obj.session.query(SetOdu16OmcConfTable).filter(
        SetOdu16OmcConfTable.config_profile_id == device_param_list[0][4]).all()
    result += str(odu16_omc_conf_table)
    for i in range(len(omc_fields)):
        omc_oid = oid_name[omc_fields[i]]
        omc_type = oid_type[omc_fields[i]]
        omc_type_val = omc_config[i]
        result += snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                           0][3], omc_oid, omc_type, omc_type_val)
    err = error_odu16(result, param, err1)
    try:
        el = EventLog()
        # el.log_event( "description detail" , "user_name" )
        if 1 in err1:
            el.log_event(
                "Values Updated in UBR UNMP Form", "%s" % (user_name))
        if int(err1[0]) == 1:
            odu16_omc_conf_table[0].omc_ip_address = omc_config[0]
        if int(err1[1]) == 1:
            odu16_omc_conf_table[0].periodic_stats_timer = omc_config[1]
        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        for j in range(0, len(omc_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = omc_config[j]
            dict["textbox"] = omc_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
        if err != '':
            raise Set_exception
    except Set_exception, e:
        resultarray["result"] = dictarr
        resultarray["tableName"] = 'SetOdu16OmcConfTable'
        resultarray['formAction'] = 'omc_config_form.py'
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)
##    finally:
##        err1=[]
##        sqlalche_obj.sql_alchemy_db_connection_close()


# Author - Anuj Samariya
# This function is used to get the data of omc configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ru configuration table data and config profile id
def ru_config_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of ru configuration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the ru configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    ru_config_get = sqlalche_obj.session.query(SetOdu16RUConfTable.channel_bandwidth, SetOdu16RUConfTable.sysnch_source, SetOdu16RUConfTable.country_code).filter(
        SetOdu16RUConfTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return ru_config_get, odu16_profile_id


# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# ru_config_fields - these are the collection of form fields which are going to set on the device and store in the database
# ru_config_param - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set
def ru_config_table_set(host_id, ru_config_fields, ru_config_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    ru_config_fields - these are the collection of form fields which are going to set on the device and store in the database
    ru_config_param - these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not
    @param host_id:
    @param ru_config_fields:
    @param ru_config_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    result = ''
    param = []
    err1 = [0, 0]
    resultarray = {}
    set_value = ''
    form_name = ['Channel Bandwidth:', 'Country Code']
    dictarr = []
    param.append('channelBandwidth.1')
    param.append('countryCode.1')
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    ru_config_set = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(
        SetOdu16RUConfTable.config_profile_id == device_param_list[0][4]).first()
    admin_state = snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
                           device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '0')
    var = admin_state.find('adminstate.1')

    if var != -1:
        ru_config_set.adminstate = 0
        result += snmp_setmultiple(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[0][3], oid_name[ru_config_fields[0]], oid_type[ru_config_fields[0]], ru_config_param[
                                   0], oid_name[ru_config_fields[1]], oid_type[ru_config_fields[1]], ru_config_param[1])
        err = error_odu16(result, param, err1)
        try:
            el = EventLog()
            if 1 in err1:
                el.log_event(
                    "Values Updated in UBR Radio Unit Form", "%s" % (user_name))
            for j in range(0, len(ru_config_fields)):
                if ru_config_param[j] == 0 or ru_config_param[j] == '0':
                    set_value = '5Mhz'
                elif ru_config_param[j] == 1 or ru_config_param[j] == '1':
                    set_value = '10Mhz'
                elif ru_config_param[j] == 2 or ru_config_param[j] == '2':
                    set_value = '20Mhz'
                elif ru_config_param[j] == 356 or ru_config_param[j] == '356':
                    set_value = 'India'
                elif ru_config_param[j] == 208 or ru_config_param[j] == '208':
                    set_value = 'Denmark'
                elif ru_config_param[j] == 752 or ru_config_param[j] == '752':
                    set_value = 'Sweden'
                dict = {}
                dict["name"] = form_name[j]
                dict["value"] = set_value
                dict["textbox"] = ru_config_fields[j]
                dict["status"] = err1[j]
                dictarr.append(dict)
            if err1[0] == 1:
                ru_config_set.channel_bandwidth = ru_config_param[0]
            if err1[1] == 1:
                ru_config_set.country_code = ru_config_param[1]
            admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                                   0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '1')
            var = admin_state.find('adminstate.1')
            if var != -1:
                ru_config_set.adminstate = 1
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            if err != '':
                raise Set_exception
        except Set_exception as e:
            sqlalche_obj.session.commit()
            result = 'Parameters are not set.Please Retry again'
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16RUConfTable'
            resultarray['formAction'] = 'RU_Cancel_Configuration.py'
            resultarray['adminState'] = '.1.3.6.1.4.1.26149.2.2.1.1.2.1'
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(resultarray)
    else:
        for j in range(0, len(ru_config_fields)):
            for j in range(0, len(ru_config_fields)):
                if ru_config_param[j] == 0 or ru_config_param[j] == '0':
                    set_value = '5Mhz'
                elif ru_config_param[j] == 1 or ru_config_param[j] == '1':
                    set_value = '10Mhz'
                elif ru_config_param[j] == 2 or ru_config_param[j] == '2':
                    set_value = '20Mhz'
                elif ru_config_param[j] == 356 or ru_config_param[j] == '356':
                    set_value = 'India'
                elif ru_config_param[j] == 208 or ru_config_param[j] == '208':
                    set_value = 'Denmark'
                elif ru_config_param[j] == 752 or ru_config_param[j] == '752':
                    set_value = 'Sweden'
                dict = {}
                dict["name"] = form_name[j]
                dict["value"] = set_value
                dict["textbox"] = ru_config_fields[j]
                dict["status"] = err1[j]
                dictarr.append(dict)
            resultarray["result"] = dictarr
            resultarray["tablename"] = 'SetOdu16RUConfTable'
            resultarray['formAction'] = 'RU_Cancel_Configuration.py'
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(resultarray)

# Author - Anuj Samariya
# This function is used to get the data of ru date time configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ru date time configuration table data and config profile id


def ru_date_time_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of ru date time configuration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the ru date time configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    ru_date_time = sqlalche_obj.session.query(
        SetOdu16RUDateTimeTable.year, SetOdu16RUDateTimeTable.month, SetOdu16RUDateTimeTable.day, SetOdu16RUDateTimeTable.hour, SetOdu16RUDateTimeTable.min,
                                              SetOdu16RUDateTimeTable.sec).filter(SetOdu16RUDateTimeTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return ru_date_time, odu16_profile_id

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# date_time_fields - these are the collection of form fields which are going to set on the device and store in the database
# date_time_param - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def ru_date_time_table_set(host_id, date_time_fields, date_time_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    date_time_fields - these are the collection of form fields which are going to set on the device and store in the database
    date_time_param - these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param date_time_fields:
    @param date_time_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    result = ""
    param = []
    form_name = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']
    dictarr = []
    resultarray = {}
    err1 = [0, 0, 0, 0, 0, 0]
    param.append('year.1')
    param.append('month.1')
    param.append('day.1')
    param.append('hour.1')
    param.append('min.1')
    param.append('sec.1')
    odu16_date_time_table = []
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    odu16_date_time_table = sqlalche_obj.session.query(SetOdu16RUDateTimeTable).filter(
        SetOdu16RUDateTimeTable.config_profile_id == device_param_list[0][4]).all()
    for i in range(len(date_time_fields)):
        oidname = oid_name[date_time_fields[i]]
        oidtype = oid_type[date_time_fields[i]]
        oidvalue = date_time_param[i]
        result += snmp_set(
            device_param_list[0][0], device_param_list[0][
                1], device_param_list[0][2],
                           device_param_list[0][3], oidname, oidtype, oidvalue)
    err = error_odu16(result, param, err1)
    try:
        el = EventLog()
        if 1 in err1:
            el.log_event(
                "Values Updated in UBR RU Date Time Form", "%s" % (user_name))
        for j in range(0, len(date_time_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = date_time_param[j]
            dict["textbox"] = date_time_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
        if err1[0] == 1:
            odu16_date_time_table[0].year = date_time_param[0]
        if err1[1] == 1:
            odu16_date_time_table[0].month = date_time_param[1]
        if err1[2] == 1:
            odu16_date_time_table[0].day = date_time_param[2]
        if err1[3] == 1:
            odu16_date_time_table[0].hour = date_time_param[3]
        if err1[4] == 1:
            odu16_date_time_table[0].min = date_time_param[4]
        if err1[5] == 1:
            odu16_date_time_table[0].sec = date_time_param[5]
        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if err != '':
            raise Set_exception
    except Set_exception as e:
        resultarray["result"] = dictarr
        resultarray["tableName"] = 'SetOdu16RUDateTimeTable'
        resultarray["formAction"] = 'RU_Date_Time.py'
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)


def network_interface_config_get():
    """


    @return:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    network_interface_config = sqlalche_obj.session.query(
        SetOdu16NetworkInterfaceConfig.ssid, SetOdu16NetworkInterfaceConfig.index).filter(SetOdu16NetworkInterfaceConfig.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return network_interface_config, odu16_profile_id


def network_interface_config_set(host_id, network_interface_config_fields, network_interface_config_param, user_name):
    """

    @param host_id:
    @param network_interface_config_fields:
    @param network_interface_config_param:
    @param user_name:
    @return: @raise:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    network_interface_config_table = []
    result = ''
    param = []
    param.append('ssId.1')
    param.append('ssId.2')
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    network_interface_config_table = sqlalche_obj.session.query(SetOdu16NetworkInterfaceConfig).filter(
        SetOdu16NetworkInterfaceConfig.config_profile_id == device_param_list[0][4]).all()
    for i in range(len(network_interface_config_fields)):
        oidname = oid_name[network_interface_config_fields[i]]
        oidtype = oid_type[network_interface_config_fields[i]]
        if network_interface_config_param[i] == "":
            oidvalue = ''
        else:
            oidvalue = network_interface_config_param[i]
        result += snmp_set(
            device_param_list[0][0], device_param_list[0][
                1], device_param_list[0][2],
                           device_param_list[0][3], oidname, oidtype, oidvalue)
    err = error_odu16(result, param)
    try:
        el = EventLog()
        if 1 in err1:
            el.log_event("Values Updated in UBR Netwrok Interface Form",
                         "%s" % (user_name))
        if err != '':
            raise Set_exception
        else:
            for i in range(len(network_interface_config_param)):
                network_interface_config_table[
                    i].ssid = network_interface_config_param[i]
                network_interface_config_table[i].index = i + 1
        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result
    except Set_exception as e:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return err
# Author - Anuj Samariya
# This function is used to get the data of ru date time configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ru date time configuration table data and config profile id


def ra_acl_config_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of ra acl configuration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the ra acl configuration table configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    ra_conf_table = sqlalche_obj.session.query(SetOdu16RAConfTable.acl_mode).filter(
        SetOdu16RAConfTable.config_profile_id == odu16_profile_id[0][0]).all()
    ra_acl_config = sqlalche_obj.session.query(SetOdu16RAAclConfigTable.mac_address, SetOdu16RAAclConfigTable.index).filter(
        SetOdu16RAAclConfigTable.config_profile_id == odu16_profile_id[0][0]).order_by(SetOdu16RAAclConfigTable.index).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return ra_acl_config, odu16_profile_id, ra_conf_table

# Author - Anuj Samariya
# This function is used to get the data of ra acl configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ra acl configuration table data and config profile id


def sync_config_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of syn configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the syn configuration table configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    sync_config_table = sqlalche_obj.session.query(
        SetOdu16SyncConfigTable.raster_time, SetOdu16SyncConfigTable.num_slaves, SetOdu16SyncConfigTable.sync_loss_threshold, SetOdu16SyncConfigTable.leaky_bucket_timer, SetOdu16SyncConfigTable.sync_lost_timeout, SetOdu16SyncConfigTable.sync_config_time_adjust,
                                                   SetOdu16SyncConfigTable.sync_config_broadcast_enable).filter(SetOdu16SyncConfigTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return sync_config_table, odu16_profile_id

# Author - Anuj Samariya
# This function is used to get the data of ra llc configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ra llc configuration table data and config profile id


def ra_llc_conf_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of ra llc configuration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the ra llc configuration table configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    ra_llc_conf_table = sqlalche_obj.session.query(
        SetOdu16RALlcConfTable.llc_arq_enable, SetOdu16RALlcConfTable.arq_win, SetOdu16RALlcConfTable.frame_loss_threshold, SetOdu16RALlcConfTable.leaky_bucket_timer_val,
                                                   SetOdu16RALlcConfTable.frame_loss_timeout).filter(SetOdu16RALlcConfTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return ra_llc_conf_table, odu16_profile_id


# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# llc_configuration_fields - these are the collection of form fields which are going to set on the device and store in the database
# llc_configuration_param - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set
def ra_llc_configuration_set(host_id, llc_configuration_fields, llc_configuration_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    date_time_fields - these are the collection of form fields which are going to set on the device and store in the database
    date_time_param - these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param llc_configuration_fields:
    @param llc_configuration_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    result = ''
    err1 = [0, 0, 0, 0, 0]
    form_name = ['ARQ Mode', 'ArqWin(Retransmit Window Size)', 'Frame Loss Threshold',
                                     'Leaky Bucket Timer', 'Frame Loss Time Out']
    param = []
    dictarr = []
    resultarray = {}
    param.append('llcArqEnable.1')
    param.append('arqWin.1')
    param.append('frameLossThreshold.1')
    param.append('leakyBucketTimerVal.1')
    param.append('frameLossTimeout.1')
    ra_llc_config = []
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    ra_llc_config = sqlalche_obj.session.query(SetOdu16RALlcConfTable).filter(
        SetOdu16RALlcConfTable.config_profile_id == device_param_list[0][4]).first()
    for i in range(len(llc_configuration_fields)):
        oidname = oid_name[llc_configuration_fields[i]]
        oidtype = oid_type[llc_configuration_fields[i]]
        oidvalue = llc_configuration_param[i]
        result += snmp_set(
            device_param_list[0][0], device_param_list[0][
                1], device_param_list[0][2],
                           device_param_list[0][3], oidname, oidtype, oidvalue)
    err = error_odu16(result, param, err1)
    val = ''
    try:
        el = EventLog()
        if 1 in err1:
            el.log_event("Values Updated in UBR LLC Form", "%s" % (user_name))
        for j in range(0, len(llc_configuration_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = llc_configuration_param[j]
            dict["textbox"] = llc_configuration_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
        if err1[0] == 1:
            ra_llc_config.llc_arq_enable = llc_configuration_param[0]
        if err1[1] == 1:
            ra_llc_config.arq_win = llc_configuration_param[1]
        if err1[2] == 1:
            ra_llc_config.frame_loss_threshold = llc_configuration_param[2]
        if err1[3] == 1:
            ra_llc_config.leaky_bucket_timer_val = llc_configuration_param[3]
        if err1[4] == 1:
            ra_llc_config.frame_loss_timeout = llc_configuration_param[4]
        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if err != '':
            raise Set_exception
    except Set_exception as e:
        resultarray["result"] = dictarr
        resultarray["tableName"] = 'SetOdu16RALlcConfTable'
        resultarray['formAction'] = 'Llc_Cancel_Configuration.py'
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)

# Author - Anuj Samariya
# This function is used to get the data of ra tdd mac configuration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ra tdd mac configuration table data and config profile id


def ra_tdd_mac_config_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of ra tdd mac configuration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the ra tdd mac configuration table configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    ra_tdd_mac_conf_table = sqlalche_obj.session.query(
        SetOdu16RATddMacConfig.rf_channel_frequency, SetOdu16RATddMacConfig.pass_phrase,
                                                       SetOdu16RATddMacConfig.rfcoding, SetOdu16RATddMacConfig.tx_power, SetOdu16RATddMacConfig.max_crc_errors,
                                                       SetOdu16RATddMacConfig.leaky_bucket_timer_value).\
        filter(SetOdu16RATddMacConfig.config_profile_id == odu16_profile_id[
               0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return ra_tdd_mac_conf_table, odu16_profile_id


# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# tdd_mac_fields - these are the collection of form fields which are going to set on the device and store in the database
# tdd_mac_param - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set
def ra_tdd_mac_config_set(host_id, tdd_mac_fields, tdd_mac_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    tdd_mac_fields - these are the collection of form fields which are going to set on the device and store in the database
    tdd_mac_param - these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param tdd_mac_fields:
    @param tdd_mac_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    ra_tdd_mac_configtable = []
    result = ''
    param = []
    dictarr = []
    resultarray = {}
    form_name = ['TDD1 MAC RF Frequency', 'Pass Phrase', 'TDD 1 MAC RF Coding',
        'TDD 1 MAC TX Power', 'Max Crc Errors', 'Leaky Bucket Timer']
    err1 = [0, 0, 0, 0, 0, 0]
    param.append('rfChannelFrequency.1')
    param.append('passPhrase.1')
    param.append('txPower.1')
    param.append('maxCrcErrors.1')
    param.append('leakyBucketTimerValue.1')
    param.append('rfcoding.1')
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    ra_tdd_mac_configtable = sqlalche_obj.session.query(SetOdu16RATddMacConfig).filter(
        SetOdu16RATddMacConfig.config_profile_id == device_param_list[0][4]).first()
    ra_config = sqlalche_obj.session.query(SetOdu16RAConfTable).filter(
        SetOdu16RAConfTable.config_profile_id == device_param_list[0][4]).first()
    admin_state = snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
                           device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '0')
    var = admin_state.find('raAdminState.1')
    if var != -1:
        ra_config.ra_admin_state = 0
        for i in range(len(tdd_mac_fields)):
            oidname = oid_name[tdd_mac_fields[i]]
            oidtype = oid_type[tdd_mac_fields[i]]
            oidvalue = tdd_mac_param[i]
            result += snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2],
                               device_param_list[0][3], oidname, oidtype, oidvalue)
        err = error_odu16(result, param, err1)
        try:
            el = EventLog()
            if 1 in err1:
                el.log_event(
                    "Values Updated in UBR Radio Frequency Form", "%s" % (user_name))
            for j in range(0, len(tdd_mac_fields)):
                dict = {}
                dict["name"] = form_name[j]
                dict["value"] = tdd_mac_param[j]
                dict["textbox"] = tdd_mac_fields[j]
                dict["status"] = err1[j]
                dictarr.append(dict)
            if err1[0] == 1:
                ra_tdd_mac_configtable.rf_channel_frequency = tdd_mac_param[0]
            if err1[1] == 1:
                ra_tdd_mac_configtable.pass_phrase = tdd_mac_param[1]
            if err1[2] == 1:
                ra_tdd_mac_configtable.rfcoding = tdd_mac_param[2]
            if err1[3] == 1:
                ra_tdd_mac_configtable.tx_power = tdd_mac_param[3]
            if err1[4] == 1:
                ra_tdd_mac_configtable.max_crc_errors = tdd_mac_param[4]
            if err1[5] == 1:
                ra_tdd_mac_configtable.leaky_bucket_timer_value = tdd_mac_param[
                    5]
            sqlalche_obj.session.commit()
            if err != '':
                admin_state = snmp_set(
                    device_param_list[0][
                        0], device_param_list[0][1], device_param_list[0][2],
                                       device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '1')
                var = admin_state.find('raAdminState.1')
                if var != -1:
                    ra_config.ra_admin_state = 1
                sqlalche_obj.session.commit()
                raise Set_exception
        except Set_exception as e:
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16RATddMacConfig'
            resultarray['formAction'] = 'Tdd_Mac_Cancel_Configuration.py'
            return str(resultarray)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
    else:
        for j in range(0, len(tdd_mac_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = tdd_mac_param[j]
            dict["textbox"] = tdd_mac_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16RATddMacConfig'
            resultarray['formAction'] = 'Tdd_Mac_Cancel_Configuration.py'
            sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)


# Author - Anuj Samariya
# This function is used to get the data of peer config table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the peer config table data and config profile id
def peer_config_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of peer config table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the peer config table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    peer_config_table = sqlalche_obj.session.query(SetOdu16PeerConfigTable.peer_mac_address , SetOdu16PeerConfigTable.index).\
        filter(
            SetOdu16PeerConfigTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return peer_config_table, odu16_profile_id

# Author - Anuj Samariya
# This function is used to get the data of ra conf table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the ra conf table data and config profile id


def ra_conf_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of ra conf table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the ra conf table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    ra_conf_table = sqlalche_obj.session.query(SetOdu16RAConfTable.acl_mode).\
        filter(
            SetOdu16RAConfTable.config_profile_id == odu16_profile_id[0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return ra_conf_table, odu16_profile_id

# Author - Anuj Samariya
# This function is used to get the data of sys omc registration table
# host_id -this id is used to get the specific config profile id i.e. config_profile_id
# return the sys omc registration table data and config profile id


def sys_omc_registration_table_get(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of sys omc registration table
    host_id -this id is used to get the specific config profile id i.e. config_profile_id
    return the sys omc registration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    odu16_profile_id = sqlalche_obj.session.query(
        Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    sys_omc_registration_table = sqlalche_obj.session.query(SetOdu16SysOmcRegistrationTable).\
        filter(SetOdu16SysOmcRegistrationTable.config_profile_id == odu16_profile_id[
               0][0]).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    return sys_omc_registration_table, odu16_profile_id

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# omc_registration_fields - these are the collection of form fields which are going to set on the device and store in the database
# omc_registration_param - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def omc_registration_configuration_set(host_id, omc_registration_fields, omc_registration_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    omc_registration_fields - these are the collection of form fields which are going to set on the device and store in the database
    omc_registration_param - these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param omc_registration_fields:
    @param omc_registration_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    omc_registration_configuration = []
    result = ''
    param = []
    dictarr = []
    err1 = [0, 0, 0, 0, 0]
    resultarray = {}
    form_name = ['Address', 'Contact Person', 'Mobile',
        'AlternateContact', 'Email']
    param.append('sysOmcRegisterContactAddr.1')
    param.append('sysOmcRegisterContactPerson.1')
    param.append('sysOmcRegisterContactMobile.1')
    param.append('sysOmcRegisterAlternateContact.1')
    param.append('sysOmcRegisterContactEmail.1')
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    omc_registration_configuration = sqlalche_obj.session.query(SetOdu16SysOmcRegistrationTable).filter(
        SetOdu16SysOmcRegistrationTable.config_profile_id == device_param_list[0][4]).first()
    for i in range(len(omc_registration_fields)):
        oidname = oid_name[omc_registration_fields[i]]
        oidtype = oid_type[omc_registration_fields[i]]
        oidvalue = omc_registration_param[i]
        result += snmp_set(
            device_param_list[0][0], device_param_list[0][
                1], device_param_list[0][2],
                           device_param_list[0][3], oidname, oidtype, oidvalue)
    err = error_odu16(result, param, err1)
    try:
        el = EventLog()
        if 1 in err1:
            el.log_event(
                "Values Updated in UBR OMC Registration Form", "%s" % (user_name))
        for j in range(0, len(omc_registration_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = omc_registration_param[j]
            dict["textbox"] = omc_registration_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
        if err1[0] == 1:
            omc_registration_configuration.sys_omc_register_contact_addr = omc_registration_param[
                0]
        if err1[1] == 1:
            omc_registration_configuration.sys_omc_register_contact_person = omc_registration_param[1]
        if err1[2] == 1:
            omc_registration_configuration.sys_omc_register_contact_mobile = omc_registration_param[2]
        if err1[3] == 1:
            omc_registration_configuration.sys_omc_register_alternate_contact = omc_registration_param[3]
        if err1[4] == 1:
            omc_registration_configuration.sys_omc_register_contact_email = omc_registration_param[
                4]
        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if err != '':
            raise Set_exception
    except Set_exception as e:
        resultarray["result"] = dictarr
        resultarray["tableName"] = 'SetOdu16SysOmcRegistrationTable'
        resultarray['formAction'] = 'sys_registration_form.py'
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# syn_configuration_fields - these are the collection of form fields which are going to set on the device and store in the database
# syn_configuration_param - these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def syn_configuration_set(host_id, syn_configuration_fields, syn_configuration_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    syn_configuration_fields - these are the collection of form fields which are going to set on the device and store in the database
    syn_configuration_param - these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param syn_configuration_fields:
    @param syn_configuration_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    syn_configuration = []
    result = ''
    param = []
    dictarr = []
    resultarray = {}
    form_name = ['Raster Time', 'Number of Slaves', 'SyncLossThreshold',
        'Leaky Bucket Timer', 'Sync Loss Time Out', 'Sync Timer Adjust']
    err1 = [0, 0, 0, 0, 0, 0]
    param.append('rasterTime.1')
    param.append('numSlaves.1')
    param.append('syncLossThreshold.1')
    param.append('leakyBucketTimer.1')
    param.append('syncLostTimeout.1')
    param.append('syncConfigTimerAdjust.1')
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    syn_configuration = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
        SetOdu16SyncConfigTable.config_profile_id == device_param_list[0][4]).first()
    admin_state = snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
                           device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '0')
    var = admin_state.find('adminStatus.1')
    if var != -1:
        syn_configuration.admin_status = 0
        for i in range(len(syn_configuration_fields)):
            oidname = oid_name[syn_configuration_fields[i]]
            oidtype = oid_type[syn_configuration_fields[i]]
            oidvalue = syn_configuration_param[i]
            result += snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2],
                               device_param_list[0][3], oidname, oidtype, oidvalue)
        err = error_odu16(result, param, err1)
        try:
            el = EventLog()
            if 1 in err1:
                el.log_event(
                    "Values Updated in UBR Synchronization Registration Form",
                             "%s" % (user_name))
            for j in range(0, len(syn_configuration_fields)):
                dict = {}
                dict["name"] = form_name[j]
                dict["value"] = syn_configuration_param[j]
                dict["textbox"] = syn_configuration_fields[j]
                dict["status"] = err1[j]
                dictarr.append(dict)
            if err1[0] == 1:
                syn_configuration.raster_time = syn_configuration_param[0]
            if err1[1] == 1:
                syn_configuration.num_slaves = syn_configuration_param[1]
            if err1[2] == 1:
                syn_configuration.sync_loss_threshold = syn_configuration_param[
                    2]
            if err1[3] == 1:
                syn_configuration.leaky_bucket_timer = syn_configuration_param[
                    3]
            if err1[4] == 1:
                syn_configuration.sync_lost_timeout = syn_configuration_param[
                    4]
            if err1[5] == 1:
                syn_configuration.sync_config_time_adjust = syn_configuration_param[
                    5]

            admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[0][
                                   3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '1')
            var = admin_state.find('adminStatus.1')
            if var != -1:
                syn_configuration.admin_status = 1
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            if err != '':
                raise Set_exception
        except Set_exception as e:
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16SyncConfigTable'
            resultarray[
                'formAction'] = 'Syn_Cancel_Omc_Registration_Configuration.py'
            resultarray['adminState'] = '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1'
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(resultarray)
    else:
        for j in range(0, len(syn_configuration_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = syn_configuration_param[j]
            dict["textbox"] = syn_configuration_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16SyncConfigTable'
            resultarray[
                'formAction'] = 'Syn_Cancel_Omc_Registration_Configuration.py'
            resultarray['adminState'] = '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1'
            sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# ra_config_fields - these are the collection of form fields which are going to set on the device and store in the database
# ra-config_param- these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def ra_config_set(host_id, ra_config_fields, ra_config_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    ra_config_fields - these are the collection of form fields which are going to set on the device and store in the database
    ra_config_param- these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param ra_config_fields:
    @param ra_config_param:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    ra_config = []
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    ra_config = sqlalche_obj.session.query(SetOdu16RAConfTable).filter(
        SetOdu16RAConfTable.config_profile_id == device_param_list[0][4]).first()
    snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '0')
    for i in range(len(ra_config_fields)):
        oidname = oid_name[ra_config_fields[i]]
        oidtype = oid_type[ra_config_param[i]]
        oidvalue = ra_config_param[i]
        result = snmp_set(device_param_list[0][0], device_param_list[0][1],
                          device_param_list[0][2], device_param_list[0][3], oidname, oidtype, oidvalue)
    ra_config.acl_mode = ra_config_param[0]
    ra_config.ssid = ra_config_param[1]
    sqlalche_obj.session.add(ra_config)
    sqlalche_obj.session.commit()
    snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '1')
    sqlalche_obj.sql_alchemy_db_connection_close()
    return result

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# peer_config_fields - these are the collection of form fields which are going to set on the device and store in the database
# peer_config_param- these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def peer_config_set(host_id, status, peer_config_fields, peer_config_param, time_slot_param, user_name):
    """






    @param host_id:
    @param status:
    @param peer_config_fields:
    @param peer_config_param:
    @param time_slot_param:
    @param user_name:
    @author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    peer_config_fields - these are the collection of form fields which are going to set on the device and store in the database
    peer_config_param- these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    if status == 1:
        result = 'Timeslot is smaller than the number of slaves you want to fill'
        return result
    else:
        peer_config_table = []
        result = ''
        dupli = []
        param = []
        err1 = []
        var = ''
        val = ''
        count = ''
        form_name = []
        dictarr = []
        resultarray = {}
        for i in range(0, len(peer_config_fields)):
            count = i + 1
            err1.append(0)
            param.append('peerMacAddress.1.%s' % (count))
            form_name.append('Timeslot %s Mac Address' % (count))

        for i in range(0, len(peer_config_param)):
            j = peer_config_param.count(peer_config_param[i])
            if j > 1:
                dupli.append(i)
        device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
            filter(Hosts.host_id == host_id).all()
        syn_configuration = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
            SetOdu16SyncConfigTable.config_profile_id == device_param_list[0][4]).all()
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '0')
        var = admin_state.find('adminStatus.1')
        if int(var) != -1:
            numslaves = snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2], device_param_list[0][3],
                                 '.1.3.6.1.4.1.26149.2.2.11.1.1.5.1', 'i', time_slot_param)
            val = numslaves.find('numSlaves.1')
            if int(val) != -1:
                syn_configuration[0].num_slaves = time_slot_param
                sqlalche_obj.session.commit()
                peer_config_table = sqlalche_obj.session.query(SetOdu16PeerConfigTable).filter(
                    SetOdu16PeerConfigTable.config_profile_id == device_param_list[0][4]).all()
                for i in range(0, len(peer_config_fields)):
                    oidname = oid_name[peer_config_fields[i]]
                    oidtype = oid_type[peer_config_fields[i]]
                    if i in dupli:
                        peer_config_param[i] = ""
                    if peer_config_param[i] == "":
                        oidvalue = ""
                    else:
                        oidvalue = peer_config_param[i]
                    result += snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                                       device_param_list[0][3], oidname, oidtype, oidvalue)
                err = error_odu16(result, param, err1)
                try:
                    el = EventLog()
                    if 1 in err1:
                        el.log_event(
                            "Values Updated in UBR Peer MAC Form", "%s" % (user_name))
                    for j in range(0, len(peer_config_fields)):
                        dict = {}
                        dict["name"] = form_name[j]
                        dict["value"] = peer_config_param[j]
                        dict["textbox"] = peer_config_fields[j]
                        dict["status"] = err1[j]
                        dictarr.append(dict)
                    for i in range(0, len(peer_config_param)):
                        if err1[i] == 1:
                            peer_config_table[
                                i].peer_mac_address = peer_config_param[i]
                            peer_config_table[i].index = i + 1
                    sqlalche_obj.session.commit()
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    if err != '':
                        raise Set_exception
                except Set_exception as e:
                    resultarray["result"] = dictarr
                    resultarray["tableName"] = 'SetOdu16PeerConfigTable'
                    resultarray['formAction'] = 'Peer_mac_Cancel.py'
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    return str(resultarray)
            else:
                for j in range(0, len(peer_config_fields)):
                    dict = {}
                    dict["name"] = form_name[j]
                    dict["value"] = peer_config_param[j]
                    dict["textbox"] = peer_config_fields[j]
                    dict["status"] = err1[j]
                    dictarr.append(dict)
                resultarray["result"] = dictarr
                resultarray["tableName"] = 'SetOdu16PeerConfigTable'
                resultarray['formAction'] = 'Peer_mac_Cancel.py'
                sqlalche_obj.sql_alchemy_db_connection_close()
                return str(resultarray)
        else:
            for j in range(0, len(peer_config_fields)):
                dict = {}
                dict["name"] = form_name[j]
                dict["value"] = peer_config_param[j]
                dict["textbox"] = peer_config_fields[j]
                dict["status"] = err1[j]
                dictarr.append(dict)
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16PeerConfigTable'
            resultarray['formAction'] = 'Peer_mac_Cancel.py'
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(resultarray)


def peer_slaves(host_id, peermac, syn_configuration_fields, syn_configuration_param):
    """

    @param host_id:
    @param peermac:
    @param syn_configuration_fields:
    @param syn_configuration_param:
    @return: @raise:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    syn_configuration = []
    result = ''
    param = []
    dictarr = []
    resultarray = {}
    form_name = ['Raster Time', 'Number of Slaves', 'SyncLossThreshold',
        'Leaky Bucket Timer', 'Sync Loss Time Out', 'Sync Timer Adjust']
    err1 = [0, 0, 0, 0, 0, 0]
    param.append('rasterTime.1')
    param.append('numSlaves.1')
    param.append('syncLossThreshold.1')
    param.append('leakyBucketTimer.1')
    param.append('syncLostTimeout.1')
    param.append('syncConfigTimerAdjust.1')
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
        filter(Hosts.host_id == host_id).all()
    syn_configuration = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
        SetOdu16SyncConfigTable.config_profile_id == device_param_list[0][4]).first()
    peer_config_table = sqlalche_obj.session.query(SetOdu16PeerConfigTable).filter(
        SetOdu16PeerConfigTable.config_profile_id == device_param_list[0][4]).all()
    admin_state = snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
                           device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '0')
    var = admin_state.find('adminStatus.1')
    timeslot = int(syn_configuration_param[1])
    timeslot = timeslot + 1
    count = []
    if var != -1:
        for i in range(int(syn_configuration_param[1]), peermac):
            peer_config_table[i].peer_mac_address = ''
            count.append(i)
            peer_config_table[i].index = i + 1
            ss = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][
                          2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s' % (i + 1), 's', "")
            count.append(ss)
        sqlalche_obj.session.commit()
        for i in range(len(syn_configuration_fields)):
            oidname = oid_name[syn_configuration_fields[i]]
            oidtype = oid_type[syn_configuration_fields[i]]
            oidvalue = syn_configuration_param[i]
            result += snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2],
                               device_param_list[0][3], oidname, oidtype, oidvalue)
        err = error_odu16(result, param, err1)
        try:
            el = EventLog()
            if 1 in err1:
                el.log_event(
                    "Values Updated in UBR UNMP Form", "%s" % (user_name))
            for j in range(0, len(syn_configuration_fields)):
                dict = {}
                dict["name"] = form_name[j]
                dict["value"] = syn_configuration_param[j]
                dict["textbox"] = syn_configuration_fields[j]
                dict["status"] = err1[j]
                dictarr.append(dict)
            if err1[0] == 1:
                syn_configuration.raster_time = syn_configuration_param[0]
            if err1[1] == 1:
                syn_configuration.num_slaves = syn_configuration_param[1]
            if err1[2] == 1:
                syn_configuration.sync_loss_threshold = syn_configuration_param[
                    2]
            if err1[3] == 1:
                syn_configuration.leaky_bucket_timer = syn_configuration_param[
                    3]
            if err1[4] == 1:
                syn_configuration.sync_lost_timeout = syn_configuration_param[
                    4]
            if err1[5] == 1:
                syn_configuration.sync_config_time_adjust = syn_configuration_param[
                    5]
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            if err != '':
                snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[0][
                         3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '1')
                raise Set_exception
        except Set_exception as e:
            resultarray["result"] = dictarr
            resultarray["tableName"] = 'SetOdu16PeerConfigTable'
            resultarray['formAction'] = 'Peer_mac_Cancel.py'
            resultarray['adminState'] = '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1'
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(resultarray)
    else:
        result = "Parameters are not set"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# acl_config_fields - these are the collection of form fields which are going to set on the device and store in the database
# acl_config_param- these are the collection of values of form fields which is set in the form and store in the database
# return the dictionary to odu_view which calues are set and which are not
# e.g 1 for set and 0 for not set


def acl_config_set(host_id, acl_field, acl_param, acl_config_fields, acl_config_param, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    acl_config_fields - these are the collection of form fields which are going to set on the device and store in the database
    acl_config_param- these are the collection of values of form fields which is set in the form and store in the database
    return the dictionary to odu_view which calues are set and which are not e.g 1 for set and 0 for not set
    @param host_id:
    @param acl_field:
    @param acl_param:
    @param acl_config_fields:
    @param acl_config_param:
    @param user_name:
    """
    global sqlalche_obj
    global html
    sqlalche_obj.sql_alchemy_db_connection_open()
    result = ''
    dictarr = []
    form_name = []
    err1 = []
    param = []
    count = 0
    resultarray = {}
    check_result = ''
    err_acl = 0
    oidname = oid_name['RU.RA.1.RAACLConfig.#.macAddress']
    oidtype = oid_type['RU.RA.1.RAACLConfig.#.macAddress']
    device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id, Hosts.snmp_read_community).\
        filter(Hosts.host_id == host_id).all()
    acl_table = sqlalche_obj.session.query(SetOdu16RAConfTable).filter(
        SetOdu16RAConfTable.config_profile_id == device_param_list[0][4]).all()
    ra_acl_config = sqlalche_obj.session.query(SetOdu16RAAclConfigTable).filter(
        SetOdu16RAAclConfigTable.config_profile_id == device_param_list[0][4]).order_by(SetOdu16RAAclConfigTable.index).all()
    acl_oid = oid_name[acl_field]
    acl_oid_type = oid_type[acl_field]
    result += snmp_set(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
                       device_param_list[0][3], acl_oid, acl_oid_type, acl_param)
    if 'aclMode.1' in result:
        err_acl = 1
        if err_acl == 1:
            acl_table[0].acl_mode = acl_param
            sqlalche_obj.session.commit()
    dic_acl = {}
    dic_acl['name'] = 'ACL Mode'
    dic_acl['value'] = acl_param
    dic_acl['textbox'] = 'RU.RA.1.RAConfTable.aclMode'
    dic_acl['status'] = err_acl
    if len(ra_acl_config) >= len(acl_config_fields):
        count = len(ra_acl_config)
    else:
        count = len(acl_config_fields)
    name_get = oidname.replace('#', '1')
    result += snmp_get(device_param_list[0][0], device_param_list[0][5],
                       device_param_list[0][2], device_param_list[0][3], name_get)

    check_result = result.find('No Such Instance currently exists at this OID')

    if int(check_result) == -1:

        for i in range(0, count):
            if i < 10:

                err1.append(0)
                form_name.append('Mac Address %s' % (i + 1))
                param.append('macaddress.1.%s' % (i + 1))
                name = oidname.replace('#', str(i + 1))
                type = oidtype.replace('#', 's')
                if acl_config_param[i] == "":
                    oidvalue = "                 "
                else:
                    oidvalue = acl_config_param[i]
                result += snmp_set(
                    device_param_list[0][
                        0], device_param_list[0][1], device_param_list[0][2],
                                   device_param_list[0][3], name, type, "%s " % (oidvalue))
            elif i >= 10:

                if len(ra_acl_config) > len(acl_config_fields):
                    for j in range(len(ra_acl_config), len(acl_config_fields), -1):
                        name = oidname.replace('#', str(j))
                        type = oidtype.replace('#', 's')
                        result += snmp_set(
                            device_param_list[0][
                                0], device_param_list[
                                    0][1], device_param_list[0][2],
                                           device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.5.1.3.1.%s' % (j), 'i', '6')
                    for k in range(10, len(acl_config_fields)):
                        err1.append(0)
                        form_name.append('Mac Address %s' % (k + 1))
                        param.append('macaddress.1.%s' % (k + 1))
                        name = oidname.replace('#', str(k + 1))
                        type = oidtype.replace('#', 's')
                        if acl_config_param[k] == "":
                            oidvalue = "                 "
                        else:
                            oidvalue = acl_config_param[k]
                        result += snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][
                                           2], device_param_list[0][3], name, type, "%s " % (oidvalue))
                    break
                elif int(len(ra_acl_config)) == int(len(acl_config_fields)):
                    for i in range(10, len(acl_config_fields)):
                        err1.append(0)
                        form_name.append('Mac Address %s' % (i + 1))
                        param.append('macaddress.1.%s' % (i + 1))
                        name = oidname.replace('#', str(i + 1))
                        type = oidtype.replace('#', 's')
                        if acl_config_param[i] == "":
                            oidvalue = "                 "
                        else:
                            oidvalue = acl_config_param[i]
                        result += snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][
                                           2], device_param_list[0][3], name, type, "%s " % (oidvalue))
                else:
                    for k in range(10, len(ra_acl_config)):
                        err1.append(0)
                        form_name.append('Mac Address %s' % (k + 1))
                        param.append('macaddress.1.%s' % (k + 1))
                        name = oidname.replace('#', str(k + 1))
                        type = oidtype.replace('#', 's')
                        if acl_config_param[k] == "":
                            oidvalue = "                 "
                        else:
                            oidvalue = acl_config_param[k]
                        result += snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][
                                           2], device_param_list[0][3], name, type, "%s " % (oidvalue))
                    for k in range(len(ra_acl_config), count):
                        err1.append(0)
                        form_name.append('Mac Address %s' % (k + 1))
                        param.append('macaddress.1.%s' % (k + 1))
                        name = oidname.replace('#', str(k + 1))
                        type = oidtype.replace('#', 's')
                        if acl_config_param[k] == "":
                            oidvalue = "                 "
                        else:
                            oidvalue = acl_config_param[k]
                        result += snmp_setmultiple(
                            device_param_list[0][0], device_param_list[0][
                                1], device_param_list[
                                    0][2], device_param_list[0][3],
                                                   '.1.3.6.1.4.1.26149.2.2.13.5.1.3.1.%s' % (k + 1), 'i', '4', name, type, "%s " % (oidvalue))

                    break
    else:
        for k in range(0, len(acl_config_fields)):
            err1.append(0)
            form_name.append('Mac Address %s' % (k + 1))
            param.append('macaddress.1.%s' % (k + 1))
            name = oidname.replace('#', str(k + 1))
            type = oidtype.replace('#', 's')
            if acl_config_param[k] == "":
                oidvalue = "                 "
            else:
                oidvalue = acl_config_param[k]
            result += snmp_setmultiple(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2], device_param_list[0][3],
                                       '.1.3.6.1.4.1.26149.2.2.13.5.1.3.1.%s' % (k + 1), 'i', '4', name, type, "%s " % (oidvalue))

    err = error_odu16(result, param, err1)
    dictarr.append(dic_acl)
    try:
        el = EventLog()
        if 1 in err1:
            el.log_event("Values Updated in UBR ACL Form", "%s" % (user_name))
        for j in range(0, len(acl_config_fields)):
            dict = {}
            dict["name"] = form_name[j]
            dict["value"] = acl_config_param[j]
            dict["textbox"] = acl_config_fields[j]
            dict["status"] = err1[j]
            dictarr.append(dict)
        del_acl_config = sqlalche_obj.session.query(SetOdu16RAAclConfigTable).filter(
            between(SetOdu16RAAclConfigTable.index, 11, int(len(ra_acl_config)))).all()
        if del_acl_config == []:
            val = 1
        else:
            for i in range(0, len(del_acl_config)):
                sqlalche_obj.session.delete(del_acl_config[i])
            sqlalche_obj.session.commit()
        for i in range(0, len(acl_config_fields)):
            if i < 10:
                if err1[i] == 1:
                    ra_acl_config[i].mac_address = acl_config_param[i]
                    ra_acl_config[i].index = i + 1
            if i >= 10:
                if err1[i] == 1:
                    sqlalche_obj.session.add(SetOdu16RAAclConfigTable('%s' % (
                        device_param_list[0][4]), '%s' % (acl_config_param[i]), '%s' % (i + 1)))
        sqlalche_obj.session.commit()
        if err != '':
            raise Set_exception
    except Set_exception as e:
        resultarray["result"] = dictarr
        resultarray["tableName"] = 'SetOdu16RAAclConfigTable'
        resultarray['formAction'] = 'Acl_Cancel_Configuration.py'
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(resultarray)


# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# table_name - it defines in which table the data is going to be saved
# textbox_value - it defines the oid name
# textbox_field - it defines the field name of database
# index_value - it defines the index parameters if exist otherwise it is empty

def retry_set_one(host_id, table_name, textbox, textbox_value, textbox_field, index_value, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    table_name - it defines in which table the data is going to be saved
    textbox_value - it defines the oid name
    textbox_field - it defines the field name of database
    index_value - it defines the index parameters if exist otherwise it is empty
    @param host_id:
    @param table_name:
    @param textbox:
    @param textbox_value:
    @param textbox_field:
    @param index_value:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    err = "0"
    result = ""
    str_table_obj = None
    oidname = oid_name[textbox]
    oidtype = oid_type[textbox]
    device_param_list = sqlalche_obj.session.query(
        Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    if textbox == 'RU.SyncClock.SyncConfigTable.rasterTime' or textbox == 'RU.SyncClock.SyncConfigTable.numSlaves' or textbox == 'RU.SyncClock.SyncConfigTable.timerAdjust':
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '0')
        if admin_state == "":
            result = "1"
        else:
            result = snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2],
                              device_param_list[0][3], oidname, oidtype, textbox_value)
            if result == "":
                result = "1"
            else:
                el = EventLog()
                el.log_event(
                    "Values Updated in UBR Synchronization Form in Retry Mode",
                             "%s" % (user_name))
                snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[0][
                         3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '1')
                str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                    table_name, table_name, device_param_list[0][4])
                exec str_table_obj
                str_table_obj = "table_result[0]." + \
                    textbox_field + " = '" + textbox_value + "'"
                exec str_table_obj
                sqlalche_obj.session.commit()
                result = "0"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

    elif textbox == 'ru.np.ra.1.tddmac.rfChannel' or textbox == 'ru.np.ra.1.tddmac.rfCoding' or textbox == 'ru.np.ra.1.tddmac.txPower' or textbox == 'RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase':
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '0')
        if admin_state == "":
            result = "1"
        else:
            el = EventLog()
            el.log_event(
                "Values Updated in UBR Radio Frequency Form in Retry Mode", "%s" % (user_name))
            result = snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2],
                              device_param_list[0][3], oidname, oidtype, textbox_value)
            if result == "":
                result = "1"
            else:
                snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[0][
                         3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '1')
                str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                    table_name, table_name, device_param_list[0][4])
                exec str_table_obj
                str_table_obj = "table_result[0]." + \
                    textbox_field + " = '" + textbox_value + "'"
                exec str_table_obj
                sqlalche_obj.session.commit()
                result = "0"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

    elif table_name == 'SetOdu16RAAclConfigTable':
        oidname = oid_name['RU.RA.1.RAACLConfig.#.macAddress']
        oidtype = oid_type['RU.RA.1.RAACLConfig.#.macAddress']
        if textbox_value == "":
            textbox_value = "                 "
        name = oidname.replace('#', index_value)
        type = oidtype.replace('#', 's')
        result = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                          0][2], device_param_list[0][3], name, type, "%s " % (textbox_value))
        if result == "":
            result = "1"
        else:
            el = EventLog()
            el.log_event("Values Updated in UBR ACL Form in Retry Mode",
                         "%s" % (user_name))
            str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                table_name, table_name, device_param_list[0][4])
            exec str_table_obj
            str_table_obj = "table_result[" + str(int(
                index_value) - 1) + "]." + textbox_field + " = '" + textbox_value + "'"
            exec str_table_obj
            str_table_obj = "table_result[" + str(int(
                index_value) - 1) + "].index" + " = '" + index_value + "'"
            sqlalche_obj.session.commit()
            result = "0"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

    elif table_name == "SetOdu16PeerConfigTable":
        oidname = oid_name[textbox]
        oidtype = oid_type[textbox]
        result = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                          0][3], oidname, oidtype, textbox_value)
        if result == "":
            result = "1"
        else:
            el = EventLog()
            el.log_event(
                "Values Updated in UBR Peer MAC Form in Retry Mode", "%s" % (user_name))
            str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                table_name, table_name, device_param_list[0][4])
            exec str_table_obj
            str_table_obj = "table_result[" + str(int(
                index_value) - 1) + "]." + textbox_field + " = '" + textbox_value + "'"
            exec str_table_obj
            str_table_obj = "table_result[" + str(int(
                index_value) - 1) + "].index" + " = '" + index_value + "'"
            sqlalche_obj.session.commit()
            result = "0"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

    elif table_name == 'SetOdu16RUConfTable':
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '0')
        if admin_state == "":
            result = "1"
        else:
            el = EventLog()
            el.log_event(
                "Values Updated in UBR Radio Unit Form in Retry Mode", "%s" % (user_name))
            result = snmp_set(
                device_param_list[0][0], device_param_list[
                    0][1], device_param_list[0][2],
                              device_param_list[0][3], oidname, oidtype, textbox_value)
            if result == "":
                result = "1"
            else:
                snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                         0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '1')
                str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                    table_name, table_name, device_param_list[0][4])
                exec str_table_obj
                str_table_obj = "table_result[0]." + \
                    textbox_field + " = '" + textbox_value + "'"
                exec str_table_obj
                sqlalche_obj.session.commit()
                result = "0"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

    else:
        result = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                          0][3], oidname, oidtype, textbox_value)
        if result == "":
            result = "1"
        else:
            el = EventLog()
            el.log_event(
                "Values Updated in UBR Form in Retry Mode", "%s" % (user_name))
            str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                table_name, table_name, device_param_list[0][4])

            exec str_table_obj
            str_table_obj = "table_result[0]." + \
                textbox_field + " = '" + textbox_value + "'"
            exec str_table_obj
            sqlalche_obj.session.commit()
            result = "0"
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

# Author - Anuj Samariya
# host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
# table_name - it defines the collection  in which table the data is going to be saved
# textbox_value - it defines the collection of oid name
# textbox_field - it defines the collection of field name of database
# index_value - it defines the index parameters if exist otherwise it is empty


def commit_to_flash(host_id, field, user_name):
    """

    @param host_id:
    @param field:
    @param user_name:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).\
            filter(Hosts.host_id == host_id).all()
        # print device_param_list[0].ip_address
        sqlalche_obj.sql_alchemy_db_connection_close()
        oidname = oid_name[field]

        result_commit = snmp_set(
            device_param_list[0][0], device_param_list[0][1],
                                 device_param_list[0][2], device_param_list[0][3], oidname, 'i', '4')
        time.sleep(5)
        if (result_commit == '' or result_commit == 'None'):
            return 'Device is not connected or Device is Rebooting.Please Retry Again.'
        else:
            el = EventLog()
            el.log_event(
                "Device Data is Commited To Flash", "%s" % (user_name))
            return "Configuration data has been permanently stored on the device"
    except Exception as e:
        return str(e)
# print commit_to_flash(72,'RU.RUOMOperationsTable.omOperationsReq',"")


def retry_set_for_all_odu16(host_id, table_name_list, textbox_list, textbox_field_list, textbox_value_list, index_value_list, user_name):
    """
    Author - Anuj Samariya
    host_id - this id is used to get the specific details of device  i.e. snmp version,snmp write community,snmp read community,snmp port,config profile id
    table_name - it defines the collection  in which table the data is going to be saved
    textbox_value - it defines the collection of oid name
    textbox_field - it defines the collection of field name of database
    index_value - it defines the index parameters if exist otherwise it is empty
    @param host_id:
    @param table_name_list:
    @param textbox_list:
    @param textbox_field_list:
    @param textbox_value_list:
    @param index_value_list:
    @param user_name:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    result = ''
    dic = {}
    str_table_obj = None
    device_param_list = sqlalche_obj.session.query(
        Hosts.snmp_version_id, Hosts.snmp_write_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
    if 'SetOdu16SyncConfigTable' in table_name_list:
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '0')
        if admin_state == '':
            dic['admin_state'] = 1
        else:
            for i in range(len(textbox_list)):
                oidname = oid_name[textbox_list[i]]
                oidtype = oid_type[textbox_list[i]]
                result = snmp_set(
                    device_param_list[0][
                        0], device_param_list[0][1], device_param_list[0][2],
                                  device_param_list[0][3], oidname, oidtype, textbox_value_list[i])
                if result == "":
                    dic[textbox_list[i]] = 1
                    snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '1')
                else:
                    el = EventLog()
                    el.log_event(
                        "Values Updated in UBR Synchronization Form in Retry All Mode",
                                 "%s" % (user_name))
                    dic[textbox_list[i]] = 0
                    str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                        table_name_list[i], table_name_list[i], device_param_list[0][4])
                    exec str_table_obj
                    str_table_obj = "table_result[0]." + \
                        textbox_field_list[i] + \
                            " = '" + textbox_value_list[i] + "'"
                    exec str_table_obj
                    sqlalche_obj.session.commit();
                    snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.11.1.1.2.1', 'i', '1')
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(dic)

    elif 'SetOdu16RATddMacConfig' in table_name_list:
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '0')
        if admin_state == '':
            dic['admin_state'] = 1
        else:
            for i in range(len(textbox_list)):
                oidname = oid_name[textbox_list[i]]
                oidtype = oid_type[textbox_list[i]]
                result = snmp_set(
                    device_param_list[0][
                        0], device_param_list[0][1], device_param_list[0][2],
                                  device_param_list[0][3], oidname, oidtype, textbox_value_list[i])
                if result == "":
                    dic[textbox_list[i]] = 1
                    snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '1')
                else:
                    el = EventLog()
                    el.log_event(
                        "Values Updated in UBR Radio Frequency Form in Retry All Mode",
                                 "%s" % (user_name))
                    dic[textbox_list[i]] = 0
                    str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                        table_name_list[i], table_name_list[i], device_param_list[0][4])
                    exec str_table_obj
                    str_table_obj = "table_result[0]." + \
                        textbox_field_list[i] + \
                            " = '" + textbox_value_list[i] + "'"
                    exec str_table_obj
                    sqlalche_obj.session.commit()
                    snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'i', '1')
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(dic)

    elif 'SetOdu16RUConfTable' in table_name_list:
        oid_multi_name = []
        oid_multi_type = []
        admin_state = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[
                               0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '0')
        if admin_state == '':
            dic['admin_state'] = 1
        else:
            for i in range(len(textbox_list)):
                oid_multi_name.append(oid_name[textbox_list[i]])
                oid_multi_type.append(oid_type[textbox_list[i]])
            result = snmp_setmultiple(
                device_param_list[0][0], device_param_list[0][1], device_param_list[
                    0][
                        2], device_param_list[
                            0][3], oid_multi_name[0], oid_multi_type[0],
                                      textbox_value_list[0], oid_multi_name[1], oid_multi_type[1], textbox_value_list[1])
            for i in range(len(textbox_list)):
                if result == "":
                    dic[textbox_list[i]] = 1
                    snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '1')
                else:
                    el = EventLog()
                    el.log_event(
                        "Values Updated in UBR Radio Unit Form in Retry All Mode", "%s" % (user_name))
                    dic[textbox_list[i]] = 0
                    str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                        table_name_list[i], table_name_list[i], device_param_list[0][4])
                    exec str_table_obj
                    str_table_obj = "table_result[0]." + \
                        textbox_field_list[i] + \
                            " = '" + textbox_value_list[i] + "'"
                    exec str_table_obj
                    sqlalche_obj.session.commit()
                    snmp_set(
                        device_param_list[0][
                            0], device_param_list[
                                0][1], device_param_list[0][2],
                             device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.1.1.2.1', 'i', '1')
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(dic)

    elif 'SetOdu16PeerConfigTable' in table_name_list:
        dupli = []
        for i in range(0, len(textbox_list)):
            j = textbox_value_list.count(textbox_value_list[i])
            if j > 1:
                dupli.append(i)
        for i in range(0, len(textbox_list)):
            oidname = oid_name[textbox_list[i]]
            oidtype = oid_type[textbox_list[i]]
            if i in dupli:
                textbox_value_list[i] = ""
            if textbox_value_list[i] == "":
                textbox_value_list[i] = ""
            result = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                              0][3], oidname, oidtype, textbox_value_list[i])
            if result == "" or result == None:
                dic[textbox_list[i]] = 1
            else:
                el = EventLog()
                el.log_event(
                    "Values Updated in UBR Peer MAC Form in Retry All Mode",
                             "%s" % (user_name))
                dic[textbox_list[i]] = 0
                str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').order_by(%s.index).all()" % (
                    table_name_list[i], table_name_list[i], device_param_list[0][4], table_name_list[i])
                exec str_table_obj
                str_table_obj = "table_result[" + str(int(index_value_list[i]) - 1) + "]." + \
                                                    textbox_field_list[i] + " = '" + \
                                                        textbox_value_list[
                                                            i] + "'"
                exec str_table_obj
                str_table_obj = "table_result[" + str(
                    int(index_value_list[i]) - 1) + "].index" + " = " + str(index_value_list[i])
                exec str_table_obj
            sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(dic)

    elif ('SetOdu16RAConfTable' in table_name_list) or ('SetOdu16RAAclConfigTable' in table_name_list):
        for i in range(0, len(textbox_list)):

            if textbox_list[i] == 'RU.RA.1.RAConfTable.aclMode':
                oidname = oid_name[textbox_list[i]]
                oidtype = oid_type[textbox_list[i]]
                result = snmp_set(
                    device_param_list[0][
                        0], device_param_list[0][1], device_param_list[0][2],
                                  device_param_list[0][3], oidname, oidtype, textbox_value_list[i])
                if result == "":
                    dic[textbox_list[i]] = 1
                else:
                    el = EventLog()
                    el.log_event(
                        "Values Updated in UBR RAConf Form in Retry All Mode",
                                 "%s" % (user_name))
                    dic[textbox_list[i]] = 0
                    str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                        table_name_list[i], table_name_list[i], device_param_list[0][4])
                    exec str_table_obj
                    str_table_obj = "table_result[0]." + \
                        textbox_field_list[i] + \
                            " = '" + textbox_value_list[i] + "'"
                    exec str_table_obj
                sqlalche_obj.session.commit()
            else:
                #
                oidname = oid_name['RU.RA.1.RAACLConfig.#.macAddress']
                oidtype = oid_type['RU.RA.1.RAACLConfig.#.macAddress']
                if textbox_value_list[i] == "":
                    textbox_value_list[i] = "                 "
                name = oidname.replace('#', str(index_value_list[i]))
                type = oidtype.replace('#', 's')
                result = snmp_set(
                    device_param_list[0][
                        0], device_param_list[0][1], device_param_list[0][2],
                                  device_param_list[0][3], name, type, "%s " % (textbox_value_list[i]))
                if result == "":
                    dic[textbox_list[i]] = 1
                else:
                    el = EventLog()
                    el.log_event(
                        "Values Updated in UBR UNMP Form", "%s" % (user_name))
                    dic[textbox_list[i]] = 0
                    str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').order_by(%s.index).all()" % (
                        table_name_list[i], table_name_list[i], device_param_list[0][4], table_name_list[i])
                    exec str_table_obj
                    str_table_obj = "table_result[" + str(int(index_value_list[i]) - 1) + "]." + \
                                                        textbox_field_list[i] + " = '" + \
                                                            textbox_value_list[
                                                                i] + "'"
                    exec str_table_obj
                    str_table_obj = "table_result[" + str(int(
                        index_value_list[i]) - 1) + "].index" + " = " + str(index_value_list[i])
                    exec str_table_obj
                sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(dic)

    else:
        for i in range(len(textbox_list)):
            oidname = oid_name[textbox_list[i]]
            oidtype = oid_type[textbox_list[i]]
            result = snmp_set(device_param_list[0][0], device_param_list[0][1], device_param_list[0][2], device_param_list[
                              0][3], oidname, oidtype, textbox_value_list[i])
            if result == "":
                dic[textbox_list[i]] = 1
            else:
                el = EventLog()
                el.log_event(
                    "Values Updated in UBR Form in Retry All Mode", "%s" % (user_name))
                dic[textbox_list[i]] = 0
                str_table_obj = "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                    table_name_list[i], table_name_list[i], device_param_list[0][4])
                exec str_table_obj
                str_table_obj = "table_result[0]." + \
                    textbox_field_list[i] + " = '" + \
                        textbox_value_list[i] + "'"
                exec str_table_obj
                sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(dic)

# Author- Anuj Samariya
# This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
# ip_address - This is the IP Address of device e.g 192.168.0.1
# mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
# selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
# return List of Devices in two dimensional list format


# new updated function
def get_device_list(ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid=None, html_var={}):  # ,sSortDir_0,iSortCol_0
    """
    Author- Anuj Samariya
    This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
    ip_address - This is the IP Address of device e.g 192.168.0.1
    mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
    selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
    return List of Devices in two dimensional list format
    @param ip_address:
    @param mac_address:
    @param selected_device:
    @param i_display_start:
    @param i_display_length:
    @param s_search:
    @param sEcho:
    @param sSortDir_0:
    @param iSortCol_0:
    @param userid:
    @param html_var:
    """
    # This is a empty list variable used for storing the device list
    device_list = []
    master_slave_select = []
    master_slave = ""
    device_dict = {}
    device_type = selected_device
    l = 0
    if device_type == '' or device_type == None:
        device_type = 'odu'
    device_list_state = "enabled"
    global sqlalche_obj
    # try block starts
    try:
        # here we create the session of sqlalchemy

        # this is the query which returns the multidimensional array of hosts table and store in device_tuple
#        device_tuple = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
#        filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
#        Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
#        UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
#        .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()

        device_dict = data_table_data_sqlalchemy(
            ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_var)
        # return device_dict
        device_tuple = device_dict["aaData"]
        index = int(device_dict["i_display_start"])
        sqlalche_obj.sql_alchemy_db_connection_open()
        device_status_host_id = ""
        global host_status_dic
        global essential_obj
        slave_data = "-"
        op_img = "images/host_status0.png"
        op_title = host_status_dic[0]
        ru_op_state = 1
        ra_op_state = 1
        sync_op_state = 1
    #[36, "172.22.0.111", "Default", "172.22.0.111", "FF:FF:FF:FF:FF:FF", " ", "odu16", 0, 304]
        # this loop create a mutildimesional list of host
        for i in range(0, len(device_tuple)):
            if device_tuple[i][6] == "odu16":
                master_slave_select = sqlalche_obj.session.query(
                    GetOdu16_ru_conf_table.default_node_type).filter(GetOdu16_ru_conf_table.host_id == device_tuple[i][0]).all()
                if len(master_slave_select) > 0:
                    if int(master_slave_select[0][0]) == 0 or int(master_slave_select[0][0]) == 2:
                        slave_data = "-"
                        master_slave = "RM18 (M)"
                    else:
                        slave_data = ""
                        host_alias = ""

                        master_host_id = sqlalche_obj.session.query(MasterSlaveLinking.master, Hosts.host_alias, Hosts.host_asset_id).\
                            outerjoin(Hosts, MasterSlaveLinking.slave == Hosts.host_id).filter(
                                MasterSlaveLinking.slave == device_tuple[i][0]).all()

                        # master_host_id =
                        # sqlalche_obj.session.query(MasterSlaveLinking.master).filter(MasterSlaveLinking.slave
                        # == device_tuple[i][0]).all()
                        if len(master_host_id) > 0:
                            # host_data =
                            # sqlalche_obj.session.query(Hosts.host_alias,Hosts.host_asset_id).filter(and_(Hosts.host_id==master_host_id[0][0],Hosts.is_deleted==0)).all()
                            host_alias = master_host_id[0].host_alias
                        # else:
                        #    host_alias = ""
##                            host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(HostAssets.host_asset_id==host_data[0].host_asset_id).all()
# master_mac = str(host_asset_data[0].ra_mac if len(host_asset_data)>0
# else "")

                            peer_status = sqlalche_obj.session.query(GetOdu16PeerNodeStatusTable.sig_strength, GetOdu16PeerNodeStatusTable.link_status).\
                                filter(GetOdu16PeerNodeStatusTable.host_id == device_tuple[i][0]).\
                                order_by(desc(GetOdu16PeerNodeStatusTable.get_odu16_peer_node_status_table_id)
                                         ).limit(1).all()
                            if len(peer_status) > 0:
                                if peer_status[0].sig_strength == None:
                                    slave_data = str(host_alias) + " ( )"
                                elif int(peer_status[0].sig_strength) == 1111111:
                                    slave_data = str(
                                        host_alias) + " (Device Unreachable)"

                                else:
                                    if peer_status[0].link_status == 1:
                                        slave_data = str(
                                            host_alias) + "( Link Disconnected )"
                                    else:
                                        slave_data = str(host_alias) + " (" + str(
                                            peer_status[0].sig_strength) + "dBm)"
                            else:
                                if host_alias != "" and host_alias != None:
                                    slave_data = str(host_alias) + "(-)"
                        master_slave = "RM18 (S)"
                else:
                    master_slave = "RM18 (-)"

                ru_data = sqlalche_obj.session.query(Odu100RuConfTable.adminstate, Odu100RaConfTable.raAdminState, Odu100SyncConfigTable.adminStatus).\
                    outerjoin(Odu100RaConfTable, Odu100RuConfTable.config_profile_id == Odu100RaConfTable.config_profile_id).\
                    outerjoin(Odu100SyncConfigTable, Odu100RuConfTable.config_profile_id == Odu100SyncConfigTable.config_profile_id).\
                    filter(
                        Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()
#                ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable.adminstate).filter(SetOdu16RUConfTable.config_profile_id==device_tuple[i][8]).all()
#                ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable.raAdminState).filter(SetOdu16RAConfTable.config_profile_id==device_tuple[i][8]).all()
# sync_data =
# sqlalche_obj.session.query(SetOdu16SyncConfigTable.adminStatus).filter(SetOdu16SyncConfigTable.config_profile_id==device_tuple[i][8]).all()

                if len(ru_data) > 0 and ru_data[0][0] != None and int(ru_data[0][0]) != 0:
                    ru_state = 0
                    image_ru_title = "RU State Locked"

                else:
                    ru_state = 1
                    image_ru_title = "RU State UnLocked"

                if len(ru_data) > 0 and ru_data[0][0] != None and int(ru_data[0][0]) != 0:
                    ra_state = 0
                    image_ra_title = "RA State Locked"
                else:
                    ra_state = 1
                    image_ra_title = "RA State Unlocked"

                if len(ru_data) > 0 and ru_data[0][0] != None and int(ru_data[0][0]) != 0:
                    sync_state = 0
                    image_sync_title = " SYNC State Locked"
                else:
                    sync_state = 0
                    image_sync_title = " SYNC State Unlocked"

            else:
                master_slave_select = sqlalche_obj.session.query(Odu100RuConfTable.defaultNodeType).filter(
                    Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()
                if len(master_slave_select) > 0:
                    if master_slave_select[0][0] == 0 or master_slave_select[0][0] == 2:
                        slave_data = "-"
                        master_slave = "RM (M)"
                    else:
                        # slave_data = "0"
                        slave_data = ""
                        host_alias = ""

                        # master_host_id =
                        # sqlalche_obj.session.query(MasterSlaveLinking.master).filter(MasterSlaveLinking.slave
                        # == device_tuple[i][0]).all()

                        master_host_id = sqlalche_obj.session.query(MasterSlaveLinking.master, Hosts.host_alias, Hosts.host_asset_id).\
                            outerjoin(Hosts, MasterSlaveLinking.slave == Hosts.host_id).filter(
                                MasterSlaveLinking.slave == device_tuple[i][0]).all()

                        if len(master_host_id) > 0:
                            # host_data =
                            # sqlalche_obj.session.query(Hosts.host_alias,Hosts.host_asset_id).filter(Hosts.host_id==master_host_id[0][0]).all()
                            host_alias = master_host_id[0].host_alias
                        # else:   # commented from raju
                        #    host_alias = "" # commented from raju

##                            host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(HostAssets.host_asset_id==host_data[0].host_asset_id).all()
##                            master_mac = str(host_asset_data[0].ra_mac if len(host_asset_data)>0 else "")+","
##                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1).\
# filter(and_(Odu100PeerNodeStatusTable.host_id==device_tuple[i][0],or_(Odu100PeerNodeStatusTable.peerMacAddr==master_mac,Odu100PeerNodeStatusTable.sigStrength1==1))).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()

                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1, Odu100PeerNodeStatusTable.linkStatus).\
                            filter(Odu100PeerNodeStatusTable.host_id == device_tuple[i][0]).order_by(desc(Odu100PeerNodeStatusTable.odu100_peerNodeStatusTable_id)).\
                            limit(1).all()

#                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1,Odu100PeerNodeStatusTable.linkStatus).\
# filter(Odu100PeerNodeStatusTable.host_id==device_tuple[i][0]).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()

                        if len(peer_status) > 0:
                            if peer_status[0].sigStrength1 == None:
                                slave_data = str(host_alias) + "()"
                            elif int(peer_status[0].sigStrength1) == 1111111:
                                slave_data = str(
                                    host_alias) + " (Device Unreachable)"
                            elif int(peer_status[0].sigStrength1) == 1:
                                slave_data = str(
                                    host_alias) + " (Device Unreachable)"
                            else:
                                if int(peer_status[0].linkStatus) == 1:
                                    slave_data = str(
                                        host_alias) + " ( Link Disconnected )"
                                else:
                                    slave_data = str(host_alias) + " (" + str(
                                        peer_status[0].sigStrength1) + "dBm)"
                        else:
                            if host_alias != "" and host_alias != None:
                                slave_data = str(host_alias) + "(-)"

                        master_slave = "RM (S)"
                else:
                    master_slave = "RM (-)"

                ru_data = sqlalche_obj.session.query(Odu100RuConfTable.adminstate, Odu100RaConfTable.raAdminState, Odu100SyncConfigTable.adminStatus).\
                    outerjoin(Odu100RaConfTable, Odu100RuConfTable.config_profile_id == Odu100RaConfTable.config_profile_id).\
                    outerjoin(Odu100SyncConfigTable, Odu100RuConfTable.config_profile_id == Odu100SyncConfigTable.config_profile_id).\
                    filter(
                        Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()

                ru_status = sqlalche_obj.session.query(Odu100RuStatusTable.ruoperationalState).filter(
                    Odu100RuStatusTable.host_id == device_tuple[i][0]).all()
                ra_status = sqlalche_obj.session.query(Odu100RaStatusTable.raoperationalState).filter(
                    Odu100RaStatusTable.host_id == device_tuple[i][0]).order_by(desc(Odu100RaStatusTable.timestamp)).all()
                sync_status = sqlalche_obj.session.query(Odu100SynchStatusTable.syncoperationalState).filter(
                    Odu100SynchStatusTable.host_id == device_tuple[i][0]).order_by(desc(Odu100SynchStatusTable.timestamp)).all()

                if len(ru_status) > 0 and ru_status[0].ruoperationalState != None:
                    ru_op_state = ru_status[0].ruoperationalState
                else:
                    ru_op_state = 1

                if len(ra_status) > 0 and ra_status[0].raoperationalState != None:
                    ra_op_state = ra_status[0].raoperationalState
                else:
                    ra_op_state = 1

                if len(sync_status) > 0 and sync_status[0].syncoperationalState == None:
                    sync_op_state = sync_status[0].syncoperationalState
                else:
                    sync_op_state = 1

                if len(ru_data) > 0:
                    if ru_data[0][0] != None and (int(ru_data[0][0]) == 0 or int(ru_op_state) == 0):
                        ru_state = 0
                        image_ru_title = "RU State Locked"
                    else:
                        ru_state = 1
                        image_ru_title = "RU State UnLocked"

                    if ru_data[0][1] != None and (int(ru_data[0][1]) == 0 or int(ra_op_state) == 0):
                        ra_state = 0
                        image_ra_title = "RA State Locked"
                    else:
                        ra_state = 1
                        image_ra_title = "RA State UnLocked"

                    if ru_data[0][2] != None and (int(ru_data[0][2]) == 0 or int(sync_op_state) == 0):
                        sync_state = 0
                        image_sync_title = "SYNC State Locked"
                    else:
                        sync_state = 1
                        image_sync_title = "SYNC State UnLocked"
                else:
                    ru_state = 1
                    image_ru_title = "RU State UnLocked"

                    ra_state = 1
                    image_ra_title = "RA State UnLocked"

                    sync_state = 1
                    image_sync_title = "SYNC State UnLocked"

#            if device_tuple[i][6] == "odu100":
#                if len(ru_data)>0:
#                    if ru_data[0][0]==None:
#                        ru_state = 1
#                        image_ru_title = "RU State UnLocked"
#                    else:
#                        if int(ru_data[0][0])==0:
#                            ru_state = 0
#                            image_ru_title = "RU State Locked"
#                        else:
#                            if int(ru_op_state)==0:
#                                ru_state = 0
#                                image_ru_title = "RU State UnLocked"
#                            else:
#                                ru_state = 1
#                                image_ru_title = "RU State UnLocked"
#                else:
#                    ru_state = 1
#                    image_ru_title = "RU State UnLocked"
#
#                if len(ru_data)>0:
#                    if ru_data[0][1]==None:
#                        ra_state = 1
#                        image_ra_title = "RA State Unlocked"
#
#                    else:
#                        if int(ru_data[0][1]) == 0:
#                            ra_state = 0
#                            image_ra_title = "RA State Locked"
#
#                        else:
#                            if int(ra_op_state)==0:
#                                ra_state = 0
#                                image_ra_title = "RA State Unlocked"
#                            else:
#                                ra_state = 1
#                                image_ra_title = "RA State Unlocked"
#                else:
#                    ra_state = 1
#                    image_ra_title = "RA State Unlocked"
#
#                if len(ru_data)>0:
#                    if ru_data[0][2]==None:
#                        sync_state = 1
#                        image_sync_title = " SYNC State Unlocked"
#
#                    else:
#                        if int(ru_data[0][2]) == 0:
#                            sync_state = 0
#                            image_sync_title = "SYNC State Locked"
#
#                        else:
#                            if int(sync_op_state)==0:
#                                sync_state = 0
#                                image_sync_title = " SYNC State Unlocked"
#                            else:
#                                sync_state = 1
#                                image_sync_title = " SYNC State Unlocked"
#                else:
#                    sync_state = 1
#                    image_sync_title = " SYNC State Unlocked"
#            else:
#                if len(ru_data)>0:
#                    if ru_data[0][0]==None:
#                        ru_state = 1
#                        image_ru_title = "RU State UnLocked"
#
#                    else:
#                        if int(ru_data[0][0])==0:
#                            ru_state = 0
#                            image_ru_title = "RU State Locked"
#
#                        else:
#                            ru_state = 1
#                            image_ru_title = "RU State UnLocked"
#
#                else:
#                    ru_state = 1
#                    image_ru_title = "RU State UnLocked"
#
#                if len(ru_data)>0:
#                    if ru_data[0][1]==None:
#                        ra_state = 1
#                        image_ra_title = "RA State Unlocked"
#
#                    else:
#                        if int(ru_data[0][1]) == 0:
#                            ra_state = 0
#                            image_ra_title = "RA State Locked"
#
#                        else:
#                            ra_state = 1
#                            image_ra_title = "RA State Unlocked"
#
#                else:
#                    ra_state = 1
#                    image_ra_title = "RA State Unlocked"
#
#                if len(ru_data)>0:
#                    if ru_data[0][2]==None:
#                        sync_state = 1
#                        image_sync_title = " SYNC State Unlocked"
#
#                    else:
#                        if int(ru_data[0][2]) == 0:
#                            sync_state = 0
#                            image_sync_title = "SYNC State Locked"
#
#                        else:
#                            sync_state = 1
#                            image_sync_title = " SYNC State Unlocked"
#
#                else:
#                    sync_state = 1
#                    image_sync_title = " SYNC State Unlocked"
            if device_tuple[i][7] <= 35:
                images = 'images/new/r-red.png'
            elif device_tuple[i][7] <= 90:
                images = 'images/new/r-black.png'
            else:
                images = 'images/new/r-green.png'

##            admin_dic = {'ru_admin':1 if ru_data[0][0]==None else int(ru_data[0][0]) if len(ru_data)>0 else 1,\
##                        'ra_admin':1 if ra_data[0][0]==None else int(ra_data[0][0]) if len(ra_data)>0 else 1,\
##                        'sync_admin':1 if sync_data[0][0]==None else int(sync_data[0][0]) if len(sync_data)>0 else 1}

            snmp_up_time_data = sqlalche_obj.db.execute(
                "select trap_event_id,timestamp from system_alarm_table where host_id='%s' order by timestamp desc limit 1" % (device_tuple[i][0]))
            snmp_up_down_time = ""
            for row in snmp_up_time_data:
                snmp_up_down_time = row['trap_event_id']
                timer_val = datetime.strftime(
                    row['timestamp'], "%d-%b-%Y %a %I:%M:%S %p")

            if snmp_up_down_time == '50001':
                device_status = "Device Unreachable since " + str(timer_val)
                device_status_image_path = "images/temp/red_dot.png"
            else:
                device_status = "Device Reachable"
                device_status_image_path = "images/temp/green_dot.png"

#            if snmp_up_down_time=="":
#                device_status = "Device Reachable"
#                device_status_image_path = "images/temp/green_dot.png"
#            elif int(snmp_up_down_time) == 50001:
#                device_status = "Device Unreachable since "+str(timer_val)
#                device_status_image_path = "images/temp/red_dot.png"
#            else:
#                device_status = "Device Reachable"
#                device_status_image_path = "images/temp/green_dot.png"
            op_status = essential_obj.get_hoststatus(device_tuple[i][0])
            if op_status == None:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[0]
            elif op_status == 0:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[op_status]
            else:
                op_img = "images/host_status1.png"
                op_title = host_status_dic[op_status]

            if i == len(device_tuple) - 1:
                device_status_host_id += str(device_tuple[i][0])
            else:
                device_status_host_id += str(device_tuple[i][0]) + ","

            monitoring_status = "<a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/info.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile w-reconcile\"/></a>" % ('sp_status_profiling.py',

                                                                                                                                                                                                                                                                      device_tuple[i][0], device_tuple[i][6], device_list_state) if device_tuple[i][6] == "odu100" else "<img src=\"images/new/info1.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile\"/>"

            live_monitoring = "&nbsp;&nbsp;<a target=\"main\" href=\"live_monitoring.py?host_id=%s&device_type=%s\"><img src=\"images/new/star-empty.png\" title=\"Live Monitoring\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" /></a>" % (device_tuple[i][0], device_tuple[i][6])\
                if device_tuple[i][6] == "odu100" else "&nbsp;&nbsp;<img src=\"images/new/star-empty.png\" title=\"Live Monitoring Not Available\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" />"

            device_list.append(
                ["<center><img id=\"device_status\" name=\"device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton w-reconcile\" original-title=\"%s\" /></center>&nbsp;&nbsp;" % (device_status_image_path, device_status, device_status), device_tuple[i][1], device_tuple[i][2], device_tuple[i][3], device_tuple[i][4], "-" if device_tuple[i][5] == " " else device_tuple[i][5], master_slave, slave_data,
                                "<ul class=\"button_group\" style=\"width:80px;\">\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.ruConfTable.adminstate\" name=\"ru.ruConfTable.adminstate\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.ruConfTable.adminstate')\">RU</a>\
                </li>\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.syncClock.syncConfigTable.adminStatus\" name=\"ru.syncClock.syncConfigTable.adminStatus\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.syncClock.syncConfigTable.adminStatus')\">SYN</a>\
                </li>\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.ra.raConfTable.raAdminState\" name=\"ru.ra.raConfTable.raAdminState\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.ra.raConfTable.raAdminState')\">RA</a>\
                </li>\
            </ul>"
                                % (
                                    "red" if ru_state == 0 else "green", image_ru_title, ru_state, device_tuple[
                                        i][0], device_tuple[i][6],
                                  "red" if sync_state == 0 else "green", image_sync_title, sync_state, device_tuple[
                                      i][0], device_tuple[i][6],
                                  "red" if ra_state == 0 else "green", image_ra_title, ra_state, device_tuple[i][0], device_tuple[i][6]),
                                "<a target=\"main\" href=\"odu_profiling.py?host_id=%s&device_type=%s&device_list_state=%s\">\
            <img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
            <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarm\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\" href=\"javascript:apFormwareUpdate('%s','%s','%s');\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton n-reconcile\"/ ></a>&nbsp;\
            <img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"imgReconcile(this,'%s','%s','odu16_','imgodu16'); state_rec=0\"/>\
            %s&nbsp;%s&nbsp;\
            <img src=\"images/new/cong_download.png\" title=\"Configuration Download \" class=\"imgbutton n-reconcile\" onclick=\"cnfigurationReportDownload(%s);\" />\
            %s"
                                % (
                                    device_tuple[
                                        i][
                                            0], device_tuple[
                                                i][6], device_list_state,
                                  device_tuple[i][0], 'sp_dashboard_profiling.py' if device_tuple[i][
                                      6] == "odu100" else 'sp_dashboard_profiling.py',
                                  device_tuple[i][
                                      0], device_tuple[
                                          i][
                                              6], device_list_state, device_tuple[i][3],
                                  device_tuple[i][0], device_tuple[i][
                                      6], device_list_state, images, device_tuple[i][7], device_tuple[i][0], device_tuple[i][6],
                                  live_monitoring, monitoring_status, device_tuple[
                                      i][0],
                                  "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (device_status_host_id) if i == len(device_tuple) - 1 else ""), "<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\" original-title=\"%s\"/></center>&nbsp;&nbsp;" % (op_img, op_title, op_title)])

        device_dict["aaData"] = device_list
        sqlalche_obj.sql_alchemy_db_connection_close()
        return device_dict
    # try block ends
    # href=\"javascript:apFormwareUpdate('%s','%s','%s');
    # exception starts
    except Exception as e:

        # return device_list
        sqlalche_obj.sql_alchemy_db_connection_close()
        output2 = {
            "sEcho": 1,
            "iTotalRecords": 10,
            "iTotalDisplayRecords": 10,
            "aaData": [],
            "query": str(e)
        }
        return output2
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# old function created by ANUJ##################################

def get_device_list_old(ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid=None, html_var={}):  # ,sSortDir_0,iSortCol_0
    """
    Author- Anuj Samariya
    This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
    ip_address - This is the IP Address of device e.g 192.168.0.1
    mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
    selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
    return List of Devices in two dimensional list format
    @param ip_address:
    @param mac_address:
    @param selected_device:
    @param i_display_start:
    @param i_display_length:
    @param s_search:
    @param sEcho:
    @param sSortDir_0:
    @param iSortCol_0:
    @param userid:
    @param html_var:
    """
    # This is a empty list variable used for storing the device list
    device_list = []
    master_slave_select = []
    master_slave = ""
    device_dict = {}
    device_type = selected_device
    l = 0
    if device_type == '' or device_type == None:
        device_type = 'odu'
    device_list_state = "enabled"
    global sqlalche_obj
    # try block starts
    try:
        # here we create the session of sqlalchemy

        # this is the query which returns the multidimensional array of hosts table and store in device_tuple
#        device_tuple = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
#        filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
#        Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
#        UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
#        .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()

        device_dict = data_table_data_sqlalchemy(
            ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_var)
        # return device_dict
        device_tuple = device_dict["aaData"]
        index = int(device_dict["i_display_start"])
        sqlalche_obj.sql_alchemy_db_connection_open()
        device_status_host_id = ""
        global host_status_dic
        global essential_obj
        slave_data = "-"
        op_img = "images/host_status0.png"
        op_title = host_status_dic[0]
        ru_op_state = 1
        ra_op_state = 1
        sync_op_state = 1
    #[36, "172.22.0.111", "Default", "172.22.0.111", "FF:FF:FF:FF:FF:FF", " ", "odu16", 0, 304]
        # this loop create a mutildimesional list of host
        for i in range(0, len(device_tuple)):
            if device_tuple[i][6] == "odu16":
                master_slave_select = sqlalche_obj.session.query(
                    GetOdu16_ru_conf_table.default_node_type).filter(GetOdu16_ru_conf_table.host_id == device_tuple[i][0]).all()
                if len(master_slave_select) > 0:
                    if int(master_slave_select[0][0]) == 0 or int(master_slave_select[0][0]) == 2:
                        slave_data = "-"
                        master_slave = "RM18 (M)"
                    else:
                        slave_data = ""
                        master_host_id = sqlalche_obj.session.query(MasterSlaveLinking.master).filter(
                            MasterSlaveLinking.slave == device_tuple[i][0]).all()
                        if len(master_host_id) > 0:
                            host_data = sqlalche_obj.session.query(Hosts.host_alias, Hosts.host_asset_id).filter(
                                and_(Hosts.host_id == master_host_id[0][0], Hosts.is_deleted == 0)).all()
                            host_alias = host_data[0].host_alias
                        else:
                            host_alias = ""
##                            host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(HostAssets.host_asset_id==host_data[0].host_asset_id).all()
# master_mac = str(host_asset_data[0].ra_mac if len(host_asset_data)>0
# else "")
                            peer_status = sqlalche_obj.session.query(GetOdu16PeerNodeStatusTable.sig_strength, GetOdu16PeerNodeStatusTable.link_status).\
                                filter(GetOdu16PeerNodeStatusTable.host_id == device_tuple[i][0]).order_by(
                                    desc(GetOdu16PeerNodeStatusTable.timestamp)).limit(1).all()
                            if len(peer_status) > 0:
                                if peer_status[0].sig_strength == None:
                                    slave_data = str(host_alias) + " ( )"
                                elif int(peer_status[0].sig_strength) == 1111111:
                                    slave_data = str(
                                        host_alias) + " (Device Unreachable)"

                                else:
                                    if peer_status[0].link_status == 1:
                                        slave_data = str(
                                            host_alias) + "( Link Disconnected )"
                                    else:
                                        slave_data = str(host_alias) + " (" + str(
                                            peer_status[0].sig_strength) + "dBm)"
                            else:
                                if host_alias != "" and host_alias != None:
                                    slave_data = str(host_alias) + "(-)"
                        master_slave = "RM18 (S)"
                else:
                    master_slave = "RM18 (-)"
                ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable.adminstate).filter(
                    SetOdu16RUConfTable.config_profile_id == device_tuple[i][8]).all()
                ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable.raAdminState).filter(
                    SetOdu16RAConfTable.config_profile_id == device_tuple[i][8]).all()
                sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable.adminStatus).filter(
                    SetOdu16SyncConfigTable.config_profile_id == device_tuple[i][8]).all()
            else:
                master_slave_select = sqlalche_obj.session.query(Odu100RuConfTable.defaultNodeType).filter(
                    Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()
                if len(master_slave_select) > 0:
                    if master_slave_select[0][0] == 0 or master_slave_select[0][0] == 2:
                        slave_data = "-"
                        master_slave = "RM (M)"
                    else:
                        # slave_data = "0"
                        slave_data = ""
                        master_host_id = sqlalche_obj.session.query(MasterSlaveLinking.master).filter(
                            MasterSlaveLinking.slave == device_tuple[i][0]).all()
                        if len(master_host_id) > 0:
                            host_data = sqlalche_obj.session.query(
                                Hosts.host_alias, Hosts.host_asset_id).filter(Hosts.host_id == master_host_id[0][0]).all()
                            host_alias = host_data[0].host_alias
                        else:
                            host_alias = ""
##                            host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(HostAssets.host_asset_id==host_data[0].host_asset_id).all()
##                            master_mac = str(host_asset_data[0].ra_mac if len(host_asset_data)>0 else "")+","
##                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1).\
# filter(and_(Odu100PeerNodeStatusTable.host_id==device_tuple[i][0],or_(Odu100PeerNodeStatusTable.peerMacAddr==master_mac,Odu100PeerNodeStatusTable.sigStrength1==1))).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()
                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1, Odu100PeerNodeStatusTable.linkStatus).\
                            filter(Odu100PeerNodeStatusTable.host_id == device_tuple[i][0]
                                   ).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()
                        if len(peer_status) > 0:
                            if peer_status[0].sigStrength1 == None:
                                slave_data = str(host_alias) + "()"
                            elif int(peer_status[0].sigStrength1) == 1111111:
                                slave_data = str(
                                    host_alias) + " (Device Unreachable)"
                            elif int(peer_status[0].sigStrength1) == 1:
                                slave_data = str(
                                    host_alias) + " (Device Unreachable)"
                            else:
                                if int(peer_status[0].linkStatus) == 1:
                                    slave_data = str(
                                        host_alias) + " ( Link Disconnected )"
                                else:
                                    slave_data = str(host_alias) + " (" + str(
                                        peer_status[0].sigStrength1) + "dBm)"
                        else:
                            if host_alias != "" and host_alias != None:
                                slave_data = str(host_alias) + "(-)"
##                    else:
##                        slave_data = "(-)"
                        master_slave = "RM (S)"
                else:
                    master_slave = "RM (-)"
                ru_data = sqlalche_obj.session.query(Odu100RuConfTable.adminstate).filter(
                    Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()
                ra_data = sqlalche_obj.session.query(Odu100RaConfTable.raAdminState).filter(
                    Odu100RaConfTable.config_profile_id == device_tuple[i][8]).all()
                sync_data = sqlalche_obj.session.query(Odu100SyncConfigTable.adminStatus).filter(
                    Odu100SyncConfigTable.config_profile_id == device_tuple[i][8]).all()
                ru_status = sqlalche_obj.session.query(Odu100RuStatusTable.ruoperationalState).filter(
                    Odu100RuStatusTable.host_id == device_tuple[i][0]).all()
                ra_status = sqlalche_obj.session.query(Odu100RaStatusTable.raoperationalState).filter(
                    Odu100RaStatusTable.host_id == device_tuple[i][0]).order_by(desc(Odu100RaStatusTable.timestamp)).all()
                sync_status = sqlalche_obj.session.query(Odu100SynchStatusTable.syncoperationalState).filter(
                    Odu100SynchStatusTable.host_id == device_tuple[i][0]).order_by(desc(Odu100SynchStatusTable.timestamp)).all()
                if len(ru_status) > 0:
                    if ru_status[0].ruoperationalState == None:
                        ru_op_state = 1
                    else:
                        ru_op_state = ru_status[0].ruoperationalState
                else:
                    ru_op_state = 1

                if len(ra_status) > 0:
                    if ra_status[0].raoperationalState == None:
                        ra_op_state = 1
                    else:
                        ra_op_state = ra_status[0].raoperationalState
                else:
                    ra_op_state = 1

                if len(sync_status) > 0:
                    if sync_status[0].syncoperationalState == None:
                        sync_op_state = 1
                    else:
                        sync_op_state = sync_status[0].syncoperationalState
                else:
                    sync_op_state = 1
            if device_tuple[i][6] == "odu100":
                if len(ru_data) > 0:
                    if ru_data[0][0] == None:
                        ru_state = 1
                        image_ru_title = "RU State UnLocked"
                    else:
                        if int(ru_data[0][0]) == 0:
                            ru_state = 0
                            image_ru_title = "RU State Locked"
                        else:
                            if int(ru_op_state) == 0:
                                ru_state = 0
                                image_ru_title = "RU State UnLocked"
                            else:
                                ru_state = 1
                                image_ru_title = "RU State UnLocked"
                else:
                    ru_state = 1
                    image_ru_title = "RU State UnLocked"

                if len(ra_data) > 0:
                    if ra_data[0][0] == None:
                        ra_state = 1
                        image_ra_title = "RA State Unlocked"

                    else:
                        if int(ra_data[0][0]) == 0:
                            ra_state = 0
                            image_ra_title = "RA State Locked"

                        else:
                            if int(ra_op_state) == 0:
                                ra_state = 0
                                image_ra_title = "RA State Unlocked"
                            else:
                                ra_state = 1
                                image_ra_title = "RA State Unlocked"
                else:
                    ra_state = 1
                    image_ra_title = "RA State Unlocked"

                if len(sync_data) > 0:
                    if sync_data[0][0] == None:
                        sync_state = 1
                        image_sync_title = " SYNC State Unlocked"

                    else:
                        if int(sync_data[0][0]) == 0:
                            sync_state = 0
                            image_sync_title = "SYNC State Locked"

                        else:
                            if int(sync_op_state) == 0:
                                sync_state = 0
                                image_sync_title = " SYNC State Unlocked"
                            else:
                                sync_state = 1
                                image_sync_title = " SYNC State Unlocked"
                else:
                    sync_state = 1
                    image_sync_title = " SYNC State Unlocked"
            else:
                if len(ru_data) > 0:
                    if ru_data[0][0] == None:
                        ru_state = 1
                        image_ru_title = "RU State UnLocked"

                    else:
                        if int(ru_data[0][0]) == 0:
                            ru_state = 0
                            image_ru_title = "RU State Locked"

                        else:
                            ru_state = 1
                            image_ru_title = "RU State UnLocked"

                else:
                    ru_state = 1
                    image_ru_title = "RU State UnLocked"

                if len(ra_data) > 0:
                    if ra_data[0][0] == None:
                        ra_state = 1
                        image_ra_title = "RA State Unlocked"

                    else:
                        if int(ra_data[0][0]) == 0:
                            ra_state = 0
                            image_ra_title = "RA State Locked"

                        else:
                            ra_state = 1
                            image_ra_title = "RA State Unlocked"

                else:
                    ra_state = 1
                    image_ra_title = "RA State Unlocked"

                if len(sync_data) > 0:
                    if sync_data[0][0] == None:
                        sync_state = 1
                        image_sync_title = " SYNC State Unlocked"

                    else:
                        if int(sync_data[0][0]) == 0:
                            sync_state = 0
                            image_sync_title = "SYNC State Locked"

                        else:
                            sync_state = 1
                            image_sync_title = " SYNC State Unlocked"

                else:
                    sync_state = 1
                    image_sync_title = " SYNC State Unlocked"

            if device_tuple[i][7] <= 35:
                images = 'images/new/r-red.png'
            elif device_tuple[i][7] <= 90:
                images = 'images/new/r-black.png'
            else:
                images = 'images/new/r-green.png'

##            admin_dic = {'ru_admin':1 if ru_data[0][0]==None else int(ru_data[0][0]) if len(ru_data)>0 else 1,\
##                        'ra_admin':1 if ra_data[0][0]==None else int(ra_data[0][0]) if len(ra_data)>0 else 1,\
##                        'sync_admin':1 if sync_data[0][0]==None else int(sync_data[0][0]) if len(sync_data)>0 else 1}

            snmp_up_time_data = sqlalche_obj.db.execute(
                "select trap_event_id,timestamp from system_alarm_table where host_id='%s' order by timestamp desc limit 1" % (device_tuple[i][0]))
            snmp_up_down_time = ""
            for row in snmp_up_time_data:
                snmp_up_down_time = row['trap_event_id']
                timer_val = datetime.strftime(
                    row['timestamp'], "%d-%b-%Y %a %I:%M:%S %p")
            if snmp_up_down_time == "":
                device_status = "Device Reachable"
                device_status_image_path = "images/temp/green_dot.png"
            elif int(snmp_up_down_time) == 50001:
                device_status = "Device Unreachable since " + str(timer_val)
                device_status_image_path = "images/temp/red_dot.png"
            else:
                device_status = "Device Reachable"
                device_status_image_path = "images/temp/green_dot.png"

            op_status = essential_obj.get_hoststatus(device_tuple[i][0])
            if op_status == None:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[0]
            elif op_status == 0:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[op_status]
            else:
                op_img = "images/host_status1.png"
                op_title = host_status_dic[op_status]

            if i == len(device_tuple) - 1:
                device_status_host_id += str(device_tuple[i][0])
            else:
                device_status_host_id += str(device_tuple[i][0]) + ","

            monitoring_status = "<a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/info.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile w-reconcile\"/></a>" % ('sp_status_profiling.py',

                                                                                                                                                                                                                                                                      device_tuple[i][0], device_tuple[i][6], device_list_state) if device_tuple[i][6] == "odu100" else "<img src=\"images/new/info1.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile\"/>"

            live_monitoring = "&nbsp;&nbsp;<a target=\"main\" href=\"live_monitoring.py?host_id=%s&device_type=%s\"><img src=\"images/new/star-empty.png\" title=\"Live Monitoring\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" /></a>" % (device_tuple[i][0], device_tuple[i][6])\
                if device_tuple[i][6] == "odu100" else "&nbsp;&nbsp;<img src=\"images/new/star-empty.png\" title=\"Live Monitoring Not Available\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" />"

            device_list.append(
                ["<center><img id=\"device_status\" name=\"device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton w-reconcile\" original-title=\"%s\" /></center>&nbsp;&nbsp;" % (device_status_image_path, device_status, device_status), device_tuple[i][1], device_tuple[i][2], device_tuple[i][3], device_tuple[i][4], "-" if device_tuple[i][5] == " " else device_tuple[i][5], master_slave, slave_data,
                                "<ul class=\"button_group\" style=\"width:80px;\">\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.ruConfTable.adminstate\" name=\"ru.ruConfTable.adminstate\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.ruConfTable.adminstate')\">RU</a>\
                </li>\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.syncClock.syncConfigTable.adminStatus\" name=\"ru.syncClock.syncConfigTable.adminStatus\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.syncClock.syncConfigTable.adminStatus')\">SYN</a>\
                </li>\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.ra.raConfTable.raAdminState\" name=\"ru.ra.raConfTable.raAdminState\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.ra.raConfTable.raAdminState')\">RA</a>\
                </li>\
            </ul>"
                                % (
                                    "red" if ru_state == 0 else "green", image_ru_title, ru_state, device_tuple[
                                        i][0], device_tuple[i][6],
                                  "red" if sync_state == 0 else "green", image_sync_title, sync_state, device_tuple[
                                      i][0], device_tuple[i][6],
                                  "red" if ra_state == 0 else "green", image_ra_title, ra_state, device_tuple[i][0], device_tuple[i][6]),
                                "<a target=\"main\" href=\"odu_profiling.py?host_id=%s&device_type=%s&device_list_state=%s\">\
            <img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
            <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarm\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\" href=\"javascript:apFormwareUpdate('%s','%s','%s');\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton n-reconcile\"/ ></a>&nbsp;\
            <img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"imgReconcile(this,'%s','%s','odu16_','imgodu16'); state_rec=0\"/>\
            %s&nbsp;%s\
            %s"
                                % (
                                    device_tuple[
                                        i][
                                            0], device_tuple[
                                                i][6], device_list_state,
                                  device_tuple[i][0], 'sp_dashboard_profiling.py' if device_tuple[i][
                                      6] == "odu100" else 'sp_dashboard_profiling.py',
                                  device_tuple[i][
                                      0], device_tuple[
                                          i][
                                              6], device_list_state, device_tuple[i][3],
                                  device_tuple[i][0], device_tuple[i][
                                      6], device_list_state, images, device_tuple[i][7], device_tuple[i][0], device_tuple[i][6],
                                  live_monitoring, monitoring_status,
                                  "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (device_status_host_id) if i == len(device_tuple) - 1 else ""), "<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\" original-title=\"%s\"/></center>&nbsp;&nbsp;" % (op_img, op_title, op_title)])

        device_dict["aaData"] = device_list
        sqlalche_obj.sql_alchemy_db_connection_close()
        return device_dict
    # try block ends
    # href=\"javascript:apFormwareUpdate('%s','%s','%s');
    # exception starts
    except Exception as e:

        # return device_list
        sqlalche_obj.sql_alchemy_db_connection_close()
        output2 = {
            "sEcho": 1,
            "iTotalRecords": 10,
            "iTotalDisplayRecords": 10,
            "aaData": [],
            "query": str(e)
        }
        return output2
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# firmware_update_device_show.py?host_id=%s&device_type=%s&device_list_state=%s
# Author- Yogesh
# This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
# ip_address - This is the IP Address of device e.g 192.168.0.1
# mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
# selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
# return List of Devices in two dimensional list format


def get_device_list_guest(ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_var={}):
    """
    Author- Anuj Samariya
    This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
    ip_address - This is the IP Address of device e.g 192.168.0.1
    mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
    selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
    return List of Devices in two dimensional list format
    @param ip_address:
    @param mac_address:
    @param selected_device:
    @param i_display_start:
    @param i_display_length:
    @param s_search:
    @param sEcho:
    @param sSortDir_0:
    @param iSortCol_0:
    @param userid:
    @param html_var:
    """
    # This is a empty list variable used for storing the device list
    device_list = []
    master_slave_select = []
    master_slave = ""
    device_dict = {}
    device_type = selected_device
    if device_type == '' or device_type == None:
        device_type = 'odu'
    device_list_state = "enabled"
    global sqlalche_obj
    # try block starts
    try:
        # here we create the session of sqlalchemy

        # this is the query which returns the multidimensional array of hosts table and store in device_tuple
#        device_tuple = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
#        filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
#        Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
#        UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
#        .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()

        device_dict = data_table_data_sqlalchemy(
            ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_var)

        device_tuple = device_dict["aaData"]
        index = int(device_dict["i_display_start"])

        sqlalche_obj.sql_alchemy_db_connection_open()
        device_status_host_id = ""
    #[36, "172.22.0.111", "Default", "172.22.0.111", "FF:FF:FF:FF:FF:FF", " ", "odu16", 0, 304]
        # this loop create a mutildimesional list of host
        for i in range(0, len(device_tuple)):
            if device_tuple[i][6] == "odu16":
                master_slave_select = sqlalche_obj.session.query(
                    GetOdu16_ru_conf_table.default_node_type).filter(GetOdu16_ru_conf_table.host_id == device_tuple[i][0]).all()
                if len(master_slave_select) > 0:
                    if int(master_slave_select[0][0]) == 0 or int(master_slave_select[0][0]) == 2:
                        slave_data = "-"
                        master_slave = "RM18 (Master)"
                    else:
                        slave_data = ""
                        master_host_id = sqlalche_obj.session.query(MasterSlaveLinking.master).filter(
                            MasterSlaveLinking.slave == device_tuple[i][0]).all()
                        if len(master_host_id) > 0:
                            host_data = sqlalche_obj.session.query(Hosts.host_alias, Hosts.host_asset_id).filter(
                                and_(Hosts.host_id == master_host_id[0][0], Hosts.is_deleted == 0)).all()
                            host_alias = host_data[0].host_alias
                        else:
                            host_alias = ""
##                            host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(HostAssets.host_asset_id==host_data[0].host_asset_id).all()
# master_mac = str(host_asset_data[0].ra_mac if len(host_asset_data)>0
# else "")
                            peer_status = sqlalche_obj.session.query(GetOdu16PeerNodeStatusTable.sig_strength, GetOdu16PeerNodeStatusTable.link_status).\
                                filter(GetOdu16PeerNodeStatusTable.host_id == device_tuple[i][0]).order_by(
                                    desc(GetOdu16PeerNodeStatusTable.timestamp)).limit(1).all()
                            if len(peer_status) > 0:
                                if peer_status[0].sig_strength == None:
                                    slave_data = str(host_alias) + " ( )"
                                elif int(peer_status[0].sig_strength) == 1111111:
                                    slave_data = str(
                                        host_alias) + " (Device Unreachable)"

                                else:
                                    if peer_status[0].link_status == 1:
                                        slave_data = str(
                                            host_alias) + "( Link Disconnected )"
                                    else:
                                        slave_data = str(host_alias) + " (" + str(
                                            peer_status[0].sig_strength) + "dBm)"
                            else:
                                slave_data = str(host_alias) + "(-)"
                        master_slave = "RM18 (S)"

                else:
                    master_slave = "Rm18(-)"
                ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable.adminstate).filter(
                    SetOdu16RUConfTable.config_profile_id == device_tuple[i][8]).all()
                ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable.raAdminState).filter(
                    SetOdu16RAConfTable.config_profile_id == device_tuple[i][8]).all()
                sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable.adminStatus).filter(
                    SetOdu16SyncConfigTable.config_profile_id == device_tuple[i][8]).all()
            else:
                master_slave_select = sqlalche_obj.session.query(Odu100RuConfTable.defaultNodeType).filter(
                    Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()
                if len(master_slave_select) > 0:
                    if master_slave_select[0][0] == 0 or master_slave_select[0][0] == 2:
                        slave_data = "-"
                        master_slave = "RM (Master)"
                    else:
                        # slave_data = "0"
                        slave_data = ""
                        master_host_id = sqlalche_obj.session.query(MasterSlaveLinking.master).filter(
                            MasterSlaveLinking.slave == device_tuple[i][0]).all()
                        if len(master_host_id) > 0:
                            host_data = sqlalche_obj.session.query(
                                Hosts.host_alias, Hosts.host_asset_id).filter(Hosts.host_id == master_host_id[0][0]).all()
                            host_alias = host_data[0].host_alias
                        else:
                            host_alias = ""
##                            host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(HostAssets.host_asset_id==host_data[0].host_asset_id).all()
##                            master_mac = str(host_asset_data[0].ra_mac if len(host_asset_data)>0 else "")+","
##                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1).\
# filter(and_(Odu100PeerNodeStatusTable.host_id==device_tuple[i][0],or_(Odu100PeerNodeStatusTable.peerMacAddr==master_mac,Odu100PeerNodeStatusTable.sigStrength1==1))).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()
                        peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1, Odu100PeerNodeStatusTable.linkStatus).\
                            filter(Odu100PeerNodeStatusTable.host_id == device_tuple[i][0]
                                   ).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()
                        if len(peer_status) > 0:
                            if peer_status[0].sigStrength1 == None:
                                slave_data = str(host_alias) + "()"
                            elif int(peer_status[0].sigStrength1) == 1111111:
                                slave_data = str(
                                    host_alias) + " (Device Unreachable)"
                            else:
                                if int(peer_status[0].linkStatus) == 1:
                                    slave_data = str(
                                        host_alias) + " ( Link Disconnected )"
                                else:
                                    slave_data = str(host_alias) + " (" + str(
                                        peer_status[0].sigStrength1) + "dBm)"
                        else:
                            slave_data = str(host_alias) + "(-)"
##                    else:
##                        slave_data = "(-)"
                        master_slave = "RM (S)"
                else:
                    master_slave = "RM(-)"
                ru_data = sqlalche_obj.session.query(Odu100RuConfTable.adminstate).filter(
                    Odu100RuConfTable.config_profile_id == device_tuple[i][8]).all()
                ra_data = sqlalche_obj.session.query(Odu100RaConfTable.raAdminState).filter(
                    Odu100RaConfTable.config_profile_id == device_tuple[i][8]).all()
                sync_data = sqlalche_obj.session.query(Odu100SyncConfigTable.adminStatus).filter(
                    Odu100SyncConfigTable.config_profile_id == device_tuple[i][8]).all()

            if len(ru_data) > 0:
                if ru_data[0][0] == None:
                    ru_state = 1
                    image_ru_title = "RU State UnLocked"
                    image_ru_path = "images/temp/green_dot.png"
                else:
                    if int(ru_data[0][0]) == 0:
                        ru_state = 0
                        image_ru_title = "RU State Locked"
                        image_ru_path = "images/temp/red_dot.png"
                    else:
                        ru_state = 1
                        image_ru_title = "RU State UnLocked"
                        image_ru_path = "images/temp/green_dot.png"
            else:
                ru_state = 1
                image_ru_title = "RU State UnLocked"
                image_ru_path = "images/temp/green_dot.png"
            if len(ra_data) > 0:
                if ra_data[0][0] == None:
                    ra_state = 1
                    image_ra_title = "RA State Unlocked"
                    image_ra_path = "images/temp/green_dot.png"
                else:
                    if int(ra_data[0][0]) == 0:
                        ra_state = 0
                        image_ra_title = "RA State Locked"
                        image_ra_path = "images/temp/red_dot.png"
                    else:
                        ra_state = 1
                        image_ra_title = "RA State Unlocked"
                        image_ra_path = "images/temp/green_dot.png"
            else:
                ra_state = 1
                image_ra_title = "RA State Unlocked"
                image_ra_path = "images/temp/green_dot.png"
            if len(sync_data) > 0:
                if sync_data[0][0] == None:
                    sync_state = 1
                    image_sync_title = " SYNC State Unlocked"
                    image_sync_path = "images/temp/green_dot.png"
                else:
                    if int(sync_data[0][0]) == 0:
                        sync_state = 0
                        image_sync_title = "SYNC State Locked"
                        image_sync_path = "images/temp/red_dot.png"
                    else:
                        sync_state = 1
                        image_sync_title = " SYNC State Unlocked"
                        image_sync_path = "images/temp/green_dot.png"
            else:
                sync_state = 1
                image_sync_title = " SYNC State Unlocked"
                image_sync_path = "images/temp/green_dot.png"

            op_status = essential_obj.get_hoststatus(device_tuple[i][0])
            if op_status == None:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[0]
            elif op_status == 0:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[op_status]
            else:
                op_img = "images/host_status1.png"
                op_title = host_status_dic[op_status]

            if device_tuple[i][7] <= 35:
                images = 'images/new/r-red.png'
            elif device_tuple[i][7] <= 90:
                images = 'images/new/r-black.png'
            else:
                images = 'images/new/r-green.png'

            admin_dic = {'ru_admin': 1 if ru_data[0][0] == None else int(ru_data[0][0]) if len(ru_data) > 0 else 1,
                         'ra_admin': 1 if ra_data[0][0] == None else int(ra_data[0][0]) if len(ra_data) > 0 else 1,
                         'sync_admin': 1 if sync_data[0][0] == None else int(sync_data[0][0]) if len(sync_data) > 0 else 1}
            snmp_up_time_data = sqlalche_obj.db.execute(
                "select trap_event_id from system_alarm_table where host_id='%s' order by timestamp desc limit 1" % (device_tuple[i][0]))
            snmp_up_down_time = ""
            for row in snmp_up_time_data:
                snmp_up_down_time = row['trap_event_id']
            if snmp_up_down_time == "":
                device_status = "Device Unreachable"
                device_status_image_path = "images/temp/red_dot.png"
            elif int(snmp_up_down_time) == 50001:
                device_status = "Device Unreachable"
                device_status_image_path = "images/temp/red_dot.png"
            else:
                device_status = "Device reachable"
                device_status_image_path = "images/temp/green_dot.png"
            if i == len(device_tuple) - 1:
                device_status_host_id += str(device_tuple[i][0])
            else:
                device_status_host_id += str(device_tuple[i][0]) + ","

            monitoring_status = "<a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/info.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile w-reconcile\"/></a>" % ('sp_status_profiling.py',
                                                                                                                                                                                                                                                                      device_tuple[i][0], device_tuple[i][6], device_list_state) if device_tuple[i][6] == "odu100" else "<img src=\"images/new/info1.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile\"/>"
            live_monitoring = "&nbsp;&nbsp;<a target=\"main\" href=\"live_monitoring.py?host_id=%s&device_type=%s\"><img src=\"images/new/star-empty.png\" title=\"Live Monitoring\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" /></a>" % (device_tuple[i][0], device_tuple[i][6])\
                if device_tuple[i][6] == "odu100" else "&nbsp;&nbsp;<img src=\"images/new/star-empty.png\" title=\"Live Monitoring Not Available\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" />"

            device_list.append(
                ["<center><img id=\"device_status\" name=\"device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton w-reconcile\"/></center>&nbsp;&nbsp;" % (device_status_image_path, device_status), device_tuple[i][1], device_tuple[i][2], device_tuple[i][3], device_tuple[i][4], "-" if device_tuple[i][5] == " " else device_tuple[i][5], master_slave, slave_data,
                                "<ul class=\"button_group\" style=\"width:115px;\">\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.ruConfTable.adminstate\" name=\"ru.ruConfTable.adminstate\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.ruConfTable.adminstate')\">RU</a>\
                </li>\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.ra.raConfTable.raAdminState\" name=\"ru.ra.raConfTable.raAdminState\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.ra.raConfTable.raAdminState')\">RA</a>\
                </li>\
                <li>\
                    <a class=\"%s n-reconcile\" id=\"ru.syncClock.syncConfigTable.adminStatus\" name=\"ru.syncClock.syncConfigTable.adminStatus\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','%s','ru.syncClock.syncConfigTable.adminStatus')\">SYNC</a>\
                </li>\
            </ul>"
                                % (
                                    "red" if ru_state == 0 else "green", image_ru_title, ru_state, device_tuple[
                                        i][0], device_tuple[i][6],
                                  "red" if ra_state == 0 else "green", image_ra_title, ra_state, device_tuple[
                                      i][0], device_tuple[i][6],
                                  "red" if sync_state == 0 else "green", image_sync_title, sync_state, device_tuple[i][0], device_tuple[i][6]),
                                "<a target=\"main\">\
            <img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarm\" class=\"imgbutton n-reconcile\"/></a>&nbsp;\
            <a target=\"main\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton n-reconcile\"/ ></a>&nbsp;\
            <img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" state_rec=0\"/>\
            %s&nbsp;%s\
            %s"
                                % (
                                    device_tuple[i][0], 'sp_dashboard_profiling.py' if device_tuple[i][
                                        6] == "odu100" else 'sp_dashboard_profiling.py',
                                    device_tuple[i][
                                        0], device_tuple[
                                            i][
                                                6], device_list_state, device_tuple[i][3],
                                    images, device_tuple[i][7],
                                    live_monitoring, monitoring_status,
                                    "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (device_status_host_id) if i == len(device_tuple) - 1 else ""),
                                "<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\"class=\"imgbutton n-reconcile\"/></center>&nbsp;&nbsp;" % (op_img, op_title)])

        device_dict["aaData"] = device_list

        sqlalche_obj.sql_alchemy_db_connection_close()
        return device_dict
    # try block ends
    # href=\"javascript:apFormwareUpdate('%s','%s','%s');
    # exception starts
    except Exception as e:

        # return device_list
        sqlalche_obj.sql_alchemy_db_connection_close()
        output2 = {
            "sEcho": 1,
            "iTotalRecords": 10,
            "iTotalDisplayRecords": 10,
            "aaData": [],
            "query": str(e)
        }
        return output2
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# Author- Anuj Samariya
# This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
# ip_address - This is the IP Address of device e.g 192.168.0.1
# mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
# selected_device - This is the selected device types from the drop down
# menu of devices e.g "odu16"


def get_device_list_odu_profiling(ip_address, mac_address, selected_device):
    """
    Author- Anuj Samariya
    This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
    ip_address - This is the IP Address of device e.g 192.168.0.1
    mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
    selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
    @param ip_address:
    @param mac_address:
    @param selected_device:
    """
    # This is a empty list variable used for storing the device list
    device_list = []
    device_type = selected_device
    device_list_state = "enabled"
    global sqlalche_obj
    # try block starts
    try:
        # here we create the session of sqlalchemy
        sqlalche_obj.sql_alchemy_db_connection_open()
        # this is the query which returns the multidimensional array of hosts
        # table and store in device_tuple
        device_tuple = sqlalche_obj.session.query(
            Hosts.host_id, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address).filter(and_(Hosts.is_deleted == 0, Hosts.ip_address.like('%s%%' % (ip_address)),
                                                                                                                                 Hosts.mac_address.like('%s%%' % (mac_address)), Hosts.device_type_id == device_type)).order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        total_record = len(device_tuple)

        # this loop create a mutildimesional list of host
        if total_record == 0:
            return 0
        elif total_record > 1:
            return 1
        else:
            return str(device_tuple[0][0])

    # try block ends

    # exception starts
    except Exception as e:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return 2
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]

# odu100 get functions ###################################################


def odu100_get_ipconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    try:
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_ip_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            odu100_ip_conf_table = sqlalche_obj.session.query(
                Odu100IpConfigTable.ipAddress, Odu100IpConfigTable.ipNetworkMask, Odu100IpConfigTable.ipDefaultGateway,
                                                              Odu100IpConfigTable.autoIpConfig).filter(Odu100IpConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_ip_conf_table == None or odu100_ip_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_ip_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]


def odu100_get_omcconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    global sqlalche_obj
    try:
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_omc_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            odu100_omc_conf_table = sqlalche_obj.session.query(
                Odu100OmcConfTable.omcIpAddress, Odu100OmcConfTable.periodicStatsTimer).filter(Odu100OmcConfTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_omc_conf_table == None or odu100_omc_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_omc_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]


def odu100_get_peerconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()

        odu100_profile_id = []
        odu100_peer_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            odu100_peer_conf_table = sqlalche_obj.session.query(
                Odu100PeerConfigTable.peerMacAddress, Odu100PeerConfigTable.guaranteedUplinkBW, Odu100PeerConfigTable.guaranteedDownlinkBW, Odu100PeerConfigTable.basicrateMCSIndex,
                                                                Odu100PeerConfigTable.maxUplinkBW, Odu100PeerConfigTable.maxDownlinkBW).filter(Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_peer_conf_table == None or odu100_peer_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_peer_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]


def odu100_get_aclconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_acl_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            odu100_acl_conf_table = sqlalche_obj.session.query(Odu100RaAclConfigTable.aclIndex, Odu100RaAclConfigTable.macaddress, Odu100RaAclConfigTable.odu100_raAclConfigTable_id, Odu100RaAclConfigTable.raIndex).filter(
                Odu100RaAclConfigTable.config_profile_id == odu100_profile_id[0]).order_by(Odu100RaAclConfigTable.aclIndex).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_acl_conf_table == None or odu100_acl_conf_table == [] or len(odu100_acl_conf_table) == 0:
            return {"success": 1, "result": [], "detail": ""}
        else:
            return {"success": 0, "result": odu100_acl_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()

# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]


def odu100_get_raconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_ra_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            odu100_ra_conf_table = sqlalche_obj.session.query(
                Odu100RaConfTable.numSlaves, Odu100RaConfTable.ssID, Odu100RaConfTable.acm, Odu100RaConfTable.dba,
                                                              Odu100RaConfTable.guaranteedBroadcastBW, Odu100RaConfTable.acs, Odu100RaConfTable.dfs, Odu100RaConfTable.aclMode, Odu100RaConfTable.antennaPort,
                                                              Odu100RaConfTable.linkDistance, Odu100RaConfTable.anc, Odu100RaConfTable.forceMimo).filter(Odu100RaConfTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_ra_conf_table == None or odu100_ra_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_ra_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]


def odu100_get_tddmacconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_tddmac_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            odu100_tddmac_conf_table = sqlalche_obj.session.query(
                Odu100RaTddMacConfigTable.encryptionType, Odu100RaTddMacConfigTable.passPhrase, Odu100RaTddMacConfigTable.txPower,
                                                                  Odu100RaTddMacConfigTable.maxCrcErrors, Odu100RaTddMacConfigTable.leakyBucketTimerValue).filter(Odu100RaTddMacConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_tddmac_conf_table == None or odu100_tddmac_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_tddmac_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]


def odu100_get_ruconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_ru_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_ru_conf_table = sqlalche_obj.session.query(
                Odu100RuConfTable.channelBandwidth, Odu100RuConfTable.synchSource, Odu100RuConfTable.countryCode,
                                                              Odu100RuConfTable.poeState, Odu100RuConfTable.alignmentControl, Odu100RuConfTable.defaultNodeType, Odu100RuConfTable.ethFiltering).filter(Odu100RuConfTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_ru_conf_table) == 0:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_ru_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]
def odu100_get_llcconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_llc_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_llc_conf_table = sqlalche_obj.session.query(Odu100RaLlcConfTable).filter(
                Odu100RaLlcConfTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_llc_conf_table) == 0:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_llc_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_ip_packet_table(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_ip_filter_table = sqlalche_obj.session.query(
            Odu100IpFilterTable).filter(Odu100IpFilterTable.host_id == host_id).all()
        return {"success": 0, "result": odu100_ip_filter_table}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def totalPacketIpMAC(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_mac_result = sqlalche_obj.session.query(Odu100MacFilterTable.filterMacAddress).filter(
            and_(Odu100MacFilterTable.host_id == host_id, Odu100MacFilterTable.filterMacAddress != "")).all()
        odu100_ip_result = sqlalche_obj.session.query(Odu100IpFilterTable.ipFilterIpAddress).filter(
            and_(Odu100IpFilterTable.host_id == host_id, Odu100IpFilterTable.ipFilterIpAddress != "")).all()
        return {"success": 0, "ip_result": odu100_ip_result, "mac_result": odu100_mac_result}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_mac_packet_table(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_mac_filter_table = sqlalche_obj.session.query(
            Odu100MacFilterTable).filter(Odu100MacFilterTable.host_id == host_id).all()
        return {"success": 0, "result": odu100_mac_filter_table}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_get_sysconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_sys_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_sys_conf_table = sqlalche_obj.session.query(Odu100SysOmcRegistrationTable).filter(
                Odu100SysOmcRegistrationTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_sys_conf_table) == 0:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_sys_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# Author - Anuj Samariya
# This function is used to get the data from database of odu100 ip configuration
# host_id - this id is used to get the specific config profile id i.e. config_profile_id
# return the ip configuration table data [type - tuple]
def odu100_get_syncconfigtable(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_sync_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_sync_conf_table = sqlalche_obj.session.query(
                Odu100SyncConfigTable.rasterTime, Odu100SyncConfigTable.syncLossThreshold, Odu100SyncConfigTable.leakyBucketTimer,
                                                                Odu100SyncConfigTable.syncLostTimeout, Odu100SyncConfigTable.syncConfigTimerAdjust, Odu100SyncConfigTable.percentageDownlinkTransmitTime).filter(Odu100SyncConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_sync_conf_table == None or odu100_sync_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_sync_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": ""}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": ""}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": ""}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": ""}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": ""}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_get_channelConfig(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_channel_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_channel_conf_table = sqlalche_obj.session.query(Odu100RaPreferredRFChannelTable.rafrequency).filter(
                Odu100RaPreferredRFChannelTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if odu100_channel_conf_table == None or odu100_channel_conf_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": odu100_channel_conf_table, "detail": ""}

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": str(e)}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": str(e)}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e)}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": str(e)}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": str(e)}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": str(e)}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": str(e)}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": str(e)}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": str(e)}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_get_status(host_id, class_name, time_stamp=0):
    """

    @param host_id:
    @param class_name:
    @param time_stamp:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        if host_id == "" or host_id == None:
            return []
        if time_stamp == 0:
            exec "get_data = sqlalche_obj.session.query(%s).filter(%s.host_id==%s).all()" % (
                class_name, class_name, host_id)
        else:
            exec "get_data = sqlalche_obj.session.query(%s).filter(%s.host_id==%s).order_by(desc(%s.timestamp)).limit(1).all()" % (
                class_name, class_name, host_id, class_name)
        if len(get_data) > 0:
            return get_data
        else:
            return []
    except Exception as e:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return str(e)
    finally:
        pass
        sqlalche_obj.sql_alchemy_db_connection_close()

# print odu100_get_status(39,'Odu100StatusTable',0)


def acl_edit_bind(uuid):
    """

    @param uuid:
    @return:
    """
    try:
        global sqlalche_obj
        dic_result = {"success": 0, "result": {}}
        sqlalche_obj.sql_alchemy_db_connection_open()
        # odu100_acl_edit_data = {"success":0,"result":{}}
        odu100_acl_edit_data = sqlalche_obj.session.query(
            Odu100RaAclConfigTable.aclIndex, Odu100RaAclConfigTable.macaddress,
                                                          Odu100RaAclConfigTable.config_profile_id).filter(Odu100RaAclConfigTable.odu100_raAclConfigTable_id == uuid).all()
        odu100_ra_conf_data = sqlalche_obj.session.query(Odu100RaConfTable.aclMode).filter(
            Odu100RaConfTable.config_profile_id == odu100_acl_edit_data[0][2]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        dic_result = {"success": 0, "result": {}}
        dic_result["result"]["aclIndex"] = str(odu100_acl_edit_data[0][0])
        dic_result["result"]["macaddress"] = odu100_acl_edit_data[0][1]
        dic_result["result"]["aclMode"] = str(odu100_ra_conf_data[0][0])
        return dic_result
    except Exception as e:
        return str(e[-1])
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def select_table_prefix(device_type_id):
    """

    @param device_type_id:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        table_prefix = sqlalche_obj.session.query(
            DeviceType.table_prefix).filter(DeviceType.device_type_id == device_type_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if table_prefix == None or table_prefix == "":
            return {"result": "Device Not Selected", "success": 0}
        else:
            return {"result": str(table_prefix[0].table_prefix), "success": 1}
    except Exception as e:
        return {"result": str(e[-1]), "success": 1}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# odu100 select list#########################################################
# Author - Anuj Samariya
# This class is used to make the select list of odu100 forms
class MakeOdu100SelectListWithDic(object):
    """
    Author - Anuj Samariya
    This class is used to make the select list of odu100 forms
    """

    # Author - Anuj Samariya
    # This function is used to create the select list of channel bandwidth of RU Configuration form
    # self - It denotes the class object[Type -MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def channel_bandwidth_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of channel bandwidth of RU Configuration form
        self - It denotes the class object [Type -MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list

        channel_bandwidth_select_list_name_value_dic = {'name': ['5', '10', '20', '40',
            '40 Short GI'], 'value': ['0', '1', '2', '3', '4']}
        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(channel_bandwidth_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of channel bandwidth of RU Configuration form
    # self - It denotes the class object[Type -MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def packet_filter_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of channel bandwidth of RU Configuration form
        self - It denotes the class object [Type -MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list

        packet_filter_select_list_name_value_dic = {'name': [
            'Disable', 'IP Filter', 'MAC Filter'], 'value': ['0', '1', '2']}

        # logme("Dev Debug: %s" %
        # (str(selected_field)+'","'+str(selected_list_state)+'","'+str(selected_list_id)+'","'+str(is_readonly)+'","'+str(select_list_initial_msg)))

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(packet_filter_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of channel bandwidth of RU Configuration form
    # self - It denotes the class object [Type - MakeOdu100SelectListWithDic]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def sync_source_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of channel bandwidth of RU Configuration form
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """
        # this dictionary is used to store the name and value of select list

        sync_source_select_list_name_value_dic = {'name': [
            'Internal clock (0)', 'Radio 1 (1)', 'External (3)'], 'value': ['0', '1', '3']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(sync_source_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of channel bandwidth of RU Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def country_code_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of channel bandwidth of RU Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - Boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """
        # this dictionary is used to store the name and value of select list

        country_code_select_list_name_value_dic = {'name': ['DBG(0)', 'Denmark(208)', 'India(356)', 'Sweden(752)', 'USA(840)'],
                                                                 'value': ['0', '208', '356', '752', '840']}

        # call the function of common_controller
        # country_code_select_list_name_value_dic - This store the name and value of select list
        # This returns the select list string in html format

        return make_select_list_using_dictionary(country_code_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of channel bandwidth of RU Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def poe_state_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of channel bandwidth of RU Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """
        # this dictionary is used to store the name and value of select list

        poe_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(poe_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def poe_state_select_list_cpu(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of channel bandwidth of RU Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """
        # this dictionary is used to store the name and value of select list

        poe_state_select_list_name_value_dic = {'name': [
            'Not Applicable'], 'value': ['2']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(poe_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of timeslot of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def timeslot_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of timeslot of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        timeslot_total_select_name_value = 16

        # this dictionary is used to store the name and value of select list
        timeslot_select_list_name_value_dic = {}

        for i in range(0, timeslot_total_select_name_value):
            if i == 0:
                timeslot_select_list_name_value_dic.setdefault(
                    'name', []).append(str(i + 1) + " Timeslot(T1/T2)")
                timeslot_select_list_name_value_dic.setdefault(
                    'value', []).append(i + 1)
            else:
                timeslot_select_list_name_value_dic.setdefault(
                    'name', []).append(str(i + 1) + " Timeslot(T2)")
                timeslot_select_list_name_value_dic.setdefault(
                    'value', []).append(i + 1)

        return make_select_list_using_dictionary(timeslot_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of encryption of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def encryption_type_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of encryption  of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list

        encryption_type_select_list_name_value_dic = {'name': [
            'None', 'AES'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(encryption_type_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of acm of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def acm_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acm  of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        acm_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(acm_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of acm of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def anc_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acm  of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        acm_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(acm_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def forcemimo_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of forcemimo  of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        forcemimo_state_select_list_name_value_dic = {'name': [
            'Disable', 'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(forcemimo_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of dba of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def dba_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of dba  of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        dba_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(dba_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of acs of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def acs_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acs of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        acs_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(acs_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of acs of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def ans_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acs of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        ans_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable'], 'value': ['0', '1']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(ans_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of dfs of RA Configuration form
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def dfs_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of dfs of RA Configuration form
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes tclass MakeOdu100SelectListWithDic(object):hat the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        dfs_state_select_list_name_value_dic = {'name': ['Disable',
            'Enable', 'NA'], 'value': ['0', '1', '2']}

        # call the function of common_controller
        # This returns the select list string in html format
        return make_select_list_using_dictionary(dfs_state_select_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of Preffered Channel List
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def default_preffered_channel_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        for i in range(0, 10):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(0)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(0)

        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def preffered_channel_select_list10(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        for i in range(5180, 5241, 5):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5260, 5321, 5):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5745, 5886, 5):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)

        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def preffered_channel_select_list20(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        for i in range(5180, 5321, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5500, 5701, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5745, 5826, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)

        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def preffered_channel_select_list40(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        for i in range(5180, 5321, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5745, 5826, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5835, 5876, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)

        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of Preffered Channel List
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def preffered_channel_select_list2(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        for i in range(5180, 5321, 5):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5745, 5886, 5):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)

        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of DHCP Channel List
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def preffered_channel_select_list2(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        for i in range(5180, 5321, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5745, 5826, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)
        for i in range(5735, 5876, 20):
            preffered_channel_list_name_value_dic.setdefault(
                'name', []).append(i)
            preffered_channel_list_name_value_dic.setdefault(
                'value', []).append(i)

        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def preffered_channel_select_list_snmp(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """
        global preferred_channel_dic
        # this dictionary is used to store the name and value of select list

        return make_select_list_using_dictionary(preferred_channel_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def preffered_channel_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg, host_id, selected_device):
        """
        Author - Anuj Samariya
        This function is used to create the select list of preffered_channel_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @param host_id:
        @param selected_device:
        """

        # this dictionary is used to store the name and value of select list
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        channel_list = sqlalche_obj.session.query(
            Odu100RaChannelListTable).filter(Odu100RaChannelListTable.host_id == host_id).all()
        preffered_channel_list_name_value_dic = {}
        preffered_channel_list_name_value_dic.setdefault('name', []).append(0)
        preffered_channel_list_name_value_dic.setdefault('value', []).append(0)
        if len(channel_list) > 0:

            for i in range(0, len(channel_list)):
                preffered_channel_list_name_value_dic.setdefault(
                    'name', []).append(channel_list[i].frequency)
                preffered_channel_list_name_value_dic.setdefault(
                    'value', []).append(channel_list[i].frequency)

        else:

            host_data = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            # return host_data
            preferred_channel_list = sqlalche_obj.session.query(Odu100RaPreferredRFChannelTable).filter(
                Odu100RaPreferredRFChannelTable.config_profile_id == host_data[0].config_profile_id).all()
            for i in range(0, len(preferred_channel_list)):
                preffered_channel_list_name_value_dic.setdefault(
                    'name', []).append(preferred_channel_list[i].rafrequency)
                preffered_channel_list_name_value_dic.setdefault(
                    'value', []).append(preferred_channel_list[i].rafrequency)
        sqlalche_obj.sql_alchemy_db_connection_close()
        return make_select_list_using_dictionary(preffered_channel_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of DHCP Channel List
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format
    def dhcp_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of DHCP channel list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        dhcp_select_list_using_dictionary = {'name': ['DISABLE',
            'ENABLE'], 'value': ['0', '1']}

        return make_select_list_using_dictionary(dhcp_select_list_using_dictionary, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    # Author - Anuj Samariya
    # This function is used to create the select list of Acl Select List
    # self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
    # selected_field - This denotes the selected field in select list [type - string]
    # selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
    # selected_list_id - This denotes the select list id [type - string]
    # is_readonly - This denotes that the select list value is only readable not writable [type -boolean]
    # select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
    # return the select list string in html format

    def acl_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of ACL Select list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        acl_select_list_using_dictionary = {'name': ['Disable',
            'Accept', 'Deny'], 'value': ['0', '1', '2']}

        return make_select_list_using_dictionary(acl_select_list_using_dictionary, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def acl_index_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg, host_id):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acl_index_select_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @param host_id:
        """

        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        firmware_result = sqlalche_obj.session.query(
            Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
        if len(firmware_result):
            firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
            if firmware == "7.2.20":
                acl_index_len = 200
            elif firmware == "7.2.25":
                acl_index_len = 32
            else:
                acl_index_len = 32
        else:
            acl_index_len = 200
        sqlalche_obj.sql_alchemy_db_connection_close()

        # this dictionary is used to store the name and value of select list
        acl_index_list_name_value_dic = {}

        for i in range(0, acl_index_len):
            acl_index_list_name_value_dic.setdefault('name', []).append(i + 1)
            acl_index_list_name_value_dic.setdefault('value', []).append(i + 1)

        return make_select_list_using_dictionary(acl_index_list_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def antenna_port_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acl_index_select_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        # this dictionary is used to store the name and value of select list

        antenna_name_value_dic = {'name': ['Port1', 'Port2',
            'MIMO'], 'value': ['1', '2', '3']}

        return make_select_list_using_dictionary(antenna_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def raster_time_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acl_index_select_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        raster_time_name_value_dic = {'name': ['2', '4'], 'value': ['2', '4']}
        return make_select_list_using_dictionary(raster_time_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

    def mcs_index_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg, attr={}):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acl_index_select_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @param attr:
        """
        mcs_index_name_value_dic = {}
        for i in range(0, 9):
            if i == 0:
                mcs_index_name_value_dic.setdefault('name', []).append(-1)
                mcs_index_name_value_dic.setdefault('value', []).append(-1)
            else:
                mcs_index_name_value_dic.setdefault('name', []).append(i - 1)
                mcs_index_name_value_dic.setdefault('value', []).append(i - 1)
##        else:
##            for i in range(0,9):
##                if i==0:
##                    mcs_index_name_value_dic.setdefault('name',[]).append(-1)
##                    mcs_index_name_value_dic.setdefault('value',[]).append(-1)
##                else:
##                    mcs_index_name_value_dic.setdefault('name',[]).append(i-1)
# mcs_index_name_value_dic.setdefault('value',[]).append(i-1)
        return make_select_list_using_dictionary(mcs_index_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg, attr)

    def mcs_index_select_list_mimo(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg, attr={}):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acl_index_select_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @param attr:
        """
        mcs_index_name_value_dic = {}

        for i in range(0, 17):
            if i == 0:
                mcs_index_name_value_dic.setdefault('name', []).append(-1)
                mcs_index_name_value_dic.setdefault('value', []).append(-1)
            else:
                mcs_index_name_value_dic.setdefault('name', []).append(i - 1)
                mcs_index_name_value_dic.setdefault('value', []).append(i - 1)
##        else:
##            for i in range(0,17):
##                if i==0:
##                    mcs_index_name_value_dic.setdefault('name',[]).append(-1)
##                    mcs_index_name_value_dic.setdefault('value',[]).append(-1)
##                else:
##                    mcs_index_name_value_dic.setdefault('name',[]).append(i-1)
# mcs_index_name_value_dic.setdefault('value',[]).append(i-1)
        return make_select_list_using_dictionary(mcs_index_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg, attr)

    def link_distance_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg):
        """
        Author - Anuj Samariya
        This function is used to create the select list of acl_index_select_list
        self - It denotes the class object[Type - MakeOdu100SelectListWithDic ]
        selected_field - This denotes the selected field in select list [type - string]
        selected_list_state - This denotes that the list type e.g enable ,disable [type - string]
        selected_list_id - This denotes the select list id [type - string]
        is_readonly - This denotes that the select list value is only readable not writable [type - boolean]
        select_list_initial_msg - This denotes the initial msg show on select list when the list is view means which msg is shown on list when no element is selected initially [type - string]
        return the select list string in html format
        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        """

        link_distance_name_value_dic = {'name': ['UPTO 20',
            'GT 20'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(link_distance_name_value_dic, selected_field, selected_list_state, selected_list_id, is_readonly, select_list_initial_msg)

# odu100 set functions ###################################################


def rename_tablename(tablename):
    """

    @param tablename:
    @return:
    """
    try:
        ss = ""
        idx = tablename.index("_")
        ss = tablename[0:idx] + tablename[idx + 1].upper() + \
                                                         tablename[
                                                             idx + 1 + 1:]
        ss = ss[0].upper() + ss[1:]
        return ss
    except Exception as e:
        return 1


def get_firmware_version(host_id):
    """

    @param host_id:
    @return:
    """
    output_dict = {'success': 0}
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        output_dict = {'success': 0}
        firmware_result = sqlalche_obj.session.query(
            Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
        if len(firmware_result):
            output_dict['output'] = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
    except:
        output_dict['success'] = 1
        output_dict['output'] = str(e[-1])
    finally:
        return output_dict
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_set_config(host_id, device_type_id, dic_result):
    # dic_result =
    # {'success':0,'result':{'ru.omcConfTable.omcIpAddress':[1,'Not
    # Done'],'ru.omcConfTable.periodicStatsTimer':[1,'Not Done']}}
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        success_result = {"success": '', "result": {}}
        global errorStatus
        rowSts = {'ru.ra.raAclConfigTable.rowSts': [
            '1.3.6.1.4.1.26149.2.2.13.5.1.3', 'Integer32', '']}
        query_result = []
        oid_admin_state = {"1": -1}
        independent_oid = []
        dependent_oid = []
        depend_oid_value = []

        key = ""
        firmware_result = sqlalche_obj.session.query(
            Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
        if len(firmware_result):
            firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
            if firmware == '7.2.29':
                Oids = aliased(Odu1007_2_29_oids)
                table_name = "odu100_7_2_29_oids"
            elif firmware == '7.2.25':
                Oids = aliased(Odu1007_2_25_oids)
                table_name = "odu100_7_2_25_oids"
            else:
                Oids = aliased(Odu1007_2_20_oids)
                table_name = "odu100_7_2_20_oids"
        else:
            Oids = aliased(Odu1007_2_20_oids)
            table_name = "odu100_7_2_20_oids"

        # Create the alias
        o1 = aliased(Oids)
        o2 = aliased(Oids)
        oid_dic_value_list = []
        pass_counter = 1
        ra = 0
        for keys in dic_result.iterkeys():
            oid_dic_value_list.append(str(keys) + str(ra))
            ra += 1
            if keys == "success":
                continue
            else:
                query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                    o1, o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                if len(query_result) > 0:
                    if query_result[0][0].dependent_id == "" or query_result[0][0].dependent_id is None:
                        independent_oid.append({keys: [query_result[0][0].oid + query_result[0][0]
                                               .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                    else:
                        if len(dependent_oid) > 0:
                            for i in range(0, len(dependent_oid)):
                                if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                    admin_state = 'ru.ruConfTable.adminstate'
                                elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                    admin_state = 'ru.ipConfigTable.adminState-1'
                                elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                    admin_state = 'ru.ra.raConfTable.raAdminState-1'
                                else:
                                    admin_state = query_result[0][1]
                                if admin_state in dependent_oid[i]:
                                    pos = i
                                    if len(depend_oid_value) > 0:
                                        depend_oid_value[pos][keys] = [query_result[0][0].oid +
                                            query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]
                                        break
                                    else:
                                        depend_oid_value.append({keys: [query_result[0][0].oid +
                                                                query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                        break
                                else:
                                    if i == len(dependent_oid) - 1:
                                        if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                            dependent_oid.append({query_result[0][1] + str(
                                                -1): [query_result[0][2] + query_result[0][3]]})
                                            depend_oid_value.append(
                                                {keys: [
                                                    query_result[0][0].oid +
                                                        query_result[
                                                            0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                        elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                            dependent_oid.append({query_result[0][1] + str(
                                                -1): [query_result[0][2] + query_result[0][3]]})
                                            depend_oid_value.append(
                                                {keys: [
                                                    query_result[0][0].oid +
                                                        query_result[
                                                            0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                        elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                            dependent_oid.append({query_result[0][1] + str(
                                                -1): [query_result[0][2] + query_result[0][3]]})
                                            depend_oid_value.append(
                                                {keys: [
                                                    query_result[0][0].oid +
                                                        query_result[
                                                            0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                        else:
                                            dependent_oid.append(
                                                {query_result[0][1]: [query_result[0][2] + query_result[0][3]]})
                                            depend_oid_value.append(
                                                {keys: [
                                                    query_result[0][0].oid +
                                                        query_result[
                                                            0][0].indexes,
                                                                    query_result[0][0].oid_type, dic_result[keys]]})
                                    else:
                                        continue
                        else:
                            if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                dependent_oid.append({query_result[0][1] + str(
                                    -1): [query_result[0][2] + query_result[0][3]]})
                                depend_oid_value.append({keys: [query_result[0][0].oid +
                                                        query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                            elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                dependent_oid.append({query_result[0][1] + str(
                                    -1): [query_result[0][2] + query_result[0][3]]})
                                depend_oid_value.append({keys: [query_result[0][0].oid +
                                                        query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                            elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                dependent_oid.append({query_result[0][1] + str(
                                    -1): [query_result[0][2] + query_result[0][3]]})
                                depend_oid_value.append({keys: [query_result[0][0].oid +
                                                        query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                            else:
                                dependent_oid.append({query_result[
                                                     0][1]: [query_result[0][2] + query_result[0][3]]})
                                depend_oid_value.append({keys: [query_result[0][0].oid +
                                                        query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                else:
                    success_result["success"] = 1
                    success_result["result"] = "There is no row in database"

        pos = len(depend_oid_value)
        if pos != 0:
            for i in range(0, len(independent_oid)):
                depend_oid_value[pos - 1].update(independent_oid[i])
        else:
            for i in range(0, len(independent_oid)):
                depend_oid_value.append(independent_oid[i])
        device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id).\
            filter(Hosts.host_id == host_id).one()
        j = -1
        if len(dependent_oid) > 0:
            for i in range(0, len(dependent_oid)):
                j += 1
                # print depend_oid_value[i]
                # ,'-------=++++++++++',dependent_oid[i],'depend_oid_value for
                # %s '%i
                if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                    result = (
                        pysnmp_set(depend_oid_value[i], device_param_list[0],
                              device_param_list[1], device_param_list[2], dependent_oid[i]))
                elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                    result = (
                        pysnmp_set(depend_oid_value[i], device_param_list[0],
                              device_param_list[1], device_param_list[2], dependent_oid[i]))
                elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                    result = (
                        pysnmp_set(depend_oid_value[i], device_param_list[0],
                              device_param_list[1], device_param_list[2], dependent_oid[i]))
                else:
                    result = pysnmp_set(
                        depend_oid_value[i], device_param_list[0],
                                        device_param_list[1], device_param_list[2], dependent_oid[i])
                if result["success"] == 0 or result["success"] == '0':
                    # print
                    # result["result"],'??????????????????/((((((((((())))))))',success_result
                    success_result["success"] = result["success"]
                    for i in result["result"]:
                        if result["result"][i] != 0:
                            result["result"][
                                i] = errorStatus[result["result"][i]]
                        else:
                            oid_list_table_field_value = sqlalche_obj.session.query(
                                Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == i, Oids.device_type_id == device_type_id)).all()
                            if len(oid_list_table_field_value) == 0:
                                continue
                            else:
                                if i in dic_result:
                                    table_name = "odu100_" + \
                                        oid_list_table_field_value[0][0]
                                    table_name = rename_tablename(table_name)
                                    exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                        table_name, table_name, device_param_list[3])
                                    exec "table_result[0].%s = '%s'" % (
                                        oid_list_table_field_value[0][1], dic_result[i])
                                    if ("odu100_" + oid_list_table_field_value[0][0]) == "odu100_ipConfigTable":
                                        host_data = sqlalche_obj.session.query(Hosts).filter(
                                            Hosts.config_profile_id == device_param_list[3]).all()
                                        if i == "ru.ipConfigTable.ipAddress":
                                            host_data[
                                                0].ip_address = dic_result[i]
                                        if i == "ru.ipConfigTable.ipNetworkMask":
                                            host_data[
                                                0].netmask = dic_result[i]
                                        if i == "ru.ipConfigTable.ipDefaultGateway":
                                            host_data[
                                                0].gateway = dic_result[i]
                                    sqlalche_obj.session.commit()
                    success_result["result"].update(result["result"])
                else:
                    success_result["success"] = 1
                    for i in result["result"]:
                        i in errorStatus
                        success_result[
                            "result"] = errorStatus.get(i, "SNMP Agent Down")

        if len(dependent_oid) > 0:
            for i in range(0, len(dependent_oid)):
                query_admin_result = sqlalche_obj.session.query(
                    Oids.oid, Oids.oid_type, Oids.indexes).filter(Oids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                    oid_list_table_field_value = []
                    table_name = ""
                    admin_state = "ru.ruConfTable.adminstate"
                    query_admin_result = sqlalche_obj.session.query(
                        Oids.oid, Oids.oid_type, Oids.indexes).filter(Oids.oid_name == "ru.ruConfTable.adminstate").one()
                    result_admin = {}
                    dic_admin_value = {"ru.ruConfTable.adminstate": [
                        query_admin_result[0] + query_admin_result[2], query_admin_result[1], '1']}
                    if len(query_admin_result) > 0:
                        result_admin = pysnmp_set(dic_admin_value, device_param_list[
                                                  0], device_param_list[1], device_param_list[2])
                        oid_list_table_field_value = sqlalche_obj.session.query(Oids.table_name, Oids.coloumn_name).filter(
                            and_(Oids.oid_name == "ru.ruConfTable.adminstate", Oids.device_type_id == device_type_id)).all()
                        if len(oid_list_table_field_value) != 0:
                            table_name = "odu100_" + \
                                oid_list_table_field_value[0][0]
                            table_name = rename_tablename(table_name)
                            exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                table_name, table_name, device_param_list[3])
                        if result_admin["success"] == 0 or result_admin["success"] == '0':
                            result_admin['success'] = 0
                            exec "table_result[0].%s = '%s'" % (
                                oid_list_table_field_value[0][1], 1)
                            # success_result["result"].update(result["result"])
                        else:
                            exec "table_result[0].%s = '%s'" % (
                                oid_list_table_field_value[0][1], 1)
                            for i in result_admin["result"]:
                                if i == 553:
                                    result_admin["result"] = str(errorStatus.get(
                                        i, "SNMP agent Unknown Error Occured"))
                                elif i == 551:
                                    result_admin["result"] = str(errorStatus.get(
                                        i, "SNMP agent Unknown Error Occured"))
                                elif result_admin["result"][i] != 0:
                                    result_admin["result"] = str(
                                        errorStatus.get(result_admin["result"][i], "SNMP agent Unknown Error Occured"))
                            result_admin['success'] = 1
                        result_admin[
                            'admin_name'] = 'ru.ruConfTable.adminstate'
                        success_result['result_admin'] = result_admin

                elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                    query_admin_result = sqlalche_obj.session.query(
                        Oids.oid, Oids.oid_type, Oids.indexes).filter(Oids.oid_name == "ru.ipConfigTable.adminState").one()
                    dic_admin_value = {"ru.ipConfigTable.adminState": [
                        query_admin_result[0] + query_admin_result[2], query_admin_result[1], '1']}
                    if len(query_admin_result) > 0:
                        result = pysnmp_set(
                            dic_admin_value, device_param_list[0],
                                            device_param_list[1], device_param_list[2])
                        if result["success"] == 0 or result["success"] == '0':
                            success_result["success"] = result["success"]
                            for i in result["result"]:
                                if result["result"][i] != 0:
                                    result["result"][
                                        i] = errorStatus[result["result"][i]]
                                else:
                                    oid_list_table_field_value = sqlalche_obj.session.query(
                                        Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == i, Oids.device_type_id == device_type_id)).all()
                                    if len(oid_list_table_field_value) == 0:
                                        continue
                                    else:
                                        if i in dic_result:

                                            table_name = "odu100_" + \
                                                oid_list_table_field_value[
                                                    0][0]
                                            table_name = rename_tablename(
                                                table_name)
                                            exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                table_name, table_name, device_param_list[3])
                                            exec "table_result[0].%s = '%s'" % (
                                                oid_list_table_field_value[0][1], dic_result[i])
                            # success_result["result"] =
                            # errorStatus[result["result"][i]]
                        else:
                            # success_result["success"] = 1
                            for i in result["result"]:
                                result["result"][i] in errorStatus
                                # success_result["result"] =
                                # errorStatus[result["result"][i]]
                elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                    query_admin_result = sqlalche_obj.session.query(
                        Oids.oid, Oids.oid_type, Oids.indexes).filter(Oids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                    dic_admin_value = {"ru.ra.raConfTable.raAdminState": [
                        query_admin_result[0] + query_admin_result[2], query_admin_result[1], '1']}
                    if len(query_admin_result) > 0:
                        result_admin = {'success': 0}
                        result_admin = pysnmp_set(dic_admin_value, device_param_list[
                                                  0], device_param_list[1], device_param_list[2])
                        # return result_admin
                        oid_list_table_field_value = sqlalche_obj.session.query(
                            Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == "ru.ra.raConfTable.raAdminState", Oids.device_type_id == device_type_id)).all()
                        table_name = "odu100_" + \
                            oid_list_table_field_value[0][0]
                        table_name = rename_tablename(table_name)
                        if result_admin["success"] == 0 or result_admin["success"] == '0':
                            if len(oid_list_table_field_value) != 0:
                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                    table_name, table_name, device_param_list[3])
                                exec "table_result[0].%s = '%s'" % (
                                    oid_list_table_field_value[0][1], 1)

                        else:
                            # edit by yogesh - to resolve some name error occur
                            # exec "table_result[0].%s =
                            # '%s'"%(oid_list_table_field_value[0][1],0)
                            for i in result_admin["result"]:
                                if i == 553:
                                    result_admin["result"] = str(errorStatus.get(
                                        i, "SNMP agent Unknown Error Occured"))
                                elif i == 551:
                                    result_admin["result"] = str(errorStatus.get(
                                        i, "SNMP agent Unknown Error Occured"))
                                elif result_admin["result"][i] != 0:
                                    result_admin["result"] = str(
                                        errorStatus.get(result_admin["result"][i], "SNMP agent Unknown Error Occured"))
                            result_admin['success'] = 1
                        result_admin[
                            'admin_name'] = 'ru.ra.raConfTable.raAdminState'
                        success_result['result_admin'] = result_admin
                    break
                else:
                    continue
        pass_counter = ""
        if(j == -1):
            if len(depend_oid_value) > 0:
                break_found = 0
                fail_result = 'Unknown error'
                for k in range(0, len(depend_oid_value)):
                    pysnm_result = pysnmp_set(
                        depend_oid_value[k], device_param_list[0],
                                              device_param_list[1], device_param_list[2])
                    if pysnm_result["success"] == 0 or pysnm_result["success"] == '0':
                        success_result["success"] = pysnm_result["success"]
                        for i in pysnm_result["result"]:
                            if pysnm_result["result"][i] != 0:
                                pysnm_result["result"][
                                    i] = errorStatus[pysnm_result["result"][i]]
                            else:
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == i, Oids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                else:
                                    if i in dic_result:
                                        table_name = "odu100_" + \
                                            oid_list_table_field_value[0][0]
                                        table_name = rename_tablename(
                                            table_name)
                                        exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                            table_name, table_name, device_param_list[3])
                                        exec "table_result[0].%s = '%s'" % (
                                            oid_list_table_field_value[0][1], dic_result[i])
                        success_result["result"].update(pysnm_result["result"])
                    else:
                        if "success" in success_result and success_result["success"] == 0:
                            pass
                        else:
                            success_result["success"] = 1

                        fail_dic = {}
                        fail_result = ''
                        for i in pysnm_result["result"]:
                            if i == 553:
                                fail_result = str(errorStatus.get(
                                    i, "SNMP agent Unknown Error Occured"))
                            elif i == 551:
                                fail_result = str(errorStatus.get(
                                    i, "SNMP agent Unknown Error Occured"))
                            else:
                                if pysnm_result["result"][i] > 95:
                                    fail_result = errorStatus.get(
                                        pysnm_result["result"][i], "Device is not respoding")
                        if len(fail_result) > 0:
                            break_found = 1
                            break
                        for j in depend_oid_value[k]:
                            if j in pysnm_result["result"]:
                                fail_dic[j] = str(errorStatus.get(
                                    pysnm_result["result"][j], "SNMP agent Unknown Error Occured"))
                            else:
                                fail_dic[j] = fail_result
                        success_result["result"].update(fail_dic)
                if break_found and success_result['success'] == 0:
                    for k in depend_oid_value:
                        if k in success_result['result']:
                            pass
                        else:
                            success_result['result'].update({k: fail_result})
                elif break_found and success_result['success'] == 1:
                    success_result['result'] = fail_result
                elif success_result['success'] == 1 and isinstance(success_result['result'], dict):
                    if len(success_result['result']) == 1:
                        success_result[
                            'result'] = success_result['result'].values()[0]
                    else:
                        success_result['success'] = 0

        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return success_result

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        import traceback
        print traceback.format_exc()
        return {"success": 1, "result": "Configuration failed.Please try again later", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Configuration failed.Please try again later", "detail": str(e)}
        import traceback
        print traceback.format_exc()
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()

# raju
# dic = {'ru.ra.raConfTable.antennaPort': '3', 'ru.ra.raConfTable.dfs': '2', 'ru.ra.raConfTable.dba': '0', 'ru.ra.tddMac.raTddMacConfigTable.passPhrase': '', 'ru.ra.raConfTable.numSlaves': '4', 'ru.ra.tddMac.raTddMacConfigTable.encryptionType': '0', 'ru.ra.raConfTable.guaranteedBroadcastBW': '1', 'ru.ra.raConfTable.anc': '1', 'ru.ra.raConfTable.ssID': '', 'ru.ra.raConfTable.linkDistance': '0', 'ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue': '11', 'ru.ra.raConfTable.acm': '1', 'ru.ra.tddMac.raTddMacConfigTable.txPower': '24', 'ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors': '40', 'ru.ra.raConfTable.acs': '0'}
# dic = {'ru.ra.llc.raLlcConfTable.frameLossTimeout': '0'}
# dic = {'ru.ruConfTable.ethFiltering': '1'}
# print 'aha'
# print odu100_set_config(14,'odu100',dic)


def controller_validation(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    oid_dic = []
    #logme('\n IN validation : '+ str(dic_result) + '\n')
    try:
        flag = 0
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        firmware_result = sqlalche_obj.session.query(
            Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
        if len(firmware_result):
            firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
            if firmware == '7.2.29':
                Oids = aliased(Odu1007_2_29_oids)
                table_name = "odu100_7_2_29_oids"
            elif firmware == '7.2.25':
                Oids = aliased(Odu1007_2_25_oids)
                table_name = "odu100_7_2_25_oids"
            else:
                Oids = aliased(Odu1007_2_20_oids)
                table_name = "odu100_7_2_20_oids"
        else:
            Oids = aliased(Odu1007_2_20_oids)
            table_name = "odu100_7_2_20_oids"
        if dic_result["success"] == '0' or dic_result["success"] == 0:
            k = 0
            for keys in dic_result.iterkeys():
                if keys == "success":
                    continue
                else:
                    oid_dic.append(str(keys) + str(k))
                    oid_list_min_max_value = sqlalche_obj.session.query(Oids.min_value, Oids.max_value).filter(
                        and_(Oids.oid_name == keys, Oids.device_type_id == device_type_id)).all()
                    oid_dic.append(oid_list_min_max_value[0])
                    k += 1
                    if len(oid_list_min_max_value) == 0:
                        flag = 1
                        continue
                    else:
                        if dic_result[keys] != None and dic_result[keys] != "":
                            if (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (oid_list_min_max_value[0][1] != "" and oid_list_min_max_value[0][1] != None):
                                if int(dic_result[keys]) <= int(oid_list_min_max_value[0][1]):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "The value is large than %s" % (
                                        oid_list_min_max_value[1])
                                    break
                            elif (oid_list_min_max_value[0][0] != "" or oid_list_min_max_value[0][0] != None) and (oid_list_min_max_value[0][1] == "" and oid_list_min_max_value[0][1] == None):
                                if int(dic_result[keys]) >= int(oid_list_min_max_value[0][0]):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "The value is smaller than %s" % (
                                        oid_list_min_max_value[0][0])
                                    break
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == None):
                                dic_result["%s" % (keys)] = dic_result[keys]
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == 'NULL') and (oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == 'NULL'):
                                dic_result["%s" % (keys)] = dic_result[keys]
                            else:
                                if (int(dic_result[keys]) >= int(oid_list_min_max_value[0][0])) and (int(dic_result[keys]) <= int(oid_list_min_max_value[0][1])):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "%s Value must be in between %s and %s" % (keys.split(
                                        ".")[-1], oid_list_min_max_value[0][0], oid_list_min_max_value[0][1])
                                    break
            if flag == 1:
                dic_result["success"] = 1
                sqlalche_obj.sql_alchemy_db_connection_close()
                return dic_result
            else:
                sqlalche_obj.sql_alchemy_db_connection_close()
                #logme('\n setconfig: '+ str(dic_result) + '\n')
                dic_result = odu100_set_config(
                    host_id, device_type_id, dic_result)
                #logme('\n RESULT setconfig: '+ str(dic_result) + '\n')
                return dic_result
        else:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        sqlalche_obj.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e)
        return str(e)
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# print
# controller_validation(4,'odu100',{'ru.omcConfTable.periodicStatsTimer':
# '12', 'success': 0, 'ru.omcConfTable.omcIpAddress': '172.22.0.95'})


def check_mac(host_id, macaddress, acl_mode, submit_btn_name, acl_index):
    """

    @param host_id:
    @param macaddress:
    @param acl_mode:
    @param submit_btn_name:
    @param acl_index:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_acl_mac_available = sqlalche_obj.session.query(
                Odu100RaAclConfigTable.macaddress, Odu100RaAclConfigTable.aclIndex).filter(Odu100RaAclConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_acl_mac_available) == 0:
            return 0
        else:
            if submit_btn_name.lower() == "add":
                for i in range(0, len(odu100_acl_mac_available)):
                    if macaddress == str(odu100_acl_mac_available[i][0]):
                        acl_flag = 1
                        break
                    else:
                        acl_flag = 0
            else:
                acl_mac_dict = dict(
                    (row[1], row[0]) for row in odu100_acl_mac_available)
                second_mac_list = list(
                    row[0] for row in odu100_acl_mac_available if row[1] != int(acl_index))
                if macaddress == acl_mac_dict.get(int(acl_index), None):
                    acl_flag = 0
                elif macaddress not in second_mac_list:
                    acl_flag = 0
                else:
                    acl_flag = 1

        if acl_flag == 0:
            return 0
        else:
            return 1
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def check_acl_accept(host_id, macaddress, acl_mode):
    """

    @param host_id:
    @param macaddress:
    @param acl_mode:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()

        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()
            odu100_acl_mac_available = sqlalche_obj.session.query(
                Odu100RaAclConfigTable.macaddress, Odu100RaAclConfigTable.aclIndex).filter(Odu100RaAclConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_acl_mac_available) == 0:
            return 2
        if len(odu100_peer_conf_table) == 0:
            return 0
        else:
            for i in odu100_peer_conf_table:
                for j in range(0, len(odu100_acl_mac_available)):
                    if (odu100_acl_mac_available[j][0] in i) or ("" in i):
                        peer_flag = 0
                    else:
                        peer_flag = 1
                        continue
                if peer_flag == 0 and i == len(odu100_peer_conf_table) - 1:
                    break
        if peer_flag == 0:
            return 0
        else:
            return 1
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def check_acl_deny(host_id, macaddress, acl_mode):
    """

    @param host_id:
    @param macaddress:
    @param acl_mode:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        peer_flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()

            odu100_acl_mac_available = sqlalche_obj.session.query(
                Odu100RaAclConfigTable.macaddress, Odu100RaAclConfigTable.aclIndex).filter(Odu100RaAclConfigTable.config_profile_id == odu100_profile_id[0]).all()

        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_acl_mac_available) == 0:
            return 0
        if len(odu100_peer_conf_table) == 0:
            return 0
        else:
            for i in odu100_peer_conf_table:
                for j in range(0, len(odu100_acl_mac_available)):
                    if (odu100_acl_mac_available[j][0] in i):
                        peer_flag = 1
                        break
                    else:
                        peer_flag = 0
                if peer_flag == 1:
                    break
        if peer_flag == 0:
            return 0
        else:
            return 1
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def mac_chk_accept(host_id, mac_list):
    """

    @param host_id:
    @param mac_list:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        peer_flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            # odu100_peer_conf_table =
            # sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(Odu100PeerConfigTable.config_profile_id
            # == odu100_profile_id[0]).all()
            odu100_acl_mac_available = sqlalche_obj.session.query(
                Odu100RaAclConfigTable.macaddress, Odu100RaAclConfigTable.aclIndex).filter(Odu100RaAclConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_acl_mac_available) == 0:
            return 2
        if len(mac_list) == 0:
            return 0
        else:
            for i in range(0, len(mac_list)):
                if peer_flag == 1:
                    break
                for j in odu100_acl_mac_available:
                    if (mac_list[i] in j) or (mac_list[i] == ""):
                        peer_flag = 0
                    else:
                        peer_flag = 1
                        break

        if peer_flag == 0:
            return 0
        else:
            return 1
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def mac_chk_deny(host_id, mac_list):
    """

    @param host_id:
    @param mac_list:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        peer_flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            # odu100_peer_conf_table =
            # sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(Odu100PeerConfigTable.config_profile_id
            # == odu100_profile_id[0]).all()
            odu100_acl_mac_available = sqlalche_obj.session.query(
                Odu100RaAclConfigTable.macaddress, Odu100RaAclConfigTable.aclIndex).filter(Odu100RaAclConfigTable.config_profile_id == odu100_profile_id[0]).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_acl_mac_available) == 0:
            return 2
        if len(mac_list) == 0:
            return 0
        else:
            for i in range(0, len(mac_list)):
                if peer_flag == 1:
                    break
                for j in odu100_acl_mac_available:
                    if (str(mac_list[i]) in j):
                        peer_flag = 1
                        break
                    else:
                        peer_flag = 0
        if peer_flag == 0:
            return 0
        else:
            return 1
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def check_acl_mac_accept(host_id, mac_address):
    """

    @param host_id:
    @param mac_address:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        peer_flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_acl_mode = sqlalche_obj.session.query(Odu100RaConfTable.aclMode).filter(
                Odu100RaConfTable.config_profile_id == odu100_profile_id[0]).all()
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()
            if len(odu100_acl_mode) > 0:
                if odu100_acl_mode[0].aclMode == 1:
                    if len(odu100_peer_conf_table) > 0:
                        for i in odu100_peer_conf_table:
                            # print "raju",
                            if mac_address in i or mac_address == "":
                                flag = 0
                            else:
                                flag = 1
                                break
                else:
                    return 0

        if flag == 0:
            return 0
        else:
            return 1
        sqlalche_obj.sql_alchemy_db_connection_close()

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def check_acl_mac_deny(host_id, mac_address):
    """

    @param host_id:
    @param mac_address:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        peer_flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_acl_mode = sqlalche_obj.session.query(Odu100RaConfTable.aclMode).filter(
                Odu100RaConfTable.config_profile_id == odu100_profile_id[0]).all()
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()

            if odu100_acl_mode[0].aclMode == 2:
                if len(odu100_peer_conf_table) > 0:
                    for i in odu100_peer_conf_table:
                        if mac_address not in i:
                            flag = 0
                        else:
                            flag = 1
                            break
                else:
                    return 0
            else:
                return 0

        if flag == 0:
            return 0
        else:
            return 1
        sqlalche_obj.sql_alchemy_db_connection_close()

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
# print check_acl_mac_accept_deny(44,'00:ff:aa:33:33:83')


def chk_peer_mac(host_id, mac_address):
    """

    @param host_id:
    @param mac_address:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        peer_flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()

        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(odu100_peer_conf_table) == 0:
            return 0
        else:
            for j in odu100_peer_conf_table:
                if mac_address in j:
                    peer_flag = 1
                    break

        if peer_flag == 0:
            return 0
        else:
            return 1
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def check_timeslot(host_id, timeslot):
    """

    @param host_id:
    @param timeslot:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_peer_conf_table = []
        flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()
            if len(odu100_peer_conf_table) == 0:
                return 0
            else:
                if int(timeslot) >= len(odu100_peer_conf_table):
                    return 0
                else:
                    for i in range(timeslot, len(odu100_peer_conf_table)):
                        if odu100_peer_conf_table[i].peerMacAddress == "":
                            flag = 0
                        else:
                            flag = i + 1
                            break
        if flag == 0:
            return 0
        else:
            return flag
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def check_acl_mac(host_id, mac_address):
    """

    @param host_id:
    @param mac_address:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        odu100_profile_id = []
        odu100_ra_conf_table = []
        odu100_peer_conf_table = []
        flag = 0
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if odu100_profile_id == None or odu100_profile_id == []:
            return {"success": 1, "result": "There is no Configruation exist for this host", "detail": ""}
        else:
            odu100_ra_conf_table = sqlalche_obj.session.query(Odu100RaConfTable.aclMode).filter(
                Odu100RaConfTable.config_profile_id == odu100_profile_id[0]).all()
            odu100_peer_conf_table = sqlalche_obj.session.query(Odu100PeerConfigTable.peerMacAddress).filter(
                Odu100PeerConfigTable.config_profile_id == odu100_profile_id[0]).all()
            if len(odu100_ra_conf_table) == 0:
                return 0
            if len(odu100_peer_conf_table) == 0:
                return 0
            else:
                if odu100_ra_conf_table[0].aclMode == 2:
                    for i in odu100_peer_conf_table:
                        if mac_address in i:
                            flag = 1
                            break
        if flag == 0:
            return 0
        else:
            return flag
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def odu100_common_cancel(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        firmware_result = sqlalche_obj.session.query(
            Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
        if len(firmware_result):
            firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
            if firmware == '7.2.29':
                Oids = aliased(Odu1007_2_29_oids)
            elif firmware == '7.2.25':
                Oids = aliased(Odu1007_2_25_oids)
            else:
                Oids = aliased(Odu1007_2_20_oids)
        else:
            Oids = aliased(Odu1007_2_20_oids)
        success_result = {}
        odu100_profile_id = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if dic_result["success"] == 0:
            for keys in dic_result["result"].iterkeys():
                if keys == "success" or keys == "aclindex":
                    continue
                else:
                    oid_list_table_field_value = sqlalche_obj.session.query(
                        Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == keys, Oids.device_type_id == device_type_id)).all()
                    table_name = "odu100_" + oid_list_table_field_value[0][0]
                    table_name = rename_tablename(table_name)
                    if table_name == "Odu100RaAclConfigTable":
                        str_table_obj = "table_result = sqlalche_obj.session.query(%s.%s).filter(%s.config_profile_id == \"%s\").first()" % (
                            table_name, oid_list_table_field_value[0][1], table_name, odu100_profile_id[0])
                    else:
                        str_table_obj = "table_result = sqlalche_obj.session.query(%s.%s).filter(%s.config_profile_id == \"%s\").one()" % (
                            table_name, oid_list_table_field_value[0][1], table_name, odu100_profile_id[0])
                    exec str_table_obj
                    for i in range(0, len(table_result)):
                        dic_result["result"][keys] = str(table_result[i])
                    success_result["success"] = 0
            sqlalche_obj.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        sqlalche_obj.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def acl_delete_bind(uuid, host_id):
    """

    @param uuid:
    @param host_id:
    @return:
    """
    try:
        global sqlalche_obj, errorStatus
        sqlalche_obj.sql_alchemy_db_connection_open()
        success_result = {"success": '', "result": {}}

        result = {}
        rowSts = []
        device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id).\
            filter(Hosts.host_id == host_id).one()
        odu100_acl_conf_table = sqlalche_obj.session.query(Odu100RaAclConfigTable).filter(
            Odu100RaAclConfigTable.odu100_raAclConfigTable_id == '%s' % (uuid)).one()

        rowSts.append({"ru.ra.raAclConfigTable.rowSts": ["1.3.6.1.4.1.26149.2.2.13.5.1.3" + "." + str(
            odu100_acl_conf_table.raIndex) + "." + str(odu100_acl_conf_table.aclIndex), "Integer32", "6"]})

        result = pysnmp_setAcl(device_param_list[0], device_param_list[1],
                               device_param_list[2], {}, {}, {}, rowSts[0])

        if result["success"] == 0 or result["success"] == '0':
            success_result["success"] = result["success"]
            for i in result["result"]:
                if result["result"][i] != 0:
                    result["result"][i] = errorStatus[result["result"][i]]
                else:
                    sqlalche_obj.session.delete(odu100_acl_conf_table)
            sqlalche_obj.session.commit()
            success_result["result"].update(result["result"])
        else:
            success_result["success"] = 1
            for i in result["result"]:
                i in errorStatus
                success_result["result"] = errorStatus[i]
        return success_result

    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# rint
# acl_delete_bind("ba52de08-ea94-11e0-8978-e069956899a4","9fad8c64-de92-11e0-b146-e069956899a4")
def commit_reboot_flash(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global errorStatus
    dependent_oid = []
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    firmware_result = sqlalche_obj.session.query(
        Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
    if len(firmware_result):
        firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
        if firmware == '7.2.29':
            Oids = aliased(Odu1007_2_29_oids)
            table_name = "odu100_7_2_29_oids"
        elif firmware == '7.2.25':
            Oids = aliased(Odu1007_2_25_oids)
            table_name = "odu100_7_2_25_oids"
        else:
            Oids = aliased(Odu1007_2_20_oids)
            table_name = "odu100_7_2_20_oids"
    else:
        Oids = aliased(Odu1007_2_20_oids)
        table_name = "odu100_7_2_20_oids"
    # Create the alias

    o1 = aliased(Oids)
    o2 = aliased(Oids)

    query_result = []
    result = {"success": 0, "result": {}}
    for keys in dic_result.iterkeys():
        query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
            o1, o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()

        if keys == "success":
            continue
        else:
            if len(query_result) > 0:

                if query_result[0][0].dependent_id == "" or query_result[0][0].dependent_id == None:
                    dependent_oid.append(
                        {keys: [
                            query_result[0][
                                0].oid + query_result[0][0].indexes,
                                         query_result[0][0].oid_type, dic_result[keys]]})

                    device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id).\
                        filter(Hosts.host_id == host_id).one()

                    # result =
                    # (pysnmp_set(depend_oid_value[i],device_param_list[0],device_param_list[1],device_param_list[2],dependent_oid[i]))
    for i in range(0, len(dependent_oid)):
        result = (pysnmp_set(dependent_oid[i], device_param_list[
                  0], device_param_list[1], device_param_list[2]))
    sqlalche_obj.sql_alchemy_db_connection_close()
    for i in result["result"]:
        if result["result"][i] != 0:
            result["result"][i] = errorStatus[result["result"][i]]
    return result


def peer_set(host_id, device_type_id, timeslot_val, dic_result, save_retry):
    # {keys:[query_result[0][0].oid+query_result[0][0].indexes,query_result[0][0].oid_type,dic_result[keys]]}
    """

    @param host_id:
    @param device_type_id:
    @param timeslot_val:
    @param dic_result:
    @param save_retry:
    @return:
    """
    try:
        global sqlalche_obj
        global errorStatus
        sqlalche_obj.sql_alchemy_db_connection_open()
        depend_oid = []
        dic = {}
        dic_r = {}
        li = []
        admin_result = {'success': 0}
        device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id).\
            filter(Hosts.host_id == host_id).all()
        admin_result = {}
        if save_retry == 1:
            for i in range(timeslot_val, 0, -1):
                if 'ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s' % (i) in dic_result:
                    dic .update(
                        {"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i): ["1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i), "OctetString", dic_result["ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i)]],
                         'ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.3.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s' % (i)]],
                         'ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.4.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s' % (i)]],
                         'ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.6.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s' % (i)]],
                         'ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.7.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s' % (i)]],
                         'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.5.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i)]],
                         'ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.6.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s' % (i)]],
                         'ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s' % (i): ['1.3.6.1.4.1.26149.2.2.13.9.1.1.7.1.%s' % (i), 'Integer32', dic_result['ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s' % (i)]]})

                else:
                    dic = {"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i): ["1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i), "OctetString",
                                                                                 dic_result["ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i)]]}
                # depend_oid.append(dic)
                # depend_oid.append({'ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s'%(i):['.1.3.6.1.4.1.26149.2.2.13.9.1.1.4.1.%s'%(i),'Integer32',dic_result['ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s'%(i)]]})
                # depend_oid.append({'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s'%(i):['.1.3.6.1.4.1.26149.2.2.13.9.1.1.5.1.%s'%(i),'Integer32',dic_result['ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s'%(i)]]})

            result = pysnmp_set(dic, device_param_list[0].ip_address, device_param_list[0].snmp_port, device_param_list[0].snmp_write_community, {
                                'raadmin-1': ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'Integer32', 0]})
            #logme(" snmp "+str(result))
            if result['success'] == 1:
                for i in result["result"]:
                    if i == 553:
                        result["result"] = str(errorStatus.get(
                            i, "SNMP agent Unknown Error Occured"))
                    elif i == 551:
                        result["result"] = str(errorStatus.get(
                            i, "SNMP agent Unknown Error Occured"))
                    else:
                        if result["result"][i] != 0:
                            result["result"] = str(errorStatus.get(
                                result["result"][i], "Device Unresponsive"))
                        else:
                            result["result"] = str(
                                errorStatus.get(i, "Device Unresponsive"))

            else:
                peer_config = sqlalche_obj.session.query(Odu100PeerConfigTable).filter(
                    Odu100PeerConfigTable.config_profile_id == device_param_list[0].config_profile_id).delete()
                sqlalche_obj.session.commit()
                for i in range(0, timeslot_val):
                    if 'ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s' % (i + 1) in dic_result:
                        peer_add = Odu100PeerConfigTable(
                            device_param_list[0].config_profile_id, 1, 1, dic_result[
                                "ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)],
                                                         dic_result['ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s' %
                                                             (i + 1)], dic_result['ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s' % (i + 1)],
                                                         dic_result['ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1)], dic_result['ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s' % (i + 1)], dic_result['ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s' % (i + 1)])
                        sqlalche_obj.session.add(peer_add)
                    else:
                        peer_add = Odu100PeerConfigTable(device_param_list[0].config_profile_id, 1, 1, dic_result[
                                                         "ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)], 512, 512, -1, 100000, 100000)
                        sqlalche_obj.session.add(peer_add)
                admin_result = pysnmp_set(
                    {'raadmin': ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1',
                        'Integer32', 1]}, device_param_list[0].ip_address,
                                          device_param_list[0].snmp_port, device_param_list[0].snmp_write_community)
                #logme('raadmin-snmp '+str(admin_result))
                ra_admin = sqlalche_obj.session.query(Odu100RaConfTable).filter(
                    Odu100RaConfTable.config_profile_id == device_param_list[0].config_profile_id).all()

                if admin_result['success'] == 1:
                    for i in admin_result['result']:
                        admin_result['result'] = errorStatus.get(
                            admin_result['result'][i], "")
                    ra_admin[0].raAdminState = 0
                else:
                    ra_admin[0].raAdminState = 1
                sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            result.update({'admin': admin_result})
            return result
        if save_retry == 2:
            for k in dic_result:
                if k == "success":
                    continue
                else:
                    if "peerMacAddress" in k:
                        name = "ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (
                            k.split(".")[-1])
                        li.append(k.split(".")[-1])
                        oid = "1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (
                            k.split(".")[-1])
                        oid_type = "OctetString"
                        oidvalue = dic_result[
                            "ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (k.split(".")[-1])]
                        dic = {name: [oid, oid_type, oidvalue]}

                    elif "guaranteedUplinkBW" in k:
                        li.append(k.split(".")[-1])
                        name = "ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (
                            k.split(".")[-1])
                        oid = "1.3.6.1.4.1.26149.2.2.13.9.1.1.3.1.%s" % (
                            k.split(".")[-1])
                        oid_type = "Integer32"
                        oidvalue = dic_result[
                            "ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (k.split(".")[-1])]
                        dic = {name: [oid, oid_type, oidvalue]}
                    elif "guaranteedDownlinkBW" in k:
                        li.append(k.split(".")[-1])
                        name = "ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (
                            k.split(".")[-1])
                        oid = "1.3.6.1.4.1.26149.2.2.13.9.1.1.4.1.%s" % (
                            k.split(".")[-1])
                        oid_type = "Integer32"
                        oidvalue = dic_result[
                            "ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (k.split(".")[-1])]
                        dic = {name: [oid, oid_type, oidvalue]}
                    elif "basicRateMCSIndex" in k:
                        li.append(k.split(".")[-1])
                        name = "ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (
                            k.split(".")[-1])
                        oid = "1.3.6.1.4.1.26149.2.2.13.9.1.1.5.1.%s" % (
                            k.split(".")[-1])
                        oid_type = "Integer32"
                        oidvalue = dic_result[
                            "ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (k.split(".")[-1])]
                        dic = {name: [oid, oid_type, oidvalue]}
                    elif "maxUplinkBW" in k:
                        li.append(k.split(".")[-1])
                        name = "ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (
                            k.split(".")[-1])
                        oid = "1.3.6.1.4.1.26149.2.2.13.9.1.1.6.1.%s" % (
                            k.split(".")[-1])
                        oid_type = "Integer32"
                        oidvalue = dic_result[
                            "ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (k.split(".")[-1])]
                        dic = {name: [oid, oid_type, oidvalue]}
                    elif "maxDownlinkBW" in k:
                        li.append(k.split(".")[-1])
                        name = "ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (
                            k.split(".")[-1])
                        oid = "1.3.6.1.4.1.26149.2.2.13.9.1.1.7.1.%s" % (
                            k.split(".")[-1])
                        oid_type = "Integer32"
                        oidvalue = dic_result[
                            "ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (k.split(".")[-1])]
                        dic = {name: [oid, oid_type, oidvalue]}
                    dic_r.update(dic)
    ##        for i in dic:
    ##            dic_r.update(i)

            result = pysnmp_set(dic_r, device_param_list[0].ip_address, device_param_list[0].snmp_port, device_param_list[0].snmp_write_community, {
                                'adminState-1': ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'Integer32', '1']})
            peer_config = sqlalche_obj.session.query(Odu100PeerConfigTable).filter(
                Odu100PeerConfigTable.config_profile_id == device_param_list[0].config_profile_id).all()
            if result['success'] == 1:
                for i in result["result"]:
                    result["result"] = errorStatus.get(i, "No response")

            else:
                if len(peer_config) > 0:
                    for i in dic_result:
                        if ('peermac' in i) and (i.split(".")[-1] in li):
                            peer_config[int((i.split(
                                ".")[-1])) - 1].peerMacAddress = dic_result[i]
                        elif ('guaranteedUplinkBW' in i) and (i.split(".")[-1] in li):
                            peer_config[int((i.split(
                                ".")[-1])) - 1].guaranteedUplinkBW = dic_result[i]
                        elif ('guaranteedDownlinkBW' in i) and (i.split(".")[-1] in li):
                            peer_config[int((i.split(
                                ".")[-1])) - 1].guaranteedDownlinkBW = dic_result[i]
                        elif ('basicRateMCSIndex' in i) and (i.split(".")[-1] in li):
                            peer_config[int((i.split(
                                ".")[-1])) - 1].basicrateMCSIndex = dic_result[i]
                        elif ('maxUplinkBW' in i) and (i.split(".")[-1] in li):
                            peer_config[int((i.split(
                                ".")[-1])) - 1].maxUplinkBW = dic_result[i]
                        elif ('maxDownlinkBW' in i) and (i.split(".")[-1] in li):
                            peer_config[int((i.split(
                                ".")[-1])) - 1].maxDownlinkBW = dic_result[i]
            admin_result = pysnmp_set(
                {'raadmin': ['1.3.6.1.4.1.26149.2.2.13.1.1.2.1',
                    'Integer32', 1]}, device_param_list[0].ip_address,
                                      device_param_list[0].snmp_port, device_param_list[0].snmp_write_community)
            ra_admin = sqlalche_obj.session.query(Odu100RaConfTable).filter(
                Odu100RaConfTable.config_profile_id == device_param_list[0].config_profile_id).all()

            if admin_result['success'] == 1:
                for i in admin_result['result']:
                    admin_result['result'] = errorStatus.get(
                        admin_result['result'][i], "")
                ra_admin[0].raAdminState = 0
            else:
                ra_admin[0].raAdminState = 1
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            result.update({'admin': admin_result})
            return result
    except Exception as e:
        import traceback
        logme(traceback.format_exc())
        return str(e)
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
#
# print
# peer_set(28,'odu100',2,{'ru.ra.peerNode.peerConfigTable.peerMacAddress.2':
# '00:80:48:71:86:94', 'ru.ra.peerNode.peerConfigTable.maxUplinkBW.2':
# '3200', 'ru.ra.peerNode.peerConfigTable.peerMacAddress.1':
# '00:80:48:71:86:91', 'ru.ra.peerNode.peerConfigTable.maxDownlinkBW.2':
# '3200', 'ru.ra.peerNode.peerConfigTable.maxDownlinkBW.1': '4000',
# 'ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.1': '512',
# 'ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.1': '512',
# 'ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.2': '512',
# 'ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.2': '512',
# 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.1': '5', 'success': 0,
# 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.2': '0',
# 'ru.ra.peerNode.peerConfigTable.maxUplinkBW.1': '4000'},1)


def chk_list(select_list):
    """

    @param select_list:
    @return:
    """
    flag = 0
    duplicate = 1
    for i in range(0, len(select_list)):
        duplicate = select_list.count(select_list[i])
        if duplicate > 1:
            flag = 1
            break
        else:
            continue
    if flag == 1:
        return 1
    else:
        return 0


def chk_mac_duplicacy(mac_list):
    """

    @param mac_list:
    @return:
    """
    flag = 0
    duplicate = 1
    if len(mac_list) > 0:
        for i in range(0, len(mac_list)):
            if mac_list[i] == "":
                continue
            else:
                duplicate = mac_list.count(mac_list[i])
            if duplicate > 1:
                flag = 1
                break
            else:
                continue
        if flag == 1:
            return 1
        else:
            return 0
    else:
        return 0


def channel_config_set(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        global errorStatus
        result = {}
        dic = {}
        dic_r = {}
        device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id, Hosts.snmp_read_community).\
            filter(Hosts.host_id == host_id).all()
        for i in dic_result:
            k = i.split(".")[-1]
            dic.update({i: ('1.3.6.1.4.1.26149.2.2.13.7.4.1.2.1.%s' %
                       str(k), 'Gauge32', dic_result[i])})
        admin_state = {'admin': [
            '1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'Integer32', '0']}

        result_admin = pysnmp_set(
            admin_state, device_param_list[
                0].ip_address, device_param_list[0].snmp_port,
                                  device_param_list[0].snmp_write_community)

        if result_admin["success"] == 0:
            result = pysnmp_set(
                dic, device_param_list[
                    0].ip_address, device_param_list[0].snmp_port,
                                device_param_list[0].snmp_write_community)
        else:
            for i in result_admin["result"]:
                i in errorStatus
                result_admin["result"] = errorStatus.get(
                    i, "SNMP Agent gone away")
                sqlalche_obj.sql_alchemy_db_connection_close()
                return result_admin

        admin_state = {'admin': [
            '1.3.6.1.4.1.26149.2.2.13.1.1.2.1', 'Integer32', 1]}
        result_admin = pysnmp_set(
            admin_state, device_param_list[
                0].ip_address, device_param_list[0].snmp_port,
                                  device_param_list[0].snmp_write_community)

        channel_config = sqlalche_obj.session.query(Odu100RaPreferredRFChannelTable).filter(
            Odu100RaPreferredRFChannelTable.config_profile_id == device_param_list[0].config_profile_id).all()
        if len(channel_config) > 0:
            if result["success"] == 0:
                m = 0
                for i in result["result"]:
                    if i == 'admin1':
                        continue
                    else:
                        if result["result"][i] != 0:
                            result["result"][
                                i] = errorStatus[result["result"][i]]
                        else:
                            channel_config[m].preindex = m + 1
                            channel_config[m].rafrequency = dic_result[i]
                        m = m + 1
            else:
                for i in result["result"]:
                    i in errorStatus
                    result["result"] = errorStatus[i]
        else:
            result["success"] = 1
            result["result"] = "Please reconcile the device"
        time.sleep(5)
        tdd_mac_status_table = pysnmp_get_table('1.3.6.1.4.1.26149.2.2.13.7.2', device_param_list[0].ip_address, int(device_param_list[0]
                                                .snmp_port), device_param_list[0].snmp_read_community)
        if tdd_mac_status_table["success"] == 0:
            if len(tdd_mac_status_table["result"]) > 0:
                tdd_mac_status = sqlalche_obj.session.query(Odu100RaTddMacStatusTable).filter(
                    Odu100RaTddMacStatusTable.host_id == host_id).delete()
                sqlalche_obj.session.commit()
                m = 0
                for i in tdd_mac_status_table["result"]:
                    tdd_mac_status_add = Odu100RaTddMacStatusTable(
                        host_id, 1, tdd_mac_status_table["result"][i][0], datetime.now())
                    sqlalche_obj.session.add(tdd_mac_status_add)
                    m = m + 1
        sqlalche_obj.session.commit()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result
    except Exception as e:
        return str(e)
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


def packet_filter_set(host_id, device_type_id, ip_mac_statue, dic_result):  # raju
    """

    @param host_id:
    @param device_type_id:
    @param ip_mac_statue:
    @param dic_result:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        global errorStatus
        result = {}
        dic = {}
        dic_r = {}
        success_result = {}
        device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id, Hosts.snmp_read_community).\
            filter(Hosts.host_id == host_id).all()
        for i in dic_result:
            split_result = i.split(".")
            k = split_result[-1]
            k1 = split_result[-2]
            if k1 == 'ipFilterIpAddress':
                dic.update({i: ('1.3.6.1.4.1.26149.2.2.17.1.1.2.%s' %
                           str(k), 'OctetString', dic_result[i])})
            elif k1 == 'ipFilterNetworkMask':
                dic.update({i: ('1.3.6.1.4.1.26149.2.2.17.1.1.3.%s' % str(k),
                           'IpAddress', dic_result[i])})
            elif k1 == 'filterMacAddress':
                dic.update({i: ('1.3.6.1.4.1.26149.2.2.17.2.1.2.%s' %
                           str(k), 'OctetString', dic_result[i])})

        result = pysnmp_set(dic, device_param_list[0].ip_address, int(
            device_param_list[0].snmp_port), device_param_list[0].snmp_write_community)

        if result["success"] == 0 or result["success"] == '0':
            success_result["success"] = result["success"]
            for i in result["result"]:
                index_value = i.split('.')[-1]
                column_name = i.split('.')[-2]
                if result["result"][i] != 0:
                    result["result"][i] = errorStatus[result["result"][i]]
                else:
                    if i in dic_result:
                        if ip_mac_statue == 0:  # 0 for ipPacketFilter and 1 for macPacketFilter
                            filter_result = sqlalche_obj.session.query(Odu100IpFilterTable).filter(
                                and_(Odu100IpFilterTable.host_id == host_id, Odu100IpFilterTable.ipFilterIndex == int(index_value))).all()
                            setattr(
                                filter_result[0], column_name, dic_result[i])
                        else:
                            filter_result = sqlalche_obj.session.query(Odu100MacFilterTable).filter(
                                and_(Odu100MacFilterTable.host_id == host_id, Odu100MacFilterTable.macFilterIndex == int(index_value))).all()
                            setattr(
                                filter_result[0], column_name, dic_result[i])
            sqlalche_obj.session.commit()
            success_result["result"] = result['result']
        else:
            success_result["success"] = 1
            for i in result["result"]:
                if i == 553:
                    result["result"] = str(errorStatus.get(
                        i, "SNMP agent Unknown Error Occured"))
                elif i == 551:
                    result["result"] = str(errorStatus.get(
                        i, "SNMP agent Unknown Error Occured"))
                else:
                    if result["result"][i] != 0:
                        result["result"] = errorStatus.get(
                            result["result"][i], "Device is not respoding")
                success_result["result"] = result['result']

        sqlalche_obj.sql_alchemy_db_connection_close()
        return success_result
    except Exception as e:
        import traceback
        print traceback.format_exc()
        return str(e[-1])
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()

# dic = {'ru.packetFilters.ipFilterTable.ipFilterIpAddress.5': '',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.4': '172.22.0.104',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.7': '',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.6': '',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.1': '172.22.0.1',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.3': '',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.2': '172.22.0.2',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.8': '',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.1':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.2':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.3':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.4':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.5':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.6':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.7':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.8':
# '255.255.255.255'}

# print packet_filter_set(11,'odu100','ip',dic)
# aa={'ru.packetFilters.ipFilterTable.ipFilterIpAddress.5': '',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.4': '172.22.0.161',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.7': '',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.6': '172.22.0.165',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.1': '172.22.0.156',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.3': '172.22.0.154',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.2': '172.22.0.158',
# 'ru.packetFilters.ipFilterTable.ipFilterIpAddress.8': '172.22.0.166',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.1':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.2':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.3':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.4':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.5': '',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.6':
# '255.255.255.255',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.7': '',
# 'ru.packetFilters.ipFilterTable.ipFilterNetworkMask.8':
# '255.255.255.255'}

# print packet_filter_set(27,'odu100','ip',aa)


def delete_site_survey_list(host_id):
    """

    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    sqlalche_obj.db.execute(
        "delete from odu100_raSiteSurveyResultTable where host_id='%s'" % (host_id))
    sqlalche_obj.sql_alchemy_db_connection_close()
##################################################### Reconcilation ######


class OduReconcilation(object):
    """
    ODU device reconciliation
    """
    def odu100_acl_reconciliation(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        try:
            global errorStatus
            global sqlalche_obj
            com_obj = CommonReconciliation()
            port = 0
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {'result': {}, 'success': 0}
            if host_id != "" or host_id != None:
                device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_read_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id, Hosts.reconcile_health, Hosts.snmp_write_community).\
                    filter(Hosts.host_id == host_id).all()
            port = int(device_param_list[0].snmp_port)
            result = pysnmp_acl_reconcile(
                "1.3.6.1.4.1.26149.2.2.13.5", device_param_list[
                    0].ip_address, port,
                                          device_param_list[0].snmp_read_community)
            if len(result) == 1:
                if 'err' in result:
                    for i in result['err']:
                        if i in errorStatus:
                            result = {
                                'success': 1, 'result': str(errorStatus[i])}
            elif len(result) > 1:
                acl_config = sqlalche_obj.session.query(Odu100RaAclConfigTable).filter(
                    Odu100RaAclConfigTable.config_profile_id == device_param_list[0][4]).delete()
                sqlalche_obj.session.commit()
                if len(result['mac']) == 0 and len(result['row']) == 0:
                    con_table_output = com_obj.reconciliation_model(
                        host_id, device_type, 'raConfTable', 0)
                    if con_table_output["success"] == 0:
                        result = {'success': 0,
                            'result': "Acl Reconciliation Done Successfully"}
                    else:
                        result = {'success': 0,
                            'result': con_table_output["result"]}
                elif (len(result['mac']) == len(result['row'])):
                    mac = result['mac']
                    row = result['row']
                    for i in row:
                        acl_row = Odu100RaAclConfigTable(
                            device_param_list[0][4], 1, i, mac[i], i)
                        sqlalche_obj.session.add(acl_row)
                    sqlalche_obj.session.commit()
                    con_table_output = com_obj.reconciliation_model(
                        host_id, device_type, 'raConfTable', 0)
                    if con_table_output["success"] == 0:
                        result = {'success': 0,
                            'result': "Acl Reconciliation Done Successfully"}
                    else:
                        result = {'success': 0,
                            'result': con_table_output["result"]}
            return result
        except Exception as e:
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def odu16_add_default_config_profile(self, host_id, device_type_id, table_prefix, insert_update):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param insert_update:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        new_profile = Odu16ConfigProfiles(
            device_type_id, "Odu16config", "Master",
                                          None, datetime.now(), None, datetime.now(), None, 0)
        sqlalche_obj.session.add(new_profile)
        sqlalche_obj.session.flush()
        sqlalche_obj.session.refresh(new_profile)
        profile_id = new_profile.config_profile_id

        try:
            default_config_profile_id = sqlalche_obj.session.query(Odu16ConfigProfiles.config_profile_id).filter(
                and_(Odu16ConfigProfiles.device_type_id == device_type_id, Odu16ConfigProfiles.config_profile_type_id == "Default")).all()

            omc_conf_data = sqlalche_obj.session.query(SetOdu16OmcConfTable.omc_ip_address, SetOdu16OmcConfTable.periodic_stats_timer).filter(
                SetOdu16OmcConfTable.config_profile_id == default_config_profile_id[0][0]).all()
            omc_conf_add_row = SetOdu16OmcConfTable(
                profile_id, omc_conf_data[0][0], omc_conf_data[0][1])
            sqlalche_obj.session.add(omc_conf_add_row)

            peer_config_data = sqlalche_obj.session.query(SetOdu16PeerConfigTable.peer_mac_address, SetOdu16PeerConfigTable.index).filter(
                SetOdu16PeerConfigTable.config_profile_id == default_config_profile_id[0][0]).all()
            for i in range(0, len(peer_config_data)):
                add_peer_config_data = SetOdu16PeerConfigTable(
                    profile_id, peer_config_data[i][0], peer_config_data[i][1])
                sqlalche_obj.session.add(add_peer_config_data)

            acl_config = sqlalche_obj.session.query(SetOdu16RAAclConfigTable.mac_address, SetOdu16RAAclConfigTable.index).filter(
                SetOdu16RAAclConfigTable.config_profile_id == default_config_profile_id[0][0]).all()
            for i in range(0, len(acl_config)):
                add_acl_config = SetOdu16RAAclConfigTable(
                    profile_id, acl_config[i][0], acl_config[i][1])
                sqlalche_obj.session.add(add_acl_config)

            ra_conf = sqlalche_obj.session.query(SetOdu16RAConfTable.raAdminState, SetOdu16RAConfTable.acl_mode, SetOdu16RAConfTable.ssid).filter(
                SetOdu16RAConfTable.config_profile_id == default_config_profile_id[0][0]).all()
            add_ra_config = SetOdu16RAConfTable(
                profile_id, ra_conf[0][0], ra_conf[0][1], ra_conf[0][2])
            sqlalche_obj.session.add(add_ra_config)

            ra_llc = sqlalche_obj.session.query(
                SetOdu16RALlcConfTable.llc_arq_enable, SetOdu16RALlcConfTable.arq_win, SetOdu16RALlcConfTable.frame_loss_threshold,
                                                SetOdu16RALlcConfTable.leaky_bucket_timer_val, SetOdu16RALlcConfTable.frame_loss_timeout).filter(SetOdu16RALlcConfTable.config_profile_id == default_config_profile_id[0][0]).all()
            add_ra_llc = SetOdu16RALlcConfTable(profile_id, ra_llc[0][0], ra_llc[0][1], ra_llc[0]
                                                [2], ra_llc[0][3], ra_llc[0][4])
            sqlalche_obj.session.add(add_ra_llc)

            ra_tdd_mac = sqlalche_obj.session.query(
                SetOdu16RATddMacConfig.rf_channel_frequency, SetOdu16RATddMacConfig.pass_phrase, SetOdu16RATddMacConfig.rfcoding,
                                                    SetOdu16RATddMacConfig.tx_power, SetOdu16RATddMacConfig.max_crc_errors, SetOdu16RATddMacConfig.leaky_bucket_timer_value).filter(SetOdu16RATddMacConfig.config_profile_id == default_config_profile_id[0][0]).all()
            add_ra_tdd_mac = SetOdu16RATddMacConfig(
                profile_id, ra_tdd_mac[0][0], ra_tdd_mac[0][1], ra_tdd_mac[0][2], ra_tdd_mac[0][3], ra_tdd_mac[0][4], ra_tdd_mac[0][5])
            sqlalche_obj.session.add(add_ra_tdd_mac)

            ru_conf = sqlalche_obj.session.query(
                SetOdu16RUConfTable.adminstate, SetOdu16RUConfTable.channel_bandwidth, SetOdu16RUConfTable.sysnch_source,
                                                 SetOdu16RUConfTable.country_code).filter(SetOdu16RUConfTable.config_profile_id == default_config_profile_id[0][0]).all()
            add_ru_conf = SetOdu16RUConfTable(
                profile_id, ru_conf[0][0], ru_conf[0][1], ru_conf[0][2], ru_conf[0][3])
            sqlalche_obj.session.add(add_ru_conf)

            ru_date_time = sqlalche_obj.session.query(
                SetOdu16RUDateTimeTable.year, SetOdu16RUDateTimeTable.month, SetOdu16RUDateTimeTable.day, SetOdu16RUDateTimeTable.hour,
                                                      SetOdu16RUDateTimeTable.min, SetOdu16RUDateTimeTable.sec).all()
            add_ru_date_time = SetOdu16RUDateTimeTable(
                profile_id, ru_date_time[0][0], ru_date_time[0][1], ru_date_time[0][2], ru_date_time[0][3], ru_date_time[0][4], ru_date_time[0][5])
            sqlalche_obj.session.add(add_ru_date_time)

            sync_config = sqlalche_obj.session.query(
                SetOdu16SyncConfigTable.adminStatus, SetOdu16SyncConfigTable.raster_time, SetOdu16SyncConfigTable.num_slaves,
                                                     SetOdu16SyncConfigTable.sync_loss_threshold, SetOdu16SyncConfigTable.leaky_bucket_timer,
                                                     SetOdu16SyncConfigTable.sync_lost_timeout, SetOdu16SyncConfigTable.sync_config_time_adjust,
                                                     SetOdu16SyncConfigTable.sync_config_broadcast_enable).filter(SetOdu16SyncConfigTable.config_profile_id == default_config_profile_id[0][0]).all()
            add_sync_config = SetOdu16SyncConfigTable(
                profile_id, sync_config[0][0], sync_config[0][1], sync_config[
                    0][
                        2], sync_config[
                            0][4], sync_config[0][5], sync_config[0][6],
                                                      sync_config[0][7])
            sqlalche_obj.session.add(add_sync_config)

            sys_register = sqlalche_obj.session.query(
                SetOdu16SysOmcRegistrationTable.sys_omc_register_contact_addr,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_contact_person,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_contact_mobile,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_alternate_contact,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_contact_email,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_active_card_hwld,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_registerne_site_direction,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_registerne_site_landmark,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_registerne_site_latitude,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_registerne_site_longitude,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_registerne_state,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_country,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_city,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_register_sitebldg,
                                                      SetOdu16SysOmcRegistrationTable.sys_omc_registersitefloor,
                                                      SetOdu16SysOmcRegistrationTable.site_mac, SetOdu16SysOmcRegistrationTable.product_id).\
                filter(SetOdu16SysOmcRegistrationTable.config_profile_id == default_config_profile_id[
                       0][0]).all()

            add_sys_register = SetOdu16SysOmcRegistrationTable(
                profile_id, sys_register[0][0], sys_register[0][
                    1], sys_register[0][2], sys_register[0][3],
                                                               sys_register[0][4], sys_register[
                                                                   0][
                                                                       5], sys_register[0][6], sys_register[0][7], sys_register[0][8],
                                                               sys_register[0][9], sys_register[0][
                                                                   10], sys_register[0][11], sys_register[0][12], sys_register[0][13],
                                                               sys_register[0][14], sys_register[0][15], sys_register[0][16])
            sqlalche_obj.session.add(add_sys_register)

            get_hw_desc_table = GetOdu16HWDescTable(host_id, None, None)
            sqlalche_obj.session.add(get_hw_desc_table)

            get_sw_status_table = GetOdu16SWStatusTable(
                host_id, None, None, None)
            sqlalche_obj.session.add(get_sw_status_table)
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            # return str(profile_id),0
            ## For MWC this is done
            return str(profile_id), 0
        except Exception as e:
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def odu100_add_default_config_profile(self, host_id, device_type_id, table_prefix, current_time, reconcile_chk, user_name):
        # global sqlalche_obj
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param current_time:
        @param reconcile_chk:
        @param user_name:
        @return:
        """
        try:

            sqlalche_obj.sql_alchemy_db_connection_open()

            new_profile = Odu16ConfigProfiles(
                device_type_id, "Odu100config", "Master", None,
                                              datetime.now(), None, datetime.now(), None, 0)
            sqlalche_obj.session.add(new_profile)
            sqlalche_obj.session.flush()
            sqlalche_obj.session.refresh(new_profile)
            new_profile_id = new_profile.config_profile_id
            default_profile_id = sqlalche_obj.session.query(Odu16ConfigProfiles.config_profile_id)\
                .filter(and_(Odu16ConfigProfiles.device_type_id == device_type_id, Odu16ConfigProfiles.config_profile_type_id == "default")).all()

            host_data = sqlalche_obj.session.query(Hosts).\
                filter(Hosts.host_id == host_id).all()
            # print "hello"
            ru_conf_data = sqlalche_obj.session.query(Odu100RuConfTable).filter(
                Odu100RuConfTable.config_profile_id == default_profile_id[0].config_profile_id).all()

            if len(ru_conf_data) > 0:
                for i in range(0, len(ru_conf_data)):

                    ru_conf_data_add = Odu100RuConfTable(
                        new_profile_id, ru_conf_data[
                            i].confIndex, ru_conf_data[i].adminstate,
                                                         ru_conf_data[i].defaultNodeType, ru_conf_data[
                                                             i].channelBandwidth,
                                                         ru_conf_data[
                                                             i].synchSource, ru_conf_data[i].countryCode, ru_conf_data[i].poeState,
                                                         ru_conf_data[i].ethFiltering, ru_conf_data[i].poePort2State, ru_conf_data[i].poePort4State, ru_conf_data[i].poePort6State)
                    sqlalche_obj.session.add(ru_conf_data_add)

            # print "hello12"
            unmp_conf_data = sqlalche_obj.session.query(Odu100OmcConfTable).filter(
                Odu100OmcConfTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(unmp_conf_data) > 0:
                for i in range(0, len(unmp_conf_data)):
                    unmp_conf_data_add = Odu100OmcConfTable(
                        new_profile_id, unmp_conf_data[i].omcConfIndex, unmp_conf_data[i].omcIpAddress, unmp_conf_data[i].periodicStatsTimer)
                    sqlalche_obj.session.add(unmp_conf_data_add)
            # print "hello13"
            registration_conf_data = sqlalche_obj.session.query(Odu100SysOmcRegistrationTable).filter(
                Odu100SysOmcRegistrationTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(registration_conf_data) > 0:
                for i in range(0, len(registration_conf_data)):
                    registration_conf_data_add = Odu100SysOmcRegistrationTable(new_profile_id, registration_conf_data[i].sysOmcRegistrationIndex,
                                                                               registration_conf_data[
                                                                                   i].sysOmcRegisterContactAddr,
                                                                               registration_conf_data[
                                                                                   i].sysOmcRegisterContactPerson, registration_conf_data[i].sysOmcRegisterContactMobile,
                                                                               registration_conf_data[i].sysOmcRegisterAlternateContact, registration_conf_data[i].sysOmcRegisterContactEmail)
                    sqlalche_obj.session.add(registration_conf_data_add)
            # print "hello14"
            synchronization_conf_data = sqlalche_obj.session.query(Odu100SyncConfigTable).filter(
                Odu100SyncConfigTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(synchronization_conf_data) > 0:
                for i in range(0, len(synchronization_conf_data)):
                    synchronization_conf_data_add = Odu100SyncConfigTable(
                        new_profile_id,
                                                                          synchronization_conf_data[
                                                                              i].syncConfigIndex, synchronization_conf_data[i].adminStatus,
                                                                          synchronization_conf_data[
                                                                              i].synchState, synchronization_conf_data[i].rasterTime,
                                                                          synchronization_conf_data[i].syncLossThreshold, synchronization_conf_data[i].leakyBucketTimer,
                                                                          synchronization_conf_data[
                                                                              i].syncLostTimeout,
                                                                          synchronization_conf_data[i].syncConfigTimerAdjust, synchronization_conf_data[i].percentageDownlinkTransmitTime)
                    sqlalche_obj.session.add(synchronization_conf_data_add)
            # print "hello15"
            ra_conf_data = sqlalche_obj.session.query(Odu100RaConfTable).filter(
                Odu100RaConfTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(ra_conf_data) > 0:
                for i in range(0, len(ra_conf_data)):
                    ra_conf_data_add = Odu100RaConfTable(new_profile_id,
                                                         ra_conf_data[
                                                             i].raIndex, ra_conf_data[i].raAdminState, ra_conf_data[i].aclMode,
                                                         ra_conf_data[i].ssID, ra_conf_data[
                                                             i].guaranteedBroadcastBW, ra_conf_data[i].dba,
                                                         ra_conf_data[i].acm, ra_conf_data[i].acs, ra_conf_data[
                                                             i].dfs, ra_conf_data[i].numSlaves, ra_conf_data[i].antennaPort,
                                                         ra_conf_data[i].linkDistance, ra_conf_data[i].anc)
                    sqlalche_obj.session.add(ra_conf_data_add)
            # print "hello16"
            tdd_mac_conf_data = sqlalche_obj.session.query(Odu100RaTddMacConfigTable).filter(
                Odu100RaTddMacConfigTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(tdd_mac_conf_data) > 0:
                for i in range(0, len(tdd_mac_conf_data)):
                    tdd_mac_conf_data_add = Odu100RaTddMacConfigTable(
                        new_profile_id,
                                                                      tdd_mac_conf_data[i].raIndex, tdd_mac_conf_data[
                                                                          i].passPhrase, tdd_mac_conf_data[i].txPower,
                                                                      tdd_mac_conf_data[
                                                                          i].maxPower, tdd_mac_conf_data[i].maxCrcErrors, tdd_mac_conf_data[i].leakyBucketTimerValue,
                                                                      tdd_mac_conf_data[i].encryptionType)
                    sqlalche_obj.session.add(tdd_mac_conf_data_add)
            # print "hello17"
            ra_llc_conf_data = sqlalche_obj.session.query(Odu100RaLlcConfTable).filter(
                Odu100RaLlcConfTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(ra_llc_conf_data) > 0:
                for i in range(0, len(ra_llc_conf_data)):
                    ra_llc_conf_data_add = Odu100RaLlcConfTable(new_profile_id,
                                                                ra_llc_conf_data[
                                                                    i].raIndex, ra_llc_conf_data[i].arqWinLow, ra_llc_conf_data[i].arqWinHigh,
                                                                ra_llc_conf_data[
                                                                    i].frameLossThreshold, ra_llc_conf_data[i].leakyBucketTimerVal, ra_llc_conf_data[i].frameLossTimeout
                                                                )
                    sqlalche_obj.session.add(ra_llc_conf_data_add)
            # print "hello19"
            channel_conf_data = sqlalche_obj.session.query(Odu100RaPreferredRFChannelTable).filter(
                Odu100RaPreferredRFChannelTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(channel_conf_data) > 0:
                for i in range(0, len(channel_conf_data)):
                    channel_conf_data_add = Odu100RaPreferredRFChannelTable(
                        new_profile_id,
                                                                            channel_conf_data[i].raIndex, channel_conf_data[i].preindex, channel_conf_data[i].preindex1, channel_conf_data[i].rafrequency)
                    sqlalche_obj.session.add(channel_conf_data_add)
            # print "hello20"
            sw_status_data = Odu100SwStatusTable(host_id, 1, None, None, None)
            sqlalche_obj.session.add(sw_status_data)
            # print "hello21"
            hw_desc_data = Odu100HwDescTable(host_id, 1, None, None)
            sqlalche_obj.session.add(hw_desc_data)
            # print "hello22"
            # ra mac is removed
            ru_status_data = Odu100RuStatusTable(
                host_id, 1, None, 1, None, None, None, None, 0, 0, 0)
            sqlalche_obj.session.add(ru_status_data)

            sqlalche_obj.session.commit()

            result = {'success': 0, 'result': [str(new_profile_id), 0]}
            # return new_profile_id,0
            ## For MWC this is done
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

        except Exception as e:
            import traceback
            # with open("/home/cscape/Desktop/ok",'w') as f:
          ##      f.write(traceback.format_exc())

            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def time_diff_rec_table(self, table_oid_dic, current_time):
        """

        @param table_oid_dic:
        @param current_time:
        @return:
        """
        table_dic = {}
        global time_diff
        time_diff = 0
        fmt = '%Y-%m-%d %H:%M:%S'
        a = str(current_time)
        global time_delay
        for i in table_oid_dic:
            if i == "raChannelListTable":
                continue
            table_rec_time = table_oid_dic[i][1]

            diff1 = datetime.strptime(str(table_rec_time), fmt)

            diff2 = datetime.strptime(a[:a.find('.') - 1], fmt)
            rec_time = (diff2 - diff1)
            rec_time = divmod(rec_time.days * 86400 + rec_time.seconds, 60)
            if rec_time[0] < time_diff:
                if table_oid_dic[i][0] == 0:
                    table_dic.update({i: table_oid_dic[i][2]})
            else:
                table_dic.update({i: table_oid_dic[i][2]})
        time_delay = diff1

        return table_dic

    def update_reconcilation_controller(self, host_id, device_type, table_prefix, current_time, user_name):
        # return {'success':0,'result':'good'}
        """

        @param host_id:
        @param device_type:
        @param table_prefix:
        @param current_time:
        @param user_name:
        @return: @raise:
        """
        import common_controller
        from odu_mib_model import odu100_table_model
        global essential_obj, host_status_dic, errorStatus, sqlalche_obj

        host_status = 0
        host_data = []
        table_oid_dic = {}
        table_var_bind = {}
        rec_not_done = []
        rec_done = []
        total_rec = 0
        rec = 0
        rec_per = 0
        table_result = []
        time_stamp = str(datetime.now())
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()

            firmware_result = sqlalche_obj.session.query(
                Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
            if len(firmware_result):
                firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
                if firmware:
                  table_name = "odu100_%s_oid_table" % (firmware.replace('.','_'))
                else:
                  raise Exception("Firmware version not specified for host, please edit host from inventory for more information")
            else:
                table_name = "odu100_7_2_20_oid_table"

            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            result = {'success': 0, 'result': ""}
            if host_id != None or host_id != "":

                essential_obj.host_status(host_id, 0, None, 10)
                host_op_status = essential_obj.get_hoststatus(host_id)

                if host_op_status != None or host_op_status != "":

                    if int(host_op_status) == 0:
                        essential_obj.host_status(host_id, 10)
                        if len(host_data) > 0:

                            ping_chk = snmp_ping(host_data[0].ip_address, host_data[
                                                 0].snmp_read_community, int(host_data[0].snmp_port))
                            if int(ping_chk) == 0:
                                host_data[0].reconcile_status = 1
                                sqlalche_obj.session.commit()
                                if device_type == "odu100":   # table change according to firmware version
                                    if firmware == "7.2.29":
                                        table_result = sqlalche_obj.session.query(
                                            Odu1007_2_29_oid_table).filter(Odu1007_2_29_oid_table.is_recon == 1).all()
                                    elif firmware == "7.2.25":
                                        table_result = sqlalche_obj.session.query(
                                            Odu1007_2_25_oid_table).filter(Odu1007_2_25_oid_table.is_recon == 1).all()
                                    else:
                                        table_result = sqlalche_obj.session.query(
                                            Odu1007_2_20_oid_table).filter(Odu1007_2_20_oid_table.is_recon == 1).all()
                                if len(table_result) > 0:
                                    for i in range(0, len(table_result)):
                                        table_oid_dic.update(
                                            {table_result[
                                                i].table_name: [table_result[i].status,
                                                             table_result[i].timestamp, table_result[i].table_oid]})
                                        table_var_bind.update({table_result[i].table_name:
                                                              table_result[i].varbinds})

                                    rec_table_dic = self.time_diff_rec_table(
                                        table_oid_dic, current_time)
                                    if len(rec_table_dic) > 0:
                                        total_rec = len(rec_table_dic)
                                        obj_system_config = SystemConfig()
                                        for j in rec_table_dic:
                                            if j == "raChannelListTable":
                                                continue
                                            column_list = []
                                            tablename = str(
                                                table_prefix) + str(j)
                                            sqlalche_tablename = rename_tablename(
                                                tablename)
                                            database_name = obj_system_config.get_sqlalchemy_credentials(
                                                )
                                            result_db = sqlalche_obj.db.execute(
                                                "SELECT COLUMN_NAME \
                                                FROM information_schema.COLUMNS \
                                                WHERE table_name = '%s' and table_schema = '%s'" % (tablename, database_name[4]))
                                            for columns in result_db:
                                                column_list.append(
                                                    columns["column_name"])
                                            time.sleep(2)
                                            # print j
                                            if j == "swStatusTable" or j == "omcConfTable":
                                                result = pysnmp_get_table_ap(str(rec_table_dic[j]) + str(
                                                    ".1"), host_data[0].ip_address, int(host_data[0].snmp_port), host_data[0].snmp_read_community)
                                                #logme('-----'+ j +'\n'+str(result)+'\n-----')
                                            else:
                                                #logme('\n>>>> '+ j +'\n'+str(rec_table_dic[j])+'\n-----')
                                                result = bulktable(
                                                    str(rec_table_dic[j]) + str(
                                                        ".1"), host_data[0].ip_address, int(host_data[0].snmp_port),
                                                                   host_data[0].snmp_read_community, table_var_bind[j])
                                                #logme('-----'+ j +'\n'+str(result)+'\n-----')
                                            # print result

                                            if result['success'] == 1:
                                                if j == "omcConfTable" and result['success'] == 1:
                                                    rec = rec + 1
                                                elif j == "raAclConfigTable" and result['success'] == 1:
                                                    rec = rec + 1
                                                elif j == "swStatusTable" and result['success'] == 1:
                                                    rec = rec + 1
                                                else:
                                                    for key in result['result']:
                                                        if int(key) == 553:
                                                            result['result'] = errorStatus.get(
                                                                key, "UNMP Server is busy.Please try after some time,2000")
                                                            result[
                                                                'success'] = 1
                                                            agent_start(host_data[0]
                                                                        .ip_address, 'root', 'public')
                                                            return
                                                        elif int(key) == 551:
                                                            result['result'] = errorStatus.get(
                                                                key, "UNMP Server is busy.Please try after some time,2002")
                                                            result[
                                                                'success'] = 1
                                                            return
                                                        elif int(key) == 97 or int(key) == 98 or int(key) == 99 or int(key) == 102:
                                                            result['result'] = errorStatus.get(
                                                                key, "UNMP Server is busy.Please try after some time,2002")
                                                            result[
                                                                'success'] = 1
                                                            return
                                                        elif int(key) == 5:
                                                            result['result'] = errorStatus.get(
                                                                key, "Device is busy.Please try again later")
                                                            result[
                                                                'success'] = 1
                                                            agent_start(host_data[0]
                                                                        .ip_address, 'root', 'public')
                                                            #return
                                                        elif int(key) == 24 or int(key) == 72:
                                                            result['result'] = errorStatus.get(
                                                                key, "Device is busy.Please try again later")
                                                            result[
                                                                'success'] = 1
                                                            agent_start(host_data[0]
                                                                        .ip_address, 'root', 'public')
                                                            #return
                                                        else:
                                                            if result['result'][key] != 0:
                                                                agent_start(
                                                                    host_data[
                                                                        0].ip_address,
                                                                            'root', 'public')
                                                                result['result'] = errorStatus.get(
                                                                    result['result'][key], "Device is not responding")
                                                                result[
                                                                    'success'] = 1
                                                                return
                                                    rec_not_done.append(str(j))
                                            else:
                                                if len(result['result']) == 0:
                                                    rec_done.append(str(j))
                                                    rec = rec + 1
                                                    if "config_profile_id" in column_list:
                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where config_profile_id = '%s' " % (tablename, host_data[0].config_profile_id))
                                                    else:
                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where host_id = '%s' " % (tablename, host_data[0].host_id))
                                                else:
                                                    rec_done.append(str(j))
                                                    rec = rec + 1
                                                    if "config_profile_id" in column_list:
                                                        sqlalche_table_result = sqlalche_obj.session.query(eval(sqlalche_tablename)).filter(
                                                            getattr(eval(sqlalche_tablename), "config_profile_id") == host_data[0].config_profile_id).all()

                                                    else:
                                                        sqlalche_table_result = sqlalche_obj.session.query(
                                                            eval(sqlalche_tablename)).filter(getattr(eval(sqlalche_tablename), "host_id") == host_id).all()
                                                    primary_key_id = tablename + \
                                                        "_id"
                                                    column_list.remove(
                                                        primary_key_id)
                                                    if "config_profile_id" in column_list:
                                                        column_list.remove(
                                                            "config_profile_id")
                                                        config_type = 1
                                                    else:
                                                        column_list.remove(
                                                            "host_id")
                                                        config_type = 0
                                                    if "timestamp" in column_list:
                                                        column_list.remove(
                                                            "timestamp")
                                                        timestamp = 1
                                                    else:
                                                        timestamp = 0

                                                    if j == "raAclConfigTable" or j == "peerConfigTable":
                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where config_profile_id = '%s' " % (tablename, host_data[0].config_profile_id))
                                                        time.sleep(1)
                                                        for row in result['result']:
                                                            sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" % (
                                                                tablename, host_data[0].config_profile_id, str(result["result"][row])[1:-1]))
                                                    else:
                                                        if len(sqlalche_table_result) > 0:
                                                            # print odu100_table_model[firmware][j]
                                                            # print result['result']
                                                            # print column_list

                                                            for row in result['result']:
                                                                if len(result['result'][row]) == len(column_list):
                                                                    for k in range(len(column_list)):
                                                                        setattr(sqlalche_table_result[row -
                                                                                1], column_list[k], result['result'][row][k])
                                                                        if timestamp == 1:
                                                                            setattr(sqlalche_table_result[row - 1],
                                                                                    "timestamp", time_stamp[:time_stamp.find('.') - 1])

                                                                else:
                                                                    index_val = 0
                                                                    for k in range(len(column_list)):
                                                                        if column_list[k] in odu100_table_model[firmware][j]:
                                                                            setattr(sqlalche_table_result[row - 1],
                                                                                    column_list[k], result['result'][row][index_val])
                                                                            index_val += 1
                                                                        if timestamp == 1:
                                                                            setattr(sqlalche_table_result[row - 1],
                                                                                    "timestamp", time_stamp[:time_stamp.find('.') - 1])
                                                        else:
                                                            for row in result['result']:
                                                                if config_type == 1:
                                                                    sqlalche_obj.db.execute("Insert into %s (%s,config_profile_id,%s) values(NULL,%s,%s)" % (
                                                                        tablename, primary_key_id, ",".join(column_list), host_data[0].config_profile_id, str(result['result'][row])[1:-1]))
                                                                else:
                                                                    if timestamp == 0:
                                                                        sqlalche_obj.db.execute("Insert into %s (%s,host_id,%s) values(NULL,%s,%s)" % (
                                                                            tablename, primary_key_id, ",".join(column_list), host_id, str(result['result'][row])[1:-1]))
                                                                    else:

                                                                        aa = "Insert into %s (%s,host_id,%s,timestamp) values(NULL,%s,%s,'%s')" % (
                                                                            tablename, primary_key_id, ",".join(column_list), host_id, str(result['result'][row])[1:-1], time_stamp[:time_stamp.find('.') - 1])
                                                                        sqlalche_obj.db.execute(aa)

                                        sqlalche_obj.db.execute(
                                            "Update %s set status = 0 where table_name in ('%s')" % (table_name, "\',\'".join(rec_not_done)))
                                        a = str(current_time)
                                        sqlalche_obj.db.execute("Update %s set status = 1,timestamp='%s' where table_name in ('%s')" % (
                                            table_name, a[:a.find('.') - 1], "\',\'".join(rec_done)))
                                        rec_per = (
                                            float(rec) / float(total_rec))
                                        rec_per = int(rec_per * 100)
                                        host_data[0].reconcile_health = rec_per
                                        host_data[0].reconcile_status = 2
                                        if rec_per != 0:
                                            sqlalche_obj.db.execute(
                                                "delete from odu100_raChannelListTable where host_id='%s'" % (host_id))
                                        sqlalche_obj.session.commit()
                                        el = EventLog()
                                        el.log_event(
                                            "Device Reconcilation Done", "%s" % (user_name))
                                        result = {"success": 0, "result":
                                            {rec_per: [host_data[0].host_alias, host_data[0].ip_address]}}
                                        return
                                    else:
                                        result = {'success': 1, 'result': " Reconciliation of device configuration data has been completed successfully %s You can reinitiate the process after %s minutes" % (str(time_delay), str(time_diff))}
                                        return
                                else:
                                    result = {'success': 1, 'result':
                                        "UNMP Server is busy.Please try after some time,1200"}
                                    host_data = sqlalche_obj.session.query(
                                        Hosts).filter(Hosts.host_id == host_id).all()
                                    host_data[0].reconcile_status = 0
                                    sqlalche_obj.session.commit()
                                    return
                            else:
                                if int(ping_chk) == 2:
                                    result = {
                                        'success': 1, 'result': "Network is unreachable"}
                                else:
                                    result = {'success': 1, 'result': "Reconciliation not done.No response from device " + str(host_data[0]
                                                                                                                             .host_alias) + "(" + str(host_data[0].ip_address + ")")}
                                return
                        else:
                            result = {'success': 1, 'result':
                                "UNMP Server is busy.Please try after some time,1100"}
                            return
                    else:
                        result = {'success': 1, 'result': "Device is busy, Device " + host_status_dic[
                            int(host_op_status)] + " is in progress. please wait ..."}
                        return
                else:
                    result = {'success': 1, 'result':
                        "UNMP Server is busy.Please try after some time,1000"}
                    return
            else:
                result = {'success': 1, 'result': "Host Not Exist"}
                return
        except Exception as e:
            import traceback
            result = {"success": 1, "result":
                "UNMP Server is busy.Please try after some time" + str(e)}
            logme(traceback.format_exc())
            return
        finally:
            #logme("result = "+str(result))
            essential_obj.host_status(host_id, 0, None, 10)
            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            if len(host_data) > 0:
                host_data[0].reconcile_status = 0
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    def reconcilation_controller(self, host_id, device_type, table_prefix, current_time, is_reconcile, user_name):
        """

        @param host_id:
        @param device_type:
        @param table_prefix:
        @param current_time:
        @param is_reconcile:
        @param user_name:
        @return:
        """
        global essential_obj, sqlalche_obj, host_status_dic, errorStatus
        host_status = 0
        host_data = []
        table_oid_dic = {}
        rec_not_done = []
        rec_done = []
        total_rec = 0
        rec = 0
        rec_per = 0
        config_profile_id = 0
        rec_table_dic = {}
        table_var_bind = {}
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {'success': 0, 'result': ""}
            if host_id != None or host_id != "":
                host_data = sqlalche_obj.session.query(Hosts).\
                    filter(Hosts.host_id == host_id).all()
                if len(host_data) > 0:
                    if is_reconcile == True:
                        if snmp_ping(host_data[0].ip_address, host_data[0].snmp_read_community, int(host_data[0].snmp_port)) == 0:
                            profile_id = Odu16ConfigProfiles(
                                device_type, None, 'Master', None, datetime.now(), None, datetime.now(), None, 0)
                            sqlalche_obj.session.add(profile_id)
                            sqlalche_obj.session.flush()
                            config_profile_id = profile_id.config_profile_id
                            sqlalche_obj.session.commit()
                            if device_type == "odu100":
                                table_result = sqlalche_obj.session.query(
                                    Odu100Oid_table).filter(Odu100Oid_table.is_recon == 1).all()
                            if len(table_result) > 0:
                                for i in range(0, len(table_result)):
                                    rec_table_dic.update(
                                        {table_result[i].table_name: table_result[i].table_oid})
                                    table_var_bind.update(
                                        {table_result[i].table_name: table_result[i].varbinds})
                                total_rec = len(table_result)
                                obj_system_config = SystemConfig()
                                for j in rec_table_dic:

                                    column_list = []
                                    tablename = str(table_prefix) + str(j)
                                    sqlalche_tablename = rename_tablename(
                                        tablename)
                                    database_name = obj_system_config.get_sqlalchemy_credentials(
                                        )
                                    result_db = sqlalche_obj.db.execute(
                                        "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'" % (tablename, database_name[4]))
                                    for columns in result_db:
                                        column_list.append(
                                            columns["column_name"])
                                    time.sleep(5)
                                    result = pysnmp_get_table(str(rec_table_dic[j]) + str(
                                        ".1"), host_data[0].ip_address, int(host_data[0].snmp_port), host_data[0].snmp_read_community, int(table_var_bind.get(j)))
                                    if result['success'] == 1:
                                        for key in result['result']:
                                            if int(key) == 553:

                                                result['result'] = errorStatus.get(
                                                    key, "UNMP Server is busy.Please try after some time,2000")
                                                result['success'] = 1
                                            elif int(key) == 551:
                                                result['result'] = errorStatus.get(
                                                    key, "UNMP Server is busy.Please try after some time,2001")
                                                result['success'] = 1
                                                return
                                            elif int(key) == 97 or int(key) == 98 or int(key) == 99 or int(key) == 102:
                                                result['result'] = errorStatus.get(
                                                    key, "UNMP Server is busy.Please try after some time,2002")
                                                result['success'] = 1
                                                return
                                            elif int(key) == 5 or int(key) == 24 or int(key) == 72:

                                                temp_result = self.odu100_add_default_config_profile(
                                                    host_id, device_type, table_prefix, is_reconcile)
                                                result = {'success': 0,
                                                    'result': [str(temp_result[0]), 0]}
                                                return
                                            else:
                                                if result['result'][key] != 0:
                                                    result['result'] = errorStatus.get(
                                                        result['result'][key], "UNMP Server is busy.Please try after some time,2002")
                                                    result['success'] = 1
                                        rec_not_done.append(str(j))
                                    else:
                                        if len(result['result']) == 0:
                                            rec_done.append(str(j))
                                            rec = rec + 1
                                        else:
                                            rec_done.append(str(j))
                                            rec = rec + 1
                                            primary_key_id = tablename + "_id"
                                            column_list.remove(primary_key_id)
                                            if "config_profile_id" in column_list:
                                                column_list.remove(
                                                    "config_profile_id")
                                                config_type = 1
                                            else:
                                                column_list.remove("host_id")
                                                config_type = 0
                                            if "timestamp" in column_list:
                                                column_list.remove("timestamp")
                                                timestamp = 1
                                            else:
                                                timestamp = 0
                                            for row in result['result']:
                                                if config_type == 1:
                                                    sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" % (
                                                        tablename, config_profile_id, str(result["result"][row])[1:-1]))
                                                else:
                                                    if timestamp == 0:
                                                        sqlalche_obj.db.execute(
                                                            "Insert into %s values(NULL,%s,%s)" % (tablename, host_id, str(result["result"][row])[1:-1]))
                                                    else:
                                                        time_stamp = str(
                                                            datetime.now())
                                                        sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s,'%s')" % (
                                                            tablename, host_id, str(result["result"][row])[1:-1], time_stamp[:time_stamp.find('.') - 1]))

                                sqlalche_obj.db.execute(
                                    "Update odu100_oid_table set status = 0 where table_name in ('%s')" % ("\',\'".join(rec_not_done)))
                                a = str(current_time)
                                sqlalche_obj.db.execute("Update odu100_oid_table set status = 1,timestamp='%s' where table_name in ('%s')" % (a[:
                                                        a.find('.') - 1], "\',\'".join(rec_done)))
                                rec_per = (float(rec) / float(total_rec))
                                rec_per = int(rec_per * 100)
                                host_data[0].reconcile_health = rec_per
                                host_data[0].reconcile_status = 2
                                sqlalche_obj.session.commit()
                                el = EventLog()
                                el.log_event(
                                    "Device Reconcilation Done", "%s" % (user_name))
                                result = {'success': 0,
                                    'result': [str(config_profile_id), rec_per]}
                            else:
                                result = {'success':
                                    1, 'result': [str(config_profile_id), 0]}
                                return
                        else:
                            temp_result = self.odu100_add_default_config_profile(
                                host_id, device_type, table_prefix, is_reconcile)
                            result = {'success':
                                0, 'result': [str(temp_result[0]), 0]}
                            return
                    else:
                        temp_result = self.odu100_add_default_config_profile(
                            host_id, device_type, table_prefix, is_reconcile)
                        result = {'success': 0,
                            'result': [str(temp_result[0]), 0]}
                        return
                else:
                    result = {'success': 1, 'result': [
                        str(config_profile_id), 0]}
                    return
            else:
                result = {'success': 1, 'result': "Host Not Exist"}
                return
        except Exception as e:
            result = {"success": 1, "result":
                "UNMP Server is busy.Please try after some time " + str(e)}
            return
        finally:
            if len(host_data) > 0:
                host_data[0].reconcile_status = 0
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    def odu16_add_current_config_profile(self, host_id, device_type_id, table_prefix, reconcile_chk=True):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param reconcile_chk:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        profile_id = None
        total_len_count = 52
        extra_count = 0
        less_count = 0
        reconcile_per = 0
        # sqlalche_obj.db.execute("Insert into config_profiles(device_type_id,profile_name,config_profile_type_id,parent_id)\
        # values('%s','%s','%s','%s')"%(device_type_id,None,'Master',None))

        host_data = sqlalche_obj.session.query(
            Hosts.snmp_version_id, Hosts.snmp_read_community, Hosts.ip_address, Hosts.snmp_port).filter(Hosts.host_id == host_id).all()
        # host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id ==
        # host_id).all()

        result = []
        walk = {}
        if reconcile_chk == True:
            if snmp_ping(host_data[0].ip_address, host_data[0].snmp_read_community, int(host_data[0].snmp_port)) == 0:
                config_id = Odu16ConfigProfiles(
                    device_type_id, None, 'Master', None,
                                                datetime.now(), None, datetime.now(), None, 0)
                # device_type_id,profile_name,config_profile_type_id,parent_id,timestamp,created_by,creation_time,updated_by,is_deleted
                sqlalche_obj.session.add(config_id)
                sqlalche_obj.session.flush()
                profile_id = config_id.config_profile_id
                # profile_id = Odu16ConfigProfiles.config_profile_id
                sqlalche_obj.session.commit()
                walk = snmp_walk(host_data[0][0], host_data[0][1], host_data[0]
                                 [2], host_data[0][3], '.1.3.6.1.4.1.26149.2', '-On', '-OQ')
                ### less_count count
                if walk.get('.1.3.6.1.4.1.26149.2.2.9.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.8.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.9.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.2.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.2.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.2.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.2.1.5.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.2.1.6.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.2.1.7.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1
        ##        if walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.5.1'):
        ##            ""
        ##        else:
        ##            less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.7.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.7.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.8.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.8.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.8.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.8.1.5.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.8.1.6.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.5.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.6.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.7.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.8.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.9.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.1.1'):
                    ""
                else:
                    less_count = less_count + 1
        ##        if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1'):
        ##            ""
        ##        else:
        ##            less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1'):
                    ""
                else:
                    less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.6.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.10.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.10.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.6.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.6.1.3.1'):
                    ""
                else:
                    pass
                    # less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.6.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1

        #######################################################################
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1') == 'raBW10Mhz':
                    ru_channel_bandwidth = 1
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1') == 'raBW5Mhz':
                    ru_channel_bandwidth = 0
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1') == 'raBW20Mhz':
                    ru_channel_bandwidth = 2
                else:
                    ru_channel_bandwidth = walk.get(
                        '.1.3.6.1.4.1.26149.2.2.1.1.7.1', -1)

                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.8.1') == 'internal':
                    ru_sync_source = 0
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.8.1') == 'radio1':
                    ru_sync_source = 1
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.8.1') == 'radio2':
                    ru_sync_source = 2
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.8.1') == 'gpioPIN':
                    ru_sync_source = 3
                else:
                    ru_sync_source = walk.get(
                        '.1.3.6.1.4.1.26149.2.2.1.1.8.1', -1)

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1'):
                    ""
                else:
                    less_count = less_count + 1

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1'):
                    ""
                else:
                    less_count = less_count + 1

                ru_config = SetOdu16RUConfTable(
                    profile_id, 1 if walk.get(
                        '.1.3.6.1.4.1.26149.2.2.9.1.2.1') == 'unlocked' else 0,
                                                ru_channel_bandwidth, ru_sync_source, walk.get('.1.3.6.1.4.1.26149.2.2.1.1.9.1'))
                sqlalche_obj.session.add(ru_config)
                date_time = SetOdu16RUDateTimeTable(
                    profile_id, walk.get('.1.3.6.1.4.1.26149.2.2.2.1.2.1',
                                         2000), walk.get(
                                             '.1.3.6.1.4.1.26149.2.2.2.1.3.1', 1),
                                                    walk.get('.1.3.6.1.4.1.26149.2.2.2.1.4.1', 1), walk.get(
                                                        '.1.3.6.1.4.1.26149.2.2.2.1.5.1', 0), walk.get('.1.3.6.1.4.1.26149.2.2.2.1.6.1', 20),
                                                    walk.get('.1.3.6.1.4.1.26149.2.2.2.1.7.1', 38))
                sqlalche_obj.session.add(date_time)

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.4.1') == 'disabled':
                    acl_val = 0
                elif walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.4.1') == 'accept':
                    acl_val = 1
                elif walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.4.1') == 'deny':
                    acl_val = 2
                else:
                    acl_val = walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.4.1', -1)
                ra_config = SetOdu16RAConfTable(
                    profile_id, 1 if walk.get(
                        '.1.3.6.1.4.1.26149.2.2.13.1.1.2.1') == 'unlocked' else 0,
                                                acl_val, walk.get('.1.3.6.1.4.1.26149.2.2.13.1.1.5.1', 'Shyam'))
                sqlalche_obj.session.add(ra_config)

                omc_config = SetOdu16OmcConfTable(
                    profile_id, walk.get('.1.3.6.1.4.1.26149.2.2.7.1.2.1', ''),
                                                  walk.get('.1.3.6.1.4.1.26149.2.2.7.1.3.1', 30))
                sqlalche_obj.session.add(omc_config)

                # in this some fileds are missing which we added later
                omc_registration = SetOdu16SysOmcRegistrationTable(
                    profile_id, walk.get('.1.3.6.1.4.1.26149.2.2.8.1.2.1', 'not populated'), walk.get(
                        '.1.3.6.1.4.1.26149.2.2.8.1.3.1', 'not populated'),
                                                                    walk.get('.1.3.6.1.4.1.26149.2.2.8.1.4.1', 'not populated'), walk.get(
                                                                        '.1.3.6.1.4.1.26149.2.2.8.1.5.1', 'not populated'), walk.get('.1.3.6.1.4.1.26149.2.2.8.1.6.1', 'not populated'),
                                                                    None, None, None, None, None, None, None, None, None, None, None, None)
                sqlalche_obj.session.add(omc_registration)

                syn_config = SetOdu16SyncConfigTable(
                    profile_id, 1 if walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.2.1') == 'unlocked' else 0, walk.get(
                        '.1.3.6.1.4.1.26149.2.2.11.1.1.4.1', 2),
                                                     walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.5.1', 1),
                                                     walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.6.1', 2), walk.get(
                                                         '.1.3.6.1.4.1.26149.2.2.11.1.1.7.1', 5), walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.8.1', 60),
                                                     walk.get('.1.3.6.1.4.1.26149.2.2.11.1.1.9.1', 10))
                sqlalche_obj.session.add(syn_config)

                llc_config = SetOdu16RALlcConfTable(
                    profile_id, walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1'), walk.get(
                        '.1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1'),
                                                  walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1'), walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1'), walk.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1'))
                sqlalche_obj.session.add(llc_config)

                if walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1') == 'racs24Mbps':
                    rf_coding = 1
                elif walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1') == 'racs48Mbps':
                    rf_coding = 2
                else:
                    rf_coding = 1
                tdd_mac_config = SetOdu16RATddMacConfig(
                    profile_id, walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.1.1', 5180), walk.get(
                        '.1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1', ''),
                                                      rf_coding, walk.get(
                                                          '.1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1', 10),
                                                      walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1', 1000), walk.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1', 5))
                sqlalche_obj.session.add(tdd_mac_config)

                for i in range(0, 8):
                    if (walk.get(".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1))):
                        ""
                    else:
                        less_count = less_count + 1
                    if (walk.get(".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1)) == '""') or (walk.get(".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1)) == ''):
                        peer_config = SetOdu16PeerConfigTable(
                            profile_id, '', int(i + 1))
                        sqlalche_obj.session.add(peer_config)
                    else:
                        peer_config = SetOdu16PeerConfigTable(profile_id, walk.get(
                            ".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1)), int(i + 1))
                        sqlalche_obj.session.add(peer_config)
                j = 0
                if ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1) in walk:
                    while(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1) in walk):
                        if (walk.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == '"                  "') or (walk.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == '""') or (walk.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == ''):
                            acl_config = SetOdu16RAAclConfigTable(
                                profile_id, '', int(j + 1))
                            sqlalche_obj.session.add(acl_config)

                        else:
                            acl_config = SetOdu16RAAclConfigTable(profile_id, walk.get(
                                ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)), int(j + 1))
                            sqlalche_obj.session.add(acl_config)

                        j = int(j + 1)
                        extra_count = extra_count + 1
                else:
                    for k in range(0, 10):
                        acl_config = SetOdu16RAAclConfigTable(
                            profile_id, '', int(k + 1))
                        sqlalche_obj.session.add(acl_config)
                    # extra_count = extra_count + 1
                    # less_count = less_count + 1
                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.3.1') == "enabled":
                    op_state = 1
                else:
                    op_state = 0

                if walk.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "rootRU":
                    node_type = 0
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "t1TDN":
                    node_type = 1
                elif walk.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "t2TDN":
                    node_type = 2
                else:
                    node_type = 3
                get_ru_conf_add = GetOdu16_ru_conf_table(
                    host_id, op_state, walk.get(
                        '.1.3.6.1.4.1.26149.2.2.1.1.4.1'),
                                                         node_type, walk.get('.1.3.6.1.4.1.26149.2.2.1.1.6.1'))

                sqlalche_obj.session.add(get_ru_conf_add)

                get_hw_desc_table = GetOdu16HWDescTable(host_id, walk.get(
                    '.1.3.6.1.4.1.26149.2.2.10.1.2.1'), walk.get('.1.3.6.1.4.1.26149.2.2.10.1.3.1'))
                sqlalche_obj.session.add(get_hw_desc_table)

                get_sw_status_table = GetOdu16SWStatusTable(host_id, walk.get(
                    '.1.3.6.1.4.1.26149.2.2.6.1.2.1'), walk.get('.1.3.6.1.4.1.26149.2.2.6.1.3.1'), walk.get('.1.3.6.1.4.1.26149.2.2.6.1.4.1'))
                sqlalche_obj.session.add(get_sw_status_table)

                sqlalche_obj.session.commit()
                total_len_count = total_len_count + extra_count
                less_count = total_len_count - less_count
                reconcile_per = (float(less_count) / float(total_len_count))
                reconcile_per = int(reconcile_per * 100)
                # host_data[0].reconcile_health = reconcile_per

                result.append(profile_id)
                sqlalche_obj.sql_alchemy_db_connection_close()
                return str(profile_id), reconcile_per
            else:
                host_data[0].reconcile_status = 0
                sqlalche_obj.session.commit()
                config_profile_id, reconcile_per = self.odu16_add_default_config_profile(
                    host_id, device_type_id, table_prefix, reconcile_chk)
                return str(config_profile_id), reconcile_per
        else:
            config_profile_id, reconcile_per = self.odu16_add_default_config_profile(
                host_id, device_type_id, table_prefix, reconcile_chk)
            return str(config_profile_id), reconcile_per

    def odu16_reconcilation_controller_update(self, host_id, device_type_id, table_prefix, insert_update, user_name):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param insert_update:
        @param user_name:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        if host_id != "" or host_id != None:
            device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_read_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id, Hosts.reconcile_health).\
                filter(Hosts.host_id == host_id).all()
        result = {}
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        host_data[0].reconcile_status = 1
        sqlalche_obj.session.commit()
        result = snmp_walk(device_param_list[0][0], device_param_list[0][1], device_param_list[
                           0][2], device_param_list[0][3], '.1.3.6.1.4.1.26149.2', '-On', '-OQ')

        if result == {}:
            result = ""
            result = {'success': 1, 'result': "Reconciliation not done.No response from device " + str(
                host_data[0].host_alias) + "(" + str(host_data[0].ip_address + ")")}
            host_data[0].reconcile_health = 0
            host_data[0].reconcile_status = 0
            sqlalche_obj.session.commit()
            return result
        else:
            total_len_count = 52
            extra_count = 0
            less_count = 0
            reconcile_per = 0
            if result.get('.1.3.6.1.4.1.26149.2.2.9.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.8.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.9.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.2.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.2.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.2.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.2.1.5.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.2.1.6.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.2.1.7.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.1.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.1.1.2.1'):
                ""
            else:
                less_count = less_count + 1

##            if result.get('.1.3.6.1.4.1.26149.2.2.13.1.1.5.1'):
##                ""
##            else:
##                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.7.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.7.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.8.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.8.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.8.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.8.1.5.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.8.1.6.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.5.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.6.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.7.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.8.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.11.1.1.9.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.1.1'):
                ""
            else:
                less_count = less_count + 1

##            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1'):
##                ""
##            else:
##                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.6.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.10.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.10.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.6.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.6.1.3.1'):
                ""
            else:
                pass
                # less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.6.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1'):
                ""
            else:
                less_count = less_count + 1

            if result.get('.1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1'):
                ""
            else:
                less_count = less_count + 1

            ru_conf = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(
                SetOdu16RUConfTable.config_profile_id == device_param_list[0][4]).all()
            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1') == 'raBW10Mhz':
                ru_conf[0].channel_bandwidth = 1
            elif result.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1') == 'raBW5Mhz':
                ru_conf[0].channel_bandwidth = 0
            elif result.get('.1.3.6.1.4.1.26149.2.2.1.1.7.1') == 'raBW20Mhz':
                ru_conf[0].channel_bandwidth = 2
            if result.get(".1.3.6.1.4.1.26149.2.2.1.1.9.1"):
                ru_conf[0].country_code = result.get(
                    ".1.3.6.1.4.1.26149.2.2.1.1.9.1")

            datetime = sqlalche_obj.session.query(SetOdu16RUDateTimeTable).filter(
                SetOdu16RUDateTimeTable.config_profile_id == device_param_list[0][4]).all()
            if result.get(".1.3.6.1.4.1.26149.2.2.2.1.2.1"):
                datetime[0].year = result.get(".1.3.6.1.4.1.26149.2.2.2.1.2.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.2.1.3.1"):
                datetime[0].month = result.get(
                    ".1.3.6.1.4.1.26149.2.2.2.1.3.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.2.1.4.1"):
                datetime[0].day = result.get(".1.3.6.1.4.1.26149.2.2.2.1.4.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.2.1.5.1"):
                datetime[0].hour = result.get(".1.3.6.1.4.1.26149.2.2.2.1.5.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.2.1.6.1"):
                datetime[0].min = result.get(".1.3.6.1.4.1.26149.2.2.2.1.6.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.2.1.7.1"):
                datetime[0].sec = result.get(".1.3.6.1.4.1.26149.2.2.2.1.7.1")

            omc_config = sqlalche_obj.session.query(SetOdu16OmcConfTable).filter(
                SetOdu16OmcConfTable.config_profile_id == device_param_list[0][4]).all()
            if result.get(".1.3.6.1.4.1.26149.2.2.7.1.2.1"):
                omc_config[0].omc_ip_address = result.get(
                    ".1.3.6.1.4.1.26149.2.2.7.1.2.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.7.1.3.1"):
                omc_config[0].periodic_stats_timer = result.get(
                    ".1.3.6.1.4.1.26149.2.2.7.1.3.1")

            omc_registration = sqlalche_obj.session.query(SetOdu16SysOmcRegistrationTable).filter(
                SetOdu16SysOmcRegistrationTable.config_profile_id == device_param_list[0][4]).all()
            if result.get(".1.3.6.1.4.1.26149.2.2.8.1.2.1"):
                omc_registration[0].sys_omc_register_contact_addr = result.get(
                    ".1.3.6.1.4.1.26149.2.2.8.1.2.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.8.1.3.1"):
                omc_registration[0].sys_omc_register_contact_person = result.get(
                    ".1.3.6.1.4.1.26149.2.2.8.1.3.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.8.1.4.1"):
                omc_registration[0].sys_omc_register_contact_mobile = result.get(
                    ".1.3.6.1.4.1.26149.2.2.8.1.4.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.8.1.5.1"):
                omc_registration[0].sys_omc_register_alternate_contact = result.get(
                    ".1.3.6.1.4.1.26149.2.2.8.1.5.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.8.1.6.1"):
                omc_registration[0].sys_omc_register_contact_email = result.get(
                    ".1.3.6.1.4.1.26149.2.2.8.1.6.1")

            syn_config = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
                SetOdu16SyncConfigTable.config_profile_id == device_param_list[0][4]).all()
            if result.get(".1.3.6.1.4.1.26149.2.2.11.1.1.4.1"):
                syn_config[0].raster_time = result.get(
                    ".1.3.6.1.4.1.26149.2.2.11.1.1.4.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.11.1.1.5.1"):
                syn_config[0].num_slaves = result.get(
                    ".1.3.6.1.4.1.26149.2.2.11.1.1.5.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.11.1.1.6.1"):
                syn_config[0].sync_loss_threshold = result.get(
                    ".1.3.6.1.4.1.26149.2.2.11.1.1.6.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.11.1.1.7.1"):
                syn_config[0].leaky_bucket_timer = result.get(
                    ".1.3.6.1.4.1.26149.2.2.11.1.1.7.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.11.1.1.8.1"):
                syn_config[0].sync_lost_timeout = result.get(
                    ".1.3.6.1.4.1.26149.2.2.11.1.1.8.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.11.1.1.9.1"):
                syn_config[0].sync_config_time_adjust = result.get(
                    ".1.3.6.1.4.1.26149.2.2.11.1.1.9.1")

            llc_config = sqlalche_obj.session.query(SetOdu16RALlcConfTable).filter(
                SetOdu16RALlcConfTable.config_profile_id == device_param_list[0][4]).all()
            llc_config[0].llc_arq_enable = result[
                ".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1"]
            llc_config[0].arq_win = result[
                ".1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1"]
            llc_config[0].frame_loss_threshold = result[
                ".1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1"]
            llc_config[0].leaky_bucket_timer_val = result[
                ".1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1"]
            llc_config[0].frame_loss_timeout = result[
                ".1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1"]

            tddmac_config = sqlalche_obj.session.query(SetOdu16RATddMacConfig).filter(
                SetOdu16RATddMacConfig.config_profile_id == device_param_list[0][4]).all()
            if result.get('.1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1') == 'racs24Mbps':
                tddmac_config[0].rfcoding = 1
            else:
                tddmac_config[0].rfcoding = 2
            if result.get(".1.3.6.1.4.1.26149.2.2.13.7.1.1.1.1"):
                tddmac_config[0].rf_channel_frequency = result.get(
                    ".1.3.6.1.4.1.26149.2.2.13.7.1.1.1.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1"):
                tddmac_config[0].tx_power = result.get(
                    ".1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.13.7.1.1.5.1"):
                tddmac_config[0].max_power = result.get(
                    ".1.3.6.1.4.1.26149.2.2.13.7.1.1.5.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1"):
                tddmac_config[0].max_crc_errors = result.get(
                    ".1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1")
            if result.get(".1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1"):
                tddmac_config[0].leaky_bucket_timer_value = result.get(
                    ".1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1")

            peer_config = sqlalche_obj.session.query(SetOdu16PeerConfigTable).filter(
                SetOdu16PeerConfigTable.config_profile_id == device_param_list[0][4]).all()
            for i in range(0, len(peer_config)):
                if (result.get(".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1)) == '""') or (result.get(".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1)) == ''):
                    peer_config[i].peer_mac_address = ''
                    peer_config[i].index = int(i + 1)
                elif result.get(".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1)):
                    peer_config[i].peer_mac_address = result.get(
                        ".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s" % (i + 1))
                    peer_config[i].index = int(i + 1)
                else:
                    less_count = less_count + 1

            acl_config = sqlalche_obj.session.query(SetOdu16RAAclConfigTable).filter(
                SetOdu16RAAclConfigTable.config_profile_id == device_param_list[0][4]).all()

            j = 0
            if ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1) in result:
                while(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1) in result):
                    if j < len(acl_config):
                        # print
                        # result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s"%(j+1))
                        if (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == '"                  "') or (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == '""') or (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == ''):
                            acl_config[j].mac_address = ''
                            acl_config[j].index = int(j + 1)
                        elif result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)):

                            acl_config[j].mac_address = result.get(
                                ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1))
                            acl_config[j].index = int(j + 1)
                        else:
                            less_count = less_count + 1
                    else:
                        if (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == '"                  "') or (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == '""') or (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)) == ''):
                            add_acl_config = SetOdu16RAAclConfigTable(
                                device_param_list[0][4], '', int(j + 1))
                            sqlalche_obj.session.add(add_acl_config)
                        else:
                            add_acl_config = SetOdu16RAAclConfigTable(device_param_list[0][4], result.get(
                                ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (j + 1)), int(j + 1))
                            sqlalche_obj.session.add(add_acl_config)
                        extra_count = extra_count + 1

                    j = j + 1
            else:
                for k in range(0, 10):
                    acl_config[k].mac_address = ''
                    acl_config[k].index = int(k + 1)
                # extra_count = extra_count + 1
                less_count = less_count + 1

            get_odu16_ru_conf = sqlalche_obj.session.query(
                GetOdu16_ru_conf_table).filter(Hosts.host_id == host_id).all()
            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.3.1') == "enabled":
                get_odu16_ru_conf[0].op_state = 1
            elif result.get('.1.3.6.1.4.1.26149.2.2.1.1.3.1') == "disabled":
                get_odu16_ru_conf[0].op_state = 0

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "rootRU":
                get_odu16_ru_conf[0].default_node_type = 0
            elif result.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "t1TDN":
                get_odu16_ru_conf[0].default_node_type = 1
            elif result.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "t2TDN":
                get_odu16_ru_conf[0].default_node_type = 2
            elif result.get('.1.3.6.1.4.1.26149.2.2.1.1.5.1') == "t3TDN":
                get_odu16_ru_conf[0].default_node_type = 3

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.4.1'):
                get_odu16_ru_conf[0].object_model_version = result.get(
                    '.1.3.6.1.4.1.26149.2.2.1.1.4.1')

            if result.get('.1.3.6.1.4.1.26149.2.2.1.1.6.1'):
                get_odu16_ru_conf[0].no_radio_interfaces = result.get(
                    '.1.3.6.1.4.1.26149.2.2.1.1.6.1')

            get_odu16_sw_status = sqlalche_obj.session.query(
                GetOdu16SWStatusTable).filter(Hosts.host_id == host_id).all()
            if len(get_odu16_sw_status) > 0:
                get_odu16_sw_status[0].active_version = result.get(
                    '.1.3.6.1.4.1.26149.2.2.6.1.2.1')
                get_odu16_sw_status[0].passive_version = result.get(
                    '.1.3.6.1.4.1.26149.2.2.6.1.3.1')
                get_odu16_sw_status[0].bootloader_version = result.get(
                    '.1.3.6.1.4.1.26149.2.2.6.1.4.1')

            get_odu16_hw_desc = sqlalche_obj.session.query(
                GetOdu16HWDescTable).filter(Hosts.host_id == host_id).all()
            if len(get_odu16_hw_desc) > 0:
                get_odu16_hw_desc[0].hw_version = result.get(
                    '.1.3.6.1.4.1.26149.2.2.10.1.2.1')
                get_odu16_hw_desc[0].hw_serial_no = result.get(
                    '.1.3.6.1.4.1.26149.2.2.10.1.3.1')

            total_len_count = total_len_count + extra_count
            less_count = total_len_count - less_count
            reconcile_per = (float(less_count) / float(total_len_count))
            reconcile_per = int(reconcile_per * 100)
            host_data[0].reconcile_health = reconcile_per
            # time.sleep(10)
            host_data[0].reconcile_status = 2
            sqlalche_obj.session.commit()
            time.sleep(3)
            host_data[0].reconcile_status = 0
            el = EventLog()
            el.log_event("Device Reconcilation Done", "%s" % (user_name))
            sqlalche_obj.session.commit()
            result = {"success": 0, "result": {reconcile_per: [
                host_data[0].host_alias, host_data[0].ip_address]}}
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result
##            if insert_update == 'imgodu16':
##                #time.sleep(10)
##                host_data[0].reconcile_status = 2
##                sqlalche_obj.session.commit()
##                time.sleep(5)
##                host_data[0].reconcile_status = 0
##                sqlalche_obj.session.commit()
##                sqlalche_obj.sql_alchemy_db_connection_close()
##                return reconcile_per
##            else:
##                time.sleep(10)
##                host_data[0].reconcile_status = 2
##                sqlalche_obj.session.commit()
##                time.sleep(5)
##                sqlalche_obj.sql_alchemy_db_connection_close()
##                return 1
##                if reconcile_per >= 90:
##                    return "Reconcilation done Succesfully"
##                else:
# return "%s Reconcilation Done.Please Reconcile Again"%(reconcile_per)

    def reconcilation_chk_status(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            global sqlalche_obj
            result = {}
            if host_id != "" or host_id != None:
                sqlalche_obj.sql_alchemy_db_connection_open()
                reconcile_status = sqlalche_obj.session.query(
                    Hosts.reconcile_status, Hosts.reconcile_health).filter(Hosts.host_id == host_id).all()
                reconcile_update = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                status = reconcile_status[0].reconcile_status
                if reconcile_status[0].reconcile_status == 2:
                    reconcile_update[0].reconcile_status = 0
                    sqlalche_obj.session.commit()
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    result = {"result": [status,
                        reconcile_status[0].reconcile_health], "success": 0}
                    return result
                else:
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    result = {"result": [status], "success": 0}
                    return result
            else:
                result = {"result": 3, "success": 0}
                return result
        except Exception as e:
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def list_reconciliation(self):
        """


        @return:
        """
        try:
            global sqlalche_obj
            result = {}
            rec_dir = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            rec_list = sqlalche_obj.session.query(
                Hosts.host_id, Hosts.reconcile_status, Hosts.reconcile_health).filter(Hosts.device_type_id.like("odu%")).all()
            sqlalche_obj.sql_alchemy_db_connection_close()
            for i in range(0, len(rec_list)):
                rec_dir[str(rec_list[i][0])] = [rec_list[i][1], rec_list[i][2]]
                # rec_tuple.append(rec_list[i][1])
            result = {"result": rec_dir, "success": 0}
            return result
        except Exception as e:
            return str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def reboot(self, host_id, device_type_id):
        """

        @param host_id:
        @param device_type_id:
        @return:
        """
        global sqlalche_obj
        result = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        oid_dict = {}
        oid_dict[1] = ['1.3.6.1.4.1.26149.2.2.5.1.2.1', 'Integer32', 5]
        host_param = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(host_param) > 0:
            snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7', host_param[0].ip_address, int(host_param[0]
                                         .snmp_port), host_param[0].snmp_read_community)
            if snmp_get_result['success'] == 0:
                if int(snmp_get_result['result'].values()[0]) == 1:
                    snmp_get_om_operation = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.2', host_param[0].ip_address, int(
                        host_param[0].snmp_port), host_param[0].snmp_read_community)
                    if snmp_get_om_operation['success'] == 0:
                        if int(snmp_get_om_operation['result'].values()[0]) == 1:
                            msg = "Software download operation is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 2:
                            msg = "Software  Activation is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 3:
                            msg = "Factory reset is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 4:
                            msg = "Commit to Flash is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 6:
                            msg = "Another Site Survey is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 7:
                            msg = "Bandwidth calculator is running.Please wait to complete that operation..."
                        else:
                            msg = "Some other operation is running.Please wait to complete that operation..."
                        result = {"success": 1, "result": msg, "flag": "1"}
                        return result
                    else:
                        if 553 in snmp_get_om_operation["result"]:
                            result = {"success": 1, "result":
                                "No Response From Device.Please Try Again", "flag": "1"}
                        elif 551 in snmp_get_om_operation["result"]:
                            result = {"success": 1,
                                "result": "Network is unreachable", "flag": "1"}
                        elif 99 in snmp_get_om_operation["result"]:
                            result = {"success": 1, "result":
                                "UNMP Server is busy.Please Retry again", "flag": "1"}
                        else:
                            return snmp_get_om_operation
                        return result
                else:
                    result = pysnmp_set1(host_param[0].ip_address, int(
                        host_param[0].snmp_port), host_param[0].snmp_write_community, oid_dict[1])
                    time.sleep(5)
                    result['flag'] = 0
                    delete_site_survey_list(host_id)
                    return result
            else:
                if 553 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "No Response From Device.Please Try Again", "flag": "1"}
                elif 551 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "Network is unreachable", "flag": "1"}
                elif 99 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "UNMP Server is busy.Please Retry again", "flag": "1"}
                else:
                    return snmp_get_result
                return result
        else:
            return {"success": 1, "result": "Host Data Not Exist"}

    def chk_ping(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        if host_id != "" or host_id != None:
            device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_read_community, Hosts.config_profile_id).\
                filter(Hosts.host_id == host_id).one()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if snmp_ping(device_param_list[0], device_param_list[2], int(device_param_list[1])) == 0:
            return 0
        else:
            return 1

# obj = OduReconcilation()
# print obj.odu100_acl_reconciliation(12,'odu100')
# print obj.odu100_add_default_config_profile(28,'odu100','odu100_',datetime.now(),True,"")
# print obj.reboot(3,'odu100')
# update_reconcilation_controller(self,host_id,device_type,table_prefix,current_time,user_name):
# print 'reconcilation call'
# print obj.update_reconcilation_controller(11,'odu100','odu100_',datetime.now(),"omdadmin")
# print
# obj.reconcilation_controller(26,'odu100','odu100_',datetime.now(),True,"anuj")


class SiteSurvey(object):
    """
    ODU device Site Survey functionality
    """

##    def site_survey(self,host_id,node_type):
##        global sqlalche_obj
##        try:
##            #print "hello"
##            obj_system_config = SystemConfig()
##            database_credentials = obj_system_config.get_sqlalchemy_credentials()
##            site_survey_table = []
##            site_survey_channel_table = []
##            column_list = []
##            result_node_type = True
##            channel_number = []
##            sqlalche_obj.sql_alchemy_db_connection_open()
##            result_db  = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'"%('odu100_raSiteSurveyResultTable',database_credentials[4]))
##            for row in result_db:
##                column_list.append(row["column_name"])
##            device_param_list = sqlalche_obj.session.query(Hosts).\
##                                filter(Hosts.host_id == host_id).all()
##            snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7',device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
##
##            #print snmp_get_result
##
##            if int(snmp_get_result['success'])==0:
##                #print snmp_get_result['result'].values()[0],"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
##                if int(snmp_get_result['result'].values()[0]) == 2 or int(snmp_get_result['result'].values()[0]) == 0 or int(snmp_get_result['result'].values()[0]) == 3:
##                    snmp_result = pysnmp_set({'omoperation':('1.3.6.1.4.1.26149.2.2.5.1.2.1','Integer32',6)},device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_write_community)
##                    #print snmp_result
##                    if ((snmp_result['success']==1 and 553 in int(snmp_result['result'])) or snmp_result['success']==0):
##                        time.sleep(2)
##                        while(result_node_type):
##                            if int(node_type)==1 or int(node_type)==3:
##                                snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7',device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
##                                #print snmp_get_result
##                                if snmp_get_result['success']==1:
##                                    if 553 in snmp_get_result['result']:
##                                        time.sleep(10)
##                                        continue
##                                    else:
##                                        if 551 in snmp_get_result["result"]:
##                                            result =  {"success":1,"result":"Network is unreachable"}
##                                            return result
##                                        elif 99 in result["result"]:
##                                            result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
##                                            return result
##                                        else:
##                                            return snmp_get_result["result"]
##
##                                elif int(snmp_get_result['success'])==0:
##                                    if int(snmp_get_result['result'].values()[0])!=1:
##                                        result_node_type = False
##                                        break
##                                    else:
##                                        time.sleep(10)
##                                        continue
##                            else:
##                                time.sleep(5)
##                                snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7',device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
##                                #print snmp_get_result
##                                if snmp_get_result['success']==0:
##                                    for key in snmp_get_result['result']:
##                                        if int(snmp_get_result['result'][key]) == 1:
##                                            flag = 0
##                                        elif int(snmp_get_result['result'][key]) == 2:
##                                            flag = 1
##                                        else:
##                                            if 553 in snmp_get_result["result"]:
##                                                result =  {"success":1,"result":"Network is unreachable"}
##                                                return result
##                                            if 551 in snmp_get_result["result"]:
##                                                result =  {"success":1,"result":"Network is unreachable"}
##                                                return result
##                                            elif 99 in snmp_get_result["result"]:
##                                                result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
##                                                return result
##                                            result_node_type = False
##                                            break
##                                    if flag == 0:
##                                        time.sleep(10)
##                                        continue
##                                    else:
##                                        result_node_type = False
##                                        time.sleep(5)
##                                        break
##                        site_survey_table = sqlalche_obj.session.query(Odu100RaSiteSurveyResultTable).filter(Odu100RaSiteSurveyResultTable.host_id == device_param_list[0].host_id).all()
##                        #print site_survey_table,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
##                        result = bulktable('1.3.6.1.4.1.26149.2.2.13.11.1',device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
##                        #print result,"#################################"
##                        if result['success']==0:
##                            if site_survey_table!=[] or len(site_survey_table)>0:
##                                column_list.remove('odu100_raSiteSurveyResultTable_id')
##                                column_list.remove('host_id')
##                                for i in result["result"]:
##                                    site_survey_channel_table = sqlalche_obj.session.query(Odu100RaSiteSurveyResultTable).filter(and_(Odu100RaSiteSurveyResultTable.host_id == device_param_list[0].host_id,Odu100RaSiteSurveyResultTable.channelnumber==result["result"][i][9])).all()
##                                    channel_number.append(str(result["result"][i][9]))
##                                    if site_survey_channel_table !=[] or len(site_survey_channel_table)>0:
##                                        for k in range(0,len(column_list)):
##                                            temp_result = str(result["result"][i][k])
##                                            exec "site_survey_table[%s].%s = '%s'"%(i-1,column_list[k],temp_result[:-1] if temp_result.count('\n') else temp_result)
##                                    else:
##                                        sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%('odu100_raSiteSurveyResultTable',host_id,str(result["result"][i])[1:-1]))
##                                sqlalche_obj.session.commit()
##                                time.sleep(1)
##                            else:
##                                for i in range(0,len(result["result"])):
##                                    sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%('odu100_raSiteSurveyResultTable',host_id,str(result["result"][i+1])[1:-1]))
##                                time.sleep(1)
##                            sqlalche_obj.db.execute("delete from odu100_raSiteSurveyResultTable where channelnumber NOT IN (%s) and host_id='%s'"%(",".join(channel_number),host_id))
##                            result = {'success':0,'result':"Calculating Site Survey Results has successfully completed."}
##                            #print "sab sahi hua"
##                            sqlalche_obj.session.commit()
##                            return result
##                        else:
##                            sqlalche_obj.session.commit()
##                            if 553 in result["result"]:
##                                result = {"success":1,"result":"No Response From Device.Please Try Again"}
##                            elif 551 in result["result"]:
##                                result =  {"success":1,"result":"Network is unreachable"}
##                            elif 99 in result["result"]:
##                                result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
##                            else:
##                                return result
##                            return result
##
##                    else:
##                        if 553 in snmp_result["result"]:
##                            result = {"success":1,"result":"No Response From Device.Please Try Again"}
##                        elif 551 in snmp_result["result"]:
##                            result =  {"success":1,"result":"Network is unreachable"}
##                        elif 99 in snmp_result["result"]:
##                            result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
##                        else:
##                            return snmp_result
##                        return result
##                else:
##                    #{'result': {'1.3.6.1.4.1.26149.2.2.5.1.7': '2'}, 'success': 0}
##                    snmp_get_om_operation = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.2',device_param_list[0].ip_address,int(device_param_list[0].snmp_port),device_param_list[0].snmp_read_community)
##                    #print snmp_get_om_operation
##                    if snmp_get_om_operation['success']==0:
##                        if int(snmp_get_om_operation['result'].values()[0]) == 1:
##                            msg = "Software  Download is running.Please wait to complete that operation..."
##                        elif int(snmp_get_om_operation['result'].values()[0]) == 2:
##                            msg = "Software  Activation is running.Please wait to complete that operation..."
##                        elif int(snmp_get_om_operation['result'].values()[0]) == 3:
##                            msg = "Factory reset is running.Please wait to complete that operation..."
##                        elif int(snmp_get_om_operation['result'].values()[0]) == 4:
##                            msg = "Commit to Flash is running.Please wait to complete that operation..."
##                        elif int(snmp_get_om_operation['result'].values()[0]) == 5:
##                            msg = "Device is rebooting.Please wait to complete that operation..."
##                        elif int(snmp_get_om_operation['result'].values()[0]) == 6:
##                            msg = "Another Site Survey is running.Please wait to complete that operation..."
##                        elif int(snmp_get_om_operation['result'].values()[0]) == 7:
##                            msg = "Bandwidth calculator is running.Please wait to complete that operation..."
##                        else:
##                            msg = "Some operation is running.Please wait to complete that operation..."
##                        result = {"success":1,"result":msg}
##                    else:
##                        if 553 in snmp_get_om_operation["result"]:
##                            result = {"success":1,"result":"No Response From Device.Please Try Again"}
##                        elif 551 in snmp_get_om_operation["result"]:
##                            result =  {"success":1,"result":"Network is unreachable"}
##                        elif 99 in snmp_get_om_operation["result"]:
##                            result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
##                        else:
##                            return snmp_get_om_operation
##                    return result
##            else:
##                if 553 in snmp_get_result["result"]:
##                    result = {"success":1,"result":"No Response From Device.Please Try Again"}
##                    return result
##                elif 551 in snmp_get_result["result"]:
##                    result =  {"success":1,"result":"Network is unreachable"}
##                    return result
##                elif 99 in snmp_get_result["result"]:
##                    result = {"success":1,"result":"UNMP has encountered an unexpected error. Please Retry"}
##                    return result
##                else:
##                    return snmp_get_result
##
##        except OperationalError as e:
##            return {"success":1,"result":"UNMP Database Server is Busy at the moment, please try again later.","detail":str(e)}
##        except DisconnectionError as e:
##            return {"success":1,"result":"Database Disconnected","detail":""}
##        except Exception as e:
##            return {'success':1,'result':"UNMP Web Server is Busy at the moment, please try again later"}
##
##        finally:
##            sqlalche_obj.sql_alchemy_db_connection_close()

    def site_survey(self, host_id, node_type, list_of_channels):
        """

        @param host_id:
        @param node_type:
        @param list_of_channels:
        @return:
        """
        global sqlalche_obj
        try:
            # print "hello"
            obj_system_config = SystemConfig()
            database_credentials = obj_system_config.get_sqlalchemy_credentials(
                )
            site_survey_table = []
            site_survey_channel_table = []
            column_list = []
            result_node_type = True
            channel_number = []

            flag = 0
            sqlalche_obj.sql_alchemy_db_connection_open()
            result_db = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'" %
                                                 ('odu100_raSiteSurveyResultTable', database_credentials[4]))
            for row in result_db:
                column_list.append(row["column_name"])
            device_param_list = sqlalche_obj.session.query(Hosts).\
                filter(Hosts.host_id == host_id).all()
            snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7', device_param_list[0].ip_address, int(
                device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)

            # print snmp_get_result,"\n\n\n"

            if int(snmp_get_result['success']) == 0:
                # sqlalche_obj.db.execute("delete from odu100_raSiteSurveyResultTable where host_id='%s'"%(host_id))
                # print
                # snmp_get_result['result'].values()[0],"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                if int(snmp_get_result['result'].values()[0]) == 2 or int(snmp_get_result['result'].values()[0]) == 0 or int(snmp_get_result['result'].values()[0]) == 3:
                    snmp_result = pysnmp_set(
                        {'omoperation': ('1.3.6.1.4.1.26149.2.2.5.1.2.1', 'Integer32', 6), 'loc': (
                            '1.3.6.1.4.1.26149.2.2.5.1.9.1', 'OctetString', list_of_channels)},
                                             device_param_list[0].ip_address, int(device_param_list[0].snmp_port), device_param_list[0].snmp_write_community)

                    # print "\n\n\n",snmp_result,"\n\n\n"

                    if ((snmp_result['success'] == 1 and 553 in int(snmp_result['result'])) or snmp_result['success'] == 0):
                        time.sleep(2)
                        temp_result = snmp_result['result']
                        for value in temp_result:
                            if temp_result[value] == 0:
                                pass
                            else:
                                result = {"success": 1, "result":
                                    "  " + str(errorStatus.get(temp_result[value]))}
                                return result

                        while(result_node_type):
                            if int(node_type) == 1 or int(node_type) == 3:
                                # print result_node_type,"\n\n"
                                snmp_get_result = pysnmp_get(
                                    '1.3.6.1.4.1.26149.2.2.5.1.7', device_param_list[
                                        0].ip_address,
                                                             int(device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
                                # print "\n\n\n",snmp_get_result,"\n\n\n"
                                if snmp_get_result['success'] == 1:
                                    if 553 in snmp_get_result['result']:
                                        time.sleep(10)
                                        continue
                                    else:
                                        if 551 in snmp_get_result["result"]:
                                            result = {"success": 1,
                                                "result": "Device is unreachable at the moment."}
                                            return result
                                        elif 99 in result["result"]:
                                            result = {"success": 1,
                                                "result": "UNMP has encountered an unexpected error. Please Retry"}
                                            return result
                                        else:

                                            return snmp_get_result["result"]

                                elif int(snmp_get_result['success']) == 0:
                                    if int(snmp_get_result['result'].values()[0]) != 1:
                                        result_node_type = False
                                        break
                                    else:
                                        time.sleep(10)
                                        continue
                            else:
                                time.sleep(5)
                                snmp_get_result = pysnmp_get(
                                    '1.3.6.1.4.1.26149.2.2.5.1.7', device_param_list[
                                        0].ip_address,
                                                             int(device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
                                # print snmp_get_result
                                if snmp_get_result['success'] == 0:
                                    for key in snmp_get_result['result']:
                                        if int(snmp_get_result['result'][key]) == 1:
                                            flag = 0
                                        elif int(snmp_get_result['result'][key]) == 2:
                                            flag = 1
                                        else:
                                            if 553 in snmp_get_result["result"]:
                                                result = {"success": 1,
                                                    "result": "Network is unreachable"}
                                                return result
                                            elif 551 in snmp_get_result["result"]:
                                                result = {"success": 1,
                                                    "result": "Network is unreachable"}
                                                return result
                                            elif 99 in snmp_get_result["result"]:
                                                result = {"success": 1, "result":
                                                    "UNMP has encountered an unexpected error. Please Retry"}
                                                return result
                                            else:
                                                result = {"success": 1, "result":
                                                    errorStatus.get(snmp_get_result["result"][key], "")}
                                            result_node_type = False
                                            break
                                    if flag == 0:
                                        time.sleep(10)
                                        continue
                                    else:
                                        result_node_type = False
                                        time.sleep(5)
                                        break
                        # site_survey_table = sqlalche_obj.session.query(Odu100RaSiteSurveyResultTable).filter(Odu100RaSiteSurveyResultTable.host_id == device_param_list[0].host_id).all()
                        # print
                        # site_survey_table,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        result = bulktable('1.3.6.1.4.1.26149.2.2.13.11.1', device_param_list[0].ip_address, int(
                            device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
                        # print result,"#################################"
                        if result['success'] == 0:
                            sqlalche_obj.db.execute(
                                "delete from odu100_raSiteSurveyResultTable where host_id='%s'" % (host_id))
                            sqlalche_obj.session.commit()
                            time.sleep(1)
                            for i in range(0, len(result["result"])):
                                sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)" % (
                                    'odu100_raSiteSurveyResultTable', host_id, str(result["result"][i + 1])[1:-1]))
                            sqlalche_obj.session.commit()
##                            if site_survey_table!=[] or len(site_survey_table)>0:
##
##                                column_list.remove('odu100_raSiteSurveyResultTable_id')
##                                column_list.remove('host_id')
##
##                                for i in result["result"]:
##                                    #site_survey_channel_table = sqlalche_obj.session.query(Odu100RaSiteSurveyResultTable).filter(and_(Odu100RaSiteSurveyResultTable.host_id == device_param_list[0].host_id,Odu100RaSiteSurveyResultTable.channelnumber==result["result"][i][9])).all()
##                                    #print site_survey_channel_table
##                                    #print result["result"]
##                                    #channel_number.append(str(result["result"][i][9]))
##                                    #print "hello"
##                                    sqlalche_obj.db.execute("delete from odu100_raSiteSurveyResultTable where host_id='%s'"%(host_id))
####                                    if site_survey_channel_table !=[] or len(site_survey_channel_table)>0:
####                                        for k in range(0,len(column_list)):
####                                            temp_result = str(result["result"][i][k])
####                                            exec "site_survey_table[%s].%s = '%s'"%(i-1,column_list[k],temp_result[:-1] if temp_result.count('\n') else temp_result)
####                                    else:
##                                    sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%('odu100_raSiteSurveyResultTable',host_id,str(result["result"][i])[1:-1]))
##                                sqlalche_obj.session.commit()
##                                time.sleep(1)
##                            else:
##                                for i in range(0,len(result["result"])):
##                                    sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%('odu100_raSiteSurveyResultTable',host_id,str(result["result"][i+1])[1:-1]))
##                                time.sleep(1)

                            result = {'success': 0, 'result':
                                "Calculating Site Survey Results has successfully completed."}
                            sqlalche_obj.session.commit()
                            return result
                        else:

                            if 553 in result["result"]:
                                agent_start(
                                    device_param_list[0].ip_address, 'root', 'public')
                                result = {"success": 1,
                                    "result": "No Response From Device.Please Try Again"}
                            elif 551 in result["result"]:
                                result = {
                                    "success": 1, "result": "Network is unreachable"}
                            elif 99 in result["result"]:
                                result = {"success": 1, "result":
                                    "UNMP has encountered an expected error. Please Retry "}
                            else:
                                for i in result['result']:
                                    if result['result'][i] != 0:
                                        result['result'] = str(errorStatus.get(
                                            result['result'][i], "SNMP agent Unknown Error Occured"))

                            return result

                    else:
                        if 553 in snmp_result["result"]:
                            agent_start(
                                device_param_list[0].ip_address, 'root', 'public')
                            result = {"success": 1,
                                "result": "No Response From Device.Please Try Again"}
                        elif 551 in snmp_result["result"]:
                            result = {"success":
                                1, "result": "Network is unreachable"}
                        elif 99 in snmp_result["result"]:
                            result = {"success": 1, "result":
                                "UNMP has encountered an eeexpected error. Please Retry"}
                        else:
                            for i in snmp_result["result"]:
                                if snmp_result["result"][i] != 0:
                                    result = {"success": 1, "result": str(
                                        errorStatus.get(snmp_result["result"][i], "SNMP agent Unknown Error Occured %s" % (snmp_get_result)))}
                        return result
                else:
                    #{'result': {'1.3.6.1.4.1.26149.2.2.5.1.7': '2'}, 'success': 0}
                    snmp_get_om_operation = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.2', device_param_list[0].ip_address, int(
                        device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
                    # print snmp_get_om_operation
                    if snmp_get_om_operation['success'] == 0:
                        if int(snmp_get_om_operation['result'].values()[0]) == 1:
                            msg = "Software  Download is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 2:
                            msg = "Software  Activation is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 3:
                            msg = "Factory reset is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 4:
                            msg = "Commit to Flash is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 5:
                            msg = "Device is rebooting.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 6:
                            msg = "Another Site Survey is running.Please wait to complete that operation..."
                        elif int(snmp_get_om_operation['result'].values()[0]) == 7:
                            msg = "Bandwidth calculator is running.Please wait to complete that operation..."
                        else:
                            msg = "Some operation is running.Please wait to complete that operation..."
                        result = {"success": 1, "result": msg}
                    else:
                        if 553 in snmp_get_om_operation["result"]:
                            agent_start(
                                device_param_list[0].ip_address, 'root', 'public')
                            result = {"success": 1,
                                "result": "No Response From Device.Please Try Again"}
                        elif 551 in snmp_get_om_operation["result"]:
                            result = {"success":
                                1, "result": "Network is unreachable"}
                        elif 99 in snmp_get_om_operation["result"]:
                            result = {"success": 1, "result":
                                "UNMP has encountered an unexpected error. Please Retry"}
                        else:
                            for i in snmp_get_om_operation["result"]:
                                if snmp_get_om_operation["result"][i] != 0:
                                    result = {"success": 1, "result": str(errorStatus.get(
                                        snmp_get_om_operation["result"][i], "SNMP agent Unknown Error Occured"))}
                            # result['result'] =
                            # str(errorStatus.get(snmp_get_result["result"][i],"SNMP
                            # agent Unknown Error Occured"))
                    return result
            else:
                if 553 in snmp_get_result["result"]:
                    agent_start(
                        device_param_list[0].ip_address, 'root', 'public')
                    result = {"success": 1, "result":
                        "No Response From Device.Please Try Again"}
                    return result
                elif 551 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "Network is unreachable"}
                    return result
                elif 99 in snmp_get_result["result"]:
                    result = {"success": 1, "result":
                        "UNMP has encountered an unexpected error. Please retry again"}
                    return result
                else:
                    for i in snmp_get_result["result"]:
                        if snmp_get_result["result"][i] != 0:
                            result = {"success": 1, "result": str(errorStatus.get(
                                snmp_get_result["result"][i], "SNMP agent Unknown Error Occured"))}
                            # result['result'] =
                            # str(errorStatus.get(snmp_get_result["result"][i],"SNMP
                            # agent Unknown Error Occured"))
                    return result
        except OperationalError as e:
            return {"success": 1, "result": "UNMP Database Server is Busy at the moment, please try again later.", "detail": str(e)}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except Exception as e:
            return {'success': 1, 'result': "UNMP Web Server is Busy at the moment, please try again later "}

        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def chk_site_survey_status(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = ""
            device_param_list = sqlalche_obj.session.query(Hosts).\
                filter(Hosts.host_id == host_id).all()
            snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7', device_param_list[0].ip_address, int(
                device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
            if int(snmp_get_result['success']) == 0:
                if int(snmp_get_result['result'].values()[0]) == 2 or int(snmp_get_result['result'].values()[0]) == 0 or int(snmp_get_result['result'].values()[0]) == 3:
                    result = "2"
                else:
                    result = "3"
                return result
            else:
                if 553 in snmp_get_result["result"]:
                    result = 553
                    return result
                elif 551 in snmp_get_result["result"]:
                    result = 551
                    return result
                elif 99 in snmp_get_result["result"]:
                    result = 99
                    return result
                else:
                    return snmp_get_result
        except Exception as e:
            return {'success': 1, 'result': str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
# obj = SiteSurvey()
# print obj.site_survey(3,1)


def acl_reconcile(host_id, device_type_id, table_prefix, insert_update):
    """

    @param host_id:
    @param device_type_id:
    @param table_prefix:
    @param insert_update:
    @return:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    if host_id != "" or host_id != None:
        device_param_list = sqlalche_obj.session.query(Hosts.snmp_version_id, Hosts.snmp_read_community, Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id, Hosts.reconcile_health, Hosts.snmp_write_community).\
            filter(Hosts.host_id == host_id).all()
    result = {}
    result = snmp_walk(
        device_param_list[0][0], device_param_list[0][
            1], device_param_list[0][2],
                       device_param_list[0][3], '.1.3.6.1.4.1.26149.2.2.13.5.1.2', '-On', '-OQ')
    if result == {}:
        result = ""
        return result
    else:
        acl_config = sqlalche_obj.session.query(SetOdu16RAAclConfigTable).filter(
            SetOdu16RAAclConfigTable.config_profile_id == device_param_list[0][4]).delete()
        # sqlalche_obj.session.delete(acl_config)
        sqlalche_obj.session.commit()

        if len(result) > 0:
            smaller = 0
            for n in result:
                greater = int(str(n).split(".")[-1])
                if smaller < greater:
                    smaller = greater
            j = smaller
            oidname = oid_name['RU.RA.1.RAACLConfig.#.macAddress']
            oidtype = oid_type['RU.RA.1.RAACLConfig.#.macAddress']
            if j < 10:
                j = 10
            for i in range(0, j):

                if ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1) in result:
                    if (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1)) == '"                  "') or (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1)) == '""') or (result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1)) == ''):
                        add_acl_config = SetOdu16RAAclConfigTable(
                            device_param_list[0][4], '', i + 1)
                    else:
                        add_acl_config = SetOdu16RAAclConfigTable(device_param_list[0][4], result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1)) if result.get(
                            ".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1)) == None else result.get(".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s" % (i + 1)).replace(" ", ""), i + 1)
                    result_final = 0
                    sqlalche_obj.session.add(add_acl_config)
                else:
                    name = oidname.replace('#', str(i + 1))
                    type = oidtype.replace('#', 's')
                    oidvalue = "                 "
                    set_result = snmp_setmultiple(
                        device_param_list[0][0], device_param_list[0][
                            6], device_param_list[
                                0][2], device_param_list[0][3],
                                                  '.1.3.6.1.4.1.26149.2.2.13.5.1.3.1.%s' % (i + 1), 'i', '4', name, type, "%s " % (oidvalue))
                    set_result.find("macaddress.1.%s" % (i + 1))
                    if set_result == -1:
                        result_final = 1
                        sqlalche_obj.sql_alchemy_db_connection_close()
                        return result_final
                    else:
                        result_final = 0
                        add_acl_config = SetOdu16RAAclConfigTable(
                            device_param_list[0][4], '', i + 1)
                    sqlalche_obj.session.add(add_acl_config)
                sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result_final
        else:
            return 2


def acl_controller_add_edit(host_id, device_type_id, dic_result, raindex):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @param raindex:
    @return:
    """
    try:
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        success_result = {"success": '', "result": {}}
        global errorStatus
        firmware_result = sqlalche_obj.session.query(
            Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
        if len(firmware_result):
            firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
            if firmware == '7.2.29':
                Oids = aliased(Odu1007_2_29_oids)
                table_name = "odu100_7_2_29_oids"
            elif firmware == '7.2.25':
                Oids = aliased(Odu1007_2_25_oids)
                table_name = "odu100_7_2_25_oids"
            else:
                Oids = aliased(Odu1007_2_20_oids)
                table_name = "odu100_7_2_20_oids"
        else:
            Oids = aliased(Odu1007_2_20_oids)
            table_name = "odu100_7_2_20_oids"
        # Create the alias
        o1 = aliased(Oids)
        o2 = aliased(Oids)

        query_result = []
        oid_admin_state = {"1": -1}
        independent_oid = []
        dependent_oid = []
        result = {}
        mac_address_dict = []
        admin_dic = []
        rowSts = []
        acl = []
        key = ""
        add_acl_dic = []
        device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id).\
            filter(Hosts.host_id == host_id).one()
        odu100_acl_conf_table = sqlalche_obj.session.query(
            Odu100RaAclConfigTable).filter(Odu100RaAclConfigTable.config_profile_id == device_param_list[3]).order_by(Odu100RaAclConfigTable.aclIndex).all()
        for keys in dic_result.iterkeys():
            if keys == "success":
                continue
            else:
                query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                    o1, o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                if len(query_result) > 0:
                    if query_result[0][0].dependent_id == "" or query_result[0][0].dependent_id == None:
                        if keys == "ru.ra.raAclConfigTable.macaddress":
                            mac_address_dict.append({keys: [query_result[0][0].oid + "." + str(raindex) + "." + str(
                                dic_result["aclindex"]), query_result[0][0].oid_type, dic_result[keys]]})
                            rowSts.append({"ru.ra.raAclConfigTable.rowSts": ["1.3.6.1.4.1.26149.2.2.13.5.1.3" +
                                          "." + str(raindex) + "." + str(dic_result["aclindex"]), "Integer32", "4"]})
                    else:
                        if keys == "ru.ra.raConfTable.aclMode":
                            dependent_oid.append({query_result[0][1]:
                                                 [query_result[0][2] + query_result[0][3]]})
                            acl.append({keys: [query_result[0][0].oid + query_result[0][0]
                                       .indexes, query_result[0][0].oid_type, dic_result[keys]]})
        if len(odu100_acl_conf_table) > 0:
            for i in range(0, len(odu100_acl_conf_table)):
                if int(dic_result["aclindex"]) == int(odu100_acl_conf_table[i].aclIndex):
                    add = 1
                    break
                else:
                    add = 0
                    continue
        else:
            add = 0
        if add == 0:
            result = pysnmp_setAcl(device_param_list[0], device_param_list[1], device_param_list[2], {} if len(
                acl) == 0 else acl[0], {} if len(dependent_oid) == 0 else dependent_oid[0], {} if len(mac_address_dict) == 0 else mac_address_dict[0], {} if len(rowSts) == 0 else rowSts[0])

            if result["success"] == 0 or result["success"] == '0':
                success_result["success"] = result["success"]
                for i in result["result"]:
                    if result["result"][i] != 0:
                        result["result"][i] = errorStatus[result["result"][i]]
                    else:
                        oid_list_table_field_value = sqlalche_obj.session.query(
                            Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == i, Oids.device_type_id == device_type_id)).all()
                        if len(oid_list_table_field_value) == 0:
                            continue
                        else:
                            if i in dic_result:
                                if i == "ru.ra.raConfTable.aclMode":
                                    table_name = "odu100_" + \
                                        oid_list_table_field_value[0][0]
                                    table_name = rename_tablename(table_name)
                                    exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                        table_name, table_name, device_param_list[3])
                                    exec "table_result[0].%s = '%s'" % (
                                        oid_list_table_field_value[0][1], dic_result[i])
                                else:
                                    add_acl_dic.append(dic_result[i])
                if len(add_acl_dic) > 0:
                    sqlalche_obj.session.add(Odu100RaAclConfigTable(
                        device_param_list[3], raindex, dic_result["aclindex"], add_acl_dic[0], 1))
                sqlalche_obj.session.commit()
                success_result["result"].update(result["result"])
            else:
                success_result["success"] = 1
                for i in result["result"]:
                    i in errorStatus
                    success_result["result"] = errorStatus[i]
        else:
            result = pysnmp_setAcl(device_param_list[0], device_param_list[1], device_param_list[2], {} if len(acl) == 0 else acl[0], {} if len(dependent_oid)
                                   == 0 else dependent_oid[0], {} if len(mac_address_dict) == 0 else mac_address_dict[0], {})
            if result["success"] == 0 or result["success"] == '0':
                success_result["success"] = result["success"]
                for i in result["result"]:
                    if result["result"][i] != 0:
                        result["result"][i] = errorStatus[result["result"][i]]
                    else:
                        oid_list_table_field_value = sqlalche_obj.session.query(
                            Oids.table_name, Oids.coloumn_name).filter(and_(Oids.oid_name == i, Oids.device_type_id == device_type_id)).all()
                        if len(oid_list_table_field_value) == 0:
                            continue
                        else:
                            if i in dic_result:
                                table_name = "odu100_" + \
                                    oid_list_table_field_value[0][0]
                                table_name = rename_tablename(table_name)
                                if table_name == "Odu100RaConfTable":
                                    exec "table_result = sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id == \"%s\")).all()" % (
                                        table_name, table_name, device_param_list[3])
                                else:
                                    exec "table_result = sqlalche_obj.session.query(%s).filter(and_(%s.config_profile_id == \"%s\",%s.aclIndex == \"%s\")).all()" % (
                                        table_name, table_name, device_param_list[3], table_name, int(dic_result["aclindex"]))
                                exec "table_result[0].%s = '%s'" % (
                                    oid_list_table_field_value[0][1], dic_result[i])
                                sqlalche_obj.session.commit()
                success_result["result"].update(result["result"])
            else:
                success_result["success"] = 1
                for i in result["result"]:
                    i in errorStatus
                    success_result["result"] = errorStatus[i]
        sqlalche_obj.sql_alchemy_db_connection_open()
        return success_result
    except ProgrammingError as e:
        return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
    except AttributeError as e:
        return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
    except OperationalError as e:
        return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
    except TimeoutError as e:
        return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
    except NameError as e:
        return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
    except UnboundExecutionError as e:
        return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
    except DatabaseError as e:
        return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
    except DisconnectionError as e:
        return {"success": 1, "result": "Database Disconnected", "detail": ""}
    except NoResultFound as e:
        return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
    except UnmappedInstanceError as e:
        return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
    except NoReferenceError as e:
        return {"success": 1, "result": "No reference Exists", "detail": ""}
    except SAWarning as e:
        return {"success": 1, "result": "Warning Occurs", "detail": ""}
    except Exception as e:
        return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()


# def change_device_network_details(self,device_dict):
##        Session = sessionmaker(bind=engine)     # making session of our current database
##        result = {}
##        chk = 0
##        if len(device_dict)>0:
##            sqlalche_obj = Session()
##            host_details =  sqlalche_obj.query(Hosts).filter(Hosts.host_id == device_dict["host_id"]).all()
##            if len(host_details)>0:
##                if host_details[0].config_profile_id == "" or host_details[0].config_profile_id == None:
##                    result = {"success":1,"result":"No Configuration exist"}
##                    sqlalche_obj.close()
##                    return result
##                else:
##                    change_net_config = {}
##                    if device_dict["device_type_id"]==UNMPDeviceType.odu16 or device_dict["device_type_id"]==UNMPDeviceType.odu100:
##                        ip_oid = ["1.3.6.1.4.1.26149.2.2.9.1.3.1","IpAddress",device_dict["ip_address"]]
##                        netmask_oid = ["1.3.6.1.4.1.26149.2.2.9.1.4.1","IpAddress",device_dict["ip_network_mask"]]
##                        gateway_oid = ["1.3.6.1.4.1.26149.2.2.9.1.5.1","IpAddress",device_dict["ip_gateway"]]
##                        autoIp = ["1.3.6.1.4.1.26149.2.2.9.1.6.1","Integer32",device_dict["dhcp"]]
##                        admin_state = ['1.3.6.1.4.1.26149.2.2.9.1.2.1','Integer32',0]
##                        dic_odu = {'ip':ip_oid,'netmask':netmask_oid,'gateway':gateway_oid,'autoip':autoIp}
##                        admin_dic = {'admin-1':admin_state}
##                        change_net_config = pysnmp_set(dic_odu,host_details[0].ip_address,host_details[0].snmp_port,host_details[0].snmp_write_community,admin_dic)
##                        admin_state = ['1.3.6.1.4.1.26149.2.2.9.1.2.1','Integer32',1]
##                        admin_dic = {'admin':admin_state}
##                        change_admin_state = pysnmp_set(admin_dic,host_details[0].ip_address,host_details[0].snmp_port,host_details[0].snmp_write_community)
##                    if device_dict["device_type_id"]==UNMPDeviceType.idu4:
##                        ip_oid = ["1.3.6.1.4.1.26149.2.1.2.4.1.2.0","IpAddress",device_dict["ip_address"]]
##                        netmask_oid = ["1.3.6.1.4.1.26149.2.1.2.4.1.3.0","IpAddress",device_dict["ip_network_mask"]]
##                        gateway_oid = ["1.3.6.1.4.1.26149.2.1.2.4.1.4.0","IpAddress",device_dict["ip_gateway"]]
##                        autoIp = ["1.3.6.1.4.1.26149.2.1.2.4.1.5.0","Integer32",device_dict["dhcp"]]
##                        dic_odu = {'ip':ip_oid,'netmask':netmask_oid,'gateway':gateway_oid,'autoip':autoIp}
##                        change_net_config = pysnmp_set(dic_odu,host_details[0].ip_address,host_details[0].snmp_port,host_details[0].snmp_write_community)
##                        for i in range(0,3):
##                            if snmp_ping(str(device_dict["ip_address"]),str(host_details[0].snmp_read_community),int(host_details[0].snmp_port))==0:
##                                change_net_config = {"result":{'ip':0,'netmask':0,'gateway':0,'autoip':0},"success":0}
##                                break
##                            else:
##                                change_net_config={"success":1}
##                                result={"result":"No response From device"}
##                                time.sleep(5)
##                                continue
##                    if change_net_config["success"]==0:
##                        for i in change_net_config["result"]:
##                            if change_net_config["result"][i]==0:
##
##                                chk = 1
##                            else:
##                                chk = 2
##                                break
##                    else:
##                        result = {"success":1}
##                        sqlalche_obj.close()
##                        return result
##                    if chk == 1:
##                        if device_dict["device_type_id"]==UNMPDeviceType.odu16:
##                            odu16_ip_details = sqlalche_obj.query(SetOdu16IPConfigTable).filter(SetOdu16IPConfigTable.config_profile_id == host_details[0].config_profile_id).all()
##                            if len(odu16_ip_details)>0:
##                                odu16_ip_details[0].ip_address = device_dict["ip_address"]
##                                odu16_ip_details[0].ip_network_mask = device_dict["ip_network_mask"]
##                                odu16_ip_details[0].ip_network_mask = device_dict["ip_gateway"]
##                                odu16_ip_details[0].ip_network_mask = device_dict["dhcp"]
##                            else:
##                                odu16_detail = SetOdu16IPConfigTable(None,host_details[0].config_profile_id,1,device_dict["ip_address"],device_dict["ip_network_mask"],device_dict["ip_gateway"],device_dict["dhcp"])
##                                sqlalche_obj.add(odu16_detail)
##                            result = {"success":0}
##                        elif device_dict["device_type_id"]==UNMPDeviceType.odu100:
##
##                            odu16_ip_details = sqlalche_obj.query(Odu100IpConfigTable).filter(Odu100IpConfigTable.config_profile_id == host_details[0].config_profile_id).all()
##                            if len(odu16_ip_details)>0:
##                                odu16_ip_details[0].ipAddress = device_dict["ip_address"]
##                                odu16_ip_details[0].ipNetworkMask = device_dict["ip_network_mask"]
##                                odu16_ip_details[0].ipDefaultGateway = device_dict["ip_gateway"]
##                                odu16_ip_details[0].autoIpConfig = device_dict["dhcp"]
##                            else:
##                                odu100_detail = Odu100IpConfigTable(None,host_details[0].config_profile_id,0,1,device_dict["ip_address"],device_dict["ip_network_mask"],device_dict["ip_gateway"],device_dict["dhcp"])
##                                sqlalche_obj.add(odu100_detail)
##
##                            result = {"success":0}
##                        elif device_dict["device_type_id"]==UNMPDeviceType.idu4:
##                            odu16_ip_details = sqlalche_obj.query(IduNetworkConfigurationsTable).filter(IduNetworkConfigurationsTable.config_profile_id == host_details[0].config_profile_id).all()
##                            if len(odu16_ip_details)>0:
##                                odu16_ip_details[0].ipaddr = device_dict["ip_address"]
##                                odu16_ip_details[0].netmask = device_dict["ip_network_mask"]
##                                odu16_ip_details[0].gateway = device_dict["ip_gateway"]
##                                odu16_ip_details[0].autoIpConfig = device_dict["dhcp"]
##                            else:
##                                idu_detail = IduNetworkConfigurationsTable(None,host_details[0].config_profile_id,0,1,device_dict["ip_address"],device_dict["ip_network_mask"],device_dict["ip_gateway"],device_dict["dhcp"])
##                                sqlalche_obj.add(idu_detail)
##                            result = {"success":0}
##                        sqlalche_obj.commit()
##                        sqlalche_obj.close()
##                        return result
##                    else:
##                        result = {"success":1,"result":"Values Not Set.Retry Again"}
##                        sqlalche_obj.close()
##                        return result
##            else:
##                result = {"success":1,"result":"No Host Exist"}
##                sqlalche_obj.close()
##                return result
##        else:
##            result = {"success":1,"result":"Parameter Not Proper"}
##            return result
# obj = OduReconcilation()
##########
# print obj.odu16_add_default_config_profile(28,'odu16','odu16_',False)
# print obj.update_reconcilation_controller(63,'odu100','odu100_',True,"")
def get_ip_mac_selected_device(h):
    """

    @param h:
    """
    global html
    obj = IpMacSearch()
    html = h
    result = {}
    selected_val = html.var('selected_val')
    ip_mac_val = html.var('ip_mac_val')
    result = obj.get_ip_mac_selected_device(selected_val, ip_mac_val)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


class OduStatus(object):
    """
    Get the current ODUC device stauts
    """
    def hw_sw_frequecy_status_chk(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        global sqlalche_obj
        hw_sw_freq_status_dic = {'success': 0, 'result': {}}
        try:
            preffered_channel_dic = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            config_profile_id = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            if device_type == "odu100":
                sw_status = sqlalche_obj.session.query(Odu100SwStatusTable.activeVersion).filter(
                    Odu100SwStatusTable.host_id == host_id).all()
                hw_status = sqlalche_obj.session.query(Odu100HwDescTable.hwSerialNo).filter(
                    Odu100HwDescTable.host_id == host_id).all()
                channel_list = sqlalche_obj.session.query(Odu100RaPreferredRFChannelTable.rafrequency).\
                    filter(
                        Odu100RaPreferredRFChannelTable.config_profile_id == config_profile_id[0][0]).all()
                channel_tuple = tuple(map(int, sum(channel_list, ())))
                ra_preffered_list = sqlalche_obj.db.execute("SELECT odu100_raChannelListTable.channelNumber , odu100_raPreferredRFChannelTable.rafrequency\
                FROM odu100_raPreferredRFChannelTable join (select * from hosts  )\
                as hosts on hosts.host_id=%s and odu100_raPreferredRFChannelTable.config_profile_id=hosts.config_profile_id\
                left join(select * from odu100_raChannelListTable) as odu100_raChannelListTable\
                on odu100_raChannelListTable.host_id = hosts.host_id and\
                odu100_raPreferredRFChannelTable.rafrequency in %s\
                and odu100_raPreferredRFChannelTable.rafrequency =odu100_raChannelListTable.frequency" % (host_id, channel_tuple if channel_tuple != () else '("")'))
                for row in ra_preffered_list:
                    if row['rafrequency'] != 0:
                        preffered_channel_dic.update(
                            {row['channelNumber']: row['rafrequency']})
            else:
                sw_status = sqlalche_obj.session.query(GetOdu16SWStatusTable.active_version).filter(
                    GetOdu16SWStatusTable.host_id == host_id).all()
                hw_status = sqlalche_obj.session.query(GetOdu16HWDescTable.hw_serial_no).filter(
                    GetOdu16HWDescTable.host_id == host_id).all()
                frequency = sqlalche_obj.session.query(SetOdu16RATddMacConfig.rf_channel_frequency).filter(
                    SetOdu16RATddMacConfig.config_profile_id == config_profile_id[0][0]).all()

            # tddmac_status =
            # sqlalche_obj.session.query(Odu100RaTddMacStatusTable.rfChanFreq).filter(Odu100RaTddMacStatusTable.host_id==host_id).all()

            if device_type == "odu100":
                hw_sw_freq_status_dic['result'] = {'sw_status': sw_status[0][0] if len(sw_status) > 0 else "-",
                                                   'hw_serail_number': hw_status[0][0] if len(hw_status) > 0 else "-", 'channel_list': preffered_channel_dic}
            else:
                hw_sw_freq_status_dic['result'] = {'sw_status': sw_status[0][0] if len(sw_status) > 0 else "-",
                                                   'hw_serail_number': hw_status[0][0] if len(hw_status) > 0 else "-", 'frequency': frequency[0][0] if len(frequency) > 0 else "-"}
        except Exception, e:
            hw_sw_freq_status_dic['success'] = 1
            hw_sw_freq_status_dic['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return hw_sw_freq_status_dic

    def peer_status_chk(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        peer_final_dic = {'success': 0, 'result': {}}
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            peer_dic = {}
            if device_type == "odu100":
                total_peer_count = sqlalche_obj.session.query(func.count(Odu100PeerNodeStatusTable.timeSlotIndex)).filter(
                    Odu100PeerNodeStatusTable.host_id == host_id).group_by(Odu100PeerNodeStatusTable.timestamp).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()
                peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.peerMacAddr, Odu100PeerNodeStatusTable.sigStrength1, Odu100PeerNodeStatusTable.timestamp).\
                    filter(
                        and_(
                            Odu100PeerNodeStatusTable.tunnelStatus == 1, Odu100PeerNodeStatusTable.linkStatus.in_(
                                [1, 2]),
                                Odu100PeerNodeStatusTable.host_id == host_id)).order_by(desc(Odu100PeerNodeStatusTable.timestamp)).limit(int(total_peer_count[0][0])if len(total_peer_count) > 0 else 0).all()
            else:
                total_peer_count = sqlalche_obj.session.query(func.count(GetOdu16PeerNodeStatusTable.timeslot_index)).filter(
                    GetOdu16PeerNodeStatusTable.host_id == host_id).group_by(GetOdu16PeerNodeStatusTable.timestamp).order_by(desc(GetOdu16PeerNodeStatusTable.timestamp)).limit(1).all()
                peer_status = sqlalche_obj.session.query(GetOdu16PeerNodeStatusTable.peer_mac_addr, GetOdu16PeerNodeStatusTable.sig_strength, GetOdu16PeerNodeStatusTable.timestamp).\
                    filter(
                        and_(
                            GetOdu16PeerNodeStatusTable.tunnel_status == 1, GetOdu16PeerNodeStatusTable.link_status.in_(
                                [1, 2]),
                                GetOdu16PeerNodeStatusTable.host_id == host_id)).order_by(desc(GetOdu16PeerNodeStatusTable.timestamp)).limit(int(total_peer_count[0][0])if len(total_peer_count) > 0 else 0).all()
            if len(peer_status) > 0:
                for i in range(0, len(peer_status)):
                    peer_dic.update(
                        {'timeslot%s' % (i + 1): {'mac_address': peer_status[i].peerMacAddr, 'signalstrength': peer_status[i].sigStrength1,
                                    'timestamp': datetime.strftime(peer_status[i].timestamp, "%d-%b-%Y %A %I:%M:%S %p")}})
                peer_final_dic['result'] = peer_dic
            else:
                peer_final_dic['success'] = 0
                peer_final_dic['result'] = {}
        except Exception, e:
            peer_final_dic['success'] = 1
            peer_final_dic['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return peer_final_dic

    def admin_states_data(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        global sqlalche_obj
        try:
            admin_dic = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            config_profile_id = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            if device_type == "odu100":
                ru_data = sqlalche_obj.session.query(Odu100RuConfTable.adminstate).filter(
                    Odu100RuConfTable.config_profile_id == config_profile_id[0][0]).all()
                ra_data = sqlalche_obj.session.query(Odu100RaConfTable.raAdminState).filter(
                    Odu100RaConfTable.config_profile_id == config_profile_id[0][0]).all()
                sync_data = sqlalche_obj.session.query(Odu100SyncConfigTable.adminStatus).filter(
                    Odu100SyncConfigTable.config_profile_id == config_profile_id[0][0]).all()
            else:
                ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable.adminstate).filter(
                    SetOdu16RUConfTable.config_profile_id == config_profile_id[0][0]).all()
                ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable.ra_admin_state).filter(
                    SetOdu16RAConfTable.config_profile_id == config_profile_id[0][0]).all()
                sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable.admin_status).filter(
                    SetOdu16SyncConfigTable.config_profile_id == config_profile_id[0][0]).all()

            admin_dic = {'ru_admin': int(ru_data[0][0]) if len(ru_data) > 0 else 1,
                         'ra_admin': int(ra_data[0][0]) if len(ra_data) > 0 else 1,
                         'sync_admin': int(sync_data[0][0]) if len(sync_data) > 0 else 1}
            admin_dic['success'] = 0
        except Exception, e:
            admin_dic['success'] = 1
            admin_dic = {'exception': str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return admin_dic

    ##    def admin_state_change(self,host_id,device_type,admin_state_name,state):
    ##        global sqlalche_obj
    ##        global errorStatus
    ##        try:
    ##            get_dic = {'ru.ruConfTable.adminstate':'1.3.6.1.4.1.26149.2.2.3.1.7.1','ru.ra.raConfTable.raAdminState':'1.3.6.1.4.1.26149.2.2.13.1.1.2.1','ru.syncClock.syncConfigTable.adminStatus':'1.3.6.1.4.1.26149.2.2.11.1.1.2.1'}
    ##            condition = True
    ##            check = 0
    ##            sqlalche_obj.sql_alchemy_db_connection_open()
    ##            host_data = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id==host_id).all()
    ##            oid_data = sqlalche_obj.session.query(Oids.oid,Oids.indexes,Oids.oid_type).filter(Oids.oid_name==admin_state_name).all()
    ##            oid_dic = {admin_state_name:[str(oid_data[0].oid)+str(oid_data[0].indexes),oid_data[0].oid_type,state]}
    ##            snmp_result = pysnmp_seter_ap(oid_dic,host_data[0].ip_address,int(host_data[0].snmp_port),host_data[0].snmp_write_community)
    ##            if admin_state_name=="ru.ruConfTable.adminstate":
    ##                while(condition):
    ##                    ru_get = pysnmp_get('1.3.6.1.4.1.26149.2.2.1.1.2',host_data[0].ip_address,int(host_data[0].snmp_port),host_data[0].snmp_read_community)
    ##                    if int(ru_get['success'])==1:
    ##                        if int(ru_get['result'].keys()[0])==553:
    ##                            time.sleep(10)
    ##                            check = check+1
    ##                            if(check>3):
    ##                                break
    ##                            else:
    ##                                continue
    ##                        else:
    ##                            break
    ##                    else:
    ##                        snmp_result['success'] = 0
    ##                        condition = False
    ##            if snmp_result['success']==0:
    ##                for i in snmp_result['result']:
    ##                    if snmp_result['result'][i]==0:
    ##                        if admin_state_name=="ru.ruConfTable.adminstate":
    ##                            if device_type==UNMPDeviceType.odu100:
    ##                                ru_data = sqlalche_obj.session.query(Odu100RuConfTable).filter(Odu100RuConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                            else:
    ##                                ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(SetOdu16RUConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                            ru_data[0].adminstate= state
    ##                        elif admin_state_name=="ru.ra.raConfTable.raAdminState":
    ##                            if device_type==UNMPDeviceType.odu100:
    ##                                ra_data = sqlalche_obj.session.query(Odu100RaConfTable).filter(Odu100RaConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                            else:
    ##                                ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable).filter(SetOdu16RAConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                            ra_data[0].raAdminState = state
    ##                        elif admin_state_name=="ru.syncClock.syncConfigTable.adminStatus":
    ##                            if device_type==UNMPDeviceType.odu100:
    ##                                sync_data = sqlalche_obj.session.query(Odu100SyncConfigTable).filter(Odu100SyncConfigTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                            else:
    ##                                sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(SetOdu16SyncConfigTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                            sync_data[0].adminStatus = state
    ##                snmp_get = pysnmp_geter(get_dic,host_data[0].ip_address,int(host_data[0].snmp_port),host_data[0].snmp_read_community)
    ##                if snmp_get['success']==0:
    ##                    for j in snmp_get['result']:
    ##                        if snmp_get['result'][j]!=-1:
    ##                            if j=="ru.ruConfTable.adminstate":
    ##                                if device_type==UNMPDeviceType.odu100:
    ##                                    ru_data = sqlalche_obj.session.query(Odu100RuConfTable).filter(Odu100RuConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                                else:
    ##                                    ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(SetOdu16RUConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                                ru_data[0].adminstate= snmp_get['result'][j]
    ##                            elif j=="ru.ra.raConfTable.raAdminState":
    ##                                if device_type==UNMPDeviceType.odu100:
    ##                                    ra_data = sqlalche_obj.session.query(Odu100RaConfTable).filter(Odu100RaConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                                else:
    ##                                    ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable).filter(SetOdu16RAConfTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                                ra_data[0].raAdminState = snmp_get['result'][j]
    ##                            elif j=="ru.syncClock.syncConfigTable.adminStatus":
    ##                                if device_type==UNMPDeviceType.odu100:
    ##                                    sync_data = sqlalche_obj.session.query(Odu100SyncConfigTable).filter(Odu100SyncConfigTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                                else:
    ##                                    sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(SetOdu16SyncConfigTable.config_profile_id==host_data[0].config_profile_id).all()
    ##                                sync_data[0].adminStatus = snmp_get['result'][j]
    ##
    ##                sqlalche_obj.session.commit()
    ##            else:
    ##                for i in snmp_result["result"]:
    ##                    #return snmp_result
    ##                    if i==553:
    ##                        snmp_result["result"] = str(host_data[0].host_alias)+" ("+str(host_data[0].ip_address)+") "+str(errorStatus.get(i,"SNMP agent Unknown Error Occured"))
    ##                    elif i==551:
    ##                        snmp_result["result"] = str(host_data[0].host_alias)+" ("+str(host_data[0].ip_address)+") "+str(errorStatus.get(i,"SNMP agent Unknown Error Occured"))
    ##                    elif snmp_result["result"][i] != 0:
    ##                        snmp_result["result"] = str(host_data[0].host_alias)+" ("+str(host_data[0].ip_address)+") "+str(errorStatus.get(snmp_result["result"][i],"SNMP agent Unknown Error Occured"))
    ##
    ##        except Exception,e:
    ##            snmp_result['success']=1
    ##            snmp_result['result']=str(e)
    ##        finally:
    ##            sqlalche_obj.sql_alchemy_db_connection_close()
    ##            return snmp_result
    def admin_state_change(self, host_id, device_type, admin_state_name, state):
        """

        @param host_id:
        @param device_type:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        try:
            get_operation_dic = {'ru.ruConfTable.adminstate': '1.3.6.1.4.1.26149.2.2.3.1.7.1', 'ru.syncClock.syncConfigTable.adminStatus':
                '1.3.6.1.4.1.26149.2.2.11.3.1.1.1', 'ru.ra.raConfTable.raAdminState': '1.3.6.1.4.1.26149.2.2.13.2.1.3.1'}
            get_dic = {
                'ru.ruConfTable.adminstate': '1.3.6.1.4.1.26149.2.2.1.1.2.1', 'ru.syncClock.syncConfigTable.adminStatus': '1.3.6.1.4.1.26149.2.2.11.1.1.2.1',
                'ru.ra.raConfTable.raAdminState': '1.3.6.1.4.1.26149.2.2.13.1.1.2.1'}
            condition = True
            check = 0
            op_state = []
            sqlalche_obj.sql_alchemy_db_connection_open()
            firmware_result = sqlalche_obj.session.query(
                Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
            if len(firmware_result):
                firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
                if firmware == '7.2.29':
                    Oids = aliased(Odu1007_2_29_oids)
                    table_name = "odu100_7_2_29_oids"
                elif firmware == '7.2.25':
                    Oids = aliased(Odu1007_2_25_oids)
                    table_name = "odu100_7_2_25_oids"
                else:
                    Oids = aliased(Odu1007_2_20_oids)
                    table_name = "odu100_7_2_20_oids"
            else:
                Oids = aliased(Odu1007_2_20_oids)
                table_name = "odu100_7_2_20_oids"

            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_data = sqlalche_obj.session.query(Oids.oid, Oids.indexes, Oids.oid_type).filter(
                Oids.oid_name == admin_state_name).all()
            oid_dic = {admin_state_name: [str(oid_data[0].oid) + str(
                oid_data[0].indexes), oid_data[0].oid_type, state]}
            snmp_result = pysnmp_seter_ap(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)
            if admin_state_name == "ru.ruConfTable.adminstate":
                while(condition):
                    ru_get = pysnmp_get('1.3.6.1.4.1.26149.2.2.1.1.2', host_data[0].ip_address, int(
                        host_data[0].snmp_port), host_data[0].snmp_read_community)
                    if int(ru_get['success']) == 1:
                        if int(ru_get['result'].keys()[0]) == 553:
                            time.sleep(10)
                            check = check + 1
                            if(check > 3):
                                break
                            else:
                                continue
                        else:
                            break
                    else:
                        snmp_result['success'] = 0
                        condition = False
            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        if admin_state_name == "ru.ruConfTable.adminstate":
                            if device_type == UNMPDeviceType.odu100:
                                ru_data = sqlalche_obj.session.query(
                                    Odu100RuConfTable).filter(Odu100RuConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            else:
                                ru_data = sqlalche_obj.session.query(
                                    SetOdu16RUConfTable).filter(SetOdu16RUConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            ru_data[0].adminstate = state
                        elif admin_state_name == "ru.ra.raConfTable.raAdminState":
                            if device_type == UNMPDeviceType.odu100:
                                ra_data = sqlalche_obj.session.query(
                                    Odu100RaConfTable).filter(Odu100RaConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            else:
                                ra_data = sqlalche_obj.session.query(
                                    SetOdu16RAConfTable).filter(SetOdu16RAConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            ra_data[0].raAdminState = state
                        elif admin_state_name == "ru.syncClock.syncConfigTable.adminStatus":
                            if device_type == UNMPDeviceType.odu100:
                                sync_data = sqlalche_obj.session.query(
                                    Odu100SyncConfigTable).filter(Odu100SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                            else:
                                sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
                                    SetOdu16SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                            sync_data[0].adminStatus = state
                sqlalche_obj.session.commit()
                snmp_get = pysnmp_geter(get_dic, host_data[0].ip_address, int(
                    host_data[0].snmp_port), host_data[0].snmp_read_community)
                # print "\n\n\n",snmp_get,"###########\n\n\n"
                if snmp_get['success'] == 0:
                    for j in snmp_get['result']:
                        if snmp_get['result'][j] != -1:
                            if j == "ru.ruConfTable.adminstate":
                                if device_type == UNMPDeviceType.odu100:
                                    ru_data = sqlalche_obj.session.query(
                                        Odu100RuConfTable).filter(Odu100RuConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                else:
                                    ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(
                                        SetOdu16RUConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                ru_data[0].adminstate = snmp_get['result'][j]
                            elif j == "ru.ra.raConfTable.raAdminState":
                                if device_type == UNMPDeviceType.odu100:
                                    ra_data = sqlalche_obj.session.query(
                                        Odu100RaConfTable).filter(Odu100RaConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                else:
                                    ra_data = sqlalche_obj.session.query(SetOdu16RAConfTable).filter(
                                        SetOdu16RAConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                ra_data[0].raAdminState = snmp_get['result'][j]
                            elif j == "ru.syncClock.syncConfigTable.adminStatus":
                                if device_type == UNMPDeviceType.odu100:
                                    sync_data = sqlalche_obj.session.query(Odu100SyncConfigTable).filter(
                                        Odu100SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                                else:
                                    sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
                                        SetOdu16SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                                sync_data[
                                    0].adminStatus = snmp_get['result'][j]
                snmp_operation_get = pysnmp_geter(get_operation_dic, host_data[0].ip_address, int(
                    host_data[0].snmp_port), host_data[0].snmp_read_community)
                # print snmp_operation_get,"^^^^^^^^^^^^^^^^"
                if snmp_operation_get['success'] == 0:
                    ru_status = sqlalche_obj.session.query(Odu100RuStatusTable).filter(
                        Odu100RuStatusTable.host_id == host_id).all()
                    ra_status = sqlalche_obj.session.query(Odu100RaStatusTable).filter(
                        Odu100RaStatusTable.host_id == host_id).order_by(desc(Odu100RaStatusTable.timestamp)).limit(1).all()
                    sync_status = sqlalche_obj.session.query(Odu100SynchStatusTable).filter(
                        Odu100SynchStatusTable.host_id == host_id).order_by(desc(Odu100SynchStatusTable.timestamp)).limit(1).all()

                    for j in snmp_operation_get['result']:
                        if snmp_operation_get['result'][j] != -1:
                            if j == "ru.ruConfTable.adminstate":
                                if len(ru_status) > 0:
                                    ru_status[
                                        0].ruoperationalState = snmp_operation_get['result'][j]

                            elif j == "ru.syncClock.syncConfigTable.adminStatus":
                                if len(sync_status) > 0:
                                    sync_status[0].syncoperationalState = snmp_operation_get[
                                        'result'][j]
                            elif j == "ru.ra.raConfTable.raAdminState":
                                if len(ra_status) > 0:
                                    ra_status[
                                        0].raoperationalState = snmp_operation_get['result'][j]

                sqlalche_obj.session.commit()
            else:
                for i in snmp_result["result"]:
                    # return snmp_result
                    if i == 553:
                        snmp_result["result"] = str(host_data[0].host_alias) + " (" + str(
                            host_data[0].ip_address) + ") " + str(errorStatus.get(i, "SNMP agent Unknown Error Occured"))
                    elif i == 551:
                        snmp_result["result"] = str(host_data[0].host_alias) + " (" + str(
                            host_data[0].ip_address) + ") " + str(errorStatus.get(i, "SNMP agent Unknown Error Occured"))
                    elif snmp_result["result"][i] != 0:
                        snmp_result["result"] = str(host_data[0].host_alias) + " (" + str(
                            host_data[0].ip_address) + ") " + str(errorStatus.get(snmp_result["result"][i], "SNMP agent Unknown Error Occured"))

        except Exception, e:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def all_lock_unlocked(self, host_id, device_type, admin_state_name, state):
        """

        @param host_id:
        @param device_type:
        @param admin_state_name:
        @param state:
        @return:
        """
        global sqlalche_obj
        global errorStatus
        ru_admin = 0
        ru_dic = {}
        try:
            snmp_result = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            firmware_result = sqlalche_obj.session.query(
                Hosts.firmware_mapping_id).filter(Hosts.host_id == host_id).all()
            if len(firmware_result):
                firmware = object_model_di['odu100'].get(firmware_result[0].firmware_mapping_id)
                if firmware == '7.2.29':
                    Oids = aliased(Odu1007_2_29_oids)
                    table_name = "odu100_7_2_29_oids"
                elif firmware == '7.2.25':
                    Oids = aliased(Odu1007_2_25_oids)
                    table_name = "odu100_7_2_25_oids"
                else:
                    Oids = aliased(Odu1007_2_20_oids)
                    table_name = "odu100_7_2_20_oids"
            else:
                Oids = aliased(Odu1007_2_20_oids)
                table_name = "odu100_7_2_20_oids"

            host_data = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            oid_dic = {}
            oid_data = sqlalche_obj.session.query(Oids.oid, Oids.indexes, Oids.oid_type).filter(
                Oids.oid_name == admin_state_name).all()
            admin_state_list = admin_state_name.split(",")
            for i in range(0, len(admin_state_list)):
                oid_data = sqlalche_obj.session.query(Oids.oid, Oids.indexes, Oids.oid_type).filter(
                    Oids.oid_name == admin_state_list[i]).all()
                if admin_state_list[i] == "ru.ruConfTable.adminstate":
                    ru_admin = 1
                    ru_dic = {admin_state_list[i]: [str(oid_data[0].oid) + str(
                        oid_data[0].indexes), oid_data[0].oid_type, state]}
                else:
                    oid_dic.update({admin_state_list[i]: [str(
                        oid_data[0].oid) + str(oid_data[0].indexes), oid_data[0].oid_type, state]})
            snmp_result = pysnmp_seter_ap(oid_dic, host_data[0].ip_address, int(
                host_data[0].snmp_port), host_data[0].snmp_write_community)
            if snmp_result['success'] == 0:
                for i in snmp_result['result']:
                    if snmp_result['result'][i] == 0:
                        if i == "ru.syncClock.syncConfigTable.adminStatus":
                            if device_type == UNMPDeviceType.odu100:
                                sync_data = sqlalche_obj.session.query(
                                    Odu100SyncConfigTable).filter(Odu100SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                            else:
                                sync_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable).filter(
                                    SetOdu16SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                            sync_data[0].adminStatus = state
                        elif i == "ru.ra.raConfTable.raAdminState":
                            if device_type == UNMPDeviceType.odu100:
                                ra_data = sqlalche_obj.session.query(
                                    Odu100RaConfTable).filter(Odu100RaConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            else:
                                ra_data = sqlalche_obj.session.query(
                                    SetOdu16RAConfTable).filter(SetOdu16RAConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            ra_data[0].raAdminState = state
                if ru_admin == 1:
                    ru_result = pysnmp_seter_ap(ru_dic, host_data[0].ip_address, int(
                        host_data[0].snmp_port), host_data[0].snmp_write_community)
                    if int(state) == 1:
                        if int(ru_result['success']) == 1:
                            for i in ru_result['result']:
                                if int(i) == 553:
                                    if device_type == UNMPDeviceType.odu100:
                                        ru_data = sqlalche_obj.session.query(Odu100RuConfTable).filter(
                                            Odu100RuConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                    else:
                                        ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(
                                            SetOdu16RUConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                    ru_data[0].adminstate = state
                                else:
                                    if i in errorStatus:
                                        ru_result["result"] = errorStatus[i]
                            snmp_result['result'].update(
                                {'ru.ruConfTable.adminstate': ru_result["result"]})
                        else:
                            if device_type == UNMPDeviceType.odu100:
                                ru_data = sqlalche_obj.session.query(
                                    Odu100RuConfTable).filter(Odu100RuConfTable.config_profile_id == host_data[0].config_profile_id).all()
                            else:
                                ru_data = sqlalche_obj.session.query(
                                    SetOdu16RUConfTable).filter(SetOdu16RUConfTable.config_profile_id == host_data[0].config_profile_id).all()
                    else:
                        if ru_result['success'] == 0:
                            for i in ru_result['result']:
                                if ru_result['result'][i] == 0:
                                    if device_type == UNMPDeviceType.odu100:
                                        ru_data = sqlalche_obj.session.query(Odu100RuConfTable).filter(
                                            Odu100RuConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                    else:
                                        ru_data = sqlalche_obj.session.query(SetOdu16RUConfTable).filter(
                                            SetOdu16RUConfTable.config_profile_id == host_data[0].config_profile_id).all()
                                    snmp_result['result'].update(
                                        {'ru.ruConfTable.adminstate': 0})
                                else:
                                    for i in ru_result["result"]:
                                        if ru_result["result"][i] != 0:
                                            if ru_result["result"].get(i) in errorStatus:
                                                ru_result["result"] = errorStatus[
                                                    ru_result["result"][i]]
                                    snmp_result['result'].update(
                                        {'ru.ruConfTable.adminstate': ru_result["result"]})
                        else:
                            for i in ru_result["result"]:
                                if ru_result["result"][i] != 0:
                                    if i in errorStatus:
                                        ru_result["result"] = errorStatus[i]
                                    else:
                                        ru_result[
                                            "result"] = "SNMP unknown error occurred"
                            snmp_result['result'].update(
                                {'ru.ruConfTable.adminstate': ru_result["result"]})

            else:
                for i in snmp_result["result"]:
                    if snmp_result["result"][i] != 0:
                        if i in errorStatus:
                            snmp_result["result"] = errorStatus[i]
            sqlalche_obj.session.commit()

        except Exception, e:
            final_result['success'] = 1
            final_result['result'] = str(e)
        finally:

            sqlalche_obj.sql_alchemy_db_connection_close()
            return snmp_result

    def global_admin_request(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            global sqlalche_obj
            global essential_obj

            admin_state_data = []
            result = {'success': 0, 'result': ""}
            temp_list = []
            admin_data_dic = {}
            peer_status = []
            host_data = []
            master_host_data = []
            sqlalche_obj.sql_alchemy_db_connection_open()
            ru_op_state = 1
            ra_op_state = 1
            sync_op_state = 1
            host_id_list = host_id.split(",")
            for i in range(0, len(host_id_list)):
                host_data = []
                temp_list = []
                peer_status = []
                master_host_data = []
                host_data = sqlalche_obj.session.query(
                    Hosts.config_profile_id, Hosts.device_type_id, Hosts.host_asset_id).filter(Hosts.host_id == host_id_list[i]).all()
                if len(host_data) > 0:
                    if host_data[0].device_type_id == UNMPDeviceType.odu16:

                        get_default_node_type = sqlalche_obj.session.query(GetOdu16_ru_conf_table.default_node_type).\
                            filter(
                                GetOdu16_ru_conf_table.host_id == host_id_list[i]).all()
                        ru_admin_data = sqlalche_obj.session.query(SetOdu16RUConfTable.adminstate).\
                            filter(
                                SetOdu16RUConfTable.config_profile_id == host_data[0].config_profile_id).all()

                        sync_admin_data = sqlalche_obj.session.query(SetOdu16SyncConfigTable.adminStatus).\
                            filter(SetOdu16SyncConfigTable.config_profile_id == host_data[
                                   0].config_profile_id).all()

                        ra_admin_data = sqlalche_obj.session.query(SetOdu16RAConfTable.raAdminState).\
                            filter(
                                SetOdu16RAConfTable.config_profile_id == host_data[0].config_profile_id).all()

                        if len(get_default_node_type) > 0:
                            if int(get_default_node_type[0].default_node_type) == 1 or int(get_default_node_type[0].default_node_type) == 3:
                                master_host_id = sqlalche_obj.session.query(
                                    MasterSlaveLinking.master).filter(MasterSlaveLinking.slave == host_id_list[i]).all()
                                if len(master_host_id) > 0:
                                    master_host_data = sqlalche_obj.session.query(
                                        Hosts.host_alias, Hosts.host_asset_id).filter(Hosts.host_id == master_host_id[0][0]).all()
                                    host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(
                                        HostAssets.host_asset_id == master_host_data[0].host_asset_id).all()
                                    master_mac = str(host_asset_data[0].ra_mac if len(
                                        host_asset_data) > 0 else "")
                                    peer_status = sqlalche_obj.session.query(GetOdu16PeerNodeStatusTable.sig_strength, GetOdu16PeerNodeStatusTable.link_status).\
                                        filter(GetOdu16PeerNodeStatusTable.host_id == host_id_list[
                                               i]).order_by(desc(GetOdu16PeerNodeStatusTable.timestamp)).limit(1).all()

                    else:
                        ru_admin_data = sqlalche_obj.session.query(Odu100RuConfTable.adminstate, Odu100RuConfTable.defaultNodeType).\
                            filter(Odu100RuConfTable.config_profile_id == host_data[
                                   0].config_profile_id).all()
                        print ru_admin_data
                        sync_admin_data = sqlalche_obj.session.query(Odu100SyncConfigTable.adminStatus).\
                            filter(
                                Odu100SyncConfigTable.config_profile_id == host_data[0].config_profile_id).all()
                        print sync_admin_data

                        ra_admin_data = sqlalche_obj.session.query(Odu100RaConfTable.raAdminState).\
                            filter(Odu100RaConfTable.config_profile_id == host_data[
                                   0].config_profile_id).all()
                        print ra_admin_data

                        ru_status = sqlalche_obj.session.query(Odu100RuStatusTable.ruoperationalState).filter(
                            Odu100RuStatusTable.host_id == host_id_list[i]).limit(1).all()
                        print ru_status, "^^^^"
                        ra_status = sqlalche_obj.session.query(Odu100RaStatusTable.raoperationalState).filter(
                            Odu100RaStatusTable.host_id == host_id_list[i]).order_by(desc(Odu100RaStatusTable.timestamp)).limit(1).all()
                        print ra_status, "^&*"
                        sync_status = sqlalche_obj.session.query(Odu100SynchStatusTable.syncoperationalState).filter(
                            Odu100SynchStatusTable.host_id == host_id_list[i]).order_by(desc(Odu100SynchStatusTable.timestamp)).limit(1).all()
                        print sync_status, "%^&*"
                        if len(ru_status) > 0:
                            if ru_status[0].ruoperationalState == None:
                                ru_op_state = 1
                            else:
                                ru_op_state = ru_status[0].ruoperationalState
                                # print
                                # ru_op_state,"%%%%%%%%%%%%%%%%%%%%%%%%%ru"
                        else:
                            ru_op_state = 1

                        if len(ra_status) > 0:
                            if ra_status[0].raoperationalState == None:
                                ra_op_state = 1
                            else:
                                ra_op_state = ra_status[0].raoperationalState

                        else:
                            ra_op_state = 1

                        if len(sync_status) > 0:
                            if sync_status[0].syncoperationalState == None:
                                sync_op_state = 1
                            else:
                                sync_op_state = sync_status[
                                    0].syncoperationalState

                        else:
                            sync_op_state = 1
                        if int(ru_admin_data[0].defaultNodeType) == 1 or int(ru_admin_data[0].defaultNodeType) == 3:
                            master_host_id = sqlalche_obj.session.query(
                                MasterSlaveLinking.master).filter(MasterSlaveLinking.slave == host_id_list[i]).all()
                            if len(master_host_id) > 0:
                                master_host_data = sqlalche_obj.session.query(
                                    Hosts.host_alias, Hosts.host_asset_id).filter(Hosts.host_id == master_host_id[0][0]).all()
                                host_asset_data = sqlalche_obj.session.query(HostAssets.ra_mac).filter(
                                    HostAssets.host_asset_id == master_host_data[0].host_asset_id).all()
                                master_mac = str(host_asset_data[0].ra_mac if len(
                                    host_asset_data) > 0 else "") + ","
                                peer_status = sqlalche_obj.session.query(Odu100PeerNodeStatusTable.sigStrength1, Odu100PeerNodeStatusTable.linkStatus).\
                                    filter(Odu100PeerNodeStatusTable.host_id == host_id_list[i]).order_by(
                                        desc(Odu100PeerNodeStatusTable.timestamp)).limit(1).all()

                    if host_data[0].device_type_id == UNMPDeviceType.odu16:
                        if len(ru_admin_data) > 0:
                            temp_list.append(int(ru_admin_data[0][0]))
                        if len(sync_admin_data) > 0:
                            temp_list.append(int(sync_admin_data[0][0]))
                        if len(ra_admin_data) > 0:
                            temp_list.append(int(ra_admin_data[0][0]))
                        if len(peer_status) > 0:
                            if peer_status[0].sig_strength == None:
                                temp_list.append(
                                    str(master_host_data[0].host_alias) + "(-)")
                            elif int(peer_status[0].sig_strength) == 1111111:
                                temp_list.append(str(
                                    master_host_data[0].host_alias) + " (Device Unreachable)")
                            else:
                                if peer_status[0].link_status == 1:
                                    temp_list.append(str(
                                        master_host_data[0].host_alias) + "( Link Disconnected )")
                                else:
                                    temp_list.append(str(master_host_data[
                                                     0].host_alias) + " (" + str(peer_status[0].sig_strength) + "dBm)")
                        else:
                            temp_list.append("")
                    else:
                        if len(ru_admin_data) > 0:
                            temp_list.append(int(ru_admin_data[0][0]))
                        if len(sync_admin_data) > 0:
                            temp_list.append(int(sync_admin_data[0][0]))
                        if len(ra_admin_data) > 0:
                            temp_list.append(int(ra_admin_data[0][0]))
                        if len(peer_status) > 0:
                            if peer_status[0].sigStrength1 == None:
                                temp_list.append(
                                    str(master_host_data[0].host_alias) + "(-)")
                            elif int(peer_status[0].sigStrength1) == 1111111:
                                temp_list.append(str(
                                    master_host_data[0].host_alias) + " (Device Unreachable)")
                            elif peer_status[0].sigStrength1 == None:
                                temp_list.append(
                                    str(master_host_data[0].host_alias) + "(-)")
                            else:
                                if int(peer_status[0].linkStatus) == 1:
                                    temp_list.append(str(
                                        master_host_data[0].host_alias) + " ( Link Disconnected )")
                                else:
                                    temp_list.append(str(master_host_data[
                                                     0].host_alias) + " (" + str(peer_status[0].sigStrength1) + "dBm)")
                        else:
                            temp_list.append("")
                    op_status = essential_obj.get_hoststatus(host_id_list[i])
                    if op_status == None:
                        op_img = "images/host_status0.png"
                    elif op_status == 0:
                        op_img = "images/host_status0.png"
                    else:
                        op_img = "images/host_status1.png"
                    temp_list.append(op_img)
                    temp_list.append(0 if op_status == None else op_status)

                    temp_list.append(int(ru_op_state))
                    temp_list.append(int(sync_op_state))
                    temp_list.append(int(ra_op_state))
                    admin_data_dic.update({host_id_list[i]: temp_list})
            result['result'] = admin_data_dic
        except Exception as e:
            result['success'] = 1
            result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

# obj = OduStatus()
# print obj.admin_state_change(28,'odu100','ru.ra.raConfTable.raAdminState',1)
# print obj.global_admin_request('4,5')


def get_modulation_rate(host_id):
    """

    @param host_id:
    @return:
    """
    global errorStatus
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    host_data = sqlalche_obj.session.query(
        Hosts).filter(Hosts.host_id == host_id).all()
    sqlalche_obj.sql_alchemy_db_connection_close()
    modulation_rate_result = bulktable(
        '1.3.6.1.4.1.26149.2.2.13.10.1', host_data[0].ip_address,
                                       int(host_data[0].snmp_port), host_data[0].snmp_read_community, 20)
    if modulation_rate_result['success'] == 1:
        for i in modulation_rate_result['result']:
            modulation_rate_result['result'] = errorStatus.get(
                i, "Device is busy.Please try again")
    return modulation_rate_result


def refresh_channel_freq_list_table(host_id, device_type):
    """

    @param host_id:
    @param device_type:
    @return:
    """
    global sqlalche_obj
    global errorStatus
    result = {'success': 0, 'result': {}}
    try:
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        global preferred_channel_dic
        flag = 1
        time.sleep(5)
        preferred_channel_dic = {}
        preferred_channel_dic.setdefault('name', []).append(0)
        preferred_channel_dic.setdefault('value', []).append(0)
        if len(host_data) > 0:
            i = 0
            while(i < 8):
                time.sleep(2)
                # snmp_get_result =
                # bulktable('1.3.6.1.4.1.26149.2.2.13.3.1',host_data[0].ip_address,int(host_data[0].snmp_port),host_data[0].snmp_read_community,20)
                flag = 0
                if snmp_get_result['success'] == 0:
                    channel_list = sqlalche_obj.session.query(Odu100RaChannelListTable).filter(
                        Odu100RaChannelListTable.host_id == host_id).delete()
                    sqlalche_obj.session.commit()
                    for i in snmp_get_result['result']:
                        channel_add = Odu100RaChannelListTable(host_id, snmp_get_result['result'][i][0], snmp_get_result['result'][i]
                                                               [1], snmp_get_result['result'][i][2], snmp_get_result['result'][i][3])
                        preferred_channel_dic.setdefault('name', []).append(
                            snmp_get_result['result'][i][3])
                        preferred_channel_dic.setdefault('value', []).append(
                            snmp_get_result['result'][i][3])
                        sqlalche_obj.session.add(channel_add)
                    sqlalche_obj.session.commit()
                    break
                else:
                    if 553 in snmp_get_result['result']:
                        time.sleep(15)
                        i = i + 1
                        flag = 1
                        continue
                    elif 551 in snmp_get_result['result']:
                        result[result] = errorStatus.get(551)
                        result['success'] = 1
                    else:
                        for i in snmp_get_result['result']:
                            if snmp_get_result[i] != 0:
                                snmp_result['result'] = errorStatus.get(
                                    i, "Device is busy.Please try again Later")
                        result['success'] = 1
            if flag == 1:
                result['success'] = 1
                result['result'] = flag

    except Exception as e:
        result = {'result': str(e), 'success': 1}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result


def channel_list_refresh(host_id, selected_device):
    """

    @param host_id:
    @param selected_device:
    @return:
    """
    global sqlalche_obj
    global errorStatus
    result = {'success': 0, 'result': {}}

    try:
        sqlalche_obj.sql_alchemy_db_connection_open()
        host_data = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        snmp_get_result = bulktable(
            '1.3.6.1.4.1.26149.2.2.13.3.1', host_data[0].ip_address,
                                    int(host_data[0].snmp_port), host_data[0].snmp_read_community, 20)
        if snmp_get_result['success'] == 0:
            channel_list = sqlalche_obj.session.query(Odu100RaChannelListTable).filter(
                Odu100RaChannelListTable.host_id == host_id).delete()
            sqlalche_obj.session.commit()
            for i in snmp_get_result['result']:
                channel_add = Odu100RaChannelListTable(
                    host_id, snmp_get_result['result'][
                        i][0], snmp_get_result['result'][i][1],
                                                       snmp_get_result['result'][i][2], snmp_get_result['result'][i][3])
                sqlalche_obj.session.add(channel_add)
            sqlalche_obj.session.commit()
            result['result'] = "RA Channel List updated successfully"
        else:
            for i in snmp_get_result["result"]:
                    # return snmp_result
                if i == 553:
                    result["result"] = str(host_data[0].host_alias) + " (" + str(host_data[0].ip_address) + ") " + str(
                        errorStatus.get(i, "SNMP agent Unknown Error Occured"))
                elif i == 551:
                    result["result"] = str(host_data[0].host_alias) + " (" + str(host_data[0].ip_address) + ") " + str(
                        errorStatus.get(i, "SNMP agent Unknown Error Occured"))
                elif snmp_get_result["result"][i] != 0:
                    result["result"] = str(host_data[0].host_alias) + " (" + str(host_data[0].ip_address) + ") " + str(
                        errorStatus.get(snmp_get_result["result"][i], "SNMP agent Unknown Error Occured"))
            result['success'] = 1
    except Exception as e:
        result = {'result':
            "UNMP has encountered an error.Please retry again %s" % (e), 'success': 1}
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result

# print channel_list_refresh(28,'odu100')


def bw_get_value(host_id, device_type):
    """

    @param host_id:
    @param device_type:
    @return:
    """
    global errorStatus
    global sqlalche_obj
    result = {'success': 0, 'result': {}}
    try:
        sqlalche_obj.sql_alchemy_db_connection_open()
        device_param_list = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        get_dic = {'tx_rate': '1.3.6.1.4.1.26149.2.2.5.1.11.1', 'tx_time':
            '1.3.6.1.4.1.26149.2.2.5.1.10.1', 'tx_bw': '1.3.6.1.4.1.26149.2.2.5.1.12.1'}
        snmp_get = pysnmp_geter(get_dic, device_param_list[0].ip_address, int(
            device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
        if int(snmp_get['success']) == 0:
            for i in snmp_get['result']:
                result['result'].update({i: snmp_get['result'][i]})
            result['success'] = 0
            return
        else:
            for i in snmp_get['result']:
                result = {'success': 1, 'result':
                    errorStatus.get(i, "SNMP Agent Down ")}
                return
    except Exception as e:
        result['success'] = 1
        result['result'] = str(e)
        return
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result


def bw_calc(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    global sqlalche_obj
    global errorStatus
    result = {'success': 0, 'result': {}}
    try:
        oid_dic = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        device_param_list = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()
        get_dic = {'tx_rate': '1.3.6.1.4.1.26149.2.2.5.1.11.1', 'tx_time':
            '1.3.6.1.4.1.26149.2.2.5.1.10.1', 'tx_bw': '1.3.6.1.4.1.26149.2.2.5.1.12.1'}
        if len(device_param_list) > 0:
            snmp_get_result = pysnmp_get('1.3.6.1.4.1.26149.2.2.5.1.7', device_param_list[0].ip_address, int(
                device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
            if snmp_get_result['success'] == 0:
                for i in snmp_get_result['result']:
                    if int(snmp_get_result['result'][i]) == 1:
                        result['success'] = 1
                        result['result'] = "Some Another OM Operation is running.Please try after some time..."
                        return
                    else:
                        for i in dic_result:
                            if i == "success":
                                continue
                            if i == "tx_rate":
                                oid_dic.update({i: [
                                               '1.3.6.1.4.1.26149.2.2.5.1.11.1', 'Integer32', dic_result[i]]})
                            if i == "tx_time":
                                oid_dic.update({i: [
                                               '1.3.6.1.4.1.26149.2.2.5.1.10.1', 'Integer32', dic_result[i]]})
                        snmp_set_result = pysnmp_set(oid_dic, device_param_list[0].ip_address, int(
                            device_param_list[0].snmp_port), device_param_list[0].snmp_write_community)
                        if int(snmp_set_result['success']) == 0:
                            for i in snmp_set_result['result']:
                                if snmp_set_result['result'][i] != 0:
                                    result = {'success': 1,
                                        'result': errorStatus.get(i, "SNMP Agent Down")}
                                    return
                                else:
                                    continue
                            snmp_om_set_result = pysnmp_set({'om_operation': ['1.3.6.1.4.1.26149.2.2.5.1.2.1', 'Integer32', 7]}, device_param_list[0]
                                                             .ip_address, device_param_list[0].snmp_port, device_param_list[0].snmp_write_community)
                            if int(snmp_om_set_result['success']) == 0:
                                snmp_get = pysnmp_geter(get_dic, device_param_list[0].ip_address, int(
                                    device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
                                if int(snmp_get['success']) == 0:
                                    for i in snmp_get['result']:
                                        result['result'].update(
                                            {i: snmp_get['result'][i]})
                                    result['success'] = 0
                                    return
                                else:
                                    for i in snmp_om_set_result['result']:
                                        result = {'success': 1,
                                            'result': errorStatus.get(i, "SNMP Agent Down ")}
                                        return

                            else:
                                for i in snmp_om_set_result['result']:
                                    result = {'success': 1,
                                        'result': errorStatus.get(i, "SNMP Agent Down")}
                                    return
                        else:
                            for i in snmp_om_set_result['result']:
                                result = {'success': 1,
                                    'result': errorStatus.get(i, "SNMP Agent Down")}
                                return

            else:
                for i in snmp_get_result['result']:
                    if int(i) == 553:
                        result['result'] = errorStatus.get(
                            i, "Device is busy,please try again later")
                    elif int(i) == 551:
                        result['result'] = errorStatus.get(
                            i, "Device is busy,please try again later")
                    elif snmp_get_result['result'][i] != 0:
                        result['result'] = errorStatus.get(
                            snmp_get_result['result'][i], "Device is busy,please try again later ")
                    else:
                        result['result'] = errorStatus.get(
                            i, "Device is not responding")
                    result['success'] = 1
                    return

        else:
            result = {'success': 1, 'result': "No Host Exist"}
    except Exception as e:
        result['success'] = 1
        result['result'] = str(e)
        return
    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result


def delete_ra_channel_list(host_id):
    """

    @param host_id:
    """
    global sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    sqlalche_obj.db.execute(
        "delete from odu100_raChannelListTable where host_id='%s'" % (host_id))
    sqlalche_obj.sql_alchemy_db_connection_close()


def get_site_survey_bll(host_id):
    """

    @param host_id:
    @return:
    """
    global sqlalche_obj, errorStatus
    result = {'success': 0, 'result': ""}
    try:
        # print "hello"
        sqlalche_obj.sql_alchemy_db_connection_open()
        device_param_list = sqlalche_obj.session.query(
            Hosts).filter(Hosts.host_id == host_id).all()

        result = bulktable('1.3.6.1.4.1.26149.2.2.13.11.1', device_param_list[0].ip_address, int(
            device_param_list[0].snmp_port), device_param_list[0].snmp_read_community)
        if result['success'] == 0:
            sqlalche_obj.db.execute(
                "delete from odu100_raSiteSurveyResultTable where host_id='%s'" % (host_id))
            sqlalche_obj.session.commit()
            time.sleep(1)
            for i in range(0, len(result["result"])):
                sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)" % (
                    'odu100_raSiteSurveyResultTable', host_id, str(result["result"][i + 1])[1:-1]))
            sqlalche_obj.session.commit()
            result = {'success': 0}
        else:
            result['success'] = 1
            if 553 in result["result"]:
                result = {"success": 1, "result":
                    "No Response From Device.Please Try Again"}
            elif 551 in result["result"]:
                result = {"success": 1, "result": "Network is unreachable"}
            elif 99 in result["result"]:
                result = {"success": 1, "result":
                    "UNMP has encountered an unexpected error. Please Retry "}
            else:
                for i in result['result']:
                    if result['result'][i] != 0:
                        result['result'] = str(errorStatus.get(
                            result['result'][i], "Device Unresponsive"))

    except OperationalError as e:
        result = {"success": 1, "result":
            "UNMP Database Server is Busy at the moment, please try again later.", "detail": str(e)}
    except DisconnectionError as e:
        result = {"success": 1, "result": "Database Disconnected",
            "detail": ""}
    except Exception as e:
        result = {'success': 1, 'result':
            "UNMP Web Server is Busy at the moment, please try again later %s" % (e)}

    finally:
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result



# print get_site_survey_bll('4')
##{'result': {'txtime': '90', 'txrate': '100', 'txbw': '-324'}, 'success': 0}
# obj = OduStatus()
# print obj.global_admin_request("43,79,80")
#{'result': {1: ['1', '1', '36', '5180'], 2: ['1', '2', '37', '5185'], 3: ['1', '3', '38', '5190'], 4: ['1', '4', '39', '5195'], 5: ['1', '5', '40', '5200'], 6: ['1', '6', '41', '5205'], 7: ['1', '7', '42', '5210'], 8: ['1', '8', '43', '5215'], 9: ['1', '9', '44', '5220'], 10: ['1', '10', '45', '5225'], 11: ['1', '11', '46', '5230'], 12: ['1', '12', '47', '5235'], 13: ['1', '13', '48', '5240'], 14: ['1', '14', '52', '5260'], 15: ['1', '15', '53', '5265'], 16: ['1', '16', '54', '5270'], 17: ['1', '17', '55', '5275'], 18: ['1', '18', '56', '5280'], 19: ['1', '19', '57', '5285'], 20: ['1', '20', '58', '5290'], 21: ['1', '21', '59', '5295'], 22: ['1', '22', '60', '5300'], 23: ['1', '23', '61', '5305'], 24: ['1', '24', '62', '5310'], 25: ['1', '25', '63', '5315'], 26: ['1', '26', '64', '5320'], 27: ['1', '27', '149', '5745'], 28: ['1', '28', '150', '5750'], 29: ['1', '29', '151', '5755'], 30: ['1', '30', '152', '5760'], 31: ['1', '31', '153', '5765'], 32: ['1', '32', '154', '5770'], 33: ['1', '33', '155', '5775'], 34: ['1', '34', '156', '5780'], 35: ['1', '35', '157', '5785'], 36: ['1', '36', '158', '5790'], 37: ['1', '37', '159', '5795'], 38: ['1', '38', '160', '5800'], 39: ['1', '39', '161', '5805'], 40: ['1', '40', '162', '5810'], 41: ['1', '41', '163', '5815'], 42: ['1', '42', '164', '5820'], 43: ['1', '43', '165', '5825'], 44: ['1', '44', '166', '5830'], 45: ['1', '45', '167', '5835'], 46: ['1', '46', '168', '5840'], 47: ['1', '47', '169', '5845'], 48: ['1', '48', '170', '5850'], 49: ['1', '49', '171', '5855'], 50: ['1', '50', '172', '5860'], 51: ['1', '51', '173', '5865'], 52: ['1', '52', '174', '5870'], 53: ['1', '53', '175', '5875'], 54: ['1', '54', '176', '5880'], 55: ['1', '55', '177', '5885']}, 'success': 0}
