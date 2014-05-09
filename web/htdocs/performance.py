#!/usr/bin/python2.6

import datetime

import MySQLdb

from lib import *
from nms_config import *

now = datetime.datetime.now()
end_date = now.strftime("%d/%m/%Y")
now = now + datetime.timedelta(days=-7)
start_date = now.strftime("%d/%m/%Y")


def performance_history(h):
    global html
    html = h
    global start_date
    global end_date
    css_list = ["css/style.css", "calendrical/calendrical.css"]
    js_list = ["js/unmp/main/performance.js", "calendrical/calendrical.js"]
    html.new_header("Performance History", "", "", css_list, js_list)
    html.write("<div id=\"host_list_start\">")
    html.write("<table class=addform>")
    html.write(
        "<colgroup><col width=\"250px\"/><col width=\"auto\"/></colgroup>")
    html.write("<tr>")
    html.write("<td> Date Range")
    html.write("</td>")
    html.write(
        "<td> <input type=\"text\" id=\"start_date\" value=\"%s\"/>&nbsp;To&nbsp; <input type=\"text\" id=\"end_date\" value=\"%s\"/>&nbsp; <input type=\"button\" id =\"submit_date\" class=\"dated\" value=\"submit\"/>" % (
        start_date, end_date))
    html.write("</td>")
    html.write("</tr>")
    html.write("</table>")

    html.write("<div id=\"host_list\">")
    host_history(h)
    html.write("</div>")
    html.write("<div id=\"service_list\"></div>")
    html.new_footer()


def service_status(h):
    global html
    global start_date
    global end_date
    html = h
    temp_service = ""
    ok_time = 0
    crt_time = 0
    ok_time_per = 0
    crt_time_per = 0
    host_time = datetime.datetime.now()
    i = 0
    dic_service = {}
    dic_service = {}
    host_name = html.var("host_name")
    # Create MySQL Connection
    db = MySQLdb.connect("localhost", "root", "root", "nms2")

    # Create Cursor Object to Fetch Data
    cursor = db.cursor()

    # SQL Query for Fething data
    if (html.var("start_date") and html.var("end_date")) != None:
        start_date_list = html.var("start_date").split("/")
        start_date_val = start_date_list[2] + "-" + \
                         start_date_list[1] + "-" + start_date_list[0] + " 00:00:00"

        end_date_list = html.var("end_date").split("/")
        end_date_val = end_date_list[2] + "-" + end_date_list[1] + "-" + \
                       end_date_list[0] + " 23:59:59"
    else:
        start_date_list = (start_date).split("/")
        start_date_val = start_date_list[2] + "-" + start_date_list[
            1] + "-" + start_date_list[0] + " 00:00:00"
        end_date_list = (end_date).split("/")
        end_date_val = end_date_list[2] + "-" + end_date_list[1] + "-" + \
                       end_date_list[0] + " 23:59:59"

    sql_service = "SELECT nagios_services.display_name As Service,nagios_hosts.display_name AS Host,nagios_statehistory.state_time,nagios_statehistory.state,nagios_statehistory.output FROM nagios_services INNER JOIN nagios_hosts ON nagios_services.host_object_id=nagios_hosts.host_object_id INNER JOIN nagios_statehistory ON nagios_services.service_object_id=nagios_statehistory.object_id where((nagios_hosts.display_name= '%s') and (nagios_statehistory.state_time between '%s' and '%s'))  ORDER BY nagios_hosts.display_name,nagios_services.display_name, nagios_statehistory.state_time desc " % (
    host_name, start_date_val, end_date_val)
    # Execute Query
    cursor.execute(sql_service)
    result = cursor.fetchall()
    html.write("<table class=\"addform\">")
    html.write(
        "<colgroup><col width=\"250px\"/><col width=\"auto\"/></colgroup>")
    html.write("<tr>")
    html.write("<th>Service Name")
    html.write("</th>")
    html.write("<th>Performance Meter")
    html.write("</th>")
    html.write("</tr>")
    all_i = 0
    for service, host, time, status, output in result:
        if service != temp_service and i != 0:
            all_i += 1
            dic_service = {temp_service: {"ok_time": ok_time,
                                          "crit_time": crt_time}}
            total_time = ok_time + crt_time
            ok_time_per = (float(ok_time) / float(total_time)) * 100.0
            crt_time_per = (float(crt_time) / float(total_time)) * 100.0
            if all_i % 2 == 0:
                html.write("<tr class='even'>")
            else:
                html.write("<tr>")
            html.write("<td>%s" % temp_service)
            html.write("</td>")
            html.write("<td><div class=\"bar-main\">")
            if crt_time_per == ok_time_per:
                crt_time_per = ok_time_per = 50
            if crt_time_per < 15:
                if crt_time_per == 0:
                    ok_time_per = 100
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%% OK</div></div><div class=\"bar-second\"></div></div>" % (
                    ok_time_per))
            elif crt_time_per >= 15 and crt_time_per <= 30:
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%% OK</div></div><div class=\"bar-second\">%.2f%%</div></div>" % (
                        ok_time_per, crt_time_per))
            else:
                if ok_time_per < 15:
                    if ok_time_per == 0:
                        crt_time_per = 100
                    html.write(
                        "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                    html.write(
                        "<div class=\"bar-second\"></div></div><div class=\"bar-second\">%.2f%% Critical</div></div>" % (
                        crt_time_per))
                elif ok_time_per >= 15 and ok_time_per <= 30:
                    html.write(
                        "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                    html.write(
                        "<div class=\"bar-second\">%.2f%%</div></div><div class=\"bar-second\">%.2f%% Critical</div></div>" % (
                            ok_time_per, crt_time_per))
                else:
                    html.write(
                        "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                    html.write(
                        "<div class=\"bar-second\">%.2f%% OK</div></div><div class=\"bar-second\">%.2f%% Critical</div></div>" % (
                            ok_time_per, crt_time_per))

            html.write("</td>")
            html.write("</tr>")
            ok_time = 0
            crt_time = 0
            host_time = datetime.datetime.now()
            ok_time = 0
            crt_time = 0
            host_time = datetime.datetime.now()
        temp_service = service
        if status == 0:
            j = host_time - time
            ok_time += (j.days * 1440) + (j.seconds / 60)
        else:
            j = host_time - time
            crt_time += (j.days * 1440) + (j.seconds / 60)
        i += 1
        host_time = time
    if i > 0:
        total_time = ok_time + crt_time
        ok_time_per = (float(ok_time) / float(total_time)) * 100.0
        crt_time_per = (float(crt_time) / float(total_time)) * 100.0

        if all_i % 2 == 1:
            html.write("<tr class='even'>")
        else:
            html.write("<tr>")
        html.write("<td>%s" % temp_service)
        html.write("</td>")
        html.write("<td><div class=\"bar-main\">")
        if crt_time_per == ok_time_per:
            crt_time_per = ok_time_per = 50
        if crt_time_per < 15:
            if crt_time_per == 0:
                ok_time_per = 100
            html.write(
                "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
            html.write(
                "<div class=\"bar-second\">%.2f%% OK</div></div><div class=\"bar-second\"></div></div>" % (ok_time_per))
        elif crt_time_per >= 15 and crt_time_per <= 30:
            html.write(
                "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
            html.write("<div class=\"bar-second\">%.2f%% OK</div></div><div class=\"bar-second\">%.2f%%</div></div>" %
                       (ok_time_per, crt_time_per))
        else:
            if ok_time_per < 15:
                if ok_time_per == 0:
                    crt_time_per = 100
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\"></div></div><div class=\"bar-second\">%.2f%% Critical</div></div>" % (
                    crt_time_per))
            elif ok_time_per >= 15 and ok_time_per <= 30:
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%%</div></div><div class=\"bar-second\">%.2f%% Critical</div></div>" % (
                        ok_time_per, crt_time_per))
            else:
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%% OK</div></div><div class=\"bar-second\">%.2f%% Critical</div></div>" % (
                        ok_time_per, crt_time_per))
        html.write("</td>")
        html.write("</tr>")
    else:
        html.write("<tr><td colspan=\"2\"> No Service Exist</td></tr>")
    html.write("</table>")
    cursor.close()
    db.close()


def host_history(h):
    global html
    global start_date
    global end_date
    html = h
    temp_host = ""
    temp_service = ""
    ok_time = 0
    crt_time = 0
    host_time = datetime.datetime.now()
    i = 0
    dic = {}
    dic_service = {}
    # Create MySQL Connection
    db = MySQLdb.connect("localhost", "root", "root", "nms2")

    # Create Cursor Object to Fetch Data
    cursor = db.cursor()
    current_host_list = ""
    history_host_list = ""
    # SQL Query for Fething data
    ##    sql_host_list = "SELECT DISTINCT host_object_id FROM nagios_hoststatus"
    ##    sql_hiostory_host_list = "SELECT DISTINCT object_id FROM `nagios_statehistory"
    ##    cursor.execute(sql_host_list)
    ##    history_host_list=cursor.fetchall()
    ##    cursor.close()
    ##    cursor=db.cursor()
    ##    cursor.execute(sql_hiostory_host_list)
    ##    current_host_list=cursor.fetchall()
    ##    cursor.close()
    ##    for i in current_host_list:
    ##        if i in history_host_list:
    ##            html.write(str(i)+' Exists<br/>')
    ##        else:
    ##            html.write(str(i)+'<br/>')
    if (html.var("start_date") and html.var("end_date")) != None:
        start_date_list = html.var("start_date").split("/")
        start_date_val = start_date_list[2] + "-" + start_date_list[
            1] + "-" + start_date_list[0] + " 00:00:00"

        end_date_list = html.var("end_date").split("/")
        end_date_val = end_date_list[2] + "-" + end_date_list[1] + "-" + \
                       end_date_list[0] + " 23:59:59"

    else:
        start_date_list = (start_date).split("/")
        start_date_val = start_date_list[2] + "-" + start_date_list[
            1] + "-" + start_date_list[0] + " 00:00:00"
        end_date_list = (end_date).split("/")
        end_date_val = end_date_list[2] + "-" + end_date_list[1] + "-" + \
                       end_date_list[0] + " 23:59:59"
    sql = "SELECT nagios_hosts.display_name, nagios_statehistory.output, nagios_statehistory.state_time ,nagios_statehistory.state \
    FROM nagios_hosts INNER JOIN nagios_hoststatus ON nagios_hosts.host_object_id = nagios_hoststatus.host_object_id \
    INNER JOIN nagios_statehistory ON nagios_statehistory.object_id = nagios_hosts.host_object_id \
    where nagios_statehistory.state_time between '%s' and '%s'\
    order by nagios_hosts.display_name,nagios_statehistory.state_time desc " % (start_date_val, end_date_val)
    ##    cursor=db.cursor()
    # Execute Query
    cursor.execute(sql)

    # fetch data
    result = cursor.fetchall()
    html.write("<div id=\"host_start_list\">")
    html.write("<table class=addform>")
    html.write(
        "<colgroup><col width=\"250px\"/><col width=\"auto\"/></colgroup>")
    html.write("<tr>")
    html.write("<tr>")
    html.write("<th>HostName")
    html.write("</th>")
    html.write("<th>Performance Meter")
    html.write("</th>")
    html.write("</tr>")
    all_i = 0
    for host, output, time, status in result:
        if host != temp_host and i != 0:
            all_i += 1
            if all_i % 2 == 0:
                html.write("<tr class='even'>")
            else:
                html.write("<tr>")
            total_time = ok_time + crt_time
            ok_time_per = (float(ok_time) / float(total_time)) * 100.0
            crt_time_per = (float(crt_time) / float(total_time)) * 100.0
            html.write(
                "<td class=\"hostname\" style=\"cursor:pointer;\">%s" % temp_host)
            html.write("</td>")
            html.write("<td><div class=\"bar-main\">")
            if crt_time_per == ok_time_per:
                crt_time_per = ok_time_per = 50
            if crt_time_per < 15:
                if crt_time_per == 0:
                    ok_time_per = 100
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%% Up</div></div><div class=\"bar-second\" title=\"%s%% Down\"></div></div>" %
                    (ok_time_per, crt_time_per))
            elif crt_time_per >= 15 and crt_time_per <= 30:
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%% Up</div></div><div class=\"bar-second\">%.2f%%</div></div>" % (
                        ok_time_per, crt_time_per))
            else:
                if ok_time_per < 15:
                    if ok_time_per == 0:
                        crt_time_per = 100
                    html.write(
                        "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                    html.write(
                        "<div class=\"bar-second\"></div></div><div class=\"bar-second\">%.2f%% Down</div></div>" % (
                        crt_time_per))
                elif ok_time_per >= 15 and ok_time_per <= 30:
                    html.write(
                        "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                    html.write(
                        "<div class=\"bar-second\">%.2f%%</div></div><div class=\"bar-second\">%.2f%% Down</div></div>" % (
                            ok_time_per, crt_time_per))
                else:
                    html.write(
                        "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                    html.write(
                        "<div class=\"bar-second\">%.2f%% Up</div></div><div class=\"bar-second\">%.2f%% Down</div></div>" % (
                            ok_time_per, crt_time_per))

            html.write("</td>")
            html.write("</tr>")
            ok_time = 0
            crt_time = 0
            host_time = datetime.datetime.now()
        temp_host = host
        if status == 0:
            j = host_time - time
            ok_time += (j.days * 1440) + (j.seconds / 60)
        else:
            j = host_time - time
            crt_time += (j.days * 1440) + (j.seconds / 60)
        i += 1
        host_time = time
    if i > 0:
        total_time = ok_time + crt_time
        ok_time_per = (float(ok_time) / float(total_time)) * 100.0
        crt_time_per = (float(crt_time) / float(total_time)) * 100.0

        if all_i % 2 == 1:
            html.write("<tr class='even'>")
        else:
            html.write("<tr>")

        html.write(
            "<td class=\"hostname\" style=\"cursor:pointer;\">%s" % temp_host)
        html.write("</td>")
        html.write("<td><div class=\"bar-main\">")
        if crt_time_per == ok_time_per:
            crt_time_per = ok_time_per = 50
        if crt_time_per < 15:
            if crt_time_per == 0:
                ok_time_per = 100
            html.write(
                "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
            html.write(
                "<div class=\"bar-second\">%.2f%% Up</div></div><div class=\"bar-second\"></div></div>" % (ok_time_per))
        elif crt_time_per >= 15 and crt_time_per <= 30:
            html.write(
                "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
            html.write("<div class=\"bar-second\">%.2f%% Up</div></div><div class=\"bar-second\">%.2f%%</div></div>" %
                       (ok_time_per, crt_time_per))
        else:
            if ok_time_per < 15:
                if ok_time_per == 0:
                    crt_time_per = 100
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\"></div></div><div class=\"bar-second\">%.2f%% Down</div></div>" % (
                    crt_time_per))
            elif ok_time_per >= 15 and ok_time_per <= 30:
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%%</div></div><div class=\"bar-second\">%.2f%% Down</div></div>" %
                    (ok_time_per, crt_time_per))
            else:
                html.write(
                    "<div class=\"bar-first\" style=\"width:%.2f%%;\">" % (ok_time_per))
                html.write(
                    "<div class=\"bar-second\">%.2f%% Up</div></div><div class=\"bar-second\">%.2f%% Down</div></div>" %
                    (ok_time_per, crt_time_per))
        html.write("</td>")
        html.write("</tr>")
    else:
        html.write("<tr><td colspan=\"2\"> No Service Exist</td></tr>")
    html.write("</table>")
    html.write("</div>")
    cursor.close()
    db.close()
