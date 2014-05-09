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

from ubre_reporting_bll import Report_bll
from ubre_reporting_view import Report


# global variables
rs2 = {"all": [], "avg": []}
# calling the view for reporting


def ubre_manage_crc_phy_report(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/ubre_reporting.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header(
        "UBRe CRC-PHY Error Report", "#ubre_sub_menu", "", css_list, js_list)
    html.write(Report.ubre_create_crc_phy_form())
    html.new_footer()


def ubre_get_crc_phy_data(h):
    global html
    html = h
    global rs2
    rs = {"all": [], "avg": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["avg"] = ubre_average_data_crc_phy(h)
    rs["all"] = ubre_total_data_crc_phy(h)
    html.write(str(rs))


def ubre_average_data_crc_phy(h):
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    average_list = r.ubre_get_avg_data_for_two_dates(
        no_of_devices, date_start, date_end, all_group, all_host)
    return average_list


def ubre_total_data_crc_phy(h):
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    total_result = r.ubre_get_total_data_for_two_dates(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def ubre_show_group_result(h):
    output_list = []
    data = h.var('tag')
    r = Report_bll()
    output, status = r.ubre_group_data(str(data))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'value': str(output[i][1]), 'key': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def ubre_show_host_result(h):
    output_list = []
    data = h.var('tag')
    r = Report_bll()
    output, status = r.ubre_host_data(str(data))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'value': str(output[i][1]) + ' (' + str(
                output[i][2]) + ', ' + str(output[i][3]) + ')', 'key': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def ubre_show_host_data_of_group(h):
    output_list = []
    data = h.var('select_value')
    r = Report_bll()
    output, status = r.ubre_host_data(str(data))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'title': str(output[i][1]) + ' (' + str(
                output[i][2]) + ', ' + str(output[i][3]) + ')', 'value': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def ubre_manage_rssi_report(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/ubre_reporting_rssi.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header(
        "UBRe RSSI Report", "#ubre_sub_menu", "", css_list, js_list)
    html.write(Report.ubre_create_rssi_form())
    html.new_footer()


def ubre_get_rssi_data(h):
    global html
    html = h
    rs = {"all": [], "avg": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["avg"] = ubre_average_data_rssi(h)
    rs["all"] = ubre_total_data_rssi(h)
    html.write(str(rs))


def ubre_average_data_rssi(h):
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    average_list = r.ubre_get_avg_data_for_two_dates_rssi(
        no_of_devices, date_start, date_end, all_group, all_host)
    return average_list


def ubre_total_data_rssi(h):
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    total_result = r.ubre_get_total_data_for_two_dates_rssi(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def ubre_manage_network_usage_report(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/ubre_reporting_network_usage.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header(
        "UBRe Network Usage Report", "#ubre_sub_menu", "", css_list, js_list)
    html.write(Report.ubre_create_network_usage_form())
    html.new_footer()


def ubre_get_network_usage_data(h):
    global html
    html = h
    rs = {"all": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["all"] = ubre_total_data_network_usage(h)
    html.write(str(rs))


def ubre_total_data_network_usage(h):
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    total_result = r.ubre_get_total_data_network_usage(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def ubre_odu_excel_reporting(h):
    global html
    html = h
    crc_avg = ubre_average_data_crc_phy(h)
    crc_total = ubre_total_data_crc_phy(h)
    r = Report_bll()
    report_status = r.ubre_crc_excel_creating(crc_avg, crc_total)
    html.write(str(report_status))


def ubre_nw_bandwidth_excel_reporting(h):
    global html
    html = h
    nw_data = ubre_total_data_network_usage(h)
    r = Report_bll()
    report_status = r.ubre_nw_bandwith_excel_creating(nw_data)
    html.write(str(report_status))


def ubre_rssi_excel_reporting(h):
    global html
    html = h
    rssi_avg = ubre_average_data_rssi(h)
    rssi_total = ubre_total_data_rssi(h)
    r = Report_bll()
    report_status = r.ubre_rssi_excel_creating(rssi_avg, rssi_total)
    html.write(str(report_status))


# def ubre_page_tip_crc_phy(h):
#     global html
#     html = h
#     html.write(Report.page_tip_crc_phy())
#
#
# def ubre_page_tip_rssi(h):
#     global html
#     html = h
#     html.write(Report.ubre_page_tip_rssi())
#
#
# def ubre_page_tip_network_usage(h):
#     global html
#     html = h
#     html.write(Report.ubre_page_tip_network_usage())


def ubre_show_group_result(h):
    output_list = []
    data = h.var('tag')
    r = Report_bll()
    output, status = r.ubre_group_data(str(data))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'value': str(output[i][1]), 'key': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def ubre_show_host_result(h):
    output_list = []
    data = h.var('tag')
    r = Report_bll()
    output, status = r.ubre_host_data(str(data))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'value': str(output[i][1]) + ' (' + str(
                output[i][2]) + ', ' + str(output[i][3]) + ')', 'key': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def ubre_show_host_data_of_group(h):
    output_list = []
    data = h.var('select_value')
    r = Report_bll()
    output, status = r.ubre_host_data(str(data))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'title': str(output[i][1]) + ' (' + str(
                output[i][2]) + ', ' + str(output[i][3]) + ')', 'value': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))
