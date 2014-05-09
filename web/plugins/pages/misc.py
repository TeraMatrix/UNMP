#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@date: 23-Oct-2011
@version: 0.1
@note: This contains miscellaneous's page & function links
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the page functions
import common_controller
import daemons_controller
import license_controller

# map URLs to page rendering functions
pagehandlers.update({

    # web sshTerminal
    "webssh": common_controller.webssh,

    # Nagios
    "tactical_overview": common_controller.tactical_overview,
    # "view_page_tip_local_dashboard": common_controller.view_page_tip_local_dashboard,
    # Daemons
    "daemons_controller": daemons_controller.mahipal_daemons,
    "load": daemons_controller.load_daemons,
    "doAction": daemons_controller.doAction_daemon,
    "get_status": daemons_controller.get_status_daemon,
    # Localhost Dashboard
    "localhost_dashboard": common_controller.localhost_dashboard,
    "system_uptime": common_controller.system_uptime,
    "system_ram": common_controller.system_ram,
    "system_harddisk_details": common_controller.system_harddisk_details,
    "system_processor_details": common_controller.system_processor_details,
    "system_bandwidth_details": common_controller.system_bandwidth_details,
    # System License
    "manage_license": license_controller.manage_license,
    "license_upload": license_controller.license_upload,

    # ip_mac_search
    "common_ip_mac_search": common_controller.common_ip_mac_search,
    "get_ip_mac_selected_device": common_controller.get_ip_mac_selected_device,

    # trap_details_show_listing

    "show_trap_alarms": common_controller.show_trap_alarms,
    "device_status": common_controller.device_status,

    ## Local Reconciliation

    "local_reconciliation": common_controller.local_reconciliation,
    "common_reconcile": common_controller.common_reconcile,
    "chk_common_reconcile": common_controller.chk_common_reconcile,
    "get_admin_state": common_controller.get_admin_state,

})
