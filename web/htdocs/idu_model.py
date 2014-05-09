#!/usr/bin/python2.6

####################### import the packages ###################################

import uuid
from nms_config import open_database_sqlalchemy_connection
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base


###############################################################################

#-------------------------Author and file Information--------------------------

###############################################################################
"""
Idu Model : This is used for making classes  of tables of databse of idu device

Author : Anuj Samariya

(CodeScape Consultants Pvt. Ltd.)

"""

###############################################################################
##                                                                           ##
##                     Author- Anuj Samariya                                 ##
##                                                                           ##
##                         IDU Model                                         ##
##                                                                           ##
##                 CodeScape Consultants Pvt. Ltd.                           ##
##                                                                           ##
##                     Dated:27 August 2011                                  ##
##                                                                           ##
###############################################################################

###############################################################################


# Create A Database Connection
db = open_database_sqlalchemy_connection()
db.echo = False
metadata = MetaData(db)

# metadata object used for binding
Base = declarative_base()
idu_result = {}

# device_type Table


class DeviceType(Base):
    """

    @param device_type_id:
    @param device_name:
    @param sdm_discovery_id:
    @param sdm_discovery_value:
    @param vnl_discovery_value:
    @param ping_discovery_value:
    @param snmp_discovery_value:
    @param upnp_discovery_value:
    @param mib_name:
    @param mib_path:
    @param is_generic:
    @param is_deleted:
    @param sequence:
    """
    __tablename__ = 'device_type'
    device_type_id = Column(VARCHAR(16), primary_key=True)
    device_name = Column(VARCHAR(64))
    sdm_discovery_id = Column(VARCHAR(8))
    sdm_discovery_value = Column(VARCHAR(16))
    vnl_discovery_value = Column(VARCHAR(16))
    ping_discovery_value = Column(VARCHAR(16))
    snmp_discovery_value = Column(VARCHAR(16))
    upnp_discovery_value = Column(VARCHAR(16))
    mib_name = Column(VARCHAR(16))
    mib_path = Column(VARCHAR(128))
    is_generic = Column(SMALLINT)
    is_deleted = Column(SMALLINT)
    sequence = Column(SMALLINT)

    def __init__(self, device_type_id, device_name, sdm_discovery_id, sdm_discovery_value, vnl_discovery_value,
                 ping_discovery_value, snmp_discovery_value, upnp_discovery_value, mib_name, mib_path, is_generic,
                 is_deleted, sequence):
        self.device_type_id = device_type_id
        self.device_name = device_name
        self.sdm_discovery_id = sdm_discovery_id
        self.sdm_discovery_value = sdm_discovery_value
        self.vnl_discovery_value = vnl_discovery_value
        self.ping_discovery_value = ping_discovery_value
        self.snmp_discovery_value = snmp_discovery_value
        self.upnp_discovery_value = upnp_discovery_value
        self.mib_name = mib_name
        self.mib_path = mib_path
        self.is_generic = is_generic
        self.is_deleted = is_deleted
        self.sequence = sequence

    def __repr__(self):
        return "<DeviceType('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d')>" \
               % (
            self.device_type_id, self.device_name, self.sdm_discovery_id, self.sdm_discovery_value,
            self.vnl_discovery_value, self.ping_discovery_value,
            self.snmp_discovery_value, self.upnp_discovery_value, self.mib_name, self.mib_path, self.is_generic,
            self.is_deleted, sequence)

# config profile type table


class ConfigProfileType(Base):
    """

    @param config_profile_type_id:
    @param config_profile_type:
    """
    __tablename__ = 'config_profile_type'
    config_profile_type_id = Column(VARCHAR(16), primary_key=True)
    config_profile_type = Column(VARCHAR(64))

    def __init__(self, config_profile_type_id, config_profile_type):
        self.config_profile_type_id = config_profile_type_id
        self.config_profile_type = config_profile_type

    def __repr__(self):
        return "<ConfigProfileType('%s','%s')>" % (self.config_profile_type_id, self.config_profile_type)

# odu16_config_profiles Table


class Idu4ConfigProfiles(Base):
    """

    @param device_type_id:
    @param config_profile_type_id:
    @param profile_name:
    @param parent_id:
    """
    __tablename__ = 'config_profiles'
    config_profile_id = Column(VARCHAR(64), primary_key=True)
    device_type_id = Column(
        VARCHAR(16), ForeignKey('device_type.device_type_id'))
    profile_name = Column(VARCHAR(64))
    config_profile_type_id = Column(VARCHAR(
        16), ForeignKey('config_profile_type.config_profile_type_id'))
    parent_id = Column(VARCHAR(64))

    config_profile_type = relationship(ConfigProfileType, backref=backref(
        'odu16_config_profiles', order_by=config_profile_type_id))
    device_type = relationship(DeviceType, backref=backref(
        'odu16_config_profiles', order_by=device_type_id))

    def __init__(self, device_type_id, config_profile_type_id, profile_name, parent_id):
        self.config_profile_id = uuid.uuid1()
        self.device_type_id = device_type_id
        self.config_profile_type_id = config_profile_type_id
        self.profile_name = profile_name
        self.parent_id = parent_id

    def __repr__(self):
        return "<ODU16ConfigProfiles('%s','%s','%s','%s','%s')>" % (
        self.config_profile_id, self.device_type_id, self.profile_name, self.config_profile_type_id, self.parent_id)


# hosts Table
class Hosts(Base):
    """

    @param host_name:
    @param host_alias:
    @param ip_address:
    @param mac_address:
    @param device_type_id:
    @param netmask:
    @param gateway:
    @param primary_dns:
    @param secondary_dns:
    @param config_profile_id:
    @param created_by:
    @param creation_time:
    @param is_deleted:
    @param updated_by:
    @param ne_id:
    @param site_id:
    @param host_state_id:
    @param priority_id:
    @param host_vendor_id:
    @param host_os_id:
    @param host_asset_id:
    @param http_username:
    @param http_password:
    @param http_port:
    @param snmp_trap_port:
    @param snmp_read_community:
    @param snmp_write_community:
    @param snmp_port:
    @param snmp_version_id:
    @param comment:
    @param icon_name:
    @param software_update_time:
    @param nms_id:
    """
    __tablename__ = 'hosts'
    host_id = Column(VARCHAR(64), primary_key=True)
    host_name = Column(VARCHAR(64))
    host_alias = Column(VARCHAR(64))
    ip_address = Column(VARCHAR(32))
    mac_address = Column(VARCHAR(32))
    device_type_id = Column(
        VARCHAR(16), ForeignKey('device_type.device_type_id'))
    netmask = Column(VARCHAR(32))
    gateway = Column(VARCHAR(32))
    primary_dns = Column(VARCHAR(32))
    secondary_dns = Column(VARCHAR(32))
    config_profile_id = Column(VARCHAR(64))
    timestamp = Column(TIMESTAMP)
    created_by = Column(VARCHAR(64))
    creation_time = Column(TIMESTAMP)
    is_deleted = Column(SMALLINT)
    updated_by = Column(VARCHAR(64))
    ne_id = Column(INTEGER)
    site_id = Column(VARCHAR(64))
    host_state_id = Column(VARCHAR(16))
    priority_id = Column(VARCHAR(16))
    host_vendor_id = Column(VARCHAR(64))
    host_os_id = Column(VARCHAR(16))
    host_asset_id = Column(VARCHAR(64))
    http_username = Column(VARCHAR(64))
    http_password = Column(VARCHAR(64))
    http_port = Column(VARCHAR(8))
    snmp_port = Column(VARCHAR(8))
    snmp_trap_port = Column(VARCHAR(8))
    snmp_read_community = Column(VARCHAR(32))
    snmp_write_community = Column(VARCHAR(32))
    snmp_version_id = Column(VARCHAR(8))
    comment = Column(VARCHAR(256))
    icon_name = Column(VARCHAR(64))
    software_update_time = Column(TIMESTAMP)
    nms_id = Column(VARCHAR(64))
    # relationship
    host = relationship(
        DeviceType, backref=backref('hosts'), order_by=device_type_id)

    def __init__(
            self, host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns,
            secondary_dns, config_profile_id, created_by, creation_time, is_deleted, updated_by, ne_id, site_id,
            host_state_id, priority_id, host_vendor_id, host_os_id, host_asset_id, http_username, http_password,
            http_port,
            snmp_trap_port, snmp_read_community, snmp_write_community, snmp_port, snmp_version_id, comment, icon_name,
            software_update_time, nms_id):
        self.host_id = uuid.uuid1()
        self.host_name = host_name
        self.host_alias = host_alias
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.device_type_id = device_type_id
        self.netmask = netmask
        self.gateway = gateway
        self.primary_dns = primary_dns
        self.secondary_dns = secondary_dns
        self.config_profile_id = config_profile_id
        self.created_by = created_by
        self.creation_time = creation_time
        self.is_deleted = is_deleted
        self.updated_by = updated_by
        self.ne_id = ne_id
        self.site_id = site_id
        self.host_state_id = host_state_id
        self.priority_id = priority_id
        self.host_vendor_id = host_vendor_id
        self.host_os_id = host_os_id
        self.host_asset_id = host_asset_id
        self.http_username = http_username
        self.http_password = http_password
        self.http_port = http_port
        self.snmp_trap_port = snmp_trap_port
        self.snmp_read_community = snmp_trap_port
        self.snmp_write_community = snmp_write_community
        self.snmp_port = snmp_port
        self.snmp_version_id = snmp_version_id
        self.comment = comment
        self.icon_name = icon_name
        self.software_update_time = software_update_time
        self.nms_id = uuid.uuid1()

    def __repr__(self):
        return "<Hosts('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" \
               % (
            self.host_id, self.host_name, self.host_alias, self.ip_address, self.mac_address, self.device_type_id,
            self.netmask,
            self.gateway, self.primary_dns, self.secondary_dns, self.config_profile_id,
            self.timestamp, self.created_by, self.creation_time, self.is_deleted, self.updated_by,
            self.ne_id, self.site_id, self.host_state_id, self.priority_id, self.host_vendor_id, self.host_os_id,
            self.host_asset_id, self.http_username, self.http_password, self.http_port, self.snmp_trap_port,
            self.snmp_read_community,
            self.snmp_write_community, self.snmp_port, self.snmp_version_id, self.comment, self.icon_name,
            self.software_update_time, self.nms_id)

# idu_acl_port_table details


class IduAclPortTable:
    """

    @param config_profile_id:
    @param acl_port_num:
    @param acl_index:
    @param acl_mac_address:
    """
    __tablename__ = "idu_acl_port_table"
    idu_acl_port_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    acl_port_num = Column(INT)
    acl_index = Column(INT)
    acl_mac_address = Column(VARCHAR(32))
    port_row_status = Column(INT)

    def __init__(self, config_profile_id, acl_port_num, acl_index, acl_mac_address):
        idu_acl_port_table_id = uuid.uuid1()
        config_profile_id = self.config_profile_id
        acl_port_num = self.acl_port_num
        acl_index = self.acl_index
        acl_mac_address = self.acl_mac_address
        port_row_status = self.port_row_status

    def __repr__(self):
        return "<IduAclPortTable('%s','%s',%d,%d,'%s',%d)>" \
               % (
        self.idu_acl_port_table_id, self.config_profile_id, self.acl_port_num, self.acl_index, self.acl_mac_address,
        self.port_row_status)

# idu_alarm_out_config_table


class IduAlarmoutConfigTable:
    """

    @param config_profile_id:
    @param alarm_out_pin:
    @param alarm_pin_state:
    """
    __tablename__ = "idu_alarm_out_config_table"
    idu_alarm_out_config_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    alarm_out_pin = Column(INT)
    alarm_pin_state = Column(INT)

    def __init__(self, config_profile_id, alarm_out_pin, alarm_pin_state):
        idu_alarm_out_config_table_id = uuid.uuid1()
        config_profile_id = self.config_profile_id
        alarm_out_pin = self.alarm_out_pin
        alarm_pin_state = self.alarm_pin_state

    def __repr__(self):
        return "<IduAlarmoutConfigTable('%s','%s',%d,%d)>" \
               % (self.idu_alarm_out_config_table_id, self.config_profile_id, self.alarm_out_pin, self.alarm_pin_state)


# idu_alarm_port_configuration_table
class IduAlarmPortConfiguration:
    """

    @param config_profile_id:
    @param alarm_pin:
    @param alarm_admin_status:
    @param alarm_string:
    @param alarm_level:
    """
    __tablename__ = "idu_alarm_port_configuration_table"
    idu_alarm_port_configuration_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    alarm_pin = Column(INT)
    alarm_admin_status = Column(INT)
    alarm_string = Column(VARCHAR(256))
    alarm_level = Column(INT)

    def __init__(self, config_profile_id, alarm_pin, alarm_admin_status, alarm_string, alarm_level):
        idu_alarm_port_configuration_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.alarm_pin = alarm_pin
        self.alarm_admin_status = alarm_admin_status
        self.alarm_string = alarm_string
        self.alarm_level = alarm_level

    def __repr__(self):
        return "<IduAlarmPortConfiguration('%s','%s',%d,%d,'%s',%d)>" \
               % (
            self.idu_alarm_port_configuration_table_id, self.config_profile_id, self.alarm_pin, self.alarm_admin_status,
            self.alarm_string,
            self.alarm_level)

# idu_atu_config_table


class IduAtuConfig:
    """

    @param idu_atu_config_table_id:
    @param config_profile_id:
    @param atu_id:
    @param atu_state:
    @param entry_type:
    @param priority:
    @param mac_address:
    @param atu_memeber_ports:
    """
    __tablename__ = "idu_atu_config_table"
    idu_atu_config_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    atu_id = Column(INT)
    atu_state = Column(INT)
    entry_type = Column(INT)
    priority = Column(INT)
    mac_address = Column(VARCHAR(32))
    atu_memeber_ports = Column(INT)

    def __init__(self, idu_atu_config_table_id, config_profile_id, atu_id, atu_state, entry_type, priority, mac_address,
                 atu_memeber_ports):
        self.config_profile_id = config_profile_id
        self.atu_id = atu_id
        self.atu_state = atu_state
        self.entry_type = entry_type
        self.priority = priority
        self.mac_address = mac_address
        self.atu_memeber_ports = atu_memeber_ports

    def __repr__(self):
        return "<IduAtuConfig('%s','%s',%d,%d,%d,%d,'%s',%d)>" \
               % (self.idu_atu_config_table_id, self.config_profile_id, self.atu_id, self.atu_state, self.entry_type,
                  self.priority, self.mac_address, self.atu_memeber_ports)

# idu_e1_port_configuration_table


class IduE1PortConfiguration:
    """

    @param config_profile_id:
    @param port_number:
    @param admin_state:
    @param clock_source:
    @param line_type:
    @param line_code:
    """
    __tablename__ = "idu_e1_port_configuration_table"
    idu_e1_port_configuration_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    port_number = Column(INT)
    admin_state = Column(INT)
    clock_source = Column(INT)
    line_type = Column(INT)
    line_code = Column(INT)

    def __init__(self, config_profile_id, port_number, admin_state, clock_source, line_type, line_code):
        self.idu_e1_port_configuration_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.port_number = port_number
        self.admin_state = admin_state
        self.clock_source = clock_source
        self.line_type = line_type
        self.line_code = line_code

    def __repr__(self):
        return "<IduE1PortConfiguration('%s','%s',%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_e1_port_configuration_table_id, self.config_profile_id, self.port_number, self.admin_state,
            self.clock_source,
            self.line_type, self.line_code)

# idu_e1_port_status_table


class IduE1PortStatus:
    """

    @param host_id:
    @param port_num:
    @param op_status:
    @param los:
    @param ais:
    @param rai:
    @param rx_frame_slip:
    @param tx_frame_slip:
    @param adpt_clk_state:
    @param bpv:
    @param adpt_clk_state:
    @param hold_over_status:
    """
    __tablename__ = "idu_e1_port_status_table"
    idu_e1_port_status_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    port_num = Column(INT)
    op_status = Column(INT)
    los = Column(INT)
    lof = Column(INT)
    ais = Column(INT)
    rai = Column(INT)
    rx_frame_slip = Column(INT)
    tx_frame_slip = Column(INT)
    bpv = Column(INT)
    adpt_clk_state = Column(INT)
    hold_over_status = Column(INT)

    def __init__(self, host_id, port_num, op_status, los, ais, rai, rx_frame_slip, tx_frame_slip, adpt_clk_state, bpv,
                 adpt_clk_state, hold_over_status):
        self.idu_e1_port_status_table_id = uuid.uuid1()
        self.host_id = host_id
        self.port_num = port_num
        self.op_status = op_status
        self.los = los
        self.lof = lof
        self.ais = ais
        self.rai = rai
        self.rx_frame_slip = rx_frame_slip
        self.tx_frame_slip = tx_frame_slip
        self.bpv = bpv
        self.adpt_clk_state = adpt_clk_state
        self.hold_over_status = hold_over_status

    def __repr__(self):
        return "<IduE1PortStatus('%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_e1_port_status_table_id, self.host_id, self.port_num, self.op_status, self.los, self.lof, self.ais,
            self.rai, self.rx_frame_slip,
            self.tx_frame_slip, self.bpv, self.adpt_clk_state, self.hold_over_status)


# idu_idu_admin_state_table

class IduIduAdminState:
    """

    @param config_profile_id:
    @param state_id:
    @param admin_state:
    """
    __tablename__ = "idu_idu_admin_state_table"
    idu_idu_admin_state_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    state_id = Column(Int)
    admin_state = Column(SMALLINT)

    def __init__(self, config_profile_id, state_id, admin_state):
        self.idu_idu_admin_state_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.state_id = state_id
        self.admin_state = admin_state

    def __repr__(self):
        return "<IduIduAdminState('%s','%s',%d,%d)>" % (
        self.idu_idu_admin_state_table_id, self.config_profile_id, self.state_id, self.admin_state)


# idu_idu_info_table
class IduIduInfoTable:
    """

    @param host_id:
    @param info_index:
    @param hw_serial_number:
    @param hw_type:
    @param hw_config_e1:
    @param hw_config_eth:
    @param hw_config_alarm:
    @param system_interface_mac:
    @param tdmoip_interface_mac:
    @param current_temperature:
    @param sys_uptime:
    """
    __tablename__ = "idu_idu_info_table"
    idu_idu_info_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    info_index = Column(Int)
    hw_serial_number = Column(VARCHAR(32))
    hw_type = Column(SMALLINT)
    hw_config_e1 = Column(SMALLINT)
    hw_config_eth = Column(SMALLINT)
    hw_config_alarm = Column(SMALLINT)
    system_interface_mac = Column(SMALLINT)
    tdmoip_interface_mac = Column(SMALLINT)
    current_temperature = Column(Int)
    sys_uptime = Column(Int)

    def __init__(self, host_id, info_index, hw_serial_number, hw_type, hw_config_e1, hw_config_eth, hw_config_alarm,
                 system_interface_mac, tdmoip_interface_mac, current_temperature, sys_uptime):
        self.idu_idu_info_table_id = uuid.uuid1()
        self.host_id = host_id
        self.info_index = info_index
        self.hw_serial_number = hw_serial_number
        self.hw_type = hw_type
        self.hw_config_e1 = hw_config_e1
        self.hw_config_eth = hw_config_eth
        self.hw_config_alarm = hw_config_alarm
        self.system_interface_mac = system_interface_mac
        self.tdmoip_interface_mac = tdmoip_interface_mac
        self.current_temperature = current_temperature
        self.sys_uptime = sys_uptime

    def __repr__(self):
        return "<IduIduInfoTable('%s','%s',%d,'%s',%d,%d,%d,%d,'%s','%s',%d,%d)>" % (self.idu_idu_info_table_id,
                                                                                     self.host_id, self.info_index,
                                                                                     self.hw_serial_number,
                                                                                     self.hw_type, self.hw_config_e1,
                                                                                     self.hw_config_eth,
                                                                                     self.hw_config_alarm,
                                                                                     self.system_interface_mac,
                                                                                     self.tdmoip_interface_mac,
                                                                                     self.current_temperature,
                                                                                     self.sys_uptime)

# idu_idu_network_statistics_table


class IduIduNetworkStatistics:
    """

    @param host_id:
    @param interface_name:
    @param rx_packets:
    @param tx_packets:
    @param rx_bytes:
    @param tx_bytes:
    @param rx_error:
    @param tx_error:
    @param rx_dropped:
    @param tx_dropped:
    @param multicasts:
    @param collisions:
    """
    __tablename__ = "IduIduNetworkStatistics"
    idu_idu_network_statistics_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    interface_name = Column(Int)
    rx_packets = Column(Int)
    tx_packets = Column(Int)
    rx_bytes = Column(Int)
    tx_bytes = Column(Int)
    rx_error = Column(Int)
    tx_error = Column(Int)
    rx_dropped = Column(Int)
    tx_dropped = Column(Int)
    multicasts = Column(Int)
    collisions = Column(Int)

    def __init__(self, host_id, interface_name, rx_packets, tx_packets, rx_bytes, tx_bytes, rx_error, tx_error,
                 rx_dropped, tx_dropped, multicasts, collisions):
        self.idu_idu_network_statistics_table_id = uuid.uuid1()
        self.host_id = host_id
        self.interface_name = interface_name
        self.self.rx_packets = rx_packets
        self.tx_packets = tx_packets
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.rx_error = rx_error
        self.tx_error = tx_error
        self.rx_dropped = rx_dropped
        self.tx_dropped = tx_dropped
        self.multicasts = multicasts
        self.collisions = collisions

    def __repr__(self):
        return "<IduIduNetworkStatistics('%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_idu_network_statistics_table_id, self.host_id, interface_name, self.rx_packets, self.tx_packets,
            self.rx_bytes, self.tx_bytes,
            self.rx_error, self.tx_error, self.rx_dropped, self.tx_dropped, self.multicasts, self.collisions)


# idu_idu_om_operations_table
class IduIduOmOperations:
    """

    @param config_profile_id:
    @param om_index:
    @param om_operation_req:
    @param user_name:
    @param password:
    @param ftp_server_address:
    @param path_name:
    @param om_operation_result:
    @param om_specific_cause:
    """
    __tablename__ = "idu_idu_om_operations_table"
    idu_idu_om_operations_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    om_index = Column(Int)
    om_operation_req = Column(Int)
    user_name = Column(VARCHAR(16))
    password = Column(VARCHAR(16))
    ftp_server_address = Column(VARCHAR(32))
    path_name = Column(VARCHAR(128))
    om_operation_result = Column(Int)
    om_specific_cause = Column(Int)

    def __init__(self, config_profile_id, om_index, om_operation_req, user_name, password, ftp_server_address,
                 path_name, om_operation_result, om_specific_cause):
        self.idu_idu_om_operations_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.om_index = config_profile_id
        self.om_operation_req = om_operation_req
        self.user_name = user_name
        self.password = password
        self.ftp_server_address = ftp_server_address
        self.path_name = path_name
        self.om_operation_result = om_operation_result
        self.om_specific_cause = om_specific_cause

    def __repr__(self):
        return "<IduIduOmOperations('%s','%s',%d,%d,'%s','%s','%s','%s',%d,%d)>" \
               % (
            self.idu_idu_om_operations_table_id, self.config_profile_id, self.om_index, self.om_operation_req,
            self.user_name,
            self.password, self.ftp_server_address, self.path_name, self.om_operation_result, self.om_specific_cause)

# idu_link_configuration_table


class IduLinkConfiguration:
    """

    @param config_profile_id:
    @param bundle_number:
    @param port_number:
    @param admin_status:
    @param src_bundle_id:
    @param dst_bundle_id:
    @param dst_ip_addr:
    @param tsa_assign:
    @param clock_recovery:
    @param bundle_size:
    @param buffer_size:
    """
    __tablename__ = idu_link_configuration_table
    idu_link_configuration_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    bundle_number = Column(Int)
    port_number = Column(Int)
    admin_status = Column(Int)
    src_bundle_id = Column(Int)
    dst_bundle_id = Column(Int)
    dst_ip_addr = Column(VARCHAR(32))
    tsa_assign = Column(VARCHAR(32))
    clock_recovery = Column(Int)
    bundle_size = Column(Int)
    buffer_size = Column(Int)

    def __init__(
            self, config_profile_id, bundle_number, port_number, admin_status, src_bundle_id, dst_bundle_id,
            dst_ip_addr, tsa_assign, clock_recovery, bundle_size,
            buffer_size):
        self.idu_link_configuration_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.bundle_number = bundle_number
        self.port_number = port_number
        self.admin_status = admin_status
        self.src_bundle_id = src_bundle_id
        self.dst_bundle_id = dst_bundle_id
        self.dst_ip_addr = dst_ip_addr
        self.tsa_assign = tsa_assign
        self.clock_recovery = clock_recovery
        self.bundle_size = bundle_size
        self.buffer_size = buffer_size

    def __repr__(self):
        return "<IduLinkConfiguration('%s','%s',%d,%d,%d,%d,%d,'%s','%s',%d,%d,%d)>" % \
               (self.idu_link_configuration_table_id, self.config_profile_id, self.bundle_number, self.port_number,
                self.admin_status, self.src_bundle_id, self.dst_bundle_id,
                self.dst_ip_addr, self.tsa_assign, self.clock_recovery, self.bundle_size, self.buffer_size)


# idu_link_statistics_table
class IduLinkStatistics:
    """

    @param host_id:
    @param bundle_number:
    @param port_number:
    @param good_frames_to_eth:
    @param good_frames_rx:
    @param lost_packets_at_rx:
    @param lost_packets_at_rx:
    @param discarded_packets:
    @param reordered_packets:
    @param underrun_events:
    """
    __tablename__ = "idu_link_statistics_table"
    idu_link_statistics_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    bundle_number = Column(Int)
    port_number = Column(Int)
    good_frames_to_eth = Column(Int)
    good_frames_rx = Column(Int)
    lost_packets_at_rx = Column(Int)
    discarded_packets = Column(Int)
    reordered_packets = Column(Int)
    underrun_events = Column(Int)

    def __init__(
            self, host_id, bundle_number, port_number, good_frames_to_eth, good_frames_rx, lost_packets_at_rx,
            lost_packets_at_rx, discarded_packets,
            reordered_packets, underrun_events):
        self.idu_link_statistics_table_id = uuid.uuid1()
        self.host_id = host_id
        self.bundle_number = bundle_number
        self.port_number = port_number
        self.good_frames_to_eth = good_frames_to_eth
        self.good_frames_rx = good_frames_rx
        self.lost_packets_at_rx = lost_packets_at_rx
        self.discarded_packets = discarded_packets
        self.reordered_packets = reordered_packets
        self.underrun_events = underrun_events

    def __return__(self):
        return "<IduLinkStatistics('%s','%s',%d,%d,%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_link_statistics_table_id, self.host_id, self.bundle_number, self.port_number,
            self.good_frames_to_eth,
            self.good_frames_rx, self.lost_packets_at_rx, self.discarded_packets, self.reordered_packets,
            self.underrun_events)

# idu_link_status_table


class IduLinkStatus:
    """

    @param host_id:
    @param bundle_num:
    @param operational_status:
    @param min_jb_level:
    @param max_jb_level:
    @param underrun_occured:
    @param overrun_occured:
    """
    __tablename__ = "idu_link_status_table"
    idu_link_status_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    bundle_num = Column(Int)
    operational_status = Column(Int)
    min_jb_level = Column(Int)
    max_jb_leveel = Column(Int)
    underrun_occured = Column(Int)
    overrun_occured = Column(Int)

    def __init__(self, host_id, bundle_num, operational_status, min_jb_level, max_jb_level, underrun_occured,
                 overrun_occured):
        self.idu_link_status_table_id = uuid.uuid1()
        self.host_id = host_id
        self.bundle_num = bundle_num
        self.operational_status = operational_status
        self.min_jb_level = min_jb_level
        self.max_jb_level = max_jb_level
        self.underrun_occured = underrun_occured
        self.overrun_occured = overrun_occured

    def __repr__(self):
        return "<IduLinkStatus('%s','%s',%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_link_status_table_id, self.host_id, self.bundle_num, self.operational_status, self.min_jb_level,
            self.max_jb_level, self.underrun_occured, self.overrun_occured)


# idu_mirroring_port_table
class IduMirroringPort:
    """

    @param config_profile_id:
    @param mirroring_index_id:
    @param mirroring_port:
    """
    __tablename__ = "idu_mirroring_port_table"
    idu_mirroring_port_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    mirroring_index_id = Column(Int)
    mirroring_port = Column(Int)

    def __init__(self, config_profile_id, mirroring_index_id, mirroring_port):
        self.idu_mirroring_port_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.mirroring_index_id = mirroring_index_id
        self.mirroring_port = mirroring_port

    def __repr__(self):
        return "<IduMirroringPort('%s','%s',%d,%d)>" \
               % (self.idu_mirroring_port_table_id, config_profile_id, mirroring_index_id, mirroring_port)

# idu_network_configurations_table


class IduNetworkConfigurations:
    """

    @param config_profile_id:
    @param interface:
    @param ip_addr:
    @param netmask:
    @param gateway:
    @param auto_ip_config:
    """
    __tablename__ = "idu_network_configurations_table"
    idu_network_configurations_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    interface = Column(Int)
    ip_addr = Column(VARCHAR(32))
    netmask = Column(VARCHAR(32))
    gateway = Column(VARCHAR(32))
    auto_ip_config = Column(Int)

    def __init__(self, config_profile_id, interface, ip_addr, netmask, gateway, auto_ip_config):
        self.idu_network_configurations_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.interface = interface
        self.ip_addr = ip_addr
        self.netmask = netmask
        self.gateway = gateway
        self.auto_ip_config = auto_ip_config

    def __repr__(self):
        return "<IduNetworkConfigurations('%s','%s',%d,'%s','%s','%s',%d)>" \
               % (
            self.idu_network_configurations_table_id, self.config_profile_id, self.interface, self.ip_addr, netmask,
            self.gateway, self.auto_ip_config)

# idu_omc_configuration_table


class IduOmcConfiguration:
    """

    @param config_profile_id:
    @param omc_index:
    @param omc_ip_address:
    @param periodic_stats_timer:
    """
    __tablename__ = idu_omc_configuration_table
    idu_omc_configuration_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    omc_index = Column(Int)
    omc_ip_address = Column(VARCHAR(32))
    periodic_stats_timer = Column(Int)

    def __init__(self, config_profile_id, omc_index, omc_ip_address, periodic_stats_timer):
        self.idu_omc_configuration_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.omc_index = omc_index
        self.omc_ip_address = omc_ip_address
        self.periodic_stats_timer = periodic_stats_timer

    def __repr__(self):
        return "<IduOmcConfiguration('%s','%s',%d,'%s',%d)>" \
               % (
            self.idu_omc_configuration_table_id, self.config_profile_id, self.omc_index, self.omc_ip_address,
            self.periodic_stats_timer)

# idu_poe_configuration_table


class IduPoeConfiguration:
    """

    @param config_profile_id:
    @param index_id:
    @param poe_admin_status:
    """
    __tablename__ = "idu_poe_configuration_table"
    idu_poe_configuration_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    index_id = Column(Int)
    poe_admin_status = Column(Int)

    def __init__(self, config_profile_id, index_id, poe_admin_status):
        self.idu_poe_configuration_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.index_id = index_id
        self.poe_admin_status = poe_admin_status

    def __repr__(self):
        return "<IduPoeConfiguration('%s','%s',%d,%d)>" \
               % (self.idu_poe_configuration_table_id, self.config_profile_id, self.index_id, self.poe_admin_status)

# idu_port_bw_table


class IduPortBW:
    """

    @param config_profile_id:
    @param switch_port_num:
    @param egress_bw_value:
    @param ingress_bw_value:
    """
    __tablename__ = "idu_port_bw_table"
    idu_port_bw_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    switch_port_num = Column(Int)
    egress_bw_value = Column(Int)
    ingress_bw_value = Column(Int)

    def __init__(self, config_profile_id, switch_port_num, egress_bw_value, ingress_bw_value):
        self.idu_port_bw_table_id = idu_port_bw_table_id
        self.config_profile_id = config_profile_id
        self.switch_port_num = switch_port_num
        self.egress_bw_value = egress_bw_value
        self.ingress_bw_value = ingress_bw_value

    def __repr(self):
        return "<IduPortBW('%s','%s',%d,%d,%d)>" \
               % (
            self.idu_port_bw_table_id, self.config_profile_id, self.switch_port_num, self.egress_bw_value,
            self.ingress_bw_value)

# idu_port_qing_table


class IduPortQing:
    """

    @param config_profile_id:
    @param switch_port_number:
    @param port_qing_state:
    @param provider_tag:
    """
    __tablename__ = "idu_port_qing_table"
    idu_port_qing_table_id = Column(VARCHAR(64))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    switch_port_number = Column(Int)
    port_qing_state = Column(Int)
    provider_tag = Column(Int)

    def __init__(self, config_profile_id, switch_port_number, port_qing_state, provider_tag):
        self.idu_port_qing_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.switch_port_number = switch_port_number
        self.port_qing_state = port_qing_state
        self.provider_tag = provider_tag

    def __repr__(self):
        return "<IduPortQing('%s','%s',%d,%d,%d)>" \
               % (
            self.idu_port_qing_table_id, self.config_profile_id, self.switch_port_number, self.port_qing_state,
            self.provider_tag)

# idu_port_secondary_statistics_table


class IduPortSecondaryStatistics:
    """

    @param host_id:
    @param switch_port_num:
    @param in_unicast:
    @param out_unicast:
    @param in_broadcast:
    @param out_broadcast:
    @param in_multicast:
    @param out_multicast:
    @param in_undersize_rx:
    @param in_fragments_rx:
    @param in_oversize_rx:
    @param in_jabber_rx:
    @param in_mac_rcv_error_rx:
    @param in_fcs_error_rx:
    @param out_fcs_error_tx:
    @param defered_tx:
    @param collision_tx:
    @param late_tx:
    @param exessive_tx:
    @param single_tx:
    @param multiple_tx:
    """
    __tablename__ = "idu_port_secondary_statistics_table"
    idu_port_secondary_statistics_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    switch_port_num = Column(Int)
    in_unicast = Column(Int)
    out_unicast = Column(Int)
    in_broadcast = Column(Int)
    out_broadcast = Column(Int)
    in_multicast = Column(Int)
    out_multicast = Column(Int)
    in_undersize_rx = Column(Int)
    in_fragments_rx = Column(Int)
    in_oversize_rx = Column(Int)
    in_jabber_rx = Column(Int)
    in_mac_rcv_error_rx = Column(Int)
    in_fcs_error_rx = Column(Int)
    out_fcs_error_tx = Column(Int)
    defered_tx = Column(Int)
    collision_tx = Column(Int)
    late_tx = Column(Int)
    exessive_tx = Column(Int)
    single_tx = Column(Int)
    multiple_tx = Column(Int)

    def __init__(
            self, host_id, switch_port_num, in_unicast, out_unicast, in_broadcast, out_broadcast, in_multicast,
            out_multicast,
            in_undersize_rx, in_fragments_rx, in_oversize_rx, in_jabber_rx, in_mac_rcv_error_rx, in_fcs_error_rx,
            out_fcs_error_tx,
            defered_tx, collision_tx, late_tx, exessive_tx, single_tx, multiple_tx):
        self.idu_port_secondary_statistics_table_id = uuid.uuid1()
        self.host_id = host_id
        self.switch_port_num = switch_port_num
        self.in_unicast = in_unicast
        self.out_unicast = out_unicast
        self.in_broadcast = in_broadcast
        self.out_broadcast = out_broadcast
        self.in_multicast = in_multicast
        self.out_multicast = out_multicast
        self.in_undersize_rx = in_undersize_rx
        self.in_fragments_rx = in_fragments_rx
        self.in_oversize_rx = in_oversize_rx
        self.in_jabber_rx = in_jabber_rx
        self.in_mac_rcv_error_rx = in_mac_rcv_error_rx
        self.in_fcs_error_rx = in_fcs_error_rx
        self.out_fcs_error_tx = out_fcs_error_tx
        self.defered_tx = defered_tx
        self.collision_tx = collision_tx
        self.late_tx = late_tx
        self.exessive_tx = exessive_tx
        self.single_tx = single_tx
        self.multiple_tx = multiple_tx

    def __repr__(self):
        return "<IduPortSecondaryStatistics('%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)>" \
               % (self.idu_port_secondary_statistics_table_id, host_id,
                  self.switch_port_num, self.in_unicast, self.out_unicast, self.in_broadcast,
                  self.out_broadcast, self.in_multicast, self.out_multicast,
                  self.in_undersize_rx, self.in_fragments_rx, self.in_oversize_rx,
                  self.in_jabber_rx, self.in_mac_rcv_error_rx,
                  self.in_fcs_error_rx, self.out_fcs_error_tx,
                  self.defered_tx, self.collision_tx, self.late_tx,
                  self.exessive_tx, self.single_tx, self.multiple_tx)

# idu_port_statistics_table


class IduPortStatistics:
    """

    @param host_id:
    @param software_stat_port_num:
    @param frame_rx:
    @param frame_tx:
    @param in_discards:
    @param in_good_octets:
    @param in_bad_octet:
    @param out_octets:
    """
    __tablename__ = "idu_port_statistics_table"
    idu_port_statistics_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    software_stat_port_num = Column(Int)
    frame_rx = Column(Int)
    frame_tx = Column(Int)
    in_discards = Column(Int)
    in_good_octets = Column(Int)
    in_bad_octet = Column(Int)
    out_octets = Column(Int)

    def __init__(self, host_id, software_stat_port_num, frame_rx, frame_tx, in_discards, in_good_octets, in_bad_octet,
                 out_octets):
        self.idu_port_statistics_table_id = uuid.uuid1()
        self.idu_port_statistics_table_id
        self.host_id = host_id
        self.software_stat_port_num = software_stat_port_num
        self.frame_rx = frame_rx
        self.frame_tx = frame_tx
        self.in_discards = in_discards
        self.in_good_octets = in_good_octets
        self.in_bad_octet = in_bad_octet
        self.out_octets = out_octets

    def __repr__(self):
        return "<IduPortStatistics('%s','%s',%d,%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_port_statistics_table_id, self.host_id, self.software_stat_port_num, self.frame_rx,
            self.frame_tx, self.in_discards, self.in_good_octets, self.in_bad_octet, self.out_octets)

# idu_port_stat_bad_frame_table


class IduPortStatBadFrame:
    """

    @param host_id:
    @param switch_bad_frame_port:
    @param in_undersize_rx:
    @param in_fragmnets_rx:
    @param in_oversize_rx:
    @param in_mac_rcv_error_rx:
    @param in_jabber_rx:
    @param in_fcs_error_rx:
    @param out_fcserr_tx:
    @param deffered_tx:
    @param collision_tx:
    @param late_tx:
    @param excessive_tx:
    @param single_tx:
    @param multiple_tx:
    """
    __tablename__ = "idu_port_stat_bad_frame_table"
    idu_port_stat_bad_frame_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    switch_bad_frame_port = Column(Int)
    in_undersize_rx = Column(Int)
    in_fragmnets_rx = Column(Int)
    in_oversize_rx = Column(Int)
    in_mac_rcv_error_rx = Column(Int)
    in_jabber_rx = Column(Int)
    in_fcs_error_rx = Column(Int)
    out_fcserr_tx = Column(Int)
    deffered_tx = Column(Int)
    collision_tx = Column(Int)
    late_tx = Column(Int)
    excessive_tx = Column(Int)
    single_tx = Column(Int)
    multiple_tx = Column(Int)

    def __init__(
            self, host_id, switch_bad_frame_port, in_undersize_rx, in_fragmnets_rx, in_oversize_rx, in_mac_rcv_error_rx,
            in_jabber_rx, in_fcs_error_rx, out_fcserr_tx, deffered_tx, collision_tx, late_tx, excessive_tx, single_tx,
            multiple_tx):
        self.idu_port_stat_bad_frame_table_id = uuid.uuid1()
        self.host_id = host_id
        self.switch_bad_frame_port = switch_bad_frame_port
        self.in_undersize_rx = in_undersize_rx
        self.in_fragmnets_rx = in_fragmnets_rx
        self.in_oversize_rx = in_oversize_rx
        self.in_mac_rcv_error_rx = in_mac_rcv_error_rx
        self.in_jabber_rx = in_jabber_rx
        self.in_fcs_error_rx = in_fcs_error_rx
        self.out_fcserr_tx = out_fcserr_tx
        self.deffered_tx = deffered_tx
        self.collision_tx = collision_tx
        self.late_tx = late_tx
        self.excessive_tx = excessive_tx
        self.single_tx = single_tx
        self.multiple_tx = multiple_tx

    def __repr__(self):
        return "<IduPortStatBadFrame('%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,)>" \
               % (
            self.idu_port_stat_bad_frame_table_id, self.host_id, self.switch_bad_frame_port, self.in_undersize_rx,
            self.in_fragmnets_rx, self.in_oversize_rx, self.in_mac_rcv_error_rx, self.in_jabber_rx,
            self.in_fcs_error_rx, self.out_fcserr_tx, self.deffered_tx, self.collision_tx,
            self.late_tx, self.excessive_tx, single_tx,
            self.multiple_tx)

# idu_port_stat_good_frame_table


class IduPortStatGoodFrame:
    """

    @param host_id:
    @param software_good_frame_port_num:
    @param in_unicast:
    @param out_unicast:
    @param in_broadcast:
    @param out_broadcast:
    @param in_multicast:
    @param out_multicast:
    """
    __tablename__ = "idu_port_stat_good_frame_table"
    idu_port_stat_good_frame_table_id = Column(VARCHAR(64))
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    software_good_frame_port_num = Column(Int)
    in_unicast = Column(Int)
    out_unicast = Column(Int)
    in_broadcast = Column(Int)
    out_broadcast = Column(Int)
    in_multicast = Column(Int)
    out_multicast = Column(Int)

    def __init__(
            self, host_id, software_good_frame_port_num, in_unicast, out_unicast, in_broadcast,
            out_broadcast, in_multicast, out_multicast):
        self.idu_port_stat_good_frame_table_id = uuid.uuid1()
        self.host_id = host_id
        self.software_good_frame_port_num = software_good_frame_port_num
        self.in_unicast = in_unicast
        self.out_unicast = out_unicast
        self.in_broadcast = in_broadcast
        self.out_broadcast = out_broadcast
        self.in_multicast = in_multicast
        self.out_multicast = out_multicast

    def __repr__(self):
        return "<IduPortStatGoodFrame('%s','%s',%d,%d,%d,%d,%d,%d,%d)>" \
               % (
            self.idu_port_stat_good_frame_table_id, self.host_id, self.software_good_frame_port_num, self.in_unicast,
            self.out_unicast, self.in_broadcast,
            out_broadcast, in_multicast, out_multicast)
