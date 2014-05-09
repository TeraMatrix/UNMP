#!/usr/bin/python2.6
from datetime import datetime
from datetime import timedelta
from json import JSONEncoder

from ap_advanced_graph_bll import APAdvancedGraph
from ap_advanced_graph_view import APAdvancedView
# from common_controller import *
# from nms_config import *
# from odu_controller import *


def get_ap_advanced_graph_value(h):
    """

    @param h:
    """
    global html
    html = h
    device_type_dict = {'ap25': 'AP25', 'odu16': 'RM18', 'odu100':
        'RM', 'idu4': 'IDU', 'ccu': 'CCU'}
    ip_address = html.var('ip_address')
    device_type_id = html.var('device_type_id')
    selected_listing = ""
    if device_type_id == 'odu100' or device_type_id == 'odu16':
        selected_listing = "odu_listing.py"
    elif device_type_id == 'idu4':
        selected_listing = "idu_listing.py"
    elif device_type_id == 'ap25':
        selected_listing = "ap_listing.py"
    elif device_type_id == 'ccu':
        selected_listing = "ccu_listing.py"
    user_id = html.req.session["user_id"]
    css_list = [
        "css/style.css", "css/custom.css", "calendrical/calendrical.css",
        "css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/lib/main/highcharts.js", "js/unmp/main/apAdvancedGraph.js",
                       "calendrical/calendrical.js", "js/lib/main/jquery.dataTables.min.js"]
    html.new_header(
        '%s %s Historical Graphs' % (device_type_dict[device_type_id],
                                     ip_address.replace("'", "")), selected_listing, "", css_list, javascript_list)
    html_content = APAdvancedView.ap_set_variable(
        ip_address, device_type_id, user_id)
    html.write(str(html_content))
    html.new_footer()


def ap_total_graph_name(h):
    """

    @param h:
    """
    global html
    html = h
    user_id = html.req.session["user_id"]
    device_type_id = html.var('device_type_id')
    ip_address = html.var('ip_address')
    ap_bll_obj = APAdvancedGraph()
    result_dict = ap_bll_obj.total_graph_name_display(device_type_id, user_id)
    controller_dict = APAdvancedView.graph_name_listing(
        result_dict, ip_address)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(controller_dict)))


def advanced_graph_json_creation(h):
    """

    @param h:
    """
    global html
    html = h
    graph_id = html.var('graph_id')
    device_type_id = html.var('device_type_id')
    ip_address = html.var('ip_address')
    user_id = html.req.session["user_id"]
    bll_obj = APAdvancedGraph()
    controller_dict = bll_obj.advanced_graph_json(
        graph_id, device_type_id, user_id, ip_address)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(controller_dict)))


def advanced_update_date_time(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        now = datetime.now()
        end_date = now.strftime("%d/%m/%Y")
        end_time = now.strftime("%H:%M")
        output_dict = {'success': 0, 'end_date': end_date,
                       'end_time': end_time}
    except Exception as e:
        output_dict = {'success': 1, 'output': str(e[-1])}
    finally:
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(output_dict)))


def advanced_graph_creation(h):
    """

    @param h:
    """
    global html
    html = h
    graph_type = html.var('graph_type')
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
    end_date = datetime.strptime(end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
    column_name = column_value.split(",")
    table_name = table_name.split(",")
    user_id = html.req.session["user_id"]
    if update_field == '' or update_field == None:
        update_field_name = ''
    else:
        update_field_name = update_field
    bll_obj = APAdvancedGraph()
    controller_dict = bll_obj.advanced_graph_data(
        'graph', user_id, table_name[0], table_name[1], table_name[-2], table_name[-
        1], start, limit, flag, start_date, end_date, ip_address,
        graph_type, update_field_name, interface_value, cal_type, column_name)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(controller_dict)))


def ap_data_table_creation(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    ip_address = html.var('ip_address')  # take ip_address from js side
    start_date = html.var('start_date')
    start_time = html.var('start_time')
    end_date = html.var('end_date')
    end_time = html.var('end_time')
    limitFlag = html.var("limitFlag")
    cal1 = html.var('cal1')
    tab1 = html.var('tab1')
    field1 = html.var('field1')
    table_name1 = html.var('table_name1')
    graph_name1 = html.var('graph_name1')
    graph1 = html.var('type1')
    start1 = html.var('start1')
    limit1 = html.var('limit1')
    start_date = datetime.strptime(
        start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
    end_date = datetime.strptime(end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
    user_id = html.req.session["user_id"]
    bll_obj = APAdvancedGraph()
    controller_dict = bll_obj.ap_data_table(
        user_id, ip_address, cal1, tab1, field1, table_name1, graph_name1, start_date, end_date, limitFlag, graph1,
        start1, limit1)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(controller_dict)))


def ap_advanced_excel_creating(h):
    """

    @param h:
    """
    global html
    html = h
    result1 = ''
    device_type = html.var('device_type_id')
    ip_address = html.var('ip_address')  # take ip_address from js side
    start_date = html.var('start_date')
    start_time = html.var('start_time')
    end_date = html.var('end_date')
    end_time = html.var('end_time')
    limitFlag = html.var("limitFlag")
    report_type = html.var("type")
    cal1 = html.var('cal1')
    tab1 = html.var('tab1')
    field1 = html.var('field1')
    table_name1 = html.var('table_name1')
    graph_name1 = html.var('graph_name1')
    graph1 = html.var('type1')
    start1 = html.var('start1')
    limit1 = html.var('limit1')
    select_option = html.var("select_option")
    if int(select_option) > 0:
        end_date = str(datetime.date(datetime.now()))
        start_time = '00:00'
        end_time = '23:59'
        if int(select_option) == 1:
            start_date = str(datetime.date(datetime.now()))
        elif int(select_option) == 2:
            start_date = str(
                datetime.date(datetime.now()) + timedelta(days=-7))
        elif int(select_option) == 3:
            start_date = str(
                datetime.date(datetime.now()) + timedelta(days=-15))
        elif int(select_option) == 4:
            start_date = str(
                datetime.date(datetime.now()) + timedelta(days=-30))

        start_date = datetime.strptime(
            start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(
            end_date + ' ' + end_time, "%Y-%m-%d %H:%M")
    else:
        start_date = datetime.strptime(
            start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
        end_date = datetime.strptime(
            end_date + ' ' + end_time, "%d/%m/%Y %H:%M")

    user_id = html.req.session["user_id"]
    bll_obj = APAdvancedGraph()
    controller_dict = bll_obj.advaeced_excel_report(
        report_type, device_type, user_id, ip_address, cal1, tab1, field1, table_name1, graph_name1, start_date,
        end_date,
        limitFlag, graph1, start1, limit1)
    html.write(str(controller_dict))


# def page_tip_advanced_dashboard(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_advanced_dashboard.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
