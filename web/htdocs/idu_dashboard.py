#!/usr/bin/python2.6
"""
@ Author            :    Rajendra Sharma
@ Project           :    UNMP
@ Version           :    0.1
@ File Name         :    idu_dashboard.py
@ Creation Date     :    1-october-2011
@ Purpose           :    This file display the graph for IDU Device.
@ Organisation      :    Code Scape Consultants Pvt. Ltd.
@ Copyright (c) 2011 Codescape Consultant Private Limited
"""
# import the packeges

from datetime import datetime
from datetime import timedelta

import MySQLdb
from mysql_collection import mysql_connection
from nms_config import get_refresh_time


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


def idu_dashboard_page(h):
    """

    @param h:
    @return: this class return the html page.
    @rtype: html code as a string
    @requires: html object
    @note: this function display the idu dashboard page.
    """
    global html
    html = h
    html.new_header("IDU MONITORING")
    host_id = html.var('host_id')
    ip_address = html.var('ip_address')
    html_page = ""
    html_page += "<script type=\"text/javascript\" src=\"js/lib/main/highcharts.js\"></script>\
             <script type=\"text/javascript\" src=\"js/unmp/main/iduDashboard.js\"></script>\
             <link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\
             <div class=\"main_div\">\
                  <div class=\"header_div\">\
             <h2 id=\"idu_name\">IDU\
             <label id=\"iduName\"></label></h2>\
             <input type=\"hidden\" id=\"refresh_time\" name=\"refresh_time\" value=\"%s\" />\
             <input type=\"hidden\" id=\"idu_host_id\" name=\"host_id\" value=\"%s\" />\
             <input type=\"hidden\" id=\"idu_ip_address\" name=\"ip_address\" value=\"%s\" />\
             </div>\
             <div id=\"idu_graph_div\">\
             <div id=\"idu_device_information\"></div>\
             <table border=\"0\" class=\"addform\"><tr><td class=\"button\"><div style=\"width:100%%;height:180px;\" id=\"idu_nw_interface_div\"></div></td></tr></table>\
             <table border=\"0\" class=\"addform\"><tr><td class=\"button\"><div style=\"width:100%%;height:180px;\" id=\"idu_tdmoip_nw_interface_div\"></div></td></tr></table>\
             <table border=\"0\" class=\"addform\"><tr><td class=\"button\"><div style=\"width:100%%;height:180px;\" id=\"idu_port_status_div\"></div></td></tr></table>\
             <table border=\"0\" class=\"addform\"><tr><td class=\"button\"><div style=\"width:100%%;height:180px;\" id=\"idu_trap_graph_div\"></div></td></tr></table>\
             <table border=\"0\" class=\"addform\"><tr><td class=\"button\"><div style=\"width:100%%;height:180px;\" id=\"idu_outage_graph_div\"></div></td></tr></table>\
             <div style=\"width:100%%;height:180px;\" id=\"idu_current_alarm_div\"></div></td></tr>\
             <div style=\"width:100%%;height:180px;margin-top:29px\" id=\"idu_current_trap_div\"></div></td></tr>\
             </div>\
             </div>" % (5, host_id, ip_address)
    html.write(html_page)
    html.footer()
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    html.new_footer()


def idu_network_interface_graph(h):
    """

    @param h:
    @return: this class return the dictionary rxBytes,txBytes of IDU network interface.
    @rtype: dictionary
    @requires: html object
    @note: this function display the idu network interface graph.
    """
    global html
    html = h
    host_id = html.var('host_id')
    rxBytes = []  # this is store the receving bytes
    txBytes = []
    timestamp = []
    idu_ip_address = '--'
    try:
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.now() + timedelta(minutes=-30)
        end_time = now.strftime('%Y-%m-%d %H:%M:%S')
        db, cursor = mysql_connection('nms_sample')
        if db == 1 or db == '1':
            raise SelfException(cursor)
        if host_id != '' or host_id != None or host_id.strip() != 'undefined':
            sql = "SELECT ip_address FROM hosts WHERE host_id='%s'" % host_id
            cursor.execute(sql)
            ip_address = cursor.fetchone()
            cursor.close()
            # close the cursor connection.
            if len(ip_address) > 0:
                cursor = db.cursor()
                idu_ip_address = ip_address[0]
                cursor.callproc("idu_nw_interfcace_statistics", (
                    start_time, end_time, get_refresh_time(), 0, host_id))
                idu_nw_result = cursor.fetchall()
                cursor.close()
                for row in idu_nw_result:
                    rxBytes.append(int(row[1]) / 1024)
                    txBytes.append(int(row[2]) / 1024)
                    timestamp.append(row[3].strftime('%H:%M'))
                # clsoe the database connection
            db.close()
        output_dict = {'success': 0, 'rxBytes': rxBytes, 'txBytes':
            txBytes, 'timestamp': timestamp, 'idu_ip_address': idu_ip_address}
        html.write(str(output_dict))
    except MySQLdb.Error, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
        if db.open:
            cursor.close()
            db.close()
    except Exception, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()


def idu_device_information(h):
    """

    @param h:
    @return: this class return the dictionary of idu device information.
    @rtype: dictionary
    @requires: html object
    @note: this function return the device information .
    """
    global html
    html = h
    host_id = html.var('host_id')  # it store the idu host id
    device_detail = ""  # it store the device information.
    try:
        db, cursor = mysql_connection('nms_sample')
        if db == 1 or db == '1':
            raise SelfException(cursor)

        sql = "SELECT info.hwSerialNumber,info.systemterfaceMac,info.tdmoipInterfaceMac,sw.activeVersion,sw.passiveVersion,sw.bootloaderVersion,info.currentTemperature,info.sysUptime FROM idu_swStatusTable as sw INNER JOIN idu_iduInfoTable as info ON sw.host_id=sw.host_id WHERE info.host_id='%s'" % host_id
        cursor.execute(sql)
        result = cursor.fetchone()
        # close the  database and cursor connection.
        cursor.close()
        db.close()
        device_detail = "<table border=\"0\" class=\"addform\">"
        device_detail += "<tr><th>H/W Serial Number</th><th>System MAC</th><th>TDMOIP Interface MAC</th><th>Active Version</th><th>Passive Version</th><th>BootLoader Version</th><th>Temperature(C)</th><th>UpTime</th></tr><tr class=\"even\">"

        if len(result) > 0:
            if result[7] != "" or result != None:
                hour = result[7] / 3600
                minute = (result[7] / 60) % 60
                second = result[7] % 60
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[0] == None or result[0] == "" else result[0]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[1] == None or result[1] == "" else result[1]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[2] == None or result[2] == "" else result[2]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[3] == None or result[3] == "" else result[3]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[4] == None or result[4] == "" else result[4]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[5] == None or result[5] == "" else result[5]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                '--' if result[6] == None or result[6] == "" else result[6]) + "</td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\">" + str(
                str(hour) + "Hr " + str(minute) + "Min " + str(second) + "Sec") + "</td>"
        else:
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"
            device_detail += "<td style=\"margin-left:2px; align:center;\"></td>"

        device_detail += "</tr></table>"

        output_dict = {'success': 0, 'device_details': device_detail}
        html.write(str(output_dict))

    except MySQLdb.Error, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
        if db.open:
            cursor.close()
            db.close()
    except Exception, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()


def idu_tdmoip_network_interface_graph(h):
    """

    @param h:
    @return: this class return the dictionary of idu tdmoip network interface information.
    @rtype: dictionary
    @requires: html object
    @note: this function return the idu tdmoip network interface information information for graph showing.
    """
    global html
    html = h
    host_id = html.var('host_id')
    rx_receving = []  # this is store the receving bytes
    tx_transmiting = []  # this is store the transmiting bytes
    timestamp = []

    try:
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.now() + timedelta(minutes=-30)
        end_time = now.strftime('%Y-%m-%d %H:%M:%S')
        db, cursor = mysql_connection('nms_sample')
        if db == 1 or db == '1':
            raise SelfException(cursor)
        cursor.callproc("idu_tdmoip_nw_interfcace_statistics", (
            start_time, end_time, get_refresh_time(), 0, host_id))
        idu_nw_result = cursor.fetchall()
        # close the data base and cursor connection.
        cursor.close()
        db.close()
        if len(idu_nw_result) > 0:
            for row in idu_nw_result:
                tx_transmiting.append(int(row[1]) / 1024)
                rx_receving.append(int(row[2]) / 1024)
                timestamp.append(row[3].strftime('%H:%M'))

        output_dict = {'success': 0, 'tx_transmiting': tx_transmiting,
                       'rx_receving': rx_receving, 'timestamp': timestamp}
        html.write(str(output_dict))

    except MySQLdb.Error, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
        if db.open:
            cursor.close()
            db.close()
    except Exception, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()


def idu_port_status_graph(h):
    """

    @param h:
    @return: this class return the dictionary of idu port status information.
    @rtype: dictionary
    @requires: html object
    @note: this function return the idu port status information information for graph showing.
    """
    global html
    html = h
    host_id = html.var('host_id')
    operation_state = []  # this is store the operation state
    link_speed = []  # this is store link speed of port status
    port_name = []  # this is store the port name
    try:
        db, cursor = mysql_connection('nms_sample')
        if db == 1 or db == '1':
            raise SelfException(cursor)
        sql = "SELECT switchstatportnum,opstate,linkspeed FROM idu_switchportstatusTable WHERE host_id='%s' ORDER BY timestamp LIMIT 5" % host_id
        cursor.execute(sql)
        idu_nw_result = cursor.fetchall()
        # close the database and cursor connection
        cursor.close()
        db.close()

        if len(idu_nw_result) > 0:
            for row in idu_nw_result:
                operation_state.append(row[1])
                link_speed.append(
                    100 if str(row[1]).strip() == 'enable' else 0)
                port_name.append(
                    'na' if row[0] == 1 or row[0].strip() == '1' else row[0])

        output_dict = {'success': 0, 'operation_state':
            operation_state, 'link_speed': link_speed, 'port_name': port_name}
        html.write(str(output_dict))

    except MySQLdb.Error, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
        if db.open:
            cursor.close()
            db.close()
    except Exception, e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()


def idu_trap_information(h):
    """

    @param h:
    @return: This function provide the latest  5 current trap and alarm of idu.
    @rtype: dictionary
    @requires: html object
    @note: this function return the latest idu trap information.
    """
    global html
    html = h
    image_title_name = {0: "Normal", 1: "Informational", 2: "Normal",
                        3: "Minor", 4: "Major", 5: "Critical"}
    image_dic = {0: "images/status-0.png", 1: "images/status-0.png", 2: "images/status-0.png", 3:
        "images/minor.png", 4: "images/status-1.png", 5: "images/critical.png"}
    length = 5
    host_id = html.var("host_id")  # take host_id from js side
    ip_address = html.var('ip_address')  # take ip_address from js side

    try:
        # create database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarms as ta WHERE ta.agent_id='%s' order by ta.timestamp limit 7 " % ip_address
        cursor.execute(sql)
        all_traps = cursor.fetchall()
        if len(all_traps) < 5:
            length = len(all_traps)
        history_trap = "<table border=\"0\" class=\"addform\">"
        history_trap += "<colgroup><col width='5%'/><col width='25%'/><col width='25%'/><col width='45%'/></colgroup>"
        history_trap += "<tr><th colspan=\"4\">Latest 5 Traps</th></tr>"
        history_trap += "<tr><th>&nbsp;</th><th>Trap Event Id</th><th>Trap Event Type</th><th>Trap Receive Date</th></tr>"
        tr_css = ""
        for i in range(length):
            if i % 2 == 0:
                tr_css = "odd"
            else:
                tr_css = "even"
            history_trap += "<tr class=\"%s\"><td><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px\" /></td>" % (
                tr_css, image_dic[all_traps[i][0]], image_title_name[all_traps[i][0]],
                image_title_name[all_traps[i][0]])
            history_trap += "<td>%s</td>" % all_traps[i][1]
            history_trap += "<td>%s</td>" % all_traps[i][2]
            history_trap += "<td>%s</td></tr>" % all_traps[i][3]
        if tr_css == "even":
            tr_css = "odd"
        else:
            tr_css = "even"
        if len(all_traps) < 1:
            history_trap += "<tr class='odd'><td colspan='4'><b>Trap does not exists.</b></td></tr>"
        history_trap += "<tr class=\"%s\"><td></td><td></td><td></td><td style=\"text-align:right\">%s</td></tr></table>" % (
        tr_css, (
            "<a href=\"status_snmptt.py?trap_status=history&ip_address=" + ip_address + "\">more>></a>" if len(
                all_traps) > 5 else ""))

        # This query return the latest five entry of current alarm
        sql = "SELECT ta.serevity,ta.trap_event_id,ta.trap_event_type,ta.trap_receive_date FROM trap_alarm_current as ta WHERE ta.agent_id='%s' order by ta.timestamp limit 7 " % ip_address
        cursor.execute(sql)
        current_alarm = cursor.fetchall()
        length = 5
        if len(current_alarm) < 5:
            length = len(current_alarm)
        current_alarm_html = "<table border=\"0\" class=\"addform\">"
        current_alarm_html += "<colgroup><col width='5%'/><col width='25%'/><col width='25%'/><col width='45%'/></colgroup>"
        current_alarm_html += "<tr><th colspan=\"4\">Latest 5 Alarms</th></tr>"
        current_alarm_html += "<tr><th>&nbsp;</th><th>Trap Event Id</th><th>Trap Event Type</th><th>Trap Receive Date</th></tr>"
        tr_css = ""

        for i in range(length):
            if i % 2 == 0:
                tr_css = "odd"
            else:
                tr_css = "even"
            current_alarm_html += "<tr class=\"%s\"><td><img src=\"%s\" alt=\"%s\" title=\"%s\" class=\"imgbutton\" style=\"width:13px\" /></td>" % (
                tr_css, image_dic[current_alarm[i][0]], image_title_name[current_alarm[i][0]],
                image_title_name[current_alarm[i][0]])
            current_alarm_html += "<td>%s</td>" % current_alarm[i][1]
            current_alarm_html += "<td>%s</td>" % current_alarm[i][2]
            current_alarm_html += "<td>%s</td></tr>" % current_alarm[i][3]
        if tr_css == "even":
            tr_css = "odd"
        else:
            tr_css = "even"

        if len(current_alarm) < 1:
            current_alarm_html += "<tr class='odd'><td colspan='4'><b>Alarm does not exists.</b></td></tr>"

        current_alarm_html += "<tr class=\"%s\"><td></td><td></td><td></td><td style=\"text-align:right\">%s</td></tr></table>" % (
            tr_css,
            "<a href=\"status_snmptt.py?trap_status=current&ip_address" + ip_address + "\" id=\"status_id\">more>></a>" if len(
                current_alarm) > 5 else "")
        # close database connection and cursor.
        cursor.close()
        db.close()

        history_trap_detail = {'success': 0, 'trap_output':
            history_trap, 'alarm_output': current_alarm_html}
        html.write(str(history_trap_detail))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()


def idu_trap_graph(h):
    """

    @param h:
    @return: This function provide the  5 day trap information of idu device.
    @rtype: dictionary
    @requires: html object
    @note: this function return the 5 day information to js file which that we can display the idu trap graph.
    """
    global html
    html = h
    normal = []
    inforamtional = []
    minor = []
    major = []
    critical = []
    time_stamp = []
    host_id = html.var("host_id")  # take host id from js side
    ip_address = html.var('ip_address')  # take ip_address from js side

    try:
        # create database connection
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        # call.proc("procedure name",(no_of_day,odu ip_address))
        cursor.callproc("trap_graph", (10, ip_address))
        trap_result = cursor.fetchall()
        # store the information in list.
        for row in trap_result:
            normal.append(int(row[1]))
            inforamtional.append(int(row[2]))
            minor.append(int(row[3]))
            major.append(int(row[4]))
            critical.append(int(row[5]))
            time_stamp.append(row[6].strftime('%x'))
        cursor.close()
        db.close()

        odu_trap_detail = {'success': 0, 'output': {'graph': [normal, inforamtional,
                                                              minor, major, critical], 'timestamp': time_stamp}}
        html.write(str(odu_trap_detail))
    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()


def idu_outage_graph(h):
    """

    @param h:
    @return: This function return the idu outage graph information.
    @rtype: dictionary
    @requires: html object
    @note: This function return the idu outage graph information of last 10 days and that inforamtion pass on js file for graph showing.
    """
    global html
    html = h
    date_days = []  # this list store the days information with date.
    up_state = []  # Its store the total up state of each day in percentage.
    down_state = []
    # Its store the total down state of each day in percentage.
    output_dict = {}  # its store the actual output for display in graph.
    ip_address = None  # default value of ip address
    host_id = html.var("host_id")  # take host id from js side
    ip_address = html.var('ip_address')  # take ip_address from js side
    current_date = datetime.date(datetime.now())
    current_datetime = datetime.strptime(str(current_date + timedelta(
        days=-10)) + " 00:00:00", '%Y-%m-%d %H:%M:%S')  # convert the string in  datetime.
    last_datetime = datetime.strptime(
        str(current_date) + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    temp_date = last_datetime
    try:
        # connection from mysql
        db, cursor = mysql_connection('nms2')
        if db == 1:
            raise SelfException(cursor)

        sql = "SELECT  nagios_hosts.address,nagios_statehistory.state_time,nagios_statehistory.state\
            FROM nagios_hosts INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id\
           where nagios_statehistory.state_time between '%s'  and '%s' and nagios_hosts.address='%s'\
            order by nagios_statehistory.state_time desc" % (current_datetime, last_datetime, ip_address)

        # Execute the query.
        cursor.execute(sql)
        result = cursor.fetchall()

        for i in range(10):
            flag = 0
            total_down_time = 0
            total_up_time = 0
            temp_down_time = ''
            temp_up_time = ''
            for row in result:
                if (temp_date + timedelta(days=-(i + 1))) <= row[1] <= (temp_date + timedelta(days=-(i))):
                    flag = 1
                    if row[2] == 1:
                        if temp_down_time == '':
                            temp_down_time = row[1]
                        else:
                            total_down_time += (temp_down_time - row[1]
                                               ).days * 1440 + (temp_down_time - row[1]).seconds / 60
                    else:
                        if temp_up_time == '':
                            temp_up_time = row[1]
                        else:
                            total_up_time += (temp_up_time - row[1]
                                             ).days * 1440 + (temp_up_time - row[1]).seconds / 60

            date_days.append(
                (temp_date + timedelta(days=-(i))).strftime("%d %B %Y"))

            total = total_up_time + total_down_time

            if flag == 1 and total > 0:
                up_state.append((total_up_time * 100) / float(total))
                down_state.append((total_down_time * 100) / float(total))
            else:
                up_state.append(0)
                down_state.append(0)
            # close the database and cursor connection.
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'up_state': up_state,
                       'down_state': down_state, 'date_days': date_days}
        html.write(str(output_dict))

    # Exception Handling
    except MySQLdb as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
    except SelfException:
        pass
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))
        if db.open:
            cursor.close()
            db.close()
