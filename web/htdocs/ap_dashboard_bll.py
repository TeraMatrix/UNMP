#!/usr/bin/python2.6
# import the packeges
from datetime import datetime

import MySQLdb

from common_controller import *
from mysql_collection import mysql_connection
from nms_config import *
from odu_controller import *
from unmp_dashboard_config import DashboardConfig
from utility import Validation


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


class APDashboard(object):
    """
    AP device specific dashboard class
    """
    def ap_dashboard(self, host_id):
        """

        @param host_id:
        @return: @raise:
        """
        try:
            db, cursor = mysql_connection('nms_sample')
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
                    if cursor.execute(
                            "SELECT ip_address from hosts where mac_address = '%s' and device_type_id = '%s'") % (
                    mac_address, selected_device):
                        result = cursor.fetchall()
                    elif cursor.execute(
                            "SELECT ip_address from hosts where ip_address = '%s' and device_type_id = '%s'") % (
                    ip_address, selected_device):
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
                    #
                    #            if host_id == "" or host_id == None:
                    #                ip_address=html.var("ip_address")
                    #                mac_address=html.var("mac_address")
                    #                selected_device=html.var("selected_device_type")
                    #                if cursor.execute("SELECT ip_address from hosts where mac_address = '%s' and device_type_id = '%s'")%(mac_address,selected_device):
                    #                    result=cursor.fetchall()
                    #                elif cursor.execute("SELECT ip_address from hosts where ip_address = '%s' and device_type_id = '%s'")%(ip_address,selected_device):
                    #                    result=cursor.fetchall()
                    #                else:
                    #                    result=()
                    #                if len(result)>0:
                    #                    ip_address=result[0][0]
                    #                else:
                    #                    ip_address=''
                    #            else:
                    #                sql="SELECT ip_address from hosts where host_id = '%s' "%(host_id)
                    #                cursor.execute(sql)
                    #                ip_address=cursor.fetchall()
                    #                if ip_address is not None and len(ip_address)>0:
                    #                    ip_address=ip_address[0][0]
                    #                else:
                    #                    ip_address=''
            output_dict = {'success': 0, 'output': '%s' % ip_address}
            return output_dict
            # odu_network_interface_table_graph(h)
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def get_dashboard_data(self):
        """


        @return:
        """
        devcie_type_attr = ['id', 'refresh_time', 'time_diffrence']
        get_data = DashboardConfig.get_config_attributes(
            'ap_dashboard', devcie_type_attr)
        odu_refresh_time = 10   # default time
        total_count = 10    # default count showing record
        if get_data is not None:
            if get_data[0][0] == 'ap_D':
                odu_refresh_time = get_data[0][1]
                total_count = get_data[0][2]
        return str(odu_refresh_time), str(total_count)

    def ap_interface(self, odu_start_date, odu_start_time, odu_end_date, odu_end_time, interface_value, ip_address,
                     limitFlag):
        """

        @param odu_start_date:
        @param odu_start_time:
        @param odu_end_date:
        @param odu_end_time:
        @param interface_value:
        @param ip_address:
        @param limitFlag:
        @return: @raise:
        """
        rx0 = []
        tx0 = []
        time_stamp0 = []
        try:
            db, cursor = mysql_connection()
            if db == 1:
                raise SelfException(cursor)
            start_time = datetime.strptime(
                odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
            end_time = datetime.strptime(
                odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query = "select (idu.rxBytes),(idu.txBytes),idu.timestamp from idu_iduNetworkStatisticsTable as idu INNER JOIN hosts as h  on  idu.host_id = h.host_id  where  h.ip_address='%s' AND  idu.timestamp >= '%s' AND idu.timestamp <='%s' and idu.interfaceName = %s order by idu.timestamp desc" % (
            ip_address, start_time, end_time, interface_value)
            sel_query += limit_data
            cursor.execute(sel_query)
            result = cursor.fetchall()
            for i in range(len(result) - 1):
                rx_byte = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                tx_byte = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                rx0.append(0 if rx_byte <= 0 else rx_byte)
                tx0.append(0 if tx_byte <= 0 else tx_byte)
                time_stamp0.append(result[i][2].strftime('%H:%M'))

            #	column_name=['tx_bytes','tx_packets']
            #	output_dic=graph_common('get_odu16_nw_interface_statistics_table',1,'2012-01-25 12:06:11','2012-01-25 13:06:11',1,column_name)
            #	html.req.content_type = 'application/json'
            #	html.req.write(str(JSONEncoder().encode(output_dic)))

            output_dict = {'success': 0, 'interface_rx': rx0,
                           'interface_tx': tx0, 'time_stamp0': time_stamp0}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            pass
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    def ap_device_information(self, ip_address):
        """

        @param ip_address:
        @return: @raise:
        """
        last_reboot_time = ''
        try:
            db, cursor = mysql_connection()
            if db == 1 or db == '1':
                raise SelfException(cursor)
            sql = "SELECT ap25_radioSetup.radioState, ap25_radioSetup.radiochannel, ap25_radioSetup.numberofVAPs, \
                          ap25_versions.softwareVersion, ap25_versions.hardwareVersion, \
                          ap25_versions.bootLoaderVersion, ap25_radioSetup.wifiMode,hosts.mac_address \
                    from ap25_radioSetup \
                    left join (select host_id,ip_address,mac_address,config_profile_id from hosts ) \
                        as hosts on hosts.ip_address='%s' \
                    left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion \
                               from ap25_versions) \
                        as ap25_versions on ap25_versions.host_id=hosts.host_id \
                    where ap25_radioSetup.config_profile_id=hosts.config_profile_id \
                    order by hosts.ip_address" % (ip_address)
            cursor.execute(sql)
            result = cursor.fetchall()

            now_time = datetime.now()
            sql = "SELECT count(ap25vap.addressMAC) \
                    from ap25_vapClientStatisticsTable as ap25vap \
                    JOIN (select host_id,ip_address,config_profile_id from hosts ) as hosts \
                        on ap25vap.host_id=hosts.host_id \
                    where hosts.ip_address='%s' \
                    and ap25vap.timestamp between '%s' -INTERVAL 6 MINUTE \
                    and '%s'" % (ip_address, now_time, now_time)
            cursor.execute(sql)
            no_of_user = cursor.fetchall()

            output_dict = {'success': 0, 'result': result,
                           'no_of_uesr': no_of_user}
            return output_dict
        # Exception Handling
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 2, 'output':
                'UNMP database Server or Services not running so please contact your Administrator.'}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            db.close()

    # generic graph json data
    def all_graph_json(self, device_type_id, user_id):
        """

        @param device_type_id:
        @param user_id:
        @return: @raise:
        """
        data_list = []
        time_list = []
        output_dic = {}
        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
            sel_query = "SELECT graph_display_id,graph_display_name,user_id,is_disabled,device_type_id,graph_id,graph_name_field,graph_name_interface,graph_tab_option,refresh_button,next_pre_option,start_value,end_value,graph_width,graph_height,graph_cal_id,show_type,show_field,show_cal_type,show_tab_option,auto_refresh_time_second FROM graph_templet_table WHERE user_id='%s' AND device_type_id='%s'" % (
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
                    row[6], user_id)
                cursor.execute(query1)
                option_tuple = cursor.fetchall()
                option_list = []
                for option in option_tuple:
                    option_list.append({'name': option[0], 'displayName':
                        option[1], 'isChecked': option[2]})
                query2 = "SELECT interface_value,interface_display_name,is_selected FROM  graph_interface_table WHERE graph_name='%s' and user_id='%s'" % (
                row[6], user_id)
                cursor.execute(query2)
                interface_tuple = cursor.fetchall()
                interface_value = []
                interface_name = []
                check_val = 0  # default value
                for interface in interface_tuple:
                    interface_value.append(interface[0])
                    interface_name.append(interface[1])
                    if int(interface[2]) == 1:
                        check_val = int(interface[0])
                query3 = "SELECT graph_cal_id,graph_cal_name FROM  graph_calculation_table where user_id='%s' and table_name='%s'" % (
                user_id, row[6])
                cursor.execute(query3)
                cal_tuple = cursor.fetchall()
                cal_list = []
                for cal in cal_tuple:
                    if int(cal[0]) == int(row[15]):
                        cal_list.append({'name': str(cal[0]
                        ), 'displayName': cal[1], 'isChecked': int(1)})
                    else:
                        cal_list.append({'name': str(cal[0]
                        ), 'displayName': cal[1], 'isChecked': int(0)})

                query4 = "SELECT url,method,other_data FROM  graph_ajax_call_information where user_id='%s' and graph_id='%s'" % (
                    row[2], row[6])
                cursor.execute(query4)
                ajax_info = cursor.fetchall()
                for ajax in ajax_info:
                    ajax_json = {'url': ajax[0], 'method': ajax[1],
                                 'cache': False, 'data': {'table_name': ajax[2]}}

                # This field is also come form database
                showType = True if int(row[16]) == 1 else False
                showFields = True if int(row[17]) == 1 else False
                showCalType = True if int(row[18]) == 1 else False
                showTabOption = True if int(row[19]) == 1 else False

                graph_dict = {'name': row[0], 'displayName': row[1], 'fields': option_list, 'calType': cal_list,
                              'ajax': ajax_json,
                              'tabList': {'value': interface_value, 'name': interface_name, 'selected': check_val},
                              'type': graph_type, 'otherOption': {'showOption': True if int(row[8]) == 1 else False,
                                                                  'showRefreshButton': True if int(
                                                                      row[9]) == 1 else False,
                                                                  'showNextPreButton': True if int(
                                                                      row[10]) == 1 else False, 'width': row[13],
                                                                  'height': str(row[14]) + "px", 'showType': showType,
                                                                  'showFields': showFields, 'showCalType': showCalType,
                                                                  'showTabOption': showTabOption,
                                                                  'autoRefresh': row[20]}, 'startFrom': row[11],
                              'itemLimit': row[12]}

                # graph_dict={'name':row[0],'graphName':row[1],'fields':option_list,'calType':cal_list,'ajax':ajax_json,'tabList':
                # {'value':interface_value,'name':interface_name,'selected':check_val},'type':graph_type,'otherOption':{'graph_tab_option':row[8],'refresh_button':row[9],'showNextPreButton':row[10],'start_value':row[11],'end_value':row[12],'width':row[13],'height':row[14]}}
                graph_json.append(graph_dict)
            json_data = []
            #        i=0
            #        for name in column_name[0]:
            #            json_data.append({'name':'%s'%table_field_dict[table_name][name],'data':data_list[i]})
            #            i+=1
            output_dic = {'success': 0, 'graphs': graph_json}
            return output_dic
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 2, 'output':
                'UNMP database Server or Services not running so please contact your Administrator.'}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            if conn.open:
                conn.close()

    def common_graph_json(self, user_id, table_name, x_axis_value, flag, start_date, end_date, ip_address, graph,
                          update_field_name, interface=1, value_cal=1, *column_name):
        """

        @param user_id:
        @param table_name:
        @param x_axis_value:
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
        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
                # query="SELECT graph_field_value,graph_field_display_name,is_checked FROM graph_field_table WHERE user_id='%s' AND graph_name='%s'"%('e243419a-f666-11e0-a835-f04da24c7c26','ap25_statisticsTable')
                # cursor.execute(query)
                # graph_field_result=cursor.fetchall()
                # table_field_dict={table_name:dict((field[0],field[1]) for field in graph_field_result),'status':'0'}
                # print table_field_dict

            # updateion part start here #
            # update the graph calculatio id for particular user for particular
            # table
            if str(update_field_name).strip() == 'calType':
                up_query = "UPDATE  graph_templet_table set graph_cal_id =%s where user_id='%s' and graph_name_field='%s'" % (
                    value_cal, user_id, table_name)
                cursor.execute(up_query)
                conn.commit()

            elif str(update_field_name).strip() == 'fields':
                up_query = "UPDATE graph_field_table set is_checked=0 where user_id='%s' and graph_name='%s'" % (
                    user_id, table_name)
                cursor.execute(up_query)
                conn.commit()

                columns = "','".join(column_name[0])
                up_query = "UPDATE graph_field_table set is_checked=1 where user_id='%s' and graph_name='%s' and graph_field_value IN ('%s')" % (
                    user_id, table_name, columns)
                cursor.execute(up_query)
                conn.commit()

            elif str(update_field_name).strip() == 'type':
                up_query = "update  graph_templet_table set graph_id =%s where user_id='%s' and graph_name_field='%s'" % (
                    graph, user_id, table_name)
                cursor.execute(up_query)
                conn.commit()

            # get the data from graph field table .
            get_coloum = "SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' AND user_id='%s'" % (
                table_name, user_id)
            cursor.execute(get_coloum)
            coloum_result = cursor.fetchall()
            clm_dict = dict(zip([coloum_result[i][0] for i in range(
                len(coloum_result))], [coloum_result[i][1] for i in range(len(coloum_result))]))
            table_field_dict1 = {table_name: clm_dict}
            graph_field_dict = dict(
                (field[0], field[2]) for field in coloum_result)

            sel_query = "select graph_title,graph_subtitle from graph_templet_table where graph_name_field='%s' and user_id='%s'" % (
                table_name, user_id)
            cursor.execute(sel_query)
            graph_name_result = cursor.fetchall()

            graph_title = '' if graph_name_result[0][
                                    0] is None or graph_name_result[0][0] == '' else graph_name_result[0][0]
            graph_sub_title = '' if graph_name_result[0][
                                        1] is None or graph_name_result[0][1] == '' else graph_name_result[0][1]

            now_time = datetime.now()
            if table_name == 'ap25_vapClientStatisticsTable':
                sql = "SELECT ap25vap.vap_id,count(ap25vap.addressMAC) \
                        from ap25_vapClientStatisticsTable as ap25vap\
                        join (select host_id,ip_address,config_profile_id from hosts ) as hosts \
                        on ap25vap.host_id=hosts.host_id \
                        where hosts.ip_address='%s'\
                        and ap25vap.timestamp between '%s'-INTERVAL 6 MINUTE \
                        and '%s' \
                        group by ap25vap.vap_id \
                        order by ap25vap.vap_id" % (ip_address, now_time, now_time)
                cursor.execute(sql)
                vap_result = cursor.fetchall()
                vap_list = ['VAP1', 'VAP2', 'VAP3', 'VAP4',
                            'VAP5', 'VAP6', 'VAP7', 'VAP8']
                time_list = vap_list
                json_data = []
                user_list = [0, 0, 0, 0, 0, 0, 0, 0]
                i = 0
                for vap_r in vap_result:
                    vap_length = len(vap_list)
                    if vap_length >= vap_r[0] and vap_r[0] > 0:
                        user_list[vap_r[0] - 1] = vap_r[1]

                json_data.append(
                    {'name': ['User Count', ' user'], 'data': user_list})

            else:
                sel_query = "SELECT "
                column_list = ',gp_tab.'.join(column_name[0])
                column_list = 'gp_tab.' + column_list
                sel_query += column_list + "," + "gp_tab.%s \
                    FROM %s as gp_tab \
                    INNER JOIN hosts \
                    ON hosts.host_id=gp_tab.host_id \
                    WHERE hosts.ip_address='%s' \
                        AND gp_tab.timestamp >= '%s' \
                        AND gp_tab.timestamp <='%s' \
                        AND gp_tab.index = '%s' \
                    ORDER BY gp_tab.timestamp desc" % (
                    x_axis_value, table_name, ip_address, start_date, end_date, interface)
                if int(flag) == 0:
                    limit_data = ''
                else:
                    limit_data = ' limit 16'
                sel_query += limit_data
                #                print sel_query
                cursor.execute(sel_query)
                result = cursor.fetchall()
                for i in range(len(column_name[0])):
                    data_list.append([])
                if calculation[int(value_cal) - 1] == 'normal':
                    for row in result:
                        for i in range(len(row) - 1):
                            if row[i] == 1 or str(row[i]) == '1':
                                data_list[i].append(0)
                            else:
                                data_list[i].append('0' if row[
                                                               i] == None or row[i] == None else int(row[i]))
                                # print row[i]
                        time_list.append((row[len(row) - 1]).strftime("%H:%M"))
                elif calculation[int(value_cal) - 1] == 'delta':
                    for k in range(len(result) - 1):
                        i = 0
                        for i in range(len(result[k]) - 1):
                            if result[k][i] == 1 or str(result[k][i]) == '1':
                                data_list[i].append(0)
                            else:
                                data_list[i].append('0' if result[k][i] == None or result[k][i]
                                                           == '' else int(result[k][i]) - int(result[k + 1][i]))
                                # print row[i]
                        time_list.append((result[k][i + 1]).strftime("%H:%M"))
                json_data = []
                i = 0
                for name in column_name[0]:
                    json_data.append(
                        {'name': ['%s' % table_field_dict1[table_name][name],
                                  graph_field_dict[name]], 'data': data_list[i]})
                    i += 1

            output_dic = {
                'success': 0, 'timestamp': time_list, 'data': json_data,
                'graph_title': graph_title, 'graph_sub_title': graph_sub_title}
            return output_dic
        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 2, 'output':
                'UNMP database Server or Services not running so please contact your Administrator.'}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
            return output_dict
        finally:
            if conn.open:
                conn.close()

    def ap_excel_report(self, user_id, ip_address, cal1, cal2, tab1, tab2, field1, field2, table_name1, table_name2,
                        graph_name1, graph_name2, start_date, end_date, select_option, limitFlag, graph1, graph2):
        """

        @param user_id:
        @param ip_address:
        @param cal1:
        @param cal2:
        @param tab1:
        @param tab2:
        @param field1:
        @param field2:
        @param table_name1:
        @param table_name2:
        @param graph_name1:
        @param graph_name2:
        @param start_date:
        @param end_date:
        @param select_option:
        @param limitFlag:
        @param graph1:
        @param graph2:
        @return: @raise:
        """
        if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(
                ip_address) == 'None':    # if ip_address not received so excel not created
            raise SelfException(
                'This UBR devices not exists so excel report can not be generated.')  # Check msg
        try:
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

            sql = "SELECT ap25_radioSetup.radioState, ap25_radioSetup.radiochannel, ap25_radioSetup.numberofVAPs, \
                        ap25_versions.softwareVersion, ap25_versions.hardwareVersion, \
                        ap25_versions.bootLoaderVersion, ap25_radioSetup.wifiMode, hosts.mac_address \
                    from ap25_radioSetup\
                    left join (select host_id,ip_address,mac_address,config_profile_id \
                                from hosts ) \
                        as hosts on hosts.ip_address='%s'\
                    left join (select host_id,softwareVersion,ap25_versions.hardwareVersion,ap25_versions.bootLoaderVersion \
                                from ap25_versions) \
                        as ap25_versions on ap25_versions.host_id=hosts.host_id \
                    where ap25_radioSetup.config_profile_id=hosts.config_profile_id \
                    order by hosts.ip_address" % (ip_address)
            cursor.execute(sql)
            result = cursor.fetchall()

            now_time = datetime.now()
            sql = "SELECT count(ap25vap.addressMAC) from ap25_vapClientStatisticsTable as ap25vap\
                    join (select host_id,ip_address,config_profile_id from hosts ) as hosts \
                    on ap25vap.host_id=hosts.host_id \
                    where hosts.ip_address='%s'\
                    and ap25vap.timestamp between '%s'-INTERVAL 6 MINUTE \
                    and '%s'" % (ip_address, now_time, now_time)
            cursor.execute(sql)
            no_of_user = cursor.fetchall()

            channel = [
                'channel-01', 'channel-02', 'channel-03', 'channel-04', 'channel-05', 'channel-06', 'channel-07',
                'channel-08', 'channel-09',
                'channel-10', 'channel-11', 'channel-12', 'channel-13', 'channel-14']
            wifi = ['wifi11g', 'wifi11gnHT20',
                    'wifi11gnHT40plus', 'wifi11gnHT40minus']
            radio = ['disabled', 'enabled']

            device_detail = [
                'Radio Status', 'Radio Channel', 'No of VAPs', 'Software Version',
                'Hardware Version', 'BootLoader Version', 'WiFi Mode', 'MAC Address', 'No of Connected User']
            table_output = []
            if len(result) > 0:
                for i in result:
                    table_output.append([device_detail[0], '--' if result[0][0]
                                                                   == None or result[0][0] == '' else radio[
                        int(result[0][0])]])
                    table_output.append([device_detail[1], '--' if result[0][1] == None or result[
                        0][1] == '' else channel[int(result[0][1]) - 1]])
                    table_output.append([device_detail[2], '--' if result[0][2]
                                                                   == None or result[0][2] == '' else result[0][2]])
                    table_output.append([device_detail[3], '--' if result[0][3]
                                                                   == None or result[0][3] == '' else result[0][3]])
                    table_output.append([device_detail[4], '--' if result[0][4]
                                                                   == None or result[0][4] == '' else result[0][4]])
                    table_output.append([device_detail[5], '--' if result[0][5]
                                                                   == None or result[0][5] == '' else result[0][5]])
                    table_output.append([device_detail[6], '--' if result[0][6]
                                                                   == None or result[0][6] == '' else wifi[
                        int(result[0][6])]])
                    table_output.append([device_detail[7], '--' if result[0][7]
                                                                   == None or result[0][7] == '' else result[0][7]])
            table_output.append(['No of Connected User', 0 if no_of_user[0][0]
                                                              == None or no_of_user[0][0] == '' else no_of_user[0][0]])

            xls_sheet = xls_book.add_sheet(
                'device_information', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "AP Information", style)
            xls_sheet.write_merge(
                1, 1, 0, 2, str('AP25') + '       ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Fields', 'Fields Value']
            # heading=[table_output[0][1],table_output[0][2],table_output[0][3],table_output[0][4],table_output[0][5],table_output[0][6],table_output[0][7]]
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

                # this is code for bandwidth
            table_split_result = table_name1.split(',')
            table_name = table_split_result[0]
            x_axis = table_split_result[1]
            field_column = field1.split(',')
            update_field_name = ''
            output_result = self.common_graph_json(
                user_id, table_name, x_axis, limitFlag, start_date, end_date, ip_address, graph1, update_field_name,
                tab1, cal1, field_column)
            d1_list = []
            headings = [x_axis]
            if int(output_result['success']) == 0:
                d1_list.append(output_result['timestamp'])
                for data_list in output_result['data']:
                    headings.append(data_list['name'][0])
                    d1_list.append(data_list['data'])
                merge_result = merge_list(d1_list)

            interface = ['eth0', 'eth1', 'br0', 'ath1', 'ath2',
                         'ath3', 'ath4', 'ath5', 'ath6', 'ath7']
            xls_sheet = xls_book.add_sheet(
                '%s' % (interface[int(tab1)]), cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "AP Information", style)
            xls_sheet.write_merge(
                1, 1, 0, 2, str('AP25') + '       ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
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

            table_split_result = table_name2.split(',')
            table_name = table_split_result[0]
            x_axis = table_split_result[1]
            field_column = field2.split(',')

            output_result = self.common_graph_json(
                user_id, table_name, x_axis, limitFlag, start_date, end_date, ip_address, graph1, update_field_name,
                tab2, cal2, field_column)
            d1_list = []
            headings = ['VAPS']
            if int(output_result['success']) == 0:
                d1_list.append(output_result['timestamp'])
                for data_list in output_result['data']:
                    headings.append(data_list['name'][0])
                    d1_list.append(data_list['data'])
                merge_result = merge_list(d1_list)

            xls_sheet = xls_book.add_sheet(
                'Connected Client', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "VAPS Information", style)
            xls_sheet.write_merge(
                1, 1, 0, 2, str('AP25') + '       ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
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
            xls_book.save(
                '/omd/sites/%s/share/check_mk/web/htdocs/download/AP_excel.xls' % nms_instance)
            output_dict = {'success': 0}
            return output_dict
        #    (self,user_id,table_name,x_axis_value,flag,start_date,end_date,ip_address,graph,update_field_name,interface=1,value_cal=1,*column_name):

        except MySQLdb as e:
            output_dict = {'success': 3, 'output': str(e[-1])}
            return output_dict
        except SelfException:
            output_dict = {'success': 2, 'output':
                'UNMP database Server or Services not running so please contact your Administrator.'}
            return output_dict
        except Exception as e:
            output_dict = {'success': 1, 'output': str(e[-1])}
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
                d1.append(arg[j][i])
            d2.append(d1)
        return d2
    else:
        return []
