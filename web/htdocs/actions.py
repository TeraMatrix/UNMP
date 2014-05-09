#!/usr/bin/python2.6
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2010             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from lib import *
import time
import config

def ajax_action(h):
    global html
    html = h

    try:
        action = html.var("action")
        if action == "reschedule":
            action_reschedule()
        else:
            raise MKGeneralException("Invalid action '%s'" % action)
    except Exception, e:
        html.write("['ERROR', %r]\n" % str(e))

def action_reschedule():
    if not config.may("action.reschedule"):
        raise MKGeneralException("You are not allowed to reschedule checks.")

    site = html.var("site")
    host = html.var("host", "")
    if not host:
        raise MKGeneralException("Action reschedule: missing host name")
    service = html.var("service", "")
    if service:
        what = "service"
        spec = "%s;%s" % (host, service)
        cmd = "SVC"
        add_filter = "Filter: service_description = %s\n" % service
    else:
        what = "host"
        spec = host
        cmd = "HOST"
        add_filter = ""

    try:
        now = int(time.time())
        html.live.command("[%d] SCHEDULE_FORCED_%s_CHECK;%s;%d" % (now, cmd, spec, now), site)
        html.live.set_only_sites([site])
        row = html.live.query_row(
                "GET %ss\n"
                "WaitObject: %s %s\n"
                "WaitCondition: last_check >= %d\n"
                "WaitTimeout: %d\n"
                "WaitTrigger: check\n"
                "Columns: last_check state plugin_output\n"
                "Filter: host_name = %s\n%s"
                % (what, host, service, now, config.reschedule_timeout * 1000, host, add_filter))
        html.live.set_only_sites()
        last_check = row[0]
        if last_check < now:
            html.write("['TIMEOUT', 'Check not executed within %d seconds']\n" % (config.reschedule_timeout))

        else:
            html.write("['OK', %d, %d, %r]\n" % (row[0], row[1], row[2].encode("utf-8")))

    except Exception, e:
        html.live.set_only_sites()
        raise MKGeneralException("Cannot reschedule check: %s" % e)
