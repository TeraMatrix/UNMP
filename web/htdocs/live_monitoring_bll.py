#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All database and model's functions Related with Inventory. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
from unmp_model import *
from utility import ErrorMessages,Validation,HostState,NagiosConfiguration,SystemSetting,DiscoveryName,PingDiscovery,SnmpDiscovery,UpnpDiscovery,UNMPDeviceType
from unmp_config import SystemConfig
from sqlalchemy import and_,or_,desc,asc
from pysnmp_module import pysnmp_set
from py_module import snmp_ping 
import MySQLdb
from json import JSONEncoder
from os.path import isfile
from time import time
import rrdtool

class DSType(object):
    counter = "COUNTER"
    derive = "DERIVE"
    absolute = "ABSOLUTE"
    gauge = "GAUGE"

class RRACF(object):
    average = "AVERAGE"
    min = "MIN" 
    max = "MAX"
    last = "LAST"

class RRDUtlityFunction(object):
    def get_peer_name(self,host_id):
        return ["1.1.1.1","2.2.2.2"]
    
class LiveMonitoringBll(object):
    def live_mortoring_data(self,device_type,ip_address,host_id):
        rrd_conf_file = "/omd/daemon/rrd.conf"
        graphs = {}
        rrd_graph = {}
        rrd_param = {}
            
        if isfile(rrd_conf_file):
            f = open(rrd_conf_file,'r')
            exec f.read()
            f.close()
            rrd_step = int(rrd_param.get("rrd_step",5))
            rrd_start = rrd_param.get("rrd_start","N")
            root_path = rrd_param.get("rrd_file_path","/omd/daemon/rrd/" )
            graphs = rrd_graph.get(device_type)
            tmp_file = root_path + "/" + device_type + "/" + ''.join(ip_address.split('.')) + '.tmp'
            table_dict={}
            if isfile(tmp_file):
                f = open(tmp_file,'r')
                exec f.read()
                f.close()
                for graph in graphs:
                    if table_dict.has_key(graph):
                        graphs[graph]["live_status"] = True
                    else:
                        graphs[graph]["live_status"] = False
                    if graphs[graph]["get_dyn_name"] != None:
                        graphs[graph]["get_dyn_name"] = graphs[graph]["get_dyn_name"](host_id)
                    graphs[graph]["ds_type"] = str(graphs[graph]["ds_type"])
                    for i in range(len(graphs[graph]["rra_cf"])):
                        graphs[graph]["rra_cf"][i] = str(graphs[graph]["rra_cf"][i])
            else:
                for graph in graphs:
                    graphs[graph]["live_status"] = False
                    if graphs[graph]["get_dyn_name"] != None:
                        graphs[graph]["get_dyn_name"] = graphs[graph]["get_dyn_name"](host_id)
                    graphs[graph]["ds_type"] = str(graphs[graph]["ds_type"])
                    for i in range(len(graphs[graph]["rra_cf"])):
                        graphs[graph]["rra_cf"][i] = str(graphs[graph]["rra_cf"][i])
            return graphs
        else:
            return graphs
            
    def convert_utc_to_ist(self,timestamp):
        offset_ist = 5.5
        return timestamp + ((offset_ist*60)*60000)
        
    def graph_data(self,device_type,ip_address,host_id,graph_name,total):
        sec = 60
        total = int(total)
        total_sec = int(total)*sec+sec
        rrd_conf_file = "/omd/daemon/rrd.conf"
        graph = {}
        rrd_graph = {}
        rrd_param = {}
        data_series = []
        is_live = False
        unit = "unit"
        if isfile(rrd_conf_file):
            f = open(rrd_conf_file,'r')
            exec f.read()
            f.close()
            rrd_step = int(rrd_param.get("rrd_step",60))
            rrd_start = rrd_param.get("rrd_start","N")
            root_path = rrd_param.get("rrd_file_path","/omd/daemon/rrd/" )
            graph = rrd_graph.get(device_type).get(graph_name,{})
            graph_file = root_path + ''.join(ip_address.split('.')) + "_" + device_type + "_" + str(graph.get("rrd_file_name"))
            tmp_file = root_path + "/" + device_type + "/" + ''.join(ip_address.split('.')) + '.tmp'
            unit = graph["unit"]
            if isfile(graph_file):
                table_dict={}
                if isfile(tmp_file):
                    f = open(tmp_file,'r')
                    exec f.read()
                    f.close()
                    if table_dict.has_key(graph_name):
                        is_live = True
                fetch_data = rrdtool.fetch(graph_file, 'AVERAGE', '-s','-%ssec' % total_sec)
                if len(fetch_data) == 3:
                    timestamp = fetch_data[0]
                    label = fetch_data[1]
                    data = fetch_data[2]
                    for i in range(len(label)):
                        data_series.append({"name":str(label[i]).replace("_"," "),"data":[]})
                    for i in range(len(data)):
                        if total != 0:
                            for lbl_i in range(len(label)):
                                if graph["show_ds"] == "-+U":
                                    data_series[lbl_i]["data"].append({"x":self.convert_utc_to_ist((timestamp[0]+(timestamp[2]*(i)))*1000),"y":data[i][lbl_i]})
                                    if lbl_i == 0:
                                        total-=1
                                elif graph["show_ds"] == "-U":
                                    if data[i][lbl_i] != None:
                                        data_series[lbl_i]["data"].append({"x":self.convert_utc_to_ist((timestamp[0]+(timestamp[2]*(i)))*1000),"y":data[i][lbl_i]})
                                        if lbl_i == 0:
                                            total-=1
                                else:
                                    if data[i][lbl_i] == None:
                                        data_series[lbl_i]["data"].append({"x":self.convert_utc_to_ist((timestamp[0]+(timestamp[2]*(i)))*1000),"y":data[i][lbl_i]})
                                        if lbl_i == 0:
                                            total-=1
                return {"data_series":data_series,"is_live":is_live,"unit":unit}    
            else:
                # creating ds
                new_ds=[]
                ds_count = len(graph["ds_name"])
                row_column_count = len(graph["row_index"]) * len(graph["column_index"])
                if ds_count==row_column_count:
                    new_ds = graph["ds_name"]
                elif ds_count>row_column_count:
                    new_ds = graph["ds_name"]
                    for ds_i in range(ds_count-row_column_count):
                        new_ds.pop(len(new_ds)-1)
                else:
                    new_ds = []
                    ex_count_temp = row_column_count - ds_count
                    for ds_i in range(1,row_column_count/ds_count):
                        for ds_nm in graph["ds_name"]:
                            new_ds.append(str(ds_nm) + str(ds_i))
                    for ds_i in range(ex_count_temp):
                        new_ds.append("temp" + str(ds_i))
                    new_ds = graph["ds_name"] + new_ds
                # creating ds
                label = new_ds
                timestamp = int(time() - total_sec)
	        for i in range(len(label)):
	            data_series.append({"name":str(label[i]).replace("_"," "),"data":[]})
	          
	        for i in range(int(total)):
	            for lbl_i in range(len(label)): 
	                data_series[lbl_i]["data"].append({"x":self.convert_utc_to_ist((timestamp+(sec*(i)))*1000),"y":0})
	                          
                return {"data_series":data_series,"is_live":is_live,"unit":unit}
        else:
            return {"data_series":data_series,"is_live":is_live,"unit":unit}
            
