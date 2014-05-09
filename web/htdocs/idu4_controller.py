#!/usr/bin/python2.6

# import the packeges
from datetime import datetime
from datetime import timedelta

from common_controller import *
from idu4_dashboard_bll import IDUDashboard
from idu4_view import idu4View
from mysql_collection import mysql_connection
from nms_config import *
from odu_controller import *
from utility import Validation


def idu4_dashboard_profiling(h):
    """

    @param h:
    """
    global html
    html = h
    flag = 0
    css_list = ["css/style.css", "css/custom.css",
                "calendrical/calendrical.css"]
    javascript_list = ["js/lib/main/highcharts.js", "js/unmp/main/idu4Dashboard.js",
                       "calendrical/calendrical.js"]
    html.new_header("IDU4 Dashboard", "", "", css_list, javascript_list)
    html.write('<div class=\"form-div\">')
    host_id = ""
    host_id = html.var("host_id")
    extr_button = {'tag': 'button', 'id': 'adSrhIDU4', 'value':
        'Advance Graph', 'name': 'adSrhIDU4'}
    # this is used for storing DeviceTypeList e.g "odu16,odu100"
    device_type = ""
    # this is used for storing DeviceListState e.g "enabled"
    device_list_state = ""
    device_list_param = []
    if html.var("device_type") != None:  # we get the variable of page through html.var
        device_type = html.var("device_type")
    if html.var("device_list_state") != None:
        device_list_state = html.var("device_list_state")
    if host_id == None:
        host_id = ""
    device_list_param = get_device_param(host_id)
    html.header("IDU4 Monitoring")
    if device_list_param == [] or device_list_param == None:
        flag = 1
        output, mac_address = get_device_field(host_id)
        if int(output) == 1:
            html.write(page_header_search("", "", "IDU4Port",
                                          None, "enabled", "device_type", extr_button))
            # html.write(page_header_search("","","UBR,UBRe",device_type,"enabled","device_type",extr_button))
        else:
            html.write(page_header_search(host_id, mac_address, "IDU4Port",
                                          device_type, "enabled", "device_type", extr_button))
    else:
        html.write(
            page_header_search(
                device_list_param[0][0], device_list_param[0][1],
                "IDU4Port", device_list_param[0][2], device_list_state, "device_type", extr_button))
    if host_id == "" or host_id == "None":
        val = ""
        flag = 1
        html.write(
            "<div id=\"idu4_show_msg\"></div><div id=\"tab_yo\">There is no profile selected</div>")
    else:
        flag = 0
        html.write(
            "<div id=\"idu4_show_msg\"></div><div id=\"tab_yo\" style=\"display:block;overflow:hidden\">")
        idu4_dashboard(h)
        html.write("</div>")
    html.write(str(idu4View.idu4_footer_tab(flag)))
    html.new_footer()


def get_device_field(ip_address):
    """

    @param ip_address:
    @return: @raise:
    """
    try:
        mac_address = ''
        db, cursor = mysql_connection()  # create the connection
        if db == 1:
            raise SelfException(cursor)
        if Validation.is_valid_ip(ip_address):
            sel_query = "select mac_address from hosts where ip_address='%s'" % (
                ip_address)
            cursor.execute(sel_query)
            mac_result = cursor.fetchall()
            if len(mac_result) > 0:
                mac_address = mac_result[0][0]
        else:
            sel_query = "select mac_address from hosts where host_id='%s'" % (
                ip_address)
            cursor.execute(sel_query)
            mac_result = cursor.fetchall()
            if len(mac_result) > 0:
                mac_address = mac_result[0][0]
        return 0, mac_address
    except SelfException:
        return 1, str(e[-1])
        pass
    except Exception as e:
        return 1, str(e[-1])
    finally:
        if db.open:
            db.close()


# listing function
def get_device_list_idu4(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
    # this is the result which we show on the page
    result = ""
    ip_address = ""
    mac_address = ""
    selected_device = "odu16"
    # take value of IPaddress from the page through html.var
    # check that value is None Then It takes the empty string
    if html.var("ip_address") == None:
        ip_address = ""
    else:
        ip_address = html.var("ip_address")

    # take value of MACAddress from the page through html.var
    # check that value is None Then It takes the empty string
    if html.var("mac_address") == None:
        mac_address = ""
    else:
        mac_address = html.var("mac_address")

    # take value of SelectedDevice from the page through html.var
    # check that value is None Then It takes the empty string
    if html.var("selected_device_type") == None:
        selected_device = "odu16"
    else:
        selected_device = html.var("selected_device_type")

    # call the function get_odu_list of odu-controller which return us the
    # list of devices in two dimensional list according to
    # IPAddress,MACaddress,SelectedDevice
    result = get_device_list_odu_profiling(
        ip_address, mac_address, selected_device)
    if result == 0 or result == 1 or result == 2:
        html.write(str(result))
    else:
        db, cursor = mysql_connection('nms_sample')
        if db == 1:
            raise SelfException(cursor)
        sel_query = "select ip_address from hosts where host_id='%s'" % (
            result)
        cursor.execute(sel_query)
        ip_address = cursor.fetchall()
        if len(ip_address) > 0:
            html.write(str(ip_address[0][0]))
        else:
            html.write('0')


def idu4_dashboard(h):
    """

    @param h:
    """
    global html
    h = html
    idu_bll_obj = IDUDashboard()
    idu_refresh_time, total_count = idu_bll_obj.get_dashboard_data()
    host_id = html.var("host_id")
    now = datetime.now()
    odu_end_date = now.strftime("%d/%m/%Y")
    odu_end_time = now.strftime("%H:%M")
    now = now + timedelta(minutes=-int(total_count))
    odu_start_date = now.strftime("%d/%m/%Y")
    odu_start_time = now.strftime("%H:%M")
    result = idu_bll_obj.idu4_dashboard(host_id)
    if int(result['success']) == 0:
        html.write(
            idu4View.idu4_table(
                result['output'], odu_start_date, odu_start_time,
                odu_end_date, odu_end_time, str(idu_refresh_time), str(total_count)))
    else:
        if int(result['success']) == 2:
            html.write(
                'Mysql Services is not running mode so please contact your administrator.')
        else:
            html.write('No data exists')


def idu4_network_interface_graph(h):
    """

    @param h:
    """
    global html
    html = h
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    interface_value = html.var('interface_value')
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    output_result = idu_bll_obj.idu4_interface(
        odu_start_date, odu_start_time, odu_end_date,
        odu_end_time, interface_value, ip_address, limitFlag)
    html.write(str(output_result))


def idu4_tdmoip_network_interface_graph(h):
    """

    @param h:
    """
    global html
    html = h
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    interface_value = html.var('interface_value')
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    output_result = idu_bll_obj.idu4_tdmoip(
        odu_start_date, odu_start_time, odu_end_date,
        odu_end_time, interface_value, ip_address, limitFlag)
    html.write(str(output_result))


def idu4_port_statistics_graph(h):
    """

    @param h:
    """
    global html
    html = h
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    port = html.var('interface_value')
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    output_result = idu_bll_obj.idu4_port_statistics(
        odu_start_date, odu_start_time, odu_end_date, odu_end_time, port, ip_address, limitFlag)
    html.write(str(output_result))


def idu4_device_details(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    idu_bll_obj = IDUDashboard()
    output = idu_bll_obj.idu4_device_information(ip_address)
    view_output = ''
    if len(output['result']) > 0:
        view_output = idu4View.device_information_view(
            output['result'], ip_address)
    else:
        view_output = idu4View.device_information_view_default()
    html.write(str({'device_table': view_output, 'success': 0}))


def idu4_event_graph(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    idu_bll_obj = IDUDashboard()
    output_result = idu_bll_obj.idu4_event(ip_address)
    html.write(str(output_result))


def idu4_outage_graph(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    idu_bll_obj = IDUDashboard()
    output_result = idu_bll_obj.idu4_outage(ip_address)
    html.write(str(output_result))


def idu4_alarm_event_table(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    table_option = html.var('table_option')
    idu_bll_obj = IDUDashboard()
    output_result = idu_bll_obj.idu4_alarm_event(ip_address, table_option)
    if output_result['success'] == 1:
        html.write(str(output_result))
    else:
        html.write(str(idu4View.idu4_event_view(
            output_result['output'], table_option, ip_address)))


def idu4_pdf_generating(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    ip_address = html.var('ip_address')  # take ip_address from js side
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    select_option = html.var('select_option')
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    output = idu_bll_obj.idu4_pdf_report(
        ip_address, odu_start_date, odu_start_time,
        odu_end_date, odu_end_time, select_option, limitFlag)
    html.write(str(output))


def idu4_excel_generating(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    ip_address = html.var('ip_address')  # take ip_address from js side
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    select_option = html.var('select_option')
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    output = idu_bll_obj.idu4_excel_report(
        ip_address, odu_start_date, odu_start_time,
        odu_end_date, odu_end_time, select_option, limitFlag)
    html.write(str(output))


def idu4_add_date_time_on_slide(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        # calling the function
        idu_bll_obj = IDUDashboard()
        refresh_time, total_count = idu_bll_obj.get_dashboard_data()
        # start datetime and end datetime variable
        now = datetime.now()
        odu_end_date = now.strftime("%d/%m/%Y")
        odu_end_time = now.strftime("%H:%M")
        now = now + timedelta(minutes=-int(total_count))
        odu_start_date = now.strftime("%d/%m/%Y")
        odu_start_time = now.strftime("%H:%M")
        output_dict = {
            'success': 0, 'end_date': odu_end_date, 'end_time': odu_end_time,
            'start_date': odu_start_date, 'start_time': odu_start_time}
        html.write(str(output_dict))
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        html.write(str(output_dict))


def idu4_link_status_table(h):
    """

    @param h:
    """
    global html
    html = h
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    interface_value = html.var('interface_value')
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    link_status_result = idu_bll_obj.idu4_link_status(
        odu_start_date, odu_start_time, odu_end_date, odu_end_time, interface_value, ip_address, limitFlag)
    link_statistics_result = idu_bll_obj.idu4_linkstatistcis(
        odu_start_date, odu_start_time, odu_end_date, odu_end_time, interface_value, ip_address, limitFlag)
    if int(link_statistics_result['success']) == 1 or int(link_status_result['success']) == 1:
        output_result = {'success': 1, 'link_statistics_result':
            link_statistics_result, 'link_status_result': link_status_result}
    else:
        link_status_view_output = idu4View.idu4_link_status_view(
            link_status_result['output'], 1)
        output_result = {'success': 0, 'graph_result': link_statistics_result[
            'result'], 'table_result': link_status_view_output['output']}
    html.write(str(output_result))


def idu4_get_link_value_name(h):
    """

    @param h:
    """
    global html
    html = h
    idu_bll_obj = IDUDashboard()
    html.write(str(idu_bll_obj.idu4_get_link_name()))


def idu4_e1_port_status_table(h):
    """

    @param h:
    """
    global html
    html = h
    odu_start_date = html.var('start_date')
    odu_start_time = html.var('start_time')
    odu_end_date = html.var('end_date')
    odu_end_time = html.var('end_time')
    port_num = html.var('interface_value')
    ip_address = html.var("ip_address")
    limitFlag = html.var("limitFlag")
    idu_bll_obj = IDUDashboard()
    output = idu_bll_obj.idu4_e1_port_status(
        odu_start_date, odu_start_time, odu_end_date,
        odu_end_time, port_num, ip_address, limitFlag)
    if int(output['success']) == 1:
        link_statistics_output = idu4View.idu4_e1_port_statistics_view(
            output['output'], 1)
        output_result = {'success': 1, 'output': output['output']}
        html.write(str(output_result))
    else:
        link_statistics_output = idu4View.idu4_e1_port_statistics_view(
            output['output'], 0)
        output_result = {'success': 0, 'e1_port_graph': output['bpv'], 'e1_port_table':
            link_statistics_output['link_table'], 'time_stamp': output['timestamp']}
        html.write(str(output_result))


# def page_tip_idu4_monitor_dashboard(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_idu4_monitor_dashboard.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
