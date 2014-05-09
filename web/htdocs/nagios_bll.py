#!/usr/bin/python2.6
"""
@author: Mahipal Choudhary
@since: 17-JULY-2012
@version: 0.1
@note: All BLL related functions Related with Nagios configuration.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2012 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

from datetime import datetime
from json import JSONEncoder
import subprocess

import MySQLdb

from common_bll import Essential
from nagios_parser import *
from unmp_config import SystemConfig


nms_instance = __file__.split("/")[3]

# Main Nagios Class


class NagiosBll(object):
    """
    Nagios related Model Class
    """
    localhost_list = []

    # The Constructor to get the localhost list.
    def __init__(self):
        try:
            self.localhost_list = []
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select host_name from hosts where is_localhost='1' "
            cursor.execute(query)
            localhost_tuple = cursor.fetchall()
            for row in localhost_tuple:
                self.localhost_list.append(row[0])
            cursor.close()
            db.close()
        except Exception, e:
            self.localhost_list = []

    # Function for Force Syncing Nagios
    def nagios_force_sync(self):
        """


        @return:
        """
        try:
            comment = "Backup before syncing & repairing the nagios configuration files."
            backup_result = create_backup(comment)
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            # write hostgroups file
            query = "select hostgroup_name,hostgroup_alias from hostgroups "
            hostgroup_db = {}
            cursor.execute(query)
            hostgroup_tuple = cursor.fetchall()
            for row in hostgroup_tuple:
                hostgroup_db[row[0]] = {'hostgroup_name': row[0],
                                        'alias': row[1]}

            dt = load_configuration(['hostgroups.cfg'])
            hostgroup_result = load_db_by_name('hostgroup')
            if hostgroup_result['success'] == 0:
                hostgroup_config = hostgroup_result['data']
            else:
                hostgroup_config = {}

            for db_hg in hostgroup_db.keys():
                if db_hg in hostgroup_config:  # hostgroup is in .cfg and DB. update name and alias
                    hostgroup_config[db_hg].update(hostgroup_db[db_hg])
                else:
                    hostgroup_config[db_hg] = hostgroup_db[
                        db_hg]  # hostgroup is in DB. Add in cfg

            for config_hg in hostgroup_config.keys():
                if config_hg in hostgroup_db:  # hostgroup is in .cfg and DB. pass
                    pass
                else:
                    hostgroup_config.pop(
                        config_hg)  # hostgroup is in .cfg only. remove.

            shelve_name = 'hostgroup'
            file_name = 'hostgroups.cfg'
            updated_dict = hostgroup_config
            attribute = "hostgroup"
            rt = nagios_force_sync_parser(
                shelve_name, file_name, updated_dict, attribute)
            if rt['success'] == 1:
                return JSONEncoder().encode(rt)
                # host template code
            dt = load_configuration(['host_templates.cfg'])
            hosttemplate_result = load_db_by_name('hosttemplate')
            hosttemplate_db = hostgroup_config
            if hosttemplate_result['success'] == 0:
                hosttemplate_config = hosttemplate_result['data']
            else:
                hosttemplate_config = {}
            generic_host = {
                'check_command': 'check-host-alive',
                'check_interval': '1',
                'check_period': '24x7',
                'contact_groups': 'check_mk',
                'event_handler_enabled': '0',
                'flap_detection_enabled': '1',
                'max_check_attempts': '5',
                'name': 'generic-host',
                'notification_interval': '5',
                'notification_options': 'u,r,f',
                'notification_period': '24X7',
                'notifications_enabled': '1',
                'process_perf_data': '1',
                'register': '0'
            }
            if ('generic-host' in hosttemplate_config):
                pass
            else:
                hosttemplate_config['generic-host'] = {
                    'action_url': "/nms2/pnp4nagios/index.php/graph?host=$HOSTNAME$&srv=_HOST_' class='tips' rel='/nms/pnp4nagios/index.php/popup?host=$HOSTNAME$&srv=_HOST_",
                    'check_command': 'check-host-alive',
                    'check_interval': '1',
                    'check_period': '24x7',
                    'contact_groups': 'check_mk',
                    'event_handler_enabled': '0',
                    'flap_detection_enabled': '1',
                    'max_check_attempts': '5',
                    'name': 'generic-host',
                    'notification_interval': '5',
                    'notification_options': 'u,r,f',
                    'notification_period': '24X7',
                    'notifications_enabled': '1',
                    'process_perf_data': '1',
                    'register': '0'
                }
                # hosttemplate_config
                # hosttemplate_db
            default_template_list = [
                'generic-host', 'check_mk_host', 'check_mk_cluster', 'host-pnp',
                'check_mk_default', 'check_mk_host-summary', 'check_mk_cluster-summary']
            for db_hg in hosttemplate_db.keys():
                if db_hg in hosttemplate_config:  # hosttemplate is in .cfg and DB. update name
                    hosttemplate_config[db_hg].update({'name': db_hg})
                else:
                    hosttemplate_config[db_hg] = generic_host.copy(
                    )  # hostgroup is in DB. Add in cfg
                    hosttemplate_config[db_hg]['name'] = db_hg

            for config_hg in hosttemplate_config.keys():
                if config_hg in hosttemplate_db:  # hostgroup is in .cfg and DB. pass
                    pass
                elif (config_hg not in default_template_list):
                    hosttemplate_config.pop(
                        config_hg)  # hostgroup is in .cfg only. remove.

            shelve_name = 'hosttemplate'
            file_name = 'host_template.cfg'
            updated_dict = hosttemplate_config
            attribute = "host"
            rt = nagios_force_sync_parser(
                shelve_name, file_name, updated_dict, attribute)
            if rt['success'] == 1:
                return JSONEncoder().encode(rt)

            # write hosts file
            query = "select h.host_name, h.host_alias, h.ip_address, h_parent.host_name, \
            hg.hostgroup_name from hostgroups as hg \
            join  hosts_hostgroups  as h_hg on h_hg.hostgroup_id= hg.hostgroup_id \
            join hosts as h on h.host_id= h_hg.host_id and h.is_deleted=0 and (not isnull(h.config_profile_id) or h.is_localhost=1) \
            left join hosts as h_parent on h_parent.host_id = h.parent_name"

            hosts_db = {}
            cursor.execute(query)
            hosts_tuple = cursor.fetchall()
            for row in hosts_tuple:
                hosts_db[row[0]] = {'host_name': row[0],
                                    'alias': row[1],
                                    'parents': row[3] if row[3] != None and row[3] != "NULL" else '',
                                    'address': row[2],
                                    'hostgroups': row[4],
                                    'use': row[4] + ",generic-host"
                }

            dt = load_configuration(['hosts.cfg'])
            hosts_result = load_db_by_name('host')
            if hosts_result['success'] == 0:
                hosts_config = hosts_result['data']
            else:
                hosts_config = {}

            for db_hg in hosts_db.keys():
                if db_hg in hosts_config:  # host is in .cfg and DB. update name and alias,etc
                    hosts_config[db_hg].update(hosts_db[db_hg])
                else:
                    hosts_config[db_hg] = hosts_db[
                        db_hg]  # host is in DB. Add in cfg

            for config_hg in hosts_config.keys():
                if config_hg in hosts_db:  # host is in .cfg and DB. pass
                    # pass
                    hosts_config[config_hg].update(hosts_db[config_hg])
                else:
                    hosts_config.pop(
                        config_hg)  # host is in .cfg only. remove.

            shelve_name = 'host'
            file_name = 'hosts.cfg'
            updated_dict = hosts_config
            attribute = "host"
            rt = nagios_force_sync_parser(
                shelve_name, file_name, updated_dict, attribute)
            if rt['success'] == 1:
                return JSONEncoder().encode(rt)

            query = "select h.host_name, hs.normal_check_interval, hs.retry_check_interval, hs.max_check_attempts , hs.service_description, \
 hs.check_command from host_services as hs \
join hosts as h on h.host_id=hs.host_id and h.is_deleted=0 and (not isnull(h.config_profile_id) or h.is_localhost=1) "

            hosts_db = {}
            cursor.execute(query)
            hosts_tuple = cursor.fetchall()
            count = 0
            for row in hosts_tuple:
                hosts_db[count] = {'host_name': row[0],
                                   'use': 'generic-service',
                                   'normal_check_interval': row[1] if row[1] != None and row[1] != "NULL" else '',
                                   'max_check_attempts': row[3] if row[3] != None and row[3] != "NULL" else '',
                                   'retry_check_interval': row[2] if row[2] != None and row[2] != "NULL" else '',
                                   'service_description': row[4] if row[4] != None and row[4] != "NULL" else '',
                                   'check_command': row[5] if row[5] != None and row[5] != "NULL" else '',
                }
                count += 1
            dt = load_configuration(['services.cfg'])
            hosts_result = load_db_by_name('service')
            if hosts_result['success'] == 0:
                hosts_config = hosts_result['data']
            else:
                hosts_config = {}

            hosts_config_dict = {}
            hosts_db_dict = {}
            count_service = 0
            for db_hg in hosts_db.keys():
                hosts_db_dict = hosts_db[db_hg]
                flag_service = 1
                for config_hg in hosts_config.keys():
                    count_service += 1
                    hosts_config_dict = hosts_config[config_hg]
                    if hosts_config_dict.get('host_name', '') == hosts_db_dict.get('host_name',
                                                                                   '0') and hosts_config_dict.get(
                            'service_description', '') == hosts_db_dict.get('service_description', '0'):
                    # if hosts_config.has_key(db_hg):# host is in .cfg and DB.
                    # update name and alias,etc
                        hosts_config[config_hg].update(hosts_db_dict)
                        flag_service = 0
                if flag_service:
                    hosts_config[
                        count_service] = hosts_db_dict  # host is in DB. Add in cfg

                #            for config_hg in hosts_config.keys():
                #                if hosts_db.has_key(config_hg):# host is in .cfg and DB. pass
                #                    pass
                #                else:
                #                    hosts_config.pop(config_hg)# host is in .cfg only. remove.
            host_service_lists = []
            for config_hg in hosts_config.keys():
                hosts_config_dict = hosts_config[config_hg]
                flag_service = 0
                temp_tuple = (hosts_config_dict.get(
                    'host_name', ''), hosts_config_dict.get('service_description', ''))
                for db_hg in hosts_db.keys():
                    count_service += 1
                    hosts_db_dict = hosts_db[db_hg]
                    # if hosts_config_dict.get('host_name','') == hosts_db_dict.get('host_name','0') and hosts_config_dict.get('service_description','') == hosts_db_dict.get('service_description','0'):
                # if hosts_config.has_key(db_hg):# host is in .cfg and DB. update name and alias,etc
                #    flag_service = 0
                if flag_service or temp_tuple in host_service_lists:
                    hosts_config.pop(config_hg)  # host is in DB. Add in cfg
                else:
                    host_service_lists.append(temp_tuple)
            shelve_name = 'service'
            file_name = 'services.cfg'
            updated_dict = hosts_config
            attribute = "service"
            rt = nagios_force_sync_parser(
                shelve_name, file_name, updated_dict, attribute)
            if rt['success'] == 1:
                return rt
            cursor.close()
            db.close()
            output = {
                "success": 0
            }
            return JSONEncoder().encode(output)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # Function for fetching information related to a hostgroup through inventory
    # like getting host template details when user clicks on a hostgroup
    # then we fetch details of the respective host template.
    def get_nagios_hostgroup_inventory(self, hostgroup_name):
        """

        @param hostgroup_name:
        @return:
        """
        try:
            host_result = {}
            host_result["options"] = {}
            host_result["data"] = {}
            hg_list = []
            attribute = "hosttemplate"
            host_template_name = hostgroup_name
            dt = load_configuration(['host_template.cfg'])
            # load_db_by_name(attribute)#get_attribute_by_name(service_description,
            # attribute)
            service_result = load_db_by_name(attribute)
            if (service_result["success"] == 0):
                service_details = service_result["data"]
            else:
                service_details = {}
            host_result = {}
            if host_template_name != None and host_template_name in service_result["data"]:
                host_result["data"] = service_result[
                    "data"][host_template_name]
            elif host_template_name == None:
                host_result["data"] = {}
            else:
                # output = {"success":1,"exception":host_template_name+" not found."}
                # return JSONEncoder().encode(output)
                host_result["data"] = {}
                pass

            host_result["options"] = {}
            file_name_list = ["timeperiod.cfg", "commands.cfg",
                              "hostgroups.cfg", "hosts.cfg", "contactgroup.cfg", "contacts.cfg"]
            corresponding_dict = ["timeperiod", "check_command",
                                  "hostgroups", "parents", "contactgroup", "contacts"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                    #                        if file_name=="host_template.cfg":
                    #                            if host_template_name!=load_result["data"][key]["name"]:
                    # hosttemplate_list.append([load_result["data"][key]["name"],load_result["data"][key]["name"]])
                        if file_name == "hosts.cfg":
                            hosttemplate_list.append([load_result["data"][key][
                                                          "host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            file_name_list = ["timeperiod.cfg", "commands.cfg",
                              "contactgroup.cfg"]
            corresponding_dict = ["timeperiod",
                                  "check_command", "contactgroup"]

            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            if hostgroup_name != load_result["data"][key]["host_name"]:
                                hosttemplate_list.append([load_result["data"][
                                                              key]["host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            # host_result["options"]["notification_options"]=[["w","w (WARNING)"],["c","c (CRITICAL)"],["u","u (UNKNOWN)"],["r","r (OK)"],["f","f (FLAPPING)"],["s","s (SCHEDULED)"]]
            # host_result["options"]["notification_options"]=[["d","d
            # (DOWN)"],["u","u (UP)"],["r","r (RECOVERY)"],["f","f
            # (FLAPPING)"],["s","s (SCHEDULED DOWNTIME)"],["n","n (NONE)"]]
            host_result["options"]["notification_options"] = [["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"],
                                                              ["r", "r (RECOVERY/OK)"], ["f",
                                                                                         "f (FLAPPING)"],
                                                              ["s", "s (SCHEDULED)"], ["n", "n (NONE)"]]
            host_result["options"]["notifications_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["initial_state"] = [["o",
                                                        "o (OK)"], ["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"]]
            host_result["options"]["active_checks_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["passive_checks_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["check_freshness"] = [["0",
                                                          "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["process_perf_data"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["flap_detection_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            # host_result["options"]["flap_detection_options"]=[["o","o
            # (OK)"],["u","u (UNREACHABLE)"]]#[["o","o (OK)"],["w","w
            # (WARNING)"],["c","c (CRITICAL)"],["u","u (UNREACHABLE)"]]
            host_result["options"]["flap_detection_options"] = [["o",
                                                                 "o (UP/OK)"], ["d", "d (DOWN)"],
                                                                ["u", "u (UNREACHABLE)"]]
            host_result["options"]["event_handler_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["success"] = 0
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # Function to save the details of a hostgroup through inventory
    def save_nagios_edit_hostgroup_inventory(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:
            attribute_data = {}
            unique_name = req_vars.get("hostgroup_name", "")
            members = req_vars.get("members", "")
            d = load_configuration(['host_template.cfg', 'hostgroups.cfg'])
            var_list = [
                "action_url", "active_checks_enabled", "address", "alias", "check_command", "check_freshness",
                "check_interval",
                "check_period", "contact_groups", "contacts", "event_handler", "event_handler_enabled",
                "first_notification_delay",
                "flap_detection_enabled", "flap_detection_options", "freshness_threshold", "high_flap_threshold",
                "host_name", "hostgroups",
                "initial_state", "low_flap_threshold", "max_check_attempts", "notes", "notes_url",
                "notification_interval", "notification_options",
                "notification_period", "notifications_enabled", "parents", "passive_checks_enabled",
                "process_performance_data", "retry_interval", "use", "process_perf_data"]
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            attribute_data['name'] = unique_name
            attribute_data['register'] = 0
            attribute_data['use'] = 'generic-host'
            attribute = "hosttemplate"
            hostgroup_name_list = []
            template_name = unique_name
            write_result = set_attribute_by_name_to_shelve(
                attribute_data, "hosttemplate", template_name)
            comment = "hostgroup %s updated at time : %s ." % (
                unique_name, str(datetime.now())[:22])
            file_name = "host_template.cfg"
            write_cfg_result = write_configuration_file(file_name, comment)
            return JSONEncoder().encode(write_cfg_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # Function for fetching information related to a service through inventory
    def get_advanced_host_settings_nagios(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select service_description,max_check_attempts,normal_check_interval,retry_check_interval from host_services where host_id='%s' " % (
                host_id)
            cursor.execute(query)
            result = cursor.fetchall()
            service_dict = {}
            if result:
                for row in result:
                    if row[0].lower().find('snmp uptime') != -1:
                        service_dict['snmp_uptime'] = [row[1], row[2], row[3]]
                    elif row[0].lower().find('statistics service') != -1 or row[0].lower().find(
                            'statictics service') != -1:
                        service_dict[
                            'statistics_service'] = [row[1], row[2], row[3]]
            cursor.close()
            db.close()
            # output = {"success":0,service_dict}
            return service_dict
        except Exception, e:
            output = {"success": 1, "result": str(e)}
            return output

    # Function for fetching information related to a host ie host_name
    def get_host_name_from_host_id(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select host_name from hosts where host_id='%s' " % (
                host_id)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result[0][0]
        except Exception, e:
            return str(e)

    #  Function to fetch information related to a host and hostgroup
    def get_hostgroup_name_from_host_id(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select hostgroup_name from hostgroups as hg\
            join (select host_id,hostgroup_id from hosts_hostgroups ) as h_hg on h_hg.hostgroup_id= hg.hostgroup_id \
             and h_hg.host_id = %s" % (host_id)
            cursor.execute(query)
            hostgroup_name_list = cursor.fetchall()
            cursor.close()
            db.close()
            return hostgroup_name_list[0][0]
        except Exception, e:
            return str(e)

    # Function to fetch hostgroup information from a host_name
    def get_hostgroup_name_from_host_name(self, host_name):
        """

        @param host_name:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select hostgroup_name from hostgroups as hg\
            join (select host_id,host_name from hosts) as h on h.host_name='%s'\
            join (select host_id,hostgroup_id from hosts_hostgroups ) as h_hg on h_hg.hostgroup_id= hg.hostgroup_id \
             and h_hg.host_id = h.host_id " % (host_name)
            cursor.execute(query)
            hostgroup_name_list = cursor.fetchall()
            cursor.close()
            db.close()
            return hostgroup_name_list[0][0]
        except Exception, e:
            return ""

    # Function to get parent name from host name
    def get_parent_name_from_host_name(self, host_name):
        """

        @param host_name:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select hp.host_name from hosts as hp\
            join (select host_id,host_name,parent_name from hosts) as h on h.host_name='%s'\
             and hp.host_id = h.parent_name " % (host_name)
            cursor.execute(query)
            hostgroup_name_list = cursor.fetchall()
            cursor.close()
            db.close()
            return hostgroup_name_list[0][0]
        except Exception, e:
            return ""

    # Function to get hostgroup name from hostgroup_id
    def get_hostgroup_name_from_hostgroup_id(self, hostgroup_id):
        """

        @param hostgroup_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select hostgroup_name from hostgroups where hostgroup_id='%s' " % (
                hostgroup_id)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result[0][0]
        except Exception, e:
            return str(e)

    # Function to save settings related to service.
    def apply_advanced_host_settings_nagios(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            # not used currently
            load_result = load_configuration(['services.cfg'])
            host_id = req_vars.get("host_id", "")
            # snmp uptime
            max_check_attempts_snmp_uptime = req_vars.get(
                "max_check_attempts_snmp_uptime", "")
            check_interval_snmp_uptime = req_vars.get(
                "check_interval_snmp_uptime", "")
            retry_interval_snmp_uptime = req_vars.get(
                "retry_interval_snmp_uptime", "")
            # statistics service
            max_check_attempts_statistics_service = req_vars.get(
                "max_check_attempts_statistics_service", "")
            check_interval_statistics_service = req_vars.get(
                "check_interval_statistics_service", "")
            retry_interval_statistics_service = req_vars.get(
                "retry_interval_statistics_service", "")

            if (host_id != ""):
                db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
                cursor = db.cursor()

                query_list = ["update host_services set  "]
                # snmp uptime
                if max_check_attempts_snmp_uptime != "":
                    query_list.append("max_check_attempts = '%s' , " %
                                      (max_check_attempts_snmp_uptime))
                if check_interval_snmp_uptime != "":
                    query_list.append(
                        "normal_check_interval = '%s' , " % (check_interval_snmp_uptime))
                if retry_interval_snmp_uptime != "":
                    query_list.append("retry_check_interval = '%s' , " %
                                      (retry_interval_snmp_uptime))

                if query_list != ["update host_services set  "]:
                    query = ''.join(query_list)[:-2] + \
                            " where host_id='%s' and service_description like 'snmp uptime%%' " % host_id
                    cursor.execute(query)
                    db.commit()

                query_list = ["update host_services set  "]
                # statistics service
                if max_check_attempts_statistics_service != "":
                    query_list.append("max_check_attempts = '%s' , " % (
                        max_check_attempts_statistics_service))
                if check_interval_statistics_service != "":
                    query_list.append("normal_check_interval = '%s' , " % (
                        check_interval_statistics_service))
                if retry_interval_statistics_service != "":
                    query_list.append("retry_check_interval = '%s' , " % (
                        retry_interval_statistics_service))

                if query_list != ["update host_services set  "]:
                    query = ''.join(query_list)[
                            :-2] + " where host_id='%s' and (service_description like 'statistics service%%' or service_description like 'statictics service%%' )" % host_id
                    cursor.execute(query)
                    db.commit()

                cursor.close()
                db.close()
            output = {"success": 0, "result": ""}
            return JSONEncoder().encode(output)
        except Exception, e:
            output = {"success": 1, "result": str(e)}
            return JSONEncoder().encode(output)

    ##############################################################################################################################
    #################################### Nagios BLL functions start

    # Common Function to get pagination data of different data tables of view
    def get_pagination_data(self, dict_name="", list_files=[], a_columns=[], req_vars={}, extra_dict=[], host_index=-1,
                            hostgroup_index=-1):
        """

        @param dict_name:
        @param list_files:
        @param a_columns:
        @param req_vars:
        @param extra_dict:
        @param host_index:
        @param hostgroup_index:
        @return:
        """
        try:
            start_index = 0
            end_index = 0
            # list_files=['hosts.cfg']
            flag_modified = 0
            flag_load = 0
            ########## check if the file has been modified since last read
            write_result = {"success": 1, "data": 0}
            write_result2 = {"success": 1, "data": 0}
            for file_name in list_files:
                modified_result = check_files_if_modified(
                    file_name)  # file_name = file_name,is_cfg=1
                # modified_result["success"] ==0 means that files are not
                # modified
                if modified_result["success"] == 1:
                    flag_modified = 1
                    break
            if flag_modified == 0:
                for file_name in list_files:
                    write_result = load_db_by_name(file_name, 1)
                    if write_result["success"] == 1:
                        flag_load = 1
                        break
            if eval(dict_name) == {}:
                flag_load = 1
            for extra_dict_name in extra_dict:
                if eval(extra_dict_name) == {}:
                    flag_load = 1
                    break
            if flag_modified or flag_load:
                eval(dict_name).clear()
                write_result2 = load_configuration(list_files)

            if write_result["success"] == 0 or write_result2["success"] == 0:
                # return host
                pass
            else:
                output = {
                    "sEcho": 1,
                    "iTotalRecords": 0,
                    "iTotalDisplayRecords": 0,
                    "aaData": [],
                    "exception": str(write_result["data"]) + "," + str(write_result2["data"])
                }
                return JSONEncoder().encode(output)
                ################### End check file if modified
            result_list = []
            dict_data = eval(dict_name)
            for host_var in dict_data:
                host_dict = dict_data[host_var]
                li = []
                if dict_name == "hostdependency" or dict_name == "servicedependency" or dict_name == "service":
                    li.append(host_var)
                for col in a_columns:
                    if col in host_dict:
                        li.append(host_dict[col])
                    else:
                        li.append("-")
                result_list.append(li)
            if hostgroup_index != -1 and host_index != -1:          # code for hostgroup
                for row in range(len(result_list)):
                    unique_name = result_list[row][hostgroup_index]
                    host_name_list = [i.strip(
                    ) for i in result_list[row][host_index].split(',')]
                    host_aliases = ""
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                    load_result = load_return_attribute("hosts.cfg")
                    assigned_hosts = ""
                    already_members = host_name_list
                    if load_result["success"] == 0:
                        for key in load_result["data"]:
                            if "hostgroups" in load_result["data"][key]:
                                host_hostgroup = load_result[
                                    "data"][key]["hostgroups"]
                                if host_hostgroup == unique_name and load_result["data"][key][
                                    "host_name"] not in already_members:
                                    assigned_hosts += load_result[
                                                          "data"][key]["alias"] + ", "

                    if assigned_hosts != "":
                        if host_aliases != "":
                            host_aliases += assigned_hosts
                        else:
                            host_aliases = assigned_hosts
                    result_list[row][host_index] = host_aliases[:-2]

            elif host_index != -1:                        # code for hosts
                for row in range(len(result_list)):
                    host_name_list = result_list[row][host_index].split(",")
                    host_aliases = ""
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        # f.close()
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                            # unique_name+=host_name+","
                    result_list[row][host_index] = host_aliases[:-2]

            i_display_start = int(req_vars.get("iDisplayStart", 0))
            i_display_length = i_display_start + int(
                req_vars.get("iDisplayLength", 0))
            i_sort_col_0 = req_vars.get("iSortCol_0", 0)
            s_search = req_vars.get("sSearch", None)
            sSortDir_0 = req_vars.get("sSortDir_0", "asc")
            sEcho = req_vars.get("sEcho", 1)
            i_total = len(result_list)
            # function for searching the value in result
            if (str(s_search) != "" and s_search != None and s_search != "Null"):
                result_search = []
                for row in result_list:
                    for data in row:
                        if str(data).find(s_search) != -1:
                            result_search.append(row)
                            break
                result_list = result_search
            if (str(sSortDir_0) == "asc"):
                result_list = sorted(result_list, key=lambda result_list:
                result_list[int(i_sort_col_0)], reverse=False)
            else:
                result_list = sorted(result_list, key=lambda result_list:
                result_list[int(i_sort_col_0)], reverse=True)
            i_filtered_total = len(result_list)
            output = {
                "sEcho": sEcho,
                "iTotalRecords": i_total,
                "iTotalDisplayRecords": i_filtered_total,
                "aaData": result_list[i_display_start:i_display_length],
                "flag_load": flag_load,
                "flag_modified": flag_modified,
                "modified_result": str(modified_result)
            }
            return output
            # return JSONEncoder().encode(output)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return output
            # return JSONEncoder().encode(output)

    ################# Host Data table function starts now

    def get_log_data(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            # a_columns = columns of data table
            # list_files = files to be loaded for this data table
            # parent_host_index = parent index of any host in data table
            # unique_index =  index of unique value in data table ie host_name
            a_columns = ["host_name", "alias", "address",
                         "parents", "hostgroups"]
            list_files = ['hosts.cfg']
            parent_host_index = 3
            # get the data table result
            host_result = self.get_pagination_data(
                "host", list_files, a_columns, req_vars)
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            if "exception" not in host_result:
                for row in range(len(aaData)):
                    parent_name = aaData[row][parent_host_index]
                    # get parent information
                    parent_info = get_attribute_by_name(parent_name, 'host')
                    if parent_info["success"] == 0:
                        aaData[row][
                            parent_host_index] = parent_info["data"]["alias"]
                    aaData[row].append("<a href=\"javascript:editHost('%s',%s);\"><img class='host_opr' \
                     title='Edit Host Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    aaData[row][unique_index], self.localhost_list.count(aaData[row][unique_index])))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # fetch nagios details by host_name
    def get_nagios_host_by_name(self, host_name):
        """

        @param host_name:
        @return:
        """
        try:
            attribute = "host"
            # load hosts.cfg
            load_result = load_configuration(['hosts.cfg'])
            # get the host information
            host_result = get_attribute_by_name(host_name, attribute)

            # declare a dict "options" which will contain all options of the
            # nagios fields
            host_result["options"] = {}

            if "parents" in host_result["data"]:
                parent_name = host_result["data"]["parents"]
                parent_info = get_attribute_by_name(parent_name, 'host')
                if parent_info["success"] == 0:
                    host_result["data"][
                        "parents"] = parent_info["data"]["alias"]

            # load options of various files and nagios fields
            file_name_list = [
                "host_template.cfg", "timeperiod.cfg", "commands.cfg",
                "hostgroups.cfg", "hosts.cfg", "contactgroup.cfg", "contacts.cfg"]
            corresponding_dict = ["use", "timeperiod", "check_command",
                                  "hostgroups", "parents", "contactgroup", "contacts"]

            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                # load the attribute in load_result['data']
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            if host_name != load_result["data"][key]["host_name"]:
                                hosttemplate_list.append([load_result["data"][
                                                              key]["host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                    # fill the options dict here
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            # fill other options which are never changing in nagios
            # host_result["options"]["notification_options"]=[["w","w (WARNING)"],["c","c (CRITICAL)"],["u","u (UNKNOWN)"],["r","r (OK)"],["f","f (FLAPPING)"],["s","s (SCHEDULED)"]]
            # host_result["options"]["notification_options"]=[["d","d"],["u","u"],["r","r"],["f","f"],["s","s"]]
            host_result["options"]["notification_options"] = [["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"],
                                                              ["r", "r (RECOVERY/OK)"],
                                                              ["f", "f (FLAPPING)"], ["s", "s (SCHEDULED)"],
                                                              ["n", "n (NONE)"]]
            host_result["options"]["notifications_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["initial_state"] = [["o",
                                                        "o (OK)"], ["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"]]
            host_result["options"]["active_checks_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["passive_checks_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["check_freshness"] = [["0",
                                                          "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["process_perf_data"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["flap_detection_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            # host_result["options"]["flap_detection_options"]=[["o","o
            # (OK)"],["u","u (UNREACHABLE)"]]#[["o","o (OK)"],["w","w
            # (WARNING)"],["c","c (CRITICAL)"],["u","u (UNREACHABLE)"]]
            host_result["options"]["flap_detection_options"] = [["o",
                                                                 "o (UP/OK)"], ["d", "d (DOWN)"],
                                                                ["u", "u (UNREACHABLE)"]]
            host_result["options"]["event_handler_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            return host_result
            # return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save nagios host details
    def save_nagios_edit_host(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:
            # load hosts.cfg
            load_result = load_configuration(['hosts.cfg'])
            # var_list is the list containing all options of nagios hosts
            var_list = [
                "action_url", "active_checks_enabled", "address", "alias", "check_command", "check_freshness",
                "check_interval",
                "check_period", "contact_groups", "contacts", "event_handler", "event_handler_enabled",
                "first_notification_delay",
                "flap_detection_enabled", "flap_detection_options", "freshness_threshold", "high_flap_threshold",
                "host_name", "hostgroups",
                "initial_state", "low_flap_threshold", "max_check_attempts", "notes", "notes_url",
                "notification_interval", "notification_options",
                "notification_period", "notifications_enabled", "parents", "passive_checks_enabled",
                "process_performance_data", "retry_interval", "use", "process_perf_data"]

            # attribute_data will contain the various options present in the
            # request sent for saving
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("host_name", "")
            old_host_alias = req_vars.get("old_host_alias", "")
            old_ip_address = req_vars.get("old_ip_address", "")
            old_hostgroup = req_vars.get("old_hostgroup", "")

            attribute = "host"
            hostgroup_name_list = []
            use = attribute_data['use']

            # check for circular host relationship
            if "parents" in attribute_data:
                es = Essential()
                parent_id = 1
                child_id = 1
                parent_name = attribute_data["parents"]
                child_name = attribute_data.get("host_name", "")
                db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
                cursor = db.cursor()
                # write hostgroups file
                query = "select host_id,host_name from hosts where host_name in ('%s','%s')" % (
                    parent_name, child_name)
                hosts_id_db = {}
                cursor.execute(query)
                hosts_id_tuple = cursor.fetchall()
                for row in hosts_id_tuple:
                    if parent_name == row[1]:
                        parent_id = row[0]
                    elif child_name == row[1]:
                        child_id = row[0]
                cursor.close()
                db.close()
                circular_check_result = es.circular_check(child_id, parent_id)
                if circular_check_result['success'] == 0:
                    pass
                else:
                    output = {
                        "success": 1,
                        "exception": "Circular reference detected for host %s " % (attribute_data['alias'])
                    }
                    return JSONEncoder().encode(output)

            # if hostgroups is present to be saved
            if "hostgroups" in attribute_data:
                hostgroup_name_list = [i.strip(
                ) for i in attribute_data["hostgroups"].split(',')]
                if attribute_data['hostgroups'] == '':
                    attribute_data[
                        'hostgroups'] = self.get_hostgroup_name_from_host_name(unique_name)
            else:
                attribute_data[
                    'hostgroups'] = self.get_hostgroup_name_from_host_name(unique_name)
            if "parents" in attribute_data:
                hostgroup_name_list = [i.strip(
                ) for i in attribute_data["parents"].split(',')]
                if attribute_data['parents'] == '':
                    attribute_data['parents'] = self.get_parent_name_from_host_name(
                        unique_name)
            else:
                attribute_data[
                    'parents'] = self.get_parent_name_from_host_name(unique_name)
            template_result = get_attribute_by_name(
                attribute_data["hostgroups"], 'hosttemplate')
            if (template_result)['success'] == 1:
                # append new hostgroup template to host_templates.cfg
                rt = self.add_new_host_template_hostgroup(
                    attribute_data["hostgroups"], True)
                if rt['success'] == 0:
                    use_li = use.split(',')
                    use_li = list(set(use_li))
                    use_index = use_li.index(
                        old_hostgroup) if use_li.count(old_hostgroup) else -1
                    if use_index != -1:
                        use_li.remove(old_hostgroup)
                    use_li.insert(0, attribute_data["hostgroups"])
                    use = ','.join(use_li)
            else:
                use_li = use.split(',')
                use_li = list(set(use_li))
                use_index = use_li.index(
                    old_hostgroup) if use_li.count(old_hostgroup) else -1
                if use_index != -1:
                    use_li.remove(old_hostgroup)
                use_li.insert(0, attribute_data["hostgroups"])

                use = ','.join(use_li)
                # use = attribute_data["hostgroups"] + "," + use
            attribute_data['use'] = use
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)
            all_hostgroups = load_return_attribute("hostgroups.cfg")
            if all_hostgroups["success"] == 0:
                hostgroup_data = all_hostgroups["data"]
                for key in hostgroup_data:
                    if hostgroup_data[key]["hostgroup_name"] not in hostgroup_name_list:
                        if "members" in hostgroup_data[key]:
                            old_members = hostgroup_data[key]["members"]
                            members_list = [
                                i.strip() for i in old_members.split(',')]
                            flag = 0
                            if unique_name in members_list:
                                members_list.remove(unique_name)
                                set_attribute_by_name_to_shelve(
                                    {"members": ",".join(members_list)}, "hostgroup",
                                    hostgroup_data[key]["hostgroup_name"])

            if write_result["success"] == 0:
                comment = "host %s updated at time : %s ." % (
                    attribute_data["alias"], str(datetime.now())[:22])
                file_name = "hosts.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                comment = "hostgroups updated due to changes in hosts %s at time : %s " % (
                    attribute_data["alias"], str(datetime.now())[:22])
                file_name = "hostgroups.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
            else:
                return JSONEncoder().encode(write_result)
            query = ""
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            if "hostgroups" in attribute_data and attribute_data["hostgroups"] != "" and attribute_data[
                "hostgroups"] != old_hostgroup:
                query = "update hosts_hostgroups set hostgroup_id=(select hostgroup_id from hostgroups where hostgroup_name='%s')\
            where host_id=(select host_id from hosts where host_name='%s')" % (
                attribute_data["hostgroups"], unique_name)
                cursor.execute(query)
                # new_host_dict={"host_name":unique_name,"alias":alias,"address":address,"use":use,"parents":parent_name,"hostgroups":hostgroup_id}
                # result = edit_for_inventory_object(host_name, file_name,
                # attribute, dict_name, new_host_dict, comment)
            if old_host_alias != attribute_data["alias"] and attribute_data["alias"] != "":
                query = "update hosts set host_alias='%s' where host_name='%s'" % (
                    attribute_data["alias"], unique_name)
                cursor.execute(query)
            if "parents" in attribute_data and attribute_data["parents"] != "":
                query = "update hosts as h left join hosts as hp on hp.host_name='%s'\
                set h.parent_name=hp.host_id where h.host_name='%s'" % (attribute_data["parents"], unique_name)
                cursor.execute(query)
            if query != "":
                db.commit()

            cursor.close()
            db.close()
            return JSONEncoder().encode(write_cfg_result)

        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    ########## end host

    #################### host template code
    # fetch host template details for data table
    def get_log_data_host_template(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            # a_columns = columns of data table
            # list_files = files to be loaded for this data table
            # parent_host_index = parents index of any host in data table
            # unique_index =  index of unique value in data table ie host_name

            a_columns = ["name", "notification_interval",
                         "max_check_attempts", "check_command"]
            list_files = ['host_template.cfg']
            parent_host_index = 0
            host_result = self.get_pagination_data(
                "hosttemplate", list_files, a_columns, req_vars)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            if "exception" not in host_result:
                for row in range(len(aaData)):
                #                    parent_name = aaData[row][parent_host_index]
                #                    parent_info = get_attribute_by_name(parent_name,'host')
                #                    if parent_info["success"]==0:
                # aaData[row][parent_host_index] = parent_info["data"]["alias"]
                    aaData[row].append("<a href=\"javascript:editHostTemplate('%s');\"><img class='host_opr' \
                     title='Edit Host Template' src='images/new/edit.png' alt='edit'/></a>" % (
                    aaData[row][unique_index]))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # Fetch host template details
    def get_nagios_host_template_by_name(self, host_template_name):
        """

        @param host_template_name:
        @return:
        """
        try:
            attribute = "hosttemplate"
            load_result = load_configuration(['host_template.cfg'])
            service_result = load_db_by_name(
                attribute)  # get_attribute_by_name(service_description, attribute)
            if (service_result["success"] == 0):
                service_details = service_result["data"]
            else:
                service_details = {}
            host_result = {}
            if host_template_name != None and host_template_name in service_result["data"]:
                host_result["data"] = service_result[
                    "data"][host_template_name]
            elif host_template_name == None:
                host_result["data"] = {}
            else:
                output = {"success": 1, "exception":
                    host_template_name + " not found."}
                return JSONEncoder().encode(output)

            #            host_result=get_attribute_by_name(host_template_name, attribute)
            host_result["options"] = {}
            if "parents" in host_result["data"]:
                parent_name = host_result["data"]["parents"]
                parent_info = get_attribute_by_name(parent_name, 'host')
                if parent_info["success"] == 0:
                    host_result["data"][
                        "parents"] = parent_info["data"]["alias"]

            file_name_list = [
                "host_template.cfg", "timeperiod.cfg", "commands.cfg",
                "hostgroups.cfg", "hosts.cfg", "contactgroup.cfg", "contacts.cfg"]
            corresponding_dict = ["use", "timeperiod", "check_command",
                                  "hostgroups", "parents", "contactgroup", "contacts"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "host_template.cfg":
                            if host_template_name != load_result["data"][key]["name"]:
                                hosttemplate_list.append(
                                    [load_result["data"][key]["name"], load_result["data"][key]["name"]])
                        elif file_name == "hosts.cfg":
                            hosttemplate_list.append([load_result["data"][key][
                                                          "host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            # host_result["options"]["notification_options"]=[["w","w (WARNING)"],["c","c (CRITICAL)"],["u","u (UNKNOWN)"],["r","r (OK)"],["f","f (FLAPPING)"],["s","s (SCHEDULED)"]]
            # host_result["options"]["notification_options"]=[["d","d"],["u","u"],["r","r"],["f","f"],["s","s"]]
            host_result["options"]["notification_options"] = [["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"],
                                                              ["r", "r (RECOVERY/OK)"], ["f",
                                                                                         "f (FLAPPING)"],
                                                              ["s", "s (SCHEDULED)"], ["n", "n (NONE)"]]
            host_result["options"]["notifications_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["initial_state"] = [["o",
                                                        "o (OK)"], ["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"]]
            host_result["options"]["active_checks_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["passive_checks_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["check_freshness"] = [["0",
                                                          "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["process_perf_data"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["flap_detection_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            # host_result["options"]["flap_detection_options"]=[["o","o
            # (OK)"],["u","u (UNREACHABLE)"]]#[["o","o (OK)"],["w","w
            # (WARNING)"],["c","c (CRITICAL)"],["u","u (UNREACHABLE)"]]
            host_result["options"]["flap_detection_options"] = [["o",
                                                                 "o (UP/OK)"], ["d", "d (DOWN)"],
                                                                ["u", "u (UNREACHABLE)"]]
            host_result["options"]["event_handler_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["register"] = [["0", "0"], ["1", "1"]]
            host_result["success"] = 0
            return host_result
            # return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save host_template details
    def save_nagios_edit_host_template(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            var_list = [
                "action_url", "active_checks_enabled", "check_command", "check_freshness", "check_interval",
                "check_period", "contact_groups", "contacts", "event_handler", "event_handler_enabled",
                "first_notification_delay",
                "flap_detection_enabled", "flap_detection_options", "freshness_threshold", "high_flap_threshold",
                "hostgroups",
                "initial_state", "low_flap_threshold", "max_check_attempts", "name", "notes", "notes_url",
                "notification_interval", "notification_options",
                "notification_period", "notifications_enabled", "parents", "passive_checks_enabled",
                "process_performance_data", "register", "retry_interval", "use", "process_perf_data"]
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("name", "")
            old_host_template_name = req_vars.get("old_host_template_name", "")
            attribute = "hosttemplate"
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)

            if write_result["success"] == 0:
                comment = "host template %s updated at time : %s ." % (
                    attribute_data["name"], str(datetime.now())[:22])
                file_name = "host_template.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # function to delete nagios host templates
    def nagios_delete_host_template(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:
            load_result = load_configuration(['host_template.cfg'])
            unique_names_li = req_vars.get(
                "host_template_names", '').split(',')
            attribute = "hosttemplate"
            unique_names_str = ", ".join(unique_names_li)
            for unique_name in unique_names_li:
                write_result = delete_attribute_by_name_from_shelve(
                    attribute, unique_name)

            if write_result["success"] == 0:
                comment = "host_template(s) %s deleted at time : %s ." % (
                    unique_names_str, str(datetime.now())[:22])
                file_name = "host_template.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)

                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

        ######################### host template ends
    ############### service starts

    def get_log_data_service(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            a_columns = ["service_description", "use",
                         "host_name", "normal_check_interval"]
            list_files = ['services.cfg', 'hosts.cfg']
            host_index = 3

            host_result = self.get_pagination_data(
                "service", list_files, a_columns, req_vars, {}, host_index)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            service_index = 1

            if "exception" not in host_result:
                for row in range(len(aaData)):
                    # unique_name = aaData[row][service_index] +
                    # (aaData[row][host_index] if aaData[row][host_index]!="-"
                    # else "")
                    unique_name = aaData[row][unique_index]
                    aaData[row].append("<a href=\"javascript:editService('%s');\"><img class='host_opr' \
                     title='Edit Service Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    unique_name))  # aaData[row][unique_index]))

            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # Fetch service details
    def get_nagios_service_by_name(self, service_description):
        """

        @param service_description:
        @return:
        """
        try:
            attribute = "service"
            load_result = load_configuration(['services.cfg'])
            service_result = load_db_by_name(
                attribute)  # get_attribute_by_name(service_description, attribute)
            if (service_result["success"] == 0):
                service_details = service_result["data"]
            else:
                service_details = {}
            host_result = {}
            #            if service_result["data"].has_key(service_description):
            #                host_result["data"] = service_result["data"][service_description]
            #            else:
            #                output = {"success":1,"exception":service_description+" not found."}
            #                return JSONEncoder().encode(output)
            #

            if service_description != None and service_description in service_result["data"]:
                host_result["data"] = service_result[
                    "data"][service_description]
            elif service_description == None:
                host_result["data"] = {}
            else:
                output = {"success": 1, "exception":
                    service_description + " not found."}
                return JSONEncoder().encode(output)

            host_result["options"] = {}
            file_name_list = [
                "service_template.cfg", "timeperiod.cfg", "commands.cfg",
                "hostgroups.cfg", "contactgroup.cfg", "hosts.cfg", "contacts.cfg"]
            corresponding_dict = ["use", "timeperiod", "check_command",
                                  "hostgroups", "contactgroup", "host_name", "contacts"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            hosttemplate_list.append([load_result["data"][key][
                                                          "host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            # host_result["options"]["notification_options"]=[["w","w (WARNING)"],["c","c (CRITICAL)"],["u","u (UNKNOWN)"],["r","r (OK)"],["f","f (FLAPPING)"],["s","s (SCHEDULED)"]]
            # host_result["options"]["notification_options"]=[["d","d"],["u","u"],["r","r"],["f","f"],["s","s"]]
            host_result["options"]["notification_options"] = [["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"],
                                                              ["r", "r (RECOVERY/OK)"], ["f",
                                                                                         "f (FLAPPING)"],
                                                              ["s", "s (SCHEDULED)"], ["n", "n (NONE)"]]
            host_result["options"]["notifications_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["initial_state"] = [["o",
                                                        "o (OK)"], ["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"]]
            host_result["options"]["active_checks_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["passive_checks_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["check_freshness"] = [["0",
                                                          "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["process_perf_data"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["flap_detection_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            # host_result["options"]["flap_detection_options"]=[["o","o
            # (OK)"],["u","u (UNREACHABLE)"]]#[["o","o (OK)"],["w","w
            # (WARNING)"],["c","c (CRITICAL)"],["u","u (UNREACHABLE)"]]
            host_result["options"]["flap_detection_options"] = [["o",
                                                                 "o (UP/OK)"], ["d", "d (DOWN)"],
                                                                ["u", "u (UNREACHABLE)"]]
            host_result["options"]["event_handler_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]

            host_result["options"]["parallelize_check"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["failure_prediction_enabled"] = [["0",
                                                                     "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["stalking_options"] = [["o",
                                                           "o (OK)"], ["w", "w (WARNING)"], ["c", "c (CRITICAL)"],
                                                          ["u", "u (UNREACHABLE)"]]
            host_result["options"]["retain_status_information"] = [["0",
                                                                    "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["retain_nonstatus_information"] = [[
                                                                          "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["obsess_over_service"] = [[
                                                                 "0", "0 (Don't obsess)"], ["1", "1 (obsess)"]]
            host_result["options"]["is_volatile"] = [["0",
                                                      "0 (not volatile)"], ["1", "1 (volatile)"]]

            host_result["success"] = 0
            return host_result
            # return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save service details
    def save_nagios_edit_service(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:
            var_list = [
                "action_url", "active_checks_enabled", "check_command", "check_freshness", "check_interval",
                "check_period",
                "contact_groups", "contacts", "display_name", "event_handler", "event_handler_enabled",
                "failure_prediction_enabled",
                "first_notification_delay", "flap_detection_enabled", "flap_detection_options", "freshness_threshold",
                "high_flap_threshold",
                "host_name", "hostgroup_name", "icon_image", "icon_image_alt", "initial_state", "is_volatile",
                "low_flap_threshold",
                "max_check_attempts", "normal_check_interval", "notes", "notes_url", "notification_interval",
                "notification_options",
                "notification_period", "notifications_enabled", "obsess_over_service", "parallelize_check",
                "passive_checks_enabled",
                "process_perf_data", "retain_nonstatus_information", "retain_status_information",
                "retry_check_interval", "retry_interval",
                "service_description", "servicegroups", "stalking_options", "use", ]
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("service_unique_key", "")
            attribute = "service"
            updated = "updated"
            if unique_name == "":
                updated = "added"
                db_result = load_db_by_name(attribute)
                li_host_dependency = []
                for key in db_result['data']:
                    li_host_dependency.append(key)
                if li_host_dependency == []:
                    unique_name = "service1"
                else:
                    li_host_dependency.sort()
                    last_host_dependency = li_host_dependency[-1]
                    unique_name = "service" + str(int(
                        last_host_dependency[len('service'):]) + 1)

            write_result = delete_attribute_by_name_from_shelve(
                attribute, unique_name)
            # unique_name=attribute_data.get("service_description","")+attribute_data.get("host_name","")
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)

            if write_result["success"] == 0:
                comment = "service %s updated at time : %s ." % (
                    attribute_data["service_description"], str(datetime.now())[:22])
                file_name = "services.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)

            ##############################################################
            ## prepare the queries for DB
            # snmp uptime
            max_check_attempts_snmp_uptime = ""
            check_interval_snmp_uptime = ""
            retry_interval_snmp_uptime = ""
            if (attribute_data["service_description"].lower().find('snmp uptime') != -1):
                max_check_attempts_snmp_uptime = attribute_data.get(
                    "max_check_attempts", "")
                check_interval_snmp_uptime = attribute_data.get(
                    "normal_check_interval", "")
                retry_interval_snmp_uptime = attribute_data.get(
                    "retry_check_interval", "")

            # statistics service
            max_check_attempts_statistics_service = ""
            check_interval_statistics_service = ""
            retry_interval_statistics_service = ""
            if ((attribute_data["service_description"].lower().find('statistics service') != -1) or
                    (attribute_data["service_description"].lower().find('statictics service') != -1)):
                max_check_attempts_statistics_service = attribute_data.get(
                    "max_check_attempts", "")
                check_interval_statistics_service = attribute_data.get(
                    "normal_check_interval", "")
                retry_interval_statistics_service = attribute_data.get(
                    "retry_check_interval", "")

            if (attribute_data.get("host_name", "") != ""):
                db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
                cursor = db.cursor()

                query_list = ["update host_services join hosts on hosts.host_id = host_services.host_id \
                 and hosts.host_name = '%s' set  " % (attribute_data.get("host_name", ""))]
                flag_service = 0
                # snmp uptime
                if max_check_attempts_snmp_uptime != "":
                    query_list.append("max_check_attempts = '%s' , " %
                                      (max_check_attempts_snmp_uptime))
                    flag_service = 1
                if check_interval_snmp_uptime != "":
                    query_list.append(
                        "normal_check_interval = '%s' , " % (check_interval_snmp_uptime))
                    flag_service = 1
                if retry_interval_snmp_uptime != "":
                    query_list.append(
                        "retry_check_interval = '%s' , " % (retry_interval_snmp_uptime))
                    flag_service = 1

                if flag_service:
                    query = ''.join(query_list)[:-2] + \
                            " where service_description like 'snmp uptime%%' "
                    cursor.execute(query)
                    db.commit()

                query_list = ["update host_services join hosts on hosts.host_id = host_services.host_id \
                 and hosts.host_name = '%s' set  " % (attribute_data.get("host_name", ""))]
                flag_service = 0
                # snmp uptime
                if max_check_attempts_statistics_service != "":
                    query_list.append("max_check_attempts = '%s' , " % (
                        max_check_attempts_statistics_service))
                    flag_service = 1
                if check_interval_statistics_service != "":
                    query_list.append("normal_check_interval = '%s' , " % (
                        check_interval_statistics_service))
                    flag_service = 1
                if retry_interval_statistics_service != "":
                    query_list.append("retry_check_interval = '%s' , " % (
                        retry_interval_statistics_service))
                    flag_service = 1

                if flag_service:
                    query = ''.join(query_list)[:-2] + " where service_description like 'statistics service%%' or \
                      service_description like 'statictics service%%' "
                    cursor.execute(query)
                    db.commit()

                cursor.close()
                db.close()
                ##############################################################
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # delete service function
    def nagios_delete_service(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:
            try:
                eval('service').clear()
            except:
                pass
            load_result = load_configuration(['services.cfg'])
            unique_names_li = req_vars.get("service_names", '').split(',')
            attribute = "service"
            unique_names_str = ", ".join(unique_names_li)
            for unique_name in unique_names_li:
                write_result = delete_attribute_by_name_from_shelve(
                    attribute, unique_name)

            if write_result["success"] == 0:
                comment = "service(s) %s deleted at time : %s ." % (
                    unique_names_str, str(datetime.now())[:22])
                file_name = "services.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

        ############## service ends

    ############### service template starts
    # fetch the data table for service templates
    def get_log_data_service_template(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            a_columns = ["name", "notification_interval",
                         "max_check_attempts", "check_command"]
            list_files = ['service_template.cfg', 'hosts.cfg']
            # req_vars["iSortCol_0"] =req_vars.get("iSortCol_0",0) if
            # req_vars.get("iSortCol_0",0)!=0 else 1
            host_result = self.get_pagination_data(
                "servicetemplate", list_files, a_columns, req_vars)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name

            if "exception" not in host_result:
                for row in range(len(aaData)):
                    unique_name = aaData[row][unique_index]
                    aaData[row].append("<a href=\"javascript:editServiceTemplate('%s');\"><img class='host_opr' \
                     title='Edit Service Template Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    unique_name))  # aaData[row][unique_index]))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # fetch details of a service template
    def get_nagios_service_template_by_name(self, service_description):
        """

        @param service_description:
        @return:
        """
        try:
            attribute = "servicetemplate"
            load_result = load_configuration(['service_template.cfg'])
            service_result = load_db_by_name(
                attribute)  # get_attribute_by_name(service_description, attribute)
            if (service_result["success"] == 0):
                service_details = service_result["data"]
            else:
                service_details = {}
            host_result = {}
            if service_description != None and service_description in service_result["data"]:
                host_result["data"] = service_result[
                    "data"][service_description]
            elif service_description == None:
                host_result["data"] = {}
            else:
                output = {"success": 1, "exception":
                    service_description + " not found."}
                return JSONEncoder().encode(output)

            host_result["options"] = {}
            file_name_list = [
                "service_template.cfg", "timeperiod.cfg", "commands.cfg",
                "hostgroups.cfg", "contactgroup.cfg", "hosts.cfg", "contacts.cfg"]
            corresponding_dict = ["use", "timeperiod", "check_command",
                                  "hostgroups", "contactgroup", "host_name", "contacts"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            hosttemplate_list.append([load_result["data"][key][
                                                          "host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            # host_result["options"]["notification_options"]=[["w","w (WARNING)"],["c","c (CRITICAL)"],["u","u (UNKNOWN)"],["r","r (OK)"],["f","f (FLAPPING)"],["s","s (SCHEDULED)"]]
            # host_result["options"]["notification_options"]=[["d","d"],["u","u"],["r","r"],["f","f"],["s","s"]]
            host_result["options"]["notification_options"] = [["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"],
                                                              ["r", "r (RECOVERY/OK)"], ["f",
                                                                                         "f (FLAPPING)"],
                                                              ["s", "s (SCHEDULED)"], ["n", "n (NONE)"]]
            host_result["options"]["notifications_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["initial_state"] = [["o",
                                                        "o (OK)"], ["d", "d (DOWN)"], ["u", "u (UNREACHABLE)"]]
            host_result["options"]["active_checks_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["passive_checks_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["check_freshness"] = [["0",
                                                          "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["process_perf_data"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["flap_detection_enabled"] = [["0",
                                                                 "0 (Disable)"], ["1", "1 (Enable)"]]
            # host_result["options"]["flap_detection_options"]=[["o","o
            # (UP/OK)"],["u","u (UNREACHABLE)"]]#[["o","o (OK)"],["w","w
            # (WARNING)"],["c","c (CRITICAL)"],["u","u (UNREACHABLE)"]]
            host_result["options"]["flap_detection_options"] = [["o",
                                                                 "o (UP/OK)"], ["d", "d (DOWN)"],
                                                                ["u", "u (UNREACHABLE)"]]
            host_result["options"]["event_handler_enabled"] = [
                ["0", "0 (Disable)"], ["1", "1 (Enable)"]]

            host_result["options"]["parallelize_check"] = [[
                                                               "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["failure_prediction_enabled"] = [["0",
                                                                     "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["stalking_options"] = [["o",
                                                           "o (OK)"], ["w", "w (WARNING)"], ["c", "c (CRITICAL)"],
                                                          ["u", "u (UNREACHABLE)"]]
            host_result["options"]["retain_status_information"] = [["0",
                                                                    "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["retain_nonstatus_information"] = [[
                                                                          "0", "0 (Disable)"], ["1", "1 (Enable)"]]
            host_result["options"]["obsess_over_service"] = [[
                                                                 "0", "0 (Don't obsess)"], ["1", "1 (obsess)"]]
            host_result["options"]["is_volatile"] = [["0",
                                                      "0 (not volatile)"], ["1", "1 (volatile)"]]
            host_result["options"]["register"] = [["0", "0"], ["1", "1"]]

            host_result["success"] = 0
            return host_result
            # return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save the service templates
    def save_nagios_edit_service_template(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            var_list = [
                "action_url", "active_checks_enabled", "check_command", "check_freshness", "check_interval",
                "check_period",
                "contact_groups", "contacts", "display_name", "event_handler", "event_handler_enabled",
                "failure_prediction_enabled",
                "first_notification_delay", "flap_detection_enabled", "flap_detection_options", "freshness_threshold",
                "high_flap_threshold",
                "host_name", "hostgroup_name", "icon_image", "icon_image_alt", "initial_state", "is_volatile",
                "low_flap_threshold",
                "max_check_attempts", "name", "normal_check_interval", "notes", "notes_url", "notification_interval",
                "notification_options",
                "notification_period", "notifications_enabled", "obsess_over_service", "parallelize_check",
                "passive_checks_enabled",
                "process_perf_data", "register", "retain_nonstatus_information", "retain_status_information",
                "retry_check_interval", "retry_interval",
                "service_description", "servicegroups", "stalking_options", "use", ]
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("name", "")
            attribute = "servicetemplate"
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)
            if write_result["success"] == 0:
                comment = "service template %s updated at time : %s ." % (
                    attribute_data["name"], str(datetime.now())[:22])
                file_name = "service_template.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # delete the service template
    def nagios_delete_service_template(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            unique_names_li = req_vars.get(
                "service_template_names", '').split(',')
            attribute = "servicetemplate"
            unique_names_str = ", ".join(unique_names_li)
            for unique_name in unique_names_li:
                write_result = delete_attribute_by_name_from_shelve(
                    attribute, unique_name)

            if write_result["success"] == 0:
                comment = "service template(s) %s deleted at time : %s ." % (
                    unique_names_str, str(datetime.now())[:22])
                file_name = "service_template.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)

                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

        ############ service template ends

    ################## hostgroup starts
    # fetch the data table of hostgroup
    def get_log_data_hostgroup(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            a_columns = ["hostgroup_name", "alias", "members"]
            list_files = ['hostgroups.cfg', 'hosts.cfg']
            host_index = 2
            hostgroup_index = 0
            host_result = self.get_pagination_data(
                "hostgroup", list_files, a_columns, req_vars,
                {}, host_index, hostgroup_index)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            if "exception" not in host_result:
                for row in range(len(aaData)):
                    unique_name = aaData[row][hostgroup_index]
                    aaData[row].append("<a href=\"javascript:editHostgroup('%s');\"><img class='host_opr' \
                     title='Edit Hostgroup Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    unique_name))  # aaData[row][unique_index]))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # get hostgroup details
    def get_nagios_hostgroup_by_name(self, hostgroup_name):
        """

        @param hostgroup_name:
        @return:
        """
        try:
            attribute = "hostgroup"
            hostgroup_result = load_db_by_name(
                attribute)  # get_attribute_by_name(service_description, attribute)
            if (hostgroup_result["success"] == 0):
                hostgroup_details = hostgroup_result["data"]
            else:
                hostgroup_details = {}
            host_result = {}
            host_result["data"] = hostgroup_result["data"][hostgroup_name]
            load_result = load_return_attribute("hosts.cfg")
            assigned_hosts = ""
            if "members" not in host_result["data"]:
                host_result["data"]["members"] = ""
            already_members = [i.strip() for i in host_result[
                "data"]["members"].split(',')]

            if load_result["success"] == 0:
                for key in load_result["data"]:
                    if "hostgroups" in load_result["data"][key]:
                        host_hostgroup = load_result["data"][key]["hostgroups"]

                        if host_hostgroup == hostgroup_name and load_result["data"][key][
                            "host_name"] not in already_members:
                            assigned_hosts += load_result[
                                                  "data"][key]["host_name"] + ","
            if assigned_hosts != "":
                assigned_hosts = assigned_hosts[:-1]
                if host_result["data"]["members"] != "":
                    host_result["data"]["members"] += "," + assigned_hosts
                else:
                    host_result["data"]["members"] = assigned_hosts
            host_result["options"] = {}
            file_name_list = ["host_template.cfg",
                              "hostgroups.cfg", "hosts.cfg"]
            corresponding_dict = ["use", "hostgroups", "members"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            if "hostgroups" in load_result["data"][key] and load_result["data"][key][
                                "hostgroups"] == hostgroup_name:
                                hosttemplate_list.append([load_result["data"][
                                                              key]["host_name"], load_result["data"][key]["alias"]])
                            elif "hostgroups" not in load_result["data"][key]:
                                hosttemplate_list.append([load_result["data"][
                                                              key]["host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            host_result["success"] = 0
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save host group details
    def save_nagios_edit_hostgroup(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:
            load_result = load_configuration(['hostgroups.cfg'])
            var_list = ['action_url', 'alias', 'hostgroup_members',
                        'hostgroup_name', 'members', 'notes', 'notes_url']
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("hostgroup_name_unique", "")
            new_name = attribute_data["hostgroup_name"]
            attribute = "hostgroup"
            ## new code
            host_name_list = []
            if "members" in attribute_data:
                host_name_list = [i.strip(
                ) for i in attribute_data["members"].split(',')]
                for host_name in host_name_list:
                    host_info = set_attribute_by_name_to_shelve(
                        {"hostgroups": attribute_data["hostgroup_name"]}, "host", host_name)

            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            # query="delete  hosts_hostgroups from hosts_hostgroups join
            # hostgroups as hg on hg.hostgroup_id =
            # hosts_hostgroups.hostgroup_id and hg.hostgroup_name='%s'
            # "%(unique_name)
            query = "update  hosts_hostgroups \
             join hostgroups as hg on hg.hostgroup_name='%s' \
              join hostgroups as hg_default on hg_default.hostgroup_name = 'Default' \
             set  hosts_hostgroups.hostgroup_id = hg_default.hostgroup_id where hosts_hostgroups.hostgroup_id = hg.hostgroup_id " % (
            unique_name)
            cursor.execute(query)
            db.commit()
            for host_name in host_name_list:
            # query="insert into hosts_hostgroups(host_hostgroup_id,host_id,hostgroup_id) values
            #(NULL,(select host_id from hosts where host_name='%s'),\
                #(select hostgroup_id from hostgroups where hostgroup_name='%s'))"%(host_name,unique_name)
                query = "update  hosts_hostgroups \
             join hostgroups as hg on hg.hostgroup_name='%s' \
              join hosts  as h on h.host_name = '%s' \
             set  hosts_hostgroups.hostgroup_id = hg.hostgroup_id \
              where hosts_hostgroups.host_id = h.host_id " % (unique_name, host_name)
                cursor.execute(query)
                db.commit()
            if new_name != unique_name:
                query = " update hostgroups set hostgroup_name='%s' where hostgroup_name='%s'" % (
                    new_name, unique_name)
                cursor.execute(query)
            db.commit()
            cursor.close()
            db.close()

            all_hosts = load_return_attribute("hosts.cfg")
            if all_hosts["success"] == 0:
                host_data = all_hosts["data"]
                for key in host_data:
                    if host_data[key]["host_name"] not in host_name_list:
                        if "hostgroups" in host_data[key]:
                            old_hostgroup = host_data[key]["hostgroups"]
                            hostgroup_list = [
                                i.strip() for i in old_hostgroup.split(',')]
                            flag = 0
                            if unique_name in hostgroup_list:
                                hostgroup_list.remove(unique_name)
                                set_attribute_by_name_to_shelve({"hostgroups": ",".join(
                                    hostgroup_list)}, "host", host_data[key]["host_name"])

            # if not attribute_data.has_key("members"):
            #    attribute_data["members"]=""
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)
            if write_result["success"] == 0:
                comment = "hostgroup: %s updated at time : %s ." % (
                    new_name, str(datetime.now())[:22])
                file_name = "hostgroups.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                comment = "hosts updated due to changes in hostgroup %s at time : %s " % (
                    new_name, str(datetime.now())[:22])
                file_name = "hosts.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)

                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # reload hostgroups and hosts settings from DB
    def reload_nagios_hostgroup(self):
        """


        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select hostgroup_name,hostgroup_id from hostgroups where is_deleted='0' "
            cursor.execute(query)
            result_hg = cursor.fetchall()
            attribute = "hostgroup"
            rt = load_configuration(['hosts.cfg', 'hostgroups.cfg'])
            hostgroup_result = load_db_by_name(attribute)
            if hostgroup_result["success"] == 0:
                hostgroup_result = hostgroup_result["data"]
            else:
                return hostgroup_result
                ## new code
            for hostgroup_name, hostgroup_id in result_hg:
                host_name_list = []
                if hostgroup_name in hostgroup_result:
                    attribute_data = hostgroup_result[
                        hostgroup_name]  # get the info of individual hostgroup
                    # host_name_list = [i.strip() for i in
                    # attribute_data["members"].split(',')]
                    query = "select host_name,host_alias,ip_address from hosts \
                     join (select host_id,hostgroup_id from hosts_hostgroups ) as h_hg on h_hg.hostgroup_id=%s and h_hg.host_id = hosts.host_id " % (
                    hostgroup_id)
                    cursor.execute(query)
                    host_name_list = cursor.fetchall()
                    for host_name in host_name_list:
                        replace_dict = {"hostgroups": hostgroup_name,
                                        'use': hostgroup_name + ',generic-host'}
                        extra_data = {'host_name': host_name[0],
                                      'alias': host_name[1],
                                      'address': host_name[2],
                        }
                        host_info = set_attribute_by_name_to_shelve(
                            replace_dict, "host", host_name[0], extra_data)

                    hostgroup_info = set_attribute_by_name_to_shelve(
                        {"members": ""}, "hostgroup", hostgroup_name)
            comment = "hostgroups updated at time : %s ." % (
                str(datetime.now())[:22])
            file_name = "hostgroups.cfg"
            write_cfg_result = write_configuration_file(file_name, comment)
            comment = "hosts updated due to changes in hostgroups at time : %s " % (
                str(datetime.now())[:22])
            file_name = "hosts.cfg"
            write_cfg_result = write_configuration_file(file_name, comment)
            return JSONEncoder().encode(write_cfg_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

        ################# hostgroup ends

    ################# command starts
    # fetch data table of command
    def get_log_data_command(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            a_columns = ["command_name", "command_line"]
            list_files = ['commands.cfg']
            host_result = self.get_pagination_data(
                "command", list_files, a_columns, req_vars)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            if "exception" not in host_result:
                for row in range(len(aaData)):
                    aaData[row].append("<a href=\"javascript:editCommand('%s');\"><img class='host_opr' \
                     title='Edit Command Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    aaData[row][unique_index]))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # fetch command details
    def get_nagios_command_by_name(self, command_name):
        """

        @param command_name:
        @return:
        """
        try:
            attribute = "command"
            host_result = get_attribute_by_name(command_name, attribute)

            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save command details
    def save_nagios_edit_command(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            attribute_data = {}
            unique_name = req_vars.get("old_command_name", "")
            updated = "updated"
            attribute_data["command_name"] = req_vars.get("command_name", "")
            attribute_data["command_line"] = req_vars.get("command_line", "")
            if (unique_name == ""):
                updated = "added"
                unique_name = attribute_data["command_name"]
            attribute = "command"
            file_name = "commands.cfg"
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)

            if write_result["success"] == 0:
                comment = "command %s %s at time : %s ." % (
                    attribute_data["command_name"], updated, str(datetime.now())[:22])
                write_cfg_result = write_configuration_file(file_name, comment)
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # delete command details
    def nagios_delete_command(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            unique_names_li = req_vars.get("command_names", '').split(',')
            attribute = "command"
            unique_names_str = ", ".join(unique_names_li)
            for unique_name in unique_names_li:
                write_result = delete_attribute_by_name_from_shelve(
                    attribute, unique_name)

            if write_result["success"] == 0:
                comment = "command(s) %s deleted at time : %s ." % (
                    unique_names_str, str(datetime.now())[:22])
                file_name = "commands.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)

                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    ##################### command ends
    ############### hostdependency
    ##### fetch data of host dependency for data table
    def get_log_data_hostdependency(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            a_columns = ["host_name", "dependent_host_name"]
            list_files = ['hostdependency.cfg', 'hosts.cfg']
            dict_name = 'hostdependency'
            extra_dict_name_li = ['host']
            host_index = 1
            # req_vars["iSortCol_0"] =req_vars.get("iSortCol_0",0) if
            # req_vars.get("iSortCol_0",0)!=0 else 1
            host_result = self.get_pagination_data(
                dict_name, list_files, a_columns, req_vars, extra_dict_name_li)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            dependent_index = 2

            if "exception" not in host_result:
                for row in range(len(aaData)):
                    # unique_name = aaData[row][service_index] +
                    # (aaData[row][host_index] if aaData[row][host_index]!="-"
                    # else "")
                    unique_name = aaData[row][unique_index]
                    host_name_list = aaData[row][host_index].split(",")
                    host_aliases = ""
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        # f.close()
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                            # unique_name+=host_name+","
                    aaData[row][host_index] = host_aliases[:-2]

                    host_name_list = aaData[row][dependent_index].split(",")
                    host_aliases = ""
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        # f.close()
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                    aaData[row][dependent_index] = host_aliases[:-2]

                    aaData[row].append("<a href=\"javascript:editHostdependency('%s');\"><img class='host_opr' \
                     title='Edit Hostgroup Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    unique_name))  # aaData[row][unique_index]))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # get host dependency details
    def get_nagios_hostdependency_by_name(self, hostdependency_name):
        """

        @param hostdependency_name:
        @return:
        """
        try:
            attribute = "hostdependency"
            load_result = load_configuration(['hostdependency.cfg'])
            service_result = load_db_by_name(
                attribute)  # get_attribute_by_name(service_description, attribute)
            if (service_result["success"] == 0):
                service_details = service_result["data"]
            else:
                service_details = {}
            host_result = {}
            if hostdependency_name != None and hostdependency_name in service_result["data"]:
                host_result["data"] = service_result[
                    "data"][hostdependency_name]
            elif hostdependency_name == None:
                host_result["data"] = {}
            else:
                output = {"success": 1, "exception":
                    hostdependency_name + " not found."}
                return JSONEncoder().encode(output)

            host_result["options"] = {}
            file_name_list = ["timeperiod.cfg",
                              "hostgroups.cfg", "hosts.cfg", "hosts.cfg"]
            corresponding_dict = ["dependency_period",
                                  "dependent_hostgroup_name", "host_name", "dependent_host_name"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            hosttemplate_list.append([load_result["data"][key][
                                                          "host_name"], load_result["data"][key]["alias"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            host_result["options"]["notification_failure_criteria"] = [["n", "n (none, always)"], ["p", "p (pending)"],
                                                                       ["u", "u (host Unreachable state)"],
                                                                       ["o", "o (host Up state)"],
                                                                       ["d", "d (host Down state)"]]

            host_result["options"]["execution_failure_criteria"] = [["n", "n (none, always)"], ["p", "p (pending)"],
                                                                    ["u", "u (host Unreachable state)"],
                                                                    ["o", "o (host Up state)"],
                                                                    ["d", "d (host Down state)"]]
            host_result["options"]["inherits_parent"] = [["0",
                                                          "0"], ["1", "1"]]
            host_result["success"] = 0
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save host dependency
    def save_nagios_edit_hostdependency(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            var_list = [
                'dependent_host_name', 'host_name', 'dependency_period', 'dependent_hostgroup_name',
                'execution_failure_criteria',
                'inherits_parent', 'notification_failure_criteria', ]
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("hostdependency_name", "")
            attribute = "hostdependency"
            updated = "updated"
            if unique_name == "":
                updated = "added"
                db_result = load_db_by_name(attribute)
                li_host_dependency = []
                for key in db_result['data']:
                    li_host_dependency.append(key)
                if li_host_dependency == []:
                    unique_name = "hostdependency1"
                else:
                    li_host_dependency.sort()
                    last_host_dependency = li_host_dependency[-1]
                    unique_name = "hostdependency" + str(
                        int(last_host_dependency[len('hostdependency'):]) + 1)

            write_result = delete_attribute_by_name_from_shelve(
                attribute, unique_name)
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)

            if write_result["success"] == 0:
                host_name_list = attribute_data["host_name"].split(",")
                host_aliases = ""
                for host_name in host_name_list:
                    host_info = get_attribute_by_name(
                        host_name.strip(), 'host')
                    # f.close()
                    if host_info["success"] == 0:
                        host_aliases += host_info["data"]["alias"] + ", "
                if host_aliases != "":
                    host_aliases = host_aliases[:-2]
                comment = "hostdependency of host(s) %s %s at time : %s ." % (
                    host_aliases, updated, str(datetime.now())[:22])
                file_name = "hostdependency.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # delete nagios host dependency
    def nagios_delete_hostdependency(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            unique_names_li = req_vars.get(
                "host_dependency_names", []).split(',')
            attribute = "hostdependency"
            db_result = load_db_by_name(attribute)
            unique_names_str = ", ".join(unique_names_li)
            host_aliases = ""
            for unique_name in unique_names_li:
                ######
                if unique_name in db_result['data']:
                    attribute_data = db_result['data'][unique_name]
                    host_name_list = attribute_data["host_name"].split(",")

                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                if host_aliases != "":
                    host_aliases = host_aliases[:-2]
                    #######
                write_result = delete_attribute_by_name_from_shelve(
                    attribute, unique_name)

            if write_result["success"] == 0:
                comment = "host dependency for host(s) %s deleted at time : %s ." % (
                    host_aliases, str(datetime.now())[:22])
                file_name = "hostdependency.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)

                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    ####### host dependency ends

    ############### servicedependency starts
    # fetch service dependency data table
    def get_log_data_servicedependency(self, req_vars):
        """

        @param req_vars:
        @return:
        """
        try:
            a_columns = ["host_name", "service_description",
                         "dependent_host_name", "dependent_service_description"]
            list_files = ['servicedependency.cfg', 'hosts.cfg', 'services.cfg']
            dict_name = 'servicedependency'
            extra_dict_name_li = ['host', 'service']
            host_index = 1
            # req_vars["iSortCol_0"] =req_vars.get("iSortCol_0",0) if
            # req_vars.get("iSortCol_0",0)!=0 else 1
            host_result = self.get_pagination_data(
                dict_name, list_files, a_columns, req_vars, extra_dict_name_li)
            # if host_result.has_key("exception"):
            aaData = host_result["aaData"]
            unique_index = 0  # index of host_name
            dependent_index = 3

            if "exception" not in host_result:
                for row in range(len(aaData)):
                    # unique_name = aaData[row][service_index] +
                    # (aaData[row][host_index] if aaData[row][host_index]!="-"
                    # else "")
                    unique_name = aaData[row][unique_index]
                    host_name_list = aaData[row][host_index].split(",")
                    host_aliases = ""
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        # f.close()
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                            # unique_name+=host_name+","
                    aaData[row][host_index] = host_aliases[:-2]

                    host_name_list = aaData[row][dependent_index].split(",")
                    host_aliases = ""
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        # f.close()
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                    aaData[row][dependent_index] = host_aliases[:-2]

                    aaData[row].append("<a href=\"javascript:editServicedependency('%s');\"><img class='host_opr' \
                     title='Edit Service Dependency Details' src='images/new/edit.png' alt='edit'/></a>" % (
                    unique_name))  # aaData[row][unique_index]))
            host_result["aaData"] = aaData
            # return host_result
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "sEcho": 1,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # fetch service depepndency details
    def get_nagios_servicedependency_by_name(self, servicedependency_name):
        """

        @param servicedependency_name:
        @return:
        """
        try:
            attribute = "servicedependency"
            load_result = load_configuration(['servicedependency.cfg'])
            service_result = load_db_by_name(
                attribute)  # get_attribute_by_name(service_description, attribute)
            if (service_result["success"] == 0):
                service_details = service_result["data"]
            else:
                service_details = {}
            host_result = {}
            if servicedependency_name != None and servicedependency_name in service_result["data"]:
                host_result["data"] = service_result[
                    "data"][servicedependency_name]
            elif servicedependency_name == None:
                host_result["data"] = {}
            else:
                output = {"success": 1, "exception":
                    servicedependency_name + " not found."}
                return JSONEncoder().encode(output)

            host_result["options"] = {}
            file_name_list = ["timeperiod.cfg", "hostgroups.cfg", "hosts.cfg",
                              "hosts.cfg", "services.cfg", "services.cfg", "contacts.cfg"]
            corresponding_dict = [
                "dependency_period", "dependent_hostgroup_name", "host_name", "dependent_host_name",
                "service_description",
                "dependent_service_description", "contacts"]
            for i in range(len(file_name_list)):
                file_name = file_name_list[i]
                hosttemplate_list = []
                result_list = []
                load_result = load_return_attribute(file_name)
                if load_result["success"] == 0:
                    for key in load_result["data"]:
                        if file_name == "hosts.cfg":
                            hosttemplate_list.append([load_result["data"][key][
                                                          "host_name"], load_result["data"][key]["alias"]])
                        elif file_name == "services.cfg":
                            hosttemplate_list.append([key.replace(
                                ' ', '___'), load_result["data"][key]["service_description"]])
                        else:
                            hosttemplate_list.append([key, key])
                host_result["options"][corresponding_dict[
                    i]] = hosttemplate_list

            host_result["options"]["notification_failure_criteria"] = [["n", "n (none, always)"], ["p", "p (pending)"],
                                                                       ["u", "u (host Unreachable state)"],
                                                                       ["o", "o (host Up state)"],
                                                                       ["d", "d (host Down state)"]]

            host_result["options"]["execution_failure_criteria"] = [["n", "n (none, always)"], ["p", "p (pending)"],
                                                                    ["u", "u (host Unreachable state)"],
                                                                    ["o", "o (host Up state)"],
                                                                    ["d", "d (host Down state)"]]
            host_result["options"]["inherits_parent"] = [["0",
                                                          "0"], ["1", "1"]]
            host_result["success"] = 0

            load_service_result = load_return_attribute("services.cfg")
            host_service_dict = {}
            for key in load_service_result["data"]:
                di_key = load_service_result["data"][key]
                if "host_name" in di_key:
                    if di_key["host_name"] in host_service_dict:
                        li_temp = host_service_dict[di_key["host_name"]]
                        if li_temp.count(di_key["service_description"]) == 0:
                            li_temp.append(di_key["service_description"])
                        host_service_dict[di_key["host_name"]] = li_temp
                    else:
                        host_service_dict[di_key[
                            "host_name"]] = [di_key["service_description"]]
            host_result["host_service_json"] = host_service_dict
            return JSONEncoder().encode(host_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # save service depepndency details
    def save_nagios_edit_servicedependency(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            var_list = [
                'dependent_host_name', 'host_name', 'dependency_period', 'dependent_hostgroup_name',
                'execution_failure_criteria',
                'inherits_parent', 'notification_failure_criteria', "service_description",
                "dependent_service_description"]
            attribute_data = {}
            for var in var_list:
                res = req_vars.get(var, "")
                if res != "" and str(res).lower() != "null":
                    attribute_data[var] = res
            unique_name = req_vars.get("servicedependency_name", "")

            attribute = "servicedependency"
            updated = "updated"
            if unique_name == "":
                updated = "added"
                db_result = load_db_by_name(attribute)
                li_host_dependency = []
                for key in db_result['data']:
                    li_host_dependency.append(key)
                if li_host_dependency == []:
                    unique_name = "servicedependency1"
                else:
                    li_host_dependency.sort()
                    last_host_dependency = li_host_dependency[-1]
                    unique_name = "servicedependency" + str(int(
                        last_host_dependency[len('servicedependency'):]) + 1)

            write_result = delete_attribute_by_name_from_shelve(
                attribute, unique_name)
            write_result = complete_write_attribute_by_name_to_shelve(
                attribute_data, attribute, unique_name)

            if write_result["success"] == 0:
                host_name_list = attribute_data["host_name"].split(",")
                host_aliases = ""
                for host_name in host_name_list:
                    host_info = get_attribute_by_name(
                        host_name.strip(), 'host')
                    # f.close()
                    if host_info["success"] == 0:
                        host_aliases += host_info["data"]["alias"] + ", "
                if host_aliases != "":
                    host_aliases = host_aliases[:-2]
                comment = "service dependency of host(s) %s and service %s %s at time : %s ." % (
                    host_aliases, attribute_data.get("service_description", ""), updated, str(datetime.now())[:22])
                file_name = "servicedependency.cfg"
                write_cfg_result = write_configuration_file(file_name, comment)
                return JSONEncoder().encode(write_cfg_result)
            else:
                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    # delete service dependency details
    def nagios_delete_servicedependency(self, req_vars={}):
        """

        @param req_vars:
        @return:
        """
        try:

            unique_names_li = req_vars.get(
                "service_dependency_names", []).split(',')
            attribute = "servicedependency"
            unique_names_str = ", ".join(unique_names_li)
            host_aliases = ""
            service_aliases = ""
            db_result = load_db_by_name(attribute)
            for unique_name in unique_names_li:
                ######
                if unique_name in db_result['data']:
                    attribute_data = db_result['data'][unique_name]
                    host_name_list = attribute_data["host_name"].split(",")
                    for host_name in host_name_list:
                        host_info = get_attribute_by_name(
                            host_name.strip(), 'host')
                        if host_info["success"] == 0:
                            host_aliases += host_info["data"]["alias"] + ", "
                    service_aliases = attribute_data["service_description"]
                if host_aliases != "":
                    host_aliases = host_aliases[:-2]
                    #######
                write_result = delete_attribute_by_name_from_shelve(
                    attribute, unique_name)

            #            if write_result["success"]==0:
            comment = "service dependency of hosts(s) %s and servie(s) %s deleted at time : %s ." % (
                host_aliases, service_aliases, str(datetime.now())[:22])
            file_name = "servicedependency.cfg"
            write_cfg_result = write_configuration_file(file_name, comment)
            return JSONEncoder().encode(write_cfg_result)
        #            else:
        #                return JSONEncoder().encode(write_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)

    ################ service dependency ends

    # get status of nagios if its running or not
    def get_nagios_status(self):
        """


        @return:
        """
        try:
            # proc = subprocess.Popen(["omd status nms nagios"],
            # stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process = subprocess.Popen(
                'omd status nagios', shell=True, stdout=subprocess.PIPE)
            output, _ = process.communicate()
            code = process.wait()
            if output.find("running") != -1:
                output = "Nagios is running"
            else:
                output = "Nagios is stopped"
            return output
        except Exception, e:
            return str(e)

    # perform actions on nagios
    def do_action_nagios(self, action):
        """

        @param action:
        @return:
        """
        try:
            process = subprocess.Popen('omd %s nagios' % (
                action), shell=True, stdout=subprocess.PIPE)
            # process = subprocess.Popen('/omd/sites/nms/bin/nagios -v
            # /omd/sites/nms/tmp/nagios/nagios.cfg', shell=True,
            # stdout=subprocess.PIPE)
            output, _ = process.communicate()
            code = process.wait()
            output_action = {
                "success": 0,
                "data": output
            }
            # return JSONEncoder().encode(output_action)
            return output_action
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            # return JSONEncoder().encode(output)
            return output_action

    # verify nagios configuration files
    def do_verify_nagios(self, action):
        """

        @param action:
        @return:
        """
        try:
            process = subprocess.Popen(
                '/omd/sites/%s/bin/nagios -v /omd/sites/%s/tmp/nagios/nagios.cfg' % (nms_instance,
                                                                                     nms_instance), shell=True,
                stdout=subprocess.PIPE)
            output, _ = process.communicate()
            code = process.wait()
            if output.find("/omd/sites/%s/tmp/nagios/nagios.cfg" % (nms_instance)) != -1:
                self.do_action_nagios("start")
                process = subprocess.Popen('/omd/sites/%s/bin/nagios -v /omd/sites/%s/tmp/nagios/nagios.cfg' % (
                    nms_instance, nms_instance), shell=True, stdout=subprocess.PIPE)
                output, _ = process.communicate()
                code = process.wait()
            output = output[207:]
            ipos = 1
            while True:
                pos = output.find('Error', ipos)
                if pos == -1:
                    break
                nindex = output.find('\n', pos + 1)
                if nindex != -1:
                    output = output[:pos] + ' <B> ' + \
                             output[pos:nindex] + ' </B> ' + output[nindex:]
                else:
                    break
                ipos = nindex + 1

            ipos = 1
            while True:
                pos = output.find('\n', ipos)
                if pos - ipos > 100:
                    sindex = output.find(' ', ipos + 100)
                    output = output[:sindex] + '\n' + output[sindex:]
                    ipos = sindex  # ipos+sindex
                else:
                    ipos = pos + 1
                if pos == -1:
                    break
            li = output.split(' ')
            hosts_di = load_db_by_name("host")
            for i in range(len(li)):
                if li[i].startswith("'host"):
                    li[i] = li[i] + " (" + hosts_di[
                        "data"][li[i][1:-1]]["alias"] + ")"
            output = ' '.join(li)
            output = "<pre>" + output + "</pre>"
            return output
        except Exception, e:
            output = "<pre>" + output + "</pre>"
            return output

    # add new host from inventory
    def add_new_host(self, host_name, alias, address, parent_name="", hostgroup_id="", use="generic-host"):
        """

        @param host_name:
        @param alias:
        @param address:
        @param parent_name:
        @param hostgroup_id:
        @param use:
        @return:
        """
        try:
            file_name = "hosts.cfg"
            dict_name = "host"
            attribute = "host"
            try:
                eval('host').clear()
            except:
                pass
            load_result = load_configuration(['hosts.cfg'])
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select host_name from hosts where host_id='%s' " % (
                parent_name)
            cursor.execute(query)
            res = cursor.fetchall()

            ## if hostgroup_id is not given
            if hostgroup_id == "":
                query = "select hostgroup_id from hosts_hostgroups where host_id=(select host_id from hosts where host_name='%s') " % (
                    host_name)
                cursor.execute(query)
                res_hg = cursor.fetchall()
                if res_hg:
                    hostgroup_id = res_hg[0][0]

            query = "select hostgroup_name from hostgroups where hostgroup_id='%s' " % (
                hostgroup_id)
            cursor.execute(query)
            res_hg = cursor.fetchall()
            db.close()
            if res:
                parent_name = res[0][0]
            if res_hg:
                hostgroup_id = res_hg[0][0]

            # code for hostgroup template
            load_result = load_configuration(['host_template.cfg'])
            template_result = get_attribute_by_name(
                hostgroup_id, 'hosttemplate')
            if (template_result)['success'] == 1:
                # append new hostgroup template to host_templates.cfg
                rt = self.add_new_host_template_hostgroup(hostgroup_id, True)
                if rt['success'] == 0:
                    use = hostgroup_id + "," + use
            else:
                use = hostgroup_id + "," + use
            new_host_dict = {"host_name": host_name, "alias": alias, "address":
                address, "use": use, "parents": parent_name, "hostgroups": hostgroup_id}
            comment = "Adding new host(%s) at time : %s" % (
                alias, str(datetime.now())[:22])
            result = append_for_inventory_new_object(
                file_name, dict_name, attribute, new_host_dict, comment)
            return result
        except Exception, e:
            return {'result': str(e), 'success': 1}

    # edit and save host details through inventory
    def edit_old_host(self, host_name, alias, address, parent_name="", hostgroup_id="", use="generic-host"):
        """

        @param host_name:
        @param alias:
        @param address:
        @param parent_name:
        @param hostgroup_id:
        @param use:
        @return:
        """
        try:
            file_name = "hosts.cfg"
            dict_name = "host"
            attribute = "host"
            rt = load_configuration(
                ['services.cfg', 'hosts.cfg', 'host_template.cfg'])
            comment = "Updating host(%s) at time : %s" % (
                alias, str(datetime.now())[:22])
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select host_name from hosts where host_id='%s' " % (
                parent_name)
            cursor.execute(query)
            res = cursor.fetchall()
            query = "select hostgroup_name from hostgroups where hostgroup_id='%s' " % (
                hostgroup_id)
            cursor.execute(query)
            res_hg = cursor.fetchall()
            db.close()
            if res:
                parent_name = res[0][0]
            if res_hg:
                hostgroup_id = res_hg[0][0]

            # code for hostgroup template
            # load_result = load_configuration(['host_template.cfg'])
            template_result = get_attribute_by_name(
                hostgroup_id, 'hosttemplate')
            if (template_result)['success'] == 1:
                # append new hostgroup template to host_templates.cfg
                rt = self.add_new_host_template_hostgroup(hostgroup_id, True)
                if rt['success'] == 0:
                    use = hostgroup_id + "," + use
            else:
                use = hostgroup_id + "," + use

            new_host_dict = {"host_name": host_name, "alias": alias, "address":
                address, "use": use, "parents": parent_name, "hostgroups": hostgroup_id}
            result = edit_for_inventory_object(
                host_name, file_name, attribute, dict_name, new_host_dict, comment)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # code for deleting host through inventory
    def delete_old_host(self, host_name):
        """

        @param host_name:
        @return:
        """
        try:
            file_name = "hosts.cfg"
            dict_name = "host"
            attribute = "host"
            try:
                eval('host').clear()
            except:
                pass

            load_result = load_configuration(['hosts.cfg'])
            host_info = get_attribute_by_name(host_name.strip(), 'host')
            if host_info["success"] == 0:
                # host_aliases += host_info["data"]["alias"]+",
                comment = "Deleting host(%s) at time : %s" % (
                    host_info["data"]["alias"], str(datetime.now())[:22])
            replace_dict = {"parents": "localhost"}
            result = delete_for_inventory_object(
                host_name, file_name, attribute, dict_name, replace_dict, comment)
            service_result = self.delete_old_service(host_name)
            try:
                eval('host').clear()
            except:
                pass

            lr = load_configuration(['hosts.cfg'])
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # add new hostgroup through inventory
    def add_new_hostgroup(self, hostgroup_name, alias):
        """

        @param hostgroup_name:
        @param alias:
        @return:
        """
        try:
            file_name = "hostgroups.cfg"
            dict_name = "hostgroup"
            attribute = "hostgroup"
            try:
                eval('hostgroup').clear()
            except:
                pass
            load_result = load_configuration(['hostgroups.cfg'])
            new_host_dict = {"hostgroup_name": hostgroup_name, "alias": alias}
            comment = "Adding new hostgroup(%s) at time : %s" % (
                hostgroup_name, str(datetime.now())[:22])
            result = append_for_inventory_new_object(
                file_name, dict_name, attribute, new_host_dict, comment)
            rt = self.add_new_host_template_hostgroup(hostgroup_name)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # edit and save hostgroup through inventory
    def edit_old_hostgroup(self, old_hostgroup_name, hostgroup_name, alias):
        """

        @param old_hostgroup_name:
        @param hostgroup_name:
        @param alias:
        @return:
        """
        try:
            file_name = "hostgroups.cfg"
            dict_name = "hostgroup"
            attribute = "hostgroup"
            comment = "Updating hostgroup(%s) at time : %s" % (
                hostgroup_name, str(datetime.now())[:22])
            new_host_dict = {"hostgroup_name": hostgroup_name, "alias": alias}
            load_result = load_configuration(['hostgroups.cfg'])
            result = edit_for_inventory_object(
                old_hostgroup_name, file_name, attribute, dict_name, new_host_dict, comment)
            rt = self.edit_host_template_hostgroup(
                old_hostgroup_name, hostgroup_name)
            rt = self.edit_host_hostgroup_inventory(
                old_hostgroup_name, hostgroup_name)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # function for editing and saving host template through hostgroup via
    # inventory
    def edit_host_template_hostgroup(self, old_hostgroup_name, new_hostgroup_name):
        # renaming the hostgroup
        """

        @param old_hostgroup_name:
        @param new_hostgroup_name:
        @return:
        """
        try:
            file_name = "host_template.cfg"
            dict_name = "hosttemplate"
            attribute = "host"
            #            replace_name="name"
            other_dict = {'name': ''}
            try:
                eval('hosttemplate').clear()
            except:
                pass
            load_result = load_configuration(['host_template.cfg'])
            comment = "Updating host template for hostgroup(%s) at time : %s" % (
                new_hostgroup_name, str(datetime.now())[:22])
            result = edit_for_inventory_object_without_unique(
                other_dict, file_name, attribute, dict_name, old_hostgroup_name,
                new_hostgroup_name, comment)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # save the host and hostgroup relationship
    def edit_host_hostgroup_inventory(self, old_hostgroup_name, new_hostgroup_name):
        # renaming the hostgroup
        """

        @param old_hostgroup_name:
        @param new_hostgroup_name:
        @return:
        """
        try:
            file_name = "hosts.cfg"
            dict_name = "host"
            attribute = "host"
            replace_name = "hostgroups"
            try:
                eval('host').clear()
            except:
                pass
            try:
                eval('hostgroup').clear()
            except:
                pass
            load_result = load_configuration(['hosts.cfg', 'hostgroups.cfg'])
            other_dict = {'use': 'generic-host', 'hostgroups': ''}
            comment = "Updating hosts for hostgroup(%s) at time : %s" % (
                new_hostgroup_name, str(datetime.now())[:22])
            result = edit_for_inventory_object_without_unique(
                other_dict, file_name, attribute, dict_name, old_hostgroup_name,
                new_hostgroup_name, comment)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # delete hostgroup through inventory
    def delete_old_hostgroup(self, hostgroup_name):
        """

        @param hostgroup_name:
        @return:
        """
        try:
            file_name = "hostgroups.cfg"
            dict_name = "hostgroup"
            attribute = "hostgroup"
            load_result = load_configuration(['hostgroups.cfg'])
            comment = "Deleting hostgroup(%s) at time : %s" % (
                hostgroup_name, str(datetime.now())[:22])
            replace_dict = {"hostgroups": "Default"}
            result = delete_for_inventory_object(
                hostgroup_name, file_name, attribute, dict_name, replace_dict, comment)
            replace_dict_template = {"use": "Default", "hostgroups": "Default"}
            old_dict_template = {"use": hostgroup_name,
                                 "hostgroups": hostgroup_name}
            try:
                eval('host').clear()
            except:
                pass
            result_hosts = delete_for_inventory_object_modify_hosts(
                old_dict_template, 'hosts.cfg', 'host', 'host', replace_dict_template, comment)
            d = load_configuration(['host_template.cfg'])
            attribute = "host"
            replace_dict_template = {"use": "generic-host"}
            result_template = delete_for_inventory_object(
                hostgroup_name, "host_template.cfg", attribute, "hosttemplate", replace_dict_template, comment, 0)
            return result
        except Exception, e:
            return {"success": 1, "result": str(e)}

    # add new host template after adding new hostgroup
    # hostgroup has a host template to save its properties
    def add_new_host_template_hostgroup(self, host_template_name, use_default_template=True,
                                        default_template_name="generic-host"):
        """

        @param host_template_name:
        @param use_default_template:
        @param default_template_name:
        @return:
        """
        try:
            attribute = "hosttemplate"
            load_result = load_configuration(['host_template.cfg'])
            host_template_result = {}
            if use_default_template:
                host_template_result = get_attribute_by_name(
                    default_template_name, attribute)
                if (host_template_result)['success'] == 1:
                    host_template_result = {}
                else:
                    host_template_result = host_template_result['data']
                host_template_result["name"] = host_template_name
                host_template_result["register"] = 0
                host_template_result['use'] = 'generic-host'
            else:
                host_template_result["name"] = host_template_name
                host_template_result["register"] = 0
                host_template_result['use'] = 'generic-host'

            write_result = complete_write_attribute_by_name_to_shelve(
                host_template_result, attribute, host_template_name)
            if write_result["success"] == 0:
                comment = "host template %s updated at time : %s ." % (
                    host_template_name, str(datetime.now())[:22])
                file_name = "host_template.cfg"
                write_cfg_result = write_configuration_file(
                    'host_template.cfg', comment, False)
                return write_cfg_result
            else:
                return write_result
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            # return JSONEncoder().encode(output)
            return output

    # add new service while adding new host through inventory
    def add_new_service(self, host_name, host_alias, service_description, max_check_attempts, normal_check_interval,
                        retry_check_interval, check_command, use="generic-service"):
        """

        @param host_name:
        @param host_alias:
        @param service_description:
        @param max_check_attempts:
        @param normal_check_interval:
        @param retry_check_interval:
        @param check_command:
        @param use:
        @return:
        """
        file_name = "services.cfg"
        dict_name = "service"
        attribute = "service"
        try:
            eval('service').clear()
        except:
            pass
        load_result = load_configuration(['service.cfg'])
        new_host_dict = {
            "host_name": host_name, "service_description": service_description,
            "max_check_attempts": max_check_attempts, "use": use,
            "normal_check_interval": normal_check_interval, "retry_check_interval": retry_check_interval,
            "check_command": check_command}

        comment = "Adding new service for host(%s) at time : %s" % (
            host_alias, str(datetime.now())[:22])
        result = append_for_inventory_new_object(
            file_name, dict_name, attribute, new_host_dict, comment)
        return result

    # edit and save service through inventory
    def edit_old_service(self, host_id, service_description, normal_check_interval):
        """

        @param host_id:
        @param service_description:
        @param normal_check_interval:
        @return:
        """
        try:
            file_name = "services.cfg"
            dict_name = "service"
            attribute = "service"
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select host_name, host_alias from hosts where host_id='%s' " % (
                host_id)
            cursor.execute(query)
            res = cursor.fetchall()
            db.close()
            load_result = load_configuration(['service.cfg'])
            host_name, host_alias = "", ""
            if res:
                host_name = res[0][0]
                host_alias = res[0][1]
            comment = "Updating service %s for host(%s) at time : %s" % (
                service_description, host_alias, str(datetime.now())[:22])
            unique_name = service_description + host_name
            new_host_dict = {"host_name": host_name, "service_description":
                service_description, "normal_check_interval": normal_check_interval}
            result = edit_for_inventory_object(
                unique_name, file_name, attribute, dict_name, new_host_dict, comment)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # delete service through inventory
    def delete_old_service(self, host_name):
        """

        @param host_name:
        @return:
        """
        try:
            file_name = "services.cfg"
            dict_name = "service"
            attribute = "service"
            unique_name = host_name
            unique_attribute = "host_name"
            try:
                eval('service').clear()
            except:
                pass
            load_result = load_configuration(['service.cfg'])
            host_info = get_attribute_by_name(host_name.strip(), 'host')
            host_alias = ""
            if host_info["success"] == 0:
                host_alias = host_info["data"]["alias"]
            comment = "Deleting service for host (%s) at time : %s" % (
                host_alias, str(datetime.now())[:22])
            replace_dict = {}
            result = delete_for_inventory_object_without_unique_name(
                unique_attribute, unique_name, file_name, attribute, dict_name, replace_dict, comment)
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # function to retrieve restore nagios configuration
    # gives the list of files present
    def restore_config_nagios(self):
        """


        @return:
        """
        try:
            result = get_file_names()
            if result["success"] == 0:
                log_file = open(result["log_path"], "r")
                f_read = log_file.readlines()
                log_file.close()
                if len(f_read) > 50:
                    result["log_data"] = f_read[len(f_read) - 50:]
                else:
                    result["log_data"] = f_read
                result["log_data"].reverse()
            return result
        except Exception, e:
            return {"success": 1, "data": str(e)}

    # restore the selected nagios file
    def restore_config_nagios_selected(self, file_name):
        """

        @param file_name:
        @return:
        """
        try:
            result = restore_backup(file_name)
            return JSONEncoder().encode(result)
        except Exception, e:
            result = {"success": 1, "data": str(e)}
            return JSONEncoder().encode(result)

    # reload the service times of nagios ie update from DB.
    def reload_nagios_service_times(self):
        """


        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query = "select host_name,host_id from hosts where is_deleted='0' "
            cursor.execute(query)
            result_host_tuple = cursor.fetchall()
            attribute = "service"
            rt = load_configuration(
                ['services.cfg', 'hosts.cfg', 'hostgroups.cfg'])
            service_result = load_db_by_name(attribute)
            if service_result["success"] == 0:
                service_result = service_result["data"]
            else:
                return service_result
                ## new code
            for host_name, host_id in result_host_tuple:
                host_name_list = []
                for key in service_result.keys():
                    if service_result[key].get("host_name", "") == host_name:
                        attribute_data = service_result[
                            key]  # get the info of individual hosts
                        query = "select normal_check_interval,service_description from host_services where host_id='%s' " % (
                            host_id)
                        cursor.execute(query)
                        service_time_list = cursor.fetchall()
                        for normal_check_interval, service_description in service_time_list:
                            if service_description.upper().find("SNMP UPTIME") != -1 and service_result[key].get(
                                    "service_description", "").upper().find("SNMP UPTIME") != -1:
                                host_info = set_attribute_by_name_to_shelve(
                                    {"normal_check_interval": normal_check_interval}, "service", key)
                            elif (service_description.upper().find("STATISTICS SERVICE") != -1 and
                                          service_result[key].get("service_description", "").upper().find(
                                                  "STATISTICS SERVICE") != -1) or (
                                    service_description.upper().find("STATICTICS SERVICE") != -1 and
                                    service_result[key].get("service_description", "").upper().find(
                                            "STATICTICS SERVICE") != -1):
                                host_info = set_attribute_by_name_to_shelve(
                                    {"normal_check_interval": normal_check_interval}, "service", key)

            db.close()
            comment = "services updated at time : %s " % (
                str(datetime.now())[:22])
            file_name = "services.cfg"
            write_cfg_result = write_configuration_file(file_name, comment)
            return JSONEncoder().encode(write_cfg_result)
        except Exception, e:
            output = {
                "success": 1,
                "exception": str(e)
            }
            return JSONEncoder().encode(output)
