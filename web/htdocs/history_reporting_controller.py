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
from history_reporting_bll import HistoryReportBll
from history_reporting import Report
from json import JSONEncoder
from common_bll import Essential

user_report_dict = None


def get_user_report_dict():
    global user_report_dict
    return user_report_dict


def set_user_report_dict(set_user_report_dict):
    global user_report_dict
    user_report_dict = set_user_report_dict


def backup_data_check_historical(h):
    global html
    html = h
    r = HistoryReportBll()
    month_var = html.var("month_var")
    result = r.backup_data_check_historical(month_var)
    html.write(str(result))


def backup_data_historical(h):
    global html
    html = h
    r = HistoryReportBll()
    month_var = html.var("month_var")
    result = r.backup_data_historical(month_var)
    html.write(str(result))


def cleanup_data_historical(h):
    global html
    html = h
    month_var = html.var("month_var")
    r = HistoryReportBll()
    result = r.cleanup_data_historical(month_var)
    html.write(str(result))


def history_report(h):
    global html, user_report_dict
    html = h
    user_report_dict = {}
    css_list = [
        "css/demo_table_jui.css", "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css",
        "css/jquery.multiselect.css", "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/calendrical.js", "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/history_reporting2.js"]
    html.new_header(
        "Backup & Restore", "history_report.py", "", css_list, js_list)
    r = HistoryReportBll()
    user_id = html.req.session["user_id"]
    result = r.get_year_month_status_historical(user_id)
    if result != "":
        year_month = result[0][0]
        status = result[0][1]
    else:
        year_month = ""
        status = ""

    html.write(Report.get_month(year_month, status))
    html.new_footer()


def main_report(h):
    global html, user_report_dict
    html = h
    r = HistoryReportBll()
    user_report_dict = {}
    user_id = html.req.session["user_id"]
    month_var = r.get_year_month_historical(user_id)
    set_time = r.set_last_access_time_historical(user_id)
    # month_var=html.var("month_var")
    # db_historical=html.req.session["db_historical"]
    db_historical = user_id.replace("-", "_") + "_db"
    css_list = [
        "css/demo_table_jui.css", "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css",
        "css/jquery.multiselect.css", "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/calendrical.js", "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/history_reporting.js"]
    html.new_header(
        "Backup & Restore", "history_report.py", "", css_list, js_list)
    device_type_user_selected_id = None
    device_type_user_selected_name = None
    user_id = html.req.session["user_id"]
    es = Essential()
    hostgroup_id_list = es.get_hostgroup_ids(user_id)
    if (hostgroup_id_list == []):
        html.write(Report.list_form([], [], device_type_user_selected_id,
                                            device_type_user_selected_name))
    else:
        result = r.get_hostgroup_device(
            user_id, hostgroup_id_list, db_historical)
        if (result["success"] == 0):
            html.write(Report.list_form(result["result"], result["host_data"],
                                        device_type_user_selected_id, device_type_user_selected_name, month_var))
        else:
            pass
    html.new_footer()


def check_db_status_historical(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    r = HistoryReportBll()
    result = r.check_db_status_historical(user_id)
    html.write(str(result))


def clear_data_historical(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    r = HistoryReportBll()
    result = r.clear_data_historical(user_id)
    html.write(str(result))


def update_db_status_historical(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    r = HistoryReportBll()
    result = r.update_db_status_historical(user_id)
    html.write(str(result))


def history_reporting_make_db(h):
    global html, user_report_dict
    html = h
    user_report_dict = {}
    r = HistoryReportBll()
    month_var = str(html.var("month_var"))
    user_id = html.req.session["user_id"]
    db_historical = user_id.replace("-", "_") + "_db"
    html.req.session["db_historical"] = db_historical
    html.req.session.save()
    user_name = html.req.session["username"]
    result = r.history_reporting_make_db(
        user_id, user_name, month_var, db_historical)
    html.write(JSONEncoder().encode(result))


def history_reporting_get_host_data(h):
    global html
    html = h
    hostgroup_id = str(html.var("hostgroup_id"))
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    r = HistoryReportBll()
    user_id = html.req.session["user_id"]
    # db_historical=html.req.session["db_historical"]
    db_historical = user_id.replace("-", "_") + "_db"
    result = r.history_reporting_get_host_data(
        hostgroup_id, device_type_id, db_historical)
    column_result = r.history_reporting_get_column_template(
        device_type_id, report_type, db_historical)
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


def history_reporting_get_columns_data(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    # db_historical=html.req.session["db_historical"]
    db_historical = user_id.replace("-", "_") + "_db"
    device_type_id = str(html.var("device_type_id"))
    report_type = str(html.var("report_type"))
    html.write(Report.get_columns(device_type_id, report_type))


def history_reporting_get_excel(h):
    global html
    html = h
    global user_report_dict
    user_id = html.req.session["user_id"]
    username = html.req.session["username"]
    # db_historical=html.req.session["db_historical"]
    db_historical = user_id.replace("-", "_") + "_db"
    user_report_dict = {}
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
    r = HistoryReportBll()
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
    result = r.history_reporting_get_excel(
        date_start, date_end, time_start, time_end, all_host, report_type, column_value, device_type, hostgroup,
        view_type,
        i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, new_user_report_dict, db_historical,
        username)
    html.write(JSONEncoder().encode(result))


# def view_page_tip_history_reporting(h):
#     global html
#     html = h
#     html.write(Report.page_tip_history_reporting())
#
#
# def view_page_tip_main_history_reporting(h):
#     global html
#     html = h
#     html.write(Report.page_tip_main_history_reporting())
