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

from mod_python import util

from analyzed_reporting import Report
from analyzed_reporting_bll import AnalyzedReportBll
from common_bll import Essential


def analyzed_report(h):
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
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/analyzed_reporting.js"]  # ,
    if (device_type_user_selected_name == None):
        html.new_header(
            "Analyzed Report", "analyzed_report.py", "", css_list, js_list)
    else:
        str_header = "analyzed_report.py?device_type_user_selected_id=%s&device_type_user_selected_name=%s" % (
            device_type_user_selected_id, device_type_user_selected_name)
        html.new_header(device_type_user_selected_name + " Report",
                        str_header, "", css_list, js_list)
    r = AnalyzedReportBll()
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


def analyzed_reporting_get_host_data(h):
    global html
    html = h
    hostgroup_id = str(html.var("hostgroup_id"))
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    r = AnalyzedReportBll()
    result = r.analyzed_reporting_get_host_data(hostgroup_id, device_type_id)
    column_result = r.analyzed_reporting_get_column_template(
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


def analyzed_reporting_get_column_range(h):
    global html
    html = h
    hostgroup_id = str(html.var("hostgroup_id"))
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    range_type = str(html.var("range_type"))
    r = AnalyzedReportBll()
    column_result = r.analyzed_reporting_get_column_range(
        device_type_id, report_type, range_type)
    selected_columns = []
    non_selected_columns = []
    if (column_result["success"] == 0 or column_result["success"] == "0"):
        selected_columns = column_result["result"][0].split(",")
        non_selected_columns = column_result["result"][1].split(",")
    if (column_result["success"] == "0"):
        res = {'html': Report.get_columns(selected_columns,
                                          non_selected_columns)}
        html.write(str(res))
    else:
        html.write(str(column_result))


def analyzed_reporting_get_columns_data(h):
    global html
    html = h
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    html.write(Report.get_columns(device_type_id, report_type))


def analyzed_reporting_get_excel(h):
    global html
    html = h
    username = html.req.session["username"]
    form = util.FieldStorage(html.req)
    html_var = form.list.table_dict()
    #    no_of_devices=str(html.var("no_of_devices"))
    html_var = form.list.table_dict()
    date_start = str(html_var.get("start_date"))
    date_end = str(html_var.get("end_date"))
    time_start = str(html_var.get("start_time"))
    time_end = str(html_var.get("end_time"))
    all_host = str(html_var.get("all_host"))
    report_type = str(html_var.get("report_type"))
    column_value = str(html_var.get("columns"))
    column_value = column_value.split(",")
    device_type = str(html_var.get("device_type"))
    hostgroup = str(html_var.get("hostgroup"))
    view_type = str(html_var.get("view_type"))
    range_type = str(html_var.get("range_type"))  # minimum , maximum
    range_duration = str(html_var.get("range_duration"))  # hourly , daily
    i_display_start = str(html_var.get("iDisplayStart"))
    i_display_length = str(html_var.get("iDisplayLength"))
    s_search = str(html_var.get("sSearch"))
    sEcho = str(html_var.get("sEcho"))
    s_search = str(html_var.get("sSearch"))
    sSortDir_0 = str(html_var.get("sSortDir_0"))
    iSortCol_0 = str(html_var.get("iSortCol_0"))
    i_display_start = html_var.get("iDisplayStart", None)
    # html_req=html.req.vars
    r = AnalyzedReportBll()
    if (str(range_duration) == "1"):
        range_duration = "HOURLY"
    elif (str(range_duration) == "2"):
        range_duration = "DAILY"
    elif (str(range_duration) == "3"):
        range_duration = "WEEKLY"
    elif (str(range_duration) == "4"):
        range_duration = "MONTHLY"

    if (str(range_type) == "1"):
        range_type = "Minimum"
    elif (str(range_type) == "2"):
        range_type = "Maximum"
    elif (str(range_type) == "3"):
        range_type = "Average"
    elif (str(range_type) == "4"):
        range_type = "Total"
    elif (str(range_type) == "5"):
        range_type = "All"
        # if(report_type=="RSSI" and range_type=="Average"):
    #	range_type="Range"
    result = r.analyzed_reporting_get_excel(
        date_start, date_end, time_start, time_end, all_host, report_type, column_value, device_type, hostgroup,
        view_type, range_type, range_duration, i_display_start,
        i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, html_var, username)
    html.write(JSONEncoder().encode(result))


# def view_page_tip_analyzed_reporting(h):
#     global html
#     html = h
#     html.write(Report.page_tip_analyzed_reporting())
