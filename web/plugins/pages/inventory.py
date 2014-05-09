#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@date: 23-Oct-2011
@version: 0.1
@note: This contains inventory's page & function links
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the page functions
import inventory_controller

# map URLs to page rendering functions
pagehandlers.update({
                     
                     # Host
                     "manage_host": inventory_controller.manage_host,
                     "grid_view_active_host": inventory_controller.grid_view_active_host,
                     "grid_view_disable_host": inventory_controller.grid_view_disable_host,
                     "grid_view_deleted_host": inventory_controller.grid_view_deleted_host,
                     "grid_view_discovered_host": inventory_controller.grid_view_discovered_host,
                     "form_host": inventory_controller.form_host,
                     "host_default_details":inventory_controller.host_default_details,
                     "add_host": inventory_controller.add_host,
                     "get_host_by_id": inventory_controller.get_host_by_id,
                     "edit_host":inventory_controller.edit_host,
                     "del_host":inventory_controller.del_host,
                     "del_deleted_host":inventory_controller.del_deleted_host,
                     "host_parents":inventory_controller.host_parents,
                     "odu_master_list":inventory_controller.odu_master_list,
                     "get_odu_ra_mac_and_node_type": inventory_controller.get_odu_ra_mac_and_node_type,
                     "get_mac_details": inventory_controller.get_mac_details,
                     "get_firmware_details": inventory_controller.get_firmware_details,
                     "get_hardware_detail": inventory_controller.get_hardware_detail,
                     "get_all_device_firmware_details": inventory_controller.get_all_device_firmware_details,
                     "get_master_mac_from_slave":inventory_controller.get_master_mac_from_slave,
                     "add_deleted_host":inventory_controller.add_deleted_host,
                     "get_network_details":inventory_controller.get_network_details,
                     "server_time":inventory_controller.server_time,
                     "is_duplicate_host_with_mac_address":inventory_controller.is_duplicate_host_with_mac_address,
                     "is_duplicate_host_with_ip_address":inventory_controller.is_duplicate_host_with_ip_address,
                     "is_duplicate_host_with_host_alias":inventory_controller.is_duplicate_host_with_host_alias,

                     # Hostgroup
                     "manage_hostgroup": inventory_controller.manage_hostgroup, 
                     "grid_view_hostgroup": inventory_controller.grid_view_hostgroup,
                     "form_hostgroup": inventory_controller.form_hostgroup,
                     "add_hostgroup": inventory_controller.add_hostgroup,
                     "get_hostgroup_by_id": inventory_controller.get_hostgroup_by_id,
                     "edit_hostgroup": inventory_controller.edit_hostgroup,
                     "del_hostgroup": inventory_controller.del_hostgroup,
                     
                     # Discovery
                     "discovery": inventory_controller.discovery,
                     "ping_discovery":inventory_controller.ping_discovery,
                     "ping_discovery_form":inventory_controller.ping_discovery_form, 
                     "ping_default_details":inventory_controller.ping_default_details,
                     "run_ping_discovery":inventory_controller.run_ping_discovery,
                     "run_snmp_discovery":inventory_controller.run_snmp_discovery,
                     "run_upnp_discovery":inventory_controller.run_upnp_discovery,
                     
                     "snmp_discovery":inventory_controller.snmp_discovery,
                     "snmp_discovery_form":inventory_controller.snmp_discovery_form,
                     "snmp_default_details":inventory_controller.snmp_default_details,
                      
                     "upnp_discovery":inventory_controller.upnp_discovery,
                     "upnp_discovery_form":inventory_controller.upnp_discovery_form,
                     "upnp_default_details":inventory_controller.upnp_default_details,
                      
                     "delete_discovered_host":inventory_controller.delete_discovered_host,
                     
                      # Service
                     "manage_service": inventory_controller.manage_service, 
                     "grid_view_service":inventory_controller.grid_view_service,
                     "edit_service_details":inventory_controller.edit_service_details,
                     "apply_service_changes":inventory_controller.apply_service_changes,
                     "update_service_table":inventory_controller.update_service_table,
                     
                     # Network Map
                     "network_map": inventory_controller.network_map, 
                     
                     # Vendor
                     "manage_vendor": inventory_controller.manage_vendor,
                     "grid_view_vendor": inventory_controller.grid_view_vendor,
                     "form_vendor": inventory_controller.form_vendor,
                     "add_vendor": inventory_controller.add_vendor,
                     "get_vendor_by_id": inventory_controller.get_vendor_by_id,
                     "edit_vendor": inventory_controller.edit_vendor,
                     "del_vendor": inventory_controller.del_vendor,
                     
                     # Black List Mac
                     "manage_black_list_mac": inventory_controller.manage_black_list_mac,
                     "grid_view_black_list_mac": inventory_controller.grid_view_black_list_mac,
                     "form_black_list_mac": inventory_controller.form_black_list_mac,
                     "add_black_list_mac": inventory_controller.add_black_list_mac,
                     "get_black_list_mac_by_id": inventory_controller.get_black_list_mac_by_id,
                     "edit_black_list_mac": inventory_controller.edit_black_list_mac,
                     "del_black_list_mac": inventory_controller.del_black_list_mac,
                     
                     # Misc
                     "write_nagios_config":inventory_controller.write_nagios_config,
                     "reload_nagios_config":inventory_controller.reload_nagios_config,
                     });
