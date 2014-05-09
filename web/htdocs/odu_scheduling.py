#!/usr/bin/python2.6

import config
import htmllib
import pprint
import sidebar
import views
import time
import defaults
import os
import cgi
import xml.dom.minidom
import subprocess
import commands
import MySQLdb
import datetime
import urllib2
import base64
import socket
import sys
from lib import *
from nms_config import *
from odu_scheduling_bll import OduSchedulingBll


################################## Scheduling ############################
class OduScheduling(object):
    @staticmethod
    def view_Scheduling_Details(res):
        html_str = '<div>\
                        <table class=\"yo-table\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" >\
                        	<colgroup width="35%"></colgroup>\
 	       			<colgroup width="45%"></colgroup>\
 	       			<colgroup width="20%"></colgroup>\
 	       			<tr class="yo-table-head">\
 	       				<th class=" vertline">Time:</th>\
		    			<th>Devices</th>\
		    			<th>Status</th>\
		    		</tr>'
        if (len(res) == 0):
            html_str += "<tr><td></td><td>No Data Exists</td><td></td></tr>"
            html_str += "</div>"
            return html_str
        #  <img id=\"close_view\" class="img-link" src="images/new/close.png" onclick="back_scheduling_status();" style="float: right; margin: 7px;" original-title="Close"\>\
        for i in range(0, len(res)):
            html_str += '<tr>\
		   <td class=" vertline" align="center">%s</td>\
		   <td class=" vertline" align="center">%s</td>\
		   <td class=" vertline" align="center">%s</td>\
		   </tr>' % (res[i][0], res[i][1], res[i][2])

        html_str += "</div>"
        return html_str

    @staticmethod
    def create_scheduling_form(device_list):
    #<div id=\"notifi_sche_on\" style=\"width:100%;\"></div>\
#    		<h2 style=\"text-align:center\">Scheduled Action Status</h2>\
        html_str = "\
        <div id=\"scheduling_button_div\" style=\"width:30%; float: right; margin: 2% 10% 0% 67%; position: absolute;\">\
		<h2 class=\".fc-header-title\" style=\"text-align:center\" >Scheduled Action Status</h2>\
		<table class=\"display\" name=\"scheduled_action_status_table\" id=\"scheduled_action_status_table\" width=\"100%%\" >\
		</table>\
	</div>\
        <div id=\"calendar\" style=\"position: relative; width:60%; margin:2% 2% 5% 2%;\"></div>"\
            "<div id=\"eventForm\" style=\"display:none;margin:10px;\">"\
            "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" style=\"margin-bottom:0px;\">"\
            "<tr>"\
            "<th id=\"form_title\" class=\"cell-title\">Add/Edit Device Schedules</th>"\
            "</tr></table>"\
            "<form id=\"schedulingForm\">"\
            "<table width=\"100%\">"\
            "<colgroup><col width='15%'/><col width='85%'/></colgroup>"\
            "<tr>"\
            "<td style=\"padding:8px 6px 6px 6px\">Device Type</td>"\
            "<td style=\"padding:3px\">\
						<select id=\"device_select_list\" name=\"device_select_list\">"

        if len(device_list) > 0:
            for i in device_list:
                html_str += '<option value="%s">%s</option>' % (i[0], i[1])
        html_str += "</select>\
					</td></tr>"\
            "<tr>"\
            "<td style=\"padding:6px\" >Event<input type=\"hidden\" id=\"scheduleId\" name=\"scheduleId\" value=\"0\" /></td>"\
            "<td>"\
            "<input type=\"radio\" id=\"radioDown\" name=\"radio\" value=\"Down\" checked>"\
            "<label for=\"radioDown\" style=\"padding-right:6px\" id=\"radioDown_label\">Radio Down</label></input>"\
            "<input type=\"radio\"  id=\"radioUp\" name=\"radio\" value=\"Up\">"\
            "<label for=\"radioUp\" style=\"padding-right:6px\" id=\"radioUp_label\">Radio UP</label></input>"\
            "<input type=\"radio\"  id=\"radioFirmware\" name=\"radio\" value=\"Firmware\">"\
            "<label for=\"radioFirmware\" style=\"padding-right:6px\" id=\"radioFirmware_label\">Firmware Update</label></input>"\
            "</td>"\
            "</tr>"\
            "<tr><td style=\"padding:6px\">Range</td>"\
            "<td>"\
            "<input type=\"text\" id=\"startDate\" name=\"startDate\" style=\"width:70px;\" /> &nbsp; <input type=\"text\" id=\"startTime\" name=\"startTime\" style=\"width:40px;\" />&nbsp; To &nbsp;"\
            "<input type=\"text\" id=\"endDate\" name=\"endDate\"  style=\"width:70px;\" /> &nbsp; <input type=\"text\" id=\"endTime\" name=\"endTime\" style=\"width:40px;\" />"\
            "<label style=\"color:red;display:none;\" id=\"dateError\"> Please enter correct date time range</label>"\
            "</td>"\
            "</tr>"\
            "<tr>"\
            "<td style=\"padding:6px\">Repeat</td>"\
            "<td>"\
            "<input type=\"checkbox\" id=\"repeat\" name=\"repeat\" value=\"1\" />"\
            "</td>"\
            "</tr>"\
            "<tr id=\"trRepeatType\" style=\"display:none;\">"\
            "<td style=\"padding:6px\">Repeat Type</td>"\
            "<td>"\
            "<select id=\"repeatType\" name=\"repeatType\">"\
            "<option value=\"Daily\">Daily</option>"\
            "<option value=\"Weekly\">Weekly</option>"\
            "<option value=\"Monthly\">Monthly</option>"\
            "</select>"\
            "</td>"\
            "</tr>"\
            "<tr id=\"trDay\" style=\"display:none;\">"\
            "<td></td>"\
            "<td>"\
            " <input type=\"checkbox\" id=\"daysun\" name=\"daysun\" value=\"1\" class=\"day\" />"\
            " <label for=\"daysun\">S</label>"\
            " <input type=\"checkbox\" id=\"daymon\" name=\"daymon\" value=\"1\" class=\"day\"/>"\
            " <label for=\"daymon\">M</label>"\
            " <input type=\"checkbox\" id=\"daytue\" name=\"daytue\" value=\"1\" class=\"day\"/>"\
            " <label for=\"daytue\">T</label>"\
            " <input type=\"checkbox\" id=\"daywed\" name=\"daywed\" value=\"1\" class=\"day\"/>"\
            " <label for=\"daywed\">W</label>"\
            " <input type=\"checkbox\" id=\"daythu\" name=\"daythu\" value=\"1\" class=\"day\"/>"\
            " <label for=\"daythu\">T</label>"\
            " <input type=\"checkbox\" id=\"dayfri\" name=\"dayfri\" value=\"1\" class=\"day\"/>"\
            " <label for=\"dayfri\">F</label>"\
            " <input type=\"checkbox\" id=\"daysat\" name=\"daysat\" value=\"1\" class=\"day\"/>"\
            " <label for=\"daysat\">S</label>"\
            "</td>"\
            "</tr>"\
            "<tr id=\"trDate\" style=\"display:none;\">"\
            "<td></td>"\
            "<td style=\"padding:6px\" >Day: <select id=\"dates\" name=\"dates\">"

        for k in range(1, 32):
            html_str += "<option value=\"" + str(k) + "\">" + \
                str(k) + "</option>"

        html_str += "</select></td>"\
            "</tr>"\
            "<tr id=\"trMonth\" style=\"display:none;\">"\
            "<td></td>"\
            "<td>"\
            "Months:<br/>"\
            " <input type=\"checkbox\" id=\"monthjan\" name=\"monthjan\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthjan\">Jan</label>"\
            " <input type=\"checkbox\" id=\"monthfeb\" name=\"monthfeb\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthfeb\">Feb</label>"\
            " <input type=\"checkbox\" id=\"monthmar\" name=\"monthmar\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthmar\">Mar</label>"\
            " <input type=\"checkbox\" id=\"monthapr\" name=\"monthapr\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthapr\">Apr</label>"\
            " <input type=\"checkbox\" id=\"monthmay\" name=\"monthmay\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthmay\">May</label>"\
            " <input type=\"checkbox\" id=\"monthjun\" name=\"monthjun\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthjun\">Jun</label>"\
            " <input type=\"checkbox\" id=\"monthjul\" name=\"monthjul\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthjul\">Jul</label>"\
            " <input type=\"checkbox\" id=\"monthaug\" name=\"monthaug\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthaug\">Aug</label>"\
            " <input type=\"checkbox\" id=\"monthsep\" name=\"monthsep\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthsep\">Sep</label>"\
            " <input type=\"checkbox\" id=\"monthoct\" name=\"monthoct\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthoct\">Oct</label>"\
            " <input type=\"checkbox\" id=\"monthnov\" name=\"monthnov\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthnov\">Nov</label>"\
            " <input type=\"checkbox\" id=\"monthdec\" name=\"monthdec\" value=\"1\" class=\"month\"/>"\
            " <label for=\"monthdec\">Dec</label>"\
            "</td>"\
            "</tr>"\
            "<tr>"\
            "<td style=\"padding:6px\" >Hosts</td>"\
            "<td style=\"padding:6px\" ><div id=\"multi_select_list_inner_div\" style=\"display:none\">"
        return html_str

    @staticmethod
    def create_scheduling_form_remain():
        html_str = "</div></td>"\
            "</tr>"\
            "<tr>"\
            "<td style=\"padding:6px\" >\
        	<div id=\"firmware_update_div_label\" style=\"display:none\"><label style=\"margin-top: 15px;margin-right: 25px;\" class=\"lbl\">Select Firmware File</label>\
        	</div>\
	</td>\
        <td><div id=\"firmware_update_div_value\" style=\"display:none\">\
		<div>"
#                                <input type=\"text\" id=\"selected_firmware\" name=\"selected_firmware\" value=\"\" readonly=\"readonly\"/>"
#                                <input type=\"button\" name=\"select_file\" id=\"select_file\" value=\"Choose File\" class=\"yo-small yo-button\"/ >\
        html_str += "              <input type=\"button\" name=\"upload_new_file\" id=\"upload_new_file\" value=\"Upload New File\" class=\"yo-small yo-button\"/>\
                </div>\
        </div></td>\
        </tr>\
        <tr><td>"\
            "<input type=\"button\" class=\"yo-button\" id=\"submitEve\" onclick=\"eventSubmit()\" value=\"Submit\" />"\
            "<input type=\"button\" class=\"yo-button\" id=\"updateEve\" style=\"display:none;\" onclick=\"eventUpdate()\" value=\"Update\" />"\
            "<input type=\"button\"class=\"yo-button\"  onclick=\"eventCancel()\" value=\"Cancel\" />"\
            "</td>"\
            "</tr>"\
            "</table>"\
            "</form>"\
            "</div>"\
            "<div class=\"calender-pop-up\" style=\"min-height:20px;width:150px;\" id=\"cEvent\"><a href=\"javascript:createEvent();\">Create Event</a></div>"\
            "<div class=\"calender-pop-up\" id=\"dEvent\"><input type=\"hidden\" id=\"scheduleId\" name=\"scheduleId\" value=\"0\" /><a href=\"#viewApDiv\" id=\"showAP\"  rel=\"facebox\">View Devices</a><br/><a href=\"javascript:editSchedule();\">Edit</a><br/><a href=\"javascript:deleteSchedule();\">Delete</a></div>"\
            "<div id=\"viewApDiv\">"\
            "</div>"
        return html_str

# function to create firmware update
    # @staticmethod
    # def device_firmware_view(h):
        # html.write("<form method=\"post\" enctype=\"multipart/form-data\"
        # action=\"firmware_file_upload.py\" style=\"font-size:10px;\"><input
        # type=\"hidden\" name=\"host_id\" value=\"%s\"/><input type=\"hidden\"
        # name=\"device_type\" value=\"%s\"/><input type=\"hidden\"
        # name=\"device_list_state\" value=\"%s\"/><label style=\"margin-top:
        # 15px;margin-right: 25px;\" class=\"lbl\">Firmware File</label><input
        # style=\"font-size:10px;\" type=\"file\" name=\"file_uploader\"
        # id=\"file_uploader\"><button name=\"button_uploader\"
        # id=\"button_uploader\" type=\"file\" style=\"font-size:10px;\" class
        # =\"yo-button yo-small\"><span
        # class=\"upload\">Upload</span></button></form>" %
        # (host_id,device_type,device_list_state))
# function to create multiple selection list for access point
    @staticmethod
    def odu_multiple_select_list(odu_list, selectListId, result):
        selectList = ""
        liList = ""
        for row in result:
            liList += "<li>" + row[1] + "<img src=\"images/add16.png\" class=\"plus plus" + selectListId + \
                "\" alt=\"+\" title=\"Add\" id=\"" + str(
                    row[0]) + "\" name=\"" + row[1] + "\"/></li>"
        selectList += "<div class=\"multiSelectList\" id=\"multiSelectList" + \
            selectListId + "\" style=\"position:;\">"
        selectList += "<input type=\"hidden\" id=\"hd" + \
            selectListId + "\" name=\"hd" + selectListId + "\" value=\"\" />"
        selectList += "<input type=\"hidden\" id=\"hdTemp" + selectListId + \
            "\" name=\"hdTemp" + selectListId + "\" value=\"" + \
            odu_list + "\" />"
        selectList += "<div class=\"selected\">"
        selectList += "<div class=\"shead\"><span id=\"count\">0</span><span> Device(s)</span><a href=\"#\" id=\"rm" + \
            selectListId + \
            "\">Remove all</a>"
        selectList += "</div>"
        selectList += "<ul>"  # <li>asdf<img src=\"images/minus16.png\" class=\"minus\" alt=\"-\" title=\"Remove\" /></li>
        selectList += "</ul>"
        selectList += "</div>"
        selectList += "<div class=\"nonSelected\">"
        selectList += "<div class=\"shead\"><a href=\"#\" id=\"add" + \
            selectListId + "\">Add all</a>"
        selectList += "</div>"
        selectList += "<ul>" + liList
        selectList += "</ul>"
        selectList += "</div>"
        selectList += "</div>"
        return selectList

    @staticmethod
    def load_non_repeative_events(schedule):
        jsonData = "{events:["
        i = 0
        try:
            for srow in schedule:
                sDate = str(srow[2]).split("-")
                eDate = str(srow[3]).split("-")
                sTime = str(srow[4]).split(":")
                eTime = str(srow[5]).split(":")
                if i > 0:
                    jsonData += ","
                jsonData += "{"
                jsonData += "id:" + str(srow[0]) + ","
                jsonData += "title:\"" + srow[1] + "\","
                jsonData += "start: new Date(" + sDate[0] + "," + str(
                    int(sDate[1]) - 1) + "," + sDate[2] + "," + sTime[0] + "," + sTime[1] + "),"
                jsonData += "end: new Date(" + eDate[0] + "," + str(
                    int(eDate[1]) - 1) + "," + eDate[2] + "," + eTime[0] + "," + eTime[1] + "),"
                jsonData += "allDay: false"
                jsonData += "}"
                i += 1
            jsonData += "]}"
            return jsonData
        except Exception, e:
            return "{events:[]}"

    @staticmethod
    def load_repeative_events(schedule):
        daily = "daily:["
        weekly = "weekly:["
        monthly = "monthly:["
        dailyI = 0
        weeklyI = 0
        monthlyI = 0
        try:
            for srow in schedule:
                if srow[7] == "Daily":
                    if dailyI > 0:
                        daily += ","
                    daily += "{"
                    daily += "id:" + str(srow[0]) + ","
                    daily += "title:\"" + srow[1] + "\","
                    daily += "start:\"" + str(srow[4]) + "\","
                    daily += "end: \"" + str(srow[5]) + "\","
                    daily += "allDay: false"
                    daily += "}"
                    dailyI += 1

                elif srow[7] == "Weekly":
                    if weeklyI > 0:
                        weekly += ","
                    weekly += "{"
                    weekly += "id:" + str(srow[0]) + ","
                    weekly += "title:\"" + srow[1] + "\","
                    weekly += "start:\"" + str(srow[4]) + "\","
                    weekly += "end: \"" + str(srow[5]) + "\","
                    weekly += "sun: " + str(srow[8]) + ","
                    weekly += "mon: " + str(srow[9]) + ","
                    weekly += "tue: " + str(srow[10]) + ","
                    weekly += "wed: " + str(srow[11]) + ","
                    weekly += "thu: " + str(srow[12]) + ","
                    weekly += "fri: " + str(srow[13]) + ","
                    weekly += "sat: " + str(srow[14]) + ","
                    weekly += "allDay: false"
                    weekly += "}"
                    weeklyI += 1

                elif srow[7] == "Monthly":
                    if monthlyI > 0:
                        monthly += ","
                    monthly += "{"
                    monthly += "id:" + str(srow[0]) + ","
                    monthly += "title:\"" + srow[1] + "\","
                    monthly += "start:\"" + str(srow[4]) + "\","
                    monthly += "end: \"" + str(srow[5]) + "\","
                    monthly += "date: " + str(srow[27]) + ","
                    monthly += "jan: " + str(srow[15]) + ","
                    monthly += "feb: " + str(srow[16]) + ","
                    monthly += "mar: " + str(srow[17]) + ","
                    monthly += "apr: " + str(srow[18]) + ","
                    monthly += "may: " + str(srow[19]) + ","
                    monthly += "jun: " + str(srow[20]) + ","
                    monthly += "jul: " + str(srow[21]) + ","
                    monthly += "aug: " + str(srow[22]) + ","
                    monthly += "sep: " + str(srow[23]) + ","
                    monthly += "oct: " + str(srow[24]) + ","
                    monthly += "nov: " + str(srow[25]) + ","
                    monthly += "dec: " + str(srow[26]) + ","
                    monthly += "allDay: false"
                    monthly += "}"
                    monthlyI += 1
            jsonData = "{" + daily + "], " + weekly + "]," + monthly + "]}"
            return jsonData
        except:
            return ("{daily:[],weekly:[],monthly:[]}")

    @staticmethod
    def view_odu_list(result):
        tableString = """
               <div><table width=\"100%\">
               	<tbody>
                       <tr><th colspan=\"4\">Device</th></tr>
               		<tr>
               			<th>S.No.</th>
               			<th>IP Address</th>
               			<th>Device type</th>
               			<th>Host Name</th>
               		</tr>
               """
        i = 0
        for row in result:
            i += 1
            tableString += "<tr><td>" + str(i) + "</td><td>" + row[1] + "</td><td>" + row[0] + \
                "</td><td>" + row[3] + "</td></tr>"
        tableString += "</tbody></table>"
        return tableString

################################## Scheduling ############################

#################################### AP Radio Status #####################
    @staticmethod
    def radio_status(result):
        socket.setdefaulttimeout(1)
        tableString = "<table style=\"margin-bottom: 0px;\" id=\"iconmeaningtable\" class=\"yo-table\" width=\"100%\"><colgroup><col width=\"auto\"><col width=\"1%\"><col width=\"6%\"><col width=\"1%\"><col width=\"6%\"><col width=\"1%\"><col width=\"6%\"></colgroup><tbody><tr><th></th><th style=\"padding: 5px 0px 5px 10px;\"><img width=\"10px\" alt=\"enable\" src=\"images/status-0.png\"></th><th>enable</th><th style=\"padding: 5px 0px 5px 10px;\"><img width=\"10px\" alt=\"disable\" src=\"images/status-2.png\"></th><th>disable</th><th style=\"padding: 5px 0px 5px 10px;\"><img width=\"10px\" alt=\"unknown\" src=\"images/status-3.png\"></th><th>unknown</th></tr></tbody></table>"

        tableString += "<table class=\"yo-table\" width=\"100%\"><colgroup><col width=\"5%\"><col width=\"25%\"><col width=\"5%\"><col width=\"25%\"><col width=\"35%\"><col width=\"5%\"></colgroup><tbody>"
        tableString += "<tr><th>S.No.</th><th>IP Address</th><th>Status</th><th>Retry Action Time</th><th>Action Msg</th><th></th></tr>"
        response = ""
        i = 0
        for row in result:
            i += 1
            username = row[3]
            password = row[4]
            port = row[5]
            tempUrl = "/cgi-bin/ServerFuncs?Method=RadioStatus"
            url = "http://" + row[2] + tempUrl

            try:
                req = urllib2.Request(url)
                auth_string = base64.encodestring(
                    "%s:%s" % (username, password))
                req.add_header("Authorization", "Basic %s" % auth_string)
                f = urllib2.urlopen(req)
                response = f.read()
            except urllib2.HTTPError, e:
                response = str(e.code)  # send http error code
            except:
                response = "Notwork Unreachable"

            if response == "400":
                message = "Bad Request"
            elif response == "401":
                message = "User name and Password are wrong"
            elif response == "404":
                message = "File Not Found"
            elif response == "501":
                message = "Server Error"
            else:
                message = "Access Point not connected"

            currentStatus = ""
            if response.find("RadioStatus = 11") != -1:
                currentStatus = "Enable"
            if response.find("RadioStatus = 01") != -1:
                currentStatus = "Enable"
            if response.find("RadioStatus = 10") != -1:
                currentStatus = "Disable"
            if response.find("RadioStatus = 00") != -1:
                currentStatus = "Disable"

            odu_bll_obj = OduSchedulingBll()
            result2 = odu_bll_obj.radio_status_repeat(row[0])

            retryTime = "-"
            retryMsg = "-"
            for row2 in result2:
                retryTime = str(row2[1]) + ", " + str(row2[2])
                retryMsg = str(row2[4]) + " (" + row2[5] + ")"

            tableString += "<tr><td>" + str(i) + "</td>"
            tableString += "<td>" + str(row[2]) + "</td>"
            if currentStatus == "Enable":
                tableString += "<td><img width=\"10px\" alt=\"enable\" title=\"Enable\" src=\"images/status-0.png\"></td>"
                tableString += "<td>" + retryTime + "</td>"
                tableString += "<td>" + retryMsg + "</td>"
                tableString += "<td><a href=\"javascript:disableRadio('" + row[2] + "','" + username + "','" + \
                    password + "','" + \
                    port + \
                    "')\">Disable</a></td>"
            elif currentStatus == "Disable":
                tableString += "<td><img width=\"10px\" alt=\"disable\" title=\"Disable\" src=\"images/status-2.png\"></td>"
                tableString += "<td>" + retryTime + "</td>"
                tableString += "<td>" + retryMsg + "</td>"
                tableString += "<td><a href=\"javascript:enableRadio('" + row[2] + "','" + username + "','" + \
                    password + "','" + \
                    port + "')\">Enable</a></td>"
            else:
                tableString += "<td><img width=\"10px\" alt=\"unknown\" title=\"" + message + \
                    "\" src=\"images/status-3.png\"></td>"
                tableString += "<td>-</td>"
                tableString += "<td>" + message + "</td>"
                tableString += "<td>-</td>"
            tableString += "</tr>"

        tableString += "</tbody></table>"
        return tableString

    @staticmethod
    def view_page_tip_scheduling():
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>Device Scheduling</h1>"\
            "<div>This page schedules events on Devices</div>"\
            "<br/>"\
            "<div>Click and Drag to Create Event on calendar</div>"\
            "<div>Select the device type, the hosts for which event has to be created and the type of event. </div>"\
            "<div>Click on any event to view its details or edit it. </div>"\
            "<br/>"\
            "<div>Events can be created for a specific date-time or repeated daily, weekly or monthly . </div>"\
            "<br/>"\
            "<div>On the right hand side of calendar, status of past scheduling is provided. </div>"\
            "<br/>"\
            "</div>"
        return html_view
