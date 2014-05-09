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
import nagios_controller
# map URLs to page rendering functions
pagehandlers.update({

    "nagios_force_sync": nagios_controller.nagios_force_sync,
    # inventory functions
    "advanced_host_settings_nagios": nagios_controller.advanced_host_settings_nagios,
    "apply_advanced_host_settings_nagios": nagios_controller.apply_advanced_host_settings_nagios,
    "edit_nagios_host_from_inventory": nagios_controller.edit_nagios_host_from_inventory,
    "edit_nagios_hostgroup_from_inventory": nagios_controller.edit_nagios_hostgroup_from_inventory,
    "edit_nagios_hostgroup_inventory": nagios_controller.edit_nagios_hostgroup_inventory,
    "save_nagios_hostgroup_inventory": nagios_controller.save_nagios_hostgroup_inventory,
    # "view_page_tip_nagios_inventory_hosts": nagios_controller.view_page_tip_nagios_inventory_hosts,
    # "view_page_tip_nagios_inventory_hostgroups": nagios_controller.view_page_tip_nagios_inventory_hostgroups,

    # host functions
    "nagios_load": nagios_controller.nagios_load,
    "get_host_data_nagios": nagios_controller.get_host_data_nagios,
    "edit_nagios_host": nagios_controller.edit_nagios_host,
    "save_nagios_edit_host": nagios_controller.save_nagios_edit_host,
    # "view_page_tip_nagios_host": nagios_controller.view_page_tip_nagios_host,

    # host template functions
    "nagios_host_template": nagios_controller.nagios_load_host_template,
    "get_host_template_data_nagios": nagios_controller.get_host_template_data_nagios,
    "edit_nagios_host_template": nagios_controller.edit_nagios_host_template,
    "save_nagios_edit_host_template": nagios_controller.save_nagios_edit_host_template,
    # "view_page_tip_nagios_host_template": nagios_controller.view_page_tip_nagios_host_template,
    "nagios_delete_host_template": nagios_controller.nagios_delete_host_template,

    # service functions
    "nagios_service": nagios_controller.nagios_service,
    "get_service_data_nagios": nagios_controller.get_service_data_nagios,
    "edit_nagios_service": nagios_controller.edit_nagios_service,
    "save_nagios_edit_service": nagios_controller.save_nagios_edit_service,
    # "view_page_tip_nagios_service": nagios_controller.view_page_tip_nagios_service,
    "nagios_delete_service": nagios_controller.nagios_delete_service,


    # service template functions
    "nagios_service_template": nagios_controller.nagios_service_template,
    "get_service_template_data_nagios": nagios_controller.get_service_template_data_nagios,
    "edit_nagios_service_template": nagios_controller.edit_nagios_service_template,
    "save_nagios_edit_service_template": nagios_controller.save_nagios_edit_service_template,
    # "view_page_tip_nagios_service_template": nagios_controller.view_page_tip_nagios_service_template,
    "nagios_delete_service_template": nagios_controller.nagios_delete_service_template,

    # hostgroup functions
    "nagios_hostgroup_load": nagios_controller.nagios_hostgroup,
    "get_hostgroup_data_nagios": nagios_controller.get_hostgroup_data_nagios,
    "edit_nagios_hostgroup": nagios_controller.edit_nagios_hostgroup,
    "save_nagios_edit_hostgroup": nagios_controller.save_nagios_edit_hostgroup,
    # "view_page_tip_nagios_hostgroup": nagios_controller.view_page_tip_nagios_hostgroup,

    # host dependency functions
    "nagios_hostdependency": nagios_controller.nagios_hostdependency,
    "get_hostdependency_data_nagios": nagios_controller.get_hostdependency_data_nagios,
    "edit_nagios_hostdependency": nagios_controller.edit_nagios_hostdependency,
    "save_nagios_edit_hostdependency": nagios_controller.save_nagios_edit_hostdependency,
    # "view_page_tip_nagios_hostdependency": nagios_controller.view_page_tip_nagios_hostdependency,
    "nagios_delete_host_dependency": nagios_controller.nagios_delete_host_dependency,

    # service dependency functions
    "nagios_servicedependency": nagios_controller.nagios_servicedependency,
    "get_servicedependency_data_nagios": nagios_controller.get_servicedependency_data_nagios,
    "edit_nagios_servicedependency": nagios_controller.edit_nagios_servicedependency,
    "save_nagios_edit_servicedependency": nagios_controller.save_nagios_edit_servicedependency,
    # "view_page_tip_nagios_servicedependency": nagios_controller.view_page_tip_nagios_servicedependency,
    "nagios_delete_service_dependency": nagios_controller.nagios_delete_service_dependency,

    # servicegroup functions
    #"nagios_servicegroup" : nagios_controller.nagios_servicegroup,
    #"get_servicegroup_data_nagios" : nagios_controller.get_servicegroup_data_nagios,
    #"edit_nagios_servicegroup":nagios_controller.edit_nagios_servicegroup,
    #"save_nagios_edit_servicegroup":nagios_controller.save_nagios_edit_servicegroup,
    #"view_page_tip_nagios_servicegroup":nagios_controller.view_page_tip_nagios_servicegroup,


    # command functions
    "nagios_command_load": nagios_controller.nagios_command,
    "get_command_data_nagios": nagios_controller.get_command_data_nagios,
    "edit_nagios_command": nagios_controller.edit_nagios_command,
    "save_nagios_edit_command": nagios_controller.save_nagios_edit_command,
    # "view_page_tip_nagios_command": nagios_controller.view_page_tip_nagios_command,
    "nagios_delete_command": nagios_controller.nagios_delete_command,

    # settings
    "settings_nagios": nagios_controller.settings_nagios,
    "do_action_nagios": nagios_controller.do_action_nagios,
    "do_verify_nagios": nagios_controller.do_verify_nagios,

    # restore
    "restore_config_nagios": nagios_controller.restore_config_nagios,
    "restore_config_nagios_selected": nagios_controller.restore_config_nagios_selected,
})
