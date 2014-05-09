#!/usr/bin/python2.6

import time
import urllib2
import base64
import socket
from nms_config import *
from common_controller import *
from unmp_model import *
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
##                         Switch Controller                                 ##
##                                                                           ##
##                 CodeScape Consultants Pvt. Ltd.                           ##
##                                                                           ##
##                     Dated:27 August 2011                                  ##
##                                                                           ##
###############################################################################

###############################################################################


# Creating Session#####################################
# session=session_db()
my = SqlAlchemyDBConnection()

error_dic = {100: 'Continue.Request received, please continue',
             101: 'Switching Protocols.Switching to new protocol obey Upgrade header',
             200: 'OK.Request fulfilled, document follows',
             201: 'Created .Document created, URL follows',
             202: 'Accepted.Request accepted, processing continues off-line',
             203: 'Non-Authoritative Information.Request fulfilled from cache',
             204: 'No Content.Request fulfilled, nothing follows',
             205: 'Reset Content.Clear input form for further input.',
             206: 'Partial Content.Partial content follows.',
             300: 'Multiple Choices.Object has several resources -- see URI list',
             301: 'Moved Permanently.Object moved permanently -- see URI list',
             302: 'Found.Object moved temporarily -- see URI list',
             303: 'See Other.Object moved -- see Method and URL list',
             304: 'Not Modified.Document has not changed since given time',
             305: 'Use Proxy.You must use proxy specified in Location to access this resource.',
             307: 'Temporary Redirect.Object moved temporarily -- see URI list',
             400: 'Bad Request.Bad request syntax or unsupported method',
             401: 'Unauthorized.No permission -- see authorization schemes',
             402: 'Payment Required.No payment -- see charging schemes',
             403: 'Forbidden.Request forbidden -- authorization will not help',
             404: 'Not Found.Nothing matches the given URI',
             405: 'Method Not Allowed.Specified method is invalid for this server.',
             406: 'Not Acceptable.URI not available in preferred format.',
             407: 'Proxy Authentication Required.You must authenticate with this proxy before proceeding.',
             408: 'Request Timeout.Request timed out; try again later.',
             409: 'Conflict.Request conflict.',
             410: 'Gone.URI no longer exists and has been permanently removed.',
             411: 'Length Required.Client must specify Content-Length.',
             412: 'Precondition Failed.Precondition in headers is false.',
             413: 'Request Entity Too Large.Entity is too large.',
             414: 'Request-URI Too Long.URI is too long.',
             415: 'Unsupported Media Type.Entity body in unsupported format.',
             416: 'Requested Range Not Satisfiable.Cannot satisfy request range.',
             417: 'Expectation Failed.Expect condition could not be satisfied.',
             500: 'Internal Server Error.Server got itself in trouble',
             501: 'Not Implemented.Server does not support this operation',
             502: 'Bad Gateway.Invalid responses from another server/proxy.',
             503: 'Service Unavailable.The server cannot process the request due to a high load',
             504: 'Gateway Timeout.The gateway server did not receive a timely response',
             505: 'HTTP Version Not.Supported.Cannot fulfill request.',
             113: 'Device is not Connected'}


def check_connection():
    """


    @return:
    """
    global my
    return my.error


def get_device_list_swt_profiling(ip_address, mac_address, selected_device):
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
    global my
    # try block starts
    try:
        # here we create the session of sqlalchemy
        my.sql_alchemy_db_connection_open()
        # this is the query which returns the multidimensional array of hosts
        # table and store in device_tuple
        device_tuple = my.session.query(
            Hosts.host_id, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address).filter(
            and_(Hosts.is_deleted == 0, Hosts.ip_address.like('%s%%' % (ip_address)),
                 Hosts.mac_address.like('%s%%' % (mac_address)), Hosts.device_type_id == selected_device)).order_by(
            Hosts.host_alias).order_by(Hosts.ip_address).all()
        total_record = len(device_tuple)
        my.sql_alchemy_db_connection_close()
        # this loop create a mutildimesional list of host
        if total_record == 0:
            return 0
        elif total_record > 1:
            return 1
        else:
            return device_tuple[0][0]

    # try block ends

    # exception starts
    except Exception as e:
        return 2
    finally:
        my.sql_alchemy_db_connection_close()

# print get_device_list_swt_profiling('','','swt4')
# Switch 4 Port get functions ############################################


def swt4_get_ip(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt4_ip_table = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt4_ip_table = my.session.query(Swt4IpSettings.mode, Swt4IpSettings.ip_address, Swt4IpSettings.subnet_mask,
                                             Swt4IpSettings.gateway).filter(
                Swt4IpSettings.config_profile_id == swt4_profile_id[0]).all()
        my.sql_alchemy_db_connection_close()
        if swt4_ip_table == None or swt4_ip_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt4_ip_table, "detail": ""}

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


def swt4_get_bandwidth_control(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt4_bandwidth_table = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt4_bandwidth_table = my.session.query(Swt4BandwidthControl.cpu_protection, Swt4BandwidthControl.port,
                                                    Swt4BandwidthControl.type, Swt4BandwidthControl.state,
                                                    Swt4BandwidthControl.rate).filter(
                Swt4BandwidthControl.config_profile_id == swt4_profile_id[0]).order_by(Swt4BandwidthControl.port).all()
        my.sql_alchemy_db_connection_close()
        if swt4_bandwidth_table == None or swt4_bandwidth_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt4_bandwidth_table, "detail": ""}

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

# print swt4_get_bandwidth_control('11ff91c2-fd83-11e0-a284-e069956899a4')


def swt4_get_storm_control(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt4_storm_table = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt4_storm_table = my.session.query(Swt4StormControl.strom_type, Swt4StormControl.state,
                                                Swt4StormControl.rate).filter(
                Swt4StormControl.config_profile_id == swt4_profile_id[0]).order_by(Swt4StormControl.strom_type).all()
        my.sql_alchemy_db_connection_close()
        if swt4_storm_table == None or swt4_storm_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt4_storm_table, "detail": ""}

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


def swt4_get_port_data(host_id):
    """
    Author - Anuj Samariya
    This function is used to get the data of omc configuration table
    host_id - this id is used to get the specific config profile id i.e. config_profile_id
    return the omc configuration table data and config profile id
    @param host_id:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt4_port_table = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt4_port_table = my.session.query(Swt4PortSettings.link_fault_pass_through, Swt4PortSettings.port,
                                               Swt4PortSettings.state, Swt4PortSettings.speed,
                                               Swt4PortSettings.flow_control).filter(
                Swt4PortSettings.config_profile_id == swt4_profile_id[0]).order_by(Swt4PortSettings.port).all()
        my.sql_alchemy_db_connection_close()
        if swt4_port_table == None or swt4_port_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt4_port_table, "detail": ""}

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


def swt4_get_vlan_data(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt4_vlan_table = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt4_vlan_table = my.session.query(
                Swt4VlanSettings.vlan_ingress_filter, Swt4VlanSettings.vlan_pass_all, Swt4VlanSettings.port,
                Swt4VlanSettings.pvid, Swt4VlanSettings.mode).filter(
                Swt4VlanSettings.config_profile_id == swt4_profile_id[0]).order_by(Swt4VlanSettings.port).all()
        my.sql_alchemy_db_connection_close()
        if swt4_vlan_table == None or swt4_vlan_table == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt4_vlan_table, "detail": ""}

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


def swt4_get_port_priority(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        port_priority = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            port_priority = my.session.query(Swt4PortBasedPriority.port, Swt4PortBasedPriority.priority).filter(
                Swt4PortBasedPriority.config_profile_id == swt4_profile_id[0]).order_by(
                Swt4PortBasedPriority.port).all()
        my.sql_alchemy_db_connection_close()
        if port_priority == None or port_priority == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": port_priority, "detail": ""}

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


def swt4_get_dscp_priority(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        dscp_priority = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            dscp_priority = my.session.query(Swt4DscpBasedPriority.dscp, Swt4DscpBasedPriority.priority).filter(
                Swt4DscpBasedPriority.config_profile_id == swt4_profile_id[0]).order_by(
                Swt4DscpBasedPriority.dscp).all()
        my.sql_alchemy_db_connection_close()
        if dscp_priority == None or dscp_priority == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": dscp_priority, "detail": ""}

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


def swt4_get_801_priority(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt4_801_priority = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt4_801_priority = my.session.query(Swt48021pBasedPriority.p802, Swt48021pBasedPriority.priority).filter(
                Swt48021pBasedPriority.config_profile_id == swt4_profile_id[0]).order_by(
                Swt48021pBasedPriority.p802).all()
        my.sql_alchemy_db_connection_close()
        if swt4_801_priority == None or swt4_801_priority == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt4_801_priority, "detail": ""}

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


def swt4_get_ip_base_priority(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        ip_priority = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            ip_priority = my.session.query(
                Swt4IpBasePriority.ip_base_priority, Swt4IpBasePriority.ip_type, Swt4IpBasePriority.ip_address,
                Swt4IpBasePriority.network_mask, Swt4IpBasePriority.priority).filter(
                Swt4IpBasePriority.config_profile_id == swt4_profile_id[0]).order_by(Swt4IpBasePriority.ip_type).all()
        my.sql_alchemy_db_connection_close()
        if ip_priority == None or ip_priority == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": ip_priority, "detail": ""}

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


def swt4_get_queue_prority(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        queue_priority = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            queue_priority = my.session.query(Swt4QueueBasedPriority.qid_map, Swt4QueueBasedPriority.priority).filter(
                Swt4QueueBasedPriority.config_profile_id == swt4_profile_id[0]).order_by(
                Swt4QueueBasedPriority.qid_map).all()
        my.sql_alchemy_db_connection_close()
        if queue_priority == None or queue_priority == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": queue_priority, "detail": ""}

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


def swt4_get_queue_weight(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        queue_weight = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            queue_weight = my.session.query(Swt4QueueWeightBased.queue, Swt4QueueWeightBased.weight).filter(
                Swt4QueueWeightBased.config_profile_id == swt4_profile_id[0]) \
                .order_by(Swt4QueueWeightBased.queue).all()
        my.sql_alchemy_db_connection_close()
        if queue_weight == None or queue_weight == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": queue_weight, "detail": ""}

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


def swt4_get_qos_abstraction(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        qos_abstraction = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            qos_abstraction = my.session.query(Swt4QosArbitration.priority, Swt4QosArbitration.level).filter(
                Swt4QosArbitration.config_profile_id == swt4_profile_id[0]).order_by(Swt4QosArbitration.priority).all()
        my.sql_alchemy_db_connection_close()
        if qos_abstraction == None or qos_abstraction == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": qos_abstraction, "detail": ""}

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


def swt4_get_1p_remarking(host_id):
    """

    @param host_id:
    @return:
    """
    try:
        global my
        my.sql_alchemy_db_connection_open()
        swt4_profile_id = []
        swt_1p_remarking = []
        swt4_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        if swt4_profile_id == None or swt4_profile_id == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            swt_1p_remarking = my.session.query(Swt41pRemarking.p_remarking, Swt41pRemarking.p802_remarking).filter(
                Swt41pRemarking.config_profile_id == swt4_profile_id[0]).order_by(Swt41pRemarking.p_remarking).all()
        my.sql_alchemy_db_connection_close()
        if swt_1p_remarking == None or swt_1p_remarking == []:
            return {"success": 1, "result": "", "detail": ""}
        else:
            return {"success": 0, "result": swt_1p_remarking, "detail": ""}

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


class MakeSwtSelectListWithDic(object):
    """
    Switch 4 configuration class: Unused now
    """
    def ip_mode_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                            select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        ip_mode_select_dic = {'name': ['StaticIp', 'DHCP'],
                              'value': ['static', 'dhcp']}
        return make_select_list_using_dictionary(ip_mode_select_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def link_fault_pass_through_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                            select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        link_fault_pass_through_select_list_dic = {'name': [
            'Disabled', 'Enabled'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(link_fault_pass_through_select_list_dic, selected_field,
                                                 selected_list_state, selected_list_id, is_readonly,
                                                 select_list_initial_msg)

    def port_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                         select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        port_select_list_dic = {'name': ['1', '2', '3', '4'],
                                'value': ['0', '1', '2', '3']}
        return make_select_list_using_dictionary(port_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def state_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                          select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        state_select_list_dic = {'name': ['Disable', 'Enable'],
                                 'value': ['0', '1']}
        return make_select_list_using_dictionary(state_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def speed_duplex_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                 select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        speed_duplex_select_list_dic = {'name': ['Auto', '10M/half', '10M/full',
                                                 '100M/half', '100M/full'], 'value': ['0', '1', '2', '3', '4']}
        return make_select_list_using_dictionary(speed_duplex_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def flow_control_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                 select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        flow_control_select_list_dic = {'name': ['Off', 'On'],
                                        'value': ['0', '1']}
        return make_select_list_using_dictionary(flow_control_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def vlan_ingress_filter_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                        select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        vlan_ingress_filter_select_list_dic = {'name': ['Disable',
                                                        'Enable'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(vlan_ingress_filter_select_list_dic, selected_field,
                                                 selected_list_state, selected_list_id, is_readonly,
                                                 select_list_initial_msg)

    def vlan_pass_all_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                  select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        vlan_pass_all_select_list_dic = {'name': ['Disable',
                                                  'Enable'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(vlan_pass_all_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def vlan_port_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                              select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        vlan_port_select_list_dic = {'name': ['Port 1', 'Port 2',
                                              'Port 3', 'Port 4', 'Port 5'], 'value': ['0', '1', '2', '3', '4']}
        return make_select_list_using_dictionary(vlan_port_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def vlan_mode_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                              select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        vlan_mode_select_list_dic = {'name': ['Original',
                                              'keep Format'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(vlan_mode_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def bandwidth_cpu_protect_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                          select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        bandwidth_cpu_protect_select_list_dic = {'name': [
            'Disable', 'Enable'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(bandwidth_cpu_protect_select_list_dic, selected_field,
                                                 selected_list_state, selected_list_id, is_readonly,
                                                 select_list_initial_msg)

    def bandwidth_port_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                   select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        bandwidth_port_select_list_dic = {'name': ['Port 1', 'Port 2', 'Port 3',
                                                   'Port 4', 'Port 5'], 'value': ['0', '1', '2', '3', '4']}
        return make_select_list_using_dictionary(bandwidth_port_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def bandwidth_type_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                   select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        bandwidth_type_select_list_dic = {'name': ['Ingress',
                                                   'Egress'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(bandwidth_type_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def bandwidth_state_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                    select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        bandwidth_state_select_list_dic = {'name': ['Disable',
                                                    'Enable'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(bandwidth_state_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def storm_type_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                               select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        storm_type_select_list_dic = {'name': ['Broadcast',
                                               'Multicast', 'UDA'], 'value': ['0', '1', '2']}
        return make_select_list_using_dictionary(storm_type_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def storm_state_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        storm_state_select_list_dic = {'name': ['off', 'on'],
                                       'value': ['0', '1']}
        return make_select_list_using_dictionary(storm_state_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def storm_rate_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                               select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        storm_rate_select_list_dic = {'name': ['10', '20', '40', '80', '160', '320',
                                               '640'], 'value': ['10', '20', '40', '80', '160', '320', '640']}
        return make_select_list_using_dictionary(storm_rate_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def common_enable_disable_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                          select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        common_enable_disable_select_list_dic = {'name': [
            'Disable', 'Enable'], 'value': ['0', '1']}
        return make_select_list_using_dictionary(common_enable_disable_select_list_dic, selected_field,
                                                 selected_list_state, selected_list_id, is_readonly,
                                                 select_list_initial_msg)

    def common_port_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        common_port_select_list_dic = {'name': ['Port 1', 'Port 2',
                                                'Port 3', 'Port 4', 'Port 5'], 'value': ['0', '1', '2', '3', '4']}
        return make_select_list_using_dictionary(common_port_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def common_priority_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                    select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        common_priority_select_list_dic = {'name': ['0', '1', '2',
                                                    '3'], 'value': ['0', '1', '2', '3']}
        return make_select_list_using_dictionary(common_priority_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def dscp_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                         select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        dscp_select_list_dic = {
        'name': ["EF", "AFL1", "AFM1", "AFH1", "AFL2", "AFM2", "AFH2", "AFL3", "AFM3", "AFH3", "AFL4", "AFM4", "AFH4",
                 "NC", "BF"], 'value': ["ef", "afl1", "afm1", "afh1",
                                        "afl2", "afm2", "afh2", "afl3", "afm3", "afh3", "afl4", "afm4", "afh4", "nc",
                                        "bf"]}
        for i in range(1, 63):
            dscp_select_list_dic.setdefault('name', []).append(str(i))
            dscp_select_list_dic.setdefault('value', []).append(str(i))
        return make_select_list_using_dictionary(dscp_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def select_list_802p(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                         select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        select_list_802p_dic = {'name': ['0', '1', '2', '3', '4',
                                         '5', '6', '7'], 'value': ['0', '1', '2', '3', '4', '5', '6', '7']}
        return make_select_list_using_dictionary(select_list_802p_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def ip_type_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                            select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        ip_type_select_list_dic = {'name': ['Group A', 'Group B'],
                                   'value': ['0', '1']}
        return make_select_list_using_dictionary(ip_type_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def queue_weight_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                 select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        queue_weight_select_list_dic = {'name': ['0', '1', '2', '3', '4', '5', '6', '7',
                                                 '8'], 'value': ['0', '1', '2', '3', '4', '5', '6', '7', '8']}
        return make_select_list_using_dictionary(queue_weight_select_list_dic, selected_field, selected_list_state,
                                                 selected_list_id, is_readonly, select_list_initial_msg)

    def qos_abstaction_priority_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                            select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        qos_abstaction_priority_select_list_dic = {'name': ['DSCP',
                                                            'PORT', 'DOT1P'], 'value': ['dscp', 'port', 'dot1p']}
        return make_select_list_using_dictionary(qos_abstaction_priority_select_list_dic, selected_field,
                                                 selected_list_state, selected_list_id, is_readonly,
                                                 select_list_initial_msg)

    def qos_abstaction_level_select_list(self, selected_field, selected_list_state, selected_list_id, is_readonly,
                                         select_list_initial_msg):
        """

        @param selected_field:
        @param selected_list_state:
        @param selected_list_id:
        @param is_readonly:
        @param select_list_initial_msg:
        @return:
        """
        qos_abstaction_level_select_list_dic = {'name': ['0', '1',
                                                         '2', '3', '4'], 'value': ['0', '1', '2', '3', '4']}
        return make_select_list_using_dictionary(qos_abstaction_level_select_list_dic, selected_field,
                                                 selected_list_state, selected_list_id, is_readonly,
                                                 select_list_initial_msg)


def swt4_ip_set(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        response = ""
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username,
            Hosts.http_password).filter(Hosts.host_id == host_id).all()
        if dic_result['result']['swt_ip_mode_selection'] == "static":
            url = "http://%s/ip_settings.cgi?mode=%s&ip=%s&msk=%s&gw=%s&dhcp_var=0&ipsetsubmit=Apply" \
                  % (
                config_profile_id[0][
                    1], dic_result['result']['swt_ip_mode_selection'],
                dic_result['result'][
                    'swt4_ip_address'], dic_result['result']['swt4_subnet_mask'],
                dic_result['result']['swt4_gateway'])
        else:
            url = "http://" + config_profile_id[0][1] + "ip_settings.cgi"
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        try:
            f = urllib2.urlopen(req, timeout=15)
            response = f.read()
        except Exception as e:
            {'success': 1, 'result': 'hello'}
        if len(config_profile_id) > 0:
            url = "http://" + dic_result['result']['swt4_ip_address']
            req = urllib2.Request(url)
            auth_string = base64.encodestring(
                "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
            req.add_header("Authorization", "Basic %s" % auth_string)
            f = urllib2.urlopen(req, timeout=15)
            response = f.read()
            res = str(response).find("SFS-400")
            if res > 0:

                swt4_data = my.session.query(Swt4IpSettings) \
                    .filter(and_(Swt4IpSettings.config_profile_id == config_profile_id[0][0])).all()
                if len(swt4_data) > 0:
                    swt4_data[0].mode = dic_result[
                        'result']['swt_ip_mode_selection']
                    swt4_data[0].ip_address = dic_result[
                        'result']['swt4_ip_address']
                    swt4_data[0].subnet_mask = dic_result[
                        'result']['swt4_subnet_mask']
                    swt4_data[0].gateway = dic_result['result']['swt4_gateway']
            host_data = my.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            host_data[0].ip_address = dic_result['result']['swt4_ip_address']
            host_data[0].netmask = dic_result['result']['swt4_subnet_mask']
            host_data[0].gateway = dic_result['result']['swt4_gateway']
            my.session.commit()
            my.sql_alchemy_db_connection_close()
            url = "http://" + str(dic_result['result']['swt4_ip_address']) + \
                  "/configuration.cgi?config_submit=++Config+Save++"
            req = urllib2.Request(url)
            auth_string = base64.encodestring(
                "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
            req.add_header("Authorization", "Basic %s" % auth_string)
            f = urllib2.urlopen(req)
            response = f.read()
            dic_result['result']['swt_ip_mode_selection'] = 0
            dic_result['result']['swt4_ip_address'] = 0
            dic_result['result']['swt4_subnet_mask'] = 0
            dic_result['result']['swt4_gateway'] = 0
            return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}

    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_port_setting_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username,
            Hosts.http_password).filter(Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/portsettings.cgi?lfp=%s&lfp_submit=Apply" % (
            dic_result['result']['swt_link_fault_selection'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        url = "http://%s/portsettings.cgi?portnoid=%s&portstate=%s&speed_duplex=%s&flow=%s&portsetting_submit=Apply" \
              % (
            config_profile_id[0][1], dic_result[
                'result']['port_select_list_id'],
            dic_result['result']['state_select_list_id'], dic_result[
                'result']['speed_duplex_list_id'],
            dic_result['result']['flow_control_select_list'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            port_data = my.session.query(Swt4PortSettings) \
                .filter(and_(Swt4PortSettings.config_profile_id == config_profile_id[0][0],
                             Swt4PortSettings.port == dic_result['result']['port_select_list_id'])).all()
            if len(port_data) > 0:
                port_data[0].link_fault_pass_through = dic_result[
                    'result']['swt_link_fault_selection']
                port_data[0].port = dic_result['result']['port_select_list_id']
                port_data[0].state = dic_result['result'][
                    'state_select_list_id']
                port_data[0].speed = dic_result['result'][
                    'speed_duplex_list_id']
                port_data[0].flow_control = dic_result[
                    'result']['flow_control_select_list']
        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result['result']['swt_link_fault_selection'] = 0
        dic_result['result']['port_select_list_id'] = 0
        dic_result['result']['state_select_list_id'] = 0
        dic_result['result']['speed_duplex_list_id'] = 0
        dic_result['result']['flow_control_select_list'] = 0
        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_vlan_setting_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username,
            Hosts.http_password).filter(Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/vlansettings.cgi?vlanfilter=%s&vlanfilter_submit=Apply" % (
            dic_result['result']['vlan_ingress_filter_id'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()

        url = "http://" + config_profile_id[0][1] + "/vlansettings.cgi?vlanpas=%s&vlanpass_submit=Apply" % (
            dic_result['result']['vlan_pass_all_id'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()

        url = "http://" + config_profile_id[0][
            1] + "/vlansettings.cgi?port=%s&vlan_pvid=%s&state=%s&vlanmode_submit=Apply" \
              % (dic_result['result']['vlan_port_id'],
                 dic_result['result']['pvid'], dic_result['result']['vlan_mode_id'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()

        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4VlanSettings) \
                .filter(and_(Swt4VlanSettings.config_profile_id == config_profile_id[0][0],
                             Swt4VlanSettings.port == dic_result['result']['vlan_port_id'])).all()
            if len(swt4_data) > 0:
                swt4_data[0].vlan_ingress_filter = dic_result[
                    'result']['vlan_ingress_filter_id']
                swt4_data[0].vlan_pass_all = dic_result[
                    'result']['vlan_pass_all_id']
                swt4_data[0].port = dic_result['result']['vlan_port_id']
                swt4_data[0].pvid = dic_result['result']['pvid']
                swt4_data[0].mode = dic_result['result']['vlan_mode_id']
        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result['result']['vlan_ingress_filter_id'] = 0
        dic_result['result']['vlan_pass_all_id'] = 0
        dic_result['result']['vlan_port_id'] = 0
        dic_result['result']['pvid'] = 0
        dic_result['result']['vlan_mode_id'] = 0
        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_bandwidth_setting_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username,
            Hosts.http_password).filter(Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/bandwidthcontrol.cgi?cpu=%s&cpu_submit=Apply" % (
            dic_result['result']['bandwidth_cpu_protect_id'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        url = "http://" + config_profile_id[0][
            1] + "/bandwidthcontrol.cgi?bw_port=%s&bw_type=%s&bw_state=%s&bw_rate=%s&bwsubmit=Apply" \
              % (dic_result['result']['bandwidth_port_select_list_id'],
                 dic_result['result']['bandwidth_type_select_list_id'], dic_result['result'][
            'bandwidth_state_select_list_id'],
                 dic_result['result']['bandwidth_rate_id'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            bandwidth_data = my.session.query(Swt4BandwidthControl) \
                .filter(and_(Swt4BandwidthControl.config_profile_id == config_profile_id[0][0],
                             Swt4BandwidthControl.port == dic_result['result']['bandwidth_port_select_list_id'])).all()
            if len(bandwidth_data) > 0:
                bandwidth_data[0].cpu_protection = dic_result[
                    'result']['bandwidth_cpu_protect_id']
                bandwidth_data[0].port = dic_result[
                    'result']['bandwidth_port_select_list_id']
                bandwidth_data[0].type = dic_result[
                    'result']['bandwidth_type_select_list_id']
                bandwidth_data[0].state = dic_result[
                    'result']['bandwidth_state_select_list_id']
                bandwidth_data[0].rate = dic_result[
                    'result']['bandwidth_rate_id']
        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result['result']['bandwidth_cpu_protect_id'] = 0
        dic_result['result']['bandwidth_port_select_list_id'] = 0
        dic_result['result']['bandwidth_type_select_list_id'] = 0
        dic_result['result']['bandwidth_state_select_list_id'] = 0
        dic_result['result']['bandwidth_rate_id'] = 0
        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_storm_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username,
            Hosts.http_password).filter(Hosts.host_id == host_id).all()
        if dic_result["result"]["storm_state_id"] == 0:
            url = "http://" + config_profile_id[0][1] + "/strom.cgi?stormtype=%s&stormstate=%s&storm_submit=+Apply+" \
                  % (dic_result["result"]["storm_type_id"],
                     dic_result["result"]["storm_state_id"])
        else:
            url = "http://" + config_profile_id[0][
                1] + "/strom.cgi?stormtype=%s&stormstate=%s&stormrate=%s&storm_submit=+Apply+" \
                  % (dic_result["result"]["storm_type_id"],
                     dic_result["result"]["storm_state_id"], dic_result["result"]["storm_rate_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            port_data = my.session.query(Swt4StormControl) \
                .filter(and_(Swt4StormControl.config_profile_id == config_profile_id[0][0],
                             Swt4StormControl.strom_type == dic_result["result"]["storm_type_id"])).all()
            if len(port_data) > 0:
                port_data[0].strom_type = dic_result['result']['storm_type_id']
                port_data[0].state = dic_result['result']['storm_state_id']
                if dic_result['result']['storm_type_id'] == 0:
                    port_data[0].rate = 0
                else:
                    port_data[0].rate = dic_result['result']['storm_rate_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        if dic_result["result"]["storm_state_id"] == 0:
            dic_result['result']['storm_type_id'] = 0
            dic_result['result']['storm_state_id'] = 0
        else:
            dic_result['result']['storm_type_id'] = 0
            dic_result['result']['storm_state_id'] = 0
            dic_result['result']['storm_rate_id'] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_storm_cancel(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4StormControl.strom_type, Swt4StormControl.state,
                                        Swt4StormControl.rate).filter(
            Swt4StormControl.config_profile_id == config_profile_id[0]).order_by(Swt4StormControl.strom_type).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_ip_cancel(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4IpSettings.mode, Swt4IpSettings.ip_address, Swt4IpSettings.subnet_mask,
                                        Swt4IpSettings.gateway).filter(
            Swt4IpSettings.config_profile_id == config_profile_id[0]).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_port_cancel(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4PortSettings.link_fault_pass_through, Swt4PortSettings.port,
                                        Swt4PortSettings.state, Swt4PortSettings.speed,
                                        Swt4PortSettings.flow_control).filter(
            Swt4PortSettings.config_profile_id == config_profile_id[0]).order_by(Swt4PortSettings.port).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_vlan_cancel(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4PortSettings.link_fault_pass_through, Swt4PortSettings.port,
                                        Swt4PortSettings.state, Swt4PortSettings.speed,
                                        Swt4PortSettings.flow_control).filter(
            Swt4PortSettings.config_profile_id == config_profile_id[0]).order_by(Swt4PortSettings.port).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_bandwidth_cancel(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4BandwidthControl.cpu_protection, Swt4BandwidthControl.port,
                                        Swt4BandwidthControl.type, Swt4BandwidthControl.state,
                                        Swt4BandwidthControl.rate).filter(
            Swt4BandwidthControl.config_profile_id == config_profile_id[0]).order_by(Swt4BandwidthControl.port).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_port_priority_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/portbased.cgi?portid=%s&portbaseprio=%s&portprio_submit=Apply" \
              % (dic_result["result"]["port_id"], dic_result["result"]["priority_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4PortBasedPriority) \
                .filter(and_(Swt4PortBasedPriority.config_profile_id == config_profile_id[0][0],
                             Swt4PortBasedPriority.port == dic_result["result"]["port_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].port = dic_result['result']['port_id']
                swt4_data[0].priority = dic_result['result']['priority_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["port_id"] = 0
        dic_result['result']["priority_id"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_port_priority_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4PortBasedPriority.port, Swt4PortBasedPriority.priority).filter(
            Swt4PortBasedPriority.config_profile_id == config_profile_id[0]).order_by(
            Swt4PortBasedPriority.port).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_dscp_priority_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/dscpbased.cgi?dscp=%s&dscp_prio=%s&dscpprio_submit=Apply" \
              % (dic_result["result"]["dscp_id"], dic_result["result"]["dscp_priority_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4DscpBasedPriority) \
                .filter(and_(Swt4DscpBasedPriority.config_profile_id == config_profile_id[0][0],
                             Swt4DscpBasedPriority.dscp == dic_result["result"]["dscp_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].dscp = dic_result['result']['dscp_id']
                swt4_data[0].priority = dic_result[
                    'result']['dscp_priority_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["dscp_id"] = 0
        dic_result['result']["dscp_priority_id"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_dscp_priority_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4DscpBasedPriority.dscp, Swt4DscpBasedPriority.priority).filter(
            Swt4DscpBasedPriority.config_profile_id == config_profile_id[0]).order_by(
            Swt4DscpBasedPriority.dscp).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_802_priority_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/dot1pbased.cgi?dot1xdscp=%s&dot1pPri=%s&dot1p_submit=Apply" \
              % (dic_result["result"]["802p_id"], dic_result["result"]["802p_priority_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt48021pBasedPriority) \
                .filter(and_(Swt48021pBasedPriority.config_profile_id == config_profile_id[0][0],
                             Swt48021pBasedPriority.p802 == dic_result["result"]["802p_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].p802 = dic_result['result']['802p_id']
                swt4_data[0].priority = dic_result[
                    'result']['802p_priority_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["802p_id"] = 0
        dic_result['result']["802p_priority_id"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_801_priority_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt48021pBasedPriority.p802, Swt48021pBasedPriority.priority).filter(
            Swt48021pBasedPriority.config_profile_id == config_profile_id[0]).order_by(
            Swt48021pBasedPriority.p802).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_ip_priority_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username,
            Hosts.http_password).filter(Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + \
              "/ipbased.cgi?ipbse=%s&ipbse_submit=Apply" % (
                  dic_result['result']['ip_priority'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        url = "http://" + config_profile_id[0][
            1] + "/ipbased.cgi?iptype=%s&Ip_ipaddr=%s&Ip_msk=%s&ipbaseprio=%s&ipbased_submit=Apply" \
              % (dic_result['result']['ip_type_id'],
                 dic_result['result']['ip_priority_address'], dic_result[
            'result']['ip_priority_net_mask'],
                 dic_result['result']['ip_priority_id'])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4IpBasePriority) \
                .filter(and_(Swt4IpBasePriority.config_profile_id == config_profile_id[0][0],
                             Swt4IpBasePriority.ip_type == dic_result['result']['ip_type_id'])).all()
            if len(swt4_data) > 0:
                swt4_data[0].ip_base_priority = dic_result[
                    'result']['ip_priority']
                swt4_data[0].ip_type = dic_result['result']['ip_type_id']
                swt4_data[0].ip_address = dic_result[
                    'result']['ip_priority_address']
                swt4_data[0].network_mask = dic_result[
                    'result']['ip_priority_net_mask']
                swt4_data[0].priority = dic_result['result']['ip_priority_id']
        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result['result']['ip_priority'] = 0
        dic_result['result']['ip_type_id'] = 0
        dic_result['result']['ip_priority_address'] = 0
        dic_result['result']['ip_priority_net_mask'] = 0
        dic_result['result']['ip_priority_id'] = 0
        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_ip_priority_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(
            Swt4IpBasePriority.ip_base_priority, Swt4IpBasePriority.ip_type, Swt4IpBasePriority.ip_address,
            Swt4IpBasePriority.network_mask, Swt4IpBasePriority.priority).filter(
            Swt4IpBasePriority.config_profile_id == config_profile_id[0]).order_by(
            Swt4IpBasePriority.ip_base_priority).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = str(table_result[i])
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_queue_priority_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/qidbased.cgi?qidmap=%s&qidPrio=%s&qid_submit=Apply" \
              % (dic_result["result"]["qid_map_id"], dic_result["result"]["qid_map_priority_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4QueueBasedPriority) \
                .filter(and_(Swt4QueueBasedPriority.config_profile_id == config_profile_id[0][0],
                             Swt4QueueBasedPriority.qid_map == dic_result["result"]["qid_map_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].qid_map = dic_result['result']['qid_map_id']
                swt4_data[0].priority = dic_result[
                    'result']['qid_map_priority_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["qid_map_id"] = 0
        dic_result['result']["qid_map_priority_id"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_queue_priority_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4QueueBasedPriority.qid_map, Swt4QueueBasedPriority.priority).filter(
            Swt4QueueBasedPriority.config_profile_id == config_profile_id[0]).order_by(
            Swt4QueueBasedPriority.qid_map).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_queue_weight_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/q-weightbased.cgi?queval=%s&qweight=%s&qweight_submit=Apply" \
              % (dic_result["result"]["queue_id"], dic_result["result"]["qid_weight_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4QueueWeightBased) \
                .filter(and_(Swt4QueueWeightBased.config_profile_id == config_profile_id[0][0],
                             Swt4QueueWeightBased.queue == dic_result["result"]["queue_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].queue = dic_result['result']['queue_id']
                swt4_data[0].weight = dic_result['result']['qid_weight_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["queue_id"] = 0
        dic_result['result']["qid_weight_id"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_queue_weight_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4QueueWeightBased.queue, Swt4QueueWeightBased.weight).filter(
            Swt4QueueWeightBased.config_profile_id == config_profile_id[0]) \
            .order_by(Swt4QueueWeightBased.queue).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_qos_abstraction_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/priority_based.cgi?priotype=%s&prioPri=%s&priobased_submit=Apply" \
              % (dic_result["result"]["qos_priority_id"], dic_result["result"]["qos_level_id"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt4QosArbitration) \
                .filter(and_(Swt4QosArbitration.config_profile_id == config_profile_id[0][0],
                             Swt4QosArbitration.priority == dic_result["result"]["qos_priority_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].priority = dic_result['result']['qos_priority_id']
                swt4_data[0].level = dic_result['result']['qos_level_id']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["qos_priority_id"] = 0
        dic_result['result']["qos_level_id"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_qos_abstraction_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt4QosArbitration.priority, Swt4QosArbitration.level).filter(
            Swt4QosArbitration.config_profile_id == config_profile_id[0]).order_by(Swt4QosArbitration.priority).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


def swt4_1p_remarking_controller(host_id, device_type_id, dic_result):
    """

    @param host_id:
    @param device_type_id:
    @param dic_result:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + "/remarking.cgi?remarking=%s&remark_prio=%s&remarking_submit=Apply" \
              % (dic_result["result"]["1p_remarking_id"], dic_result["result"]["1p_remarking_priority"])
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        if len(config_profile_id) > 0:
            swt4_data = my.session.query(Swt41pRemarking) \
                .filter(and_(Swt41pRemarking.config_profile_id == config_profile_id[0][0],
                             Swt41pRemarking.p_remarking == dic_result["result"]["1p_remarking_id"])).all()
            if len(swt4_data) > 0:
                swt4_data[0].p_remarking = dic_result[
                    'result']['1p_remarking_id']
                swt4_data[0].p802_remarking = dic_result[
                    'result']['1p_remarking_priority']

        my.session.commit()
        my.sql_alchemy_db_connection_close()
        dic_result["result"]["1p_remarking_id"] = 0
        dic_result['result']["1p_remarking_priority"] = 0

        return dic_result
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def swt4_1p_remarking_cancel(host_id, device_type, dic_result):
    """

    @param host_id:
    @param device_type:
    @param dic_result:
    @return:
    """
    try:
        flag = 0
        global my
        my.sql_alchemy_db_connection_open()
        success_result = {}
        config_profile_id = my.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
        table_result = my.session.query(Swt41pRemarking.p_remarking, Swt41pRemarking.p802_remarking).filter(
            Swt41pRemarking.config_profile_id == config_profile_id[0]).order_by(Swt41pRemarking.p_remarking).first()
        print len(table_result)
        if dic_result["success"] == 0:
            print len(dic_result['result'])
            print dic['result'][0][1]
            for i in range(0, len(dic_result['result'])):
                dic_result['result'][i][1] = table_result[i]
            my.sql_alchemy_db_connection_close()
            return dic_result
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        return dic_result


dic = {'result': [['swt_ip_mode_selection', 'static'], ['swt4_ip_address', '172.22.0.106.'], [
    'swt4_subnet_mask', '172.22.0.1'], ['swt4_gateway', '255.255.255.0']], 'success': 0}


def commit_to_flash(host_id):
    """

    @param host_id:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + \
              "/configuration.cgi?config_submit=++Config+Save++"
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}
    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def reboot_final_controller(host_id, firmware):
    """

    @param host_id:
    @param firmware:
    @return:
    """
    global my
    global error_dic
    my.sql_alchemy_db_connection_open()
    try:
        config_profile_id = my.session.query(
            Hosts.config_profile_id, Hosts.ip_address, Hosts.http_username, Hosts.http_password).filter(
            Hosts.host_id == host_id).all()
        url = "http://" + config_profile_id[0][1] + \
              "/reboot.cgi?Firmware_display=%s&reboot_submit=+++Reboot++" % (
                  firmware)
        req = urllib2.Request(url)
        auth_string = base64.encodestring(
            "%s:%s" % (config_profile_id[0][2], config_profile_id[0][3]))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        return {'success': 0, 'result': 'Your device is Going to Reboot.Please Wait For Two minutes'}
    except urllib2.HTTPError, e:
        my.sql_alchemy_db_connection_close()
        if e.code in error_dic:
            return {'success': 1, 'result': error_dic[e.code]}

    except Exception as e:
        my.sql_alchemy_db_connection_close()
        return {'success': 1, 'result': str(e[-1])}
    finally:
        my.sql_alchemy_db_connection_close()


def create_default_configprofile_for_swt4(host_id, device_type_id, table_prefix, insert_update):
    """

    @param host_id:
    @param device_type_id:
    @param table_prefix:
    @param insert_update:
    @return:
    """
    global my
    my.sql_alchemy_db_connection_open()
    config_profile_id = ""
    config_profile_id = uuid.uuid1()
    my.db.execute("Insert into config_profiles(config_profile_id,device_type_id,profile_name,config_profile_type_id,parent_id)\
                            values('%s','%s','%s','%s','%s')" % (
    config_profile_id, device_type_id, None, 'Master', None))
    my.session.commit()
    default_config_profile_id = my.session.query(Odu16ConfigProfiles.config_profile_id).filter(
        and_(Odu16ConfigProfiles.device_type_id == device_type_id,
             Odu16ConfigProfiles.config_profile_type_id == "Default")).all()
    ## Get Ip Details
    bandwidth_data = my.session.query(Swt4BandwidthControl.cpu_protection, Swt4BandwidthControl.port,
                                      Swt4BandwidthControl.type, Swt4BandwidthControl.state,
                                      Swt4BandwidthControl.rate).filter(
        Swt4BandwidthControl.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(bandwidth_data)):
        bandwidth_add_row = Swt4BandwidthControl(
            config_profile_id, bandwidth_data[i][0], bandwidth_data[i][1], bandwidth_data[i][2], bandwidth_data[i][3],
            bandwidth_data[i][4])
        my.session.add(bandwidth_add_row)

    storm_data = my.session.query(Swt4StormControl.strom_type, Swt4StormControl.state, Swt4StormControl.rate).filter(
        Swt4StormControl.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(storm_data)):
        storm_add_row = Swt4StormControl(config_profile_id, storm_data[i][0],
                                         storm_data[i][1], storm_data[i][2])
        my.session.add(storm_add_row)

    port_stats = my.session.query(Swt4PortStatistics.port, Swt4PortStatistics.state, Swt4PortStatistics.speed,
                                  Swt4PortStatistics.flow_control).filter(
        Swt4PortStatistics.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(port_stats)):
        port_stats_add = Swt4PortStatistics(
            config_profile_id, port_stats[i][0], port_stats[i][1],
            port_stats[i][2], port_stats[i][3])
        my.session.add(port_stats_add)

    port_setting = my.session.query(Swt4PortSettings.link_fault_pass_through, Swt4PortSettings.port,
                                    Swt4PortSettings.state, Swt4PortSettings.speed,
                                    Swt4PortSettings.flow_control).filter(
        Swt4PortSettings.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(port_setting)):
        port_settings_add = Swt4PortSettings(
            config_profile_id, port_setting[i][
                0], port_setting[i][1], port_setting[i][2],
            port_setting[i][3], port_setting[i][4])
        my.session.add(port_settings_add)

    ip_details = my.session.query(Swt4IpSettings.mode, Swt4IpSettings.ip_address, Swt4IpSettings.subnet_mask,
                                  Swt4IpSettings.gateway).filter(
        Swt4IpSettings.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(ip_details)):
        ip_add_row = Swt4IpSettings(config_profile_id, ip_details[i][0],
                                    ip_details[i][1], ip_details[i][2], ip_details[i][3])
        my.session.add(ip_add_row)

    vlan_settings = my.session.query(Swt4VlanSettings.vlan_ingress_filter, Swt4VlanSettings.vlan_pass_all,
                                     Swt4VlanSettings.port, Swt4VlanSettings.pvid, Swt4VlanSettings.mode).filter(
        Swt4VlanSettings.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(vlan_settings)):
        vlan_add_row = Swt4VlanSettings(
            config_profile_id, vlan_settings[i][
                0], vlan_settings[i][1], vlan_settings[i][2],
            vlan_settings[i][3], vlan_settings[i][4])
        my.session.add(vlan_add_row)

    port_prty = my.session.query(Swt4PortBasedPriority.port, Swt4PortBasedPriority.priority).filter(
        Swt4PortBasedPriority.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(port_prty)):
        port_prty_add = Swt4PortBasedPriority(
            config_profile_id, port_prty[i][0], port_prty[i][1])
        my.session.add(port_prty_add)

    dscp_based = my.session.query(Swt4DscpBasedPriority.dscp, Swt4DscpBasedPriority.priority).filter(
        Swt4DscpBasedPriority.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(dscp_based)):
        dscp_based_add = Swt4DscpBasedPriority(
            config_profile_id, dscp_based[i][0], dscp_based[i][1])
        my.session.add(dscp_based_add)

    swt802_data = my.session.query(Swt48021pBasedPriority.p802, Swt48021pBasedPriority.priority).filter(
        Swt48021pBasedPriority.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(swt802_data)):
        swt802_data_add = Swt48021pBasedPriority(
            config_profile_id, swt802_data[i][0], swt802_data[i][1])
        my.session.add(swt802_data_add)

    ip_prty = my.session.query(Swt4IpBasePriority.ip_base_priority, Swt4IpBasePriority.ip_type,
                               Swt4IpBasePriority.ip_address, Swt4IpBasePriority.network_mask,
                               Swt4IpBasePriority.priority).filter(
        Swt4IpBasePriority.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(ip_prty)):
        ip_prty_add = Swt4IpBasePriority(config_profile_id, ip_prty[i][0], ip_prty[i]
        [1], ip_prty[i][2], ip_prty[i][3], ip_prty[i][4])
        my.session.add(ip_prty_add)

    queue_base_prty = my.session.query(Swt4QueueBasedPriority.qid_map, Swt4QueueBasedPriority.priority).filter(
        Swt4QueueBasedPriority.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(queue_base_prty)):
        queue_base_prty_add = Swt4QueueBasedPriority(
            config_profile_id, queue_base_prty[i][0], queue_base_prty[i][1])
        my.session.add(queue_base_prty_add)

    queue_weight = my.session.query(Swt4QueueWeightBased.queue, Swt4QueueWeightBased.weight).filter(
        Swt4QueueWeightBased.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(queue_weight)):
        queue_weight_add = Swt4QueueWeightBased(
            config_profile_id, queue_weight[i][0], queue_weight[i][1])
        my.session.add(queue_weight_add)

    qos_prty = my.session.query(Swt4QosArbitration.priority, Swt4QosArbitration.level).filter(
        Swt4QosArbitration.config_profile_id == default_config_profile_id[0][0]).all()
    for i in range(0, len(qos_prty)):
        qos_prty_add = Swt4QosArbitration(
            config_profile_id, qos_prty[i][0], qos_prty[i][1])
        my.session.add(qos_prty_add)

    ##    swt4_1p_remark = my.session.query(Swt41pRemarking.p_remarking,Swt41pRemarking.p802_remarking).filter(Swt41pRemarking.config_profile_id == default_config_profile_id[0][0]).all()
    ##    for i in range(0,len(swt4_1p_remark)):
    ##        swt4_1p_remark_add = (config_profile_id,swt4_1p_remark[i][0],swt4_1p_remark[i][1])
    ##        my.session.add(swt4_1p_remark_add)
    ##
    my.session.commit()
    my.sql_alchemy_db_connection_close()
    return config_profile_id


# print create_default_configprofile_for_swt4('f60538bc-
# 0ed7-11e1-aea8-e069956899a4','swt4','swt4_',False)
