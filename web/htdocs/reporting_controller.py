#!/usr/bin/python2.6

"""
@author: Mahipal Choudhary
@since: 07-Nov-2011
@version: 0.1
@note: All Controller functions Related with Reporting.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# Import modules that contain the function and libraries
from json import JSONEncoder

from reporting import Report
from reporting_bll import Report_bll


# global variables
rs2 = {"all": [], "avg": []}
# calling the view for reporting


def manage_crc_phy_report(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/reporting.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header(
        "UBR CRC-PHY Error Report", "#ubr_sub_menu", "", css_list, js_list)
    html.write(Report.create_crc_phy_form())
    html.new_footer()


def get_crc_phy_data(h):
    """

    @param h:
    """
    global html
    html = h
    rs = {"all": [], "avg": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["avg"] = average_data_crc_phy(h)
    rs["all"] = total_data_crc_phy(h)
    html.write(str(rs))


def average_data_crc_phy(h):
    """

    @param h:
    @return:
    """
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    average_list = r.get_avg_data_for_two_dates(
        no_of_devices, date_start, date_end, all_group, all_host)
    return average_list


def total_data_crc_phy(h):
    """

    @param h:
    @return:
    """
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
    total_result = r.get_total_data_for_two_dates(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def manage_rssi_report(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/reporting_rssi.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header("UBR RSSI Report", "#ubr_sub_menu", "", css_list, js_list)
    html.write(Report.create_rssi_form())
    html.new_footer()


def get_rssi_data(h):
    """

    @param h:
    """
    global html
    html = h
    rs = {"all": [], "avg": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["avg"] = average_data_rssi(h)
    rs["all"] = total_data_rssi(h)
    html.write(str(rs))


def average_data_rssi(h):
    """

    @param h:
    @return:
    """
    global html
    html = h
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    all_host = str(html.var("all_host"))
    all_group = str(html.var("all_group"))
    r = Report_bll()
    average_list = r.get_avg_data_for_two_dates_rssi(
        no_of_devices, date_start, date_end, all_group, all_host)
    return average_list


def total_data_rssi(h):
    """

    @param h:
    @return:
    """
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
    total_result = r.get_total_data_for_two_dates_rssi(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def manage_network_usage_report(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/reporting_network_usage.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header(
        "UBR Network Usage Report", "#ubr_sub_menu", "", css_list, js_list)
    html.write(Report.create_network_usage_form())
    html.new_footer()


def get_network_usage_data(h):
    """

    @param h:
    """
    global html
    html = h
    rs = {"all": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["all"] = total_data_network_usage(h)
    html.write(str(rs))


def total_data_network_usage(h):
    """

    @param h:
    @return:
    """
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
    total_result = r.get_total_data_network_usage(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def manage_network_outage_report(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/reporting_network_outage.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header("Network Outage Report",
                    "manage_network_outage_report.py", "", css_list, js_list)
    html.write(Report.create_network_outage_form())
    html.new_footer()


def get_network_outage_data(h):
    """

    @param h:
    """
    global html
    html = h
    rs = {"all": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["all"] = total_data_network_outage(h)
    html.write(str(rs))


def total_data_network_outage(h):
    """

    @param h:
    @return:
    """
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
    total_result = r.get_total_data_network_outage(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def odu_excel_reporting(h):
    """

    @param h:
    """
    global html
    html = h
    crc_avg = average_data_crc_phy(h)
    crc_total = total_data_crc_phy(h)
    r = Report_bll()
    report_status = r.crc_excel_creating(crc_avg, crc_total)
    html.write(str(report_status))


def nw_bandwidth_excel_reporting(h):
    """

    @param h:
    """
    global html
    html = h
    nw_data = total_data_network_usage(h)
    r = Report_bll()
    report_status = r.nw_bandwith_excel_creating(nw_data)
    html.write(str(report_status))


def rssi_excel_reporting(h):
    """

    @param h:
    """
    global html
    html = h
    rssi_avg = average_data_rssi(h)
    rssi_total = total_data_rssi(h)
    r = Report_bll()
    report_status = r.rssi_excel_creating(rssi_avg, rssi_total)
    html.write(str(report_status))


def outage_excel_reporting(h):
    """

    @param h:
    """
    global html
    html = h
    outage_total = total_data_network_outage(h)
    r = Report_bll()
    report_status = r.outage_excel_creating(outage_total)
    html.write(str(report_status))


def manage_trap_report(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css",
                "css/calendrical.css", "css/fcbkcomplete.css", "css/style12.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/reporting_traps.js", "js/lib/main/jquery.fcbkcomplete.js"]
    html.new_header(
        "Event Report", "manage_trap_report.py", "", css_list, js_list)
    html.write(Report.create_trap_form())
    html.new_footer()


def get_trap_data(h):
    """

    @param h:
    """
    global html
    html = h
    rs = {"all": []}
    no_of_devices = str(html.var("no_of_devices"))
    date_start = str(html.var("start_date"))
    date_end = str(html.var("end_date"))
    time_start = str(html.var("start_time"))
    time_end = str(html.var("end_time"))
    rs["all"] = total_data_trap(h)
    html.write(str(rs))


def total_data_trap(h):
    """

    @param h:
    @return:
    """
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
    total_result = r.get_total_data_trap(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result


def total_data_trap_excel(h):
    """

    @param h:
    @return:
    """
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
    total_result, alarm_result = r.get_total_trap_data_excel(
        no_of_devices, date_start, date_end, time_start, time_end, all_group, all_host)
    return total_result, alarm_result


def event_excel_reporting(h):
    """

    @param h:
    """
    global html
    html = h
    event_total, alarm_result = total_data_trap_excel(h)
    r = Report_bll()
    if alarm_result != 1:
        report_status = r.event_excel_creating(event_total, alarm_result)
        html.write(str(report_status))
    else:
        html.write(str(event_total))

#
# def page_tip_crc_phy(h):
#     global html
#     html = h
#     html.write(Report.page_tip_crc_phy())
#
#
# def page_tip_rssi(h):
#     global html
#     html = h
#     html.write(Report.page_tip_rssi())
#
#
# def page_tip_network_outage(h):
#     global html
#     html = h
#     html.write(Report.page_tip_network_outage())
#
#
# def page_tip_network_usage(h):
#     global html
#     html = h
#     html.write(Report.page_tip_network_usage())
#
#
# def page_tip_trap(h):
#     global html
#     html = h
#     html.write(Report.page_tip_trap())
#
#
# def page_tip_inventory_report(h):
#     global html
#     html = h
#     html.write(Report.page_tip_for_inventory())


def show_group_result(h):
    """

    @param h:
    """
    output_list = []
    data = h.var('tag')
    common = h.var('common')
    r = Report_bll()
    output, status = r.group_data(str(data), str(common))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'value': str(output[i][1]), 'key': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def show_host_result(h):
    """

    @param h:
    """
    output_list = []
    data = h.var('tag')
    common = h.var('common')
    r = Report_bll()
    output, status = r.host_data(str(data), str(common))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'value': str(output[i][1]) + ' (' + str(
                output[i][2]) + ', ' + str(output[i][3]) + ')', 'key': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))


def show_host_data_of_group(h):
    """

    @param h:
    """
    output_list = []
    data = h.var('select_value')
    common = h.var('common')
    r = Report_bll()
    output, status = r.host_data(str(data), str(common))
    if status == 0:
        for i in range(0, len(output)):
            temp_dic = {'title': str(output[i][1]) + ' (' + str(
                output[i][2]) + ', ' + str(output[i][3]) + ')', 'value': str(output[i][0])}
            output_list.append(temp_dic)
    else:
        output_list.append(str(output))
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(output_list)))

# calling the view for reporting


def inventory_report(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/lib/main/calendrical.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/inventory_report.js"]
    html.new_header(
        "Inventory Report", "inventory_report.py", "", css_list, js_list)
    html.write(Report.invetory_view())
    html.new_footer()


def inventory_reprot_creating(h):
    """

    @param h:
    """
    global html
    html = h
    r = Report_bll()
    user_id = html.req.session['user_id']
    result = r.inventory_excel_report_creation(user_id)
    html.write(str(result))
