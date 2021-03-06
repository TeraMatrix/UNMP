#!/usr/bin/python2.6
import config
import htmllib
import time
import cgi
import MySQLdb
import sys
from common_controller import *
from nms_config import *
from odu_controller import *
from datetime import datetime
from datetime import timedelta
import time
from mysql_collection import mysql_connection
from utility import Validation
from operator import itemgetter
from advanced_status_view import AdvancedStatusView
from advanced_status_bll import AdvancedStatusBll
import json
from json import JSONEncoder
from encodings import undefined


global bll_obj
bll_obj = AdvancedStatusBll()


def get_advanced_status_value(h):
    global html, bll_obj
    html = h
    device_type_dict = {'ap25': 'AP25', 'odu16': 'RM18', 'odu100':
                        'RM', 'idu4': 'IDU'}
    ip_address = html.var('ip_address')
    device_type_id = html.var('device_type_id')
    user_id = html.req.session["user_id"]
    selected_listing = ""
    if device_type_id == 'odu100' or device_type_id == 'odu16':
        selected_listing = "odu_listing.py"
    elif device_type_id == 'idu4':
        selected_listing = "idu_listing.py"
    elif device_type_id == 'ap25':
        selected_listing = "ap_listing.py"
    elif device_type_id == 'ccu':
        selected_listing = "ccu_listing.py"

    css_list = [
        "css/style.css", "css/custom.css", "calendrical/calendrical.css",
        "css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/highcharts.js", "js/advanced_status.js",
                       "calendrical/calendrical.js", "js/jquery.dataTables.min.js"]
    html.new_header(
        '%s %s Historical Status' % (device_type_dict[device_type_id],
                                     ip_address.replace("'", "")), selected_listing, "", css_list, javascript_list)
    html_content = AdvancedStatusView.ap_set_variable(
        ip_address, device_type_id, user_id)
    html.write(str(html_content))
    html.new_footer()


def ap_total_status_name(h):
    global html, bll_obj
    html = h
    user_id = html.req.session["user_id"]
    device_type_id = html.var('device_type_id')
    ip_address = html.var('ip_address')
    result_dict = bll_obj.total_graph_name_display(device_type_id, user_id)
    controller_dict = AdvancedStatusView.graph_name_listing(
        result_dict, ip_address)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(controller_dict)))


def advanced_status_json_creation(h):
    global html, bll_obj
    html = h
    graph_id = html.var('graph_id')
    device_type_id = html.var('device_type_id')
    ip_address = html.var('ip_address')
    user_id = html.req.session["user_id"]
    controller_dict = bll_obj.advanced_graph_json(
        graph_id, device_type_id, user_id, ip_address)
    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(controller_dict)))


def advanced_status_update_date_time(h):
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


def advanced_status_creation(h):
    global html, bll_obj
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
    controller_dict = bll_obj.advanced_graph_data(
        'graph', user_id, table_name[0], table_name[1], table_name[-2], table_name[-
                                                                                   1], start, limit, flag, start_date, end_date, ip_address,
        graph_type, update_field_name, interface_value, cal_type, column_name)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(controller_dict)))


def status_data_table_creation(h):
    global html, bll_obj
    html = h
    result1 = ''
    ip_address = html.var('ip_address')  # take ip_address from js side
    start_date = html.var('start_date')
    start_time = html.var('start_time')
    end_date = html.var('end_date')
    end_time = html.var('end_time')
    device_type = html.var('device_type')
    graph_id = html.var('graph_id')
    start_date = datetime.strptime(
        start_date + ' ' + start_time, "%d/%m/%Y %H:%M")
    end_date = datetime.strptime(end_date + ' ' + end_time, "%d/%m/%Y %H:%M")
    user_id = html.req.session["user_id"]
    controller_dict = bll_obj.ap_data_table(
        user_id, ip_address, start_date, end_date, graph_id, device_type)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(controller_dict)))


def advanced_status_excel_creating(h):
    global html, bll_obj
    html = h
    result1 = ''
    device_type = html.var('device_type_id')
    ip_address = html.var('ip_address')  # take ip_address from js side
    start_date = html.var('start_date')
    start_time = html.var('start_time')
    end_date = html.var('end_date')
    end_time = html.var('end_time')
    report_type = html.var("type")
    graph_id = html.var("graph_id")
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
    controller_dict = bll_obj.advaeced_excel_report(
        report_type, device_type, user_id, ip_address, start_date,
        end_date, graph_id, select_option)
#    html.req.content_type = 'application/json'
#    html.req.write(str(JSONEncoder().encode(controller_dict)))
    html.write(str(controller_dict))


def page_tip_advanced_status(h):
        global html
        html = h
        html_view = ""
        html_view = ""\
            "<div id=\"help_container\">"\
            "<h1>Dashboard</h1>"\
            "<div>This <strong>Dashboard</strong> show all device silver statistics information by graph.</div>"\
            "<br/>"\
            "<br/>"\
            "<div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/back.jpeg\"/></div><div class=\"txt-div\">Back to current status page.</div></div>"\
            "<br/>"\
            "<div><input class=\"yo-button yo-small\" type=\"button\" style=\"width: 30px;\" value=\"Historical Status\" name=\"odu_graph_show\"> This button open a window on self click and show more information by historical status.</div>"\
            "<div><input class=\"yo-button yo-small\" type=\"button\" style=\"width: 30px;\" value=\"Search\" name=\"odu_graph_show\"> Search the devices.</div>"\
            "<div><input class=\"yo-button yo-small\" type=\"button\" style=\"width: 50px;\" value=\"Configuration\" name=\"odu_graph_show\"> This is open a window for customize the graph according to User.</div>"\
            "<br/>"\
            "<div><button id=\"odu_report_btn\" class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\"><span class=\"report\">Report</span></button>Download the Excel report.</div>"\
            "<br/>"\
            "<div><button id=\"odu_report_btn\" class=\"yo-button\" style=\"margin-top: 5px;\" type=\"submit\"><span class=\"report\">CSV Report</span></button>Download the CSV report.</div>"\
            "<br/>\
        <br/>\
        <div><strong>Note:</strong>This page show real time information of device and it page refresh on 5 min time interval.\
        Search button search device by MAC address and IP address and show information by table.\
        </div>"\
        "</div>"
        html.write(str(html_view))
