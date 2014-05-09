#!/usr/bin/python2.6
'''
@author: Mahipal Choudhary
@since: 02-Nov-2011
@version: 0.1
@note: All controller functions needed with daemons management
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''
import daemons
import daemons_bll
import sys
import os
import time
import atexit
from signal import SIGTERM
# dict_port={1:"-",2:"6790",3:"-",4:"-"}
# dict_id={1:"unmp-alarm",2:"unmp-ds",3:"unmp-nbi-supplier",4:"unmp-local"}
# dict_name={1:"Alarm Parser",2:"Auto Discovery server",3: "NBI Service",4:"UNMP System Monitor"}
# dict_pid={1:"/omd/daemon/tmp/unmp-trap.pid",2:"/omd/daemon/tmp/unmp-ds.pid",3:"/omd/daemon/tmp/unmp-nbi-supplier.pid",4:"/omd/daemon/tmp/unmp-local.pid"}
# dict_details={1:"UNMP Core Process to Capture & Log Traps, Alarms &
# Alerts.",2:"UNMP Device Discovery Server.",3:"UNMP Core Process for Trap
# Forwarding",4:"UNMP Core Process for UNMP System Monitor"}

dict_port = {1: "-", 2: "6790", 3: "-", 4: "-"}
dict_id = {1: "unmp-alarm", 2: "unmp-ds", 3: "unmp-local", 4: "nagios"}
dict_name = {1: "Alarm Parser", 2: "Auto Discovery server", 3:
    "UNMP System Monitor", 4: "Nagios"}
dict_pid = {1: "/omd/daemon/tmp/unmp-trap.pid", 2: "/omd/daemon/tmp/unmp-ds.pid", 3:
    "/omd/daemon/tmp/unmp-local.pid", 4: "nagios"}
dict_details = {1: "UNMP Core Process to Capture & Log Traps, Alarms & Alerts.", 2:
    "UNMP Device Discovery Server.", 3: "UNMP Core Process for UNMP System Monitor", 4: "Nagios core process"}


# dict_pidfile={"unmp-alarm":"/omd/daemon/tmp/unmp-trap.pid","unmp-
# ds":"/omd/daemon/tmp/unmp-ds.pid","unmp-nbi-supplier":"/omd/daemon/tmp
# /unmp-nbi-supplier.pid","unmp-local":"/omd/daemon/tmp/unmp-local.pid"}

dict_pidfile = {
    "unmp-alarm": "/omd/daemon/tmp/unmp-trap.pid", "unmp-ds": "/omd/daemon/tmp/unmp-ds.pid",
    "unmp-local": "/omd/daemon/tmp/unmp-local.pid", "nagios": "nagios"}


def mahipal_daemons(h):
    global html
    html = h
    html.new_header("Daemons Management", "daemons_controller.py", "",
        [], ["js/unmp/main/daemon.js"])
    html.write(
        daemons.index(dict_id, dict_name, dict_pid, dict_port, dict_details))
    html.new_footer()


def load_daemons(h):
    global html
    html = h
    s = daemons_bll.load()
    html.write(str(s))


def doAction_daemon(h):
    global html
    html = h
    daemonName = html.var("daemonName")
    action = html.var("action")
    username = html.req.session["username"]
    s = daemons_bll.doAction(daemonName, action, username)
    html.write(str(s))


def get_status_daemon(h):
    global html
    html = h
    pidfile = html.var("pidfile")
    pid = dict_pidfile[pidfile]
    html.write(str(daemons_bll.get_status(pid)))


# def page_tip_daemons(h):
#     global html
#     html = h
#     html.write(daemons.page_tip_daemons())
