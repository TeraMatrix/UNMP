#!/usr/bin/python2.6
# import the packeges
from datetime import datetime
import time

import MySQLdb

from common_controller import *
from error_message import ErrorMessageClass
from mysql_collection import mysql_connection
from nms_config import *
from odu100_common_dashboard import MainOutage
from odu_controller import *
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
    @copyright: 2011 Code Scape Consulta            sel_query = "select device_type_id,device_name from device_type"
            cursor.execute(sel_query)
            device_type_result=cursor.fetchall()
            device_name =dict((row[0],row[1]) for row in device_type_result)
nts Pvt. Ltd.
    """
    def __init__(self, msg):
        pass


class SPDashboardBll(object):
    """
    AP dashboard Modal class
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
        odu_refresh_time = 10  # default time
        total_count = 180      # default count showing record
        if get_data is not None:
            if get_data[0][0] == 'odu_dashboard':
                odu_refresh_time = get_data[0][1]
                total_count = get_data[0][2]
        return str(odu_refresh_time), str(total_count)

    def sp_device_information(self, ip_address, device_type):
        """

        @param ip_address:
        @param device_type:
        @return: @raise:
        """
        last_reboot_time = ''
        output_dict = {}
        try:
            db, cursor = mysql_connection()
            if db == 1 or db == '1':
                raise SelfException(cursor)
            if device_type.strip() == 'ap25':
                sql = "select ap25_radioSetup.radioState,ap25_radioSetup.radiochannel,ap25_radioSetup.numberofVAPs,\
                ap25_versions.softwareVersion,ap25_versions.hardwareVersion\
                ,ap25_versions.bootLoaderVersion,ap25_radioSetup.wifiMode,hosts.mac_address from ap25_radioSetup\
                left join (select host_id,ip_address,mac_address,config_profile_id from hosts where hosts.is_deleted=0 ) as hosts on hosts.ip_address='%s'\
                left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion from ap25_versions)\
                 as ap25_versions on ap25_versions.host_id=hosts.host_id where ap25_radioSetup.config_profile_id=hosts.config_profile_id order by hosts.ip_address" % (ip_address)
                cursor.execute(sql)
                result = cursor.fetchall()

                sql = "SELECT count(*) FROM ap_connected_client inner join hosts on ap_connected_client.host_id=hosts.host_id \
                 WHERE state='1' and hosts.ip_address='%s' and hosts.is_deleted=0" % (ip_address)
                cursor.execute(sql)
                no_of_user = cursor.fetchall()
                output_dict = {'success': 0, 'result': result,
                               'no_of_uesr': no_of_user, 'device_type': device_type}
            elif device_type.strip() == 'odu16':
                sql = "SELECT fm.rf_channel_frequency,ts.peer_node_status_num_slaves,sw.active_version ,hw.hw_version,lrb.last_reboot_reason,\
                    cb.channel_bandwidth ,op.op_state ,op.default_node_type,hs.mac_address,hs.ip_address FROM  hosts as hs \
                    LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hs.config_profile_id \
                    LEFT JOIN (select host_id,peer_node_status_num_slaves,timestamp from get_odu16_peer_node_status_table where peer_mac_addr is Not Null and peer_mac_addr<>'' ) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hs.host_id \
                    LEFT JOIN  get_odu16_ru_status_table as lrb ON lrb.host_id=hs.host_id \
                    LEFT JOIN set_odu16_ru_conf_table as cb ON cb.config_profile_id = hs.config_profile_id \
                    LEFT JOIN get_odu16_ru_conf_table as op ON op.host_id=hs.host_id \
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                #---- Query for get the last reboot time of particular device ------#
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()
                output_dict = {'success': 0, 'result': result,
                               'last_reboot_time': last_reboot_time, 'device_type': device_type}
            elif device_type.strip() == 'odu100':
                sql = "SELECT fm.rfChanFreq,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,lrb.ruoperationalState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM\
                    hosts as hs \
                    LEFT JOIN odu100_raTddMacStatusTable as fm ON fm.host_id = hs.host_id\
                    LEFT JOIN (select host_id,peerNodeStatusNumSlaves,timestamp from odu100_peerNodeStatusTable \
                    where peerMacAddr is Not Null and peerMacAddr<>'' and linkStatus=2 and tunnelStatus=1) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                    LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                    LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id \
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()
                output_dict = {'success': 0, 'result': result,
                               'last_reboot_time': last_reboot_time, 'device_type': device_type}
            elif device_type.strip() == 'idu4':
                sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,\
                sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw\
                INNER JOIN idu_iduInfoTable as info ON info.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id \
                WHERE hosts.ip_address='%s' and hosts.is_deleted=0 limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchall()
                output_dict = {'success': 0, 'result':
                               result, 'device_type': device_type}
            elif device_type.strip() == 'ccu':
                sql = "SELECT info.ccuITSiteCCUType,info.ccuITSerialNumber,info.ccuITHardwareVersion,soft.ccuSIActiveSoftwareVersion,soft.ccuSIBootLoaderVersion,\
			soft.ccuSIBackupSoftwareVersion,status.ccuSDLastRebootReason,net.ccuNCMACAddress,soft.ccuSICommunicationProtocolVersion\
			from ccu_ccuStatusDataTable as status inner join hosts on status.host_id=hosts.host_id\
			inner join ccu_ccuSoftwareInformationTable as soft on soft.host_id=hosts.host_id\
			inner join ccu_ccuNetworkConfigurationTable as net on net.host_id=hosts.host_id\
			inner join ccu_ccuInformationTable as info on info.host_id=hosts.host_id\
			where hosts.ip_address='%s' and hosts.is_deleted=0 and hosts.device_type_id='ccu' limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchall()
                output_dict = {'success': 0, 'result':
                               result, 'device_type': device_type}

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
    def specific_all_graph_json(self, device_type_id, user_id, ip_address):
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

            # check the deivce is master or Slave.
            master_slave_status = get_master_slave_value(ip_address)
            sel_query = "SELECT graph_display_id,graph_display_name,user_id,is_disabled,device_type_id,graph_id,graph_tab_option,refresh_button,next_pre_option,\
            start_value,end_value,graph_width,graph_height,graph_cal_id,show_type,show_field,show_cal_type,show_tab_option,auto_refresh_time_second \
             FROM graph_templet_table WHERE user_id='%s' AND device_type_id='%s' AND is_disabled=0 and dashboard_type=0" % (user_id, device_type_id)
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

                if master_slave_status['success'] == 0 and int(master_slave_status['status']) == 0:
                    if ajax_json['data']['table_name'].split(',')[0] == 'odu100_synchStatisticsTable' or ajax_json['data']['table_name'].split(',')[0] == 'get_odu16_synch_statistics_table':
                        pass
                    else:
                        graph_json.append(graph_dict)
                else:
                    graph_json.append(graph_dict)
#		graph_json.append(graph_dict)

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

    def common_graph_json(self, display_type, user_id, table_name, x_axis_value, index_name, graph_id, flag, start_date, end_date, start, limit, ip_address, graph, update_field_name, interface=1, value_cal=1, *column_name):
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
        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)

            default_value = {'y': 0, 'marker': {'symbol':
                                                'url(images/ab.png)'}}
            if display_type == 'table' or display_type == 'excel' or display_type == 'csv':
                default_value = 'Device Unreachable'
            elif display_type == 'pdf':
                default_value = 'DU'
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
            get_coloum = "SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' \
             AND user_id='%s'" % (graph_id, user_id)
            cursor.execute(get_coloum)
            coloum_result = cursor.fetchall()
            clm_dict = dict(zip([coloum_result[i][0] for i in range(
                len(coloum_result))], [coloum_result[i][1] for i in range(len(coloum_result))]))
            table_field_dict1 = {table_name: clm_dict}
            graph_field_dict = dict(
                (field[0], field[2]) for field in coloum_result)

            sel_query = "select graph_title,graph_subtitle from graph_templet_table where graph_display_id='%s' and user_id='%s' \
             and dashboard_type=0" % (graph_id, user_id)
            cursor.execute(sel_query)
            graph_name_result = cursor.fetchall()
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
                sql = "select addressMAC %s from ap25_vapClientStatisticsTable as ap inner join hosts on ap.host_id=hosts.host_id where hosts.ip_address='%s' \
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
                        {'name': ['RSL', ' dbm'], 'data': rssi_list})
                else:
                    json_data.append({'name': ['', ''], 'data': rssi_list})
                    time_list = []

            elif table_name.strip() == 'outage':
                # if (end_date - start_date).days < 5:
                #     start_date = datetime.strptime(str(datetime.date(
                #         datetime.now()) + timedelta(days=-4)) + ' ' + '00:00:00', "%Y-%m-%d %H:%M:%S")
                # else:
                #     start_date = datetime.strptime(str(datetime.date(
                #         start_date)) + ' ' + '00:00:00', "%Y-%m-%d %H:%M:%S")
                outage_result = self.sp_advanced_outage_graph(
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
                output_dic = {'success': 0, 'timestamp': odu100_rssi_result['time_stamp'], 'data': odu100_rssi_result['display_signal_strength'],
                              'graph_title': graph_title, 'graph_sub_title': graph_sub_title, 'range_min': odu100_rssi_result['range_min'], 'range_max': odu100_rssi_result['range_max']}
                return output_dic
            else:
                if display_type in ['excel', 'pdf', 'csv']:
                    sel_query = "Select "
                    if len(column_name[0][0]) > 0:
                        column_list = ',gp_tab.'.join(column_name[0])
                        column_list = 'gp_tab.' + column_list
                        sel_query += column_list + "," + "gp_tab.%s from %s as gp_tab INNER JOIN hosts ON hosts.host_id=gp_tab.host_id \
		        where hosts.ip_address='%s' AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' and gp_tab.%s = '%s' and hosts.is_deleted=0 \
		        order by gp_tab.timestamp desc" % (x_axis_value, table_name, ip_address, start_date, end_date, index_name, interface)
                    else:
                        sel_query += "gp_tab.%s from %s as gp_tab INNER JOIN hosts ON hosts.host_id=gp_tab.host_id where hosts.ip_address='%s'\
		         AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' and gp_tab.%s = '%s' and hosts.is_deleted=0 \
		         order by gp_tab.timestamp desc" % (x_axis_value, table_name, ip_address, start_date, end_date, index_name, interface)
                else:
                    sel_query = "Select "
                    if len(column_name[0][0]) > 0:
                        column_list = ',gp_tab.'.join(column_name[0])
                        column_list = 'gp_tab.' + column_list
                        sel_query += column_list + "," + "gp_tab.%s from %s as gp_tab INNER JOIN hosts ON hosts.host_id=gp_tab.host_id where hosts.ip_address='%s' \
		        AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' AND gp_tab.%s = '%s' and hosts.is_deleted=0 \
		        order by gp_tab.timestamp desc limit 10" % (x_axis_value, table_name, ip_address, start_date, end_date, index_name, interface)
                    else:
                        sel_query += "gp_tab.%s from %s as gp_tab INNER JOIN hosts ON hosts.host_id=gp_tab.host_id where hosts.ip_address='%s'\
		         AND gp_tab.timestamp >= '%s' AND gp_tab.timestamp <='%s' AND  gp_tab.%s = '%s' and hosts.is_deleted=0 \
		         order by gp_tab.timestamp desc limit 10" % (x_axis_value, table_name, ip_address, start_date, end_date, index_name, interface)

                cursor.execute(sel_query)
                result = cursor.fetchall()
                for i in range(len(column_name[0])):
                    data_list.append([])

                if calculation[int(value_cal) - 1] == 'normal':
                    for row in result:
                        for i in range(len(row) - 1):
                            data_list[i].append(0 if row[i]
                                                == None or row[i] == None else int(row[i]))
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
                'success': 0, 'timestamp': time_list, 'data': json_data,
                'graph_title': graph_title, 'graph_sub_title': graph_sub_title, 'range_min': 0, 'range_max': 0}
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

    def sp_total_display_graph(self, device_type_id, user_id, ip_address):
        """

        @param device_type_id:
        @param user_id:
        @param ip_address:
        @return:
        """
        try:

            # check the deivce is master or not.
            master_slave_status = get_master_slave_value(ip_address)

            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select graph_display_id from graph_templet_table where device_type_id='%s' and user_id='%s' and is_disabled=0 and dashboard_type=0" % (
                device_type_id, user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            count = 0
            if len(result) > 0:
                if master_slave_status['success'] == 0 and master_slave_status['status'] == 0:
                    graph_id_list = [row[0] for row in result if row[0]
                                     not in ['odu100synclost', 'odu16synclost']]
                    count = int(len(graph_id_list))  # for sync lost
                    # count=int(len(result))
                else:
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

    def sp_advanced_outage_graph(self, display_type, ip_address, start_date, end_date):
        """this function create the outage graph field and show the outage graph.
        @param display_type:
        @param ip_address:
        @param start_date:
        @param end_date:
        """
        date_days = []   # this list store the days information with date.
        up_state = []
            # Its store the total up state of each day in percentage.
        down_state = []
            # Its store the total down state of each day in percentage.
        output_dict = {}  # its store the actual output for display in graph.
        result = get_outage(start_date, end_date, ip_address)
        if int(result['success']) == 1:
            return get_outage
        else:
            for row in result['result']:
                if display_type.strip() == 'graph':
                    date_days.append(time.mktime(datetime.strptime(
                        row[0].strip(), "%Y-%m-%d").timetuple()) * 1000)
                else:
                    date_days.append(datetime.strftime(datetime.strptime(
                        row[0].strip(), '%Y-%m-%d'), '%d %b %Y'))
                up_state.append(row[2])
                down_state.append(row[3])
            date_days.reverse()
            up_state.reverse()
            down_state.reverse()
            output_dict = {'success': 0, 'Reachable': up_state,
                           'Unreachable': down_state, 'date_days': date_days}
            return output_dict

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
        signal_flag = 1
        rssi_dict = []
        default_list = {}
        default_rssi = {}
        time_stamp_signal1 = []
        new_default_value = {'y': 0, 'marker': {'symbol':
                                                'url(images/ab.png)'}}
        default_value = {'y': 0, 'marker': {'symbol': 'url(images/ab.png)'}}
        link_name = "Link"
        qaulity = '(%)'
        min_value = 0
        max_value = 0
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            if display_type.strip() == 'pdf':
                default_value = 'DU'
                new_default_value = "--"
            elif display_type.strip() != 'graph':
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
            count_result = ()
            default_count = 10
            if table_name.strip() == 'odu100_peerNodeStatusTable':
                sel_query = "select DISTINCT(timeSlotIndex) from odu100_peerNodeStatusTable where timestamp >= '%s' AND timestamp <='%s'" % (start_time, end_time)
                cursor.execute(sel_query)
                count_result = cursor.fetchall()
            elif table_name.strip() == 'get_odu16_peer_node_status_table':
                sel_query = "select DISTINCT(timeslot_index) from get_odu16_peer_node_status_table where timestamp >= '%s' AND timestamp <='%s'" % (
                    start_time, end_time)
                cursor.execute(sel_query)
                count_result = cursor.fetchall()
            if len(count_result) > 0:
                default_count = int(count_result[0][0]) * 10

            if display_type == 'graph':
                if (graph_id).strip() == 'odu100link' or (graph_id).strip() == 'odu16link':
                    if table_name.strip() == 'odu100_peerNodeStatusTable':
                        min_value = 0
                        max_value = 100
                        sel_query = "select odu.timeSlotIndex,(IFNULL((odu.txLinkQuality),0)),odu.timestamp,odu.ssIdentifier,odu.linkStatus,odu.tunnelStatus,\
                        odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' and odu.timeSlotIndex IN (%s) AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and h.is_deleted=0 \
                        order by odu.timestamp desc limit %s" % (ip_address, column_field, start_time, end_time, default_count)
                    elif table_name.strip() == 'get_odu16_peer_node_status_table':
                        min_value = -100
                        max_value = 1
                        sel_query = "select odu.timeslot_index,(IFNULL((odu.sig_strength),0)),odu.timestamp,odu.ssidentifier,odu.link_status,odu.tunnel_status,\
                        odu.peer_mac_addr from  get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' and odu.timeSlotIndex IN (%s) AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and h.is_deleted=0 \
                        order by odu.timestamp desc limit %s" % (ip_address, column_field, start_time, end_time, default_count)
                elif table_name.strip() == 'ap25_vapClientStatisticsTable':
                    qaulity = '(count)'
                    link_name = "VAP"
                    if (graph_id).strip() == 'vapConnectedClient':
                        min_value = 0
                        max_value = 0
                        sel_query = "select ap.vap_id,count(ap.addressMAC),ap.timestamp from  ap25_vapClientStatisticsTable as ap \
                        INNER JOIN hosts as h on ap.host_id = h.host_id  where h.ip_address='%s' and ap.vap_id IN (%s) AND ap.addressMAC!='' AND \
                        ap.timestamp >= '%s' AND ap.timestamp <='%s' and h.is_deleted=0 group by ap.vap_id,ap.timestamp \
                        order by ap.timestamp desc limit %s" % (ip_address, column_field, start_time, end_time, default_count)
                    elif (graph_id).strip() == 'totalConnectedClient':
                        link_name = "Total Client"
                        min_value = 0
                        max_value = 0
                        sel_query = "select ap.vap_id,count(ap.addressMAC),ap.timestamp from  ap25_vapClientStatisticsTable as ap \
                        INNER JOIN hosts as h on ap.host_id = h.host_id  where h.ip_address='%s' and ap.vap_id IN (1,2,3,4,5,6,7,8) \
                        AND ap.addressMAC!='' AND ap.timestamp >= '%s' AND ap.timestamp <='%s' and h.is_deleted=0 group by ap.timestamp \
                        order by ap.timestamp desc limit %s" % (ip_address, start_time, end_time, default_count)
                else:
                    qaulity = '(dBm)'
                    if table_name.strip() == 'odu100_peerNodeStatusTable':
                        min_value = -100
                        max_value = 1
                        sel_query = "select odu.timeSlotIndex,(IFNULL((odu.sigStrength%s),0)),odu.timestamp,odu.ssIdentifier,odu.linkStatus,odu.tunnelStatus,\
                        odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' and odu.timeSlotIndex IN (%s) AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and h.is_deleted=0 \
                        order by odu.timestamp desc limit %s" % (1 if graph_id.strip() == 'odu100rssi' else 2, ip_address, column_field, start_time, end_time, default_count)
                    elif table_name.strip() == 'get_odu16_peer_node_status_table':
                        min_value = -100
                        max_value = -1
                        sel_query = "select odu.timeslot_index,(IFNULL((odu.sig_strength),0)),odu.timestamp,odu.ssidentifier,odu.link_status,odu.tunnel_status,\
                        odu.peer_mac_addr from  get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' and odu.timeslot_index IN (%s) AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and h.is_deleted=0 \
                        order by odu.timestamp desc limit %s" % (ip_address, column_field, start_time, end_time, default_count)
            else:
                if (graph_id).strip() == 'odu100link' or (graph_id).strip() == 'odu16link':
                    if table_name.strip() == 'odu100_peerNodeStatusTable':
                        min_value = 0
                        max_value = 100
                        sel_query = "select odu.timeSlotIndex,(IFNULL((odu.txLinkQuality),0)),odu.timestamp,odu.ssIdentifier,odu.linkStatus,odu.tunnelStatus,\
                        odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeSlotIndex IN (%s) and h.is_deleted=0 \
                        order by odu.timestamp desc" % (ip_address, start_time, end_time, column_field)
                    elif table_name.strip() == 'get_odu16_peer_node_status_table':
                        min_value = -100
                        max_value = 1
                        sel_query = "select odu.timeslot_index,(IFNULL((odu.sig_strength),0)),odu.timestamp,odu.ssidentifier,odu.link_status,odu.tunnel_status,\
                        odu.peer_mac_addr from  get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeslot_index IN (%s) and h.is_deleted=0 \
                        order by odu.timestamp desc" % (ip_address, start_time, end_time, column_field)
                elif table_name.strip() == 'ap25_vapClientStatisticsTable':
                    qaulity = '(count)'
                    link_name = "VAP"
                    if (graph_id).strip() == 'vapConnectedClient':
                        min_value = 0
                        max_value = 0
                        sel_query = "select ap.vap_id,count(ap.addressMAC),ap.timestamp from  ap25_vapClientStatisticsTable as ap \
                        INNER JOIN hosts as h on ap.host_id = h.host_id  where h.ip_address='%s' and ap.vap_id IN (%s) AND ap.addressMAC!='' \
                        AND ap.timestamp >= '%s' AND ap.timestamp <='%s' and h.is_deleted=0 group by ap.vap_id,ap.timestamp \
                        order by ap.timestamp desc " % (ip_address, column_field, start_time, end_time)
                    elif (graph_id).strip() == 'totalConnectedClient':
                        link_name = "Total Client"
                        min_value = 0
                        max_value = 0
                        sel_query = "select ap.vap_id,count(ap.addressMAC),ap.timestamp from  ap25_vapClientStatisticsTable as ap \
                        INNER JOIN hosts as h on ap.host_id = h.host_id  where h.ip_address='%s' and ap.vap_id IN (1,2,3,4,5,6,7,8) AND \
                        ap.addressMAC!='' AND ap.timestamp >= '%s' AND ap.timestamp <='%s' and h.is_deleted=0 group by ap.timestamp \
                        order by ap.timestamp desc " % (ip_address, start_time, end_time)
                else:
                    qaulity = '(dBm)'
                    if table_name.strip() == 'odu100_peerNodeStatusTable':
                        min_value = -100
                        max_value = 1
                        sel_query = "select odu.timeSlotIndex,(IFNULL((odu.sigStrength%s),0)),odu.timestamp,odu.ssIdentifier,odu.linkStatus,odu.tunnelStatus,\
                        odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
                        where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.timeSlotIndex IN (%s) and h.is_deleted=0 \
                        order by odu.timestamp desc" % (1 if graph_id.strip() == 'odu100rssi' else 2, ip_address, start_time, end_time, column_field)
                    elif table_name.strip() == 'get_odu16_peer_node_status_table':
                        min_value = -100
                        max_value = 1
                        sel_query = "select odu.timeslot_index,(IFNULL((odu.sig_strength),0)),odu.timestamp,odu.ssidentifier,odu.link_status,\
                        odu.tunnel_status,odu.peer_mac_addr from  get_odu16_peer_node_status_table as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  \
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
                j = 0
                for i in column_list:
                    signal_json_data.append({'name': ['%s%s' % (
                        link_name, '' if link_name == 'Total Client' else i), qaulity], 'data': rssi_dict[j][i]})
                    j += 1
            else:
                if len(rssi_dict) > 0:
                    signal_json_data.append(
                        {'name': ['Master-Link', qaulity], 'data': rssi_dict[0][1]})
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

    def sp_event_alarm(self, ip_address, device_type):
        """

        @param ip_address:
        @param device_type:
        @return: @raise:
        """
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            sql = "SELECT ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,ta.trap_receive_date,description \
            FROM trap_alarms as ta inner join hosts on ta.agent_id=hosts.ip_address WHERE ta.agent_id='%s' order by ta.timestamp desc limit 7 " % ip_address
            cursor.execute(sql)
            all_traps = cursor.fetchall()

#            sql="SELECT ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,ta.trap_receive_date,description FROM trap_alarm_current as ta inner join hosts on ta.agent_id=hosts.ip_address WHERE ta.agent_id='%s' order by ta.timestamp desc limit 7 "%ip_address
#            cursor.execute(sql)
#            current_alarm=cursor.fetchall()

            output_dict = {'success': 0, 'Event': all_traps,
                           'Alarm': all_traps}
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
            graph_list = show_graph.split(',')
            if show_graph.strip() != '':
                sql = "UPDATE graph_templet_table SET is_disabled=1 WHERE user_id='%s' and device_type_id='%s' and dashboard_type=0" % (
                    user_id, device_type_id)
                cursor.execute(sql)
                db.commit()
                sql1 = "UPDATE graph_templet_table SET is_disabled=0 WHERE user_id='%s' AND device_type_id='%s' AND graph_display_id IN ('%s') \
                and dashboard_type=0" % (user_id, device_type_id, "','".join(graph_list))
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

    def sp_dashboard_get_graph_name(self, user_id, device_type, ip_address):
        """

        @param user_id:
        @param device_type:
        @param ip_address:
        @return:
        """
        try:
            make_list = lambda x: [
                " - " if i == None or i == '' else str(i) for i in x]
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select graph_display_name,is_disabled,graph_display_id from graph_templet_table where device_type_id='%s' and user_id='%s' \
            and dashboard_type=0" % (device_type, user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            selected_graph = []
            non_selected_graph = []
            master_slave_status = get_master_slave_value(ip_address)
            for row in result:
                temp = []
                temp.append(row[0])
                temp.append(row[2])
                if master_slave_status['success'] == 0 and int(master_slave_status['status']) == 0 and (row[2] == 'odu100synclost' or row[2] == 'odu16synclost'):
                    pass
                else:
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

    def sp_total_display_graph(self, device_type_id, user_id, ip_address):
        """

        @param device_type_id:
        @param user_id:
        @param ip_address:
        @return:
        """
        try:
            master_slave_status = get_master_slave_value(ip_address)

            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = " select graph_display_id from graph_templet_table where device_type_id='%s' and user_id='%s' and is_disabled=0 and \
            dashboard_type=0" % (device_type_id, user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            count = 0
            if len(result) > 0:
                if master_slave_status['success'] == 0 and master_slave_status['status'] == 0:
                    graph_id_list = [row[0] for row in result if row[0]
                                     not in ['odu100synclost', 'odu16synclost']]
                    count = int(len(graph_id_list))  # for sync lost
                    # count=int(len(result))
                else:
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

    def sp_ap_client_information(self, device_type_id, ip_address):
        """

        @param device_type_id:
        @param ip_address:
        @return:
        """
        try:
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            sql = "SELECT client_name,mac,rssi,vap_id,ap.total_tx,ap.total_rx,hosts1.host_alias,first_seen_time,hst.host_alias,\
            last_seen_time,if(ap_connected_client.state='1','Yes','No') as state FROM ap_client_details as ap \
            inner join (select host_id,host_alias,ip_address from hosts where is_deleted=0) as hosts1  on hosts1.host_id=ap.first_seen_ap_id \
            inner join (select host_id,host_alias,ip_address from hosts where hosts.is_deleted=0) as hst on hst.host_id=ap.last_seen_ap_id \
            inner join ap_client_ap_data as ap_data on ap.client_id=ap_data.client_id \
            join (select client_id,state,host_id from ap_connected_client) as ap_connected_client on ap_connected_client.host_id=hst.host_id \
            and ap_connected_client.client_id=ap.client_id and ap_connected_client.state='1' where hst.ip_address='%s'" % (ip_address)
            cursor.execute(sql)
            result = cursor.fetchall()

            sql = "SELECT host_id FROM hosts where hosts.ip_address='%s' and hosts.device_type_id='%s' and is_deleted='0' limit 1" % (
                ip_address, device_type_id)
            cursor.execute(sql)
            host_id_result = cursor.fetchall()
            host_id = host_id_result[0][0]
            db.close()
            result_dict = {"success": "0", "result": result,
                           'host_id': host_id}
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
    def sp_excel_report(self, device_type, user_id, ip_address, cal_list, tab_list, field_list, table_name_list, graph_name_list, start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list):
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
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(ip_address) == 'None':
            raise SelfException(
                'This UBR devices not exists so excel report can not be generated.')
        try:
            display_type = 'excel'
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

            table_output = []
            nms_instance = __file__.split("/")[3]
            import xlwt
            from xlwt import Workbook, easyxf
            # create the excel file
            xls_book = Workbook(encoding='ascii')
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

            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # create the device type dict
            sel_query = "select device_type_id,device_name from device_type"
            cursor.execute(sel_query)
            device_type_result = cursor.fetchall()
            device_name = dict((row[0], row[1]) for row in device_type_result)

            login_user_name = ''
            sel_query = "SELECT host_alias FROM hosts WHERE ip_address='%s' and hosts.is_deleted=0" % (
                ip_address)
            cursor.execute(sel_query)
            uesr_information = cursor.fetchall()
            if len(uesr_information) > 0:
                login_user_name = uesr_information[0][0]

            save_file_name = str(device_name[device_type]) + '_' + str(
                login_user_name) + '_' + str(start_date) + '.xls'
            wifi = ['wifi11g', 'wifi11gnHT20',
                'wifi11gnHT40plus', 'wifi11gnHT40minus']
            radio = ['disabled', 'enabled']
            device_detail = [
                'Radio Status', 'Radio Channel', 'No Of VAPs', 'Software Version', 'Hardware Version', 'BootLoader Version', 'WiFi Mode', 'MAC Address',
                           'No Of Connected User']

            last_reboot_resion = {
                0: 'Power Cycle', 1: 'Watchdog Reset', 2: 'Normal', 3: 'Kernel Crash Reset', 4: 'Radio Count Mismatch Reset', 5: 'Unknown Soft',
                                6: 'Unknown Reset'}
            default_node_type = {0: 'rootRU', 1: 't1TDN', 2:
                't2TDN', 3: 't2TEN'}
            operation_state = {0: 'disabled', 1: 'enabled'}
            channel = {0: 'raBW5MHz', 1: 'raBW10MHz', 2:
                'raBW20MHz', 3: 'raBW40MHz', 4: 'raBW40SGIMHz'}

            if device_type.strip() == 'ap25':
                channel = [
                    'channel-01', 'channel-02', 'channel-03', 'channel-04', 'channel-05', 'channel-06', 'channel-07', 'channel-08',
                         'channel-09', 'channel-10', 'channel-11', 'channel-12', 'channel-13', 'channel-14']

                device_detail = [
                    'Radio Status', 'Radio Channel', 'No of VAPs', 'Software Version', 'Hardware Version', 'BootLoader Version',
                               'WiFi Mode', 'MAC Address', 'No of Connected User']

                sql = "select ap25_radioSetup.radioState,ap25_radioSetup.radiochannel,ap25_radioSetup.numberofVAPs,\
                ap25_versions.softwareVersion,ap25_versions.hardwareVersion\
                ,ap25_versions.bootLoaderVersion,ap25_radioSetup.wifiMode,hosts.mac_address from ap25_radioSetup\
                left join (select host_id,ip_address,mac_address,config_profile_id from hosts where hosts.is_deleted=0 ) as hosts on hosts.ip_address='%s'\
                left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion from ap25_versions) \
                as ap25_versions on ap25_versions.host_id=hosts.host_id where ap25_radioSetup.config_profile_id=hosts.config_profile_id \
                order by hosts.ip_address" % (ip_address)
                cursor.execute(sql)
                result = cursor.fetchall()

                sql = "SELECT count(*) FROM ap_connected_client inner join hosts on ap_connected_client.host_id=hosts.host_id  \
                WHERE state='1' and hosts.ip_address='%s' and hosts.is_deleted=0 " % (ip_address)
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
                sql = "SELECT fm.rf_channel_frequency,ts.peer_node_status_num_slaves,sw.active_version ,hw.hw_version,lrb.last_reboot_reason,\
                    cb.channel_bandwidth ,op.op_state ,op.default_node_type,hs.mac_address,hs.ip_address FROM  hosts as hs \
                    LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hs.config_profile_id \
                    LEFT JOIN (select host_id,peer_node_status_num_slaves,timestamp from get_odu16_peer_node_status_table \
                    where peer_mac_addr is Not Null and peer_mac_addr<>'' ) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hs.host_id \
                    LEFT JOIN  get_odu16_ru_status_table as lrb ON lrb.host_id=hs.host_id \
                    LEFT JOIN set_odu16_ru_conf_table as cb ON cb.config_profile_id = hs.config_profile_id \
                    LEFT JOIN get_odu16_ru_conf_table as op ON op.host_id=hs.host_id \
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                cursor.execute(sql)
                result = cursor.fetchone()
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()

            elif device_type.strip() == 'ccu':
                sql = "SELECT info.ccuITSiteCCUType,info.ccuITSerialNumber,info.ccuITHardwareVersion,soft.ccuSIActiveSoftwareVersion,soft.ccuSIBootLoaderVersion,\
			soft.ccuSIBackupSoftwareVersion,status.ccuSDLastRebootReason,net.ccuNCMACAddress,soft.ccuSICommunicationProtocolVersion\
			from ccu_ccuStatusDataTable as status inner join hosts on status.host_id=hosts.host_id\
			inner join ccu_ccuSoftwareInformationTable as soft on soft.host_id=hosts.host_id\
			inner join ccu_ccuNetworkConfigurationTable as net on net.host_id=hosts.host_id\
			inner join ccu_ccuInformationTable as info on info.host_id=hosts.host_id\
			where hosts.ip_address='%s' and hosts.is_deleted=0 and hosts.device_type_id='ccu' limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchall()
                ccu_type = ['ccu100', 'ccu250', 'ccu500']
                device_field = [
                    'CCU Type', 'Serial Number', 'Hardware Version', 'Active Software Version', 'Backup Software Version',
                    'BootLoader Version', 'Last Reboot Reason', 'MAC Address', 'Protocol Version']
                if len(result) > 0 and result != None:
                    table_output.append([device_field[0], str('--' if result[0][0] == None or result[
                                        0][0] == "" else ccu_type[int(result[0][0])])])
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
                    table_output.append([device_field[7], str(
                        '--' if result[0][7] == None or result[0][7] == "" else result[0][7])])
                    table_output.append([device_field[8], str(
                        '--' if result[0][8] == None or result[0][8] == "" else result[0][7])])

            elif device_type.strip() == 'odu100':
                sql = "SELECT fm.rfChanFreq,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,\
                lrb.ruoperationalState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM hosts as hs \
                    LEFT JOIN odu100_raTddMacStatusTable as fm ON fm.host_id = hs.host_id\
                    LEFT JOIN (select host_id,peerNodeStatusNumSlaves,timestamp from odu100_peerNodeStatusTable \
                    where peerMacAddr is Not Null and peerMacAddr<>'' and linkStatus=2 and tunnelStatus=1) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                    LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                    LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                cursor.execute(sql)
                result = cursor.fetchone()
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()

            elif device_type.strip() == 'idu4':
                sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,\
                sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw \
                INNER JOIN idu_iduInfoTable as info ON info.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id\
                WHERE hosts.ip_address='%s' and hosts.is_deleted=0 limit 1" % ip_address
                cursor.execute(sql)
                result = cursor.fetchall()

            if device_type.strip() == 'odu16' or device_type.strip() == 'odu100':
                device_field = [
                    'Frequency', 'Time Slot', 'Active Version', 'Hardware Version', 'Last Reboot Reason', 'Channel',
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
                    'Active Version', 'Passive Version', 'BootLoader Version', 'Temperature(C)', 'Uptime']
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

            # create the excel sheet for devcice information .
            xls_sheet = xls_book.add_sheet(
                'Device Information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "%s Information (%s--%s)" % (
                device_name[device_type], str(start_date), str(end_date)), style)
            xls_sheet.write_merge(1, 1, 0, 2, device_name[device_type] +
                                  '       ' + str(ip_address) + str(device_postfix), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Fields', 'Fields Value']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)   # in general, freeze after last heading row
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

            idu4_port = {'0': '(odu)', '1': '(eth0)', '2':
                                '(eth0)', '3': '(eth1)', '4': '(maxima)'}
            interface_list = {'get_odu16_nw_interface_statistics_table': {'1': '(eth0)', '2': '(br0)', '3': '(eth1)'}, 'odu100_nwInterfaceStatisticsTable': {'1': '(eth0)', '2': '(eth1)'}, 'ap25_statisticsTable': {'0': '(eth0)', '1': '(br0)', '2': '(ath0)', '3': '(ath1)', '4': '(ath2)', '5': '(ath3)', '6': '(ath4)', '7': '(ath5)', '8': '(ath6)'},
'idu_e1PortStatusTable': {'1': '(port1)', '2': '(port2)', '3': '(port3)', '4': '(port4)'}, 'idu_portstatisticsTable': idu4_port, 'idu_swPrimaryPortStatisticsTable': idu4_port, 'idu_portSecondaryStatisticsTable': idu4_port}
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
                if graph_id.strip() == "odu100peernode":
                    interface_list['odu100_peerNodeStatusTable'] = {'1': '(Link1)', '2': '(Link2)', '3': '(Link3)', '4': '(Link4)', '5': '(Link5)', '6': '(Link6)', '7': '(Link7)', '8': '(Link8)', '9': '(Link9)',
                                                                  '10': '(Link10)', '11': '(Link11)', '12': '(Link12)', '13': '(Link13)', '14': '(Link14)', '15': '(Link15)', '16': '(Link16)'}
                else:
                    [interface_list.pop('odu100_peerNodeStatusTable') for ke in interface_list.keys(
                        ) if ke.strip() == 'odu100_peerNodeStatusTable']

                table_dic_key = [interface for interface in interface_list.keys(
                    ) if interface == table_name]
                interface_name = '' if len(table_dic_key) == 0 else interface_list[
                                            table_dic_key[0].strip()][tab_list[i]]
                output_result = self.common_graph_json(
                    display_type, user_id, table_name, x_axis, index_name, graph_id, limitFlag, start_date, end_date, start, limit,
                                                       ip_address, graph_list[i], update_field_name, tab_list[i], cal_list[i], field_column)
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

                if len(headings) < 2:
                    continue
                xls_sheet = xls_book.add_sheet(
                    str(graph_name_list[i]), cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(0, 0, 0, len(headings) - 1, "%s%s (%s--%s)" % (
                    str(graph_name_list[i]), interface_name, str(start_date), str(end_date)), style)
                xls_sheet.write_merge(1, 1, 0, len(headings) - 1, device_name[device_type] + '   ' + str(
                    ip_address) + str(device_postfix) + '  Display Information -: (%s)' % str(cal_type), style)
                xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                l = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                for colx, value in enumerate(headings):
                    xls_sheet.write(l - 1, colx, value, heading_xf)
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    l)   # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there

                for k in range(len(merge_result)):
                    for j in range(len(merge_result[k])):
                        width = 5000
                        xls_sheet.write(l, j, str(merge_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                    l = l + 1

            if device_type == 'ap25':
                merge_result = ()
                client_result = self.sp_ap_client_information(
                    device_type, ip_address)
                if client_result['success'] == '0' or client_result['success'] == '0':
                    merge_result = client_result['result']
                headings = ['Client Alias', 'MAC Address', 'RSL', 'VAP', 'Total Tx(Mbps)', 'Total Rx(Mbps)', 'First AP',
                                                                                   'First Seen Time', 'Last AP', 'Last Seen Time', 'Connected']
                xls_sheet = xls_book.add_sheet(
                    'Client Detail', cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(0, 0, 0, len(
                    headings) - 1, 'Client Details (%s--%s)' % (start_date, end_date), style)
                xls_sheet.write_merge(1, 1, 0, len(headings) - 1, device_name[device_type] + '       ' +
                                      str(ip_address) + str(device_postfix), style)
                xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)   # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for k in range(len(merge_result)):
                    for j in range(len(merge_result[k])):
                        width = 5000
                        xls_sheet.write(i, j, str(merge_result[k][j]), style1)
                        xls_sheet.col(j).width = width
                    i = i + 1

            # Event and Alarm report Start Here. ---->
            # This is common file for all Device.
            sql = "SELECT ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,ta.trap_receive_date,description \
            FROM trap_alarms as ta inner join hosts on ta.agent_id=hosts.ip_address WHERE ta.agent_id='%s' and ta.timestamp>='%s' and ta.timestamp<='%s' \
            order by ta.timestamp desc" % (ip_address, start_date, end_date)

            cursor.execute(sql)
            current_alarm = cursor.fetchall()
            merge_result = []
            serevity_list = ['Normal', 'Information', 'Normal',
                'Minor', 'Major', 'Critical']

            for row in current_alarm:
                merge_result.append([row[5], serevity_list[int(
                    row[0])], row[1], row[2], row[3], row[6]])
            headings = ['Received Date', 'Severity',
                'Event Name', 'Event ID', 'Event Type', 'Description']
            xls_sheet = xls_book.add_sheet('Events', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, len(
                headings) - 1, 'Device Events (%s--%s)' % (start_date, end_date), style)
            xls_sheet.write_merge(1, 1, 0, len(headings) - 1, device_name[device_type] + '       ' + str(
                ip_address) + str(device_postfix), style)
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

    #          # Event and Alarm report End Here. ---->
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
    def sp_csv_report(self, device_type, user_id, ip_address, cal_list, tab_list, field_list, table_name_list, graph_name_list, start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list):
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
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(ip_address) == 'None':
            raise SelfException(
                'This devices not exists so excel report can not be generated.')
        try:
            display_type = 'csv'
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
            table_output = []
            nms_instance = __file__.split("/")[3]
            import csv

            # create the connection with database
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # create the device type dict
            sel_query = "select device_type_id,device_name from device_type"
            cursor.execute(sel_query)
            device_type_result = cursor.fetchall()
            device_name = dict((row[0], row[1]) for row in device_type_result)

            login_user_name = ''
            sel_query = "SELECT host_alias FROM hosts WHERE ip_address='%s' and hosts.is_deleted=0" % (
                ip_address)
            cursor.execute(sel_query)
            uesr_information = cursor.fetchall()
            if len(uesr_information) > 0:
                login_user_name = uesr_information[0][0]
            save_file_name = str(device_name[device_type]) + '_' + str(
                login_user_name) + '_' + str(start_date) + '.csv'

            wifi = ['wifi11g', 'wifi11gnHT20',
                'wifi11gnHT40plus', 'wifi11gnHT40minus']
            radio = ['disabled', 'enabled']
            device_detail = [
                'Radio Status', 'Radio Channel', 'No Of VAPs', 'Software Version', 'Hardware Version', 'BootLoader Version', 'WiFi Mode',
                           'MAC Address', 'No Of Connected User']

            last_reboot_resion = {
                0: 'Power Cycle', 1: 'Watchdog Reset', 2: 'Normal', 3: 'Kernel Crash Reset', 4: 'Radio Count Mismatch Reset', 5: 'Unknown Soft',
                                6: 'Unknown Reset'}
            default_node_type = {0: 'rootRU', 1: 't1TDN', 2:
                't2TDN', 3: 't2TEN'}
            operation_state = {0: 'disabled', 1: 'enabled'}
            channel = {0: 'raBW5MHz', 1: 'raBW10MHz', 2:
                'raBW20MHz', 3: 'raBW40MHz', 4: 'raBW40SGIMHz'}
            if device_type.strip() == 'ap25':
                channel = [
                    'channel-01', 'channel-02', 'channel-03', 'channel-04', 'channel-05', 'channel-06', 'channel-07', 'channel-08',
                         'channel-09', 'channel-10', 'channel-11', 'channel-12', 'channel-13', 'channel-14']

                device_detail = [
                    'Radio Status', 'Radio Channel', 'No of VAPs', 'Software Version', 'Hardware Version', 'BootLoader Version',
                               'WiFi Mode', 'MAC Address', 'No of Connected User']

                sql = "select ap25_radioSetup.radioState,ap25_radioSetup.radiochannel,ap25_radioSetup.numberofVAPs,\
                ap25_versions.softwareVersion,ap25_versions.hardwareVersion\
                ,ap25_versions.bootLoaderVersion,ap25_radioSetup.wifiMode,hosts.mac_address from ap25_radioSetup\
                left join (select host_id,ip_address,mac_address,config_profile_id from hosts where hosts.is_deleted=0) as hosts on hosts.ip_address='%s'\
                left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion from ap25_versions)\
                 as ap25_versions on ap25_versions.host_id=hosts.host_id where ap25_radioSetup.config_profile_id=hosts.config_profile_id \
                 order by hosts.ip_address" % (ip_address)
                cursor.execute(sql)
                result = cursor.fetchall()

                sql = "SELECT count(*) FROM ap_connected_client inner join hosts on ap_connected_client.host_id=hosts.host_id  WHERE state='1' and \
                hosts.ip_address='%s'  and hosts.is_deleted=0 " % (ip_address)
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
                sql = "SELECT fm.rf_channel_frequency,ts.peer_node_status_num_slaves,sw.active_version ,hw.hw_version,lrb.last_reboot_reason,\
                    cb.channel_bandwidth ,op.op_state ,op.default_node_type,hs.mac_address,hs.ip_address FROM  hosts as hs \
                    LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hs.config_profile_id \
                    LEFT JOIN (select host_id,peer_node_status_num_slaves,timestamp from get_odu16_peer_node_status_table where peer_mac_addr is Not Null and peer_mac_addr<>'' ) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hs.host_id \
                    LEFT JOIN  get_odu16_ru_status_table as lrb ON lrb.host_id=hs.host_id \
                    LEFT JOIN set_odu16_ru_conf_table as cb ON cb.config_profile_id = hs.config_profile_id \
                    LEFT JOIN get_odu16_ru_conf_table as op ON op.host_id=hs.host_id \
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                #---- Query for get the last reboot time of particular device ------#
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()
            elif device_type.strip() == 'odu100':
                sql = "SELECT fm.rfChanFreq,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,\
                lrb.ruoperationalState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM hosts as hs \
                    LEFT JOIN odu100_raTddMacStatusTable as fm ON fm.host_id = hs.host_id\
                    LEFT JOIN (select host_id,peerNodeStatusNumSlaves,timestamp from odu100_peerNodeStatusTable \
                    where peerMacAddr is Not Null and peerMacAddr<>'' and linkStatus=2 and tunnelStatus=1) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                    LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                    LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()

            elif device_type.strip() == 'ccu':
                sql = "SELECT info.ccuITSiteCCUType,info.ccuITSerialNumber,info.ccuITHardwareVersion,soft.ccuSIActiveSoftwareVersion,soft.ccuSIBootLoaderVersion,\
			soft.ccuSIBackupSoftwareVersion,status.ccuSDLastRebootReason,net.ccuNCMACAddress,soft.ccuSICommunicationProtocolVersion\
			from ccu_ccuStatusDataTable as status inner join hosts on status.host_id=hosts.host_id\
			inner join ccu_ccuSoftwareInformationTable as soft on soft.host_id=hosts.host_id\
			inner join ccu_ccuNetworkConfigurationTable as net on net.host_id=hosts.host_id\
			inner join ccu_ccuInformationTable as info on info.host_id=hosts.host_id\
			where hosts.ip_address='%s' and hosts.is_deleted=0 and hosts.device_type_id='ccu' limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchall()
                ccu_type = ['ccu100', 'ccu250', 'ccu500']
                device_field = [
                    'CCU Type', 'Serial Number', 'Hardware Version', 'Active Software Version', 'Backup Software Version',
                    'BootLoader Version', 'Last Reboot Reason', 'MAC Address', 'Protocol Version']
                if len(result) > 0 and result != None:
                    table_output.append([device_field[0], str('--' if result[0][0] == None or result[
                                        0][0] == "" else ccu_type[int(result[0][0])])])
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
                    table_output.append([device_field[7], str(
                        '--' if result[0][7] == None or result[0][7] == "" else result[0][7])])
                    table_output.append([device_field[8], str(
                        '--' if result[0][8] == None or result[0][8] == "" else result[0][7])])

            elif device_type.strip() == 'idu4':
                sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,\
                sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw \
                INNER JOIN idu_iduInfoTable as info ON info.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id\
                WHERE hosts.ip_address='%s' and hosts.is_deleted=0 limit 1" % ip_address
                cursor.execute(sql)
                result = cursor.fetchall()

            if device_type.strip() == 'odu16' or device_type.strip() == 'odu100':
                device_field = [
                    'Frequency', 'Time Slot', 'Active Version', 'Hardware Version', 'Last Reboot Reason', 'Channel', 'Operation State',
                              'Node Type', 'MAC Address', 'Last Reboot Time']

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
                    'H/W Serial Number', 'System MAC', 'TDMOIP Interface MAC', 'Active Version', 'Passive Version', 'BootLoader Version',
                              'Temperature(C)', 'Uptime']

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

            # create the csv file.
            path = '/omd/sites/%s/share/check_mk/web/htdocs/download/%s' % (
                nms_instance, save_file_name)
            ofile = open(path, "wb")
            writer = csv.writer(ofile, delimiter=',', quotechar='"')

            headings = ['Fields', 'Fields Value']
            blank_row = ["", "", ""]
            main_row = ['Device Information']
            second_row = [str(device_name[device_type]) +
                              ' Information', str(start_date), str(end_date)]
            writer.writerow(main_row)
            writer.writerow(second_row)
            writer.writerow(blank_row)
            writer.writerow(headings)
            for row1 in table_output:
                writer.writerow(row1)

            idu4_port = {'0': '(odu)', '1': '(eth0)', '2':
                                '(eth0)', '3': '(eth1)', '4': '(maxima)'}
            interface_list = {'get_odu16_nw_interface_statistics_table': {'1': '(eth0)', '2': '(br0)', '3': '(eth1)'}, 'odu100_nwInterfaceStatisticsTable': {'1': '(eth0)', '2': '(eth1)'}, 'ap25_statisticsTable': {'0': '(eth0)', '1': '(br0)', '2': '(ath0)', '3': '(ath1)', '4': '(ath2)', '5': '(ath3)', '6': '(ath4)', '7': '(ath5)', '8': '(ath6)'},
'idu_e1PortStatusTable': {'1': '(port1)', '2': '(port2)', '3': '(port3)', '4': '(port4)'}, 'idu_portstatisticsTable': idu4_port, 'idu_swPrimaryPortStatisticsTable': idu4_port, 'idu_portSecondaryStatisticsTable': idu4_port}
            # Start for CRC/PHY Error Report

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
                if graph_id.strip() == "odu100peernode":
                    interface_list['odu100_peerNodeStatusTable'] = {'1': '(Link1)', '2': '(Link2)', '3': '(Link3)', '4': '(Link4)', '5': '(Link5)', '6': '(Link6)', '7': '(Link7)', '8': '(Link8)', '9': '(Link9)',
                                                                  '10': '(Link10)', '11': '(Link11)', '12': '(Link12)', '13': '(Link13)', '14': '(Link14)', '15': '(Link15)', '16': '(Link16)'}
                else:
                    [interface_list.pop('odu100_peerNodeStatusTable') for ke in interface_list.keys(
                        ) if ke.strip() == 'odu100_peerNodeStatusTable']

                table_dic_key = [interface for interface in interface_list.keys(
                    ) if interface == table_name]
                interface_name = '' if len(table_dic_key) == 0 else interface_list[
                                            table_dic_key[0].strip()][tab_list[i]]
                output_result = self.common_graph_json(
                    display_type, user_id, table_name, x_axis, index_name, graph_id, limitFlag, start_date, end_date, start, limit,
                                                       ip_address, graph_list[i], update_field_name, tab_list[i], cal_list[i], field_column)
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
                main_row = [str(graph_name_list[i]) + str(interface_name)]
                second_row = [device_name[device_type] + str(
                    device_postfix), str(ip_address) + ' Display Information -:' + str(cal_type)]
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
                client_result = self.sp_ap_client_information(
                    device_type, ip_address)
                if client_result['success'] == '0' or client_result['success'] == '0':
                    merge_result = client_result['result']
                headings = ['Client Alias', 'MAC Address', 'RSL', 'VAP', 'Total Tx(Mbps)', 'Total Rx(Mbps)', 'First AP',
                                                                                   'First Seen Time', 'Last AP', 'Last Seen Time', 'Connected']
                blank_row = ["", "", ""]
                main_row = ['Client Details']
                second_row = [device_name[device_type] + str(
                    device_postfix), str(ip_address)]
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

            # Event and Alarm report Start Here. ---->
            # This is common file for all Device.
            sql = "SELECT ta.serevity,ta.event_id,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,ta.trap_receive_date,description \
            FROM trap_alarms as ta inner join hosts on ta.agent_id=hosts.ip_address WHERE ta.agent_id='%s' and ta.timestamp>='%s' and ta.timestamp<='%s' \
            order by ta.timestamp desc" % (ip_address, start_date, end_date)
            cursor.execute(sql)
            current_alarm = cursor.fetchall()
            merge_result = []
            serevity_list = ['Normal', 'Information', 'Normal',
                'Minor', 'Major', 'Critical']
            for row in current_alarm:
                merge_result.append([row[5], serevity_list[int(
                    row[0])], row[1], row[2], row[3], row[6]])
            headings = ['Received Date', 'Severity',
                'Event Name', 'Event ID', 'Event Type', 'Description']
            blank_row = ["", "", ""]
            main_row = ['Device Events']
            second_row = [device_name[device_type] + str(
                device_postfix), str(ip_address)]
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

            # Event and Alarm report End Here. ---->
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

    def sp_pdf_report(self, device_type, user_id, ip_address, cal_list, graph_id_list, tab_list, field_list, table_name_list, graph_name_list, start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list):
        """

        @param device_type:
        @param user_id:
        @param ip_address:
        @param cal_list:
        @param graph_id_list:
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
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(ip_address) == 'None':
            raise SelfException(
                'This devices not exists so excel report can not be generated.')
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

            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)

            # create the device type dict
            sel_query = "select device_type_id,device_name from device_type"
            cursor.execute(sel_query)
            device_type_result = cursor.fetchall()
            device_name = dict((row[0], row[1]) for row in device_type_result)

            idu4_port = {'0': '(odu)', '1': '(eth0)', '2':
                                '(eth0)', '3': '(eth1)', '4': '(maxima)'}
            interface_list = {'get_odu16_nw_interface_statistics_table': {'1': '(eth0)', '2': '(br0)', '3': '(eth1)'}, 'odu100_nwInterfaceStatisticsTable': {'1': '(eth0)', '2': '(eth1)'}, 'ap25_statisticsTable': {'0': '(eth0)', '1': '(br0)', '2': '(ath0)', '3': '(ath1)', '4': '(ath2)', '5': '(ath3)', '6': '(ath4)', '7': '(ath5)', '8': '(ath6)'},
'idu_e1PortStatusTable': {'1': '(port1)', '2': '(port2)', '3': '(port3)', '4': '(port4)'}, 'idu_portstatisticsTable': idu4_port, 'idu_swPrimaryPortStatisticsTable': idu4_port, 'idu_portSecondaryStatisticsTable': idu4_port,
'odu100_peerNodeStatusTable': {'1': '(Link1)', '2': '(Link2)', '3': '(Link3)', '4': '(Link4)', '5': '(Link5)', '6': '(Link6)', '7': '(Link7)', '8': '(Link8)', '9': '(Link9)', '16': '(Link16)'}}

            # we are geting the login user name here.
            login_user_name = ''
            sel_query = "SELECT host_alias FROM hosts WHERE ip_address='%s' and hosts.is_deleted=0" % (
                ip_address)
            cursor.execute(sel_query)
            uesr_information = cursor.fetchall()
            if len(uesr_information) > 0:
                login_user_name = uesr_information[0][0]
            save_file_name = str(device_name[device_type]) + '_' + str(
                login_user_name) + '_' + str(start_date) + '.pdf'

            wifi = ['wifi11g', 'wifi11gnHT20',
                'wifi11gnHT40plus', 'wifi11gnHT40minus']
            radio = ['disabled', 'enabled']
            device_detail = [
                'Radio Status', 'Radio Channel', 'No of VAPs', 'Software Version', 'Hardware Version', 'BootLoader Version', 'WiFi Mode',
                           'MAC Address', 'No of Connected User']

            last_reboot_resion = {
                0: 'Power cycle', 1: 'Watchdog reset', 2: 'Normal', 3: 'Kernel crash reset', 4: 'Radio count mismatch reset',
                                5: 'Unknown-Soft', 6: 'Unknown reset'}

            default_node_type = {0: 'rootRU', 1: 't1TDN', 2:
                't2TDN', 3: 't2TEN'}
            operation_state = {0: 'disabled', 1: 'enabled'}
            channel = {0: 'raBW5MHz', 1: 'raBW10MHz', 2:
                'raBW20MHz', 3: 'raBW40MHz', 4: 'raBW40SGIMHz'}

            styleSheet = getSampleStyleSheet()
            ubr_report = []
            MARGIN_SIZE = 14 * mm
            PAGE_SIZE = A4
            nms_instance = __file__.split("/")[3]
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
                left join (select host_id,ip_address,mac_address,config_profile_id from hosts where hosts.is_deleted=0 ) as hosts on hosts.ip_address='%s'\
                left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion from ap25_versions) as ap25_versions on ap25_versions.host_id=hosts.host_id where ap25_radioSetup.config_profile_id=hosts.config_profile_id order by hosts.ip_address" % (ip_address)
                cursor.execute(sql)
                result = cursor.fetchall()

                sql = "SELECT count(*) FROM ap_connected_client inner join hosts on ap_connected_client.host_id=hosts.host_id  WHERE state='1' and hosts.ip_address='%s'" % (
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
                sql = "SELECT fm.rf_channel_frequency,ts.peer_node_status_num_slaves,sw.active_version ,hw.hw_version,lrb.last_reboot_reason,\
                    cb.channel_bandwidth ,op.op_state ,op.default_node_type,hs.mac_address,hs.ip_address FROM  hosts as hs \
                    LEFT JOIN set_odu16_ra_tdd_mac_config as fm ON fm.config_profile_id = hs.config_profile_id \
                    LEFT JOIN (select host_id,peer_node_status_num_slaves,timestamp from get_odu16_peer_node_status_table where peer_mac_addr is Not Null and peer_mac_addr<>'' ) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  get_odu16_sw_status_table as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN get_odu16_hw_desc_table as hw ON hw.host_id=hs.host_id \
                    LEFT JOIN  get_odu16_ru_status_table as lrb ON lrb.host_id=hs.host_id \
                    LEFT JOIN set_odu16_ru_conf_table as cb ON cb.config_profile_id = hs.config_profile_id \
                    LEFT JOIN get_odu16_ru_conf_table as op ON op.host_id=hs.host_id \
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                #---- Query for get the last reboot time of particular device ------#
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()

            elif device_type.strip() == 'ccu':
                sql = "SELECT info.ccuITSiteCCUType,info.ccuITSerialNumber,info.ccuITHardwareVersion,soft.ccuSIActiveSoftwareVersion,soft.ccuSIBootLoaderVersion,\
			soft.ccuSIBackupSoftwareVersion,status.ccuSDLastRebootReason,net.ccuNCMACAddress,soft.ccuSICommunicationProtocolVersion\
			from ccu_ccuStatusDataTable as status inner join hosts on status.host_id=hosts.host_id\
			inner join ccu_ccuSoftwareInformationTable as soft on soft.host_id=hosts.host_id\
			inner join ccu_ccuNetworkConfigurationTable as net on net.host_id=hosts.host_id\
			inner join ccu_ccuInformationTable as info on info.host_id=hosts.host_id\
			where hosts.ip_address='%s' and hosts.is_deleted=0 and hosts.device_type_id='ccu' limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchall()
                ccu_type = ['ccu100', 'ccu250', 'ccu500']
                device_field = [
                    'CCU Type', 'Serial Number', 'Hardware Version', 'Active Software Version', 'Backup Software Version',
                    'BootLoader Version', 'Last Reboot Reason', 'MAC Address', 'Protocol Version']
                if len(result) > 0 and result != None:
                    table_output.append([device_field[0], str('--' if result[0][0] == None or result[
                                        0][0] == "" else ccu_type[int(result[0][0])])])
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
                    table_output.append([device_field[7], str(
                        '--' if result[0][7] == None or result[0][7] == "" else result[0][7])])
                    table_output.append([device_field[8], str(
                        '--' if result[0][8] == None or result[0][8] == "" else result[0][7])])

            elif device_type.strip() == 'odu100':
                sql = "SELECT fm.rfChanFreq,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,lrb.ruoperationalState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM\
                    hosts as hs \
                    LEFT JOIN odu100_raTddMacStatusTable as fm ON fm.host_id = hs.host_id\
                    LEFT JOIN (select host_id,peerNodeStatusNumSlaves,timestamp from odu100_peerNodeStatusTable \
                    where peerMacAddr is Not Null and peerMacAddr<>'' and linkStatus=2 and tunnelStatus=1) as ts ON ts.host_id = hs.host_id \
                    LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                    LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                    LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                    LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                    where hs.ip_address='%s' and hs.is_deleted=0 order by ts.timestamp desc limit 1" % ip_address
                #--- execute the query ------#
                cursor.execute(sql)
                result = cursor.fetchone()
                sel_query = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address
                cursor.execute(sel_query)
                last_reboot_time = cursor.fetchall()
            elif device_type.strip() == 'idu4':
                sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw INNER JOIN idu_iduInfoTable as info ON info.host_id=sw.host_id INNER JOIN hosts ON hosts.host_id=sw.host_id WHERE hosts.ip_address='%s'  and hosts.is_deleted=0 limit 1" % ip_address
                cursor.execute(sql)
                result = cursor.fetchall()
            if device_type.strip() == 'odu16' or device_type.strip() == 'odu100':
                device_field = [
                    'Frequency', 'Time Slot', 'Active Version', 'Hardware Version', 'Last Reboot Reason', 'Channel',
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
                    'H/W Serial Number', 'System MAC', 'TDMOIP Interface MAC', 'Active Version', 'Passive Version',
                              'BootLoader Version', 'Temperature(C)', 'UpTime']

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
                        headings.append(str(
                            data_list['name'][0]) + str(data_list['name'][1]))

                        d1_list.append(data_list['data'])
                    merge_result = merge_list(d1_list)
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
                table_output = []
                # table_output.append(headings)
                for small_list in merge_result:
                    table_output.append(small_list)
                data1 = []
                data1.append(['', '%s%s' % (
                    graph_name_list[i], interface_name), '', ''])
                t = Table(
                    data1, [.021 * inch, 2.51 * inch, 2.26 * inch, 2.22 * inch])
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, 0), (1, 0), (0.91, 0.91, 0.91)),
                                       ('FONT', (0, 0), (1, 0),
                                        'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.black),
                                       ('BOX', (1, 0), (1, 0), .38, (0.29, 0.29, 0.29))]))

                # this is for permission to download folder
                import os
                os.system(
                    'chmod 777 /omd/sites/UNMP/share/check_mk/htdocs/web/download/* -R')
                # this is for permission to download

                ubr_report.append(Spacer(11, 11))
                time.sleep(2)
                im = Image(
                    "/omd/sites/%s/share/check_mk/web/htdocs/download/%s.png" % (nms_instance,
                           graph_id_list[i]), width=7.1 * inch, height=3 * inch)
                im.hAlign = 'LEFT'
                ubr_report.append(im)
                ubr_report.append(Spacer(11, 11))
                ubr_report.append(t)

                if table_name.strip() == 'outage':
                    table_output.insert(0, headings)
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

                    t = Table(data, [3.3 * inch, 1.9 * inch, 1.9 * inch])
                    t.setStyle(
                        TableStyle(
                            [(
                                'FONT', (0, 0), (len(headings) - 1, 0), 'Helvetica', 10),
                                           ('FONT', (0, 1),
                                            (len(headings) - 1, int(len(table_output)) - 1), 'Helvetica', 9),
                                           ('ALIGN', (1, 0), (len(
                                               headings) - 1, int(
                                                   len(
                                                       table_output)) - 1), 'CENTER'),
                                           ('BACKGROUND', (0, 0), (
                                               len(
                                                   headings) - 1, 0), (
                                                       0.91, 0.91, 0.91)),
                                           ('LINEABOVE', (0,
                                            0), (
                                                len(
                                                    headings) - 1, 0), .29, (
                                                        .29, .29, .29)),
                                           ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.21, (0.74, 0.74, 0.74))]))

                    for i in range(1, len(table_output)):
                        if i % 2 == 1:
                            t.setStyle(
                                TableStyle(
                                    [(
                                        'BACKGROUND', (1, i), (len(headings) - 1, i), (0.95, 0.95, 0.95)),
                                                   ('BACKGROUND', (0, i - 1), (0, i - 1), (0.98, 0.98, 0.98))]))
                        else:
                            t.setStyle(TableStyle([('BACKGROUND', (1, i), (len(headings) - 1, i), (0.91, 0.91, 0.91))
                                                   ]))
                    t.setStyle(TableStyle(
                        [('BACKGROUND', (0, 0), (0, 0), (0.91, 0.91, 0.91))]))
                    ubr_report.append(t)
                    if len(table_output) == 1:
                        data1 = []
                        data1.append(['No data exists.'])
                        t = Table(data1, [7.10 * inch])
                        t.setStyle(
                            TableStyle(
                                [(
                                    'BACKGROUND', (0, 0), (1, 0), (0.91, 0.91, 0.91)),
                                               ('FONT', (0, 0), (0, 0), 'Helvetica', 9), (
                                                   'TEXTCOLOR', (0, 0), (0, 0), colors.black),
                                               ('BOX', (0, 0), (0, 0), .29, (0.56, 0.56, 0.56))]))
                        ubr_report.append(t)
                else:
                    table_output = conversion_to_pdf(table_output, headings)
                    data = table_output
                    t = Table(data, [2.5 * inch, 1.15 *
                              inch, 1.15 * inch, 1.15 * inch, 1.15 * inch])
                    t.setStyle(
                        TableStyle([('FONT', (0, 0), (4, 0), 'Helvetica', 10),
                                           ('FONT', (0, 1), (4, int(
                                               len(
                                                   table_output)) - 1), 'Helvetica', 9),
                                           ('ALIGN', (1, 0), (4, int(len(
                                               table_output)) - 1), 'CENTER'),
                                           ('BACKGROUND', (0, 0),
                                            (4, 0), (0.91, 0.91, 0.91)),
                                           ('LINEABOVE', (0, 0),
                                            (4, 0), .29, (.29, .29, .29)),
                                           ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.21, (0.74, 0.74, 0.74))]))

                    for i in range(1, len(table_output)):
                        if i % 2 == 1:
                            t.setStyle(
                                TableStyle(
                                    [(
                                        'BACKGROUND', (1, i), (4, i), (0.95, 0.95, 0.95)),
                                                   ('BACKGROUND', (0, i - 1),
                                                    (0, i - 1), (0.98, 0.98, 0.98)),
                                                   ]))
                        else:
                            t.setStyle(TableStyle([('BACKGROUND', (1, i), (4, i), (0.91, 0.91, 0.91))
                                                   ]))
                    t.setStyle(TableStyle(
                        [('BACKGROUND', (0, 0), (0, 0), (0.91, 0.91, 0.91))]))
                    ubr_report.append(t)
                    if len(table_output) == 1:
                        data1 = []
                        data1.append(['No data exists.'])
                        t = Table(data1, [7.10 * inch])
                        t.setStyle(
                            TableStyle(
                                [(
                                    'BACKGROUND', (0, 0), (1, 0), (0.91, 0.91, 0.91)),
                                               ('FONT', (0, 0), (0, 0), 'Helvetica', 9), (
                                                   'TEXTCOLOR', (0, 0), (0, 0), colors.black),
                                               ('BOX', (0, 0), (0, 0), .29, (0.56, 0.56, 0.56))]))
                        ubr_report.append(t)
            ubr_report.append(Spacer(31, 31))
            data1 = []
            data1.append(["** DU Device Unreachable"])
            t = Table(data1, [7.1 * inch])
            t.setStyle(
                TableStyle(
                    [(
                        'BACKGROUND', (0, 0), (0, 0), (0.91, 0.91, 0.91)), ('FONT', (0, 0), (0, 0), 'Helvetica', 11),
                                   ('TEXTCOLOR', (0, 0), (0, 0), colors.black), ('BOX', (0, 0), (0, 0), .29, (0.56, 0.56, 0.56))]))
            ubr_report.append(t)

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


def get_master_slave_value(ip_address):
    """

    @param ip_address:
    @return: @raise:
    """
    try:
        conn, cursor = mysql_connection()
        if conn == 1:
            raise SelfException(cursor)
        sel_query = "SELECT device_type_id FROM hosts WHERE hosts.ip_address='%s' limit 1" % (
            ip_address)
        cursor.execute(sel_query)
        device_type = cursor.fetchall()
        status_result = ()
        if len(device_type) > 0 and device_type[0][0] == 'odu100':
            sel_query = "SELECT defaultNodeType FROM odu100_ruConfTable as def INNER JOIN hosts ON hosts.config_profile_id=def.config_profile_id \
	    WHERE hosts.ip_address='%s' and hosts.is_deleted=0  limit 1" % (ip_address)
            cursor.execute(sel_query)
            status_result = cursor.fetchall()
        elif len(device_type) > 0 and device_type[0][0] == 'odu16':
            sel_query = "SELECT default_node_type FROM  get_odu16_ru_conf_table as def INNER JOIN hosts ON hosts.host_id=def.host_id \
	    WHERE hosts.ip_address='%s' and hosts.is_deleted=0  limit 1" % (ip_address)
            cursor.execute(sel_query)
            status_result = cursor.fetchall()
        elif len(device_type) > 0 and device_type[0][0] == 'idu4':
            sel_query = "SELECT hwType FROM   idu_iduInfoTable as def INNER JOIN hosts ON hosts.host_id=def.host_id WHERE hosts.ip_address='%s' \
	    and hosts.is_deleted=0  limit 1" % (ip_address)
            cursor.execute(sel_query)
            status_result = cursor.fetchall()
        elif len(device_type) > 0 and device_type[0][0] == 'ap25':
            sel_query = "SELECT radioAPmode FROM ap25_radioSetup as def INNER JOIN hosts ON hosts.config_profile_id=def.config_profile_id \
	    WHERE hosts.ip_address='%s' and hosts.is_deleted=0  limit 1" % (ip_address)
            cursor.execute(sel_query)
            status_result = cursor.fetchall()
        status = 0
        if len(status_result) > 0:
            if status_result[0][0] == None or status_result[0][0] == '':
                status = 0
            elif device_type[0][0] == 'ap25':
                status = status_result[0][0]
            else:
                if int(status_result[0][0]) == 0 or int(status_result[0][0]) == 2:
                    status = 0
                else:
                    status = 1
        output_dict = {'success': 0, 'status': status,
            'ip_address': ip_address, 'device_type': device_type[0][0]}
        return output_dict
    except Exception, e:
        output_dict = {'success': 1, 'error_msg': str(e[-1])}
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
                d1.append(arg[j][i])
            d2.append(d1)
        return d2
    else:
        return []


# def main_outage(result_tuple, end_date):
#     try:
#         count = 1
#         is_date = 0
#         main_date = ''
#         main_ip = ''
#         main_list = []
#         uptime = None
#         downtime = None
#         prev_value = ''
#         temp_temp = []
#         for tpl in result_tuple:
#             count += 1
#             tpl_temp = tpl
#             temp_ip = tpl[3]
#             temp_date = tpl[2]
#             temp_value = tpl[0]
#             if temp_ip == main_ip:
#                 if temp_date.month > main_date.month or temp_date.day > main_date.day:
#                     count += 1

#                     is_date = 1
#                 else:
#                     if prev_value == '50002':
#                         if uptime == None:
#                             uptime = (temp_date - main_date)
#                         else:
#                             uptime += (temp_date - main_date)

#                     elif prev_value == '50001':
#                         if downtime == None:
#                             downtime = (temp_date - main_date)
#                         else:
#                             downtime += (temp_date - main_date)
#                     count += 1
#                     main_date = temp_date  # print "jump1"

#             else:
#                 is_new = 1

#             if is_new:
#                 if prev_value != '':
#                     is_date = 1
#                 else:
#                     main_date = temp_date
#                 main_ip = temp_ip
#                 is_new = 0

#             if is_date:
#                 if uptime == None or downtime == None:
#                     mid_date = datetime(main_date.year,
#                                         main_date.month, main_date.day, 23, 59, 59)
#                     delta = mid_date - main_date
#                     if prev_value == '50002':
#                         uptime = delta
#                     elif prev_value == '50001':
#                         downtime = delta
#                     count += 1
#                 else:
#                     mid_date = datetime(main_date.year,
#                                         main_date.month, main_date.day, 23, 59, 59)
#                     delta = mid_date - main_date
#                     if prev_value == '50002':
#                         uptime += delta
#                     elif prev_value == '50001':
#                         downtime += delta
#                     count += 1

#                 main_list.append([main_date, tpl_temp[3], uptime, downtime])
#                 uptime = None
#                 downtime = None

# #                    day_diff=(temp_date-main_date).days
#                 # day_diff = round(float(d.seconds + d.days *
#                 # 86400)/float(86400))
#                 day_diff = temp_date.day - main_date.day
#                 if day_diff > 1:
#                     for i in range(1, day_diff):
#                         leftout_date = main_date + timedelta(days=i)
#                         if prev_value == '50002':
#                             main_list.append([leftout_date,
#                                              tpl_temp[3], timedelta(0, 86399), None])
#                         elif prev_value == '50001':
#                             main_list.append([leftout_date,
#                                              tpl_temp[3], None, timedelta(0, 86399)])
#                     delta = temp_date - leftout_date
#                     if prev_value == '50002':
#                         if uptime == None:
#                             uptime = delta
#                         else:
#                             uptime += delta
#                     elif prev_value == '50001':
#                         if downtime == None:
#                             downtime = delta
#                         else:
#                             downtime += delta
#                 else:
#                     mid_date = datetime(temp_date.year,
#                                         temp_date.month, temp_date.day, 00, 00, 00)
#                     delta = temp_date - mid_date
#                     if prev_value == '50002':
#                         uptime = delta
#                     elif prev_value == '50001':
#                         downtime = delta
#                     count += 1

#                 main_date = temp_date
#                 is_date = 0

#             prev_value = temp_value
#         ############################# outside loop
#         if uptime == None or downtime == None:
#             mid_date = datetime(
#                 main_date.year, main_date.month, main_date.day, 23, 59, 59)
#             delta = mid_date - main_date
#             if prev_value == '50002':
#                 uptime = delta
#             elif prev_value == '50001':
#                 downtime = delta
#         main_list.append([main_date, tpl_temp[3], uptime, downtime])
#         day_diff = (end_date - main_date).days  # temp_date.day-main_date.day
#         if day_diff > 1:
#             for i in range(1, day_diff + 1):
#                 leftout_date = main_date + timedelta(days=i)
#                 if prev_value == '50002':
#                     main_list.append([leftout_date,
#                                      tpl_temp[3], timedelta(0, 86399), None])
#                 elif prev_value == '50001':
#                     main_list.append([leftout_date,
#                                      tpl_temp[3], None, timedelta(0, 86399)])
#             main_date = leftout_date
#         day_diff = end_date.day - main_date.day
#         # if day_diff > 1:
#         if day_diff > 1 or end_date.month - main_date.month > 0:
#             leftout_date = main_date + timedelta(days=1)
#             if prev_value == '50002':
#                 main_list.append(
#                     [leftout_date, tpl_temp[3], timedelta(0, 86399), None])
#             elif prev_value == '50001':
#                 main_list.append(
#                     [leftout_date, tpl_temp[3], None, timedelta(0, 86399)])
#         main_dict = {}
#         main_dict['success'] = 0
#         main_dict['result'] = main_list
#         main_dict['outage'] = "main_outage"
#         # with open('/home/cscape/Desktop/ok.txt','w') as f:
#         #    f.write(str(main_dict))
#         return main_dict
#     except Exception, e:
#         main_dict = {}
#         main_dict['success'] = 1
#         main_dict['result'] = str(e)
#         return main_dict


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
            else:
                if len(result) < 1 and status_result != ():
                    # result = status_result
                    t_date = datetime.strptime(
                        start_date, "%Y-%m-%d %H:%M:%S")
                    t_date = t_date.replace(hour=0, minute=0, second=0)
                    t_list = ((status_result[0][0],
                              status_result[0][1], t_date, status_result[0][3]),)
                    result = t_list

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
                        i[-2] = int(round(float(uptime) * 100 / float(total)))
                        i[-1] = int(
                            round(float(downtime) * 100 / float(total)))
                        if int(i[-2]) + int(i[-1]) != 100:
                            i[-2] = int(i[-2]) + 1
                        tr.append(i)
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


def conversion_to_pdf(data_list, heading):
    """

    @param data_list:
    @param heading:
    @return:
    """
    new_list = []
    if len(data_list) > 0:
        for i in range(1, len(data_list[0])):
            temp_list = []
            for j in range(len(data_list)):
                temp_list.append(0 if data_list[j][i] == 'DU' or data_list[j][
                                 i] == '--' else data_list[j][i])
            print temp_list
            new_list.append([heading[i], min(temp_list), max(temp_list), float(
                sum(temp_list) / len(data_list)), sum(temp_list)])
    pdf_heading = ['Field Name', 'Minimum', 'Maximum', 'Average', 'Total']
    new_list.insert(0, pdf_heading)
    return new_list
