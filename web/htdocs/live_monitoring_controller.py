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
from live_monitoring_bll import LiveMonitoringBll
from live_monitoring import LiveMonitoring
from inventory_bll import HostBll
from json import JSONEncoder
from rrd import RRDGraph

# Live Monitoring
def live_monitoring_page(h):
    global html
    html = h
    css_list = []
    js_list = ["js/highcharts.js","js/pages/live_monitoring.js"]
    header_btn = LiveMonitoring.header_buttons()
    html.new_header("Live Monitoring","live_monitoring.py",header_btn,css_list,js_list)
    host_id = html.var("host_id")
    #lm_bll = LiveMonitoringBll()
    #host_obj = HostBll().get_host_by_id(host_id)
    #graph_list = lm_bll.live_mortoring_data(host_obj["device_type"],host_obj["ip_address"])
    #html.write(LiveMonitoring.live_monitring(host_obj,graph_list))
    html.write(LiveMonitoring.live_monitring(host_id))
    html.new_footer()

def get_live_monitoring_graphs(h):
    global html
    html = h
    lm_bll = LiveMonitoringBll()
    monitoring_graphs = lm_bll.live_mortoring_data(html.var("device_type"),html.var("ip_address"),html.var("host_id"))
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(monitoring_graphs))
    #html.write(str(monitoring_graphs))
    
def get_graph_data(h):
    global html
    html = h
    lm_bll = LiveMonitoringBll()
    device_type = html.var("device_type")
    ip_address = html.var("ip_address")
    host_id = html.var("host_id")
    graph_name = html.var("graph_name")
    total = html.var("total")
    graph_data = lm_bll.graph_data(device_type,ip_address,host_id,graph_name,total)
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(graph_data))
    
def live_graph_action(h):
    global html
    html = h
    lm_bll = LiveMonitoringBll()
    action = html.var("action")		# start/stop
    device_type = html.var("device_type")
    ip_address = html.var("ip_address")
    host_id = html.var("host_id")
    graph_name = html.var("graph_name")
    community = html.var("community")
    port = html.var("port")
    version = html.var("version")
    rr = RRDGraph(device_type,ip_address,community,int(port),version)
    rr.rrd(graph_name,action)
    html.write("0")
    
