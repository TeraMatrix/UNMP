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

#!/usr/bin/python

import config


def render_wato_files():
    if not config.may("use_wato"):
        html.write(
            "You are not allowed to use Check_MK's web configuration GUI.")
    elif len(config.config_files) == 0:
        html.write("No configuration files are defined.<br>"
                   "Please set the variable <tt>config_files</tt><br>"
                   "in <tt>multisite.mk</tt>.")

    else:
        if config.is_multisite():
            sitenames = config.sites.keys()
            sitenames.sort()
            for sitename in sitenames:
                site = config.sites[sitename]
                state = html.site_status[sitename]["state"]
                if state != "disabled":
                    html.write("<h3>%s</h3>\n" % site["alias"])
                    ajax_url = site["url_prefix"] + \
                               "check_mk/ajax_wato_files.py"
                    html.javascript(
                        "document.write(get_url_sync('%s'));" % ajax_url)
        else:
            ajax_wato_files(html)


def ajax_wato_files(h):
    global html
    html = h
    if config.may("use_wato"):
        html.write('<ul>')
        for filename, title, roles in config.config_files:
            if config.role in roles:
                bulletlink(title, "wato.py?filename=%s" % filename)
        html.write('</ul>')


# sidebar_snapins["wato"] = {
#    "title" : "Check_MK Web Administration Tool",
#    "description" : "WATO - the Web Administration Tool of Check_MK - manage hosts to be monitored without access to the command line",
#    "author" : "Mathias Kettner",
#    "render" : render_wato_files,
#    "allowed" : [ "admin", "user" ],
#}
