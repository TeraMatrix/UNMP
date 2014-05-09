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
Odu Model : This is used for making classes  of tables of databse of odu16 device

Author : Anuj Samariya

(CodeScape Consultants Pvt. Ltd.)

"""

###############################################################################
##                                                                           ##
##                     Author- Anuj Samariya                                 ##
##                                                                           ##
##                         ODU Model                                         ##
##                                                                           ##
##                 CodeScape Consultants Pvt. Ltd.                           ##
##                                                                           ##
##                     Dated:27 August 2011                                  ##
##                                                                           ##
###############################################################################

###############################################################################


# metadata object used for binding
Base = declarative_base()

# device_type Table
###############################  Odu16 Tables #################################


class DeviceType(Base):
    """
    device_type Table
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
    table_prefix = Column(VARCHAR(32))
    is_generic = Column(SMALLINT)
    is_deleted = Column(SMALLINT)
    sequence = Column(SMALLINT)

    def __init__(self, device_type_id, device_name, sdm_discovery_id, sdm_discovery_value, vnl_discovery_value,
                 ping_discovery_value, snmp_discovery_value, upnp_discovery_value, mib_name, mib_path, table_prefix,
                 is_generic, is_deleted, sequence):
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
        self.table_prefix = table_prefix
        self.is_generic = is_generic
        self.is_deleted = is_deleted
        self.sequence = sequence

    def __repr__(self):
        return "<DeviceType('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d')>" \
               % (
            self.device_type_id, self.device_name, self.sdm_discovery_id, self.sdm_discovery_value,
            self.vnl_discovery_value, self.ping_discovery_value,
            self.snmp_discovery_value, self.upnp_discovery_value, self.mib_name, self.mib_path, self.table_prefix,
            self.is_generic, self.is_deleted, sequence)


# config_profile_type Table
class ConfigProfileType(Base):
    """
    config_profile_type Table
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
class Odu16ConfigProfiles(Base):
    """
    odu16_config_profiles Table
    """
    __tablename__ = 'config_profiles'
    config_profile_id = Column(VARCHAR(64), primary_key=True)
    device_type_id = Column(
        VARCHAR(16), ForeignKey('device_type.device_type_id'))
    profile_name = Column(VARCHAR(64))
    config_profile_type_id = Column(VARCHAR(
        16), ForeignKey('config_profile_type.config_profile_type_id'))
    parent_id = Column(VARCHAR(64))

    # relationship
    # config_profile_type=relationship(ConfigProfileType,backref=backref('config_profiles',order_by=config_profile_type_id))
    # device_type=relationship(DeviceType,backref=backref('config_profiles',order_by=device_type_id))
    def __init__(self, config_profile_id, device_type_id, profile_name, config_profile_type_id, parent_id):
        self.config_profile_id = config_profile_id
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
    @param dns_state:
    @param config_profile_id:
    @param timestamp:
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
    @param snmp_read_community:
    @param snmp_write_community:
    @param snmp_port:
    @param snmp_trap_port:
    @param snmp_version_id:
    @param comment:
    @param nms_id:
    @param parent_name:
    @param lock_status:
    @param is_localhost:
    """
    __tablename__ = "hosts"
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
    dns_state = Column(VARCHAR(16))
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    timestamp = Column(TIMESTAMP)
    created_by = Column(VARCHAR(64))
    creation_time = Column(TIMESTAMP)
    is_deleted = Column(SMALLINT(6))
    updated_by = Column(VARCHAR(64))
    ne_id = Column(INT(64))
    site_id = Column(VARCHAR(64), ForeignKey('sites.site_id'))
    host_state_id = Column(
        VARCHAR(16), ForeignKey('host_states.host_state_id'))
    priority_id = Column(VARCHAR(16), ForeignKey('priority.priority_id'))
    host_vendor_id = Column(
        VARCHAR(64), ForeignKey('host_vendor.host_vendor_id'))
    host_os_id = Column(VARCHAR(16), ForeignKey('host_os.host_os_id'))
    host_asset_id = Column(
        VARCHAR(64), ForeignKey('host_assets.host_asset_id'))
    http_username = Column(VARCHAR(64))
    http_password = Column(VARCHAR(64))
    http_port = Column(VARCHAR(8))
    snmp_read_community = Column(VARCHAR(32))
    snmp_write_community = Column(VARCHAR(32))
    snmp_port = Column(VARCHAR(8))
    snmp_trap_port = Column(VARCHAR(8))
    snmp_version_id = Column(VARCHAR(8))
    comment = Column(VARCHAR(256))
    nms_id = Column(VARCHAR(64), ForeignKey('nms_instance.nms_id'))
    parent_name = Column(VARCHAR(64))
    lock_status = Column(CHAR(8))
    is_localhost = Column(SMALLINT(6))

    def __init__(self, host_name, host_alias, ip_address, mac_address, device_type_id, netmask, gateway, primary_dns,
                 secondary_dns, dns_state, config_profile_id, timestamp, created_by, creation_time, is_deleted,
                 updated_by, ne_id, site_id, host_state_id, priority_id, host_vendor_id, host_os_id, host_asset_id,
                 http_username, http_password, http_port, snmp_read_community, snmp_write_community, snmp_port,
                 snmp_trap_port, snmp_version_id, comment, nms_id, parent_name, lock_status, is_localhost):
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
        self.dns_state = dns_state
        self.config_profile_id = config_profile_id
        self.timestamp = timestamp
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
        self.snmp_read_community = snmp_read_community
        self.snmp_write_community = snmp_write_community
        self.snmp_port = snmp_port
        self.snmp_trap_port = snmp_trap_port
        self.snmp_version_id = snmp_version_id
        self.comment = comment
        self.nms_id = nms_id
        self.parent_name = parent_name
        self.lock_status = lock_status
        self.is_localhost = is_localhost

    def __repr__(self):
        return "<Hosts('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.host_id, self.host_name, self.host_alias, self.ip_address, self.mac_address, self.device_type_id,
        self.netmask, self.gateway, self.primary_dns, self.secondary_dns, self.dns_state, self.config_profile_id,
        self.timestamp, self.created_by, self.creation_time, self.is_deleted, self.updated_by, self.ne_id, self.site_id,
        self.host_state_id, self.priority_id, self.host_vendor_id, self.host_os_id, self.host_asset_id,
        self.http_username, self.http_password, self.http_port, self.snmp_read_community, self.snmp_write_community,
        self.snmp_port, self.snmp_trap_port, self.snmp_version_id, self.comment, self.nms_id, self.parent_name,
        self.lock_status, self.is_localhost)


class HostAssets(Base):
    """

    @param host_asset_id:
    @param longitude:
    @param latitude:
    @param serial_number:
    @param hardware_version:
    @param software_update_state:
    @param software_update_msg:
    @param software_update_time:
    """
    __tablename__ = "host_assets"
    host_asset_id = Column(VARCHAR(64), primary_key=True)
    longitude = Column(VARCHAR(32))
    latitude = Column(VARCHAR(32))
    serial_number = Column(VARCHAR(32))
    hardware_version = Column(VARCHAR(32))
    software_update_state = Column(SMALLINT(8))
    software_update_msg = Column(VARCHAR(128))
    software_update_time = Column(TIMESTAMP)

    def __init__(self, host_asset_id, longitude, latitude, serial_number, hardware_version, software_update_state,
                 software_update_msg, software_update_time):
        self.host_asset_id = uuid.uuid1()
        self.longitude = longitude
        self.latitude = latitude
        self.serial_number = serial_number
        self.hardware_version = hardware_version
        self.software_update_state = software_update_state
        self.software_update_msg = software_update_msg
        self.software_update_time = software_update_time

    def __repr__(self):
        return "<HostAssets('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.host_asset_id, self.longitude, self.latitude, self.serial_number, self.hardware_version,
        self.software_update_state, self.software_update_msg, self.software_update_time)


# set_odu16_ip_config_table Table
class SetOdu16IPConfigTable(Base):
    """
    set_odu16_ip_config_table Table
    """
    __tablename__ = 'set_odu16_ip_config_table'
    set_odu16_ip_config_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    admin_state = Column(SMALLINT)
    auto_ip_config = Column(INTEGER)

    def __init__(self, config_profile_id, admin_state, auto_ip_config):
        self.set_odu16_ip_config_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.admin_state = admin_state
        self.auto_ip_config = auto_ip_config

    def __repr__(self):
        return "SetOdu16IPConfigTable<'%s','%s','%d','%d'>" % (
        self.set_odu16_ip_config_table_id, self.config_profile_id, self.admin_state, self.auto_ip_config)

# set_odu16_network_interface_config_table Table


class SetOdu16NetworkInterfaceConfig(Base):
    """
    set_odu16_network_interface_config_table Table
    """
    __tablename__ = 'set_odu16_network_interface_config_table'
    set_odu16_network_interface_config_entry_id = Column(
        VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    ssid = Column(VARCHAR(32))
    index = Column(INTEGER)

    def __init__(self, config_profile_id, ssid, index):
        self.set_odu16_network_interface_config_entry_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.ssid = ssid
        self.index = index

    def __repr__(self):
        return "SetOdu16NetworkInterfaceConfigTable<'%s','%s','%s','%d'>" % (
        self.set_odu16_network_interface_config_entry_id, self.config_profile_id, self.ssid, self.index)


# set_odu16_omc_conf_table Table
class SetOdu16OmcConfTable(Base):
    """
    set_odu16_omc_conf_table Table
    """
    __tablename__ = 'set_odu16_omc_conf_table'
    set_odu16_omc_conf_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    omc_ip_address = Column(VARCHAR(32))
    periodic_stats_timer = Column(INTEGER)

    def __init__(self, config_profile_id, omc_ip_address, periodic_stats_timer):
        self.set_odu16_omc_conf_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.omc_ip_address = omc_ip_address
        self.periodic_stats_timer = periodic_stats_timer

    def __repr__(self):
        return "SetOdu16OmcConfTable<'%s','%s','%s','%d'>" % (
        self.set_odu16_omc_conf_table_id, self.config_profile_id, self.omc_ip_address, self.periodic_stats_timer)

# set_odu16_peer_config_table Table


class SetOdu16PeerConfigTable(Base):
    """
    set_odu16_peer_config_table Table
    """
    __tablename__ = 'set_odu16_peer_config_table'
    set_odu16_peer_config_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    peer_mac_address = Column(TEXT)
    index = Column(INTEGER)

    def __init__(self, config_profile_id, peer_mac_address, index):
        self.set_odu16_peer_config_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.peer_mac_address = peer_mac_address
        self.index = index

    def __repr__(self):
        return "SetOdu16PeerConfig<'%s','%s','%s','%d'>" % (
        self.set_odu16_peer_config_table_id, self.config_profile_id, self.peer_mac_address, self.index)

# set_odu16_ra_acl_config_table Table


class SetOdu16RAAclConfigTable(Base):
    """
    set_odu16_ra_acl_config_table Table
    """
    __tablename__ = 'set_odu16_ra_acl_config_table'
    set_odu16_ra_acl_config_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    mac_address = Column(TEXT)
    index = Column(INTEGER)

    def __init__(self, config_profile_id, mac_address, index):
        self.set_odu16_ra_acl_config_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.mac_address = mac_address
        self.index = index

    def __repr__(self):
        return "SetOdu16RAAclConfig<'%s','%s','%s','%d'>" % (
        self.set_odu16_ra_acl_config_table_id, self.config_profile_id, self.mac_address, self.index)


# set_odu16_om_operations_table Table
class SetOdu16OmOperationsTable(Base):
    """
    set_odu16_om_operations_table Table
    """
    __tablename__ = 'set_odu16_om_operations_table'
    set_odu16_om_operations_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    om_operation_req = Column(INTEGER)
    user_name = Column(VARCHAR(64))
    password = Column(VARCHAR(64))
    ftp_server_address = Column(VARCHAR(32))
    path_name = Column(VARCHAR(256))
    enable_swam = Column(INTEGER)

    def __init__(self, config_profile_id, om_operation_req, user_name, password, ftp_server_address, path_name,
                 enable_swam):
        self.set_odu16_om_operations_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.om_operation_req = om_operation_req
        self.user_name = user_name
        self.password = password
        self.ftp_server_address = ftp_server_address
        self.path_name = path_name
        self.enable_swam = enable_swam

    def __repr__(self):
        return "SetOdu16OmOperationsTable<'%s','%s','%d','%s','%s','%s','%s','%d'>" % (
        self.set_odu16_om_operations_table_id, self.config_profile_id, self.om_operation_req, self.user_name,
        self.password, self.ftp_server_address, self.path_name, self.enable_swam)


# set_odu16_ra_conf_table Table
class SetOdu16RAConfTable(Base):
    """
    set_odu16_ra_conf_table Table
    """
    __tablename__ = 'set_odu16_ra_conf_table'
    set_odu16_ra_conf_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    ra_admin_state = Column(SMALLINT)
    acl_mode = Column(SMALLINT)
    ssid = Column(VARCHAR(64))

    def __init__(self, config_profile_id, ra_admin_state, acl_mode, ssid):
        self.set_odu16_ra_conf_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.ra_admin_state = ra_admin_state
        self.acl_mode = acl_mode
        self.ssid = ssid

    def __repr__(self):
        return "SetOdu16OmOperationsTable<'%s','%s','%d','%s','%s','%s','%s','%d'>" % (
        self.set_odu16_ra_conf_table_id, self.config_profile_id, self.ra_admin_state, self.acl_mode, self.ssid)


# set_odu16_ra_llc_conf_table
class SetOdu16RALlcConfTable(Base):
    """
    set_odu16_ra_llc_conf_table
    """
    __tablename__ = 'set_odu16_ra_llc_conf_table'
    set_odu16_ra_llc_conf_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    llc_arq_enable = Column(SMALLINT)
    arq_win = Column(INTEGER)
    frame_loss_threshold = Column(INTEGER)
    leaky_bucket_timer_val = Column(INTEGER)
    frame_loss_timeout = Column(INTEGER)

    def __init__(self, config_profile_id, llc_arq_enable, arq_win, frame_loss_threshold, leaky_bucket_timer_val,
                 frame_loss_timeout):
        self.set_odu16_ra_llc_conf_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.llc_arq_enable = llc_arq_enable
        self.arq_win = arq_win
        self.frame_loss_threshold = frame_loss_threshold
        self.leaky_bucket_timer_val = leaky_bucket_timer_val
        self.frame_loss_timeout = frame_loss_timeout

    def __repr__(self):
        return "SetOdu16RALlcConfTable<'%s','%s','%d','%d','%d','%d','%d'>" % (
        self.set_odu16_ra_llc_conf_table_id, self.config_profile_id, self.llc_arq_enable, self.arq_win,
        self.frame_loss_threshold, self.leaky_bucket_timer_val, self.frame_loss_timeout)


# set_odu16_ra_tdd_mac_config Table
class SetOdu16RATddMacConfig(Base):
    """
    set_odu16_ra_tdd_mac_config Table
    """
    __tablename__ = 'set_odu16_ra_tdd_mac_config'
    set_odu16_ra_tdd_mac_config_table_id = Column(
        VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    rf_channel_frequency = Column(INTEGER)
    pass_phrase = Column(VARCHAR(64))
    rfcoding = Column(SMALLINT)
    tx_power = Column(INTEGER)
    max_power = Column(INTEGER)
    max_crc_errors = Column(INTEGER)
    leaky_bucket_timer_value = Column(INTEGER)

    def __init__(self, config_profile_id, rf_channel_frequency, pass_phrase, rfcoding, tx_power, max_crc_errors,
                 leaky_bucket_timer_value):
        self.set_odu16_ra_tdd_mac_config_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.rf_channel_frequency = rf_channel_frequency
        self.pass_phrase = pass_phrase
        self.rfcoding = rfcoding
        self.tx_power = tx_power
        self.max_crc_errors = max_crc_errors
        self.leaky_bucket_timer_value = leaky_bucket_timer_value

    def __repr__(self):
        return "SetOdu16RATddMacConfig<'%s','%s','%d','%s','%d','%d','%d','%d','%d'>" % (
        self.set_odu16_ra_tdd_mac_config_table_id, self.config_profile_id, self.rf_channel_frequency, self.pass_phrase,
        self.rfcoding, self.tx_power, self.max_crc_errors, self.leaky_bucket_timer_value, self.max_power)


# set_odu16_ru_conf_table Table
class SetOdu16RUConfTable(Base):
    """
    set_odu16_ru_conf_table Table
    """
    __tablename__ = 'set_odu16_ru_conf_table'
    set_odu16_ru_conf_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    adminstate = Column(SMALLINT)
    channel_bandwidth = Column(INTEGER)
    sysnch_source = Column(INTEGER)
    country_code = Column(VARCHAR(16))

    def __init__(self, config_profile_id, adminstate, channel_bandwidth, sysnch_source, country_code):
        self.set_odu16_ru_conf_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.adminstate = adminstate
        self.channel_bandwidth = channel_bandwidth
        self.sysnch_source = sysnch_source
        self.country_code = country_code

    def __repr__(self):
        return "SetOdu16RUConfTable<'%s','%s','%d','%d','%d','%s'>" % (
        self.set_odu16_ru_conf_table_id, self.config_profile_id, self.adminstate, self.channel_bandwidth,
        self.sysnch_source, self.country_code)

# set_odu16_ru_date_time_table Table


class SetOdu16RUDateTimeTable(Base):
    """
    set_odu16_ru_date_time_table Table
    """
    __tablename__ = 'set_odu16_ru_date_time_table'
    set_odu16_ru_date_time_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    year = Column(INTEGER)
    month = Column(INTEGER)
    day = Column(INTEGER)
    hour = Column(INTEGER)
    min = Column(INTEGER)
    sec = Column(INTEGER)

    def __init__(self, config_profile_id, year, month, day, hour, min, sec):
        self.set_odu16_ru_date_time_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec

    def __repr__(self):
        return "SetOdu16RUConfTable<'%s','%s','%d','%d','%d','%d','%d','%d'>" % (
        self.set_odu16_ru_date_time_table_id, self.config_profile_id, self.year, self.month, self.day, self.hour,
        self.min, self.sec)

# set_odu16_sync_config_table Table


class SetOdu16SyncConfigTable(Base):
    """
    set_odu16_sync_config_table Table
    """
    __tablename__ = 'set_odu16_sync_config_table'
    set_odu16_sync_config_table_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    admin_status = Column(SMALLINT)
    raster_time = Column(INTEGER)
    num_slaves = Column(INTEGER)
    sync_loss_threshold = Column(INTEGER)
    leaky_bucket_timer = Column(INTEGER)
    sync_lost_timeout = Column(INTEGER)
    sync_config_time_adjust = Column(INTEGER)
    sync_config_broadcast_enable = Column(SMALLINT)

    def __init__(self, config_profile_id, admin_status, raster_time, num_slaves, sync_loss_threshold,
                 leaky_bucket_timer, sync_lost_timeout, sync_config_time_adjust):
        self.set_odu16_sync_config_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.admin_status = admin_status
        self.raster_time = raster_time
        self.num_slaves = num_slaves
        self.sync_loss_threshold = sync_loss_threshold
        self.leaky_bucket_timer = leaky_bucket_timer
        self.sync_lost_timeout = sync_lost_timeout
        self.sync_config_time_adjust = sync_config_time_adjust

    def __repr__(self):
        return "SetOdu16SyncConfigTable<'%s','%s','%d','%d','%d','%d','%d','%d','%d','%d'>" % (
        self.set_odu16_sync_config_table_id, self.config_profile_id, self.admin_status, self.raster_time,
        self.num_slaves, self.sync_loss_threshold, self.leaky_bucket_timer, self.sync_lost_timeout,
        self.sync_config_time_adjust, self.sync_config_broadcast_enable)

# set_odu16_misc Table


class SetOdu16Misc(Base):
    """
    set_odu16_misc Table
    """
    __tablename__ = 'set_odu16_misc'
    set_odu16_misc_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    sys_contact = Column(VARCHAR(256))
    sys_name = Column(VARCHAR(256))
    sys_location = Column(VARCHAR(256))
    snmp_enable_authen_traps = Column(SMALLINT)

    def __init__(self, config_profile_id, sys_contact, sys_name, sys_location, snmp_enable_authen_traps):
        self.set_odu16_misc_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.sys_contact = sys_contact
        self.sys_name = sys_name
        self.sys_location = sys_location
        self.snmp_enable_authen_traps = snmp_enable_authen_traps

    def __repr__(self):
        return "SetOdu16Misc<'%s','%s','%s','%s','%s','%d'>" % (
        self.set_odu16_misc_id, self.config_profile_id, self.sys_contact, self.sys_name, self.sys_location,
        self.snmp_enable_authen_traps)

# set_odu16_sys_omc_registration_table  Table


class SetOdu16SysOmcRegistrationTable(Base):
    """
    set_odu16_sys_omc_registration_table
    """
    __tablename__ = 'set_odu16_sys_omc_registration_table'
    set_odu16_sys_omc_registration_table_id = Column(
        VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    sys_omc_register_contact_addr = Column(VARCHAR(128))
    sys_omc_register_contact_person = Column(VARCHAR(32))
    sys_omc_register_contact_mobile = Column(VARCHAR(16))
    sys_omc_register_alternate_contact = Column(VARCHAR(64))
    sys_omc_register_contact_email = Column(VARCHAR(64))
    sys_omc_register_active_card_hwld = Column(VARCHAR(30))
    sys_omc_registerne_site_direction = Column(VARCHAR(30))
    sys_omc_registerne_site_landmark = Column(VARCHAR(30))
    sys_omc_registerne_site_latitude = Column(VARCHAR(30))
    sys_omc_registerne_site_longitude = Column(VARCHAR(30))
    sys_omc_registerne_state = Column(VARCHAR(30))
    sys_omc_register_country = Column(VARCHAR(30))
    sys_omc_register_city = Column(VARCHAR(30))
    sys_omc_register_sitebldg = Column(VARCHAR(30))
    sys_omc_registersitefloor = Column(VARCHAR(30))

    def __init__(
            self, config_profile_id, sys_omc_register_contact_addr, sys_omc_register_contact_person,
            sys_omc_register_contact_mobile, sys_omc_register_alternate_contact, sys_omc_register_contact_email,
            sys_omc_register_active_card_hwld, sys_omc_registerne_site_direction, sys_omc_registerne_site_landmark,
            sys_omc_registerne_site_latitude,
            sys_omc_registerne_site_longitude, sys_omc_registerne_state, sys_omc_register_country,
            sys_omc_register_city, sys_omc_register_sitebldg,
            sys_omc_registersitefloor):
        self.set_odu16_sys_omc_registration_table_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.sys_omc_register_contact_addr = sys_omc_register_contact_addr
        self.sys_omc_register_contact_person = sys_omc_register_contact_person
        self.sys_omc_register_contact_mobile = sys_omc_register_contact_mobile
        self.sys_omc_register_alternate_contact = sys_omc_register_alternate_contact
        self.sys_omc_register_contact_email = sys_omc_register_contact_email
        self.sys_omc_register_active_card_hwld = sys_omc_register_active_card_hwld
        self.sys_omc_registerne_site_direction = sys_omc_registerne_site_direction
        self.sys_omc_registerne_site_landmark = sys_omc_registerne_site_landmark
        self.sys_omc_registerne_site_latitude = sys_omc_registerne_site_latitude
        self.sys_omc_registerne_site_longitude = sys_omc_registerne_site_longitude
        self.sys_omc_registerne_state = sys_omc_registerne_state
        self.sys_omc_register_country = sys_omc_register_country
        self.sys_omc_register_city = sys_omc_register_city
        self.sys_omc_register_sitebldg = sys_omc_register_sitebldg
        self.sys_omc_registersitefloor = sys_omc_registersitefloor

    def __repr__(self):
        return "SetOdu16Misc<'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'>" % (
        self.set_odu16_sys_omc_registration_table_id, self.config_profile_id, self.sys_omc_register_contact_addr,
        self.sys_omc_register_contact_person, self.sys_omc_register_contact_mobile,
        self.sys_omc_register_alternate_contact, self.sys_omc_register_contact_email,
        self.sys_omc_register_active_card_hwld,
        self.sys_omc_registerne_site_direction,
        self.sys_omc_registerne_site_landmark,
        self.sys_omc_registerne_site_latitude,
        self.sys_omc_registerne_site_longitude,
        self.sys_omc_registerne_state,
        self.sys_omc_register_country,
        self.sys_omc_register_city,
        self.sys_omc_register_sitebldg,
        self.sys_omc_registersitefloor
        )


class GetOdu16_ru_conf_table(Base):
    """

    @param host_id:
    @param op_state:
    @param object_model_version:
    @param default_node_type:
    @param no_radio_interfaces:
    """
    __tablename__ = "get_odu16_ru_conf_table"
    get_odu16_ru_conf_table_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    op_state = Column(SMALLINT)
    object_model_version = Column(VARCHAR)
    default_node_type = Column(SMALLINT)
    no_radio_interfaces = Column(INT)

    def __init__(self, host_id, op_state, object_model_version, default_node_type, no_radio_interfaces):
        self.get_odu16_ru_conf_table_id = uuid.uuid1()
        self.host_id = host_id
        self.op_state = op_state
        self.object_model_version = object_model_version
        self.default_node_type = default_node_type
        self.no_radio_interfaces = no_radio_interfaces

    def __repr__(self):
        return "<GetOdu16_ru_conf_table('%s','%s','%s','%s','%s','%s')>" % (
        self.get_odu16_ru_conf_table_id, self.host_id, self.op_state, self.object_model_version, self.default_node_type,
        self.no_radio_interfaces)


class GetOdu16PeerNodeStatusTable(Base):
    """

    @param host_id:
    @param link_status:
    @param tunnel_status:
    @param sig_strength:
    @param peer_mac_addr:
    @param ssidentifier:
    @param peer_node_status_raster_time:
    @param peer_node_status_num_slaves:
    @param peer_node_status_timer_adjust:
    @param peer_node_status_rf_config:
    @param index:
    @param timeslot_index:
    @param timestamp:
    """
    __tablename__ = "get_odu16_peer_node_status_table"
    get_odu16_peer_node_status_table_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    link_status = Column(VARCHAR(16))
    tunnel_status = Column(VARCHAR(16))
    sig_strength = Column(INT)
    peer_mac_addr = Column(VARCHAR(32))
    ssidentifier = Column(VARCHAR(32))
    peer_node_status_raster_time = Column(INT)
    peer_node_status_num_slaves = Column(INT)
    peer_node_status_timer_adjust = Column(INT)
    peer_node_status_rf_config = Column(VARCHAR(16))
    index = Column(SMALLINT)
    timeslot_index = Column(SMALLINT)
    timestamp = Column(TIMESTAMP)

    def __init__(self, host_id, link_status, tunnel_status, sig_strength, peer_mac_addr, ssidentifier,
                 peer_node_status_raster_time, peer_node_status_num_slaves, peer_node_status_timer_adjust,
                 peer_node_status_rf_config, index, timeslot_index, timestamp):
        self.get_odu16_peer_node_status_table_id = uuid.uuid1()
        self.host_id = host_id
        self.link_status = link_status
        self.tunnel_status = tunnel_status
        self.sig_strength = sig_strength
        self.peer_mac_addr = peer_mac_addr
        self.ssidentifier = ssidentifier
        self.peer_node_status_raster_time = peer_node_status_raster_time
        self.peer_node_status_num_slaves = peer_node_status_num_slaves
        self.peer_node_status_timer_adjust = peer_node_status_timer_adjust
        self.peer_node_status_rf_config = peer_node_status_rf_config
        self.index = index
        self.timeslot_index = timeslot_index
        self.timestamp = timestamp

    def __repr__(self):
        return "<GetOdu16PeerNodeStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.get_odu16_peer_node_status_table_id, self.host_id, self.link_status, self.tunnel_status, self.sig_strength,
        self.peer_mac_addr, self.ssidentifier, self.peer_node_status_raster_time, self.peer_node_status_num_slaves,
        self.peer_node_status_timer_adjust, self.peer_node_status_rf_config, self.index, self.timeslot_index,
        self.timestamp)


############################## Odu16 ##########################################
############################# odu100 Tables ###################################
class Odu100EswATUConfigTable(Base):
    """

    @param config_profile_id:
    @param eswATUConfigAtuId:
    @param eswATUConfigEntryType:
    @param eswATUConfigPriorityVal:
    @param eswATUConfigMacAddress:
    @param eswATUConfigMemberPorts:
    @param eswATUConfigRowStatus:
    """
    __tablename__ = "odu100_eswATUConfigTable"
    odu100_eswATUConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswATUConfigAtuId = Column(INTEGER)
    eswATUConfigEntryType = Column(INTEGER)
    eswATUConfigPriorityVal = Column(INTEGER)
    eswATUConfigMacAddress = Column(VARCHAR(32))
    eswATUConfigMemberPorts = Column(INTEGER)
    eswATUConfigRowStatus = Column(INTEGER)

    def __init__(self, config_profile_id, eswATUConfigAtuId, eswATUConfigEntryType, eswATUConfigPriorityVal,
                 eswATUConfigMacAddress, eswATUConfigMemberPorts, eswATUConfigRowStatus):
        self.odu100_eswATUConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswATUConfigAtuId = eswATUConfigAtuId
        self.eswATUConfigEntryType = eswATUConfigEntryType
        self.eswATUConfigPriorityVal = eswATUConfigPriorityVal
        self.eswATUConfigMacAddress = eswATUConfigMacAddress
        self.eswATUConfigMemberPorts = eswATUConfigMemberPorts
        self.eswATUConfigRowStatus = eswATUConfigRowStatus

    def __repr__(self):
        return "<Odu100EswATUConfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswATUConfigTable_id, self.config_profile_id, self.eswATUConfigAtuId, self.eswATUConfigEntryType,
        self.eswATUConfigPriorityVal, self.eswATUConfigMacAddress, self.eswATUConfigMemberPorts,
        self.eswATUConfigRowStatus)


class Odu100EswBadFramesTable(Base):
    """

    @param host_id:
    @param eswBadFramesPortNum:
    @param eswBadFramesInUndersizeRx:
    @param eswBadFramesInFragmentsRx:
    @param eswBadFramesInOversizeRx:
    @param eswBadFramesInJabberRx:
    @param eswBadFramesInFCSErrRx:
    @param eswBadFramesOutFCSErrTx:
    @param eswBadFramesDeferredTx:
    @param eswBadFramesCollisionsTx:
    @param eswBadFramesLateTx:
    @param eswBadFramesExcessiveTx:
    @param eswBadFramesSingleTx:
    @param eswBadFramesMultipleTx:
    """
    __tablename__ = "odu100_eswBadFramesTable"
    odu100_eswBadFramesTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    eswBadFramesPortNum = Column(INTEGER)
    eswBadFramesInUndersizeRx = Column(INTEGER)
    eswBadFramesInFragmentsRx = Column(INTEGER)
    eswBadFramesInOversizeRx = Column(INTEGER)
    eswBadFramesInJabberRx = Column(INTEGER)
    eswBadFramesInFCSErrRx = Column(INTEGER)
    eswBadFramesOutFCSErrTx = Column(INTEGER)
    eswBadFramesDeferredTx = Column(INTEGER)
    eswBadFramesCollisionsTx = Column(INTEGER)
    eswBadFramesLateTx = Column(INTEGER)
    eswBadFramesExcessiveTx = Column(INTEGER)
    eswBadFramesSingleTx = Column(INTEGER)
    eswBadFramesMultipleTx = Column(INTEGER)

    def __init__(self, host_id, eswBadFramesPortNum, eswBadFramesInUndersizeRx, eswBadFramesInFragmentsRx,
                 eswBadFramesInOversizeRx, eswBadFramesInJabberRx, eswBadFramesInFCSErrRx, eswBadFramesOutFCSErrTx,
                 eswBadFramesDeferredTx, eswBadFramesCollisionsTx, eswBadFramesLateTx, eswBadFramesExcessiveTx,
                 eswBadFramesSingleTx, eswBadFramesMultipleTx):
        self.odu100_eswBadFramesTable_id = uuid.uuid1()
        self.host_id = host_id
        self.eswBadFramesPortNum = eswBadFramesPortNum
        self.eswBadFramesInUndersizeRx = eswBadFramesInUndersizeRx
        self.eswBadFramesInFragmentsRx = eswBadFramesInFragmentsRx
        self.eswBadFramesInOversizeRx = eswBadFramesInOversizeRx
        self.eswBadFramesInJabberRx = eswBadFramesInJabberRx
        self.eswBadFramesInFCSErrRx = eswBadFramesInFCSErrRx
        self.eswBadFramesOutFCSErrTx = eswBadFramesOutFCSErrTx
        self.eswBadFramesDeferredTx = eswBadFramesDeferredTx
        self.eswBadFramesCollisionsTx = eswBadFramesCollisionsTx
        self.eswBadFramesLateTx = eswBadFramesLateTx
        self.eswBadFramesExcessiveTx = eswBadFramesExcessiveTx
        self.eswBadFramesSingleTx = eswBadFramesSingleTx
        self.eswBadFramesMultipleTx = eswBadFramesMultipleTx

    def __repr__(self):
        return "<Odu100EswBadFramesTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswBadFramesTable_id, self.host_id, self.eswBadFramesPortNum, self.eswBadFramesInUndersizeRx,
        self.eswBadFramesInFragmentsRx, self.eswBadFramesInOversizeRx, self.eswBadFramesInJabberRx,
        self.eswBadFramesInFCSErrRx, self.eswBadFramesOutFCSErrTx, self.eswBadFramesDeferredTx,
        self.eswBadFramesCollisionsTx, self.eswBadFramesLateTx, self.eswBadFramesExcessiveTx, self.eswBadFramesSingleTx,
        self.eswBadFramesMultipleTx)


class Odu100EswGoodFramesTable(Base):
    """

    @param host_id:
    @param eswGoodFramesPortNum:
    @param eswGoodFramesInUnicast:
    @param eswGoodFramesOutUnicast:
    @param eswGoodFramesInBCast:
    @param eswGoodFramesOurBCast:
    @param eswGoodFramesInMCast:
    @param eswGoodFramesOutMcast:
    """
    __tablename__ = "odu100_eswGoodFramesTable"
    odu100_eswGoodFramesTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    eswGoodFramesPortNum = Column(INTEGER)
    eswGoodFramesInUnicast = Column(INTEGER)
    eswGoodFramesOutUnicast = Column(INTEGER)
    eswGoodFramesInBCast = Column(INTEGER)
    eswGoodFramesOurBCast = Column(INTEGER)
    eswGoodFramesInMCast = Column(INTEGER)
    eswGoodFramesOutMcast = Column(INTEGER)

    def __init__(self, host_id, eswGoodFramesPortNum, eswGoodFramesInUnicast, eswGoodFramesOutUnicast,
                 eswGoodFramesInBCast, eswGoodFramesOurBCast, eswGoodFramesInMCast, eswGoodFramesOutMcast):
        self.odu100_eswGoodFramesTable_id = uuid.uuid1()
        self.host_id = host_id
        self.eswGoodFramesPortNum = eswGoodFramesPortNum
        self.eswGoodFramesInUnicast = eswGoodFramesInUnicast
        self.eswGoodFramesOutUnicast = eswGoodFramesOutUnicast
        self.eswGoodFramesInBCast = eswGoodFramesInBCast
        self.eswGoodFramesOurBCast = eswGoodFramesOurBCast
        self.eswGoodFramesInMCast = eswGoodFramesInMCast
        self.eswGoodFramesOutMcast = eswGoodFramesOutMcast

    def __repr__(self):
        return "<Odu100EswGOOdFramesTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswGoodFramesTable_id, self.host_id, self.eswGoodFramesPortNum, self.eswGoodFramesInUnicast,
        self.eswGoodFramesOutUnicast, self.eswGoodFramesInBCast, self.eswGoodFramesOurBCast, self.eswGoodFramesInMCast,
        self.eswGoodFramesOutMcast)


class Odu100EswMirroringPortTable(Base):
    """

    @param config_profile_id:
    @param eswMirroringPortIndexId:
    @param eswMirroringPort:
    @param eswMirroringPortSecond:
    """
    __tablename__ = "odu100_eswMirroringPortTable"
    odu100_eswMirroringPortTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswMirroringPortIndexId = Column(INTEGER)
    eswMirroringPort = Column(INTEGER)
    eswMirroringPortSecond = Column(INTEGER)

    def __init__(self, config_profile_id, eswMirroringPortIndexId, eswMirroringPort, eswMirroringPortSecond):
        self.odu100_eswMirroringPortTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswMirroringPortIndexId = eswMirroringPortIndexId
        self.eswMirroringPort = eswMirroringPort
        self.eswMirroringPortSecond = eswMirroringPortSecond

    def __repr__(self):
        return "<Odu100EswMirrOringPOrtTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_eswMirroringPortTable_id, self.config_profile_id, self.eswMirroringPortIndexId,
        self.eswMirroringPort, self.eswMirroringPortSecond)


class Odu100EswPortAccessListTable(Base):
    """

    @param config_profile_id:
    @param eswPortACLPortNum:
    @param eswPortACLSecIndex:
    @param eswPortACLMacAddress:
    """
    __tablename__ = "odu100_eswPortAccessListTable"
    odu100_eswPortAccessListTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswPortACLPortNum = Column(INTEGER)
    eswPortACLSecIndex = Column(INTEGER)
    eswPortACLMacAddress = Column(VARCHAR(32))

    def __init__(self, config_profile_id, eswPortACLPortNum, eswPortACLSecIndex, eswPortACLMacAddress):
        self.odu100_eswPortAccessListTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswPortACLPortNum = eswPortACLPortNum
        self.eswPortACLSecIndex = eswPortACLSecIndex
        self.eswPortACLMacAddress = eswPortACLMacAddress

    def __repr__(self):
        return "<Odu100EswPOrtAccessListTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_eswPortAccessListTable_id, self.config_profile_id, self.eswPortACLPortNum, self.eswPortACLSecIndex,
        self.eswPortACLMacAddress)


class Odu100EswPortBwTable(Base):
    """

    @param config_profile_id:
    @param eswPortBwPortNum:
    @param eswPortBwEgressBw:
    @param eswPortBwIngressBw:
    """
    __tablename__ = "odu100_eswPortBwTable"
    odu100_eswPortBwTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswPortBwPortNum = Column(INTEGER)
    eswPortBwEgressBw = Column(INTEGER)
    eswPortBwIngressBw = Column(INTEGER)

    def __init__(self, config_profile_id, eswPortBwPortNum, eswPortBwEgressBw, eswPortBwIngressBw):
        self.odu100_eswPortBwTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswPortBwPortNum = eswPortBwPortNum
        self.eswPortBwEgressBw = eswPortBwEgressBw
        self.eswPortBwIngressBw = eswPortBwIngressBw

    def __repr__(self):
        return "<Odu100EswPOrtBwTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_eswPortBwTable_id, self.config_profile_id, self.eswPortBwPortNum, self.eswPortBwEgressBw,
        self.eswPortBwIngressBw)


class Odu100EswPortConfigTable(Base):
    """

    @param config_profile_id:
    @param eswPortConfigPortNum:
    @param eswPortConfigAdminState:
    @param eswPortConfigLinkMode:
    @param eswPortConfigPortVid:
    @param eswPortConfigAuthState:
    @param eswPortConfigMirrDir:
    @param eswPortConfigDotqMode:
    @param eswPortConfigMacFlowControl:
    """
    __tablename__ = "odu100_eswPortConfigTable"
    odu100_eswPortConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswPortConfigPortNum = Column(INTEGER)
    eswPortConfigAdminState = Column(INTEGER)
    eswPortConfigLinkMode = Column(INTEGER)
    eswPortConfigPortVid = Column(INTEGER)
    eswPortConfigAuthState = Column(INTEGER)
    eswPortConfigMirrDir = Column(INTEGER)
    eswPortConfigDotqMode = Column(INTEGER)
    eswPortConfigMacFlowControl = Column(INTEGER)

    def __init__(self, config_profile_id, eswPortConfigPortNum, eswPortConfigAdminState, eswPortConfigLinkMode,
                 eswPortConfigPortVid, eswPortConfigAuthState, eswPortConfigMirrDir, eswPortConfigDotqMode,
                 eswPortConfigMacFlowControl):
        self.odu100_eswPortConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswPortConfigPortNum = eswPortConfigPortNum
        self.eswPortConfigAdminState = eswPortConfigAdminState
        self.eswPortConfigLinkMode = eswPortConfigLinkMode
        self.eswPortConfigPortVid = eswPortConfigPortVid
        self.eswPortConfigAuthState = eswPortConfigAuthState
        self.eswPortConfigMirrDir = eswPortConfigMirrDir
        self.eswPortConfigDotqMode = eswPortConfigDotqMode
        self.eswPortConfigMacFlowControl = eswPortConfigMacFlowControl

    def __repr__(self):
        return "<Odu100EswPOrtCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswPortConfigTable_id, self.config_profile_id, self.eswPortConfigPortNum,
        self.eswPortConfigAdminState, self.eswPortConfigLinkMode, self.eswPortConfigPortVid,
        self.eswPortConfigAuthState, self.eswPortConfigMirrDir, self.eswPortConfigDotqMode,
        self.eswPortConfigMacFlowControl)


class Odu100EswPortQinQTable(Base):
    """

    @param config_profile_id:
    @param eswPortQinQPortNum:
    @param eswPortQinQAuthState:
    @param eswPortQinQProviderTag:
    """
    __tablename__ = "odu100_eswPortQinQTable"
    odu100_eswPortQinQTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswPortQinQPortNum = Column(INTEGER)
    eswPortQinQAuthState = Column(INTEGER)
    eswPortQinQProviderTag = Column(INTEGER)

    def __init__(self, config_profile_id, eswPortQinQPortNum, eswPortQinQAuthState, eswPortQinQProviderTag):
        self.odu100_eswPortQinQTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswPortQinQPortNum = eswPortQinQPortNum
        self.eswPortQinQAuthState = eswPortQinQAuthState
        self.eswPortQinQProviderTag = eswPortQinQProviderTag

    def __repr__(self):
        return "<Odu100EswPOrtQinQTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_eswPortQinQTable_id, self.config_profile_id, self.eswPortQinQPortNum, self.eswPortQinQAuthState,
        self.eswPortQinQProviderTag)


class Odu100EswPortStatisticsTable(Base):
    """

    @param host_id:
    @param eswPortStatisticsPortNum:
    @param eswPortStatisticsInDiscards:
    @param eswPortStatisticsInGoodOctets:
    @param eswPortStatisticsInBadOctets:
    @param eswPortStatisticsOutOctets:
    """
    __tablename__ = "odu100_eswPortStatisticsTable"
    odu100_eswPortStatisticsTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    eswPortStatisticsPortNum = Column(INTEGER)
    eswPortStatisticsInDiscards = Column(INTEGER)
    eswPortStatisticsInGoodOctets = Column(INTEGER)
    eswPortStatisticsInBadOctets = Column(INTEGER)
    eswPortStatisticsOutOctets = Column(INTEGER)

    def __init__(self, host_id, eswPortStatisticsPortNum, eswPortStatisticsInDiscards, eswPortStatisticsInGoodOctets,
                 eswPortStatisticsInBadOctets, eswPortStatisticsOutOctets):
        self.odu100_eswPortStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.eswPortStatisticsPortNum = eswPortStatisticsPortNum
        self.eswPortStatisticsInDiscards = eswPortStatisticsInDiscards
        self.eswPortStatisticsInGoodOctets = eswPortStatisticsInGoodOctets
        self.eswPortStatisticsInBadOctets = eswPortStatisticsInBadOctets
        self.eswPortStatisticsOutOctets = eswPortStatisticsOutOctets

    def __repr__(self):
        return "<Odu100EswPOrtStatisticsTable('%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswPortStatisticsTable_id, self.host_id, self.eswPortStatisticsPortNum,
        self.eswPortStatisticsInDiscards, self.eswPortStatisticsInGoodOctets, self.eswPortStatisticsInBadOctets,
        self.eswPortStatisticsOutOctets)


class Odu100EswPortStatusTable(Base):
    """

    @param host_id:
    @param eswPortStatusPortNum:
    @param eswPortStatusOpState:
    @param eswPortStatusLinkSpeed:
    @param eswPortStatusMacFlowControl:
    """
    __tablename__ = "odu100_eswPortStatusTable"
    odu100_eswPortStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    eswPortStatusPortNum = Column(INTEGER)
    eswPortStatusOpState = Column(INTEGER)
    eswPortStatusLinkSpeed = Column(INTEGER)
    eswPortStatusMacFlowControl = Column(INTEGER)

    def __init__(self, host_id, eswPortStatusPortNum, eswPortStatusOpState, eswPortStatusLinkSpeed,
                 eswPortStatusMacFlowControl):
        self.odu100_eswPortStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.eswPortStatusPortNum = eswPortStatusPortNum
        self.eswPortStatusOpState = eswPortStatusOpState
        self.eswPortStatusLinkSpeed = eswPortStatusLinkSpeed
        self.eswPortStatusMacFlowControl = eswPortStatusMacFlowControl

    def __repr__(self):
        return "<Odu100EswPOrtStatusTable('%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswPortStatusTable_id, self.host_id, self.eswPortStatusPortNum, self.eswPortStatusOpState,
        self.eswPortStatusLinkSpeed, self.eswPortStatusMacFlowControl)


class Odu100EswVlanConfigTable(Base):
    """

    @param config_profile_id:
    @param eswVlanConfigVlanId:
    @param eswVlanConfigVlanName:
    @param eswVlanConfigVlanType:
    @param eswVlanConfigVlanTag:
    @param eswVlanConfigMemberPorts:
    @param eswVlanConfigRowStatus:
    """
    __tablename__ = "odu100_eswVlanConfigTable"
    odu100_eswVlanConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    eswVlanConfigVlanId = Column(INTEGER)
    eswVlanConfigVlanName = Column(VARCHAR(8))
    eswVlanConfigVlanType = Column(INTEGER)
    eswVlanConfigVlanTag = Column(INTEGER)
    eswVlanConfigMemberPorts = Column(INTEGER)
    eswVlanConfigRowStatus = Column(INTEGER)

    def __init__(self, config_profile_id, eswVlanConfigVlanId, eswVlanConfigVlanName, eswVlanConfigVlanType,
                 eswVlanConfigVlanTag, eswVlanConfigMemberPorts, eswVlanConfigRowStatus):
        self.odu100_eswVlanConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.eswVlanConfigVlanId = eswVlanConfigVlanId
        self.eswVlanConfigVlanName = eswVlanConfigVlanName
        self.eswVlanConfigVlanType = eswVlanConfigVlanType
        self.eswVlanConfigVlanTag = eswVlanConfigVlanTag
        self.eswVlanConfigMemberPorts = eswVlanConfigMemberPorts
        self.eswVlanConfigRowStatus = eswVlanConfigRowStatus

    def __repr__(self):
        return "<Odu100EswVlanCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_eswVlanConfigTable_id, self.config_profile_id, self.eswVlanConfigVlanId, self.eswVlanConfigVlanName,
        self.eswVlanConfigVlanType, self.eswVlanConfigVlanTag, self.eswVlanConfigMemberPorts,
        self.eswVlanConfigRowStatus)


class Odu100HwDescTable(Base):
    """

    @param host_id:
    @param hwDescIndex:
    @param hwVersion:
    @param hwSerialNo:
    """
    __tablename__ = "odu100_hwDescTable"
    odu100_hwDescTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    hwDescIndex = Column(INTEGER)
    hwVersion = Column(VARCHAR(128))
    hwSerialNo = Column(VARCHAR(64))

    def __init__(self, host_id, hwDescIndex, hwVersion, hwSerialNo):
        self.odu100_hwDescTable_id = uuid.uuid1()
        self.host_id = host_id
        self.hwDescIndex = hwDescIndex
        self.hwVersion = hwVersion
        self.hwSerialNo = hwSerialNo

    def __repr__(self):
        return "<Odu100HwDescTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_hwDescTable_id, self.host_id, self.hwDescIndex, self.hwVersion, self.hwSerialNo)


class Odu100IpConfigTable(Base):
    """

    @param config_profile_id:
    @param ipConfigIndex:
    @param adminState:
    @param ipAddress:
    @param ipNetworkMask:
    @param ipDefaultGateway:
    @param autoIpConfig:
    """
    __tablename__ = "odu100_ipConfigTable"
    odu100_ipConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    ipConfigIndex = Column(INTEGER)
    adminState = Column(INTEGER)
    ipAddress = Column(VARCHAR(32))
    ipNetworkMask = Column(VARCHAR(32))
    ipDefaultGateway = Column(VARCHAR(32))
    autoIpConfig = Column(INTEGER)

    def __init__(self, config_profile_id, ipConfigIndex, adminState, ipAddress, ipNetworkMask, ipDefaultGateway,
                 autoIpConfig):
        self.odu100_ipConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.ipConfigIndex = ipConfigIndex
        self.adminState = adminState
        self.ipAddress = ipAddress
        self.ipNetworkMask = ipNetworkMask
        self.ipDefaultGateway = ipDefaultGateway
        self.autoIpConfig = autoIpConfig

    def __repr__(self):
        return "<Odu100IpCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_ipConfigTable_id, self.config_profile_id, self.ipConfigIndex, self.adminState, self.ipAddress,
        self.ipNetworkMask, self.ipDefaultGateway, self.autoIpConfig)


class Odu100NwInterfaceStatisticsTable(Base):
    """

    @param host_id:
    @param nwStatsIndex:
    @param rxPackets:
    @param txPackets:
    @param rxBytes:
    @param txBytes:
    @param rxErrors:
    @param txErrors:
    @param rxDropped:
    @param txDropped:
    """
    __tablename__ = "odu100_nwInterfaceStatisticsTable"
    odu100_nwInterfaceStatisticsTable_id = Column(
        VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    nwStatsIndex = Column(INTEGER)
    rxPackets = Column(INTEGER)
    txPackets = Column(INTEGER)
    rxBytes = Column(INTEGER)
    txBytes = Column(INTEGER)
    rxErrors = Column(INTEGER)
    txErrors = Column(INTEGER)
    rxDropped = Column(INTEGER)
    txDropped = Column(INTEGER)

    def __init__(self, host_id, nwStatsIndex, rxPackets, txPackets, rxBytes, txBytes, rxErrors, txErrors, rxDropped,
                 txDropped):
        self.odu100_nwInterfaceStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.nwStatsIndex = nwStatsIndex
        self.rxPackets = rxPackets
        self.txPackets = txPackets
        self.rxBytes = rxBytes
        self.txBytes = txBytes
        self.rxErrors = rxErrors
        self.txErrors = txErrors
        self.rxDropped = rxDropped
        self.txDropped = txDropped

    def __repr__(self):
        return "<Odu100NwInterfaceStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_nwInterfaceStatisticsTable_id, self.host_id, self.nwStatsIndex, self.rxPackets, self.txPackets,
        self.rxBytes, self.txBytes, self.rxErrors, self.txErrors, self.rxDropped, self.txDropped)


class Odu100NwInterfaceStatusTable(Base):
    """

    @param host_id:
    @param nwStatusIndex:
    @param nwInterfaceName:
    @param operationalState:
    @param macAddress:
    """
    __tablename__ = "odu100_nwInterfaceStatusTable"
    odu100_nwInterfaceStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    nwStatusIndex = Column(INTEGER)
    nwInterfaceName = Column(VARCHAR(16))
    operationalState = Column(INTEGER)
    macAddress = Column(VARCHAR(32))

    def __init__(self, host_id, nwStatusIndex, nwInterfaceName, operationalState, macAddress):
        self.odu100_nwInterfaceStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.nwStatusIndex = nwStatusIndex
        self.nwInterfaceName = nwInterfaceName
        self.operationalState = operationalState
        self.macAddress = macAddress

    def __repr__(self):
        return "<Odu100NwInterfaceStatusTable('%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_nwInterfaceStatusTable_id, self.host_id, self.nwStatusIndex, self.nwInterfaceName,
        self.operationalState, self.macAddress)


class Odu100OmcConfTable(Base):
    """

    @param config_profile_id:
    @param omcConfIndex:
    @param omcIpAddress:
    @param periodicStatsTimer:
    """
    __tablename__ = "odu100_omcConfTable"
    odu100_omcConfTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    omcConfIndex = Column(INTEGER)
    omcIpAddress = Column(VARCHAR(32))
    periodicStatsTimer = Column(INTEGER)

    def __init__(self, config_profile_id, omcConfIndex, omcIpAddress, periodicStatsTimer):
        self.odu100_omcConfTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.omcConfIndex = omcConfIndex
        self.omcIpAddress = omcIpAddress
        self.periodicStatsTimer = periodicStatsTimer

    def __repr__(self):
        return "<Odu100OmcCOnfTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_omcConfTable_id, self.config_profile_id, self.omcConfIndex, self.omcIpAddress,
        self.periodicStatsTimer)


class Odu100PeerConfigTable(Base):
    """

    @param config_profile_id:
    @param raIndex:
    @param timeslotIndex:
    @param peerMacAddress:
    @param guaranteedUplinkBW:
    @param guaranteedDownlinkBW:
    @param basicrateMCSIndex:
    """
    __tablename__ = "odu100_peerConfigTable"
    odu100_peerConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    timeslotIndex = Column(INTEGER)
    peerMacAddress = Column(VARCHAR(32))
    guaranteedUplinkBW = Column(INTEGER)
    guaranteedDownlinkBW = Column(INTEGER)
    basicRateMCSIndex = Column(INTEGER)

    def __init__(self, config_profile_id, raIndex, timeslotIndex, peerMacAddress, guaranteedUplinkBW,
                 guaranteedDownlinkBW, basicrateMCSIndex):
        self.odu100_peerConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.timeslotIndex = timeslotIndex
        self.peerMacAddress = peerMacAddress
        self.guaranteedUplinkBW = guaranteedUplinkBW
        self.guaranteedDownlinkBW = guaranteedDownlinkBW
        self.basicRateMCSIndex = basicRateMCSIndex

    def __repr__(self):
        return "<Odu100PeerCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_peerConfigTable_id, self.config_profile_id, self.raIndex, self.timeslotIndex, self.peerMacAddress,
        self.guaranteedUplinkBW, self.guaranteedDownlinkBW, self.basicRateMCSIndex)


class Odu100PeerLinkStatisticsTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param timeslotindex:
    @param txdroped:
    @param rxDataSubFrames:
    @param txDataSubFrames:
    @param signalstrength1:
    @param txRetransmissions5:
    @param txRetransmissions4:
    @param txRetransmissions3:
    @param txRetransmissions2:
    @param txRetransmissions1:
    @param txRetransmissions0:
    @param rxRetransmissions5:
    @param rxRetransmissions4:
    @param rxRetransmissions3:
    @param rxRetransmissions2:
    @param rxRetransmissions1:
    @param rxRetransmissions0:
    @param rxBroadcastDataSubFrames:
    @param rateIncreases:
    @param rateDecreases:
    @param emptyRasters:
    @param rxDroppedTpPkts:
    @param rxDroppedRadioPkts:
    @param signalstrength2:
    """
    __tablename__ = "odu100_peerLinkStatisticsTable"
    odu100_peerLinkStatisticsTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    timeslotindex = Column(INTEGER)
    txdroped = Column(INTEGER)
    rxDataSubFrames = Column(INTEGER)
    txDataSubFrames = Column(INTEGER)
    signalstrength1 = Column(INTEGER)
    txRetransmissions5 = Column(INTEGER)
    txRetransmissions4 = Column(INTEGER)
    txRetransmissions3 = Column(INTEGER)
    txRetransmissions2 = Column(INTEGER)
    txRetransmissions1 = Column(INTEGER)
    txRetransmissions0 = Column(INTEGER)
    rxRetransmissions5 = Column(INTEGER)
    rxRetransmissions4 = Column(INTEGER)
    rxRetransmissions3 = Column(INTEGER)
    rxRetransmissions2 = Column(INTEGER)
    rxRetransmissions1 = Column(INTEGER)
    rxRetransmissions0 = Column(INTEGER)
    rxBroadcastDataSubFrames = Column(INTEGER)
    rateIncreases = Column(INTEGER)
    rateDecreases = Column(INTEGER)
    emptyRasters = Column(INTEGER)
    rxDroppedTpPkts = Column(INTEGER)
    rxDroppedRadioPkts = Column(INTEGER)
    signalstrength2 = Column(INTEGER)

    def __init__(self, host_id, raIndex, timeslotindex, txdroped, rxDataSubFrames, txDataSubFrames, signalstrength1,
                 txRetransmissions5, txRetransmissions4, txRetransmissions3, txRetransmissions2, txRetransmissions1,
                 txRetransmissions0, rxRetransmissions5, rxRetransmissions4, rxRetransmissions3, rxRetransmissions2,
                 rxRetransmissions1, rxRetransmissions0, rxBroadcastDataSubFrames, rateIncreases, rateDecreases,
                 emptyRasters, rxDroppedTpPkts, rxDroppedRadioPkts, signalstrength2):
        self.odu100_peerLinkStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.timeslotindex = timeslotindex
        self.txdroped = txdroped
        self.rxDataSubFrames = rxDataSubFrames
        self.txDataSubFrames = txDataSubFrames
        self.signalstrength1 = signalstrength1
        self.txRetransmissions5 = txRetransmissions5
        self.txRetransmissions4 = txRetransmissions4
        self.txRetransmissions3 = txRetransmissions3
        self.txRetransmissions2 = txRetransmissions2
        self.txRetransmissions1 = txRetransmissions1
        self.txRetransmissions0 = txRetransmissions0
        self.rxRetransmissions5 = rxRetransmissions5
        self.rxRetransmissions4 = rxRetransmissions4
        self.rxRetransmissions3 = rxRetransmissions3
        self.rxRetransmissions2 = rxRetransmissions2
        self.rxRetransmissions1 = rxRetransmissions1
        self.rxRetransmissions0 = rxRetransmissions0
        self.rxBroadcastDataSubFrames = rxBroadcastDataSubFrames
        self.rateIncreases = rateIncreases
        self.rateDecreases = rateDecreases
        self.emptyRasters = emptyRasters
        self.rxDroppedTpPkts = rxDroppedTpPkts
        self.rxDroppedRadioPkts = rxDroppedRadioPkts
        self.signalstrength2 = signalstrength2

    def __repr__(self):
        return "<Odu100PeerLinkStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_peerLinkStatisticsTable_id, self.host_id, self.raIndex, self.timeslotindex, self.txdroped,
        self.rxDataSubFrames, self.txDataSubFrames, self.signalstrength1, self.txRetransmissions5,
        self.txRetransmissions4, self.txRetransmissions3, self.txRetransmissions2, self.txRetransmissions1,
        self.txRetransmissions0, self.rxRetransmissions5, self.rxRetransmissions4, self.rxRetransmissions3,
        self.rxRetransmissions2, self.rxRetransmissions1, self.rxRetransmissions0, self.rxBroadcastDataSubFrames,
        self.rateIncreases, self.rateDecreases, self.emptyRasters, self.rxDroppedTpPkts, self.rxDroppedRadioPkts,
        self.signalstrength2)


class Odu100PeerRateStatisticsTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param mcsIndex:
    @param timeSlotindex:
    @param peerrate:
    @param per:
    @param ticks:
    @param ticksMinimumRateTx:
    @param ticksWasted:
    """
    __tablename__ = "odu100_peerRateStatisticsTable"
    odu100_peerRateStatisticsTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    mcsIndex = Column(INTEGER)
    timeSlotindex = Column(INTEGER)
    peerrate = Column(INTEGER)
    per = Column(INTEGER)
    ticks = Column(INTEGER)
    ticksMinimumRateTx = Column(INTEGER)
    ticksWasted = Column(INTEGER)

    def __init__(self, host_id, raIndex, mcsIndex, timeSlotindex, peerrate, per, ticks, ticksMinimumRateTx,
                 ticksWasted):
        self.odu100_peerRateStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.mcsIndex = mcsIndex
        self.timeSlotindex = timeSlotindex
        self.peerrate = peerrate
        self.per = per
        self.ticks = ticks
        self.ticksMinimumRateTx = ticksMinimumRateTx
        self.ticksWasted = ticksWasted

    def __repr__(self):
        return "<Odu100PeerRateStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_peerRateStatisticsTable_id, self.host_id, self.raIndex, self.mcsIndex, self.timeSlotindex,
        self.peerrate, self.per, self.ticks, self.ticksMinimumRateTx, self.ticksWasted)


class Odu100PeerTunnelStatisticsTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param tsIndex:
    @param rxPacket:
    @param txPacket:
    @param rxBundles:
    @param txBundles:
    @param rxDroped:
    @param txDroped:
    """
    __tablename__ = "odu100_peerTunnelStatisticsTable"
    odu100_peerTunnelStatisticsTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    tsIndex = Column(INTEGER)
    rxPacket = Column(INTEGER)
    txPacket = Column(INTEGER)
    rxBundles = Column(INTEGER)
    txBundles = Column(INTEGER)
    rxDroped = Column(INTEGER)
    txDroped = Column(INTEGER)

    def __init__(self, host_id, raIndex, tsIndex, rxPacket, txPacket, rxBundles, txBundles, rxDroped, txDroped):
        self.odu100_peerTunnelStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.tsIndex = tsIndex
        self.rxPacket = rxPacket
        self.txPacket = txPacket
        self.rxBundles = rxBundles
        self.txBundles = txBundles
        self.rxDroped = rxDroped
        self.txDroped = txDroped

    def __repr__(self):
        return "<Odu100PeerTunnelStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_peerTunnelStatisticsTable_id, self.host_id, self.raIndex, self.tsIndex, self.rxPacket,
        self.txPacket, self.rxBundles, self.txBundles, self.rxDroped, self.txDroped)


class Odu100PeerNodeStatusTable(Base):
    """

    @param odu100_peerNodeStatusTable_id:
    @param host_id:
    @param raIndex:
    @param timeSlotIndex:
    @param linkStatus:
    @param tunnelStatus:
    @param sigStrength1:
    @param peerMacAddr:
    @param ssIdentifier:
    @param peerNodeStatusNumSlaves:
    @param peerNodeStatusrxRate:
    @param peerNodeStatustxRate:
    @param allocatedTxBW:
    @param allocatedRxBW:
    @param usedTxBW:
    @param usedRxBW:
    @param txbasicRate:
    @param sigStrength2:
    @param rxbasicRate:
    @param txLinkQuality:
    @param peerNodeStatustxTime:
    @param peerNodeStatusrxTime:
    @param timestamp:
    """
    __tablename__ = "odu100_peerNodeStatusTable"
    odu100_peerNodeStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INT)
    timeSlotIndex = Column(INT)
    linkStatus = Column(INT)
    tunnelStatus = Column(INT)
    sigStrength1 = Column(INT)
    peerMacAddr = Column(VARCHAR(32))
    ssIdentifier = Column(VARCHAR(32))
    peerNodeStatusNumSlaves = Column(INT)
    peerNodeStatusrxRate = Column(INT)
    peerNodeStatustxRate = Column(INT)
    allocatedTxBW = Column(INT)
    allocatedRxBW = Column(INT)
    usedTxBW = Column(INT)
    usedRxBW = Column(INT)
    txbasicRate = Column(INT)
    sigStrength2 = Column(INT)
    rxbasicRate = Column(INT)
    txLinkQuality = Column(INT)
    peerNodeStatustxTime = Column(INT)
    peerNodeStatusrxTime = Column(INT)
    timestamp = Column(TIMESTAMP)

    def __init__(self, odu100_peerNodeStatusTable_id, host_id, raIndex, timeSlotIndex, linkStatus, tunnelStatus,
                 sigStrength1, peerMacAddr, ssIdentifier, peerNodeStatusNumSlaves, peerNodeStatusrxRate,
                 peerNodeStatustxRate, allocatedTxBW, allocatedRxBW, usedTxBW, usedRxBW, txbasicRate, sigStrength2,
                 rxbasicRate, txLinkQuality, peerNodeStatustxTime, peerNodeStatusrxTime, timestamp):
        self.odu100_peerNodeStatusTable_id = odu100_peerNodeStatusTable_id
        self.host_id = host_id
        self.raIndex = raIndex
        self.timeSlotIndex = timeSlotIndex
        self.linkStatus = linkStatus
        self.tunnelStatus = tunnelStatus
        self.sigStrength1 = sigStrength1
        self.peerMacAddr = peerMacAddr
        self.ssIdentifier = ssIdentifier
        self.peerNodeStatusNumSlaves = peerNodeStatusNumSlaves
        self.peerNodeStatusrxRate = peerNodeStatusrxRate
        self.peerNodeStatustxRate = peerNodeStatustxRate
        self.allocatedTxBW = allocatedTxBW
        self.allocatedRxBW = allocatedRxBW
        self.usedTxBW = usedTxBW
        self.usedRxBW = usedRxBW
        self.txbasicRate = txbasicRate
        self.sigStrength2 = sigStrength2
        self.rxbasicRate = rxbasicRate
        self.txLinkQuality = txLinkQuality
        self.peerNodeStatustxTime = peerNodeStatustxTime
        self.peerNodeStatusrxTime = peerNodeStatusrxTime
        self.timestamp = timestamp

    def __repr__(self):
        return "<Odu100PeerNodeStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_peerNodeStatusTable_id, self.host_id, self.raIndex, self.timeSlotIndex, self.linkStatus,
        self.tunnelStatus, self.sigStrength1, self.peerMacAddr, self.ssIdentifier, self.peerNodeStatusNumSlaves,
        self.peerNodeStatusrxRate, self.peerNodeStatustxRate, self.allocatedTxBW, self.allocatedRxBW, self.usedTxBW,
        self.usedRxBW, self.txbasicRate, self.sigStrength2, self.rxbasicRate, self.txLinkQuality,
        self.peerNodeStatustxTime, self.peerNodeStatusrxTime, self.timestamp)


class Odu100RaAclConfigTable(Base):
    """

    @param config_profile_id:
    @param raIndex:
    @param aclIndex:
    @param macaddress:
    @param rowSts:
    """
    __tablename__ = "odu100_raAclConfigTable"
    odu100_raAclConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    aclIndex = Column(INTEGER)
    macaddress = Column(VARCHAR(32))
    rowSts = Column(INTEGER)

    def __init__(self, config_profile_id, raIndex, aclIndex, macaddress, rowSts):
        self.odu100_raAclConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.aclIndex = aclIndex
        self.macaddress = macaddress
        self.rowSts = rowSts

    def __repr__(self):
        return "<Odu100RaAclCOnfigTable('%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raAclConfigTable_id, self.config_profile_id, self.raIndex, self.aclIndex, self.macaddress,
        self.rowSts)


class Odu100RaChannelListTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param raChanIndex:
    @param channelNumber:
    @param frequency:
    """
    __tablename__ = "odu100_raChannelListTable"
    odu100_raChannelListTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    raChanIndex = Column(INTEGER)
    channelNumber = Column(INTEGER)
    frequency = Column(INTEGER)

    def __init__(self, host_id, raIndex, raChanIndex, channelNumber, frequency):
        self.odu100_raChannelListTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.raChanIndex = raChanIndex
        self.channelNumber = channelNumber
        self.frequency = frequency

    def __repr__(self):
        return "<Odu100RaChannelListTable('%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raChannelListTable_id, self.host_id, self.raIndex, self.raChanIndex, self.channelNumber,
        self.frequency)


class Odu100RaConfTable(Base):
    """

    @param config_profile_id:
    @param raIndex:
    @param raAdminState:
    @param aclMode:
    @param ssID:
    @param guaranteedBroadcastBW:
    @param dba:
    @param acm:
    @param acs:
    @param dfs:
    @param numSlaves:
    @param antennaPort:
    """
    __tablename__ = "odu100_raConfTable"
    odu100_raConfTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    raAdminState = Column(INTEGER)
    aclMode = Column(INTEGER)
    ssID = Column(VARCHAR(32))
    guaranteedBroadcastBW = Column(INTEGER)
    dba = Column(INTEGER)
    acm = Column(INTEGER)
    acs = Column(INTEGER)
    dfs = Column(INTEGER)
    numSlaves = Column(INTEGER)
    antennaPort = Column(INTEGER)

    def __init__(self, config_profile_id, raIndex, raAdminState, aclMode, ssID, guaranteedBroadcastBW, dba, acm, acs,
                 dfs, numSlaves, antennaPort):
        self.odu100_raConfTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.raAdminState = raAdminState
        self.aclMode = aclMode
        self.ssID = ssID
        self.guaranteedBroadcastBW = guaranteedBroadcastBW
        self.dba = dba
        self.acm = acm
        self.acs = acs
        self.dfs = dfs
        self.numSlaves = numSlaves
        self.antennaPort = antennaPort

    def __repr__(self):
        return "<Odu100RaCOnfTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raConfTable_id, self.config_profile_id, self.raIndex, self.raAdminState, self.aclMode, self.ssID,
        self.guaranteedBroadcastBW, self.dba, self.acm, self.acs, self.dfs, self.numSlaves, self.antennaPort)


class Odu100RaLlcConfTable(Base):
    """

    @param config_profile_id:
    @param raIndex:
    @param arqWinLow:
    @param arqWinHigh:
    @param frameLossThreshold:
    @param leakyBucketTimerVal:
    @param frameLossTimeout:
    """
    __tablename__ = "odu100_raLlcConfTable"
    odu100_raLlcConfTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    arqWinLow = Column(INTEGER)
    arqWinHigh = Column(INTEGER)
    frameLossThreshold = Column(INTEGER)
    leakyBucketTimerVal = Column(INTEGER)
    frameLossTimeout = Column(INTEGER)

    def __init__(self, config_profile_id, raIndex, arqWinLow, arqWinHigh, frameLossThreshold, leakyBucketTimerVal,
                 frameLossTimeout):
        self.odu100_raLlcConfTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.arqWinLow = arqWinLow
        self.arqWinHigh = arqWinHigh
        self.frameLossThreshold = frameLossThreshold
        self.leakyBucketTimerVal = leakyBucketTimerVal
        self.frameLossTimeout = frameLossTimeout

    def __repr__(self):
        return "<Odu100RaLlcCOnfTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raLlcConfTable_id, self.config_profile_id, self.raIndex, self.arqWinLow, self.arqWinHigh,
        self.frameLossThreshold, self.leakyBucketTimerVal, self.frameLossTimeout)


class Odu100RaPreferredRFChannelTable(Base):
    """

    @param config_profile_id:
    @param raIndex:
    @param preindex:
    @param rafrequency:
    """
    __tablename__ = "odu100_raPreferredRFChannelTable"
    odu100_raPreferredRFChannelTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    preindex = Column(INTEGER)
    rafrequency = Column(INTEGER)

    def __init__(self, config_profile_id, raIndex, preindex, rafrequency):
        self.odu100_raPreferredRFChannelTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.preindex = preindex
        self.rafrequency = rafrequency

    def __repr__(self):
        return "<Odu100RaPreferredRFChannelTable('%s','%s','%s','%s','%s')>" % (
        self.odu100_raPreferredRFChannelTable_id, self.config_profile_id, self.raIndex, self.preindex, self.rafrequency)


class Odu100RaScanListTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param raScanIndex:
    @param ssid:
    @param signalStrength:
    @param macAddr:
    @param rastertime:
    @param timeslot:
    @param maxSlaves:
    @param channelNum:
    @param basicRate:
    @param radfs:
    @param raacm:
    """
    __tablename__ = "odu100_raScanListTable"
    odu100_raScanListTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    raScanIndex = Column(INTEGER)
    ssid = Column(VARCHAR(32))
    signalStrength = Column(INTEGER)
    macAddr = Column(VARCHAR(32))
    rastertime = Column(INTEGER)
    timeslot = Column(INTEGER)
    maxSlaves = Column(INTEGER)
    channelNum = Column(INTEGER)
    basicRate = Column(INTEGER)
    radfs = Column(INTEGER)
    raacm = Column(INTEGER)

    def __init__(self, host_id, raIndex, raScanIndex, ssid, signalStrength, macAddr, rastertime, timeslot, maxSlaves,
                 channelNum, basicRate, radfs, raacm):
        self.odu100_raScanListTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.raScanIndex = raScanIndex
        self.ssid = ssid
        self.signalStrength = signalStrength
        self.macAddr = macAddr
        self.rastertime = rastertime
        self.timeslot = timeslot
        self.maxSlaves = maxSlaves
        self.channelNum = channelNum
        self.basicRate = basicRate
        self.radfs = radfs
        self.raacm = raacm

    def __repr__(self):
        return "<Odu100RaScanListTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raScanListTable_id, self.host_id, self.raIndex, self.raScanIndex, self.ssid, self.signalStrength,
        self.macAddr, self.rastertime, self.timeslot, self.maxSlaves, self.channelNum, self.basicRate, self.radfs,
        self.raacm)


class Odu100RaSiteSurveyResultTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param scanIndex:
    @param rfChannelFrequency:
    @param numCrcErrors:
    @param maxRslCrcError:
    @param numPhyErrors:
    @param maxRslPhyError:
    @param maxRslValidFrames:
    @param channelnumber:
    @param noiseFloor:
    """
    __tablename__ = "odu100_raSiteSurveyResultTable"
    odu100_raSiteSurveyResultTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    scanIndex = Column(INTEGER)
    rfChannelFrequency = Column(INTEGER)
    numCrcErrors = Column(INTEGER)
    maxRslCrcError = Column(INTEGER)
    numPhyErrors = Column(INTEGER)
    maxRslPhyError = Column(INTEGER)
    maxRslValidFrames = Column(INTEGER)
    channelnumber = Column(INTEGER)
    noiseFloor = Column(INTEGER)

    def __init__(self, host_id, raIndex, scanIndex, rfChannelFrequency, numCrcErrors, maxRslCrcError, numPhyErrors,
                 maxRslPhyError, maxRslValidFrames, channelnumber, noiseFloor):
        self.odu100_raSiteSurveyResultTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.scanIndex = scanIndex
        self.rfChannelFrequency = rfChannelFrequency
        self.numCrcErrors = numCrcErrors
        self.maxRslCrcError = maxRslCrcError
        self.numPhyErrors = numPhyErrors
        self.maxRslPhyError = maxRslPhyError
        self.maxRslValidFrames = maxRslValidFrames
        self.channelnumber = channelnumber
        self.noiseFloor = noiseFloor

    def __repr__(self):
        return "<Odu100RaSiteSurveyResultTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raSiteSurveyResultTable_id, self.host_id, self.raIndex, self.scanIndex, self.rfChannelFrequency,
        self.numCrcErrors, self.maxRslCrcError, self.numPhyErrors, self.maxRslPhyError, self.maxRslValidFrames,
        self.channelnumber, self.noiseFloor)


class Odu100RaStatusTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param currentTimeSlot:
    @param raMacAddress:
    @param raoperationalState:
    @param unusedTxTimeUL:
    @param unusedTxTimeDL:
    """
    __tablename__ = "odu100_raStatusTable"
    odu100_raStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    currentTimeSlot = Column(INTEGER)
    raMacAddress = Column(VARCHAR(32))
    raoperationalState = Column(INTEGER)
    unusedTxTimeUL = Column(INTEGER)
    unusedTxTimeDL = Column(INTEGER)

    def __init__(self, host_id, raIndex, currentTimeSlot, raMacAddress, raoperationalState, unusedTxTimeUL,
                 unusedTxTimeDL):
        self.odu100_raStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.currentTimeSlot = currentTimeSlot
        self.raMacAddress = raMacAddress
        self.raoperationalState = raoperationalState
        self.unusedTxTimeUL = unusedTxTimeUL
        self.unusedTxTimeDL = unusedTxTimeDL

    def __repr__(self):
        return "<Odu100RaStatusTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raStatusTable_id, self.host_id, self.raIndex, self.currentTimeSlot, self.raMacAddress,
        self.raoperationalState, self.unusedTxTimeUL, self.unusedTxTimeDL)


class Odu100RaTddMacConfigTable(Base):
    """

    @param config_profile_id:
    @param raIndex:
    @param passPhrase:
    @param txPower:
    @param maxPower:
    @param maxCrcErrors:
    @param leakyBucketTimerValue:
    @param encryptionType:
    """
    __tablename__ = "odu100_raTddMacConfigTable"
    odu100_raTddMacConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    passPhrase = Column(VARCHAR(64))
    txPower = Column(INTEGER)
    maxPower = Column(INTEGER)
    maxCrcErrors = Column(INTEGER)
    leakyBucketTimerValue = Column(INTEGER)
    encryptionType = Column(INTEGER)

    def __init__(self, config_profile_id, raIndex, passPhrase, txPower, maxPower, maxCrcErrors, leakyBucketTimerValue,
                 encryptionType):
        self.odu100_raTddMacConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.passPhrase = passPhrase
        self.txPower = txPower
        self.maxPower = maxPower
        self.maxCrcErrors = maxCrcErrors
        self.leakyBucketTimerValue = leakyBucketTimerValue
        self.encryptionType = encryptionType

    def __repr__(self):
        return "<Odu100RaTddMacCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raTddMacConfigTable_id, self.config_profile_id, self.raIndex, self.passPhrase, self.txPower,
        self.maxPower, self.maxCrcErrors, self.leakyBucketTimerValue, self.encryptionType)


class Odu100RaTddMacStatisticsTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param rxpackets:
    @param txpackets:
    @param rxerrors:
    @param txerrors:
    @param rxdropped:
    @param txdropped:
    @param rxCrcErrors:
    @param rxPhyError:
    """
    __tablename__ = "odu100_raTddMacStatisticsTable"
    odu100_raTddMacStatisticsTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    rxpackets = Column(INTEGER)
    txpackets = Column(INTEGER)
    rxerrors = Column(INTEGER)
    txerrors = Column(INTEGER)
    rxdropped = Column(INTEGER)
    txdropped = Column(INTEGER)
    rxCrcErrors = Column(INTEGER)
    rxPhyError = Column(INTEGER)

    def __init__(self, host_id, raIndex, rxpackets, txpackets, rxerrors, txerrors, rxdropped, txdropped, rxCrcErrors,
                 rxPhyError):
        self.odu100_raTddMacStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.rxpackets = rxpackets
        self.txpackets = txpackets
        self.rxerrors = rxerrors
        self.txerrors = txerrors
        self.rxdropped = rxdropped
        self.txdropped = txdropped
        self.rxCrcErrors = rxCrcErrors
        self.rxPhyError = rxPhyError

    def __repr__(self):
        return "<Odu100RaTddMacStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raTddMacStatisticsTable_id, self.host_id, self.raIndex, self.rxpackets, self.txpackets,
        self.rxerrors, self.txerrors, self.rxdropped, self.txdropped, self.rxCrcErrors, self.rxPhyError)


class Odu100RaTddMacStatusTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param rfChanFreq:
    """
    __tablename__ = "odu100_raTddMacStatusTable"
    odu100_raTddMacStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    rfChanFreq = Column(INTEGER)

    def __init__(self, host_id, raIndex, rfChanFreq):
        self.odu100_raTddMacStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.rfChanFreq = rfChanFreq

    def __repr__(self):
        return "<Odu100RaTddMacStatusTable('%s','%s','%s','%s')>" % (
        self.odu100_raTddMacStatusTable_id, self.host_id, self.raIndex, self.rfChanFreq)


class Odu100RaValidPhyRatesTable(Base):
    """

    @param host_id:
    @param raIndex:
    @param mcsindex:
    @param spatialStreams:
    @param modulationType:
    @param codingRate:
    @param rate:
    """
    __tablename__ = "odu100_raValidPhyRatesTable"
    odu100_raValidPhyRatesTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    mcsindex = Column(INTEGER)
    spatialStreams = Column(INTEGER)
    modulationType = Column(INTEGER)
    codingRate = Column(INTEGER)
    rate = Column(INTEGER)

    def __init__(self, host_id, raIndex, mcsindex, spatialStreams, modulationType, codingRate, rate):
        self.odu100_raValidPhyRatesTable_id = uuid.uuid1()
        self.host_id = host_id
        self.raIndex = raIndex
        self.mcsindex = mcsindex
        self.spatialStreams = spatialStreams
        self.modulationType = modulationType
        self.codingRate = codingRate
        self.rate = rate

    def __repr__(self):
        return "<Odu100RaValidPhyRatesTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_raValidPhyRatesTable_id, self.host_id, self.raIndex, self.mcsindex, self.spatialStreams,
        self.modulationType, self.codingRate, self.rate)


class Odu100RuConfTable(Base):
    """

    @param config_profile_id:
    @param confIndex:
    @param adminstate:
    @param defaultNodeType:
    @param channelBandwidth:
    @param synchSource:
    @param countryCode:
    @param poeState:
    @param alignmentControl:
    """
    __tablename__ = "odu100_ruConfTable"
    odu100_ruConfTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    confIndex = Column(INTEGER)
    adminstate = Column(INTEGER)
    defaultNodeType = Column(INTEGER)
    channelBandwidth = Column(INTEGER)
    synchSource = Column(INTEGER)
    countryCode = Column(INTEGER)
    poeState = Column(INTEGER)
    alignmentControl = Column(INTEGER)

    def __init__(self, config_profile_id, confIndex, adminstate, defaultNodeType, channelBandwidth, synchSource,
                 countryCode, poeState, alignmentControl):
        self.odu100_ruConfTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.confIndex = confIndex
        self.adminstate = adminstate
        self.defaultNodeType = defaultNodeType
        self.channelBandwidth = channelBandwidth
        self.synchSource = synchSource
        self.countryCode = countryCode
        self.poeState = poeState
        self.alignmentControl = alignmentControl

    def __repr__(self):
        return "<Odu100RuCOnfTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_ruConfTable_id, self.config_profile_id, self.confIndex, self.adminstate, self.defaultNodeType,
        self.channelBandwidth, self.synchSource, self.countryCode, self.poeState, self.alignmentControl)


class Odu100RuDateTimeTable(Base):
    """

    @param config_profile_id:
    @param dateIndex:
    @param year:
    @param month:
    @param day:
    @param hour:
    @param min:
    @param sec:
    """
    __tablename__ = "odu100_ruDateTimeTable"
    odu100_ruDateTimeTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    dateIndex = Column(INTEGER)
    year = Column(INTEGER)
    month = Column(INTEGER)
    day = Column(INTEGER)
    hour = Column(INTEGER)
    min = Column(INTEGER)
    sec = Column(INTEGER)

    def __init__(self, config_profile_id, dateIndex, year, month, day, hour, min, sec):
        self.odu100_ruDateTimeTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.dateIndex = dateIndex
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec

    def __repr__(self):
        return "<Odu100RuDateTimeTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_ruDateTimeTable_id, self.config_profile_id, self.dateIndex, self.year, self.month, self.day,
        self.hour, self.min, self.sec)


class Odu100RuOmOperationsTable(Base):
    """

    @param config_profile_id:
    @param omIndex:
    @param omOperationReq:
    @param userName:
    @param password:
    @param ftpServerAddress:
    @param pathName:
    @param omOperationResult:
    @param omSpecificCause:
    @param listOfChannels:
    @param txTime:
    @param txRate:
    @param txBW:
    """
    __tablename__ = "odu100_ruOmOperationsTable"
    odu100_ruOmOperationsTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    omIndex = Column(INTEGER)
    omOperationReq = Column(INTEGER)
    userName = Column(VARCHAR(16))
    password = Column(VARCHAR(16))
    ftpServerAddress = Column(VARCHAR(32))
    pathName = Column(VARCHAR(128))
    omOperationResult = Column(INTEGER)
    omSpecificCause = Column(INTEGER)
    listOfChannels = Column(VARCHAR(256))
    txTime = Column(INTEGER)
    txRate = Column(INTEGER)
    txBW = Column(INTEGER)

    def __init__(self, config_profile_id, omIndex, omOperationReq, userName, password, ftpServerAddress, pathName,
                 omOperationResult, omSpecificCause, listOfChannels, txTime, txRate, txBW):
        self.odu100_ruOmOperationsTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.omIndex = omIndex
        self.omOperationReq = omOperationReq
        self.userName = userName
        self.password = password
        self.ftpServerAddress = ftpServerAddress
        self.pathName = pathName
        self.omOperationResult = omOperationResult
        self.omSpecificCause = omSpecificCause
        self.listOfChannels = listOfChannels
        self.txTime = txTime
        self.txRate = txRate
        self.txBW = txBW

    def __repr__(self):
        return "<Odu100RuOmOperatiOnsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_ruOmOperationsTable_id, self.config_profile_id, self.omIndex, self.omOperationReq, self.userName,
        self.password, self.ftpServerAddress, self.pathName, self.omOperationResult, self.omSpecificCause,
        self.listOfChannels, self.txTime, self.txRate, self.txBW)


class Odu100RuStatusTable(Base):
    """

    @param host_id:
    @param statusIndex:
    @param lastRebootReason:
    @param isConfigCommitedToFlash:
    @param upTime:
    @param poeStatus:
    @param cpuId:
    @param ruoperationalState:
    """
    __tablename__ = "odu100_ruStatusTable"
    odu100_ruStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    statusIndex = Column(INTEGER)
    lastRebootReason = Column(INTEGER)
    isConfigCommitedToFlash = Column(INTEGER)
    upTime = Column(INTEGER)
    poeStatus = Column(INTEGER)
    cpuId = Column(INTEGER)
    ruoperationalState = Column(INTEGER)

    def __init__(self, host_id, statusIndex, lastRebootReason, isConfigCommitedToFlash, upTime, poeStatus, cpuId,
                 ruoperationalState):
        self.odu100_ruStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.statusIndex = statusIndex
        self.lastRebootReason = lastRebootReason
        self.isConfigCommitedToFlash = isConfigCommitedToFlash
        self.upTime = upTime
        self.poeStatus = poeStatus
        self.cpuId = cpuId
        self.ruoperationalState = ruoperationalState

    def __repr__(self):
        return "<Odu100RuStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_ruStatusTable_id, self.host_id, self.statusIndex, self.lastRebootReason,
        self.isConfigCommitedToFlash, self.upTime, self.poeStatus, self.cpuId, self.ruoperationalState)


class Odu100SwStatusTable(Base):
    """

    @param host_id:
    @param swStatusIndex:
    @param activeVersion:
    @param passiveVersion:
    @param bootloaderVersion:
    """
    __tablename__ = "odu100_swStatusTable"
    odu100_swStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    swStatusIndex = Column(INTEGER)
    activeVersion = Column(VARCHAR(32))
    passiveVersion = Column(VARCHAR(32))
    bootloaderVersion = Column(VARCHAR(64))

    def __init__(self, host_id, swStatusIndex, activeVersion, passiveVersion, bootloaderVersion):
        self.odu100_swStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.swStatusIndex = swStatusIndex
        self.activeVersion = activeVersion
        self.passiveVersion = passiveVersion
        self.bootloaderVersion = bootloaderVersion

    def __repr__(self):
        return "<Odu100SwStatusTable('%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_swStatusTable_id, self.host_id, self.swStatusIndex, self.activeVersion, self.passiveVersion,
        self.bootloaderVersion)


class Odu100SyncConfigTable(Base):
    """

    @param config_profile_id:
    @param syncConfigIndex:
    @param adminStatus:
    @param synchState:
    @param rasterTime:
    @param syncLossThreshold:
    @param leakyBucketTimer:
    @param syncLostTimeout:
    @param syncConfigTimerAdjust:
    @param percentageDownlinkTransmitTime:
    """
    __tablename__ = "odu100_syncConfigTable"
    odu100_syncConfigTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    syncConfigIndex = Column(INTEGER)
    adminStatus = Column(INTEGER)
    synchState = Column(INTEGER)
    rasterTime = Column(INTEGER)
    syncLossThreshold = Column(INTEGER)
    leakyBucketTimer = Column(INTEGER)
    syncLostTimeout = Column(INTEGER)
    syncConfigTimerAdjust = Column(INTEGER)
    percentageDownlinkTransmitTime = Column(INTEGER)

    def __init__(self, config_profile_id, syncConfigIndex, adminStatus, synchState, rasterTime, syncLossThreshold,
                 leakyBucketTimer, syncLostTimeout, syncConfigTimerAdjust, percentageDownlinkTransmitTime):
        self.odu100_syncConfigTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.syncConfigIndex = syncConfigIndex
        self.adminStatus = adminStatus
        self.synchState = synchState
        self.rasterTime = rasterTime
        self.syncLossThreshold = syncLossThreshold
        self.leakyBucketTimer = leakyBucketTimer
        self.syncLostTimeout = syncLostTimeout
        self.syncConfigTimerAdjust = syncConfigTimerAdjust
        self.percentageDownlinkTransmitTime = percentageDownlinkTransmitTime

    def __repr__(self):
        return "<Odu100SyncCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_syncConfigTable_id, self.config_profile_id, self.syncConfigIndex, self.adminStatus, self.synchState,
        self.rasterTime, self.syncLossThreshold, self.leakyBucketTimer, self.syncLostTimeout,
        self.syncConfigTimerAdjust, self.percentageDownlinkTransmitTime)


class Odu100SynchStatisticsTable(Base):
    """

    @param host_id:
    @param syncConfigIndex:
    @param syncLostCounter:
    """
    __tablename__ = "odu100_synchStatisticsTable"
    odu100_synchStatisticsTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    syncConfigIndex = Column(INTEGER)
    syncLostCounter = Column(INTEGER)

    def __init__(self, host_id, syncConfigIndex, syncLostCounter):
        self.odu100_synchStatisticsTable_id = uuid.uuid1()
        self.host_id = host_id
        self.syncConfigIndex = syncConfigIndex
        self.syncLostCounter = syncLostCounter

    def __repr__(self):
        return "<Odu100SynchStatisticsTable('%s','%s','%s','%s')>" % (
        self.odu100_synchStatisticsTable_id, self.host_id, self.syncConfigIndex, self.syncLostCounter)


class Odu100SynchStatusTable(Base):
    """

    @param host_id:
    @param syncConfigIndex:
    @param syncoperationalState:
    @param syncrasterTime:
    @param timerAdjust:
    @param syncpercentageDownlinkTransmitTime:
    """
    __tablename__ = "odu100_synchStatusTable"
    odu100_synchStatusTable_id = Column(VARCHAR(64), primary_key=True)
    host_id = Column(VARCHAR(64), ForeignKey('hosts.host_id'))
    syncConfigIndex = Column(INTEGER)
    syncoperationalState = Column(INTEGER)
    syncrasterTime = Column(INTEGER)
    timerAdjust = Column(INTEGER)
    syncpercentageDownlinkTransmitTime = Column(INTEGER)

    def __init__(self, host_id, syncConfigIndex, syncoperationalState, syncrasterTime, timerAdjust,
                 syncpercentageDownlinkTransmitTime):
        self.odu100_synchStatusTable_id = uuid.uuid1()
        self.host_id = host_id
        self.syncConfigIndex = syncConfigIndex
        self.syncoperationalState = syncoperationalState
        self.syncrasterTime = syncrasterTime
        self.timerAdjust = timerAdjust
        self.syncpercentageDownlinkTransmitTime = syncpercentageDownlinkTransmitTime

    def __repr__(self):
        return "<Odu100SynchStatusTable('%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_synchStatusTable_id, self.host_id, self.syncConfigIndex, self.syncoperationalState,
        self.syncrasterTime, self.timerAdjust, self.syncpercentageDownlinkTransmitTime)


class Odu100SysOmcRegistrationTable(Base):
    """

    @param config_profile_id:
    @param sysOmcRegistrationIndex:
    @param sysOmcRegisterContactAddr:
    @param sysOmcRegisterContactPerson:
    @param sysOmcRegisterContactMobile:
    @param sysOmcRegisterAlternateContact:
    @param sysOmcRegisterContactEmail:
    """
    __tablename__ = "odu100_sysOmcRegistrationTable"
    odu100_sysOmcRegistrationTable_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    sysOmcRegistrationIndex = Column(INTEGER)
    sysOmcRegisterContactAddr = Column(VARCHAR(32))
    sysOmcRegisterContactPerson = Column(VARCHAR(32))
    sysOmcRegisterContactMobile = Column(VARCHAR(32))
    sysOmcRegisterAlternateContact = Column(VARCHAR(32))
    sysOmcRegisterContactEmail = Column(VARCHAR(32))

    def __init__(self, config_profile_id, sysOmcRegistrationIndex, sysOmcRegisterContactAddr,
                 sysOmcRegisterContactPerson, sysOmcRegisterContactMobile, sysOmcRegisterAlternateContact,
                 sysOmcRegisterContactEmail):
        self.odu100_sysOmcRegistrationTable_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.sysOmcRegistrationIndex = sysOmcRegistrationIndex
        self.sysOmcRegisterContactAddr = sysOmcRegisterContactAddr
        self.sysOmcRegisterContactPerson = sysOmcRegisterContactPerson
        self.sysOmcRegisterContactMobile = sysOmcRegisterContactMobile
        self.sysOmcRegisterAlternateContact = sysOmcRegisterAlternateContact
        self.sysOmcRegisterContactEmail = sysOmcRegisterContactEmail

    def __repr__(self):
        return "<Odu100SysOmcRegistratiOnTable('%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.odu100_sysOmcRegistrationTable_id, self.config_profile_id, self.sysOmcRegistrationIndex,
        self.sysOmcRegisterContactAddr, self.sysOmcRegisterContactPerson, self.sysOmcRegisterContactMobile,
        self.sysOmcRegisterAlternateContact, self.sysOmcRegisterContactEmail)


# Oid Database classes ####################

class Oids(Base):
    """

    @param oid_id:
    @param device_type_id:
    @param oid:
    @param oid_name:
    @param oid_type:
    @param access:
    @param default_value:
    @param min_value:
    @param max_value:
    @param indexes:
    @param dependent_id:
    @param multivalue:
    @param table_name:
    @param coloumn_name:
    """
    __tablename__ = "oids"
    oid_id = Column(VARCHAR(64), primary_key=True)
    device_type_id = Column(
        VARCHAR(16), ForeignKey('device_type.device_type_id'))
    oid = Column(VARCHAR(256))
    oid_name = Column(VARCHAR(256))
    oid_type = Column(VARCHAR(16))
    access = Column(SMALLINT)
    default_value = Column(VARCHAR(256))
    min_value = Column(VARCHAR(128))
    max_value = Column(VARCHAR(256))
    indexes = Column(VARCHAR(256))
    dependent_id = Column(VARCHAR(64), ForeignKey('oids.oid_id'))
    multivalue = Column(SMALLINT)
    table_name = Column(VARCHAR(128))
    coloumn_name = Column(VARCHAR(128))

    def __init__(self, oid_id, device_type_id, oid, oid_name, oid_type, access, default_value, min_value, max_value,
                 indexes, dependent_id, multivalue, table_name, coloumn_name):
        self.oid_id = oid_id
        self.device_type_id = device_type_id
        self.oid = oid
        self.oid_name = oid_name
        self.oid_type = oid_type
        self.access = access
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.indexes = indexes
        self.dependent_id = dependent_id
        self.multivalue = multivalue
        self.table_name = table_name
        self.coloumn_name = coloumn_name

    def __repr__(self):
        return "<Oids('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.oid_id, self.device_type_id, self.oid, self.oid_name, self.oid_type, self.access, self.default_value,
        self.min_value, self.max_value, self.indexes, self.dependent_id, self.multivalue, self.table_name,
        self.coloumn_name)


class OidsMultivalues(Base):
    """

    @param oids_multivalue_id:
    @param oid_id:
    @param value:
    @param name:
    """
    __tablename__ = "oids_multivalues"
    oids_multivalue_id = Column(VARCHAR(64), primary_key=True)
    oid_id = Column(VARCHAR(64), ForeignKey('oids.oid_id'))
    value = Column(VARCHAR(128))
    name = Column(VARCHAR(128))

    def __init__(self, oids_multivalue_id, oid_id, value, name):
        self.oids_multivalue_id = oids_multivalue_id
        self.oid_id = oid_id
        self.value = value
        self.name = name

    def __repr__(self):
        return "<OidsMultivalues('%s','%s','%s','%s')>" % (self.oids_multivalue_id, self.oid_id, self.value, self.name)


class NmsGraphs(Base):
    """

    @param device_type_id:
    @param tablename:
    @param is_deleted:
    """
    __tablename__ = "nms_graphs"
    nms_graphs_id = Column(VARCHAR(64), primary_key=True)
    device_type_id = Column(
        VARCHAR(16), ForeignKey('device_type.device_type_id'))
    tablename = Column(VARCHAR(64))
    is_deleted = Column(SMALLINT(6))

    def __init__(self, device_type_id, tablename, is_deleted):
        self.nms_graphs_id = uuid.uuid1()
        self.device_type_id = device_type_id
        self.tablename = tablename
        self.is_deleted = is_deleted

    def __repr__(self):
        return "<NmsGraphs('%s','%s','%s','%s')>" % (
        self.nms_graphs_id, self.device_type_id, self.tablename, self.is_deleted)


class TrapAlarms(Base):
    """

    @param trap_alarm_id:
    @param event_id:
    @param trap_id:
    @param agent_id:
    @param trap_date:
    @param trap_receive_date:
    @param serevity:
    @param trap_event_id:
    @param trap_event_type:
    @param manage_obj_id:
    @param manage_obj_name:
    @param component_id:
    @param trap_ip:
    @param description:
    @param timestamp:
    """
    __tablename__ = "trap_alarms"
    trap_alarm_id = Column(VARCHAR(64), primary_key=True)
    event_id = Column(VARCHAR(32))
    trap_id = Column(VARCHAR(32))
    agent_id = Column(VARCHAR(32))
    trap_date = Column(VARCHAR(32))
    trap_receive_date = Column(VARCHAR(32))
    serevity = Column(INT)
    trap_event_id = Column(VARCHAR(32))
    trap_event_type = Column(VARCHAR(32))
    manage_obj_id = Column(VARCHAR(32))
    manage_obj_name = Column(VARCHAR(32))
    component_id = Column(VARCHAR(32))
    trap_ip = Column(VARCHAR(32))
    description = Column(VARCHAR(256))
    timestamp = Column(TIMESTAMP)

    def __init__(self, trap_alarm_id, event_id, trap_id, agent_id, trap_date, trap_receive_date, serevity,
                 trap_event_id, trap_event_type, manage_obj_id, manage_obj_name, component_id, trap_ip, description,
                 timestamp):
        self.trap_alarm_id = trap_alarm_id
        self.event_id = event_id
        self.trap_id = trap_id
        self.agent_id = agent_id
        self.trap_date = trap_date
        self.trap_receive_date = trap_receive_date
        self.serevity = serevity
        self.trap_event_id = trap_event_id
        self.trap_event_type = trap_event_type
        self.manage_obj_id = manage_obj_id
        self.manage_obj_name = manage_obj_name
        self.component_id = component_id
        self.trap_ip = trap_ip
        self.description = description
        self.timestamp = timestamp

    def __repr__(self):
        return "<TrapAlarms('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (
        self.trap_alarm_id, self.event_id, self.trap_id, self.agent_id, self.trap_date, self.trap_receive_date,
        self.serevity, self.trap_event_id, self.trap_event_type, self.manage_obj_id, self.manage_obj_name,
        self.component_id, self.trap_ip, self.description, self.timestamp)

###################################### SWITCH MODEL CREATED HERE #########


class Swt4BandwidthControl(Base):
    """

    @param config_profile_id:
    @param cpu_protection:
    @param port:
    @param type:
    @param state:
    @param rate:
    """
    __tablename__ = "swt4_bandwidth_control"
    switch_bandwidth_control_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    cpu_protection = Column(INT)
    port = Column(TINYINT)
    type = Column(TINYINT)
    state = Column(TINYINT)
    rate = Column(INT)

    def __init__(self, config_profile_id, cpu_protection, port, type, state, rate):
        self.switch_bandwidth_control_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.cpu_protection = cpu_protection
        self.port = port
        self.type = type
        self.state = state
        self.rate = rate

    def __repr__(self):
        return "<Swt4Bandwidth_control('%s','%s','%s','%s','%s','%s','%s')>" % (
        self.switch_bandwidth_control_id, self.config_profile_id, self.cpu_protection, self.port, self.type, self.state,
        self.rate)


class Swt4StormControl(Base):
    """

    @param config_profile_id:
    @param strom_type:
    @param state:
    @param rate:
    """
    __tablename__ = "swt4_storm_control"
    switch_storm_control_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    strom_type = Column(TINYINT(4))
    state = Column(TINYINT(4))
    rate = Column(TINYINT(4))

    def __init__(self, config_profile_id, strom_type, state, rate):
        self.switch_storm_control_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.strom_type = strom_type
        self.state = state
        self.rate = rate

    def __repr__(self):
        return "<Swt4Storm_control('%s','%s','%s','%s','%s')>" % (
        self.switch_storm_control_id, self.config_profile_id, self.strom_type, self.state, self.rate)


class Swt4PortStatistics(Base):
    """

    @param config_profile_id:
    @param port:
    @param state:
    @param speed:
    @param flow_control:
    """
    __tablename__ = "swt4_port_statistics"
    switch_port_statistics_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    port = Column(TINYINT)
    state = Column(TINYINT)
    speed = Column(TINYINT)
    flow_control = Column(TINYINT)

    def __init__(self, config_profile_id, port, state, speed, flow_control):
        self.switch_port_statistics_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.port = port
        self.state = state
        self.speed = speed
        self.flow_control = flow_control

    def __repr__(self):
        return "<Swt4Port_statistics('%s','%s','%s','%s','%s','%s')>" % (
        self.switch_port_statistics_id, self.config_profile_id, self.port, self.state, self.speed, self.flow_control)


class Swt4PortSettings(Base):
    """

    @param config_profile_id:
    @param link_fault_pass_through:
    @param port:
    @param state:
    @param speed:
    @param flow_control:
    """
    __tablename__ = "swt4_port_settings"
    swt4_port_settings_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    link_fault_pass_through = Column(SMALLINT)
    port = Column(SMALLINT)
    state = Column(SMALLINT)
    speed = Column(SMALLINT)
    flow_control = Column(SMALLINT)

    def __init__(self, config_profile_id, link_fault_pass_through, port, state, speed, flow_control):
        self.swt4_port_settings_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.link_fault_pass_through = link_fault_pass_through
        self.port = port
        self.state = state
        self.speed = speed
        self.flow_control = flow_control

    def __repr__(self):
        return "<Swt4Port_settings('%s','%s','%s','%s','%s','%s','%s')>" % (
        self.swt4_port_settings_id, self.config_profile_id, self.link_fault_pass_through, self.port, self.state,
        self.speed, self.flow_control)


class Swt4IpSettings(Base):
    """

    @param config_profile_id:
    @param mode:
    @param ip_address:
    @param subnet_mask:
    @param gateway:
    """
    __tablename__ = "swt4_ip_settings"
    switch_ip_settings_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    mode = Column(VARCHAR(12))
    ip_address = Column(VARCHAR(15))
    subnet_mask = Column(VARCHAR(15))
    gateway = Column(VARCHAR(15))

    def __init__(self, config_profile_id, mode, ip_address, subnet_mask, gateway):
        self.switch_ip_settings_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.mode = mode
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.gateway = gateway

    def __repr__(self):
        return "<Swt4IpSettings('%s','%s','%s','%s','%s','%s')>" % (
        self.switch_ip_settings_id, self.config_profile_id, self.mode, self.ip_address, self.subnet_mask, self.gateway)


class Swt4VlanSettings(Base):
    """

    @param config_profile_id:
    @param vlan_ingress_filter:
    @param vlan_pass_all:
    @param port:
    @param pvid:
    @param mode:
    """
    __tablename__ = "swt4_vlan_settings"
    swt4_vlan_settings_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    vlan_ingress_filter = Column(SMALLINT)
    vlan_pass_all = Column(SMALLINT)
    port = Column(SMALLINT)
    pvid = Column(SMALLINT)
    mode = Column(SMALLINT)

    def __init__(self, config_profile_id, vlan_ingress_filter, vlan_pass_all, port, pvid, mode):
        self.swt4_vlan_settings_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.vlan_ingress_filter = vlan_ingress_filter
        self.vlan_pass_all = vlan_pass_all
        self.port = port
        self.pvid = pvid
        self.mode = mode

    def __repr__(self):
        return "<Swt4VlanSettings('%s','%s','%s','%s','%s','%s','%s')>" % (
        self.swt4_vlan_settings_id, self.config_profile_id, self.vlan_ingress_filter, self.vlan_pass_all, self.port,
        self.pvid, self.mode)


class Swt4PortBasedPriority(Base):
    """

    @param config_profile_id:
    @param port:
    @param priority:
    """
    __tablename__ = "swt4_port_based_priority"
    switch_port_based_priority_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    port = Column(TINYINT)
    priority = Column(TINYINT)

    def __init__(self, config_profile_id, port, priority):
        self.switch_port_based_priority_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.port = port
        self.priority = priority

    def __repr__(self):
        return "<Swt4PortBasedPriority('%s','%s','%s','%s')>" % (
        self.switch_port_based_priority_id, self.config_profile_id, self.port, self.priority)


class Swt4DscpBasedPriority(Base):
    """

    @param switch_dscp_based_priority_id:
    @param config_profile_id:
    @param dscp:
    @param priority:
    """
    __tablename__ = "swt4_dscp_based_priority"
    switch_dscp_based_priority_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    dscp = Column(VARCHAR(8))
    priority = Column(TINYINT)

    def __init__(self, switch_dscp_based_priority_id, config_profile_id, dscp, priority):
        self.switch_dscp_based_priority_id = switch_dscp_based_priority_id
        self.config_profile_id = config_profile_id
        self.dscp = dscp
        self.priority = priority

    def __repr__(self):
        return "<Swt4DscpBasedPriority('%s','%s','%s','%s')>" % (
        self.switch_dscp_based_priority_id, self.config_profile_id, self.dscp, self.priority)


class Swt48021pBasedPriority(Base):
    """

    @param config_profile_id:
    @param p802:
    @param priority:
    """
    __tablename__ = "swt4_802_1p_based_priority"
    switch_802_1p_based_priority_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    p802 = Column(TINYINT)
    priority = Column(TINYINT)

    def __init__(self, config_profile_id, p802, priority):
        self.switch_802_1p_based_priority_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.p802 = p802
        self.priority = priority

    def __repr__(self):
        return "<Swt48021pBasedPriority('%s','%s','%s','%s')>" % (
        self.switch_802_1p_based_priority_id, self.config_profile_id, self.p802, self.priority)


class Swt4IpBasePriority(Base):
    """

    @param config_profile_id:
    @param ip_base_priority:
    @param ip_type:
    @param ip_address:
    @param network_mask:
    @param priority:
    """
    __tablename__ = "swt4_ip_base_priority"
    swt4_ip_base_priority_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    ip_base_priority = Column(INT)
    ip_type = Column(INT)
    ip_address = Column(VARCHAR(15))
    network_mask = Column(VARCHAR(15))
    priority = Column(INT)

    def __init__(self, config_profile_id, ip_base_priority, ip_type, ip_address, network_mask, priority):
        self.swt4_ip_base_priority_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.ip_base_priority = ip_base_priority
        self.ip_type = ip_type
        self.ip_address = ip_address
        self.network_mask = network_mask
        self.priority = priority

    def __repr__(self):
        return "<Swt4IpBasePriority('%s','%s','%s','%s','%s','%s','%s')>" % (
        self.swt4_ip_base_priority_id, self.config_profile_id, self.ip_base_priority, self.ip_type, self.ip_address,
        self.network_mask, self.priority)


class Swt4QueueBasedPriority(Base):
    """

    @param config_profile_id:
    @param qid_map:
    @param priority:
    """
    __tablename__ = "swt4_queue_based_priority"
    switch_queue_based_priority_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    qid_map = Column(TINYINT)
    priority = Column(TINYINT)

    def __init__(self, config_profile_id, qid_map, priority):
        self.switch_queue_based_priority_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.qid_map = qid_map
        self.priority = priority

    def __repr__(self):
        return "<Swt4QueueBasedPriority('%s','%s','%s','%s')>" % (
        self.switch_queue_based_priority_id, self.config_profile_id, self.qid_map, self.priority)


class Swt4QueueWeightBased(Base):
    """

    @param config_profile_id:
    @param queue:
    @param weight:
    """
    __tablename__ = "swt4_queue_weight_based"
    switch_queue_weight_based = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    queue = Column(TINYINT)
    weight = Column(TINYINT)

    def __init__(self, config_profile_id, queue, weight):
        self.switch_queue_weight_based = switch_queue_weight_based
        self.config_profile_id = config_profile_id
        self.queue = queue
        self.weight = weight

    def __repr__(self):
        return "<Swt4QueueWeightBased('%s','%s','%s','%s')>" % (
        self.switch_queue_weight_based, self.config_profile_id, self.queue, self.weight)


class Swt4QosArbitration(Base):
    """

    @param config_profile_id:
    @param priority:
    @param level:
    """
    __tablename__ = "swt4_qos_arbitration"
    switch_qos_arbitration_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    priority = Column(VARCHAR(15))
    level = Column(TINYINT)

    def __init__(self, config_profile_id, priority, level):
        self.switch_qos_arbitration_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.priority = priority
        self.level = level

    def __repr__(self):
        return "<Swt4QosArbitration('%s','%s','%s','%s')>" % (
        self.switch_qos_arbitration_id, self.config_profile_id, self.priority, self.level)


class Swt41pRemarking(Base):
    """

    @param config_profile_id:
    @param p_remarking:
    @param p802_remarking:
    """
    __tablename__ = "swt4_1p_remarking"
    switch_1p_remarking_id = Column(VARCHAR(64), primary_key=True)
    config_profile_id = Column(
        VARCHAR(64), ForeignKey('config_profiles.config_profile_id'))
    p_remarking = Column(TINYINT)
    p802_remarking = Column(TINYINT)

    def __init__(self, config_profile_id, p_remarking, p802_remarking):
        self.switch_1p_remarking_id = uuid.uuid1()
        self.config_profile_id = config_profile_id
        self.p_remarking = p_remarking
        self.p802_remarking = p802_remarking

    def __repr__(self):
        return "<Swt41pRemarking('%s','%s','%s','%s')>" % (
        self.switch_1p_remarking_id, self.config_profile_id, self.p_remarking, self.p802_remarking)


###################################### SWITCH MODEL ENDS HERE ############
###############################################################################
#----------------------Clear Mapping-------------------------------------------
clear_mappers()

#----------------------Define Mapping------------------------------------------

mapper(TrapAlarms, TrapAlarms.__table__)

#---------------------Mapping For DeviceType-----------------------------------
device_type_table = DeviceType.__table__
mapper(
    DeviceType, device_type_table,
    properties={'hosts': relationship(Hosts, backref='device_type', cascade="all, delete, delete-orphan"),
                'config_profiles': relationship(Odu16ConfigProfiles, backref='device_type',
                                                cascade="all, delete, delete-orphan"),
                'nms_graphs': relationship(NmsGraphs, backref='device_type', cascade="all,delete,delete-orphan")})

#-------------------Mapping For ConfigProfileType
config_profile_type_table = ConfigProfileType.__table__
mapper(ConfigProfileType, config_profile_type_table, properties={'config_profiles': relationship(
    Odu16ConfigProfiles, backref='config_profile', cascade="all, delete, delete-orphan")})

#-----------------------Mapper for HostAssets---------------
mapper(HostAssets, HostAssets.__table__)


#-----------------Mapping For ODU16IPConfig------------------------------------
odu_ip_config_table = SetOdu16IPConfigTable.__table__
mapper(SetOdu16IPConfigTable, odu_ip_config_table)

#-----------------Mapping For ODU16NetworkInterface-----------------------
odu_ip_config_table = SetOdu16NetworkInterfaceConfig.__table__
mapper(SetOdu16NetworkInterfaceConfig, odu_ip_config_table)

#-----------------Mapping For ODU16OmcConfTable---------------------------
odu_omc_conf_table = SetOdu16OmcConfTable.__table__
mapper(SetOdu16OmcConfTable, odu_omc_conf_table)

#-----------------Mapping For ODU16PeerConfigTable------------------------
odu_peer_config_table = SetOdu16PeerConfigTable.__table__
mapper(SetOdu16PeerConfigTable, odu_peer_config_table)

#-----------------Mapping For ODU16RAAclConfigTable-----------------------
odu_ra_acl_config_table = SetOdu16RAAclConfigTable.__table__
mapper(SetOdu16RAAclConfigTable, odu_ra_acl_config_table)

#-----------------Mapping For ODU16OmOperationsTable----------------------
odu_om_operations__table = SetOdu16OmOperationsTable.__table__
mapper(SetOdu16OmOperationsTable, odu_om_operations__table)

#-----------------Mapping For ODU16RAConfTable----------------------------
odu_ra_conf__table = SetOdu16RAConfTable.__table__
mapper(SetOdu16RAConfTable, odu_ra_conf__table)

#-----------------Mapping For ODU16RALlcConfTable-------------------------
odu_ra_llc_conf_table = SetOdu16RALlcConfTable.__table__
mapper(SetOdu16RALlcConfTable, odu_ra_llc_conf_table)

#-----------------Mapping For ODU16RATddMacConfig-------------------------
odu_ra_tdd_mac_config_table = SetOdu16RATddMacConfig.__table__
mapper(SetOdu16RATddMacConfig, odu_ra_tdd_mac_config_table)


#-----------------Mapping For ODU16RUConfTable----------------------------
odu_ru_conf_table = SetOdu16RUConfTable.__table__
mapper(SetOdu16RUConfTable, odu_ru_conf_table)

#-----------------Mapping For ODU16RUDateTimeTable------------------------
odu_ru_date_time_table = SetOdu16RUDateTimeTable.__table__
mapper(SetOdu16RUDateTimeTable, odu_ru_date_time_table)

#-----------------Mapping For ODU16SyncConfigTable------------------------
odu_sync_config_table = SetOdu16SyncConfigTable.__table__
mapper(SetOdu16SyncConfigTable, odu_sync_config_table)


#-----------------Mapping For ODU16Misc------------------------------------
odu_misc_table = SetOdu16Misc.__table__
mapper(SetOdu16Misc, odu_misc_table)

#-----------------Mapping For Odu16SysOmcReguistrationTable--------------------
odu_sys_registration_table = SetOdu16SysOmcRegistrationTable.__table__

#---------------Mapping for GetOdu16_ru_conf_tables
mapper(GetOdu16_ru_conf_table, GetOdu16_ru_conf_table.__table__)

#-----------------Mapping for odu100--------------------
mapper(SetOdu16SysOmcRegistrationTable, odu_sys_registration_table)

mapper(Odu100EswATUConfigTable, Odu100EswATUConfigTable.__table__)

mapper(Odu100EswBadFramesTable, Odu100EswBadFramesTable.__table__)

mapper(Odu100EswGoodFramesTable, Odu100EswGoodFramesTable.__table__)

mapper(Odu100EswMirroringPortTable, Odu100EswMirroringPortTable.__table__)

mapper(Odu100EswPortAccessListTable, Odu100EswPortAccessListTable.__table__)

mapper(Odu100EswPortBwTable, Odu100EswPortBwTable.__table__)

mapper(Odu100EswPortConfigTable, Odu100EswPortConfigTable.__table__)

mapper(Odu100EswPortQinQTable, Odu100EswPortQinQTable.__table__)

mapper(Odu100EswPortStatisticsTable, Odu100EswPortStatisticsTable.__table__)

mapper(Odu100EswPortStatusTable, Odu100EswPortStatusTable.__table__)

mapper(Odu100EswVlanConfigTable, Odu100EswVlanConfigTable.__table__)

mapper(Odu100HwDescTable, Odu100HwDescTable.__table__)

mapper(Odu100IpConfigTable, Odu100IpConfigTable.__table__)

mapper(Odu100NwInterfaceStatisticsTable,
       Odu100NwInterfaceStatisticsTable.__table__)

mapper(Odu100NwInterfaceStatusTable, Odu100NwInterfaceStatusTable.__table__)

mapper(Odu100OmcConfTable, Odu100OmcConfTable.__table__)

mapper(Odu100PeerConfigTable, Odu100PeerConfigTable.__table__)

mapper(Odu100PeerLinkStatisticsTable, Odu100PeerLinkStatisticsTable.__table__)

mapper(Odu100PeerNodeStatusTable, Odu100PeerNodeStatusTable.__table__)

mapper(Odu100PeerRateStatisticsTable, Odu100PeerRateStatisticsTable.__table__)

mapper(Odu100PeerTunnelStatisticsTable,
       Odu100PeerTunnelStatisticsTable.__table__)

mapper(Odu100RaAclConfigTable, Odu100RaAclConfigTable.__table__)

mapper(Odu100RaChannelListTable, Odu100RaChannelListTable.__table__)

mapper(Odu100RaConfTable, Odu100RaConfTable.__table__)

mapper(Odu100RaLlcConfTable, Odu100RaLlcConfTable.__table__)

mapper(Odu100RaPreferredRFChannelTable,
       Odu100RaPreferredRFChannelTable.__table__)

mapper(Odu100RaScanListTable, Odu100RaScanListTable.__table__)

mapper(Odu100RaSiteSurveyResultTable, Odu100RaSiteSurveyResultTable.__table__)

mapper(Odu100RaStatusTable, Odu100RaStatusTable.__table__)

mapper(Odu100RaTddMacConfigTable, Odu100RaTddMacConfigTable.__table__)

mapper(Odu100RaTddMacStatisticsTable, Odu100RaTddMacStatisticsTable.__table__)

mapper(Odu100RaTddMacStatusTable, Odu100RaTddMacStatusTable.__table__)

mapper(Odu100RaValidPhyRatesTable, Odu100RaValidPhyRatesTable.__table__)

mapper(Odu100RuConfTable, Odu100RuConfTable.__table__)

mapper(Odu100RuDateTimeTable, Odu100RuDateTimeTable.__table__)

mapper(Odu100RuOmOperationsTable, Odu100RuOmOperationsTable.__table__)

mapper(Odu100RuStatusTable, Odu100RuStatusTable.__table__)

mapper(Odu100SwStatusTable, Odu100SwStatusTable.__table__)

mapper(Odu100SyncConfigTable, Odu100SyncConfigTable.__table__)

mapper(Odu100SynchStatisticsTable, Odu100SynchStatisticsTable.__table__)

mapper(Odu100SynchStatusTable, Odu100SynchStatusTable.__table__)

mapper(Odu100SysOmcRegistrationTable, Odu100SysOmcRegistrationTable.__table__)

mapper(OidsMultivalues, OidsMultivalues.__table__)

mapper(NmsGraphs, NmsGraphs.__table__)
################### oid mappers ###############################################

mapper(Oids, Oids.__table__, properties={'oids_multivalues': relationship(
    OidsMultivalues, backref="oids", cascade="all,delete,delete-orphan")})

mapper(GetOdu16PeerNodeStatusTable, GetOdu16PeerNodeStatusTable.__table__)


# SWITCH MAPPING START HERE ##############################################

mapper(Swt4BandwidthControl, Swt4BandwidthControl.__table__)
mapper(Swt4StormControl, Swt4StormControl.__table__)
mapper(Swt4PortStatistics, Swt4PortStatistics.__table__)
mapper(Swt4PortSettings, Swt4PortSettings.__table__)
mapper(Swt4IpSettings, Swt4IpSettings.__table__)
mapper(Swt4VlanSettings, Swt4VlanSettings.__table__)
mapper(Swt4PortBasedPriority, Swt4PortBasedPriority.__table__)
mapper(Swt4DscpBasedPriority, Swt4DscpBasedPriority.__table__)
mapper(Swt48021pBasedPriority, Swt48021pBasedPriority.__table__)
mapper(Swt4IpBasePriority, Swt4IpBasePriority.__table__)
mapper(Swt4QueueBasedPriority, Swt4QueueBasedPriority.__table__)
mapper(Swt4QueueWeightBased, Swt4QueueWeightBased.__table__)
mapper(Swt4QosArbitration, Swt4QosArbitration.__table__)
mapper(Swt41pRemarking, Swt41pRemarking.__table__)


# SWITCH MAPPING ENDS HERE ###############################################


# Mappers ##########################################
#--------------------Mapping For Host------------------------------------------
host_table = Hosts.__table__
mapper(
    Hosts, host_table, properties={'odu100_eswBadFramesTable': relationship(Odu100EswBadFramesTable, backref="hosts",
                                                                            cascade="all,delete,delete-orphan"),
                                   'odu100_eswGoodFramesTable': relationship(Odu100EswGoodFramesTable, backref="hosts",
                                                                             cascade="all,delete,delete-orphan"),
                                   'odu100_eswPortStatisticsTable': relationship(Odu100EswPortStatisticsTable,
                                                                                 backref="hosts",
                                                                                 cascade="all,delete,delete-orphan"),
                                   'odu100_eswPortStatusTable': relationship(Odu100EswPortStatusTable, backref="hosts",
                                                                             cascade="all,delete,delete-orphan"),
                                   'odu100_hwDescTable': relationship(Odu100HwDescTable, backref="hosts",
                                                                      cascade="all,delete,delete-orphan"),
                                   'odu100_nwInterfaceStatisticsTable': relationship(Odu100NwInterfaceStatisticsTable,
                                                                                     backref="hosts",
                                                                                     cascade="all,delete,delete-orphan"),
                                   'odu100_nwInterfaceStatusTable': relationship(Odu100NwInterfaceStatusTable,
                                                                                 backref="hosts",
                                                                                 cascade="all,delete,delete-orphan"),
                                   'odu100_peerLinkStatisticsTable': relationship(Odu100PeerLinkStatisticsTable,
                                                                                  backref="hosts",
                                                                                  cascade="all,delete,delete-orphan"),
                                   'odu100_peerNodeStatusTable': relationship(Odu100PeerNodeStatusTable,
                                                                              backref="hosts",
                                                                              cascade="all,delete,delete-orphan"),
                                   'odu100_peerRateStatisticsTable': relationship(Odu100PeerRateStatisticsTable,
                                                                                  backref="hosts",
                                                                                  cascade="all,delete,delete-orphan"),
                                   'odu100_peerTunnelStatisticsTable': relationship(Odu100PeerTunnelStatisticsTable,
                                                                                    backref="hosts",
                                                                                    cascade="all,delete,delete-orphan"),
                                   'odu100_raChannelListTable': relationship(Odu100RaChannelListTable, backref="hosts",
                                                                             cascade="all,delete,delete-orphan"),
                                   'odu100_raScanListTable': relationship(Odu100RaScanListTable, backref="hosts",
                                                                          cascade="all,delete,delete-orphan"),
                                   'odu100_raSiteSurveyResultTable': relationship(Odu100RaSiteSurveyResultTable,
                                                                                  backref="hosts",
                                                                                  cascade="all,delete,delete-orphan"),
                                   'odu100_raStatusTable': relationship(Odu100RaStatusTable, backref="hosts",
                                                                        cascade="all,delete,delete-orphan"),
                                   'odu100_raTddMacStatisticsTable': relationship(Odu100RaTddMacStatisticsTable,
                                                                                  backref="hosts",
                                                                                  cascade="all,delete,delete-orphan"),
                                   'odu100_raTddMacStatusTable': relationship(Odu100RaTddMacStatusTable,
                                                                              backref="hosts",
                                                                              cascade="all,delete,delete-orphan"),
                                   'odu100_raValidPhyRatesTable': relationship(Odu100RaValidPhyRatesTable,
                                                                               backref="hosts",
                                                                               cascade="all,delete,delete-orphan"),
                                   'odu100_ruStatusTable': relationship(Odu100RuStatusTable, backref="hosts",
                                                                        cascade="all,delete,delete-orphan"),
                                   'odu100_swStatusTable': relationship(Odu100SwStatusTable, backref="hosts",
                                                                        cascade="all,delete,delete-orphan"),
                                   'odu100_synchStatisticsTable': relationship(Odu100SynchStatisticsTable,
                                                                               backref="hosts",
                                                                               cascade="all,delete,delete-orphan"),
                                   'odu100_synchStatusTable': relationship(Odu100SynchStatusTable, backref="hosts",
                                                                           cascade="all,delete,delete-orphan"),
                                   'get_odu16_ru_conf_table': relationship(GetOdu16_ru_conf_table, backref="hosts",
                                                                           cascade="all,delete,delete-orphan"),
                                   'get_odu16_peer_node_status_table': relationship(GetOdu16PeerNodeStatusTable,
                                                                                    backref="hosts",
                                                                                    cascade="all,delete,delete-orphan")
    })

tablename = Odu16ConfigProfiles.__table__
mapper(
    Odu16ConfigProfiles, tablename, properties={
    'set_odu16_ip_config_table': relationship(SetOdu16IPConfigTable, backref="config_profiles",
                                              cascade="all,delete,delete-orphan"),
    'set_odu16_network_interface_config': relationship(SetOdu16NetworkInterfaceConfig, backref="config_profiles",
                                                       cascade="all,delete,delete-orphan"),
    'set_odu16_omc_conf_table': relationship(SetOdu16OmcConfTable, backref="config_profiles",
                                             cascade="all,delete,delete-orphan"),
    'set_odu16_peer_config_table': relationship(SetOdu16PeerConfigTable, backref="config_profiles",
                                                cascade="all,delete,delete-orphan"),
    'set_odu16_ra_acl_config_table': relationship(SetOdu16RAAclConfigTable, backref="config_profiles",
                                                  cascade="all,delete,delete-orphan"),
    'set_odu16_om_operations_table': relationship(SetOdu16OmOperationsTable, backref="config_profiles",
                                                  cascade="all,delete,delete-orphan"),
    'set_odu16_ra_conf_table': relationship(SetOdu16RAConfTable, backref="config_profiles",
                                            cascade="all,delete,delete-orphan"),
    'set_odu16_ra_llc_conf_table': relationship(SetOdu16RALlcConfTable, backref="config_profiles",
                                                cascade="all,delete,delete-orphan"),
    'set_odu16_ra_tdd_mac_config': relationship(SetOdu16RATddMacConfig, backref="config_profiles",
                                                cascade="all,delete,delete-orphan"),
    'set_odu16_ru_conf_table': relationship(SetOdu16RUConfTable, backref="config_profiles",
                                            cascade="all,delete,delete-orphan"),
    'set_odu16_ru_date_time_table': relationship(SetOdu16RUDateTimeTable, backref="config_profiles",
                                                 cascade="all,delete,delete-orphan"),
    'set_odu16_sync_config_table': relationship(SetOdu16SyncConfigTable, backref="config_profiles",
                                                cascade="all,delete,delete-orphan"),
    'set_odu16_misc': relationship(SetOdu16Misc, backref="config_profiles", cascade="all,delete,delete-orphan"),
    'set_odu16_sys_omc_registration_table': relationship(SetOdu16SysOmcRegistrationTable, backref="config_profiles",
                                                         cascade="all,delete,delete-orphan"),
    'odu100_eswATUConfigTable': relationship(Odu100EswATUConfigTable, backref="config_profiles",
                                             cascade="all,delete,delete-orphan"),
    'odu100_eswMirroringPortTable': relationship(Odu100EswMirroringPortTable, backref="config_profiles",
                                                 cascade="all,delete,delete-orphan"),
    'odu100_eswPortAccessListTable': relationship(Odu100EswPortAccessListTable, backref="config_profiles",
                                                  cascade="all,delete,delete-orphan"),
    'odu100_eswPortBwTable': relationship(Odu100EswPortBwTable, backref="config_profiles",
                                          cascade="all,delete,delete-orphan"),
    'odu100_eswPortConfigTable': relationship(Odu100EswPortConfigTable, backref="config_profiles",
                                              cascade="all,delete,delete-orphan"),
    'odu100_eswPortQinQTable': relationship(Odu100EswPortQinQTable, backref="config_profiles",
                                            cascade="all,delete,delete-orphan"),
    'odu100_eswVlanConfigTable': relationship(Odu100EswVlanConfigTable, backref="config_profiles",
                                              cascade="all,delete,delete-orphan"),
    'odu100_ipConfigTable': relationship(Odu100IpConfigTable, backref="config_profiles",
                                         cascade="all,delete,delete-orphan"),
    'odu100_omcConfTable': relationship(Odu100OmcConfTable, backref="config_profiles",
                                        cascade="all,delete,delete-orphan"),
    'odu100_peerConfigTable': relationship(Odu100PeerConfigTable, backref="config_profiles",
                                           cascade="all,delete,delete-orphan"),
    'odu100_raAclConfigTable': relationship(Odu100RaAclConfigTable, backref="config_profiles",
                                            cascade="all,delete,delete-orphan"),
    'odu100_raConfTable': relationship(Odu100RaConfTable, backref="config_profiles",
                                       cascade="all,delete,delete-orphan"),
    'odu100_raLlcConfTable': relationship(Odu100RaLlcConfTable, backref="config_profiles",
                                          cascade="all,delete,delete-orphan"),
    'odu100_raPreferredRFChannelTable': relationship(Odu100RaPreferredRFChannelTable, backref="config_profiles",
                                                     cascade="all,delete,delete-orphan"),
    'odu100_raTddMacConfigTable': relationship(Odu100RaTddMacConfigTable, backref="config_profiles",
                                               cascade="all,delete,delete-orphan"),
    'odu100_ruConfTable': relationship(Odu100RuConfTable, backref="config_profiles",
                                       cascade="all,delete,delete-orphan"),
    'odu100_ruDateTimeTable': relationship(Odu100RuDateTimeTable, backref="config_profiles",
                                           cascade="all,delete,delete-orphan"),
    'odu100_ruOmOperationsTable': relationship(Odu100RuOmOperationsTable, backref="config_profiles",
                                               cascade="all,delete,delete-orphan"),
    'odu100_syncConfigTable': relationship(Odu100SyncConfigTable, backref="config_profiles",
                                           cascade="all,delete,delete-orphan"),
    'odu100_sysOmcRegistrationTable': relationship(Odu100SysOmcRegistrationTable, backref="config_profiles",
                                                   cascade="all,delete,delete-orphan"),
    'swt4_bandwidth_control': relationship(Swt4BandwidthControl, backref="config_profiles",
                                           cascade="all,delete,delete-orphan"),
    'swt4_storm_control': relationship(Swt4StormControl, backref="config_profiles", cascade="all,delete,delete-orphan"),
    'swt4_port_statistics': relationship(Swt4PortStatistics, backref="config_profiles",
                                         cascade="all,delete,delete-orphan"),
    'swt4_port_settings': relationship(Swt4PortSettings, backref="config_profiles", cascade="all,delete,delete-orphan"),
    'swt4_ip_settings': relationship(Swt4IpSettings, backref="config_profiles", cascade="all,delete,delete-orphan"),
    'swt4_vlan_settings': relationship(Swt4VlanSettings, backref="config_profiles", cascade="all,delete,delete-orphan"),
    'swt4_port_based_priority': relationship(Swt4PortBasedPriority, backref="config_profiles",
                                             cascade="all,delete,delete-orphan"),
    'swt4_dscp_based_priority': relationship(Swt4DscpBasedPriority, backref="config_profiles",
                                             cascade="all,delete,delete-orphan"),
    'swt4_802_1p_based_priority': relationship(Swt48021pBasedPriority, backref="config_profiles",
                                               cascade="all,delete,delete-orphan"),
    'swt4_ip_base_priority': relationship(Swt4IpBasePriority, backref="config_profiles",
                                          cascade="all,delete,delete-orphan"),
    'swt4_queue_based_priority': relationship(Swt4QueueBasedPriority, backref="config_profiles",
                                              cascade="all,delete,delete-orphan"),
    'swt4_queue_weight_based': relationship(Swt4QueueWeightBased, backref="config_profiles",
                                            cascade="all,delete,delete-orphan"),
    'swt4_qos_arbitration': relationship(Swt4QosArbitration, backref="config_profiles",
                                         cascade="all,delete,delete-orphan"),
    'swt4_1p_remarking': relationship(Swt41pRemarking, backref="config_profiles", cascade="all,delete,delete-orphan")})

########################### mapping of odu100 ############################
