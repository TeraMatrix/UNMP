#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@date: 23-Oct-2011
@version: 0.1
@note: This contains role, group and user's page & function links
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the page functions
import usr_mgt_view
import user_controller
import hostgroup_mgmt_controller
# import role_mgt_view

# map URLs to page rendering functions
pagehandlers.update({

    # User
    "check_name": usr_mgt_view.check_name,
    "manage_user": usr_mgt_view.user_view,
    "add_user": usr_mgt_view.add_user,
    "add_group": usr_mgt_view.add_group,
    "edit_user_view": usr_mgt_view.edit_user_view,
    "edit_user": usr_mgt_view.edit_user,
    "change_password": usr_mgt_view.change_password,
    "del_user": usr_mgt_view.del_user,
    "user_detail_table": usr_mgt_view.user_detail_table,
    "user_settings": user_controller.user_settings,
    "get_user_settings": user_controller.get_user_settings,
    "save_user_settings_personal": user_controller.set_user_settings_personal,
    "user_settings_password": user_controller.get_user_settings_password,
    "save_user_settings_password": user_controller.set_user_settings_password,
    "check_password": user_controller.check_password,
    "lock_unlock_usr":usr_mgt_view.lock_unlock_usr,


    # help
    # "help_users_main": usr_mgt_view.page_tip_user_main,
    # "help_users_group": usr_mgt_view.page_tip_user_group,
    # "help_group_user": usr_mgt_view.page_tip_group_user,
    # "help_hostgroup_group": usr_mgt_view.page_tip_hostgroup_group,
    # "help_change_password": usr_mgt_view.page_tip_change_password,
    # "help_change_user_setting": usr_mgt_view.page_tip_change_user_setting,

    # Group
    "group_info": usr_mgt_view.group_info,
    "group_users": usr_mgt_view.group_users,
    "edit_group_view": usr_mgt_view.edit_group_view,
    "edit_group": usr_mgt_view.edit_group,
    "del_group": usr_mgt_view.del_group,
    "group_table": usr_mgt_view.group_table,

    # Group User
    "add_users_togroup": usr_mgt_view.add_users_togroup,
    "del_users_fromgroup": usr_mgt_view.del_users_fromgroup,
    "add_useringp_view": usr_mgt_view.add_useringp_view,
    "move_usertogp_view": usr_mgt_view.move_usertogp_view,
    "manage_group": usr_mgt_view.group_user_view,

    # Group Hostgroup
    "add_hgingp_view": usr_mgt_view.add_hgingp_view,
    "add_hostgroup_togroup": usr_mgt_view.add_hostgroup_togroup,
    "show_hostgroups": usr_mgt_view.show_hostgroups,
    "del_hostgroup_fromgroup": usr_mgt_view.del_hostgroup_fromgroup,
    "move_hostgroup_togroup": usr_mgt_view.move_hostgroup_togroup,
    "move_hgtogp_view": usr_mgt_view.move_hgtogp_view,

    # Hostgroup Group
    "hostgroup_group_view": usr_mgt_view.hostgroup_group_view,
    "group_hostgroups1": usr_mgt_view.group_hostgroups1,
    "group_to_hg_view": usr_mgt_view.group_to_hg_view,
    "add_group_tohostgroup": usr_mgt_view.add_group_tohostgroup,
    "move_group_tohostgroup": usr_mgt_view.move_group_tohostgroup,
    "del_group_fromhostgroup": usr_mgt_view.del_group_fromhostgroup,
    "hostgroup_table": usr_mgt_view.hostgroup_table,
    "hostgroup_info": usr_mgt_view.hostgroup_info,
    "hostgroup_groups": usr_mgt_view.hostgroup_groups,
    "add_gpinhg_view": usr_mgt_view.add_gpinhg_view,
    "show_groups": usr_mgt_view.show_groups,
    "move_gptohg_view": usr_mgt_view.move_gptohg_view,
    # hostgroup new
    "hostgroup_mgmt_view": hostgroup_mgmt_controller.hostgroup_mgmt_view,
    "get_hostgroup_data": hostgroup_mgmt_controller.get_hostgroup_data,
    "get_user_data_hostgroup": hostgroup_mgmt_controller.get_user_data_hostgroup,
    "show_groups_user": hostgroup_mgmt_controller.get_user_data_hostgroup,
    "viewGroupDetails": hostgroup_mgmt_controller.viewGroupDetails,
    # "view_page_tip_hostgroup": hostgroup_mgmt_controller.view_page_tip_hostgroup,
    # Role
    #"manage_role":role_mgt_view.role_view1,
    #    "check_rolename":role_mgt_view.check_rolename,
    #    "role_view1":role_mgt_view.role_view1,
    #    "role_table":role_mgt_view.role_table,
    #    "role_info":role_mgt_view.role_info,
    #    "add_roleview":role_mgt_view.add_roleview,
    #    "add_role":role_mgt_view.add_role,
    #    "edit_roleview":role_mgt_view.edit_roleview,
    #    "edit_role":role_mgt_view.edit_role,
    #    "del_role":role_mgt_view.del_role,
})
