#!/usr/bin/python2.6

'''
@author: Mahipal Choudhary
@since: 07-Dec-2011
@version: 0.1
@note: All Controller functions Related with Vieweing logs.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


# Import modules that contain the function and libraries
from json import JSONEncoder
import os

from common_bll import Essential
from log import Log
from log_bll import Log_bll


def main_log(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css", "css/calendrical.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.dataTables.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/calendrical.js", "js/unmp/main/log.js"]

    group = html.req.session["group"].lower()
    user_details = []
    header_btn = ""
    if group == "superadmin" or group == "admin":
        l = Log_bll()
        user_details = l.get_user_names()
        header_btn = "<div class=\"header-icon\"><img onclick=\"LogSettings();\" class=\"n-tip-image\" src=\"images/%s/wrench.png\" id=\"add_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\"></div>" % theme

    html.new_header(
        "LOG DETAILS", "log_user.py", header_btn, css_list, js_list)
    # html.write(Log.create_log_form())
    html.write(Log.manage_events(group, user_details))
    html.new_footer()


def get_data(h):
    global html
    html = h
    l = Log_bll()
    sEcho = str(html.var("sEcho"))
    iColumns = html.var("iColumns", 0)
    iDisplayLength = str(html.var("iDisplayLength", 10))
    iDisplayStart = str(html.var("iDisplayStart", 0))
    sColumns = str(html.var("sColumns"))
    sEcho = str(html.var("sEcho"))
    sSearch = str(html.var("sSearch"))
    iSortCol_0 = html.var("iSortCol_0", -1)
    sSortDir_0 = html.var("sSortDir_0", "asc")

    month = html.var("month", "")
    log_type = html.var("log_type", "")
    selected_user = html.var("user_name", "")
    group = html.req.session["group"].lower()

    date_start = ""
    date_end = ""
    time_start = ""
    time_end = ""
    if str(month) == "20":
        date_start = str(html.var("start_date"))
        date_end = str(html.var("end_date"))
        time_start = str(html.var("start_time"))
        time_end = str(html.var("end_time"))
    result = l.get_log_data_bll(
        sEcho, iColumns, iDisplayLength, iDisplayStart, sColumns, sSearch, iSortCol_0, sSortDir_0, month, log_type,
        selected_user,
        group, date_start, date_end, time_start, time_end)
    html.write(JSONEncoder().encode(result))


def get_current_data(h):
    global html
    html = h
    l = Log_bll()
    result = l.get_header_data()
    # html.write(str(result))
    html_str = Log.make_header_log(result)
    html.write(html_str)


def get_log_data_excel(h):
    try:
        global html
        html = h
        month = html.var("month", "")
        log_type = html.var("log_type", "")
        selected_user = html.var("user_name", "")
        report_type = html.var("report_type", 1)
        date_start = ""
        date_end = ""
        time_start = ""
        time_end = ""
        if str(month) == "20":
            date_start = str(html.var("start_date"))
            date_end = str(html.var("end_date"))
            time_start = str(html.var("start_time"))
            time_end = str(html.var("end_time"))
        username = html.req.session["username"]
        l = Log_bll()
        result = l.get_log_data_report(month, log_type, report_type, username,
                                       selected_user, date_start, date_end, time_start, time_end)
        html.write(JSONEncoder().encode(result))
    except Exception, e:
        html.write(str(e))


def get_alarm_current_data(h):
    global html
    html = h
    l = Log_bll()
    user_id = html.req.session["user_id"]
    el = Essential()
    hostgroup_id_list = el.get_hostgroup_ids(user_id)
    result = l.get_alarm_header_data(hostgroup_id_list)
    device_type_dict = l.get_device_type_dict()
    html_str = Log.make_alarm_header_log(result, device_type_dict)
    html.write(html_str)


def clear_old_logs(h):
    global html
    html = h
    l = Log_bll()
    result = l.clear_old_logs()
    html.write(JSONEncoder().encode(result))


# def view_page_tip_log_user(h):
#     global html
#     html = h
#     html.write(Log.view_page_tip_log_user())


def edit_log_settings(h):
    global html
    html = h
    file_path = "/omd/daemon/configuration_file.unmp"
    val = 0
    if os.path.isfile(file_path):
        file_obj = open(file_path, "r")
        lines = file_obj.readlines()
        file_obj.close()
        for line in lines:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            li = line.split('=')
            if li[0].strip() == "set_user_trail":
                val = li[1].strip()
                break
    try:
        if str(val) == "1":
            html_selected = "<option selected='selected' value='1'>Enable</option><option value='0'>Disable</option>"
        else:
            html_selected = "<option value='1'>Enable</option><option selected='selected' value='0'>Disable</option>"
        html_view = "<h2>User trail settings:</h2>\
		<div class=\"row-elem\"></div>\
		<div class=\"row-elem\">\
		<label class=\"lbl lbl-big\" style=\"width:90px;\" > User trail:</label>\
		<select name=\"user_trail_state\" id=\"user_trail_state\" class=\"multiselect\" title=\"Click to select an option\">\
		%s</select></div>\
		<button class=\"yo-small yo-button\" id=\"apply_log_settings\" type=\"button\">Apply Changes</button>\
		<button class=\"yo-small yo-button\" id=\"clear_old_logs\" type=\"button\">Clear old logs</button>" % (
        html_selected)
        html.write(html_view)
    except Exception, e:
        html.write(str(e))


def apply_log_settings(h):
    global html
    html = h
    user_trail_state = html.var("user_trail_state")
    try:
        file_path = "/omd/daemon/configuration_file.unmp"
        if not os.path.isfile(file_path):
            return 0
        file_obj = open(file_path, "r")
        lines = file_obj.readlines()
        file_obj.close()
        for i in range(len(lines)):
            if lines[i].startswith("#") or lines[i] == "":
                continue
            line_li = lines[i].split('=')
            if line_li[0].strip() == "set_user_trail":
                line_li[1] = user_trail_state
                lines[i] = ' = '.join(line_li)
                break

        file_obj = open(file_path, "w")
        file_obj.writelines(lines)
        file_obj.close()
        html.write(str({"success": 0, "result": ""}))
    except Exception, e:
        html.write(str({"success": 1, "result": str(e)}))
