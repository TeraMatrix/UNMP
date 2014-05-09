#!/usr/bin/python2.6

import rrdtool,sys
from daemon import Daemon

UNMP_RRD_FILE = "/omd/daemon/unmp_rrd.conf"

class Localhost(object):
    def get_cpu_usage(self,interval):
        from psutil import cpu_percent
        try:
            return cpu_percent(interval=interval, percpu=True)
        except Exception,e:
            return []

    def get_cpu_number(self):
        from psutil import NUM_CPUS
        try:
            cpu_name = []
            for i in range(NUM_CPUS):
                cpu_name.append("CPU_%s" % (i+1))
            return cpu_name
        except Exception,e:
            return []

    def get_interface_usage(self):
        from psutil import network_io_counters
        interface_bytes_list = [0,0]
        try:
            all_interface_bytes = network_io_counters(pernic=True)
            interface_name = None
            for inte in all_interface_bytes:
                if all_interface_bytes[inte].bytes_sent > 0 and all_interface_bytes[inte].bytes_recv > 0:
                    if str(inte).find("lo") == -1:
                        interface_name = inte
                        break
            if interface_name!=None:
                interface_bytes_list[0] = all_interface_bytes[interface_name].bytes_sent
                interface_bytes_list[1] = all_interface_bytes[interface_name].bytes_recv
            return interface_bytes_list
        except Exception,e:
            return interface_bytes_list

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

execfile(UNMP_RRD_FILE)

class RRD(object):
    def create_rrd(self,file_name,start,step,data_sources,rra,):
        rrdtool.create(file_name,
                       '--start', start,
                       '--step',step,
                       data_sources,rra)
        #print "RRD File Created"

    def insert_data(self,file_name,timestamp,data):
            rrdtool.update(file_name,'%s:%s' % (timestamp,":".join(map(str,data))))

class MonitorLocalhost(object):
    def __init__(self):
          self.rrd_graph = rrd_graph

    def unmp_server_rrd(self):
        from os.path import isfile
        from time import sleep
        while True:
            if(isinstance(self.rrd_graph, dict)):
                for graph in self.rrd_graph["graph"]:
                    if(isinstance(graph, dict)):
                        if isfile(self.rrd_graph["rrd_file_path"] + graph["rrd_file_name"]):
                            pass
                        else:
                            # creating ds
                            ds = []
                            rra = []
                            for d in graph["ds_name"]:
                                ds.append('DS:%s:%s:%s:%s:%s'%(d,graph["ds_type"],graph["ds_heartbeat"],graph["ds_lower_limit"],graph["ds_upper_limit"]))
                            for r in range(len(graph['rra_cf'])):
                                #'RRA:MIN:0.5:12:60',
                                rra.append('RRA:%s:%s:%s:%s'%(graph['rra_cf'][r],graph['rra_x_file_factor'][r],graph['rra_dataset'][r],graph['rra_samples'][r]))

                            RRD().create_rrd(self.rrd_graph["rrd_file_path"] + graph["rrd_file_name"],self.rrd_graph["rrd_start"],self.rrd_graph["rrd_step"],ds,rra)
                        #print graph["para"]
                        # is_snmp true/false
                        data = graph["function"](*graph["para"])
                        RRD().insert_data(self.rrd_graph["rrd_file_path"] + graph["rrd_file_name"],graph["timestamp"],data)
            else:
                #print "RRD graph configuration not in a well format"
                pass
            sleep(int(self.rrd_graph.get("rrd_step",5)))

class MyDaemon(Daemon):
    """
    this Class is calling main() and Daemonizing my localhost_monitor
    it extends Daemon class and provides start stop functioality for daemon
    """
    def run(self):
		try:
			MonitorLocalhost().unmp_server_rrd()
		except:
			print "error"

if __name__ == "__main__":
	daemon = MyDaemon('/omd/daemon/tmp/unmp-local.pid','unmp-local')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		else:
			print " Unknown command"
			print " Usage: unmp-local status | start | stop | restart | help  \n     Please use help option if you are using it first time"
			sys.exit(2)
		sys.exit(0)
	else:
		print " Usage: unmp-local status | start | stop | restart | help \n     Please use help option if you are using it first time"
		sys.exit(2)

