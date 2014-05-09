#!/usr/bin/python2.6

from datetime import datetime
import logging
import time

import MySQLdb
from sqlalchemy import and_, or_, desc, asc
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *

from common_bll import EventLog, Essential
from common_controller import *
from py_module import snmp_ping
from pysnmp_ap import *
from unmp_config import SystemConfig
from unmp_model import *
from utility import UNMPDeviceType  # , ErrorMessages, Validation


debug_start = 0
time_diff = 0
time_delay = 0

#@TODO: remove this logging and use logme facility
logging.basicConfig(filename='/omd/daemon/log/recon_log.log',
                    format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)
if debug_start > 0:
    logging.info(" lggin start: ")

errorStatus = {0: 'noError',
               1: 'Device Unresponsive',
               2: 'Parameter is out of range',
               3: 'Bad Value Parameter',
               4: 'Read Only Parameter',
               5: 'General Error. Device Unresponsive',
               6: 'Read Only Parameter',
               7: 'Wrong Type',
               8: 'Wrong Length',
               9: 'Wrong Encoding',
               10: 'Channel Ineffective',
               11: 'No Creation',
               12: 'Inconsistent Value',
               13: 'Resource Unavailable',
               14: 'Commit Failed',
               15: 'Undo Failed',
               16: 'Authorization Error',
               17: 'Not Writable',
               21: 'Invalid radio index',
               22: 'Invalid timeslot index',
               23: 'Invalid MAC address',
               24: 'RU admin state needs to be locked',
               '24': 'Device is not responding',
               25: 'Parameter can not be modified for sync source radio',
               26: 'Sync admin state needs to be locked',
               27: 'Raster time, timer adjust , percentDlTxTime can be specified only when sync source is internal.',
               28: 'RA admin state needs to be locked',
               29: 'Site survey inprogress, can"t do another operation.',
               30: 'Pass phrase not allowed if encryption is not enabled, UNLOCK failed',
               31: 'Blank passphrase is not allowed, UNLOCK failed.',
               32: 'Value specified for mcsindex is not valid for antenna port, UNLOCK failed.',
               33: 'Configured channel is unavailable in RAChannelList, UNLOCK failed',
               34: 'Can not support configured guaranteed bw for specified configuration, UNLOCK failed.',
               38: 'Radio Access admin state needs to be locked',
               39: 'Another O&M operation already in progress.',
               40: 'Two values should be non-zero and one value should be zero in bw calculator.',
               41: 'Error in IP configuration, check IP address, netmask and default gateway are correctly entered.',
               44: 'Numslaves one is not valid if guaranteed broadcast bandwidth is non zero or DBA enabled.',
               49: 'Invalid oid received',
               50: 'On master if aggregate of uplink guaranteedBW found greater than the node bandwidth',
               51: 'On master if aggregate of downlink guaranteedBW found greater than the node bandwidth',
               52: 'Max uplink bw is not in range within guaranteedUplinkBW to nodeBandwidth',
               53: 'Max downlinklink bw is not in range within guaranteedUplinkBW to nodeBandwidth',
               54: 'All timeslots for which MAC is not specified should have same set of values for all attributes',
               18: 'inconsistentName',
               50: 'On master if aggregate of uplink guaranteedBW found greater than the node bandwidth',
               551: 'Network is Unreachable',
               553: 'Request Timeout.Please Wait and Retry Again',
               55: 'Configuration Failed.Please try again later',
               91: 'Arguments are not proper',
               96: 'Configuration Failed.Please try again later',
               97: 'ip-port-community_not_passed',
               98: 'otherException',
               99: 'SNMP agent unknownn error',
               102: 'Unkown Error Occured',
               553: 'Request Timeout'}


host_status_dic = {0: 'No operation', 1: 'Firmware download', 2: 'Firmware upgrade', 3: 'Restore default config', 4: 'Flash commit', 5: 'Reboot', 6: 'Site survey', 7: 'Calculate BW', 8: 'Uptime service', 9: 'Statistics gathering', 10: 'Reconciliation', 11:
                   'Table reconciliation', 12: 'Set operation', 13: 'Live monitoring', 14: 'Status capturing', 15: 'AP Scaning'}

essential_obj = Essential()


class DeviceParameters(object):
    """
    Get the device parameters provided the host_id
    """
    def get_device_parameter(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            device_list_param = []
            device_list_param = sqlalche_obj.session.query(
                Hosts.ip_address, Hosts.mac_address, Hosts.device_type_id, Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            if device_list_param == None:
                device_list_param = []
            return device_list_param
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()


class APDeviceList(object):
    """
    Device AP related listing class
    """
    def ap_device_list(self, ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid=None, html_req={}):
        """
        Author- Anuj Samariya
        This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
        ip_address - This is the IP Address of device e.g 192.168.0.1
        mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
        selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
        return List of Devices in two dimensional list format
        @param ip_address:
        @param mac_address:
        @param selected_device:
        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param sSortDir_0:
        @param iSortCol_0:
        @param userid:
        @param html_req:
        """
        device_dict = {}
        # try block starts
        try:
            device_dict = data_table_data_sqlalchemy(
                ip_address, mac_address, selected_device, i_display_start, i_display_length,
                s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_req)
            # here we create the session of sqlalchemy

            # this is the query which returns the multidimensional array of hosts table and store in device_list
##            device_list = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health).\
##            filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
##            Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(selected_device)),UsersGroups.user_id=='%s'%(userid),\
##            UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
##            .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
            return device_dict
        # try block ends

        # exception starts
        except Exception as e:
            output2 = {
                "sEcho": 1,
                "iTotalRecords": 10,
                "iTotalDisplayRecords": 10,
                "aaData": [],
                "query": str(e)
            }
            return output2

    def ap_device_list_profiling(self, ip_address, mac_address, selected_device):
        """

        @param ip_address:
        @param mac_address:
        @param selected_device:
        @return:
        """
        global sqlalche_obj
        device_list = []
        device_type = selected_device
        device_list_state = "enabled"
        # try block starts
        try:
            # here we create the session of sqlalchemy
            sqlalche_obj.sql_alchemy_db_connection_open()
            # this is the query which returns the multidimensional array of
            # hosts table and store in device_tuple
            device_list = sqlalche_obj.session.query(
                Hosts.host_id, Hosts.host_alias, Hosts.ip_address, Hosts.mac_address).filter(and_(Hosts.is_deleted == 0, Hosts.ip_address.like('%s%%' % (ip_address)),
                                                                                                  Hosts.mac_address.like('%s%%' % (mac_address)), Hosts.device_type_id == device_type)).order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
            return device_list
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    def get_time_ago(self, date1):
        """

        @param date1:
        @return:
        """
        last_check = ""

        date1 = datetime.strptime(
            date1, "%Y-%m-%d %H:%M:%S")  # mysql datetime syntax
        if datetime.now() > date1:
            delta = datetime.now() - date1
        else:
            delta = date1 - datetime.now()
        second = delta.seconds
        if delta.days != 0:
            last_check = str(delta.days) + " days ago"
        else:
            if second < 60:
                last_check = str(second) + " sec ago"
            elif second < 3600:
                minute = int(second / 60)
                last_check = str(minute) + " min ago"
            else:
                hour = int(second / 3600)
                minute = int((second - hour * 3600) / 60)
                last_check = str(hour) + " hour," + str(minute) + " min ago"
        return last_check

    def ap_client_list(self):
        """


        @return:
        """
        global sqlalche_obj

        # try block starts
        try:
            # here we create the session of sqlalchemy
            sqlalche_obj.sql_alchemy_db_connection_open()
            client_list = []
            # this is the query which returns the multidimensional array of
            # hosts table and store in device_tuple
            device_list = sqlalche_obj.db.execute("select client_name,UPPER(mac) as mac,total_tx,total_rx,first_seen_time,hosts_first.host_alias as host_alias1, \
            last_seen_time,hosts_last.host_alias as host_alias2,if(ap_connected_client.state='1','Yes','No') as state, \
            ap_client_ap_data.rssi as rssi,ap25_basicVAPconfigTable.vapESSID as ssid,client_ip, ap.client_id as  client_id\
            from ap_client_details as ap \
            join (select host_id,host_alias,ip_address from hosts) as hosts_first on hosts_first.host_id=ap.first_seen_ap_id \
            join (select host_id,host_alias,ip_address,config_profile_id from hosts) as hosts_last on hosts_last.host_id=ap.last_seen_ap_id \
            join (select rssi,host_id,client_id,vap_id from ap_client_ap_data ) as ap_client_ap_data \
            on ap_client_ap_data.host_id= ap.last_seen_ap_id and ap_client_ap_data.client_id=ap.client_id \
            join (select vapESSID,config_profile_id,vapselection_id from ap25_basicVAPconfigTable) \
            as ap25_basicVAPconfigTable on ap25_basicVAPconfigTable.config_profile_id=hosts_last.config_profile_id and \
            ap25_basicVAPconfigTable.vapselection_id=ap_client_ap_data.vap_id\
            join (select state,host_id,client_id from ap_connected_client ) as ap_connected_client on ap.client_id=ap_connected_client.client_id and ap.last_seen_ap_id=ap_connected_client.host_id order by ap.client_id")
            for row in device_list:
                client_list.append(
                    [row["state"], row["client_name"], row["mac"], row["client_ip"] != None and row["client_ip"] or "", str(row["total_tx"]), str(row["total_rx"]), row["host_alias2"], str(row["rssi"]),
                     row["ssid"], self.get_time_ago(
                     str(row["last_seen_time"])), row["host_alias2"], "<a href=\"javascript:editClient('%s');\"><img alt=\"edit\" src=\"images/new/edit.png\" class=\"host_opr\" title=\"Edit Client Details\"/></a>&nbsp;<a href=\"client_dashboard_profiling.py?client_mac=%s&device_type=%s\"><img alt=\"Performance Monitoring\" src=\"images/new/graph.png\" class=\"host_opr\" title=\"Client Performance Monitoring\"/></a>" % (row["client_id"], row["mac"], "ap25")
                     ])

            return client_list
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

    #######################
    def pagination_create_table(self, i_display_start, i_display_length, s_search, sEcho, req_vars):
        """

        @param i_display_start:
        @param i_display_length:
        @param s_search:
        @param sEcho:
        @param req_vars:
        @return:
        """
        a_columns = ["if(ap_connected_client.state='1','<img alt=\"Yes\" src=\"images/host_status_ap_0.png\" class=\"host_opr n-reconcile\" title=\"Yes\"/>','<img alt=\"No\" src=\"images/host_status_ap_1.png\" class=\"host_opr n-reconcile\" title=\"No\"/>')", "client_name", "UPPER(mac)", "ifnull(client_ip,'-')", "total_tx", "total_rx", "ifnull(hosts_first.host_alias,'-')",
                     "ifnull(ap_client_ap_data.rssi,'-')", "ifnull(ap25_basicVAPconfigTable.vapESSID,'-')", "last_seen_time", "ifnull(hosts_last.host_alias,'-')",
                     "ap_client_details.client_id"
                     ]
        s_index_column = a_columns[-1]  # "ap.timestamp";
        s_table = "ap_client_details "  # " ap25_statisticsTable as ap "
        s_join = " left join (select host_id,host_alias,ip_address from hosts) as hosts_first on hosts_first.host_id=ap_client_details.first_seen_ap_id \
            left join (select host_id,host_alias,ip_address,config_profile_id from hosts) as hosts_last on hosts_last.host_id=ap_client_details.last_seen_ap_id \
            left join (select rssi,host_id,client_id,vap_id from ap_client_ap_data ) as ap_client_ap_data \
            on ap_client_ap_data.host_id= ap_client_details.last_seen_ap_id and ap_client_ap_data.client_id=ap_client_details.client_id \
            left join (select vapESSID,config_profile_id,vapselection_id from ap25_basicVAPconfigTable) \
            as ap25_basicVAPconfigTable on ap25_basicVAPconfigTable.config_profile_id=hosts_last.config_profile_id and \
            ap25_basicVAPconfigTable.vapselection_id=ap_client_ap_data.vap_id\
            left join (select state,host_id,client_id from ap_connected_client ) as ap_connected_client on ap_client_details.client_id=ap_connected_client.client_id and ap_client_details.last_seen_ap_id=ap_connected_client.host_id"
        s_order = "order by ap_client_details.client_id,ap_connected_client.state desc"
        s_where = ""  # query_dict["where"]
        s_group_by = ""  # query_dict["group_by"]
        # a_columns will store table columns ... Not necessarily same as on HTML
        # s_index_column is the index column
        # s_table will store table name
        # s_join will store join query
        # s_order = variable which stores order by query
        # s_where = variable which stores where condition
        # s_group_by = group by query
        # sql=" select %s from %s %s %s %s
        # %s"%(query_dict["columns"],query_dict["table_name"],query_dict["join"],query_dict["where"],query_dict["group_by"],query_dict["order_by"])
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            # sql = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (" , ".join(a_columns),s_table,s_join,s_where,s_group_by,s_order)#,s_limit)
            # i_total=cursor.execute(sql)
            s_limit = ""
            # Ordering
            s_limit = ""
            i_display_start = req_vars.get("iDisplayStart", 0)
            i_display_length = req_vars.get("iDisplayLength", 0)
            if (i_display_start != None and i_display_length != '-1'):
                s_limit = "LIMIT %s, %s" % (MySQLdb.escape_string(
                    i_display_start), MySQLdb.escape_string(i_display_length))

            # Ordering
            i_sort_col_0 = req_vars.get("iSortCol_0", None)
            if i_sort_col_0 != None:
                s_order = "ORDER BY  "
                for i in range(0, int(req_vars.get("iSortingCols", 0))):
                    i_sort_col_i = int(req_vars.get("iSortCol_%s" % i, -1))
                    b_sortable_ = req_vars.get(
                        "bSortable_%s" % i_sort_col_i, None)
                    if b_sortable_ == "true":
                        s_sort_dir_i = req_vars.get("sSortDir_%s" % i, "asc")
                        s_order += "%s %s, " % (
                            a_columns[i_sort_col_i], MySQLdb.escape_string(s_sort_dir_i))

                s_order = s_order[:-2]
                if s_order == "ORDER BY":
                    s_order = ""

            # Filtering
            # s_where = "";
            s_where = ""
            s_search = req_vars.get("sSearch", None)
            if s_search != "" and s_search != None:
                s_where = "WHERE ("
                for i in range(0, len(a_columns)):
                    s_where += "%s LIKE '%%%s%%' OR " % (
                        a_columns[i], MySQLdb.escape_string(s_search))
                s_where = s_where[:-3]
                s_where += ")"
##            s_search = req_vars.get("sSearch",None)
##            if s_search != None:
##                s_where += "AND ("
##                for i in range(0,len(a_columns)):
##                    s_where += "%s LIKE '%%%s%%' OR " % (a_columns[i],MySQLdb.escape_string(s_search))
##                s_where = s_where[:-3]
##                s_where += ")"
##
##            # Individual column filtering
##            for i in range(0,len(a_columns)):
##                b_searchable_i = req_vars.get("bSearchable_%s" % i,None)
##                s_search_i = req_vars.get("sSearch_%s" % i,"")
##                if (b_searchable_i == "true" and s_search_i != ""):
##                    if s_where == "":
##                        s_where = "WHERE ";
##                    else:
##                        s_where += " AND ";
# s_where += "%s LIKE '%%%s%%' " %
# (a_columns[i],MySQLdb.escape_string(s_search_i))

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # SQL queries
            # Get data to display
            sql_query = "SELECT SQL_CALC_FOUND_ROWS %s FROM %s %s %s %s %s" % (
                ", ".join(a_columns), s_table, s_join, s_where, s_order, s_limit)
            # return sql_query
            check_query = sql_query
            # create sql query - End
            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            r_result = cursor.fetchall()
            check_result = r_result
            # close the cursor
            cursor.close()

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # Data set length after filtering
            sql_query = "SELECT FOUND_ROWS()"

            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            i_filtered_total = cursor.fetchone()[0]

            # close the cursor
            cursor.close()

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # Total data set length
            sql_query = "SELECT COUNT(%s) FROM %s %s %s " % (
                s_index_column, s_table, s_join, s_where)

            # execute sql query
            cursor.execute(sql_query)

            # fetch data from executed sql query
            i_total = cursor.fetchone()[0]

            # close the cursor
            cursor.close()

            result_data = []
            if(r_result != ()):
                for a_row in r_result:
                    row = []
                    client_id = a_row[-1]
                    mac = a_row[2]
                    for i in range(len(a_row)):
                        if i == len(a_row) - 1:
                            pass
                        else:
                            if isinstance(a_row[i], datetime):
                                row.append(str(a_row[i]))
                            else:
                                row.append(a_row[i])
                    row.append(
                        "<a href=\"javascript:editClient('%s');\"><img alt=\"edit\" src=\"images/new/edit.png\" class=\"host_opr n-reconcile\" title=\"Edit Client Details\"/></a>&nbsp;<a href=\"client_dashboard_profiling.py?client_mac=%s&device_type=%s&path=0\"><img alt=\"Performance Monitoring\" src=\"images/new/graph.png\" class=\"host_opr n-reconcile\" title=\"Client Performance Monitoring\"/></a>&nbsp;" % (client_id, mac, "ap25"))
                    result_data.append(list(row))

            output = {
                "success": 0,
                "sEcho": int(req_vars.get("sEcho", 0)),
                "iTotalRecords": int(i_total),  # i_filtered_total,#i_total,
                "iTotalDisplayRecords": int(i_filtered_total),  # i_filtered_total,
                "aaData": result_data,
                "query": sql_query
            }
            db.close()
            return output

        except Exception, e:
    #		return {"succcess" : 1 , "result":str(e) }
            output = {
                "success": 0,
                "sEcho": int(sEcho),
                "iTotalRecords": 0,  # i_total,#i_filtered_total,#i_total,
                "iTotalDisplayRecords": 0,  # i_filtered_total,
                "aaData": [],
                "result": [],
                "exception": str(e)

            }
            return output


    ##########################
# obj = APDeviceList()
# print obj.ap_client_list()
class APCommitToFlash(object):
    """AP Commit To Flash class

    """
    def commit_to_flash(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj, essential_obj, host_status_dic, errorStatus
        result = {}
        oid_dict = {}
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            i = 0
            oid_dict[1] = ['1.3.6.1.4.1.26149.10.5.1.0', 'Integer32', 1]
            host_param = sqlalche_obj.session.query(
                Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.snmp_read_community).filter(Hosts.host_id == host_id).all()
            host_op_state = essential_obj.host_status(host_id, 4)
            if int(host_op_state) == 0:
                if len(host_param) > 0:
                    result = single_set(host_param[0].ip_address, int(
                        host_param[0].snmp_port), host_param[0].snmp_write_community, oid_dict[1])
                    if result["success"] == 0:
                        oid_dict[2] = [
                            '1.3.6.1.4.1.26149.10.5.3.0', 'Integer32', 1]
                        result = single_set(host_param[0].ip_address, int(
                            host_param[0].snmp_port), host_param[0].snmp_write_community, oid_dict[2])
                        if result["success"] == 0:
                            time.sleep(20)
                            while(i < 5):
                                get_result = pysnmp_get(
                                    '1.3.6.1.4.1.26149.10.5.3',
                                    host_param[0].ip_address, int(host_param[0].snmp_port), 'public')
                                if get_result["success"] == 0:
                                    result = {"success": 0, "result":
                                              "Configuration data saved permanently in the device"}
                                    return result
                                i = i + 1
                                time.sleep(10)
                            result = {'success':
                                      1, 'result': 'Device is Not Responding'}
                        else:
                            k = result['result'].keys()[0]
                            if k != 553 and k != '553':
                                if k in errorStatus:
                                    result = {"success":
                                              1, "result": errorStatus[k]}
                                else:
                                    try:
                                        result = {"success": 1, "result": result[
                                            'result'].get(oid_dict[1][0], ' Unknown snmp error , Please try again later')}
                                    except:
                                        result = {"success": 1,
                                                  "result": " Unknown snmp error , Please try again later"}
                            else:
                                result = {'success': 1,
                                          'result': 'Device SNMP agent is Not Responding'}
                    else:
                        k = result['result'].keys()[0]
                        if k != 553 and k != '553':
                            if k in errorStatus:
                                result = {
                                    "success": 1, "result": errorStatus[k]}
                            else:
                                try:
                                    result = {"success": 1, "result": result['result']
                                              .get(oid_dict[1][0], ' Unknown snmp error , Please try again later')}
                                except:
                                    result = {"success": 1,
                                              "result": " Unknown snmp error , Please try again later"}
                        else:
                            result = {'success': 1,
                                      'result': 'Device SNMP agent is Not Responding'}
                    return result
                    # return {'success':1,'data':'onvnaoh'}
                else:
                    return {"success": 1, "result": "Host Data Not Exist"}
            else:
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}
        except Exception, e:
            # return {"success":1,"result":str(e[-1])}
            return {'success': 1, 'cvah': 'fagrfa'}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            essential_obj.host_status(host_id, 0, None, 4)

    def commit_to_flash_test(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj, essential_obj, host_status_dic, errorStatus
        result = {}
        oid_dict = {}
        try:
            sqlalche_obj.sql_alchemy_db_connection_open()
            i = 0
            oid_dict[1] = ['1.3.6.1.4.1.26149.10.5.2.0', 'Integer32', 1]
            host_param = sqlalche_obj.session.query(
                Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.snmp_read_community).filter(Hosts.host_id == host_id).all()
            host_op_state = essential_obj.host_status(host_id, 4)
            if int(host_op_state) == 0:
                if len(host_param) > 0:
                    result = single_set(host_param[0].ip_address, int(
                        host_param[0].snmp_port), host_param[0].snmp_write_community, oid_dict[1])
                    if result["success"] == 0:
                        result = {"success": 0, "result":
                                  "Configuration data saved permanently in the device"}  # check
                        return
                    else:
                        k = result['result'].keys()[0]
                        if k != 553 and k != '553':
                            if k in errorStatus:
                                result = {
                                    "success": 1, "result": errorStatus[k]}
                            else:
                                try:
                                    result = {"success": 1, "result": result['result']
                                              .get(oid_dict[1][0], ' Unknown snmp error , Please try again later')}
                                except:
                                    result = {"success": 1,
                                              "result": " Unknown snmp error , Please try again later"}
                        else:
                            while(i < 5):
                                time.sleep(20)
                                i = i + 1
                                get_result = pysnmp_get(
                                    '1.3.6.1.4.1.26149.10.5.3',
                                    host_param[0].ip_address, int(host_param[0].snmp_port), 'public')
                                if get_result["success"] == 0:
                                    result = {"success": 0, "result":
                                        "Configuration data saved permanently in the device"}
                                    return result

                            result = {'success':
                                1, 'result': 'Device is Not Responding'}
                        return result
                else:
                    return {"success": 1, "result": "Host Data Not Exist"}
            else:
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}
        except Exception, e:
            return {"success": 1, "result": str(e[-1])}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            essential_obj.host_status(host_id, 0, None, 4)

# obj = APCommitToFlash()
# print obj.commit_to_flash(60)


def rename_tablename(tablename):
    """

    @param tablename:
    @return:
    """
    try:
        ss = ""
        idx = tablename.index("_")
        ss = tablename[0:idx] + tablename[idx + 1].upper() + \
                                                         tablename[
                                                             idx + 1 + 1:]
        ss = ss[0].upper() + ss[1:]
        return ss
    except Exception as e:
        return e


class Reconciliation(object):
    """
    AP reconciliation
    """
##    def update_configuration(self,host_id,device_type_id):
##        host_param = []
##        global errorStatus
##        global sqlalche_obj
##        try:
##            sqlalche_obj.sql_alchemy_db_connection_open()
##            obj_system_config = SystemConfig()
##            table_prefix = "ap25_"
##            total_table = 11
##            rec = 1
##            total_per = 0
##            column_list = []
##            host_param = sqlalche_obj.session.query(Hosts).filter(Hosts.host_id == host_id).all()
##            config_profile_id = host_param[0].config_profile_id
##            if len(host_param)>0:
##                snmp_ping_result = snmp_ping(host_param[0].ip_address,host_param[0].snmp_read_community,int(host_param[0].snmp_port))
##                if int(snmp_ping_result)==0:
##                    host_param[0].reconcile_status = 1
##                    sqlalche_obj.session.commit()
##                    database_name = obj_system_config.get_sqlalchemy_credentials()
##                    result = vapsetup_ap(str(host_param[0].ip_address),int(host_param[0].snmp_port))
##                    if result["success"]==0:
##                        rec = rec + 1
##                        vap_selection = sqlalche_obj.session.query(Ap25VapSelection).filter(Ap25VapSelection.config_profile_id == config_profile_id).all()
##                        if len(result["result"]["vap"])==2:
##                            for i in range(0,len(vap_selection)):
##                                vap_selection[i].totalVAPsPresent = result["result"]["vap"][0]
##                                vap_selection[i].selectVap = result["result"]["vap"][1]
##                                sqlalche_obj.session.flush()
##                        vap_tables = ['ap25_basicVAPsetup','ap25_basicVAPsecurity','ap25_vapWPAsecuritySetup','ap25_basicACLsetup','ap25_aclMacTable']
##                        for i in result["result"]["data"]:
##
##                            for j in range(0,len(result["result"]["data"][i])):
##
##
##                                column_list = []
##                                result_db  = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'"%(vap_tables[j],database_name[4]))
##                                for row in result_db:
##                                    column_list.append(row["column_name"])
##
##                                primary_key = vap_tables[j]+"_id"
##                                column_list.remove(primary_key)
##                                column_list.remove('config_profile_id')
##
##                                if 'vapselection_id' in column_list:
##                                    column_list.remove('vapselection_id')
##                                sql_alche_table_name = rename_tablename(vap_tables[j])
##                                if vap_tables[j]=="ap25_aclMacTable":
##                                    table_result = sqlalche_obj.session.query(eval('%s'%(sql_alche_table_name))).filter(and_(eval('%s'%(sql_alche_table_name)).\
##                                                    config_profile_id=='%s'%(config_profile_id),(eval('%s'%(sql_alche_table_name)).vapselection_id=='%s'%(vap_selection[i].ap25_vapSelection_id)))).all()
##                                    sqlalche_obj.db.execute("delete from %s where config_profile_id='%s' and vapselection_id='%s'"%(vap_tables[j],config_profile_id,vap_selection[i].ap25_vapSelection_id))
##                                    sqlalche_obj.session.commit()
##                                    table_result = sqlalche_obj.session.query(eval('%s'%(sql_alche_table_name))).filter(and_(eval('%s'%(sql_alche_table_name)).\
##                                                    config_profile_id=='%s'%(config_profile_id),(eval('%s'%(sql_alche_table_name)).vapselection_id=='%s'%(vap_selection[i].ap25_vapSelection_id)))).all()
##                                else:
##                                    table_result = sqlalche_obj.session.query(eval('%s'%(sql_alche_table_name))).filter(eval('%s'%(sql_alche_table_name)).config_profile_id=='%s'%(config_profile_id)).all()
##
##                                if len(table_result)>0:
##
##
##                                    if len(result["result"]["data"][i][j])>0:
##
##                                        for k in range(0,len(result["result"]["data"][i][j])):
##                                            exec "table_result[%s].%s = '%s'"%(i-1,column_list[k],result["result"]["data"][i][j][k])
##                                else:
##                                    if vap_tables[j] == "ap25_aclMacTable":
##                                        if len(result["result"]["data"][i][j])>0:
##                                            for k in range(0,len(result["result"]["data"][i][j])):
##                                                sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s,%s)"%(vap_tables[j],config_profile_id,vap_selection[i].ap25_vapSelection_id,str(result["result"]["data"][i][j][k])[1:-1]))
##                                time.sleep(2)
##                    else:
##                        if rec>0:
##                            rec = rec - 1
##                    node_tables = sqlalche_obj.session.query(Ap25OidTable.table_name,Ap25OidTable.table_oid,Ap25OidTable.isNode).filter(Ap25OidTable.isVap==1).all()
##                    for i in range(0,len(node_tables)):
####                        if node_tables[i][0]=='versions':
####                            continue
##                        column_list=[]
##
##                        tablename = table_prefix + node_tables[i][0]
##                        result_db  = sqlalche_obj.db.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'"%(tablename,database_name[4]))
##                        for row in result_db:
##                            column_list.append(row["column_name"])
##
##                        if (node_tables[i][2]==0):
##                            result = pysnmp_get_node(node_tables[i][1],host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_read_community)
##                        else:
##                            result = pysnmp_get_table(node_tables[i][1],host_param[0].ip_address,int(host_param[0].snmp_port),host_param[0].snmp_read_community)
##
##                        if result["success"]==0:
##                            rec=rec+1
##                            sqlalche_table_name = rename_tablename(tablename)
##                            primary_key = tablename+"_id"
##                            if 'config_profile_id' in column_list:
##                                config_id = 0
##                                table_result = sqlalche_obj.session.query(eval('%s'%(sqlalche_table_name))).filter(eval('%s'%(sqlalche_table_name)).config_profile_id=='%s'%(config_profile_id)).all()
##
##                            else:
##                                config_id = 1
##                                table_result = sqlalche_obj.session.query(eval('%s'%(sqlalche_table_name))).filter(eval('%s'%(sqlalche_table_name)).host_id=='%s'%(host_id)).all()
##
##                            if len(result["result"])>0:
##                                if len(table_result)>0:
##                                    column_list.remove(primary_key)
##                                    if config_id == 0:
##                                        column_list.remove('config_profile_id')
##                                        for i in result["result"]:
##                                            for k in range(0,len(column_list)):
##                                                temp_result = str(result["result"][i][k])
##
##                                                exec "table_result[%s].%s = '%s'"%(i-1,column_list[k],temp_result[:-1] if temp_result.count('\n') else temp_result)
##
##                                    else:
##                                        column_list.remove('host_id')
##                                        for i in result["result"]:
##                                            for k in range(0,len(column_list)):
##                                                temp_result = str(result["result"][i][k])
##
##                                                exec "table_result[%s].%s = '%s'"%(i-1,column_list[k],temp_result[:-1] if temp_result.count('\n') else temp_result)
##                                else:
##                                    for i in range(0,len(result["result"])):
##                                        if config_id == 0:
##                                            sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,config_profile_id,str(result["result"][i+1])[1:-1]))
##                                        else:
##
##                                            sqlalche_obj.db.execute("Insert into %s values (NULL,%s,%s)"%(tablename,host_id,str(result["result"][i+1])[1:-1]))
##                        else:
##                            if rec>0:
##                                rec = rec - 1
##                        #sqlalche_obj.db.execute("insert into ap25_versions values(NULL,%s,'%s','%s','%s')"%(host_id,'Rev.b','','0.0.5'))
##                        sqlalche_obj.session.commit()
##                    total_per = float(rec)/float(total_table)
##                    total_per = int(total_per*100)
##                    host_param[0].reconcile_status = 2
##                    host_param[0].reconcile_health = total_per
##                    sqlalche_obj.session.commit()
##                    time.sleep(1)
##                    host_param[0].reconcile_status = 0
##                    sqlalche_obj.session.commit()
##                    result = {"success":0,"result":{total_per:[host_param[0].host_name,host_param[0].ip_address]}}
##                    return result
##                else:
##                    if snmp_ping_result == 2:
##                        result = {"success":1,"result":"Network is Unreachable"}
##                    elif snmp_ping_result == 1:
##                        result = {"success":1,"result":"%s(%s) Device may not be connected or may be reboot"%(host_param[0].host_name,host_param[0].ip_address)}
##                    elif snmp_ping_result == 3:
##                        result = {"success":1,"result":"%s(%s) Device is unresponsive"%(host_param[0].host_name,host_param[0].ip_address)}
##                    host_param[0].reconcile_status = 0
##                    sqlalche_obj.session.commit()
##                    return result
##            else:
##                result = {"success":1,"result":"Host data not exist"}
##                return result
##        except Exception as e:
##            host_param[0].reconcile_health = 0
##            host_param[0].reconcile_status = 0
##            sqlalche_obj.session.commit()
##            result = {"success":1,"result":"Error Occured %s"%str(e)}
##            return result
##        finally:
##            sqlalche_obj.sql_alchemy_db_connection_close()

    def time_diff_rec_table(self, table_oid_dic, current_time):
        """

        @param table_oid_dic:
        @param current_time:
        @return:
        """
        table_dic = {}
        global time_diff
        time_diff = 0
        fmt = '%Y-%m-%d %H:%M:%S'
        a = str(current_time)
        global time_delay
        for i in table_oid_dic:
            if i == "raChannelListTable":
                continue
            table_rec_time = table_oid_dic[i][1]

            diff1 = datetime.strptime(str(table_rec_time), fmt)

            diff2 = datetime.strptime(a[:a.find('.') - 1], fmt)
            rec_time = (diff2 - diff1)
            rec_time = divmod(rec_time.days * 86400 + rec_time.seconds, 60)
            if rec_time[0] < time_diff:
                if table_oid_dic[i][0] == 0:
                    table_dic.update({i: table_oid_dic[i][2]})
            else:
                table_dic.update({i: table_oid_dic[i][2]})
        time_delay = diff1

        return table_dic

    def update_configuration(self, host_id, device_type, table_prefix, current_time, user_name):
        """

        @param host_id:
        @param device_type:
        @param table_prefix:
        @param current_time:
        @param user_name:
        @return:
        """
        global essential_obj, sqlalche_obj, host_status_dic, errorStatus
        host_status = 0
        host_data = []
        table_oid_dic = {}
        table_var_bind = {}
        rec_not_done = []
        rec_done = []
        total_rec = 0
        rec = 0
        rec_per = 0
        table_form = ""
        time_stamp = str(datetime.now())
        chcek_flag = 0  # chcek the enter in reconcilation or not
        try:
            if debug_start > 0:
                logging.info(" start: ")
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(Hosts).\
                filter(Hosts.host_id == host_id).all()
            result = {'success': 0, 'result': "Devcie is Busy"}
            if host_id != None or host_id != "":
                host_op_status = essential_obj.host_status(host_id, 10)

                if host_op_status != None or host_op_status != "":

                    if int(host_op_status) == 0:
                        chcek_flag = 1
                        if len(host_data) > 0:
                            ping_chk = snmp_ping(host_data[0].ip_address, host_data[
                                                 0].snmp_read_community, int(host_data[0].snmp_port))
                            if debug_start > 0:
                                logging.info(" ping_chk: " + str(ping_chk))
                            if int(ping_chk) == 0:
                                host_data[0].reconcile_status = 1
                                sqlalche_obj.session.commit()
                                if device_type == "ap25":
                                # mac address updation in table
                                    try:
                                        oid_dic = {
                                            'mac_address': '1.3.6.1.4.1.26149.10.4.1.3.0'}
                                        get_result = pysnmp_geter(oid_dic, host_data[0].ip_address, int(
                                            host_data[0].snmp_port), host_data[0].snmp_read_community)
                                        if get_result['success'] == 0:
                                            get_result = get_result['result']
                                            sqlalche_obj.db.execute(
                                                "Update hosts set mac_address = '%s' where ip_address='%s'" % (get_result['mac_address'],
                                                                                                                                 host_data[0].ip_address))
                                            sqlalche_obj.session.commit()
                                    except:
                                        pass
                                    # mac address updation

                                    table_result = sqlalche_obj.session.query(
                                        Ap25Oid_table).filter(Ap25Oid_table.is_recon == 1).all()
                                    print table_result
                                    if debug_start > 0:
                                        logging.info(" table_result: " +
                                                     str(table_result))
                                if len(table_result) > 0:
                                    for i in range(0, len(table_result)):
                                        table_oid_dic.update(
                                            {table_result[
                                                i].table_name: [table_result[i].status,
                                                             table_result[i].timestamp, table_result[i].table_oid]})
                                        table_var_bind.update({table_result[i].table_name:
                                                              table_result[i].varbinds})

                                    rec_table_dic = self.time_diff_rec_table(
                                        table_oid_dic, current_time)

                                    if len(rec_table_dic) > 0:
                                        total_rec = len(rec_table_dic)
                                        obj_system_config = SystemConfig()
                                        for j in rec_table_dic:
                                            # print j
                                            column_list = []
                                            tablename = str(
                                                table_prefix) + str(j)
                                            if debug_start > 0:
                                                logging.info(
                                                    " table_name: " + str(j))
                                            sqlalche_tablename = rename_tablename(
                                                tablename)
                                            database_name = obj_system_config.get_sqlalchemy_credentials(
                                                )
                                            result_db = sqlalche_obj.db.execute(
                                                "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s' and table_schema = '%s'" % (tablename, database_name[4]))

                                            for columns in result_db:
                                                column_list.append(
                                                    columns["column_name"])
                                            if debug_start > 0:
                                                logging.info(" column_list: " +
                                                             str(column_list))
                                            if debug_start > 0:
                                                logging.info(" database_name: " +
                                                             str(database_name))
                                            time.sleep(5)

                                            result = bulktable(
                                                rec_table_dic[j], host_data[
                                                    0].ip_address,
                                                               int(host_data[0].snmp_port), host_data[0].snmp_read_community, int(table_var_bind.get(j)))
                                            if debug_start > 0:
                                                logging.info(
                                                    " resut: " + str(result))
                                            if result['success'] == 1:
                                                for key in result['result']:
                                                    if int(key) == 53 or int(key) == 553:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2000")
                                                        result['success'] = 1

                                                    elif int(key) == 51:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2001")
                                                        result['success'] = 1
                                                        return
                                                    elif int(key) == 51:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2002")
                                                        result['success'] = 1
                                                        return
                                                    elif int(key) == 97 or int(key) == 98 or int(key) == 99 or int(key) == 102:
                                                        result['result'] = errorStatus.get(
                                                            key, "UNMP Server is busy.Please try after some time,2002")
                                                        result['success'] = 1
                                                        return
                                                    elif int(key) == 5 or int(key) == 24 or int(key) == 72:
                                                        result['result'] = errorStatus.get(
                                                            key, "Device is busy.Please try again later")
                                                        result['success'] = 1

                                                    else:
                                                        if key in errorStatus:
                                                            result['result'] = errorStatus.get(
                                                                key, "UNMP Server is busy.Please try after some time,2003")
                                                rec_not_done.append(str(j))
                                            else:
                                                if debug_start > 0:
                                                    logging.info(
                                                        " else part: \n\n")
                                                if len(result['result']) == 0:
                                                    rec_done.append(str(j))
                                                    rec = rec + 1
                                                    if "config_profile_id" in column_list:

                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where config_profile_id = '%s' " % (tablename, host_data[0].config_profile_id))
                                                    else:
                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where host_id = '%s' " % (tablename, host_data[0].host_id))
                                                else:
                                                    if debug_start > 0:
                                                        logging.info(
                                                            " debug: \n\n")
                                                    rec_done.append(str(j))
                                                    rec = rec + 1
                                                    if debug_start > 0:
                                                        logging.info(
                                                            " sqlalchetablename \n\n",
                                                                     str(sqlalche_tablename))

                                                    if "config_profile_id" in column_list:
                                                        if debug_start > 0:
                                                            logging.info(
                                                                " debug isi mein : ")
                                                        table_form = "123"
                                                        table_form = eval(
                                                            sqlalche_tablename)
                                                        sqlalche_table_result = sqlalche_obj.session.query(eval(sqlalche_tablename)).filter(
                                                            getattr(eval(sqlalche_tablename), "config_profile_id") == host_data[0].config_profile_id).all()
                                                        if debug_start > 0:
                                                            logging.info(" sqlalche_table_result : " +
                                                                         str(sqlalche_table_result))

                                                    else:
                                                        sqlalche_table_result = sqlalche_obj.session.query(
                                                            eval(sqlalche_tablename)).filter(getattr(eval(sqlalche_tablename), "host_id") == host_id).all()
                                                    primary_key_id = tablename + \
                                                        "_id"
                                                    column_list.remove(
                                                        primary_key_id)
                                                    if "config_profile_id" in column_list:
                                                        column_list.remove(
                                                            "config_profile_id")
                                                        config_type = 1
                                                    else:
                                                        column_list.remove(
                                                            "host_id")
                                                        config_type = 0
                                                    if "timestamp" in column_list:
                                                        column_list.remove(
                                                            "timestamp")

                                                        timestamp = 1
                                                    else:
                                                        timestamp = 0
                                                    if j == "basicACLconfigTable" and j == "aclMacTable":  # previously and is or
                                                        sqlalche_obj.db.execute(
                                                            "delete from %s where config_profile_id = '%s' " % (tablename, host_data[0].config_profile_id))
                                                        time.sleep(1)
                                                        for row in result['result']:
                                                            sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" % (
                                                                tablename, host_data[0].config_profile_id, str(result["result"][row])[1:-1]))
                                                    else:
                                                        if len(sqlalche_table_result) > 0:
                                                            for row in result['result']:
                                                                for val in range(0, len(result['result'][row])):
                                                                    setattr(sqlalche_table_result[row -
                                                                            1], column_list[val], str(result['result'][row][val]))
                                                                    if timestamp == 1:
                                                                        setattr(sqlalche_table_result[row - 1],
                                                                                "timestamp", time_stamp[:time_stamp.find('.') - 1])
                                                        else:
                                                            for row in result['result']:
                                                                if config_type == 1:
                                                                    sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" % (
                                                                        tablename, host_data[0].config_profile_id, str(result["result"][row])[1:-1]))
                                                                else:
                                                                    if timestamp == 0:
                                                                        sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s)" % (
                                                                            tablename, host_id, str(result["result"][row])[1:-1]))
                                                                    else:
                                                                        sqlalche_obj.db.execute("Insert into %s values(NULL,%s,%s,'%s')" % (tablename, host_id, str(
                                                                            result["result"][row])[1:-1], time_stamp[:time_stamp.find('.') - 1]))
                                        if len(rec_not_done) > 0:
                                            sqlalche_obj.db.execute("Update ap25_oid_table set status = 0 where table_name in ('%s')" %
                                                                    ("\',\'".join(rec_not_done)))

                                        if len(rec_done) > 0:
                                            a = str(current_time)
                                            sqlalche_obj.db.execute("Update ap25_oid_table set status = 1,timestamp='%s' where table_name in ('%s')" %
                                                                    (a[:a.find('.') - 1], "\',\'".join(rec_done)))
                                        rec_per = (
                                            float(rec) / float(total_rec))
                                        rec_per = int(rec_per * 100)
                                        host_data[0].reconcile_health = rec_per
                                        host_data[0].reconcile_status = 2
                                        sqlalche_obj.session.commit()
                                        el = EventLog()
                                        el.log_event(
                                            "Device Reconcilation Done", "%s" % (user_name))
                                        result = {"success": 0, "result":
                                            {rec_per: [host_data[0].host_alias, host_data[0].ip_address]}}
                                        return
                                    else:
                                        result = {'success': 1, 'result': " Reconciliation of device configuration data has been completed successfully %s You can reinitiate the process after %s minutes" % (str(time_delay), str(time_diff))}
                                        return
                                else:
                                    result = {'success': 1, 'result':
                                        "UNMP Server is busy.Please try after some time,1200"}
                                    return
                            else:
                                if int(ping_chk) == 2:
                                    result = {
                                        'success': 1, 'result': "Network is unreachable"}
                                else:
                                    result = {'success': 1, 'result': "Reconciliation not done.No response from device " + str(host_data[0]
                                                                                                                             .host_alias) + "(" + str(host_data[0].ip_address + ")")}
                                return
                        else:
                            result = {'success': 1, 'result':
                                "UNMP Server is busy.Please try after some time,1100"}
                            return
                    else:
                        result = {'success': 1, 'result': "Device is busy, Device " + host_status_dic.get(
                            int(host_op_status), 'Other Operation') + " is in progress. please wait ..."}
                        return
                else:
                    result = {'success': 1, 'result':
                        "UNMP Server is busy.Please try after some time,1000"}
                    return
            else:
                result = {'success': 1, 'result': "Host Not Exist"}
                return
        except Exception as e:
            result = {"success": 1, "result":
                "UNMP Server is busy.Please try after some time %s" % str(e)}
            return
        finally:
            if chcek_flag == 1:
                essential_obj.host_status(host_id, 0, None, 10)
            if len(host_data) > 0:
                host_data[0].reconcile_status = 0
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    ####################### Device Reconciliation with isReconciliation reconc
    def default_configuration_added(self, host_id, device_type_id, table_prefix, current_time, user_name, reconcile_chk=True):
        """

        @param host_id:
        @param device_type_id:
        @param table_prefix:
        @param current_time:
        @param user_name:
        @param reconcile_chk:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        new_profile = Odu16ConfigProfiles(
            device_type_id, "APConfiguration", "Master",
                                          None, datetime.now(), None, datetime.now(), None, 0)
        sqlalche_obj.session.add(new_profile)
        sqlalche_obj.session.flush()
        sqlalche_obj.session.refresh(new_profile)
        new_profile_id = new_profile.config_profile_id
        reconcile_per = 0
        default_profile_id = sqlalche_obj.session.query(Odu16ConfigProfiles.config_profile_id)\
            .filter(and_(Odu16ConfigProfiles.device_type_id == device_type_id, Odu16ConfigProfiles.config_profile_type_id == "default")).all()

        if len(default_profile_id) == 0:
            return new_profile_id, 0
        else:
            ipdata = sqlalche_obj.session.query(Ap25AccesspointIPsettings).filter(
                Ap25AccesspointIPsettings.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(ipdata) > 0:
                for i in range(0, len(ipdata)):
                    ip_add_row = Ap25AccesspointIPsettings(
                        new_profile_id, "" if ipdata[
                            i].lanIPaddress == None else ipdata[
                                i].lanIPaddress,
                                                           "" if ipdata[i].lanSubnetMask == None else ipdata[
                                                               i].lanSubnetMask,
                                                           "" if ipdata[i].lanGatewayIP == None else ipdata[
                                                               i].lanGatewayIP,
                                                           "" if ipdata[i].lanPrimaryDNS == None else ipdata[
                                                               i].lanPrimaryDNS,
                                                           "" if ipdata[i].lanSecondaryDNS == None else ipdata[i].lanSecondaryDNS)
                    sqlalche_obj.session.add(ip_add_row)

            vapselection_data = sqlalche_obj.session.query(Ap25VapSelection).filter(
                Ap25VapSelection.config_profile_id == default_profile_id[0].config_profile_id).all()
            vap_selection_id = []
            if len(vapselection_data) > 0:
                for i in range(0, len(vapselection_data)):
                    vapselection_add_row = Ap25VapSelection(
                        new_profile_id, vapselection_data[i].totalVAPsPresent, vapselection_data[i].selectVap)
                    sqlalche_obj.session.add(vapselection_add_row)
                    sqlalche_obj.session.flush()
                    sqlalche_obj.session.refresh(vapselection_add_row)
                    vap_selection_id.append(
                        vapselection_add_row.ap25_vapSelection_id)
            # print "hello"
            vapsecurity_data = sqlalche_obj.session.query(Ap25BasicVAPsecurity).filter(
                Ap25BasicVAPsecurity.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(vapsecurity_data) > 0:
                for i in range(0, len(vapsecurity_data)):
                    vapsecurity_add_row = Ap25BasicVAPsecurity(
                        new_profile_id, vap_selection_id[i], vapsecurity_data[i].vapSecurityMode)
                    sqlalche_obj.session.add(vapsecurity_add_row)
            # print "hello12"
            basicvapsetup_data = sqlalche_obj.session.query(Ap25BasicVAPconfigTable).filter(
                Ap25BasicVAPconfigTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(basicvapsetup_data) > 0:
                for i in range(0, len(basicvapsetup_data)):
                    basicvapsetup_add_row = Ap25BasicVAPconfigTable(
                        new_profile_id, vap_selection_id[
                            i], basicvapsetup_data[i].vapESSID,
                                                                    basicvapsetup_data[
                                                                        i].vapHiddenESSIDstate, basicvapsetup_data[i].vapRTSthresholdValue,
                                                                    basicvapsetup_data[
                                                                        i].vapFragmentationThresholdValue,
                                                                    basicvapsetup_data[i].vapBeaconInterval, basicvapsetup_data[i].vlanId,
                                                                    basicvapsetup_data[
                                                                        i].vlanPriority,
                                                                    basicvapsetup_data[i].vapMode, basicvapsetup_data[i].vapSecurityMode)
                    sqlalche_obj.session.add(basicvapsetup_add_row)
            # print "hello123"
            wepsecurity_data = sqlalche_obj.session.query(Ap25VapWEPsecurityConfigTable).filter(
                Ap25VapWEPsecurityConfigTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(wepsecurity_data) > 0:
                for i in range(0, len(wepsecurity_data)):
                    wepsecurity_add_row = Ap25VapWEPsecurityConfigTable(
                        new_profile_id, wepsecurity_data[i].vapWEPmode, 1,
                                                                        wepsecurity_data[i].vapWEPprimaryKey, wepsecurity_data[i].vapWEPkey1,
                                                                        wepsecurity_data[i].vapWEPkey2, wepsecurity_data[i].vapWEPkey3, wepsecurity_data[i].vapWEPkey4)
                    sqlalche_obj.session.add(wepsecurity_add_row)
            # print "hello14"
            acl_data = sqlalche_obj.session.query(Ap25AclMacTable).filter(
                Ap25AclMacTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(acl_data) > 0:
                for i in range(0, len(acl_data)):
                    acl_add_row = Ap25AclMacTable(
                        new_profile_id, vap_selection_id[i], acl_data[i].macaddress)
                    sqlalche_obj.session.query(acl_add_row)
            # print "hello15"
            basicacl_data = sqlalche_obj.session.query(Ap25BasicACLconfigTable).filter(
                Ap25BasicACLconfigTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(basicacl_data) > 0:
                for i in range(0, len(basicacl_data)):
                    basicacl_add_row = Ap25BasicACLconfigTable(
                        new_profile_id, vap_selection_id[i], basicacl_data[i].aclState, basicacl_data[i].aclMode)
                    sqlalche_obj.session.add(basicacl_add_row)
            # print "hello16"
            dhcp_data = sqlalche_obj.session.query(Ap25DhcpServer).filter(
                Ap25DhcpServer.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(dhcp_data) > 0:
                for i in range(0, len(dhcp_data)):
                    dhcp_add_row = Ap25DhcpServer(
                        new_profile_id, dhcp_data[i].dhcpServerStatus, dhcp_data[
                            i].dhcpStartIPaddress, dhcp_data[
                                i].dhcpEndIPaddress,
                                                  dhcp_data[i].dhcpSubnetMask, dhcp_data[i].dhcpClientLeaseTime)

                    sqlalche_obj.session.add(dhcp_add_row)
            # print "hello56"
            radioselection_data = sqlalche_obj.session.query(Ap25RadioSelection).filter(
                Ap25RadioSelection.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(radioselection_data) > 0:
                for i in range(0, len(radioselection_data)):
                    radioselection_row_add = Ap25RadioSelection(
                        new_profile_id, radioselection_data[i].radio)
                    sqlalche_obj.session.add(radioselection_row_add)
            # print "hello67"
            radiosetup_data = sqlalche_obj.session.query(Ap25RadioSetup).filter(
                Ap25RadioSetup.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(radiosetup_data) > 0:
                for i in range(0, len(radiosetup_data)):
                    radiosetup_row_add = Ap25RadioSetup(
                        new_profile_id, radiosetup_data[
                            i].radioState, radiosetup_data[i].radioAPmode,
                                                        radiosetup_data[
                                                            i].radioManagementVLANstate, radiosetup_data[i].radioCountryCode, radiosetup_data[i].numberOfVAPs,
                                                        radiosetup_data[i].radioChannel, radiosetup_data[
                                                            i].wifiMode, radiosetup_data[i].radioTxPower,
                                                        radiosetup_data[
                                                            i].radioGatingIndex, radiosetup_data[i].radioAggregation, radiosetup_data[i].radioAggFrames,
                                                        radiosetup_data[
                                                            i].radioAggSize,
                                                        radiosetup_data[i].radioAggMinSize, radiosetup_data[
                                                            i].radioChannelWidth,
                                                        radiosetup_data[i].radioTXChainMask, radiosetup_data[i].radioRXChainMask)
                    sqlalche_obj.session.add(radiosetup_row_add)
            # print "hello78"
            service_data = sqlalche_obj.session.query(Ap25Services).filter(
                Ap25Services.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(service_data) > 0:
                for i in range(0, len(service_data)):
                    service_data_add_row = Ap25Services(
                        new_profile_id, service_data[
                            i].upnpServerStatus, service_data[
                                i].systemLogStatus,
                                                        service_data[i].systemLogIP, service_data[i].systemLogPort, service_data[i].systemTime)

                    sqlalche_obj.session.add(service_data_add_row)
            # print "hello90"
            wpa_data = sqlalche_obj.session.query(Ap25VapWPAsecurityConfigTable).filter(
                Ap25VapWPAsecurityConfigTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(wpa_data) > 0:
                for i in range(0, len(wpa_data)):
                    wpa_add_row = Ap25VapWPAsecurityConfigTable(
                        new_profile_id, vap_selection_id[
                            i], wpa_data[
                                i].vapWPAmode, wpa_data[i].vapWPAcypher,
                                                                wpa_data[
                                                                    i].vapWPArekeyInterval, wpa_data[i].vapWPAmasterReKey, wpa_data[i].vapWEPrekeyInt,
                                                                wpa_data[i].vapWPAkeyMode, wpa_data[
                                                                    i].vapWPAconfigPSKPassPhrase, wpa_data[i].vapWPArsnPreAuth,
                                                                wpa_data[i].vapWPArsnPreAuthInterface, wpa_data[
                                                                    i].vapWPAeapReAuthPeriod,
                                                                wpa_data[i].vapWPAserverIP, wpa_data[i].vapWPAserverPort, wpa_data[i].vapWPAsharedSecret)
                    sqlalche_obj.session.add(wpa_add_row)
            # print "hello10"
            basicconfiguration_data = sqlalche_obj.session.query(Ap25BasicConfiguration).filter(
                Ap25BasicConfiguration.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(basicconfiguration_data) > 0:
                for i in range(0, len(basicconfiguration_data)):
                    basicconfig_add_row = Ap25BasicConfiguration(
                        new_profile_id, basicconfiguration_data[i].accesspointName)
                    sqlalche_obj.session.add(basicconfig_add_row)
            aclstats_data = sqlalche_obj.session.query(Ap25AclStatisticsTable).filter(
                Ap25AclStatisticsTable.config_profile_id == default_profile_id[0].config_profile_id).all()
            if len(aclstats_data) > 0:
                for i in range(0, len(aclstats_data)):
                    aclstats_add_row = Ap25AclStatisticsTable(
                        new_profile_id, aclstats_data[i].aclTotalsINDEX, aclstats_data[i].vapNumber, aclstats_data[i].totalMACentries)
                    sqlalche_obj.session.add(aclstats_add_row)
            # print "hello45"
            version_data = sqlalche_obj.session.query(
                Ap25Versions).filter(Ap25Versions.host_id == host_id).all()
            if len(version_data) > 0:
                for i in range(0, len(version_data)):
                    version_add_row = Ap25Versions(host_id, version_data[i].hardwareVersion, version_data[i]
                                                   .softwareVersion, version_data[i].bootLoaderVersion)
                    sqlalche_obj.session.add(version_add_row)
            # print "hello90"
            host_param = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()

            host_param[0].config_profile_id = new_profile_id
            sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            return str(new_profile_id), 0

    def reconciliation_status(self):
        """


        @return:
        """
        global sqlalche_obj
        result = {}
        rec_dir = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        rec_list = sqlalche_obj.session.query(Hosts.host_id, Hosts.reconcile_status, Hosts.reconcile_health).filter(and_(
            Hosts.device_type_id.like(UNMPDeviceType.ap25 + "%"))).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(rec_list) > 0:
            for i in range(0, len(rec_list)):
                rec_dir[str(rec_list[i][0])] = [rec_list[i][1], rec_list[i][2]]
            result = {"result": rec_dir, "success": 0}
            return result

    def reconciliation_chk_status(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        result = {}
        sqlalche_obj.sql_alchemy_db_connection_open()
        if host_id != "" or host_id != None:
            # process status
            op_status = essential_obj.get_hoststatus(host_id)
            # print op_status
            if op_status == None:
                op_img = "images/host_status0.png"
            elif op_status == 0:
                op_img = "images/host_status0.png"
            else:
                op_img = "images/host_status1.png"

            reconcile_status = sqlalche_obj.session.query(
                Hosts.reconcile_status, Hosts.reconcile_health).filter(Hosts.host_id == host_id).all()
            reconcile_update = sqlalche_obj.session.query(
                Hosts).filter(Hosts.host_id == host_id).all()
            status = reconcile_status[0].reconcile_status
            if reconcile_status[0].reconcile_status == 2:
                reconcile_update[0].reconcile_status = 0
                sqlalche_obj.session.commit()
            sqlalche_obj.sql_alchemy_db_connection_close()
            result = {"result": [status, reconcile_status[0].reconcile_health,
                op_img, 0 if op_status == None else op_status], "success": 0}
            return result
        else:
            sqlalche_obj.sql_alchemy_db_connection_close()
            result = {"result": "Host No exist", "success": 1}
            return result

    def reboot(self, host_id):
        """

        @param host_id:
        @return:
        """
        global sqlalche_obj
        result = {}
        i = 0
        global errorStatus, host_status_dic, essential_obj
        oid_dict = {}
        get_result = {}
        try:
            host_op_state = essential_obj.host_status(host_id, 5)
            if int(host_op_state) == 0:
                try:
                    sqlalche_obj.sql_alchemy_db_connection_open()
                    host_param = sqlalche_obj.session.query(
                        Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community,
                                                            Hosts.snmp_read_community).filter(Hosts.host_id == host_id).all()
                    oid_dict[1] = [
                        '1.3.6.1.4.1.26149.10.5.3.0', 'Integer32', 1]
                    if len(host_param) > 0:
                        result = single_set(host_param[0].ip_address, int(host_param[0]
                                            .snmp_port), host_param[0].snmp_write_community, oid_dict[1])
                        if result["success"] == 0:
                            time.sleep(40)
                            while(i < 10):
                                get_result = pysnmp_get(
                                    '1.3.6.1.4.1.26149.10.5.3',
                                                        host_param[0].ip_address, int(host_param[0].snmp_port), 'public')
                                if get_result["success"] == 0:
                                    result = {"success":
                                        0, "result": "Device is rebooting successfully"}
                                    return result
                                else:
                                    for k in get_result["result"]:
                                        if k != 53 and k != '53':
                                            if k in errorStatus:
                                                result = {"success": 1,
                                                    "result": errorStatus[k]}
                                                return result
                                        elif k == 51 and k == '51':
                                            if k in errorStatus:
                                                result = {"success": 1,
                                                    "result": errorStatus[k]}
                                                return result
                                        else:
                                            i = i + 1
                                            time.sleep(10)
                            result = {'success':
                                1, 'result': 'Device is Not Responding'}
                            return result
                        else:
                            for k in result["result"]:
                                if k in errorStatus:
                                    result = {"success":
                                        1, "result": errorStatus[k]}
                                    return result
                    else:
                        return {"success": 1, "result": "Host Data Not Exist"}
                finally:
                    if sqlalche_obj.error == 0:
                        sqlalche_obj.sql_alchemy_db_connection_open()
                    essential_obj.host_status(host_id, 0, None, 5)
            else:
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}
        except Exception, e:
            return {"success": 1, "result": str(e[-1])}

# obj.update_configuration(host_id,device_type,table_prefix,current_time,user_name)

# obj = Reconciliation()
# print 'jai'
# print obj.update_configuration(6,"ap25","ap25_",datetime.now(),'omdadmin')
# print obj.update_configuration(52,"ap25","ap25_",datetime.now(),"")


class DHCPClientInformation(object):
    """
    AP DHCP mode and connected clients
    """
    def ap_dhcp_client_information(self, host_id, calculate):
        """

        @param host_id:
        @param calculate:
        @return:
        """
        global sqlalche_obj, host_status_dic, essential_obj
        global errorStatus
        result = {}
        try:
            host_op_state = essential_obj.host_status(host_id, 12)
            if int(host_op_state) == 0:
                try:
                    sqlalche_obj.sql_alchemy_db_connection_open()
                    # sqlalche_obj.session.flush()
                    if int(calculate) == 0:
                        host_param = sqlalche_obj.session.query(
                            Ap25DhcpClientsTable.ap25_dhcpClientsTable_id, Ap25DhcpClientsTable.dhcpClientsMACaddress, Ap25DhcpClientsTable.dhcpClientsIPaddress,
                                                                Ap25DhcpClientsTable.dhcpClientsExpiresIn, Ap25DhcpClientsTable.timestamp).filter(Hosts.host_id == host_id).all()
                        result['success'] = 0
                        temp_dict = {}
                        for i in range(len(host_param)):
                            temp_dict[i + 1] = [host_param[i].dhcpClientsMACaddress, host_param[i]
                                .dhcpClientsIPaddress, host_param[i].dhcpClientsExpiresIn, host_param[i].timestamp]
                        result['result'] = temp_dict
                        return result
                    else:
                        host_param = sqlalche_obj.session.query(
                            Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community,
                                                                Hosts.snmp_read_community).filter(Hosts.host_id == host_id).all()
                        if len(host_param) > 0:
                            client_table = sqlalche_obj.session.query(Ap25DhcpClientsTable).filter(
                                Ap25DhcpClientsTable.host_id == host_id).all()
                            for client in client_table:
                                sqlalche_obj.session.delete(client)
                            sqlalche_obj.session.commit()
                            result = bulktable(
                                '1.3.6.1.4.1.26149.10.1.3.2.1.1', host_param[
                                    0].ip_address,
                                               int(host_param[0].snmp_port), host_param[0].snmp_read_community)
                            if result["success"] == 0:
                                for k in result['result']:
                                    result["result"][k].append(datetime.now(
                                        ).strftime('%Y %m %d %H:%M:%S'))
                                    dhcp_client_data = Ap25DhcpClientsTable(
                                        host_id, result['result'][k][0], result['result'][k][1], result['result'][k][2])
                                    sqlalche_obj.session.add(dhcp_client_data)
                                sqlalche_obj.session.commit()
                                return result
                            else:
                                for k in result["result"]:
                                    if k in errorStatus:
                                        result = {"success":
                                            1, "result": errorStatus[k]}
                                return result
                        else:
                            return "No Host Exist"
                finally:
                    if sqlalche_obj.error == 0:
                        sqlalche_obj.sql_alchemy_db_connection_open()
                        essential_obj.host_status(host_id, 0, None, 12)

            else:
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}
        except Exception, e:
            return {"success": 1, "result": str(e[-1])}


class APScan(object):
    """
    AP device functionality AP scan
    """
    def ap_scan(self, host_id, calculate):
        """

        @param host_id:
        @param calculate:
        @return:
        """
        global sqlalche_obj, host_status_dic, essential_obj
        global errorStatus
        result = {}
        try:
            host_op_state = essential_obj.host_status(host_id, 12)
            if int(host_op_state) == 0:
                try:
                    sqlalche_obj.sql_alchemy_db_connection_open()
                    # sqlalche_obj.session.flush()
                    if int(calculate) == 0:
                        host_param = sqlalche_obj.session.query(
                            Ap25ApScanDataTable.macAddress, Ap25ApScanDataTable.essid, Ap25ApScanDataTable.frequency, Ap25ApScanDataTable.quality,
                                                                Ap25ApScanDataTable.signalLevel, Ap25ApScanDataTable.noiseLevel, Ap25ApScanDataTable.beconIntervel, Ap25ApScanDataTable.Timestamp).filter(Hosts.host_id == host_id).all()
                        result['success'] = 0
                        temp_dict = {}
                        for i in range(len(host_param)):
                            temp_dict[i + 1] = [str(i), host_param[i].macAddress, host_param[i].essid, host_param[i].frequency, host_param[i].quality, host_param[i]
                                                  .signalLevel, host_param[i].noiseLevel, host_param[i].beconIntervel, str(host_param[i].Timestamp)]
                        result['result'] = temp_dict
                        return result
                    else:
                        host_param = sqlalche_obj.session.query(
                            Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community,
                                                                Hosts.snmp_read_community).filter(Hosts.host_id == host_id).all()
                        if len(host_param) > 0:
                            scan_table = sqlalche_obj.session.query(Ap25ApScanDataTable).filter(
                                Ap25ApScanDataTable.host_id == host_id).all()
                            for scan_row in scan_table:
                                sqlalche_obj.session.delete(scan_row)
                            sqlalche_obj.session.commit()
                            result = bulktable(
                                '1.3.6.1.4.1.26149.10.4.5.1.1.1', host_param[
                                    0].ip_address,
                                               int(host_param[0].snmp_port), host_param[0].snmp_read_community)
                            if result["success"] == 0:
                                for k in result["result"]:
                                    ap_scan_data = Ap25ApScanDataTable(host_id, str(result["result"][k][1]).replace(
                                        '\n', ''), result["result"][k][2], result["result"][k][3], result["result"][k][4], result["result"][k][5], result["result"][k][6], str(result["result"][k][7]).replace('\n', ''))
                                    sqlalche_obj.session.add(ap_scan_data)
                                    result["result"][k].append(datetime.now(
                                        ).strftime('%Y %m %d %H:%M:%S'))
                                sqlalche_obj.session.commit()
                                return result
                            else:
                                for k in result["result"]:
                                    if k in errorStatus:
                                        result = {"success":
                                            1, "result": errorStatus[k]}
                                return result
                        else:
                            return "No Host Exist"
                finally:
                    if sqlalche_obj.error == 0:
                        sqlalche_obj.sql_alchemy_db_connection_open()
                    essential_obj.host_status(host_id, 0, None, 12)
            else:
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}
        except Exception, e:
            return {"success": 1, "result": str(e[-1])}


class APGetData(object):
    """
    Get AP device data
    """
    def ap_get_data(self, class_name, host_id):
        """

        @param class_name:
        @param host_id:
        @return:
        """
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == "" or host_id == None:
                return []
            config_id = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
            if len(config_id) > 0:
                get_data = sqlalche_obj.session.query(eval('%s' % (class_name))).filter(eval(
                    '%s' % (class_name)).config_profile_id == '%s' % (config_id[0].config_profile_id)).all()
                if len(get_data) > 0:
                    return get_data
                else:
                    return []
            else:
                return []
        except Exception as e:
            return e
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()

# obj = APGetData()
# ad=obj.ap_get_data('Ap25VapWPAsecurityConfigTable',5)
# for row in ad:
#	print row


class APCommonSetValidation(object):
    """
    Validation for AP forms
    """

    def common_set_config(self, host_id, device_type_id, dic_result, id=None, index=0, special_case=0):
    # dic_result = {'success':0,'result':{'ru.omcConfTable.omcIpAddress':[1,'Not Done'],'ru.omcConfTable.periodicStatsTimer':[1,'Not Done']}}
    # return dic_result
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param index:
        @param special_case:
        @return:
        """
        try:
            global sqlalche_obj, essential_obj, host_status_dic
            sqlalche_obj.sql_alchemy_db_connection_open()
            success_result = {"success": '', "result": {}}
            global errorStatus
            o1 = aliased(Ap25Oids)
            table_name = "Ap25Oids"
            o2 = aliased(Ap25Oids)
            rowSts = {'ru.ra.raAclConfigTable.rowSts': [
                '1.3.6.1.4.1.26149.2.2.13.5.1.3', 'Integer32', '']}
            query_result = []
            oid_admin_state = {"1": -1}
            independent_oid = []
            dependent_oid = []
            depend_oid_value = []
            result = {}
            key = ""
            exist_data = 0
            host_op_state = essential_obj.host_status(host_id, 12)
            # temp_str=''
            if int(host_op_state) == 0:
                for keys in dic_result.iterkeys():
                    # temp_str=str(temp_str)+' in lop'
                    if keys == "success":
                        continue
                    else:
                        query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                            o1, o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                        # temp_str=str(temp_str)+' %s '%query_result
                        if len(query_result) > 0:
                            if query_result[0][0].dependent_id == "" or query_result[0][0].dependent_id == None:
                                independent_oid.append({keys: [query_result[0][0].oid +
                                                       query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                # temp_str=str(temp_str)+' first '
                            else:
                                # temp_str=str(temp_str)+' first else '
                                if len(dependent_oid) > 0:
                                    for i in range(0, len(dependent_oid)):
                                        if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                            admin_state = 'ru.ruConfTable.adminstate'
                                        elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                            admin_state = 'ru.ipConfigTable.adminState-1'
                                        elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                            admin_state = 'ru.ra.raConfTable.raAdminState-1'
                                        else:
                                            admin_state = query_result[0][1]
                                        if admin_state in dependent_oid[i]:
                                            pos = i
                                            if len(depend_oid_value) > 0:
                                                depend_oid_value[pos][keys] = [query_result[
                                                    0][0].oid + query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]
                                                break
                                            else:
                                                depend_oid_value.append({keys: [query_result[0][0].oid + query_result[0][0]
                                                                        .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                                break
                                        else:
                                            if i == len(dependent_oid) - 1:
                                                if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                                    dependent_oid.append({query_result[0][1] + str(
                                                        -1): [query_result[0][2] + query_result[0][3]]})
                                                    depend_oid_value.append({keys: [query_result[0][0].oid + query_result[
                                                                            0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                                elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                                    dependent_oid.append({query_result[0][1] + str(
                                                        -1): [query_result[0][2] + query_result[0][3]]})
                                                    depend_oid_value.append({keys: [query_result[0][0].oid + query_result[
                                                                            0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                                elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                                    dependent_oid.append({query_result[0][1] + str(
                                                        -1): [query_result[0][2] + query_result[0][3]]})
                                                    depend_oid_value.append({keys: [query_result[0][0].oid + query_result[
                                                                            0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                                else:
                                                    dependent_oid.append({query_result[0][1]
                                                                         : [query_result[0][2] + query_result[0][3]]})
                                                    depend_oid_value.append({keys: [query_result[0][0].oid + query_result[
                                                                            0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                            else:
                                                continue
                                else:
                                    if query_result[0][1] == 'ru.ruConfTable.adminstate':
                                        dependent_oid.append({query_result[0][1] + str(
                                            -1): [query_result[0][2] + query_result[0][3]]})
                                        depend_oid_value.append({keys: [query_result[0][0].oid +
                                                                query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                    elif query_result[0][1] == 'ru.ipConfigTable.adminState':
                                        dependent_oid.append({query_result[0][1] + str(
                                            -1): [query_result[0][2] + query_result[0][3]]})
                                        depend_oid_value.append({keys: [query_result[0][0].oid +
                                                                query_result[0][0].indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                    elif query_result[0][1] == 'ru.ra.raConfTable.raAdminState':
                                        dependent_oid.append({query_result[0][1] + str(
                                            -1): [query_result[0][2] + query_result[0][3]]})
                                        depend_oid_value.append({keys: [query_result[0][0].oid + query_result[0][0]
                                                                .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                                    else:
                                        dependent_oid.append(
                                            {query_result[0][1]: [query_result[0][2] + query_result[0][3]]})
                                        depend_oid_value.append({keys: [query_result[0][0].oid + query_result[0][0]
                                                                .indexes, query_result[0][0].oid_type, dic_result[keys]]})
                        else:
                            success_result["success"] = 1
                            success_result[
                                "result"] = "There is no row in database"

                pos = len(depend_oid_value)
                if pos != 0:
                    # temp_str=str(temp_str)+' pos'
                    for i in range(0, len(independent_oid)):
                        depend_oid_value[pos - 1].update(independent_oid[i])
                else:
                    # temp_str=str(temp_str)+' pos else %s '%independent_oid
                    for i in range(0, len(independent_oid)):
                        depend_oid_value.append(independent_oid[i])
                device_param_list = sqlalche_obj.session.query(Hosts.ip_address, Hosts.snmp_port, Hosts.snmp_write_community, Hosts.config_profile_id).\
                    filter(Hosts.host_id == host_id).one()
                j = -1
                if len(dependent_oid) > 0:
                    # temp_str=str(temp_str)+' second if'
                    for i in range(0, len(dependent_oid)):
                        j += 1
                        if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                            result = (
                                pysnmp_seter(
                                    depend_oid_value[i], device_param_list[0],
                                      device_param_list[1], device_param_list[2], dependent_oid[i]))
                        elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                            result = (
                                pysnmp_seter(
                                    depend_oid_value[i], device_param_list[0],
                                      device_param_list[1], device_param_list[2], dependent_oid[i]))
                        elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                            result = (
                                pysnmp_seter(
                                    depend_oid_value[i], device_param_list[0],
                                      device_param_list[1], device_param_list[2], dependent_oid[i]))
                        else:
                            result = pysnmp_seter(depend_oid_value[i], device_param_list[0], device_param_list[
                                                  1], device_param_list[2], dependent_oid[i])
                        if result["success"] == 0 or result["success"] == '0':
                            success_result["success"] = result["success"]
                            for i in result["result"]:
                                if result["result"][i] != 0:
                                    result["result"][
                                        i] = errorStatus[result["result"][i]]
                                else:
                                    oid_list_table_field_value = sqlalche_obj.session.query(
                                        Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()
                                    if len(oid_list_table_field_value) == 0:
                                        continue
                                    else:

                                        if i in dic_result:
                                            table_name = "ap25_" + \
                                                oid_list_table_field_value[
                                                    0][0]
                                            table_name = rename_tablename(
                                                table_name)
                                            exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                table_name, table_name, device_param_list[3])
                                            exec "table_result[0].%s = '%s'" % (
                                                oid_list_table_field_value[0][1], dic_result[i])
                                            if ("ap25_" + oid_list_table_field_value[0][0]) == "odu100_ipConfigTable":
                                                host_data = sqlalche_obj.session.query(
                                                    Hosts).filter(Hosts.config_profile_id == device_param_list[3]).all()
                                                if i == "ru.ipConfigTable.ipAddress":
                                                    host_data[
                                                        0].ip_address = dic_result[i]
                                                if i == "ru.ipConfigTable.ipNetworkMask":
                                                    host_data[
                                                        0].netmask = dic_result[i]
                                                if i == "ru.ipConfigTable.ipDefaultGateway":
                                                    host_data[
                                                        0].gateway = dic_result[i]
                                            sqlalche_obj.session.commit()
                            success_result["result"].update(result["result"])
                        else:
                            success_result["success"] = 1
                            for i in result["result"]:
                                i in errorStatus
                                success_result["result"] = errorStatus[i]

                if len(dependent_oid) > 0:
                    # temp_str=str(temp_str)+' thired if'
                    for i in range(0, len(dependent_oid)):
                        query_admin_result = sqlalche_obj.session.query(Ap25Oids.oid, Ap25Oids.oid_type, Ap25Oids.indexes).filter(
                            Ap25Oids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                        if 'ru.ruConfTable.adminstate-1' in dependent_oid[i]:
                            admin_state = "ru.ruConfTable.adminstate"
                            query_admin_result = sqlalche_obj.session.query(
                                Ap25Oids.oid, Ap25Oids.oid_type, Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ruConfTable.adminstate").one()
                            dic_admin_value = {"ru.ruConfTable.adminstate": [query_admin_result[0] +
                                query_admin_result[2], query_admin_result[1], '1']}
                            if len(query_admin_result) > 0:
                                result = pysnmp_seter(
                                    dic_admin_value, device_param_list[0],
                                                      device_param_list[1], device_param_list[2])
                                if result["success"] == 0 or result["success"] == '0':
                                    success_result[
                                        "success"] = result["success"]
                                    for i in result["result"]:
                                        if result["result"][i] != 0:
                                            result["result"][i] = errorStatus[
                                                result["result"][i]]
                                        else:
                                            oid_list_table_field_value = sqlalche_obj.session.query(
                                                Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()
                                            if len(oid_list_table_field_value) == 0:
                                                continue
                                            else:
                                                if i in dic_result:
                                                    table_name = "ap25_" + \
                                                        oid_list_table_field_value[
                                                            0][0]
                                                    table_name = rename_tablename(
                                                        table_name)
                                                    exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                        table_name, table_name, device_param_list[3])

                                                    exec "table_result[0].%s = '%s'" % (
                                                        oid_list_table_field_value[0][1], dic_result[i])
                                                sqlalche_obj.session.commit()
                                    # success_result["result"].update(result["result"])
                                else:
                                    # success_result["success"] = 1
                                    for i in result["result"]:
                                        result["result"][i] in errorStatus
                                        # success_result["result"] =
                                        # errorStatus[result["result"][i]]

                        elif 'ru.ipConfigTable.adminState-1' in dependent_oid[i]:
                            query_admin_result = sqlalche_obj.session.query(
                                Ap25Oids.oid, Ap25Oids.oid_type, Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ipConfigTable.adminState").one()
                            dic_admin_value = {"ru.ipConfigTable.adminState": [
                                query_admin_result[0] + query_admin_result[2], query_admin_result[1], '1']}
                            if len(query_admin_result) > 0:
                                result = pysnmp_seter(
                                    dic_admin_value, device_param_list[0],
                                                      device_param_list[1], device_param_list[2])
                                if result["success"] == 0 or result["success"] == '0':
                                    success_result[
                                        "success"] = result["success"]
                                    for i in result["result"]:
                                        if result["result"][i] != 0:
                                            result["result"][i] = errorStatus[
                                                result["result"][i]]
                                        else:
                                            oid_list_table_field_value = sqlalche_obj.session.query(
                                                Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()
                                            if len(oid_list_table_field_value) == 0:
                                                continue
                                            else:
                                                if i in dic_result:

                                                    table_name = "ap25_" + \
                                                        oid_list_table_field_value[
                                                            0][0]
                                                    table_name = rename_tablename(
                                                        table_name)
                                                    exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                        table_name, table_name, device_param_list[3])
                                                    exec "table_result[0].%s = '%s'" % (oid_list_table_field_value[0][
                                                                                        1], dic_result[i])
                                    # success_result["result"] =
                                    # errorStatus[result["result"][i]]
                                else:
                                    # success_result["success"] = 1
                                    for i in result["result"]:
                                        result["result"][i] in errorStatus
                                        # success_result["result"] =
                                        # errorStatus[result["result"][i]]
                        elif 'ru.ra.raConfTable.raAdminState-1' in dependent_oid[i]:
                            query_admin_result = sqlalche_obj.session.query(
                                Ap25Oids.oid, Ap25Oids.oid_type, Ap25Oids.indexes).filter(Ap25Oids.oid_name == "ru.ra.raConfTable.raAdminState").one()
                            dic_admin_value = {"ru.ra.raConfTable.raAdminState": [
                                query_admin_result[0] + query_admin_result[2], query_admin_result[1], '1']}
                            if len(query_admin_result) > 0:
                                result = pysnmp_seter(dic_admin_value, device_param_list[
                                                      0], device_param_list[1], device_param_list[2])
                                if result["success"] == 0 or result["success"] == '0':
                                    success_result[
                                        "success"] = result["success"]
                                    for i in result["result"]:
                                        if result["result"][i] != 0:
                                            result["result"][i] = errorStatus[
                                                result["result"][i]]
                                        else:
                                            oid_list_table_field_value = sqlalche_obj.session.query(
                                                Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()
                                            if len(oid_list_table_field_value) == 0:
                                                continue
                                            else:
                                                if i in dic_result:
                                                    table_name = "ap25_" + \
                                                        oid_list_table_field_value[
                                                            0][0]
                                                    table_name = rename_tablename(
                                                        table_name)
                                                    exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                        table_name, table_name, device_param_list[3])
                                                    exec "table_result[0].%s = '%s'" % (
                                                        oid_list_table_field_value[0][1], dic_result[i])
                                    # success_result["result"].update(result["result"])
                                else:
                                    for i in result["result"]:
                                        result["result"][i] in errorStatus
                                        # success_result["result"] =
                                        # errorStatus[result["result"][i]]
                            break
                        else:
                            continue
                if(j == -1):
                    if len(depend_oid_value) > 0:
                        # temp_str=str(temp_str)+' 4 if'
                        dic_oid = {}
                        # temp_str=str(temp_str)+' 4 if %s '%depend_oid_value
                        for i in range(0, len(depend_oid_value)):
                            dic_oid.update(depend_oid_value[i])
                        if id != None:
                            for key in depend_oid_value[i]:
                                oid = depend_oid_value[i][key][0][0:-1]
                                depend_oid_value[
                                    i][key][0] = str(oid) + str(id)
                        result = pysnmp_seter(dic_oid, device_param_list[0],
                                              device_param_list[1], device_param_list[2])
                        # return
                        # {'success':1,'reew':str(result),'dic_oid':dic_oid}
                        if result["success"] == 0 or result["success"] == '0':
                            success_result["success"] = result["success"]
                            for i in result["result"]:
                                if result["result"][i] != 0:
                                    result["result"][
                                        i] = errorStatus[result["result"][i]]
                                else:
                                    oid_list_table_field_value = sqlalche_obj.session.query(
                                        Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()
                                    oid_list_table_field_value1 = sqlalche_obj.session.query(
                                        Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id))
                                        # if i=='radioSetup.radioCountryCode':
                                        # return
                                        # {'success':1,'devi':str(oid_list_table_field_value),'qy':str(oid_list_table_field_value1)}
                                    if len(oid_list_table_field_value) == 0:
                                        continue
                                    else:
                                        if i in dic_result:
                                            sql_table_name = "ap25_" + \
                                                oid_list_table_field_value[
                                                    0][0]
                                            tableName = sql_table_name + "_id"
                                            table_name = rename_tablename(
                                                sql_table_name)
                                            if index != 0:
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(and_(%s.%s==%s,%s.config_profile_id == \"%s\")).all()" % (
                                                    table_name, table_name, tableName, index, table_name, device_param_list[3])
                                            else:
                                                exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").all()" % (
                                                    table_name, table_name, device_param_list[3])
                                                # exec "table_result = sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\")"%(table_name,table_name,device_param_list[3])
                                            # return
                                            # {'success':1,'res':str(table_result)}
                                            if len(table_result) > 0:
                                                if special_case != 0 and special_case != '0':
                                                    exec "sqlalche_obj.session.query(%s).filter(%s.config_profile_id == \"%s\").update({'%s':%s})" % (
                                                        table_name, table_name, device_param_list[3], oid_list_table_field_value[0][1], dic_result[i])
                                                else:
                                                    exec "table_result[0].%s = '%s'" % (
                                                        oid_list_table_field_value[0][1], dic_result[i])
                                            else:
                                                exist_data = 1
                            if exist_data == 1:
                                success_result["success"] = 1
                                success_result[
                                    "result"] = "Reconcilation process has exited. \n Please retry."
                            else:
                                success_result[
                                    "result"].update(result["result"])
                        else:
                            if 553 in result["result"]:
                                return {"success": 1, "result": "No Response From Device.Please Try Again"}
                            elif 53 in result["result"]:
                                return {"success": 1, "result": "No Response From Device.Please Try Again"}
                            elif 551 in result["result"]:
                                return {"success": 1, "result": "Network is unreachable"}
                            elif 99 in result["result"]:
                                return {"success": 1, "result": "UNMP has encountered an unexpected error. Please Retry"}
                            else:
                                success_result["success"] = 0
                                for i in result["result"]:
                                    if result["result"][i] != 0:
                                        if result["result"][i] in errorStatus:
                                            result["result"][i] = errorStatus[
                                                result["result"][i]]
                                success_result[
                                    "result"].update(result["result"])

                sqlalche_obj.session.commit()
                sqlalche_obj.sql_alchemy_db_connection_close()
                return success_result
                # return temp_str
            else:
                op_status = essential_obj.get_hoststatus(host_id)
                if op_status == None:
                    op_img = "images/host_status0.png"
                elif op_status == 0:
                    op_img = "images/host_status0.png"
                else:
                    op_img = "images/host_status1.png"
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ...",
                        'op_image': op_img, 'op_status': 0 if op_status == None else op_status}

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occurs", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            essential_obj.host_status(host_id, 0, None, 12)

    def common_validation(self, host_id, device_type_id, dic_result, id=None, index=0, special_case=0):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param id:
        @param index:
        @param special_case:
        @return:
        """
        try:
            obj_set = APCommonSetValidation()
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            temp_dic = {}
            if dic_result["success"] == '0' or dic_result["success"] == 0:
                for keys in dic_result.iterkeys():
                    if keys == "success":
                        continue
                    else:
                        oid_list_min_max_value = sqlalche_obj.session.query(
                            Ap25Oids.min_value, Ap25Oids.max_value).filter(and_(Ap25Oids.oid_name == keys, Ap25Oids.device_type_id == device_type_id)).all()
                        temp_dic[keys] = oid_list_min_max_value
                        if len(oid_list_min_max_value) == 0:
                            flag = 1
                            continue
                        else:
                            if (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (oid_list_min_max_value[0][1] != "" and oid_list_min_max_value[0][1] != None):
                                if int(dic_result[keys]) <= int(oid_list_min_max_value[0][1]):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "The value is large than %s" % (
                                        oid_list_min_max_value[1])
                                    break
                            elif (oid_list_min_max_value[0][0] != "" or oid_list_min_max_value[0][0] != None) and (oid_list_min_max_value[0][1] == "" and oid_list_min_max_value[0][1] == None):
                                if int(dic_result[keys]) >= int(oid_list_min_max_value[0][0]):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "The value is smaller than %s" % (
                                        oid_list_min_max_value[0][0])
                                    break
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == None) and (oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == None):
                                dic_result["%s" % (keys)] = dic_result[keys]
                            elif (oid_list_min_max_value[0][0] == "" or oid_list_min_max_value[0][0] == 'NULL') and (oid_list_min_max_value[0][1] == "" or oid_list_min_max_value[0][1] == 'NULL'):
                                dic_result["%s" % (keys)] = dic_result[keys]
                            else:
                                if (int(dic_result[keys]) >= int(oid_list_min_max_value[0][0])) and (int(dic_result[keys]) <= int(oid_list_min_max_value[0][1])):
                                    dic_result[
                                        "%s" % (keys)] = dic_result[keys]
                                else:
                                    dic_result = {}
                                    flag = 1
                                    dic_result["result"] = "%s Value must be in between %s and %s" % (keys.split(
                                        ".")[-1], oid_list_min_max_value[0][0], oid_list_min_max_value[0][1])
                                    break
                if flag == 1:
                    dic_result["success"] = 1
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    return dic_result
                else:
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    dic_result = obj_set.common_set_config(
                        host_id, device_type_id, dic_result, id, index, special_case=0)
                    return dic_result
            else:
                sqlalche_obj.sql_alchemy_db_connection_close()
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            dic_result["success"] = 1
            dic_result["result"] = str(e)
            return str(e)

    def ap_cancel_form(self, host_id, device_type_id, dic_result):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @return:
        """
        try:
            flag = 0
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            success_result = {}
            profile_id = sqlalche_obj.session.query(
                Hosts.config_profile_id).filter(Hosts.host_id == host_id).one()
            if dic_result["success"] == 0:
                for keys in dic_result:
                    if keys == "success":
                        continue
                    else:
                        oid_list_table_field_value = sqlalche_obj.session.query(
                            Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == keys, Ap25Oids.device_type_id == device_type_id)).all()

                        table_name = "ap25_" + oid_list_table_field_value[0][0]
                        table_name = rename_tablename(table_name)
                        str_table_obj = "table_result = sqlalche_obj.session.query(%s.%s).filter(%s.config_profile_id == \"%s\").all()" % (
                            table_name, oid_list_table_field_value[0][1], table_name, profile_id[0])
                        exec str_table_obj
                        if len(table_result) > 0:
                            for i in range(0, len(table_result)):
                                dic_result[keys] = str(table_result[i][0])
                        else:
                            dic_result = {}
                            dic_result["success"] = 1
                            dic_result["result"] = "Data Not Exixt"
                sqlalche_obj.sql_alchemy_db_connection_close()
                return dic_result
        except Exception as e:
            sqlalche_obj.sql_alchemy_db_connection_close()
            dic_result["success"] = 1
            dic_result["result"] = str(e[-1])
            return dic_result

    def basic_acl_set(self, host_id, device_type_id, dic_result):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @return:
        """
        try:
            global sqlalche_obj, essential_obj, host_status_dic
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            global errorStatus
            o1 = aliased(Ap25Oids)
            table_name = "Ap25Oids"
            o2 = aliased(Ap25Oids)
            result = {}
            independent_oid = []
            depend_oid_value = []
            set_vap_acl = {}
            basic_acl = {}
            host_op_state = essential_obj.host_status(host_id, 12)
            if int(host_op_state) == 0:
                host_data = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                select_vpa_data = []
                for keys in dic_result.iterkeys():
                    if keys == "success" or keys == "vap_selection_id":
                        continue
                    else:
                        query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                            o1, o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()
                        if len(query_result) > 0:
                            independent_oid.append({keys: [query_result[0][0].oid + str(
                                ".") + str(dic_result["vapSelection.selectVap"]), query_result[0][0].oid_type, dic_result[keys]]})

                for i in independent_oid:
                    for keys in i.iterkeys():
                        if keys == "vapSelection.selectVap":
                            set_vap_acl = i
                        else:
                            basic_acl.update(i)

                result = pysnmp_seter(basic_acl, host_data[0].ip_address,
                                      host_data[0].snmp_port, host_data[0].snmp_write_community)

                if result["success"] == 0 or result["success"] == '0':
                    for i in result["result"]:
                        if result["result"][i] != 0:
                            result["result"][
                                i] = errorStatus[result["result"][i]]
                        else:
                            if i in dic_result:
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()
                                if len(oid_list_table_field_value) == 0:
                                    continue
                                if i == "vapSelection.selectVap":
                                    continue
    ##                                select_vap_data = sqlalche_obj.session.query(Ap25VapSelection).filter(Ap25VapSelection.config_profile_id==host_data[0].config_profile_id).all()
    ##                                if len(select_vap_data)>0:
    ##                                    for j in range(0,len(select_vap_data)):
    # select_vap_data[j].selectVap = dic_result[i]
                                else:
                                    basic_acl_data = sqlalche_obj.session.query(Ap25BasicACLconfigTable).filter(
                                        and_(Ap25BasicACLconfigTable.vapselection_id == dic_result['vap_selection_id'], Ap25BasicACLconfigTable.config_profile_id == host_data[0].config_profile_id)).all()
                                    if len(basic_acl_data) > 0:
                                        for k in range(0, len(basic_acl_data)):
                                            if oid_list_table_field_value[0].coloumn_name == "basicACLconfigTable.aclAddMAC" or oid_list_table_field_value[0].coloumn_name == "basicACLconfigTable.aclDeleteOneMAC" or oid_list_table_field_value[0].coloumn_name == "basicACLconfigTable.aclDeleteAllMACs":
                                                continue
                                            else:
                                                exec "basic_acl_data[%s].%s = '%s'" % (
                                                    k, oid_list_table_field_value[0].coloumn_name, dic_result[i])
                    sqlalche_obj.session.commit()
                else:
                    if 53 in result["result"] or 553 in result["result"]:
                        result = {"success": 1, "result":
                            "No Response From Device.Please Try Again"}
                    elif 51 in result["result"]:
                        result = {"success": 1,
                            "result": "Network is unreachable"}
                    elif 99 in result["result"]:
                        result = {"success": 1, "result":
                            "UNMP has encountered an unexpected error. Please Retry"}
                    else:
                        for i in result['result']:
                            result = {"success": 1, "result": errorStatus.get(
                                result['result'][i], "Device is busy.Please try again later")}
                return result
            else:
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}

        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occurs", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            essential_obj.host_status(host_id, 0, None, 12)

    def vap_set(self, host_id, device_type_id, dic_result, selectedvap, vap_id):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param selectedvap:
        @param vap_id:
        @return:
        """
        try:
            global sqlalche_obj, essential_obj, host_status_dic
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            global errorStatus
            host_op_state = essential_obj.host_status(host_id, 12)
            if int(host_op_state) == 0:
                o1 = aliased(Ap25Oids)
                table_name = "Ap25Oids"
                o2 = aliased(Ap25Oids)
                result = {}
                vap_data = {}
                independent_oid = []
                host_data = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                for keys in dic_result.iterkeys():
                    if keys == "success":
                        continue
                    else:

                        query_result = sqlalche_obj.session.query(o2, o1.oid_name, o1.oid, o1.indexes).outerjoin(
                            o1, o1.oid_id == o2.dependent_id).filter(and_(o2.oid_name == keys, o2.device_type_id == device_type_id)).all()

                        if len(query_result) > 0:
                            try:
                                key = int(dic_result[keys])
                            except:
                                key = dic_result[keys]
                            if keys == "vapWEPsecurityConfigTable.vapWEPmode" or keys == "vapWEPsecurityConfigTable.vapWEPkey1" or keys == "vapWEPsecurityConfigTable.vapWEPkey2"\
                               or keys == "vapWEPsecurityConfigTable.vapWEPkey3" or keys == "vapWEPsecurityConfigTable.vapWEPkey4" or keys == "vapWEPsecurityConfigTable.vapWEPprimaryKey":
                                independent_oid.append({keys: [str(query_result[0][0].oid) + str(
                                    query_result[0][0].indexes), query_result[0][0].oid_type, key]})
                            else:
                                independent_oid.append({keys: [str(query_result[0][0].oid) + "." + str(
                                    selectedvap), query_result[0][0].oid_type, key]})

                # return
                for i in independent_oid:
                    for keys in i.iterkeys():
                        vap_data.update(i)

                result = pysnmp_seter(vap_data, host_data[0].ip_address, host_data[0]
                                      .snmp_port, host_data[0].snmp_write_community)

                # return {'result':result,'raju':vap_data} # for testing
                if result["success"] == 0 or result["success"] == '0':
                    for i in result["result"]:
                        if result["result"][i] != 0:
                            result["result"][
                                i] = errorStatus[result["result"][i]]
                        else:
                            if i in dic_result:
                                oid_list_table_field_value = sqlalche_obj.session.query(
                                    Ap25Oids.table_name, Ap25Oids.coloumn_name).filter(and_(Ap25Oids.oid_name == i, Ap25Oids.device_type_id == device_type_id)).all()

                                if len(oid_list_table_field_value) == 0:
                                    continue
                                if i == "selectedVap":
                                    continue
                                tablename = "ap25_" + \
                                    oid_list_table_field_value[0].table_name
                                sql_table_name = rename_tablename(tablename)
                                if i == "vapWEPsecurityConfigTable.vapWEPmode" or i == "vapWEPsecurityConfigTable.vapWEPkey1" or i == "vapWEPsecurityConfigTable.vapWEPkey2" or i == "vapWEPsecurityConfigTable.vapWEPkey3" or i == "vapWEPsecurityConfigTable.vapWEPkey4" or i == "vapWEPsecurityConfigTable.vapWEPprimaryKey":

                                    exec "table_result=sqlalche_obj.session.query(%s).filter(%s.config_profile_id=='%s').all()" % (
                                        sql_table_name, sql_table_name, host_data[0].config_profile_id)

                                    exec "table_result[0].%s='%s'" % (
                                        oid_list_table_field_value[0].coloumn_name, dic_result[i])
                                else:
                                    exec "table_result=sqlalche_obj.session.query(%s).filter(and_(%s.vapselection_id=='%s',%s.config_profile_id=='%s')).all()" % (
                                        sql_table_name, sql_table_name, vap_id, sql_table_name, host_data[0].config_profile_id)
                                    exec "table_result[0].%s='%s'" % (
                                        oid_list_table_field_value[0].coloumn_name, dic_result[i])

                                sqlalche_obj.session.commit()
                else:
                    if 53 in result["result"]:
                        result = {"success": 1, "result":
                            "No Response From Device.Please Try Again"}
                    elif 553 in result["result"]:
                        result = {"success": 1, "result":
                            "No Response From Device.Please Try Again"}
                    elif 51 in result["result"]:
                        result = {"success": 1,
                            "result": "Network is unreachable"}
                    elif 99 in result["result"]:
                        result = {"success": 1, "result":
                            "UNMP has encountered an unexpected error. Please Retry"}
                    else:
                        for i in result['result']:
                            result = {"success": 1, "result": errorStatus.get(
                                result['result'][i], "Device is busy.Please try again later")}
                return result
            else:
                op_status = essential_obj.get_hoststatus(host_id_list[i])
                if op_status == None:
                    op_img = "images/host_status0.png"
                elif op_status == 0:
                    op_img = "images/host_status0.png"
                else:
                    op_img = "images/host_status1.png"
                return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ...",
                        'op_image': op_img, 'op_status': 0 if op_status == None else op_status}
        except ProgrammingError as e:
            return {"success": 1, "result": "Some Programming Error Occurs", "detail": ""}
        except AttributeError as e:
            return {"success": 1, "result": "Some Attribute Error Occurs", "detail": str(e)}
        except OperationalError as e:
            return {"success": 1, "result": "Some Operational Error Occurs", "detail": str(e)}
        except TimeoutError as e:
            return {"success": 1, "result": "Timeout Error Occurs", "detail": ""}
        except NameError as e:
            return {"success": 1, "result": "Some Name Error Occurs", "detail": str(e[-1])}
        except UnboundExecutionError as e:
            return {"success": 1, "result": "Unbound Execution Error Occurs", "detail": ""}
        except DatabaseError as e:
            return {"success": 1, "result": "Database Error Occurs,Contact Your Administrator", "detail": ""}
        except DisconnectionError as e:
            return {"success": 1, "result": "Database Disconnected", "detail": ""}
        except NoResultFound as e:
            return {"success": 1, "result": "No result Found For this opeartion", "detail": str(e)}
        except UnmappedInstanceError as e:
            return {"success": 1, "result": "Some Unmapped instance error", "detail": ""}
        except NoReferenceError as e:
            return {"success": 1, "result": "No reference Exists", "detail": ""}
        except SAWarning as e:
            return {"success": 1, "result": "Warning Occurs", "detail": ""}
        except Exception as e:
            return {"success": 1, "result": "Operation Failed,contact Administrator", "detail": str(e)}
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            essential_obj.host_status(host_id, 0, None, 12)

# obj = APCommonSetValidation()
#####
# print obj.common_validation(31,'ap25',{"success": 0,"radioSetup.numberofVAPs": 2})
# print obj.basic_acl_set(31,'ap25',{"basicACLconfigTable.aclMode": "0", "vap_selection_id": "27", "vapSelection.selectVap": "3", "basicACLconfigTable.aclState": "0", "success": 0})
# print obj.vap_set(31,'ap25',
#{"basicVAPconfigTable.vapESSID": "SHYAM-2G3", "basicVAPconfigTable.vapBeaconInterval": "100", "success": 0, \
#"basicVAPconfigTable.vapSecurityMode": "0", \
#"basicVAPconfigTable.vapMode": "0"},\
# 1,25)


class SelectVap(object):
    """
    AP VAP related class
    """
    def select_vap_vap(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        final_result = []
        host_data = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        result_data = sqlalche_obj.session.query(Ap25BasicACLconfigTable.aclState, Ap25BasicACLconfigTable.aclMode, Ap25BasicACLconfigTable.vapselection_id).filter(
            Ap25BasicACLconfigTable.config_profile_id == host_data[0].config_profile_id).all()

        for i in range(0, len(result_data)):
            sub_list = [int(i) for i in result_data[i]]
            final_result.append(sub_list)
        sqlalche_obj.sql_alchemy_db_connection_close()
        return final_result

    def select_vap_change(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        print host_id, device_type
        final_result = []
        sub_list_basic_vap = []
        sub_list_wep = []
        sub_list_wpa = []
        sub_list_basic_vap_security = []
        host_data = sqlalche_obj.session.query(
            Hosts.config_profile_id).filter(Hosts.host_id == host_id).all()
        result_basic_vap_data = sqlalche_obj.session.query(
            Ap25BasicVAPconfigTable.vapselection_id, Ap25BasicVAPconfigTable.vapESSID, Ap25BasicVAPconfigTable.vapHiddenESSIDstate,
                                                           Ap25BasicVAPconfigTable.vapRTSthresholdValue,
                                                           Ap25BasicVAPconfigTable.vapFragmentationThresholdValue,
                                                           Ap25BasicVAPconfigTable.vapBeaconInterval).filter(Ap25BasicVAPconfigTable.config_profile_id == host_data[0].config_profile_id).all()

        result_wep_security_data = sqlalche_obj.session.query(
            Ap25VapWEPsecurityConfigTable.vapWEPmode,
                                                              Ap25VapWEPsecurityConfigTable.vapWEPprimaryKey,
                                                              Ap25VapWEPsecurityConfigTable.vapWEPkey1,
                                                              Ap25VapWEPsecurityConfigTable.vapWEPkey2,
                                                              Ap25VapWEPsecurityConfigTable.vapWEPkey3,
                                                              Ap25VapWEPsecurityConfigTable.vapWEPkey4).filter(Ap25VapWEPsecurityConfigTable.config_profile_id == host_data[0].config_profile_id).all()

        result_wpa_security_data = sqlalche_obj.session.query(
            Ap25VapWPAsecurityConfigTable.vapWPAmode,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAcypher,
                                                              Ap25VapWPAsecurityConfigTable.vapWPArekeyInterval,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAmasterReKey,
                                                              Ap25VapWPAsecurityConfigTable.vapWEPrekeyInt,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAkeyMode,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase,
                                                              Ap25VapWPAsecurityConfigTable.vapWPArsnPreAuth,
                                                              Ap25VapWPAsecurityConfigTable.vapWPArsnPreAuthInterface,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAeapReAuthPeriod,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAserverIP,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAserverPort,
                                                              Ap25VapWPAsecurityConfigTable.vapWPAsharedSecret).filter(Ap25VapWPAsecurityConfigTable.config_profile_id == host_data[0].config_profile_id).all()
        result_basic_vap_security_mode = sqlalche_obj.session.query(
            Ap25BasicVAPconfigTable.vapSecurityMode, Ap25BasicVAPconfigTable.vapMode,
                                                                    Ap25BasicVAPconfigTable.vlanId, Ap25BasicVAPconfigTable.vlanPriority).filter(Ap25BasicVAPconfigTable.config_profile_id == host_data[0].config_profile_id).all()

        for i in range(0, len(result_basic_vap_data)):
            for j in result_basic_vap_data[i]:
                if isinstance(j, str):
                    sub_list_basic_vap.append(j)
                else:
                    if j == None:
                        sub_list_basic_vap.append("")
                    else:
                        sub_list_basic_vap.append(int(j))
        for i in range(0, len(result_wep_security_data)):
            for j in result_wep_security_data[i]:
                if isinstance(j, str):
                    sub_list_wep.append(j)
                else:
                    if j == None:
                        sub_list_wep.append("")
                    else:
                        sub_list_wep.append(int(j))
        for i in range(0, len(result_wpa_security_data)):
            for j in result_wpa_security_data[i]:
                if isinstance(j, str):
                    sub_list_wpa.append(j)
                else:
                    if j == None:
                        sub_list_wpa.append("")
                    else:
                        sub_list_wpa.append(int(j))

        for i in range(0, len(result_basic_vap_security_mode)):
            for j in result_basic_vap_security_mode[i]:
                if isinstance(j, str):
                    sub_list_basic_vap_security.append(j)
                else:
                    if j == None:
                        sub_list_basic_vap_security.append("")
                    else:
                        sub_list_basic_vap_security.append(int(j))

        v1, v2, v3 = 0, 0, 0
        li = []
        for i in range(0, 8):
            temp_li = []
            temp_li += sub_list_basic_vap[v1:v1 + 6]
            v1 = v1 + 6
            temp_li += sub_list_wep
            temp_li += sub_list_wpa[v2:v2 + 13]
            v2 = v2 + 13
            temp_li += sub_list_basic_vap_security
            v3 = v3 + 2
            li.append(temp_li)
        sqlalche_obj.sql_alchemy_db_connection_close()
        return li

    def select_mac(self, vap_select_id):
        """

        @param vap_select_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        final_result = []
        result_data = sqlalche_obj.session.query(Ap25AclMacTable).filter(
            Ap25AclMacTable.vapselection_id == vap_select_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        return result_data
# abj=SelectVap()
# abj.select_vap_change(5,'ap25')


class MacOperations(object):
    """
    AP based MAC operations
    """

    def chk_mac_duplicate(self, macaddress, vap_selection_id):
        """

        @param macaddress:
        @param vap_selection_id:
        @return:
        """
        global sqlalche_obj
        sqlalche_obj.sql_alchemy_db_connection_open()
        success = 0
        mac_list = sqlalche_obj.session.query(Ap25AclMacTable.macaddress).filter(
            Ap25AclMacTable.vapselection_id == vap_selection_id).all()
        sqlalche_obj.sql_alchemy_db_connection_close()
        if len(mac_list) > 0:
            for i in mac_list:

                if macaddress in i:
                    success = 1
                    break
                else:
                    success = 0
            return success
        else:
            return success

    def add_acl(self, host_id, device_type_id, dic_result, vap_selection_id, selected_vap):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param vap_selection_id:
        @param selected_vap:
        @return:
        """
        global sqlalche_obj, essential_obj, host_status_dic
        m = 0
        host_op_state = essential_obj.host_status(host_id, 12)
        if int(host_op_state) == 0:
            try:
                sqlalche_obj.sql_alchemy_db_connection_open()
                host_data = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                acl_mac_data = sqlalche_obj.session.query(Ap25AclMacTable.macaddress).filter(
                    Ap25AclMacTable.vapselection_id == vap_selection_id).all()
                vap_index = len(acl_mac_data)
                final_result = {}
                errorIndex = 0
                for i in dic_result:
                    if i == "success":
                        continue
                    mac_length = len(dic_result[i])
                    for j in range(0, len(dic_result[i])):
                        result = pysnmp_seter({i: ['1.3.6.1.4.1.26149.10.2.3.4.1.1.4.' + str(
                            selected_vap), 'OctetString', dic_result[i][j]]}, host_data[0].ip_address, host_data[0].snmp_port, host_data[0].snmp_write_community)
                        # result =
                        # pysnmp_seter({i:['1.3.6.1.4.1.26149.10.2.3.4.1.1.4.1','OctetString',dic_result[i][j]]},host_data[0].ip_address,host_data[0].snmp_port,host_data[0].snmp_write_community)
                        if result["success"] == 0 or result["success"] == '0':
                            for k in result["result"]:
                                if k == 'vap_select':
                                    continue
                                if result["result"][k] != 0:
                                    errorIndex = 1
                                    result["result"][i] = errorStatus.get(
                                        result["result"][i], 'undefied snmp error')
                                    if len(mac_length) > 0:
                                        mac_length = mac_length - 1

                                else:
                                    sqlalche_obj.db.execute("Insert into %s values(NULL,'%s','%s','%s','%s')" % (
                                        'ap25_aclMacTable', host_data[0].config_profile_id, vap_selection_id, vap_index, dic_result[i][j]))
                                    vap_index = vap_index + 1
                                    m = m + 1
                                    final_result = {
                                        "success": 0, "result": "%s Mac are added" % (m)}
                        else:
                            if 53 in result["result"] or 553 in result["result"]:
                                if m > 0:
                                    final_result = {"success": 1, "result":
                                        "%s Mac are added.No Response From Device.Please Try Again for remaining macaddresses" % (m)}
                                else:
                                    final_result = {"success": 1, "result":
                                        "No Response From Device.Please Try Again for remaining macaddresses"}
                            elif 51 in result["result"]:
                                if m > 0:
                                    final_result = {"success": 1, "result":
                                        "%s Mac are added.But after that network is unreachable" % (m)}
                                else:
                                    final_result = {
                                        "success": 1, "result": "Network is unreachable"}
                            elif 99 in result["result"]:
                                if m > 0:
                                    final_result = {"success": 1, "result":
                                        "%s Mac are added.But after that UNMP has encountered an unexpected error" % (m)}
                                else:
                                    final_result = {"success": 1, "result":
                                        "UNMP has encountered an unexpected error. Please Retry"}
                            break
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    if errorIndex == 1:
                        return result
                    else:
                        return final_result
            finally:
                essential_obj.host_status(host_id, 0, None, 12)
                if sqlalche_obj.error == 0:
                    sqlalche_obj.sql_alchemy_db_connection_close()
        else:
            return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}

    def delete_acl(self, host_id, device_type_id, dic_result, selected_vap, vap_selection_id):
        """

        @param host_id:
        @param device_type_id:
        @param dic_result:
        @param selected_vap:
        @param vap_selection_id:
        @return:
        """
        global sqlalche_obj, essential_obj, host_status_dic
        m = 0
        host_op_state = essential_obj.host_status(host_id, 12)
        if int(host_op_state) == 0:
            try:
                sqlalche_obj.sql_alchemy_db_connection_open()
                final_result = {}
                errorIndex = 0
                host_data = sqlalche_obj.session.query(
                    Hosts).filter(Hosts.host_id == host_id).all()
                for i in dic_result:
                    if i == "success":
                        continue
                    mac_length = len(dic_result[i])
                    for j in range(0, len(dic_result[i])):
                        result = pysnmp_seter({i: ['1.3.6.1.4.1.26149.10.2.3.4.1.1.5.' + str(
                            selected_vap), 'OctetString', dic_result[i][j]]}, host_data[0].ip_address, host_data[0].snmp_port, host_data[0].snmp_write_community)
                        if result["success"] == 0 or result["success"] == '0':
                            for k in result["result"]:
                                if k == 'vap_select':
                                    continue
                                if result["result"][k] != 0:
                                    result["result"][i] = errorStatus.get(
                                        result["result"][i], 'undefied snmp error')
                                    errorIndex = 1
                                    if len(mac_length) > 0:
                                        mac_length = mac_length - 1

                                else:
                                    sqlalche_obj.db.execute("delete from ap25_aclMacTable where macaddress='%s' and vapselection_id='%s'" %
                                                            (dic_result[i][j], vap_selection_id))
                                    m = m + 1
                                    final_result = {
                                        "success": 0, "result": "%s Mac are Deleted" % (m)}
                        else:
                            if 53 in result["result"] or 553 in result["result"]:
                                if m > 0:
                                    final_result = {"success": 1, "result":
                                        "%s Mac are deleted.No Response From Device.Please Try Again for remaining macaddresses" % (m)}
                                else:
                                    final_result = {"success": 1, "result":
                                        "No Response From Device.Please Try Again for remaining macaddresses"}
                            elif 51 in result["result"]:
                                if m > 0:
                                    final_result = {"success": 1, "result":
                                        "%s Mac are deleted.But after that network is unreachable" % (m)}
                                else:
                                    final_result = {
                                        "success": 1, "result": "Network is unreachable"}
                            elif 99 in result["result"]:
                                if m > 0:
                                    final_result = {"success": 1, "result":
                                        "%s Mac are deleted.But after that UNMP has encountered an unexpected error" % (m)}
                                else:
                                    final_result = {"success": 1, "result":
                                        "UNMP has encountered an unexpected error. Please Retry"}
                            else:
                                final_result = {
                                    "success": 1, "result": "%s" % (errorStatus)}
                            break
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    if errorIndex == 1:
                        return result
                    else:
                        return final_result
            finally:
                essential_obj.host_status(host_id, 0, None, 12)
                if sqlalche_obj.error == 0:
                    sqlalche_obj.sql_alchemy_db_connection_close()
        else:
            return {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) + " is in progress. please wait ..."}

    def delete_all_mac(self, host_id, device_type_id, selected_vap, vap_selection_id):
        """

        @param host_id:
        @param device_type_id:
        @param selected_vap:
        @param vap_selection_id:
        @return:
        """
        try:
            global sqlalche_obj, essential_obj, host_status_dic, errorStatus
            sqlalche_obj.sql_alchemy_db_connection_open()
            result = {}
            fianl_result = {'success': 1, 'result': ''}
            errorIndex = 0
            host_op_state = essential_obj.host_status(host_id, 12)
            if int(host_op_state) == 0:
                try:
                    host_data = sqlalche_obj.session.query(
                        Hosts).filter(Hosts.host_id == host_id).all()
                    result = pysnmp_seter({'delete_mac': ['1.3.6.1.4.1.26149.10.2.3.4.1.1.6.' + str(selected_vap), 'Integer32', 1]}, host_data[0]
                                          .ip_address, host_data[0].snmp_port, host_data[0].snmp_write_community)
                    if result["success"] == 0 or result["success"] == '0':
                        for k in result["result"]:
                            if k == 'vap_select':
                                continue
                            if result["result"][k] != 0:
                                result["result"][k] = errorStatus.get(
                                    result["result"][k], 'undefied snmp error')
                                errorIndex = 1
                            else:
                                sqlalche_obj.db.execute(
                                    "delete from ap25_aclMacTable where vapselection_id='%s'" % (vap_selection_id))
                                final_result = {'success':
                                    0, 'result': 'All Mac Deleted SuccessFully'}

                    else:
                        if 53 in result["result"] or 553 in result["result"]:
                            final_result = {"success": 1, "result":
                                "No Response From Device.Please Try Again for remaining macaddresses"}
                        elif 51 in result["result"]:
                            final_result = {
                                "success": 1, "result": "Network is unreachable"}
                        elif 99 in result["result"]:
                            final_result = {"success": 1, "result":
                                "UNMP has encountered an unexpected error. Please Retry"}
                    sqlalche_obj.sql_alchemy_db_connection_close()
                    if errorIndex == 1:
                        return result
                    else:
                        return final_result
                finally:
                    essential_obj.host_status(host_id, 0, None, 12)
            else:
                snmp_result = {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(
                    int(host_op_state), "other operation")) + " is in progress. please wait ..."}
        except Exception as e:
            return {'success': 1, 'result': result}
        finally:
            if sqlalche_obj.error == 0:
                sqlalche_obj.sql_alchemy_db_connection_close()


class APRadioState(object):
    """
    AP radio state list
    """
    def radio_enable_disable(self, host_id, admin_state, state):
        """

        @param host_id:
        @param admin_state:
        @param state:
        @return:
        """
        global sqlalche_obj, essential_obj, host_status_dic
        global errorStatus
        try:
            snmp_result = {}
            host_op_state = essential_obj.host_status(host_id, 12)
            if int(host_op_state) == 0:
                try:
                    sqlalche_obj.sql_alchemy_db_connection_open()
                    host_data = sqlalche_obj.session.query(
                        Hosts).filter(Hosts.host_id == host_id).all()
                    oid_data = sqlalche_obj.session.query(
                        Ap25Oids.oid, Ap25Oids.indexes, Ap25Oids.oid_type).filter(Ap25Oids.oid_name == admin_state).all()
                    oid_dic = {admin_state: [str(oid_data[0].oid) + str(
                        oid_data[0].indexes), oid_data[0].oid_type, state]}
                    snmp_result = pysnmp_seter(oid_dic, host_data[0].ip_address, int(
                        host_data[0].snmp_port), host_data[0].snmp_write_community)
                    if snmp_result['success'] == 0:
                        for i in snmp_result['result']:
                            if snmp_result['result'][i] == 0:
                                main_admin_data = sqlalche_obj.session.query(Ap25RadioSetup).filter(
                                    Ap25RadioSetup.config_profile_id == host_data[0].config_profile_id).all()
                                main_admin_data[0].radioState = state
                            sqlalche_obj.session.commit()
                    else:
                        for i in snmp_result["result"]:
                            if snmp_result["result"][i] != 0:
                                if i in errorStatus:
                                    snmp_result["result"] = errorStatus[i]
                    snmp_result['image'] = 'images/host_status0.png'
                finally:
                    if sqlalche_obj.error == 0:
                        sqlalche_obj.sql_alchemy_db_connection_close()
                    essential_obj.host_status(host_id, 0, None, 12)
            else:
                snmp_result = {"success": 1, "result": "Device is busy, Device " + str(host_status_dic.get(int(host_op_state), "other operation")) +
                                                                                     " is in progress. please wait ...", 'image': 'images/host_status1.png'}
        except:
            snmp_result['success'] = 1
            snmp_result['result'] = str(e)
            snmp_result['image'] = 'images/host_status1.png'
        finally:
            return snmp_result

    def chk_radio_status(self, host_id):
        """

        @param host_id:
        @return:
        """
        result = {'success': 0, 'result': ""}
        try:
            global sqlalche_obj, essential_obj
            radio_status = {}
            sqlalche_obj.sql_alchemy_db_connection_open()
            if host_id == None or host_id == "" or host_id == "undefined":
                result = {"success": 1, "result": "No host exist"}
            else:
                host_id_list = host_id.split(",")
                for i in range(0, len(host_id_list)):

                    op_status = essential_obj.get_hoststatus(host_id_list[i])
                    # print op_status
                    if op_status == None:
                        op_img = "images/host_status0.png"
                    elif op_status == 0:
                        op_img = "images/host_status0.png"
                    else:
                        op_img = "images/host_status1.png"

                    host_data_list = sqlalche_obj.session.query(
                        Hosts.config_profile_id).filter(Hosts.host_id == host_id_list[i]).all()
                    if len(host_data_list) > 0:
                        radio_state = sqlalche_obj.session.query(Ap25RadioSetup.radioState, Ap25RadioSetup.radioAPmode).filter(
                            Ap25RadioSetup.config_profile_id == host_data_list[0].config_profile_id).all()
                        radio_status.update({host_id_list[i]: [radio_state[0].radioState if len(
                            radio_state) > 0 else "", radio_state[0].radioAPmode if len(radio_state) > 0 else "", op_img, 0 if op_status == None else op_status]})
                result = {'success': 0, 'result': radio_status}
        except Exception as e:
            result['success'] = 1
            result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result


class APConnectedClients(object):
    """
    AP connected client list
    """
    def total_connected_clients(self, host_id):
        """

        @param host_id:
        @return:
        """
        try:
            global sqlalche_obj
            sqlalche_obj.sql_alchemy_db_connection_open()
            host_data = sqlalche_obj.session.query(Hosts.ip_address).filter(
                Hosts.host_id == host_id).all()
            if len(host_data) > 0:
                ip_address = host_data[0].ip_address
            result = {'success': 0, 'result': ""}
            flag = 1
            connected_clients = 1
            connected_clients = sqlalche_obj.db.execute(
                "SELECT count(*) as client,host_id FROM ap_connected_client WHERE host_id='%s' and state='1'" % (host_id))

            for row in connected_clients:
                flag = 0
                result['result'] = [int(row['client']), row['host_id']]
            if flag == 1:
                result['result'] = 0
        except Exception as e:
            result['success'] = 1
            result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    def client_details(self, client_id):
        """

        @param client_id:
        @return:
        """
        try:
            global sqlalche_obj
            result = {"success": 1, "result": "client deatails not exist"}
            sqlalche_obj.sql_alchemy_db_connection_open()
            client_data = sqlalche_obj.session.query(
                ApClient_details.client_name, ApClient_details.mac, ApClient_details.client_ip).filter(ApClient_details.client_id == client_id).all()
            if len(client_data) > 0:
                result["success"] = 0
                result["result"] = {"client_id": client_id,
                                    "client_name": client_data[0].client_name != None and client_data[0].client_name or "",
                                    "client_mac": client_data[0].mac,
                                    "client_ip": client_data[0].client_ip != None and client_data[0].client_ip or ""}
        except Exception as e:
            result['success'] = 1
            result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

    def edit_ap_client_details(self, client_id, client_name, client_ip):
        """

        @param client_id:
        @param client_name:
        @param client_ip:
        @return:
        """
        try:
            global sqlalche_obj
            result = {"success": 1, "result":
                "UNMP Server is busy, try again later."}
            sqlalche_obj.sql_alchemy_db_connection_open()
            client_data = sqlalche_obj.session.query(ApClient_details).filter(
                ApClient_details.client_id == client_id).all()
            if len(client_data) > 0:
                client_data[0].client_name = client_name
                client_data[0].client_ip = client_ip
                sqlalche_obj.session.commit()
                result['success'] = 0
                result['result'] = "Client deatils updated successfully"
            else:
                result[
                    "result"] = "Client Deatils can't update. please try again later."
        except Exception as e:
            result['success'] = 1
            result['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return result

# obj = APConnectedClients()
# print obj.total_connected_clients(6)
# obj = APRadioState()

# print obj.radio_enable_disable(70,'radioSetup.radioState',1)
# print obj.chk_radio_status("6")
# obj = APCommonSetValidation()
####
# print obj.vap_set(42,'ap25', {'vapWEPsecuritySetup.vapWEPprimaryKey': '4', 'success': 0, 'basicVAPsetup.vapBeaconInterval': '100', 'vapWEPsecuritySetup.vapWEPmode': '1', 'basicVAPsetup.vapESSID': 'anuj', 'vapWEPsecuritySetup.vapWEPkey4': '12345', 'vapWEPsecuritySetup.vapWEPkey1': '', 'vapWEPsecuritySetup.vapWEPkey2': '12345', 'vapWEPsecuritySetup.vapWEPkey3': '12345'},\
##                1,17)

# obj = Reconciliation()
######
# print obj.update_configuration(46,'ap25')
