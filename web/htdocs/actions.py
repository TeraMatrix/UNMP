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

import time

import config
from lib import *


def ajax_action(h):
    global html
    html = h

    try:
        action = html.var("action")
        if action == "reschedule":
            view_type = html.var("view_type", "")
            if view_type == "UNMP":
                action_reschedule_modified()
            else:
                action_reschedule()
        else:
            raise MKGeneralException("Invalid action '%s'" % action)
    except Exception, e:
        html.write("['ERROR', %r]\n" % str(e))


def get_time_tick(timetick):
    import datetime

    last_check = ""
    if datetime.datetime.now() > datetime.datetime.fromtimestamp(timetick):
        delta = datetime.datetime.now(
        ) - datetime.datetime.fromtimestamp(timetick)
    else:
        delta = datetime.datetime.fromtimestamp(
            timetick) - datetime.datetime.now()
    second = delta.seconds
    if second < 60:
        last_check = str(second) + " sec"
    elif second < 3600:
        minute = int(second / 60)
        second = second % 60
        last_check = str(minute) + " min," + str(second) + " sec"
    else:
        hour = int(second / 3600)
        minute = int((second - hour * 3600) / 60)
        last_check = str(hour) + " hour," + str(minute) + " min"
    return last_check


def paint_age(timestamp, has_been_checked, bold_if_younger_than):
    """
    @return: this function return the host host status age.
    @rtype: this function return type string.
    @requires: this function take three argument 1. timestamp(total up tiem) , 2. this process checked or not(boolean value) , 3. total up time is grether than 10 min or not. .
    @author: Rajendra Sharma
    @since: 20 sept 2011
    @version: 0.1
    @date: 18 sept 2011
    @note: this function return the host host status age.
    @organization: Code Scape Consultants Pvt. Ltd.
    @copyright: 2011 Code Scape Consultants Pvt. Ltd.
    """
    if not has_been_checked:
        return "age", "-"
    import time

    age = time.time() - timestamp
    if age >= 48 * 3600 or age < -48 * 3600:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    # Time delta less than two days => make relative time
    if age < 0:
        age = -age
        prefix = "in "
    else:
        prefix = ""
    if age < bold_if_younger_than:
        age_class = "age recent"
    else:
        age_class = "age"
    return prefix + html.age_text(age)


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
        html.live.command("[%d] SCHEDULE_FORCED_%s_CHECK;%s;%d" % (
            now, cmd, spec, now), site)
        html.live.set_only_sites([site])
        row = html.live.query_row(
            "GET %ss\n"
            "WaitObject: %s %s\n"
            "WaitCondition: last_check >= %d\n"
            "WaitTimeout: %d\n"
            "WaitTrigger: check\n"
            "Columns: last_check state plugin_output service_last_state_change service_last_check service_next_check service_execution_time service_plugin_output service_long_plugin_output state \n"  # "Columns: last_check state plugin_output \n"#
            "Filter: host_name = %s\n%s"
            % (what, host, service, now, config.reschedule_timeout * 1000, host, add_filter))
        html.live.set_only_sites()
        # str('0' if host_age==0 else paint_age(host_age, checked == 1, 60 *
        # 10))
        last_check = row[0]
        if last_check < now:
            html.write("['TIMEOUT', 'Check not executed within %d seconds %s %s']\n" % (
                config.reschedule_timeout), now, last_check)

        else:
            output = row[7]
            all_output = row[8]
            all_device_detail = ' (' + str(all_output).replace('\\n', '') + ')'
            html.write("['OK', %d, %d, %r]\n" % (row[0], row[
                1], row[2].encode("utf-8")))
            # f=open("/home/cscape/Desktop/acb.txt","a")
            # f.write(str("['OK', %d, %d, %r,'%s','%s','%s','%s','%s','%s']" % (row[0], row[1], row[2].encode("utf-8"),str(row[9]), str(str('0' if row[3]==0 else paint_age(row[3], True, 60 * 10))), str(get_time_tick(row[4])), str(get_time_tick(row[5])), str(row[6]),output+str('' if all_device_detail.strip()=='()' else all_device_detail) )))
            # f.close()
            # html.write("['OK', %d, %d, %r,'%s','%s','%s','%s','%s','%s']" %
            # (row[0], row[1], row[2].encode("utf-8"),str(row[9]), str(str('0'
            # if row[3]==0 else paint_age(row[3], True, 60 * 10))),
            # str(get_time_tick(row[4])), str(get_time_tick(row[5])),
            # str(row[6]),output+str('' if all_device_detail.strip()=='()' else
            # all_device_detail) ))

    except Exception, e:
        html.live.set_only_sites()
        raise MKGeneralException("Cannot reschedule check: %s" % e)


def action_reschedule_modified():
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
        time1 = now
        html.live.command("[%d] SCHEDULE_FORCED_%s_CHECK;%s;%d" % (
            now, cmd, spec, now), site)
        html.live.set_only_sites([site])
        row = html.live.query_row(
            "GET %ss\n"
            "WaitObject: %s %s\n"
            "WaitCondition: last_check >= %d\n"
            "WaitTimeout: %d\n"
            "WaitTrigger: check\n"
            "Columns: last_check state plugin_output service_last_state_change service_last_check service_next_check service_execution_time service_plugin_output service_long_plugin_output state \n"  # "Columns: last_check state plugin_output \n"#
            "Filter: host_name = %s\n%s"
            % (what, host, service, now, config.reschedule_timeout * 1000, host, add_filter))
        html.live.set_only_sites()
        # str('0' if host_age==0 else paint_age(host_age, checked == 1, 60 *
        # 10))
        last_check = row[0]
        if last_check < now:  # and (time.time()-time1)>100:
            html.write("['TIMEOUT', 'Check not executed within %d seconds',%s,%s]\n" %
                       (config.reschedule_timeout, str(now), str(time.time() - time1)))

        else:
            output = row[7]
            all_output = row[8]
            all_device_detail = ' (' + str(all_output).replace('\\n', '') + ')'
            # html.write("['OK', %d, %d, %r]\n" % (row[0], row[1], row[2].encode("utf-8")))
            # f=open("/home/cscape/Desktop/acb.txt","a")
            # f.write(str("['OK', %d, %d, %r,'%s','%s','%s','%s','%s','%s']" % (row[0], row[1], row[2].encode("utf-8"),str(row[9]), str(str('0' if row[3]==0 else paint_age(row[3], True, 60 * 10))), str(get_time_tick(row[4])), str(get_time_tick(row[5])), str(row[6]),output+str('' if all_device_detail.strip()=='()' else all_device_detail) )))
            # f.close()
            html.write("['OK', %d, %d, %r,'%s','%s','%s','%s','%s','%s']" % (row[0], row[1], row[2].encode(
                "utf-8"), str(row[9]), str(str('0' if row[3] == 0 else paint_age(row[3], True, 60 * 10))),
                                                                             str(get_time_tick(row[4])),
                                                                             str(get_time_tick(row[5])), str(row[6]),
                                                                             output + str(
                                                                                 '' if all_device_detail.strip() == '()' else all_device_detail)))

    except Exception, e:
        html.live.set_only_sites()
        raise MKGeneralException("Cannot reschedule check: %s" % e)
