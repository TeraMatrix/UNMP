#!/usr/bin/python2.6

#Use non_primary=True to create a non primary Mapper

# Import modules that contain sqlalchemy functions, libraries and variable
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper,relationship, backref,clear_mappers,sessionmaker,aliased
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, CHAR, TEXT, INT,INTEGER,TINYINT, DATE, VARCHAR, FLOAT, BIGINT, SMALLINT, TIME, TIMESTAMP, ForeignKey
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

# Import modules that contain the function and libraries
import uuid
from unmp_config import SystemConfig

engine = create_engine('%s://%s:%s@%s/%s' % SystemConfig.get_sqlalchemy_credentials(), echo=False,pool_size=3,max_overflow=2,pool_timeout=30)
Base = declarative_base()


class Acknowledge(Base):
	__tablename__= "acknowledge"
	acknowledge_id = Column(VARCHAR(16),primary_key=True)
	acknowledge_name = Column(VARCHAR(32))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,acknowledge_id,acknowledge_name,is_deleted,sequence):
		self.acknowledge_id = acknowledge_id
		self.acknowledge_name = acknowledge_name
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<Acknowledge('%s','%s','%s','%s')>" %(self.acknowledge_id,self.acknowledge_name,self.is_deleted,self.sequence)


class Actions(Base):
	__tablename__= "actions"
	action_id = Column(VARCHAR(64),primary_key=True)
	action_name = Column(VARCHAR(32))
	action_options = Column(VARCHAR(256))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,action_id,action_name,action_options,is_deleted,sequence):
		self.action_id = action_id
		self.action_name = action_name
		self.action_options = action_options
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<Actions('%s','%s','%s','%s','%s')>" %(self.action_id,self.action_name,self.action_options,self.is_deleted,self.sequence)


##class ApScheduling(Base):
##	__tablename__= "ap_scheduling"
##	ap_scheduling_id = Column(VARCHAR(64),primary_key=True)
##	event = Column(VARCHAR(16))
##	start_date = Column(DATE)
##	end_date = Column(DATE)
##	start_time = Column(TIME)
##	end_time = Column(TIME)
##	is_repeated = Column(SMALLINT)
##	repeat_type = Column(VARCHAR(16))
##	sun = Column(SMALLINT)
##	mon = Column(SMALLINT)
##	tue = Column(SMALLINT)
##	wed = Column(SMALLINT)
##	thu = Column(SMALLINT)
##	fri = Column(SMALLINT)
##	sat = Column(SMALLINT)
##	jan = Column(SMALLINT)
##	feb = Column(SMALLINT)
##	mar = Column(SMALLINT)
##	apr = Column(SMALLINT)
##	may = Column(SMALLINT)
##	jun = Column(SMALLINT)
##	jul = Column(SMALLINT)
##	aug = Column(SMALLINT)
##	sept = Column(SMALLINT)
##	oct = Column(SMALLINT)
##	nov = Column(SMALLINT)
##	dece = Column(SMALLINT)
##	day = Column(SMALLINT)
##	timestamp = Column(TIMESTAMP)
##	created_by = Column(VARCHAR(64))
##	creation_time = Column(TIMESTAMP)
##	updated_by = Column(VARCHAR(64))
##	is_deleted = Column(SMALLINT)
##
##	def __init__(self,event,start_date,end_date,start_time,end_time,is_repeated,repeat_type,sun,mon,tue,wed,thu,fri,sat,jan,feb,mar,apr,may,jun,jul,aug,sept,oct,nov,dece,day,timestamp,created_by,creation_time,updated_by,is_deleted):
##		self.ap_scheduling_id = uuid.uuid1()
##		self.event = event
##		self.start_date = start_date
##		self.end_date = end_date
##		self.start_time = start_time
##		self.end_time = end_time
##		self.is_repeated = is_repeated
##		self.repeat_type = repeat_type
##		self.sun = sun
##		self.mon = mon
##		self.tue = tue
##		self.wed = wed
##		self.thu = thu
##		self.fri = fri
##		self.sat = sat
##		self.jan = jan
##		self.feb = feb
##		self.mar = mar
##		self.apr = apr
##		self.may = may
##		self.jun = jun
##		self.jul = jul
##		self.aug = aug
##		self.sept = sept
##		self.oct = oct
##		self.nov = nov
##		self.dece = dece
##		self.day = day
##		self.timestamp = timestamp
##		self.created_by = created_by
##		self.creation_time = creation_time
##		self.updated_by = updated_by
##		self.is_deleted = is_deleted
##		
##	def __repr__(self):
##		return "<ApScheduling('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap_scheduling_id,self.event,self.start_date,self.end_date,self.start_time,self.end_time,self.is_repeated,self.repeat_type,self.sun,self.mon,self.tue,self.wed,self.thu,self.fri,self.sat,self.jan,self.feb,self.mar,self.apr,self.may,self.jun,self.jul,self.aug,self.sept,self.oct,self.nov,self.dece,self.day,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.is_deleted)
##
##
##class ApSchedulingHostMapping(Base):
##	__tablename__= "ap_scheduling_host_mapping"
##	ap_scheduling_host_mapping_id = Column(VARCHAR(64),primary_key=True)
##	ap_scheduling_id = Column(VARCHAR(64),ForeignKey('ap_scheduling.ap_scheduling_id'))
##	host_id = Column(VARCHAR(64),ForeignKey('hosts.host_id'))
##
##	def __init__(self,ap_scheduling_id,host_id):
##		self.ap_scheduling_host_mapping_id = uuid.uuid1()
##		self.ap_scheduling_id = ap_scheduling_id
##		self.host_id = host_id
##		
##	def __repr__(self):
##		return "<ApSchedulingHostMapping('%s','%s','%s')>" %(self.ap_scheduling_host_mapping_id,self.ap_scheduling_id,self.host_id)


class BlackListMacs(Base):
	__tablename__= "black_list_macs"
	black_list_mac_id = Column(VARCHAR(64),primary_key=True)
	mac_address = Column(VARCHAR(32))
	description = Column(VARCHAR(128))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	cteation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,mac_address,description,timestamp,created_by,cteation_time,updated_by,is_deleted):
		self.black_list_mac_id = uuid.uuid1()
		self.mac_address = mac_address
		self.description = description
		self.timestamp = timestamp
		self.created_by = created_by
		self.cteation_time = cteation_time
		self.updated_by = updated_by
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<BlackListMacs('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.black_list_mac_id,self.mac_address,self.description,self.timestamp,self.created_by,self.cteation_time,self.updated_by,self.is_deleted)


class Cities(Base):
	__tablename__= "cities"
	city_id = Column(VARCHAR(64),primary_key=True)
	city_name = Column(VARCHAR(64))
	state_id = Column(VARCHAR(64),ForeignKey('states.state_id'))
	is_deleted = Column(SMALLINT)

	def __init__(self,city_name,state_id,is_deleted):
		self.city_id = uuid.uuid1()
		self.city_name = city_name
		self.state_id = state_id
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<Cities('%s','%s','%s','%s')>" %(self.city_id,self.city_name,self.state_id,self.is_deleted)


class Odu16ConfigProfiles(Base):
	__tablename__= "config_profiles"
	config_profile_id = Column(INTEGER,primary_key=True)
	device_type_id = Column(VARCHAR(16),ForeignKey('device_type.device_type_id'))
	profile_name = Column(VARCHAR(64))
	config_profile_type_id = Column(VARCHAR(16),ForeignKey('config_profile_type.config_profile_type_id'))
	parent_id = Column(VARCHAR(64))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,device_type_id,profile_name,config_profile_type_id,parent_id,timestamp,created_by,creation_time,updated_by,is_deleted):
		self.config_profile_id = None
		self.device_type_id = device_type_id
		self.profile_name = profile_name
		self.config_profile_type_id = config_profile_type_id
		self.parent_id = parent_id
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<ConfigProfiles('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.config_profile_id,self.device_type_id,self.profile_name,self.config_profile_type_id,self.parent_id,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.is_deleted)


class ConfigProfileType(Base):
	__tablename__= "config_profile_type"
	config_profile_type_id = Column(VARCHAR(16),primary_key=True)
	config_profile_type = Column(VARCHAR(64))

	def __init__(self,config_profile_type_id,config_profile_type):
		self.config_profile_type_id = config_profile_type_id
		self.config_profile_type = config_profile_type
		
	def __repr__(self):
		return "<ConfigProfileType('%s','%s')>" %(self.config_profile_type_id,self.config_profile_type)


class Countries(Base):
	__tablename__= "countries"
	country_id = Column(VARCHAR(64),primary_key=True)
	country_name = Column(VARCHAR(64))
	country_code = Column(VARCHAR(16))
	is_deleted = Column(SMALLINT)

	def __init__(self,country_name,country_code,is_deleted):
		self.country_id = uuid.uuid1()
		self.country_name = country_name
		self.country_code = country_code
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<Countries('%s','%s','%s','%s')>" %(self.country_id,self.country_name,self.country_code,self.is_deleted)


class DaemonEvents(Base):
	__tablename__= "daemon_events"
	daemon_event_id = Column(INTEGER,primary_key=True)
	daemon_name = Column(VARCHAR(16))
	error_no = Column(INT)
	state = Column(SMALLINT)
	timestamp = Column(TIMESTAMP)
	short_description = Column(VARCHAR(64))
	is_viewed = Column(SMALLINT)

	def __init__(self,daemon_name,error_no,state,timestamp,short_description,is_viewed):
		self.daemon_event_id = None
		self.daemon_name = daemon_name
		self.error_no = error_no
		self.state = state
		self.timestamp = timestamp
		self.short_description = short_description
		self.is_viewed = is_viewed
		
	def __repr__(self):
		return "<DaemonEvents('%s','%s','%s','%s','%s','%s','%s')>" %(self.daemon_event_id,self.daemon_name,self.error_no,self.state,self.timestamp,self.short_description,self.is_viewed)


class DaemonTimestamp(Base):
	__tablename__= "daemon_timestamp"
	daemon_timestamp_id = Column(INTEGER,primary_key=True)
	daemon_name = Column(VARCHAR(32))
	timestamp = Column(TIMESTAMP)

	def __init__(self,daemon_name,timestamp):
		self.daemon_timestamp_id = None
		self.daemon_name = daemon_name
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<DaemonTimestamp('%s','%s','%s')>" %(self.daemon_timestamp_id,self.daemon_name,self.timestamp)


class DeviceType(Base):
    __tablename__= "device_type"
    device_type_id = Column(VARCHAR(16),primary_key=True)
    device_name = Column(VARCHAR(64))
    sdm_discovery_id = Column(VARCHAR(8))
    sdm_discovery_value = Column(VARCHAR(64))
    vnl_discovery_value = Column(VARCHAR(64))
    ping_discovery_value = Column(VARCHAR(64))
    snmp_discovery_value = Column(VARCHAR(64))
    upnp_discovery_value = Column(VARCHAR(64))
    icon_name = Column(VARCHAR(64))
    mib_name = Column(VARCHAR(32))
    mib_path = Column(VARCHAR(256))
    table_prefix = Column(VARCHAR(32))
    is_generic = Column(SMALLINT)
    is_deleted = Column(SMALLINT)
    sequence = Column(SMALLINT)

    def __init__(self,device_name,sdm_discovery_id,sdm_discovery_value,vnl_discovery_value,ping_discovery_value,snmp_discovery_value,upnp_discovery_value,icon_name,mib_name,mib_path,table_prefix,is_generic,is_deleted,sequence):
        self.device_type_id = uuid.uuid1()
        self.device_name = device_name
        self.sdm_discovery_id = sdm_discovery_id
        self.sdm_discovery_value = sdm_discovery_value
        self.vnl_discovery_value = vnl_discovery_value
        self.ping_discovery_value = ping_discovery_value
        self.snmp_discovery_value = snmp_discovery_value
        self.upnp_discovery_value = upnp_discovery_value
        self.icon_name = icon_name
        self.mib_name = mib_name
        self.mib_path = mib_path
        self.table_prefix = table_prefix
        self.is_generic = is_generic
        self.is_deleted = is_deleted
        self.sequence = sequence
        
    def __repr__(self):
        return "<DeviceType('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.device_type_id,self.device_name,self.sdm_discovery_id,self.sdm_discovery_value,self.vnl_discovery_value,self.ping_discovery_value,self.snmp_discovery_value,self.upnp_discovery_value,self.icon_name,self.mib_name,self.mib_path,self.table_prefix,self.is_generic,self.is_deleted,self.sequence)


class DiscoveredHosts(Base):
	__tablename__= "discovered_hosts"
	discovered_host_id = Column(INTEGER,primary_key=True)
	discovery_id = Column(INTEGER,ForeignKey('discovery.discovery_id'))
	host_alias = Column(VARCHAR(64))
	ip_address = Column(VARCHAR(32))
	device_type_id = Column(VARCHAR(64),ForeignKey('device_type.device_type_id'))
	mac_address = Column(VARCHAR(32))

	def __init__(self,discovery_id,host_alias,ip_address,device_type_id,mac_address):
		self.discovered_host_id =None
		self.discovery_id = discovery_id
		self.host_alias = host_alias
		self.ip_address = ip_address
		self.device_type_id = device_type_id
		self.mac_address = mac_address
		
	def __repr__(self):
		return "<DiscoveredHosts('%s','%s','%s','%s','%s','%s')>" %(self.discovered_host_id,self.discovery_id,self.host_alias,self.ip_address,self.device_type_id,self.mac_address)


class Discovery(Base):
	__tablename__= "discovery"
	discovery_id = Column(INTEGER,primary_key=True)
	discovery_type_id = Column(INTEGER,ForeignKey('discovery_type.discovery_type_id'))
	ip_start_range = Column(VARCHAR(32))
	ip_end_range = Column(VARCHAR(32))
	timeout = Column(INT)
	snmp_community = Column(VARCHAR(32))
	snmp_port = Column(VARCHAR(8))
	snmp_version = Column(VARCHAR(8))
	sdm_device_list = Column(VARCHAR(64))
	scheduling_id = Column(VARCHAR(8),ForeignKey('scheduling.scheduling_id'))
	service_management = Column(VARCHAR(16))
	done_percent = Column(INT)
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,discovery_type_id,ip_start_range,ip_end_range,timeout,snmp_community,snmp_port,snmp_version,sdm_device_list,scheduling_id,service_management,done_percent,timestamp,created_by,creation_time,updated_by,is_deleted):
		self.discovery_id = None
		self.discovery_type_id = discovery_type_id
		self.ip_start_range = ip_start_range
		self.ip_end_range = ip_end_range
		self.timeout = timeout
		self.snmp_community = snmp_community
		self.snmp_port = snmp_port
		self.snmp_version = snmp_version
		self.sdm_device_list = sdm_device_list
		self.scheduling_id = scheduling_id
		self.service_management = service_management
		self.done_percent = done_percent
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<Discovery('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.discovery_id,self.discovery_type_id,self.ip_start_range,self.ip_end_range,self.timeout,self.snmp_community,self.snmp_port,self.snmp_version,self.sdm_device_list,self.scheduling_id,self.service_management,self.done_percent,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.is_deleted)


class DiscoveryType(Base):
	__tablename__= "discovery_type"
	discovery_type_id = Column(VARCHAR(16),primary_key=True)
	discovery_type = Column(VARCHAR(16))
	description = Column(VARCHAR(128))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,discovery_type_id,discovery_type,description,is_deleted,sequence):
		self.discovery_type_id = discovery_type_id
		self.discovery_type = discovery_type
		self.description = description
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<DiscoveryType('%s','%s','%s','%s','%s')>" %(self.discovery_type_id,self.discovery_type,self.description,self.is_deleted,self.sequence)


class ErrorDescription(Base):
	__tablename__= "error_description"
	error_no = Column(INT,primary_key=True)
	error_causes = Column(TEXT)
	probable_solution = Column(TEXT)

	def __init__(self,error_no,error_causes,probable_solution):
		self.error_no = error_no
		self.error_causes = error_causes
		self.probable_solution = probable_solution
		
	def __repr__(self):
		return "<ErrorDescription('%s','%s','%s')>" %(self.error_no,self.error_causes,self.probable_solution)


class EventLog(Base):
	__tablename__= "event_log"
	event_logs = Column(INTEGER,primary_key=True)
	event_type_id = Column(VARCHAR(64))
	description = Column(VARCHAR(128))
	timestamp = Column(TIMESTAMP)

	def __init__(self,event_type_id,description,timestamp):
		self.event_logs = None
		self.event_type_id = event_type_id
		self.description = description
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<EventLog('%s','%s','%s','%s')>" %(self.event_logs,self.event_type_id,self.description,self.timestamp)


class EventType(Base):
	__tablename__= "event_type"
	event_type_id = Column(INTEGER,primary_key=True)
	event_name = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,event_name,is_deleted):
		self.event_type_id = None
		self.event_name = event_name
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<EventType('%s','%s','%s')>" %(self.event_type_id,self.event_name,self.is_deleted)


class Groups(Base):
	__tablename__= "groups"
	group_id = Column(VARCHAR(64),primary_key=True)
	group_name = Column(VARCHAR(64))
	description = Column(VARCHAR(128))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)
	updated_by = Column(VARCHAR(64))
	role_id = Column(VARCHAR(64),ForeignKey('roles.role_id'))
	is_default = Column(SMALLINT)

	def __init__(self,group_name,description,timestamp,created_by,creation_time,is_deleted,updated_by,role_id,is_default):
		self.group_id = uuid.uuid1()
		self.group_name = group_name
		self.description = description
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.is_deleted = is_deleted
		self.updated_by = updated_by
		self.role_id = role_id
		self.is_default = is_default
		
	def __repr__(self):
		return "<Groups('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.group_id,self.group_name,self.description,self.timestamp,self.created_by,self.creation_time,self.is_deleted,self.updated_by,self.role_id,self.is_default)


class Hostgroups(Base):
	__tablename__= "hostgroups"
	hostgroup_id = Column(INTEGER,primary_key=True)
	hostgroup_name = Column(VARCHAR(64))
	hostgroup_alias = Column(VARCHAR(64))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)
	updated_by = Column(VARCHAR(64))
	is_default = Column(SMALLINT)

	def __init__(self,hostgroup_name,hostgroup_alias,timestamp,created_by,creation_time,is_deleted,updated_by,is_default):
		self.hostgroup_id = None
		self.hostgroup_name = hostgroup_name
		self.hostgroup_alias = hostgroup_alias
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.is_deleted = is_deleted
		self.updated_by = updated_by
		self.is_default = is_default
		
	def __repr__(self):
		return "<Hostgroups('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.hostgroup_id,self.hostgroup_name,self.hostgroup_alias,self.timestamp,self.created_by,self.creation_time,self.is_deleted,self.updated_by,self.is_default)


class HostgroupsGroups(Base):
	__tablename__= "hostgroups_groups"
	hostgroup_group_id = Column(INTEGER,primary_key=True)
	hostgroup_id = Column(VARCHAR(64),ForeignKey('hostgroups.hostgroup_id'))
	group_id = Column(VARCHAR(64),ForeignKey('groups.group_id'))

	def __init__(self,hostgroup_id,group_id):
		self.hostgroup_group_id = None
		self.hostgroup_id = hostgroup_id
		self.group_id = group_id
		
	def __repr__(self):
		return "<HostgroupsGroups('%s','%s','%s')>" %(self.hostgroup_group_id,self.hostgroup_id,self.group_id)


class Hosts(Base):
    __tablename__= "hosts"
    host_id = Column(INTEGER,primary_key=True)
    host_name = Column(VARCHAR(64))
    host_alias = Column(VARCHAR(64))
    ip_address = Column(VARCHAR(32))
    mac_address = Column(VARCHAR(32))
    device_type_id = Column(VARCHAR(16),ForeignKey('device_type.device_type_id'))
    netmask = Column(VARCHAR(32))
    gateway = Column(VARCHAR(32))
    primary_dns = Column(VARCHAR(32))
    secondary_dns = Column(VARCHAR(32))
    dns_state = Column(VARCHAR(16))
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    timestamp = Column(TIMESTAMP)
    created_by = Column(VARCHAR(64))
    creation_time = Column(TIMESTAMP)
    is_deleted = Column(SMALLINT)
    updated_by = Column(VARCHAR(64))
    ne_id = Column(INT)
    site_id = Column(INTEGER,ForeignKey('sites.site_id'))
    host_state_id = Column(VARCHAR(16),ForeignKey('host_states.host_state_id'))
    priority_id = Column(VARCHAR(16),ForeignKey('priority.priority_id'))
    host_vendor_id = Column(INTEGER,ForeignKey('host_vendor.host_vendor_id'))
    host_os_id = Column(VARCHAR(16),ForeignKey('host_os.host_os_id'))
    host_asset_id = Column(INTEGER,ForeignKey('host_assets.host_asset_id'))
    http_username = Column(VARCHAR(64))
    http_password = Column(VARCHAR(64))
    http_port = Column(VARCHAR(8))
    snmp_read_community = Column(VARCHAR(32))
    snmp_write_community = Column(VARCHAR(32))
    snmp_port = Column(VARCHAR(8))
    snmp_trap_port = Column(VARCHAR(8))
    snmp_version_id = Column(VARCHAR(8))
    comment = Column(VARCHAR(256))
    nms_id = Column(VARCHAR(64),ForeignKey('nms_instance.nms_id'))
    parent_name = Column(VARCHAR(64))
    lock_status = Column(CHAR(8))
    is_localhost = Column(SMALLINT)
    reconcile_health = Column(SMALLINT)
    reconcile_status = Column(SMALLINT)
    ssh_username = Column(VARCHAR(64))
    ssh_password = Column(VARCHAR(64))
    ssh_port = Column(INTEGER)
    firmware_mapping_id = Column(VARCHAR(16))
    def __init__(self,host_name,host_alias,ip_address,mac_address,device_type_id,netmask,gateway,primary_dns,secondary_dns,dns_state,config_profile_id,timestamp,created_by,creation_time,is_deleted,updated_by,ne_id,site_id,host_state_id,priority_id,host_vendor_id,host_os_id,host_asset_id,http_username,http_password,http_port,snmp_read_community,snmp_write_community,snmp_port,snmp_trap_port,snmp_version_id,comment,nms_id,parent_name,lock_status,is_localhost,reconcile_health=0,reconcile_status=0,ssh_username=None,ssh_password=None,ssh_port=None,firmware_mapping_id=None):
        self.host_id = None
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
        self.reconcile_health = reconcile_health   
        self.reconcile_status = reconcile_status     
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.ssh_port = ssh_port
        self.firmware_mapping_id = firmware_mapping_id
        
    def __repr__(self):
        return "<Hosts('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_id,self.host_name,self.host_alias,self.ip_address,self.mac_address,self.device_type_id,self.netmask,self.gateway,self.primary_dns,self.secondary_dns,self.dns_state,self.config_profile_id,self.timestamp,self.created_by,self.creation_time,self.is_deleted,self.updated_by,self.ne_id,self.site_id,self.host_state_id,self.priority_id,self.host_vendor_id,self.host_os_id,self.host_asset_id,self.http_username,self.http_password,self.http_port,self.snmp_read_community,self.snmp_write_community,self.snmp_port,self.snmp_trap_port,self.snmp_version_id,self.comment,self.nms_id,self.parent_name,self.lock_status,self.is_localhost,self.reconcile_health,self.reconcile_status,self.ssh_username,self.ssh_password,self.ssh_port,self.firmware_mapping_id)


class HostsHostgroups(Base):
	__tablename__= "hosts_hostgroups"
	host_hostgroup_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	hostgroup_id = Column(VARCHAR(64),ForeignKey('hostgroups.hostgroup_id'))

	def __init__(self,host_id,hostgroup_id):
		self.host_hostgroup_id = None
		self.host_id = host_id
		self.hostgroup_id = hostgroup_id
		
	def __repr__(self):
		return "<HostsHostgroups('%s','%s','%s')>" %(self.host_hostgroup_id,self.host_id,self.hostgroup_id)


class HostAlertActionMapping(Base):
	__tablename__= "host_alert_action_mapping"
	host_alert_action_mapping_id = Column(INTEGER,primary_key=True)
	host_alert_masking_id = Column(VARCHAR(64),ForeignKey('host_alert_masking.host_alert_masking_id'))
	acknowlegde_id = Column(VARCHAR(64))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	next_scheduling = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)

	def __init__(self,host_alert_masking_id,acknowlegde_id,timestamp,created_by,creation_time,updated_by,next_scheduling,is_deleted):
		self.host_alert_action_mapping_id = None
		self.host_alert_masking_id = host_alert_masking_id
		self.acknowlegde_id = acknowlegde_id
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.next_scheduling = next_scheduling
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<HostAlertActionMapping('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_alert_action_mapping_id,self.host_alert_masking_id,self.acknowlegde_id,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.next_scheduling,self.is_deleted)


class HostAlertMasking(Base):
	__tablename__= "host_alert_masking"
	host_alert_masking_id = Column(INTEGER,primary_key=True)
	host_object_id = Column(INT)
	current_status = Column(SMALLINT)
	group_id = Column(VARCHAR(64),ForeignKey('groups.group_id'))
	action_id = Column(VARCHAR(16),ForeignKey('actions.action_id'))
	scheduling_minutes = Column(INT)
	is_repeated = Column(SMALLINT)
	acknowledge_id = Column(VARCHAR(16),ForeignKey('acknowledge.acknowledge_id'))
	description = Column(VARCHAR(256))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,host_object_id,current_status,group_id,action_id,scheduling_minutes,is_repeated,acknowledge_id,description,timestamp,created_by,creation_time,updated_by,is_deleted):
		self.host_alert_masking_id = None
		self.host_object_id = host_object_id
		self.current_status = current_status
		self.group_id = group_id
		self.action_id = action_id
		self.scheduling_minutes = scheduling_minutes
		self.is_repeated = is_repeated
		self.acknowledge_id = acknowledge_id
		self.description = description
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<HostAlertMasking('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_alert_masking_id,self.host_object_id,self.current_status,self.group_id,self.action_id,self.scheduling_minutes,self.is_repeated,self.acknowledge_id,self.description,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.is_deleted)


class HostAssets(Base):
    __tablename__= "host_assets"
    host_asset_id = Column(INTEGER,primary_key=True)
    longitude = Column(VARCHAR(32))
    latitude = Column(VARCHAR(32))
    serial_number = Column(VARCHAR(32))
    hardware_version = Column(VARCHAR(32))
    firmware_update_time = Column(TIMESTAMP)
    firmware_status = Column(Enum('0','1','2','3','4','5','6','11','12','13','14','15','16',name='enumhostassets'))
    firmware_type = Column(VARCHAR(10))
    firmware_file_name = Column(VARCHAR(50))
    firmware_msg = Column(VARCHAR(64))
    firmware_file_path = Column(VARCHAR(50))    
    ra_mac = Column(VARCHAR(18))

    def __init__(self,longitude,latitude,serial_number,hardware_version,firmware_update_time="0000-00-00 00:00:00",firmware_status=0,firmware_type=None,firmware_file_name=None,firmware_msg=None,firmware_file_path=None,ra_mac = " "):
        self.host_asset_id = None
        self.longitude = longitude
        self.latitude = latitude
        self.serial_number = serial_number
        self.hardware_version = hardware_version
        self.firmware_update_time = firmware_update_time
        self.firmware_status = firmware_status
        self.firmware_type = firmware_type
        self.firmware_file_name = firmware_file_name
        self.firmware_msg = firmware_msg
        self.firmware_file_path = firmware_file_path
        self.ra_mac = ra_mac
        
    def __repr__(self):
        return "<HostAssets('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_asset_id,self.longitude,self.latitude,self.serial_number,self.hardware_version,self.firmware_update_time,self.firmware_status,self.firmware_type,self.firmware_file_name,self.firmware_msg,self.firmware_file_path,self.ra_mac)

##class HostAssets(Base):
##	__tablename__= "host_assets"
##	host_asset_id = Column(INTEGER,primary_key=True)
##	longitude = Column(VARCHAR(32))
##	latitude = Column(VARCHAR(32))
##	serial_number = Column(VARCHAR(32))
##	hardware_version = Column(VARCHAR(32))
##	software_update_time = Column(TIMESTAMP)
##	software_update_state = Column(SMALLINT)
##	software_update_msg = Column(VARCHAR(128))
##
##	def __init__(self,longitude,latitude,serial_number,hardware_version,software_update_time,software_update_state,software_update_msg):
##		self.host_asset_id = None
##		self.longitude = longitude
##		self.latitude = latitude
##		self.serial_number = serial_number
##		self.hardware_version = hardware_version
##		self.software_update_time = software_update_time
##		self.software_update_state = software_update_state
##		self.software_update_msg = software_update_msg
##		
##	def __repr__(self):
##		return "<HostAssets('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_asset_id,self.longitude,self.latitude,self.serial_number,self.hardware_version,self.software_update_time,self.software_update_state,self.software_update_msg)

class HostOs(Base):
	__tablename__= "host_os"
	host_os_id = Column(VARCHAR(16),primary_key=True)
	os_name = Column(VARCHAR(32))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,host_os_id,os_name,is_deleted,sequence):
		self.host_os_id = host_os_id
		self.os_name = os_name
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<HostOs('%s','%s','%s','%s')>" %(self.host_os_id,self.os_name,self.is_deleted,self.sequence)


class HostStates(Base):
	__tablename__= "host_states"
	host_state_id = Column(VARCHAR(16),primary_key=True)
	state_name = Column(VARCHAR(32))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,host_state_id,state_name,is_deleted,sequence):
		self.host_state_id = host_state_id
		self.state_name = state_name
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<HostStates('%s','%s','%s','%s')>" %(self.host_state_id,self.state_name,self.is_deleted,self.sequence)

class HostServices(Base):
	__tablename__= "host_services"
	host_service_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	service_description = Column(VARCHAR(64))
	check_command = Column(VARCHAR(256))
	max_check_attempts = Column(INT)
	normal_check_interval = Column(INT)
	retry_check_interval = Column(INT)
	is_deleted = Column(SMALLINT)

	def __init__(self,host_id,service_description,check_command,max_check_attempts,normal_check_interval,retry_check_interval,is_deleted):
		self.host_service_id = None
		self.host_id = host_id
		self.service_description = service_description
		self.check_command = check_command
		self.max_check_attempts = max_check_attempts
		self.normal_check_interval = normal_check_interval
		self.retry_check_interval = retry_check_interval
		self.is_deleted = is_deleted  
		
	def __repr__(self):
		return "<HostStates('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_service_id,self.host_id,self.service_description,self.check_command,self.max_check_attempts,self.normal_check_interval,self.retry_check_interval,self.is_deleted)

class HostVendor(Base):
	__tablename__= "host_vendor"
	host_vendor_id = Column(INTEGER,primary_key=True)
	vendor_name = Column(VARCHAR(64))
	description = Column(VARCHAR(128))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,vendor_name,description,timestamp,created_by,creation_time,updated_by,is_deleted):
		self.host_vendor_id = None
		self.vendor_name = vendor_name
		self.description = description
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<HostVendor('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.host_vendor_id,self.vendor_name,self.description,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.is_deleted)

class LocalhostBandwidth(Base):
	__tablename__= "localhost_bandwidth"
	localhost_bandwidth_id = Column(INTEGER,primary_key=True)
	interface = Column(VARCHAR(16))
	tx = Column(BIGINT)
	rx = Column(BIGINT)
	timestamp = Column(TIMESTAMP)

	def __init__(self,interface,tx,rx,timestamp):
		self.localhost_bandwidth_id = None
		self.interface = interface
		self.tx = tx
		self.rx = rx
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<LocalhostBandwidth('%s','%s','%s','%s','%s')>" %(self.localhost_bandwidth_id,self.interface,self.tx,self.rx,self.timestamp)

class LocalhostCpuUsage(Base):
	__tablename__= "localhost_cpu_usage"
	localhost_cpu_usage_id = Column(INTEGER,primary_key=True)
	cpu_usage = Column(FLOAT(32,4))
	timestamp = Column(TIMESTAMP)

	def __init__(self,cpu_usage,timestamp):
		self.localhost_cpu_usage_id = None
		self.cpu_usage = cpu_usage
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<LocalhostCpuUsage('%s','%s','%s')>" %(self.localhost_cpu_usage_id,self.cpu_usage,self.timestamp)

class Modules(Base):
	__tablename__= "modules"
	module_id = Column(VARCHAR(64),primary_key=True)
	module_name = Column(VARCHAR(32))
	page_link_id = Column(VARCHAR(64))
	is_default = Column(SMALLINT)
	is_deleted = Column(SMALLINT)
	page_id = Column(VARCHAR(64),ForeignKey('pages.page_id'))

	def __init__(self,module_name,page_link_id,is_default,is_deleted,page_id):
		self.module_id = uuid.uuid1()
		self.module_name = module_name
		self.page_link_id = page_link_id
		self.is_default = is_default
		self.is_deleted = is_deleted
		self.page_id = page_id
		
	def __repr__(self):
		return "<Modules('%s','%s','%s','%s','%s','%s')>" %(self.module_id,self.module_name,self.page_link_id,self.is_default,self.is_deleted,self.page_id)




class NmsGraphs(Base):
	__tablename__= "nms_graphs"
	nms_graphs_id = Column(VARCHAR(64),primary_key=True)
	device_type_id = Column(VARCHAR(16),ForeignKey('device_type.device_type_id'))
	tablename = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,device_type_id,tablename,is_deleted):
		self.nms_graphs_id = uuid.uuid1()
		self.device_type_id = device_type_id
		self.tablename = tablename
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<NmsGraphs('%s','%s','%s','%s')>" %(self.nms_graphs_id,self.device_type_id,self.tablename,self.is_deleted)


class NmsInstance(Base):
	__tablename__= "nms_instance"
	nms_id = Column(VARCHAR(64),primary_key=True)
	nms_name = Column(VARCHAR(32))
	longitude = Column(VARCHAR(32))
	latitude = Column(VARCHAR(32))
	timestamp = Column(TIMESTAMP)

	def __init__(self,nms_name,longitude,latitude,timestamp):
		self.nms_id = uuid.uuid1()
		self.nms_name = nms_name
		self.longitude = longitude
		self.latitude = latitude
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<NmsInstance('%s','%s','%s','%s','%s')>" %(self.nms_id,self.nms_name,self.longitude,self.latitude,self.timestamp)



class Odu1007_2_25_oids(Base):
	__tablename__= "odu100_7_2_25_oids"
	oid_id = Column(INTEGER,primary_key=True)
	device_type_id = Column(VARCHAR(16),ForeignKey('device_type.device_type_id'))
	oid = Column(VARCHAR(256))
	oid_name = Column(VARCHAR(256))
	oid_type = Column(VARCHAR(16))
	access = Column(SMALLINT)
	default_value = Column(VARCHAR(256))
	min_value = Column(VARCHAR(128))
	max_value = Column(VARCHAR(256))
	indexes = Column(VARCHAR(256))
	dependent_id = Column(INTEGER)
	multivalue = Column(SMALLINT)
	table_name = Column(VARCHAR(128))
	coloumn_name = Column(VARCHAR(128))
	indexes_name = Column(VARCHAR(64))

	def __init__(self,oid_id,device_type_id,oid,oid_name,oid_type,access,default_value,min_value,max_value,indexes,dependent_id,multivalue,table_name,coloumn_name,indexes_name):
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
		self.indexes_name = indexes_name
		
	def __repr__(self):
		return "<Odu1007_2_25_oids('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.oid_id,self.device_type_id,self.oid,self.oid_name,self.oid_type,self.access,self.default_value,self.min_value,self.max_value,self.indexes,self.dependent_id,self.multivalue,self.table_name,self.coloumn_name,self.indexes_name)

class Odu1007_2_25_oids_multivalues(Base):
	__tablename__= "odu100_7_2_25_oids_multivalues"
	oids_multivalue_id = Column(INTEGER,primary_key=True)
	oid_id = Column(VARCHAR(64),ForeignKey('odu100_7_2_25_oids.oid_id'))
	value = Column(VARCHAR(128))
	name = Column(VARCHAR(128))

	def __init__(self,oids_multivalue_id,oid_id,value,name):
		self.oids_multivalue_id = oids_multivalue_id
		self.oid_id = oid_id
		self.value = value
		self.name = name
		
	def __repr__(self):
		return "<Odu1007_2_25_oids_multivalues('%s','%s','%s','%s')>" %(self.oids_multivalue_id,self.oid_id,self.value,self.name)

class Odu1007_2_25_oid_table(Base):
	__tablename__= "odu100_7_2_25_oid_table"
	table_name = Column(VARCHAR(64),primary_key=True)
	table_oid = Column(VARCHAR(64))
	varbinds = Column(TINYINT)
	is_recon = Column(INTEGER)
	status = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,table_name,table_oid,varbinds,is_recon,status,timestamp):
		self.table_name = table_name
		self.table_oid = table_oid
		self.varbinds = varbinds
		self.is_recon = is_recon
		self.status = status
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<Odu1007_2_25_oid_table('%s','%s','%s','%s','%s','%s')>" %(self.table_name,self.table_oid,self.varbinds,self.is_recon,self.status,self.timestamp)



class Odu1007_2_20_oids(Base):
    __tablename__= "odu100_7_2_20_oids"
    oid_id = Column(INTEGER,primary_key=True)
    device_type_id = Column(VARCHAR(16),ForeignKey('device_type.device_type_id'))
    oid = Column(VARCHAR(256))
    oid_name = Column(VARCHAR(256))
    oid_type = Column(VARCHAR(16))
    access = Column(SMALLINT)
    default_value = Column(VARCHAR(256))
    min_value = Column(VARCHAR(128))
    max_value = Column(VARCHAR(256))
    indexes = Column(VARCHAR(256))
    dependent_id = Column(VARCHAR(64))
    multivalue = Column(SMALLINT)
    table_name = Column(VARCHAR(128))
    coloumn_name = Column(VARCHAR(128))
    indexes_name = Column(VARCHAR(64))

    def __init__(self,device_type_id,oid,oid_name,oid_type,access,default_value,min_value,max_value,indexes,dependent_id,multivalue,table_name,coloumn_name,indexes_name):
        self.oid_id = None
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
        self.indexes_name = indexes_name
        
    def __repr__(self):
        return "<Odu1007_2_20_oids('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.oid_id,self.device_type_id,self.oid,self.oid_name,self.oid_type,self.access,self.default_value,self.min_value,self.max_value,self.indexes,self.dependent_id,self.multivalue,self.table_name,self.coloumn_name,self.indexes_name)


class Odu1007_2_20_oids_multivalues(Base):
	__tablename__= "odu100_7_2_20_oids_multivalues"
	oids_multivalue_id = Column(INTEGER,primary_key=True)
	oid_id = Column(VARCHAR(64),ForeignKey('odu100_7_2_20_oids.oid_id'))
	value = Column(VARCHAR(128))
	name = Column(VARCHAR(128))

	def __init__(self,oid_id,value,name):
		self.oids_multivalue_id = None
		self.oid_id = oid_id
		self.value = value
		self.name = name
		
	def __repr__(self):
		return "<Odu1007_2_20_oids_multivalues('%s','%s','%s','%s')>" %(self.oids_multivalue_id,self.oid_id,self.value,self.name)


class Pages(Base):
	__tablename__= "pages"
	page_id = Column(VARCHAR(64),primary_key=True)
	page_name = Column(VARCHAR(64))
	page_link_id = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)
	snapin_id = Column(VARCHAR(64),ForeignKey('snapins.snapin_id'))

	def __init__(self,page_name,page_link_id,is_deleted,snapin_id):
		self.page_id = uuid.uuid1()
		self.page_name = page_name
		self.page_link_id = page_link_id
		self.is_deleted = is_deleted
		self.snapin_id = snapin_id
		
	def __repr__(self):
		return "<Pages('%s','%s','%s','%s','%s')>" %(self.page_id,self.page_name,self.page_link_id,self.is_deleted,self.snapin_id)


class PagesLink(Base):
	__tablename__= "pages_link"
	pages_link_id = Column(VARCHAR(64),primary_key=True)
	page_link = Column(VARCHAR(256))
	is_deleted = Column(SMALLINT)

	def __init__(self,page_link,is_deleted):
		self.pages_link_id = uuid.uuid1()
		self.page_link = page_link
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<PagesLink('%s','%s','%s')>" %(self.pages_link_id,self.page_link,self.is_deleted)


class Priority(Base):
	__tablename__= "priority"
	priority_id = Column(VARCHAR(16),primary_key=True)
	priority_name = Column(VARCHAR(32))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,priority_id,priority_name,is_deleted,sequence):
		self.priority_id = priority_id
		self.priority_name = priority_name
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<Priority('%s','%s','%s','%s')>" %(self.priority_id,self.priority_name,self.is_deleted,self.sequence)


##class RetryApScheduling(Base):
##	__tablename__= "retry_ap_scheduling"
##	retry_ap_scheduling_id = Column(VARCHAR(64),primary_key=True)
##	retry_date = Column(DATE)
##	retry_time = Column(TIME)
##	host_id = Column(VARCHAR(64),ForeignKey('hosts.host_id'))
##	message = Column(VARCHAR(256))
##	event = Column(VARCHAR(16))
##	timestamp = Column(TIMESTAMP)
##	created_by = Column(VARCHAR(64))
##
##	def __init__(self,retry_date,retry_time,host_id,message,event,timestamp,created_by):
##		self.retry_ap_scheduling_id = uuid.uuid1()
##		self.retry_date = retry_date
##		self.retry_time = retry_time
##		self.host_id = host_id
##		self.message = message
##		self.event = event
##		self.timestamp = timestamp
##		self.created_by = created_by
##		
##	def __repr__(self):
##		return "<RetryApScheduling('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.retry_ap_scheduling_id,self.retry_date,self.retry_time,self.host_id,self.message,self.event,self.timestamp,self.created_by)


class Roles(Base):
	__tablename__= "roles"
	role_id = Column(VARCHAR(64),primary_key=True)
	role_name = Column(VARCHAR(64))
	description = Column(VARCHAR(128))
	parent_id = Column(VARCHAR(64))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)
	updated_by = Column(VARCHAR(64))

	def __init__(self,role_name,description,parent_id,timestamp,created_by,creation_time,is_deleted,updated_by):
		self.role_id = uuid.uuid1()
		self.role_name = role_name
		self.description = description
		self.parent_id = parent_id
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.is_deleted = is_deleted
		self.updated_by = updated_by
		
	def __repr__(self):
		return "<Roles('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.role_id,self.role_name,self.description,self.parent_id,self.timestamp,self.created_by,self.creation_time,self.is_deleted,self.updated_by)


class RolePagesLink(Base):
	__tablename__= "role_pages_link"
	role_pages_link_id = Column(VARCHAR(64),primary_key=True)
	role_id = Column(VARCHAR(64),ForeignKey('roles.role_id'))
	pages_link_id = Column(VARCHAR(64),ForeignKey('pages_link.pages_link_id'))

	def __init__(self,role_id,pages_link_id):
		self.role_pages_link_id = uuid.uuid1()
		self.role_id = role_id
		self.pages_link_id = pages_link_id
		
	def __repr__(self):
		return "<RolePagesLink('%s','%s','%s')>" %(self.role_pages_link_id,self.role_id,self.pages_link_id)


class Scheduling(Base):
	__tablename__= "scheduling"
	scheduling_id = Column(VARCHAR(8),primary_key=True)
	scheduling_name = Column(VARCHAR(16))
	is_deleted = Column(SMALLINT)
	sequence = Column(SMALLINT)

	def __init__(self,scheduling_id,scheduling_name,is_deleted,sequence):
		self.scheduling_id = scheduling_id
		self.scheduling_name = scheduling_name
		self.is_deleted = is_deleted
		self.sequence = sequence
		
	def __repr__(self):
		return "<Scheduling('%s','%s','%s','%s')>" %(self.scheduling_id,self.scheduling_name,self.is_deleted,self.sequence)


class ServiceTemplates(Base):
	__tablename__= "service_templates"
	service_template_id = Column(VARCHAR(64),primary_key=True)
	device_type_id = Column(VARCHAR(64),ForeignKey('device_type.device_type_id'))
	template_name = Column(VARCHAR(64))
	service_description = Column(VARCHAR(64))
	check_command = Column(VARCHAR(256))
	max_check_attempts = Column(INT)
	normal_check_interval = Column(INT)
	retry_check_interval = Column(INT)
	remark = Column(VARCHAR(128))
	is_deleted = Column(SMALLINT)

	def __init__(self,device_type_id,template_name,service_description,check_command,max_check_attempts,normal_check_interval,retry_check_interval,remark,is_deleted):
		self.service_template_id = uuid.uuid1()
		self.device_type_id = device_type_id
		self.template_name = template_name
		self.service_description = service_description
		self.check_command = check_command
		self.max_check_attempts = max_check_attempts
		self.normal_check_interval = normal_check_interval
		self.retry_check_interval = retry_check_interval
		self.remark = remark
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<ServiceTemplates('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.service_template_id,self.device_type_id,self.template_name,self.service_description,self.check_command,self.max_check_attempts,self.normal_check_interval,self.retry_check_interval,self.remark,self.is_deleted)


class Sites(Base):
	__tablename__= "sites"
	site_id = Column(INTEGER,primary_key=True)
	site_name = Column(VARCHAR(64))
	ip_address = Column(VARCHAR(32))
	description = Column(VARCHAR(128))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)
	updated_by = Column(VARCHAR(64))

	def __init__(self,site_name,ip_address,description,timestamp,created_by,creation_time,is_deleted,updated_by):
		self.site_id = None
		self.site_name = site_name
		self.ip_address = ip_address
		self.description = description
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.is_deleted = is_deleted
		self.updated_by = updated_by
		
	def __repr__(self):
		return "<Sites('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.site_id,self.site_name,self.ip_address,self.description,self.timestamp,self.created_by,self.creation_time,self.is_deleted,self.updated_by)


class Snapins(Base):
	__tablename__= "snapins"
	snapin_id = Column(VARCHAR(64),primary_key=True)
	snapin_name = Column(VARCHAR(64))
	author = Column(VARCHAR(32))
	description = Column(VARCHAR(128))
	is_menu = Column(SMALLINT)
	is_deleted = Column(SMALLINT)

	def __init__(self,snapin_name,author,description,is_menu,is_deleted):
		self.snapin_id = uuid.uuid1()
		self.snapin_name = snapin_name
		self.author = author
		self.description = description
		self.is_menu = is_menu
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<Snapins('%s','%s','%s','%s','%s','%s')>" %(self.snapin_id,self.snapin_name,self.author,self.description,self.is_menu,self.is_deleted)


class SnmpAdvanceOptions(Base):
	__tablename__= "snmp_advance_options"
	snmp_advance_option_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	discovery_id = Column(VARCHAR(64),ForeignKey('discovery.discovery_id'))
	snmp_username = Column(VARCHAR(64))
	snmp_password = Column(VARCHAR(64))
	authentication_key = Column(VARCHAR(64))
	authentication_protocol = Column(VARCHAR(64))
	private_password = Column(VARCHAR(64))
	private_key = Column(VARCHAR(64))
	private_protocol = Column(VARCHAR(64))

	def __init__(self,host_id,discovery_id,snmp_username,snmp_password,authentication_key,authentication_protocol,private_password,private_key,private_protocol):
		self.snmp_advance_option_id = None
		self.host_id = host_id
		self.discovery_id = discovery_id
		self.snmp_username = snmp_username
		self.snmp_password = snmp_password
		self.authentication_key = authentication_key
		self.authentication_protocol = authentication_protocol
		self.private_password = private_password
		self.private_key = private_key
		self.private_protocol = private_protocol
		
	def __repr__(self):
		return "<SnmpAdvanceOptions('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.snmp_advance_option_id,self.host_id,self.discovery_id,self.snmp_username,self.snmp_password,self.authentication_key,self.authentication_protocol,self.private_password,self.private_key,self.private_protocol)


class States(Base):
	__tablename__= "states"
	state_id = Column(VARCHAR(64),primary_key=True)
	state_name = Column(VARCHAR(64))
	country_id = Column(VARCHAR(64),ForeignKey('countries.country_id'))
	is_deleted = Column(SMALLINT)

	def __init__(self,state_name,country_id,is_deleted):
		self.state_id = uuid.uuid1()
		self.state_name = state_name
		self.country_id = country_id
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<States('%s','%s','%s','%s')>" %(self.state_id,self.state_name,self.country_id,self.is_deleted)


class TcpDiscovery(Base):
	__tablename__= "tcp_discovery"
	ne_id = Column(INT,primary_key=True)
	sys_omc_register_contact_addr = Column(VARCHAR(128))
	sys_omc_register_contact_person = Column(VARCHAR(32))
	sys_omc_register_contact_mobile = Column(VARCHAR(16))
	sys_omc_register_alternate_contact = Column(VARCHAR(64))
	sys_omc_register_contact_email = Column(VARCHAR(64))
	sys_omc_register_active_card_hwld = Column(VARCHAR(32))
	sys_omc_registerne_site_direction = Column(VARCHAR(32))
	sys_omc_registerne_site_landmark = Column(VARCHAR(32))
	sys_omc_registerne_site_latitude = Column(VARCHAR(32))
	sys_omc_registerne_site_longitude = Column(VARCHAR(32))
	sys_omc_registerne_state = Column(VARCHAR(32))
	sys_omc_registerne_country = Column(VARCHAR(32))
	sys_omc_registerne_city = Column(VARCHAR(32))
	sys_omc_registerne_sitebldg = Column(VARCHAR(32))
	sys_omc_registerne_sitefloor = Column(VARCHAR(32))
	site_mac = Column(VARCHAR(32))
	product_id = Column(INT)
	timestamp = Column(TIMESTAMP)
	ip_address = Column(VARCHAR(32))
	is_set = Column(SMALLINT)

	def __init__(self,sys_omc_register_contact_addr,sys_omc_register_contact_person,sys_omc_register_contact_mobile,sys_omc_register_alternate_contact,sys_omc_register_contact_email,sys_omc_register_active_card_hwld,sys_omc_registerne_site_direction,sys_omc_registerne_site_landmark,sys_omc_registerne_site_latitude,sys_omc_registerne_site_longitude,sys_omc_registerne_state,sys_omc_registerne_country,sys_omc_registerne_city,sys_omc_registerne_sitebldg,sys_omc_registerne_sitefloor,site_mac,product_id,timestamp,ip_address,is_set):
		self.ne_id = None
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
		self.sys_omc_registerne_country = sys_omc_registerne_country
		self.sys_omc_registerne_city = sys_omc_registerne_city
		self.sys_omc_registerne_sitebldg = sys_omc_registerne_sitebldg
		self.sys_omc_registerne_sitefloor = sys_omc_registerne_sitefloor
		self.site_mac = site_mac
		self.product_id = product_id
		self.timestamp = timestamp
		self.ip_address = ip_address
		self.is_set = is_set
		
	def __repr__(self):
		return "<TcpDiscovery('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ne_id,self.sys_omc_register_contact_addr,self.sys_omc_register_contact_person,self.sys_omc_register_contact_mobile,self.sys_omc_register_alternate_contact,self.sys_omc_register_contact_email,self.sys_omc_register_active_card_hwld,self.sys_omc_registerne_site_direction,self.sys_omc_registerne_site_landmark,self.sys_omc_registerne_site_latitude,self.sys_omc_registerne_site_longitude,self.sys_omc_registerne_state,self.sys_omc_registerne_country,self.sys_omc_registerne_city,self.sys_omc_registerne_sitebldg,self.sys_omc_registerne_sitefloor,self.site_mac,self.product_id,self.timestamp,self.ip_address,self.is_set)


class TcpHealthCheck(Base):
	__tablename__= "tcp_health_check"
	tcp_health_check_id = Column(INT,primary_key=True)
	ne_id = Column(INT)
	health_check = Column(INT)
	ip_address = Column(VARCHAR(32))
	timestamp = Column(TIMESTAMP)
	last_timestamp = Column(TIMESTAMP)

	def __init__(self,ne_id,health_check,ip_address,timestamp,last_timestamp):
		self.tcp_health_check_id = None
		self.ne_id = ne_id
		self.health_check = health_check
		self.ip_address = ip_address
		self.timestamp = timestamp
		self.last_timestamp = last_timestamp
		
	def __repr__(self):
		return "<TcpHealthCheck('%s','%s','%s','%s','%s','%s')>" %(self.tcp_health_check_id,self.ne_id,self.health_check,self.ip_address,self.timestamp,self.last_timestamp)


class TrapAlarms(Base):
	__tablename__= "trap_alarms"
	trap_alarm_id = Column(INTEGER,primary_key=True)
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

	def __init__(self,event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description,timestamp):
		self.trap_alarm_id = None
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
		return "<TrapAlarms('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.trap_alarm_id,self.event_id,self.trap_id,self.agent_id,self.trap_date,self.trap_receive_date,self.serevity,self.trap_event_id,self.trap_event_type,self.manage_obj_id,self.manage_obj_name,self.component_id,self.trap_ip,self.description,self.timestamp)


class TrapAlarmActionMapping(Base):
	__tablename__= "trap_alarm_action_mapping"
	trap_alarm_action_mapping_id = Column(INTEGER,primary_key=True)
	trap_alarm_masking_id = Column(VARCHAR(64),ForeignKey('trap_alarm_masking.trap_alarm_masking_id'))
	acknowledge_id = Column(VARCHAR(64),ForeignKey('acknowledge.acknowledge_id'))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	next_scheduling = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)

	def __init__(self,trap_alarm_masking_id,acknowledge_id,timestamp,created_by,creation_time,updated_by,next_scheduling,is_deleted):
		self.trap_alarm_action_mapping_id = None
		self.trap_alarm_masking_id = trap_alarm_masking_id
		self.acknowledge_id = acknowledge_id
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.next_scheduling = next_scheduling
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<TrapAlarmActionMapping('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.trap_alarm_action_mapping_id,self.trap_alarm_masking_id,self.acknowledge_id,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.next_scheduling,self.is_deleted)


class TrapAlarmClear(Base):
	__tablename__= "trap_alarm_clear"
	trap_alarm_clear_id = Column(INTEGER,primary_key=True)
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

	def __init__(self,event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description,timestamp):
		self.trap_alarm_clear_id = None
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
		return "<TrapAlarmClear('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.trap_alarm_clear_id,self.event_id,self.trap_id,self.agent_id,self.trap_date,self.trap_receive_date,self.serevity,self.trap_event_id,self.trap_event_type,self.manage_obj_id,self.manage_obj_name,self.component_id,self.trap_ip,self.description,self.timestamp)


class TrapAlarmCurrent(Base):
	__tablename__= "trap_alarm_current"
	trap_alarm_current_id = Column(INTEGER,primary_key=True)
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

	def __init__(self,event_id,trap_id,agent_id,trap_date,trap_receive_date,serevity,trap_event_id,trap_event_type,manage_obj_id,manage_obj_name,component_id,trap_ip,description,timestamp):
		self.trap_alarm_current_id = None
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
		return "<TrapAlarmCurrent('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.trap_alarm_current_id,self.event_id,self.trap_id,self.agent_id,self.trap_date,self.trap_receive_date,self.serevity,self.trap_event_id,self.trap_event_type,self.manage_obj_id,self.manage_obj_name,self.component_id,self.trap_ip,self.description,self.timestamp)


class TrapAlarmFieldTable(Base):
	__tablename__= "trap_alarm_field_table"
	trap_alarm_field = Column(VARCHAR(32),primary_key=True)
	field_name = Column(VARCHAR(32))
	field_type = Column(VARCHAR(16))

	def __init__(self,field_name,field_type):
		self.trap_alarm_field = None
		self.field_name = field_name
		self.field_type = field_type
		
	def __repr__(self):
		return "<TrapAlarmFieldTable('%s','%s','%s')>" %(self.trap_alarm_field,self.field_name,self.field_type)


class TrapAlarmMasking(Base):
	__tablename__= "trap_alarm_masking"
	trap_alarm_masking_id = Column(INTEGER,primary_key=True)
	trap_alarm_field = Column(VARCHAR(32),ForeignKey('trap_alarm_field_table.trap_alarm_field'))
	trap_alarm_value = Column(VARCHAR(128))
	action_id = Column(VARCHAR(64),ForeignKey('actions.action_id'))
	group_id = Column(VARCHAR(64),ForeignKey('groups.group_id'))
	scheduling_minutes = Column(INT)
	is_repeated = Column(SMALLINT)
	description = Column(TEXT)
	acknowledge_id = Column(VARCHAR(16),ForeignKey('acknowledge.acknowledge_id'))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))
	is_deleted = Column(SMALLINT)

	def __init__(self,trap_alarm_field,trap_alarm_value,action_id,group_id,scheduling_minutes,is_repeated,description,acknowledge_id,timestamp,created_by,creation_time,updated_by,is_deleted):
		self.trap_alarm_masking_id = None
		self.trap_alarm_field = trap_alarm_field
		self.trap_alarm_value = trap_alarm_value
		self.action_id = action_id
		self.group_id = group_id
		self.scheduling_minutes = scheduling_minutes
		self.is_repeated = is_repeated
		self.description = description
		self.acknowledge_id = acknowledge_id
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		self.is_deleted = is_deleted
		
	def __repr__(self):
		return "<TrapAlarmMasking('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.trap_alarm_masking_id,self.trap_alarm_field,self.trap_alarm_value,self.action_id,self.group_id,self.scheduling_minutes,self.is_repeated,self.description,self.acknowledge_id,self.timestamp,self.created_by,self.creation_time,self.updated_by,self.is_deleted)


class TrapIdMapping(Base):
	__tablename__= "trap_id_mapping"
	trap_id_mapping_id = Column(INTEGER,primary_key=True)
	trap_event_type = Column(VARCHAR(32))
	trap_event_id = Column(VARCHAR(32))
	is_alarm = Column(SMALLINT)
	is_deleted = Column(SMALLINT)
	trap_clear_mapping_id = Column(VARCHAR(32))
	trap_clear_mapping_type = Column(VARCHAR(32))
	priority_id = Column(VARCHAR(16),ForeignKey('priority.priority_id'))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	updated_by = Column(VARCHAR(64))

	def __init__(self,trap_event_type,trap_event_id,is_alarm,is_deleted,trap_clear_mapping_id,trap_clear_mapping_type,priority_id,timestamp,created_by,creation_time,updated_by):
		self.trap_id_mapping_id = None
		self.trap_event_type = trap_event_type
		self.trap_event_id = trap_event_id
		self.is_alarm = is_alarm
		self.is_deleted = is_deleted
		self.trap_clear_mapping_id = trap_clear_mapping_id
		self.trap_clear_mapping_type = trap_clear_mapping_type
		self.priority_id = priority_id
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.updated_by = updated_by
		
	def __repr__(self):
		return "<TrapIdMapping('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.trap_id_mapping_id,self.trap_event_type,self.trap_event_id,self.is_alarm,self.is_deleted,self.trap_clear_mapping_id,self.trap_clear_mapping_type,self.priority_id,self.timestamp,self.created_by,self.creation_time,self.updated_by)


class Users(Base):
	__tablename__= "users"
	user_id = Column(VARCHAR(64),primary_key=True)
	first_name = Column(VARCHAR(64))
	last_name = Column(VARCHAR(64))
	designation = Column(VARCHAR(64))
	company_name = Column(VARCHAR(64))
	mobile_no = Column(VARCHAR(16))
	address = Column(VARCHAR(128))
	city_id = Column(VARCHAR(64))
	state_id = Column(VARCHAR(64))
	country_id = Column(VARCHAR(64))
	email_id = Column(VARCHAR(128))

	def __init__(self,first_name,last_name,designation,company_name,mobile_no,address,city_id,state_id,country_id,email_id):
		self.user_id = uuid.uuid1()
		self.first_name = first_name
		self.last_name = last_name
		self.designation = designation
		self.company_name = company_name
		self.mobile_no = mobile_no
		self.address = address
		self.city_id = city_id
		self.state_id = state_id
		self.country_id = country_id
		self.email_id = email_id
		
	def __repr__(self):
		return "<Users('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.user_id,self.first_name,self.last_name,self.designation,self.company_name,self.mobile_no,self.address,self.city_id,self.state_id,self.country_id,self.email_id)


class UsersGroups(Base):
	__tablename__= "users_groups"
	user_group_id = Column(VARCHAR(64),primary_key=True)
	user_id = Column(VARCHAR(64),ForeignKey('users.user_id'))
	group_id = Column(VARCHAR(64),ForeignKey('groups.group_id'))

	def __init__(self,user_id,group_id):
		self.user_group_id = uuid.uuid1()
		self.user_id = user_id
		self.group_id = group_id
		
	def __repr__(self):
		return "<UsersGroups('%s','%s','%s')>" %(self.user_group_id,self.user_id,self.group_id)


class UserLogin(Base):
	__tablename__= "user_login"
	user_login_id = Column(VARCHAR(64),primary_key=True)
	user_id = Column(VARCHAR(64),ForeignKey('users.user_id'))
	user_name = Column(VARCHAR(64))
	password = Column(VARCHAR(64))
	timestamp = Column(TIMESTAMP)
	created_by = Column(VARCHAR(64))
	creation_time = Column(TIMESTAMP)
	is_deleted = Column(SMALLINT)
	updated_by = Column(VARCHAR(64))
	nms_id = Column(VARCHAR(64),ForeignKey('nms_instance.nms_id'))

	def __init__(self,user_id,user_name,password,timestamp,created_by,creation_time,is_deleted,updated_by,nms_id):
		self.user_login_id = uuid.uuid1()
		self.user_id = user_id
		self.user_name = user_name
		self.password = password
		self.timestamp = timestamp
		self.created_by = created_by
		self.creation_time = creation_time
		self.is_deleted = is_deleted
		self.updated_by = updated_by
		self.nms_id = nms_id
		
	def __repr__(self):
		return "<UserLogin('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.user_login_id,self.user_id,self.user_name,self.password,self.timestamp,self.created_by,self.creation_time,self.is_deleted,self.updated_by,self.nms_id)


#########################################################Anuj Samariya Model ###################################################################################


class SetOdu16IPConfigTable(Base):
    """
    set_odu16_ip_config_table Table 
    """
    __tablename__= 'set_odu16_ip_config_table'
    set_odu16_ip_config_table_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    admin_state = Column(SMALLINT)
    ip_address = Column(VARCHAR(16))
    ip_network_mask = Column(VARCHAR(16))
    ip_default_gateway = Column(VARCHAR(16))
    auto_ip_config = Column(INTEGER)

    def __init__(self,set_odu16_ip_config_table_id,config_profile_id,admin_state,ip_address,ip_network_mask,ip_default_gateway,auto_ip_config):
        self.set_odu16_ip_config_table_id = None
        self.config_profile_id = config_profile_id
        self.admin_state = admin_state
        self.ip_address = ip_address
        self.ip_network_mask = ip_network_mask
        self.ip_default_gateway = ip_default_gateway
        self.auto_ip_config = auto_ip_config
        
    def __repr__(self):
        return "<SetOdu16_ip_config_table('%s','%s','%s','%s','%s','%s','%s')>" %(self.set_odu16_ip_config_table_id,self.config_profile_id,self.admin_state,self.ip_address,self.ip_network_mask,self.ip_default_gateway,self.auto_ip_config)
    
#set_odu16_network_interface_config_table Table
class SetOdu16NetworkInterfaceConfig(Base):
    """
    set_odu16_network_interface_config_table Table
    """
    __tablename__='set_odu16_network_interface_config_table'
    set_odu16_network_interface_config_entry_id = Column(INTEGER,primary_key=True)	
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 	
    ssid =	Column(VARCHAR(32))
    index =  Column(INTEGER)

    def __init__(self,config_profile_id,ssid,index):
        self.set_odu16_network_interface_config_entry_id=None
        self.config_profile_id = config_profile_id
        self.ssid=ssid
        self.index=index
        
    def __repr__(self):
        return "SetOdu16NetworkInterfaceConfigTable<'%s','%s','%s','%s'>" %(self.set_odu16_network_interface_config_entry_id ,self.config_profile_id,self.ssid,self.index)
    
    
#set_odu16_omc_conf_table Table
class SetOdu16OmcConfTable(Base):
    """
    set_odu16_omc_conf_table Table
    """
    __tablename__= 'set_odu16_omc_conf_table'
    set_odu16_omc_conf_table_id= Column(INTEGER,primary_key=True)
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 	
    omc_ip_address = Column(VARCHAR(32))
    periodic_stats_timer = Column(INTEGER)
    def __init__(self,config_profile_id,omc_ip_address,periodic_stats_timer):
        self.set_odu16_omc_conf_table_id=None
        self.config_profile_id = config_profile_id
        self.omc_ip_address=omc_ip_address
        self.periodic_stats_timer=periodic_stats_timer
        
    def __repr__(self):
        return "SetOdu16OmcConfTable<'%s','%s','%s','%s'>" %(self.set_odu16_omc_conf_table_id,self.config_profile_id,self.omc_ip_address,self.periodic_stats_timer)        

#set_odu16_peer_config_table Table
class SetOdu16PeerConfigTable(Base):
    """
    set_odu16_peer_config_table Table
    """
    __tablename__= 'set_odu16_peer_config_table'
    set_odu16_peer_config_table_id = Column(INTEGER,primary_key=True)
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 	
    peer_mac_address = Column(TEXT)
    index = Column(INTEGER)
    
    def __init__(self,config_profile_id,peer_mac_address,index):
        self.set_odu16_peer_config_table_id=None
        self.config_profile_id = config_profile_id
        self.peer_mac_address=peer_mac_address
        self.index=index
        
    def __repr__(self):
        return "SetOdu16PeerConfig<'%s','%s','%s','%s'>" %(self.set_odu16_peer_config_table_id,self.config_profile_id,self.peer_mac_address,self.index)        

#set_odu16_ra_acl_config_table Table
class SetOdu16RAAclConfigTable(Base):
    """
    set_odu16_ra_acl_config_table Table
    """
    __tablename__= 'set_odu16_ra_acl_config_table'
    set_odu16_ra_acl_config_table_id = Column(INTEGER,primary_key=True)
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 	
    mac_address = Column(TEXT)
    index = Column(INTEGER)
    
    def __init__(self,config_profile_id,mac_address,index):
        self.set_odu16_ra_acl_config_table_id=None
        self.config_profile_id=config_profile_id
        self.mac_address=mac_address
        self.index=index
        
    def __repr__(self):
        return "SetOdu16RAAclConfig<'%s','%s','%s','%s'>" %(self.set_odu16_ra_acl_config_table_id ,self.config_profile_id,self.mac_address,self.index)        


#set_odu16_om_operations_table Table
class SetOdu16OmOperationsTable(Base):
    """
    set_odu16_om_operations_table Table
    """
    __tablename__= 'set_odu16_om_operations_table'
    set_odu16_om_operations_table_id =	Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    om_operation_req =	Column(INTEGER) 		
    user_name =	Column(VARCHAR(64)) 	
    password =	Column(VARCHAR(64)) 	
    ftp_server_address =	Column(VARCHAR(32))
    path_name =	Column(VARCHAR(256)) 	
    enable_swam =	Column(INTEGER)
    
    def __init__(self,config_profile_id,om_operation_req,user_name,password,ftp_server_address,path_name,enable_swam):
        self.set_odu16_om_operations_table_id = None
        self.config_profile_id = config_profile_id
        self.om_operation_req=om_operation_req
        self.user_name=user_name
        self.password=password
        self.ftp_server_address=ftp_server_address
        self.path_name=path_name
        self.enable_swam=enable_swam
    def __repr__(self):
        return "SetOdu16OmOperationsTable<'%s','%s','%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_om_operations_table_id,self.config_profile_id ,self.om_operation_req,self.user_name,self.password,self.ftp_server_address,self.path_name,self.enable_swam)        


#set_odu16_ra_conf_table Table
class SetOdu16RAConfTable(Base):	
    """
    set_odu16_ra_conf_table Table
    """
    __tablename__= 'set_odu16_ra_conf_table'
    set_odu16_ra_conf_table_id=	Column(INTEGER,primary_key=True) 
    config_profile_id=	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    raAdminState=	Column(SMALLINT) 		
    acl_mode  =	Column(SMALLINT) 	
    ssid = Column(VARCHAR(64))
    def __init__(self,config_profile_id,raAdminState,acl_mode,ssid):
        self.set_odu16_ra_conf_table_id = None
        self.config_profile_id = config_profile_id
        self.raAdminState=raAdminState
        self.acl_mode=acl_mode
        self.ssid=ssid
    def __repr__(self):
        return "SetOdu16OmOperationsTable<'%s','%s','%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_ra_conf_table_id,self.config_profile_id,self.raAdminState,self.acl_mode,self.ssid)        



#set_odu16_ra_llc_conf_table
class SetOdu16RALlcConfTable(Base):
    """
    set_odu16_ra_llc_conf_table
    """
    __tablename__= 'set_odu16_ra_llc_conf_table'
    set_odu16_ra_llc_conf_table_id=	Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    llc_arq_enable = Column(SMALLINT) 		
    arq_win = Column(INTEGER) 	
    frame_loss_threshold = Column(INTEGER) 		
    leaky_bucket_timer_val = Column(INTEGER) 	
    frame_loss_timeout = Column(INTEGER)
    def __init__(self,config_profile_id,llc_arq_enable,arq_win,frame_loss_threshold,leaky_bucket_timer_val,frame_loss_timeout):
        self.set_odu16_ra_llc_conf_table_id=None
        self.config_profile_id = config_profile_id
        self.llc_arq_enable=llc_arq_enable
        self.arq_win=arq_win
        self.frame_loss_threshold=frame_loss_threshold
        self.leaky_bucket_timer_val=leaky_bucket_timer_val
        self.frame_loss_timeout=frame_loss_timeout
        
    def __repr__(self):
        return "SetOdu16RALlcConfTable<'%s','%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_ra_llc_conf_table_id,self.config_profile_id,self.llc_arq_enable,self.arq_win,self.frame_loss_threshold,self.leaky_bucket_timer_val,self.frame_loss_timeout)
    
    
#set_odu16_ra_tdd_mac_config Table
class SetOdu16RATddMacConfig(Base):
    """
    set_odu16_ra_tdd_mac_config Table
    """
    __tablename__= 'set_odu16_ra_tdd_mac_config'
    set_odu16_ra_tdd_mac_config_table_id = Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    rf_channel_frequency  = Column(INTEGER) 		
    pass_phrase  = Column(VARCHAR(64)) 	
    rfcoding = Column(SMALLINT) 		
    tx_power = Column(INTEGER) 	
    max_power =	Column(INTEGER) 	
    max_crc_errors = Column(INTEGER)
    leaky_bucket_timer_value = Column(INTEGER)
    def __init__(self,config_profile_id,rf_channel_frequency,pass_phrase,rfcoding,tx_power,max_crc_errors,leaky_bucket_timer_value):
        self.set_odu16_ra_tdd_mac_config_table_id= None
        self.config_profile_id = config_profile_id
        self.rf_channel_frequency=rf_channel_frequency
        self.pass_phrase=pass_phrase
        self.rfcoding=rfcoding
        self.tx_power=tx_power
        self.max_crc_errors=max_crc_errors
        self.leaky_bucket_timer_value=leaky_bucket_timer_value
        
    def __repr__(self):
        return "SetOdu16RATddMacConfig<'%s','%s','%s','%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_ra_tdd_mac_config_table_id,self.config_profile_id,self.rf_channel_frequency,self.pass_phrase,self.rfcoding,self.tx_power,self.max_crc_errors,self.leaky_bucket_timer_value,self.max_power)


#set_odu16_ru_conf_table Table
class SetOdu16RUConfTable(Base):
    """
    set_odu16_ru_conf_table Table
    """
    __tablename__= 'set_odu16_ru_conf_table'
    set_odu16_ru_conf_table_id = Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    adminstate  = Column(SMALLINT) 		
    channel_bandwidth  = Column(INTEGER) 	
    sysnch_source = Column(INTEGER) 		
    country_code = Column(VARCHAR(16)) 	
    def __init__(self,config_profile_id,adminstate,channel_bandwidth,sysnch_source,country_code):
        self.set_odu16_ru_conf_table_id = None
        self.config_profile_id = config_profile_id
        self.adminstate=adminstate
        self.channel_bandwidth=channel_bandwidth
        self.sysnch_source=sysnch_source
        self.country_code=country_code
        
    def __repr__(self):
        return "SetOdu16RUConfTable<'%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_ru_conf_table_id,self.config_profile_id,self.adminstate,self.channel_bandwidth,self.sysnch_source,self.country_code)

#set_odu16_ru_date_time_table Table
class SetOdu16RUDateTimeTable(Base):
    """
    set_odu16_ru_date_time_table Table
    """
    __tablename__= 'set_odu16_ru_date_time_table'
    set_odu16_ru_date_time_table_id = Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    year  = Column(INTEGER) 		
    month = Column(INTEGER) 	
    day= Column(INTEGER) 		
    hour = Column(INTEGER) 
    min = Column(INTEGER)
    sec = Column(INTEGER)
    def __init__(self,config_profile_id,year,month,day,hour,min,sec):
        self.set_odu16_ru_date_time_table_id = None
        self.config_profile_id = config_profile_id
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.min=min
        self.sec=sec
        
    def __repr__(self):
        return "SetOdu16RUConfTable<'%s','%s','%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_ru_date_time_table_id,self.config_profile_id,self.year,self.month,self.day,self.hour,self.min,self.sec)

#set_odu16_sync_config_table Table
class SetOdu16SyncConfigTable(Base):
    """
    set_odu16_sync_config_table Table
    """
    __tablename__= 'set_odu16_sync_config_table'
    set_odu16_sync_config_table_id  = Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    adminStatus =Column(SMALLINT)
    raster_time  = Column(INTEGER) 		
    num_slaves = Column(INTEGER) 	
    sync_loss_threshold= Column(INTEGER) 		
    leaky_bucket_timer = Column(INTEGER) 
    sync_lost_timeout = Column(INTEGER)
    sync_config_time_adjust = Column(INTEGER)
    sync_config_broadcast_enable = Column(SMALLINT)
    def __init__(self,config_profile_id,adminStatus,raster_time,num_slaves,sync_loss_threshold,leaky_bucket_timer,sync_lost_timeout,sync_config_time_adjust):
        self.set_odu16_sync_config_table_id= None
        self.config_profile_id = config_profile_id
        self.adminStatus=adminStatus
        self.raster_time=raster_time
        self.num_slaves=num_slaves
        self.sync_loss_threshold=sync_loss_threshold
        self.leaky_bucket_timer=leaky_bucket_timer
        self.sync_lost_timeout=sync_lost_timeout
        self.sync_config_time_adjust=sync_config_time_adjust
        
    def __repr__(self):
        return "SetOdu16SyncConfigTable<'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'>" %(self.set_odu16_sync_config_table_id,self.config_profile_id,self.adminStatus,self.raster_time,self.num_slaves,self.sync_loss_threshold,self.leaky_bucket_timer,self.sync_lost_timeout,self.sync_config_time_adjust,self.sync_config_broadcast_enable)

#set_odu16_misc Table
class SetOdu16Misc(Base):
    """
    set_odu16_misc Table
    """
    __tablename__= 'set_odu16_misc'
    set_odu16_misc_id = Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    sys_contact = Column(VARCHAR(256)) 		
    sys_name = Column(VARCHAR(256)) 	
    sys_location = Column(VARCHAR(256)) 		
    snmp_enable_authen_traps = Column(SMALLINT) 
    def __init__(self,config_profile_id,sys_contact,sys_name,sys_location,snmp_enable_authen_traps):
        self.set_odu16_misc_id = None
        self.config_profile_id = config_profile_id
        self.sys_contact= sys_contact
        self.sys_name= sys_name
        self.sys_location = sys_location
        self.snmp_enable_authen_traps = snmp_enable_authen_traps 
        
    def __repr__(self):
        return "SetOdu16Misc<'%s','%s','%s','%s','%s','%s'>" % (self.set_odu16_misc_id,self.config_profile_id,self.sys_contact,self.sys_name,self.sys_location,self.snmp_enable_authen_traps)

#set_odu16_sys_omc_registration_table  Table
class SetOdu16SysOmcRegistrationTable(Base):
    """
    set_odu16_sys_omc_registration_table  
    """
    __tablename__ = 'set_odu16_sys_omc_registration_table'
    set_odu16_sys_omc_registration_table_id =Column(INTEGER,primary_key=True) 
    config_profile_id =	Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    sys_omc_register_contact_addr =	Column(VARCHAR(128))	
    sys_omc_register_contact_person =Column(VARCHAR(32))
    sys_omc_register_contact_mobile =Column(VARCHAR(16))
    sys_omc_register_alternate_contact =Column(VARCHAR(64))
    sys_omc_register_contact_email =Column(VARCHAR(64))	
    sys_omc_register_active_card_hwld = Column(VARCHAR(30)) 	
    sys_omc_registerne_site_direction =	Column(VARCHAR(30)) 
    sys_omc_registerne_site_landmark =Column(VARCHAR(30)) 	
    sys_omc_registerne_site_latitude =Column(VARCHAR(30)) 	
    sys_omc_registerne_site_longitude =Column(VARCHAR(30)) 	
    sys_omc_registerne_state =Column(VARCHAR(30)) 	
    sys_omc_register_country =Column(VARCHAR(30)) 
    sys_omc_register_city =Column(VARCHAR(30)) 	
    sys_omc_register_sitebldg =Column(VARCHAR(30)) 
    sys_omc_registersitefloor =Column(VARCHAR(30))
    site_mac = Column(VARCHAR(32))
    product_id = Column(INT)
    
    def __init__(self,config_profile_id,sys_omc_register_contact_addr,sys_omc_register_contact_person,sys_omc_register_contact_mobile ,sys_omc_register_alternate_contact,sys_omc_register_contact_email,\
                sys_omc_register_active_card_hwld,sys_omc_registerne_site_direction,sys_omc_registerne_site_landmark,sys_omc_registerne_site_latitude,\
                sys_omc_registerne_site_longitude,sys_omc_registerne_state,sys_omc_register_country,sys_omc_register_city,sys_omc_register_sitebldg,\
                sys_omc_registersitefloor,site_mac,product_id):
        self.set_odu16_sys_omc_registration_table_id = None
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
        self.site_mac = site_mac
        self.product_id = product_id
        
    def __repr__(self):
        return "SetOdu16Misc<'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'>" % (self.set_odu16_sys_omc_registration_table_id,self.config_profile_id,self.sys_omc_register_contact_addr,self.sys_omc_register_contact_person,self.sys_omc_register_contact_mobile\
     ,self.sys_omc_register_alternate_contact,self.sys_omc_register_contact_email,\
        self.sys_omc_register_active_card_hwld,\
        self.sys_omc_registerne_site_direction,\
        self.sys_omc_registerne_site_landmark,\
        self.sys_omc_registerne_site_latitude,\
        self.sys_omc_registerne_site_longitude,\
        self.sys_omc_registerne_state,\
        self.sys_omc_register_country, \
        self.sys_omc_register_city, \
        self.sys_omc_register_sitebldg ,\
        self.sys_omc_registersitefloor,\
        self.site_mac,\
        self.product_id
        )

class GetOdu16_ru_conf_table(Base):
	__tablename__= "get_odu16_ru_conf_table"
	get_odu16_ru_conf_table_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	op_state = Column(SMALLINT)
	object_model_version = Column(VARCHAR)
	default_node_type = Column(SMALLINT)
	no_radio_interfaces = Column(INT)

	def __init__(self,host_id,op_state,object_model_version,default_node_type,no_radio_interfaces):
		self.get_odu16_ru_conf_table_id = None
		self.host_id = host_id
		self.op_state = op_state
		self.object_model_version = object_model_version
		self.default_node_type = default_node_type
		self.no_radio_interfaces = no_radio_interfaces

		
	def __repr__(self):
		return "<GetOdu16_ru_conf_table('%s','%s','%s','%s','%s','%s')>" %(self.get_odu16_ru_conf_table_id,self.host_id,self.op_state,self.object_model_version,self.default_node_type,self.no_radio_interfaces)

# Class for get_odu16_ra_status_table
class GetOdu16RaStatusTable(Base):
	__tablename__= "get_odu16_ra_status_table"
	get_odu16_ra_status_table_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	current_timeslot = Column(SMALLINT)
	ra_mac_address = Column(VARCHAR)

	def __init__(self,host_id,current_timeslot,ra_mac_address):
		self.get_odu16_ra_status_table_id = None
		self.host_id = host_id
		self.current_timeslot = current_timeslot
		self.ra_mac_address = ra_mac_address

	def __repr__(self):
		return "<GetOdu16RaStatusTable('%s','%s','%s','%s')>" %										(self.get_odu16_ra_status_table_id,self.host_id,self.current_timeslot,self.ra_mac_address)



#CREATE enum_index AS Enum ('1','2','3','4','5','6','7','8')

class GetOdu16PeerNodeStatusTable(Base):
	__tablename__= "get_odu16_peer_node_status_table"
	get_odu16_peer_node_status_table_id = Column(INTEGER,primary_key=True)
	host_id = Column(VARCHAR(64))
	link_status = Column(VARCHAR(16))
	tunnel_status = Column(VARCHAR(16))
	sig_strength = Column(INT)
	peer_mac_addr = Column(VARCHAR(32))
	ssidentifier = Column(VARCHAR(32))
	peer_node_status_raster_time = Column(INT)
	peer_node_status_num_slaves = Column(Enum('1','2','3','4','5','6','7','8',name='enumslaves'))
	peer_node_status_timer_adjust = Column(INT)
	peer_node_status_rf_config = Column(VARCHAR(16))
	index = Column(Enum('1','2','3','4','5','6','7','8',name='enumIndex'))
	timeslot_index = Column(Enum('1','2','3','4','5','6','7','8',name='enumtimeslot'))
	timestamp = Column(TIMESTAMP)
	

	def __init__(self,host_id,link_status,tunnel_status,sig_strength,peer_mac_addr,ssidentifier,peer_node_status_raster_time,peer_node_status_num_slaves,peer_node_status_timer_adjust,peer_node_status_rf_config,index,timeslot_index,timestamp):
		self.get_odu16_peer_node_status_table_id = None
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
		return "<GetOdu16PeerNodeStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.get_odu16_peer_node_status_table_id,self.host_id,self.link_status,self.tunnel_status,self.sig_strength,self.peer_mac_addr,self.ssidentifier,self.peer_node_status_raster_time,self.peer_node_status_num_slaves,self.peer_node_status_timer_adjust,self.peer_node_status_rf_config,self.index,self.timeslot_index,self.timestamp)

class GetOdu16SWStatusTable(Base):
	__tablename__= "get_odu16_sw_status_table"
	get_odu16_sw_status_table_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	active_version = Column(VARCHAR(32))
	passive_version = Column(VARCHAR(32))
	bootloader_version = Column(VARCHAR(64))

	def __init__(self,host_id,active_version,passive_version,bootloader_version):
		self.get_odu16_sw_status_table_id = None
		self.host_id = host_id
		self.active_version = active_version
		self.passive_version = passive_version
		self.bootloader_version = bootloader_version
		
	def __repr__(self):
		return "<GetOdu16_sw_status_table('%s','%s','%s','%s','%s')>" %(self.get_odu16_sw_status_table_id,self.host_id,self.active_version,self.passive_version,self.bootloader_version)

class GetOdu16HWDescTable(Base):
	__tablename__= "get_odu16_hw_desc_table"
	get_odu16_hw_desc_table_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	hw_version = Column(VARCHAR(128))
	hw_serial_no = Column(VARBINARY(64))

	def __init__(self,host_id,hw_version,hw_serial_no):
		self.get_odu16_hw_desc_table_id = None
		self.host_id = host_id
		self.hw_version = hw_version
		self.hw_serial_no = hw_serial_no
		
	def __repr__(self):
		return "<GetOdu16_hw_desc_table('%s','%s','%s','%s')>" %(self.get_odu16_hw_desc_table_id,self.host_id,self.hw_version,self.hw_serial_no)

class GetOdu16RAScanListTable(Base):
	__tablename__= "get_odu16_ra_scan_list_table"
	get_odu16_ra_scan_list_table_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	ssid = Column(VARCHAR(32))
	signal_strength = Column(INTEGER)
	mac_addr = Column(VARCHAR(24))
	raster_time = Column(INTEGER)
	timeslot = Column(INTEGER)
	max_slaves = Column(INTEGER)
	rf_coding = Column(SMALLINT)
	channel_num = Column(INTEGER)

	def __init__(self,host_id,ssid,signal_strength,mac_addr,raster_time,timeslot,max_slaves,rf_coding,channel_num):
		self.get_odu16_ra_scan_list_table_id = None
		self.host_id = host_id
		self.ssid = ssid
		self.signal_strength = signal_strength
		self.mac_addr = mac_addr
		self.raster_time = raster_time
		self.timeslot = timeslot
		self.max_slaves = max_slaves
		self.rf_coding = rf_coding
		self.channel_num = channel_num
		
	def __repr__(self):
		return "<GetOdu16_ra_scan_list_table('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.get_odu16_ra_scan_list_table_id,self.host_id,self.ssid,self.signal_strength,self.mac_addr,self.raster_time,self.timeslot,self.max_slaves,self.rf_coding,self.channel_num)

############################## Odu16 ##########################################

############################# odu100 Tables ###################################

class Odu100EswATUConfigTable(Base):
	__tablename__= "odu100_eswATUConfigTable"
	odu100_eswATUConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswATUConfigAtuId = Column(INTEGER)
	eswATUConfigEntryType = Column(INTEGER)
	eswATUConfigPriorityVal = Column(INTEGER)
	eswATUConfigMacAddress = Column(VARCHAR(32))
	eswATUConfigMemberPorts = Column(INTEGER)
	eswATUConfigRowStatus = Column(INTEGER)

	def __init__(self,config_profile_id,eswATUConfigAtuId,eswATUConfigEntryType,eswATUConfigPriorityVal,eswATUConfigMacAddress,eswATUConfigMemberPorts,eswATUConfigRowStatus):
		self.odu100_eswATUConfigTable_id = None
		self.config_profile_id = config_profile_id
		self.eswATUConfigAtuId = eswATUConfigAtuId
		self.eswATUConfigEntryType = eswATUConfigEntryType
		self.eswATUConfigPriorityVal = eswATUConfigPriorityVal
		self.eswATUConfigMacAddress = eswATUConfigMacAddress
		self.eswATUConfigMemberPorts = eswATUConfigMemberPorts
		self.eswATUConfigRowStatus = eswATUConfigRowStatus
		
	def __repr__(self):
		return "<Odu100EswATUConfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswATUConfigTable_id,self.config_profile_id,self.eswATUConfigAtuId,self.eswATUConfigEntryType,self.eswATUConfigPriorityVal,self.eswATUConfigMacAddress,self.eswATUConfigMemberPorts,self.eswATUConfigRowStatus)

class Odu100EswBadFramesTable(Base):
	__tablename__= "odu100_eswBadFramesTable"
	odu100_eswBadFramesTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
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

	def __init__(self,host_id,eswBadFramesPortNum,eswBadFramesInUndersizeRx,eswBadFramesInFragmentsRx,eswBadFramesInOversizeRx,eswBadFramesInJabberRx,eswBadFramesInFCSErrRx,eswBadFramesOutFCSErrTx,eswBadFramesDeferredTx,eswBadFramesCollisionsTx,eswBadFramesLateTx,eswBadFramesExcessiveTx,eswBadFramesSingleTx,eswBadFramesMultipleTx):
		self.odu100_eswBadFramesTable_id = None
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
		return "<Odu100EswBadFramesTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswBadFramesTable_id,self.host_id,self.eswBadFramesPortNum,self.eswBadFramesInUndersizeRx,self.eswBadFramesInFragmentsRx,self.eswBadFramesInOversizeRx,self.eswBadFramesInJabberRx,self.eswBadFramesInFCSErrRx,self.eswBadFramesOutFCSErrTx,self.eswBadFramesDeferredTx,self.eswBadFramesCollisionsTx,self.eswBadFramesLateTx,self.eswBadFramesExcessiveTx,self.eswBadFramesSingleTx,self.eswBadFramesMultipleTx)

class Odu100EswGoodFramesTable(Base):
	__tablename__= "odu100_eswGoodFramesTable"
	odu100_eswGoodFramesTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	eswGoodFramesPortNum = Column(INTEGER)
	eswGoodFramesInUnicast = Column(INTEGER)
	eswGoodFramesOutUnicast = Column(INTEGER)
	eswGoodFramesInBCast = Column(INTEGER)
	eswGoodFramesOutBCast = Column(INTEGER)
	eswGoodFramesInMCast = Column(INTEGER)
	eswGoodFramesOutMcast = Column(INTEGER)

	def __init__(self,host_id,eswGoodFramesPortNum,eswGoodFramesInUnicast,eswGoodFramesOutUnicast,eswGoodFramesInBCast,eswGoodFramesOutBCast,eswGoodFramesInMCast,eswGoodFramesOutMcast):
		self.odu100_eswGoodFramesTable_id = None
		self.host_id = host_id
		self.eswGoodFramesPortNum = eswGoodFramesPortNum
		self.eswGoodFramesInUnicast = eswGoodFramesInUnicast
		self.eswGoodFramesOutUnicast = eswGoodFramesOutUnicast
		self.eswGoodFramesInBCast = eswGoodFramesInBCast
		self.eswGoodFramesOutBCast = eswGoodFramesOutBCast
		self.eswGoodFramesInMCast = eswGoodFramesInMCast
		self.eswGoodFramesOutMcast = eswGoodFramesOutMcast
		
	def __repr__(self):
		return "<Odu100EswGOOdFramesTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswGoodFramesTable_id,self.host_id,self.eswGoodFramesPortNum,self.eswGoodFramesInUnicast,self.eswGoodFramesOutUnicast,self.eswGoodFramesInBCast,self.eswGoodFramesOutBCast,self.eswGoodFramesInMCast,self.eswGoodFramesOutMcast)

class Odu100EswMirroringPortTable(Base):
	__tablename__= "odu100_eswMirroringPortTable"
	odu100_eswMirroringPortTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswMirroringPortIndexId = Column(INTEGER)
	eswMirroringPort = Column(INTEGER)
	eswMirroringPortSecond = Column(INTEGER)

	def __init__(self,config_profile_id,eswMirroringPortIndexId,eswMirroringPort,eswMirroringPortSecond):
		self.odu100_eswMirroringPortTable_id = None
		self.config_profile_id = config_profile_id
		self.eswMirroringPortIndexId = eswMirroringPortIndexId
		self.eswMirroringPort = eswMirroringPort
		self.eswMirroringPortSecond = eswMirroringPortSecond
		
	def __repr__(self):
		return "<Odu100EswMirrOringPOrtTable('%s','%s','%s','%s','%s')>" %(self.odu100_eswMirroringPortTable_id,self.config_profile_id,self.eswMirroringPortIndexId,self.eswMirroringPort,self.eswMirroringPortSecond)

class Odu100EswPortAccessListTable(Base):
	__tablename__= "odu100_eswPortAccessListTable"
	odu100_eswPortAccessListTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswPortACLPortNum = Column(INTEGER)
	eswPortACLSecIndex = Column(INTEGER)
	eswPortACLMacAddress = Column(VARCHAR(32))

	def __init__(self,config_profile_id,eswPortACLPortNum,eswPortACLSecIndex,eswPortACLMacAddress):
		self.odu100_eswPortAccessListTable_id = None
		self.config_profile_id = config_profile_id
		self.eswPortACLPortNum = eswPortACLPortNum
		self.eswPortACLSecIndex = eswPortACLSecIndex
		self.eswPortACLMacAddress = eswPortACLMacAddress
		
	def __repr__(self):
		return "<Odu100EswPOrtAccessListTable('%s','%s','%s','%s','%s')>" %(self.odu100_eswPortAccessListTable_id,self.config_profile_id,self.eswPortACLPortNum,self.eswPortACLSecIndex,self.eswPortACLMacAddress)

class Odu100EswPortBwTable(Base):
	__tablename__= "odu100_eswPortBwTable"
	odu100_eswPortBwTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswPortBwPortNum = Column(INTEGER)
	eswPortBwEgressBw = Column(INTEGER)
	eswPortBwIngressBw = Column(INTEGER)

	def __init__(self,config_profile_id,eswPortBwPortNum,eswPortBwEgressBw,eswPortBwIngressBw):
		self.odu100_eswPortBwTable_id = None
		self.config_profile_id = config_profile_id
		self.eswPortBwPortNum = eswPortBwPortNum
		self.eswPortBwEgressBw = eswPortBwEgressBw
		self.eswPortBwIngressBw = eswPortBwIngressBw
		
	def __repr__(self):
		return "<Odu100EswPOrtBwTable('%s','%s','%s','%s','%s')>" %(self.odu100_eswPortBwTable_id,self.config_profile_id,self.eswPortBwPortNum,self.eswPortBwEgressBw,self.eswPortBwIngressBw)

class Odu100EswPortConfigTable(Base):
	__tablename__= "odu100_eswPortConfigTable"
	odu100_eswPortConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswPortConfigPortNum = Column(INTEGER)
	eswPortConfigAdminState = Column(INTEGER)
	eswPortConfigLinkMode = Column(INTEGER)
	eswPortConfigPortVid = Column(INTEGER)
	eswPortConfigAuthState = Column(INTEGER)
	eswPortConfigMirrDir = Column(INTEGER)
	eswPortConfigDotqMode = Column(INTEGER)
	eswPortConfigMacFlowControl = Column(INTEGER)

	def __init__(self,config_profile_id,eswPortConfigPortNum,eswPortConfigAdminState,eswPortConfigLinkMode,eswPortConfigPortVid,eswPortConfigAuthState,eswPortConfigMirrDir,eswPortConfigDotqMode,eswPortConfigMacFlowControl):
		self.odu100_eswPortConfigTable_id = None
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
		return "<Odu100EswPOrtCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswPortConfigTable_id,self.config_profile_id,self.eswPortConfigPortNum,self.eswPortConfigAdminState,self.eswPortConfigLinkMode,self.eswPortConfigPortVid,self.eswPortConfigAuthState,self.eswPortConfigMirrDir,self.eswPortConfigDotqMode,self.eswPortConfigMacFlowControl)

class Odu100EswPortQinQTable(Base):
	__tablename__= "odu100_eswPortQinQTable"
	odu100_eswPortQinQTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswPortQinQPortNum = Column(INTEGER)
	eswPortQinQAuthState = Column(INTEGER)
	eswPortQinQProviderTag = Column(INTEGER)

	def __init__(self,config_profile_id,eswPortQinQPortNum,eswPortQinQAuthState,eswPortQinQProviderTag):
		self.odu100_eswPortQinQTable_id = None
		self.config_profile_id = config_profile_id
		self.eswPortQinQPortNum = eswPortQinQPortNum
		self.eswPortQinQAuthState = eswPortQinQAuthState
		self.eswPortQinQProviderTag = eswPortQinQProviderTag
		
	def __repr__(self):
		return "<Odu100EswPOrtQinQTable('%s','%s','%s','%s','%s')>" %(self.odu100_eswPortQinQTable_id,self.config_profile_id,self.eswPortQinQPortNum,self.eswPortQinQAuthState,self.eswPortQinQProviderTag)

class Odu100EswPortStatisticsTable(Base):
	__tablename__= "odu100_eswPortStatisticsTable"
	odu100_eswPortStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	eswPortStatisticsPortNum = Column(INTEGER)
	eswPortStatisticsInDiscards = Column(INTEGER)
	eswPortStatisticsInGoodOctets = Column(INTEGER)
	eswPortStatisticsInBadOctets = Column(INTEGER)
	eswPortStatisticsOutOctets = Column(INTEGER)

	def __init__(self,host_id,eswPortStatisticsPortNum,eswPortStatisticsInDiscards,eswPortStatisticsInGoodOctets,eswPortStatisticsInBadOctets,eswPortStatisticsOutOctets):
		self.odu100_eswPortStatisticsTable_id = None
		self.host_id = host_id
		self.eswPortStatisticsPortNum = eswPortStatisticsPortNum
		self.eswPortStatisticsInDiscards = eswPortStatisticsInDiscards
		self.eswPortStatisticsInGoodOctets = eswPortStatisticsInGoodOctets
		self.eswPortStatisticsInBadOctets = eswPortStatisticsInBadOctets
		self.eswPortStatisticsOutOctets = eswPortStatisticsOutOctets
		
	def __repr__(self):
		return "<Odu100EswPOrtStatisticsTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswPortStatisticsTable_id,self.host_id,self.eswPortStatisticsPortNum,self.eswPortStatisticsInDiscards,self.eswPortStatisticsInGoodOctets,self.eswPortStatisticsInBadOctets,self.eswPortStatisticsOutOctets)

class Odu100EswPortStatusTable(Base):
	__tablename__= "odu100_eswPortStatusTable"
	odu100_eswPortStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	eswPortStatusPortNum = Column(INTEGER)
	eswPortStatusOpState = Column(INTEGER)
	eswPortStatusLinkSpeed = Column(INTEGER)
	eswPortStatusMacFlowControl = Column(INTEGER)

	def __init__(self,host_id,eswPortStatusPortNum,eswPortStatusOpState,eswPortStatusLinkSpeed,eswPortStatusMacFlowControl):
		self.odu100_eswPortStatusTable_id = None
		self.host_id = host_id
		self.eswPortStatusPortNum = eswPortStatusPortNum
		self.eswPortStatusOpState = eswPortStatusOpState
		self.eswPortStatusLinkSpeed = eswPortStatusLinkSpeed
		self.eswPortStatusMacFlowControl = eswPortStatusMacFlowControl
		
	def __repr__(self):
		return "<Odu100EswPOrtStatusTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswPortStatusTable_id,self.host_id,self.eswPortStatusPortNum,self.eswPortStatusOpState,self.eswPortStatusLinkSpeed,self.eswPortStatusMacFlowControl)

class Odu100EswVlanConfigTable(Base):
	__tablename__= "odu100_eswVlanConfigTable"
	odu100_eswVlanConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	eswVlanConfigVlanId = Column(INTEGER)
	eswVlanConfigVlanName = Column(VARCHAR(8))
	eswVlanConfigVlanType = Column(INTEGER)
	eswVlanConfigVlanTag = Column(INTEGER)
	eswVlanConfigMemberPorts = Column(INTEGER)
	eswVlanConfigRowStatus = Column(INTEGER)

	def __init__(self,config_profile_id,eswVlanConfigVlanId,eswVlanConfigVlanName,eswVlanConfigVlanType,eswVlanConfigVlanTag,eswVlanConfigMemberPorts,eswVlanConfigRowStatus):
		self.odu100_eswVlanConfigTable_id = None
		self.config_profile_id = config_profile_id
		self.eswVlanConfigVlanId = eswVlanConfigVlanId
		self.eswVlanConfigVlanName = eswVlanConfigVlanName
		self.eswVlanConfigVlanType = eswVlanConfigVlanType
		self.eswVlanConfigVlanTag = eswVlanConfigVlanTag
		self.eswVlanConfigMemberPorts = eswVlanConfigMemberPorts
		self.eswVlanConfigRowStatus = eswVlanConfigRowStatus
		
	def __repr__(self):
		return "<Odu100EswVlanCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_eswVlanConfigTable_id,self.config_profile_id,self.eswVlanConfigVlanId,self.eswVlanConfigVlanName,self.eswVlanConfigVlanType,self.eswVlanConfigVlanTag,self.eswVlanConfigMemberPorts,self.eswVlanConfigRowStatus)

class Odu100HwDescTable(Base):
	__tablename__= "odu100_hwDescTable"
	odu100_hwDescTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	hwDescIndex = Column(INTEGER)
	hwVersion = Column(VARCHAR(128))
	hwSerialNo = Column(VARCHAR(64))

	def __init__(self,host_id,hwDescIndex,hwVersion,hwSerialNo):
		self.odu100_hwDescTable_id = None
		self.host_id = host_id
		self.hwDescIndex = hwDescIndex
		self.hwVersion = hwVersion
		self.hwSerialNo = hwSerialNo
		
	def __repr__(self):
		return "<Odu100HwDescTable('%s','%s','%s','%s','%s')>" %(self.odu100_hwDescTable_id,self.host_id,self.hwDescIndex,self.hwVersion,self.hwSerialNo)

class Odu100IpConfigTable(Base):
    __tablename__= "odu100_ipConfigTable"
    odu100_ipConfigTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    ipConfigIndex = Column(INTEGER)
    adminState = Column(INTEGER)
    ipAddress = Column(VARCHAR(32))
    ipNetworkMask = Column(VARCHAR(32))
    ipDefaultGateway = Column(VARCHAR(32))
    autoIpConfig = Column(INTEGER)
    managementMode  = Column(TINYINT)
    managementVlanTag  = Column(INTEGER)

    def __init__(self,config_profile_id,ipConfigIndex,adminState,ipAddress,ipNetworkMask,ipDefaultGateway,autoIpConfig,managementMode=0,managementVlanTag=0):
        self.odu100_ipConfigTable_id = None
        self.config_profile_id = config_profile_id
        self.ipConfigIndex = ipConfigIndex
        self.adminState = adminState
        self.ipAddress = ipAddress
        self.ipNetworkMask = ipNetworkMask
        self.ipDefaultGateway = ipDefaultGateway
        self.autoIpConfig = autoIpConfig
        self.managementMode = managementMode
        self.managementVlanTag = managementVlanTag
        
    def __repr__(self):
        return "<Odu100IpCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_ipConfigTable_id,self.config_profile_id,self.ipConfigIndex,self.adminState,self.ipAddress,self.ipNetworkMask,self.ipDefaultGateway,self.autoIpConfig,self.managementMode,self.managementVlanTag)

class Odu100NwInterfaceStatisticsTable(Base):
	__tablename__= "odu100_nwInterfaceStatisticsTable"
	odu100_nwInterfaceStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	nwStatsIndex = Column(INTEGER)
	rxPackets = Column(INTEGER)
	txPackets = Column(INTEGER)
	rxBytes = Column(INTEGER)
	txBytes = Column(INTEGER)
	rxErrors = Column(INTEGER)
	txErrors = Column(INTEGER)
	rxDropped = Column(INTEGER)
	txDropped = Column(INTEGER)

	def __init__(self,host_id,nwStatsIndex,rxPackets,txPackets,rxBytes,txBytes,rxErrors,txErrors,rxDropped,txDropped):
		self.odu100_nwInterfaceStatisticsTable_id = None
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
		return "<Odu100NwInterfaceStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_nwInterfaceStatisticsTable_id,self.host_id,self.nwStatsIndex,self.rxPackets,self.txPackets,self.rxBytes,self.txBytes,self.rxErrors,self.txErrors,self.rxDropped,self.txDropped)

class Odu100NwInterfaceStatusTable(Base):
	__tablename__= "odu100_nwInterfaceStatusTable"
	odu100_nwInterfaceStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	nwStatusIndex = Column(INTEGER)
	nwInterfaceName = Column(VARCHAR(16))
	operationalState = Column(INTEGER)
	macAddress = Column(VARCHAR(32))

	def __init__(self,host_id,nwStatusIndex,nwInterfaceName,operationalState,macAddress):
		self.odu100_nwInterfaceStatusTable_id = None
		self.host_id = host_id
		self.nwStatusIndex = nwStatusIndex
		self.nwInterfaceName = nwInterfaceName
		self.operationalState = operationalState
		self.macAddress = macAddress
		
	def __repr__(self):
		return "<Odu100NwInterfaceStatusTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_nwInterfaceStatusTable_id,self.host_id,self.nwStatusIndex,self.nwInterfaceName,self.operationalState,self.macAddress)

class Odu100OmcConfTable(Base):
	__tablename__= "odu100_omcConfTable"
	odu100_omcConfTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	omcConfIndex = Column(INTEGER)
	omcIpAddress = Column(VARCHAR(32))
	periodicStatsTimer = Column(INTEGER)

	def __init__(self,config_profile_id,omcConfIndex,omcIpAddress,periodicStatsTimer):
		self.odu100_omcConfTable_id = None
		self.config_profile_id = config_profile_id
		self.omcConfIndex = omcConfIndex
		self.omcIpAddress = omcIpAddress
		self.periodicStatsTimer = periodicStatsTimer
		
	def __repr__(self):
		return "<Odu100OmcCOnfTable('%s','%s','%s','%s','%s')>" %(self.odu100_omcConfTable_id,self.config_profile_id,self.omcConfIndex,self.omcIpAddress,self.periodicStatsTimer)

class Odu100PeerConfigTable(Base):
    __tablename__= "odu100_peerConfigTable"
    odu100_peerConfigTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    timeslotIndex = Column(INTEGER)
    peerMacAddress = Column(VARCHAR(32))
    guaranteedUplinkBW = Column(INTEGER)
    guaranteedDownlinkBW = Column(INTEGER)
    basicrateMCSIndex = Column(INTEGER)
    maxUplinkBW = Column(INTEGER)
    maxDownlinkBW = Column(INTEGER)

    def __init__(self,config_profile_id,raIndex,timeslotIndex,peerMacAddress,guaranteedUplinkBW,guaranteedDownlinkBW,basicrateMCSIndex,maxUplinkBW,maxDownlinkBW):
        self.odu100_peerConfigTable_id = None
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.timeslotIndex = timeslotIndex
        self.peerMacAddress = peerMacAddress
        self.guaranteedUplinkBW = guaranteedUplinkBW
        self.guaranteedDownlinkBW = guaranteedDownlinkBW
        self.basicrateMCSIndex = basicrateMCSIndex
        self.maxUplinkBW = maxUplinkBW
        self.maxDownlinkBW = maxDownlinkBW
        
    def __repr__(self):
        return "<Odu100PeerCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_peerConfigTable_id,self.config_profile_id,self.raIndex,self.timeslotIndex,self.peerMacAddress,self.guaranteedUplinkBW,self.guaranteedDownlinkBW,self.basicrateMCSIndex,self.maxUplinkBW,self.maxDownlinkBW)

class Odu100PeerLinkStatisticsTable(Base):
	__tablename__= "odu100_peerLinkStatisticsTable"
	odu100_peerLinkStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
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

	def __init__(self,host_id,raIndex,timeslotindex,txdroped,rxDataSubFrames,txDataSubFrames,signalstrength1,txRetransmissions5,txRetransmissions4,txRetransmissions3,txRetransmissions2,txRetransmissions1,txRetransmissions0,rxRetransmissions5,rxRetransmissions4,rxRetransmissions3,rxRetransmissions2,rxRetransmissions1,rxRetransmissions0,rxBroadcastDataSubFrames,rateIncreases,rateDecreases,emptyRasters,rxDroppedTpPkts,rxDroppedRadioPkts,signalstrength2):
		self.odu100_peerLinkStatisticsTable_id = None
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
		return "<Odu100PeerLinkStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_peerLinkStatisticsTable_id,self.host_id,self.raIndex,self.timeslotindex,self.txdroped,self.rxDataSubFrames,self.txDataSubFrames,self.signalstrength1,self.txRetransmissions5,self.txRetransmissions4,self.txRetransmissions3,self.txRetransmissions2,self.txRetransmissions1,self.txRetransmissions0,self.rxRetransmissions5,self.rxRetransmissions4,self.rxRetransmissions3,self.rxRetransmissions2,self.rxRetransmissions1,self.rxRetransmissions0,self.rxBroadcastDataSubFrames,self.rateIncreases,self.rateDecreases,self.emptyRasters,self.rxDroppedTpPkts,self.rxDroppedRadioPkts,self.signalstrength2)



class Odu100PeerRateStatisticsTable(Base):
	__tablename__= "odu100_peerRateStatisticsTable"
	odu100_peerRateStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	raIndex = Column(INTEGER)
	mcsIndex = Column(INTEGER)
	timeSlotindex = Column(INTEGER)
	peerrate = Column(INTEGER)
	per = Column(INTEGER)
	ticks = Column(INTEGER)
	ticksMinimumRateTx = Column(INTEGER)
	ticksWasted = Column(INTEGER)

	def __init__(self,host_id,raIndex,mcsIndex,timeSlotindex,peerrate,per,ticks,ticksMinimumRateTx,ticksWasted):
		self.odu100_peerRateStatisticsTable_id = None
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
		return "<Odu100PeerRateStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_peerRateStatisticsTable_id,self.host_id,self.raIndex,self.mcsIndex,self.timeSlotindex,self.peerrate,self.per,self.ticks,self.ticksMinimumRateTx,self.ticksWasted)

class Odu100PeerTunnelStatisticsTable(Base):
	__tablename__= "odu100_peerTunnelStatisticsTable"
	odu100_peerTunnelStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	raIndex = Column(INTEGER)
	tsIndex = Column(INTEGER)
	rxPacket = Column(INTEGER)
	txPacket = Column(INTEGER)
	rxBundles = Column(INTEGER)
	txBundles = Column(INTEGER)
	rxDroped = Column(INTEGER)
	txDroped = Column(INTEGER)

	def __init__(self,host_id,raIndex,tsIndex,rxPacket,txPacket,rxBundles,txBundles,rxDroped,txDroped):
		self.odu100_peerTunnelStatisticsTable_id = None
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
		return "<Odu100PeerTunnelStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_peerTunnelStatisticsTable_id,self.host_id,self.raIndex,self.tsIndex,self.rxPacket,self.txPacket,self.rxBundles,self.txBundles,self.rxDroped,self.txDroped)

class Odu100PeerNodeStatusTable(Base):
	__tablename__= "odu100_peerNodeStatusTable"
	odu100_peerNodeStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
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
	timestamp = Column(DATETIME)

	def __init__(self,host_id,raIndex,timeSlotIndex,linkStatus,tunnelStatus,sigStrength1,peerMacAddr,ssIdentifier,peerNodeStatusNumSlaves,peerNodeStatusrxRate,peerNodeStatustxRate,allocatedTxBW,allocatedRxBW,usedTxBW,usedRxBW,txbasicRate,sigStrength2,rxbasicRate,txLinkQuality,peerNodeStatustxTime,peerNodeStatusrxTime,timestamp):
		self.odu100_peerNodeStatusTable_id = None
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
		return "<Odu100PeerNodeStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_peerNodeStatusTable_id,self.host_id,self.raIndex,self.timeSlotIndex,self.linkStatus,self.tunnelStatus,self.sigStrength1,self.peerMacAddr,self.ssIdentifier,self.peerNodeStatusNumSlaves,self.peerNodeStatusrxRate,self.peerNodeStatustxRate,self.allocatedTxBW,self.allocatedRxBW,self.usedTxBW,self.usedRxBW,self.txbasicRate,self.sigStrength2,self.rxbasicRate,self.txLinkQuality,self.peerNodeStatustxTime,self.peerNodeStatusrxTime,self.timestamp)

class Odu100RaAclConfigTable(Base):
	__tablename__= "odu100_raAclConfigTable"
	odu100_raAclConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	raIndex = Column(INTEGER)
	aclIndex = Column(INTEGER)
	macaddress = Column(VARCHAR(32))
	rowSts = Column(INTEGER)

	def __init__(self,config_profile_id,raIndex,aclIndex,macaddress,rowSts):
		self.odu100_raAclConfigTable_id = None
		self.config_profile_id = config_profile_id
		self.raIndex = raIndex
		self.aclIndex = aclIndex
		self.macaddress = macaddress
		self.rowSts = rowSts
		
	def __repr__(self):
		return "<Odu100RaAclCOnfigTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_raAclConfigTable_id,self.config_profile_id,self.raIndex,self.aclIndex,self.macaddress,self.rowSts)

class Odu100RaChannelListTable(Base):
	__tablename__= "odu100_raChannelListTable"
	odu100_raChannelListTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	raIndex = Column(INTEGER)
	raChanIndex = Column(INTEGER)
	channelNumber = Column(INTEGER)
	frequency = Column(INTEGER)

	def __init__(self,host_id,raIndex,raChanIndex,channelNumber,frequency):
		self.odu100_raChannelListTable_id = None
		self.host_id = host_id
		self.raIndex = raIndex
		self.raChanIndex = raChanIndex
		self.channelNumber = channelNumber
		self.frequency = frequency
		
	def __repr__(self):
		return "<Odu100RaChannelListTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_raChannelListTable_id,self.host_id,self.raIndex,self.raChanIndex,self.channelNumber,self.frequency)


class FirmwareMapping(Base):
	__tablename__= "firmware_mapping"
	firmware_mapping_id = Column(VARCHAR(16),primary_key=True)
	device_type_id = Column(VARCHAR(16),ForeignKey('device_type.device_type_id'))
	firmware_desc = Column(VARCHAR(32))

	def __init__(self,firmware_mapping_id,device_type_id,firmware_desc):
		self.firmware_mapping_id = firmware_mapping_id
		self.device_type_id = device_type_id
		self.firmware_desc = firmware_desc
		
	def __repr__(self):
		return "<FirmwareMapping('%s','%s','%s')>" %(self.firmware_mapping_id,self.device_type_id,self.firmware_desc)




class Odu100RaConfTable(Base):
	__tablename__= "odu100_raConfTable"
	odu100_raConfTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
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
	linkDistance = Column(INTEGER)
	anc = Column(INTEGER)

	def __init__(self,config_profile_id,raIndex,raAdminState,aclMode,ssID,guaranteedBroadcastBW,dba,acm,acs,dfs,numSlaves,antennaPort,linkDistance=0,anc=0):
		self.odu100_raConfTable_id = None
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
		self.linkDistance = linkDistance
		self.anc = anc
		
	def __repr__(self):
		return "<Odu100RaConfTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raConfTable_id,self.config_profile_id,self.raIndex,self.raAdminState,self.aclMode,self.ssID,self.guaranteedBroadcastBW,self.dba,self.acm,self.acs,self.dfs,self.numSlaves,self.antennaPort,self.linkDistance,self.anc)

class Odu100RaLlcConfTable(Base):
	__tablename__= "odu100_raLlcConfTable"
	odu100_raLlcConfTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	raIndex = Column(INTEGER)
	arqWinLow = Column(INTEGER)
	arqWinHigh = Column(INTEGER)
	frameLossThreshold = Column(INTEGER)
	leakyBucketTimerVal = Column(INTEGER)
	frameLossTimeout = Column(INTEGER)

	def __init__(self,config_profile_id,raIndex,arqWinLow,arqWinHigh,frameLossThreshold,leakyBucketTimerVal,frameLossTimeout):
		self.odu100_raLlcConfTable_id = None
		self.config_profile_id = config_profile_id
		self.raIndex = raIndex
		self.arqWinLow = arqWinLow
		self.arqWinHigh = arqWinHigh
		self.frameLossThreshold = frameLossThreshold
		self.leakyBucketTimerVal = leakyBucketTimerVal
		self.frameLossTimeout = frameLossTimeout
		
	def __repr__(self):
		return "<Odu100RaLlcCOnfTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raLlcConfTable_id,self.config_profile_id,self.raIndex,self.arqWinLow,self.arqWinHigh,self.frameLossThreshold,self.leakyBucketTimerVal,self.frameLossTimeout)

class Odu100RaPreferredRFChannelTable(Base):
    __tablename__= "odu100_raPreferredRFChannelTable"
    odu100_raPreferredRFChannelTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    raIndex = Column(INTEGER)
    preindex = Column(INTEGER)
    preindex1 = Column(INTEGER)
    rafrequency = Column(INTEGER)

    def __init__(self,config_profile_id,raIndex,preindex,preindex1,rafrequency):
        self.odu100_raPreferredRFChannelTable_id = None
        self.config_profile_id = config_profile_id
        self.raIndex = raIndex
        self.preindex = preindex
        self.preindex1 = preindex1
        self.rafrequency = rafrequency
        
    def __repr__(self):
        return "<Odu100RaPreferredRFChannelTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_raPreferredRFChannelTable_id,self.config_profile_id,self.raIndex,self.preindex,self.preindex1,self.rafrequency)

class Odu100RaScanListTable(Base):
	__tablename__= "odu100_raScanListTable"
	odu100_raScanListTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
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

	def __init__(self,host_id,raIndex,raScanIndex,ssid,signalStrength,macAddr,rastertime,timeslot,maxSlaves,channelNum,basicRate,radfs,raacm):
		self.odu100_raScanListTable_id = None
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
		return "<Odu100RaScanListTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raScanListTable_id,self.host_id,self.raIndex,self.raScanIndex,self.ssid,self.signalStrength,self.macAddr,self.rastertime,self.timeslot,self.maxSlaves,self.channelNum,self.basicRate,self.radfs,self.raacm)

class Odu100RaSiteSurveyResultTable(Base):
    __tablename__= "odu100_raSiteSurveyResultTable"
    odu100_raSiteSurveyResultTable_id = Column(INTEGER,primary_key=True)
    host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    scanIndex = Column(INTEGER)
    scanIndex1 = Column(INTEGER)
    rfChannelFrequency = Column(INTEGER)
    numCrcErrors = Column(INTEGER)
    maxRslCrcError = Column(INTEGER)
    numPhyErrors = Column(INTEGER)
    maxRslPhyError = Column(INTEGER)
    maxRslValidFrames = Column(INTEGER)
    channelnumber = Column(INTEGER)
    noiseFloor = Column(INTEGER)

    def __init__(self,host_id,raIndex,scanIndex,scanIndex1,rfChannelFrequency,numCrcErrors,maxRslCrcError,numPhyErrors,maxRslPhyError,maxRslValidFrames,channelnumber,noiseFloor):
        self.odu100_raSiteSurveyResultTable_id = None
        self.host_id = host_id
        self.raIndex = raIndex
        self.scanIndex = scanIndex
        self.scanIndex1 = scanIndex1
        self.rfChannelFrequency = rfChannelFrequency
        self.numCrcErrors = numCrcErrors
        self.maxRslCrcError = maxRslCrcError
        self.numPhyErrors = numPhyErrors
        self.maxRslPhyError = maxRslPhyError
        self.maxRslValidFrames = maxRslValidFrames
        self.channelnumber = channelnumber
        self.noiseFloor = noiseFloor
        
    def __repr__(self):
        return "<Odu100RaSiteSurveyResultTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raSiteSurveyResultTable_id,self.host_id,self.raIndex,self.scanIndex,self.scanIndex1,self.rfChannelFrequency,self.numCrcErrors,self.maxRslCrcError,self.numPhyErrors,self.maxRslPhyError,self.maxRslValidFrames,self.channelnumber,self.noiseFloor)

class Odu100RaStatusTable(Base):
	__tablename__= "odu100_raStatusTable"
	odu100_raStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	raIndex = Column(INTEGER)
	currentTimeSlot = Column(INTEGER)
	raMacAddress = Column(VARCHAR(32))
	raoperationalState = Column(INTEGER)
	unusedTxTimeUL = Column(INTEGER)
	unusedTxTimeDL = Column(INTEGER)
	ancStatus = Column(ENUM('0','1'))
	ancHwAvailable = Column(ENUM('0','1'))
	timestamp = Column(DATETIME)

	def __init__(self,host_id,raIndex,currentTimeSlot,raMacAddress,raoperationalState,unusedTxTimeUL,unusedTxTimeDL,ancStatus,ancHwAvailable,timestamp):
		self.odu100_raStatusTable_id = None
		self.host_id = host_id
		self.raIndex = raIndex
		self.currentTimeSlot = currentTimeSlot
		self.raMacAddress = raMacAddress
		self.raoperationalState = raoperationalState
		self.unusedTxTimeUL = unusedTxTimeUL
		self.unusedTxTimeDL = unusedTxTimeDL
		self.ancStatus = ancStatus
		self.ancHwAvailable = ancHwAvailable
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<Odu100RaStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raStatusTable_id,self.host_id,self.raIndex,self.currentTimeSlot,self.raMacAddress,self.raoperationalState,self.unusedTxTimeUL,self.unusedTxTimeDL,self.ancStatus,self.ancHwAvailable,self.timestamp)



class Odu100MacFilterTable(Base):
	__tablename__= "odu100_macFilterTable"
	odu100_macFilterTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	macFilterIndex = Column(INTEGER)
	filterMacAddress = Column(VARCHAR(19))
	timestamp = Column(DATETIME)

	def __init__(self,host_id,macFilterIndex,filterMacAddress,timestamp):
		self.odu100_macFilterTable_id = None
		self.host_id = host_id
		self.macFilterIndex = macFilterIndex
		self.filterMacAddress = filterMacAddress
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<Odu100MacFilterTable('%s','%s','%s','%s','%s')>" %(self.odu100_macFilterTable_id,self.host_id,self.macFilterIndex,self.filterMacAddress,self.timestamp)


class Odu100IpFilterTable(Base):
	__tablename__= "odu100_ipFilterTable"
	odu100_ipFilterTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	ipFilterIndex = Column(INTEGER)
	ipFilterIpAddress = Column(VARCHAR(16))
	ipFilterNetworkMask = Column(VARCHAR(16))
	timestamp = Column(DATETIME)

	def __init__(self,host_id,ipFilterIndex,ipFilterIpAddress,ipFilterNetworkMask,timestamp):
		self.odu100_ipFilterTable_id = None
		self.host_id = host_id
		self.ipFilterIndex = ipFilterIndex
		self.ipFilterIpAddress = ipFilterIpAddress
		self.ipFilterNetworkMask = ipFilterNetworkMask
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<Odu100IpFilterTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_ipFilterTable_id,self.host_id,self.ipFilterIndex,self.ipFilterIpAddress,self.ipFilterNetworkMask,self.timestamp)


class Odu100RaTddMacConfigTable(Base):
	__tablename__= "odu100_raTddMacConfigTable"
	odu100_raTddMacConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	raIndex = Column(INTEGER)
	passPhrase = Column(VARCHAR(64))
	txPower = Column(INTEGER)
	maxPower = Column(INTEGER)
	maxCrcErrors = Column(INTEGER)
	leakyBucketTimerValue = Column(INTEGER)
	encryptionType = Column(INTEGER)

	def __init__(self,config_profile_id,raIndex,passPhrase,txPower,maxPower,maxCrcErrors,leakyBucketTimerValue,encryptionType):
		self.odu100_raTddMacConfigTable_id = None
		self.config_profile_id = config_profile_id
		self.raIndex = raIndex
		self.passPhrase = passPhrase
		self.txPower = txPower
		self.maxPower = maxPower
		self.maxCrcErrors = maxCrcErrors
		self.leakyBucketTimerValue = leakyBucketTimerValue
		self.encryptionType = encryptionType
		
	def __repr__(self):
		return "<Odu100RaTddMacCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raTddMacConfigTable_id,self.config_profile_id,self.raIndex,self.passPhrase,self.txPower,self.maxPower,self.maxCrcErrors,self.leakyBucketTimerValue,self.encryptionType)

class Odu100RaTddMacStatisticsTable(Base):
	__tablename__= "odu100_raTddMacStatisticsTable"
	odu100_raTddMacStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	raIndex = Column(INTEGER)
	rxpackets = Column(INTEGER)
	txpackets = Column(INTEGER)
	rxerrors = Column(INTEGER)
	txerrors = Column(INTEGER)
	rxdropped = Column(INTEGER)
	txdropped = Column(INTEGER)
	rxCrcErrors = Column(INTEGER)
	rxPhyError = Column(INTEGER)

	def __init__(self,host_id,raIndex,rxpackets,txpackets,rxerrors,txerrors,rxdropped,txdropped,rxCrcErrors,rxPhyErrors):
		self.odu100_raTddMacStatisticsTable_id = None
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
		return "<Odu100RaTddMacStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raTddMacStatisticsTable_id,self.host_id,self.raIndex,self.rxpackets,self.txpackets,self.rxerrors,self.txerrors,self.rxdropped,self.txdropped,self.rxCrcErrors,self.rxPhyError)

class Odu100RaTddMacStatusTable(Base):
    __tablename__= "odu100_raTddMacStatusTable"
    odu100_raTddMacStatusTable_id = Column(INTEGER,primary_key=True)
    host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
    raIndex = Column(INTEGER)
    rfChanFreq = Column(INTEGER)
    timestamp = Column(TIMESTAMP)
    def __init__(self,host_id,raIndex,rfChanFreq,timestamp):
        self.odu100_raTddMacStatusTable_id = None
        self.host_id = host_id
        self.raIndex = raIndex
        self.rfChanFreq = rfChanFreq
        self.timestamp = timestamp
    def __repr__(self):
        return "<Odu100RaTddMacStatusTable('%s','%s','%s','%s','%s')>" %(self.odu100_raTddMacStatusTable_id,self.host_id,self.raIndex,self.rfChanFreq,self.timestamp)

class Odu100RaValidPhyRatesTable(Base):
	__tablename__= "odu100_raValidPhyRatesTable"
	odu100_raValidPhyRatesTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	raIndex = Column(INTEGER)
	mcsindex = Column(INTEGER)
	spatialStreams = Column(INTEGER)
	modulationType = Column(INTEGER)
	codingRate = Column(INTEGER)
	rate = Column(INTEGER)

	def __init__(self,host_id,raIndex,mcsindex,spatialStreams,modulationType,codingRate,rate):
		self.odu100_raValidPhyRatesTable_id = None
		self.host_id = host_id
		self.raIndex = raIndex
		self.mcsindex = mcsindex
		self.spatialStreams = spatialStreams
		self.modulationType = modulationType
		self.codingRate = codingRate
		self.rate = rate
		
	def __repr__(self):
		return "<Odu100RaValidPhyRatesTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_raValidPhyRatesTable_id,self.host_id,self.raIndex,self.mcsindex,self.spatialStreams,self.modulationType,self.codingRate,self.rate)

class Odu100RuConfTable(Base):
	__tablename__= "odu100_ruConfTable"
	odu100_ruConfTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	confIndex = Column(INTEGER)
	adminstate = Column(INTEGER)
	defaultNodeType = Column(INTEGER)
	channelBandwidth = Column(INTEGER)
	synchSource = Column(INTEGER)
	countryCode = Column(INTEGER)
	poeState = Column(INTEGER)
	alignmentControl = Column(INTEGER)
	ethFiltering = Column(INTEGER)
	poePort2State = Column(INTEGER)
	poePort4State = Column(INTEGER)
	poePort6State = Column(INTEGER)

	def __init__(self,config_profile_id,confIndex,adminstate,defaultNodeType,channelBandwidth,synchSource,countryCode,poeState=0,alignmentControl=0,ethFiltering=0,poePort2State=0,poePort4State=0,poePort6State=0):
		self.odu100_ruConfTable_id = None
		self.config_profile_id = config_profile_id
		self.confIndex = confIndex
		self.adminstate = adminstate
		self.defaultNodeType = defaultNodeType
		self.channelBandwidth = channelBandwidth
		self.synchSource = synchSource
		self.countryCode = countryCode
		self.poeState = poeState
		self.alignmentControl = alignmentControl
		self.ethFiltering = ethFiltering
		self.poePort2State = poePort2State
		self.poePort4State = poePort4State
		self.poePort6State = poePort6State
		
	def __repr__(self):
		return "<Odu100RuConfTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', %s)>" %(self.odu100_ruConfTable_id,self.config_profile_id,self.confIndex,self.adminstate,self.defaultNodeType,self.channelBandwidth,self.synchSource,self.countryCode,self.poeState,self.alignmentControl,self.ethFiltering, self.poePort2State,self.poePort4State,self.poePort6State)

class Odu100RuDateTimeTable(Base):
	__tablename__= "odu100_ruDateTimeTable"
	odu100_ruDateTimeTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	dateIndex = Column(INTEGER)
	year = Column(INTEGER)
	month = Column(INTEGER)
	day = Column(INTEGER)
	hour = Column(INTEGER)
	min = Column(INTEGER)
	sec = Column(INTEGER)

	def __init__(self,config_profile_id,dateIndex,year,month,day,hour,min,sec):
		self.odu100_ruDateTimeTable_id = None
		self.config_profile_id = config_profile_id
		self.dateIndex = dateIndex
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.min = min
		self.sec = sec
		
	def __repr__(self):
		return "<Odu100RuDateTimeTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_ruDateTimeTable_id,self.config_profile_id,self.dateIndex,self.year,self.month,self.day,self.hour,self.min,self.sec)

class Odu100RuOmOperationsTable(Base):
	__tablename__= "odu100_ruOmOperationsTable"
	odu100_ruOmOperationsTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
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

	def __init__(self,config_profile_id,omIndex,omOperationReq,userName,password,ftpServerAddress,pathName,omOperationResult,omSpecificCause,listOfChannels,txTime,txRate,txBW):
		self.odu100_ruOmOperationsTable_id = None
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
		return "<Odu100RuOmOperatiOnsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_ruOmOperationsTable_id,self.config_profile_id,self.omIndex,self.omOperationReq,self.userName,self.password,self.ftpServerAddress,self.pathName,self.omOperationResult,self.omSpecificCause,self.listOfChannels,self.txTime,self.txRate,self.txBW)

class Odu100RuStatusTable(Base):
	__tablename__= "odu100_ruStatusTable"
	odu100_ruStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	statusIndex = Column(INTEGER)
	lastRebootReason = Column(INTEGER)
	isConfigCommitedToFlash = Column(INTEGER)
	upTime = Column(INTEGER)
	poeStatus = Column(INTEGER)
	cpuId = Column(INTEGER)
	ruoperationalState = Column(INTEGER)
	nodeBandwidth = Column(INTEGER)
	poePort2Status = Column(INTEGER)
	poePort4Status = Column(INTEGER)
	poePort6Status = Column(INTEGER)

	def __init__(self,host_id,statusIndex,lastRebootReason,isConfigCommitedToFlash,upTime,poeStatus,cpuId,ruoperationalState,nodeBandwidth,poePort2Status=0,poePort4Status=0,poePort6Status=0):
		self.odu100_ruStatusTable_id = None
		self.host_id = host_id
		self.statusIndex = statusIndex
		self.lastRebootReason = lastRebootReason
		self.isConfigCommitedToFlash = isConfigCommitedToFlash
		self.upTime = upTime
		self.poeStatus = poeStatus
		self.cpuId = cpuId
		self.ruoperationalState = ruoperationalState
		self.nodeBandwidth = nodeBandwidth
		self.poePort2Status = poePort2Status
		self.poePort4Status = poePort4Status
		self.poePort6Status = poePort6Status
		
	def __repr__(self):
		return "<Odu100RuStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_ruStatusTable_id,self.host_id,self.statusIndex,self.lastRebootReason,self.isConfigCommitedToFlash,self.upTime,self.poeStatus,self.cpuId,self.ruoperationalState,self.nodeBandwidth,self.poePort2Status,self.poePort4Status,self.poePort6Status)


class Odu100SwStatusTable(Base):
	__tablename__= "odu100_swStatusTable"
	odu100_swStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	swStatusIndex = Column(INTEGER)
	activeVersion = Column(VARCHAR(32))
	passiveVersion = Column(VARCHAR(32))
	bootloaderVersion = Column(VARCHAR(64))

	def __init__(self,host_id,swStatusIndex,activeVersion,passiveVersion,bootloaderVersion):
		self.odu100_swStatusTable_id = None
		self.host_id = host_id
		self.swStatusIndex = swStatusIndex
		self.activeVersion = activeVersion
		self.passiveVersion = passiveVersion
		self.bootloaderVersion = bootloaderVersion
		
	def __repr__(self):
		return "<Odu100SwStatusTable('%s','%s','%s','%s','%s','%s')>" %(self.odu100_swStatusTable_id,self.host_id,self.swStatusIndex,self.activeVersion,self.passiveVersion,self.bootloaderVersion)

class Odu100SyncConfigTable(Base):
	__tablename__= "odu100_syncConfigTable"
	odu100_syncConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	syncConfigIndex = Column(INTEGER)
	adminStatus = Column(INTEGER)
	synchState = Column(INTEGER)
	rasterTime = Column(INTEGER)
	syncLossThreshold = Column(INTEGER)
	leakyBucketTimer = Column(INTEGER)
	syncLostTimeout = Column(INTEGER)
	syncConfigTimerAdjust = Column(INTEGER)
	percentageDownlinkTransmitTime = Column(INTEGER)

	def __init__(self,config_profile_id,syncConfigIndex,adminStatus,synchState,rasterTime,syncLossThreshold,leakyBucketTimer,syncLostTimeout,syncConfigTimerAdjust,percentageDownlinkTransmitTime):
		self.odu100_syncConfigTable_id = None
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
		return "<Odu100SyncCOnfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_syncConfigTable_id,self.config_profile_id,self.syncConfigIndex,self.adminStatus,self.synchState,self.rasterTime,self.syncLossThreshold,self.leakyBucketTimer,self.syncLostTimeout,self.syncConfigTimerAdjust,self.percentageDownlinkTransmitTime)

class Odu100SynchStatisticsTable(Base):
	__tablename__= "odu100_synchStatisticsTable"
	odu100_synchStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	synchStatsIndex = Column(INTEGER)
	syncLostCounter = Column(INTEGER)

	def __init__(self,host_id,synchStatsIndex,syncLostCounter):
		self.odu100_synchStatisticsTable_id = None
		self.host_id = host_id
		self.synchStatsIndex = synchStatsIndex
		self.syncLostCounter = syncLostCounter
		
	def __repr__(self):
		return "<Odu100SynchStatisticsTable('%s','%s','%s','%s')>" %(self.odu100_synchStatisticsTable_id,self.host_id,self.synchStatsIndex,self.syncLostCounter)

class Odu100SynchStatusTable(Base):
    __tablename__= "odu100_synchStatusTable"
    odu100_synchStatusTable_id = Column(INTEGER,primary_key=True)
    host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
    synchStatsIndex = Column(INTEGER)
    syncoperationalState = Column(INTEGER)
    syncrasterTime = Column(INTEGER)
    timerAdjust = Column(INTEGER)
    syncpercentageDownlinkTransmitTime = Column(INTEGER)
    timestamp = Column(DATETIME)

    def __init__(self,host_id,synchStatsIndex,syncoperationalState,syncrasterTime,timerAdjust,syncpercentageDownlinkTransmitTime,timestamp):
        self.odu100_synchStatusTable_id = None
        self.host_id = host_id
        self.synchStatsIndex = synchStatsIndex
        self.syncoperationalState = syncoperationalState
        self.syncrasterTime = syncrasterTime
        self.timerAdjust = timerAdjust
        self.syncpercentageDownlinkTransmitTime = syncpercentageDownlinkTransmitTime
        self.timestamp = timestamp 
        
    def __repr__(self):
        return "<Odu100SynchStatusTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_synchStatusTable_id,self.host_id,self.synchStatsIndex,self.syncoperationalState,self.syncrasterTime,self.timerAdjust,self.syncpercentageDownlinkTransmitTime,self.timestamp)

class Odu100SysOmcRegistrationTable(Base):
	__tablename__= "odu100_sysOmcRegistrationTable"
	odu100_sysOmcRegistrationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	sysOmcRegistrationIndex = Column(INTEGER)
	sysOmcRegisterContactAddr = Column(VARCHAR(32))
	sysOmcRegisterContactPerson = Column(VARCHAR(32))
	sysOmcRegisterContactMobile = Column(VARCHAR(32))
	sysOmcRegisterAlternateContact = Column(VARCHAR(32))
	sysOmcRegisterContactEmail = Column(VARCHAR(32))

	def __init__(self,config_profile_id,sysOmcRegistrationIndex,sysOmcRegisterContactAddr,sysOmcRegisterContactPerson,sysOmcRegisterContactMobile,sysOmcRegisterAlternateContact,sysOmcRegisterContactEmail):
		self.odu100_sysOmcRegistrationTable_id = None
		self.config_profile_id = config_profile_id
		self.sysOmcRegistrationIndex = sysOmcRegistrationIndex
		self.sysOmcRegisterContactAddr = sysOmcRegisterContactAddr
		self.sysOmcRegisterContactPerson = sysOmcRegisterContactPerson
		self.sysOmcRegisterContactMobile = sysOmcRegisterContactMobile
		self.sysOmcRegisterAlternateContact = sysOmcRegisterAlternateContact
		self.sysOmcRegisterContactEmail = sysOmcRegisterContactEmail
		
	def __repr__(self):
		return "<Odu100SysOmcRegistratiOnTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.odu100_sysOmcRegistrationTable_id,self.config_profile_id,self.sysOmcRegistrationIndex,self.sysOmcRegisterContactAddr,self.sysOmcRegisterContactPerson,self.sysOmcRegisterContactMobile,self.sysOmcRegisterAlternateContact,self.sysOmcRegisterContactEmail)

tablename=Odu16ConfigProfiles.__table__

class IduAclportTable(Base):
    __tablename__= "idu_aclportTable"
    idu_aclportTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    aclportnum = Column(INTEGER)
    aclindex = Column(INTEGER)
    aclmacaddress = Column(VARCHAR(32))
    portrowstatus = Column(INTEGER)

    def __init__(self,config_profile_id,aclportnum,aclindex,aclmacaddress,portrowstatus):
        self.idu_aclportTable_id = None
        self.config_profile_id = config_profile_id
        self.aclportnum = aclportnum
        self.aclindex = aclindex
        self.aclmacaddress = aclmacaddress
        self.portrowstatus = portrowstatus
        
    def __repr__(self):
        return "<IduAclportTable('%s','%s','%s','%s','%s','%s')>" %(self.idu_aclportTable_id,self.config_profile_id,self.aclportnum,self.aclindex,self.aclmacaddress,self.portrowstatus)

class IduAlarmOutConfigTable(Base):
	__tablename__= "idu_alarmOutConfigTable"
	idu_alarmOutConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	alarmOutPin = Column(INTEGER)
	alarmPinState = Column(INTEGER)

	def __init__(self,config_profile_id,alarmOutPin,alarmPinState):
		self.idu_alarmOutConfigTable_id = None
		self.config_profile_id = config_profile_id
		self.alarmOutPin = alarmOutPin
		self.alarmPinState = alarmPinState
		
	def __repr__(self):
		return "<IduAlarmOutConfigTable('%s','%s','%s','%s')>" %(self.idu_alarmOutConfigTable_id,self.config_profile_id,self.alarmOutPin,self.alarmPinState)

class IduAlarmPortConfigurationTable(Base):
	__tablename__= "idu_alarmPortConfigurationTable"
	idu_alarmPortConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	alarmPin = Column(INTEGER)
	alarmAdminStatus = Column(INTEGER)
	alarmString = Column(VARCHAR(256))
	alarmLevel = Column(INTEGER)

	def __init__(self,config_profile_id,alarmPin,alarmAdminStatus,alarmString,alarmLevel):
		self.idu_alarmPortConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.alarmPin = alarmPin
		self.alarmAdminStatus = alarmAdminStatus
		self.alarmString = alarmString
		self.alarmLevel = alarmLevel
		
	def __repr__(self):
		return "<IduAlarmPortConfigurationTable('%s','%s','%s','%s','%s','%s')>" %(self.idu_alarmPortConfigurationTable_id,self.config_profile_id,self.alarmPin,self.alarmAdminStatus,self.alarmString,self.alarmLevel)

class IduAtuconfigTable(Base):
	__tablename__= "idu_atuconfigTable"
	idu_atuconfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	atuid = Column(INTEGER)
	atustate = Column(INTEGER)
	entrytype = Column(INTEGER)
	priority = Column(INTEGER)
	macaddress = Column(VARCHAR(32))
	atumemberports = Column(INTEGER)

	def __init__(self,config_profile_id,atuid,atustate,entrytype,priority,macaddress,atumemberports):
		self.idu_atuconfigTable_id = None
		self.config_profile_id = config_profile_id
		self.atuid = atuid
		self.atustate = atustate
		self.entrytype = entrytype
		self.priority = priority
		self.macaddress = macaddress
		self.atumemberports = atumemberports
		
	def __repr__(self):
		return "<IduAtuconfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_atuconfigTable_id,self.config_profile_id,self.atuid,self.atustate,self.entrytype,self.priority,self.macaddress,self.atumemberports)

class IduE1PortConfigurationTable(Base):
	__tablename__= "idu_e1PortConfigurationTable"
	idu_e1PortConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	portNumber = Column(INTEGER)
	adminState = Column(INTEGER)
	clockSource = Column(INTEGER)
	lineType = Column(INTEGER)
	lineCode = Column(INTEGER)

	def __init__(self,config_profile_id,portNumber,adminState,clockSource,lineType,lineCode):
		self.idu_e1PortConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.portNumber = portNumber
		self.adminState = adminState
		self.clockSource = clockSource
		self.lineType = lineType
		self.lineCode = lineCode
		
	def __repr__(self):
		return "<IduE1PortConfigurationTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_e1PortConfigurationTable_id,self.config_profile_id,self.portNumber,self.adminState,self.clockSource,self.lineType,self.lineCode)



class IduE1PortStatusTable(Base):
	__tablename__= "idu_e1PortStatusTable"
	idu_e1PortStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	portNum = Column(INTEGER)
	opStatus = Column(INTEGER)
	los = Column(INTEGER)
	lof = Column(INTEGER)
	ais = Column(INTEGER)
	rai = Column(INTEGER)
	rxFrameSlip = Column(INTEGER)
	txFrameSlip = Column(INTEGER)
	bpv = Column(INTEGER)
	adptClkState = Column(INTEGER)
	holdOverStatus = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,portNum,opStatus,los,lof,ais,rai,rxFrameSlip,txFrameSlip,bpv,adptClkState,holdOverStatus,timestamp):
		self.idu_e1PortStatusTable_id = None
		self.host_id = host_id
		self.portNum = portNum
		self.opStatus = opStatus
		self.los = los
		self.lof = lof
		self.ais = ais
		self.rai = rai
		self.rxFrameSlip = rxFrameSlip
		self.txFrameSlip = txFrameSlip
		self.bpv = bpv
		self.adptClkState = adptClkState
		self.holdOverStatus = holdOverStatus
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduE1PortStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_e1PortStatusTable_id,self.host_id,self.portNum,self.opStatus,self.los,self.lof,self.ais,self.rai,self.rxFrameSlip,self.txFrameSlip,self.bpv,self.adptClkState,self.holdOverStatus,self.timestamp)



class IduIduAdminStateTable(Base):
	__tablename__= "idu_iduAdminStateTable"
	idu_iduAdminStateTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	stateId = Column(INTEGER)
	adminstate = Column(SMALLINT)

	def __init__(self,config_profile_id,stateId,adminstate):
		self.idu_iduAdminStateTable_id = None
		self.config_profile_id = config_profile_id
		self.stateId = stateId
		self.adminstate = adminstate
		
	def __repr__(self):
		return "<IduIduAdminStateTable('%s','%s','%s','%s')>" %(self.idu_iduAdminStateTable_id,self.config_profile_id,self.stateId,self.adminstate)


class IduIduInfoTable(Base):
	__tablename__= "idu_iduInfoTable"
	idu_iduInfoTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	infoIndex = Column(INTEGER)
	hwSerialNumber = Column(VARCHAR(32))
	hwType = Column(SMALLINT)
	hwConfigE1 = Column(SMALLINT)
	hwConfigEth = Column(SMALLINT)
	hwConfigAlarm = Column(SMALLINT)
	systemterfaceMac = Column(VARCHAR(32))
	tdmoipInterfaceMac = Column(VARCHAR(32))
	currentTemperature = Column(INTEGER)
	sysUptime = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,infoIndex,hwSerialNumber,hwType,hwConfigE1,hwConfigEth,hwConfigAlarm,systemterfaceMac,tdmoipInterfaceMac,currentTemperature,sysUptime,timestamp):
		self.idu_iduInfoTable_id = None
		self.host_id = host_id
		self.infoIndex = infoIndex
		self.hwSerialNumber = hwSerialNumber
		self.hwType = hwType
		self.hwConfigE1 = hwConfigE1
		self.hwConfigEth = hwConfigEth
		self.hwConfigAlarm = hwConfigAlarm
		self.systemterfaceMac = systemterfaceMac
		self.tdmoipInterfaceMac = tdmoipInterfaceMac
		self.currentTemperature = currentTemperature
		self.sysUptime = sysUptime
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduIduInfoTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_iduInfoTable_id,self.host_id,self.infoIndex,self.hwSerialNumber,self.hwType,self.hwConfigE1,self.hwConfigEth,self.hwConfigAlarm,self.systemterfaceMac,self.tdmoipInterfaceMac,self.currentTemperature,self.sysUptime,self.timestamp)


class IduIduNetworkStatisticsTable(Base):
	__tablename__= "idu_iduNetworkStatisticsTable"
	idu_iduNetworkStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	interfaceName = Column(INTEGER)
	rxPackets = Column(INTEGER)
	txPackets = Column(INTEGER)
	rxBytes = Column(INTEGER)
	txBytes = Column(INTEGER)
	rxErrors = Column(INTEGER)
	txErrors = Column(INTEGER)
	rxDropped = Column(INTEGER)
	txDropped = Column(INTEGER)
	multicasts = Column(INTEGER)
	collisions = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,interfaceName,rxPackets,txPackets,rxBytes,txBytes,rxErrors,txErrors,rxDropped,txDropped,multicasts,collisions,timestamp):
		self.idu_iduNetworkStatisticsTable_id = None
		self.host_id = host_id
		self.interfaceName = interfaceName
		self.rxPackets = rxPackets
		self.txPackets = txPackets
		self.rxBytes = rxBytes
		self.txBytes = txBytes
		self.rxErrors = rxErrors
		self.txErrors = txErrors
		self.rxDropped = rxDropped
		self.txDropped = txDropped
		self.multicasts = multicasts
		self.collisions = collisions
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduIduNetworkStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_iduNetworkStatisticsTable_id,self.host_id,self.interfaceName,self.rxPackets,self.txPackets,self.rxBytes,self.txBytes,self.rxErrors,self.txErrors,self.rxDropped,self.txDropped,self.multicasts,self.collisions,self.timestamp)


class IduIduOmOperationsTable(Base):
	__tablename__= "idu_iduOmOperationsTable"
	idu_iduOmOperationsTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	omIndex = Column(INTEGER)
	omOperationReq = Column(INTEGER)
	userName = Column(VARCHAR(16))
	password = Column(VARCHAR(16))
	ftpServerAddress = Column(VARCHAR(32))
	pathName = Column(VARCHAR(128))
	omOperationResult = Column(INTEGER)
	omSpecificCause = Column(INTEGER)

	def __init__(self,config_profile_id,omIndex,omOperationReq,userName,password,ftpServerAddress,pathName,omOperationResult,omSpecificCause):
		self.idu_iduOmOperationsTable_id = None
		self.config_profile_id = config_profile_id
		self.omIndex = omIndex
		self.omOperationReq = omOperationReq
		self.userName = userName
		self.password = password
		self.ftpServerAddress = ftpServerAddress
		self.pathName = pathName
		self.omOperationResult = omOperationResult
		self.omSpecificCause = omSpecificCause
		
	def __repr__(self):
		return "<IduIduOmOperationsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_iduOmOperationsTable_id,self.config_profile_id,self.omIndex,self.omOperationReq,self.userName,self.password,self.ftpServerAddress,self.pathName,self.omOperationResult,self.omSpecificCause)



class IduLinkConfigurationTable(Base):
    __tablename__= "idu_linkConfigurationTable"
    idu_linkConfigurationTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    portNumber = Column(Integer)
    bundleNumber = Column(INTEGER)
    adminStatus = Column(INTEGER)
    srcBundleID = Column(INTEGER)
    dstBundleID = Column(INTEGER)
    dstIPAddr = Column(VARCHAR(32))
    tsaAssign = Column(VARCHAR(32))
    clockRecovery = Column(INTEGER)
    bundleSize = Column(INTEGER)
    bufferSize = Column(INTEGER)
    rowStatus = Column(INTEGER)

    def __init__(self,config_profile_id,portNumber,bundleNumber,adminStatus,srcBundleID,dstBundleID,dstIPAddr,tsaAssign,clockRecovery,bundleSize,bufferSize,rowStatus):
        self.idu_linkConfigurationTable_id = None
        self.config_profile_id = config_profile_id
        self.portNumber = portNumber
        self.bundleNumber = bundleNumber
        self.adminStatus = adminStatus
        self.srcBundleID = srcBundleID
        self.dstBundleID = dstBundleID
        self.dstIPAddr = dstIPAddr
        self.tsaAssign = tsaAssign
        self.clockRecovery = clockRecovery
        self.bundleSize = bundleSize
        self.bufferSize = bufferSize
        self.rowStatus = rowStatus
        
    def __repr__(self):
        return "<IduLinkConfigurationTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_linkConfigurationTable_id,self.config_profile_id,self.portNumber,self.bundleNumber,self.adminStatus,self.srcBundleID,self.dstBundleID,self.dstIPAddr,self.tsaAssign,self.clockRecovery,self.bundleSize,self.bufferSize,self.rowStatus)




class IduLinkStatisticsTable(Base):
	__tablename__= "idu_linkStatisticsTable"
	idu_linkStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	bundlenumber = Column(INTEGER)
	goodFramesToEth = Column(INTEGER)
	goodFramesRx = Column(INTEGER)
	lostPacketsAtRx = Column(INTEGER)
	discardedPackets = Column(INTEGER)
	reorderedPackets = Column(INTEGER)
	underrunEvents = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,bundlenumber,goodFramesToEth,goodFramesRx,lostPacketsAtRx,discardedPackets,reorderedPackets,underrunEvents,timestamp):
		self.idu_linkStatisticsTable_id = None
		self.host_id = host_id
		self.bundlenumber = bundlenumber
		self.goodFramesToEth = goodFramesToEth
		self.goodFramesRx = goodFramesRx
		self.lostPacketsAtRx = lostPacketsAtRx
		self.discardedPackets = discardedPackets
		self.reorderedPackets = reorderedPackets
		self.underrunEvents = underrunEvents
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduLinkStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_linkStatisticsTable_id,self.host_id,self.bundlenumber,self.goodFramesToEth,self.goodFramesRx,self.lostPacketsAtRx,self.discardedPackets,self.reorderedPackets,self.underrunEvents,self.timestamp)


class IduLinkStatusTable(Base):
	__tablename__= "idu_linkStatusTable"
	idu_linkStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	bundleNum = Column(INTEGER)
	operationalStatus = Column(INTEGER)
	minJBLevel = Column(INTEGER)
	maxJBLevel = Column(INTEGER)
	underrunOccured = Column(INTEGER)
	overrunOccured = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,bundleNum,operationalStatus,minJBLevel,maxJBLevel,underrunOccured,overrunOccured,timestamp):
		self.idu_linkStatusTable_id = None
		self.host_id = host_id
		self.bundleNum = bundleNum
		self.operationalStatus = operationalStatus
		self.minJBLevel = minJBLevel
		self.maxJBLevel = maxJBLevel
		self.underrunOccured = underrunOccured
		self.overrunOccured = overrunOccured
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduLinkStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_linkStatusTable_id,self.host_id,self.bundleNum,self.operationalStatus,self.minJBLevel,self.maxJBLevel,self.underrunOccured,self.overrunOccured,self.timestamp)

class IduMirroringportTable(Base):
	__tablename__= "idu_mirroringportTable"
	idu_mirroringportTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	mirroringindexid = Column(INTEGER)
	mirroringport = Column(INTEGER)

	def __init__(self,config_profile_id,mirroringindexid,mirroringport):
		self.idu_mirroringportTable_id = None
		self.config_profile_id = config_profile_id
		self.mirroringindexid = mirroringindexid
		self.mirroringport = mirroringport
		
	def __repr__(self):
		return "<IduMirroringportTable('%s','%s','%s','%s')>" %(self.idu_mirroringportTable_id,self.config_profile_id,self.mirroringindexid,self.mirroringport)





class IduNetworkConfigurationsTable(Base):
	__tablename__= "idu_networkConfigurationsTable"
	idu_networkConfigurationsTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	interface = Column(INTEGER)
	ipaddr = Column(VARCHAR(32))
	netmask = Column(VARCHAR(32))
	gateway = Column(VARCHAR(32))
	autoIpConfig = Column(INTEGER)

	def __init__(self,config_profile_id,interface,ipaddr,netmask,gateway,autoIpConfig):
		self.idu_networkConfigurationsTable_id = None
		self.config_profile_id = config_profile_id
		self.interface = interface
		self.ipaddr = ipaddr
		self.netmask = netmask
		self.gateway = gateway
		self.autoIpConfig = autoIpConfig
		
	def __repr__(self):
		return "<IduNetworkConfigurationsTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_networkConfigurationsTable_id,self.config_profile_id,self.interface,self.ipaddr,self.netmask,self.gateway,self.autoIpConfig)

class IduOids(Base):
	__tablename__= "idu_oids"
	oid_id = Column(INTEGER,primary_key=True)
	device_type_id = Column(VARCHAR(16))
	oid = Column(VARCHAR(256))
	oid_name = Column(VARCHAR(256))
	oid_type = Column(VARCHAR(16))
	access = Column(SMALLINT)
	default_value = Column(VARCHAR(256))
	min_value = Column(VARCHAR(128))
	max_value = Column(VARCHAR(256))
	indexes = Column(VARCHAR(256))
	dependent_id = Column(INTEGER)
	multivalue = Column(SMALLINT)
	table_name = Column(VARCHAR(128))
	coloumn_name = Column(VARCHAR(128))
	indexes_name = Column(VARCHAR(64))

	def __init__(self,oid_id,device_type_id,oid,oid_name,oid_type,access,default_value,min_value,max_value,indexes,dependent_id,multivalue,table_name,coloumn_name,indexes_name):
		self.oid_id = None
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
		self.indexes_name = indexes_name
		
	def __repr__(self):
		return "<IduOids('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.oid_id,self.device_type_id,self.oid,self.oid_name,self.oid_type,self.access,self.default_value,self.min_value,self.max_value,self.indexes,self.dependent_id,self.multivalue,self.table_name,self.coloumn_name,self.indexes_name)

class IduOids_multivalues(Base):
	__tablename__= "idu_oids_multivalues"
	oids_multivalue_id = Column(INTEGER,primary_key=True)
	oid_id = Column(INTEGER)
	value = Column(VARCHAR(128))
	name = Column(VARCHAR(128))

	def __init__(self,oids_multivalue_id,oid_id,value,name):
		self.oids_multivalue_id = None
		self.oid_id = oid_id
		self.value = value
		self.name = name
		
	def __repr__(self):
		return "<IduOids_multivalues('%s','%s','%s','%s')>" %(self.oids_multivalue_id,self.oid_id,self.value,self.name)

class IduOmcConfigurationTable(Base):
	__tablename__= "idu_omcConfigurationTable"
	idu_omcConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	omcIndex = Column(INTEGER)
	omcIpAddress = Column(VARCHAR(32))
	periodicStatsTimer = Column(INTEGER)

	def __init__(self,config_profile_id,omcIndex,omcIpAddress,periodicStatsTimer):
		self.idu_omcConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.omcIndex = omcIndex
		self.omcIpAddress = omcIpAddress
		self.periodicStatsTimer = periodicStatsTimer
		
	def __repr__(self):
		return "<IduOmcConfigurationTable('%s','%s','%s','%s','%s')>" %(self.idu_omcConfigurationTable_id,self.config_profile_id,self.omcIndex,self.omcIpAddress,self.periodicStatsTimer)



class IduPoeConfigurationTable(Base):
	__tablename__= "idu_poeConfigurationTable"
	idu_poeConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	indexId = Column(INTEGER)
	poeAdminStatus = Column(INTEGER)

	def __init__(self,config_profile_id,indexId,poeAdminStatus):
		self.idu_poeConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.indexId = indexId
		self.poeAdminStatus = poeAdminStatus
		
	def __repr__(self):
		return "<IduPoeConfigurationTable('%s','%s','%s','%s')>" %(self.idu_poeConfigurationTable_id,self.config_profile_id,self.indexId,self.poeAdminStatus)




class IduPortBwTable(Base):
	__tablename__= "idu_portBwTable"
	idu_portBwTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	switchportnum = Column(INTEGER)
	egressbwvalue = Column(INTEGER)
	ingressbwvalue = Column(INTEGER)

	def __init__(self,config_profile_id,switchportnum,egressbwvalue,ingressbwvalue):
		self.idu_portBwTable_id = None
		self.config_profile_id = config_profile_id
		self.switchportnum = switchportnum
		self.egressbwvalue = egressbwvalue
		self.ingressbwvalue = ingressbwvalue
		
	def __repr__(self):
		return "<IduPortBwTable('%s','%s','%s','%s','%s')>" %(self.idu_portBwTable_id,self.config_profile_id,self.switchportnum,self.egressbwvalue,self.ingressbwvalue)


class IduPortSecondaryStatisticsTable(Base):
	__tablename__= "idu_portSecondaryStatisticsTable"
	idu_portSecondaryStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	switchPortNum = Column(INTEGER)
	inUnicast = Column(INTEGER)
	outUnicast = Column(INTEGER)
	inBroadcast = Column(INTEGER)
	outBroadcast = Column(INTEGER)
	inMulticast = Column(INTEGER)
	outMulricast = Column(INTEGER)
	inUndersizeRx = Column(INTEGER)
	inFragmentsRx = Column(INTEGER)
	inOversizeRx = Column(INTEGER)
	inJabberRx = Column(INTEGER)
	inMacRcvErrorRx = Column(INTEGER)
	inFCSErrorRx = Column(INTEGER)
	outFCSErrorTx = Column(INTEGER)
	deferedTx = Column(INTEGER)
	collisionTx = Column(INTEGER)
	lateTx = Column(INTEGER)
	exessiveTx = Column(INTEGER)
	singleTx = Column(INTEGER)
	multipleTx = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,switchPortNum,inUnicast,outUnicast,inBroadcast,outBroadcast,inMulticast,outMulricast,inUndersizeRx,inFragmentsRx,inOversizeRx,inJabberRx,inMacRcvErrorRx,inFCSErrorRx,outFCSErrorTx,deferedTx,collisionTx,lateTx,exessiveTx,singleTx,multipleTx,timestamp):
		self.idu_portSecondaryStatisticsTable_id = None
		self.host_id = host_id
		self.switchPortNum = switchPortNum
		self.inUnicast = inUnicast
		self.outUnicast = outUnicast
		self.inBroadcast = inBroadcast
		self.outBroadcast = outBroadcast
		self.inMulticast = inMulticast
		self.outMulricast = outMulricast
		self.inUndersizeRx = inUndersizeRx
		self.inFragmentsRx = inFragmentsRx
		self.inOversizeRx = inOversizeRx
		self.inJabberRx = inJabberRx
		self.inMacRcvErrorRx = inMacRcvErrorRx
		self.inFCSErrorRx = inFCSErrorRx
		self.outFCSErrorTx = outFCSErrorTx
		self.deferedTx = deferedTx
		self.collisionTx = collisionTx
		self.lateTx = lateTx
		self.exessiveTx = exessiveTx
		self.singleTx = singleTx
		self.multipleTx = multipleTx
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduPortSecondaryStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_portSecondaryStatisticsTable_id,self.host_id,self.switchPortNum,self.inUnicast,self.outUnicast,self.inBroadcast,self.outBroadcast,self.inMulticast,self.outMulricast,self.inUndersizeRx,self.inFragmentsRx,self.inOversizeRx,self.inJabberRx,self.inMacRcvErrorRx,self.inFCSErrorRx,self.outFCSErrorTx,self.deferedTx,self.collisionTx,self.lateTx,self.exessiveTx,self.singleTx,self.multipleTx,self.timestamp)

class IduPortqinqTable(Base):
	__tablename__= "idu_portqinqTable"
	idu_portqinqTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	switchportnumber = Column(INTEGER)
	portqinqstate = Column(INTEGER)
	providertag = Column(INTEGER)

	def __init__(self,config_profile_id,switchportnumber,portqinqstate,providertag):
		self.idu_portqinqTable_id = None
		self.config_profile_id = config_profile_id
		self.switchportnumber = switchportnumber
		self.portqinqstate = portqinqstate
		self.providertag = providertag
		
	def __repr__(self):
		return "<IduPortqinqTable('%s','%s','%s','%s','%s')>" %(self.idu_portqinqTable_id,self.config_profile_id,self.switchportnumber,self.portqinqstate,self.providertag)


class IduPortstatbadframeTable(Base):
	__tablename__= "idu_portstatbadframeTable"
	idu_portstatbadframeTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	switchbadframeport = Column(INTEGER)
	inundersizerx = Column(INTEGER)
	infragmnetsrx = Column(INTEGER)
	inoversizerx = Column(INTEGER)
	inmacrcverrorrx = Column(INTEGER)
	injabberrx = Column(INTEGER)
	infcserrorrx = Column(INTEGER)
	outfcserrtx = Column(INTEGER)
	defferedtx = Column(INTEGER)
	collisiontx = Column(INTEGER)
	latetx = Column(INTEGER)
	excessivetx = Column(INTEGER)
	singletx = Column(INTEGER)
	multipletx = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,switchbadframeport,inundersizerx,infragmnetsrx,inoversizerx,inmacrcverrorrx,injabberrx,infcserrorrx,outfcserrtx,defferedtx,collisiontx,latetx,excessivetx,singletx,multipletx,timestamp):
		self.idu_portstatbadframeTable_id = None
		self.host_id = host_id
		self.switchbadframeport = switchbadframeport
		self.inundersizerx = inundersizerx
		self.infragmnetsrx = infragmnetsrx
		self.inoversizerx = inoversizerx
		self.inmacrcverrorrx = inmacrcverrorrx
		self.injabberrx = injabberrx
		self.infcserrorrx = infcserrorrx
		self.outfcserrtx = outfcserrtx
		self.defferedtx = defferedtx
		self.collisiontx = collisiontx
		self.latetx = latetx
		self.excessivetx = excessivetx
		self.singletx = singletx
		self.multipletx = multipletx
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduPortstatbadframeTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_portstatbadframeTable_id,self.host_id,self.switchbadframeport,self.inundersizerx,self.infragmnetsrx,self.inoversizerx,self.inmacrcverrorrx,self.injabberrx,self.infcserrorrx,self.outfcserrtx,self.defferedtx,self.collisiontx,self.latetx,self.excessivetx,self.singletx,self.multipletx,self.timestamp)




class IduPortstatgoodframeTable(Base):
	__tablename__= "idu_portstatgoodframeTable"
	idu_portstatgoodframeTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	softwaregoodframeportnum = Column(INTEGER)
	inunicast = Column(INTEGER)
	outunicast = Column(INTEGER)
	inbroadcast = Column(INTEGER)
	outbroadcast = Column(INTEGER)
	inmulticast = Column(INTEGER)
	outmulticast = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,softwaregoodframeportnum,inunicast,outunicast,inbroadcast,outbroadcast,inmulticast,outmulticast,timestamp):
		self.idu_portstatgoodframeTable_id = None
		self.host_id = host_id
		self.softwaregoodframeportnum = softwaregoodframeportnum
		self.inunicast = inunicast
		self.outunicast = outunicast
		self.inbroadcast = inbroadcast
		self.outbroadcast = outbroadcast
		self.inmulticast = inmulticast
		self.outmulticast = outmulticast
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduPortstatgoodframeTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_portstatgoodframeTable_id,self.host_id,self.softwaregoodframeportnum,self.inunicast,self.outunicast,self.inbroadcast,self.outbroadcast,self.inmulticast,self.outmulticast,self.timestamp)



class IduPortstatisticsTable(Base):
	__tablename__= "idu_portstatisticsTable"
	idu_portstatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	softwarestatportnum = Column(INTEGER)
	framerx = Column(INTEGER)
	frametx = Column(INTEGER)
	indiscards = Column(INTEGER)
	ingoodoctets = Column(INTEGER)
	inbadoctet = Column(INTEGER)
	outoctets = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,softwarestatportnum,framerx,frametx,indiscards,ingoodoctets,inbadoctet,outoctets,timestamp):
		self.idu_portstatisticsTable_id = None
		self.host_id = host_id
		self.softwarestatportnum = softwarestatportnum
		self.framerx = framerx
		self.frametx = frametx
		self.indiscards = indiscards
		self.ingoodoctets = ingoodoctets
		self.inbadoctet = inbadoctet
		self.outoctets = outoctets
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduPortstatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_portstatisticsTable_id,self.host_id,self.softwarestatportnum,self.framerx,self.frametx,self.indiscards,self.ingoodoctets,self.inbadoctet,self.outoctets,self.timestamp)




class IduRtcConfigurationTable(Base):
	__tablename__= "idu_rtcConfigurationTable"
	idu_rtcConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	rtcIndex = Column(INTEGER)
	year = Column(INTEGER)
	month = Column(INTEGER)
	day = Column(INTEGER)
	hour = Column(INTEGER)
	min = Column(INTEGER)
	sec = Column(INTEGER)

	def __init__(self,config_profile_id,rtcIndex,year,month,day,hour,min,sec):
		self.idu_rtcConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.rtcIndex = rtcIndex
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.min = min
		self.sec = sec
		
	def __repr__(self):
		return "<IduRtcConfigurationTable('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_rtcConfigurationTable_id,self.config_profile_id,self.rtcIndex,self.year,self.month,self.day,self.hour,self.min,self.sec)




class IduSectorIdentificationTable(Base):
	__tablename__= "idu_sectorIdentificationTable"
	idu_sectorIdentificationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	sectorIndex = Column(INTEGER)
	countryCode = Column(INTEGER)
	operatorCode = Column(INTEGER)
	deploymentCode = Column(INTEGER)
	sectorCode = Column(INTEGER)

	def __init__(self,config_profile_id,sectorIndex,countryCode,operatorCode,deploymentCode,sectorCode):
		self.idu_sectorIdentificationTable_id = None
		self.config_profile_id = config_profile_id
		self.sectorIndex = sectorIndex
		self.countryCode = countryCode
		self.operatorCode = operatorCode
		self.deploymentCode = deploymentCode
		self.sectorCode = sectorCode
		
	def __repr__(self):
		return "<IduSectorIdentificationTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_sectorIdentificationTable_id,self.config_profile_id,self.sectorIndex,self.countryCode,self.operatorCode,self.deploymentCode,self.sectorCode)

class IduSwPrimaryPortStatisticsTable(Base):
	__tablename__= "idu_swPrimaryPortStatisticsTable"
	idu_swPrimaryPortStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	swportnumber = Column(INTEGER)
	framesRx = Column(INTEGER)
	framesTx = Column(INTEGER)
	inDiscard = Column(INTEGER)
	inGoodOctets = Column(INTEGER)
	inBadOctets = Column(INTEGER)
	outOctets = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,swportnumber,framesRx,framesTx,inDiscard,inGoodOctets,inBadOctets,outOctets,timestamp):
		self.idu_swPrimaryPortStatisticsTable_id = None
		self.host_id = host_id
		self.swportnumber = swportnumber
		self.framesRx = framesRx
		self.framesTx = framesTx
		self.inDiscard = inDiscard
		self.inGoodOctets = inGoodOctets
		self.inBadOctets = inBadOctets
		self.outOctets = outOctets
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduSwPrimaryPortStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_swPrimaryPortStatisticsTable_id,self.host_id,self.swportnumber,self.framesRx,self.framesTx,self.inDiscard,self.inGoodOctets,self.inBadOctets,self.outOctets,self.timestamp)


class IduSwStatusTable(Base):
	__tablename__= "idu_swStatusTable"
	idu_swStatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	swStatusIndex = Column(INTEGER)
	activeVersion = Column(VARCHAR(32))
	passiveVersion = Column(VARCHAR(32))
	bootloaderVersion = Column(VARCHAR(64))
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,swStatusIndex,activeVersion,passiveVersion,bootloaderVersion,timestamp):
		self.idu_swStatusTable_id = None
		self.host_id = host_id
		self.swStatusIndex = swStatusIndex
		self.activeVersion = activeVersion
		self.passiveVersion = passiveVersion
		self.bootloaderVersion = bootloaderVersion
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduSwStatusTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_swStatusTable_id,self.host_id,self.swStatusIndex,self.activeVersion,self.passiveVersion,self.bootloaderVersion,self.timestamp)




class IduSwitchPortconfigTable(Base):
	__tablename__= "idu_switchPortconfigTable"
	idu_switchPortconfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	switchportNum = Column(INTEGER)
	swadminState = Column(INTEGER)
	swlinkMode = Column(INTEGER)
	portvid = Column(INTEGER)
	macauthState = Column(INTEGER)
	mirroringdirection = Column(INTEGER)
	portdotqmode = Column(INTEGER)
	macflowcontrol = Column(INTEGER)

	def __init__(self,config_profile_id,switchportNum,swadminState,swlinkMode,portvid,macauthState,mirroringdirection,portdotqmode,macflowcontrol):
		self.idu_switchPortconfigTable_id = None
		self.config_profile_id = config_profile_id
		self.switchportNum = switchportNum
		self.swadminState = swadminState
		self.swlinkMode = swlinkMode
		self.portvid = portvid
		self.macauthState = macauthState
		self.mirroringdirection = mirroringdirection
		self.portdotqmode = portdotqmode
		self.macflowcontrol = macflowcontrol
		
	def __repr__(self):
		return "<IduSwitchPortconfigTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_switchPortconfigTable_id,self.config_profile_id,self.switchportNum,self.swadminState,self.swlinkMode,self.portvid,self.macauthState,self.mirroringdirection,self.portdotqmode,self.macflowcontrol)





class IduSwitchportstatusTable(Base):
	__tablename__= "idu_switchportstatusTable"
	idu_switchportstatusTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	switchstatportnum = Column(INTEGER)
	opstate = Column(INTEGER)
	linkspeed = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,switchstatportnum,opstate,linkspeed,timestamp):
		self.idu_switchportstatusTable_id = None
		self.host_id = host_id
		self.switchstatportnum = switchstatportnum
		self.opstate = opstate
		self.linkspeed = linkspeed
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduSwitchportstatusTable('%s','%s','%s','%s','%s','%s')>" %(self.idu_switchportstatusTable_id,self.host_id,self.switchstatportnum,self.opstate,self.linkspeed,self.timestamp)



class IduSysOmcRegistrationTable(Base):
	__tablename__= "idu_sysOmcRegistrationTable"
	idu_sysOmcRegistrationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	sysOmcRegistrationIndex = Column(INTEGER)
	sysOmcRegisterContactAddr = Column(VARCHAR(32))
	sysOmcRegisterContactPerson = Column(VARCHAR(32))
	sysOmcRegisterContactMobile = Column(VARCHAR(32))
	sysOmcRegisterAlternateContact = Column(VARCHAR(32))
	sysOmcRegisterContactEmail = Column(VARCHAR(32))

	def __init__(self,config_profile_id,sysOmcRegistrationIndex,sysOmcRegisterContactAddr,sysOmcRegisterContactPerson,sysOmcRegisterContactMobile,sysOmcRegisterAlternateContact,sysOmcRegisterContactEmail):
		self.idu_sysOmcRegistrationTable_id = None
		self.config_profile_id = config_profile_id
		self.sysOmcRegistrationIndex = sysOmcRegistrationIndex
		self.sysOmcRegisterContactAddr = sysOmcRegisterContactAddr
		self.sysOmcRegisterContactPerson = sysOmcRegisterContactPerson
		self.sysOmcRegisterContactMobile = sysOmcRegisterContactMobile
		self.sysOmcRegisterAlternateContact = sysOmcRegisterAlternateContact
		self.sysOmcRegisterContactEmail = sysOmcRegisterContactEmail
		
	def __repr__(self):
		return "<IduSysOmcRegistrationTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_sysOmcRegistrationTable_id,self.config_profile_id,self.sysOmcRegistrationIndex,self.sysOmcRegisterContactAddr,self.sysOmcRegisterContactPerson,self.sysOmcRegisterContactMobile,self.sysOmcRegisterAlternateContact,self.sysOmcRegisterContactEmail)



class IduTdmoipNetworkInterfaceConfigurationTable(Base):
	__tablename__= "idu_tdmoipNetworkInterfaceConfigurationTable"
	idu_tdmoipNetworkInterfaceConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	interfaceid = Column(INTEGER)
	ipaddress = Column(VARCHAR(32))

	def __init__(self,config_profile_id,interfaceid,ipaddress):
		self.idu_tdmoipNetworkInterfaceConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.interfaceid = interfaceid
		self.ipaddress = ipaddress
		
	def __repr__(self):
		return "<IduTdmoipNetworkInterfaceConfigurationTable('%s','%s','%s','%s')>" %(self.idu_tdmoipNetworkInterfaceConfigurationTable_id,self.config_profile_id,self.interfaceid,self.ipaddress)



class IduTdmoipNetworkInterfaceStatisticsTable(Base):
	__tablename__= "idu_tdmoipNetworkInterfaceStatisticsTable"
	idu_tdmoipNetworkInterfaceStatisticsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	indexid = Column(INTEGER)
	bytesTransmitted = Column(INTEGER)
	bytesReceived = Column(INTEGER)
	framesTransmittedOk = Column(INTEGER)
	framesReceivedOk = Column(INTEGER)
	goodClassifiedFramesRx = Column(INTEGER)
	checksumErrorPackets = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,indexid,bytesTransmitted,bytesReceived,framesTransmittedOk,framesReceivedOk,goodClassifiedFramesRx,checksumErrorPackets,timestamp):
		self.idu_tdmoipNetworkInterfaceStatisticsTable_id = None
		self.host_id = host_id
		self.indexid = indexid
		self.bytesTransmitted = bytesTransmitted
		self.bytesReceived = bytesReceived
		self.framesTransmittedOk = framesTransmittedOk
		self.framesReceivedOk = framesReceivedOk
		self.goodClassifiedFramesRx = goodClassifiedFramesRx
		self.checksumErrorPackets = checksumErrorPackets
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<IduTdmoipNetworkInterfaceStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_tdmoipNetworkInterfaceStatisticsTable_id,self.host_id,self.indexid,self.bytesTransmitted,self.bytesReceived,self.framesTransmittedOk,self.framesReceivedOk,self.goodClassifiedFramesRx,self.checksumErrorPackets,self.timestamp)



class IduTemperatureSensorConfigurationTable(Base):
	__tablename__= "idu_temperatureSensorConfigurationTable"
	idu_temperatureSensorConfigurationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	tempIndex = Column(INTEGER)
	tempMax = Column(INTEGER)
	tempMin = Column(INTEGER)

	def __init__(self,config_profile_id,tempIndex,tempMax,tempMin):
		self.idu_temperatureSensorConfigurationTable_id = None
		self.config_profile_id = config_profile_id
		self.tempIndex = tempIndex
		self.tempMax = tempMax
		self.tempMin = tempMin
		
	def __repr__(self):
		return "<IduTemperatureSensorConfigurationTable('%s','%s','%s','%s','%s')>" %(self.idu_temperatureSensorConfigurationTable_id,self.config_profile_id,self.tempIndex,self.tempMax,self.tempMin)

class IduVlanconfigTable(Base):
	__tablename__= "idu_vlanconfigTable"
	idu_vlanconfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	vlanid = Column(INTEGER)
	vlanname = Column(VARCHAR(16))
	vlantype = Column(INTEGER)
	vlantag = Column(INTEGER)
	memberports = Column(INTEGER)
	vlanrowstatus = Column(INTEGER)

	def __init__(self,config_profile_id,vlanid,vlanname,vlantype,vlantag,memberports,vlanrowstatus):
		self.idu_vlanconfigTable_id = None
		self.config_profile_id = config_profile_id
		self.vlanid = vlanid
		self.vlanname = vlanname
		self.vlantype = vlantype
		self.vlantag = vlantag
		self.memberports = memberports
		self.vlanrowstatus = vlanrowstatus
		
	def __repr__(self):
		return "<IduVlanconfigTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.idu_vlanconfigTable_id,self.config_profile_id,self.vlanid,self.vlanname,self.vlantype,self.vlantag,self.memberports,self.vlanrowstatus)

class IduOidTable(Base):
    __tablename__= "idu_oid_table"
    table_name = Column(VARCHAR(64),primary_key=True)
    table_oid = Column(VARCHAR(64))
    varbinds = Column(TINYINT)

    def __init__(self,table_name,table_oid,varbinds):
        self.table_name = table_name
        self.table_oid = table_oid
        self.varbinds = varbinds
        
    def __repr__(self):
        return "<IduOid_table('%s','%s','%s')>" %(self.table_name,self.table_oid,self.varbinds)



########################################################### Master Slave Linking Classes Of Tables#######################################################

# create class for master_slave_linking table 
class MasterSlaveLinking(Base):
    __tablename__  = 'master_slave_linking'

    master_slave_linking_id =Column(Integer,primary_key=True)
    master = Column(Integer)
    slave = Column(Integer)

    def __init__(self,master,slave):
        self.master_slave_linking_id = None
        self.master = master 
        self.slave = slave 

    def __repr__(self):
        return "<MasterSlaveLinking('%s','%s','%s')>" % (self.master_slave_linking_id,self.acltype_vap,self.maclist,self.vap_vap)

##########################################################################################################################################################
##
###########################################################################################################################################################

##################################### AP MODEL STARTS HERE #######################################################################################

class Ap25AccesspointIPsettings(Base):
    __tablename__= "ap25_accesspointIPsettings"
    ap25_accesspointIPsettings_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    lanIPaddress = Column(VARCHAR(16))
    lanSubnetMask = Column(VARCHAR(16))
    lanGatewayIP = Column(VARCHAR(16))
    lanPrimaryDNS = Column(VARCHAR(16))
    lanSecondaryDNS = Column(VARCHAR(16))

    def __init__(self,config_profile_id,lanIPaddress,lanSubnetMask,lanGatewayIP,lanPrimaryDNS,lanSecondaryDNS):
        self.ap25_accesspointIPsettings_id = None
        self.config_profile_id = config_profile_id
        self.lanIPaddress = lanIPaddress
        self.lanSubnetMask = lanSubnetMask
        self.lanGatewayIP = lanGatewayIP
        self.lanPrimaryDNS = lanPrimaryDNS
        self.lanSecondaryDNS = lanSecondaryDNS
        
    def __repr__(self):
        return "<Ap25AccesspointIPsettings('%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_accesspointIPsettings_id,self.config_profile_id,self.lanIPaddress,self.lanSubnetMask,self.lanGatewayIP,self.lanPrimaryDNS,self.lanSecondaryDNS)


class Ap25AclMacTable(Base):
    __tablename__= "ap25_aclMacTable"
    ap25_aclMacTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    vapselection_id = Column(INTEGER,ForeignKey('ap25_vapSelection.ap25_vapSelection_id'))
    aclMACsIndex = Column(SMALLINT)
    macaddress = Column(VARCHAR(18))
    

    def __init__(self,config_profile_id,ap25_aclMacTable_id,vapselection_id,aclMACsIndex,macaddress):
        self.ap25_aclMacTable_id = None
        self.config_profile_id = config_profile_id
        self.vapselection_id = vapselection_id
        self.aclMACsIndex = aclMACsIndex
        self.macaddress = macaddress
        
    def __repr__(self):
        return "<Ap25AclMacTable('%s','%s','%s','%s','%s')>" %(self.ap25_aclMacTable_id,self.config_profile_id,self.vapselection_id,self.aclMACsIndex,self.macaddress)

class Ap25AclStatisticsTable(Base):
	__tablename__= "ap25_aclStatisticsTable"
	ap25_aclStatisticsTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	aclTotalsINDEX = Column(INTEGER)
	vapNumber = Column(INTEGER)
	totalMACentries = Column(INTEGER)

	def __init__(self,config_profile_id,aclTotalsINDEX,vapNumber,totalMACentries):
		self.ap25_aclStatisticsTable_id = None
		self.config_profile_id = config_profile_id
		self.aclTotalsINDEX = aclTotalsINDEX
		self.vapNumber = vapNumber
		self.totalMACentries = totalMACentries
		
	def __repr__(self):
		return "<Ap25AclStatisticsTable('%s','%s','%s','%s','%s')>" %(self.ap25_aclStatisticsTable_id,self.config_profile_id,self.aclTotalsINDEX,self.vapNumber,self.totalMACentries)


class Ap25BasicACLconfigTable(Base):
    __tablename__= "ap25_basicACLconfigTable"
    ap25_basicACLconfigTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    vapselection_id = Column(INTEGER,ForeignKey('ap25_vapSelection.ap25_vapSelection_id'))
    aclState = Column(SMALLINT)
    aclMode = Column(SMALLINT)
    aclAddMAC = Column(VARCHAR(18))
    aclDeleteOneMAC = Column(VARCHAR(10))
    aclDeleteAllMACs = Column(VARCHAR(10))

    def __init__(self,config_profile_id,vapselection_id,aclState,aclMode,aclAddMAC='',aclDeleteOneMAC='',aclDeleteAllMACs=0):
        self.ap25_basicACLconfigTable_id= None
        self.config_profile_id = config_profile_id
        self.vapselection_id = vapselection_id
        self.aclState = aclState
        self.aclMode = aclMode
        self.aclAddMAC = aclAddMAC
        self.aclDeleteOneMAC = aclDeleteOneMAC
        self.aclDeleteAllMACs = aclDeleteAllMACs
        
    def __repr__(self):
        return "<Ap25BasicACLsetup('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_basicACLconfigTable_id,self.config_profile_id,self.vapselection_id,self.aclState,self.aclMode,\
                                                                                self.aclAddMAC,self.aclDeleteOneMAC,self.aclDeleteAllMACs)

class Ap25BasicConfiguration(Base):
	__tablename__= "ap25_basicConfiguration"
	ap25_basicConfiguration_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	accesspointName = Column(VARCHAR(16))

	def __init__(self,config_profile_id,accesspointName):
		self.ap25_basicConfiguration_id = None
		self.config_profile_id = config_profile_id
		self.accesspointName = accesspointName
		
	def __repr__(self):
		return "<Ap25BasicConfiguration('%s','%s','%s')>" %(self.ap25_basicConfiguration_id,self.config_profile_id,self.accesspointName)

class Ap25BasicVAPsecurity(Base):
    __tablename__= "ap25_basicVAPsecurity"
    ap25_basicVAPsecurity_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    vapselection_id = Column(INTEGER,ForeignKey('ap25_vapSelection.ap25_vapSelection_id'))
    vapSecurityMode = Column(SMALLINT)

    def __init__(self,config_profile_id,vapselection_id,vapSecurityMode):
        self.ap25_basicVAPsecurity_id = None
        self.config_profile_id = config_profile_id
        self.vapselection_id = vapselection_id
        self.vapSecurityMode = vapSecurityMode
        
    def __repr__(self):
        return "<Ap25BasicVAPsecurity('%s','%s','%s','%s')>" %(self.ap25_basicVAPsecurity_id,self.config_profile_id,self.vapselection_id,self.vapSecurityMode)



class Ap25BasicVAPconfigTable(Base):
    __tablename__= "ap25_basicVAPconfigTable"
    ap25_basicVAPconfigTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    vapselection_id = Column(INTEGER,ForeignKey('ap25_vapSelection.ap25_vapSelection_id'))
    vapESSID = Column(VARCHAR(32))
    vapHiddenESSIDstate = Column(SMALLINT)
    vapRTSthresholdValue = Column(SMALLINT)
    vapFragmentationThresholdValue = Column(SMALLINT)
    vapBeaconInterval = Column(SMALLINT)
    vlanId = Column(INTEGER)
    vlanPriority = Column(INTEGER)
    vapMode = Column(INTEGER)
    vapSecurityMode = Column(SMALLINT)
    vapRadioMac=Column(VARCHAR(20))

    def __init__(self,config_profile_id,vapselection_id,vapESSID,vapHiddenESSIDstate,vapRTSthresholdValue,vapFragmentationThresholdValue,vapBeaconInterval,vlanId=0,vlanPriority=0,vapMode=0,vapSecurityMode=0,vapRadioMac=""):
        self.ap25_basicVAPconfigTable_id = None
        self.config_profile_id = config_profile_id
        self.vapselection_id = vapselection_id
        self.vapESSID = vapESSID
        self.vapHiddenESSIDstate = vapHiddenESSIDstate
        self.vapRTSthresholdValue = vapRTSthresholdValue
        self.vapFragmentationThresholdValue = vapFragmentationThresholdValue
        self.vapBeaconInterval = vapBeaconInterval
        self.vlanId = vlanId
        self.vlanPriority = vlanPriority
        self.vapMode = vapMode
        self.vapSecurityMode = vapSecurityMode
        self.vapRadioMac = vapRadioMac
    def __repr__(self):
        return "<Ap25BasicVAPsetup('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>"\
     %(self.ap25_basicVAPconfigTable_id, self.config_profile_id, self.vapselection_id, self.vapESSID, self.vapHiddenESSIDstate,\
    self.vapRTSthresholdValue, self.vapFragmentationThresholdValue, self.vapBeaconInterval, self.vlanId, self.vlanPriority, self.vapMode, self.vapSecurityMode, self.vapRadioMac)

class Ap25DhcpServer(Base):
    __tablename__= "ap25_dhcpServer"
    ap25_dhcpServer_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    dhcpServerStatus = Column(TINYINT)
    dhcpStartIPaddress = Column(VARCHAR(16))
    dhcpEndIPaddress = Column(VARCHAR(16))
    dhcpSubnetMask = Column(VARCHAR(16))
    dhcpClientLeaseTime = Column(INTEGER)

    def __init__(self,config_profile_id,dhcpServerStatus,dhcpStartIPaddress,dhcpEndIPaddress,dhcpSubnetMask,dhcpClientLeaseTime):
        self.ap25_dhcpServer_id = None
        self.config_profile_id = config_profile_id
        self.dhcpServerStatus = dhcpServerStatus
        self.dhcpStartIPaddress = dhcpStartIPaddress
        self.dhcpEndIPaddress = dhcpEndIPaddress
        self.dhcpSubnetMask = dhcpSubnetMask
        self.dhcpClientLeaseTime = dhcpClientLeaseTime
        
    def __repr__(self):
        return "<Ap25DhcpServer('%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_dhcpServer_id,self.config_profile_id,self.dhcpServerStatus,self.dhcpStartIPaddress,self.dhcpEndIPaddress,self.dhcpSubnetMask,self.dhcpClientLeaseTime)

class Ap25DhcpClientsTable(Base):
	__tablename__= "ap25_dhcpClientsTable"
	ap25_dhcpClientsTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	dhcpClientsMACaddress = Column(VARCHAR(20))
	dhcpClientsIPaddress = Column(VARCHAR(16))
	dhcpClientsExpiresIn = Column(VARCHAR(32))
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,dhcpClientsMACaddress,dhcpClientsIPaddress,dhcpClientsExpiresIn):
		self.ap25_dhcpClientsTable_id = None
		self.host_id = host_id
		self.dhcpClientsMACaddress = dhcpClientsMACaddress
		self.dhcpClientsIPaddress = dhcpClientsIPaddress
		self.dhcpClientsExpiresIn = dhcpClientsExpiresIn
		self.timestamp = None
		
	def __repr__(self):
		return "<Ap25DhcpClientsTable('%s','%s','%s','%s','%s','%s')>" %(self.ap25_dhcpClientsTable_id,self.host_id,self.dhcpClientsMACaddress,self.dhcpClientsIPaddress,self.dhcpClientsExpiresIn,self.timestamp)


class Ap25ApScanDataTable(Base):
	__tablename__= "ap25_apScanDataTable"
	ap25_apScanDataTable_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	macAddress = Column(VARCHAR(20))
	essid = Column(VARCHAR(32))
	frequency = Column(VARCHAR(10))
	quality = Column(VARCHAR(10))
	signalLevel = Column(VARCHAR(10))
	noiseLevel = Column(VARCHAR(10))
	beconIntervel = Column(VARCHAR(10))
	Timestamp = Column(TIMESTAMP)

	def __init__(self,host_id,macAddress,essid,frequency,quality,signalLevel,noiseLevel,beconIntervel):
		self.ap25_apScanDataTable_id = None
		self.host_id = host_id
		self.macAddress = macAddress
		self.essid = essid
		self.frequency = frequency
		self.quality = quality
		self.signalLevel = signalLevel
		self.noiseLevel = noiseLevel
		self.beconIntervel = beconIntervel
		self.Timestamp = None
		
	def __repr__(self):
		return "<Ap25ApScanDataTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_apScanDataTable_id,self.host_id,self.macAddress,self.essid,self.frequency,self.quality,self.signalLevel,self.noiseLevel,self.beconIntervel,self.Timestamp)


class Ap25RadioSelection(Base):
    __tablename__= "ap25_radioSelection"
    ap25_radioSelection_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    radio = Column(VARCHAR(10))

    def __init__(self,config_profile_id,radio):
        self.ap25_radioSelection_id = None
        self.config_profile_id = config_profile_id
        self.radio = radio
        
    def __repr__(self):
        return "<Ap25RadioSelection('%s','%s','%s')>" %(self.ap25_radioSelection_id,self.config_profile_id,self.radio)

class Ap25RadioSetup(Base):
    __tablename__= "ap25_radioSetup"
    ap25_radioSetup_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    radioState = Column(SMALLINT)
    radioAPmode = Column(SMALLINT)
    radioManagementVLANstate = Column(SMALLINT)
    radioCountryCode = Column(INTEGER)
    numberOfVAPs = Column(SMALLINT)
    radioChannel = Column(SMALLINT)
    wifiMode = Column(SMALLINT)
    radioTxPower = Column(SMALLINT)
    radioGatingIndex = Column(SMALLINT)
    radioAggregation = Column(SMALLINT)
    radioAggFrames = Column(INTEGER)
    radioAggSize = Column(INTEGER)
    radioAggMinSize = Column(INTEGER)
    radioChannelWidth = Column(SMALLINT)
    radioTXChainMask = Column(SMALLINT)
    radioRXChainMask = Column(SMALLINT)

    def __init__(self,config_profile_id,radioState,radioAPmode,radioManagementVLANstate,radioCountryCode,numberOfVAPs,radioChannel,wifiMode,radioTxPower,radioGatingIndex,radioAggregation,radioAggFrames,radioAggSize,radioAggMinSize,radioChannelWidth,radioTXChainMask,radioRXChainMask):
        self.ap25_radioSetup_id = None
        self.config_profile_id = config_profile_id
        self.radioState = radioState
        self.radioAPmode = radioAPmode
        self.radioManagementVLANstate = radioManagementVLANstate
        self.radioCountryCode = radioCountryCode
        self.numberOfVAPs = numberOfVAPs
        self.radioChannel = radioChannel
        self.wifiMode = wifiMode
        self.radioTxPower = radioTxPower
        self.radioGatingIndex = radioGatingIndex
        self.radioAggregation = radioAggregation
        self.radioAggFrames = radioAggFrames
        self.radioAggSize = radioAggSize
        self.radioAggMinSize = radioAggMinSize
        self.radioChannelWidth = radioChannelWidth
        self.radioTXChainMask = radioTXChainMask
        self.radioRXChainMask = radioRXChainMask
        
    def __repr__(self):
        return "<Ap25RadioSetup('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" \
    %(self.ap25_radioSetup_id,self.config_profile_id,self.radioState,self.radioAPmode,self.radioManagementVLANstate,self.radioCountryCode,self.numberOfVAPs,self.radioChannel,self.wifiMode,self.radioTxPower,self.radioGatingIndex,self.radioAggregation,self.radioAggFrames,self.radioAggSize,self.radioAggMinSize,self.radioChannelWidth,self.radioTXChainMask,self.radioRXChainMask)


class Ap25Services(Base):
    __tablename__= "ap25_services"
    ap25_services_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    upnpServerStatus = Column(SMALLINT)
    systemLogStatus = Column(SMALLINT)
    systemLogIP = Column(VARCHAR(16))
    systemLogPort = Column(INTEGER)
    systemTime = Column(VARCHAR(31))

    def __init__(self,config_profile_id,upnpServerStatus,systemLogStatus,systemLogIP,systemLogPort,systemTime):
        self.ap25_services_id = None
        self.config_profile_id = config_profile_id
        self.upnpServerStatus = upnpServerStatus
        self.systemLogStatus = systemLogStatus
        self.systemLogIP = systemLogIP
        self.systemLogPort = systemLogPort
        self.systemTime = systemTime
        
    def __repr__(self):
        return "<Ap25Services('%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_services_id,self.config_profile_id,self.upnpServerStatus,self.systemLogStatus,self.systemLogIP,self.systemLogPort,self.systemTime)

class Ap25StatisticsTable(Base):
    __tablename__= "ap25_statisticsTable"
    ap25_systemInfo_id = Column(INTEGER,primary_key=True)
    host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
    statisticsIndex = Column(INTEGER)
    statisticsInterface = Column(VARCHAR(30))
    statisticsRxPackets = Column(INTEGER)
    statisticsTxPackets = Column(INTEGER)
    statisticsRxError = Column(INTEGER)
    statisticsTxError = Column(INTEGER)

    def __init__(self,host_id,statisticsIndex,statisticsInterface,statisticsRxPackets,statisticsTxPackets,statisticsRxError,statisticsTxError):
        self.ap25_systemInfo_id = None
        self.host_id = host_id
        self.statisticsIndex = statisticsIndex
        self.statisticsInterface = statisticsInterface
        self.statisticsRxPackets = statisticsRxPackets
        self.statisticsTxPackets = statisticsTxPackets
        self.statisticsRxError = statisticsRxError
        self.statisticsTxError = statisticsTxError
        
    def __repr__(self):
        return "<Ap25StatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_systemInfo_id,self.host_id,self.statisticsIndex,self.statisticsInterface,self.statisticsRxPackets,self.statisticsTxPackets,self.statisticsRxError,self.statisticsTxError)

class Ap25VapClientStatisticsTable(Base):
    __tablename__= "ap25_vapClientStatisticsTable"
    ap25_vapClientStatisticsTable_id = Column(INTEGER,primary_key=True)
    host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
    slNum = Column(INTEGER)
    addressMAC = Column(INTEGER)
    aid = Column(INTEGER)
    chan = Column(INTEGER)
    txRate = Column(VARCHAR(11))
    rxRate = Column(VARCHAR(11))
    rssi = Column(INTEGER)
    idle = Column(INTEGER)
    txSEQ = Column(INTEGER)
    rxSEQ = Column(INTEGER)
    caps = Column(VARCHAR(11))

    def __init__(self,host_id,slNum,addressMAC,aid,chan,txRate,rxRate,rssi,idle,txSEQ,rxSEQ,caps):
        self.ap25_vapClientStatisticsTable_id = None
        self.host_id = host_id
        self.slNum = slNum
        self.addressMAC = addressMAC
        self.aid = aid
        self.chan = chan
        self.txRate = txRate
        self.rxRate = rxRate
        self.rssi = rssi
        self.idle = idle
        self.txSEQ = txSEQ
        self.rxSEQ = rxSEQ
        self.caps = caps
        
    def __repr__(self):
        return "<Ap25VapClientStatisticsTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_vapClientStatisticsTable_id,self.host_id,self.slNum,self.addressMAC,self.aid,self.chan,self.txRate,self.rxRate,self.rssi,self.idle,self.txSEQ,self.rxSEQ,self.caps)

class Ap25VapSelection(Base):
    __tablename__= "ap25_vapSelection"
    ap25_vapSelection_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    totalVAPsPresent = Column(INTEGER)
    selectVap = Column(SMALLINT)

    def __init__(self,config_profile_id,totalVAPsPresent,selectVap):
        self.ap25_vapSelection_id = None
        self.config_profile_id = config_profile_id
        self.totalVAPsPresent = totalVAPsPresent
        self.selectVap = selectVap
        
    def __repr__(self):
        return "<Ap25VapSelection('%s','%s','%s','%s')>" %(self.ap25_vapSelection_id,self.config_profile_id,self.totalVAPsPresent,self.selectVap)

class Ap25VapWEPsecurityConfigTable(Base):
    __tablename__= "ap25_vapWEPsecurityConfigTable"
    ap25_vapWEPsecurityConfigTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id')) 
    basicVAPconfigIndex = Column(INTEGER)   
    vapWEPmode = Column(SMALLINT)
    vapWEPprimaryKey = Column(SMALLINT)
    vapWEPkey1 = Column(VARCHAR(22))
    vapWEPkey2 = Column(VARCHAR(22))
    vapWEPkey3 = Column(VARCHAR(22))
    vapWEPkey4 = Column(VARCHAR(22))

    def __init__(self,config_profile_id,basicVAPconfigIndex,vapWEPmode,vapWEPprimaryKey,vapWEPkey1,vapWEPkey2,vapWEPkey3,vapWEPkey4):
        self.ap25_vapWEPsecurityConfigTable_id = None
        self.config_profile_id = config_profile_id        
        self.basicVAPconfigIndex = basicVAPconfigIndex
        self.vapWEPmode = vapWEPmode
        self.vapWEPprimaryKey = vapWEPprimaryKey
        self.vapWEPkey1 = vapWEPkey1
        self.vapWEPkey2 = vapWEPkey2
        self.vapWEPkey3 = vapWEPkey3
        self.vapWEPkey4 = vapWEPkey4
        
    def __repr__(self):
        return "<Ap25VapWEPsecuritySetup('%s','%s','%s','%s','%s','%s','%s','%s')>"\
        %(self.ap25_vapWEPsecurityConfigTable_id,self.config_profile_id,self.vapWEPmode,self.vapWEPprimaryKey,self.vapWEPkey1,self.vapWEPkey2,self.vapWEPkey3,self.vapWEPkey4)

class Ap25VapWPAsecurityConfigTable(Base):
    __tablename__= "ap25_vapWPAsecurityConfigTable"
    ap25_vapWPAsecurityConfigTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    vapselection_id = Column(INTEGER,ForeignKey('ap25_vapSelection.ap25_vapSelection_id'))
    vapWPAmode = Column(SMALLINT)
    vapWPAcypher = Column(SMALLINT)
    vapWPArekeyInterval = Column(INTEGER)
    vapWPAmasterReKey = Column(INTEGER)
    vapWEPrekeyInt = Column(INTEGER)
    vapWPAkeyMode = Column(SMALLINT)
    vapWPAconfigPSKPassPhrase = Column(VARCHAR(33))
    vapWPArsnPreAuth = Column(SMALLINT)
    vapWPArsnPreAuthInterface = Column(VARCHAR(16))
    vapWPAeapReAuthPeriod = Column(INTEGER)
    vapWPAserverIP = Column(VARCHAR(16))
    vapWPAserverPort = Column(INTEGER)
    vapWPAsharedSecret = Column(VARCHAR(32))

    def __init__(self,config_profile_id,vapselection_id,vapWPAmode,vapWPAcypher,vapWPArekeyInterval,vapWPAmasterReKey,vapWEPrekeyInt,vapWPAkeyMode,vapWPAconfigPSKPassPhrase,vapWPArsnPreAuth,vapWPArsnPreAuthInterface,vapWPAeapReAuthPeriod,vapWPAserverIP,vapWPAserverPort,vapWPAsharedSecret):
        self.ap25_vapWPAsecurityConfigTable_id = None
        self.config_profile_id = config_profile_id
        self.vapselection_id = vapselection_id
        self.vapWPAmode = vapWPAmode
        self.vapWPAcypher = vapWPAcypher
        self.vapWPArekeyInterval = vapWPArekeyInterval
        self.vapWPAmasterReKey = vapWPAmasterReKey
        self.vapWEPrekeyInt = vapWEPrekeyInt
        self.vapWPAkeyMode = vapWPAkeyMode
        self.vapWPAconfigPSKPassPhrase = vapWPAconfigPSKPassPhrase
        self.vapWPArsnPreAuth = vapWPArsnPreAuth
        self.vapWPArsnPreAuthInterface = vapWPArsnPreAuthInterface
        self.vapWPAeapReAuthPeriod = vapWPAeapReAuthPeriod
        self.vapWPAserverIP = vapWPAserverIP
        self.vapWPAserverPort = vapWPAserverPort
        self.vapWPAsharedSecret = vapWPAsharedSecret
        
    def __repr__(self):
        return "<Ap25VapWPAsecuritySetup('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap25_vapWPAsecurityConfigTable_id,self.config_profile_id,self.vapselection_id,self.vapWPAmode,self.vapWPAcypher,self.vapWPArekeyInterval,self.vapWPAmasterReKey,self.vapWEPrekeyInt,self.vapWPAkeyMode,self.vapWPAconfigPSKPassPhrase,self.vapWPArsnPreAuth,self.vapWPArsnPreAuthInterface,self.vapWPAeapReAuthPeriod,self.vapWPAserverIP,self.vapWPAserverPort,self.vapWPAsharedSecret)

class Ap25Versions(Base):
	__tablename__= "ap25_versions"
	ap25_versions_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	hardwareVersion = Column(VARCHAR(15))
	softwareVersion = Column(VARCHAR(25))
	bootLoaderVersion = Column(VARCHAR(15))

	def __init__(self,host_id,hardwareVersion,softwareVersion,bootLoaderVersion):
		self.ap25_versions_id = None
		self.host_id = host_id
		self.hardwareVersion = hardwareVersion
		self.softwareVersion = softwareVersion
		self.bootLoaderVersion = bootLoaderVersion
		
	def __repr__(self):
		return "<Ap25Versions('%s','%s','%s','%s','%s')>" %(self.ap25_versions_id,self.host_id,self.hardwareVersion,self.softwareVersion,self.bootLoaderVersion)

class Ap25Oid_table(Base):
	__tablename__= "ap25_oid_table"
	table_name = Column(VARCHAR(64),primary_key=True)
	table_oid = Column(VARCHAR(64))
	varbinds = Column(TINYINT)
	is_recon = Column(INTEGER)
	status = Column(INTEGER)
	isNode = Column(TINYINT)
	timestamp = Column(TIMESTAMP)

	def __init__(self,table_name,table_oid,varbinds,is_recon,status,isNode,timestamp):
		self.table_name = table_name
		self.table_oid = table_oid
		self.varbinds = varbinds
		self.is_recon = is_recon
		self.status = status
		self.isNode = isNode
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<Ap25Oid_table('%s','%s','%s','%s','%s','%s','%s')>" %(self.table_name,self.table_oid,self.varbinds,self.is_recon,self.status,self.isNode,self.timestamp)




class Ap25Oids(Base):
	__tablename__= "ap25_oids"
	oid_id = Column(INTEGER,primary_key=True)
	device_type_id = Column(VARCHAR(16))
	oid = Column(VARCHAR(256))
	oid_name = Column(VARCHAR(256))
	oid_type = Column(VARCHAR(16))
	access = Column(SMALLINT)
	default_value = Column(VARCHAR(256))
	min_value = Column(VARCHAR(128))
	max_value = Column(VARCHAR(256))
	indexes = Column(VARCHAR(256))
	dependent_id = Column(INTEGER)
	multivalue = Column(SMALLINT)
	table_name = Column(VARCHAR(128))
	coloumn_name = Column(VARCHAR(128))
	indexes_name = Column(VARCHAR(64))

	def __init__(self,oid_id,device_type_id,oid,oid_name,oid_type,access,default_value,min_value,max_value,indexes,dependent_id,multivalue,table_name,coloumn_name,indexes_name):
		self.oid_id = None
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
		self.indexes_name = indexes_name
		
	def __repr__(self):
		return "<Ap25Oids('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.oid_id,self.device_type_id,self.oid,self.oid_name,self.oid_type,self.access,self.default_value,self.min_value,self.max_value,self.indexes,self.dependent_id,self.multivalue,self.table_name,self.coloumn_name,self.indexes_name)

class Ap25OidsMultivalues(Base):
	__tablename__= "ap25_oids_multivalues"
	oids_multivalue_id = Column(INTEGER,primary_key=True)
	oid_id = Column(INTEGER)
	value = Column(VARCHAR(128))
	name = Column(VARCHAR(128))

	def __init__(self,oids_multivalue_id,oid_id,value,name):
		self.oids_multivalue_id = None
		self.oid_id = oid_id
		self.value = value
		self.name = name
		
	def __repr__(self):
		return "<Ap25Oids_multivalues('%s','%s','%s','%s')>" %(self.oids_multivalue_id,self.oid_id,self.value,self.name)


class ApClient_ap_data(Base):
	__tablename__= "ap_client_ap_data"
	ap_client_ap_data_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	client_id = Column(INTEGER)
	client_mac = Column(VARCHAR(20))
	vap_id = Column(TINYINT)
	slNum = Column(INTEGER)
	aid = Column(INTEGER)
	chan = Column(INTEGER)
	txRate = Column(VARCHAR(11))
	rxRate = Column(VARCHAR(11))
	rssi = Column(INTEGER)
	idle = Column(INTEGER)
	total_tx = Column(INTEGER)
	total_rx = Column(INTEGER)
	caps = Column(VARCHAR(11))
	timestamp = Column(DATETIME)

	def __init__(self,host_id,client_id,client_mac,vap_id,slNum,aid,chan,txRate,rxRate,rssi,idle,total_tx,total_rx,caps,timestamp):
		self.ap_client_ap_data_id = None
		self.host_id = host_id
		self.client_id = client_id
		self.client_mac = client_mac
		self.vap_id = vap_id
		self.slNum = slNum
		self.aid = aid
		self.chan = chan
		self.txRate = txRate
		self.rxRate = rxRate
		self.rssi = rssi
		self.idle = idle
		self.total_tx = total_tx
		self.total_rx = total_rx
		self.caps = caps
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<ApClient_ap_data('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ap_client_ap_data_id,self.host_id,self.client_id,self.client_mac,self.vap_id,self.slNum,self.aid,self.chan,self.txRate,self.rxRate,self.rssi,self.idle,self.total_tx,self.total_rx,self.caps,self.timestamp)

class ApClient_details(Base):
    __tablename__= "ap_client_details"
    client_id = Column(INTEGER,primary_key=True)
    client_name = Column(VARCHAR(32))
    mac = Column(VARCHAR(20))
    total_tx = Column(INTEGER)
    total_rx = Column(INTEGER)
    first_seen_time = Column(DATETIME)
    first_seen_ap_id = Column(INTEGER)
    last_seen_time = Column(DATETIME)
    last_seen_ap_id = Column(INTEGER)
    client_ip = Column(VARCHAR(20))

    def __init__(self,client_name,mac,total_tx,total_rx,first_seen_time,first_seen_ap_id,last_seen_time,last_seen_ap_id,client_ip):
        self.client_id = None
        self.client_name = client_name
        self.mac = mac
        self.total_tx = total_tx
        self.total_rx = total_rx
        self.first_seen_time = first_seen_time
        self.first_seen_ap_id = first_seen_ap_id
        self.last_seen_time = last_seen_time
        self.last_seen_ap_id = last_seen_ap_id
        self.client_ap = client_ap
        
    def __repr__(self):
        return "<ApClient_details('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" \
                %(self.client_id,self.client_name,self.mac,self.total_tx,self.total_rx,self.first_seen_time,self.first_seen_ap_id,self.last_seen_time,self.last_seen_ap_id,self.client_ip)

class ApConnected_client(Base):
	__tablename__= "ap_connected_client"
	ap_connected_client_id = Column(INTEGER,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	client_id = Column(INTEGER)
	client_mac = Column(VARCHAR(20))
	state = Column(ENUM('0','1'),name='enumclient')

	def __init__(self,host_id,client_id,client_mac,state):
		self.ap_connected_client_id = None
		self.host_id = host_id
		self.client_id = client_id
		self.client_mac = client_mac
		self.state = state
		
	def __repr__(self):
		return "<ApConnected_client('%s','%s','%s','%s','%s')>" %(self.ap_connected_client_id,self.host_id,self.client_id,self.client_mac,self.state)


###################################### AP MODEL ENDS HERE #######################################################################################

class FirmwareListTable(Base):
	__tablename__= "firmware_list_table"
	firmware_list_table_id = Column(INTEGER,primary_key=True)
	device_type = Column(VARCHAR(10))
	firmware_file_name = Column(VARCHAR(50))
	firmware_file_path = Column(VARCHAR(200))

	def __init__(self,device_type,firmware_file_name,firmware_file_path):
		self.firmware_list_table_id = None
		self.device_type = device_type
		self.firmware_file_name = firmware_file_name
		self.firmware_file_path = firmware_file_path
		
	def __repr__(self):
		return "<FirmwareList_table('%s','%s','%s','%s')>" %(self.firmware_list_table_id,self.device_type,self.firmware_file_name,self.firmware_file_path)


##################################################Rahul Tables For License #################################################################

class LicenseInfo(Base):
	__tablename__= "license_info"
	minutes = Column(INT,primary_key=True)
	last_check_date = Column(DATETIME)
	is_valid = Column(TINYINT)
	timestamp = Column(TIMESTAMP)

	def __init__(self,minutes,last_check_date,is_valid):
		self.minutes = minutes
		self.last_check_date = last_check_date
		self.is_valid = is_valid
		self.timestamp = None
		
	def __repr__(self):
		return "<LicenseInfo('%s','%s','%s','%s')>" %(self.minutes,self.last_check_date,self.is_valid,self.timestamp)


class LicenseDetails(Base):
	__tablename__= "license_details"
	license_id = Column(VARCHAR(32),primary_key=True)
	issued_client = Column(VARCHAR(32))
	issue_date = Column(DATETIME)
	expire_date = Column(DATETIME)
	timestamp = Column(TIMESTAMP)

	def __init__(self,license_id,issued_client,issue_date,expire_date):
		self.license_id = license_id
		self.issued_client = issued_client
		self.issue_date = issue_date
		self.expire_date = expire_date
		self.timestamp = None
		
	def __repr__(self):
		return "<LicenseDetails('%s','%s','%s','%s','%s')>" %(self.license_id,self.issued_client,self.issue_date,self.expire_date,self.timestamp)



class HostStatus(Base):
	__tablename__= "host_status"
	status_id = Column(INTEGER,primary_key=True)
	host_ip = Column(VARCHAR(32))
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	status = Column(Enum('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', name='enumstate'))
	plugin_status = Column(TINYINT)
	timestamp = Column(TIMESTAMP)

	def __init__(self,host_ip,host_id,status,plugin_status):
		self.status_id = None
		self.host_ip = host_ip
		self.host_id = host_id
		self.status = status
		self.plugin_status = plugin_status
		self.timestamp = None
		
	def __repr__(self):
		return "<HostStatus('%s','%s','%s','%s','%s')>" %(self.license_id, self.issued_client, self.issue_date, self.expire_date, self.plugin_status, self.timestamp)
    
    
class Odu1007_2_20_oid_table(Base):
	__tablename__= "odu100_7_2_20_oid_table"
	table_name = Column(VARCHAR(64),primary_key=True)
	table_oid = Column(VARCHAR(64))
	varbinds = Column(TINYINT)
	is_recon = Column(INTEGER)
	status = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,table_name,table_oid,varbinds,is_recon,status,timestamp):
		self.table_name = table_name
		self.table_oid = table_oid
		self.varbinds = varbinds
		self.is_recon = is_recon
		self.status = status
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<Odu1007_2_20_oid_table('%s','%s','%s','%s','%s','%s')>" %(self.table_name,self.table_oid,self.varbinds,self.is_recon,self.status,self.timestamp)


##############################################CCU##########################################################

class CcuInformationTable(Base):
	__tablename__= "ccu_ccuInformationTable"
	ccu_ccuInformationTable_id = Column(Integer,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	ccuITIndex = Column(Integer)
	ccuITSiteCCUType = Column(Integer)
	ccuITCCUId = Column(VARCHAR(20))
	ccuITSerialNumber = Column(VARCHAR(20))
	ccuITHardwareVersion = Column(VARCHAR(15))

	def __init__(self,host_id,ccuITIndex,ccuITSiteCCUType,ccuITCCUId,ccuITSerialNumber,ccuITHardwareVersion):
		self.ccu_ccuInformationTable_id = None
		self.host_id = host_id
		self.ccuITIndex = ccuITIndex
		self.ccuITSiteCCUType = ccuITSiteCCUType
		self.ccuITCCUId = ccuITCCUId
		self.ccuITSerialNumber = ccuITSerialNumber
		self.ccuITHardwareVersion = ccuITHardwareVersion
		
	def __repr__(self):
		return "<CcuInformationTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuInformationTable_id,self.host_id,self.ccuITIndex,self.ccuITSiteCCUType,self.ccuITCCUId,self.ccuITSerialNumber,self.ccuITHardwareVersion)

class CcuNetworkConfigurationTable(Base):
	__tablename__= "ccu_ccuNetworkConfigurationTable"
	ccu_ccuNetworkConfigurationTable_id = Column(Integer,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	ccuNCIndex = Column(Integer)
	ccuNCMACAddress = Column(VARCHAR(20))
	ccuNCCCUIP = Column(VARCHAR(18))
	ccuNCCCUNetMask = Column(VARCHAR(18))
	ccuNCOMCIP = Column(VARCHAR(18))
	ccuNCDHCPAssignedIP = Column(VARCHAR(18))
	ccuNCDHCPNetMask = Column(VARCHAR(18))
	ccuNCDefaultGateway = Column(VARCHAR(18))

	def __init__(self,host_id,ccuNCIndex,ccuNCMACAddress,ccuNCCCUIP,ccuNCCCUNetMask,ccuNCOMCIP,ccuNCDHCPAssignedIP,ccuNCDHCPNetMask,ccuNCDefaultGateway):
		self.ccu_ccuNetworkConfigurationTable_id = None
		self.host_id = host_id
		self.ccuNCIndex = ccuNCIndex
		self.ccuNCMACAddress = ccuNCMACAddress
		self.ccuNCCCUIP = ccuNCCCUIP
		self.ccuNCCCUNetMask = ccuNCCCUNetMask
		self.ccuNCOMCIP = ccuNCOMCIP
		self.ccuNCDHCPAssignedIP = ccuNCDHCPAssignedIP
		self.ccuNCDHCPNetMask = ccuNCDHCPNetMask
		self.ccuNCDefaultGateway = ccuNCDefaultGateway
		
	def __repr__(self):
		return "<CcuNetworkConfigurationTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuNetworkConfigurationTable_id,self.host_id,self.ccuNCIndex,self.ccuNCMACAddress,self.ccuNCCCUIP,self.ccuNCCCUNetMask,self.ccuNCOMCIP,self.ccuNCDHCPAssignedIP,self.ccuNCDHCPNetMask,self.ccuNCDefaultGateway)

class CcuRealTimeStatusTable(Base):
	__tablename__= "ccu_ccuRealTimeStatusTable"
	ccu_ccuRealTimeStatusTable_id = Column(Integer,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	ccuRTSIndex = Column(Integer)
	ccuRTSSystemVoltage = Column(Integer)
	ccuRTSSolarCurrent = Column(Integer)
	ccuRTSSMPSCurrent = Column(VARCHAR(32))
	ccuRTSBatteryCurrent = Column(Integer)
	ccuRTSLoadCurrent = Column(Integer)
	ccuRTSBatterySOC = Column(Integer)
	ccuRTSInternalTemperature = Column(Integer)
	ccuRTSBatteryAmbientTemperature = Column(Integer)
	ccuRTSSMPSTemperature = Column(Integer)
	ccuRTSACVoltageReading = Column(Integer)
	ccuRTSAlarmStatusByte = Column(Integer)

	def __init__(self,host_id,ccuRTSIndex,ccuRTSSystemVoltage,ccuRTSSolarCurrent,ccuRTSSMPSCurrent,ccuRTSBatteryCurrent,ccuRTSLoadCurrent,ccuRTSBatterySOC,ccuRTSInternalTemperature,ccuRTSBatteryAmbientTemperature,ccuRTSSMPSTemperature,ccuRTSACVoltageReading,ccuRTSAlarmStatusByte):
		self.ccu_ccuRealTimeStatusTable_id = None
		self.host_id = host_id
		self.ccuRTSIndex = ccuRTSIndex
		self.ccuRTSSystemVoltage = ccuRTSSystemVoltage
		self.ccuRTSSolarCurrent = ccuRTSSolarCurrent
		self.ccuRTSSMPSCurrent = ccuRTSSMPSCurrent
		self.ccuRTSBatteryCurrent = ccuRTSBatteryCurrent
		self.ccuRTSLoadCurrent = ccuRTSLoadCurrent
		self.ccuRTSBatterySOC = ccuRTSBatterySOC
		self.ccuRTSInternalTemperature = ccuRTSInternalTemperature
		self.ccuRTSBatteryAmbientTemperature = ccuRTSBatteryAmbientTemperature
		self.ccuRTSSMPSTemperature = ccuRTSSMPSTemperature
		self.ccuRTSACVoltageReading = ccuRTSACVoltageReading
		self.ccuRTSAlarmStatusByte = ccuRTSAlarmStatusByte
		
	def __repr__(self):
		return "<CcuRealTimeStatusTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuRealTimeStatusTable_id,self.host_id,self.ccuRTSIndex,self.ccuRTSSystemVoltage,self.ccuRTSSolarCurrent,self.ccuRTSSMPSCurrent,self.ccuRTSBatteryCurrent,self.ccuRTSLoadCurrent,self.ccuRTSBatterySOC,self.ccuRTSInternalTemperature,self.ccuRTSBatteryAmbientTemperature,self.ccuRTSSMPSTemperature,self.ccuRTSACVoltageReading,self.ccuRTSAlarmStatusByte)

class CcuStatusDataTable(Base):
	__tablename__= "ccu_ccuStatusDataTable"
	ccu_ccuStatusDataTable_id = Column(Integer,primary_key=True)
	host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
	ccuSDIndex = Column(Integer)
	ccuSDLastRebootReason = Column(Integer)
	ccuSDUpTimeSecs = Column(VARCHAR(32))
	ccuSDKwHReading = Column(INTEGER)
	ccuSDBatteryHealth = Column(Integer)
	ccuSDBatteryState = Column(Integer)
	ccuSDLoadConnectedStatus = Column(Integer)
	ccuSDACAvailability = Column(Integer)
	ccuSDExternalChargingStatus = Column(Integer)
	ccuSDChargeDischargeCycle = Column(Integer)

	def __init__(self,host_id,ccuSDIndex,ccuSDLastRebootReason,ccuSDUpTimeSecs,ccuSDKwHReading,ccuSDBatteryHealth,ccuSDBatteryState,ccuSDLoadConnectedStatus,ccuSDACAvailability,ccuSDExternalChargingStatus,ccuSDChargeDischargeCycle):
		self.ccu_ccuStatusDataTable_id = None
		self.host_id = host_id
		self.ccuSDIndex = ccuSDIndex
		self.ccuSDLastRebootReason = ccuSDLastRebootReason
		self.ccuSDUpTimeSecs = ccuSDUpTimeSecs
		self.ccuSDKwHReading = ccuSDKwHReading
		self.ccuSDBatteryHealth = ccuSDBatteryHealth
		self.ccuSDBatteryState = ccuSDBatteryState
		self.ccuSDLoadConnectedStatus = ccuSDLoadConnectedStatus
		self.ccuSDACAvailability = ccuSDACAvailability
		self.ccuSDExternalChargingStatus = ccuSDExternalChargingStatus
		self.ccuSDChargeDischargeCycle = ccuSDChargeDischargeCycle
		
	def __repr__(self):
		return "<CcuStatusDataTable('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuStatusDataTable_id,self.host_id,self.ccuSDIndex,self.ccuSDLastRebootReason,self.ccuSDUpTimeSecs,self.ccuSDKwHReading,self.ccuSDBatteryHealth,self.ccuSDBatteryState,self.ccuSDLoadConnectedStatus,self.ccuSDACAvailability,self.ccuSDExternalChargingStatus,self.ccuSDChargeDischargeCycle)

class CcuSoftwareInformationTable(Base):
    __tablename__= "ccu_ccuSoftwareInformationTable"
    ccu_ccuSoftwareInformationTable_id = Column(Integer,primary_key=True)
    host_id = Column(INTEGER,ForeignKey('hosts.host_id'))
    ccuSIIndex = Column(Integer)
    ccuSIActiveSoftwareVersion = Column(VARCHAR(20))
    ccuSIBackupSoftwareVersion = Column(VARCHAR(20))
    ccuSICommunicationProtocolVersion = Column(VARCHAR(20))
    ccuSIBootLoaderVersion = Column(VARCHAR(13))

    def __init__(self,host_id,ccuSIIndex,ccuSIActiveSoftwareVersion,ccuSIBackupSoftwareVersion,ccuSICommunicationProtocolVersion,ccuSIBootLoaderVersion):
        self.ccu_ccuSoftwareInformationTable_id = None
        self.host_id = host_id
        self.ccuSIIndex = ccuSIIndex
        self.ccuSIActiveSoftwareVersion = ccuSIActiveSoftwareVersion
        self.ccuSIBackupSoftwareVersion = ccuSIBackupSoftwareVersion
        self.ccuSICommunicationProtocolVersion = ccuSICommunicationProtocolVersion
        self.ccuSIBootLoaderVersion = ccuSIBootLoaderVersion
        
    def __repr__(self):
        return "<CcuSoftwareInformationTable('%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuSoftwareInformationTable_id,self.host_id,self.ccuSIIndex,self.ccuSIActiveSoftwareVersion,self.ccuSIBackupSoftwareVersion,self.ccuSICommunicationProtocolVersion,self.ccuSIBootLoaderVersion)


class CcuAlarmAndThresholdTable(Base):
	__tablename__= "ccu_ccuAlarmAndThresholdTable"
	ccu_ccuAlarmAndThresholdTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	ccuATIndex = Column(INTEGER)
	ccuATHighTemperatureAlarm = Column(TINYINT)
	ccuATPSMRequest = Column(TINYINT)
	ccuATSMPSMaxCurrentLimit = Column(SMALLINT)
	ccuATPeakLoadCurrent = Column(SMALLINT)
	ccuATLowVoltageDisconnectLevel = Column(SMALLINT)

	def __init__(self,config_profile_id,ccuATIndex,ccuATHighTemperatureAlarm,ccuATPSMRequest,ccuATSMPSMaxCurrentLimit,ccuATPeakLoadCurrent,ccuATLowVoltageDisconnectLevel):
		self.ccu_ccuAlarmAndThresholdTable_id = None
		self.config_profile_id = config_profile_id
		self.ccuATIndex = ccuATIndex
		self.ccuATHighTemperatureAlarm = ccuATHighTemperatureAlarm
		self.ccuATPSMRequest = ccuATPSMRequest
		self.ccuATSMPSMaxCurrentLimit = ccuATSMPSMaxCurrentLimit
		self.ccuATPeakLoadCurrent = ccuATPeakLoadCurrent
		self.ccuATLowVoltageDisconnectLevel = ccuATLowVoltageDisconnectLevel
		
	def __repr__(self):
		return "<CcuAlarm_threshold_table('%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuAlarmAndThresholdTable_id,self.config_profile_id,self.ccuATIndex,self.ccuATHighTemperatureAlarm,self.ccuATPSMRequest,self.ccuATSMPSMaxCurrentLimit,self.ccuATPeakLoadCurrent,self.ccuATLowVoltageDisconnectLevel)

class CcuAuxIOTable(Base):
    __tablename__= "ccu_ccuAuxIOTable"
    ccu_ccuAuxIOTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    ccuAIIndex = Column(INTEGER)
    ccuAIExternalOutput1 = Column(TINYINT)
    ccuAIExternalOutput2 = Column(TINYINT)
    ccuAIExternalOutput3 = Column(TINYINT)
    ccuAIExternalInput1 = Column(TINYINT)
    ccuAIExternalInput2 = Column(TINYINT)
    ccuAIExternalInput3 = Column(TINYINT)
    ccuAIExternalInput1AlarmType = Column(TINYINT)
    ccuAIExternalInput2AlarmType = Column(TINYINT)
    ccuAIExternalInput3AlarmType = Column(TINYINT)

    def __init__(self,config_profile_id,ccuAIIndex,ccuAIExternalOutput1,ccuAIExternalOutput2,ccuAIExternalOutput3,ccuAIExternalInput1,ccuAIExternalInput2,ccuAIExternalInput3,ccuAIExternalInput1AlarmType,ccuAIExternalInput2AlarmType,ccuAIExternalInput3AlarmType):
        self.ccu_ccuAuxIOTable_id = None
        self.config_profile_id = config_profile_id
        self.ccuAIIndex = ccuAIIndex
        self.ccuAIExternalOutput1 = ccuAIExternalOutput1
        self.ccuAIExternalOutput2 = ccuAIExternalOutput2
        self.ccuAIExternalOutput3 = ccuAIExternalOutput3
        self.ccuAIExternalInput1 = ccuAIExternalInput1
        self.ccuAIExternalInput2 = ccuAIExternalInput2
        self.ccuAIExternalInput3 = ccuAIExternalInput3
        self.ccuAIExternalInput1AlarmType = ccuAIExternalInput1AlarmType
        self.ccuAIExternalInput2AlarmType = ccuAIExternalInput2AlarmType
        self.ccuAIExternalInput3AlarmType = ccuAIExternalInput3AlarmType
        
    def __repr__(self):
        return "<CcuAux_io_table('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" \
        %(self.ccu_ccuAuxIOTable_id,self.config_profile_id,self.ccuAIIndex,self.ccuAIExternalOutput1,self.ccuAIExternalOutput2,self.ccuAIExternalOutput3,\
        self.ccuAIExternalInput1,self.ccuAIExternalInput2,self.ccuAIExternalInput3,self.ccuAIExternalInput1AlarmType,self.ccuAIExternalInput2AlarmType,self.ccuAIExternalInput3AlarmType)


class CcuBatteryPanelConfigTable(Base):
	__tablename__= "ccu_ccuBatteryPanelConfigTable"
	ccu_ccuBatteryPanelConfigTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	ccuBPCIndex = Column(INTEGER)
	ccuBPCSiteBatteryCapacity = Column(SMALLINT)
	ccuBPCSiteSolarPanelwP = Column(SMALLINT)
	ccuBPCSiteSolarPanelCount = Column(SMALLINT)
	ccuBPCNewBatteryInstallationDate = Column(VARCHAR(13))

	def __init__(self,config_profile_id,ccuBPCIndex,ccuBPCSiteBatteryCapacity,ccuBPCSiteSolarPanelwP,ccuBPCSiteSolarPanelCount,ccuBPCNewBatteryInstallationDate):
		self.ccu_ccuBatteryPanelConfigTable_id = None
		self.config_profile_id = config_profile_id
		self.ccuBPCIndex = ccuBPCIndex
		self.ccuBPCSiteBatteryCapacity = ccuBPCSiteBatteryCapacity
		self.ccuBPCSiteSolarPanelwP = ccuBPCSiteSolarPanelwP
		self.ccuBPCSiteSolarPanelCount = ccuBPCSiteSolarPanelCount
		self.ccuBPCNewBatteryInstallationDate = ccuBPCNewBatteryInstallationDate
		
	def __repr__(self):
		return "<CcuBattery_panel_config_table('%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuBatteryPanelConfigTable_id,self.config_profile_id,self.ccuBPCIndex,self.ccuBPCSiteBatteryCapacity,self.ccuBPCSiteSolarPanelwP,self.ccuBPCSiteSolarPanelCount,self.ccuBPCNewBatteryInstallationDate)



class CcuControlTable(Base):
	__tablename__= "ccu_ccuControlTable"
	ccu_ccuControlTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	ccuCTIndex = Column(INTEGER)
	ccuCTLoadTurnOff = Column(SMALLINT)
	ccuCTSMPSCharging = Column(TINYINT)
	ccuCTRestoreDefault = Column(TINYINT)
	ccuCTCCUReset = Column(TINYINT)

	def __init__(self,config_profile_id,ccuCTIndex,ccuCTLoadTurnOff,ccuCTSMPSCharging,ccuCTRestoreDefault,ccuCTCCUReset):
		self.ccu_ccuControlTable_id = None
		self.config_profile_id = config_profile_id
		self.ccuCTIndex = ccuCTIndex
		self.ccuCTLoadTurnOff = ccuCTLoadTurnOff
		self.ccuCTSMPSCharging = ccuCTSMPSCharging
		self.ccuCTRestoreDefault = ccuCTRestoreDefault
		self.ccuCTCCUReset = ccuCTCCUReset
		
	def __repr__(self):
		return "<CcuControl_table('%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuControlTable_id,self.config_profile_id,self.ccuCTIndex,self.ccuCTLoadTurnOff,self.ccuCTSMPSCharging,self.ccuCTRestoreDefault,self.ccuCTCCUReset)


class CcuOidTable(Base):
	__tablename__= "ccu_oid_table"
	table_name = Column(VARCHAR(64),primary_key=True)
	table_oid = Column(VARCHAR(64))
	varbinds = Column(TINYINT)
	is_recon = Column(INTEGER)
	status = Column(INTEGER)
	timestamp = Column(TIMESTAMP)

	def __init__(self,table_name,table_oid,varbinds,is_recon,status,timestamp):
		self.table_name = table_name
		self.table_oid = table_oid
		self.varbinds = varbinds
		self.is_recon = is_recon
		self.status = status
		self.timestamp = timestamp
		
	def __repr__(self):
		return "<CCUOIDTable('%s','%s','%s','%s','%s','%s')>" %(self.table_name,self.table_oid,self.varbinds,self.is_recon,self.status,self.timestamp)


class CcuOids(Base):
	__tablename__= "ccu_oids"
	oid_id = Column(INTEGER,primary_key=True)
	device_type_id = Column(VARCHAR(16))
	oid = Column(VARCHAR(256))
	oid_name = Column(VARCHAR(256))
	oid_type = Column(VARCHAR(16))
	access = Column(SMALLINT)
	default_value = Column(VARCHAR(256))
	min_value = Column(VARCHAR(128))
	max_value = Column(VARCHAR(256))
	indexes = Column(VARCHAR(256))
	dependent_id = Column(INTEGER)
	multivalue = Column(SMALLINT)
	table_name = Column(VARCHAR(128))
	coloumn_name = Column(VARCHAR(128))
	indexes_name = Column(VARCHAR(64))

	def __init__(self,oid_id,device_type_id,oid,oid_name,oid_type,access,default_value,min_value,max_value,indexes,dependent_id,multivalue,table_name,coloumn_name,indexes_name):
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
		self.indexes_name = indexes_name
		
	def __repr__(self):
		return "<CcuOids('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %(self.oid_id,self.device_type_id,self.oid,self.oid_name,self.oid_type,self.access,self.default_value,self.min_value,self.max_value,self.indexes,self.dependent_id,self.multivalue,self.table_name,self.coloumn_name,self.indexes_name)





class CcuPeerInformationTable(Base):
    __tablename__= "ccu_ccuPeerInformationTable"
    ccu_ccuPeerInformationTable_id = Column(INTEGER,primary_key=True)
    config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
    ccuPIIndex = Column(INTEGER)
    ccuPIPeer1MACID = Column(VARCHAR(20))
    ccuPIPeer2MACID = Column(VARCHAR(20))
    ccuPIPeer3MACID = Column(VARCHAR(20))
    ccuPIPeer4MACID = Column(VARCHAR(20))

    def __init__(self,config_profile_id,ccuPIIndex,ccuPIPeer1MACID,ccuPIPeer2MACID,ccuPIPeer3MACID,ccuPIPeer4MACID):
        self.ccu_ccuPeerInformationTable_id = None
        self.config_profile_id = config_profile_id
        self.ccuPIIndex = ccuPIIndex
        self.ccuPIPeer1MACID = ccuPIPeer1MACID
        self.ccuPIPeer2MACID = ccuPIPeer2MACID
        self.ccuPIPeer3MACID = ccuPIPeer3MACID
        self.ccuPIPeer4MACID = ccuPIPeer4MACID
        
    def __repr__(self):
        return "<CcuPeer_info_table('%s','%s','%s','%s','%s','%s','%s')>" %(self.ccu_ccuPeerInformationTable_id,self.config_profile_id,self.ccuPIIndex,self.ccuPIPeer1MACID,self.ccuPIPeer2MACID,self.ccuPIPeer3MACID,self.ccuPIPeer4MACID)



class CcuSiteInformationTable(Base):
	__tablename__= "ccu_ccuSiteInformationTable"
	ccu_ccuSiteInformationTable_id = Column(INTEGER,primary_key=True)
	config_profile_id = Column(INTEGER,ForeignKey('config_profiles.config_profile_id'))
	ccuSITIndex = Column(INTEGER)
	ccuSITSiteName = Column(VARCHAR(65))

	def __init__(self,config_profile_id,ccuSITIndex,ccuSITSiteName):
		self.ccu_ccuSiteInformationTable_id = None
		self.config_profile_id = config_profile_id
		self.ccuSITIndex = ccuSITIndex
		self.ccuSITSiteName = ccuSITSiteName
		
	def __repr__(self):
		return "<CcuSite_info_table('%s','%s','%s','%s')>" %(self.ccu_ccuSiteInformationTable_id,self.config_profile_id,self.ccuSITIndex,self.ccuSITSiteName)



###########################################################################################################

############################################################################################################################################



# define mappers
clear_mappers()

mapper(CcuInformationTable,CcuInformationTable.__table__)
mapper(CcuNetworkConfigurationTable,CcuNetworkConfigurationTable.__table__)
mapper(CcuRealTimeStatusTable,CcuRealTimeStatusTable.__table__)
mapper(CcuStatusDataTable,CcuStatusDataTable.__table__)
mapper(CcuSoftwareInformationTable,CcuSoftwareInformationTable.__table__)
mapper(CcuAlarmAndThresholdTable,CcuAlarmAndThresholdTable.__table__)
mapper(CcuAuxIOTable,CcuAuxIOTable.__table__)
mapper(CcuBatteryPanelConfigTable,CcuBatteryPanelConfigTable.__table__)
mapper(CcuControlTable,CcuControlTable.__table__)
mapper(CcuOidTable,CcuOidTable.__table__)
mapper(CcuOids,CcuOids.__table__)
mapper(CcuPeerInformationTable,CcuPeerInformationTable.__table__)
mapper(CcuSiteInformationTable,CcuSiteInformationTable.__table__)

mapper(HostStatus,HostStatus.__table__)
mapper(Odu1007_2_20_oid_table,Odu1007_2_20_oid_table.__table__)

##################################AP MAPPING STARTS HERE ##############################################################

mapper(Ap25AccesspointIPsettings,Ap25AccesspointIPsettings.__table__)
mapper(Ap25AclMacTable,Ap25AclMacTable.__table__)
mapper(Ap25AclStatisticsTable,Ap25AclStatisticsTable.__table__)
mapper(Ap25BasicACLconfigTable,Ap25BasicACLconfigTable.__table__)
mapper(Ap25BasicConfiguration,Ap25BasicConfiguration.__table__)
mapper(Ap25BasicVAPsecurity,Ap25BasicVAPsecurity.__table__)
mapper(Ap25BasicVAPconfigTable,Ap25BasicVAPconfigTable.__table__)
mapper(Ap25DhcpServer,Ap25DhcpServer.__table__)
mapper(Ap25DhcpClientsTable,Ap25DhcpClientsTable.__table__)
mapper(Ap25ApScanDataTable,Ap25ApScanDataTable.__table__)
mapper(Ap25RadioSelection,Ap25RadioSelection.__table__)
mapper(Ap25RadioSetup,Ap25RadioSetup.__table__)
mapper(Ap25Services,Ap25Services.__table__)
mapper(Ap25StatisticsTable,Ap25StatisticsTable.__table__)
mapper(Ap25VapClientStatisticsTable,Ap25VapClientStatisticsTable.__table__)
mapper(Ap25VapWEPsecurityConfigTable,Ap25VapWEPsecurityConfigTable.__table__)
mapper(Ap25VapWPAsecurityConfigTable,Ap25VapWPAsecurityConfigTable.__table__)
mapper(Ap25Versions,Ap25Versions.__table__)
mapper(Ap25Oid_table,Ap25Oid_table.__table__)
mapper(Ap25Oids,Ap25Oids.__table__)
mapper(Ap25OidsMultivalues,Ap25OidsMultivalues.__table__)
mapper(ApClient_ap_data,ApClient_ap_data.__table__)
mapper(ApClient_details,ApClient_details.__table__)
mapper(ApConnected_client,ApConnected_client.__table__)

mapper(Ap25VapSelection,Ap25VapSelection.__table__,properties={'ap25_aclMacTable':relationship(Ap25AclMacTable,backref="ap25_vapSelection",cascade="all,delete,delete-orphan"),\
'ap25_basicVAPsecurity':relationship(Ap25BasicVAPsecurity,backref="ap25_vapSelection",cascade="all,delete,delete-orphan"),\
'ap25_basicVAPconfigTable':relationship(Ap25BasicVAPconfigTable,backref="ap25_vapSelection",cascade="all,delete,delete-orphan"),\
'ap25_vapWPAsecurityConfigTable':relationship(Ap25VapWPAsecurityConfigTable,backref="ap25_vapSelection",cascade="all,delete,delete-orphan")})

##################################AP MAPPING ENDS HERE ##############################################################
mapper(FirmwareListTable,FirmwareListTable.__table__)

################################################## Anuj Mapper Model Defined #########################################################################

##################################LICESNE MAPPING##################################
mapper(LicenseDetails,LicenseDetails.__table__)
mapper(LicenseInfo,LicenseInfo.__table__)
############################################################################################


#---------------Mapping for GetOdu16RaStatusTable 
mapper(GetOdu16RaStatusTable,GetOdu16RaStatusTable.__table__)

#-----------------Mapping For ODU16IPConfig------------------------------------
odu_ip_config_table=SetOdu16IPConfigTable.__table__
mapper(SetOdu16IPConfigTable,odu_ip_config_table)

#-----------------Mapping For ODU16NetworkInterface------------------------------------
odu_ip_config_table=SetOdu16NetworkInterfaceConfig.__table__
mapper(SetOdu16NetworkInterfaceConfig,odu_ip_config_table)

#-----------------Mapping For ODU16OmcConfTable------------------------------------
odu_omc_conf_table=SetOdu16OmcConfTable.__table__
mapper(SetOdu16OmcConfTable,odu_omc_conf_table)

#-----------------Mapping For ODU16PeerConfigTable------------------------------------
odu_peer_config_table=SetOdu16PeerConfigTable.__table__
mapper(SetOdu16PeerConfigTable,odu_peer_config_table)

#-----------------Mapping For ODU16RAAclConfigTable------------------------------------
odu_ra_acl_config_table=SetOdu16RAAclConfigTable.__table__
mapper(SetOdu16RAAclConfigTable,odu_ra_acl_config_table)

#-----------------Mapping For ODU16OmOperationsTable------------------------------------
odu_om_operations__table=SetOdu16OmOperationsTable.__table__
mapper(SetOdu16OmOperationsTable,odu_om_operations__table) 

#-----------------Mapping For ODU16RAConfTable------------------------------------
odu_ra_conf__table=SetOdu16RAConfTable.__table__
mapper(SetOdu16RAConfTable,odu_ra_conf__table) 

#-----------------Mapping For ODU16RALlcConfTable------------------------------------
odu_ra_llc_conf_table=SetOdu16RALlcConfTable.__table__
mapper(SetOdu16RALlcConfTable,odu_ra_llc_conf_table)

#-----------------Mapping For ODU16RATddMacConfig------------------------------------
odu_ra_tdd_mac_config_table=SetOdu16RATddMacConfig.__table__
mapper(SetOdu16RATddMacConfig,odu_ra_tdd_mac_config_table)


#-----------------Mapping For ODU16RUConfTable------------------------------------
odu_ru_conf_table=SetOdu16RUConfTable.__table__
mapper(SetOdu16RUConfTable,odu_ru_conf_table)

#-----------------Mapping For ODU16RUDateTimeTable------------------------------------
odu_ru_date_time_table=SetOdu16RUDateTimeTable.__table__
mapper(SetOdu16RUDateTimeTable,odu_ru_date_time_table) 

#-----------------Mapping For ODU16SyncConfigTable------------------------------------
odu_sync_config_table=SetOdu16SyncConfigTable.__table__
mapper(SetOdu16SyncConfigTable,odu_sync_config_table)


#-----------------Mapping For ODU16Misc------------------------------------
odu_misc_table=SetOdu16Misc.__table__
mapper(SetOdu16Misc,odu_misc_table)

#-----------------Mapping For Odu16SysOmcReguistrationTable--------------------
odu_sys_registration_table=SetOdu16SysOmcRegistrationTable.__table__

#---------------Mapping for GetOdu16_ru_conf_tables 
mapper(GetOdu16_ru_conf_table,GetOdu16_ru_conf_table.__table__)

mapper(GetOdu16SWStatusTable,GetOdu16SWStatusTable.__table__)

mapper(GetOdu16HWDescTable,GetOdu16HWDescTable.__table__)

mapper(GetOdu16RAScanListTable,GetOdu16RAScanListTable.__table__)

#-----------------Mapping for odu100--------------------
mapper(SetOdu16SysOmcRegistrationTable,odu_sys_registration_table)

mapper(Odu100EswATUConfigTable,Odu100EswATUConfigTable.__table__)

mapper(Odu100EswBadFramesTable,Odu100EswBadFramesTable.__table__)

mapper(Odu100EswGoodFramesTable,Odu100EswGoodFramesTable.__table__)


#mapper(Odu1007_2_25_oids,Odu1007_2_25_oids.__table__)

mapper(Odu1007_2_25_oids_multivalues,Odu1007_2_25_oids_multivalues.__table__)

mapper(Odu1007_2_25_oid_table,Odu1007_2_25_oid_table.__table__)

mapper(Odu100EswMirroringPortTable,Odu100EswMirroringPortTable.__table__)

mapper(Odu100EswPortAccessListTable,Odu100EswPortAccessListTable.__table__)

mapper(Odu100EswPortBwTable,Odu100EswPortBwTable.__table__)

mapper(Odu100EswPortConfigTable,Odu100EswPortConfigTable.__table__)

mapper(Odu100EswPortQinQTable,Odu100EswPortQinQTable.__table__)

mapper(Odu100EswPortStatisticsTable,Odu100EswPortStatisticsTable.__table__)

mapper(Odu100EswPortStatusTable,Odu100EswPortStatusTable.__table__)

mapper(Odu100EswVlanConfigTable,Odu100EswVlanConfigTable.__table__)

mapper(Odu100HwDescTable,Odu100HwDescTable.__table__)

mapper(Odu100IpConfigTable,Odu100IpConfigTable.__table__)

mapper(Odu100NwInterfaceStatisticsTable,Odu100NwInterfaceStatisticsTable.__table__)

mapper(Odu100NwInterfaceStatusTable,Odu100NwInterfaceStatusTable.__table__)

mapper(Odu100OmcConfTable,Odu100OmcConfTable.__table__)

mapper(Odu100PeerConfigTable,Odu100PeerConfigTable.__table__)

mapper(Odu100PeerLinkStatisticsTable,Odu100PeerLinkStatisticsTable.__table__)

mapper(Odu100PeerNodeStatusTable,Odu100PeerNodeStatusTable.__table__)

mapper(Odu100PeerRateStatisticsTable,Odu100PeerRateStatisticsTable.__table__)

mapper(Odu100PeerTunnelStatisticsTable,Odu100PeerTunnelStatisticsTable.__table__)

mapper(Odu100RaAclConfigTable,Odu100RaAclConfigTable.__table__)

mapper(Odu100RaChannelListTable,Odu100RaChannelListTable.__table__)

mapper(Odu100RaConfTable,Odu100RaConfTable.__table__)

mapper(Odu100RaLlcConfTable,Odu100RaLlcConfTable.__table__)

mapper(Odu100RaPreferredRFChannelTable,Odu100RaPreferredRFChannelTable.__table__)

mapper(Odu100RaScanListTable,Odu100RaScanListTable.__table__)

mapper(Odu100RaSiteSurveyResultTable,Odu100RaSiteSurveyResultTable.__table__)

mapper(Odu100RaStatusTable,Odu100RaStatusTable.__table__)

mapper(Odu100RaTddMacConfigTable,Odu100RaTddMacConfigTable.__table__)

mapper(Odu100RaTddMacStatisticsTable,Odu100RaTddMacStatisticsTable.__table__)

mapper(Odu100RaTddMacStatusTable,Odu100RaTddMacStatusTable.__table__)

mapper(Odu100RaValidPhyRatesTable,Odu100RaValidPhyRatesTable.__table__)

mapper(Odu100RuConfTable,Odu100RuConfTable.__table__)

mapper(Odu100RuDateTimeTable,Odu100RuDateTimeTable.__table__)

mapper(Odu100RuOmOperationsTable,Odu100RuOmOperationsTable.__table__)

mapper(Odu100RuStatusTable,Odu100RuStatusTable.__table__)

mapper(Odu100MacFilterTable,Odu100MacFilterTable.__table__)

mapper(Odu100IpFilterTable,Odu100IpFilterTable.__table__)

mapper(Odu100SwStatusTable,Odu100SwStatusTable.__table__)

mapper(Odu100SyncConfigTable,Odu100SyncConfigTable.__table__)

mapper(Odu100SynchStatisticsTable,Odu100SynchStatisticsTable.__table__)

mapper(FirmwareMapping,FirmwareMapping.__table__)

mapper(Odu100SynchStatusTable,Odu100SynchStatusTable.__table__)

mapper(Odu100SysOmcRegistrationTable,Odu100SysOmcRegistrationTable.__table__)


mapper(GetOdu16PeerNodeStatusTable,GetOdu16PeerNodeStatusTable.__table__)


##################################IDU MAPPING START HERE ##############################################################


mapper(IduAclportTable,IduAclportTable.__table__)
mapper(IduAlarmOutConfigTable,IduAlarmOutConfigTable.__table__)
mapper(IduAlarmPortConfigurationTable,IduAlarmPortConfigurationTable.__table__)
mapper(IduAtuconfigTable,IduAtuconfigTable.__table__)
mapper(IduE1PortConfigurationTable,IduE1PortConfigurationTable.__table__)
mapper(IduE1PortStatusTable,IduE1PortStatusTable.__table__)
mapper(IduIduAdminStateTable,IduIduAdminStateTable.__table__)
mapper(IduIduInfoTable,IduIduInfoTable.__table__)
mapper(IduIduNetworkStatisticsTable,IduIduNetworkStatisticsTable.__table__)
mapper(IduIduOmOperationsTable,IduIduOmOperationsTable.__table__)
mapper(IduLinkConfigurationTable,IduLinkConfigurationTable.__table__)
mapper(IduLinkStatisticsTable,IduLinkStatisticsTable.__table__)
mapper(IduLinkStatusTable,IduLinkStatusTable.__table__)
mapper(IduMirroringportTable,IduMirroringportTable.__table__)
mapper(IduNetworkConfigurationsTable,IduNetworkConfigurationsTable.__table__)
mapper(IduOids,IduOids.__table__)
mapper(IduOids_multivalues,IduOids_multivalues.__table__)
mapper(IduOmcConfigurationTable,IduOmcConfigurationTable.__table__)
mapper(IduPoeConfigurationTable,IduPoeConfigurationTable.__table__)
mapper(IduPortBwTable,IduPortBwTable.__table__)
mapper(IduPortSecondaryStatisticsTable,IduPortSecondaryStatisticsTable.__table__)
mapper(IduPortqinqTable,IduPortqinqTable.__table__)
mapper(IduPortstatbadframeTable,IduPortstatbadframeTable.__table__)
mapper(IduPortstatgoodframeTable,IduPortstatgoodframeTable.__table__)
mapper(IduPortstatisticsTable,IduPortstatisticsTable.__table__)
mapper(IduRtcConfigurationTable,IduRtcConfigurationTable.__table__)
mapper(IduSectorIdentificationTable,IduSectorIdentificationTable.__table__)
mapper(IduSwPrimaryPortStatisticsTable,IduSwPrimaryPortStatisticsTable.__table__)
mapper(IduSwStatusTable,IduSwStatusTable.__table__)
mapper(IduSwitchPortconfigTable,IduSwitchPortconfigTable.__table__)
mapper(IduSwitchportstatusTable,IduSwitchportstatusTable.__table__)
mapper(IduSysOmcRegistrationTable,IduSysOmcRegistrationTable.__table__)
mapper(IduTdmoipNetworkInterfaceConfigurationTable,IduTdmoipNetworkInterfaceConfigurationTable.__table__)
mapper(IduTdmoipNetworkInterfaceStatisticsTable,IduTdmoipNetworkInterfaceStatisticsTable.__table__)
mapper(IduTemperatureSensorConfigurationTable,IduTemperatureSensorConfigurationTable.__table__)
mapper(IduVlanconfigTable,IduVlanconfigTable.__table__)
mapper(IduOidTable,IduOidTable.__table__)

##################################IDU MAPPING END HERE ##############################################################


##################################SWITCH MAPPING START HERE ##############################################################

##mapper(Swt4BandwidthControl,Swt4BandwidthControl.__table__)
##mapper(Swt4StormControl,Swt4StormControl.__table__)
##mapper(Swt4PortStatistics,Swt4PortStatistics.__table__)
##mapper(Swt4PortSettings,Swt4PortSettings.__table__)
##mapper(Swt4IpSettings,Swt4IpSettings.__table__)
##mapper(Swt4VlanSettings,Swt4VlanSettings.__table__)
##mapper(Swt4PortBasedPriority,Swt4PortBasedPriority.__table__)
##mapper(Swt4DscpBasedPriority,Swt4DscpBasedPriority.__table__)
##mapper(Swt48021pBasedPriority,Swt48021pBasedPriority.__table__)
##mapper(Swt4IpBasePriority,Swt4IpBasePriority.__table__)
##mapper(Swt4QueueBasedPriority,Swt4QueueBasedPriority.__table__)
##mapper(Swt4QueueWeightBased,Swt4QueueWeightBased.__table__)
##mapper(Swt4QosArbitration,Swt4QosArbitration.__table__)
##mapper(Swt41pRemarking,Swt41pRemarking.__

##################################SWITCH MAPPING ENDS HERE ##############################################################
##################################Master Slave mapping ##################################################################################################

#-----------------Mapping For MasterSlaveLinking------------------------------------
master_slave_linking=MasterSlaveLinking.__table__
mapper(MasterSlaveLinking,master_slave_linking)

###########################################################################################################################################################

#--------------------Mapping For Host------------------------------------------
host_table=Hosts.__table__
mapper(Hosts,host_table,properties={'odu100_eswBadFramesTable':relationship(Odu100EswBadFramesTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_eswGoodFramesTable':relationship(Odu100EswGoodFramesTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_eswPortStatisticsTable':relationship(Odu100EswPortStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_eswPortStatusTable':relationship(Odu100EswPortStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_hwDescTable':relationship(Odu100HwDescTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_nwInterfaceStatisticsTable':relationship(Odu100NwInterfaceStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_nwInterfaceStatusTable':relationship(Odu100NwInterfaceStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_macFilterTable':relationship(Odu100MacFilterTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_ipFilterTable':relationship(Odu100IpFilterTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_peerLinkStatisticsTable':relationship(Odu100PeerLinkStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_peerNodeStatusTable':relationship(Odu100PeerNodeStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_peerRateStatisticsTable':relationship(Odu100PeerRateStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_peerTunnelStatisticsTable':relationship(Odu100PeerTunnelStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raChannelListTable':relationship(Odu100RaChannelListTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raScanListTable':relationship(Odu100RaScanListTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raSiteSurveyResultTable':relationship(Odu100RaSiteSurveyResultTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raStatusTable':relationship(Odu100RaStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raTddMacStatisticsTable':relationship(Odu100RaTddMacStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raTddMacStatusTable':relationship(Odu100RaTddMacStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_raValidPhyRatesTable':relationship(Odu100RaValidPhyRatesTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_ruStatusTable':relationship(Odu100RuStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_swStatusTable':relationship(Odu100SwStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_synchStatisticsTable':relationship(Odu100SynchStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'odu100_synchStatusTable':relationship(Odu100SynchStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'get_odu16_ru_conf_table':relationship(GetOdu16_ru_conf_table,backref="hosts",cascade="all,delete,delete-orphan"),\
'get_odu16_ra_status_table':relationship(GetOdu16RaStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"get_odu16_sw_status_table":relationship(GetOdu16SWStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"get_odu16_hw_desc_table":relationship(GetOdu16HWDescTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"get_odu16_ra_scan_list_table":relationship(GetOdu16RAScanListTable,backref="hosts",cascade="all,delete,delete-orphan"),\
#'get_odu16_peer_node_status_table':relationship(GetOdu16PeerNodeStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
#"retry_ap_scheduling":relationship(RetryApScheduling,backref="hosts",cascade="all,delete,delete-orphan"),\
"snmp_advance_options":relationship(SnmpAdvanceOptions,backref="hosts",cascade="all,delete,delete-orphan"),\
#"ap_scheduling_host_mapping":relationship(ApSchedulingHostMapping,backref="hosts",cascade="all,delete,delete-orphan"),\
"hosts_hostgroups":relationship(HostsHostgroups,backref="hosts",cascade="all,delete,delete-orphan"),\
"host_services":relationship(HostServices,backref="hosts", cascade="all,delete,delete-orphan"),\
"idu_e1PortStatusTable":relationship(IduE1PortStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_iduInfoTable":relationship(IduIduInfoTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_iduNetworkStatisticsTable":relationship(IduIduNetworkStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_linkStatisticsTable":relationship(IduLinkStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_linkStatusTable":relationship(IduLinkStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_portSecondaryStatisticsTable":relationship(IduPortSecondaryStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_portstatbadframeTable":relationship(IduPortstatbadframeTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_portstatgoodframeTable":relationship(IduPortstatgoodframeTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_portstatisticsTable":relationship(IduPortstatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_swPrimaryPortStatisticsTable":relationship(IduSwPrimaryPortStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_swStatusTable":relationship(IduSwStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_switchportstatusTable":relationship(IduSwitchportstatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
"idu_tdmoipNetworkInterfaceStatisticsTable":relationship(IduTdmoipNetworkInterfaceStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ap25_statisticsTable':relationship(Ap25StatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ap25_vapClientStatisticsTable':relationship(Ap25VapClientStatisticsTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ap25_versions':relationship(Ap25Versions,backref="hosts",cascade="all,delete,delete-orphan"),\
'host_status':relationship(HostStatus,backref="hosts",cascade="all,delete,delete-orphan"),\
'ap_client_ap_data':relationship(ApClient_ap_data,backref="hosts",cascade="all,delete,delete-orphan"),\
'ap_connected_client':relationship(ApConnected_client,backref="hosts",cascade="all,delete,delete-orphan"),\
'ccu_InformationTable':relationship(CcuInformationTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ccu_NetworkConfigurationTable':relationship(CcuNetworkConfigurationTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ccu_RealTimeStatusTable':relationship(CcuRealTimeStatusTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ccu_StatusDataTable':relationship(CcuStatusDataTable,backref="hosts",cascade="all,delete,delete-orphan"),\
'ccu_softwareinformationtable':relationship(CcuSoftwareInformationTable,backref="hosts",cascade="all,delete,delete-orphan"),'ap25_dhcpClientsTable':relationship(Ap25DhcpClientsTable,backref="hosts",cascade="all,delete,delete-orphan"),
'ap25_apScanDataTable':relationship(Ap25ApScanDataTable,backref="hosts",cascade="all,delete,delete-orphan")
})



###################################### Mapping for Config Profiles #########################################################################################



mapper(Odu16ConfigProfiles,tablename,properties={'set_odu16_ip_config_table':relationship(SetOdu16IPConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_network_interface_config':relationship(SetOdu16NetworkInterfaceConfig,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_omc_conf_table':relationship(SetOdu16OmcConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_peer_config_table':relationship(SetOdu16PeerConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_ra_acl_config_table':relationship(SetOdu16RAAclConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_om_operations_table':relationship(SetOdu16OmOperationsTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_ra_conf_table':relationship(SetOdu16RAConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_ra_llc_conf_table':relationship(SetOdu16RALlcConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_ra_tdd_mac_config':relationship(SetOdu16RATddMacConfig,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_ru_conf_table':relationship(SetOdu16RUConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_ru_date_time_table':relationship(SetOdu16RUDateTimeTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_sync_config_table':relationship(SetOdu16SyncConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_misc':relationship(SetOdu16Misc,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'set_odu16_sys_omc_registration_table':relationship(SetOdu16SysOmcRegistrationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswATUConfigTable':relationship(Odu100EswATUConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswMirroringPortTable':relationship(Odu100EswMirroringPortTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswPortAccessListTable':relationship(Odu100EswPortAccessListTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswPortBwTable':relationship(Odu100EswPortBwTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswPortConfigTable':relationship(Odu100EswPortConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswPortQinQTable':relationship(Odu100EswPortQinQTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_eswVlanConfigTable':relationship(Odu100EswVlanConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_ipConfigTable':relationship(Odu100IpConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_omcConfTable':relationship(Odu100OmcConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_peerConfigTable':relationship(Odu100PeerConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_raAclConfigTable':relationship(Odu100RaAclConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_raConfTable':relationship(Odu100RaConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_raLlcConfTable':relationship(Odu100RaLlcConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_raPreferredRFChannelTable':relationship(Odu100RaPreferredRFChannelTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_raTddMacConfigTable':relationship(Odu100RaTddMacConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_ruConfTable':relationship(Odu100RuConfTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_ruDateTimeTable':relationship(Odu100RuDateTimeTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_ruOmOperationsTable':relationship(Odu100RuOmOperationsTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_syncConfigTable':relationship(Odu100SyncConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'odu100_sysOmcRegistrationTable':relationship(Odu100SysOmcRegistrationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_aclportTable':relationship(IduAclportTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_alarmOutConfigTable':relationship(IduAlarmOutConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_alarmPortConfigurationTable':relationship(IduAlarmPortConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_atuconfigTable':relationship(IduAtuconfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_e1PortConfigurationTable':relationship(IduE1PortConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_iduAdminStateTable':relationship(IduIduAdminStateTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_iduOmOperationsTable':relationship(IduIduOmOperationsTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_linkConfigurationTable':relationship(IduLinkConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_mirroringportTable':relationship(IduMirroringportTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_networkConfigurationsTable':relationship(IduNetworkConfigurationsTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_omcConfigurationTable':relationship(IduOmcConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_poeConfigurationTable':relationship(IduPoeConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_portBwTable':relationship(IduPortBwTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_portqinqTable':relationship(IduPortqinqTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_rtcConfigurationTable':relationship(IduRtcConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_sectorIdentificationTable':relationship(IduSectorIdentificationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_switchPortconfigTable':relationship(IduSwitchPortconfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_sysOmcRegistrationTable':relationship(IduSysOmcRegistrationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_tdmoipNetworkInterfaceConfigurationTable':relationship(IduTdmoipNetworkInterfaceConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_temperatureSensorConfigurationTable':relationship(IduTemperatureSensorConfigurationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'idu_vlanconfigTable':relationship(IduVlanconfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_accesspointIPsettings':relationship(Ap25AccesspointIPsettings,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_basicConfiguration':relationship(Ap25BasicConfiguration,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_dhcpServer':relationship(Ap25DhcpServer,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_radioSelection':relationship(Ap25RadioSelection,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_radioSetup':relationship(Ap25RadioSetup,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_services':relationship(Ap25Services,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_vapSelection':relationship(Ap25VapSelection,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_aclMacTable':relationship(Ap25AclMacTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_basicACLconfigTable':relationship(Ap25BasicACLconfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_basicVAPsecurity':relationship(Ap25BasicVAPsecurity,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_basicVAPconfigTable':relationship(Ap25BasicVAPconfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_vapWPAsecurityConfigTable':relationship(Ap25VapWPAsecurityConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ap25_vapWEPsecurityConfigTable':relationship(Ap25VapWEPsecurityConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'Ap25AclStatisticsTable':relationship(Ap25AclStatisticsTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ccu_alarm_threshold_table':relationship(CcuAlarmAndThresholdTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ccu_aux_io_table':relationship(CcuAuxIOTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ccu_battery_panel_config_table':relationship(CcuBatteryPanelConfigTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ccu_control_table':relationship(CcuControlTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ccu_peer_info_table':relationship(CcuPeerInformationTable,backref="config_profiles",cascade="all,delete,delete-orphan"),\
'ccu_site_info_table':relationship(CcuSiteInformationTable,backref="config_profiles",cascade="all,delete,delete-orphan")})
##'swt4_bandwidth_control':relationship(Swt4BandwidthControl,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_storm_control':relationship(Swt4StormControl,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_port_statistics':relationship(Swt4PortStatistics,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_port_settings':relationship(Swt4PortSettings,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_ip_settings':relationship(Swt4IpSettings,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_vlan_settings':relationship(Swt4VlanSettings,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_port_based_priority':relationship(Swt4PortBasedPriority,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_dscp_based_priority':relationship(Swt4DscpBasedPriority,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_802_1p_based_priority':relationship(Swt48021pBasedPriority,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_ip_base_priority':relationship(Swt4IpBasePriority,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_queue_based_priority':relationship(Swt4QueueBasedPriority,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_queue_weight_based':relationship(Swt4QueueWeightBased,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_qos_arbitration':relationship(Swt4QosArbitration,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##'swt4_1p_remarking':relationship(Swt41pRemarking,backref="config_profiles",cascade="all,delete,delete-orphan"),\
##"hosts":relationship(Hosts,backref="config_profiles",cascade="all,delete,delete-orphan")})






####################################################################################################################################################


# single mapper
mapper(BlackListMacs,BlackListMacs.__table__)
mapper(Cities,Cities.__table__)
mapper(DaemonEvents,DaemonEvents.__table__)
mapper(DaemonTimestamp,DaemonTimestamp.__table__)
mapper(DiscoveredHosts,DiscoveredHosts.__table__)
mapper(ErrorDescription,ErrorDescription.__table__)
mapper(EventLog,EventLog.__table__)
#mapper(ApSchedulingHostMapping,ApSchedulingHostMapping.__table__)
mapper(HostgroupsGroups,HostgroupsGroups.__table__)
mapper(HostsHostgroups,HostsHostgroups.__table__)
mapper(HostAlertActionMapping,HostAlertActionMapping.__table__)
mapper(LocalhostBandwidth,LocalhostBandwidth.__table__)
mapper(LocalhostCpuUsage,LocalhostCpuUsage.__table__)
mapper(Modules,Modules.__table__)
mapper(NmsGraphs,NmsGraphs.__table__)
#mapper(Odu1007_2_20_oids,Odu1007_2_20_oids.__table__)
mapper(Odu1007_2_20_oids_multivalues,Odu1007_2_20_oids_multivalues.__table__)
#mapper(RetryApScheduling,RetryApScheduling.__table__)
mapper(RolePagesLink,RolePagesLink.__table__)
mapper(ServiceTemplates,ServiceTemplates.__table__)
mapper(SnmpAdvanceOptions,SnmpAdvanceOptions.__table__)
mapper(TcpDiscovery,TcpDiscovery.__table__)
mapper(TcpHealthCheck,TcpHealthCheck.__table__)
mapper(TrapAlarms,TrapAlarms.__table__)
mapper(TrapAlarmActionMapping,TrapAlarmActionMapping.__table__)
mapper(TrapAlarmClear,TrapAlarmClear.__table__)
mapper(TrapAlarmCurrent,TrapAlarmCurrent.__table__)
mapper(TrapIdMapping,TrapIdMapping.__table__)
mapper(UsersGroups,UsersGroups.__table__)
mapper(UserLogin,UserLogin.__table__)

# foreign key mapper
mapper(Hostgroups,Hostgroups.__table__,properties={"hostgroups_groups":relationship(HostgroupsGroups,backref="hostgroups",cascade="all,delete,delete-orphan"),\
"hosts_hostgroups":relationship(HostsHostgroups,backref="hostgroups",cascade="all,delete,delete-orphan")})

mapper(States,States.__table__,properties={"cities":relationship(Cities,backref="states",cascade="all,delete,delete-orphan")})

mapper(Countries,Countries.__table__,properties={"states":relationship(States,backref="countries",cascade="all,delete,delete-orphan")})

#mapper(ApScheduling,ApScheduling.__table__,properties={"ap_scheduling_host_mapping":relationship(ApSchedulingHostMapping,backref="ap_scheduling", cascade="all,delete,delete-orphan")})

mapper(HostServices,HostServices.__table__)

mapper(DeviceType,DeviceType.__table__,properties={"config_profiles":relationship(Odu16ConfigProfiles,backref="device_type",cascade="all,delete,delete-orphan"),\
"discovered_hosts":relationship(DiscoveredHosts,backref="device_type",cascade="all,delete,delete-orphan"),\
"hosts":relationship(Hosts,backref="device_type",cascade="all,delete,delete-orphan"),\
"firmware_mapping":relationship(FirmwareMapping,backref="device_type",cascade="all,delete,delete-orphan"),\
"nms_graphs":relationship(NmsGraphs,backref="device_type",cascade="all,delete,delete-orphan"),\
"odu100_7_2_20_oids":relationship(Odu1007_2_20_oids,backref="device_type",cascade="all,delete,delete-orphan"),\
"odu100_7_2_25_oids":relationship(Odu1007_2_25_oids,backref="device_type",cascade="all,delete,delete-orphan"),\
"service_template":relationship(ServiceTemplates,backref="device_type",cascade="all,delete,delete-orphan")})

mapper(Discovery,Discovery.__table__,properties={"discovered_hosts":relationship(DiscoveredHosts,backref="discovery",cascade="all,delete,delete-orphan"),\
"snmp_advance_options":relationship(SnmpAdvanceOptions,backref="discovery",cascade="all,delete,delete-orphan")})

mapper(DiscoveryType,DiscoveryType.__table__,properties={"discovery":relationship(Discovery,backref="discovery_type",cascade="all,delete,delete-orphan")})

#mapper(EventType,EventType.__table__,properties={"event_log":relationship(EventLog,backref="event_type",cascade="all,delete,delete-orphan")})

mapper(Groups,Groups.__table__,properties={"hostgroups_groups":relationship(HostgroupsGroups,backref="groups",cascade="all,delete,delete-orphan"),\
"host_alert_masking":relationship(HostAlertMasking,backref="groups",cascade="all,delete,delete-orphan"),\
"trap_alarm_masking":relationship(TrapAlarmMasking,backref="groups",cascade="all,delete,delete-orphan"),\
"users_groups":relationship(UsersGroups,backref="groups",cascade="all,delete,delete-orphan")})

mapper(Acknowledge,Acknowledge.__table__,properties={"host_alert_masking":relationship(HostAlertMasking,backref="acknowledge",cascade="all,delete,delete-orphan"),\
"trap_alarm_action_mapping":relationship(TrapAlarmActionMapping,backref="acknowledge",cascade="all,delete,delete-orphan"),\
"trap_alarm_masking":relationship(TrapAlarmMasking,backref="acknowledge",cascade="all,delete,delete-orphan")})

mapper(Actions,Actions.__table__,properties={"host_alert_masking":relationship(HostAlertMasking,backref="actions",cascade="all,delete,delete-orphan"),\
"trap_alarm_masking":relationship(TrapAlarmMasking,backref="actions",cascade="all,delete,delete-orphan")})

##mapper(ConfigProfiles,ConfigProfiles.__table__,properties={"hosts":relationship(Hosts,backref="config_profiles",cascade="all,delete,delete-orphan")})

mapper(ConfigProfileType,ConfigProfileType.__table__,properties={"config_profiles":relationship(Odu16ConfigProfiles,backref="config_profile_type",cascade="all,delete,delete-orphan")})

##mapper(Hosts,Hosts.__table__,properties={"retry_ap_scheduling":relationship(RetryApScheduling,backref="hosts",cascade="all,delete,delete-orphan"),\
##"snmp_advance_options":relationship(SnmpAdvanceOptions,backref="hosts",cascade="all,delete,delete-orphan"),\
##"ap_scheduling_host_mapping":relationship(ApSchedulingHostMapping,backref="hosts",cascade="all,delete,delete-orphan"),\
##"hosts_hostgroups":relationship(HostsHostgroups,backref="hosts",cascade="all,delete,delete-orphan")})

mapper(HostAlertMasking,HostAlertMasking.__table__,properties={"host_alert_action_mapping":relationship(HostAlertActionMapping,backref="host_alert_masking",cascade="all,delete,delete-orphan")})

mapper(HostAssets,HostAssets.__table__,properties={"hosts":relationship(Hosts,backref="host_assets",cascade="all,delete,delete-orphan")})

#mapper(FirmwareMapping,FirmwareMapping.__table__,properties={"hosts":relationship(Hosts,backref="firmware_mapping",cascade="all,delete,delete-orphan")})

mapper(HostOs,HostOs.__table__,properties={"hosts":relationship(Hosts,backref="host_os",cascade="all,delete,delete-orphan")})

mapper(HostStates,HostStates.__table__,properties={"hosts":relationship(Hosts,backref="host_states",cascade="all,delete,delete-orphan")})

mapper(HostVendor,HostVendor.__table__,properties={"hosts":relationship(Hosts,backref="host_vendor",cascade="all,delete,delete-orphan")})

mapper(NmsInstance,NmsInstance.__table__,properties={"hosts":relationship(Hosts,backref="nms_instance",cascade="all,delete,delete-orphan"),\
"user_login":relationship(UserLogin,backref="nms_instance",cascade="all,delete,delete-orphan")})

mapper(Odu1007_2_20_oids,Odu1007_2_20_oids.__table__,properties={"odu100_7_2_20_oids_multivalues":relationship(Odu1007_2_20_oids_multivalues,backref="odu100_7_2_20_oids",cascade="all,delete,delete-orphan")})

mapper(Odu1007_2_25_oids,Odu1007_2_25_oids.__table__,properties={"odu100_7_2_25_oids_multivalues":relationship(Odu1007_2_25_oids_multivalues,backref="odu100_7_2_25_oids",cascade="all,delete,delete-orphan")})


mapper(Pages,Pages.__table__,properties={"modules":relationship(Modules,backref="pages",cascade="all,delete,delete-orphan")})

mapper(PagesLink,PagesLink.__table__,properties={"role_pages_link":relationship(RolePagesLink,backref="pages_link",cascade="all,delete,delete-orphan")})

mapper(Priority,Priority.__table__,properties={"hosts":relationship(Hosts,backref="priority",cascade="all,delete,delete-orphan"),\
"trap_id_mapping":relationship(TrapIdMapping,backref="priority",cascade="all,delete,delete-orphan")})

mapper(Roles,Roles.__table__,properties={"groups":relationship(Groups,backref="roles",cascade="all,delete,delete-orphan"),\
"role_pages_link":relationship(RolePagesLink,backref="roles",cascade="all,delete,delete-orphan")})

mapper(Scheduling,Scheduling.__table__,properties={"discovery":relationship(Discovery,backref="scheduling",cascade="all,delete,delete-orphan")})

mapper(Sites,Sites.__table__,properties={"hosts":relationship(Hosts,backref="sites",cascade="all,delete,delete-orphan")})

mapper(Snapins,Snapins.__table__,properties={"pages":relationship(Pages,backref="snapins",cascade="all,delete,delete-orphan")})

mapper(TrapAlarmFieldTable,TrapAlarmFieldTable.__table__,properties={"trap_alarm_masking":relationship(TrapAlarmMasking,backref="trap_alarm_field_table",cascade="all,delete,delete-orphan")})

mapper(TrapAlarmMasking,TrapAlarmMasking.__table__,properties={"trap_alarm_action_mapping":relationship(TrapAlarmActionMapping,backref="trap_alarm_masking",cascade="all,delete,delete-orphan")})

mapper(Users,Users.__table__,properties={"users_groups":relationship(UsersGroups,backref="users",cascade="all,delete,delete-orphan"),\
"user_login":relationship(UserLogin,backref="users",cascade="all,delete,delete-orphan")})

###################################### SWITCH MODEL CREATED HERE #######################################################################################

##class Swt4BandwidthControl(Base):
##	__tablename__= "swt4_bandwidth_control"
##	switch_bandwidth_control_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	cpu_protection = Column(INT)
##	port = Column(TINYINT)
##	type = Column(TINYINT)
##	state = Column(TINYINT)
##	rate = Column(INT)
##
##	def __init__(self,config_profile_id,cpu_protection,port,type,state,rate):
##		self.switch_bandwidth_control_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.cpu_protection = cpu_protection
##		self.port = port
##		self.type = type
##		self.state = state
##		self.rate = rate
##		
##	def __repr__(self):
##		return "<Swt4Bandwidth_control('%s','%s','%s','%s','%s','%s','%s')>" %(self.switch_bandwidth_control_id,self.config_profile_id,self.cpu_protection,self.port,self.type,self.state,self.rate)
##
##
##class Swt4StormControl(Base):
##	__tablename__= "swt4_storm_control"
##	switch_storm_control_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	strom_type = Column(TINYINT(4))
##	state = Column(TINYINT(4))
##	rate = Column(TINYINT(4))
##
##	def __init__(self,config_profile_id,strom_type,state,rate):
##		self.switch_storm_control_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.strom_type = strom_type
##		self.state = state
##		self.rate = rate
##		
##	def __repr__(self):
##		return "<Swt4Storm_control('%s','%s','%s','%s','%s')>" %(self.switch_storm_control_id,self.config_profile_id,self.strom_type,self.state,self.rate)
##
##class Swt4PortStatistics(Base):
##	__tablename__= "swt4_port_statistics"
##	switch_port_statistics_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	port = Column(TINYINT)
##	state = Column(TINYINT)
##	speed = Column(TINYINT)
##	flow_control = Column(TINYINT)
##
##	def __init__(self,config_profile_id,port,state,speed,flow_control):
##		self.switch_port_statistics_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.port = port
##		self.state = state
##		self.speed = speed
##		self.flow_control = flow_control
##		
##	def __repr__(self):
##		return "<Swt4Port_statistics('%s','%s','%s','%s','%s','%s')>" %(self.switch_port_statistics_id,self.config_profile_id,self.port,self.state,self.speed,self.flow_control)
##
##class Swt4PortSettings(Base):
##    __tablename__= "swt4_port_settings"
##    swt4_port_settings_id = Column(VARCHAR(64),primary_key=True)
##    config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##    link_fault_pass_through = Column(SMALLINT)
##    port = Column(SMALLINT)
##    state = Column(SMALLINT)
##    speed = Column(SMALLINT)
##    flow_control = Column(SMALLINT)
##    def __init__(self,config_profile_id,link_fault_pass_through,port,state,speed,flow_control):
##        self.swt4_port_settings_id = uuid.uuid1()
##        self.config_profile_id = config_profile_id
##        self.link_fault_pass_through = link_fault_pass_through
##        self.port = port
##        self.state = state
##        self.speed = speed
##        self.flow_control = flow_control
##        
##    def __repr__(self):
##        return "<Swt4Port_settings('%s','%s','%s','%s','%s','%s','%s')>" %(self.swt4_port_settings_id,self.config_profile_id,self.link_fault_pass_through,self.port,self.state,self.speed,self.flow_control)
##
##class Swt4IpSettings(Base):
##	__tablename__= "swt4_ip_settings"
##	switch_ip_settings_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	mode = Column(VARCHAR(12))
##	ip_address = Column(VARCHAR(15))
##	subnet_mask = Column(VARCHAR(15))
##	gateway = Column(VARCHAR(15))
##
##	def __init__(self,config_profile_id,mode,ip_address,subnet_mask,gateway):
##		self.switch_ip_settings_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.mode = mode
##		self.ip_address = ip_address
##		self.subnet_mask = subnet_mask
##		self.gateway = gateway
##		
##	def __repr__(self):
##		return "<Swt4IpSettings('%s','%s','%s','%s','%s','%s')>" %(self.switch_ip_settings_id,self.config_profile_id,self.mode,self.ip_address,self.subnet_mask,self.gateway)
##
##class Swt4VlanSettings(Base):
##    __tablename__= "swt4_vlan_settings"
##    swt4_vlan_settings_id = Column(VARCHAR(64),primary_key=True)
##    config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##    vlan_ingress_filter = Column(SMALLINT)
##    vlan_pass_all = Column(SMALLINT)
##    port = Column(SMALLINT)
##    pvid = Column(SMALLINT)
##    mode = Column(SMALLINT)
##
##    def __init__(self,config_profile_id,vlan_ingress_filter,vlan_pass_all,port,pvid,mode):
##        self.swt4_vlan_settings_id = uuid.uuid1()
##        self.config_profile_id = config_profile_id
##        self.vlan_ingress_filter = vlan_ingress_filter
##        self.vlan_pass_all = vlan_pass_all
##        self.port = port
##        self.pvid = pvid
##        self.mode = mode
##        
##    def __repr__(self):
##        return "<Swt4VlanSettings('%s','%s','%s','%s','%s','%s','%s')>" %(self.swt4_vlan_settings_id,self.config_profile_id,self.vlan_ingress_filter,self.vlan_pass_all,self.port,self.pvid,self.mode)
##
##class Swt4PortBasedPriority(Base):
##	__tablename__= "swt4_port_based_priority"
##	switch_port_based_priority_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	port = Column(TINYINT)
##	priority = Column(TINYINT)
##
##	def __init__(self,config_profile_id,port,priority):
##		self.switch_port_based_priority_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.port = port
##		self.priority = priority
##		
##	def __repr__(self):
##		return "<Swt4PortBasedPriority('%s','%s','%s','%s')>" %(self.switch_port_based_priority_id,self.config_profile_id,self.port,self.priority)
##
##class Swt4DscpBasedPriority(Base):
##	__tablename__= "swt4_dscp_based_priority"
##	switch_dscp_based_priority_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	dscp = Column(VARCHAR(8))
##	priority = Column(TINYINT)
##	def __init__(self,config_profile_id,dscp,priority):
##		self.switch_dscp_based_priority_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.dscp = dscp
##		self.priority = priority
##		
##	def __repr__(self):
##		return "<Swt4DscpBasedPriority('%s','%s','%s','%s')>" %(self.switch_dscp_based_priority_id,self.config_profile_id,self.dscp,self.priority)
##
##class Swt48021pBasedPriority(Base):
##    __tablename__= "swt4_802_1p_based_priority"
##    switch_802_1p_based_priority_id = Column(VARCHAR(64),primary_key=True)
##    config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##    p802 = Column(TINYINT)
##    priority = Column(TINYINT)
##
##    def __init__(self,config_profile_id,p802,priority):
##        self.switch_802_1p_based_priority_id = uuid.uuid1()
##        self.config_profile_id = config_profile_id
##        self.p802 = p802
##        self.priority = priority
##        
##    def __repr__(self):
##        return "<Swt48021pBasedPriority('%s','%s','%s','%s')>" %(self.switch_802_1p_based_priority_id,self.config_profile_id,self.p802,self.priority)
##
##
##class Swt4IpBasePriority(Base):
##	__tablename__= "swt4_ip_base_priority"
##	swt4_ip_base_priority_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	ip_base_priority = Column(INT)
##	ip_type = Column(INT)
##	ip_address = Column(VARCHAR(15))
##	network_mask = Column(VARCHAR(15))
##	priority = Column(INT)
##
##	def __init__(self,config_profile_id,ip_base_priority,ip_type,ip_address,network_mask,priority):
##		self.swt4_ip_base_priority_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.ip_base_priority = ip_base_priority
##		self.ip_type = ip_type
##		self.ip_address = ip_address
##		self.network_mask = network_mask
##		self.priority = priority
##		
##	def __repr__(self):
##		return "<Swt4IpBasePriority('%s','%s','%s','%s','%s','%s','%s')>" %(self.swt4_ip_base_priority_id,self.config_profile_id,self.ip_base_priority,self.ip_type,self.ip_address,self.network_mask,self.priority)
##
##
##class Swt4QueueBasedPriority(Base):
##	__tablename__= "swt4_queue_based_priority"
##	switch_queue_based_priority_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	qid_map = Column(TINYINT)
##	priority = Column(TINYINT)
##
##	def __init__(self,config_profile_id,qid_map,priority):
##		self.switch_queue_based_priority_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.qid_map = qid_map
##		self.priority = priority
##		
##	def __repr__(self):
##		return "<Swt4QueueBasedPriority('%s','%s','%s','%s')>" %(self.switch_queue_based_priority_id,self.config_profile_id,self.qid_map,self.priority)
##
##
##class Swt4QueueWeightBased(Base):
##	__tablename__= "swt4_queue_weight_based"
##	switch_queue_weight_based = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	queue = Column(TINYINT)
##	weight = Column(TINYINT)
##
##	def __init__(self,config_profile_id,queue,weight):
##		self.switch_queue_weight_based = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.queue = queue
##		self.weight = weight
##		
##	def __repr__(self):
##		return "<Swt4QueueWeightBased('%s','%s','%s','%s')>" %(self.switch_queue_weight_based,self.config_profile_id,self.queue,self.weight)
##
##class Swt4QosArbitration(Base):
##	__tablename__= "swt4_qos_arbitration"
##	switch_qos_arbitration_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	priority = Column(VARCHAR(15))
##	level = Column(TINYINT)
##
##	def __init__(self,config_profile_id,priority,level):
##		self.switch_qos_arbitration_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.priority = priority
##		self.level = level
##		
##	def __repr__(self):
##		return "<Swt4QosArbitration('%s','%s','%s','%s')>" %(self.switch_qos_arbitration_id,self.config_profile_id,self.priority,self.level)
##
##class Swt41pRemarking(Base):
##	__tablename__= "swt4_1p_remarking"
##	switch_1p_remarking_id = Column(VARCHAR(64),primary_key=True)
##	config_profile_id = Column(VARCHAR(64),ForeignKey('config_profiles.config_profile_id'))
##	p_remarking = Column(TINYINT)
##	p802_remarking = Column(TINYINT)
##
##	def __init__(self,config_profile_id,p_remarking,p802_remarking):
##		self.switch_1p_remarking_id = uuid.uuid1()
##		self.config_profile_id = config_profile_id
##		self.p_remarking = p_remarking
##		self.p802_remarking = p802_remarking
##		
##	def __repr__(self):
##		return "<Swt41pRemarking('%s','%s','%s','%s')>" %(self.switch_1p_remarking_id,self.config_profile_id,self.p_remarking,self.p802_remarking)
##
##















