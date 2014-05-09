#!/usr/bin/python2.6
# import the packeges
import MySQLdb
# from common_controller import *
# from nms_config import *
# from odu_controller import *
from mysql_collection import mysql_connection
from error_message import ErrorMessageClass
from specific_dashboard_bll import SPDashboardBll
from specific_dashboard_bll import get_master_slave_value


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

# class APAdvancedGraph(object):


class AdvancedStatusBll(object):
    """
    Device specific Advanced status Model class
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
            sel_query = "SELECT host_id FROM hosts WHERE device_type_id='%s' and ip_address=%s and is_deleted=0 " % (
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
            sel_query = "SELECT graph_display_name,graph_display_id FROM graph_templet_table WHERE device_type_id='%s' and user_id='%s' \
            and dashboard_type=1" % (device_type_id, user_id)
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

            sel_query = "SELECT graph_display_id,graph_display_name,user_id,is_disabled,device_type_id,graph_id,graph_tab_option,refresh_button,\
            next_pre_option,start_value,end_value,graph_width,graph_height,graph_cal_id,show_type,show_field,show_cal_type,show_tab_option,\
            auto_refresh_time_second FROM graph_templet_table WHERE user_id='%s' AND device_type_id='%s' AND graph_display_id='%s' \
            and dashboard_type=1" % (user_id, device_type_id, graph_id)
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
                    if len(option_tuple) > 0 and (row[0] == 'odu100rssi' or row[0] == 'odu16rssi'):
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
                    #                for option in option_tuple:
                    # option_list.append({'name':option[0],'displayName':option[1],'isChecked':option[2]})
                query2 = "SELECT interface_value,interface_display_name,is_selected FROM  graph_interface_table WHERE graph_name='%s' and user_id='%s'" % (
                row[0], user_id)
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
                for interface in interface_tuple:
                    interface_value.append(interface[0])
                    interface_name.append(interface[1])
                    if int(interface[2]) == 1:
                        check_val = int(interface[0])
                query3 = "SELECT graph_cal_id,graph_cal_name FROM  graph_calculation_table where user_id='%s' and table_name='%s'" % (
                user_id, row[0])
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
                query5 = "SELECT url,method,other_data FROM  total_count_item where user_id='%s' and graph_id='%s'" % (
                user_id, row[0])
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
                graph_dict = {'name': row[0], 'displayName': row[1], 'fields': option_list, 'calType': cal_list,
                              'ajax': ajax_json,
                              'tabList': {'value': interface_value, 'name': interface_name, 'selected': check_val},
                              'type': graph_type, 'otherOption': {'showOption': True if int(row[6]) == 1 else False,
                                                                  'showRefreshButton': True if int(
                                                                      row[7]) == 1 else False,
                                                                  'showNextPreButton': True if int(
                                                                      row[8]) == 1 else False, 'width': row[11],
                                                                  'height': str(
                                                                      row[12]) + "px", 'showType': showType,
                                                                  'showFields': showFields, 'showCalType': showCalType,
                                                                  'showTabOption': showTabOption,
                                                                  'autoRefresh': row[18]}, 'startFrom': row[9],
                              'itemLimit': row[10], 'totalItemAjax': total_item_json}

                # this is check the master or slave for sync lsot graph showing or not.
                #                if master_slave_status['success']==0 and int(master_slave_status['status'])==0:
                #                    if ajax_json['data']['table_name'].split(',')[0]=='odu100_synchStatisticsTable' or ajax_json['data']['table_name'].split(',')[0]=='get_odu16_peer_node_status_table':
                #                        pass
                #                    else:
                #                        graph_json.append(graph_dict)
                #
                #		else:
                #		    graph_json.append(graph_dict)
                graph_json.append(graph_dict)

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

    def advanced_graph_data(self, user_id, ip_address, start_date, end_date, graph_id, device_type_id):
        """

        @param user_id:
        @param ip_address:
        @param start_date:
        @param end_date:
        @param graph_id:
        @param device_type_id:
        @return: @raise:
        """
        data_list = []
        time_list = []
        output_dic = {}
        json_data = []
        op_state = 2
        req = []
        td = []
        th = []
        sp_bll_obj = SPDashboardBll(
        )  # specific bll dashboard file object created for reusablity
        result = ()
        table_name_dict = {
            'odu100NWstatus': 'odu100_nwInterfaceStatusTable', 'odu100syncstatus': 'odu100_synchStatusTable',
            'odu100Rastatus': 'odu100_raStatusTable', 'idu4e1portstatus': 'idu_e1PortStatusTable',
            'idu4linkstatustable': 'idu_linkStatusTable'}
        default_value = 'Device Unreachable'
        try:
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
                # get the data from graph field table .
            get_coloum = "SELECT graph_field_value,graph_field_display_name,tool_tip_title FROM graph_field_table WHERE graph_name='%s' AND user_id='%s'" % (
                graph_id, user_id)
            cursor.execute(get_coloum)
            coloum_result = cursor.fetchall()
            column_name = [col[0].strip() for col in coloum_result]

            clm_dict = dict(zip([coloum_result[i][0].strip() for i in range(
                len(coloum_result))], [coloum_result[i][1] for i in range(len(coloum_result))]))
            table_field_dict1 = {graph_id: clm_dict}
            graph_field_dict = dict(
                (field[0], field[2]) for field in coloum_result)

            sel_query = "select graph_title,graph_subtitle from graph_templet_table where graph_display_id='%s' and user_id='%s' and device_type_id='%s' and dashboard_type=1" % (
                graph_id, user_id, device_type_id)
            cursor.execute(sel_query)
            graph_name_result = cursor.fetchall()
            graph_title = ''  # default value
            graph_sub_title = ''  # default value
            if len(graph_name_result) > 0:
                graph_title = '' if graph_name_result[0][
                                        0] == None or graph_name_result[0][0] == '' else graph_name_result[0][0]
                graph_sub_title = '' if graph_name_result[0][
                                            1] == None or graph_name_result[0][1] == '' else graph_name_result[0][1]

            if graph_id.strip() == 'idu4e1portstatus':
                sel_query = "select  idu.portNum, \
			(if(idu.opStatus=0,'Disable',if(idu.opStatus=1111111,idu.opStatus,'Enable'))) as opStatus, \
			(if(idu.los=0,'Bit Clear',if(idu.los=1111111,idu.los,'Bit Set'))) as los, \
			(if(idu.lof=0,'Bit Clear',if(idu.lof=1111111,idu.lof,'Bit Set'))) as lof, \
			(if(idu.ais=0,'Bit Clear',if(idu.ais=1111111,idu.ais,'Bit Set'))) as ais, \
			(if(idu.rai=0,'Bit Clear',if(idu.rai=1111111,idu.rai,'Bit Set'))) as rai, \
			(if(idu.rxFrameSlip=0,'Bit Clear',if(idu.rxFrameSlip=1111111,idu.rxFrameSlip,'Bit Set'))) as rxFrameSlip, \
			(if(idu.txFrameSlip=0,'Bit Clear',if(idu.txFrameSlip=1111111,idu.txFrameSlip,'Bit Set'))) as txFrameSlip, \
			bpv, \
			(if(idu.adptClkState=0,'State Idle', \
		    		(if(idu.adptClkState=1,'State Self Test', \
		 		     (if(idu.adptClkState=2,'State Acquisition', \
		 	             	(if(idu.adptClkState=3,'State Tracking', \
		 	             	    (if(idu.adptClkState=4,'State Tracking2',\
		 	             	    (if(idu.adptClkState=5,'State Recovered', \
		 	             	    if(idu.adptClkState=1111111,idu.adptClkState,'State Not Active'))) \
		 	             	         	 )) \
		 	             	  )) \
		 	         )) \
		 	    )) \
			)) \
		       as adptClkState, \
		     (if(idu.holdOverStatus=0,'In Normal Mode',if(idu.holdOverStatus=1111111,idu.holdOverStatus,'In Hold Over Mode'))) as holdOverStatus,idu.timestamp \
		 from  idu_e1PortStatusTable as idu INNER JOIN hosts ON hosts.host_id=idu.host_id  where hosts.ip_address='%s' and idu.timestamp >='%s' and idu.timestamp <='%s' and hosts.is_deleted=0  order by idu.timestamp desc,idu.portNum asc" % (
                ip_address, start_date, end_date)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                given = ['portNum', 'opStatus', 'los', 'lof', 'ais', 'rai',
                         'rxFrameSlip', 'txFrameSlip', 'bpv', 'adptClkState', 'holdOverStatus', 'timestamp']
                req = []
                req.append('timestamp')
                req.append('portNum')
                req.extend(column_name)
                td = manage_list(req, given, result)
                th.append('Timestamp')
                th.append('Port Number')
                for name in column_name:
                    th.append(table_field_dict1[graph_id][name])
            elif graph_id.strip() == 'idu4linkstatustable':
                op_state = 3
                sel_query = "select idu.portNum,idu.bundleNum,\
			(if(idu.operationalStatus=0,'Disable',if(idu.operationalStatus=1111111,idu.operationalStatus,'Enable'))) as operationalStatus,\
			minJBLevel,\
			maxJBLevel,\
			(if(idu.underrunOccured=0,'Bit Clear',if(idu.underrunOccured=1111111,idu.underrunOccured,'Bit Set'))) as underrunOccured,\
			(if(idu.overrunOccured=0,'Bit Clear',if(idu.overrunOccured=1111111,idu.overrunOccured,'Bit Set'))) as overrunOccured ,idu.timestamp\
		 from   idu_linkStatusTable as idu INNER JOIN hosts ON hosts.host_id=idu.host_id where hosts.ip_address='%s' and idu.timestamp >='%s' and idu.timestamp <='%s' and hosts.is_deleted=0 order by idu.timestamp desc,idu.bundleNum asc " % (
                ip_address, start_date, end_date)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                given = ['bundleNum', 'portNum', 'operationalStatus',
                         'minJBLevel', 'maxJBLevel', 'underrunOccured', 'overrunOccured', 'timestamp']
                req.append('timestamp')
                req.append('portNum')
                req.append('bundleNum')
                req.extend(column_name)
                td = manage_list(req, given, result)
                th.append('Timestamp')
                th.append('Port Number')
                th.append('Link Nnumber')
                for name in column_name:
                    th.append(table_field_dict1[graph_id][name])
            elif graph_id.strip() == 'odu100Rastatus':
                op_state = 1
                sel_query = "select odu.currentTimeSlot,\
			odu.raMacAddress,\
			(if(odu.raoperationalState=0,'Disable',if(odu.raoperationalState=1111111,odu.raoperationalState,'Enable'))) as raoperationalState,\
			odu.unusedTxTimeUL,odu.unusedTxTimeDL,odu.timestamp\
			from   odu100_raStatusTable as odu INNER JOIN hosts ON hosts.host_id=odu.host_id where hosts.ip_address='%s' and odu.timestamp >='%s' and odu.timestamp <='%s' and hosts.is_deleted=0 order by odu.timestamp desc " % (
                ip_address, start_date, end_date)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                given = ['currentTimeSlot', 'raMacAddress',
                         'raoperationalState', 'unusedTxTimeUL', 'unusedTxTimeDL', 'timestamp']
                req.append('timestamp')
                req.extend(column_name)
                td = manage_list(req, given, result)
                th.append('Timestamp')
                for name in column_name:
                    th.append(table_field_dict1[graph_id][name])
            elif graph_id.strip() == 'odu100syncstatus':
                op_state = 1
                sel_query = "select (if(odu.syncoperationalState=0,'Disable',if(odu.syncoperationalState=1111111,odu.syncoperationalState,'Enable'))) as syncoperationalState,\
			odu.syncrasterTime,\
			odu.timerAdjust,odu.syncpercentageDownlinkTransmitTime,odu.timestamp\
			from   odu100_synchStatusTable as odu INNER JOIN hosts ON hosts.host_id=odu.host_id where hosts.ip_address='%s' and odu.timestamp >='%s' and odu.timestamp <='%s' and hosts.is_deleted=0 order by odu.timestamp desc" % (
                ip_address, start_date, end_date)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                given = ['syncoperationalState', 'syncrasterTime',
                         'timerAdjust', 'syncpercentageDownlinkTransmitTime', 'timestamp']
                req.append('timestamp')
                req.extend(column_name)
                td = manage_list(req, given, result)
                th.append('Timestamp')
                for name in column_name:
                    th.append(table_field_dict1[graph_id][name])
            elif graph_id.strip() == 'odu100NWstatus':
                op_state = 1
                sel_query = "select odu.nwStatusIndex,\
			odu.nwInterfaceName,\
			(if(odu.operationalState=0,'Disable',if(odu.operationalState=1111111,odu.operationalState,'Enable'))) as operationalState,\
			odu.macAddress,odu.timestamp\
			from    odu100_nwInterfaceStatusTable as odu INNER JOIN hosts ON hosts.host_id=odu.host_id where hosts.ip_address='%s' and odu.timestamp >='%s' and odu.timestamp <='%s' and hosts.is_deleted=0 order by odu.timestamp desc,odu.nwInterfaceName asc " % (
                ip_address, start_date, end_date)
                cursor.execute(sel_query)
                result = cursor.fetchall()
                given = ['nwStatusIndex', 'nwInterfaceName',
                         'operationalState', 'macAddress', 'timestamp']
                req.append('timestamp')
                req.extend(column_name)
                td = manage_list(req, given, result)
                th.append('Timestamp')
                for name in column_name:
                    th.append(table_field_dict1[graph_id][name])
            data_list = td
            if len(data_list) > 0:
                for d1 in range(len(data_list)):
                    count = 0
                    for d2 in range(len(data_list[0])):
                        if data_list[d1][d2] == 1111111 or data_list[d1][d2] == '1111111':
                            count += 1
                    if count == len(data_list[0]) - op_state:
                        for d3 in range(len(data_list[0])):
                            if d3 == 0:
                                continue
                            data_list[d1][d3] = default_value
            table_dict = {'td': data_list, 'th': th}
            output_dic = {
                'success': 0, 'timestamp': time_list, 'data': table_dict,
                'graph_title': graph_title, 'graph_sub_title': graph_sub_title}
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

    def advaeced_excel_report(self, report_type, device_type_id, user_id, ip_address, start_date, end_date, graph_id,
                              select_option):
        """

        @param report_type:
        @param device_type_id:
        @param user_id:
        @param ip_address:
        @param start_date:
        @param end_date:
        @param graph_id:
        @param select_option:
        @return: @raise:
        """
        try:
            import csv
            import xlwt
            from xlwt import Workbook, easyxf

            xls_book = Workbook(encoding='ascii')
            nms_instance = __file__.split(
                "/")[3]       # it gives instance name of nagios system
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

            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)

            device_name_list = {'ap25': 'AP25', 'odu16':
                'RM18', 'odu100': 'RM', 'idu4': 'IDU'}
            login_user_name = ''
            sel_query = "SELECT host_alias FROM hosts WHERE ip_address='%s' and hosts.is_deleted=0" % (
                ip_address)
            cursor.execute(sel_query)
            uesr_information = cursor.fetchall()
            if len(uesr_information) > 0:
                login_user_name = uesr_information[0][0]
            master_slave_status = get_master_slave_value(ip_address)
            device_postfix = '(Master)'
            if master_slave_status['success'] == 0 and master_slave_status['status'] > 0:
                device_postfix = '(Slave)'
            sel_query = "select graph_display_id,graph_display_name from graph_templet_table where graph_display_id='%s' and user_id='%s' and device_type_id='%s' and dashboard_type=1" % (
                graph_id, user_id, device_type_id)
            cursor.execute(sel_query)
            graph_name_result = cursor.fetchall()
            # graph_name_dict=dict((field[0],field[2]) for field in graph_name_result)
            graph_name = [field[1] for field in graph_name_result]
            headings = []
            merge_result = []
            output_result = self.advanced_graph_data(
                user_id, ip_address, start_date, end_date, graph_id, device_type_id)
            if int(output_result['success']) == 0:
                headings = output_result['data']['th']
                for data_list in output_result['data']['td']:
                    merge_result.append(data_list)
            else:
                raise SelfException('MySQL Error')

            # we get the host inforamtion.
            sel_query = "SELECT device_type.device_name,hosts.host_alias FROM hosts INNER JOIN device_type ON hosts.device_type_id=device_type.device_type_id WHERE hosts.ip_address='%s' and hosts.is_deleted=0" % (
                ip_address)
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
                '(eth1)', '3': '(cpu)', '4': '(maxima)'}
            #,'idu_portstatisticsTable':idu4_port'idu_portstatisticsTable':idu4_port
            interface_list = {'get_odu16_nw_interface_statistics_table': {'1': '(eth0)', '2': '(br0)', '3': '(eth1)'},
                              'odu100_nwInterfaceStatisticsTable': {'1': '(eth0)', '2': '(eth1)'},
                              'ap25_statisticsTable': {'0': '(eth0)', '1': '(br0)', '2': '(ath0)', '3': '(ath1)',
                                                       '4': '(ath2)', '5': '(ath3)', '6': '(ath4)', '7': '(ath5)',
                                                       '8': '(ath6)'},
                              'idu_e1PortStatusTable': {'1': '(port1)', '2': '(port2)', '3': '(port3)', '4': '(port4)'},
                              'idu_portstatisticsTable': idu4_port, 'idu_swPrimaryPortStatisticsTable': idu4_port,
                              'idu_portSecondaryStatisticsTable': idu4_port}

            if report_type == 'excelReport':
                save_file_name = str(device_name_list[device_type_id]) + '_' + str(
                    login_user_name) + '_' + str(start_date) + '.xls'
                xls_sheet = xls_book.add_sheet(
                    'Device Status Sheet', cell_overwrite_ok=True)
                xls_sheet.row(0).height = 521
                xls_sheet.row(1).height = 421
                xls_sheet.write_merge(
                    0, 0, 0, len(headings) - 1, str(graph_name[0]), style)
                xls_sheet.write_merge(1, 1, 0, len(headings) - 1, str(device_type) + '       ' + str(
                    ip_address) + str(device_postfix) + '     (' + str(start_date) + '-' + str(end_date) + ')', style)
                xls_sheet.write_merge(2, 2, 0, len(headings) - 1, "")
                i = 4
                heading_xf = xlwt.easyxf(
                    'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
                xls_sheet.set_panes_frozen(
                    True)  # frozen headings instead of split panes
                xls_sheet.set_horz_split_pos(
                    i)  # in general, freeze after last heading row
                xls_sheet.set_remove_splits(
                    True)  # if user does unfreeze, don't leave a split there
                for colx, value in enumerate(headings):
                    xls_sheet.write(i - 1, colx, value, heading_xf)
                for k in range(len(merge_result)):
                    for j in range(len(merge_result[k])):
                        width = 5000
                        xls_sheet.write(i, j, str(merge_result[k][j]), style1)
                        xls_sheet.col(j).width = width
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
                main_row = [str(graph_name[0])]
                second_row = [str(device_type), str(ip_address) + str(
                    device_postfix) + '      (' + str(start_date) + '-' + str(end_date) + ')']
                writer.writerow(main_row)
                writer.writerow(second_row)
                writer.writerow(blank_row)
                writer.writerow(headings)
                for row1 in merge_result:
                    writer.writerow(row1)
                ofile.close()
            output_dict = {'success': 0, 'output': 'Report Generated Successfully.', 'file_name':
                str(save_file_name), 'path': path}
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

    def ap_data_table(self, user_id, ip_address, start_date, end_date, graph_id, device_type):
        """

        @param user_id:
        @param ip_address:
        @param start_date:
        @param end_date:
        @param graph_id:
        @param device_type:
        @return: @raise:
        """
        try:
            datatable_column_list = []
            merge_result = []
            conn, cursor = mysql_connection()
            if conn == 1:
                raise SelfException(cursor)
            output_result = self.advanced_graph_data(
                user_id, ip_address, start_date, end_date, graph_id, device_type)
            if int(output_result['success']) == 0:
                datatable_column_list = output_result['data']['th']
                for data_list in output_result['data']['td']:
                    merge_result.append(data_list)
            else:
                raise SelfException('MySQL Error')
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


def manage_list(req, given, result):
    """

    @param req:
    @param given:
    @param result:
    @return:
    """
    outdata = []
    inpt = result
    for i in inpt:
        li = []
        for k in req:
            li.append("0")
        for j in given:
            if (req.count(j) >= 1):
                loc = given.index(j)
                wloc = req.index(j)
                temp = i[loc]
                li.pop(wloc)
                li.insert(wloc, str(temp))
        outdata.append(li)
    return outdata


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
