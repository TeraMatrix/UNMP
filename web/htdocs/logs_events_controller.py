#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 20-Apr-2012
@version: 0.1
@note: All Controller function Related with Logs and Events.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


# Import modules that contain the function and libraries
from logs_events import LogsEvents
from logs_events_bll import LogsEventsBll
from time import time
from json import JSONEncoder
from datetime import datetime

service_status_list = ["Ok","Warning","Critical","Unknown"]

# Logs
def manage_logs(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/device_logs.js"]
    snapin_list = []
    header_btn = LogsEvents().header_buttons()
    html.new_header("Global Logs","manage_logs.py",header_btn,css_list,js_list,snapin_list)
    html.write(LogsEvents().manage_logs())
    html.new_footer()

def search_logs(h):
    global html
    global service_status_list
    html = h
    host = html.var("host")
    service = html.var("service")
    logtime = html.var("logtime")
    logtime_ = ">"
    logtime_sec = html.var("logtime_sec")
    logtime_min = html.var("logtime_min")
    logtime_hours = html.var("logtime_hours")
    logtime_days = html.var("logtime_days")
    log_plugin_output = html.var("log_plugin_output")

    if logtime == "before":
        logtime_ = "<"

    time_stamp = int(time())
    try:
        logtime_sec = int(logtime_sec)
        logtime_min = int(logtime_min)
        logtime_hours = int(logtime_hours)
        logtime_days = int(logtime_days)
    except Exception,e:
        logtime_sec = 0
        logtime_min = 0
        logtime_hours = 0
        logtime_days = 0

    logtime_sec += logtime_min *60
    logtime_sec += logtime_hours *3600
    logtime_sec += logtime_days *86400
    time_stamp -= logtime_sec


    query_events = "GET log\nColumns: state log_time log_type host_name service_description log_plugin_output\nFilter: host_name ~~ %s\nFilter: service_description ~~ %s\nFilter: log_plugin_output ~~ %s\nFilter: log_time %s %s" % ("",service,log_plugin_output,logtime_,time_stamp)
    html.live.set_prepend_site(True)
    query_events_data = html.live.query(query_events)
    #query_events_data.sort()
    html.live.set_prepend_site(False)
    final_data = []
    hosts_dict = LogsEventsBll().get_hosts_dict()
    for i in range(len(query_events_data)):
        #if str(query_events_data[i][3]) != "":
        query_events_data[i][1] = "<span style=\"display:none;\">%s</span><img src=\"images/new/status-%s.png\" alt=\"%s\"/>" % (query_events_data[i][1],query_events_data[i][1],service_status_list[query_events_data[i][1]])
        query_events_data[i][2] = "<span style=\"display:none;\">%s</span>%s" % LogsEventsBll().convert_time(query_events_data[i][2])
        #datetime.fromtimestamp(query_events_data[i][2]).strftime('%Y-%m-%d %H:%M:%S')
        if hosts_dict.has_key(query_events_data[i][4]):
            query_events_data[i][4] = hosts_dict[query_events_data[i][4]]
        if host == "":
            final_data.append(query_events_data[i])
        elif query_events_data[i][4].find(host) != -1:
            final_data.append(query_events_data[i])
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(final_data))       
# End-Logs

# Events
def manage_events(h):
    global html
    html = h
    host=html.var("host") and html.var("host") or ""
    service=html.var("service") and html.var("service") or ""
    log_plugin_output=html.var("log_plugin_output") and html.var("log_plugin_output") or ""
    logtime_sec=html.var("logtime_sec") and html.var("logtime_sec") or 0
    logtime_min=html.var("logtime_min") and html.var("logtime_min") or 0
    logtime_hours=html.var("logtime_hours") and html.var("logtime_hours") or 0
    logtime_days=html.var("logtime_days") and html.var("logtime_days") or 1
    logtime=html.var("logtime") and html.var("logtime") or "since"

    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/device_events.js"]
    snapin_list = []
    header_btn = LogsEvents().header_buttons()
    html.new_header("Hosts and Service Events","manage_events.py",header_btn,css_list,js_list,snapin_list)
    html.write(LogsEvents().manage_events(host,service,log_plugin_output,logtime_sec,logtime_min,logtime_hours,logtime_days,logtime))
    html.new_footer()

def search_events(h):
    global html
    global service_status_list
    html = h
    host = html.var("host")
    service = html.var("service")
    logtime = html.var("logtime")
    logtime_ = ">"
    logtime_sec = html.var("logtime_sec")
    logtime_min = html.var("logtime_min")
    logtime_hours = html.var("logtime_hours")
    logtime_days = html.var("logtime_days")
    log_plugin_output = html.var("log_plugin_output")

    if logtime == "before":
        logtime_ = "<"

    time_stamp = int(time())
    try:
        logtime_sec = int(logtime_sec)
        logtime_min = int(logtime_min)
        logtime_hours = int(logtime_hours)
        logtime_days = int(logtime_days)
    except Exception,e:
        logtime_sec = 0
        logtime_min = 0
        logtime_hours = 0
        logtime_days = 0

    logtime_sec += logtime_min *60
    logtime_sec += logtime_hours *3600
    logtime_sec += logtime_days *86400
    time_stamp -= logtime_sec


    query_events = "GET log\nColumns: state log_time host_name service_description log_state_type log_plugin_output\nFilter: host_name ~~ %s\nFilter: service_description ~~ %s\nFilter: log_plugin_output ~~ %s\nFilter: log_time %s %s\nFilter: class = 1" % ("",service,log_plugin_output,logtime_,time_stamp)
    html.live.set_prepend_site(True)
    query_events_data = html.live.query(query_events)
    #query_events_data.sort()
    html.live.set_prepend_site(False)
    final_data = []
    hosts_dict = LogsEventsBll().get_hosts_dict()
    for i in range(len(query_events_data)):
        #if str(query_events_data[i][3]) != "":
        query_events_data[i][1] = "<span style=\"display:none;\">%s</span><img src=\"images/new/status-%s.png\" alt=\"%s\"/>" % (query_events_data[i][1],query_events_data[i][1],service_status_list[query_events_data[i][1]])
        query_events_data[i][2] = "<span style=\"display:none;\">%s</span>%s" % LogsEventsBll().convert_time(query_events_data[i][2])
        #datetime.fromtimestamp(query_events_data[i][2]).strftime('%Y-%m-%d %H:%M:%S')
        if hosts_dict.has_key(query_events_data[i][3]):
            query_events_data[i][3] = hosts_dict[query_events_data[i][3]]
        if host == "":
            final_data.append(query_events_data[i])
        elif query_events_data[i][3].find(host) != -1:
            final_data.append(query_events_data[i])
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(final_data))   

# End-Events