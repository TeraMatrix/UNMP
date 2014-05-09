#!/usr/bin/python2.6
# import the packeges
from datetime import datetime, timedelta
from json import JSONEncoder

import ap_advanced_graph_controller
from common_controller import *
from error_message import ErrorMessageClass
from mysql_collection import mysql_connection
from nms_config import *
from odu_controller import *
from specific_dashboard_bll import SPDashboardBll
from specific_dashboard_view import SPDashboardView
from utility import Validation

# create the global object of sp_bll_obj
global sp_bll_obj, err_obj
err_obj = ErrorMessageClass()
sp_bll_obj = SPDashboardBll()


def sp_dashboard_profiling(h):
    """

    @param h:
    """
    global html
    html = h
    flag = 0
    device_type = html.var("device_type")
    device_name_dict = {'odu16': 'RM18', 'odu100': 'RM', 'idu4': 'IDU',
                        'ap25': 'Access Point', 'ccu': 'CCU'}
    css_list = ["css/style.css", "css/custom.css",
                "calendrical/calendrical.css", 'css/ccpl_jquery_combobox.css']
    javascript_list = ["js/lib/main/highcharts.js", 'js/unmp/main/ccpl_jquery_autocomplete.js',
                       "js/unmp/main/specific_dashboard.js", "calendrical/calendrical.js"]
    host_id = ""
    host_id = html.var("host_id")
    selected_listing = ""
    device_type_id = html.var("device_type")
    if device_type_id == 'odu100' or device_type_id == 'odu16':
        selected_listing = "odu_listing.py"
    elif device_type_id == 'idu4':
        selected_listing = "idu_listing.py"
    elif device_type_id == 'ap25':
        selected_listing = "ap_listing.py"
    elif device_type_id == 'ccu':
        selected_listing = "ccu_listing.py"

    output, ip_address = get_device_field(host_id, "ip_address")
    ip_address = ip_address if int(output) == 0 else ""
    html.new_header(str(device_name_dict[device_type]) + " %s Dashboard" % (
        ip_address), selected_listing, SPDashboardView.header_buttons(), css_list, javascript_list)
    html.write('<div class=\"form-div\" >')
    extr_button = [{'tag': 'button', 'id': 'sp_ad_graph', 'value': 'Historical Graphs', 'name': 'sp_ad_graph'},
                   {'tag': 'button', 'id': 'sp_show_graph_list', 'value': 'Dashboard Configuration',
                    'name': 'sp_show_graph_list'}]
    device_type = ""
    device_list_state = ""
    device_list_param = []
    if html.var("device_type") != None:
        device_type = html.var("device_type")
    if html.var("device_list_state") != None:
        device_list_state = html.var("device_list_state")
    if host_id == None:
        host_id = ""
    device_list_param = get_device_param(host_id)
    if device_list_param == [] or device_list_param == None:
        flag = 1
        output, mac_address = get_device_field(host_id, "mac_address")
        if int(output) == 1:
            html.write(
                page_header_search(
                    "", "", "RM18,RM,Access Point,IDU,CCU", None,
                    "enabled", "device_type", extr_button))
        else:
            html.write(
                page_header_search(
                    host_id, mac_address, "RM18,RM,Access Point,IDU,CCU",
                    device_type, "enabled", "device_type", extr_button))
    else:
        logme(page_header_search(
            device_list_param[0][0], device_list_param[
                0][1], "RM18,RM,Access Point,IDU,CCU",
            device_list_param[0][2], device_list_state, "device_type", extr_button))
        html.write(
            page_header_search(
                device_list_param[0][0], device_list_param[
                    0][1], "RM18,RM,Access Point,IDU,CCU",
                device_list_param[0][2], device_list_state, "device_type", extr_button))
    if host_id == "" or host_id == "None":
        flag = 1
        html.write("<div id=\"sp_show_msg\"></div><div id=\"tab_yo\">There is no profile selected</div>")
    else:
        flag = 0
        html.write("<div id=\"sp_show_msg\"></div><div id=\"tab_yo\" style=\"display:block;overflow:hidden\">")
        sp_dashboard(h)
        html.write("</div>")
    html.write(str(SPDashboardView.sp_footer_tab(flag)))
    html.new_footer()


def get_device_field(ip_address, get_field):
    """

    @param ip_address:
    @param get_field:
    @return: @raise:
    """
    try:
        mac_address = ''
        db, cursor = mysql_connection()
        if db == 1:
            raise SelfException(cursor)
        if Validation.is_valid_ip(ip_address):
            sel_query = "select %s from hosts where ip_address='%s'" % (
                get_field, ip_address)
            cursor.execute(sel_query)
            mac_result = cursor.fetchall()
            if len(mac_result) > 0:
                mac_address = mac_result[0][0]
        else:
            sel_query = "select %s from hosts where host_id='%s'" % (
                get_field, ip_address)
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


def sp_client_information(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    device_type = h.var('device_type_id')
    h.req.content_type = 'application/json'
    output = sp_bll_obj.sp_ap_client_information(device_type, ip_address)
    view_output = ''
    if int(output['success']) == 0:
        view_output = SPDashboardView.sp_ap_client_table_view(output)
        output_dict = view_output
        h.req.write(str(JSONEncoder().encode(output_dict)))
    else:
        h.req.write(str(JSONEncoder().encode(output)))


def sp_add_date_time_on_slide(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        device_type = h.var('device_type_id')
        ip_address = h.var('ip_address')
        user_id = html.req.session["user_id"]
        refresh_time, total_count = sp_bll_obj.get_dashboard_data()
        graph_result = sp_bll_obj.sp_dashboard_get_graph_name(
            user_id, device_type, ip_address)
        now = datetime.now()
        sp_end_date = now.strftime("%d/%m/%Y")
        sp_end_time = now.strftime("%H:%M")
        now = now + timedelta(minutes=-int(total_count))
        sp_start_date = now.strftime("%d/%m/%Y")
        sp_start_time = now.strftime("%H:%M")
        h.req.content_type = 'application/json'
        if int(graph_result['success']) == 1:
            h.req.write(str(JSONEncoder().encode(graph_result['result'])))
        else:
            output_dict = {
                'success': 0, 'end_date': sp_end_date, 'end_time': sp_end_time, 'start_date': sp_start_date,
                'start_time': sp_start_time, 'show_graph_table': SPDashboardView.sp_get_graph(graph_result['selected'],
                                                                                              graph_result[
                                                                                                  'non_selected'])}

            h.req.write(str(JSONEncoder().encode(output_dict)))
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        h.req.content_type = 'application/json'
        h.req.write(str(JSONEncoder().encode(output_dict)))


def get_device_list_odu(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h
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
    #        welcome_odu_monitor_page(h)
        if Validation.is_valid_ip(result):
            ip_address = result
            if ip_address is not '' or ip_address is not None:
                html.write('0')
            else:
                html.write(str(ip_address[0][0]))
        else:
            db, cursor = mysql_connection()
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


def sp_dashboard(h):
    """

    @param h:
    """
    global html, sp_bll_obj
    h = html
    #    sp_bll_obj=SPDashboardBll()
    sp_refresh_time, total_count = sp_bll_obj.get_dashboard_data()
    host_id = html.var("host_id")
    now = datetime.now()
    sp_end_date = now.strftime("%d/%m/%Y")
    sp_end_time = now.strftime("%H:%M")
    now = now + timedelta(minutes=-int(total_count))
    sp_start_date = now.strftime("%d/%m/%Y")
    sp_start_time = now.strftime("%H:%M")
    result = sp_bll_obj.sp_dashboard(host_id)
    if int(result['success']) == 0:
        html.write(
            SPDashboardView.sp_table(
                result['output'], sp_start_date, sp_start_time,
                sp_end_date, sp_end_time, str(sp_refresh_time), str(total_count)))
    else:
        if int(result['success']) == 2:
            html.write(
                'Mysql Services is not running mode so please contact your administrator.')
        else:
            html.write('No data exists')


def sp_generic_json(h):
    """

    @param h:
    """
    global html, sp_bll_obj
    html = h
    device_type = h.var('device_type_id')
    ip_address = h.var('ip_address')
    user_id = html.req.session["user_id"]
    result_dict = sp_bll_obj.specific_all_graph_json(
        device_type, user_id, ip_address)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(result_dict)))


def sp_device_details(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    device_type = h.var('device_type_id')
    h.req.content_type = 'application/json'
    output = sp_bll_obj.sp_device_information(ip_address, device_type)
    view_output = ''
    if int(output['success']) == 0:
        view_output = SPDashboardView.device_information_view(
            output, ip_address)
        output_dict = {'device_table': view_output, 'success': 0}
        h.req.write(str(JSONEncoder().encode(output_dict)))
    else:
        h.req.write(str(JSONEncoder().encode(output)))


def sp_event_alarm_information(h):
    """

    @param h:
    """
    global html
    html = h
    ip_address = html.var("ip_address")
    device_type = h.var('device_type_id')
    h.req.content_type = 'application/json'
    output = sp_bll_obj.sp_event_alarm(ip_address, device_type)
    if output['success'] == 0 or output['success'] == 0:
        event_alarm_output = SPDashboardView.sp_event_alarm_table_view(
            output, ip_address)
        h.req.write(str(JSONEncoder().encode(event_alarm_output)))
    else:
        h.req.write(str(JSONEncoder().encode(output)))


def sp_common_graph_creation(h):
    """

    @param h:
    """
    global html, sp_bll_obj
    html = h
    display_type = 'graph'
    graph_type = html.var('graph_type')
    if int(graph_type) == 2:
        ap_advanced_graph_controller.advanced_graph_creation(
            h)  # This is call a advanced graph function
    else:
        table_name = html.var('table_name')
        column_value = html.var('field')
        cal_type = html.var('calType')
        interface_value = html.var('tab')
        graph_type = html.var('type')
        start_date = html.var('start_date')
        start_time = html.var('start_time')
        end_date = html.var('end_date')
        end_time = html.var('end_time')
        flag = html.var('flag')
        ip_address = html.var('ip_address')
        update_field = html.var('update')
        start = html.var('start')
        limit = html.var('limit')
        start_date = datetime.strptime(
            start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
        end_date = datetime.strptime(
            end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
        column_name = column_value.split(",")
        table_name = table_name.split(",")
        user_id = html.req.session["user_id"]
        if update_field == '' or update_field == None:
            update_field_name = ''
        else:
            update_field_name = update_field
        result_dict = sp_bll_obj.common_graph_json(
            display_type, user_id, table_name[0], table_name[1], table_name[-
            2], table_name[
                -1], flag, start_date, end_date, start, limit,
            ip_address, graph_type, update_field_name, interface_value, cal_type, column_name)
        h.req.content_type = 'application/json'
        h.req.write(str(JSONEncoder().encode(result_dict)))


def update_show_graph(h):
    """

    @param h:
    """
    global html
    html = h
    user_id = html.req.session["user_id"]
    device_type = html.var("device_type_id")
    show_graph = html.var("selected_graph")
    result = sp_bll_obj.update_show_graph_table(
        device_type, user_id, show_graph)
    html.write(str(result))


# def page_tip_sp_monitor_dashboard(h):
#         global html
#         html = h
#         import defaults
#         f = open(defaults.web_dir + "/htdocs/locale/page_tip_sp_monitor_dashboard.html", "r")
#         html_view = f.read()
#         f.close()
#         html.write(str(html_view))


def sp_excel_report_genrating(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    h.req.content_type = 'application/json'

    try:
        ip_address = html.var('ip_address')
        start_date = html.var('start_date')
        start_time = html.var('start_time')
        end_date = html.var('end_date')
        end_time = html.var('end_time')
        select_option = html.var('select_option')
        limitFlag = html.var("limitFlag")
        device_type_id = html.var('device_type_id')
        user_id = html.req.session["user_id"]
        result = sp_bll_obj.sp_total_display_graph(
            device_type_id, user_id, ip_address)
        if int(result['success']) == 0:
            total_show_graph = int(result['show_graph'])
            cal_list = []
            tab_list = []
            field_list = []
            table_name_list = []
            graph_name_list = []
            graph_list = []
            start_list = []
            limit_list = []
            for i in range(1, total_show_graph + 1):
                cal_list.append(html.var('cal%s' % i))
                tab_list.append(html.var('tab%s' % i))
                field_list.append(html.var('field%s' % i))
                table_name_list.append(html.var('table_name%s' % i))
                graph_name_list.append(html.var('graph_name%s' % i))
                graph_list.append(html.var('type%s' % i))
                start_list.append(html.var('start%s' % i))
                limit_list.append(html.var('limit%s' % i))
            if int(select_option) > 0:
                end_date = str(datetime.date(datetime.now()))
                start_time = '00:00'
                end_time = '23:59'
                if int(select_option) == 1:
                    start_date = str(datetime.date(datetime.now()))
                elif int(select_option) == 2:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-1))
                elif int(select_option) == 3:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-2))
                elif int(select_option) == 4:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-7))

                start_date = datetime.strptime(
                    start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
                end_date = datetime.strptime(
                    end_date + ' ' + end_time, "%Y-%m-%d %H:%M")
            else:
                start_date = datetime.strptime(
                    start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
                end_date = datetime.strptime(
                    end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
            result_dict = sp_bll_obj.sp_excel_report(
                device_type_id, user_id, ip_address, cal_list, tab_list, field_list, table_name_list, graph_name_list,
                start_date,
                end_date, select_option, limitFlag, graph_list, start_list, limit_list)
            h.req.write(str(JSONEncoder().encode(result_dict)))
        else:
            h.req.write(str(JSONEncoder().encode(result)))

    except Exception, e:
        output_dict = {'success': 1, 'error': str(e[-1])}
        h.req.write(str(JSONEncoder().encode(output_dict)))


def sp_csv_report_genrating(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    h.req.content_type = 'application/json'

    try:
        ip_address = html.var('ip_address')
        start_date = html.var('start_date')
        start_time = html.var('start_time')
        end_date = html.var('end_date')
        end_time = html.var('end_time')
        select_option = html.var('select_option')
        limitFlag = html.var("limitFlag")
        device_type_id = html.var('device_type_id')
        user_id = html.req.session["user_id"]
        result = sp_bll_obj.sp_total_display_graph(
            device_type_id, user_id, ip_address)
        if int(result['success']) == 0:
            total_show_graph = int(result['show_graph'])
            cal_list = []
            tab_list = []
            field_list = []
            table_name_list = []
            graph_name_list = []
            graph_list = []
            start_list = []
            limit_list = []
            for i in range(1, total_show_graph + 1):
                cal_list.append(html.var('cal%s' % i))
                tab_list.append(html.var('tab%s' % i))
                field_list.append(html.var('field%s' % i))
                table_name_list.append(html.var('table_name%s' % i))
                graph_name_list.append(html.var('graph_name%s' % i))
                graph_list.append(html.var('type%s' % i))
                start_list.append(html.var('start%s' % i))
                limit_list.append(html.var('limit%s' % i))
            if int(select_option) > 0:
                end_date = str(datetime.date(datetime.now()))
                start_time = '00:00'
                end_time = '23:59'
                if int(select_option) == 1:
                    start_date = str(datetime.date(datetime.now()))
                elif int(select_option) == 2:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-1))
                elif int(select_option) == 3:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-2))
                elif int(select_option) == 4:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-7))

                start_date = datetime.strptime(
                    start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
                end_date = datetime.strptime(
                    end_date + ' ' + end_time, "%Y-%m-%d %H:%M")
            else:
                start_date = datetime.strptime(
                    start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
                end_date = datetime.strptime(
                    end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
            result_dict = sp_bll_obj.sp_csv_report(
                device_type_id, user_id, ip_address, cal_list, tab_list, field_list, table_name_list, graph_name_list,
                start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list)

            h.req.write(str(JSONEncoder().encode(result_dict)))
        else:
            h.req.write(str(JSONEncoder().encode(result)))

    except Exception, e:
        output_dict = {'success': 1, 'error': str(e[-1])}
        h.req.write(str(JSONEncoder().encode(output_dict)))


def sp_pdf_report_genrating(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    h.req.content_type = 'application/json'
    try:
        ip_address = html.var('ip_address')
        start_date = html.var('start_date')
        start_time = html.var('start_time')
        end_date = html.var('end_date')
        end_time = html.var('end_time')
        select_option = html.var('select_option')
        limitFlag = html.var("limitFlag")
        device_type_id = html.var('device_type_id')
        user_id = html.req.session["user_id"]
        result = sp_bll_obj.sp_total_display_graph(
            device_type_id, user_id, ip_address)
        if int(result['success']) == 0:
            total_show_graph = int(result['show_graph'])
            cal_list = []
            tab_list = []
            field_list = []
            table_name_list = []
            graph_name_list = []
            graph_list = []
            start_list = []
            limit_list = []
            graph_id_list = []
            for i in range(1, total_show_graph + 1):
                cal_list.append(html.var('cal%s' % i))
                graph_id_list.append(html.var('graph_id%s' % i))
                tab_list.append(html.var('tab%s' % i))
                field_list.append(html.var('field%s' % i))
                table_name_list.append(html.var('table_name%s' % i))
                graph_name_list.append(html.var('graph_name%s' % i))
                graph_list.append(html.var('type%s' % i))
                start_list.append(html.var('start%s' % i))
                limit_list.append(html.var('limit%s' % i))
            if int(select_option) > 0:
                end_date = str(datetime.date(datetime.now()))
                start_time = '00:00'
                end_time = '23:59'
                if int(select_option) == 1:
                    start_date = str(datetime.date(datetime.now()))
                elif int(select_option) == 2:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-1))
                elif int(select_option) == 3:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-2))
                elif int(select_option) == 4:
                    start_date = str(
                        datetime.date(datetime.now()) + timedelta(days=-7))

                start_date = datetime.strptime(
                    start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
                end_date = datetime.strptime(
                    end_date + ' ' + end_time, "%Y-%m-%d %H:%M")
            else:
                start_date = datetime.strptime(
                    start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
                end_date = datetime.strptime(
                    end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
            result_dict = sp_bll_obj.sp_pdf_report(
                device_type_id, user_id, ip_address, cal_list, graph_id_list, tab_list, field_list, table_name_list,
                graph_name_list,
                start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list)
            h.req.write(str(JSONEncoder().encode(result_dict)))
        else:
            h.req.write(str(JSONEncoder().encode(result)))
    except Exception, e:
        output_dict = {'success': 1, 'error': str(e[-1])}
        h.req.write(str(JSONEncoder().encode(output_dict)))
