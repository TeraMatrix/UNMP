#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@date: 23-Oct-2011
@version: 0.1
@note: This contains help link for each page
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the page functions
import inventory_controller
import reporting_controller
import daemons_controller
import common_controller
import license_controller

# map URLs to page rendering functions
pagehandlers.update({
    # "help": common_controller.unmp_help,
    # "help_inventory_hostgroup": inventory_controller.page_tip_inventory_hostgroup,
    # "help_inventory_host": inventory_controller.page_tip_inventory_host,
    # "help_inventory_discovery": inventory_controller.page_tip_inventory_discovery,
    # "help_inventory_service": inventory_controller.page_tip_inventory_service,
    # "help_inventory_network_map": inventory_controller.page_tip_inventory_network_map,
    # "help_inventory_vendor": inventory_controller.page_tip_inventory_vendor,
    # "help_inventory_black_list_mac": inventory_controller.page_tip_inventory_black_list_mac,
    # "help_crc_phy": reporting_controller.page_tip_crc_phy,
    # "help_rssi": reporting_controller.page_tip_rssi,
    # "help_network_usage": reporting_controller.page_tip_network_usage,
    # "help_network_outage": reporting_controller.page_tip_network_outage,
    # "help_trap": reporting_controller.page_tip_trap,
    # "help_daemons": daemons_controller.page_tip_daemons,
    # "help_license": license_controller.page_tip_license,
})
