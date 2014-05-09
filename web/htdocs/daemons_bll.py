#!/usr/bin/python2.6
'''
@author: Mahipal Choudhary
@since: 02-Nov-2011
@version: 0.1
@note: All BLL functions needed with daemons management
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''
import atexit
import os
from signal import SIGTERM
import subprocess
import sys
import time

from common_bll import EventLog


# dict_port={1:"-",2:"6790",3:"-",4:"-"}
# dict_id={1:"unmp-alarm",2:"unmp-ds",3:"unmp-nbi-supplier",4:"unmp-local"}
# dict_name={1:"Alarm Parser",2:"Auto Discovery server",3: "NBI Service",4:"UNMP System Monitor"}
# dict_pid={1:"/omd/daemon/tmp/unmp-trap.pid",2:"/omd/daemon/tmp/unmp-ds.pid",3:"/omd/daemon/tmp/unmp-nbi-supplier.pid",4:"/omd/daemon/tmp/unmp-local.pid"}
# dict_details={1:"UNMP core process to capture and log Traps, Alarms and
# Alerts.",2:"UNMP device discovery server.",3:"UNMP core process for trap
# forwarding",4:"UNMP core process for UNMP System Monitor"}

dict_port = {1: "-", 2: "6790", 3: "-"}
dict_id = {1: "unmp-alarm", 2: "unmp-ds", 3: "unmp-local", 4: "nagios"}
dict_name = {1: "Alarm Parser", 2: "Auto Discovery server", 3:
    "UNMP System Monitor", 4: "Nagios"}
dict_pid = {1: "/omd/daemon/tmp/unmp-trap.pid", 2: "/omd/daemon/tmp/unmp-ds.pid", 3:
    "/omd/daemon/tmp/unmp-local.pid", 4: "nagios"}
dict_details = {1: "UNMP core process to capture and log Traps, Alarms and Alerts.", 2:
    "UNMP device discovery server.", 3: "UNMP core process for UNMP System Monitor", 4: "Nagios core process"}


def load():
    global dict_pid, dict_id
    dict_status = {}
    s = ""
    for i in dict_pid:
        status = get_status(dict_pid[i])
        s = s + str(dict_id[i]) + "," + str(status) + \
            ","  # dict_status[i]=status
    return s


def doAction(daemonName, action, username):
    import datetime

    time1 = datetime.datetime.now()
    if daemonName == 'nagios':
        return do_action_nagios(action)
    daemonPath = "/omd/sites/UNMP/etc/init.d/" + \
                 daemonName  # daemonName = unmp-ds, unmp-alarm
    if not os.path.isfile(daemonPath):
        return 1
    try:
        if daemonName == 'unmp-nbi-supplier':
            daemonPath1 = '/etc/init.d/' + 'unmp-nbi-naming'
            daemonPath2 = '/etc/init.d/' + 'unmp-nbi-notify'
            daemonPath3 = '/etc/init.d/' + 'unmp-nbi-supplier'
            if not (os.path.isfile(daemonPath1) and os.path.isfile(daemonPath2)):
                return 1

            if action == 'start':
                proc = subprocess.Popen([daemonPath1, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath2, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath3, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif action == 'stop':
                proc = subprocess.Popen([daemonPath3, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath2, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath1, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif action == 'restart':
                proc = subprocess.Popen([daemonPath3, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath2, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath1, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath1, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath2, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                code = proc.wait()
                proc = subprocess.Popen([daemonPath3, action],
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            output, _ = proc.communicate()
            code = proc.wait()
        else:
            proc = subprocess.Popen(
                [daemonPath, action], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = proc.communicate()
            code = proc.wait()
            # return output
            # return 0

    except ValueError as e:
        el = EventLog()
        # time2 = datetime.datetime.now()
        desc = str(e)
        el.log_event(desc, username, 1)
        return 1
    if (output.find("[Errno 1] Operation not permitted") == -1):
        el = EventLog()
        actionlog = action
        if action == 'stop':
            actionlog = 'stopp'
        key_daemon = [key for key, value in dict_id.iteritems(
        ) if value == daemonName]
        desc = "Daemon %s is %sed" % (dict_name[key_daemon[0]], actionlog)
        # time2 = datetime.datetime.now()
        el.log_event(desc, username, 0)
        return 0
    else:
        el = EventLog()
        # time2 = datetime.datetime.now()
        key_daemon = [key for key, value in dict_id.iteritems(
        ) if value == daemonName]
        desc = "operation not permitted to %s the daemon %s " % (
            action, dict_name[key_daemon[0]])
        el.log_event(desc, username, 1)
        return 2
    if action in ('stop', 'restart'):
        time.sleep(1)
    return 0


def get_status(pidfile):
    try:
        if pidfile == 'nagios':
            return get_nagios_status()
        if pidfile == '/omd/daemon/tmp/unmp-nbi-supplier.pid' or pidfile == '/omd/daemon/tmp/unmp-nbi-supplier.pid':
            pf1 = file(pidfile, 'r')
            pf2 = file('/omd/daemon/tmp/unmp-nbi-notify.pid', 'r')
            pf3 = file('/omd/daemon/tmp/unmp-nbi-naming.pid', 'r')
            pfid1 = pf1.read().strip()
            pfid2 = pf2.read().strip()
            pfid3 = pf3.read().strip()

            if pfid1 != '' and pfid1 != None and pfid2 != '' and pfid2 != None and pfid3 != '' and pfid3 != None:
                pid1 = int(pfid1)
                pid2 = int(pfid2)
                pid3 = int(pfid3)
            else:
                pid1 = 0
                pid2 = 0
                pid3 = 0
            pf1.close()
            pf2.close()
            pf3.close()
        else:
            pf = file(pidfile, 'r')
            pfid = pf.read().strip()
            if pfid != '' and pfid != None:
                pid = int(pfid)
            else:
                pid = 0
            pf.close()
    except IOError:
        pid = None
        pid1 = None
        pid2 = None
        pid3 = None

    try:
        if pidfile == '/omd/daemon/tmp/unmp-nbi-supplier.pid' or pidfile == '/omd/daemon/tmp/unmp-nbi-supplier.pid':
            procfile1 = file("/proc/%d/status" % pid1, 'r')
            procfile1.close()
            procfile2 = file("/proc/%d/status" % pid2, 'r')
            procfile2.close()
            procfile3 = file("/proc/%d/status" % pid3, 'r')
            procfile3.close()
        else:
            procfile = file("/proc/%d/status" % pid, 'r')
            procfile.close()
    except IOError, err:
        return 1  # +str(type(pid))# sys.stdout.write("  *Probably Daemon Service is not running. There is not a process with the PID specified in PidFile  **try to start it\n")
    except TypeError, err:
        return 1  # +str(type(pid))#sys.stdout.write("  *Daemon Service is not running. \n")

    return 0  # sys.stdout.write("  *Daemon Service with the PID %d is [32mrunning [0m          [42m OK [0m \n" % pid)


def get_nagios_status():
    try:
        # proc = subprocess.Popen(["omd status nms nagios"],
        # stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process = subprocess.Popen(
            'omd status nagios', shell=True, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        code = process.wait()
        if output.find("running") != -1:
            output = 0
        else:
            output = 1
        return output
    except Exception, e:
        return 1


def do_action_nagios(action):
    try:
        process = subprocess.Popen(
            'omd %s nagios' % (action), shell=True, stdout=subprocess.PIPE)
        # process = subprocess.Popen('/omd/sites/nms/bin/nagios -v
        # /omd/sites/nms/tmp/nagios/nagios.cfg', shell=True,
        # stdout=subprocess.PIPE)
        output, _ = process.communicate()
        code = process.wait()
        output_action = {
            "success": 0,
            "data": output
        }
        # return JSONEncoder().encode(output_action)
        return 0
    except Exception, e:
        output = {
            "success": 1,
            "exception": str(e)
        }
        # return JSONEncoder().encode(output)
        return 1
