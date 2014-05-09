#!/usr/bin/python2.6

'''
@author: Mahipal Choudhary
@since: 07-Nov-2011
@version: 0.1
@note: All Controller functions Related with Reporting.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
from json import JSONEncoder

from main_reporting_bll import MainReportBll
from main_reporting import Report
from common_bll import Essential

user_report_dict = None


def get_user_report_dict():
    global user_report_dict
    return user_report_dict


def set_user_report_dict(set_user_report_dict):
    global user_report_dict
    user_report_dict = set_user_report_dict


def main_report(h):
    global html, user_report_dict
    html = h
    user_report_dict = {}
    device_type_user_selected_id = html.var("device_type_user_selected_id")
    device_type_user_selected_name = html.var("device_type_user_selected_name")
    #    device_type_user_selected_id="odu16"
    #    device_type_user_selected_name="UBR"
    css_list = [
        "css/demo_table_jui.css", "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css",
        "css/jquery.multiselect.css", "css/jquery.multiselect.filter.css",
        "css/jquery-ui-1.8.4.custom.css"]  # ,"css/jquery.multiselect.filter.css"]
    js_list = [
        "js/lib/main/calendrical.js", "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/main_reporting.js"]  # ,
    snapin_list = ["reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    if (device_type_user_selected_name is None):
        html.new_header("General Report", "main_report.py", "",
                        css_list, js_list, snapin_list)
    else:
        str_header = "main_report_%s.py?device_type_user_selected_id=%s&device_type_user_selected_name=%s" % (
            device_type_user_selected_id, device_type_user_selected_id, device_type_user_selected_name)
        html.new_header(device_type_user_selected_name + " Report",
                        str_header, "", css_list, js_list, snapin_list)
    r = MainReportBll()
    user_id = html.req.session["user_id"]
    es = Essential()
    hostgroup_id_list = es.get_hostgroup_ids(user_id)
    if (hostgroup_id_list == []):
        html.write(Report.list_form([], [], device_type_user_selected_id,
                                            device_type_user_selected_name))
    else:
        result = r.get_hostgroup_device(user_id, hostgroup_id_list)
        if (result["success"] == 0):
            html.write(Report.list_form(result["result"], result["host_data"],
                                        device_type_user_selected_id, device_type_user_selected_name))
        else:
            pass
    html.new_footer()


def main_reporting_get_host_data(h):
    global html
    html = h
    hostgroup_id = str(html.var("hostgroup_id"))
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    r = MainReportBll()
    result = r.main_reporting_get_host_data(hostgroup_id, device_type_id)
    column_result = r.main_reporting_get_column_template(
        device_type_id, report_type)
    selected_columns = []
    non_selected_columns = []
    if (column_result["success"] == 0 or column_result["success"] == "0"):
        selected_columns = column_result["result"][0].split(",")
        non_selected_columns = column_result["result"][1].split(",")
    if (result["success"] == 0 or column_result["success"] == "0"):
        res = {'html': Report.get_columns(
            selected_columns, non_selected_columns), 'result': str(result['result'])}
        html.write(str(res))
    else:
        pass


def main_reporting_get_columns_data(h):
    global html
    html = h
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    html.write(Report.get_columns(device_type_id, report_type))


def main_reporting_get_excel(h):
    global html
    html = h
    global rs2
    global user_report_dict
    user_report_dict = {}
    username = html.req.session["username"]
    #    no_of_devices=str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    all_host = str(html.var("all_host"))
    report_type = str(html.var("report_type"))
    column_value = str(html.var("columns"))
    column_value = column_value.split(",")
    device_type = str(html.var("device_type"))
    hostgroup = str(html.var("hostgroup"))
    view_type = str(html.var("view_type"))
    i_display_start = str(html.var("iDisplayStart"))
    i_display_length = str(html.var("iDisplayLength"))
    s_search = str(html.var("sSearch"))
    sEcho = str(html.var("sEcho"))
    s_search = str(html.var("sSearch"))
    sSortDir_0 = str(html.var("sSortDir_0"))
    iSortCol_0 = str(html.var("iSortCol_0"))
    r = MainReportBll()
    #### dict defined
    new_user_report_dict = {}
    new_user_report_dict["user_id"] = html.req.session["user_id"]
    new_user_report_dict["report_type"] = report_type
    new_user_report_dict["device_type"] = device_type
    new_user_report_dict["all_host"] = all_host
    new_user_report_dict["start_date"] = date_start
    new_user_report_dict["end_date"] = date_end
    new_user_report_dict["start_time"] = time_start
    new_user_report_dict["end_time"] = time_end
    ####
    result = r.main_reporting_get_excel(
        date_start, date_end, time_start, time_end, all_host, report_type, column_value, device_type, hostgroup,
        view_type, i_display_start, i_display_length,
        s_search, sEcho, sSortDir_0, iSortCol_0, new_user_report_dict, username)
    html.write(JSONEncoder().encode(result))


def trap_main_report(h):
    global html, user_report_dict
    html = h
    user_report_dict = {}
    css_list = [
        "css/demo_table_jui.css", "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css",
        "css/jquery.multiselect.css", "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/calendrical.js", "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/main_reporting_trap.js"]
    snapin_list = ["reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    html.new_header(
        "Events Report", "trapreport.py", "", css_list, js_list, snapin_list)
    r = MainReportBll()
    user_id = html.req.session["user_id"]
    es = Essential()
    hostgroup_id_list = es.get_hostgroup_ids(user_id)
    if (hostgroup_id_list == []):
        html.write(Report.trap_list_form([], []))
    else:
        result = r.get_hostgroup_device(user_id, hostgroup_id_list)
        if (result["success"] == 0):
            html.write(
                Report.trap_list_form(result["result"], result["host_data"]))
        else:
            pass
    html.new_footer()


def trap_main_reporting_get_host_data(h):
    global html
    html = h
    hostgroup_id = str(html.var("hostgroup_id"))
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    r = MainReportBll()
    result = r.main_reporting_get_host_data(hostgroup_id, device_type_id)
    if (result["success"] == 0):
        res = {'result': str(result['result'])}
        html.write(str(res))
    else:
        pass


def trap_main_reporting_get_excel(h):
    global html
    html = h
    global rs2
    global user_report_dict
    user_report_dict = {}
    username = html.req.session["username"]
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    all_host = str(html.var("all_host"))
    report_type = str(html.var("report_type"))
    device_type = str(html.var("device_type"))
    hostgroup = str(html.var("hostgroup"))
    view_type = str(html.var("view_type"))
    i_display_start = str(html.var("iDisplayStart"))
    i_display_length = str(html.var("iDisplayLength"))
    s_search = str(html.var("sSearch"))
    sEcho = str(html.var("sEcho"))
    s_search = str(html.var("sSearch"))
    sSortDir_0 = str(html.var("sSortDir_0"))
    iSortCol_0 = str(html.var("iSortCol_0"))
    r = MainReportBll()
    #### dict defined
    new_user_report_dict = {}
    new_user_report_dict["user_id"] = html.req.session["user_id"]
    new_user_report_dict["report_type"] = report_type
    new_user_report_dict["device_type"] = device_type
    new_user_report_dict["all_host"] = all_host
    new_user_report_dict["start_date"] = date_start
    new_user_report_dict["end_date"] = date_end
    new_user_report_dict["start_time"] = time_start
    new_user_report_dict["end_time"] = time_end
    ####
    if (hostgroup == ""):
        user_id = html.req.session["user_id"]
        es = Essential()
        hostgroup_id_list = es.get_hostgroup_ids(user_id)
    else:
        hostgroup_id_list = [hostgroup]
    result = r.trap_main_reporting_get_excel(
        date_start, date_end, time_start, time_end, all_host, report_type, device_type, hostgroup, view_type,
        i_display_start,
        i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, new_user_report_dict, username, hostgroup_id_list)
    html.write(JSONEncoder().encode(result))


# def view_page_tip_main_reporting(h):
#     global html
#     html = h
#     html.write(Report.page_tip_main_reporting())
#
#
# def trap_view_page_tip_main_reporting(h):
#     global html
#     html = h
#     html.write(Report.trap_page_tip_main_reporting())
