#!/usr/bin/python2.6
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2010             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Import modules that contain the page functions

import main
import page_logwatch
import views
import sidebar
import permissions
import actions
import user_management
import shortcutlink
import templates
import overview
import host_config
import dashboard
import scheduling
import firmware
import performance
import nagvis_maps
import status_snmptt
import odu_view
import alarm_masking
import alarm_trap_information
# map URLs to page rendering functions
import odu_monitor_view
import alarm_mapping
import odu_dashboard
import googlemap
import circle_graph
import unmp_user_management
import idu_dashboard
import firmware_update
import swt4_view
import daemons_controller
import odu100_dashboard
import odu100_common_dashboard
import example
import default_data_delete
import unmp_login
import log_controller
import idu_profiling_controller
#import idu4_controller
import idu4_controller
import odu_scheduling_controller
import manage_login_controller
import ap_dashboard_controller
import ap_profiling_controller
import ap_advanced_graph_controller
import specific_dashboard_controller
import firmware_controller
import sp_status_controller
import advanced_status_controller
import client_dashboard_controller
import ccu

pagehandlers.update({
   "index"                 : main.page_index,
   "main"                  : main.page_main,
   "switch_site"           : main.ajax_switch_site,
   "edit_views"            : views.page_edit_views,
   "edit_view"             : views.page_edit_view,
   "get_edit_column"       : views.ajax_get_edit_column,
   "export_views"          : views.ajax_export,
   "view"                  : views.page_view,
   "logwatch"              : page_logwatch.page,
   "side"                  : sidebar.page_side,
   "sidebar_add_snapin"    : sidebar.page_add_snapin,
   "sidebar_snapin"        : sidebar.ajax_snapin,
   "sidebar_openclose"     : sidebar.ajax_openclose,
   "sidebar_move_snapin"   : sidebar.move_snapin,
   "switch_master_state"   : sidebar.ajax_switch_masterstate,
   "add_bookmark"          : sidebar.ajax_add_bookmark,
   "del_bookmark"          : sidebar.ajax_del_bookmark,
   "customlink_openclose"  : sidebar.ajax_customlink_openclose,
   "edit_bookmark"         : sidebar.page_edit_bookmark,
   "view_permissions"      : permissions.page_view_permissions,
   "edit_permissions"      : permissions.page_edit_permissions,
   "nagios_action"         : actions.ajax_action,
# shortcut links on first page
#    "auto_discovery"        : shortcutlink.page_auto_discovery,
#   "manage_host_service"   : shortcutlink.page_manage_host_service,
#    "view_alerts"           : shortcutlink.page_view_alerts,
#    "manage_hostgroup"      : shortcutlink.page_manage_hostgroup,
#    "manage_servicegroup"   : shortcutlink.page_manage_servicegroup,
#    "manage_host"           : shortcutlink.page_manage_host,
#    "manage_service"        : shortcutlink.page_manage_service,

#auto discovery
# #    "ajaxcall_autodiscovery_ping": shortcutlink.autodiscovery_ping,
#    "ajaxcall_autodiscovery_snmp": shortcutlink.autodiscovery_snmp,
#    "ajaxcall_autodiscovery_upnp": shortcutlink.autodiscovery_upnp,
#    "ajaxcall_autodiscovery_sdmc": shortcutlink.autodiscovery_sdmc,
#    "start_ajaxcall_autodiscovery_ping": shortcutlink.start_autodiscovery_ping,
#   "start_ajaxcall_autodiscovery_snmp": shortcutlink.start_autodiscovery_snmp,
#    "start_ajaxcall_autodiscovery_upnp": shortcutlink.start_autodiscovery_upnp,
#    "start_ajaxcall_autodiscovery_sdmc": shortcutlink.start_autodiscovery_sdmc,
# hostgroup
#    "ajaxcall_add_hostgroup": shortcutlink.ajax_add_hostgroup,
#    "ajaxcall_delete_hostgroup": shortcutlink.ajax_delete_hostgroup,
#    "ajaxcall_update_hostgroup": shortcutlink.ajax_update_hostgroup,
#    "form_for_hostgroup"    : shortcutlink.form_for_hostgroup,
#    "grid_view_hostgroup"   : shortcutlink.grid_view_hostgroup,
# servicegroup
#    "ajaxcall_add_servicegroup": shortcutlink.ajax_add_servicegroup,
#    "ajaxcall_delete_servicegroup": shortcutlink.ajax_delete_servicegroup,
#    "ajaxcall_update_servicegroup": shortcutlink.ajax_update_servicegroup,
#    "form_for_servicegroup"    : shortcutlink.form_for_servicegroup,
#    "grid_view_servicegroup"   : shortcutlink.grid_view_servicegroup,
# host
#    "ajaxcall_add_host": shortcutlink.ajax_add_host,
#    "ajaxcall_delete_host": shortcutlink.ajax_delete_host,
#    "ajaxcall_update_host": shortcutlink.ajax_update_host,
#    "form_for_host"    : shortcutlink.form_for_host,
#    "grid_view_host"   : shortcutlink.grid_view_host,
#    "parent_multiple_select_list":shortcutlink.parent_multiple_select_list,
# service
#  #   "ajaxcall_add_service": shortcutlink.ajax_add_service,
#    "ajaxcall_delete_service": shortcutlink.ajax_delete_service,
#    "ajaxcall_update_service": shortcutlink.ajax_update_service,
#    "form_for_service"    : shortcutlink.form_for_service,
#  #   "grid_view_service"   : shortcutlink.grid_view_service,
#    "form_for_service_setting": shortcutlink.form_for_service_setting,
# service template
#    "manage_service_template": templates.page_manage_service_template,
# manage user
#   "manage_user"     : user_management.page_manage_user,
#   "user_grid_view"  : user_management.user_grid_view,
#   "form_for_user"   : user_management.form_for_user,
#   "add_user"        : user_management.add_user,
#   "delete_user"     : user_management.delete_user,
#   "update_user"     : user_management.update_user,
#   "change_password" : user_management.page_change_password,
#   "password_changed": user_management.password_changed,
#   "logout"          : user_management.logout,
# network_overview
#    "network_overview": overview.network_overview,
#    "discoveryAndNetworkDetails": overview.discoveryAndNetworkDetails,
#    "dicoveredHostDetailsForPing": overview.dicoveredHostDetailsForPing,
#    "dicoveredHostDetailsForSnmp": overview.dicoveredHostDetailsForSnmp,
#    "dicoveredHostDetailsForUpnp": overview.dicoveredHostDetailsForUPnP,
#    "dicoveredHostDetailsForSdmc": overview.dicoveredHostDetailsForSDMC,
#    "discoveryDetailsForPing": overview.discoveryDetailsForPing,
#    "discoveryDetailsForSnmp": overview.discoveryDetailsForSnmp,
#  #   "discoveryDetailsForUpnp": overview.discoveryDetailsForUPnP,
#    "discoveryDetailsForSdmc": overview.discoveryDetailsForSDMC,
#    "discoveryStatus": overview.discoveryStatus,
#    "stopStartDiscovery": overview.stopStartDiscovery,
#    "startDiscovery": overview.startDiscovery,
#    "createHostConfiguration": overview.createHostConfiguration,
#    "createSeviceConfiguration":overview.createSeviceConfiguration,
#    "discoveredHostDetailsForAll":overview.discoveredHostDetailsForAll,
# host configuration management and template management
   "manage_configuration_template" : host_config.manage_configuration_template,
   "view_configuration_template" : host_config.view_configuration_template,
   "add_configuration_template" : host_config.add_configuration_template,
   "delete_configuration_template" : host_config.delete_configuration_template,
   "edit_configuration_template" : host_config.edit_configuration_template,
   "create_config_tamplate": host_config.create_config_tamplate,
   "manage_host_configuration" : host_config.manage_host_configuration,
   "discoverDevices": host_config.discoverDevices,
   "factory_reset":host_config.factory_reset,
   "set_ip": host_config.set_ip,
   "apply_config_template": host_config.apply_config_template,
   "image_upload": host_config.image_upload,
# Update ACL
   "update_acl": host_config.update_acl,
   "list_of_mac_address": host_config.list_of_mac_address,
   "delete_mac_address": host_config.delete_mac_address,
   "add_mac_address":host_config.add_mac_address,
   "upload_mac_address_file":host_config.upload_mac_address_file,
   "select_ap_to_apply_mac":host_config.select_ap_to_apply_mac,
   "http_request_for_ap":host_config.http_request_for_ap,
# NMS Dashboard
   "nms_dashboard":dashboard.nms_dashboard,
   "harddisk_details":dashboard.harddisk_details,
   "ram_details":dashboard.ram_details,
   "processor_details":dashboard.processor_details,
   "processor_last_details":dashboard.processor_last_details,
   "bandwidth_last_details":dashboard.bandwidth_last_details,
   "bandwidth_details":dashboard.bandwidth_details,
   "ap_graph":dashboard.ap_graph,
   "ap_user_graph":dashboard.ap_user_graph,
   "get_number_of_aps":dashboard.get_number_of_aps,
# AP Dasboard
   "ap_dashboard":dashboard.ap_dashboard,
   "ap_interfaces":dashboard.ap_interfaces,
   "access_point_details_table":dashboard.access_point_details_table,
   "ap_connected_user":dashboard.ap_connected_user,
   "get_uptime_connected_client":dashboard.get_uptime_connected_client,
   "ap_clients_dashboard":dashboard.ap_clients_dashboard,
   "get_overall_bandwidth":dashboard.get_overall_bandwidth,
# Scheduling
   "ap_scheduling":scheduling.ap_scheduling,
   "add_ap_scheduler":scheduling.add_ap_scheduler,
   "load_non_repeative_events":scheduling.load_non_repeative_events,
   "load_repeative_events":scheduling.load_repeative_events,
   "event_resize":scheduling.event_resize,
   "event_drop":scheduling.event_drop,
   "delete_ap_scheduler":scheduling.delete_ap_scheduler,
   "view_access_point_list":scheduling.view_access_point_list,
   "get_ap_schedule_details":scheduling.get_ap_schedule_details,
   "update_ap_scheduler":scheduling.update_ap_scheduler,
   "radio_status":scheduling.radio_status,
   "change_redio":scheduling.change_redio,
# Firmware
   "firmware_update":firmware.update,
   "get_device_by_type":firmware.device_table,
# Performance
    "performance_history":performance.performance_history,
    "get_service_by_host":performance.service_status,
    "host_history":performance.host_history,
# Map generater
    "nagvis_maps":nagvis_maps.create_maps,
# Alarm Detail
    "status_snmptt":status_snmptt.start_page,
    "trap_filter_function":status_snmptt.trap_filter_function,
    "trap_detail_information":status_snmptt.trap_detail_information,
    "trap_search_elements":status_snmptt.trap_search_elements,
    "trap_report_creating":status_snmptt.trap_report_creating,
    "update_date_time":status_snmptt.update_date_time,
    "page_tip_event_details":status_snmptt.page_tip_event_details,
    

#Odu Details
    "odu_dashboard":odu_view.odu_dashboard,
    "odu_profiling":odu_view.odu_profiling,
    "odu_profiling_form":odu_view.odu_profiling_form,
    "odu_listing":odu_view.odu_listing,
    "omc_config_detail":odu_view.omc_config_detail,
    "ru_configuration":odu_view.ru_configuration,
    "tdd_mac_config":odu_view.tdd_mac_config,
    "omc_registration_configuration":odu_view.omc_registration_configuration,
    "syn_configuration":odu_view.syn_configuration,
    "ra_config":odu_view.ra_config,
    "ra_llc_configuration" : odu_view.ra_llc_configuration,
    "peer_config":odu_view.peer_config,
    "Peer_mac_Cancel":odu_view.Peer_mac_Cancel,
    "acl_config":odu_view.acl_config,
    "peer_delete_slaves":odu_view.peer_delete_slaves,
    "Omc_Config":odu_view.Omc_Config,	
    "omc_config_form":odu_view.omc_config_form,
    "RU_Configuration":odu_view.RU_Configuration,
    "RU_Cancel_Configuration":odu_view.RU_Cancel_Configuration,
    "Tdd_Mac_Configuration":odu_view.Tdd_Mac_Configuration,
    "Tdd_Mac_Cancel_Configuration":odu_view.Tdd_Mac_Cancel_Configuration,
    "SysOmc_Registration_Configuration":odu_view.SysOmc_Registration_Configuration,
    "sys_registration_form":odu_view.sys_registration_form,
    "Syn_Omc_Registration_Configuration":odu_view.Syn_Omc_Registration_Configuration,
    "Syn_Cancel_Omc_Registration_Configuration":odu_view.Syn_Cancel_Omc_Registration_Configuration,
    "Peer_mac":odu_view.Peer_mac,
    "Acl_Configuration":odu_view.Acl_Configuration,
    "Acl_Cancel_Configuration":odu_view.Acl_Cancel_Configuration,
    "get_device_data_table":odu_view.get_device_data_table,
    "retry_set_for_odu16":odu_view.retry_set_for_odu16,
    "retry_set_all_for_odu16":odu_view.retry_set_all_for_odu16,
    "commit_flash":odu_view.commit_flash,
    "get_device_list_odu":odu_view.get_device_list_odu,
    "cancel_odu_form":odu_view.cancel_odu_form,
    "odu100_profiling_form":odu_view.odu100_profiling_form,
    "odu100_omc_config":odu_view.odu100_omc_config,
    "odu100_sync_config":odu_view.odu100_sync_config,
    "odu100_ip_config":odu_view.odu100_ip_config,
    "odu100_ra_configuration":odu_view.odu100_ra_configuration,
    "odu100_ru_configuration":odu_view.odu100_ru_configuration,
    "odu100_peer_configuration":odu_view.odu100_peer_configuration,
    "odu100_commit_to_flash":odu_view.odu100_commit_to_flash,
    "acl_data_bind":odu_view.acl_data_bind,
    "odu100_acl_add_mac_config":odu_view.odu100_acl_add_mac_config,
    "acl_delete":odu_view.acl_delete,
    "acl_reconciliation" : odu_view.acl_reconciliation,
    "odu16_reconcilation" : odu_view.odu16_reconcilation,
    "chk_reconcilation_status" : odu_view.chk_reconcilation_status,
    "reconcilation_list" : odu_view.reconcilation_list,
    "page_tip_odu_listing" : odu_view.page_tip_odu_listing,
    "page_tip_odu_profiling" : odu_view.page_tip_odu_profiling,
    "update_mac_list" : odu_view.update_mac_list,
    "odu100_acl_reconcile" : odu_view.odu100_acl_reconcile,
    "odu100_acl_mode" : odu_view.odu100_acl_mode,
    "channel_configuration" : odu_view.channel_configuration,
    "sys_registration_configuration" : odu_view.sys_registration_configuration,
    "refresh_channel_list" : odu_view.refresh_channel_list,
    "view_modulation_rate" : odu_view.view_modulation_rate,
    "site_survey_data" : odu_view.site_survey_data,
    "site_survey_result" : odu_view.site_survey_result,
    "site_survey_snmp" : odu_view.site_survey_snmp,
    "hw_sw_frequency_status" : odu_view.hw_sw_frequency_status,
    "show_peer_status" : odu_view.show_peer_status,
    "admin_state_show": odu_view.admin_state_show,
    "change_admin_state" : odu_view.change_admin_state,
    "all_lock_unlock" : odu_view.all_lock_unlock,
    "global_admin_status" : odu_view.global_admin_status,
    "bw_calculate_form" : odu_view.bw_calculate_form,
    "bw_action" : odu_view.bw_action,
    "refresh_peer_form" : odu_view.refresh_peer_form,
    "reboot_odu" : odu_view.reboot_odu,
    "ping_chk" : odu_view.ping_chk,
    "llc_configuration" : odu_view.llc_configuration,
    "ra_channel_list_table" : odu_view.ra_channel_list_table,
    "refresh_channel_freq_list" : odu_view.refresh_channel_freq_list,
    "get_site_survey" : odu_view.get_site_survey,
    "odu_form_reconcile" : odu_view.odu_form_reconcile,
#alarm masking detail
   "alarm_masking":alarm_masking.start_page,
   "alarm_masking_information":alarm_masking.alarm_masking_information,
   "add_edit_masking_table_form":alarm_masking.add_edit_masking_table_form,
   "add_form_entry2":alarm_masking.add_form_entry,
   "edit_masking_form_entry":alarm_masking.edit_masking_form_entry,
   "delete_masking_field":alarm_masking.delete_masking_field,
   "page_tip_alarm_masking":alarm_masking.page_tip_alarm_masking,


### change alarm detail aaccording to css its new page
   "alarm_trap_information":alarm_trap_information.start_page,
   "alarm_datail_function":alarm_trap_information.alarm_datail_function,



# alarm_mapping  
   "alarm_mapping":alarm_mapping.start_page,
   "get_trap_lists":alarm_mapping.get_trap_lists,   
   "alarm_datail_function":alarm_mapping.alarm_datail_function,
   "add_edit_form_show":alarm_mapping.add_edit_form_show,
   "add_form_entry":alarm_mapping.add_form_entry,
   "edit_form_entry":alarm_mapping.edit_form_entry,
   "delete_alarm_id":alarm_mapping.delete_alarm_id,
   "page_tip_alarm_mapping":alarm_mapping.page_tip_alarm_mapping,



#google map 

   "googlemap":googlemap.graph,
   "google_host_graph":googlemap.google_host_graph,
   "save_updates":googlemap.save_updates,
   "show_details":googlemap.show_details,
   "nms_details":googlemap.nms_details,
   "new_discover_deviec":googlemap.new_discover_deviec,
   "new_host_update":googlemap.new_host_update,
   "site_show_management":googlemap.site_show_management,
   "host_status_update_information":googlemap.host_status_update_information,
   "enabled_device_state":googlemap.enabled_device_state,   
   "page_tip_google_map":googlemap.page_tip_google_map,
   

# circle_map(Network Map)
  "circle_graph":circle_graph.graph,
  "show_network_graph":circle_graph.show_network_graph,
  "network_nms_details":circle_graph.network_nms_details,
  "show_host_details":circle_graph.show_host_details,
  "page_tip_circle_graph":circle_graph.page_tip_circle_graph,


# ODU Dashboard
   "odu_dashboard":odu_dashboard.odu_dashboard_page,
   "odu_network_interface_graph":odu_dashboard.odu_network_interface_graph,
   "get_no_of_odu":odu_dashboard.get_no_of_odu,
   "odu_tdd_mac_error":odu_dashboard.odu_tdd_mac_error,
   "odu_peer_node_signal":odu_dashboard.odu_peer_node_signal,
   "odu_synslost_counter":odu_dashboard.odu_synslost_counter,
   "all_odu_outage_graph":odu_dashboard.odu_outage_graph,
   "odu_common_dashboard_report_generating":odu_dashboard.odu_common_dashboard_report_generating,
   "page_tip_ubr_common_dashboard":odu_dashboard.page_tip_ubr_common_dashboard,


# login/logout
   "login":unmp_login.login,
   "unmp_login":unmp_login.unmp_login,
   "unmp_logout":unmp_login.unmp_logout,

# idu_dashboard ---------
  "idu_dashboard":idu_dashboard.idu_dashboard_page,
  "idu_network_interface_graph":idu_dashboard.idu_network_interface_graph,
  "idu_device_information":idu_dashboard.idu_device_information,
  "idu_tdmoip_network_interface_graph":idu_dashboard.idu_tdmoip_network_interface_graph,
  "idu_port_status_graph":idu_dashboard.idu_port_status_graph,
  "idu_trap_information":idu_dashboard.idu_trap_information,
  "idu_trap_graph":idu_dashboard.idu_trap_graph,
  "idu_outage_graph":idu_dashboard.idu_outage_graph,
  

#Firmware Update
   "firmware_listing":firmware_update.firmware_listing,
   "get_device_list_for_firmware":firmware_update.get_device_list_for_firmware,
   "firmware_process":firmware_update.firmware_process,
   "firmware_update_set":firmware_update.firmware_update_set,
   "update_firmware_result":firmware_update.update_firmware_result,
   "page_tip_firmware_update" : firmware_update.page_tip_firmware_update,
   "firmware_file_upload":firmware_update.firmware_file_upload,
   "ap_firmware_view":firmware_update.ap_firmware_view,
   "odu_firmware_file_upload":firmware_update.odu_firmware_file_upload,
   "odu_firmware_view":firmware_update.odu_firmware_view,
   "idu_firmware_view" : firmware_update.idu_firmware_view,
   "idu_firmware_file_upload" : firmware_update.idu_firmware_file_upload,
   "firmware_update_device_show" : firmware_controller.firmware_update_device_show,
   "firmware_master_slave_list" : firmware_controller.firmware_master_slave_list,
   #"firmware_file_upload":firmware_controller.firmware_file_upload,
   "select_firmware_table" : firmware_controller.select_firmware_table,
   "update_firmware_view" : firmware_controller.update_firmware_view,    
   
   
   
#Switch Profiling
   "swt_profiling" : swt4_view.swt_profiling,
   "swt4_profiling_form" : swt4_view.swt4_profiling_form,
   "get_device_list" : swt4_view.get_device_list,
   "swt_ip_config_form_action" : swt4_view.swt_ip_config_form_action,
   "swt4_port_setting_form_action" : swt4_view.swt4_port_setting_form_action,
   "swt4_vlan_setting_form_action" : swt4_view.swt4_vlan_setting_form_action,
   "swt_bandwidth_form_action" : swt4_view.swt_bandwidth_form_action,
   "swt_storm_form_action" : swt4_view.swt_storm_form_action,
   "swt4_port_priority_action" : swt4_view.swt4_port_priority_action,
   "swt4_dscp_priority_action" : swt4_view.swt4_dscp_priority_action,
   "swt4_802_priority_action" : swt4_view.swt4_802_priority_action,
   "swt4_ip_base_priority_action" : swt4_view.swt4_ip_base_priority_action,
   "swt4_queue_priority_action" : swt4_view.swt4_queue_priority_action,
   "swt4_queue_weight_action" : swt4_view.swt4_queue_weight_action,
   "swt4_qos_abstraction_action" : swt4_view.swt4_qos_abstraction_action,
   "swt4_1p_remarking_action" : swt4_view.swt4_1p_remarking_action,
   "update_bandwidth" : swt4_view.update_bandwidth,
   "update_port_settings" : swt4_view.update_port_settings,
   "update_storm" : swt4_view.update_storm,
   "update_vlan" : swt4_view.update_vlan,
   "update_port_priority" : swt4_view.update_port_priority,
   "update_dscp_priority" : swt4_view.update_dscp_priority,
   "update_802_priority" : swt4_view.update_802_priority,
   "update_ip_base_priority" : swt4_view.update_ip_base_priority,
   "update_queue_priority" : swt4_view.update_queue_priority,
   "update_queue_weight" : swt4_view.update_queue_weight,
   "update_qos_abstraction" : swt4_view.update_qos_abstraction,
   "update_1p_remarking" : swt4_view.update_1p_remarking,
   "swt4_commit_flash" : swt4_view.swt4_commit_flash,
   "reboot" : swt4_view.reboot,
   "reboot_final" : swt4_view.reboot_final,
# Mahipal-Daemons
    "daemons_controller":daemons_controller.mahipal_daemons,
    "load":daemons_controller.load_daemons,
    "doAction":daemons_controller.doAction_daemon,
    "get_status":daemons_controller.get_status_daemon,


# ODU Monitoing 
   "odu_profiling1":odu_monitor_view.odu_profiling,
   "odu_monitor_view":odu_monitor_view.welcome_odu_monitor_page,
   "odu_network_interface_table_graph":odu_monitor_view.odu_network_interface_table_graph,
   "get_device_list_odu_for_monitoring":odu_monitor_view.get_device_list_odu,
   "odu_device_information":odu_monitor_view.odu_device_information,
   "odu_trap_graph":odu_monitor_view.odu_trap_graph,
   "odu_trap_information":odu_monitor_view.odu_trap_information,
   "odu_outage_graph":odu_monitor_view.odu_outage_graph,
   "odu_error_graph":odu_monitor_view.odu_error_graph,
   "odu_signal_strength_graph":odu_monitor_view.odu_signal_strength_graph,
   "odu_device_report":odu_monitor_view.odu_device_report,
   "odu_sync_lost_graph":odu_monitor_view.odu_sync_lost_graph,
   "page_tip_ubr_monitor_dashboard":odu_monitor_view.page_tip_ubr_monitor_dashboard,
   "odu_excel_report_genrating":odu_monitor_view.odu_excel_report_genrating,
   "add_date_time_on_slide":odu_monitor_view.add_date_time_on_slide,

# odu 100 dashboard
  "odu100_profiling1":odu100_dashboard.odu_profiling,
  "get_device_list_odu100_for_monitoring":odu100_dashboard.get_device_list_odu100,
  "odu100_dashboard":odu100_dashboard.odu100_dashboard,
  "odu100_network_interface_table_graph":odu100_dashboard.odu100_network_interface_table_graph,
  "odu100_error_graph":odu100_dashboard.odu100_error_graph,
  "odu100_sync_lost_graph":odu100_dashboard.odu100_sync_lost_graph,
  "odu100_signal_strength_graph":odu100_dashboard.odu100_signal_strength_graph,
  "odu100_trap_graph":odu100_dashboard.odu100_trap_graph,
  "odu100_outage_graph":odu100_dashboard.odu100_outage_graph,
  "odu100_trap_information":odu100_dashboard.odu100_trap_information,
  "odu100_device_information":odu100_dashboard.odu100_device_information,
  "odu100_device_report":odu100_dashboard.odu100_device_report,
  "odu100_excel_report_genrating":odu100_dashboard.odu100_excel_report_genrating,
  "page_tip_ubre_monitor_dashboard":odu100_dashboard.page_tip_ubre_monitor_dashboard,
  "add_date_time_on_slide_odu100":odu100_dashboard.add_date_time_on_slide_odu100,




# odu100 common dashboard
  "odu100_common_dashboard":odu100_common_dashboard.odu100_common_dashboard,
  "odu100_network_interface_graph":odu100_common_dashboard.odu100_network_interface_graph,
  "get_no_of_odu100_devices":odu100_common_dashboard.get_no_of_odu100_devices,
  "odu100_tdd_mac_error":odu100_common_dashboard.odu100_tdd_mac_error,
  "odu100_peer_node_signal":odu100_common_dashboard.odu100_peer_node_signal,
  "odu100_synslost_counter":odu100_common_dashboard.odu100_synslost_counter,
  "odu100_common_dashboard_outage_graph":odu100_common_dashboard.odu100_common_dashboard_outage_graph,
  "odu100_common_dashboard_report_generating":odu100_common_dashboard.odu100_common_dashboard_report_generating,
  
# device pages
    "device_details_example":example.device_details_example,
    "page_tip_device_detail":example.page_tip_device_detail,
    "view_service_details_example":example.view_service_details_example,
    "nagios_hostgroup" : example.nagios_hostgroup,
    "nagios_host_details" : example.nagios_host_details,
    "edit_hostgroup_service_details":example.edit_hostgroup_service_details,
    "apply_nagios_hostgroup_changes":example.apply_nagios_hostgroup_changes,
    "apply_hostgroup_host_changes":example.apply_hostgroup_host_changes,
    "help_nagios_hostgroup":example.help_nagios_hostgroup,
    
# sample data deletion
    "default_data_delete":default_data_delete.default_data, 
# Log Pages
   "log_user":log_controller.main_log,
   "get_log_data":log_controller.get_data,
   "get_current_log_data":log_controller.get_current_data,
   "get_alarm_log_data_form":log_controller.get_alarm_current_data,
   "view_page_tip_log_user" :log_controller.view_page_tip_log_user,   

#IDU Pages
   "idu_listing" : idu_profiling_controller.idu_listing, 
   "idu_profiling" : idu_profiling_controller.idu_profiling,
   "page_tip_idu_listing" : idu_profiling_controller.page_tip_idu_listing,
   "idu_device_listing_table" : idu_profiling_controller.idu_device_listing_table,
   "get_device_list_idu_profiling" : idu_profiling_controller.get_device_list_idu_profiling,
   "alarm_port_form" : idu_profiling_controller.alarm_port_form,
   "port_configuration_form" : idu_profiling_controller.port_configuration_form,
   "port_bandwidth_form" : idu_profiling_controller.port_bandwidth_form,
   "port_QinQ_form" : idu_profiling_controller.port_QinQ_form,
   "port_ATU_form" : idu_profiling_controller.port_ATU_form,
   "device_update_reconciliation":idu_profiling_controller.device_update_reconciliation,
   "reconciliation_status_idu" : idu_profiling_controller.reconciliation_status_idu,
   "commit_to_flash" : idu_profiling_controller.commit_to_flash,
   "reboot" : idu_profiling_controller.reboot,
   "ping_check" : idu_profiling_controller.ping_check,
   "temperature_form_action" : idu_profiling_controller.temperature_form_action,
   "date_time_action" : idu_profiling_controller.date_time_action,
   "poe_form_action" : idu_profiling_controller.poe_form_action,
   "swt_bw_action" : idu_profiling_controller.swt_bw_action,
   "update_bw_form" : idu_profiling_controller.update_bw_form,
   "mirror_port_form_action" : idu_profiling_controller.mirror_port_form_action,
   "update_qinq_form" : idu_profiling_controller.update_qinq_form,
   "qinq_form_action" : idu_profiling_controller.qinq_form_action,
   "unmp_ip_action" : idu_profiling_controller.unmp_ip_action, 
   "e1_port" : idu_profiling_controller.e1_port,
   "swt_port_config_action" : idu_profiling_controller.swt_port_config_action,
   "update_swt_port_form" : idu_profiling_controller.update_swt_port_form,
   "port_vlan_add_form" : idu_profiling_controller.port_vlan_add_form,
   "vlan_form_action" : idu_profiling_controller.vlan_form_action,
   "update_vlan_port_form" : idu_profiling_controller.update_vlan_port_form,
   "e1_port_form_action" : idu_profiling_controller.e1_port_form_action,
   "link_port_delete" : idu_profiling_controller.link_port_delete,
   "update_link_port_table" : idu_profiling_controller.update_link_port_table,
   "port_link_form" : idu_profiling_controller.port_link_form,
   "link_form_action" : idu_profiling_controller.link_form_action,
   "update_e1_port_table" : idu_profiling_controller.update_e1_port_table,
   "get_selected_timeslot" : idu_profiling_controller.get_selected_timeslot,
   "vlan_port_delete" : idu_profiling_controller.vlan_port_delete,
   "idu_hw_sw_frequency_status" : idu_profiling_controller.idu_listing_status,
   "e1_admin_state_show" : idu_profiling_controller.e1_admin_state_show,
   "link_admin_state_show" : idu_profiling_controller.link_admin_state_show,
   "main_admin_state_show" : idu_profiling_controller.main_admin_state_show,
   "e1_admin_parameters" : idu_profiling_controller.e1_admin_parameters,
   "link_admin_parameters" : idu_profiling_controller.link_admin_parameters,
   "main_admin_parameters" : idu_profiling_controller.main_admin_parameters,
   "all_locked_unlocked" : idu_profiling_controller.all_locked_unlocked,
   "link_all_locked_unlocked" : idu_profiling_controller.link_all_locked_unlocked,
   "link_status_count" : idu_profiling_controller.link_status_count,
   "global_admin_request" : idu_profiling_controller.global_admin_request,
   "global_admin" : idu_profiling_controller.global_admin,
   "page_tip_idu_profiling" : idu_profiling_controller.page_tip_idu_profiling,
   "idu_form_reconcile" : idu_profiling_controller.idu_form_reconcile,
# IDU 4 port dashboard start here
   "idu4_dashboard_profiling":idu4_controller.idu4_dashboard_profiling,
   "idu4_dashboard":idu4_controller.idu4_dashboard,
   "idu4_network_interface_graph":idu4_controller.idu4_network_interface_graph,
   "idu4_tdmoip_network_interface_graph":idu4_controller.idu4_tdmoip_network_interface_graph,
   "idu4_device_details":idu4_controller.idu4_device_details,
   "idu4_event_graph":idu4_controller.idu4_event_graph,
   "idu4_outage_graph":idu4_controller.idu4_outage_graph,
   "idu4_alarm_event_table":idu4_controller.idu4_alarm_event_table,
   "idu4_excel_generating":idu4_controller.idu4_excel_generating,
   "idu4_pdf_generating":idu4_controller.idu4_pdf_generating,
   "page_tip_idu4_monitor_dashboard":idu4_controller.page_tip_idu4_monitor_dashboard,
   "idu4_add_date_time_on_slide":idu4_controller.idu4_add_date_time_on_slide,
   "idu4_port_statistics_graph":idu4_controller.idu4_port_statistics_graph,
   "idu4_link_status_table":idu4_controller.idu4_link_status_table,
   "idu4_e1_port_status_table":idu4_controller.idu4_e1_port_status_table,
   "idu4_get_link_value_name":idu4_controller.idu4_get_link_value_name,
   
# Manage login
   "manage_login":manage_login_controller.get_data,
   "get_login_data":manage_login_controller.get_login_data,
   "delete_login_data":manage_login_controller.delete_login_data,
   "view_page_tip_manage_login":manage_login_controller.view_page_tip_manage_login,   
       
    # odu scheduling
   "odu_scheduling" : odu_scheduling_controller.odu_scheduling,
   "add_odu_scheduler":odu_scheduling_controller.add_odu_scheduler,
   "delete_odu_scheduler":odu_scheduling_controller.delete_odu_scheduler,
   "get_odu_schedule_details":odu_scheduling_controller.get_odu_schedule_details,
   "update_odu_scheduler":odu_scheduling_controller.update_odu_scheduler,
   "load_repeative_events_odu":odu_scheduling_controller.load_repeative_events_odu,
   "load_non_repeative_events_odu":odu_scheduling_controller.load_non_repeative_events_odu,
   "event_resize_odu":odu_scheduling_controller.event_resize_odu,
   "event_drop_odu":odu_scheduling_controller.event_drop_odu,
   "view_access_point_list_odu":odu_scheduling_controller.view_access_point_list_odu,
   "show_scheduling_status":odu_scheduling_controller.view_Scheduling_Details,
   "view_page_tip_scheduling":odu_scheduling_controller.view_page_tip_scheduling,
   
   # ap scheduling
   "odu_scheduling_get_device_info" : odu_scheduling_controller.odu_scheduling_get_device_info,
   # firmware scheduling
   "scheduling_firmware_file_upload":odu_scheduling_controller.scheduling_firmware_file_upload,
   "device_firmware_view":odu_scheduling_controller.device_firmware_view,   

# AP dashboard

   "ap_dashboard_profiling":ap_dashboard_controller.ap_dashboard_profiling,
   "ap_dashboard":ap_dashboard_controller.ap_dashboard,
   "ap_network_interface_graph":ap_dashboard_controller.ap_network_interface_graph,
   "get_device_list_ap_for_monitoring":ap_dashboard_controller.get_device_list_ap,
   "ap_add_date_time_on_slide":ap_dashboard_controller.ap_add_date_time_on_slide,
   "page_tip_ap_monitor_dashboard":ap_dashboard_controller.page_tip_ap_monitor_dashboard,
   "generic_json":ap_dashboard_controller.generic_json,
   "common_graph_creation":ap_dashboard_controller.common_graph_creation,
   "ap_device_details":ap_dashboard_controller.ap_device_details,
   "ap_excel_report_genrating":ap_dashboard_controller.ap_excel_report_genrating,

#AP Listing
   "ap_listing" : ap_profiling_controller.ap_listing,
   "page_tip_ap_listing" : ap_profiling_controller.page_tip_ap_listing,
   "ap_device_listing_table" : ap_profiling_controller.ap_device_listing_table,
   "get_device_list_ap_profiling" : ap_profiling_controller.get_device_list_ap_profiling,
   "ap_profiling" : ap_profiling_controller.ap_profiling,
   "commit_to_flash" : ap_profiling_controller.commit_to_flash,
   "acl_add_form" : ap_profiling_controller.acl_add_form,
   "acl_upload_form" : ap_profiling_controller.acl_upload_form,
   "update_reconciliation" : ap_profiling_controller.update_reconciliation,
   "reconciliation_status" : ap_profiling_controller.reconciliation_status,
   "chk_reconciliation_status" : ap_profiling_controller.chk_reconciliation_status,
   "ap25_reconcilation" : ap_profiling_controller.ap25_reconcilation,
   "ap25_reboot" : ap_profiling_controller.ap25_reboot,
   "ap_scan" : ap_profiling_controller.ap_scan,
   "ap_radio_form_action" : ap_profiling_controller.ap_radio_form_action,
   "ap_service_form_action" : ap_profiling_controller.ap_service_form_action,
   "selectVap" : ap_profiling_controller.selectVap,
   "select_vap_acl" : ap_profiling_controller.select_vap_acl,
   "ap_acl_form_action" : ap_profiling_controller.ap_acl_form_action,
   "acl_add_form_action" : ap_profiling_controller.acl_add_form_action,
   "delete_all_mac" : ap_profiling_controller.delete_all_mac,
   "delete_single_mac" : ap_profiling_controller.delete_single_mac,
   "vap_vap_select" : ap_profiling_controller.vap_vap_select,
   "ap_vap_form_action": ap_profiling_controller.ap_vap_form_action,
   "show_wireless_status" : ap_profiling_controller.show_wireless_status,
   "service_status" : ap_profiling_controller.service_status,
   "system_info" : ap_profiling_controller.system_info,
   "show_radio_admin" : ap_profiling_controller.show_radio_admin,
   "disable_enable_radio" : ap_profiling_controller.disable_enable_radio,
   "chk_radio_state" : ap_profiling_controller.chk_radio_state,
   "connected_clients" : ap_profiling_controller.connected_clients,
   "get_client_data_table" : ap_profiling_controller.get_client_data_table,
   "edit_ap_client":ap_profiling_controller.edit_ap_client,
   "edit_ap_client_details":ap_profiling_controller.edit_ap_client_details,
   "ap_form_reconcile" : ap_profiling_controller.ap_form_reconcile,
# AP Advanced Graph
   "get_ap_advanced_graph_value":ap_advanced_graph_controller.get_ap_advanced_graph_value,
   "ap_total_graph_name":ap_advanced_graph_controller.ap_total_graph_name,
   "advanced_graph_json_creation":ap_advanced_graph_controller.advanced_graph_json_creation,
   "ap_data_table_creation":ap_advanced_graph_controller.ap_data_table_creation,
   "ap_advanced_excel_creating":ap_advanced_graph_controller.ap_advanced_excel_creating,
   "advanced_update_date_time":ap_advanced_graph_controller.advanced_update_date_time,
   "page_tip_advanced_dashboard":ap_advanced_graph_controller.page_tip_advanced_dashboard,

#Specific Dashboard  graph
   "sp_dashboard_profiling":specific_dashboard_controller.sp_dashboard_profiling,
   "sp_dashboard":specific_dashboard_controller.sp_dashboard,
   "sp_generic_json":specific_dashboard_controller.sp_generic_json,
   "sp_common_graph_creation":specific_dashboard_controller.sp_common_graph_creation,
   "sp_device_details":specific_dashboard_controller.sp_device_details,
   "sp_client_information":specific_dashboard_controller.sp_client_information,
   "sp_excel_report_genrating":specific_dashboard_controller.sp_excel_report_genrating,
   "sp_csv_report_genrating":specific_dashboard_controller.sp_csv_report_genrating,
   "page_tip_sp_monitor_dashboard":specific_dashboard_controller.page_tip_sp_monitor_dashboard,
   "sp_add_date_time_on_slide":specific_dashboard_controller.sp_add_date_time_on_slide,
   "sp_event_alarm_information":specific_dashboard_controller.sp_event_alarm_information,
   "sp_pdf_report_genrating":specific_dashboard_controller.sp_pdf_report_genrating,
   "update_show_graph":specific_dashboard_controller.update_show_graph,


# This shipped function for status table showing
   "sp_status_profiling":sp_status_controller.sp_status_profiling,
   "sp_dashboard":sp_status_controller.sp_dashboard,
   "sp_generic_table_json":sp_status_controller.sp_generic_table_json,
   "sp_common_status_table_creation":sp_status_controller.sp_common_status_table_creation,
   "sp_status_device_details":sp_status_controller.sp_status_device_details,
   "sp_excel_status_report_genrating":sp_status_controller.sp_excel_status_report_genrating,
   "sp_csv_status_report_genrating":sp_status_controller.sp_csv_status_report_genrating,
   "page_tip_sp_status_table":sp_status_controller.page_tip_sp_status_table,
   "sp_add_date_time_on_slide_status":sp_status_controller.sp_add_date_time_on_slide_status,
   "update_show_graph_status":sp_status_controller.update_show_graph_status,
   "update_status_table_in_database":sp_status_controller.update_status_table_in_database,


   "get_advanced_status_value":advanced_status_controller.get_advanced_status_value,
   "ap_total_status_name":advanced_status_controller.ap_total_status_name,
   "advanced_status_json_creation":advanced_status_controller.advanced_status_json_creation,
   "status_data_table_creation":advanced_status_controller.status_data_table_creation,
   "advanced_status_excel_creating":advanced_status_controller.advanced_status_excel_creating,
   "advanced_status_update_date_time":advanced_status_controller.advanced_status_update_date_time,
   "page_tip_advanced_status":advanced_status_controller.page_tip_advanced_status,
	
# Dashboard  Client
   "client_dashboard_profiling":client_dashboard_controller.client_dashboard_profiling,
   "client_generic_json":client_dashboard_controller.client_generic_json,
   "client_graph_creation":client_dashboard_controller.client_graph_creation,
   "client_add_date_time_on_slide":client_dashboard_controller.client_add_date_time_on_slide,
   "client_device_details":client_dashboard_controller.client_device_details,
   "client_excel_report_genrating":client_dashboard_controller.client_excel_report_genrating,
   "client_csv_report_genrating":client_dashboard_controller.client_csv_report_genrating,
   "client_add_date_time_on_slide":client_dashboard_controller.client_add_date_time_on_slide,
   "client_state_information":client_dashboard_controller.client_state_information,
   "page_tip_client_monitor_dashboard":client_dashboard_controller.page_tip_client_monitor_dashboard,
   "update_client_graph":client_dashboard_controller.update_client_graph,
#   "sp_dashboard":specific_dashboard_controller.sp_dashboard,
#   "sp_event_alarm_information":specific_dashboard_controller.sp_event_alarm_information,
#   "sp_pdf_report_genrating":specific_dashboard_controller.sp_pdf_report_genrating,
#   "update_show_graph":specific_dashboard_controller.update_show_graph,

#CCU Listing
   "ccu_listing" : ccu.ccu_listing,
   "ccu_device_listing_table" : ccu.ccu_device_listing_table,
   "ccu_profiling" : ccu.ccu_profiling,	
   "get_device_list_ccu_profiling" : ccu.get_device_list_ccu_profiling,
   "battery_panel_action" : ccu.battery_panel_action,
   "alarm_threshold_action" : ccu.alarm_threshold_action,
   "peer_action" : ccu.peer_action,
   "unmp_ip_action" : ccu.unmp_ip_action,
   "aux_action" : ccu.aux_action,

   
})
