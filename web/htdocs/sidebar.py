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

import config
import defaults
import livestatus
import htmllib
import views
import pprint
import os
import copy
from lib import *
from unmp_config import SystemConfig

dashboard_refresh_time = SystemConfig.get_default_dashboard_refresh_time()
company = SystemConfig.get_company_details()
about_us = SystemConfig.get_system_about_us()

sidebar_snapins = {}

# Constants to be used in snapins
snapin_width = 230

# Load all snapins
snapins_dir = defaults.web_dir + "/plugins/sidebar"
for fn in os.listdir(snapins_dir):
    if fn.endswith(".py"):
        execfile(snapins_dir + "/" + fn)
if defaults.omd_root:
    local_snapins_dir = defaults.omd_root + \
                        "/local/share/check_mk/web/plugins/sidebar"
    if os.path.exists(local_snapins_dir):
        for fn in os.listdir(local_snapins_dir):
            if fn.endswith(".py"):
                execfile(local_snapins_dir + "/" + fn)

# Declare permissions: each snapin creates one permission
config.declare_permission_section("sidesnap", "Sidebar snapins")
for name, snapin in sidebar_snapins.items():
    config.declare_permission("sidesnap.%s" % name,
                              snapin["title"],
                              "",
                              snapin["allowed"])

# Helper functions to be used by snapins


def link(text, target):
    # Convert relative links into absolute links. We have three kinds
    # of possible links and we change only [3]
    # [1] protocol://hostname/url/link.py
    # [2] /absolute/link.py
    # [3] relative.py
    if not (":" in target[:10]) and target[0] != '/':
        target = defaults.url_prefix + "check_mk/" + target
    return "<a target=\"main\" class=link href=\"%s\">%s</a>" % (target, htmllib.attrencode(text))


def simplelink(text, target):
    html.write(link(text, target) + "<br>\n")


def footnotelinks(links):
    html.write("<div class=footnotelink>")
    for text, target in links:
        html.write(link(text, target))
    html.write("</div>\n")


def iconbutton(what, url, target="side", handler="", name=""):
    if target == "side":
        onclick = "onclick=\"get_url('%s', %s, '%s')\"" % \
                  (url, handler, name)
        href = "#"
        tg = ""
    else:
        onclick = ""
        href = "%scheck_mk/%s" % (defaults.url_prefix, url)
        tg = "target=%s" % target
    html.write(
        "<a href=\"%s\" %s %s><img class=iconbutton onmouseover=\"hilite_icon(this, 1)\" onmouseout=\"hilite_icon(this, 0)\" align=absmiddle src=\"%scheck_mk/images/button_%s_lo.png\"></a>\n " % (
        href, onclick, tg, defaults.url_prefix, what))


def nagioscgilink(text, target):
    html.write("<li class=sidebar><a target=\"main\" class=link href=\"%snagios/cgi-bin/%s\">%s</a></li>" %
               (defaults.url_prefix, target, htmllib.attrencode(text)))


def heading(text):
    html.write("<h3>%s</h3>\n" % htmllib.attrencode(text))


def load_user_config():
    path = config.user_confdir + "/sidebar.mk"
    try:
        user_config = eval(file(path).read())
    except:
        user_config = config.sidebar

    # Remove entries the user is not allowed for or which have state "off"
    # (from legacy version)
    return [entry for entry in user_config if entry[1] != "off" and config.may("sidesnap." + entry[0])]


def save_user_config(user_config):
    if True:  # config.may("configure_sidebar"):
        config.save_user_file("sidebar", user_config)


def sidebar_head():
    html.write("<div id=\"page_header\">\
			<div id=\"logo\"><a href=\"%s\" target=\"main\">%s</a></div>\
		</div><div id=\"header2\"></div>" % (company["website"], company["name"]))


def sidebar_foot():
    html.write('<div id="side_footer">')
    if True:  # config.may("configure_sidebar"):
        html.write('<div class=button>\n')
        html.write('<a target="main" href="sidebar_add_snapin.py"')
        html.write('>Add snapin</a></div>')
    html.write("<div class=copyright>%s</div>\n" % (about_us["version"]))
    html.write('</div>')

# Standalone sidebar


def page_side(h):
    if not config.may("see_sidebar"):
        return

    global html
    html = h
    html.write("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
<title>Check_MK Sidebar</title>
<link href="check_mk.css" type="text/css" rel="stylesheet">
<link href="css/example.css" type="text/css" rel="stylesheet">""")
    if config.custom_style_sheet:
        html.write('<link rel="stylesheet" type="text/css" href="%s">' %
                   config.custom_style_sheet)

    html.write("""
<script type="text/javascript" src="js/check_mk.js"></script>
<script type="text/javascript" src="js/sidebar.js"></script>
</head>
<body class="side" onload="initScrollPos()" onunload="storeScrollPos()">
<div id="check_mk_sidebar">""")

    views.html = h
    views.load_views()
    sidebar_head()
    user_config = load_user_config()
    refresh_snapins = []

    html.write('<div id="side_content">')
    for name, state in user_config:
        if not name in sidebar_snapins or not config.may("sidesnap." + name):
            continue
        if state in ["open", "closed"]:
            refresh_url = render_snapin(name, state)
            refresh_time = sidebar_snapins.get(name).get("refresh", 0)
            if refresh_time > 0:
                refresh_snapins.append([name, refresh_time, refresh_url])
    html.write('</div>')
    sidebar_foot()
    html.write('</div>')

    html.write("<script language=\"javascript\">\n")
    html.write("registerEdgeListeners();\n")
    html.write("setSidebarHeight();\n")
    html.write("refresh_snapins = %r;\n" % refresh_snapins)
    html.write("sidebar_scheduler();\n")
    html.write("window.onresize = function() { setSidebarHeight(); }\n")
    html.write("</script>\n")

    # html.write("</div>\n")
    html.write("</body>\n</html>")


def render_snapin(name, state):
    snapin = sidebar_snapins.get(name)
    styles = snapin.get("styles")
    if styles:
        html.write("<style>\n%s\n</style>\n" % styles)

    html.write("<div id=\"snapin_container_%s\" class=snapin>\n" % name)
    if state == "closed":
        style = ' style="display:none"'
        headclass = "closed"
    else:
        style = ""
        headclass = "open"
    url = "sidebar_openclose.py?name=%s&state=" % name

    html.write('<div class="head %s" ' % headclass)
    if True:  # config.may("configure_sidebar"):
        html.write("onmouseover=\"document.body.style.cursor='move';\" onmouseout=\"document.body.style.cursor='';\""
                   " onmousedown=\"snapinStartDrag(event)\" onmouseup=\"snapinStopDrag(event)\">")
    else:
        html.write(">")
    if True:  # config.may("configure_sidebar"):
        html.write('<div class="closesnapin">')
        iconbutton("closesnapin", "sidebar_openclose.py?name=%s&state=off" %
                                  name, "side", "removeSnapin", 'snapin_' + name)
        html.write('</div>')
        pass
    html.write(
        "<b class=heading onclick=\"toggle_sidebar_snapin(this,'%s')\" onmouseover=\"this.style.cursor='pointer'\" "
        "onmouseout=\"this.style.cursor='auto'\">%s</b>" % (url, snapin["title"]))
    html.write("</div>")

    html.write("<div id=\"snapin_%s\" class=content%s>\n" % (name, style))
    refresh_url = ''
    try:
        url = snapin["render"]()
        # Fetch the contents from an external URL. Don't render it on our own.
        if not url is None:
            refresh_url = url
            html.write('<script>get_url("%s", updateContents, "snapin_%s")</script>' % (
                refresh_url, name))
    except Exception, e:
        snapin_exception(e)
    html.write('</div><div class="foot"%s></div>\n' % style)
    html.write('</div>')
    return refresh_url


def snapin_exception(e):
    if config.debug:
        raise
    else:
        html.write("<div class=snapinexception>\n"
                   "<h2>Error</h2>\n"
                   "<p>%s</p></div>" % e)


def ajax_openclose(h):
    global html
    html = h

    config = load_user_config()
    new_config = []
    for name, usage in config:
        if html.var("name") == name:
            usage = html.var("state")
        if usage != "off":
            new_config.append((name, usage))
    save_user_config(new_config)


def ajax_snapin(h):
    global html
    html = h
    snapname = html.var("name")
    if not config.may("sidesnap." + snapname):
        return
    snapin = sidebar_snapins.get(snapname)
    try:
        snapin["render"]()
    except Exception, e:
        snapin_exception(e)


def move_snapin(h):
    if not True:  # config.may("configure_sidebar"):
        return

    global html
    html = h
    snapname_to_move = html.var("name")
    beforename = html.var("before")

    snapin_config = load_user_config()

    # Get current state of snaping being moved (open, closed)
    snap_to_move = None
    for name, state in snapin_config:
        if name == snapname_to_move:
            snap_to_move = name, state
    if not snap_to_move:
        return # snaping being moved not visible. Cannot be.

    # Build new config by removing snaping at current position
    # and add before "beforename" or as last if beforename is not set
    new_config = []
    for name, state in snapin_config:
        if name == snapname_to_move:
            continue  # remove at this position
        elif name == beforename:
            new_config.append(snap_to_move)
        new_config.append((name, state))
    if not beforename:  # insert as last
        new_config.append(snap_to_move)
    save_user_config(new_config)


def page_add_snapin(h):
    if not True:  # config.may("configure_sidebar"):
        raise MKGeneralException("You are not allowed to change the sidebar.")

    global html
    html = h
    html.new_header("Available snapins")
    used_snapins = [name for (name, state) in load_user_config()]

    addname = html.var("name")
    if addname in sidebar_snapins and addname not in used_snapins and html.check_transaction():
        user_config = load_user_config() + [(addname, "open")]
        save_user_config(user_config)
        used_snapins = [name for (name, state) in load_user_config()]
        html.reload_sidebar()

    names = sidebar_snapins.keys()
    names.sort()

    for name in names:
        if name in used_snapins:
            continue
        snapin = sidebar_snapins[name]
        title = snapin["title"]
        description = snapin.get("description", "")
        image_path = snapin.get("image", "images/new/add.png")
        author = snapin.get("author")
        transid = html.current_transid(html.req.session["username"])
        url = 'sidebar_add_snapin.py?name=%s&_transid=%d&pos=top' % (
            name, transid)

        html.write('<div class="shortcut-icon-div"\
                onclick="window.location.href=\'%s\';">\
                <div><img alt="" src="%s"/></div>\
                <div style="width: 60%%;"><span class="head">%s</span><span class=\'sub-head\'>%s</span></div>\
                </div>' % (url, image_path, title, description))
        # if author:
        #    html.write("<br><i>Author: %s</i>" % author)
    html.new_footer()
