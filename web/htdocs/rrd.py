#!/usr/bin/python2.6

import os
from os.path import isfile
import subprocess

import rrdtool

# from utility import UNMPDeviceType# RRA: <consolidation function> : <XFiles factor> : <dataset> : <samples>
# DS: <name> : <DS type> : <heartbeat> : <lower limit> : <upper limit>
# import logging
# logging.basicConfig(filename='/omd/daemon/debug.log',format='%(levelname)s:
# %(asctime)s >> %(message)s', level=logging.DEBUG)

RRD_CONF_FILE = "/omd/daemon/rrd.conf"
LIVE_MONITORING_FILE = "/omd/daemon/live_monitor.py"


class UNMPDeviceType(object):
    '''
    @author: Yogesh Kumar
    @since: 20-Oct-2011
    @version: 0.1
    @var object: object of class object
    @summary: This Class use to define device types
    '''

    ap25 = "ap25"
    idu4 = "idu4"
    idu8 = "idu8"
    odu16 = "odu16"
    odu100 = "odu100"
    swt24 = "swt24"
    swt4 = "swt4"
    generic = "unknown"


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
    def get_peer_name(self):
        return ["1.1.1.1", "2.2.2.2"]


class RRDGraph(object):
    def __init__(self, device_type=None, ip_address=None, community="public", port=161, version="2c"):
        self.device_type = device_type
        self.ip_address = ip_address
        self.community = community
        self.port = port
        self.version = version
        self.stop_it = 0

    def write_tmp(self, file_path, given_table_dict=None, ip=None, community=None, port=None, version=None, action=None,
                  time_out=60):
        # logging.info(" in write testing ")
        st = ''
        file_flag = 0
        file_table_dict = None
        if isfile(file_path):
            # logging.info(" in write file file exists ")
            file_flag = 1
            f = open(file_path, 'r')
            exec f.read()
            f.close()
            try:
                if table_dict:
                    file_table_dict = table_dict
                else:
                    file_table_dict = {}
            except Exception, e:
                file_table_dict = {}

        key = given_table_dict.keys()[0]
        st = "\nsnmp_param = {'%s':['%s','%s']}" % (ip, community, port)
        if file_flag:
            # if file_table_dict.has_key(''):
            #    pass
            # else:
            if action == "start":
                file_table_dict[key] = given_table_dict[key]
            elif action == 'stop':
                if key in file_table_dict:
                    file_table_dict.pop(key)
                    if len(file_table_dict) == 0:
                        self.stop_it = 1
            st += "\ntable_dict=%s" % (file_table_dict)
        else:
            if action == "start":
                st += "\ntable_dict = { '%s' : %s } " % (
                    key, given_table_dict[key])
        st += "\ntimeout=%s" % (time_out)
        #        if self.stop_it == 0:
        f = open(file_path, 'w')
        f.write(st)
        f.close()
        # logging.info(" in write end "+st+' ::'+file_path)

    def rrd(self, table, action='start'):
        global RRD_CONF_FILE
        import traceback

        st_ = '  Nothing '
        try:

            from time import sleep, time

            rrd_graph = {}
            rrd_param = {}
            if isfile(RRD_CONF_FILE):
                f = open(RRD_CONF_FILE)
                exec f.read()
                f.close()
                self.rrd_step = int(rrd_param.get("rrd_step", 60))
                self.rrd_start = rrd_param.get("rrd_start", "N")
                self.root_path = rrd_param.get(
                    "rrd_file_path", "/omd/daemon/rrd/")
                t1 = time()
                graph = rrd_graph.get(self.device_type).get(table)
                # logging.info(" rrd start ")
                if isinstance(graph, dict) and self.device_type != None and self.ip_address != None:
                    self.rrd_step = graph["rrd_step"]
                    # logging.info(" in the IF ")
                    # files path
                    tmp_file_path = self.root_path + \
                                    self.device_type + "/" + \
                                    ''.join(self.ip_address.split('.')) + '.tmp'
                    rrd_file_path = self.root_path + ''.join(self.ip_address.split(
                        '.')) + "_" + self.device_type + "_" + graph["rrd_file_name"]

                    # check rrd file
                    if isfile(rrd_file_path):
                        pass
                    else:
                        # creating ds
                        new_ds = []
                        ds_count = len(graph["ds_name"])
                        row_column_count = len(
                            graph["row_index"]) * len(graph["column_index"])
                        if ds_count == row_column_count:
                            new_ds = graph["ds_name"]
                        elif ds_count > row_column_count:
                            new_ds = graph["ds_name"]
                            for ds_i in range(ds_count - row_column_count):
                                new_ds.pop(len(new_ds) - 1)
                        else:
                            new_ds = []
                            ex_count_temp = row_column_count - ds_count
                            for ds_i in range(1, row_column_count / ds_count):
                                for ds_nm in graph["ds_name"]:
                                    new_ds.append(str(ds_nm) + str(ds_i))
                            for ds_i in range(ex_count_temp):
                                new_ds.append("temp" + str(ds_i))
                            new_ds = graph["ds_name"] + new_ds
                            # creating ds
                        ds = []
                        rra = []
                        for d in new_ds:
                            ds.append("DS:%s:%s:%s:%s:%s" % (d, graph["ds_type"], graph[
                                "ds_heartbeat"], graph["ds_lower_limit"], graph["ds_upper_limit"]))

                        for r in range(len(graph['rra_cf'])):
                            rra.append("RRA:%s:%s:%s:%s" % (graph['rra_cf'][r], graph[
                                'rra_x_file_factor'][r], graph['rra_dataset'][r], graph['rra_samples'][r]))

                        self.create_rrd(rrd_file_path,
                                        self.rrd_start, self.rrd_step, ds, rra)

                    # check if a file exists
                    # create a file name then check file existing use it to change file name
                    # if exists then execute
                    try:
                        out = 0
                        # logging.info(" in try internal  "+str(graph))
                        if (graph["is_snmp"] == True):
                            table_dict = {str(table): {'row': graph["row_index"], 'col': graph["column_index"],
                                                       'oid': graph["oid_table"], 'file':
                                rrd_file_path, 'row_count': graph["row_count"],
                                                       'unreachable_value': graph["unreachable_value"]}}
                            # logging.info(" in try internal
                            # "+str(table_dict))
                            if isfile(tmp_file_path):  # 'file exist'
                                # logging.info(' file hai '+str(tmp_file_path))
                                self.write_tmp(
                                    tmp_file_path, table_dict, self.ip_address,
                                    self.community, self.port, self.version, action, self.rrd_step)
                                if action == 'stop':
                                    if self.stop_it:
                                        if os.path.isfile(tmp_file_path):
                                            os.unlink(tmp_file_path)
                                        subprocess.Popen(
                                            [LIVE_MONITORING_FILE, 'stop',
                                             tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                        output, err = popen_obj.communicate()
                                        out = output
                                        return
                                popen_obj = subprocess.Popen(
                                    [LIVE_MONITORING_FILE, 'status',
                                     tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                output, err = popen_obj.communicate()
                                if output.find('Service with the PID') != -1:
                                    pass
                                    # logging.info(' is running hai ')
                                else:
                                    subprocess.Popen(
                                        [LIVE_MONITORING_FILE, 'start',
                                         tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                    output, err = popen_obj.communicate()
                                    out = output
                                    return
                            else:
                                # logging.info(' no file so start
                                # '+tmp_file_path+action)
                                self.write_tmp(
                                    tmp_file_path, table_dict, self.ip_address,
                                    self.community, self.port, self.version, action, self.rrd_step)
                                popen_obj = subprocess.Popen(
                                    [LIVE_MONITORING_FILE, 'start',
                                     tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                output, err = popen_obj.communicate()
                                out = output
                                return
                    except Exception, e:
                        out = 1
                        print str(e)
                        st_ = str(traceback.format_exc())
                    finally:
                        return out

                        # popen call    #self.sleep_time # rrd_file_name,
                        # graph["timestamp"]
        except Exception, e:
            print str(e)
            st_ = str(traceback.format_exc())
            print str(e)

        finally:
            # f= open('/omd/daemon/debug.log','a')
            pass
            # f.write("\n  ok``````` "+str(st_))
            # f.close()

    def create_rrd(self, file_name, start, step, data_sources, rra):
        rrdtool.create(file_name,
                       '--start', str(start),
                       '--step', str(step),
                       data_sources, rra)

# rr = RRDGraph("odu100","172.22.0.120","public",161,"2c")
# rr.rrd("sync_loss","start")
