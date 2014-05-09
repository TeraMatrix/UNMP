#!/usr/bin/python2.6
#######################################################################################
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	defaul_data_delete.py
# Creation Date			:	18-September-2011
# Purpose			:	This file delete the default data.

##########################################################################

# success 0 means No error
# success 1  Exception or Error
# success 2 means some mysql error(services not running,connection not created)


# import the modules(pakesges)
import MySQLdb
from mysql_collection import mysql_connection


# Exception class for own exception handling.
class SelfException(Exception):
    """
    @return: this class return the exception msg.
    @rtype: dictionary
    @requires: Exception class package(module)
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @organization: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """

    def __init__(self, msg):
        output_dictt = {'success': 2, 'output': str(msg)}
        html.write(str(output_dictt))


def default_data(h):
    global html
    html = h
    flag = 0
    css_list = []
    javascript_list = []
    html.new_header("Delete Sample Data", "", "", css_list, javascript_list)
    try:
        db, cursor = mysql_connection('nms_copy')
        if db == 1:
            raise SelfException(cursor)
        cursor.execute(
            "DELETE FROM `config_profiles` WHERE `config_profiles`.`config_profile_id` = '7f87a5a2-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "DELETE FROM `config_profiles` WHERE `config_profiles`.`config_profile_id` = 'cd597544-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute("DELETE FROM `host_assets` WHERE `host_asset_id` = '7f7544e8-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute("DELETE FROM `host_assets` WHERE `host_asset_id` = 'cd42cb00-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_nw_interface_statistics_table` WHERE host_id='7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_nw_interface_statistics_table` WHERE host_id='cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_peer_node_status_table` WHERE host_id='7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_peer_node_status_table` WHERE host_id='cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_ra_tdd_mac_statistics_entry` WHERE host_id='7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_ra_tdd_mac_statistics_entry` WHERE host_id='cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "delete FROM  `get_odu16_synch_statistics_table` WHERE host_id='7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "delete FROM  `get_odu16_synch_statistics_table` WHERE host_id='cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_ru_conf_table` WHERE host_id='7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "delete FROM `get_odu16_ru_conf_table` WHERE host_id='cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute("delete FROM `hostgroups_groups` WHERE `hostgroup_id`='02df7db2-12a3-11e1-9bb7-207c8f2e8042'")
        cursor.execute(
            "DELETE FROM `hosts` WHERE `hosts`.`host_id` = '7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "DELETE FROM `hosts` WHERE `hosts`.`host_id` = 'cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "delete FROM `hosts_hostgroups` WHERE host_id='7f7a23fa-12a2-11e1-9791-207c8f2e8042'")
        cursor.execute(
            "delete FROM `hosts_hostgroups` WHERE host_id='cd44d4c2-12a2-11e1-acca-207c8f2e8042'")
        cursor.execute(
            "DELETE FROM  `nagios_hosts` WHERE `nagios_hosts`.`host_id` = 3634")
        cursor.execute(
            "DELETE FROM  `nagios_hosts` WHERE `nagios_hosts`.`host_id` = 3635")
        cursor.execute(
            "DELETE FROM  `nagios_hoststatus` WHERE `host_object_id` = 628")
        cursor.execute(
            "DELETE FROM  `nagios_hoststatus` WHERE `host_object_id` = 617")
        cursor.execute(
            "DELETE FROM  `nagios_statehistory` WHERE `object_id` = 628")
        cursor.execute(
            "DELETE FROM  `nagios_statehistory` WHERE `object_id` = 617")
        cursor.execute("DELETE FROM  `nagios_hosts` WHERE `host_id` = 628")
        cursor.execute("DELETE FROM  `nagios_hosts` WHERE `host_id` = 617")
        cursor.execute(
            "DELETE FROM `trap_alarms` WHERE `agent_id` = '172.22.0.110'")
        cursor.execute(
            "DELETE FROM `trap_alarms` WHERE `agent_id` = '172.22.0.111'")
        cursor.execute(
            "DELETE FROM `trap_alarms` WHERE `agent_id` = '172.22.0.103'")
        cursor.execute(
            "DELETE FROM `trap_alarm_clear` WHERE `agent_id` = '172.22.0.110'")
        cursor.execute(
            "DELETE FROM `trap_alarm_clear` WHERE `agent_id` = '172.22.0.111'")
        cursor.execute(
            "DELETE FROM `trap_alarm_clear` WHERE `agent_id` = '172.22.0.15'")
        cursor.execute(
            "DELETE FROM `trap_alarm_clear` WHERE `agent_id` = '172.22.0.102'")
        cursor.execute(
            "DELETE FROM `trap_alarm_clear` WHERE `agent_id` = '172.22.0.103'")
        cursor.execute(
            "DELETE FROM `trap_alarm_current` WHERE `agent_id` = '172.22.0.110'")
        cursor.execute(
            "DELETE FROM `trap_alarm_current` WHERE `agent_id` = '172.22.0.111'")
        cursor.execute(
            "DELETE FROM `trap_alarm_current` WHERE `agent_id` = '172.22.0.15'")
        cursor.execute(
            "DELETE FROM `trap_alarm_current` WHERE `agent_id` = '172.22.0.102'")
        cursor.execute(
            "DELETE FROM `trap_alarm_current` WHERE `agent_id` = '172.22.0.103'")

        cursor.close()
        db.commit()
        db.close()
        html.write(str("All sample data deleted successfully."))
        html.new_footer()
    except MySQLdb as e:
        html.write("Sorry data couldn't be deleted.")
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        pass
    except Exception as e:
        html.write("Sorry data couldn't be deleted.")
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()
