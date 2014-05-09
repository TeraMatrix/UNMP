#!/usr/bin/python2.6
from datetime import datetime

import MySQLdb

from mysql_collection import mysql_connection
from nms_config import *
from odu100_common_dashboard import ubr_outage_calculation
from unmp_dashboard_config import DashboardConfig

#######################################################################################
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	odu_dashboard.py
# Creation Date			:	11-September-2011
# Purpose			:	This file display the graph for ODU COMMON DASHBOARD.
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


def odu_dashboard_page(h):
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
    javascript_list = ["js/lib/main/highcharts.js", "js/unmp/main/oduDashboard.js"]
    html.new_header("UBR Common DashBoard", "", "", css_list, javascript_list)
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
    <div id=\"main_odu16_common_div\">\
    <input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />\
    <input type=\"hidden\" id=\"no_of_device\" name=\"no_of_device\" value=\"%s\" />\
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
    </div></div>\
    <div class=\"form-div-footer\">\
    <button type=\"submit\" class=\"yo-small yo-button\" id=\"odu_common_report_btn\" onclick="oduCommonReportGeneration();"><span class=\"save\">Report</span></button>\
    </div>' % (refresh_time, no_of_devcie)
    return dash_str


def odu_network_interface_graph(h):
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
        cursor.callproc("odu_interface_graph", (
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


def get_no_of_odu(h):
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

        sql = "SELECT count(host_id) FROM hosts WHERE device_type_id like 'odu16%'"
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


def odu_tdd_mac_error(h):
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
            "odu_tdd_mac_error", (int(start), (int(start) + int(limit))))
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
                            crc_error.append(
                                int(result[i * 2][0]))  # -int(result[2*i+1][0]))
                            phy_error.append(
                                int(result[i * 2][
                                    1]))  # -int(result[2*i+1][1])) ## Doubt (Peeyush) Arithmatic Operation on wron values for Delta
                            odu_name.append((result[i * 2][2]))

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


def odu_peer_node_signal(h):
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

        cursor.callproc("odu_peer_node_signal", (
            int(start), (int(start) + int(limit)), interface_value))
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


def odu_synslost_counter(h):
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
    @organisation: Code Scape Consultants Pvt. Ltd.
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
            "odu_sync_lost_counter", (int(start), (int(start) + int(limit))))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if result is not None:
            if len(result) > 0:
                if len(result[0]) > 1 and len(result) > 1:
                    # html.write(str(result));
                    for i in range(5):
                        if i * 2 + 1 >= len(result):
                            sync_lost.append(0)
                            odu_name.append(" ")

                        else:
                            sync_lost.append(
                                int(result[i * 2][
                                    0]))  # -int(result[i*2+1][0])) ## Doubt (Peeyush) Why is there an Aritmatic operation being performed here ?
                            # odu_name.append((result[i*2+1][1]))
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
            # cursor.close() ## close cursor as soon as result is fetched ## comment by Peeyush
        # db.close()
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
def odu_outage_graph(h):
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
    ip_address_list = []
    start = html.var("start")  # starting range for odu data fatching.
    limit = html.var("limit")  # ending range for odu data fatching.
    # calling the procedure
    current_date = str(
        datetime.date(datetime.now()))  # this is provided current date.
    current_datetime = datetime.strptime(str(
        current_date) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
    last_datetime = datetime.strptime(
        str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    try:
        # connection from mysql
        db, cursor = mysql_connection('nms2')
        if db == 1:
            raise SelfException(cursor)
        sel_query = "SELECT ip_address FROM hosts WHERE device_type_id='odu16' order by ip_address limit %s,%s" % (
            start, limit)
        cursor.execute(sel_query)
        ip_result = cursor.fetchall()
        for ip in ip_result:
            ip_address_list.append(ip[0])
        output_dict = ubr_outage_calculation(
            current_datetime, last_datetime, ip_address_list)
        cursor.close()
        db.close()
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
def odu_common_dashboard_report_generating(h):
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

        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)
        styleSheet = getSampleStyleSheet()
        odu_common_report = []
        MARGIN_SIZE = 14 * mm
        PAGE_SIZE = A4
        nms_instance = __file__.split("/")[3]
        pdfdoc = '/omd/sites/%s/share/check_mk/web/htdocs/report/odu_common_table.pdf' % nms_instance
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
        odu_common_report.append(im)
        odu_common_report.append(Spacer(1, 1))

        data = []
        data.append(['UBR Common Dashboard', (str(datetime.now().strftime(
            '%d %b %Y')) + '-' + str(datetime.now().strftime('%d %b %Y')))])
        t = Table(data, [3.5 * inch, 4 * inch])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (5, 1), 1, (0.7, 0.7, 0.7)),
            ('TEXTCOLOR', (0, 0), (0, 0), (0.11, 0.11, 0.11)),
            ('TEXTCOLOR', (1, 0), (1, 0), (0.65, 0.65, 0.65)),
            ('FONT', (0, 0), (1, 0), 'Helvetica', 14),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT')]))
        odu_common_report.append(t)
        odu_common_report.append(Spacer(11, 11))

        ########################################### ODU Network Interface r
        odu_common_report.append(Spacer(21, 21))

        netwok_table_name = ['UBR Network Bandwidth(eth0)', 'UBR Network Bandwidth(br0)',
                             'UBR Network Bandwidth(eth1)']
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu_interface_graph", (
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
        odu_common_report.append(t)
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
        odu_common_report.append(t)
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
        odu_common_report.append(t)

        #######################################################################

        ########################################### ODU Error Graph ###########
        odu_common_report.append(Spacer(31, 31))
        # create the cursor
        cursor = db.cursor()
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu_tdd_mac_error", (int(error_start), (
            int(error_start) + int(error_end))))
        result = cursor.fetchall()
        # function calling
        # table_output=table_list_creation(result1,'ODU Crc//Phy Error','Crc Error(error count)','Phy Error(error count)')
        # close the database and cursor connection.
        table_output = []
        table_output.append(['UBR Devices', 'Crc Error(error count)',
                             'Phy Error(error count)'])
        length = (str(len(result) / 2)).split('.')[0]
        if length > 0:
            if len(result[0]) > 1:
                for i in range(int(length)):
                    table_output.append([(result[i * 2 + 1][2]), int(result[i * 2][0]) - int(
                        result[i * 2 + 1][0]), int(result[i * 2][1]) - int(result[i * 2 + 1][1])])

        cursor.close()
        data1 = []
        data1.append(['UBR Crc Phy Error', '', ''])
        t = Table(data1, [1.51 * inch, 2.8 * inch, 2.77 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (0, 0), (0, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (0, 0), (0, 0), colors.white)]))
        odu_common_report.append(t)
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
        odu_common_report.append(t)
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
        odu_common_report.append(t)
        #######################################################################

        ########################################### ODU Signal Strength report
        odu_common_report.append(Spacer(31, 31))
        signal_interface = ['(peer0)', '(peer1)', '(peer2)', '(peer3)',
                            '(peer4)', '(peer5)', '(peer6)', '(peer7)']
        # create the cursor
        cursor = db.cursor()
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu_peer_node_signal", (
            int(ss_start), (int(ss_start) + int(ss_end)), ss_interface))
        result1 = cursor.fetchall()
        # function calling
        table_output = table_list_signal_sync(result1, 'ODU Signal Strength' + str(
            signal_interface[int(ss_interface)]), 'Signal Strength(dBm)')
        # close the database and cursor connection.
        cursor.close()
        data1 = []
        data1.append(['', 'UBR Signal Strength' + str(
            signal_interface[int(ss_interface)]), '', ''])
        t = Table(data1, [.021 * inch, 2.1 * inch, 2.45 * inch, 2.4 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu_common_report.append(t)

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
        odu_common_report.append(t)
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
        odu_common_report.append(t)

        #######################################################################

        ########################################### ODU Sync lost report ######
        odu_common_report.append(Spacer(31, 31))
        # create the cursor
        cursor = db.cursor()
        # prepare SQL query to get total number of access points in this system
        cursor.callproc("odu_sync_lost_counter", (int(sync_start),
                                                  (int(sync_start) + int(sync_end))))
        result = cursor.fetchall()
        # function calling
        # table_output=table_list_signal_sync(result1,'ODU Sync Lost','Sync
        # Lost')
        table_output = []
        # function calling
        # table_output=table_list_signal_sync(result1,'ODU Sync Lost','Sync
        # Lost')
        table_output.append(['UBR Devices', 'Sync Loss'])

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
        data1.append(['', 'UBR Sync Loss', '', ''])
        t = Table(data1, [.021 * inch, 1.23 * inch, 2.92 * inch, 2.8 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu_common_report.append(t)

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
        odu_common_report.append(t)
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
        odu_common_report.append(t)
        #######################################################################

        # close the first database connection

        #######################################################################

        #################### OUTAGE GRAPH for common dashboard ################
        odu_common_report.append(Spacer(31, 31))
        start = html.var(
            "outage_start")  # starting range for odu data fatching.
        limit = html.var("outage_limit")  # ending range for odu data fatching.
        ip_address_list = []
        cursor = db.cursor()
        # calling the procedure
        current_date = str(
            datetime.date(datetime.now()))  # this is provided current date.
        current_datetime = datetime.strptime(str(
            current_date) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
        last_datetime = datetime.strptime(
            str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        sel_query = "SELECT ip_address FROM hosts WHERE device_type_id='odu16' order by ip_address limit %s,%s" % (
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
        data1.append(['', 'UBR Reachability Statistics', '', ''])
        t = Table(data1, [.021 * inch, 2.45 * inch, 2.3 * inch, 2.2 * inch])
        t.setStyle(
            TableStyle(
                [(
                     'BACKGROUND', (1, 0), (1, 0), (0.35, 0.35, 0.35)), ('FONT', (0,
                                                                                  0), (1, 0), 'Helvetica', 11),
                 ('TEXTCOLOR', (1, 0), (2, 0), colors.white)]))
        odu_common_report.append(t)

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
        odu_common_report.append(t)
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
        odu_common_report.append(t)
        #######################################################################

        pdf_doc.build(odu_common_report)
        output_dict = {'success': 0, 'output': 'pdf downloaded'}
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
    temp = ['UBR Devices', first_header, second_header]
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
    temp = ['UBR Devices', first_header]
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
    output.append(['UBR Devices', 'Reachable(%)', 'Unreachable(%)'])
    i = 0
    for odu in odu_name:
        output.append([odu, round(up_state[i], 2), round(down_state[i], 2)])
        i += 1
    return output


# def page_tip_ubr_common_dashboard(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_ubr_common_dashboard.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
