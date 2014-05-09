#!/usr/bin/python2.6
# import the packeges
import config
import htmllib
import time
import cgi
import MySQLdb
import sys
from common_controller import *
from nms_config import *
from odu_controller import *
from datetime import datetime
from datetime import timedelta
from mysql_collection import mysql_connection
from unmp_dashboard_config import DashboardConfig
from operator import itemgetter
from utility import Validation
from error_message import ErrorMessageClass
from specific_dashboard_bll import SPDashboardBll, get_master_slave_value
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


class APAdvancedGraph(object):
    """
    AP device related advanced graph class
    """

    def get_host_id(self, ip_address, device_type):
        """

        @param ip_address:
        @param device_type:
        @return: @raise:
        """
        try:
            host_id = 1  # Default value
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
            sel_query = "SELECT host_id FROM hosts WHERE device_type_id='%s' and ip_address=%s and is_deleted=0" % (
                device_type, str(ip_address))
            cursor.execute(sel_query)
            host_result = cursor.fetchall()
            if len(host_result) > 0:
                host_id = host_result[0][0] if host_result[
                    0][0] != None or host_result[0][0] != "" else ""
            output_dict = {'success': 0, 'host_id': host_id}
            return output_dict
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

    def total_graph_name_display(self, device_type_id, user_id):
        """

        @param device_type_id:
        @param user_id:
        @return: @raise:
        """
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            sel_query = "SELECT graph_display_name,graph_display_id FROM graph_templet_table WHERE device_type_id='%s' and user_id='%s'\
             and is_disabled=0 and dashboard_type=0" % (device_type_id, user_id)
            cursor.execute(sel_query)
            graph_name = cursor.fetchall()
            output_dict = {'success': 0, 'result': graph_name}
            return output_dict
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

    def advanced_graph_json(self, graph_id, device_type_id, user_id, ip_address):
        """

        @param graph_id:
        @param device_type_id:
        @param user_id:
        @param ip_address:
        @return: @raise:
        """
        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)

            # check the deivce is master or not.
            master_slave_status = get_master_slave_value(ip_address)

            sel_query = "SELECT graph_display_id,graph_display_name,user_id,is_disabled,device_type_id,graph_id,graph_tab_option,refresh_button,next_pre_option,start_value,end_value,graph_width,graph_height,graph_cal_id,show_type,show_field,show_cal_type,show_tab_option,auto_refresh_time_second FROM graph_templet_table WHERE user_id='%s' AND device_type_id='%s' AND graph_display_id='%s' and dashboard_type=0" % (
                user_id, device_type_id, graph_id)
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
                if master_slave_status['success'] == 0 and int(master_slave_status['status']) > 0:
                    if len(option_tuple) > 0 and (row[0] == 'odu100rssi' or row[0] == 'odu16rssi' or row[0] == 'odu100rssi2' or row[0] == 'odu100link'):
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
                        interface_name.append('Master')
                        check_val = int(1)
                    else:
                        for interface in interface_tuple:
                            interface_value.append(interface[0])
                            interface_name.append(interface[1])
                            if int(interface[2]) == 1:
                                check_val = int(interface[0])
                else:
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

                # this is check the master or slave for sync lsot graph showing
                # or not.
                if master_slave_status['success'] == 0 and int(master_slave_status['status']) == 0:
                    if ajax_json['data']['table_name'].split(',')[0] == 'odu100_synchStatisticsTable' or ajax_json['data']['table_name'].split(',')[0] == 'get_odu16_synch_statistics_table':
                        pass
                    else:
                        graph_json.append(graph_dict)
                else:
                    graph_json.append(graph_dict)
#		graph_json.append(graph_dict)

            output_dic = {'success': 0, 'graphs': graph_json}
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

    def advanced_graph_data(self, display_type, user_id, table_name, x_axis_value, index_name, graph_id, start, limit, flag, start_date, end_date, ip_address, graph, update_field_name, interface=1, value_cal=1, *column_name):
        """

        @param display_type:
        @param user_id:
        @param table_name:
        @param x_axis_value:
        @param index_name:
        @param graph_id:
        @param start:
        @param limit:
        @param flag:
        @param start_date:
        @param end_date:
        @param ip_address:
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
        sp_bll_obj = SPDashboardBll(
        )  # specific bll dashboard file object created for reusablity

        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
            if str(update_field_name).strip() == 'calType':
                up_query = "update  graph_templet_table set graph_cal_id =%s where user_id='%s' and graph_display_id='%s' and dashboard_type=0" % (
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
                up_query = "update  graph_templet_table set graph_id =%s where user_id='%s' and graph_display_id='%s' and dashboard_type=0" % (graph, user_id, graph_id)
                cursor.execute(up_query)
                conn.commit()

            # get the data from graph field table .
            get_coloum = "SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' AND user_id='%s'" % (
                graph_id, user_id)
            cursor.execute(get_coloum)
            coloum_result = cursor.fetchall()
            clm_dict = dict(zip([coloum_result[i][0] for i in range(
                len(coloum_result))], [coloum_result[i][1] for i in range(len(coloum_result))]))
            table_field_dict1 = {table_name: clm_dict}
            graph_field_dict = dict(
                (field[0], field[2]) for field in coloum_result)

            sel_query = "select graph_title,graph_subtitle from graph_templet_table where graph_display_id='%s' and user_id='%s' and dashboard_type=0" % (
                graph_id, user_id)
            cursor.execute(sel_query)
            graph_name_result = cursor.fetchall()
            graph_title = ''  # default value
            graph_sub_title = ''  # default value
            if len(graph_name_result) > 0:
                graph_title = '' if graph_name_result[0][
                    0] == None or graph_name_result[0][0] == '' else graph_name_result[0][0]
                graph_sub_title = '' if graph_name_result[0][
                    1] == None or graph_name_result[0][1] == '' else graph_name_result[0][1]

            if str(graph_id).strip() == 'apVAPUserConnect123':
                if column_name[0][0] == "rssi":
                    column_list = ','.join(column_name[0])
                    column_list = ',' + column_list
                else:
                    column_list = ''
                sql = "select addressMAC %s from ap25_vapClientStatisticsTable as ap inner join hosts on ap.host_id=hosts.host_id where hosts.ip_address='%s'\
                 order by ap25_vapClientStatisticsTable_id limit %s,%s" % (column_list, ip_address, start, limit)
                cursor.execute(sql)
                connected_user_result = cursor.fetchall()
                mac_list = []
                rssi_list = []
                json_data = []
                var_count = 0
                for connect_user in connected_user_result:
                    var_count = len(connect_user)
                    mac_list.append(connect_user[0])
                    if len(connect_user) == 2:
                        rssi_list.append(connect_user[1])

                time_list = mac_list
                if var_count == 2:
                    json_data.append(
                        {'name': ['RSSI', ' dbm'], 'data': rssi_list})
                else:
                    json_data.append({'name': ['', ''], 'data': rssi_list})
                    time_list = []

            elif table_name.strip() == 'outage':
                # if (end_date - start_date).days < 5:
                #     start_date = datetime.strptime(datetime.strftime(datetime.now(
                #     ) + timedelta(days=-4), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                outage_result = sp_bll_obj.sp_advanced_outage_graph(
                    display_type, ip_address, start_date, end_date)
                if int(outage_result['success']) != 0:
                    return outage_result
                if column_name[0][0] == "":
                    output_dic = {'success': 0, 'timestamp': outage_result['date_days'], 'data': [],
                                  'graph_title': graph_title, 'graph_sub_title': graph_sub_title}
                else:
                    for name in column_name[0]:
                        json_data.append(
                            {"data": outage_result[name], "name": [name, '(%)']})
                    time_list = outage_result['date_days']
                    output_dic = {
                        'success': 0, 'timestamp': time_list, 'data': json_data, 'graph_title': graph_title, 'graph_sub_title': graph_sub_title,
                        'range_min': 0, 'range_max': 100}
                return output_dic
            elif (table_name.strip() == 'odu100_peerNodeStatusTable' or table_name.strip() == 'get_odu16_peer_node_status_table' or table_name.strip() == 'ap25_vapClientStatisticsTable') and (graph_id.strip() == 'odu100rssi' or graph_id.strip() == 'odu100link' or graph_id.strip() == 'odu16rssi' or graph_id.strip() == 'odu100rssi2' or graph_id.strip() == 'totalConnectedClient' or graph_id.strip() == 'vapConnectedClient'):
                odu100_rssi_result = self.sp_signal_strength_graph(
                    display_type, graph_id, ip_address, start_date, end_date, table_name, column_name[0])
                if int(odu100_rssi_result['success']) != 0:
                    return odu100_rssi_result
                output_dic = {'success': 0, 'timestamp': odu100_rssi_result['time_stamp'], 'data': odu100_rssi_result['display_signal_strength'], 'graph_title': graph_title,
                              'graph_sub_title': graph_sub_title, 'range_min': odu100_rssi_result['range_min'], 'range_max': odu100_rssi_result['range_max']}
                return output_dic
            else:
                sel_query = "Select "
                if len(column_name[0][0]) > 0:
                    column_list = ',gp_tab.'.join(column_name[0])
                    column_list = 'gp_tab.' + column_list

                    sel_query += column_list + "," + "gp_tab.%s from %s as gp_tab INNER JOIN hosts ON hosts.host_id=gp_tab.host_id \
                    where hosts.ip_address='%s' AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' and gp_tab.%s = '%s' and hosts.is_deleted=0 \
                    order by gp_tab.timestamp desc" % (x_axis_value, table_name, ip_address, start_date, end_date, index_name, interface)
                else:
                    sel_query += "gp_tab.%s from %s as gp_tab INNER JOIN hosts ON hosts.host_id=gp_tab.host_id \
                    where hosts.ip_address='%s' AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' and gp_tab.%s = '%s' and hosts.is_deleted=0 \
                    order by gp_tab.timestamp desc" % (x_axis_value, table_name, ip_address, start_date, end_date, index_name, interface)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                for i in range(len(column_name[0])):
                    data_list.append([])
                default_value = {'y': 0, 'marker': {
                    'symbol': 'url(images/device-down.gif)'}}
                if display_type == 'table' or display_type == 'excel':
                    default_value = 'Device Unreachable'

                if calculation[int(value_cal) - 1] == 'normal':
                    for row in result:
                        for i in range(len(row) - 1):
                            data_list[i].append(0 if row[i]
                                                == None or row[i] == None else int(row[i]))
                        if display_type == 'table' or display_type == 'excel':
                            time_list.append(str((row[len(row) - 1])))
                        else:
                            time_list.append(time.mktime(datetime.strptime(
                                str(row[len(row) - 1])[:19], '%Y-%m-%d %H:%M:%S').timetuple()) * 1000)
                elif calculation[int(value_cal) - 1] == 'delta':
                    for k in range(len(result) - 1):
                        i = 0
                        count = 0
                        for d2 in range(len(result[k]) - 1):
                            if result[k][d2] == 1111111 or str(result[k][d2]) == '1111111':
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

                        if display_type == 'table' or display_type == 'excel':
                            time_list.append(
                                str((result[k][len(result[k]) - 1])))
                        else:
                            time_list.append(time.mktime(datetime.strptime(str(result[k][len(
                                result[k]) - 1])[:19], '%Y-%m-%d %H:%M:%S').timetuple()) * 1000)

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
                'range_min': 0, 'range_max': 0}
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

    def sp_signal_strength_graph(self, display_type, graph_id, ip_address, start_time, end_time, table_name, column_list):
        """

        @param display_type:
        @param graph_id:
        @param ip_address:
        @param start_time:
        @param end_time:
        @param table_name:
        @param column_list:
        @return: @raise:
        """
        min_value = 0
        max_value = 0
        signal_flag = 1
        rssi_dict = []
        default_list = {}
        default_rssi = {}
        time_stamp_signal1 = []
        default_value = {'y': 0, 'marker': {'symbol':
                                            'url(images/device-down.gif)'}}
        new_default_value = {'y': 0, 'marker': {'symbol':
                                                'url(images/device-down.gif)'}}
        link_name = "Link"
        qaulity = '(%)'

        try:
            # Open database connection
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            if display_type.strip() != 'graph':
                new_default_value = "--"
                default_value = 'Device Unreachable'

            column_field = "''"
            for col in column_list:
                if str(col).strip() != '':
                    rssi_dict.append({int(col): []})
                    default_rssi[int(col)] = new_default_value
                    column_field = ','.join(column_list)
            default_list = default_rssi
            master_slave_status = get_master_slave_value(ip_address)

            status = 0
            if master_slave_status['success'] == 0:
                if master_slave_status['device_type'] == 'ap25':
                    status = 0
                else:
                    status = master_slave_status['status']
            status_name = 'Master' if status == 0 else 'Slave'
            signal_flag = 0

            if (graph_id).strip() == 'odu100link' or (graph_id).strip() == 'odu16link':
                if table_name.strip() == 'odu100_peerNodeStatusTable':
                    min_value = 0
                    min_value = 100
                    sel_query = "select odu.timeSlotIndex,(IFNULL((odu.txLinkQuality),0)),odu.timestamp,odu.ssIdentifier,odu.linkStatus,odu.tunnelStatus,\
                    odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id \
                    where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeSlotIndex IN (%s) and h.is_deleted=0 \
                    order by odu.timestamp desc" % (ip_address, start_time, end_time, column_field)
                elif table_name.strip() == 'get_odu16_peer_node_status_table':
                    min_value = -100
                    min_value = 1
                    sel_query = "select odu.timeslot_index,(IFNULL((odu.sig_strength),0)),odu.timestamp,odu.ssidentifier,odu.link_status,odu.tunnel_status,\
                    odu.peer_mac_addr from  get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                    where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeslot_index IN (%s) and h.is_deleted=0  \
                    order by odu.timestamp desc" % (ip_address, start_time, end_time, column_field)
            elif table_name.strip() == 'ap25_vapClientStatisticsTable':
                qaulity = '(count)'
                link_name = "VAP"
                if (graph_id).strip() == 'vapConnectedClient':
                    min_value = 0
                    min_value = 0
                    sel_query = "select ap.vap_id,count(ap.addressMAC),ap.timestamp from  ap25_vapClientStatisticsTable as ap\
                     INNER JOIN hosts as h on ap.host_id = h.host_id  where h.ip_address='%s' and ap.vap_id IN (%s) AND \
                     ap.addressMAC!='' AND ap.timestamp >= '%s' AND ap.timestamp <='%s' and h.is_deleted=0  group by ap.vap_id,ap.timestamp \
                     order by ap.timestamp desc" % (ip_address, column_field, start_time, end_time)
                elif (graph_id).strip() == 'totalConnectedClient':
                    link_name = "Total Client"
                    min_value = 0
                    min_value = 0
                    sel_query = "select ap.vap_id,count(ap.addressMAC),ap.timestamp from  ap25_vapClientStatisticsTable as ap \
                    INNER JOIN hosts as h on ap.host_id = h.host_id  where h.ip_address='%s' and ap.vap_id IN (1,2,3,4,5,6,7,8) AND\
                     ap.addressMAC!='' AND ap.timestamp >= '%s' AND ap.timestamp <='%s' and h.is_deleted=0  group by ap.timestamp \
                     order by ap.timestamp desc" % (ip_address, start_time, end_time)
            else:
                qaulity = '(dBm)'
                if table_name.strip() == 'odu100_peerNodeStatusTable':
                    min_value = -100
                    min_value = 1
                    sel_query = "select odu.timeSlotIndex,(IFNULL((odu.sigStrength1),0)),odu.timestamp,odu.ssIdentifier,\
                    odu.linkStatus,odu.tunnelStatus,odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id\
                     where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeSlotIndex IN (%s) and h.is_deleted=0 \
                     order by odu.timestamp desc" % (ip_address, start_time, end_time, column_field)
                elif table_name.strip() == 'get_odu16_peer_node_status_table':
                    min_value = -100
                    min_value = 1
                    sel_query = "select odu.timeslot_index,(IFNULL((odu.sig_strength),0)),odu.timestamp,odu.ssidentifier,odu.link_status,odu.tunnel_status,\
                    odu.peer_mac_addr from  get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id \
                     where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeslot_index IN (%s) and h.is_deleted=0 \
                     order by odu.timestamp desc" % (ip_address, start_time, end_time, column_field)

            cursor.execute(sel_query)
            signal_strength = cursor.fetchall()
            flag = 0
            for k in range(0, len(signal_strength) - 1):
                flag = 1
                if signal_strength[k][1] == 1111111 or str(signal_strength[k][1]) == '1111111':
                    for i in range(len(rssi_dict)):
                        rssi_dict[i][rssi_dict[i]
                                     .keys()[0]].append(default_value)
                    time_stamp_signal1.append(datetime.strptime(
                        str(signal_strength[k][2])[:19], '%Y-%m-%d %H:%M:%S'))
                else:
                    if signal_strength[k][2] == signal_strength[k + 1][2]:
                        default_rssi[int(
                            signal_strength[k][0])] = int(signal_strength[k][1])
                    else:
                        default_rssi[int(
                            signal_strength[k][0])] = int(signal_strength[k][1])
                        for i in range(len(rssi_dict)):
                            rssi_dict[i][rssi_dict[i].keys()[0]].append(
                                default_rssi[rssi_dict[i].keys()[0]])
                        time_stamp_signal1.append(datetime.strptime(str(
                            signal_strength[k][2])[:19], '%Y-%m-%d %H:%M:%S'))
                        default_rssi = default_list
            if len(signal_strength) > 0 and flag == 0:
                if signal_strength[0][1] == 1111111 or str(signal_strength[0][1]) == '1111111':
                    for i in range(len(rssi_dict)):
                        rssi_dict[i][rssi_dict[i]
                                     .keys()[0]].append(default_value)
                    time_stamp_signal1.append(datetime.strptime(
                        str(signal_strength[0][2])[:19], '%Y-%m-%d %H:%M:%S'))
                else:
                    default_rssi[int(
                        signal_strength[0][0])] = int(signal_strength[0][1])
                    for i in range(len(rssi_dict)):
                        rssi_dict[i][rssi_dict[i].keys(
                        )[0]].append(default_rssi[rssi_dict[i].keys()[0]])
                    time_stamp_signal1.append(datetime.strptime(
                        str(signal_strength[0][2])[:19], '%Y-%m-%d %H:%M:%S'))
            if flag == 1 and len(signal_strength) > 0:
                if signal_strength[k + 1][1] == 1111111 or str(signal_strength[k + 1][1]) == '1111111':
                    for i in range(len(rssi_dict)):
                        rssi_dict[i][rssi_dict[i]
                                     .keys()[0]].append(default_value)
                    time_stamp_signal1.append(datetime.strptime(str(
                        signal_strength[k + 1][2])[:19], '%Y-%m-%d %H:%M:%S'))
                else:
                    default_rssi[int(signal_strength[k +
                                     1][0])] = int(signal_strength[k + 1][1])
                    for i in range(len(rssi_dict)):
                        rssi_dict[i][rssi_dict[i].keys(
                        )[0]].append(default_rssi[rssi_dict[i].keys()[0]])
                    time_stamp_signal1.append(datetime.strptime(str(
                        signal_strength[k + 1][2])[:19], '%Y-%m-%d %H:%M:%S'))

            if display_type.strip() == 'graph':
                for time_index in range(len(time_stamp_signal1)):
                    time_stamp_signal1[time_index] = time.mktime(
                        time_stamp_signal1[time_index].timetuple()) * 1000

            for col in column_list:
                if str(col).strip() != '':
                    column_list = [int(i) for i in column_list]
                else:
                    column_list = []
            signal_json_data = []
            if status_name == 'Master':
                signal_json_data = []
                j = 0  # iterate the value of variable for rssi dict.
                for i in column_list:
                    signal_json_data.append({'name': ['%s%s' % (
                        link_name, '' if link_name == 'Total Client' else i), qaulity], 'data': rssi_dict[j][i]})
                    j += 1
            else:
                if len(rssi_dict) > 0:
                    signal_json_data.append(
                        {'name': ['Master-Link', qaulity], 'data': rssi_dict[0][1]})

            # close the connection
            db.close()
            output_dict = {
                'success': 0, 'time_stamp': time_stamp_signal1, 'display_signal_strength': signal_json_data,
                'range_min': min_value, 'range_max': max_value}
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

    def advaeced_excel_report(self, report_type, device_type_id, user_id, ip_address, cal1, tab1, field1, table_name1, graph_name1, start_date, end_date, limitFlag, graph1, start1, limit1):
        """

        @param report_type:
        @param device_type_id:
        @param user_id:
        @param ip_address:
        @param cal1:
        @param tab1:
        @param field1:
        @param table_name1:
        @param graph_name1:
        @param start_date:
        @param end_date:
        @param limitFlag:
        @param graph1:
        @param start1:
        @param limit1:
        @return: @raise:
        """
        try:
            import csv
            import xlwt
            from xlwt import Workbook, easyxf
            xls_book = Workbook(encoding='ascii')
            nms_instance = __file__.split("/")[3]
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

#            datatable_column_list=[]
            table_split_result = table_name1.split(',')
            table_name = table_split_result[0]
            x_axis = table_split_result[1]
            index_name = table_split_result[-2]
            graph_id = table_split_result[-1]
            field_column = field1.split(',')
            update_field_name = ''

            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)

            device_name_list = {'ap25': 'AP25', 'odu16':
                                'RM18', 'odu100': 'RM', 'idu4': 'IDU', 'ccu': 'CCU'}
            login_user_name = ''
            sel_query = "SELECT host_alias FROM hosts WHERE ip_address='%s'" % (
                ip_address)
            cursor.execute(sel_query)
            uesr_information = cursor.fetchall()

            if len(uesr_information) > 0:
                login_user_name = uesr_information[0][0]

            master_slave_status = get_master_slave_value(ip_address)
            ap_mode_dic = {0: 'standard', 1: 'rootAP', 2: 'repeater', 3:
                           'client', 4: 'multiAP', 5: 'multiVLAN', 6: 'dynamicVLAN'}
            device_postfix = '(Master)'
            if master_slave_status['success'] == 0:
                if master_slave_status['device_type'] == 'ap25':
                    device_postfix = ' Mode :- %s ' % ap_mode_dic[
                        master_slave_status['status']]
                else:
                    device_postfix = '(Slave)' if master_slave_status[
                        'status'] > 0 else '(Master)'

            cal_type = ''
            if int(cal1) == 1:
                cal_type = 'Total'
            elif int(cal1) == 2:
                cal_type = 'Delta'

            headings = []
            first_column = x_axis.capitalize()
            headings = [first_column]

            merge_result = []
            d1_list = []
            output_result = self.advanced_graph_data(
                'excel', user_id, table_name, x_axis, index_name, graph_id, start1, limit1, limitFlag, start_date, end_date, ip_address,
                graph1, update_field_name, tab1, cal1, field_column)
            if int(output_result['success']) == 0:
                d1_list.append(output_result['timestamp'])
                for data_list in output_result['data']:
                    d1_list.append(data_list['data'])
                    headings.append(str(
                        data_list['name'][0]) + ' ' + str(data_list['name'][1]))
                merge_result = merge_list(d1_list)
            if len(headings) < 2:
                output_dict = {'success': 1, 'error_msg':
                               '' + str(err_obj.get_error_msg(106))}
                return output_dict

            # we get the host inforamtion.
            sel_query = "SELECT device_type.device_name,hosts.host_alias FROM hosts INNER JOIN device_type ON hosts.device_type_id=device_type.device_type_id \
             WHERE hosts.ip_address='%s' and hosts.is_deleted=0" % (ip_address)
            cursor.execute(sel_query)
            host_result = cursor.fetchall()
            device_type = ''
            device_name = ''
            if len(host_result) > 0:
                device_type = ('--' if host_result[0][0]
                               == '' or host_result[0][0] == None else host_result[0][0])
                device_name = ('--' if host_result[0][1]
                               == '' or host_result[0][1] == None else host_result[0][1])

            idu4_port = {'0': '(odu)', '1': '(eth0)', '2':
                         '(eth0)', '3': '(eth1)', '4': '(maxima)'}
            interface_list = {'get_odu16_nw_interface_statistics_table': {'1': '(eth0)', '2': '(br0)', '3': '(eth1)'},
                              'odu100_nwInterfaceStatisticsTable': {'1': '(eth0)', '2': '(eth1)'}, 'ap25_statisticsTable': {'0': '(eth0)', '1': '(br0)', '2': '(ath0)', '3': '(ath1)', '4': '(ath2)', '5': '(ath3)', '6': '(ath4)', '7': '(ath5)', '8': '(ath6)'},
                              'idu_e1PortStatusTable': {'1': '(port1)', '2': '(port2)', '3': '(port3)', '4': '(port4)'}, 'idu_portstatisticsTable': idu4_port,
                              'idu_swPrimaryPortStatisticsTable': idu4_port, 'idu_portSecondaryStatisticsTable': idu4_port}

            if graph_id.strip() == "odu100peernode":
                interface_list['odu100_peerNodeStatusTable'] = {'1': '(Link1)', '2': '(Link2)', '3': '(Link3)', '4': '(Link4)', '5': '(Link5)', '6': '(Link6)', '7': '(Link7)', '8': '(Link8)', '9': '(Link9)',
                                                                '10': '(Link10)', '11': '(Link11)', '12': '(Link12)', '13': '(Link13)', '14': '(Link14)', '15': '(Link15)', '16': '(Link16)'}

            table_dic_key = [interface for interface in interface_list.keys(
            ) if interface == table_name]
            interface_name = '' if len(
                table_dic_key) == 0 else interface_list[table_dic_key[0].strip()][tab1]
            if report_type == 'excelReport':
                save_file_name = str(device_name_list[device_type_id]) + '_' + str(
                    login_user_name) + '_' + str(start_date) + '.xls'
                sheet_no = 1
                xls_sheet = xls_book.add_sheet(
                    '%s%s' % (graph_name1, sheet_no), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(0, 0, 0, len(headings) - 1, str(graph_name1) + ' ' + str(
                    interface_name) + '  (' + str(start_date) + '-' + str(end_date) + ')', style)
                xls_sheet.write_merge(1, 1, 0, len(headings) - 1, str(device_type) + '       ' + str(
                    ip_address) + str(device_postfix) + '  Calculation Type -: ' + str(cal_type), style)
                xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)   # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for k in range(len(merge_result)):
                    for j in range(len(merge_result[k])):
                        width = 5000
                        xls_sheet.write(i, j, str(merge_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                    if i == 60000:
                        sheet_no += 1
                        xls_sheet = xls_book.add_sheet('%s%s' % (
                            graph_name1, sheet_no), cell_overwrite_ok=True)
                        xls_sheet.row(0).height = 521
                        xls_sheet.row(1).height = 421
                        xls_sheet.write_merge(0, 0, 0, len(headings) - 1, str(graph_name1) + ' ' + str(
                            interface_name) + '  (' + str(start_date) + '-' + str(end_date) + ')', style)
                        xls_sheet.write_merge(1, 1, 0, len(headings) - 1, str(device_type) + '       ' + str(
                            ip_address) + str(device_postfix) + '  Calculation Type -: ' + str(cal_type), style)
                        xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                        i = 4
                        heading_xf = xlwt.easyxf(
                            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                        xls_sheet.set_panes_frozen(
                            True)   # frozen headings instead of split panes
                        xls_sheet.set_horz_split_pos(
                            i)    # in general, freeze after last heading row
                        xls_sheet.set_remove_splits(
                            True)  # if user does unfreeze, don't leave a split there
                        for colx, value in enumerate(headings):
                            xls_sheet.write(i - 1, colx, value, heading_xf)
                    i = i + 1
                path = '/omd/sites/%s/share/check_mk/web/htdocs/download/%s' % (
                    nms_instance, save_file_name)
                xls_book.save(path)
            elif report_type == 'csvReport':
                save_file_name = str(device_name_list[device_type_id]) + '_' + str(
                    login_user_name) + '_' + str(start_date) + '.csv'
                path = '/omd/sites/%s/share/check_mk/web/htdocs/download/%s' % (
                    nms_instance, save_file_name)
                ofile = open(path, "wb")
                writer = csv.writer(ofile, delimiter=',', quotechar='"')
                blank_row = ["", "", ""]
                main_row = [str(graph_name1) + str(
                    interface_name), str(start_date), str(end_date)]
                second_row = [str(device_type), str(ip_address) + str(
                    device_postfix), 'Calculation Type -: ' + str(cal_type)]
                writer.writerow(main_row)
                writer.writerow(second_row)
                writer.writerow(blank_row)
                writer.writerow(headings)
                for row1 in merge_result:
                    writer.writerow(row1)
                ofile.close()
            output_dict = {'success': 0, 'output': 'Report %s Generated Successfully.' % (
                graph_name1), 'file_name': str(save_file_name), 'path': path}
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
            if conn.open:
                conn.close()

    def ap_data_table(self, user_id, ip_address, cal1, tab1, field1, table_name1, graph_name1, start_date, end_date, limitFlag, graph1, start1, limit1):
        """

        @param user_id:
        @param ip_address:
        @param cal1:
        @param tab1:
        @param field1:
        @param table_name1:
        @param graph_name1:
        @param start_date:
        @param end_date:
        @param limitFlag:
        @param graph1:
        @param start1:
        @param limit1:
        @return: @raise:
        """
        try:
            datatable_column_list = []
            table_split_result = table_name1.split(',')
            table_name = table_split_result[0]
            x_axis = table_split_result[1]
            index_name = table_split_result[-2]
            graph_id = table_split_result[-1]
            field_column = field1.split(',')
            update_field_name = ''
            datatable_column_list.append(x_axis)

            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
            d1_list = []
            d2_list = []
            sel_query = "SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE user_id='%s' and graph_name='%s'" % (user_id, graph_id)
            cursor.execute(sel_query)
            field_result = cursor.fetchall()

            graph_field_dict = dict(
                (field[0], field[1]) for field in field_result)
            graph_tip_dict = dict(
                (field[0], field[2]) for field in field_result)

            master_slave_status = get_master_slave_value(ip_address)
            table_name_list = ['odu100_peerNodeStatusTable',
                              'get_odu16_peer_node_status_table']

            if master_slave_status['success'] == 0:
                if int(master_slave_status['status']) == 1 and table_name in table_name_list and graph_id != "odu100peernode":
                    for val in field_column:
                        if str(val).strip() != "":
                            datatable_column_list.append(
                                'MASTER-Link' + ' ' + str(graph_tip_dict[val]))
                else:
                    for val in field_column:
                        if str(val).strip() != "":
                            datatable_column_list.append(
                                str(graph_field_dict[val]) + ' ' + str(graph_tip_dict[val]))
            else:
                raise SelfException('MySQL Problem.')

            merge_result = []
            output_result = self.advanced_graph_data(
                'table', user_id, table_name, x_axis, index_name, graph_id, start1, limit1, limitFlag, start_date, end_date,
                                                     ip_address, graph1, update_field_name, tab1, cal1, field_column)
            if int(output_result['success']) == 0:
                d1_list.append(output_result['timestamp'])
                for data_list in output_result['data']:
                    d1_list.append(data_list['data'])
            merge_result = merge_list(d1_list)

            output_dict = {'success': 0, 'table': merge_result,
                'column': datatable_column_list}
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
            if conn.open:
                conn.close()


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
