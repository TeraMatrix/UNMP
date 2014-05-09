#!/usr/bin/python2.6

######################################################################################
# Author			:	Rajendra Sharma
# Project			:	UNMP
# Version			:	0.1
# File Name			:	Trap_inforamtion.py
# Creation Date			:	13-September-2011
# Purpose			:	This file display the Trap information for all devices.
# Copyright (c) 2011 Codescape Consultant Private Limited

##########################################################################

# success 0 means No error
# success 1  Exception or Error
# success 2 means some mysql error(services not running,connection not created)


## import module
from datetime import datetime
from datetime import timedelta

import MySQLdb
from mysql_collection import mysql_connection

# Exception class for own exception handling.


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


def start_page(h):
    """

    @param h:
    @return: this function display the html page for trap information.
    @rtype: return type html page.
    @requires: Its take html object as a argument.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 13 sept 2011
    @note: this function display the trap information page on browser.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    css_list = ["css/custom.css", "css/demo_table_jui.css",
                "css/jquery-ui-1.8.4.custom.css", "facebox/facebox.css", "css/calendrical.css"]
    js_list = [
        "facebox/facebox.js", "js/unmp/main/eventDetails.js"
        "js/lib/main/jquery.dataTables.min.js", "js/lib/main/calendrical.js"]
    h.new_header("Events Details", "", "", css_list, js_list)
    ip_address = html.var("ip_address")
    now = datetime.now()
    odu_end_date = now.strftime("%d/%m/%Y")
    odu_end_time = now.strftime("%H:%M")
    now = now + timedelta(minutes=-60)
    odu_start_date = now.strftime("%d/%m/%Y")
    odu_start_time = now.strftime("%H:%M")

    html.write("<div id=\"top_image_div\">")
    html.write(
        "<table class=\"addform\" style=\"border:0px None\"><tr class=\"odd\">")

    html.write("<td style=\"width:150px; font-weight: bold;\">Alarm Type")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<input type=\"radio\" value=\"1\" name=\"option\" id=\"option1\" checked=\"checked\" class=\"table_option\" width=\"12px\"/>")
    html.write("</td>")

    html.write("<td>")
    html.write("<label for=\"option1\" width=\"25px\">Current</label>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<input type=\"radio\" value=\"2\" name=\"option\" id=\"option2\" class=\"table_option\" width=\"12px\"/>")
    html.write("</td>")

    html.write("<td>")
    html.write("<label for=\"option2\" width=\"25px\">Clear</label>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<input type=\"radio\" value=\"3\" name=\"option\" id=\"option3\" class=\"table_option\" width=\"12px\" />")
    html.write("</td>")

    html.write("<td>")
    html.write("<label for=\"option3\" width=\"25px\" >History</label>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<input class=\"yo-button yo-small\" type=\"button\" value=\"Advanced Search\" id=\"btn_filter\" name=\"btn_filter\" style=\"margin:10px 20px 10px 200px;\"/>")
    html.write("</td>")

    html.write("<td style=\"vertical-align:middle;\">")
    html.write(
        "<div class=\"trap_select_option_div\" style=\" width: 130px;\" id=\"informational_div\">")
    html.write(
        "<img src=\"images/lb.png\"  name=\"select_option_div\" alt=\"Informational\" title=\"Informational\" style=\"width:12px\" class=\"imgbutton\" /><span class=\"inactive-linkclass\" style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand;\">Informational</span>")
    html.write("</div>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<div class=\"trap_select_option_div\" style=\" width:100px;\" id=\"normal_div\">")
    html.write(
        "<img src=\"images/gr.png\"  name=\"select_option_div\" alt=\"Normal\" title=\"Normal\" style=\"width:12px\" class=\"imgbutton\"/><span class=\"inactive-linkclass\" style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand; \" >Normal</span>")
    html.write("</div>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<div class=\"trap_select_option_div\" style=\" width:100px;\" id=\"minor_div\">")
    html.write(
        "<img src=\"images/yel.png\" alt=\"Minor\" name=\"select_option_div\" title=\"Minor\" class=\"imgbutton\" style=\"width:12px\" /><span class=\"inactive-linkclass\" style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand; \">Minor</span>")
    html.write("</div>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<div class=\"trap_select_option_div\" style=\" width:100px;\" id=\"major_div\">")
    html.write(
        "<img src=\"images/or.png\" alt=\"Major\" name=\"select_option_div\" title=\"Major\"  class=\"imgbutton\" style=\"width:12px\"  /><span style=\"line-height:20px; padding:0px 12px;cursor:pointer;cursor:hand; \">Major</span>")
    html.write("</div>")
    html.write("</td>")

    html.write("<td>")
    html.write(
        "<div class=\"trap_select_option_div\" style=\" width:110px;\" id=\"critical_div\">")
    html.write(
        "<img src=\"images/red.png\" alt=\"Critical\" name=\"select_option_div\" title=\"Critical\" class=\"imgbutton\" style=\"width:12px\"/><span  style=\"line-height:20px; padding:0px 12px; cursor:pointer;cursor:hand; \">Critical</span>")
    html.write("</div>")
    html.write("</td>")

    html.write("</tr></table>")
    html.write("</div>")

    html.write("<div id=\"main_div\">")
    trap_status = html.var('trap_status')
    html_form = '<form id=\"alarm_info_form\" action=\"alarm_current_detail.py\" method=\"get\" >\
		    <div>\
		        <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
		            <tr>\
		                <th id=\"form_title\" class=\"cell-title\">Events Search</th>\
		            </tr>\
		        </table>\
			<input type=\"hidden\" value=\"%s\"  id=\"trap_status_id\"/>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"agentId\">Agent ID</label>\
		            <input type=\"text\" id=\"agentId\" name=\"agent_id\" value=\"%s\"/>\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"eventId\">Event ID</label>\
		            <input type=\"text\" id=\"eventId\" name=\"eventId\"/>\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"eventType\">Event Type</label>\
		            <input type=\"text\" id=\"eventType\" name=\"eventType\"/>\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"M_obj\">Manage Object ID</label>\
		            <input type=\"text\" id=\"M_obj\" name=\"M_obj\"/>\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"M_name\">Manage Object Name</label>\
		            <input type=\"text\" id=\"M_name\" name=\"M_name\"/>\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"camponent_id\">Component ID</label>\
		            <input type=\"text\" id=\"camponent_id\" name=\"camponent_id\"/>\
		        </div>\
		        <div class=\"row-elem\">\
			  <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"30%%\">\
			    <tr>\
			    <td style=\"vertical-align:middle;\">\
				    <label class=\"lbl lbl-big\" for=\"serevity\">Severity</label>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <input type=\"checkbox\" name=\"serevity\" id=\"serevity1\" value=\"1\" />\
			    </td >\
			    <td style=\"vertical-align:middle;\">\
				    <label for=\"serevity1\" >Informational</label>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <input type=\"checkbox\" name=\"serevity\" id=\"serevity2\" value=\"2\" />\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <label for=\"serevity2\" >Normal</label>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <input type=\"checkbox\" name=\"serevity\" value=\"3\" id=\"serevity3\"/>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <label for=\"serevity3\" >Minor</label>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <input type=\"checkbox\" name=\"serevity\" value=\"4\" id=\"serevity4\"/>\
			    </td style=\"vertical-align:middle;\">\
			    <td style=\"vertical-align:middle;\">\
				    <label for=\"serevity4\" >Major</label>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
			 	    <input type=\"checkbox\" name=\"serevity\" value=\"5\" id=\"serevity5\"/>\
			    </td>\
			    <td style=\"vertical-align:middle;\">\
				    <label for=\"serevity5\" >Critical</label>\
			   </td>\
			   </tr>\
			</table>\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl lbl-big\" for=\"event_date\">Date</label>\
			    <input type=\"textbox\" name=\"event_start_date\" value=\"%s\" id=\"event_start_date\" style=\"width:80px;\"/>\
			    <input type=\"textbox\" name=\"event_start_time\" value=\"%s\" id=\"event_start_time\" style=\"width:50px;\"/>\
			    <lable>--</lable>\
			    <input type=\"textbox\" name=\"event_end_date\" value=\"%s\" id=\"event_end_date\" style=\"width:80px;\"/>\
			    <input type=\"textbox\" name=\"event_end_time\" value=\"%s\" id=\"event_end_time\" style=\"width:50px;\"/>\
		        </div>\
		        <div class=\"row-elem\">\
			    <input type=\"submit\" name=\"submit\" class=\"yo-small yo-button\" id=\"submit_html\" value=\"submit\" />\
			    <input type=\"button\" class=\"yo-small yo-button\"  id=\"btn_hide\" name=\"btn_hide\" value=\"Hide Search\" />\
			</div></div></form>' % (
    trap_status, ("" if ip_address == "" or ip_address == None else ip_address.replace("-", "")), odu_start_date,
    odu_start_time, odu_end_date, odu_end_time)
    html.write(str(html_form))
    html.write("<div id=\"trap_data_table\">\
	<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" id=\"trap_detail\" class=\"display\">\
	</table></div>\
	<div id=\"detail_info_id\"></div></div>")
    html.new_footer()


def trap_filter_function(h):
    """

    @param h:
    @return: this function return the filter result of trap information.
    @rtype: dictinoary.
    @requires: Its required a html object that provide the trap_information page information.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 13 sept 2011
    @note: this function filter the result according to user action and show the result in table form.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    image_dic = {0: "images/gr.png", 1: "images/lb.png", 2: "images/gr.png", 3:
        "images/yel.png", 4: "images/or.png", 5: "images/red.png"}
    image_title_name = {0: "Normal", 1: "Informational", 2: "Normal",
                        3: "Minor", 4: "Major", 5: "Critical"}
    option = html.var(
        "option")  # option take (current,clear,history)status number by html object(Trap_information page).
    event_id = html.var(
        "event_id")  # event_id take Event Type name id by html object(Trap_information page).
    event_type = html.var(
        "eventType")  # event_type take Event Type name name by html object(Trap_information page).
    m_object = html.var(
        "M_obj")  # M_object take Manage object id by html object(Trap_information page).
    m_name = html.var(
        "M_name")  # M_name take Manage object name by html object(Trap_information page).
    trap_ip = html.var(
        "ip")  # trap_ip take trap ip by html object(Trap_information page).
    camponent_id = html.var(
        "camponent_id")  # camponent_id take camponent id by html object(Trap_information page).
    serevity1 = html.var(
        "serevity1")  # serevity variable take serevity value by html object(Trap_information page).
    serevity2 = html.var("serevity2")
    serevity3 = html.var("serevity3")
    serevity4 = html.var("serevity4")
    serevity5 = html.var("serevity5")
    agent_id = html.var("agent_id")
    last_time = html.var("last_execution_time")
    time_interval = html.var("time_interval_value")
    start_date = html.var('event_start_date')
    start_time = html.var('event_start_time')
    end_date = html.var('event_end_date')
    end_time = html.var('event_end_time')
    start_datetime = datetime.strptime(
        (start_date + start_time), '%d/%m/%Y%H:%M')
    end_datetime = datetime.strptime((end_date + end_time), '%d/%m/%Y%H:%M')
    sql = ""  # its store the sql query for filter the database.
    sql_1 = ""
    sql_i = 1  # sql_i make the sql query for trap field.
    sql_j = 1  # sql+j make the fields for serevity value.
    primary_key_id = ""  # it store the primary_key_id for particular table according to selected option(ratio button on the trap information page.)
    table_name = ""  # it store the table name  for particular table according to selected option(ratio button on the trap information page.)
    if (event_id) != None:
        if sql_i > 1:
            sql += " and"
        sql += " trap_event_id like '%" + event_id + "%'"
        sql_i += 1
    if (event_type) != None:
        if sql_i > 1:
            sql += " and"
        sql += " trap_event_type like '%" + event_type + "%'"
        sql_i += 1
    if (m_object) != None:
        if sql_i > 1:
            sql += " and"
        sql += " manage_obj_id like '%" + m_object + "%'"
        sql_i += 1
    if (m_name) != None:
        if sql_i > 1:
            sql += " and"
        sql += " manage_obj_name like '%" + m_name + "%'"
        sql_i += 1
    if (camponent_id) != None:
        if sql_i > 1:
            sql += " and"
        sql += " component_id like '%" + camponent_id + "%'"
        sql_i += 1

    if option == "1":                     # 1 Stand for Current Alarm Details
        table_name = "trap_alarm_current"
        primary_key_id = "trap_alarm_current_id"
    if option == "2":                        # 2 Stand for Clear Alarm Details
        table_name = "trap_alarm_clear"
        primary_key_id = "trap_alarm_clear_id"
    if option == "3":                    # 3 Stand for All alarm details
        table_name = "trap_alarms"
        primary_key_id = "trap_alarm_id"

    if (serevity1) != None:
        if sql_j > 1:
            sql_1 += " or"
        sql_1 += " serevity like '%" + serevity1 + "%'"
        sql_j += 1
    if (serevity2) != None:
        if sql_j > 1:
            sql_1 += " or"
        sql_1 += " serevity like '%" + serevity2 + "%'"
        sql_1 += " or"
        sql_1 += " serevity like '%" + (0 if serevity2 == 2 else 'None') + "%'"
        sql_j += 1
    if (serevity3) != None:
        if sql_j > 1:
            sql_1 += " or"
        sql_1 += " serevity like '%" + serevity3 + "%'"
        sql_j += 1
    if (serevity4) != None:
        if sql_j > 1:
            sql_1 += " or"
        sql_1 += " serevity like '%" + serevity4 + "%'"
        sql_j += 1
    if (serevity5) != None:
        if sql_j > 1:
            sql_1 += " or"
        sql_1 += " serevity like '%" + serevity5 + "%'"
        sql_j += 1

    if sql_j > 1:
        sql = sql + " and (" + sql_1 + ")"

    if agent_id == "" or agent_id == None:
        sql = "SELECT ta." + primary_key_id + ",ta.event_id,ta.agent_id,ta.trap_receive_date,ta.serevity,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,hosts.host_alias From " + \
              table_name + \
              " as ta INNER JOIN hosts ON ta.agent_id=hosts.ip_address WHERE " + \
              sql
    else:
        if "-" in agent_id:
            sql = "SELECT ta." + primary_key_id + ",ta.event_id,ta.agent_id,ta.trap_receive_date,ta.serevity,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,hosts.host_alias From " + table_name + \
                  " as ta INNER JOIN hosts ON ta.agent_id=hosts.ip_address WHERE agent_id='" + \
                  agent_id.replace("-", "") + "' and " + sql
        else:
            sql = "SELECT " + primary_key_id + ",ta.event_id,ta.agent_id,ta.trap_receive_date,ta.serevity,ta.trap_event_id,ta.trap_event_type,hosts.device_type_id,hosts.host_alias From " + table_name + \
                  " as ta INNER JOIN hosts ON ta.agent_id=hosts.ip_address WHERE agent_id like  '" + \
                  agent_id + "%' and " + sql

    if time_interval is not None and last_time is not None:
        sql += " and ta.timestamp < '%s' and ta.timestamp >= '%s'" % (
            datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes=1), last_time)
    try:
        # database connection and cursor object creation.
        db, cursor = mysql_connection('nms_sample')
        # check the connection created or not.
        if db == 1:
            raise SelfException(cursor)
        sql += "AND ta.timestamp BETWEEN '%s' AND '%s' order by trap_receive_date desc" % (
            start_datetime, end_datetime)
        cursor.execute(sql)
        result = cursor.fetchall()
        result_len = len(result)
        data_table = []
        i = 0
        if result is not None:
            if len(result) > 0:
                for row in result:
                    i += 1
                    img = '<label style="display:none;">%s</label><img src="%s" alt="%s" title="%s" class="imgbutton" style="width:12px" onclick="alarmDetail(\'%s\')"/>' % (
                        row[4], image_dic[int(row[4])], image_title_name[int(row[4])], image_title_name[int(row[4])],
                        row[0])
                    datetime_object = datetime.strptime(
                        row[3], '%a %b %d %H:%M:%S %Y')
                    data_table.append([img, datetime_object.strftime("%d %B %Y"), datetime_object.strftime(
                        "%I:%M:%S %p"), row[7], row[8], row[1], row[2], row[5], row[6]])

        else:
            data_table = ""
        cursor.close()
        db.close()
        output_dict = {'success': 0, 'data_table': data_table,
                       'last_execution_time': str(datetime.now())}
        html.write(str(output_dict))

    # Exception Handling
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        pass
    except AttributeError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except NameError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except MySQLdb as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
    except DatabaseError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()


def trap_detail_information(h):
    """

    @param h:
    @return: this function provide the information in detail of particular trap.
    @rtype: dictinoary.
    @requires: Its required a html object that provide the trap_information page information.
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 13 sept 2011
    @note: this function detail trap informaton according to user clickable action on the table.
    @organisation: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    global html
    html = h
    option = html.var(
        "option")  # option take (current,clear,history)status number by html object(Trap_information page).
    trap_id = html.var(
        "trap_id")  # trap_id take trap id by html object(Trap_information page).
    image_title_name = {0: "Normal", 1: "Informational", 2: "Normal",
                        3: "Minor", 4: "Major", 5: "Critical"}
    try:

        # create the data base and cursor object.
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)

        if option == 1 or option == "1":
            table_name = "trap_alarm_current"
            primary_key_id = "trap_alarm_current_id"

        elif option == 2 or option == "2":
            table_name = "trap_alarm_clear"
            primary_key_id = "trap_alarm_clear_id"

        elif option == 3 or option == "3":
            primary_key_id = "trap_alarm_id"
            table_name = "trap_alarms"

        sql = "SELECT * FROM %s WHERE %s='%s'" % (
            table_name, primary_key_id, trap_id)
        # html.write(str(sql))
        cursor.execute(sql)
        result = cursor.fetchone()

        cursor.close()
        db.close()
        html.write("<div id=\"login_div\">")

        html.write("<table class=\"addform\" style=\"margin-left: 5px;\">")

        html.write("<tr>")
        html.write("<th colspan=\"2\">")
        html.write("Alarm Details")
        html.write("</th>")
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Event Name</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[1])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Event OId</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[2])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Agent Id</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[3])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Up Time</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[4])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Receive Date</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[5])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Severity</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % image_title_name[result[6]])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Event ID</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[7])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Event Type</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[8])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Manage Object Id</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[9])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Manage Object Name</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[10])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Component Id</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[11])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Event Ip</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[12])
        html.write("</tr>")

        html.write("<tr>")
        html.write("<td>")
        html.write("<b>Description</b>")
        html.write("</td>")
        html.write("<td>%s</td>" % result[13])
        html.write("</tr>")

        html.write("</table>")
        html.write("</div>")

    # Exception Handling
    except SelfException:
        if db.open:
            cursor.close()
            db.close()
        pass
    except AttributeError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except NameError as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    except MySQLdb as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {'success': 1, 'output': str(e)}
        html.write(str(output_dict))
    except Exception as e:
        if db.open:
            cursor.close()
            db.close()
        output_dict = {"success": 1, 'output': str(e)}
        html.write(str(output_dict))
    finally:
        if db.open:
            cursor.close()
            db.close()

#
# def page_tip_event_details(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_event_details.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
