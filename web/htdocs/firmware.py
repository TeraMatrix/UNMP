#!/usr/bin/python2.6

import os.path
import os

from xml.dom.minidom import parse

from lib import *
import nms_config


def update(h):
    global html
    sitename = __file__.split("/")[3]
    path = "/omd/sites/%s/share/check_mk/web/htdocs/xml/shyamdevices.xml" % sitename
    html = h
    i = 0
    css_list = []
    js_list = ["js/unmp/main/firmware.js"]
    header_btn = ""
    html.new_header("Firmware Update", "", header_btn, css_list, js_list)
    html.write(
        "<table class=\"addform\" style=\"border:0px none;\"><colgroup><col width=\"140px\"/><col width=\"auto\"/></colgroup>")
    html.write(
        "<tr><td>Select Devices:</td><td><select name=\"select_devices\" id=\"select_devices\">")
    if (os.path.isfile(path)):
        f = parse(path)
        try:
            for node in f.getElementsByTagName('device'):
                if (i == 0):
                    html.write(
                        "<option selected=\"true\" value=\"NoDevice\">-- Select Device Type --</option>")
                i += 1
                html.write("<option value=\"%s\">%s</option>" % (
                    node.getAttribute('id'), node.getAttribute('name')))
            if (i == 0):
                html.write(
                    "<option selected=\"true\" value=\"\">-- No Device Found --</option>")
        except Exception, e:
            html.write(
                "<option selected=\"true\" value=\"\">-- No Device Found --</option>")
    else:
        html.write(
            "<option selected=\"true\" value=\"\">-- No Device Found --</option>")
    html.write(
        "</select></td><td rowspan=\"2\"><div id=\"image_load\"></div></td></tr>")
    html.write("<tr><td>")
    html.write("Choose Firmware:")
    html.write("</td><td>")
    html.write("<input type=\"file\" name=\"firmware\" id=\"firmware\" />")
    html.write("<label class=\"error file-error\" style=\"display:none;\">Please Choose Frimware file</label>")
    html.write("</td></tr>")
    html.write("</table>")
    html.write("<div id=\"device_list\">")
    device_table(h)
    html.write("</div>")
    html.write(
        "<div class=\"loading\" ><img src='images/loading.gif' alt=''/></div>")
    html.new_footer()


def device_table(h):
    global html
    html = h
    data_str = ""
    device_type = html.var("device_type")
    data_str += "<div><table class=\"addform\">"
    data_str += "<colgroup><col width=\"1%\"/><col width=\"20%\"/><col width=\"20%\"/><col width=\"20%\"/><col width=\"auto\"/></colgroup>"
    data_str += "<tr>"
    data_str += "<th><input type=\"checkbox\" name=\"check_all\"/></th>"
    data_str += "<th>HostName</th>"
    data_str += "<th>Address</th>"
    data_str += "<th>Device Type</th>"
    data_str += "<th></th>"
    data_str += "</tr>"

    i = 0
    # SQL Query for Fething data
    if device_type is not None:
        # Create MySQL Connection
        db = nms_config.open_database_connection()

        # Create Cursor Object to Fetch Data
        cursor = db.cursor()

        sql = "SELECT hostname,ipaddress,devicetype FROM nms_devices where devicetype='%s';" % (
            device_type)

        # Execute Query
        cursor.execute(sql)

        # fetch data
        result = cursor.fetchall()

        for row in result:
            i += 1
            if i % 2 == 0:
                data_str += "<tr class='even'>"
            else:
                data_str += "<tr>"

            data_str += "<td><input type=\"checkbox\" name=\"host\" id=\"host%s\"/>" % i
            data_str += "</td>"
            data_str += "<td>"
            data_str += row[0]
            data_str += "</td>"
            data_str += "<td>"
            data_str += row[1]
            data_str += "</td>"
            data_str += "<td>"
            data_str += row[2]
            data_str += "</td>"
            data_str += "<td><div id=\"loading_host%s\"></div></td>" % i
            data_str += "</tr>"
        cursor.close()
        nms_config.close_connection(db)

    if i == 0:
        data_str += "<tr><td colspan=\"4\"> No Host Found</td></tr>"
    else:
        data_str += "<tr><td colspan=\"4\"><input type=\"button\" id=\"update_btn\" name=\"update_btn\" value=\"Upload File\" /><input type=\"button\" id=\"active_btn\" name=\"active_btn\" value=\"Update & Activate\" style=\"display:none;\" /></td></tr>"
    data_str += "</table></div>"
    html.write(data_str)
