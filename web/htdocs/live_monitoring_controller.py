#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All Controller functions Related with Inventory.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


# Import modules that contain the function and libraries
from json import JSONEncoder

from rrd import RRDGraph

from common import Common
from inventory_bll import HostBll
from live_monitoring import LiveMonitoring
from live_monitoring_bll import LiveMonitoringBll


# Live Monitoring


def live_monitoring_page(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/lib/main/highcharts.js", "js/lib/main/jquery.dataTables.min.js",
               "js/unmp/main/live_monitoring.js"]
    header_btn = LiveMonitoring.header_buttons()

    selected_listing = "live_monitoring.py"
    device_type_id = html.var("device_type")
    if device_type_id == 'odu100' or device_type_id == 'odu16':
        selected_listing = "odu_listing.py"
    elif device_type_id == 'idu4':
        selected_listing = "idu_listing.py"
    elif device_type_id == 'ap25':
        selected_listing = "ap_listing.py"
    elif device_type_id == 'ccu':
        selected_listing = "ccu_listing.py"

    html.new_header(
        "Live Monitoring", selected_listing, header_btn, css_list, js_list)
    host_id = html.var("host_id")
    html.write(LiveMonitoring.live_monitring(host_id))
    html.new_footer()


def get_live_monitoring_graphs(h):
    global html
    html = h
    lm_bll = LiveMonitoringBll()
    monitoring_graphs = lm_bll.live_mortoring_data(
        html.var("device_type"), html.var("ip_address"), html.var("host_id"))
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(monitoring_graphs))


def get_graph_data(h):
    global html
    html = h
    lm_bll = LiveMonitoringBll()
    device_type = html.var("device_type")
    ip_address = html.var("ip_address")
    host_id = html.var("host_id")
    graph_name = html.var("graph_name")
    total = html.var("total")
    cf = html.var("cf")
    resolution = html.var(
        "resolution") != None and int(html.var("resolution")) or 1
    graph_data = lm_bll.graph_data(
        device_type, ip_address, host_id, graph_name, total, cf, resolution)
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(graph_data))


def live_graph_action(h):
    global html
    html = h
    lm_bll = LiveMonitoringBll()
    action = html.var("action")        # start/stop
    device_type = html.var("device_type")
    ip_address = html.var("ip_address")
    host_id = html.var("host_id")
    graph_name = html.var("graph_name")
    community = html.var("community")
    port = html.var("port")
    version = html.var("version")
    rr = RRDGraph(device_type, ip_address, community, int(port), version)
    rr.rrd(graph_name, action)
    html.write("0")


# def page_tip_live_monitoring(h):
#     global html
#     html = h
#     html.write(LiveMonitoring.page_tip_live_monitoring())


def settings_live_monitoring(h):
    global html
    html = h

    hst_bll = HostBll(
    )                             # creating the HostBll object

    # get device_type_select_list
    device = hst_bll.device_type()
    device_id = []
    device_name = []

    selected = html.var("device_type")
    list_id = "device_type"
    list_name = "device_type"
    title = "Choose Device Type"
    message = None  # "-- Select Device Type --"
    for dv in device:
        device_id.append(dv.device_type_id)
        device_name.append(dv.device_name)

    device_type_select_list = Common.make_select_list(
        device_id, device_name, selected, list_id, list_name, title, message)

    # get protocol list [cgi/snmp]
    value = ["1", "0"]
    name = ["SNMP", "CGI"]
    selected = "1"
    list_id = "is_snmp"
    list_name = "is_snmp"
    title = "Choose Protocol"
    protocol_select_list = Common.make_select_list(
        value, name, selected, list_id, list_name, title)

    # get protocol list [cgi/snmp]
    value = ["COUNTER", "DERIVE", "ABSOLUTE", "GAUGE"]
    name = ["Counter", "Derive", "Absolute", "Gauge"]
    selected = "COUNTER"
    list_id = "ds_type"
    list_name = "ds_type"
    title = "Choose type of dataset"
    dataset_select_list = Common.make_select_list(
        value, name, selected, list_id, list_name, title)

    # get ds_show_select_list list [-+U/-U/+U]
    value = ["-+U", "-U", "+U"]
    name = ["All", "Only Know Values", "Only Unknown Values"]
    selected = "-+U"
    list_id = "show_ds"
    list_name = "show_ds"
    title = "Select Dataset Show"
    ds_show_select_list = Common.make_select_list(
        value, name, selected, list_id, list_name, title)

    # get refresh_rate_select_list list[5/10/20/30/.....]
    value = ["5", "10", "15", "20", "30", "60", "120", "180", "240", "300"]
    name = ["5 sec", "10 sec", "15 sec", "20 sec", "30 sec", "1 min",
            "2 min", "3 min", "4 min", "5 min"]
    selected = "30"
    list_id = "rrd_step"
    list_name = "rrd_step"
    title = "Select Refresh Rate"
    refresh_rate_select_list = Common.make_select_list(
        value, name, selected, list_id, list_name, title)

    html.write(
        LiveMonitoring.settings_live_monitoring(
            device_type_select_list, protocol_select_list,
            dataset_select_list, ds_show_select_list, refresh_rate_select_list))


def save_live_monitoring_config(h):
    global html
    html = h
    device_type = html.var("device_type")
    graph_key = html.var("graph_key")

    new_rrd_param = {}
    new_rrd_param["rrd_step"] = html.var("rrd_step")

    new_graph_data = {}
    new_graph_data[graph_key] = {}

    new_graph_data[graph_key]["name"] = html.var("name")
    new_graph_data[graph_key]["desc"] = html.var("desc")
    new_graph_data[graph_key]["is_localhost"] = html.var("is_localhost")
    new_graph_data[graph_key]["is_snmp"] = html.var(
        "is_snmp") == "1" and True or False
    new_graph_data[graph_key]["oid_table"] = html.var("oid_table")
    new_graph_data[graph_key]["row_index"] = map(int, str(html.var(
        "row_index")).split(","))
    new_graph_data[graph_key]["column_index"] = map(int, str(html.var(
        "column_index")).split(","))
    new_graph_data[graph_key]["ds_name"] = map(str, str(html.var(
        "ds_name")).split(","))
    new_graph_data[graph_key]["ds_type"] = html.var("ds_type")
    new_graph_data[graph_key]["ds_heartbeat"] = html.var("ds_heartbeat")
    new_graph_data[graph_key]["ds_lower_limit"] = html.var("ds_lower_limit")
    new_graph_data[graph_key]["ds_upper_limit"] = html.var("ds_upper_limit")
    new_graph_data[graph_key]["unit"] = html.var("unit")
    new_graph_data[graph_key]["rrd_file_name"] = html.var("rrd_file_name")
    new_graph_data[graph_key]["timestamp"] = html.var("timestamp")
    new_graph_data[graph_key]["show_ds"] = html.var("show_ds")
    new_graph_data[graph_key]["dyn_ds_name"] = html.var("dyn_ds_name")
    new_graph_data[graph_key][
        "get_dyn_name"] = None  # html.var("get_dyn_name") == "" and None or html.var("get_dyn_name")
    new_graph_data[graph_key]["unreachable_value"] = html.var(
        "unreachable_value")

    rrd_step = int(html.var("rrd_step"))
    rrd_size = int(html.var("rrd_size")) * 60 * 60
    rra_cf = map(str, str(html.var("rra_cf")).split(","))
    rra_x_file_factor = []
    rra_dataset = map(int, str(html.var("rra_dataset")).split(","))
    rra_samples = []
    for i in range(0, len(rra_cf)):
        rra_x_file_factor.append('0.5')
        rra_samples.append((rrd_size / (rrd_step * rra_dataset[i])))
    new_graph_data[graph_key]["rrd_size"] = rrd_size
    new_graph_data[graph_key]["rra_cf"] = rra_cf
    new_graph_data[graph_key]["rra_x_file_factor"] = rra_x_file_factor
    new_graph_data[graph_key]["rra_dataset"] = rra_dataset
    new_graph_data[graph_key]["rra_samples"] = rra_samples
    new_graph_data[graph_key]["rrd_step"] = rrd_step

    result = LiveMonitoringBll().write_live_monitoring_config_file(
        device_type, new_graph_data, new_rrd_param)
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))


def load_live_monitoring_default_config(h):
    global html
    html = h
    result = LiveMonitoringBll().reload_default_live_monitoring_config_file()
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))


def download_live_monitoring_excel_file(h):
    global html
    html = h


def download_live_monitoring_csv_file(h):
    global html
    html = h
