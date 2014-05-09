#!/usr/bin/python2.6
# import the packeges
from datetime import datetime, timedelta
from json import JSONEncoder

import ap_advanced_graph_controller
from client_dashboard_bll import ClientDashboardBll
from client_dashboard_view import ClientDashboardView
from common_controller import *
from error_message import ErrorMessageClass
from mysql_collection import mysql_connection
from nms_config import *
from odu_controller import *
from utility import Validation


# create the global object of sp_bll_obj
global sp_bll_obj, err_obj
err_obj = ErrorMessageClass()
client_bll_obj = ClientDashboardBll()


def client_dashboard_profiling(h):
    global html
    html = h
    flag = 0
    device_type = html.var("device_type")
    device_name_dict = {'odu16': 'RM18', 'odu100': 'RM', 'idu4': 'IDU',
                        'ap25': 'Access Point'}
    css_list = ["css/style.css", "css/custom.css",
                "calendrical/calendrical.css", 'css/ccpl_jquery_combobox.css']
    javascript_list = ["js/lib/main/highcharts.js", 'js/unmp/main/ccpl_jquery_autocomplete.js',
                       "js/unmp/main/client_dashboard.js", "calendrical/calendrical.js"]
    mac_address = ""
    # mac_address = html.var("mac_address")
    ap_mac_address = html.var("client_mac")
    # output,ip_address=get_device_field(host_id,"ip_address")
    # ip_address=ip_address if int(output)==0 else ""
    html.new_header(str(device_name_dict[device_type]) + " %s Dashboard" % (
        'Client'), "ap_listing.py", "", css_list, javascript_list)
    html.write('<div class=\"form-div\" >')
    extr_button = [{'tag': 'button', 'id': 'sp_ad_graph', 'value': 'Historical Graphs', 'name': 'sp_ad_graph'}, {'tag':
                                                                                                                     'button',
                                                                                                                 'id': 'sp_show_graph_list',
                                                                                                                 'value': 'Dashboard Configuration',
                                                                                                                 'name': 'sp_show_graph_list'}]
    device_type = ""
    device_list_state = ""
    device_list_param = []
    if html.var("device_type") is not None:
        device_type = html.var("device_type")
    if html.var("device_list_state") is not None:
        device_list_state = html.var("device_list_state")
    host_id = ''
    device_list_param = get_device_param(host_id)
    # default date time for graph showing 5 hr
    now = datetime.now()
    sp_end_date = now.strftime("%d/%m/%Y")
    sp_end_time = now.strftime("%H:%M")
    now = now + timedelta(minutes=-int(300))
    sp_start_date = now.strftime("%d/%m/%Y")
    sp_start_time = now.strftime("%H:%M")
    html.write("<div style=\"position: relative; display: block;\" id=\"filterOptions\">\
		<div style=\"float: right; font-size: 10px; color: rgb(85, 85, 85); font-weight: bold; padding: -2px 20px 0px 0px;\" >\
		<input type=\"text\" name=\"sp_start_date\" value=\"%s\" id=\"sp_start_date\" style=\"width:100px;\"/>\
		<input type=\"text\" name=\"sp_start_time\" value=\"%s\" id=\"sp_start_time\" style=\"width:80px;\"/>\
		<input type=\"text\" name=\"sp_end_date\" value=\"%s\" id=\"sp_end_date\" style=\"width:100px;\"/>\
		<input type=\"text\" name=\"sp_end_time\" value=\"%s\" id=\"sp_end_time\" style=\"width:80px;\"/>\
		<button id=\"advancedSrh\" type=\"submit\" class=\"yo-button yo-small\" style=\"margin-top:5px;\" onclick=\"advancedSrchBtn();\"><span>Go</span></button>\
		</div>\
    		<div>\
            	<input type=\"button\" style=\"margin-top: 2px;margin-left: 10px\" class=\"yo-small yo-button\" value=\"Dashboard Configuration\" name=\"sp_show_graph_list\" id=\"sp_show_graph_list\">\
            	<input type=\"button\" style=\"margin-top: 2px;\" class=\"yo-small yo-button\" value=\"Back\" name=\"back_to_ap\" id=\"back_to_ap\" >\
            	</div></div>" % (sp_start_date, sp_start_time, sp_end_date, sp_end_time))

    if ap_mac_address == "" or ap_mac_address is None:
        val = ""
        flag = 1
        html.write("<div id=\"sp_show_msg\"></div><div id=\"tab_yo\">There is no profile selected</div>")
    else:
        flag = 0
        html.write("<div id=\"sp_show_msg\"></div><div id=\"tab_yo\" style=\"display:block;overflow:hidden\">")
        client_dashboard(h)
        html.write("</div>")
    html.write(str(ClientDashboardView.sp_footer_tab(flag)))
    html.new_footer()


def client_add_date_time_on_slide(h):
    global html
    html = h
    try:
        device_type = h.var('device_type_id')
        user_id = html.req.session["user_id"]
        refresh_time, total_count = client_bll_obj.get_dashboard_data()
        graph_result = client_bll_obj.client_dashboard_get_graph_name(
            user_id, device_type)
        now = datetime.now()
        sp_end_date = now.strftime("%d/%m/%Y")
        sp_end_time = now.strftime("%H:%M")
        now = now + timedelta(minutes=-int(300))
        sp_start_date = now.strftime("%d/%m/%Y")
        sp_start_time = now.strftime("%H:%M")
        h.req.content_type = 'application/json'
        if int(graph_result['success']) == 1:
            h.req.write(str(JSONEncoder().encode(graph_result['result'])))
        else:
            output_dict = {'success': 0, 'end_date': sp_end_date, 'end_time': sp_end_time, 'start_date': sp_start_date,
                           'start_time': sp_start_time, 'show_graph_table':
                ClientDashboardView.sp_get_graph(graph_result['selected'], graph_result['non_selected'])}
            h.req.write(str(JSONEncoder().encode(output_dict)))
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
        h.req.content_type = 'application/json'
        h.req.write(str(JSONEncoder().encode(output_dict)))


def get_device_list_odu(h):
    global html
    html = h
    result = ""
    ip_address = ""
    mac_address = ""
    selected_device = "odu16"
    if html.var("ip_address") is None:
        ip_address = ""
    else:
        ip_address = html.var("ip_address")
    if html.var("mac_address") is None:
        mac_address = ""
    else:
        mac_address = html.var("mac_address")
    if html.var("selected_device_type") is None:
        selected_device = "odu16"
    else:
        selected_device = html.var("selected_device_type")
    result = get_device_list_odu_profiling(
        ip_address, mac_address, selected_device)
    if result == 0 or result == 1 or result == 2:
        html.write(str(result))
    else:
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


def client_dashboard(h):
    global html, client_bll_obj
    h = html
    sp_refresh_time, total_count = client_bll_obj.get_dashboard_data()
    mac_address = html.var("client_mac")
    path = html.var("path")
    host_id = html.var("host_id")
    #    now=datetime.now()
    #    sp_end_date=now.strftime("%d/%m/%Y")
    #    sp_end_time=now.strftime("%H:%M")
    #    now=now+timedelta(minutes=-int(total_count))
    #    sp_start_date=now.strftime("%d/%m/%Y")
    #   sp_start_time=now.strftime("%H:%M")
    html.write(ClientDashboardView.sp_table(
        mac_address, str(sp_refresh_time), str(total_count), path, host_id))


def client_generic_json(h):
    global html, sp_bll_obj
    html = h
    device_type = h.var('device_type_id')
    mac_address = h.var('mac_address')
    user_id = html.req.session["user_id"]
    result_dict = client_bll_obj.client_all_graph_json(
        device_type, user_id, mac_address)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(result_dict)))


def client_state_information(h):
    global html, client_bll_obj
    html = h
    mac_address = html.var("mac_address")
    h.req.content_type = 'application/json'
    output = client_bll_obj.client_state_data(mac_address)
    view_output = ''
    if int(output['success']) == 0:
        view_output = ClientDashboardView.sp_ap_client_table_view(output)
        output_dict = view_output
        h.req.write(str(JSONEncoder().encode(output_dict)))
    else:
        h.req.write(str(JSONEncoder().encode(output)))


def client_device_details(h):
    global html
    html = h
    mac_address = html.var("mac_address")
    h.req.content_type = 'application/json'
    output = client_bll_obj.client_device_information(mac_address)
    view_output = ''
    if int(output['success']) == 0:
        view_output = ClientDashboardView.client_information_view(output)
        output_dict = {'device_table': view_output, 'success': 0}
        h.req.write(str(JSONEncoder().encode(output_dict)))
    else:
        h.req.write(str(JSONEncoder().encode(output)))


def client_graph_creation(h):
    global html, client_bll_obj
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
        mac_address = html.var('mac_address')
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
        if update_field == '' or update_field is None:
            update_field_name = ''
        else:
            update_field_name = update_field
        result_dict = client_bll_obj.client_graph_json(
            display_type, user_id, table_name[0], table_name[1], table_name[-
            2], table_name[
                -1], flag, start_date, end_date, start, limit,
            mac_address, graph_type, update_field_name, interface_value, cal_type, column_name)
        h.req.content_type = 'application/json'
        h.req.write(str(JSONEncoder().encode(result_dict)))


def update_client_graph(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    device_type = html.var("device_type_id")
    show_graph = html.var("selected_graph")
    result = client_bll_obj.update_show_graph_table(
        device_type, user_id, show_graph)
    html.write(str(result))


# def page_tip_client_monitor_dashboard(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_client_monitor_dashboard.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))


def client_excel_report_genrating(h):
    global html
    html = h
    result1 = ''
    h.req.content_type = 'application/json'  # define the request type.

    try:
        mac_address = html.var('mac_address')  # take ip_address from js side
        start_date = html.var('start_date')
        start_time = html.var('start_time')
        end_date = html.var('end_date')
        end_time = html.var('end_time')
        select_option = html.var('select_option')
        limitFlag = html.var("limitFlag")
        device_type_id = html.var('device_type_id')
        user_id = html.req.session["user_id"]
        result = client_bll_obj.client_total_display_graph(
            device_type_id, user_id)
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
                #    start_date=datetime.strptime(start_date+' '+start_time,"%d/%m/%Y %H:%M")
                #    end_date=datetime.strptime(end_date+' '+end_time,"%d/%m/%Y %H:%M")
            result_dict = client_bll_obj.client_excel_report(
                device_type_id, user_id, mac_address, cal_list, tab_list, field_list, table_name_list, graph_name_list,
                start_date, end_date, select_option, limitFlag, graph_list, start_list, limit_list)
            h.req.write(str(JSONEncoder().encode(result_dict)))
        else:
            h.req.write(str(JSONEncoder().encode(result)))

    except Exception, e:
        output_dict = {'success': 1, 'error': str(e[-1])}
        h.req.write(str(JSONEncoder().encode(output_dict)))


def client_csv_report_genrating(h):
    global html
    html = h
    result1 = ''
    h.req.content_type = 'application/json'  # define the request type.

    try:
        mac_address = html.var('mac_address')  # take ip_address from js side
        start_date = html.var('start_date')
        start_time = html.var('start_time')
        end_date = html.var('end_date')
        end_time = html.var('end_time')
        select_option = html.var('select_option')
        limitFlag = html.var("limitFlag")
        device_type_id = html.var('device_type_id')
        user_id = html.req.session["user_id"]
        result = client_bll_obj.client_total_display_graph(
            device_type_id, user_id)
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
            result_dict = client_bll_obj.client_csv_report(
                device_type_id, user_id, mac_address, cal_list, tab_list, field_list, table_name_list, graph_name_list,
                start_date,
                end_date, select_option, limitFlag, graph_list, start_list, limit_list)
            h.req.write(str(JSONEncoder().encode(result_dict)))
        else:
            h.req.write(str(JSONEncoder().encode(result)))

    except Exception, e:
        output_dict = {'success': 1, 'error': str(e[-1])}
        h.req.write(str(JSONEncoder().encode(output_dict)))
