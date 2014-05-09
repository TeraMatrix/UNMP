#!/usr/bin/python2.6

####################### import the packages ###################################
try:
    import uuid
    from nms_config import *
    from sqlalchemy import *
    from sqlalchemy.orm import *
    from sqlalchemy.dialects.mysql import *
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.exc import *
    from sqlalchemy.orm.exc import *
    from traceback import *
    from sys import *
except ImportError as e:
    print e

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

try:
    # Create A Database Connection
    db = open_database_sqlalchemy_connection()
    db.echo = False
    metadata = MetaData(db)

    # metadata object used for binding
    Base = declarative_base()

    # device_type Table
    class DeviceType(Base):
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

    class Hosts(Base):
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
                snmp_trap_port, snmp_read_community, snmp_write_community, snmp_port, snmp_version_id, comment,
                icon_name, software_update_time, nms_id):
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
        '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                    (self.host_id, self.host_name, self.host_alias, self.ip_address, self.mac_address,
                     self.device_type_id, self.netmask,
                     self.gateway, self.primary_dns, self.secondary_dns, self.config_profile_id,
                     self.timestamp, self.created_by, self.creation_time, self.is_deleted, self.updated_by,
                     self.ne_id, self.site_id, self.host_state_id, self.priority_id, self.host_vendor_id,
                     self.host_os_id,
                     self.host_asset_id, self.http_username, self.http_password, self.http_port, self.snmp_trap_port,
                     self.snmp_read_community,
                     self.snmp_write_community, self.snmp_port, self.snmp_version_id, self.comment, self.icon_name,
                     self.software_update_time, self.nms_id)

    clear_mappers()

    Session = sessionmaker(bind=db)
    session = Session()

    #--------------------Mapping For Host-------------------------------------
    device_type_table = DeviceType.__table__
    mapper(DeviceType, device_type_table, properties={'hosts': relationship(
        Hosts, backref='device_type', cascade="all, delete, delete-orphan")})
    dic = {}
    host_table = Hosts.__table__
    mapper(Hosts, host_table)
    device_param_list = session.query(
        Hosts.snmp_version_id, Hosts.snmp_write_community,
        Hosts.ip_address, Hosts.snmp_port, Hosts.config_profile_id).all()
    add_device = DeviceType(
        'idu', 'idu port', 'idu8', '', '', '', '', '', '', '', '2', 0, 11)
    close_database_sqlalchemy_connection(db)
    session.flush()
    session.add(add_device)
    session.commit()
    ##    session.delete(add_device)
    ##    session.commit()
    print device_param_list

except ProgrammingError as e:
    print e, "1"
except AttributeError as e:
    print e, "2"
except OperationalError as e:
    print e, "3"
except TimeoutError as e:
    print e, "4"
except NameError as e:
    print e, "5"
except UnboundExecutionError as e:
    print e, "6"
except DatabaseError as e:
    dic['success'] = 1
    dic['reuslt'] = str(e[-1])
    print dic
except DisconnectionError as e:
    print e, "8"
except NoResultFound as e:
    print e, "9"
except UnmappedInstanceError as e:
    print e, "10"
except NoReferenceError as e:
    print e, "11"
except SAWarning as e:
    print e, "12"
except Exception as e:
    print e, "13"
