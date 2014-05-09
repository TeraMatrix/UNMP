#!/usr/bin/python2.6
import MySQLdb
from nms_config import *
from datetime import datetime
from datetime import timedelta
from mysql_collection import mysql_connection
from unmp_dashboard_config import DashboardConfig
from common_controller import logme


#######################################################################################
# Author            :    Rajendra Sharma
# Project            :    UNMP
# Version            :    0.1
# File Name            :    odu_dashboard.py
# Creation Date            :    11-September-2011
# Purpose            :    This file display the graph for ODU COMMON DASHBOARD.
# Copyright (c) 2011 Codescape Consultant Private Limited

##########################################################################


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
    devcie_type_attr = ['id', 'refresh_time', 'show_device']
    get_data = DashboardConfig.get_config_attributes(
        'odu16_cdashboard', devcie_type_attr)
    refresh_time = 10   # default time
    total_count = 10    # default count showing record
    if get_data is not None:
        if get_data[0][0] == 'odu16_C':
            refresh_time = get_data[0][1]
            total_count = get_data[0][2]
    return str(refresh_time), str(total_count)


def odu100_common_dashboard(h):
    """

    @param h:
    @return: this function create the page for ODU common Dashboard.
    @rtype: this function return the html page for ODU common Dashboard graph display.
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function display the ODU common Dashboard and its display the all odu graph(network interface,peer Node ,signal strength graph ,Sync lost graph.).
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    css_list = ["css/style.css", "css/selection_interface.css"]
    javascript_list = ["js/lib/main/highcharts.js", "js/unmp/main/odu100CommonDashboard.js"]
    html.new_header("UBRe Common DashBoard", "", "", css_list, javascript_list)
    refresh_time, no_of_devcie = get_dashboard_data()
    html.write(str(dashboard_table(str(refresh_time), str(no_of_devcie))))
    html.new_footer()


def dashboard_table(refresh_time, no_of_devcie):
    """

    @param refresh_time:
    @param no_of_devcie:
    @return:
    """
    dash_str = '\
    <div id=\"show_message_div\"></div>\
    <div id=\"main_odu100_common_div\">\
    <input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />\
    <input type=\"hidden\" id=\"no_of_device\" name=\"no_of_device\" value=\"%s\" />\
    <div id="show_graph">\
    <div class=\"form-div\">\
    <table cellspacing="10px" cellpadding="0" width="100%%">\
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
        </tr>\
    </table>\
    </div>\
    <div class=\"form-div-footer\">\
    <button type=\"submit\" class=\"yo-small yo-button\" id=\"odu100_common_report_btn\" onclick="odu100CommonReportGeneration();"><span class=\"save\">Report</span></button>\
    </div>\
    </div></div>' % (refresh_time, no_of_devcie)
    return dash_str


def odu100_network_interface_graph(h):
    """

    @param h:
    @return: this function return a dictnoray of network interface for Network Interface graph showing .
    @rtype: this function return a dictnoray for Network interface graph .
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function display Network Interface graph for all interface.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    odu_name = []  # this list store the odu name.
    rx0 = []  # this list store the rx interface value for  odu.
    tx0 = []  # this list store the tx interface value for odu.
    start = html.var("start")  # starting range for odu data fatching.
    limit = html.var("limit")  # ending range for odu data fatching.
    output_dict = {}  # it contain the output result.
    interface_value = html.var("interface_value")  # interface value of odu
    try:
        refresh_time = get_refresh_time()
        # Open database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)
            # calling the procedure
        cursor.callproc("odu100_interface_graph", (
            int(start), (int(start) + int(limit)), interface_value))
        result = cursor.fetchall()
        if result is not None:
            if len(result) > 0:
                if len(result[0]) > 1 and len(result) > 1:
                    for i in range(5):
                        if i >= len(result):
                            rx0.append(0)
                            tx0.append(0)
                            odu_name.append(" ")

                        else:
                            rx0.append(int(result[i][0]) / 1024)
                            tx0.append(int(result[i][1]) / 1024)
                            odu_name.append(str(result[i][2]))

                else:
                    if len(result[0]) > 1:
                        index_val = 2
                    else:
                        index_val = 0
                    for i in range(5):
                        if i >= len(result):
                            rx0.append(0)
                            tx0.append(0)
                            odu_name.append(" ")
                        else:
                            rx0.append(0)
                            tx0.append(0)
                            odu_name.append((result[i][index_val]))
            # close the database and cursor connection.
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'rx_interface': rx0,
                       'tx_interface': tx0, 'odu_name': odu_name}
        html.write(str(output_dict))

    # Exception Handling Part
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


def get_no_of_odu100_devices(h):
    """

    @param h:
    @return: this function given the no of odu exists in database.
    @rtype: this function return a dictnoray.
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function return the no of odu exists in the database.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    total_odu = 0  # default value
    try:
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        sql = "SELECT count(host_id) FROM hosts WHERE device_type_id like 'ODU100%'"
        cursor.execute(sql)
        total = cursor.fetchone()

        if len(total) > 0:
            total_odu = total[0]
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'output': str(total_odu)}
        html.write(str(output_dict))
    # Exception Handling Part
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


def odu100_tdd_mac_error(h):
    """

    @param h:
    @return: this function return a dictnoray with error(crc,phy) information for Error graph showing
    @rtype: this function return a dictnoray.
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function display the Error(CRC/PHY) Graph
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    crc_error = []  # this list store the crc error information.
    phy_error = []  # this list store the phy error information.
    odu_name = []  # this list store the odu name.
    start = html.var("start")  # starting range for odu data fatching.
    limit = html.var("limit")  # ending range for odu data fatching.
    output_dict = {}  # it contain the output result.
    try:
        refresh_time = get_refresh_time()
        # Open database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        cursor.callproc(
            "odu100_tdd_mac_error", (int(start), (int(start) + int(limit))))
        result = cursor.fetchall()
        # close the cursor and database connection.
        cursor.close()
        db.close()
        if result is not None:
            if len(result) > 0:
                if len(result[0]) > 1 and len(result) > 1:
                    for i in range(5):
                        if i * 2 + 1 >= len(result):
                            crc_error.append(0)
                            phy_error.append(0)
                            odu_name.append(" ")

                        else:
                            val = int(
                                result[i * 2][0]) - int(result[i * 2 + 1][0])
                            val1 = int(
                                result[i * 2][1]) - int(result[i * 2 + 1][1])
                            crc_error.append(val if val > 0 else 0)
                            phy_error.append(val1 if val1 > 0 else 0)
                            odu_name.append((result[i * 2 + 1][2]))

                else:
                    if len(result[0]) > 1:
                        index_val = 2
                    else:
                        index_val = 0
                    for i in range(5):
                        if i >= len(result):
                            crc_error.append(0)
                            phy_error.append(0)
                            odu_name.append(" ")

                        else:
                            crc_error.append(0)
                            phy_error.append(0)
                            odu_name.append((result[i][index_val]))
        output_dict = {'success': 0, 'crc_error': crc_error,
                       'phy_error': phy_error, 'odu_name': odu_name}
        html.write(str(output_dict))
    # Exception Handling Part
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


def odu100_peer_node_signal(h):
    """

    @param h:
    @return: this function return a dictnoray with error(crc,phy) information for Error graph showing
    @rtype: this function return a dictnoray.
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function display the Error(CRC/PHY) Graph
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    signal_value = []  # this list store the signal value.
    odu_name = []  # this list store the odu name.
    start = html.var("start")  # starting range for odu data fatching.
    limit = html.var("limit")  # ending range for odu data fatching.
    output_dict = {}  # it contain the output result.
    interface_value = html.var(
        "interface_value")  # it give the interface value
    try:
        refresh_time = get_refresh_time()
        # Open database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        cursor.callproc("odu100_peer_node_signal", (
            int(start), (int(start) + int(limit)), int(interface_value) + 1))
        result = cursor.fetchall()

        if result is not None:
            if len(result) > 0:
                if len(result[0]) > 1:
                    for i in range(5):
                        if i >= len(result):
                            signal_value.append(0)
                            odu_name.append(" ")

                        else:
                            signal_value.append(int(result[i][0]))
                            odu_name.append((result[i][1]))

                else:
                    for i in range(5):
                        if i >= len(result):
                            signal_value.append(0)
                            odu_name.append(" ")
                        else:
                            signal_value.append(0)
                            odu_name.append((result[i][0]))

        # close the connection
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'signal': signal_value,
                       'odu_name': odu_name}
        html.write(str(output_dict))
    # Exception Handling Part
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


def odu100_synslost_counter(h):
    """

    @param h:
    @return: this function return a dictnoray with sync lost information for odu device.
    @rtype: this function return a dictnoray.
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function display the Sync Lost Graph.
    @organisati    on: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    odu_name = []  # this list store the odu name.
    start = html.var("start")  # starting range for odu data fatching.
    limit = html.var("limit")  # ending range for odu data fatching.
    output_dict = {}  # it contain the output result.
    sync_lost = []  # this list store the sync lost value for odu.
    try:
        # Open database connection
        # db = open_database_connection()
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        cursor.callproc(
            "odu100_sync_lost_counter", (int(start), (int(start) + int(limit))))
        result = cursor.fetchall()
        if result is not None:
            if len(result) > 0:
                if len(result[0]) > 1 and len(result) > 1:
                    for i in range(5):
                        if i * 2 + 1 >= len(result):
                            sync_lost.append(0)
                            odu_name.append(" ")

                        else:
                            val = int(
                                result[i * 2][0]) - int(result[i * 2 + 1][0])
                            sync_lost.append(val if val > 0 else 0)
                            odu_name.append((result[i * 2][1]))

                else:
                    if len(result[0]) > 1:
                        index_val = 1
                    else:
                        index_val = 0
                    for i in range(5):
                        if i >= len(result):
                            sync_lost.append(0)
                            odu_name.append(" ")

                        else:
                            sync_lost.append(0)
                            odu_name.append((result[i][index_val]))
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'counter': sync_lost,
                       'odu_name': odu_name}
        html.write(str(output_dict))
    # Exception Handling Part
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

# this function is used for display the outage graph.
# this function take one html argument.
# this return the dictionary of value to javascript file for display the graph.


def odu100_common_dashboard_outage_graph(h):
    """

    @param h:
    @return: this function return a dictnoray with outage information for odu device.
    @rtype: this function return a dictnoray.
    @requires: this function take one html agrument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function display the Outage Graph.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    odu_name = []  # its store the odu name in list.
    up_state = []  # Its store the total up state for each odu in percentage.
    down_state = []
    # Its store the total down state of each odu in percentage.
    output_dict = {}  # its store the actual output for display in graph.
    start = html.var("start")  # starting range for odu data fatching.
    limit = html.var("limit")  # ending range for odu data fatching.
    device_type = 'odu100'
    current_date = str(
        datetime.date(datetime.now()))  # this is provided current date.
    current_datetime = datetime.strptime(str(
        current_date) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
    last_datetime = datetime.strptime(
        str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    ip_address_list = []
    try:
        # connection from mysql
        db, cursor = mysql_connection('nms2')
        if db == 1:
            raise SelfException(cursor)
        sel_query = "SELECT ip_address FROM hosts WHERE device_type_id='odu100' order by ip_address limit %s,%s" % (
        start, limit)
        cursor.execute(sel_query)
        ip_result = cursor.fetchall()
        for ip in ip_result:
            ip_address_list.append(ip[0])
        output_dict = ubr_outage_calculation(
            current_datetime, last_datetime, ip_address_list)
        cursor.close()
        db.close()
        # output_dict={'success':0,'up_state':up_state,'down_state':down_state,'odu_name':odu_name}
        html.write(str(output_dict))
    # Exception Handling Part
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


# ODU COMMON DASHBOARD REPORT GENERATOR --------------------------->
def odu100_common_dashboard_report_generating(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h

    # take the starting and ending limit of current graph showing
    nw_start = html.var('nw_start')
    nw_end = html.var('nw_limit')
    nw_interface = html.var('nw_interface_value')

    ss_start = html.var('ss_start')
    ss_end = html.var('ss_limit')
    ss_interface = html.var('ss_interface_value')

    error_start = html.var('error_start')
    error_end = html.var('error_limit')

    sync_start = html.var('sync_start')
    sync_end = html.var('sync_limit')

    result1 = ''
    try:
        # print >> file_obj,file_name
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

        db, cursor = mysql_connection('midnms')
        if db == 1:
            raise SelfException(cursor)
        styleSheet = getSampleStyleSheet()
        odu100_common_report = []
        MARGIN_SIZE = 14 * mm
        PAGE_SIZE = A4
        nms_instance = __file__.split("/")[3]
        pdfdoc = '/omd/sites/%s/share/check_mk/web/htdocs/report/odu100_common_table.pdf' % nms_instance
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
        odu100_common_report.append(im)
        odu100_common_report.append(Spacer(1, 1))

        data = []
        data.append(['UBRe Common Dashboard', (str(datetime.now().strftime(
            '%d %b %Y')) + '-' + str(datetime.now().strftime('%d %b %Y')))])
        t = Table(data, [3.5 * inch, 4 * inch])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (5, 1), 1, (0.7, 0.7, 0.7)),
            ('TEXTCOLOR', (0, 0), (0, 0), (0.11, 0.11, 0.11)),
            ('TEXTCOLOR', (1, 0), (1, 0), (0.65, 0.65, 0.65)),
            ('FONT', (0, 0), (1, 0), 'Helvetica', 14),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
        odu100_common_report.append(t)
        odu100_common_report.append(Spacer(11, 11))

        ########################################### ODU Network Interface repor
        odu100_common_report.append(Spacer(21, 21))
        netwok_table_name = [
            'UBRe Network Bandwidth(eth0)', 'UBRe Network Bandwidth(eth1)']
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu100_interface_graph", (
            int(nw_start), (int(nw_start) + int(nw_end)), nw_interface))
        result1 = cursor.fetchall()
        # function calling
        table_output = table_list_creation(
            result1, '', 'Transmitted Rate(bps)', 'Received Rate(bps)')
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(
            ['', str(netwok_table_name[int(nw_interface) - 1]), '', ''])
        t = Table(data1, [.021 * inch, 2.45 * inch, 2.3 * inch, 2.2 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_common_report.append(t)
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
        odu100_common_report.append(t)
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
        odu100_common_report.append(t)

        #######################################################################

        ########################################### ODU Error Graph ###########
        odu100_common_report.append(Spacer(31, 31))
        # create the cursor
        cursor = db.cursor()
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu100_tdd_mac_error", (int(error_start),
                                                 (int(error_start) + int(error_end))))
        result = cursor.fetchall()
        # function calling
        table_output = []
        table_output.append(['UBRe Devices', 'Crc Error(error count)',
                             'Phy Error(error count)'])

        # table_output=table_list_creation(result1,'ODU Crc//Phy Error','Crc
        # Error(error count)','Phy Error(error count)')

        length = (str(len(result) / 2)).split('.')[0]
        if length > 0:
            if len(result[0]) > 1:
                for i in range(int(length)):
                    table_output.append([(result[i * 2 + 1][2]), int(result[i * 2][0]) - int(
                        result[i * 2 + 1][0]), int(result[i * 2][1]) - int(result[i * 2 + 1][1])])
            # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'UBRe Crc/Phy Error', '', ''])
        t = Table(data1, [.021 * inch, 2.45 * inch, 2.3 * inch, 2.2 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_common_report.append(t)
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
                               ('GRID', (0, 0), (5, int(len(table_output))), 0.21, (0.7, 0.7, 0.7))]))
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
        odu100_common_report.append(t)
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
        odu100_common_report.append(t)
        #######################################################################

        ########################################### ODU Signal Strength report
        odu100_common_report.append(Spacer(31, 31))
        signal_interface = ['(peer0)', '(peer1)', '(peer2)', '(peer3)', '(peer4)', '(peer5)', '(peer6)', '(peer7)',
                            '(peer8)', '(peer9)', '(peer10)',
                            '(peer11)', '(peer12)', '(peer13)', '(peer14)', '(peer15)']
        # create the cursor
        cursor = db.cursor()
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu100_peer_node_signal", (
            int(ss_start), (int(ss_start) + int(ss_end)), int(ss_interface) + 1))
        result1 = cursor.fetchall()
        # function calling
        table_output = table_list_signal_sync(result1, 'ODU Signal Strength' + str(
            signal_interface[int(ss_interface)]), 'Signal Strength(dBm)')
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'UBRe Signal Strength' + str(
            signal_interface[int(ss_interface)]), '', ''])
        t = Table(data1, [.021 * inch, 2.45 * inch, 2.3 * inch, 2.2 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_common_report.append(t)

        data = table_output
        t = Table(data, [3.55 * inch, 3.55 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (
                                   1, int(
                                       len(
                                           table_output)) - 1), 'Helvetica', 9),
                               ('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 10),
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
        odu100_common_report.append(t)
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
        odu100_common_report.append(t)

        #######################################################################

        ########################################### ODU Sync lost report ######
        odu100_common_report.append(Spacer(31, 31))
        # create the cursor
        cursor = db.cursor()

        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu100_sync_lost_counter", (int(
            sync_start), (int(sync_start) + int(sync_end))))
        result = cursor.fetchall()
        table_output = []
        # function calling
        # table_output=table_list_signal_sync(result1,'ODU Sync Lost','Sync
        # Lost')
        table_output.append(['UBRe Devices', 'Sync Loss'])

        # table_output=table_list_creation(result1,'ODU Crc//Phy Error','Crc
        # Error(error count)','Phy Error(error count)')
        length = (str(len(result) / 2)).split('.')[0]
        if length > 0:
            if len(result[0]) > 1:
                for i in range(int(length)):
                    table_output.append([(result[i * 2 + 1][1]), int(
                        result[i * 2][0]) - int(result[i * 2 + 1][0])])
            # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'UBRe Sync Loss', '', ''])
        t = Table(data1, [.021 * inch, 2.45 * inch, 2.3 * inch, 2.2 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_common_report.append(t)

        data = table_output
        t = Table(data, [3.55 * inch, 3.55 * inch])
        t.setStyle(TableStyle([('FONT', (0, 0), (1, 0), 'Helvetica-Bold', 10),
                               ('FONT', (0, 1), (1, int(len(
                                   table_output)) - 1), 'Helvetica', 9),
                               ('ALIGN', (1,
                                          0), (1, int(len(table_output)) - 1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (3, 0), (0.9, 0.9, 0.9)),
                               ('LINEABOVE',
                                (0, 0), (3, 0), 1.21, (0.35, 0.35, 0.35)),
                               ('GRID', (0, 0), (3, int(len(table_output)) - 1), 0.31, (0.75, 0.75, 0.75))]))
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
        odu100_common_report.append(t)
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
        odu100_common_report.append(t)
        #######################################################################

        # close the first database connection

        #######################################################################

        #################### OUTAGE GRAPH for common dashboard ################
        odu100_common_report.append(Spacer(31, 31))
        ip_address_list = []
        start = html.var(
            "outage_start")  # starting range for odu data fatching.
        limit = html.var("outage_limit")  # ending range for odu data fatching.
        cursor = db.cursor()
        # calling the procedure
        current_date = str(
            datetime.date(datetime.now()))  # this is provided current date.
        current_datetime = datetime.strptime(str(
            current_date) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_datetime = datetime.strptime(
            str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        sel_query = "SELECT ip_address FROM hosts WHERE device_type_id='odu100' order by ip_address limit %s,%s" % (
            int(start), int(limit))
        cursor.execute(sel_query)
        ip_result = cursor.fetchall()
        for ip in ip_result:
            ip_address_list.append(ip[0])
        output_dict = ubr_outage_calculation(
            current_datetime, last_datetime, ip_address_list)
        # close the database and cursor connection
        cursor.close()
        db.close()
        if int(output_dict['success']) == 1:
            table_output = outage_graph_generation(
                odu_name, down_state, up_state)
        else:
            table_output = outage_graph_generation(
                output_dict['odu_name'], output_dict['down_state'], output_dict['up_state'])
        data1 = []
        data1.append(['', 'UBRe Reachability Statistics', '', ''])
        t = Table(data1, [.021 * inch, 2.45 * inch, 2.3 * inch, 2.2 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu100_common_report.append(t)

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
        odu100_common_report.append(t)
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
        odu100_common_report.append(t)
        #######################################################################

        pdf_doc.build(odu100_common_report)
        output_dict = {'success': 0, 'output': 'pdf downloaded'}
        html.write(str(output_dict))
    # Exception Handling Part
    except MySQLdb as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    finally:
        if db.open:
            cursor.close()
            db.close()


def table_list_creation(result, table_name, first_header, second_header):
    """

    @param result:
    @param table_name:
    @param first_header:
    @param second_header:
    @return:
    """
    table_output = []
    # table_output.append([table_name])
    temp = ['UBRe Devices', first_header, second_header]
    table_output.append(temp)
    if result is not None:
        if len(result) > 0:
            if len(result[0]) > 1:
                for i in range(int(len(result))):
                    table_output.append(
                        [result[i][2], result[i][0], result[i][1]])
    return table_output


def table_list_signal_sync(result, table_name, first_header):
    """

    @param result:
    @param table_name:
    @param first_header:
    @return:
    """
    table_output = []
    temp = ['UBRe Devices', first_header]
    table_output.append(temp)
    if result is not None:
        if len(result) > 0:
            if len(result[0]) > 1:
                for i in range(int(len(result))):
                    table_output.append([result[i][1], result[i][0]])
    return table_output


def outage_graph_generation(odu_name, down_state, up_state):
    """

    @param odu_name:
    @param down_state:
    @param up_state:
    @return:
    """
    output = []
    output.append(['UBRe Devices', 'Reachable(%)', 'Unreachable(%)'])
    i = 0
    for odu in odu_name:
        output.append([odu, round(up_state[i], 2), round(down_state[i], 2)])
        i += 1
    return output


def ubr_outage_calculation(start_date, end_date, ip_address_list):
    """

    @param start_date:
    @param end_date:
    @param ip_address_list:
    @return:
    """
    ip_address = []  # this list store the days information with date.
    up_state = []  # Its store the total up state of each day in percentage.
    down_state = []
    # Its store the total down state of each day in percentage.
    output_dict = {}  # its store the actual output for display in graph.
    result = get_outage(start_date, end_date, ip_address_list)
    if int(result['success']) == 1:
        return get_outage
    else:
        for row in result['result']:
            ip_address.append(row[1])
            up_state.append(row[2])
            down_state.append(row[3])
        output_dict = {'success': 0, 'up_state': up_state,
                       'down_state': down_state, 'odu_name': ip_address}
        return output_dict


def get_outage(d1, d2, ip_address_list):
    """

    @param d1:
    @param d2:
    @param ip_address_list:
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
        for ip_address in ip_address_list:
            sel_query = "SELECT trap_event_id,trap_event_type,timestamp,agent_id FROM system_alarm_table \
            where agent_id='%s' and timestamp>='%s' and timestamp<='%s' order by timestamp" % (
            ip_address, start_date, end_date)
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


class MainOutage(object):
    """

    @param result_tuple:
    @param end_date:
    @param start_date:
    """
    from copy import deepcopy

    def __init__(self, result_tuple, end_date, start_date):
        self.prev_value = None
        self.prev_date = None
        self.prev_ip = None
        self.main_list = []
        self.prev_tpl = None
        self.result_tuple = result_tuple
        self.end_date = end_date
        if self.result_tuple and start_date < result_tuple[0][2]:
            self.start_date = deepcopy(result_tuple[0][2])
        else:
            self.start_date = start_date

            # logme(" odu100 ", end_date, start_date)

    def fill_leftout_dates(self, leftout_days, mid_date, temp_date, is_last_call):
        """

        @param leftout_days:
        @param mid_date:
        @param temp_date:
        @param is_last_call:
        """
        for i in range(leftout_days):
            self.prev_date = mid_date + timedelta(days=i + 1)
            uptime, downtime = None, None
            if self.prev_tpl[0] == '50002':
                uptime = timedelta(0, 86399)
            else:
                downtime = timedelta(0, 86399)
            if not is_last_call:
                if self.prev_date.year == temp_date.year and self.prev_date.month == temp_date.month and self.prev_date.day == temp_date.day:
                    continue
                # logme(" left "+str(self.prev_date)+ "  || "+str(self.prev_value) + "  || "+str(self.prev_tpl[0]) + "\n")
            self.main_list.append([self.prev_date, self.prev_tpl[3], uptime, downtime])

        if is_last_call:
            if self.prev_date and self.prev_date < self.end_date:
                uptime, downtime = None, None
                logme(str(self.prev_value) + " ---------  " + str(self.prev_tpl))
                if self.prev_value == '50002':
                    uptime = timedelta(0, 86399)
                else:
                    downtime = timedelta(0, 86399)
                    #if (self.end_date - temp_date) > timedelta(0, 86399):
                if self.main_list[-1][0].year == self.end_date.year and self.main_list[-1][
                    0].month == self.end_date.month and self.main_list[-1][0].day == self.end_date.day:
                    # logme(" in in ")
                    pass
                else:
                    # logme(repr(self.main_list[-1][0])+ "  ***  "+ repr(temp_date))
                    self.main_list.append([self.end_date, self.prev_tpl[3], uptime, downtime])

    def fill_first(self, temp_date, uptime, downtime):
        """

        @param temp_date:
        @param uptime:
        @param downtime:
        @return:
        """
        date_to_use = temp_date - timedelta(days=1)
        mid_date = datetime(date_to_use.year,
                            date_to_use.month, date_to_use.day, 23, 59, 59)

        if self.prev_value == '50002':
            if uptime == None:
                uptime = (temp_date - mid_date)
            else:
                uptime += (temp_date - mid_date)

        elif self.prev_value == '50001':
            if downtime == None:
                downtime = (temp_date - mid_date)
            else:
                downtime += (temp_date - mid_date)
        return uptime, downtime

    def fill_end_dates(self, temp_date, temp_value, uptime, downtime):
        """

        @param temp_date:
        @param temp_value:
        @param uptime:
        @param downtime:
        """
        deduct_date = temp_date
        if self.start_date > temp_date:
            deduct_date = self.start_date
        if self.end_date.month > temp_date.month or self.end_date.day > temp_date.day:
            mid_date = datetime(temp_date.year,
                                temp_date.month, temp_date.day, 23, 59, 59)
        else:
            if self.end_date.hour >= temp_date.hour:
                mid_date = self.end_date
            else:
                mid_date = None

        if mid_date:
            if temp_value == '50002':
                if uptime:
                    uptime += (mid_date - deduct_date)
                else:
                    uptime = (mid_date - deduct_date)

            elif temp_value == '50001':
                if downtime:
                    downtime += (mid_date - deduct_date)
                else:
                    downtime = (mid_date - deduct_date)
                # logme(" END "+str(temp_date) + "\n")
            self.main_list.append([temp_date, self.prev_tpl[3], uptime, downtime])


    def get_outage(self):
        """


        @return:
        """
        try:
            uptime = None
            downtime = None
            for tpl in self.result_tuple:
                temp_ip = tpl[3]
                temp_date = tpl[2]
                temp_value = tpl[0]
                if self.prev_tpl:
                    self.prev_value = self.prev_tpl[0]
                    self.prev_date = self.prev_tpl[2]

                if temp_ip == self.prev_ip:
                    if temp_date.month > self.prev_date.month or temp_date.day > self.prev_date.day:
                        is_date = 1
                    else:
                        # logme('\n')
                        # logme(" self.st, temp_date, uptime, self.prev_value, downtime "+ str(self.start_date)+ " || " + str(temp_date)+ " || " + str(uptime)+ " || " + str(self.prev_value)+ " || " + str(downtime))
                        # logme('\n')
                        if self.prev_value == '50002':
                            if uptime == None:
                                # below is the previos condition that causing problem.
                                # if self.start_date < temp_date and (temp_date - self.start_date ) < timedelta(0, 86399):
                                # needed to test this new one
                                if downtime is None and self.start_date < temp_date and (
                                    temp_date - self.start_date ) < timedelta(0,
                                                                              86399) and temp_date.day == self.start_date.day:
                                    uptime = (temp_date - self.start_date)
                                else:
                                    uptime = (temp_date - self.prev_date)
                            else:
                                uptime += (temp_date - self.prev_date)

                        elif self.prev_value == '50001':
                            if downtime == None:
                                if uptime is None and self.start_date < temp_date and (
                                    temp_date - self.start_date ) < timedelta(0,
                                                                              86399) and temp_date.day == self.start_date.day:
                                    downtime = (temp_date - self.start_date)
                                else:
                                    downtime = (temp_date - self.prev_date)
                            else:
                                downtime += (temp_date - self.prev_date)

                        self.prev_date = temp_date  # print "jump1"

                else:
                    is_new = 1

                if is_new:
                    is_new = 0
                    self.prev_ip = temp_ip
                    is_date = 1
                    if self.prev_value:
                        # print " IS NEW TESTED "
                        uptime, downtime = self.fill_first(temp_date, uptime, downtime)
                        self.fill_end_dates(temp_date, temp_value, uptime, downtime)

                    self.prev_value = None
                    self.prev_date = None

                if is_date:
                    if uptime == None and downtime == None and not self.prev_value:
                        if self.start_date < temp_date and (temp_date - self.start_date ) < timedelta(0, 86399):
                            # date_to_use = temp_date - timedelta(days = 1)
                            # mid_date = datetime(date_to_use.year,
                            #                 date_to_use.month, date_to_use.day, 23, 59, 59)
                            mid_date = deepcopy(self.start_date)
                            delta = temp_date - mid_date
                            # print "IF temp_date, delta ", temp_date,' || ',  delta
                            if temp_value == '50001':
                                uptime = delta
                            elif temp_value == '50002':
                                downtime = delta
                    else:
                        mid_date = datetime(self.prev_date.year,
                                            self.prev_date.month, self.prev_date.day, 23, 59, 59)
                        delta = mid_date - self.prev_date
                        # print ">>>ELSE temp_date, delta ", mid_date, " || ",self.prev_date,' || ',  temp_date,' || ',  uptime, ' || ', downtime
                        if self.prev_value == '50002':
                            if uptime == None:
                                uptime = delta
                            else:
                                uptime += delta

                        elif self.prev_value == '50001':
                            if downtime == None:
                                downtime = delta
                            else:
                                downtime += delta

                                # print "ELSE temp_date, delta ", self.prev_date,' || ',  temp_date,' || ',  uptime, ' || ', downtime

                    if self.prev_value:
                        # print " ______________ ", self.prev_date,' || ',  uptime,' || ',  downtime
                        self.main_list.append([self.prev_date, self.prev_tpl[3], uptime, downtime])
                        uptime = None
                        downtime = None

                        #leftout_days = (temp_date - self.prev_date).days
                        #self.fill_leftout_dates((temp_date - self.prev_date).days, self.prev_date + timedelta(days = 1))
                        self.fill_leftout_dates((temp_date - self.prev_date).days, self.prev_date, temp_date, 0)

                        uptime, downtime = None, None

                if is_date and self.prev_value:
                    # print " ^^^^^^^^^^^^^^^^^^^^^  ", uptime,' || ', temp_date,' || ',  downtime
                    uptime, downtime = self.fill_first(temp_date, uptime, downtime)
                    # print " >>>>>>>>>>>>>>>>>  ", uptime,' || ',  temp_date,' || ',  downtime

                is_date = 0
                self.prev_tpl = tpl[:]

            if self.result_tuple:
                if uptime is None and downtime is None:
                    uptime, downtime = self.fill_first(temp_date, uptime, downtime)

                self.fill_end_dates(temp_date, temp_value, uptime, downtime)
                self.fill_leftout_dates((self.end_date - temp_date).days, temp_date, temp_date, 1)

            main_dict = {}
            main_dict['success'] = 0
            main_dict['result'] = self.main_list
            main_dict['outage'] = "main_outage"
            # logme(" ^^^^^^^^^^  ", main_dict)
            return main_dict
        except Exception:
            import traceback

            main_dict = {}
            main_dict['success'] = 1
            main_dict['result'] = traceback.format_exc()
            logme("Exception mainoutage.getoutage odu100", traceback.format_exc())
            return main_dict