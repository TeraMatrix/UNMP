#!/usr/bin/python2.6
# import the packeges
from datetime import datetime, timedelta
import time

import MySQLdb

from common_controller import *
from error_message import ErrorMessageClass
from mysql_collection import mysql_connection
from nms_config import *
from odu100_common_dashboard import MainOutage
from odu_controller import *
from specific_dashboard_bll import get_master_slave_value
from unmp_dashboard_config import DashboardConfig
from utility import Validation



global err_obj
err_obj = ErrorMessageClass()


class SelfException(Exception):
    """
    @return: this class return the exception msg.
    @rtype: dictionary
    @requires: Exception class package(module)
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    def __init__(self, msg):
        pass


class ClientDashboardBll(object):
    """
    AP device Connected client dashboard modal class
    """
    def sp_dashboard(self, host_id):
        """

        @param host_id:
        @return: This function return the ip_address.
        @rtype: dictionary
        @author: Rajendra Sharma
        @version: 0.1
        @date: 5 March 2012
        @organisation: Code Scape Consultants Pvt. Ltd.
        @copyright: 2011 Code Scape Consultants Pvt. Ltd.
        """

        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            ip_address = ""
            mac_address = ""
            selected_device = ""
            if Validation.is_valid_ip(host_id):
                ip_address = host_id
            else:
                if host_id == "" or host_id == None or str(host_id) == 'None':
                    ip_address = html.var("ip_address")
                    mac_address = html.var("mac_address")
                    selected_device = html.var("selected_device_type")
                    if cursor.execute("SELECT ip_address from hosts where mac_address = '%s' and device_type_id = '%s' and is_deleted=0") % (mac_address, selected_device):
                        result = cursor.fetchall()
                    elif cursor.execute("SELECT ip_address from hosts where ip_address = '%s' and device_type_id = '%s' and is_deleted=0") % (ip_address, selected_device):
                        result = cursor.fetchall()
                    else:
                        result = ()
                    if len(result) > 0:
                        ip_address = result[0][0]
                    else:
                        ip_address = ''
                else:
                    sql = "SELECT ip_address from hosts where host_id = '%s' " % (
                        host_id)
                    cursor.execute(sql)
                    ip_address = cursor.fetchall()
                    if ip_address is not None and len(ip_address) > 0:
                        ip_address = ip_address[0][0]
                    else:
                        ip_address = ''
            output_dict = {'success': 0, 'output': '%s' % ip_address}
            return output_dict
            # odu_network_interface_table_graph(h)
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

    def get_dashboard_data(self):
        """


        @return:
        """
        devcie_type_attr = ['id', 'refresh_time', 'time_diffrence']
        get_data = DashboardConfig.get_config_attributes(
            'odu_dashboard', devcie_type_attr)
        odu_refresh_time = 10   # default time
        total_count = 180   # default count showing record
        if get_data is not None:
            if get_data[0][0] == 'odu_dashboard':
                odu_refresh_time = get_data[0][1]
                total_count = get_data[0][2]
        return str(odu_refresh_time), str(total_count)

    def client_device_information(self, mac_address):
        """

        @param mac_address:
        @return: @raise:
        """
        output_dict = {}
        try:
            db, cursor = mysql_connection()
            if db == 1 or db == '1':
                raise SelfException(cursor)
            sql = "SELECT hosts.host_alias,client_name,UPPER(mac),rssi,vap_id,ap.total_tx,ap.total_rx FROM ap_client_details as ap \
            inner join hosts on hosts.host_id=ap.last_seen_ap_id \
            inner join ap_client_ap_data as ap_data on ap.client_id=ap_data.client_id \
            where ap.mac='%s' and hosts.device_type_id='ap25' and hosts.is_deleted=0" % (mac_address)
            cursor.execute(sql)
            result = cursor.fetchall()
            output_dict = {'success': 0, 'result': result}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

    # generic graph json data
    def client_all_graph_json(self, device_type_id, user_id, ip_address):
        """

        @param device_type_id:
        @param user_id:
        @param ip_address:
        @return: @raise:
        """
        data_list = []
        time_list = []
        output_dic = {}
        check_var = ''
        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)

            # check the deivce is master or not.
            master_slave_status = get_master_slave_value(ip_address)
            sel_query = "SELECT graph_display_id,graph_display_name,user_id,is_disabled,device_type_id,graph_id,graph_tab_option,refresh_button,next_pre_option,start_value,end_value,graph_width,graph_height,graph_cal_id,show_type,show_field,show_cal_type,show_tab_option,auto_refresh_time_second FROM graph_templet_table WHERE user_id='%s' AND device_type_id='%s' AND is_disabled=0 and dashboard_type=2" % (
                user_id, device_type_id)
            cursor.execute(sel_query)
            result = cursor.fetchall()
            graph_json = []

            # json format start here
            for row in result:
                query1 = "SELECT graph_id,graph_name,graph_type FROM graph_type"
                cursor.execute(query1)
                graph_tuple = cursor.fetchall()
                graph_type = []
                for value in graph_tuple:
                    if value[0] == row[5]:
                        graph_type.append(
                            {'value': value[0], 'name': value[1], 'isChecked': 1})
                    else:
                        graph_type.append(
                            {'value': value[0], 'name': value[1], 'isChecked': 0})
                query1 = "SELECT graph_field_value,graph_field_display_name,is_checked FROM graph_field_table WHERE graph_name='%s' and user_id='%s'" % (
                    row[0], user_id)
                cursor.execute(query1)
                option_tuple = cursor.fetchall()
                option_list = []
                # display the peer according to master

                if master_slave_status['success'] == 0 and int(master_slave_status['status']) > 0:
                    if len(option_tuple) > 0 and (row[0] == 'odu100rssi' or row[0] == 'odu16rssi' or row[0] == 'odu100rssi2' or row[0] == 'odu100link'):
# option_list.append({'name':option_tuple[0][0],'displayName':option_tuple[0][1],'isChecked':option_tuple[0][2]})
                        option_list.append({'name': option_tuple[0][0], 'displayName':
                                           'Master-Link', 'isChecked': option_tuple[0][2]})
                    else:
                        for option in option_tuple:
                            option_list.append({'name': option[0],
                                               'displayName': option[1], 'isChecked': option[2]})
                else:
                    for option in option_tuple:
                        option_list.append({'name': option[0],
                                           'displayName': option[1], 'isChecked': option[2]})

                query2 = "SELECT interface_value,interface_display_name,is_selected FROM  graph_interface_table WHERE graph_name='%s' and user_id='%s'" % (row[0], user_id)
                cursor.execute(query2)
                interface_tuple = cursor.fetchall()
                interface_value = []
                interface_name = []
                if device_type_id == 'odu16' or device_type_id == 'odu100':
                    check_val = 1  # default value
                elif device_type_id == 'idu4':
                    check_val = 0  # default value
                else:
                    check_val = 0  # default value

                if master_slave_status['success'] == 0 and int(master_slave_status['status']) > 0:
                    if (row[0] == 'odu100peernode'):
                        interface_value.append(1)
                        interface_name.append('Master-Link')
                        check_val = int(1)
                    else:
                        for interface in interface_tuple:
                            interface_value.append(interface[0])
                            interface_name.append(interface[1])
                            if int(interface[2]) == 1:
                                check_val = int(interface[0])
                else:
                    check_var += "2" + str(row[0])
                    for interface in interface_tuple:
                        interface_value.append(interface[0])
                        interface_name.append(interface[1])
                        if int(interface[2]) == 1:
                            check_val = int(interface[0])

                query3 = "SELECT graph_cal_id,graph_cal_name FROM  graph_calculation_table where user_id='%s' and table_name='%s'" % (user_id, row[0])
                cursor.execute(query3)
                cal_tuple = cursor.fetchall()
                cal_list = []
                for cal in cal_tuple:
                    if int(cal[0]) == int(row[13]):
                        cal_list.append({'name': str(cal[0]
                                                     ), 'displayName': cal[1], 'isChecked': int(1)})
                    else:
                        cal_list.append({'name': str(cal[0]
                                                     ), 'displayName': cal[1], 'isChecked': int(0)})

                ajax_json = {}
                query4 = "SELECT url,method,other_data FROM  graph_ajax_call_information where user_id='%s' and graph_id='%s'" % (
                    user_id, row[0])
                cursor.execute(query4)
                ajax_info = cursor.fetchall()
                for ajax in ajax_info:
                    ajax_json = {'url': ajax[0], 'method': ajax[1],
                                 'cache': False, 'data': {'table_name': ajax[2]}}

                total_item_json = {}
                query5 = "SELECT url,method,other_data FROM  total_count_item where user_id='%s' and graph_id='%s'" % (user_id, row[0])
                cursor.execute(query5)
                total_count_info = cursor.fetchall()
                for count_info in total_count_info:
                    total_item_json = {'url': count_info[0], 'method':
                                       count_info[1], 'cache': False, 'data': {'table_name': count_info[2]}}

                # This field is also come form database
                showType = True if int(row[14]) == 1 else False
                showFields = True if int(row[15]) == 1 else False
                showCalType = True if int(row[16]) == 1 else False
                showTabOption = True if int(row[17]) == 1 else False

                graph_dict = {'name': row[0], 'displayName': row[1], 'fields': option_list, 'calType': cal_list, 'ajax': ajax_json, 'tabList': {'value': interface_value, 'name': interface_name, 'selected': check_val}, 'type': graph_type, 'otherOption': {'showOption': True if int(row[6]) == 1 else False, 'showRefreshButton': True if int(row[7]) == 1 else False, 'showNextPreButton': True if int(row[8]) == 1 else False, 'width': row[11], 'height': str(
                    row[12]) + "px", 'showType': showType, 'showFields': showFields, 'showCalType': showCalType, 'showTabOption': showTabOption, 'autoRefresh': row[18]}, 'startFrom': row[9], 'itemLimit': row[10], 'totalItemAjax': total_item_json}

                # this is check the master or slave for sync lsot graph showing or not.
                # this is check the master or slave for sync lsot graph showing
                # or not.
                if master_slave_status['success'] == 0 and int(master_slave_status['status']) == 0:
                    if ajax_json['data']['table_name'].split(',')[0] == 'odu100_synchStatisticsTable' or ajax_json['data']['table_name'].split(',')[0] == 'get_odu16_synch_statistics_table':
                        pass
                    else:
                        graph_json.append(graph_dict)
                else:
                    graph_json.append(graph_dict)

            output_dic = {'success': 0, 'graphs': graph_json, 'cde': check_var}
            return output_dic
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if conn.open:
                conn.close()

    def client_graph_json(self, display_type, user_id, table_name, x_axis_value, index_name, graph_id, flag, start_date, end_date, start, limit, mac_address, graph, update_field_name, interface=1, value_cal=1, *column_name):
        """

        @param display_type:
        @param user_id:
        @param table_name:
        @param x_axis_value:
        @param index_name:
        @param graph_id:
        @param flag:
        @param start_date:
        @param end_date:
        @param start:
        @param limit:
        @param mac_address:
        @param graph:
        @param update_field_name:
        @param interface:
        @param value_cal:
        @param column_name:
        @return: @raise:
        """
        data_list = []
        time_list = []
        calculation = ['normal', 'delta']
        output_dic = {}
        json_data = []
        min_value = 0
        max_value = 0

        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)

            default_value = {'y': 0, 'marker': {'symbol':
                                                'url(images/device-down.gif)'}}
            # default_value=0
            if display_type == 'table' or display_type == 'excel' or display_type == 'csv':
                default_value = 'Device Unreachable'
            elif display_type == 'pdf':
                default_value = 'DU'
            # update the graph calculatio id for particular user for particular
            # table
            if str(update_field_name).strip() == 'calType':
                up_query = "update  graph_templet_table set graph_cal_id =%s where user_id='%s' and graph_display_id='%s' and dashboard_type=2" % (
                    value_cal, user_id, graph_id)
                cursor.execute(up_query)
                conn.commit()

            elif str(update_field_name).strip() == 'fields':
                up_query = "update graph_field_table set is_checked=0 where user_id='%s' and graph_name='%s'" % (
                    user_id, graph_id)
                cursor.execute(up_query)
                conn.commit()

                columns = "','".join(column_name[0])
                up_query = "update graph_field_table set is_checked=1 where user_id='%s' and graph_name='%s' and graph_field_value IN ('%s')" % (
                    user_id, graph_id, columns)
                cursor.execute(up_query)
                conn.commit()

            elif str(update_field_name).strip() == 'type':
                up_query = "update  graph_templet_table set graph_id =%s where user_id='%s' and graph_display_id='%s' and dashboard_type=2" % (graph, user_id, graph_id)
                cursor.execute(up_query)
                conn.commit()
            # get the data from graph field table .
            get_coloum = "SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' \
            AND user_id='%s'" % (graph_id, user_id)
            cursor.execute(get_coloum)
            coloum_result = cursor.fetchall()
            clm_dict = dict(zip([coloum_result[i][0] for i in range(
                len(coloum_result))], [coloum_result[i][1] for i in range(len(coloum_result))]))
            table_field_dict1 = {table_name: clm_dict}
            graph_field_dict = dict(
                (field[0], field[2]) for field in coloum_result)

            sel_query = "select graph_title,graph_subtitle from graph_templet_table where graph_display_id='%s' and user_id='%s' and dashboard_type=2" % (
                graph_id, user_id)
            cursor.execute(sel_query)
            graph_name_result = cursor.fetchall()
            graph_title = '' if graph_name_result[0][
                0] == None or graph_name_result[0][0] == '' else graph_name_result[0][0]
            graph_sub_title = '' if graph_name_result[0][
                1] == None or graph_name_result[0][1] == '' else graph_name_result[0][1]

            if graph_id.strip() == 'apClientRssi123':  # this is not using
                odu100_rssi_result = self.sp_signal_strength_graph(
                    display_type, graph_id, mac_address, start_date, end_date, table_name, column_name[0])
                if int(odu100_rssi_result['success']) != 0:
                    return odu100_rssi_result
                output_dic = {'success': 0, 'timestamp': odu100_rssi_result['time_stamp'], 'data': odu100_rssi_result['display_signal_strength'],
                              'graph_title': graph_title, 'graph_sub_title': graph_sub_title}
                return output_dic
            else:
                if display_type in ['excel', 'pdf', 'csv']:
                    sel_query = "Select "
                    if len(column_name[0][0]) > 0:
                        column_list = ',gp_tab.'.join(column_name[0])
                        column_list = 'gp_tab.' + column_list
                        sel_query += column_list + "," + "gp_tab.%s from %s as gp_tab where UPPER(gp_tab.addressMAC)='%s' AND gp_tab.timestamp >= '%s' \
		        AND gp_tab.timestamp <='%s' order by gp_tab.timestamp desc" % (x_axis_value, table_name, mac_address, start_date, end_date)
                    else:
                        sel_query += "gp_tab.%s from %s as gp_tab where UPPER(gp_tab.addressMAC)='%s' AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' \
		        order by gp_tab.timestamp desc" % (x_axis_value, table_name, mac_address, start_date, end_date)
                else:
                    sel_query = "Select "
                    if len(column_name[0][0]) > 0:
                        column_list = ',gp_tab.'.join(column_name[0])
                        column_list = 'gp_tab.' + column_list
                        sel_query += column_list + "," + "gp_tab.%s from %s as gp_tab where UPPER(gp_tab.addressMAC)='%s' AND gp_tab.timestamp >= '%s' \
		        AND gp_tab.timestamp <='%s'  order by gp_tab.timestamp desc" % (x_axis_value, table_name, mac_address, start_date, end_date)
                    else:
                        sel_query += "gp_tab.%s from %s as gp_tab where UPPER(gp_tab.addressMAC)='%s' AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' \
		        order by gp_tab.timestamp desc" % (x_axis_value, table_name, mac_address, start_date, end_date)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                for i in range(len(column_name[0])):
                    data_list.append([])

                if calculation[int(value_cal) - 1] == 'normal':
                    for row in result:
                        for i in range(len(row) - 1):
                            if graph_id == "apClientRssi":
                                min_value = -100
                                max_value = 1
                                data_list[i].append(0 if row[i] == None or row[i] == None else (
                                    0 - int(str(row[i][:-1])) if 'M' in str(row[i]) else row[i]))
                            else:
                                min_value = 0
                                max_value = 0
                                data_list[i].append(0 if row[i] == None or row[i] == None else int(
                                    str(row[i][:-1]) if 'M' in str(row[i]) else row[i]))
                        time_list.append(datetime.strptime(
                            str(row[len(row) - 1])[:19], '%Y-%m-%d %H:%M:%S'))

                elif calculation[int(value_cal) - 1] == 'delta':
                    for k in range(len(result) - 1):
                        count = 0
                        temp = []
                        for d2 in range(len(result[k]) - 1):
                            if result[k][d2] == 1111111 or result[k][d2] == '1111111':
                                count += 1
                        if count == len(result[k]) - 1:
                            for d3 in range(len(result[k]) - 1):
                                data_list[d3].append(default_value)
                        else:
                            for i in range(len(result[k]) - 1):
                                val = (0 if int(result[k][i]) == 1111111 else int(result[k][i])) - \
                                    (0 if int(result[
                                        k + 1][i]) == 1111111 else int(result[k + 1][i]))
                                main_val = val if val > 0 else 0
                                data_list[i].append(0 if result[k][
                                                    i] == None or result[k][i] == '' else main_val)
                        time_list.append(datetime.strptime(str(result[k][len(
                            result[k]) - 1])[:19], '%Y-%m-%d %H:%M:%S'))

                if display_type in ['graph']:
                    for index_val in range(len(time_list)):
                        time_list[index_val] = time.mktime(
                            time_list[index_val].timetuple()) * 1000

                if len(data_list) > 0 and calculation[int(value_cal) - 1] == 'normal':
                    for d1 in range(len(data_list[0])):
                        count = 0
                        for d2 in range(len(data_list)):
                            if data_list[d2][d1] == 1111111 or data_list[d2][d1] == '1111111':
                                count += 1
                        if count == len(data_list):
                            for d3 in range(len(data_list)):
                                data_list[d3][d1] = default_value

                if len(column_name[0][0]) > 0:
                    i = 0
                    for name in column_name[0]:
                        json_data.append({'name': ['%s' % table_field_dict1[table_name][
                                         name], graph_field_dict[name]], 'data': data_list[i]})
                        i += 1
            output_dic = {
                'success': 0, 'timestamp': time_list, 'data': json_data, 'graph_title': graph_title, 'graph_sub_title': graph_sub_title,
                'range_min': min_value, 'range_max': max_value}
            return output_dic
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if conn.open:
                conn.close()

    def update_show_graph_table(self, device_type_id, user_id, show_graph):
        """

        @param device_type_id:
        @param user_id:
        @param show_graph:
        @return: @raise:
        """
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            # this is for latest Event
            graph_list = show_graph.split(',')
            if show_graph.strip() != '':
                sql = "UPDATE graph_templet_table SET is_disabled=1 WHERE user_id='%s' and device_type_id='%s' and dashboard_type=2" % (
                    user_id, device_type_id)
                cursor.execute(sql)
                db.commit()
                sql1 = "UPDATE graph_templet_table SET is_disabled=0 WHERE user_id='%s' AND device_type_id='%s' AND graph_display_id IN ('%s') and \
                dashboard_type=2" % (user_id, device_type_id, "','".join(graph_list))
                cursor.execute(sql1)
                db.commit()
            output_dict = {'success': 0, 'result': 'updated successfully'}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

    def client_dashboard_get_graph_name(self, user_id, device_type):
        """

        @param user_id:
        @param device_type:
        @return:
        """
        try:
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select graph_display_name,is_disabled,graph_display_id from graph_templet_table where device_type_id='%s' and user_id='%s' and \
            dashboard_type=2" % (device_type, user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            selected_graph = []
            non_selected_graph = []
            for row in result:
                temp = []
                temp.append(row[0])
                temp.append(row[2])
                if int(row[1]) == 1:
                    non_selected_graph.append(temp)
                else:
                    selected_graph.append(temp)
            db.close()
            result_dict = {"success": "0", "selected":
                           selected_graph, "non_selected": non_selected_graph}
            return result_dict
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

    def client_total_display_graph(self, device_type_id, user_id):
        """

        @param device_type_id:
        @param user_id:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select graph_display_id from graph_templet_table where device_type_id='%s' and user_id='%s' and is_disabled=0 and dashboard_type=2" % (
                device_type_id, user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            count = 0
            if len(result) > 0:
                count = int(len(result))
            else:
                count = 0
            db.close()
            result_dict = {"success": "0", "show_graph": count}
            return result_dict
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

    def client_state_data(self, mac_address):
        """

        @param mac_address:
        @return:
        """
        try:
            # check the deivce is master or not.
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "select client_name,UPPER(mac),total_tx,total_rx,first_seen_time,ifnull(hosts_first.host_alias,'-') as first_host_alias,last_seen_time,ifnull(hosts_last.host_alias,'-') as last_host_alias,if(ap_connected_client.state='1','Yes','No') from ap_client_details as ap \
join (select host_id,host_alias,ip_address from hosts where is_deleted=0) as hosts_first on hosts_first.host_id=ap.first_seen_ap_id \
join (select host_id,host_alias,ip_address from hosts where is_deleted=0) as hosts_last on hosts_last.host_id=ap.last_seen_ap_id \
join (select state,host_id,client_id from ap_connected_client ) as ap_connected_client on ap.client_id=ap_connected_client.client_id and ap.last_seen_ap_id=ap_connected_client.host_id \
where ap.mac='%s'\
order by ap.client_id" % (mac_address)
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close()
            result_dict = {"success": "0", "result": result}
            return result_dict
        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

######### reportring work start here .########
# Excel reporting start here.
    def client_excel_report(self, device_type, user_id, mac_address, cal_list, tab_list, field_list, table_name_list, graph_name_list, start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list):
#        if mac_address=='' or mac_address==None or mac_address=='undefined' or str(mac_address)=='None':    # if ip_address not received so excel not created
#            raise SelfException('This Client not exists so excel report can not be generated.')  # Check msg
#        check_var=''
        """

        @param device_type:
        @param user_id:
        @param mac_address:
        @param cal_list:
        @param tab_list:
        @param field_list:
        @param table_name_list:
        @param graph_name_list:
        @param start_date:
        @param end_date:
        @param select_option:
        @param limitFlag:
        @param graph_list:
        @param start_list:
        @param limit_list:
        @return: @raise:
        """
        try:
            device_name = {'ap25': 'AP25', 'odu16': 'RM18',
                           'odu100': 'RM', 'idu4': 'IDU'}
            table_output = []
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            import xlwt
            from xlwt import Workbook, easyxf
            # create the excel file
            xls_book = Workbook(encoding='ascii')
            # Excel reproting Style part
            style = xlwt.XFStyle()
            borders = xlwt.Borders()
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 23
            borders.right_colour = 23
            borders.top_colour = 23
            borders.bottom_colour = 23
            style.borders = borders
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = 16
            style.pattern = pattern
            font = xlwt.Font()
            font.bold = True
            font.colour_index = 0x09
            style.font = font
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style.alignment = alignment
            style1 = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style1.alignment = alignment
            # -----------   End of style ---------#

            # create the connection with database
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # save file name of excel
            save_file_name = 'AP25_' + str(start_date) + '.xls'
            # device value correspondes to no.
            if device_type.strip() == 'ap25':
                result = self.client_device_information(mac_address)
                if result['success'] == 0 and len(result) > 0:
                    result = result['result']
                    device_detail = ['AP alias', 'Client Alias',
                                     'MAC Address', 'RSSI', 'VAP', 'Total Tx(Mbps)', 'Total Rx(Mbps)']
                    for i in result:
                        table_output.append([device_detail[0], '--' if result[0][0]
                                            == None or result[0][0] == '' else result[0][0]])
                        table_output.append([device_detail[1], '--' if result[0][1]
                                            == None or result[0][1] == '' else result[0][1]])
                        table_output.append([device_detail[2], '--' if result[0][2]
                                            == None or result[0][2] == '' else result[0][2]])
                        table_output.append([device_detail[3], '--' if result[0][3]
                                            == None or result[0][3] == '' else result[0][3]])
                        table_output.append([device_detail[4], '--' if result[0][4]
                                            == None or result[0][4] == '' else result[0][4]])
                        table_output.append([device_detail[5], '--' if result[0][5]
                                            == None or result[0][5] == '' else result[0][5]])
                        table_output.append([device_detail[6], '--' if result[0][6]
                                            == None or result[0][6] == '' else result[0][6]])

            # create the excel sheet for devcice information .
            xls_sheet = xls_book.add_sheet(
                'Client_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "AP25 Client Information (%s--%s)" % (str(
                start_date), str(end_date)), style)
            xls_sheet.write_merge(1, 1, 0, 2, "", style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Field Name', 'Field Value']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(table_output)):
                for j in range(len(table_output[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(table_output[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1

            for i in range(len(tab_list)):
                cal_type = ''
                if int(cal_list[i]) == 1:
                    cal_type = 'Total'
                elif int(cal_list[i]) == 2:
                    cal_type = 'Delta'
                table_split_result = table_name_list[i].split(',')
                table_name = table_split_result[0]
                x_axis = table_split_result[1]
                index_name = table_split_result[-2]
                graph_id = table_split_result[-1]
                field_column = field_list[i].split(',')
                update_field_name = ''
                start = 0  # default value for start and end here .
                limit = 0
                output_result = self.client_graph_json(
                    'excel', user_id, table_name, x_axis, index_name, graph_id, limitFlag, start_date, end_date, start, limit,
                    mac_address, graph_list[i], update_field_name, tab_list[i], cal_list[i], field_column)
                d1_list = []
                first_column = x_axis.capitalize()
                headings = [first_column]
                if int(output_result['success']) == 0:
                    d1_list.append(output_result['timestamp'])
                    for data_list in output_result['data']:
                        headings.append(str(
                            data_list['name'][0]) + str(data_list['name'][1]))
                        d1_list.append(data_list['data'])
                    merge_result = merge_list(d1_list)

                # if no column select so report not created.
                if len(headings) < 2:
                    continue
                xls_sheet = xls_book.add_sheet(
                    str(graph_name_list[i]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(0, 0, 0, len(headings) - 1, "%s (%s--%s)" % (
                    str(graph_name_list[i]), str(start_date), str(end_date)), style)
                xls_sheet.write_merge(1, 1, 0, len(headings) - 1, device_name[device_type] + '   ' + str(
                    mac_address) + '  Display Information -: (%s)' % str(cal_type), style)
                xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                l = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                for colx, value in enumerate(headings):
                    xls_sheet.write(l - 1, colx, value, heading_xf)
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    l)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there

                for k in range(len(merge_result)):
                    for j in range(len(merge_result[k])):
                        width = 5000
                        xls_sheet.write(l, j, str(merge_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                    l = l + 1
                # End for CRC/PHY Error Excel Report

            if device_type == 'ap25':
                merge_result = ()
                client_result = self.client_state_data(mac_address)
                if client_result['success'] == 0 or client_result['success'] == '0':
                    merge_result = client_result['result']
                headings = ['Client Alias', 'MAC Address', 'Total Tx(Mbps)', 'Total Rx(Mbps)', 'First Seen Time',
                            'First Seen AP', 'Last Seen Time', 'Last Seen AP', 'Current State']
                xls_sheet = xls_book.add_sheet(
                    'Client Details', cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, len(headings) - 1, 'Client State Information (%s--%s)' % (start_date, end_date), style)
                xls_sheet.write_merge(
                    1, 1, 0, len(headings) - 1, device_name[device_type], style)
                xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for k in range(len(merge_result)):
                    for j in range(len(merge_result[k])):
                        width = 5000
                        xls_sheet.write(i, j, str(merge_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                    i = i + 1

            xls_book.save('/omd/sites/%s/share/check_mk/web/htdocs/download/%s' % (
                nms_instance, save_file_name))
            output_dict = {'success': 0, 'output':
                           'report created successfully.', 'file_name': save_file_name}
            return output_dict

        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except ImportError, e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 101 ' + str(
                err_obj.get_error_msg(101)), 'main_msg': str(e[-1])}
            return output_dict
        except IOError, e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 103 ' + str(
                err_obj.get_error_msg(103)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

# CSV reporting start here.
    def client_csv_report(self, device_type, user_id, mac_address, cal_list, tab_list, field_list, table_name_list, graph_name_list, start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list):
#        if ip_address=='' or ip_address==None or ip_address=='undefined' or str(ip_address)=='None':    # if ip_address not received so excel not created
#            raise SelfException('This devices not exists so excel report can not be generated.')  # Check msg
        # check_var=''
        """

@param device_type:
@param user_id:
@param mac_address:
@param cal_list:
@param tab_list:
@param field_list:
@param table_name_list:
@param graph_name_list:
@param start_date:
@param end_date:
@param select_option:
@param limitFlag:
@param graph_list:
@param start_list:
@param limit_list:
@return: @raise:
"""
        try:
            display_type = 'csv'
            table_output = []
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
            import csv

            device_name = {'ap25': 'AP25', 'odu16': 'RM18',
                           'odu100': 'RM', 'idu4': 'IDU'}

            # create the connection with database
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # finished
            # save file name of excel
            save_file_name = 'AP25_' + str(start_date) + '.csv'

            # device value correspondes to no.
            if device_type.strip() == 'ap25':
                result = self.client_device_information(mac_address)
                if result['success'] == 0 and len(result) > 0:
                    result = result['result']
                    device_detail = ['AP alias', 'Client Alias',
                                     'MAC Address', 'RSSI', 'VAP', 'Total Tx(Mbps)', 'Total Rx(Mbps)']
                    for i in result:
                        table_output.append([device_detail[0], '--' if result[0][0]
                                            == None or result[0][0] == '' else result[0][0]])
                        table_output.append([device_detail[1], '--' if result[0][1]
                                            == None or result[0][1] == '' else result[0][1]])
                        table_output.append([device_detail[2], '--' if result[0][2]
                                            == None or result[0][2] == '' else result[0][2]])
                        table_output.append([device_detail[3], '--' if result[0][3]
                                            == None or result[0][3] == '' else result[0][3]])
                        table_output.append([device_detail[4], '--' if result[0][4]
                                            == None or result[0][4] == '' else result[0][4]])
                        table_output.append([device_detail[5], '--' if result[0][5]
                                            == None or result[0][5] == '' else result[0][5]])
                        table_output.append([device_detail[6], '--' if result[0][6]
                                            == None or result[0][5] == '' else result[0][6]])

            # create the csv file.
            path = '/omd/sites/%s/share/check_mk/web/htdocs/download/%s' % (
                nms_instance, save_file_name)
            ofile = open(path, "wb")
            writer = csv.writer(ofile, delimiter=',', quotechar='"')

            headings = ['Field Name', 'Field Value']
            blank_row = ["", "", ""]
            main_row = ['Client Information']
            second_row = [str(device_name[device_type]) +
                          ' Information', str(start_date), str(end_date)]
            writer.writerow(main_row)
            writer.writerow(second_row)
            writer.writerow(blank_row)
            writer.writerow(headings)
            for row1 in table_output:
                writer.writerow(row1)

            for i in range(len(tab_list)):
                cal_type = ''
                if int(cal_list[i]) == 1:
                    cal_type = 'Total'
                elif int(cal_list[i]) == 2:
                    cal_type = 'Delta'

                table_split_result = table_name_list[i].split(',')
                table_name = table_split_result[0]
                x_axis = table_split_result[1]
                index_name = table_split_result[-2]
                graph_id = table_split_result[-1]
                field_column = field_list[i].split(',')
                update_field_name = ''
                start = 0  # default value for start and end here .
                limit = 0
                output_result = self.client_graph_json(
                    display_type, user_id, table_name, x_axis, index_name, graph_id, limitFlag, start_date, end_date, start, limit,
                    mac_address, graph_list[i], update_field_name, tab_list[i], cal_list[i], field_column)
                d1_list = []
                first_column = x_axis.capitalize()
                headings = [first_column]
                if int(output_result['success']) == 0:
                    d1_list.append(output_result['timestamp'])
                    for data_list in output_result['data']:
                        headings.append(str(
                            data_list['name'][0]) + str(data_list['name'][1]))
                        d1_list.append(data_list['data'])
                    merge_result = merge_list(d1_list)

        # if no column select so report not created.
                if len(headings) < 2:
                    continue

                blank_row = ["", "", ""]
                main_row = [str(graph_name_list[i])]
                second_row = [device_name[device_type] +
                              ' Client State Information -:' + str(cal_type)]
                blank_row = ["", "", ""]
                writer.writerow(['------', '--Break--', '------'])
                writer.writerow(blank_row)
                writer.writerow(blank_row)
                writer.writerow(blank_row)
                writer.writerow(main_row)
                writer.writerow(second_row)
                writer.writerow(blank_row)
                writer.writerow(headings)
                for row1 in merge_result:
                    writer.writerow(row1)

            # This report create only for AP.
            if device_type == 'ap25':
                merge_result = ()
                client_result = self.client_state_data(mac_address)
                if client_result['success'] == 0 or client_result['success'] == '0':
                    merge_result = client_result['result']
                headings = ['Client Alias', 'MAC Address', 'Total Tx(Mbps)', 'Total Rx(Mbps)', 'First Seen Time',
                            'First Seen AP', 'Last Seen Time', 'Last Seen AP', 'Current State']
                blank_row = ["", "", ""]
                main_row = ['Client State Information']
                second_row = [device_name[device_type]]
                blank_row = ["", "", ""]
                writer.writerow(['------', '--Break--', '------'])
                writer.writerow(blank_row)
                writer.writerow(blank_row)
                writer.writerow(blank_row)
                writer.writerow(main_row)
                writer.writerow(second_row)
                writer.writerow(blank_row)
                writer.writerow(headings)
                for row1 in merge_result:
                    writer.writerow(row1)

            ofile.close()
            output_dict = {'success': 0, 'output':
                           'report created successfully.', 'file_name': save_file_name}
            return output_dict
        #    (self,user_id,table_name,x_axis_value,flag,start_date,end_date,ip_address,graph,update_field_name,interface=1,value_cal=1,*column_name):

        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except ImportError, e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 101 ' + str(
                err_obj.get_error_msg(101)), 'main_msg': str(e[-1])}
            return output_dict
        except IOError, e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 103 ' + str(
                err_obj.get_error_msg(103)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104 ' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()

    def sp_pdf_report(self, device_type, user_id, ip_address, cal_list, tab_list, field_list, table_name_list, graph_name_list, start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list):
        """

        @param device_type:
        @param user_id:
        @param ip_address:
        @param cal_list:
        @param tab_list:
        @param field_list:
        @param table_name_list:
        @param graph_name_list:
        @param start_date:
        @param end_date:
        @param select_option:
        @param limitFlag:
        @param graph_list:
        @param start_list:
        @param limit_list:
        @return: @raise:
        """
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(ip_address) == 'None':    # if ip_address not received so excel not created
            raise SelfException(
                'This devices not exists so excel report can not be generated.')  # Check msg
        try:
            from reportlab.lib import colors
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
            import reportlab
            from reportlab.platypus import Image
            from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Frame, BaseDocTemplate, Frame, PageTemplate
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch, cm, mm
            from reportlab.lib import colors
            from reportlab.platypus.paragraph import Paragraph
            from reportlab.lib.enums import TA_JUSTIFY
            import copy

            display_type = 'pdf'
            master_slave_status = get_master_slave_value(ip_address)
            device_postfix = '(Master)'
            if master_slave_status['success'] == 0 and master_slave_status['status'] > 0:
                device_postfix = '(Slave)'

            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            device_name = {'ap25': 'AP25', 'odu16': 'RM18',
                           'odu100': 'RM', 'idu4': 'IDU'}
            idu4_port = {'0': '(odu)', '1': '(eth0)', '2':
                         '(eth1)', '3': '(cpu)', '4': '(maxima)'}
            interface_list = {'get_odu16_nw_interface_statistics_table': {'1': '(eth0)', '2': '(br0)', '3': '(eth1)'}, 'odu100_nwInterfaceStatisticsTable': {'1': '(eth0)', '2': '(eth1)'}, 'ap25_statisticsTable': {'0': '(eth0)', '1': '(br0)', '2': '(ath0)', '3': '(ath1)', '4': '(ath2)', '5': '(ath3)', '6': '(ath4)', '7': '(ath5)', '8': '(ath6)'},
                              'idu_e1PortStatusTable': {'1': '(port1)', '2': '(port2)', '3': '(port3)', '4': '(port4)'}, 'idu_portstatisticsTable': idu4_port, 'idu_swPrimaryPortStatisticsTable': idu4_port, 'idu_portSecondaryStatisticsTable': idu4_port,
                              'odu100_peerNodeStatusTable': {'1': '(Link1)', '2': '(Link2)', '3': '(Link3)', '4': '(Link4)', '5': '(Link5)', '6': '(Link6)', '7': '(Link7)', '8': '(Link8)', '9': '(Link9)', '16': '(Link16)'}}

            # we are geting the login user name here.
            login_user_name = ''
            sel_query = "SELECT host_alias FROM hosts WHERE ip_address='%s'" % (
                ip_address)
            cursor.execute(sel_query)
            uesr_information = cursor.fetchall()
            if len(uesr_information) > 0:
                login_user_name = uesr_information[0][0]
            # finished
            # save file name.
            save_file_name = str(device_name[device_type]) + '_' + str(
                login_user_name) + '_' + str(start_date) + '.pdf'

            # device value correspondes to no.
            wifi = ['wifi11g', 'wifi11gnHT20',
                    'wifi11gnHT40plus', 'wifi11gnHT40minus']
            radio = ['disabled', 'enabled']
            device_detail = [
                'Radio Status', 'Radio Channel', 'No of VAPs', 'Software Version',
                'Hardware Version', 'BootLoader Version', 'WiFi Mode', 'MAC Address', 'No of Connected User']

            last_reboot_resion = {0: 'Power cycle', 1: 'Watchdog reset', 2: 'Normal', 3:
                                  'Kernel crash reset', 4: 'Radio count mismatch reset', 5: 'Unknown-Soft', 6: 'Unknown reset'}
            default_node_type = {0: 'rootRU', 1: 't1TDN', 2:
                't2TDN', 3: 't2TEN'}
            operation_state = {0: 'disabled', 1: 'enabled'}
            channel = {0: 'raBW5MHz', 1: 'raBW10MHz', 2:
                'raBW20MHz', 3: 'raBW40MHz', 4: 'raBW40SGIMHz'}

            # style of the pdf report
            styleSheet = getSampleStyleSheet()
            ubr_report = []
            MARGIN_SIZE = 14 * mm
            PAGE_SIZE = A4
            nms_instance = __file__.split("/")[3]
# pdfdoc="/omd/sites/%s/share/check_mk/web/htdocs/download/IDU4_PDF_Report.pdf"%(nms_instance,start_time,end_time)
            pdfdoc = "/omd/sites/%s/share/check_mk/web/htdocs/download/%s" % (
                nms_instance, save_file_name)
            pdf_doc = BaseDocTemplate(pdfdoc, pagesize=PAGE_SIZE,
                                      leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
                                      topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
            main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,
                               PAGE_SIZE[0] - 2 *
                                   MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
                               leftPadding=0, rightPadding=0, bottomPadding=0,
                               topPadding=0, id='main_frame')
            main_template = PageTemplate(
                id='main_template', frames=[main_frame])
            pdf_doc.addPageTemplates([main_template])
            im = Image(
                "/omd/sites/%s/share/check_mk/web/htdocs/images/%s/logo.png" % (nms_instance,
                       theme), width=1.5 * inch, height=.5 * inch)
            im.hAlign = 'LEFT'
            ubr_report.append(im)
            ubr_report.append(Spacer(1, 1))
            data = []
            data.append([device_name[device_type] + str(device_postfix) + str(
                ip_address), str(start_date) + '--' + str(end_date)])
            t = Table(data, [3.5 * inch, 4 * inch])
            t.setStyle(TableStyle([
                ('LINEBELOW', (0, 0), (5, 1), 1, (0.7, 0.7, 0.7)),
                ('TEXTCOLOR', (0, 0), (0, 0), (0.11, 0.11, 0.11)),
                ('TEXTCOLOR', (1, 0), (1, 0), (0.65, 0.65, 0.65)),
                ('FONT', (0, 0), (1, 0), 'Helvetica', 14),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
            ubr_report.append(t)
            ubr_report.append(Spacer(11, 11))
            table_output = []
            table_output.append(['Fields', 'Values'])
            if device_type.strip() == 'ap25':
                channel = [
                    'channel-01', 'channel-02', 'channel-03', 'channel-04', 'channel-05', 'channel-06', 'channel-07', 'channel-08', 'channel-09',
                    'channel-10', 'channel-11', 'channel-12', 'channel-13', 'channel-14']
                device_detail = [
                    'Radio Status', 'Radio Channel', 'No of VAPs', 'Software Version', 'Hardware Version',
                    'BootLoader Version', 'WiFi Mode', 'MAC Address', 'No of Connected User']
                sql = "select ap25_radioSetup.radioState,ap25_radioSetup.radiochannel,ap25_radioSetup.numberofVAPs,\
                ap25_versions.softwareVersion,ap25_versions.hardwareVersion\
                ,ap25_versions.bootLoaderVersion,ap25_radioSetup.wifiMode,hosts.mac_address from ap25_radioSetup\
                left join (select host_id,ip_address,mac_address,config_profile_id from hosts where hosts.is_deleted=0) as hosts on hosts.ip_address='%s'\
                left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion from ap25_versions) as ap25_versions on ap25_versions.host_id=hosts.host_id where ap25_radioSetup.config_profile_id=hosts.config_profile_id order by hosts.ip_address" % (ip_address)
                cursor.execute(sql)
                result = cursor.fetchall()

                sql = "SELECT count(*) FROM ap_connected_client inner join hosts on ap_connected_client.host_id=hosts.host_id  WHERE state='1' and hosts.ip_address='%s'  and hosts.is_deleted=0 " % (
                    ip_address)
                cursor.execute(sql)
                no_of_user = cursor.fetchall()
                if len(result) > 0:
                    for i in result:
                        table_output.append([device_detail[0], '--' if result[0][0]
                                            == None or result[0][0] == '' else radio[int(result[0][0])]])
                        table_output.append([device_detail[1], '--' if result[0][1]
                                            == None or result[0][1] == '' else channel[int(result[0][1]) - 1]])
                        table_output.append([device_detail[2], '--' if result[0][2]
                                            == None or result[0][2] == '' else result[0][2]])
                        table_output.append([device_detail[3], '--' if result[0][3]
                                            == None or result[0][3] == '' else result[0][3]])
                        table_output.append([device_detail[4], '--' if result[0][4]
                                            == None or result[0][4] == '' else result[0][4]])
                        table_output.append([device_detail[5], '--' if result[0][5]
                                            == None or result[0][5] == '' else result[0][5]])
                        table_output.append([device_detail[6], '--' if result[0][6]
                                            == None or result[0][6] == '' else wifi[int(result[0][6])]])
                        table_output.append([device_detail[7], '--' if result[0][7]
                                            == None or result[0][7] == '' else result[0][7]])
                if len(no_of_user) > 0:
                    table_output.append(['No of Connected User', 0 if no_of_user[0][0]
                                        == None or no_of_user[0][0] == '' else no_of_user[0][0]])
            elif device_type.strip() == 'odu16':
                sql = "SELECT fm.rf_channel_frequency,ts.num_slaves,sw.active_version ,hw.hw_version,lrb.last_reboot_reason,cb.channel_bandwidth ,op.op_state ,op.default_node_type,hs.mac_address,hs.ip_address FROM  hosts as hs LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hs.config_profile_id LEFT JOIN set_odu16_sync_config_table as ts ON ts.config_profile_id = hs.config_profile_id LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hs.host_id LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hs.host_id  LEFT JOIN  get_odu16_ru_status_table as lrb ON lrb.host_id=hs.host_id LEFT JOIN set_odu16_ru_conf_table as cb ON cb.config_profile_id = hs.config_profile_id LEFT JOIN get_odu16_ru_conf_table as op ON op.host_id=hs.host_id where hs.ip_address='%s' limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                #---- Query for get the last reboot time of particular device ------#
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()
            elif device_type.strip() == 'odu100':
                sql = "SELECT fm.rfChanFreq,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,lrb.ruoperationalState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM\
                    hosts as hs \
                    LEFT JOIN odu100_raTddMacStatusTable as fm ON fm.host_id = hs.host_id\
                    LEFT JOIN odu100_peerNodeStatusTable as ts ON ts.host_id = hs.host_id\
                    LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                    LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                    LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                    where hs.ip_address='%s' limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()
            elif device_type.strip() == 'idu4':
                sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw INNER JOIN idu_iduInfoTable as info ON info.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id WHERE hosts.ip_address='%s' limit 1" % ip_address
                cursor.execute(sql)
                result = cursor.fetchall()
            if device_type.strip() == 'odu16' or device_type.strip() == 'odu100':
                device_field = [
                    'Frequency', 'Slaves', 'Active Version', 'Hardware Version', 'Last Reboot Reason', 'Channel',
                    'Operation State', 'Node Type', 'MAC Address', 'Last Reboot Time']
                if len(result) > 0 and result != None:
                    if device_postfix == '(Master)':
                        master_slave_result = str(
                            '--' if result[1] == None or result[1] == "" else result[1])
                    else:
                        master_slave_result = 'N/A'
                    table_output.append([device_field[0], str(
                        '--' if result[0] == None or result[0] == "" else result[0])])
                    table_output.append(
                        [device_field[1], str(master_slave_result)])
                    table_output.append([device_field[2], str(
                        '--' if result[2] == None or result[2] == "" else result[2])])
                    table_output.append([device_field[3], str(
                        '--' if result[3] == None or result[3] == "" else result[3])])
                    table_output.append([device_field[4], str('--' if result[4] == None or result[4]
                                        == "" else last_reboot_resion[int(result[4])])])
                    table_output.append([device_field[5], str('--' if result[5] == None or result[5]
                                        == "" or result[5] < 0 else channel[int(result[5])])])
                    table_output.append([device_field[6], str('--' if result[6] == None or result[6]
                                        == "" else operation_state[int(result[6])])])
                    table_output.append([device_field[7], str('--' if result[7] == None or result[7]
                                        == "" else default_node_type[int(result[7])])])
                    table_output.append([device_field[8], str(
                        '--' if result[8] == None or result[8] == "" else result[8])])
                if len(last_reboot_time) > 0:
                    table_output.append([device_field[9], '--' if last_reboot_time[0][0]
                                        == None or last_reboot_time[0][0] == '' else last_reboot_time[0][0]])
                else:
                    table_output.append([device_field[9], '--'])

            if device_type.strip() == 'idu4':
                hour = 0
                minute = 0
                second = 0
                device_detail = ''
                device_field = [
                    'H/W Serial Number', 'System MAC', 'TDMOIP Interface MAC',
                    'Active Version', 'Passive Version', 'BootLoader Version', 'Temperature(C)', 'UpTime']
                if len(result) > 0 and result != None:
                    if result != None and result[0][7] != None:
                        hour = result[0][7] / 3600
                        minute = (result[0][7] / 60) % 60
                        second = result[0][7] % 60
                    table_output.append([device_field[0], str(
                        '--' if result[0][0] == None or result[0][0] == "" else result[0][0])])
                    table_output.append([device_field[1], str(
                        '--' if result[0][1] == None or result[0][1] == "" else result[0][1])])
                    table_output.append([device_field[2], str(
                        '--' if result[0][2] == None or result[0][2] == "" else result[0][2])])
                    table_output.append([device_field[3], str(
                        '--' if result[0][3] == None or result[0][3] == "" else result[0][3])])
                    table_output.append([device_field[4], str(
                        '--' if result[0][4] == None or result[0][4] == "" else result[0][4])])
                    table_output.append([device_field[5], str(
                        '--' if result[0][5] == None or result[0][5] == "" else result[0][5])])
                    table_output.append([device_field[6], str(
                        '--' if result[0][6] == None or result[0][6] == "" else result[0][6])])
                    table_output.append([device_field[7], (str(str(
                        hour) + "Hr " + str(minute) + "Min " + str(second) + "Sec"))])

            data1 = []
            data1.append(['', '%s Device Information' %
                         device_name[device_type], '', ''])
            t = Table(
                data1, [.021 * inch, 2.51 * inch, 2.26 * inch, 2.22 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            ubr_report.append(t)
            t = Table(table_output, [3.55 * inch, 3.55 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 10),
                                   ('FONT', (0, 1), (1, int(
                                       len(
                                           table_output)) - 1), 'Helvetica', 9),
                                   ('ALIGN', (1,
                                    0), (
                                        1, int(
                                            len(table_output)) - 1), 'CENTER'),
                                   ('BACKGROUND',
                                    (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                                   ('LINEABOVE',
                                    (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                                   ('GRID', (0, 0), (5, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                'BACKGROUND', (1, i), (1, i), (0.95, 0.95, 0.95)),
                                           ('BACKGROUND', (0, i - 1),
                                            (0, i - 1), (0.98, 0.98, 0.98)),
                                           ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), (0.9, 0.9, 0.9))
                                           ]))
            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            ubr_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            ubr_report.append(t)
            for i in range(len(tab_list)):
                ubr_report.append(Spacer(21, 21))
                table_split_result = table_name_list[i].split(',')
                table_name = table_split_result[0]
                x_axis = table_split_result[1]
                index_name = table_split_result[-2]
                graph_id = table_split_result[-1]
                field_column = field_list[i].split(',')
                update_field_name = ''
                start = 0  # default value for start and end here .
                limit = 0
                if graph_id.strip() == "odu100peernode":
                    interface_list['odu100_peerNodeStatusTable'] = {'1': '(Link1)', '2': '(Link2)', '3': '(Link3)', '4': '(Link4)', '5': '(Link5)', '6': '(Link6)', '7': '(Link7)', '8': '(Link8)', '9': '(Link9)',
                                                                  '10': '(Link10)', '11': '(Link11)', '12': '(Link12)', '13': '(Link13)', '14': '(Link14)', '15': '(Link15)', '16': '(Link16)'}
                else:
                    [interface_list.pop('odu100_peerNodeStatusTable') for ke in interface_list.keys(
                        ) if ke.strip() == 'odu100_peerNodeStatusTable']

                table_dic_key = [interface for interface in interface_list.keys(
                    ) if interface == table_name]
                interface_name = '' if len(
                    table_dic_key) == 0 else interface_list[table_dic_key[0]][tab_list[i]]
                output_result = self.common_graph_json(
                    display_type, user_id, table_name, x_axis, index_name, graph_id, limitFlag, start_date, end_date, start, limit,
                                                       ip_address, graph_list[i], update_field_name, tab_list[i], cal_list[i], field_column)
                d1_list = []
                first_column = x_axis.capitalize()
                headings = [first_column]
                if int(output_result['success']) == 0:
                    d1_list.append(output_result['timestamp'])
                    for data_list in output_result['data']:
#                        headings.append(data_list['name'][0])
                        headings.append(str(
                            data_list['name'][0]) + str(data_list['name'][1]))

                        d1_list.append(data_list['data'])
                    merge_result = merge_list(d1_list)
                # if no column select so report not created.
                if len(headings) < 2:
                    continue
                if table_name.strip() == 'get_odu16_peer_node_status_table' or table_name.strip() == 'odu100_peerNodeStatusTable':
                    table_output = []
                    table_output1 = []
                    if len(headings) > 9:
                        headings1 = [first_column]
                        headings1.extend(headings[9:])
                        table_output.append(headings[:9])
                        table_output1.append(headings1)
                        headings = headings[:9]
                        for small_list in merge_result:
                            table_output.append(small_list[:9])
                            table_output1.append(small_list[0])
                            table_output1.extend(small_list[9:])
                    else:
                        headings1 = []
                        table_output.append(headings)
                        for small_list in merge_result:
                            table_output.append(small_list)

                    data1 = []
                    data1.append(['', '%s%s' % (
                        graph_name_list[i], interface_name), '', ''])
                    t = Table(data1, [.021 * inch, 2.51 *
                              inch, 2.26 * inch, 2.22 * inch])
                    t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                        'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
                    ubr_report.append(t)
                    data = table_output
                    if len(headings) == 1:
                        t = Table(data, [7.1 * inch])
                    elif len(headings) == 2:
                        t = Table(data, [3.55 * inch, 3.55 * inch])
                    elif len(headings) == 3:
                        t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
                    elif len(headings) == 4:
                        t = Table(
                            data, [2 * inch, 1.7 * inch, 1.7 * inch, 1.7 * inch])
                    elif len(headings) == 5:
                        t = Table(data, [1.7 * inch,
                                  1.35 * inch, 1.35 * inch, 1.35 * inch, 1.35 * inch])
                    elif len(headings) == 6:
                        t = Table(data, [1.65 * inch, 1.09 * inch, 1.09 * inch,
                                  1.09 * inch, 1.09 * inch, 1.09 * inch, 1.09 * inch])
                    elif len(headings) == 7:
                        t = Table(data, [1.1 * inch, 1 * inch,
                                  1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])
                    elif len(headings) == 8:
                        t = Table(data, [1 * inch, .87 * inch, .87 * inch, .87 * inch, .87 *
                                  inch, .87 * inch, .87 * inch, .87 * inch, .87 * inch])
                    elif len(headings) == 9:
                        t = Table(data, [1.1 * inch, .75 * inch, .75 * inch, .75 * inch, .75 *
                                  inch, .75 * inch, .75 * inch, .75 * inch, .75 * inch])
        # t = Table(data,[2.7 * inch, 2.2 * inch, 1.5*inch, .7*inch])
                    t.setStyle(
                        TableStyle(
                            [(
                                'FONT', (0, 0), (len(headings) - 1, 0), 'Helvetica-Bold', 10),
                                           ('FONT', (0, 1), (len(
                                               headings) - 1, int(
                                                   len(
                                                       table_output)) - 1), 'Helvetica', 9),
                                           ('ALIGN', (1, 0), (len(
                                               headings) - 1, int(
                                                   len(
                                                       table_output)) - 1), 'CENTER'),
                                           ('BACKGROUND', (0, 0),
                                            (len(headings) - 1, 0), (0.9, 0.9, 0.9)),
                                           ('LINEABOVE', (0, 0),
                                            (len(headings) - 1, 0), 1.21, (0.35, 0.35, 0.35)),
                                           ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

                    for i in range(1, len(table_output)):
                        if i % 2 == 1:
                            t.setStyle(
                                TableStyle(
                                    [(
                                        'BACKGROUND', (1, i), (len(headings) - 1, i), (0.95, 0.95, 0.95)),
                                                   ('BACKGROUND', (0, i - 1),
                                                    (0, i - 1), (0.98, 0.98, 0.98)),
                                                   ]))
                        else:
                            t.setStyle(TableStyle([('BACKGROUND', (1, i), (len(headings) - 1, i), (0.9, 0.9, 0.9))
                                                   ]))

                    t.setStyle(TableStyle(
                        [('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
                    ubr_report.append(t)
                    data1 = []
                    if len(table_output) > 1:
                        data1.append(['1-' + str(len(
                            table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                    else:
                        data1.append(['0-' + str(len(
                            table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                    t = Table(data1, [7.10 * inch])
                    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                        'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
                    ubr_report.append(t)

                    if len(headings1) > 0:
                        ubr_report.append(Spacer(21, 21))
                        data1 = []
                        # data1.append(['','RSL Statistics','',''])
                        data1.append(['', '%s%s' % (
                            graph_name_list[i], interface_name), '', ''])
                        t = Table(data1, [.021 *
                                  inch, 2.51 * inch, 2.26 * inch, 2.22 * inch])
                        t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (
                            0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
                        ubr_report.append(t)
                        data = table_output1
                        if len(headings1) == 1:
                            t = Table(data, [7.1 * inch])
                        elif len(headings1) == 2:
                            t = Table(data, [3.55 * inch, 3.55 * inch])
                        elif len(headings1) == 3:
                            t = Table(
                                data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
                        elif len(headings1) == 4:
                            t = Table(data, [2 *
                                      inch, 1.7 * inch, 1.7 * inch, 1.7 * inch])
                        elif len(headings1) == 5:
                            t = Table(data, [1.7 * inch, 1.35 *
                                      inch, 1.35 * inch, 1.35 * inch, 1.35 * inch])
                        elif len(headings1) == 6:
                            t = Table(data, [1.65 * inch, 1.09 * inch, 1.09 *
                                      inch, 1.09 * inch, 1.09 * inch, 1.09 * inch, 1.09 * inch])
                        elif len(headings1) == 7:
                            t = Table(data, [1.1 * inch, 1 * inch, 1 *
                                      inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])
                        elif len(headings1) == 8:
                            t = Table(data, [1 * inch, .87 * inch, .87 * inch, .87 *
                                      inch, .87 * inch, .87 * inch, .87 * inch, .87 * inch, .87 * inch])
                        elif len(headings1) == 9:
                            t = Table(data, [1.1 * inch, .75 * inch, .75 * inch, .75 *
                                      inch, .75 * inch, .75 * inch, .75 * inch, .75 * inch, .75 * inch])
            # t = Table(data,[2.7 * inch, 2.2 * inch, 1.5*inch, .7*inch])
                        t.setStyle(
                            TableStyle(
                                [(
                                    'FONT', (0, 0), (len(headings1) - 1, 0), 'Helvetica-Bold', 10),
                                               ('FONT', (0, 1), (len(headings1) - 1, int(len(
                                                   table_output1)) - 1), 'Helvetica', 9),
                                               ('ALIGN', (1, 0), (len(
                                                   headings1) - 1, int(
                                                       len(
                                                           table_output1)) - 1), 'CENTER'),
                                               ('BACKGROUND', (0, 0), (len(
                                                   headings1) - 1, 0), (
                                                       0.9, 0.9, 0.9)),
                                               ('LINEABOVE', (0,
                                                0), (
                                                    len(
                                                        headings1) - 1, 0), 1.21, (0.35, 0.35, 0.35)),
                                               ('GRID', (0, 0), (8, int(len(table_output1)) - 1), 0.31, (0.75, 0.75, 0.75))]))

                        for i in range(1, len(table_output1)):
                            if i % 2 == 1:
                                t.setStyle(
                                    TableStyle(
                                        [(
                                            'BACKGROUND', (1, i), (len(headings1) - 1, i), (0.95, 0.95, 0.95)),
                                                       ('BACKGROUND', (0, i - 1), (
                                                           0, i - 1), (
                                                               0.98, 0.98, 0.98)),
                                                       ]))
                            else:
                                t.setStyle(TableStyle([('BACKGROUND', (1, i), (len(headings1) - 1, i), (0.9, 0.9, 0.9))
                                                       ]))

                        t.setStyle(TableStyle([(
                            'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
                        ubr_report.append(t)
                        data1 = []
                        if len(table_output) > 1:
                            data1.append(['1-' + str(len(
                                table_output1) - 1) + ' of ' + str(len(table_output1) - 1)])
                        else:
                            data1.append(['0-' + str(len(
                                table_output1) - 1) + ' of ' + str(len(table_output1) - 1)])
                        t = Table(data1, [7.10 * inch])
                        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (
                            0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
                        ubr_report.append(t)

                else:
                    table_output = []
                    table_output.append(headings)
                    for small_list in merge_result:
                        table_output.append(small_list)
                    data1 = []
                    data1.append(['', '%s%s' % (
                        graph_name_list[i], interface_name), '', ''])
                    t = Table(data1, [.021 * inch, 2.51 *
                              inch, 2.26 * inch, 2.22 * inch])
                    t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                        'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
                    ubr_report.append(t)

                    data = table_output
                    if len(headings) == 1:
                        t = Table(data, [7.1 * inch])
                    elif len(headings) == 2:
                        t = Table(data, [3.55 * inch, 3.55 * inch])
                    elif len(headings) == 3:
                        t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
                    elif len(headings) == 4:
                        t = Table(
                            data, [2 * inch, 1.7 * inch, 1.7 * inch, 1.7 * inch])
                    elif len(headings) == 5:
                        t = Table(data, [1.7 * inch,
                                  1.35 * inch, 1.35 * inch, 1.35 * inch, 1.35 * inch])
                    elif len(headings) == 6:
                        t = Table(data, [1.15 * inch, 1.19 *
                                  inch, 1.19 * inch, 1.19 * inch, 1.19 * inch, 1.19 * inch])
                    elif len(headings) == 7:
                        t = Table(data, [1.1 * inch, 1 *
                                  inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])
                    elif len(headings) == 8:
                        t = Table(data, [1.17 * inch, .97 * inch,
                                  .97 * inch, .97 * inch, .97 * inch, .97 * inch, .97 * inch, .97 * inch])
                    elif len(headings) == 9:
                        t = Table(data, [1.1 * inch, .75 * inch, .75 * inch, .75 * inch, .75 *
                                  inch, .75 * inch, .75 * inch, .75 * inch, .75 * inch])

        # t = Table(data,[2.7 * inch, 2.2 * inch, 1.5*inch, .7*inch])
                    t.setStyle(
                        TableStyle(
                            [(
                                'FONT', (0, 0), (len(headings) - 1, 0), 'Helvetica-Bold', 10),
                                           ('FONT', (0, 1), (len(
                                               headings) - 1, int(
                                                   len(
                                                       table_output)) - 1), 'Helvetica', 9),
                                           ('ALIGN', (1, 0), (len(
                                               headings) - 1, int(
                                                   len(
                                                       table_output)) - 1), 'CENTER'),
                                           ('BACKGROUND', (0, 0),
                                            (len(headings) - 1, 0), (0.9, 0.9, 0.9)),
                                           ('LINEABOVE', (0, 0),
                                            (len(headings) - 1, 0), 1.21, (0.35, 0.35, 0.35)),
                                           ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

                    for i in range(1, len(table_output)):
                        if i % 2 == 1:
                            t.setStyle(
                                TableStyle(
                                    [(
                                        'BACKGROUND', (1, i), (len(headings) - 1, i), (0.95, 0.95, 0.95)),
                                                   ('BACKGROUND', (0, i - 1),
                                                    (0, i - 1), (0.98, 0.98, 0.98)),
                                                   ]))
                        else:
                            t.setStyle(TableStyle([('BACKGROUND', (1, i), (len(headings) - 1, i), (0.9, 0.9, 0.9))
                                                   ]))
                    t.setStyle(TableStyle(
                        [('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
                    ubr_report.append(t)
                    data1 = []
                    if len(table_output) > 1:
                        data1.append(['1-' + str(len(
                            table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                    else:
                        data1.append(['0-' + str(len(
                            table_output) - 1) + ' of ' + str(len(table_output) - 1)])
                    t = Table(data1, [7.10 * inch])
                    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                        'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
                    ubr_report.append(t)

            ubr_report.append(Spacer(21, 21))
            sql = "SELECT ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,ta.trap_receive_date,description FROM trap_alarms as ta inner join hosts on ta.agent_id=hosts.ip_address WHERE ta.agent_id='%s' and ta.timestamp>='%s' and ta.timestamp<='%s' order by ta.timestamp desc limit 7 " % (ip_address, start_date, end_date)

            cursor.execute(sql)
            current_alarm = cursor.fetchall()
            table_output = []
            serevity_list = ['Normal', 'Information', 'Normal',
                'Minor', 'Major', 'Critical']
            headings = ['Received Date', 'Severity',
                'Event Name', 'Event ID', 'Event Type', 'Description']
            table_output.append(headings)
            for row in current_alarm:
                table_output.append([row[5], serevity_list[int(
                    row[0])], row[1], row[2], row[3], row[6]])
                # table_output.append([row[0],row[5],row[4],row[1],row[2],row[3],row[6]])
            data1 = []
            data1.append(['', 'Device Events ', '', ''])
            t = Table(
                data1, [.021 * inch, 2.21 * inch, 2.56 * inch, 2.22 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            ubr_report.append(t)
            data = table_output
            t = Table(data, [1.15 * inch, 1.19 * inch, 1.19 *
                      inch, 1.19 * inch, 1.19 * inch, 1.19 * inch])
            t.setStyle(
                TableStyle(
                    [(
                        'FONT', (0, 0), (len(headings) - 1, 0), 'Helvetica-Bold', 10),
                                   ('FONT', (0, 1), (len(headings) -
                                    1, int(
                                        len(
                                            table_output)) - 1), 'Helvetica', 9),
                                   ('ALIGN', (1, 0), (len(
                                       headings) - 1, int(
                                           len(table_output)) - 1), 'CENTER'),
                                   ('BACKGROUND', (
                                       0, 0), (
                                           len(
                                               headings) - 1, 0), (
                                                   0.9, 0.9, 0.9)),
                                   ('LINEABOVE', (0, 0), (
                                       len(
                                           headings) - 1, 0), 1.21, (
                                               0.35, 0.35, 0.35)),
                                   ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                'BACKGROUND', (1, i), (len(headings) - 1, i), (0.95, 0.95, 0.95)),
                                           ('BACKGROUND', (0, i - 1),
                                            (0, i - 1), (0.98, 0.98, 0.98)),
                                           ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (len(headings) - 1, i), (0.9, 0.9, 0.9))
                                           ]))
            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            ubr_report.append(t)
            data1 = []
            if len(table_output) > 1:
                data1.append(['1-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            else:
                data1.append(['0-' + str(
                    len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
            t = Table(data1, [7.10 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), (
                'GRID', (0, 0), (5, 0), 0.31, (0.75, 0.75, 0.75)), ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
            ubr_report.append(t)

            ubr_report.append(Spacer(31, 31))
            data1 = []
            data1.append(["** DU Device Unreachable"])
            t = Table(data1, [7.1 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.51, 0.51, 0.51)), (
                'FONT', (0, 0), (0, 0), 'Helvetica', 11), ('TEXTCOLOR', (0, 0), (0, 0), colors.white)]))
            ubr_report.append(t)
#            ubr_report.append(Spacer(21,21))
#            sql="SELECT ta.trap_receive_date,ta.trap_event_type,ta.description FROM trap_alarm_current as ta inner join hosts on ta.agent_id=hosts.ip_address WHERE ta.agent_id='%s' and ta.timestamp>='%s' and ta.timestamp<='%s'  order by ta.timestamp desc "%(ip_address,start_date,end_date)
#            cursor.execute(sql)
#            all_traps=cursor.fetchall()
#            table_output=[]
#            serevity_list=['Normal','Information','Normal','Minor','Major','Critical']
#            headings = ['severity','Event Name','Device Type','Event Id','Event Type','Receive Date']
#            table_output.append(headings)
#            for row in all_traps:
#                table_output.append([row[0],row[1],row[2]])
#            data1=[]
#            data1.append(['','Device Events','',''])
#            t = Table(data1, [.021*inch,2.21 * inch, 2.56 * inch, 2.22*inch])
#            t.setStyle(TableStyle([('BACKGROUND',(1,0),(1,0),(0.35,0.35,0.35)),('FONT', (0, 0), (1, 0), 'Helvetica', 11),#('TEXTCOLOR',(1,0),(2,0),colors.white)]))
#            ubr_report.append(t)
#            data=table_output
#	    t = Table(data,[1.2 * inch, 2.4 * inch, 3.51*inch])
#            t.setStyle(TableStyle([('FONT', (0, 0), (len(headings)-1, 0), 'Helvetica-Bold', 10),
#            ('FONT', (0, 1), (len(headings)-1, int(len(table_output))-1), 'Helvetica', 9),
#            ('ALIGN', (1,0), (len(headings)-1, int(len(table_output))-1), 'CENTER'),
#            ('BACKGROUND',(0,0),(len(headings)-1,0),(0.9,0.9,0.9)),
#            ('LINEABOVE',(0,0), (len(headings)-1, 0), 1.21,(0.35,0.35,0.35)),
#            ('GRID',(0,0),(8,int(len(table_output))-1),0.31,(0.75,0.75,0.75))]))

#            for i in range(1,len(table_output)):
#                if i%2==1:
#                    t.setStyle(TableStyle([('BACKGROUND',(1,i),(len(headings)-1,i),(0.95,0.95,0.95)),
#                            ('BACKGROUND',(0,i-1),(0,i-1),(0.98,0.98,0.98)),
#                               ]))
#                else:
#                    t.setStyle(TableStyle([('BACKGROUND',(1,i),(len(headings)-1,i),(0.9,0.9,0.9))
#                               ]))
#            t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),(0.9,0.9,0.9))]))
#            ubr_report.append(t)
#            data1=[]
#            if len(table_output)>1:
#                data1.append(['1-'+str(len(table_output)-1)+' of '+str(len(table_output)-1)])
#            else:
#                data1.append(['0-'+str(len(table_output)-1)+' of '+str(len(table_output)-1)])
#            t = Table(data1, [7.10*inch])
#            t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),(0.9,0.9,0.9)),('GRID',(0,0),(5,0),0.31,(0.75,0.75,0.75)),('ALIGN', (0,0), (0, 0), 'RIGHT')]))
#            ubr_report.append(t)

            pdf_doc.build(ubr_report)
            output_dict = {'success': 0, 'output':
                'pdf downloaded', 'file_name': save_file_name}
            return output_dict

        except MySQLdb as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 102 ' + str(
                err_obj.get_error_msg(102)), 'main_msg': str(e[-1])}
            return output_dict
        except ImportError, e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 101 ' + str(
                err_obj.get_error_msg(101)), 'main_msg': str(e[-1])}
            return output_dict
        except IOError, e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 103 ' + str(
                err_obj.get_error_msg(103)), 'main_msg': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 1, 'error_msg': 'Error No : 104' + str(
                err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'error_msg': 'Error No : 105 ' + str(
                err_obj.get_error_msg(105)), 'main_msg': str(e[-1])}
            return output_dict
        finally:
            if db.open:
                db.close()


def merge_list(arg):
    """

    @param arg:
    @return:
    """
    total = len(arg)
    flag = True
    d2 = []
    for i in range(total - 1):
        if len(arg[i]) != len(arg[i + 1]):
            flag = False
            break
        else:
            flag = True

    if flag:
        for i in range(len(arg[0])):
            d1 = []
            for j in range(total):
                d1.append(str(arg[j][i]))
            d2.append(d1)
        return d2
    else:
        return []


def main_outage(result_tuple, end_date):
    """

    @param result_tuple:
    @param end_date:
    @return:
    """
    try:
        is_date = 0
        main_date = ''
        main_ip = ''
        main_list = []
        uptime = None
        downtime = None
        prev_value = ''
        temp_temp = []
        for tpl in result_tuple:
            tpl_temp = tpl
            temp_ip = tpl[3]
            temp_date = tpl[2]
            temp_value = tpl[0]
            if temp_ip == main_ip:
                if temp_date.month > main_date.month or temp_date.day > main_date.day:
                    is_date = 1
                else:
                    if temp_value == '50002':
                        if uptime == None:
                            uptime = (temp_date - main_date)
                        else:
                            uptime += (temp_date - main_date)

                    elif temp_value == '50001':
                        if downtime == None:
                            downtime = (temp_date - main_date)
                        else:
                            downtime += (temp_date - main_date)
            else:
                is_new = 1

            if is_new:
                if prev_value != '':
                    is_date = 1
                else:
                    main_date = temp_date
                main_ip = temp_ip
                is_new = 0

            if is_date:
                if uptime == None or downtime == None:
                    mid_date = datetime(main_date.year,
                                        main_date.month, main_date.day, 23, 59, 59)
                    delta = mid_date - main_date
                    if prev_value == '50002':
                        uptime = delta
                    elif prev_value == '50001':
                        downtime = delta

                main_list.append([main_date, tpl_temp[3], uptime, downtime])
#                    day_diff=(temp_date-main_date).days
                # day_diff = round(float(d.seconds + d.days *
                # 86400)/float(86400))
                day_diff = temp_date.day - main_date.day
                if day_diff > 1:
                    for i in range(1, day_diff):
                        leftout_date = main_date + timedelta(days=i)
                        if prev_value == '50002':
                            main_list.append([leftout_date,
                                             tpl_temp[3], timedelta(0, 86399), None])
                        elif prev_value == '50001':
                            main_list.append([leftout_date,
                                             tpl_temp[3], None, timedelta(0, 86399)])
                main_date = temp_date
                uptime = None
                downtime = None
                is_date = 0

            prev_value = temp_value

        if uptime == None or downtime == None:
            mid_date = datetime(
                main_date.year, main_date.month, main_date.day, 23, 59, 59)
            delta = mid_date - main_date
            if prev_value == '50002':
                uptime = delta
            elif prev_value == '50001':
                downtime = delta
        main_list.append([main_date, tpl_temp[3], uptime, downtime])
        day_diff = (end_date - main_date).days  # temp_date.day-main_date.day
        if day_diff > 1:
            for i in range(1, day_diff + 1):
                leftout_date = main_date + timedelta(days=i)
                if prev_value == '50002':
                    main_list.append([leftout_date,
                                     tpl_temp[3], timedelta(0, 86399), None])
                elif prev_value == '50001':
                    main_list.append([leftout_date,
                                     tpl_temp[3], None, timedelta(0, 86399)])
            main_date = leftout_date
        day_diff = end_date.day - main_date.day
        if day_diff > 1:
            leftout_date = main_date + timedelta(days=1)
            if prev_value == '50002':
                main_list.append(
                    [leftout_date, tpl_temp[3], timedelta(0, 86399), None])
            elif prev_value == '50001':
                main_list.append(
                    [leftout_date, tpl_temp[3], None, timedelta(0, 86399)])
        main_dict = {}
        main_dict['success'] = 0
        main_dict['result'] = main_list
        main_dict['outage'] = "main_outage"
        return main_dict
    except Exception, e:
        main_dict = {}
        main_dict['success'] = 1
        main_dict['result'] = str(e)
        return main_dict


def get_outage(d1, d2, ip_address):
    """

    @param d1:
    @param d2:
    @param ip_address:
    @return: @raise:
    """
    try:
        conn, cursor = mysql_connection()
        if conn == 1:
            raise SelfException(cursor)
        date_temp1 = str(d1)
        date_temp2 = str(d2)
        start_date = date_temp1
        end_date = date_temp2
        li_result = []
        # main_outage(result_tuple,end_date):
        main_result = []
        if 1 == 1:
            sel_query = "SELECT trap_event_id,trap_event_type,timestamp,agent_id FROM system_alarm_table \
            where agent_id='%s' and timestamp>='%s' and timestamp<='%s' order by timestamp" % (ip_address, start_date, end_date)
            cursor.execute(sel_query)
            result = cursor.fetchall()
            sel_query = "SELECT trap_event_id,trap_event_type,timestamp,agent_id FROM system_alarm_table \
             WHERE timestamp<='%s' and agent_id='%s' order by timestamp desc limit 1" % (start_date, ip_address)
            cursor.execute(sel_query)
            status_result = cursor.fetchall()
            if status_result != () and result != ():
                t_date = result[0][2]
                t_date = t_date.replace(hour=0, minute=0, second=0)
                t_list = ((status_result[0][0],
                          status_result[0][1], t_date, status_result[0][3]),)
                result = t_list + result

            m = MainOutage(result, datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"), datetime.strptime(
                    start_date, "%Y-%m-%d %H:%M:%S"))
            temp_res = m.get_outage()
            # temp_res = main_outage(result, datetime.strptime(
            #     end_date[:18], "%Y-%m-%d %H:%M:%S"))
            if str(temp_res['success']) == "0":
                li_res = temp_res['result']
                tr = []
                for i in li_res:
                    if i[-2] == None:
                        uptime = 0
                    else:
                        uptime = i[-2].seconds
                    if i[-1] == None:
                        downtime = 0
                    else:
                        downtime = i[-1].seconds
                    total = uptime + downtime
                    if total != 0:
                        i[0] = str(i[0])[:11]
                        i[-2] = (uptime * 100) / total
                        i[-1] = (downtime * 100) / total
                        if int(i[-2]) + int(i[-1]) != 100:
                            i[-2] = int(i[-2]) + 1
                        tr.append(i)
                        #[leftout_date,main_ip,tpl_temp[4],tpl_temp[5],tpl_temp[6],None,timedelta(0, 86399)])
                        main_result.append(i)

        result_dict = {}
        result_dict['success'] = 0
        result_dict['result'] = main_result
        result_dict['outage'] = "get_outage"
        return result_dict
    except SelfException:
        output_dict = {'success': 1, 'error_msg': 'Error No : 104' +
            str(err_obj.get_error_msg(104)), 'main_msg': str(e[-1])}
        return output_dict
    except Exception, e:
        main_dict = {}
        main_dict['success'] = 1
        main_dict['result'] = str(e)
        return main_dict



