#!/usr/bin/python
#######################################################################################
# Author            :    Rajendra Sharma
# Project            :    UNMP
# Version            :    0.1
# File Name            :    odu_dashboard.py
# Creation Date            :    11-September-2011
# Purpose            :    This file display the graph for ODU Device type DASHBOARD.
# Copyright (c) 2011 Codescape Consultant Private Limited

##########################################################################

from datetime import datetime
from datetime import timedelta
from operator import itemgetter

import MySQLdb
from common_bll import Essential
from common_controller import *
from mysql_collection import mysql_connection
from nms_config import *
from odu_controller import *
from unmp_dashboard_config import DashboardConfig
from utility import Validation


# Exception class for own created exception.


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
        output_dict = {'success': 2, 'output': str(msg)}
        html.write(str(output_dict))


def get_dashboard_data():
    """


    @return:
    """
    devcie_type_attr = ['id', 'refresh_time', 'time_diffrence']
    get_data = DashboardConfig.get_config_attributes(
        'odu100_dashboard', devcie_type_attr)
    odu_refresh_time = 10   # default time
    total_count = 10    # default count showing record
    if get_data is not None:
        if get_data[0][0] == 'odu100_D':
            odu_refresh_time = get_data[0][1]
            total_count = get_data[0][2]
    return str(odu_refresh_time), str(total_count)


def odu_profiling(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_id = html.req.session['user_id']
    es = Essential()

    if es.is_host_allow(user_id, host_id) == 0:
        flag = 0
        css_list = ["css/style.css", "css/custom.css",
                    "calendrical/calendrical.css"]
        javascript_list = ["js/lib/main/highcharts.js",
                           "js/unmp/main/odu100Dashboard.js", "calendrical/calendrical.js"]
        html.new_header("UBRe Dashboard", "", "", css_list, javascript_list)
        html.write('<div class=\"form-div\">')
        host_id = ""
        extr_button = {'tag': 'button', 'id': 'adSrhODU100',
                       'value': 'Advance Graph', 'name': 'adSrhODU100'}
        host_id = html.var("host_id")
        # this is used for storing DeviceTypeList e.g "odu16,odu100"
        device_type = ""

        # this is used for storing DeviceListState e.g "enabled"
        device_list_state = ""

        device_list_param = []
        if html.var("device_type") != None:  # we get the variable of page through html.var
            device_type = html.var("device_type")
        if html.var("device_list_state") != None:
            device_list_state = html.var("device_list_state")
        if host_id == None:
            host_id = ""
        device_list_param = get_device_param(host_id)
        html.header("UBRe Monitoring")
        if device_list_param == [] or device_list_param == None:
            flag = 1
            output, mac_address = get_device_field(host_id)
            if int(output) == 1:
                html.write(page_header_search("", "", "UBR,UBRe",
                                              device_type, "enabled", "device_type", extr_button))
            else:
                html.write(page_header_search(host_id, mac_address,
                                              "UBR,UBRe", device_type, "enabled", "device_type", extr_button))
        else:
            html.write(
                page_header_search(
                    device_list_param[0][0], device_list_param[0][1],
                    "UBR,UBRe", device_list_param[0][2], device_list_state, "device_type", extr_button))
        if host_id == "" or host_id == "None":
            val = ""
            flag = 1
            html.write(
                "<div id=\"odu100_show_msg\"></div><div id=\"tab_yo\">There is no profile selected</div>")
        else:
            html.write(
                "<div id=\"odu100_show_msg\"></div><div id=\"tab_yo\" style=\"display:block;overflow:hidden\">")
            flag = 0
            odu100_dashboard(h)
            html.write("</div>")
        if flag == 0:
            html.write('<div id=\"report_button_div\" class=\"form-div-footer\">\
		<table cellspacing="9px" cellpadding="0">\
		<tr>\
		<td style="vertical-align:middle;"><input type=\"radio\" value=\"0\" name=\"option\" id=\"current_rept_div\" class=\"table_option\" width=\"12px\"/></td>\
		<td style="vertical-align:middle;"><label for=\"current_rept_div\" width=\"25px\">Current Time</label></td>\
		<td style="vertical-align:middle;"><input type=\"radio\" value=\"1\" name=\"option\" id=\"day1_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
		<td style="vertical-align:middle;"><label for=\"day1_rprt_div\" width=\"25px\">1 Day</label></td>\
		<td style="vertical-align:middle;"><input type=\"radio\" value=\"2\" name=\"option\" id=\"day2_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
		<td style="vertical-align:middle;"><label for=\"day2_rprt_div\" width=\"25px\">2 Day</label></td>\
		<td style="vertical-align:middle;"><input type=\"radio\" value=\"3\" name=\"option\" id=\"day3_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
		<td style="vertical-align:middle;"><label for=\"day3_rprt_div\" width=\"25px\">3 Day</label></td>\
		<td style="vertical-align:middle;"><input type=\"radio\" value=\"4\" name=\"option\" id=\"week_rprt_div\" class=\"table_option\" width=\"12px\"/></td>\
		<td style="vertical-align:middle;"><label for=\"week_rprt_div\" width=\"25px\">1 Week</label></td>\
		<td style="text-align:right"><button type=\"submit\" class=\"yo-button\" id=\"odu_report_btn\" style=\"margin-top:5px;\" onclick="odu100ReportGeneration();"><span class=\"save\">Report</span></button></td>\
		 <td style="text-align:left"><button type=\"submit\" class=\"yo-button\" style=\"margin-top:5px;\" onclick="odu100ExcelReportGeneration();"><span class=\"report\">Report</span></button></td>\
		</tr></table>\
		</div></div>\
		')
        else:
            html.write('</div>')
    else:
        html.new_header(" Warning : Page request not granted", "", "")
        html.write(
            "<div class=\"warning\" > Access Restricted. Please request access from UNMP admin.</div>")
    html.new_footer()


def get_device_field(ip_address):
    """

    @param ip_address:
    @return: @raise:
    """
    try:
        mac_address = ''
        db, cursor = mysql_connection()  # create the connection
        if db == 1:
            raise SelfException(cursor)
        if Validation.is_valid_ip(ip_address):
            sel_query = "select mac_address from hosts where ip_address='%s'" % (
                ip_address)
            cursor.execute(sel_query)
            mac_result = cursor.fetchall()
            if len(mac_result) > 0:
                mac_address = mac_result[0][0]
        else:
            sel_query = "select mac_address from hosts where host_id='%s'" % (
                ip_address)
            cursor.execute(sel_query)
            mac_result = cursor.fetchall()
            if len(mac_result) > 0:
                mac_address = mac_result[0][0]
        return 0, mac_address
    except SelfException:
        return 1, str(e[-1])
    except Exception as e:
        return 1, str(e[-1])
    finally:
        if db and db.open:
            db.close()
            cursor.close()


def get_device_list_odu100(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h

    # this is the result which we show on the page
    result = ""
    ip_address = ""
    mac_address = ""
    selected_device = "odu16"
    # take value of IPaddress from the page through html.var
    # check that value is None Then It takes the empty string
    if html.var("ip_address") == None:
        ip_address = ""
    else:
        ip_address = html.var("ip_address")

    # take value of MACAddress from the page through html.var
    # check that value is None Then It takes the empty string
    if html.var("mac_address") == None:
        mac_address = ""
    else:
        mac_address = html.var("mac_address")

    # take value of SelectedDevice from the page through html.var
    # check that value is None Then It takes the empty string
    if html.var("selected_device_type") == None:
        selected_device = "odu16"
    else:
        selected_device = html.var("selected_device_type")

    # call the function get_odu_list of odu-controller which return us the
    # list of devices in two dimensional list according to
    # IPAddress,MACaddress,SelectedDevice
    result = get_device_list_odu_profiling(
        ip_address, mac_address, selected_device)
    if result == 0 or result == 1 or result == 2:
        html.write(str(result))
    else:
        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)
        if Validation.is_valid_ip(result):
            ip_address = result
            if ip_address is not '' or ip_address is not None:
                html.write('0')
            else:
                html.write(str(ip_address[0][0]))
        else:
            sel_query = "select ip_address from hosts where host_id='%s'" % (
                result)
            cursor.execute(sel_query)
            ip_address = cursor.fetchall()
            if len(ip_address) > 0:
                html.write(str(ip_address[0][0]))
            else:
                html.write('0')
        cursor.close()
        db.close()
        # odu100_dashboard(h)

#	html.write(str(result))


def dashboard_table(ip_address, odu_start_date, odu_start_time, odu_end_date, odu_end_time, odu_refresh_time,
                    total_count):
    """

    @param ip_address:
    @param odu_start_date:
    @param odu_start_time:
    @param odu_end_date:
    @param odu_end_time:
    @param odu_refresh_time:
    @param total_count:
    @return:
    """
    dash_str = '\
    <input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />\
    <input type=\"hidden\" id=\"ip_address\" name=\"ip_address\" value=\"%s\" />\
    <input type=\"hidden\" id=\"total_count\" name=\"total_count\" value=\"%s\" />\
    <div style=\"float: right; font-size: 10px; color: rgb(85, 85, 85); font-weight: bold; padding: 10px 20px;\" >\
    <input type=\"textbox\" name=\"odu_start_date\" value=\"%s\" id=\"odu_start_date\" style=\"width:100px;\"/>\
    <input type=\"textbox\" name=\"odu_start_time\" value=\"%s\" id=\"odu_start_time\" style=\"width:80px;\"/>\
    <lable>--</lable>\
    <input type=\"textbox\" name=\"odu_end_date\" value=\"%s\" id=\"odu_end_date\" style=\"width:100px;\"/>\
    <input type=\"textbox\" name=\"odu_end_time\" value=\"%s\" id=\"odu_end_time\" style=\"width:80px;\"/>\
    <input type=\"button\" class=\"yo-small  yo-button\" name=\"odu_graph_show\" value=\"graph\" id=\"odu_graph_show\" style=\"width:50px;\"/>\
   </div>\
    </div>\
    <div id="odu100_host_info_div"></div>\
    <table id=\"odu100_device_graph\" cellspacing="10px" cellpadding="0" width="100%%">\
        <colgroup>\
            <col width="50%%" style="width:50%%;"/>\
            <col width="50%%" style="width:50%%;"/>\
        </colgroup>\
        <tr>\
            <td><div id="dashboard1" class="db-box"></div></td>\
            <td><div id="dashboard2" class="db-box"></div></td>\
        </tr>\
        <tr>\
            <td><div id="dashboard3" class="db-box"></div></td>\
            <td><div id="dashboard4" class="db-box"></div></td>\
        </tr>\
        <tr>\
            <td><div id="dashboard5" class="db-box"></div></td>\
            <td><div id="dashboard6" class="db-box"></div></td>\
        </tr>\
        <tr>\
            <td><div id="dashboard7" class="db-box"></div></td>\
            <td><div id="dashboard8" class="db-box"></div></td>\
        </tr>\
    </table>' % (odu_refresh_time, ip_address, total_count, odu_start_date, odu_start_time, odu_end_date, odu_end_time)
    return dash_str


def odu100_dashboard(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    host_id = html.var("host_id")
    odu_refresh_time, total_count = get_dashboard_data()
    # start datetime and end datetime variable
    now = datetime.now()
    odu_end_date = now.strftime("%d/%m/%Y")
    odu_end_time = now.strftime("%H:%M")
    now = now + timedelta(minutes=-int(total_count))
    odu_start_date = now.strftime("%d/%m/%Y")
    odu_start_time = now.strftime("%H:%M")

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
            if host_id == "" or host_id == None:
                ip_address = html.var("ip_address")
                mac_address = html.var("mac_address")
                selected_device = html.var("selected_device_type")
                if cursor.execute("SELECT ip_address from hosts where mac_address = '%s' and device_type_id = '%s'") % (
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
        cursor.close()
        db.close()
        html.write(
            str(dashboard_table(ip_address, odu_start_date, odu_start_time,
                                odu_end_date, odu_end_time, str(odu_refresh_time), str(total_count))))

        # odu_network_interface_table_graph(h)
    # Exception Handling
    except MySQLdb as e:
        html.write('No Data Exists For Graphs.')
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        pass
    except Exception as e:
        html.write('No Data Exists For Graphs.')
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()


def odu100_network_interface_table_graph(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    rx0 = []
    tx0 = []
    time_stamp0 = []
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    interface_value = html.var('interface_value')
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    try:
        # Open database connection

        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)
            # prepare a cursor object using cursor() method
        # convert the string in datetime
        start_time = datetime.strptime(
            odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
        end_time = datetime.strptime(
            odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
        if int(limitFlag) == 0:
            limit_data = ''
        else:
            limit_data = ' limit 16'
        sel_query = "select (odu.rxBytes),(odu.txBytes),odu.timestamp from odu100_nwInterfaceStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where  h.ip_address='%s' AND  odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.nwStatsIndex = '%s' order by odu.timestamp desc" % (
            ip_address, start_time, end_time, interface_value)
        sel_query += limit_data
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if result is not None:
            for i in range(len(result) - 1):
                rx_byte = ((int(result[i][0]) - int(result[i + 1][0])) / 1024)
                tx_byte = ((int(result[i][1]) - int(result[i + 1][1])) / 1024)
                rx0.append(0 if rx_byte <= 0 else rx_byte)
                tx0.append(0 if tx_byte <= 0 else tx_byte)
                time_stamp0.append(result[i][2].strftime('%H:%M'))
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'interface_rx': rx0, 'interface_tx': tx0,
                       'time_stamp0': time_stamp0, 'ip_address': ip_address}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


def odu100_error_graph(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    crc_error = []
    phy_error = []
    error_time_stamp = []
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    try:
        # Open database connection

        db, cursor = mysql_connection('nms_sample')
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
        sel_query = "select IFNULL((odu.rxCrcErrors),0),IFNULL((odu.rxPhyError),0),odu.timestamp from  odu100_raTddMacStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp <='%s' AND odu.timestamp >= '%s' order by odu.timestamp" % (
            ip_address, end_time, start_time)
        sel_query += limit_data
        cursor.execute(sel_query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        # calling the procedure.
        for i in range(len(result) - 1):
            crc_error.append(0 if (int(result[i][0]) - int(result[i + 1][0])) <
                                  0 else (int(result[i][0]) - int(result[i + 1][0])))
            phy_error.append(0 if (int(result[i][0]) - int(result[i + 1][1])) <
                                  0 else (int(result[i][0]) - int(result[i + 1][1])))
            error_time_stamp.append(result[i][2].strftime('%H:%M'))
            # reverse the value in list
        error_time_stamp.reverse()
        crc_error.reverse()
        crc_error.reverse()
        output_dict = {
            'success': 0, 'crc_error': crc_error, 'phy_error': phy_error,
            'time_stamp': error_time_stamp, 'time': str(start_time), 'end_time': str(end_time)}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


def odu100_sync_lost_graph(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    sync_lost = []
    sync_time_stamp = []
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    limitFlag = html.var("limitFlag")
    ip_address = html.var("ip_address")
    try:
        # Open database connection

        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)
            # convert the string to datetime
        start_time = datetime.strptime(
            odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
        end_time = datetime.strptime(
            odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
        if int(limitFlag) == 0:
            limit_data = ''
        else:
            limit_data = ' limit 16'
        sel_query = "select IFNULL((odu.syncLostCounter),0),odu.timestamp from  odu100_synchStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' order by odu.timestamp" % (
            ip_address, start_time, end_time)
        sel_query += limit_data
        cursor.execute(sel_query)
        result = cursor.fetchall()
        if result is not None:
            for i in range(len(result) - 1):
                sync_lost.append(0 if (int(result[i][0]) - int(
                    result[i + 1][0])) < 0 else (int(result[i][0]) - int(result[i + 1][0])))
                sync_time_stamp.append(result[i][1].strftime('%H:%M'))
            # reverse the list
        sync_time_stamp.reverse()
        sync_lost.reverse()
        output_dict = {'success': 0, 'sync_lost': sync_lost,
                       'sync_time_stamp': sync_time_stamp}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


def odu100_signal_strength_graph(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    signal_flag = 1
    signal_interface1 = []
    signal_interface2 = []
    signal_interface3 = []
    signal_interface4 = []
    signal_interface5 = []
    signal_interface6 = []
    signal_interface7 = []
    signal_interface8 = []
    signal_interface9 = []
    signal_interface10 = []
    signal_interface11 = []
    signal_interface12 = []
    signal_interface13 = []
    signal_interface14 = []
    signal_interface15 = []
    signal_interface16 = []

    time_stamp_signal1 = []

    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    limitFlag = html.var("limitFlag")
    ip_address = html.var("ip_address")
    signal_strength = [
        "peer1", "peer2", "peer3", "peer4", "peer5", "peer6", "peer7", "peer8",
        "peer9", "peer10", "peer11", "peer12", "peer13", "peer14", "peer15", "peer16"]
    try:
        # Open database connection

        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)

        # convert the string to datetime
        start_time = datetime.strptime(
            odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
        end_time = datetime.strptime(
            odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
        # Signal Strength  json list creation #
        sel_query = "SELECT defaultNodeType FROM odu100_ruConfTable as def INNER JOIN hosts ON hosts.config_profile_id=def.config_profile_id WHERE hosts.ip_address='%s'" % (
            ip_address)
        cursor.execute(sel_query)
        status_result = cursor.fetchall()
        status = 0
        if len(status_result) > 0:
            status = 0 if status_result[0][0] == None else status_result[0][0]
        status_name = 'Master' if int(status) == 0 else 'Slave'
        if int(limitFlag) == 0:
            limit_data = ''
        else:
            signal_flag = 0
            if status_name == 'Master':
                limit_data = ' limit 40'
            else:
                limit_data = ' limit 5'
        sel_query = "select odu.timeSlotIndex,(IFNULL((odu.sigStrength1),0)),odu.timestamp,odu.ssIdentifier,odu.linkStatus,odu.tunnelStatus,odu.peerMacAddr from  odu100_peerNodeStatusTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' order by odu.timestamp desc" % (
            ip_address, start_time, end_time)
        sel_query += limit_data
        cursor.execute(sel_query)
        signal_strength = cursor.fetchall()
        count = 0
        flag = 0
        default_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for k in range(0, len(signal_strength) - 1):
            flag = 1
            if count == 5 and signal_flag == 0:
                break
            if signal_strength[k][1] == 1 or str(signal_strength[k][1]) == '1':
                count += 1
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%H:%M')))
            else:
                if signal_strength[k][2] == signal_strength[k + 1][2]:
                    default_list[int(
                        signal_strength[k][0]) - 1] = int(signal_strength[k][1])
                else:

                    count += 1
                    default_list[int(
                        signal_strength[k][0]) - 1] = int(signal_strength[k][1])
                    signal_interface1.append(default_list[0])
                    signal_interface2.append(default_list[1])
                    signal_interface3.append(default_list[2])
                    signal_interface4.append(default_list[3])
                    signal_interface5.append(default_list[4])
                    signal_interface6.append(default_list[5])
                    signal_interface7.append(default_list[6])
                    signal_interface8.append(default_list[7])
                    signal_interface9.append(default_list[8])
                    signal_interface10.append(default_list[9])
                    signal_interface11.append(default_list[10])
                    signal_interface12.append(default_list[11])
                    signal_interface13.append(default_list[12])
                    signal_interface14.append(default_list[13])
                    signal_interface15.append(default_list[14])
                    signal_interface16.append(default_list[15])
                    time_stamp_signal1.append(
                        str((signal_strength[k][2]).strftime('%H:%M')))
                    default_list = [0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if len(signal_strength) > 0 and flag == 0:
            if signal_strength[0][1] == 1 or str(signal_strength[0][1]) == '1':
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[0][2]).strftime('%H:%M')))
            else:
                default_list[int(signal_strength[0][0]) -
                             1] = int(signal_strength[0][1])
                signal_interface1.append(default_list[0])
                signal_interface2.append(default_list[1])
                signal_interface3.append(default_list[2])
                signal_interface4.append(default_list[3])
                signal_interface5.append(default_list[4])
                signal_interface6.append(default_list[5])
                signal_interface7.append(default_list[6])
                signal_interface8.append(default_list[7])
                signal_interface9.append(default_list[8])
                signal_interface10.append(default_list[9])
                signal_interface11.append(default_list[10])
                signal_interface12.append(default_list[11])
                signal_interface13.append(default_list[12])
                signal_interface14.append(default_list[13])
                signal_interface15.append(default_list[14])
                signal_interface16.append(default_list[15])
                time_stamp_signal1.append(
                    str((signal_strength[0][2]).strftime('%H:%M')))
        if flag == 1 and len(signal_strength) > 0:
            if signal_strength[k][1] == 1 or str(signal_strength[k][1]) == '1':
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%H:%M')))
            else:
                default_list[int(signal_strength[k][0]) -
                             1] = int(signal_strength[k][1])
                signal_interface1.append(default_list[0])
                signal_interface2.append(default_list[1])
                signal_interface3.append(default_list[2])
                signal_interface4.append(default_list[3])
                signal_interface5.append(default_list[4])
                signal_interface6.append(default_list[5])
                signal_interface7.append(default_list[6])
                signal_interface8.append(default_list[7])
                signal_interface9.append(default_list[8])
                signal_interface10.append(default_list[9])
                signal_interface11.append(default_list[10])
                signal_interface12.append(default_list[11])
                signal_interface13.append(default_list[12])
                signal_interface14.append(default_list[13])
                signal_interface15.append(default_list[14])
                signal_interface16.append(default_list[15])
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%H:%M')))

        # reverse the string
        signal_list = []
        signal_list.append(signal_interface1)
        signal_list.append(signal_interface2)
        signal_list.append(signal_interface3)
        signal_list.append(signal_interface4)
        signal_list.append(signal_interface5)
        signal_list.append(signal_interface6)
        signal_list.append(signal_interface7)
        signal_list.append(signal_interface8)
        signal_list.append(signal_interface9)
        signal_list.append(signal_interface10)
        signal_list.append(signal_interface11)
        signal_list.append(signal_interface12)
        signal_list.append(signal_interface13)
        signal_list.append(signal_interface14)
        signal_list.append(signal_interface15)
        signal_list.append(signal_interface16)
        time_stamp_signal1.reverse()
        peer_count = 0
        for signal in signal_list:
            signal.reverse()
            for i in signal:
                if i != 0:
                    peer_count += 1
                    break

        if status_name == 'Master':
            signal_json_data = "["
            for i in range(peer_count):
                signal_json_data += "{name:'peer%s',data:%s}%s" % (
                    i + 1, signal_list[i], ',' if i < peer_count - 1 else '')
            signal_json_data += "]"
        else:
            signal_json_data = "[{name:'peer1',data:%s}]" % (signal_interface1)
            # close the connection
        db.close()
        output_dict = {'success': 0, 'time_stamp':
            time_stamp_signal1, 'display_signal_strength': signal_json_data}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()

# This function display the odu trap graph according to servity and its take only
# This function take h request parameter
# This function return 5 day graph information for graph display.
# Data return in json dictionary format.


def odu100_trap_graph(h):
    """ This function get ip_address of odu device  form and retuen the 5 day information.
    @param h:
    """
    global html
    html = h
    normal = []
    inforamtional = []
    minor = []
    major = []
    critical = []
    time_stamp = []
    ip_address = html.var("ip_address")
    odu_trap_detail = {}
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')

    try:
        # create database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        # convert the string to datetime
        # convert the string to datetime
        end_time = datetime.strptime(
            odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
        start_time = datetime.strptime(
            odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
        if start_time > datetime.now():
            start_time = datetime.now()
            # calculate the total days
        # total_days=((start_time-end_time).days)  check after the consult to
        # peeyush sir

        # call.proc("procedure name",(no_of_day,odu ip_address))
        sql = "SELECT count(ta.trap_event_id),date(ta.timestamp) ,ta.serevity FROM trap_alarms as ta  where  date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s AND ta.agent_id='%s'  group by serevity,date(ta.timestamp) order by  timestamp desc" % (
        5, ip_address)
        cursor.execute(sql)
        trap_result = cursor.fetchall()
        if trap_result is not None:
            # store the information in list.
            for i in range(0, 5):
                normal1 = 0
                inforamtional1 = 0
                minor1 = 0
                major1 = 0
                critical1 = 0
                for row in trap_result:
                    if datetime.date(datetime.now() + timedelta(days=-i)) == row[1]:
                        if int(row[2]) == 0:
                            normal1 += int(row[0])
                        elif int(row[2]) == 2:
                            normal1 += int(row[0])
                        elif int(row[2]) == 1:
                            inforamtional1 += int(row[0])
                        elif int(row[2]) == 3:
                            minor1 += int(row[0])
                        elif int(row[2]) == 4:
                            major1 += int(row[0])
                        elif int(row[2]) == 5:
                            critical1 += int(row[0])
                time_stamp.append(datetime.date(
                    datetime.now() + timedelta(days=-i)).strftime('%x'))
                normal.append(normal1)
                inforamtional.append(inforamtional1)
                minor.append(minor1)
                major.append(major1)
                critical.append(critical1)
        time_stamp.reverse()
        normal.reverse()
        inforamtional.reverse()
        minor.reverse()
        major.reverse()
        critical.reverse()

        cursor.close()
        db.close()
        odu_trap_detail = {'success': 0, 'output': {'graph': [normal, inforamtional,
                                                              minor, major, critical], 'timestamp': time_stamp}}
        html.write(str(odu_trap_detail))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


# this function show the outage graph for particular device.
# this function take one argument and return the dictionary of outage
# graph information.
def odu100_outage_graph(h):
    """this function create the outage graph field and show the outage graph.
    @param h:
    """
    global html
    html = h
    date_days = []  # this list store the days information with date.
    up_state = []  # Its store the total up state of each day in percentage.
    down_state = []
    # Its store the total down state of each day in percentage.
    output_dict = {}  # its store the actual output for display in graph.
    last_status = ''
    down_flag = 0
    up_flag = 0
    ip_address = html.var("ip_address")
    current_date = datetime.date(datetime.now())
    # ed=str(current_date+timedelta(days=-14)) # Its used for testing.
    # cd=str(current_date+timedelta(days=-23)) # Its used for testing.
    current_datetime = datetime.strptime(str(current_date + timedelta(
        days=-5)) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
    # last_datetime=datetime.strptime(str(current_date+timedelta(days=-1))+"
    # 23:59:59",'%Y-%m-%d %H:%M:%S') # convert the string in  datetime.
    last_datetime = datetime.strptime(
        str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    temp_date = last_datetime
    # this datetime last status calculation
    last_status_current_time = datetime.strptime(str(current_date + timedelta(
        days=-6)) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
    last_status_end_time = datetime.strptime(str(current_date + timedelta(
        days=-5)) + " 23:59:59", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
    try:
        # connection from mysql
        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)

        sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
		    FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
		   where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
		    order by nagios_statehistory.state_time " % (current_datetime, last_datetime, ip_address)
        # Execute the query.
        cursor.execute(sql)
        result = cursor.fetchall()

        # this query get last status of device
        sel_sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
		    FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
		   where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
		    order by nagios_statehistory.state_time  desc limit 1" % (
        last_status_current_time, last_status_end_time, ip_address)
        # Execute the query.
        cursor.execute(sel_sql)
        last_state = cursor.fetchall()
        if last_state is not None:
            if len(last_state) > 0:
                last_status = last_state[0][2]

        if result is not None:
            if len(result) > 0:
                for i in range(5):
                    flag = 0
                    total_down_time = 0
                    total_up_time = 0
                    temp_down_time = ''
                    temp_up_time = ''
                    temp_time = ''
                    j = 0
                    for row in result:
                        if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                            flag = 1
                            if row[2] == 0:
                                if temp_up_time == '':
                                    temp_up_time = row[1]
                                    if last_status == '' and up_flag == 0:
                                        if temp_time is not '':
                                            if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                total_up_time += abs((
                                                                         row[1] - temp_time).days * 1440 + (
                                                                     row[1] - temp_time).seconds / 60)
                                                temp_up_time = row[1]
                                            else:
                                                total_down_time += abs(
                                                    (row[1] - temp_time).days * 1440 + (
                                                    row[1] - temp_time).seconds / 60)
                                                temp_down_time = row[1]
                                        up_flag = 1
                                    elif last_status is not '' and up_flag == 0:
                                        up_flag = 1
                                        if last_status == 0:
                                            total_up_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                        else:
                                            total_down_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:
                                    if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                        total_up_time += abs((
                                                                 row[1] - temp_time).days * 1440 + (
                                                             row[1] - temp_time).seconds / 60)
                                        temp_up_time = row[1]
                                    else:
                                        total_down_time += abs((row[1] - temp_time).days * 1440 + (
                                            row[1] - temp_time).seconds / 60)
                                        temp_down_time = row[1]
                            else:
                                if temp_down_time == '':
                                    temp_down_time = row[1]
                                    if last_status == '' and down_flag == 0:
                                        if temp_time is not '':
                                            if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                total_up_time += abs((
                                                                         row[1] - temp_time).days * 1440 + (
                                                                     row[1] - temp_time).seconds / 60)
                                                temp_up_time = row[1]
                                            else:
                                                total_down_time += abs(
                                                    (row[1] - temp_time).days * 1440 + (
                                                    row[1] - temp_time).seconds / 60)
                                                temp_down_time = row[1]
                                        down_flag = 1
                                    elif last_status is not '' and down_flag == 0:
                                        down_flag = 1
                                        if last_status == 0:
                                            total_up_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                        else:
                                            total_down_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:

                                    if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                        total_up_time += abs((
                                                                 row[1] - temp_time).days * 1440 + (
                                                             row[1] - temp_time).seconds / 60)
                                        temp_up_time = row[1]
                                    else:
                                        total_down_time += abs((row[1] - temp_time).days * 1440 + (
                                            row[1] - temp_time).seconds / 60)
                                        temp_down_time = row[1]

                        if j < len(result):
                            temp_time = row[1]
                        j += 1
                    if flag == 1:
                        if result[j - 1][2] == 0:
                            total_up_time = abs((result[j - 1][1] - (temp_date + timedelta(days=-i))).days *
                                                1440 + (
                            result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                        else:
                            total_down_time = abs((result[j - 1][1] - (
                                temp_date + timedelta(days=-i))).days * 1440 + (
                                                  result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                    date_days.append(
                        (temp_date + timedelta(days=-(i))).strftime("%d %b %Y"))
                    total = total_up_time + total_down_time
                    if flag == 1 and total > 0:
                        up_state.append(
                            round((total_up_time * 100) / float(total), 2))
                        down_state.append(
                            round((total_down_time * 100) / float(total), 2))
                    else:
                        up_state.append(0)
                        down_state.append(0)
            else:
                sel_sql = "SELECT  nagios_hosts.address,nagios_hoststatus.status_update_time,nagios_hoststatus.current_state\
				    FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hoststatus.host_object_id = nagios_hosts.host_object_id\
				   where nagios_hoststatus.status_update_time between '%s'  and '%s' and nagios_hosts.address='%s'\
				    order by nagios_hoststatus.status_update_time " % (current_datetime, last_datetime, ip_address)
                cursor.execute(sel_sql)
                result = cursor.fetchall()
                for i in range(5):
                    flag = 0
                    total_down_time = 0
                    total_up_time = 0
                    for row in result:
                        if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                            flag = 1
                            if row[2] == 0:
                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                    days=-(i + 1)))).days * 1440 + (
                                                    row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                            else:
                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                    days=-(i + 1)))).days * 1440 + (
                                                      row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                    date_days.append(
                        (temp_date + timedelta(days=-(i))).strftime("%d %b %Y"))
                    total = total_up_time + total_down_time
                    if flag == 1 and total > 0:
                        up_state.append(
                            round((total_up_time * 100) / float(total), 2))
                        down_state.append(
                            round((total_down_time * 100) / float(total), 2))
                    else:
                        up_state.append(0)
                        down_state.append(0)

        # close the database and cursor connection.
        cursor.close()
        db.close()

        up_state.reverse()
        down_state.reverse()
        date_days.reverse()

        output_dict = {'success': 0, 'up_state': up_state,
                       'down_state': down_state, 'date_days': date_days}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


# This function display the table of latest current alarms and latest traps.
# This function take h request parameter.
# This function return latest information of alarms and trap.
# This return data in json format.
def odu100_trap_information(h):
    """ This finction get  ip_address in varcahr form and return the last 5 alarm from trap from history.
    @param h:
    """
    global html
    html = h
    image_title_name = {0: "Normal", 1: "Informational", 2: "Normal",
                        3: "Minor", 4: "Major", 5: "Critical"}
    image_dic = {0: "images/status-0.png", 1: "images/status-0.png", 2: "images/status-0.png", 3:
        "images/minor.png", 4: "images/status-1.png", 5: "images/critical.png"}
    length = 5
    history_trap_detail = {}
    ip_address = html.var("ip_address")
    table_option = html.var('table_option')

    # host_id=html.var("host_id")
    try:
        # create database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        if table_option.strip() == "trap":
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' order by ta.timestamp desc limit 7 " % ip_address
            cursor.execute(sql)
            all_traps = cursor.fetchall()

            if len(all_traps) < 5:
                length = len(all_traps)

            history_trap = '<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
            history_trap += '<tbody>\
            <tr class="yo-table-head" >\
                <th class=" vertline">&nbsp;</th>\
                <th>Event Id</th>\
                <th>Event Type</th>\
                <th>Receive Date</th>\
            </tr>'

            for i in range(length):
                if i < 4:
                    history_trap += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                        image_dic[all_traps[i][0]], image_title_name[all_traps[i][0]],
                        image_title_name[all_traps[i][0]])
                    history_trap += '<td>%s</td>' % all_traps[i][1]
                    history_trap += '<td>%s</td>' % all_traps[i][2]
                    history_trap += '<td>%s</td></tr>' % all_traps[i][3]
                else:
                    history_trap += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                        image_dic[all_traps[i][0]], image_title_name[all_traps[i][0]],
                        image_title_name[all_traps[i][0]])
                    history_trap += '<td>%s</td>' % all_traps[i][1]
                    history_trap += '<td>%s</td>' % all_traps[i][2]
                    history_trap += '<td>%s&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s</td></tr>' % (
                        all_traps[i][3], ((
                                          "<a href=\"status_snmptt.py?trap_status=history&ip_address=" + ip_address + "\">more>></a>" if len(
                                              all_traps) > 5 else "")))
            cursor.close()

            if len(all_traps) < 1:
                history_trap += '<tr ><td colspan="4"><b>Alarm does not exists.</b></td></tr>'

        else:
            # This query return the latest five entry of current alarm
            cursor = db.cursor()
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' order by ta.timestamp desc limit 7 " % ip_address
            cursor.execute(sql)
            current_alarm = cursor.fetchall()

            length = 5

            if len(current_alarm) < 5:
                length = len(current_alarm)

            current_alarm_html = '<table width="100%" border="0" cellpadding="0" cellspacing="0" class="yo-table">'
            current_alarm_html += '<tbody>\
            <tr class="yo-table-head">\
                <th class=" vertline">&nbsp;</th>\
                <th>Event Id</th>\
                <th>Event Type</th>\
                <th>Receive Date</th>\
            </tr>'
            for i in range(length):
                if i < 4:
                    current_alarm_html += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                        image_dic[current_alarm[i][0]], image_title_name[current_alarm[i][0]],
                        image_title_name[current_alarm[i][0]])
                    current_alarm_html += '<td>%s</td>' % current_alarm[i][1]
                    current_alarm_html += '<td>%s</td>' % current_alarm[i][2]
                    current_alarm_html += '<td>%s</td></tr>' % current_alarm[
                        i][3]
                else:
                    current_alarm_html += '<tr><td class="vertline"><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px;\"/></td>' % (
                        image_dic[current_alarm[i][0]], image_title_name[current_alarm[i][0]],
                        image_title_name[current_alarm[i][0]])
                    current_alarm_html += '<td>%s</td>' % current_alarm[i][1]
                    current_alarm_html += '<td>%s</td>' % current_alarm[i][2]
                    current_alarm_html += '<td>%s&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%s</td></tr>' % (
                        current_alarm[i][3], ((
                                              "<a href=\"status_snmptt.py?trap_status=history&ip_address=" + ip_address + "\">more>></a>" if len(
                                                  current_alarm) > 5 else "")))
            cursor.close()

            if len(current_alarm) < 1:
                current_alarm_html += '<tr ><td colspan="4"><b>Alarm does not exists.</b></td></tr>'

            # close database connection and cursor.
            cursor.close()
            history_trap = current_alarm_html
        db.close()
        history_trap_detail = {'success': 0, 'output': history_trap, }
        html.write(str(history_trap_detail))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()

# This function silver information of particular device for device dashboard.
# This function take one request parameter.
# This function return the device information in table form.


def odu100_device_information(h):
    """ This function take one html object as a argument and return the device information in table.
    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    last_reboot_time = ""  # default value
    host_id = ""  # default value
    device_detail = ''
    try:
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)
        last_reboot_resion = {0: 'Power cycle', 1: 'Watchdog reset', 2: 'Normal', 3:
            'Kernel crash reset', 4: 'Radio count mismatch reset', 5: 'Unknown-Soft', 6: 'Unknown reset'}
        default_node_type = {0: 'rootRU', 1: 't1TDN', 2: 't2TDN', 3: 't2TEN'}
        operation_state = {0: 'disabled', 1: 'enabled'}
        channel = {0: 'raBW5Mhz', 1: 'raBW10Mhz', 2: 'raBW20Mhz',
                   3: 'raBW5	0Mhz'}
        # get the host id correspondence.

        sql = "SELECT host_id FROM hosts WHERE ip_address='%s'" % ip_address
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            if len(result) > 0:
                host_id = result[0]
                #----- This Query provide the some device informaion ------#
                sql = "SELECT fm.frequency,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,cb.opState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM\
                        hosts as hs \
                        LEFT JOIN odu100_raChannelListTable as fm ON fm.host_id = hs.host_id\
                        LEFT JOIN odu100_peerNodeStatusTable as ts ON ts.host_id = hs.host_id\
                        LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                        LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                        LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                        LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                        where hs.host_id='%s' limit 1" % host_id
                #--- execute the query ------#
            cursor.execute(sql)
            result = cursor.fetchone()
            sel_query = "SELECT count(*) FROM  odu100_peerNodeStatusTable WHERE  linkStatus=2 and tunnelStatus=1 and  host_id=='%s' group by timeSlotIndex limit 1" % host_id
            cursor.execute(sql)
            slave = cursor.fetchall()
            if len(slave) > 1:
                no_of_slave = '--' if slave[0][
                                          0] == None or slave[0][0] == '' else slave[0][0]
            else:
                no_of_slave = '--'

            #---- Query for get the last reboot time of particular device ------#
            sql = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address

            #----- store the last reboot time value in variable ----- #
            if cursor.execute(sql):
                reboot_time = cursor.fetchall()
                if str(reboot_time).strip() != None or str(reboot_time).strip() != 'undefined' or str(
                        reboot_time).strip() != "":
                    if len(reboot_time) > 0:
                        last_reboot_time = reboot_time[0][0]
                #-- Create the table. ---- #
            if result is not None:
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                ' + str(
                    '--' if result[len(result) - 1] == None or result[len(result) - 1] == ""  else result[
                        len(result) - 1]) + '\
                            </th>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Host Details\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Frequency\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[0] == None or result[0] == ""  else result[0]) + '</td>\
                            <td class="cell-label">\
                                Slaves\
                            </td>\
                            <td class="cell-info">' + str(no_of_slave) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Active Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[2] == None or result[2] == ""  else result[2]) + '</td>\
                            <td class="cell-label">\
                                Hardware Version\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[3] == None or result[3] == ""  else result[3]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Reason\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[4] == None or result[4] == ""  else last_reboot_resion[result[4]]) + '</td>\
                            <td class="cell-label">\
                                Channel\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[5] == None or result[5] == "" else channel[int(str(result[5]))
                    ]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Operation state\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[6] == None or result[6] == ""  else operation_state[result[6]]) + '</td>\
                            <td class="cell-label">\
                                Node Type\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[7] == None or result[7] == ""  else default_node_type[result[7]]) + '</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if result[8] == None or result[8] == ""  else result[8]) + '</td>\
                            <td class="cell-label">\
                                Last Reboot Time\
                            </td>\
                            <td class="cell-info">' + str(
                    '--' if last_reboot_time == None or last_reboot_time == ""  else last_reboot_time) + '</td>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Graphs\
                            </th>\
                            </tr>\
                        <tbody></table>'

            else:
                device_detail = '<table class="tt-table" cellspacing="0" cellpadding="0" width="100%">'
                device_detail += '<tbody>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Host Details\
                            </th>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Frequency\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Slaves\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Active Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Hardware Version\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Reason\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Channel\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Operation state\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Node Type\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                MAC Address\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <td class="cell-label">\
                                Last Reboot Time\
                            </td>\
                            <td class="cell-info">--</td>\
                            </tr>\
                            <tr>\
                            <th class="cell-title" colspan="4">\
                                Graphs\
                            </th>\
                            </tr>\
                        <tbody></table>'

        cursor.close()
        db.close()

        output_dict = {'success': 0, 'device_table': device_detail}
        html.write(str(output_dict))

    #---- pass the json -- #
    #---- Exception is  raise than pass exception in json format ---#

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


def add_date_time_on_slide_odu100(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        # calling the function
        refresh_time, total_count = get_dashboard_data()
        # start datetime and end datetime variable
        now = datetime.now()
        odu_end_date = now.strftime("%d/%m/%Y")
        odu_end_time = now.strftime("%H:%M")
        now = now + timedelta(minutes=-int(total_count))
        odu_start_date = now.strftime("%d/%m/%Y")
        odu_start_time = now.strftime("%H:%M")
        output_dict = {
            'success': 0, 'end_date': odu_end_date, 'end_time': odu_end_time,
            'start_date': odu_start_date, 'start_time': odu_start_time}
        html.write(str(output_dict))
    except Exception as e:
        output_dict = {'success': 1}
        html.write(str(output_dict))


    ###########################################################################################################################
    #--- ODU100 REPORT GENERATING START ---#

###########################################################################################################################
# ODU report generator function
def odu100_device_report(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    result1 = ''
    ip_address = html.var('ip_address')  # take ip_address from js side
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    select_option = html.var('select_option')
    limitFlag = html.var("limitFlag")
    refresh_time = 5  # defasult time

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

        start_time = datetime.strptime(
            odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
        end_time = datetime.strptime(
            odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
        total_days = ((start_time - end_time).days)
        if int(select_option) == 1:
            total_days = 1
        elif int(select_option) == 2:
            total_days = 2
        elif int(select_option) == 3:
            total_days = 3
        elif int(select_option) == 4:
            total_days = 7
            # create the database connection and check the connection created or
        # not
        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)

        styleSheet = getSampleStyleSheet()
        odu100_report = []
        MARGIN_SIZE = 14 * mm
        PAGE_SIZE = A4
        nms_instance = __file__.split("/")[3]
        pdfdoc = '/omd/sites/%s/share/check_mk/web/htdocs/report/odutable.pdf' % nms_instance
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
        im = Image("/omd/sites/%s/share/check_mk/web/htdocs/images/new/logo.png" %
                   nms_instance, width=1.5 * inch, height=.5 * inch)
        im.hAlign = 'LEFT'
        odu100_report.append(im)
        odu100_report.append(Spacer(1, 1))

        data = []
        data.append(
            ['UBRe  ' + str(ip_address), str(start_time) + '--' + str(end_time)])
        t = Table(data, [3.5 * inch, 4 * inch])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (5, 1), 1, (0.7, 0.7, 0.7)),
            ('TEXTCOLOR', (0, 0), (0, 0), (0.11, 0.11, 0.11)),
            ('TEXTCOLOR', (1, 0), (1, 0), (0.65, 0.65, 0.65)),
            ('FONT', (0, 0), (1, 0), 'Helvetica', 14),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
        odu100_report.append(t)
        odu100_report.append(Spacer(11, 11))

        ########################################### ODU Device Information ####
        odu100_report.append(Spacer(21, 21))
        result1 = ''
        # create the cursor
        cursor = db.cursor()
        # get the host id correspondence.
        sql = "SELECT host_id FROM hosts WHERE ip_address='%s'" % ip_address
        cursor.execute(sql)
        result = cursor.fetchone()
        if len(result) > 0:
            host_id = result[0]
            #----- This Query provide the some device informaion ------#
            sql = "SELECT fm.frequency,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,cb.opState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM\
                        hosts as hs \
                        LEFT JOIN odu100_raChannelListTable as fm ON fm.host_id = hs.host_id\
                        LEFT JOIN odu100_peerNodeStatusTable as ts ON ts.host_id = hs.host_id\
                        LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                        LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                        LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                        LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                        where hs.host_id='%s'" % host_id
            #--- execute the query ------#
            cursor.execute(sql)
            result = cursor.fetchall()
            sel_query = "SELECT count(*) FROM  odu100_peerNodeStatusTable WHERE  linkStatus=2 and tunnelStatus=1 and  host_id=='%s' group by timeSlotIndex limit 1" % host_id
            cursor.execute(sql)
            slave = cursor.fetchall()
            if len(slave) > 1:
                no_of_slave = '--' if slave[0][
                                          0] == None or slave[0][0] == '' else slave[0][0]
            else:
                no_of_slave = '--'

            table_output = device_information_function(
                result, 'ODU Device Information', no_of_slave)

        #---- Query for get the last reboot time of particular device ------#
        sql = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address

        #----- store the last reboot time value in variable ----- #
        if cursor.execute(sql):
            reboot_time = cursor.fetchall()
            if str(reboot_time).strip() != None or str(reboot_time).strip() != 'undefined' or str(
                    reboot_time).strip() != "":
                if len(reboot_time) > 0:
                    table_output.append(
                        ['Last Reboot Time', str(reboot_time[0][0])])
            # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'UBRe Device Information', '', ''])
        t = Table(data1, [.021 * inch, 1.8 * inch, 2.95 * inch, 2.6 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)

        data = table_output
        t = Table(data, [3.55 * inch, 3.55 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (1, 0), 'Helvetica', 9),
                               ('FONT', (0, 1), (
                                   1, int(
                                       len(
                                           table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (1, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (5, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (1, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        ##################################### Error Graph Table Report#########
        odu100_report.append(Spacer(31, 31))

        cursor = db.cursor()
        result1 = ''
        if int(select_option) == 0:
            sel_query = "select IFNULL((odu.rxCrcErrors),0),IFNULL((odu.rxPhyError),0),odu.timestamp from  odu100_raTddMacStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp <='%s' AND odu.timestamp >= '%s' order by odu.timestamp desc" % (
                ip_address, end_time, start_time)
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query += limit_data

        else:
            sel_query = "select IFNULL((odu.rxCrcErrors),0),IFNULL((odu.rxPhyError),0),odu.timestamp from  odu100_raTddMacStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s order by odu.timestamp desc" % (
                ip_address, total_days)
        cursor.execute(sel_query)
        result1 = cursor.fetchall()
        table_output = table_list_creation(
            result1, 'CRC/PHY ERROR', 'Crc Error(error count)',
            'Phy Error(error count)', 'Time(HH:MM:SS)', )
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'CRC/PHY ERROR', '', ''])
        t = Table(data1, [.021 * inch, 1.43 * inch, 2.95 * inch, 2.57 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)
        data = table_output
        t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (2, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (2, int(len(
                                   table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (2, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (5, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (2, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        ##################################### Sync Lost Graph Table Report#####
        odu100_report.append(Spacer(31, 31))

        cursor = db.cursor()
        result1 = ''
        if int(select_option) == 0:
            sel_query = "select IFNULL((odu.syncLostCounter),0),odu.timestamp from  odu100_synchStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' order by odu.timestamp desc" % (
                ip_address, start_time, end_time)

            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query += limit_data

        else:
            sel_query = "select IFNULL((odu.syncLostCounter),0),odu.timestamp from  odu100_synchStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s order by odu.timestamp desc" % (
            ip_address, total_days)
        cursor.execute(sel_query)
        result1 = cursor.fetchall()
        table_output = sync_table_list_creation(
            result1, 'Sync Lost', 'Sync Lost(error count)', 'Time(HH:MM:SS)', )
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'Sync Lost', '', ''])
        t = Table(data1, [.021 * inch, .85 * inch, 3.10 * inch, 3.0 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)
        data = table_output
        t = Table(data, [3.55 * inch, 3.55 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (1, 0), 'Helvetica', 9),
                               ('FONT', (0, 1), (
                                   1, int(
                                       len(
                                           table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (1, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (5, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (1, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        ##################################### Signal Strength Graph Table Repor
        odu100_report.append(Spacer(31, 31))
        status = 0
        signal_flag = 1
        cursor = db.cursor()
        signal_interface1 = []
        signal_interface2 = []
        signal_interface3 = []
        signal_interface4 = []
        signal_interface5 = []
        signal_interface6 = []
        signal_interface7 = []
        signal_interface8 = []
        signal_interface9 = []
        signal_interface10 = []
        signal_interface11 = []
        signal_interface12 = []
        signal_interface13 = []
        signal_interface14 = []
        signal_interface15 = []
        signal_interface16 = []
        time_stamp_signal1 = []

        sel_query = "SELECT default_node_type FROM get_odu16_ru_conf_table as def INNER JOIN hosts ON hosts.host_id=def.host_id WHERE hosts.ip_address='%s'" % (
        ip_address)
        cursor.execute(sel_query)
        status_result = cursor.fetchall()
        status = 0
        if len(status_result) > 0:
            status = 0 if status_result[0][0] == None else status_result[0][0]
        status_name = 'Master' if int(status) == 0 else 'Slave'

        if int(select_option) == 0:
            sel_query = "select odu.raScanIndex,(IFNULL((odu.signalStrength),0)),odu.timestamp from  odu100_raScanListTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' order by odu.timestamp desc" % (
                ip_address, start_time, end_time)
            signal_flag = 0
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 40'
            sel_query += limit_data
        else:
            sel_query = "select odu.raScanIndex,(IFNULL((odu.signalStrength),0)),odu.timestamp from  odu100_raScanListTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s order by odu.timestamp desc" % (
            ip_address, total_days)
        cursor.execute(sel_query)
        signal_strength = cursor.fetchall()
        count = 0
        flag = 0
        default_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for k in range(0, len(signal_strength) - 1):
            flag = 1
            if count == 5 and signal_flag == 0:
                break
            if signal_strength[k][1] == 1 or str(signal_strength[k][1]) == '1':
                count += 1
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
            else:
                if signal_strength[k][2] == signal_strength[k + 1][2]:
                    default_list[int(
                        signal_strength[k][0]) - 1] = int(signal_strength[k][1])
                else:
                    count += 1
                    default_list[int(
                        signal_strength[k][0]) - 1] = int(signal_strength[k][1])
                    signal_interface1.append(default_list[0])
                    signal_interface2.append(default_list[1])
                    signal_interface3.append(default_list[2])
                    signal_interface4.append(default_list[3])
                    signal_interface5.append(default_list[4])
                    signal_interface6.append(default_list[5])
                    signal_interface7.append(default_list[6])
                    signal_interface8.append(default_list[7])
                    signal_interface9.append(default_list[8])
                    signal_interface10.append(default_list[9])
                    signal_interface11.append(default_list[10])
                    signal_interface12.append(default_list[11])
                    signal_interface13.append(default_list[12])
                    signal_interface14.append(default_list[13])
                    signal_interface15.append(default_list[14])
                    signal_interface16.append(default_list[15])
                    time_stamp_signal1.append(str(
                        (signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
                    default_list = [0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if len(signal_strength) > 0 and flag == 0:
            if signal_strength[0][1] == 1 or str(signal_strength[0][1]) == '1':
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[0][2]).strftime('%d-%m-%Y %H:%M')))
            else:
                default_list[int(signal_strength[0][0]) -
                             1] = int(signal_strength[0][1])
                signal_interface1.append(default_list[0])
                signal_interface2.append(default_list[1])
                signal_interface3.append(default_list[2])
                signal_interface4.append(default_list[3])
                signal_interface5.append(default_list[4])
                signal_interface6.append(default_list[5])
                signal_interface7.append(default_list[6])
                signal_interface8.append(default_list[7])
                signal_interface9.append(default_list[8])
                signal_interface10.append(default_list[9])
                signal_interface11.append(default_list[10])
                signal_interface12.append(default_list[11])
                signal_interface13.append(default_list[12])
                signal_interface14.append(default_list[13])
                signal_interface15.append(default_list[14])
                signal_interface16.append(default_list[15])
                time_stamp_signal1.append(
                    str((signal_strength[0][2]).strftime('%d-%m-%Y %H:%M')))
        if flag == 1 and len(signal_strength) > 0:
            if signal_strength[k][1] == 1 or str(signal_strength[k][1]) == '1':
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
            else:
                default_list[int(signal_strength[k][0]) -
                             1] = int(signal_strength[k][1])
                signal_interface1.append(default_list[0])
                signal_interface2.append(default_list[1])
                signal_interface3.append(default_list[2])
                signal_interface4.append(default_list[3])
                signal_interface5.append(default_list[4])
                signal_interface6.append(default_list[5])
                signal_interface7.append(default_list[6])
                signal_interface8.append(default_list[7])
                signal_interface9.append(default_list[8])
                signal_interface10.append(default_list[9])
                signal_interface11.append(default_list[10])
                signal_interface12.append(default_list[11])
                signal_interface13.append(default_list[12])
                signal_interface14.append(default_list[13])
                signal_interface15.append(default_list[14])
                signal_interface16.append(default_list[15])
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
        if status_name == 'Master':
            data1 = []
            data1.append(['', 'RSSI', '', ''])
            t = Table(
                data1, [.021 * inch, .51 * inch, 3.87 * inch, 2.57 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            odu100_report.append(t)
            table_output = []
            table_output.append(['Time(HH:MM)', 'peer1', 'peer2', 'peer3',
                                 'peer4', 'peer5', 'peer6', 'peer7', 'peer8'])
            k = 0
            for time_field in time_stamp_signal1:
                table_output.append([str(time_field), str(signal_interface1[k]), str(
                    signal_interface2[k]), str(signal_interface3[k]), str(signal_interface4[k]),
                                     str(signal_interface5[k]), str(signal_interface6[k]), str(signal_interface7[k]),
                                     str(signal_interface8[k])])
                k = k + 1
            t = Table(
                table_output, [1.5 * inch, .7 * inch, .7 * inch, .7 * inch,
                               .7 * inch, .7 * inch, .7 * inch, .7 * inch, .7 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (8, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (8,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 8, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (9, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (9, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (8, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                             ('BACKGROUND', (1, i -
                                                1), (8, i - 1), (0.9, 0.9, 0.9))
                            ]))
            odu100_report.append(t)
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
            odu100_report.append(t)
            odu100_report.append(Spacer(31, 31))

            # PDF for peer9 to peer16
            data1 = []
            data1.append(['', 'RSSI', '', ''])
            t = Table(
                data1, [.021 * inch, .51 * inch, 3.87 * inch, 2.57 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            odu100_report.append(t)
            table_output = []
            table_output.append(['Time(HH:MM)', 'peer9', 'peer10', 'peer11',
                                 'peer12', 'peer13', 'peer14', 'peer15', 'peer16'])
            k = 0
            for time_field in time_stamp_signal1:
                table_output.append(
                    [str(time_field), str(signal_interface9[k]), str(signal_interface10[k]), str(signal_interface11[k]),
                     str(signal_interface12[k]), str(signal_interface13[k]
                    ), str(signal_interface14[k]), str(signal_interface15[k]), str(signal_interface16[k])])
                k = k + 1
            t = Table(
                table_output, [1.5 * inch, .7 * inch, .7 * inch, .7 * inch,
                               .7 * inch, .7 * inch, .7 * inch, .7 * inch, .7 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (8, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (8,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 8, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (9, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (9, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (8, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                             ('BACKGROUND', (1, i -
                                                1), (8, i - 1), (0.9, 0.9, 0.9))
                            ]))
            odu100_report.append(t)
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
            odu100_report.append(t)
        else:
            data1 = []
            data1.append(['', 'RSSI', '', ''])
            t = Table(
                data1, [.021 * inch, .51 * inch, 3.87 * inch, 2.57 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            odu100_report.append(t)
            table_output = []
            table_output.append(['Time(HH:MM)', 'peer1'])
            k = 0
            for time_field in time_stamp_signal1:
                table_output.append(
                    [str(time_field), str(signal_interface1[k])])
                k = k + 1
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
            odu100_report.append(t)
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
            odu100_report.append(t)

        #######################################################################
        ########################################### ODU Latest 5 Alams ########
        odu100_report.append(Spacer(31, 31))

        result1 = ''
        # create the cursor
        cursor = db.cursor()
        trap_days = ((end_time - start_time).days)
        if int(select_option) == 0:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND ta.timestamp<='%s' order by ta.timestamp" % (
                ip_address, start_time, end_time)

        else:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp" % (
            ip_address, trap_days)
        cursor.execute(sql)
        result1 = cursor.fetchall()
        table_output = table_list_trap(result1, 'Lateat 5 Alarms')
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'Alarms Information', '', ''])
        t = Table(data1, [.021 * inch, 1.50 * inch, 3.08 * inch, 2.37 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)

        data = table_output
        t = Table(data, [inch, inch, 2.55 * inch, 2.55 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (3, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (3, int(len(
                                   table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (3, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (3, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (3, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (3, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (3, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        ########################################### ODU Latest 5 Traps ########
        odu100_report.append(Spacer(31, 31))
        result1 = ''
        # create the cursor
        cursor = db.cursor()
        if int(select_option) == 0:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND  ta.timestamp<='%s' order by ta.timestamp" % (
                ip_address, start_time, end_time)
        else:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp " % (
                ip_address, trap_days)
        cursor.execute(sql)
        result1 = cursor.fetchall()
        table_output = table_list_trap(result1, 'Lateat 5 Traps')
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'Events Information', '', ''])
        t = Table(data1, [.021 * inch, 1.50 * inch, 3.08 * inch, 2.37 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)

        data = table_output
        t = Table(data, [inch, inch, 2.55 * inch, 2.55 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (3, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (3, int(len(
                                   table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (3, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (3, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (3, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (3, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (3, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        ########################################### ODU Trap Information ######
        odu100_report.append(Spacer(31, 31))
        # create the cursor
        cursor = db.cursor()
        days = (total_days if int(total_days) > 5 else 5)
        cursor.callproc("trap_graph", (days, ip_address))
        result1 = cursor.fetchall()
        table_output = table_list_alarm(
            result1, 'Last 10 Days Events Information')
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'Events Statistics', '', ''])
        t = Table(data1, [.021 * inch, 1.50 * inch, 2.44 * inch, 2.95 * inch])

        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)

        data = table_output
        t = Table(data, [1.45 * 1.1 * inch, 1.1 * inch, 1.1 * inch, 1.1 *
                                                                    inch, 1.1 * inch, 1.1 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (5, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (5, int(len(
                                   table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (5, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (5, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (5, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (5, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (5, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        ########################################### ODU INTERFACE #############
        nw_interface = [
            'NETWORK BANDWIDTH RATE(eth0)', 'NETWORK BANDWIDTH RATE(eth1)']
        interface_index = 1
        for interface in nw_interface:
            odu100_report.append(Spacer(31, 31))
            cursor = db.cursor()
            result1 = ''
            # prepare SQL query to get total number of access points in this system
            # cursor.callproc("odu100_network_interface",(start_time,end_time,refresh_time,interface_index,ip_address))
            # result1=cursor.fetchall()
            if int(select_option) == 0:
                sel_query = "select (odu.rxBytes),(odu.txBytes),odu.timestamp from odu100_nwInterfaceStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where  h.ip_address='%s' AND  odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.nwStatsIndex = '%s' order by timestamp desc" % (
                    ip_address, start_time, end_time, interface_index)
                if int(limitFlag) == 0:
                    limit_data = ''
                else:
                    limit_data = ' limit 16'
                sel_query += limit_data
            else:
                sel_query = "select (odu.rxBytes),(odu.txBytes),odu.timestamp from odu100_nwInterfaceStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id where  h.ip_address='%s' AND  date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s and odu.nwStatsIndex = '%s' order by timestamp desc" % (
                    ip_address, total_days, interface_index)
            cursor.execute(sel_query)
            result1 = cursor.fetchall()
            table_output = nw_table_list_creation(
                result1, interface, 'Receving Bytes(Rx)',
                'Transmitting Bytes(Tx)', 'Time(HH:MM:SS)', )
            # close the database and cursor connection.
            cursor.close()

            data1 = []
            data1.append(['', interface, '', ''])
            t = Table(
                data1, [.021 * inch, 2.75 * inch, 2.12 * inch, 2.12 * inch])
            t.setStyle(TableStyle([('BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), (
                'FONT', (0, 0), (1, 0), 'Helvetica', 11), ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
            odu100_report.append(t)

            data = table_output
            t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
            t.setStyle(
                TableStyle([('FONT', (0, 0), (2, 0), 'Helvetica-Bold', 10),
                            ('FONT', (0, 1), (2,
                                              int(
                                                  len(
                                                      table_output)) - 1), 'Helvetica', 9),
                            ('ALIGN', (1,
                                       0), (
                                 2, int(
                                     len(table_output)) - 1), 'CENTER'),
                            ('BACKGROUND',
                             (0, 0), (2, 0), (0.9, 0.9, 0.9)),
                            ('LINEABOVE',
                             (0, 0), (2, 0), 1.21, (0.35, 0.35, 0.35)),
                            ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

            for i in range(1, len(table_output)):
                if i % 2 == 1:
                    t.setStyle(
                        TableStyle(
                            [(
                                 'BACKGROUND', (1, i), (2, i), (0.95, 0.95, 0.95)),
                             ('BACKGROUND', (0, i - 1),
                              (0, i - 1), (0.98, 0.98, 0.98)),
                            ]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), (0.9, 0.9, 0.9))
                    ]))

            t.setStyle(
                TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
            odu100_report.append(t)
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
            odu100_report.append(t)
            interface_index += 1
            #######################################################################

        # close the first database connection
        db.close()

        ########################################### ODU OUTAGE report generatio
        odu100_report.append(Spacer(31, 31))
        # create the cursor and database connection
        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)
        date_days = []  # this list store the days information with date.
        up_state = []
        # Its store the total up state of each day in percentage.
        down_state = []
        # Its store the total down state of each day in percentage.
        output_dict = {}  # its store the actual output for display in graph.\
        last_status = ''
        down_flag = 0
        up_flag = 0
        current_date = datetime.date(datetime.now())
        current_datetime = datetime.strptime(str(current_date + timedelta(
            days=-(total_days))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_datetime = datetime.strptime(
            str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        temp_date = last_datetime

        # this datetime last status calculation
        last_status_current_time = datetime.strptime(str(current_date + timedelta(
            days=-(total_days + 1))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_status_end_time = datetime.strptime(str(current_date + timedelta(
            days=-(total_days))) + " 23:59:59", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.

        sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
	    FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
	   where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
	    order by nagios_statehistory.state_time " % (current_datetime, last_datetime, ip_address)
        # Execute the query.
        cursor.execute(sql)
        result = cursor.fetchall()

        # this query get last status of device
        sel_sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
	    FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
	   where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
	    order by nagios_statehistory.state_time  desc limit 1" % (
        last_status_current_time, last_status_end_time, ip_address)
        # Execute the query.
        cursor.execute(sel_sql)
        last_state = cursor.fetchall()
        if last_state is not None:
            if len(last_state) > 0:
                last_status = last_state[0][2]
        if result is not None:
            if len(result) > 0:
                for i in range((total_days + 1)):
                    flag = 0
                    total_down_time = 0
                    total_up_time = 0
                    temp_down_time = ''
                    temp_up_time = ''
                    temp_time = ''
                    j = 0
                    for row in result:
                        if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                            flag = 1
                            if row[2] == 0:
                                if temp_up_time == '':
                                    temp_up_time = row[1]
                                    if last_status == '' and up_flag == 0:
                                        if temp_time is not '':
                                            if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                total_up_time += abs((
                                                                         row[1] - temp_time).days * 1440 + (
                                                                     row[1] - temp_time).seconds / 60)
                                                temp_up_time = row[1]
                                            else:
                                                total_down_time += abs(
                                                    (row[1] - temp_time).days * 1440 + (
                                                    row[1] - temp_time).seconds / 60)
                                                temp_down_time = row[1]
                                        up_flag = 1
                                    elif last_status is not '' and up_flag == 0:
                                        up_flag = 1
                                        if last_status == 0:
                                            total_up_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                        else:
                                            total_down_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:
                                    if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                        total_up_time += abs((
                                                                 row[1] - temp_time).days * 1440 + (
                                                             row[1] - temp_time).seconds / 60)
                                        temp_up_time = row[1]
                                    else:
                                        total_down_time += abs((row[1] - temp_time).days * 1440 + (
                                            row[1] - temp_time).seconds / 60)
                                        temp_down_time = row[1]
                            else:
                                if temp_down_time == '':
                                    temp_down_time = row[1]
                                    if last_status == '' and down_flag == 0:
                                        if temp_time is not '':
                                            if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                total_up_time += abs((
                                                                         row[1] - temp_time).days * 1440 + (
                                                                     row[1] - temp_time).seconds / 60)
                                                temp_up_time = row[1]
                                            else:
                                                total_down_time += abs(
                                                    (row[1] - temp_time).days * 1440 + (
                                                    row[1] - temp_time).seconds / 60)
                                                temp_down_time = row[1]
                                        down_flag = 1
                                    elif last_status is not '' and down_flag == 0:
                                        down_flag = 1
                                        if last_status == 0:
                                            total_up_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                        else:
                                            total_down_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:

                                    if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                        total_up_time += abs((
                                                                 row[1] - temp_time).days * 1440 + (
                                                             row[1] - temp_time).seconds / 60)
                                        temp_up_time = row[1]
                                    else:
                                        total_down_time += abs((row[1] - temp_time).days * 1440 + (
                                            row[1] - temp_time).seconds / 60)
                                        temp_down_time = row[1]

                        if j < len(result):
                            temp_time = row[1]
                        j += 1
                    if flag == 1:
                        if result[j - 1][2] == 0:
                            total_up_time = abs((result[j - 1][1] - (temp_date + timedelta(days=-i))).days *
                                                1440 + (
                            result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                        else:
                            total_down_time = abs((result[j - 1][1] - (
                                temp_date + timedelta(days=-i))).days * 1440 + (
                                                  result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                    date_days.append(
                        (temp_date + timedelta(days=-(i))).strftime("%d %b %Y"))
                    total = total_up_time + total_down_time
                    if flag == 1 and total > 0:
                        up_state.append(
                            round((total_up_time * 100) / float(total), 2))
                        down_state.append(
                            round((total_down_time * 100) / float(total), 2))
                    else:
                        up_state.append(0)
                        down_state.append(0)
            else:
                sel_sql = "SELECT  nagios_hosts.address,nagios_hoststatus.status_update_time,nagios_hoststatus.current_state\
			    FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hoststatus.host_object_id = nagios_hosts.host_object_id\
			   where nagios_hoststatus.status_update_time between '%s'  and '%s' and nagios_hosts.address='%s'\
			    order by nagios_hoststatus.status_update_time " % (current_datetime, last_datetime, ip_address)
                cursor.execute(sel_sql)
                result = cursor.fetchall()
                for i in range((total_days + 1)):
                    flag = 0
                    total_down_time = 0
                    total_up_time = 0
                    for row in result:
                        if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                            flag = 1
                            if row[2] == 0:
                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                    days=-(i + 1)))).days * 1440 + (
                                                    row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                            else:
                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                    days=-(i + 1)))).days * 1440 + (
                                                      row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                    date_days.append(
                        (temp_date + timedelta(days=-(i))).strftime("%d %b %Y"))
                    total = total_up_time + total_down_time
                    if flag == 1 and total > 0:
                        up_state.append(
                            round((total_up_time * 100) / float(total), 2))
                        down_state.append(
                            round((total_down_time * 100) / float(total), 2))
                    else:
                        up_state.append(0)
                        down_state.append(0)
            # close the database and cursor connection.
        cursor.close()
        db.close()
        date_days.reverse()
        up_state.reverse()
        down_state.reverse()

        data1 = []
        data1.append(['', 'Outage Status', '', ''])
        t = Table(data1, [.021 * inch, 1.15 * inch, 2.94 * inch, 2.87 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_report.append(t)

        table_output = outage_graph_generation(date_days, down_state, up_state)
        data = table_output
        t = Table(data, [2.7 * inch, 2.2 * inch, 2.2 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (2, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (2, int(len(
                                   table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (2, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (2, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (2, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (8, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))

        for i in range(1, len(table_output)):
            if i % 2 == 1:
                t.setStyle(
                    TableStyle(
                        [('BACKGROUND', (1, i), (2, i), (0.95, 0.95, 0.95)),
                         ('BACKGROUND', (0, i -
                                            1), (0, i - 1), (0.98, 0.98, 0.98)),
                        ]))
            else:
                t.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), (0.9, 0.9, 0.9))
                ]))

        t.setStyle(
            TableStyle([('BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9))]))
        odu100_report.append(t)
        data1 = []
        if len(table_output) > 1:
            data1.append(['1-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        else:
            data1.append(['0-' + str(
                len(table_output) - 1) + ' of ' + str(len(table_output) - 1)])
        t = Table(data1, [7.10 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.9, 0.9, 0.9)), ('GRID', (0, 0),
                                                                      (5, 0), 0.31, (0.75, 0.75, 0.75)),
                 ('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
        odu100_report.append(t)
        #######################################################################

        pdf_doc.build(odu100_report)
        output_dict = {'success': 0, 'output': 'pdf downloaded'}
        html.write(str(output_dict))
    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


def nw_table_list_creation(result, table_name, first_header, second_header, time):
    """

    @param result:
    @param table_name:
    @param first_header:
    @param second_header:
    @param time:
    @return:
    """
    output = []
    first_h = [time, first_header, second_header]
    output.append(first_h)
    if result is not None:
        for i in range(len(result) - 1):
            rx_byte = ((int(result[i][0]) - int(result[i + 1][0])))
            tx_byte = ((int(result[i][1]) - int(result[i + 1][1])))
            temp_list = []
            temp_list = [result[i][2].strftime('%d-%m-%Y %H:%M'), (
                0 if rx_byte <= 0 else rx_byte), (0 if tx_byte <= 0 else tx_byte)]
            output.append(temp_list)
    return output


def sync_table_list_creation(result, table_name, first_header, time):
    """

    @param result:
    @param table_name:
    @param first_header:
    @param time:
    @return:
    """
    output = []
    first_h = [time, first_header]
    output.append(first_h)
    for i in range(0, len(result) - 1):
        temp_list = []
        temp_list = [result[i][1].strftime('%d-%m-%Y %H:%M'), 0 if (
                                                                       int(result[i][0]) - int(
                                                                           result[i + 1][0])) < 0 else (
        int(result[i][0]) - int(result[i + 1][0]))]
        output.append(temp_list)
    return output


def table_list_creation(result, table_name, first_header, second_header, time):
    """

    @param result:
    @param table_name:
    @param first_header:
    @param second_header:
    @param time:
    @return:
    """
    output = []
    first_h = [time, first_header, second_header]
    output.append(first_h)
    for i in range(0, len(result) - 1):
        temp_list = []
        temp_list = [result[i][2].strftime('%d-%m-%Y %H:%M'), 0 if (int(
            result[i][0]) - int(result[i + 1][0])) < 0 else (int(result[i][0]) - int(result[i + 1][0])),
                     0 if (int(result[i][1]) - int(result[i + 1][1])) < 0 else (
                     int(result[i][1]) - int(result[i + 1][1]))]
        output.append(temp_list)
    return output


def table_list_alarm(result, table_name):
    """

    @param result:
    @param table_name:
    @return:
    """
    output = []
    result = sorted(result, key=itemgetter(6))
    first_h = ['Date', 'Normal', 'Informational', 'Minor', 'Major', 'Critical']
    output.append(first_h)
    for i in range(0, len(result)):
        temp_list = []
        temp_list = [result[i][6].strftime(
            '%x'), result[i][1], result[i][2], result[i][3], result[i][4], result[i][5]]
        output.append(temp_list)
    return output


def table_list_trap(result, table_name):
    """

    @param result:
    @param table_name:
    @return:
    """
    length = 5
    output = []
    first_h = ['Severity', 'Event Id', 'Event State', 'Receive Date']
    output.append(first_h)
    result = sorted(result, key=itemgetter(3))
    if len(result) < 5:
        length = len(result)
    for i in range(0, length):
        temp_list = []
        temp_list = [result[i][0], result[i][1], result[i][2], datetime.strptime(str(
            result[i][3]), '%a %b %d %H:%M:%S %Y').strftime('%x')]
        output.append(temp_list)
    return output


def device_information_function(result, table_name, slave):
    """

    @param result:
    @param table_name:
    @param slave:
    @return:
    """
    last_reboot_resion = {
        0: 'Power cycle', 1: 'Watchdog reset', 2: 'Normal', 3: 'Kernel crash reset',
        4: 'Radio count mismatch reset', 5: 'Unknown-Soft', 6: 'Unknown reset'}
    default_node_type = {0: 'rootRU', 1: 't1TDN', 2: 't2TDN', 3: 't2TEN'}
    operation_state = {0: 'disabled', 1: 'enabled'}
    channel = {0: 'raBW5Mhz', 1: 'raBW10Mhz', 2: 'raBW20Mhz', 3:
        'raBW50Mhz', 3: 'raBW100Mhz'}
    device_field = [
        'Frequency', 'Slaves', 'Active Version', 'Hardware Version', 'Interfaces',
        'Last Reboot Reason', 'Channel', 'Operation state', 'Node Type', 'MAC Address', 'Last Reboot Time']
    output = []
    output.append([device_field[0], str('--' if result[0][0]
                                                == None or result[0][0] == "" else result[0][0])])
    output.append([device_field[1], str(slave)])
    output.append([device_field[2], str('--' if result[0][2]
                                                == None or result[0][2] == "" else result[0][2])])
    output.append([device_field[3], str('--' if result[0][3]
                                                == None or result[0][3] == "" else result[0][3])])
    output.append([device_field[5], str('--' if result[0][4] == None or result[0][4]
                                                == "" else last_reboot_resion[result[0][4]])])
    output.append([device_field[6], str('--' if result[0][5]
                                                == None or result[0][5] == "" else channel[result[0][5]])])
    output.append([device_field[7], str('--' if result[0][6] == None or result[0][6]
                                                == "" else operation_state[result[0][6]])])
    output.append([device_field[8], str('--' if result[0][7] == None or result[0][7]
                                                == "" else default_node_type[result[0][7]])])
    output.append([device_field[9], str('--' if result[0][8]
                                                == None or result[0][8] == "" else result[0][8])])
    return output


def outage_graph_generation(date_time, down_state, up_state):
    """

    @param date_time:
    @param down_state:
    @param up_state:
    @return:
    """
    output = []
    output.append(['Date', 'up_state(%)', 'down_state(%)'])
    i = 0
    for date_time1 in date_time:
        output.append(
            [date_time1, round(up_state[i], 2), round(down_state[i], 2)])
        i += 1
    return output

############################################ ODU REPORT GENERATING END ###

######################################## ODU excel report creating start #


def odu100_excel_report_genrating(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    result1 = ''
    ip_address = html.var('ip_address')  # take ip_address from js side
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    select_option = html.var('select_option')
    limitFlag = html.var("limitFlag")
    if ip_address == '' or ip_address == None or ip_address == 'undefined' or str(
            ip_address) == 'None':    # if ip_address not received so excel not created
        raise SelfException(
            'This UBR devices not exists so excel report can not be generated.')  # Check msg
    try:
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        # create the start datetime and end datatime
        start_time = datetime.strptime(
            odu_start_date + ' ' + odu_start_time, "%d/%m/%Y %H:%M")
        end_time = datetime.strptime(
            odu_end_date + ' ' + odu_end_time, "%d/%m/%Y %H:%M")
        if start_time > datetime.now():
            start_time = datetime.now()

        # calculating the total days between start and end date.
        total_days = ((end_time - start_time).days)
        if select_option:
            if int(select_option) == 4:
                total_days = 7
            else:
                total_days = int(select_option)

        # create the mysql connection
        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)

        # Import the modules for excel generating.
        import xlwt

        # create the excel file
        xls_book = xlwt.Workbook(encoding='ascii')

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

        # we get the host inforamtion.
        sel_query = "SELECT device_type.device_name,hosts.host_alias FROM hosts INNER JOIN device_type ON hosts.device_type_id=device_type.device_type_id WHERE hosts.ip_address='%s'" % (
            ip_address)
        cursor.execute(sel_query)
        host_result = cursor.fetchall()
        device_type = ''
        device_name = ''
        if len(host_result) > 0:
            device_type = ('--' if host_result[0][0] == '' or host_result[
                0][0] == None else host_result[0][0])
            device_name = ('--' if host_result[0][1] == '' or host_result[
                0][1] == None else host_result[0][1])
            # end the host information fucntion

        # Device Inforamtion Excel Creation start here.
        sql = "SELECT host_id FROM hosts WHERE ip_address='%s'" % ip_address
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            host_id = result[0][0]
            #----- This Query provide the some device informaion ------#
            sql = "SELECT fm.frequency,ts.peerNodeStatusNumSlaves,sw.activeVersion ,hw.hwVersion,lrb.lastRebootReason,cb.channelBandwidth ,cb.opState ,cb.defaultNodeType,hs.mac_address,hs.ip_address FROM\
                        hosts as hs \
                        LEFT JOIN odu100_raChannelListTable as fm ON fm.host_id = hs.host_id\
                        LEFT JOIN odu100_peerNodeStatusTable as ts ON ts.host_id = hs.host_id\
                        LEFT JOIN  odu100_swStatusTable as sw ON sw.host_id=hs.host_id \
                        LEFT JOIN odu100_hwDescTable as hw ON hw.host_id=hs.host_id  \
                        LEFT JOIN  odu100_ruStatusTable as lrb ON lrb.host_id=hs.host_id\
                        LEFT JOIN odu100_ruConfTable as cb ON cb.config_profile_id = hs.config_profile_id\
                        where hs.host_id='%s'" % host_id
            #--- execute the query ------#
            cursor.execute(sql)
            result1 = cursor.fetchall()
            sel_query = "SELECT count(*) FROM  odu100_peerNodeStatusTable WHERE  linkStatus=2 and tunnelStatus=1 and  host_id=='%s' group by timeSlotIndex limit 1" % host_id
            cursor.execute(sql)
            slave = cursor.fetchall()
            if len(slave) > 1:
                no_of_slave = '--' if slave[0][
                                          0] == None or slave[0][0] == '' else slave[0][0]
            else:
                no_of_slave = '--'
            table_output = device_information_function(
                result1, 'ODU Device Information', no_of_slave)
            #---- Query for get the last reboot time of particular device ------#
        sql = "SELECT trap_receive_date from trap_alarms where trap_event_type = 'NODE_UP' and agent_id='%s' order by timestamp desc limit 1" % ip_address

        #----- store the last reboot time value in variable ----- #
        cursor.execute(sql)
        reboot_time = cursor.fetchall()
        if len(reboot_time) > 0:
            table_output.append(['Last Reboot Time', str(reboot_time[0][0])])
        else:
            table_output.append(['Last Reboot Time', '--'])

        xls_sheet = xls_book.add_sheet(
            'device_information', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 2, "UBRe Device Information", style)
        xls_sheet.write_merge(1, 1, 0, 2, str(device_type) + '       ' + str(
            device_name) + '         ' + str(ip_address), style)
        xls_sheet.write_merge(2, 2, 0, 2, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Element', 'Element Values']
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

        # Device Inforamtion Excel Creation ending.

        # CRC PHY Excel Creation start here.
        if int(select_option) == 0:
            sel_query = "select IFNULL((odu.rxCrcErrors),0),IFNULL((odu.rxPhyError),0),odu.timestamp from  odu100_raTddMacStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp <='%s' AND odu.timestamp >= '%s' order by odu.timestamp desc" % (
                ip_address, end_time, start_time)
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query += limit_data

        else:
            sel_query = "select IFNULL((odu.rxCrcErrors),0),IFNULL((odu.rxPhyError),0),odu.timestamp from  odu100_raTddMacStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s order by odu.timestamp desc" % (
                ip_address, total_days)
        cursor.execute(sel_query)
        crc_result = cursor.fetchall()
        crc_list = []
        for i in range(0, len(crc_result) - 1):
            temp_list = []
            temp_list = [crc_result[i][2].strftime('%d-%m-%Y %H:%M'), 0 if (int(crc_result[i][0]) - int(
                crc_result[i + 1][0])) < 0 else (int(crc_result[i][0]) - int(crc_result[i + 1][0])),
                         0 if (int(crc_result[i][1]) - int(crc_result[i + 1][1])) < 0 else (
                         int(crc_result[i][1]) - int(crc_result[i + 1][1]))]
            crc_list.append(temp_list)

        crc_list = sorted(crc_list, key=itemgetter(0))
        xls_sheet = xls_book.add_sheet('Crc_Phy_Error', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 2, "Crc Phy Error Information", style)
        xls_sheet.write(1, 0, device_type, style)
        xls_sheet.write(1, 1, device_name, style)
        xls_sheet.write(1, 2, ip_address, style)
        xls_sheet.write_merge(2, 2, 0, 2, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Time', 'Crc Error', 'Phy Error']
        xls_sheet.set_panes_frozen(
            True)  # frozen headings instead of split panes
        xls_sheet.set_horz_split_pos(
            i)  # in general, freeze after last heading row
        xls_sheet.set_remove_splits(
            True)  # if user does unfreeze, don't leave a split there
        for colx, value in enumerate(headings):
            xls_sheet.write(i - 1, colx, value, heading_xf)
        for k in range(len(crc_list) - 1):
            for j in range(len(crc_list[k])):
                width = 5000
                xls_sheet.write(i, j, str(crc_list[k][j]), style1)
                xls_sheet.col(j).width = width
            i = i + 1
            # CRC PHY Excel ending here.

        # Sync Lost Excel Creation start here.
        if int(select_option) == 0:
            sel_query = "select IFNULL((odu.syncLostCounter),0),odu.timestamp from  odu100_synchStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' order by odu.timestamp desc" % (
                ip_address, start_time, end_time)

            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 16'
            sel_query += limit_data

        else:
            sel_query = "select IFNULL((odu.syncLostCounter),0),odu.timestamp from  odu100_synchStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s order by odu.timestamp desc" % (
            ip_address, total_days)
        cursor.execute(sel_query)
        sync_result = cursor.fetchall()

        sync_list = []
        for i in range(0, len(sync_result) - 1):
            temp_list = []
            temp_list = [sync_result[i][1].strftime('%d-%m-%Y %H:%M'), 0 if (int(sync_result[i][0]) - int(
                sync_result[i + 1][0])) < 0 else (int(sync_result[i][0]) - int(sync_result[i + 1][0]))]
            sync_list.append(temp_list)

        sync_list = sorted(sync_list, key=itemgetter(0))
        xls_sheet = xls_book.add_sheet('Sync_lost', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 2, "Sync Lost Information", style)
        xls_sheet.write(1, 0, device_type, style)
        xls_sheet.write(1, 1, device_name, style)
        xls_sheet.write(1, 2, ip_address, style)
        xls_sheet.write_merge(2, 2, 0, 2, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Time', 'Sync Lost']
        xls_sheet.set_panes_frozen(
            True)  # frozen headings instead of split panes
        xls_sheet.set_horz_split_pos(
            i)  # in general, freeze after last heading row
        xls_sheet.set_remove_splits(
            True)  # if user does unfreeze, don't leave a split there
        for colx, value in enumerate(headings):
            xls_sheet.write(i - 1, colx, value, heading_xf)
        for k in range(len(sync_list) - 1):
            for j in range(len(sync_list[k])):
                width = 5000
                xls_sheet.write(i, j, str(sync_list[k][j]), style1)
                xls_sheet.col(j).width = width
            i = i + 1
            # Sync List Excel ending here.

        # Network bandwith Excel Creation start here.
        network_bandwidth = ['eth0', 'eth1']
        for index in range(1, 3):
            if int(select_option) == 0:
                sel_query = "select (odu.rxBytes),(odu.txBytes),odu.timestamp from odu100_nwInterfaceStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where  h.ip_address='%s' AND  odu.timestamp >= '%s' AND odu.timestamp <='%s' and odu.nwStatsIndex = '%s' order by timestamp desc" % (
                    ip_address, start_time, end_time, index)
                if int(limitFlag) == 0:
                    limit_data = ''
                else:
                    limit_data = ' limit 16'
                sel_query += limit_data
            else:
                sel_query = "select (odu.rxBytes),(odu.txBytes),odu.timestamp from odu100_nwInterfaceStatisticsTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id where  h.ip_address='%s' AND  date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s and odu.nwStatsIndex = '%s' order by timestamp desc" % (
                    ip_address, total_days, index)
            cursor.execute(sel_query)
            nw_result = cursor.fetchall()

            network_list = []
            for i in range(0, len(nw_result) - 1):
                temp_list = []
                temp_list = [nw_result[i][2].strftime('%d-%m-%Y %H:%M'), 0 if (int(nw_result[i][0]) - int(
                    nw_result[i + 1][0])) < 0 else (int(nw_result[i][0]) - int(nw_result[i + 1][0])),
                             0 if (int(nw_result[i][1]) - int(nw_result[i + 1][1])) < 0 else (
                             int(nw_result[i][1]) - int(nw_result[i + 1][1]))]
                network_list.append(temp_list)

            network_list = sorted(network_list, key=itemgetter(0))
            xls_sheet = xls_book.add_sheet('network_bandwidth(%s)' % network_bandwidth[
                index - 1], cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(0, 0, 0, 2, "Network Bandwidth Information (%s)" %
                                              network_bandwidth[index - 1], style)
            xls_sheet.write(1, 0, device_type, style)
            xls_sheet.write(1, 1, device_name, style)
            xls_sheet.write(1, 2, ip_address, style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Time', 'Receving Bytes', 'Transmitting Bytes']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(network_list) - 1):
                for j in range(len(network_list[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(network_list[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1
            # Network bandwith Excel ending here.

        # Signal Strength Excel creating here.
        signal_flag = 1
        status = 0
        signal_interface1 = []
        signal_interface2 = []
        signal_interface3 = []
        signal_interface4 = []
        signal_interface5 = []
        signal_interface6 = []
        signal_interface7 = []
        signal_interface8 = []
        signal_interface9 = []
        signal_interface10 = []
        signal_interface11 = []
        signal_interface12 = []
        signal_interface13 = []
        signal_interface14 = []
        signal_interface15 = []
        signal_interface16 = []
        time_stamp_signal1 = []

        sel_query = "SELECT default_node_type FROM get_odu16_ru_conf_table as def INNER JOIN hosts ON hosts.host_id=def.host_id WHERE hosts.ip_address='%s'" % (
        ip_address)
        cursor.execute(sel_query)
        status_result = cursor.fetchall()
        status = 0
        if len(status_result) > 0:
            status = 0 if status_result[0][0] == None else status_result[0][0]
        status_name = 'Master' if int(status) == 0 else 'Slave'

        if int(select_option) == 0:
            sel_query = "select odu.raScanIndex,(IFNULL((odu.signalStrength),0)),odu.timestamp from  odu100_raScanListTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND odu.timestamp >= '%s' AND odu.timestamp <='%s' order by odu.timestamp desc" % (
                ip_address, start_time, end_time)
            signal_flag = 0
            if int(limitFlag) == 0:
                limit_data = ''
            else:
                limit_data = ' limit 40'
            sel_query += limit_data
        else:
            sel_query = "select odu.raScanIndex,(IFNULL((odu.signalStrength),0)),odu.timestamp from  odu100_raScanListTable as odu INNER JOIN hosts as h  on  odu.host_id = h.host_id  where h.ip_address='%s' AND date(odu.timestamp) <=current_date() AND date(odu.timestamp) >= current_date()-%s order by odu.timestamp desc" % (
            ip_address, total_days)
        cursor.execute(sel_query)
        signal_strength = cursor.fetchall()
        count = 0
        flag = 0
        default_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for k in range(0, len(signal_strength) - 1):
            flag = 1
            if count == 5 and signal_flag == 0:
                break
            if signal_strength[k][1] == 1 or str(signal_strength[k][1]) == '1':
                count += 1
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
            else:
                if signal_strength[k][2] == signal_strength[k + 1][2]:
                    default_list[int(
                        signal_strength[k][0]) - 1] = int(signal_strength[k][1])
                else:
                    count += 1
                    default_list[int(
                        signal_strength[k][0]) - 1] = int(signal_strength[k][1])
                    signal_interface1.append(default_list[0])
                    signal_interface2.append(default_list[1])
                    signal_interface3.append(default_list[2])
                    signal_interface4.append(default_list[3])
                    signal_interface5.append(default_list[4])
                    signal_interface6.append(default_list[5])
                    signal_interface7.append(default_list[6])
                    signal_interface8.append(default_list[7])
                    signal_interface9.append(default_list[8])
                    signal_interface10.append(default_list[9])
                    signal_interface11.append(default_list[10])
                    signal_interface12.append(default_list[11])
                    signal_interface13.append(default_list[12])
                    signal_interface14.append(default_list[13])
                    signal_interface15.append(default_list[14])
                    signal_interface16.append(default_list[15])
                    time_stamp_signal1.append(str(
                        (signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
                    default_list = [0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if len(signal_strength) > 0 and flag == 0:
            if signal_strength[0][1] == 1 or str(signal_strength[0][1]) == '1':
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[0][2]).strftime('%d-%m-%Y %H:%M')))
            else:
                default_list[int(signal_strength[0][0]) -
                             1] = int(signal_strength[0][1])
                signal_interface1.append(default_list[0])
                signal_interface2.append(default_list[1])
                signal_interface3.append(default_list[2])
                signal_interface4.append(default_list[3])
                signal_interface5.append(default_list[4])
                signal_interface6.append(default_list[5])
                signal_interface7.append(default_list[6])
                signal_interface8.append(default_list[7])
                signal_interface9.append(default_list[8])
                signal_interface10.append(default_list[9])
                signal_interface11.append(default_list[10])
                signal_interface12.append(default_list[11])
                signal_interface13.append(default_list[12])
                signal_interface14.append(default_list[13])
                signal_interface15.append(default_list[14])
                signal_interface16.append(default_list[15])
                time_stamp_signal1.append(
                    str((signal_strength[0][2]).strftime('%d-%m-%Y %H:%M')))
        if flag == 1 and len(signal_strength) > 0:
            if signal_strength[k][1] == 1 or str(signal_strength[k][1]) == '1':
                signal_interface1.append(0)
                signal_interface2.append(0)
                signal_interface3.append(0)
                signal_interface4.append(0)
                signal_interface5.append(0)
                signal_interface6.append(0)
                signal_interface7.append(0)
                signal_interface8.append(0)
                signal_interface9.append(0)
                signal_interface10.append(0)
                signal_interface11.append(0)
                signal_interface12.append(0)
                signal_interface13.append(0)
                signal_interface14.append(0)
                signal_interface15.append(0)
                signal_interface16.append(0)
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
            else:
                default_list[int(signal_strength[k][0]) -
                             1] = int(signal_strength[k][1])
                signal_interface1.append(default_list[0])
                signal_interface2.append(default_list[1])
                signal_interface3.append(default_list[2])
                signal_interface4.append(default_list[3])
                signal_interface5.append(default_list[4])
                signal_interface6.append(default_list[5])
                signal_interface7.append(default_list[6])
                signal_interface8.append(default_list[7])
                signal_interface9.append(default_list[8])
                signal_interface10.append(default_list[9])
                signal_interface11.append(default_list[10])
                signal_interface12.append(default_list[11])
                signal_interface13.append(default_list[12])
                signal_interface14.append(default_list[13])
                signal_interface15.append(default_list[14])
                signal_interface16.append(default_list[15])
                time_stamp_signal1.append(
                    str((signal_strength[k][2]).strftime('%d-%m-%Y %H:%M')))
        signal_list = []
        k = 0
        if status_name == 'Master':
            for time_field in time_stamp_signal1:
                signal_list.append(
                    [str(time_field), str(signal_interface1[k]), str(signal_interface2[k]), str(signal_interface3[k]),
                     str(signal_interface4[k]), str(signal_interface5[k]
                    ), str(signal_interface6[k]), str(signal_interface7[k]), str(signal_interface8[k])])
                k = k + 1
            signal_list = sorted(signal_list, key=itemgetter(0))
            xls_sheet = xls_book.add_sheet(
                'Signal_strength', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 16, "Signal Strength Information", style)
            xls_sheet.write_merge(1, 1, 0, 16, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 16, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = [
                'Time', 'Peer1', 'Peer2', 'Peer3', 'Peer4', 'Peer5', 'Peer6', 'Peer7',
                'Peer8', 'peer9', 'peer10', 'peer11', 'peer12', 'peer13', 'peer14', 'peer15', 'peer16']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(signal_list) - 1):
                for j in range(len(signal_list[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(signal_list[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1
        else:
            for time_field in time_stamp_signal1:
                signal_list.append(
                    [str(time_field), str(signal_interface1[k])])
                k = k + 1
            signal_list = sorted(signal_list, key=itemgetter(0))
            xls_sheet = xls_book.add_sheet(
                'Signal_strength', cell_overwrite_ok=True)
            xls_sheet.row(0).height = 521
            xls_sheet.row(1).height = 421
            xls_sheet.write_merge(
                0, 0, 0, 2, "Signal Strength Information", style)
            xls_sheet.write_merge(1, 1, 0, 2, str(device_type) + '       ' + str(
                device_name) + '         ' + str(ip_address), style)
            xls_sheet.write_merge(2, 2, 0, 2, "")
            i = 4
            heading_xf = xlwt.easyxf(
                'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
            headings = ['Time', 'Peer1']
            xls_sheet.set_panes_frozen(
                True)  # frozen headings instead of split panes
            xls_sheet.set_horz_split_pos(
                i)  # in general, freeze after last heading row
            xls_sheet.set_remove_splits(
                True)  # if user does unfreeze, don't leave a split there
            for colx, value in enumerate(headings):
                xls_sheet.write(i - 1, colx, value, heading_xf)
            for k in range(len(signal_list) - 1):
                for j in range(len(signal_list[k])):
                    width = 5000
                    xls_sheet.write(i, j, str(signal_list[k][j]), style1)
                    xls_sheet.col(j).width = width
                i = i + 1

        # Signal Strength Excel Ending here.

        # Trap Information Excel starting here.
        normal = []
        inforamtional = []
        minor = []
        major = []
        critical = []
        time_stamp = []

        sql = "SELECT count(ta.trap_event_id),date(ta.timestamp) ,ta.serevity FROM trap_alarms as ta  where  date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s AND ta.agent_id='%s'  group by serevity,date(ta.timestamp) order by  timestamp desc" % (
        total_days, ip_address)
        cursor.execute(sql)
        trap_result = cursor.fetchall()
        if trap_result is not None:
            # store the information in list.
            for i in range(0, 5):
                normal1 = 0
                inforamtional1 = 0
                minor1 = 0
                major1 = 0
                critical1 = 0
                for row in trap_result:
                    if datetime.date(datetime.now() + timedelta(days=-i)) == row[1]:
                        if int(row[2]) == 0:
                            normal1 += int(row[0])
                        elif int(row[2]) == 2:
                            normal1 += int(row[0])
                        elif int(row[2]) == 1:
                            inforamtional1 += int(row[0])
                        elif int(row[2]) == 3:
                            minor1 += int(row[0])
                        elif int(row[2]) == 4:
                            major1 += int(row[0])
                        elif int(row[2]) == 5:
                            critical1 += int(row[0])
                time_stamp.append(datetime.date(
                    datetime.now() + timedelta(days=-i)).strftime('%d %b %Y'))
                normal.append(normal1)
                inforamtional.append(inforamtional1)
                minor.append(minor1)
                major.append(major1)
                critical.append(critical1)

        event_list = []
        k = 0
        for time in time_stamp:
            event_list.append([int(inforamtional[k]), int(
                normal[k]), int(minor[k]), int(major[k]), int(critical[k]), str(time_stamp[k])])
            k += 1
        event_list = sorted(event_list, key=itemgetter(5))
        xls_sheet = xls_book.add_sheet(
            'event_count_information', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 5, " %s Days Event Information" %
                                          'Current' if total_days == 0 else total_days, style)
        xls_sheet.write_merge(1, 1, 0, 5, str(device_type) + '       ' + str(
            device_name) + '         ' + str(ip_address), style)
        xls_sheet.write_merge(2, 2, 0, 5, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Informational', 'Normal', 'Minor', 'Major',
                    'Critical', 'Time']
        xls_sheet.set_panes_frozen(
            True)  # frozen headings instead of split panes
        xls_sheet.set_horz_split_pos(
            i)  # in general, freeze after last heading row
        xls_sheet.set_remove_splits(
            True)  # if user does unfreeze, don't leave a split there
        for colx, value in enumerate(headings):
            xls_sheet.write(i - 1, colx, value, heading_xf)
        for k in range(len(event_list)):
            for j in range(len(event_list[k])):
                width = 5000
                xls_sheet.write(i, j, str(event_list[k][j]), style1)
                xls_sheet.col(j).width = width
            i = i + 1

        # Trap Information Excel Ending here.

        # event Information excel start here.
        trap_days = ((end_time - start_time).days)
        if int(select_option) == 0:
            # sql="SELECT
            # ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date
            # FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND
            # date(ta.timestamp)=current_date()  order by ta.timestamp "%(ip_address)
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND ta.timestamp<='%s' order by ta.timestamp " % (
                ip_address, start_time, end_time)

        else:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp " % (
                ip_address, trap_days)
        cursor.execute(sql)
        trap_result = cursor.fetchall()
        severity_list = ['Informational', 'Normal',
                         'Informational', 'Minor', 'Major', 'Critical']

        xls_sheet = xls_book.add_sheet(
            'alarm_information', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 3, "%s Days Alarm Information" %
                                          'Current' if trap_days == 0 else trap_days, style)
        xls_sheet.write_merge(1, 1, 0, 3, str(device_type) + '       ' + str(
            device_name) + '         ' + str(ip_address), style)
        xls_sheet.write_merge(2, 2, 0, 3, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Severity', 'Event ID', 'Event Type', 'Receive Date']
        xls_sheet.set_panes_frozen(
            True)  # frozen headings instead of split panes
        xls_sheet.set_horz_split_pos(
            i)  # in general, freeze after last heading row
        xls_sheet.set_remove_splits(
            True)  # if user does unfreeze, don't leave a split there
        for colx, value in enumerate(headings):
            xls_sheet.write(i - 1, colx, value, heading_xf)
        for k in range(len(trap_result)):
            for j in range(len(trap_result[k])):
                if j == 0:
                    width = 5000
                    xls_sheet.write(
                        i, j, severity_list[trap_result[k][j]], style1)
                    xls_sheet.col(j).width = width
                else:
                    width = 5000
                    xls_sheet.write(i, j, str(trap_result[k][j]), style1)
                    xls_sheet.col(j).width = width
            i = i + 1

        # event Information excel end here.

        # event Information excel start here.
        if int(select_option) == 0:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND ta.timestamp>='%s' AND  ta.timestamp<='%s' order by ta.timestamp " % (
                ip_address, start_time, end_time)
        else:
            sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' AND date(ta.timestamp)<=current_date() and  date(ta.timestamp)>current_date()-%s order by ta.timestamp " % (
                ip_address, trap_days)
        cursor.execute(sql)
        trap_result = cursor.fetchall()
        severity_list = ['Informational', 'Normal',
                         'Informational', 'Minor', 'Major', 'Critical']

        xls_sheet = xls_book.add_sheet(
            'event_information', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 3, "%s Days Event Information" %
                                          'Current' if trap_days == 0 else trap_days, style)
        xls_sheet.write_merge(1, 1, 0, 3, str(device_type) + '       ' + str(
            device_name) + '         ' + str(ip_address), style)
        xls_sheet.write_merge(2, 2, 0, 3, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Severity', 'Event ID', 'Event Type', 'Receive Date']
        xls_sheet.set_panes_frozen(
            True)  # frozen headings instead of split panes
        xls_sheet.set_horz_split_pos(
            i)  # in general, freeze after last heading row
        xls_sheet.set_remove_splits(
            True)  # if user does unfreeze, don't leave a split there
        for colx, value in enumerate(headings):
            xls_sheet.write(i - 1, colx, value, heading_xf)
        for k in range(len(trap_result)):
            for j in range(len(trap_result[k])):
                if j == 0:
                    width = 5000
                    xls_sheet.write(
                        i, j, severity_list[trap_result[k][j]], style1)
                    xls_sheet.col(j).width = width
                else:
                    width = 5000
                    xls_sheet.write(i, j, str(trap_result[k][j]), style1)
                    xls_sheet.col(j).width = width
            i = i + 1

        # event Information excel end here.

        # Outage excel start here.
        date_days = []  # this list store the days information with date.
        up_state = []
        # Its store the total up state of each day in percentage.
        down_state = []
        # Its store the total down state of each day in percentage.
        output_dict = {}  # its store the actual output for display in graph.\
        last_status = ''
        down_flag = 0
        up_flag = 0
        current_date = datetime.date(datetime.now())
        current_datetime = datetime.strptime(str(current_date + timedelta(
            days=-(total_days))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_datetime = datetime.strptime(
            str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        temp_date = last_datetime

        # this datetime last status calculation
        last_status_current_time = datetime.strptime(str(current_date + timedelta(
            days=-(total_days + 1))) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_status_end_time = datetime.strptime(str(current_date + timedelta(
            days=-(total_days))) + " 23:59:59", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.

        sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
		    FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
		   where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
		    order by nagios_statehistory.state_time " % (current_datetime, last_datetime, ip_address)
        # Execute the query.
        cursor.execute(sql)
        result = cursor.fetchall()

        # this query get last status of device
        sel_sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
		    FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
		   where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
		    order by nagios_statehistory.state_time  desc limit 1" % (
        last_status_current_time, last_status_end_time, ip_address)
        # Execute the query.
        cursor.execute(sel_sql)
        last_state = cursor.fetchall()
        if last_state is not None:
            if len(last_state) > 0:
                last_status = last_state[0][2]
        if result is not None:
            if len(result) > 0:
                for i in range((total_days + 1)):
                    flag = 0
                    total_down_time = 0
                    total_up_time = 0
                    temp_down_time = ''
                    temp_up_time = ''
                    temp_time = ''
                    j = 0
                    for row in result:
                        if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                            flag = 1
                            if row[2] == 0:
                                if temp_up_time == '':
                                    temp_up_time = row[1]
                                    if last_status == '' and up_flag == 0:
                                        if temp_time is not '':
                                            if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                total_up_time += abs((
                                                                         row[1] - temp_time).days * 1440 + (
                                                                     row[1] - temp_time).seconds / 60)
                                                temp_up_time = row[1]
                                            else:
                                                total_down_time += abs(
                                                    (row[1] - temp_time).days * 1440 + (
                                                    row[1] - temp_time).seconds / 60)
                                                temp_down_time = row[1]
                                        up_flag = 1
                                    elif last_status is not '' and up_flag == 0:
                                        up_flag = 1
                                        if last_status == 0:
                                            total_up_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                        else:
                                            total_down_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:
                                    if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                        total_up_time += abs((
                                                                 row[1] - temp_time).days * 1440 + (
                                                             row[1] - temp_time).seconds / 60)
                                        temp_up_time = row[1]
                                    else:
                                        total_down_time += abs((row[1] - temp_time).days * 1440 + (
                                            row[1] - temp_time).seconds / 60)
                                        temp_down_time = row[1]
                            else:
                                if temp_down_time == '':
                                    temp_down_time = row[1]
                                    if last_status == '' and down_flag == 0:
                                        if temp_time is not '':
                                            if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                                total_up_time += abs((
                                                                         row[1] - temp_time).days * 1440 + (
                                                                     row[1] - temp_time).seconds / 60)
                                                temp_up_time = row[1]
                                            else:
                                                total_down_time += abs(
                                                    (row[1] - temp_time).days * 1440 + (
                                                    row[1] - temp_time).seconds / 60)
                                                temp_down_time = row[1]
                                        down_flag = 1
                                    elif last_status is not '' and down_flag == 0:
                                        down_flag = 1
                                        if last_status == 0:
                                            total_up_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                        else:
                                            total_down_time = abs((row[1] - (temp_date + timedelta(
                                                days=-(i + 1)))).days * 1440 + (row[1] - (
                                            temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                                else:

                                    if result[j - 1][2] == 0 or result[j - 1][2] == "0":
                                        total_up_time += abs((
                                                                 row[1] - temp_time).days * 1440 + (
                                                             row[1] - temp_time).seconds / 60)
                                        temp_up_time = row[1]
                                    else:
                                        total_down_time += abs((row[1] - temp_time).days * 1440 + (
                                            row[1] - temp_time).seconds / 60)
                                        temp_down_time = row[1]

                        if j < len(result):
                            temp_time = row[1]
                        j += 1
                    if flag == 1:
                        if result[j - 1][2] == 0:
                            total_up_time = abs((result[j - 1][1] - (temp_date + timedelta(days=-i))).days *
                                                1440 + (
                            result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                        else:
                            total_down_time = abs((result[j - 1][1] - (
                                temp_date + timedelta(days=-i))).days * 1440 + (
                                                  result[j - 1][1] - (temp_date + timedelta(days=-i))).seconds / 60)
                    date_days.append(
                        (temp_date + timedelta(days=-(i))).strftime("%d %b %Y"))
                    total = total_up_time + total_down_time
                    if flag == 1 and total > 0:
                        up_state.append(
                            round((total_up_time * 100) / float(total), 2))
                        down_state.append(
                            round((total_down_time * 100) / float(total), 2))
                    else:
                        up_state.append(0)
                        down_state.append(0)
            else:
                sel_sql = "SELECT  nagios_hosts.address,nagios_hoststatus.status_update_time,nagios_hoststatus.current_state\
				    FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hoststatus.host_object_id = nagios_hosts.host_object_id\
				   where nagios_hoststatus.status_update_time between '%s'  and '%s' and nagios_hosts.address='%s'\
				    order by nagios_hoststatus.status_update_time " % (current_datetime, last_datetime, ip_address)
                cursor.execute(sel_sql)
                result = cursor.fetchall()
                for i in range((total_days + 1)):
                    flag = 0
                    total_down_time = 0
                    total_up_time = 0
                    for row in result:
                        if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                            flag = 1
                            if row[2] == 0:
                                total_up_time = abs((row[1] - (temp_date + timedelta(
                                    days=-(i + 1)))).days * 1440 + (
                                                    row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                            else:
                                total_down_time = abs((row[1] - (temp_date + timedelta(
                                    days=-(i + 1)))).days * 1440 + (
                                                      row[1] - (temp_date + timedelta(days=-(i + 1)))).seconds / 60)
                    date_days.append(
                        (temp_date + timedelta(days=-(i))).strftime("%d %b %Y"))
                    total = total_up_time + total_down_time
                    if flag == 1 and total > 0:
                        up_state.append(
                            round((total_up_time * 100) / float(total), 2))
                        down_state.append(
                            round((total_down_time * 100) / float(total), 2))
                    else:
                        up_state.append(0)
                        down_state.append(0)
            # close the database and cursor connection.
        # reverse the data
        outage_list = []
        k = 0
        for day in date_days:
            outage_list.append([day, up_state[k], down_state[k]])
            k += 1
        outage_list = sorted(outage_list, key=itemgetter(0))

        xls_sheet = xls_book.add_sheet(
            'outage_information', cell_overwrite_ok=True)
        xls_sheet.row(0).height = 521
        xls_sheet.row(1).height = 421
        xls_sheet.write_merge(0, 0, 0, 2, "%s Days Outage Information" %
                                          'Current' if total_days == 0 else total_days, style)
        xls_sheet.write_merge(1, 1, 0, 2, str(device_type) + '       ' + str(
            device_name) + '         ' + str(ip_address), style)
        xls_sheet.write_merge(2, 2, 0, 2, "")
        i = 4
        heading_xf = xlwt.easyxf(
            'font: bold on; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_green;')
        headings = ['Date', 'Up State', 'Down State']
        xls_sheet.set_panes_frozen(
            True)  # frozen headings instead of split panes
        xls_sheet.set_horz_split_pos(
            i)  # in general, freeze after last heading row
        xls_sheet.set_remove_splits(
            True)  # if user does unfreeze, don't leave a split there
        for colx, value in enumerate(headings):
            xls_sheet.write(i - 1, colx, value, heading_xf)
        for k in range(len(outage_list)):
            for j in range(len(outage_list[k])):
                width = 5000
                xls_sheet.write(i, j, str(outage_list[k][j]), style1)
                xls_sheet.col(j).width = width
            i = i + 1
            # Outage excel end here.

        # close the database connection and cursor connection
        cursor.close()
        db.close()

        # if len(crc_result)>0:
        xls_book.save('/omd/sites/%s/share/check_mk/web/htdocs/download/ubre_specific_report.xls' %
                      nms_instance)
        output_dict = {"success": 0, 'output': 'file succesfully downloaded'}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 3, 'output': str(e[-1])}
        html.write(str(output_dict))
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
    finally:
        if db.open:
            db.close()


######################################## ODU excel report creating  end ##


############################################  ODU Device Type dashboard cr
#
# def page_tip_ubre_monitor_dashboard(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_ubre_monitor_dashboard.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
