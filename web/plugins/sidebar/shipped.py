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

import views, time, defaults, MySQLdb,xml.dom.minidom
from lib import *

# Python 2.3 does not have 'set' in normal namespace.
# But it can be imported from 'sets'
try:
    set()
except NameError:
    from sets import Set as set

# -----------------------------------------------------------------------
#      _       _           _       _     _             _   _
#     / \   __| |_ __ ___ (_)_ __ (_)___| |_ _ __ __ _| |_(_) ___  _ __
#    / _ \ / _` | '_ ` _ \| | '_ \| / __| __| '__/ _` | __| |/ _ \| '_ \
#   / ___ \ (_| | | | | | | | | | | \__ \ |_| | | (_| | |_| | (_) | | | |
#  /_/   \_\__,_|_| |_| |_|_|_| |_|_|___/\__|_|  \__,_|\__|_|\___/|_| |_|
#
# -----------------------------------------------------------------------
def render_admin():
    html.write('<ul>')
    bulletlink("View permissions", "view_permissions.py")
    if config.may("edit_permissions"):
        bulletlink("Edit permissions", "edit_permissions.py")
    if config.may("manage_user"):
        bulletlink("Manage User", "manage_user.py")
    html.write('</ul>')

#sidebar_snapins["admin"] = {
#    "title" : "Administration",
#    "description" : "Links to administrations functions, e.g. configuration of permissions",
#    "author" : "Mathias Kettner",
#    "render" : render_admin,
#    "allowed" : [ "admin" ],
#}


# --------------------------------------------------------------
#   __     ___
#   \ \   / (_) _____      _____
#    \ \ / /| |/ _ \ \ /\ / / __|
#     \ V / | |  __/\ V  V /\__ \
#      \_/  |_|\___| \_/\_/ |___/
#
# --------------------------------------------------------------
visible_views = [ "allhosts", "searchsvc" ]

def render_views():
    def render_topic(topic, s):
        first = True
        for t, title, name in s:
            if config.visible_views and name not in config.visible_views:
                continue
            if config.hidden_views and name in config.hidden_views:
                continue
            if t == topic:
                if first:
                    html.write("<h3>%s</h3>\n" % topic)
                    first = False
                    html.write("<ul>")
                bulletlink(title, "view.py?view_name=%s" % name)
        if not first: # at least one item rendered
            html.write("</ul>")

    s = [ (view.get("topic", "Other"), view["title"], name) for name, view in html.available_views.items() if not view["hidden"] ]
    s.sort()

    # Enforce a certain order on the topics
    known_topics = [ "Hosts", "Hostgroups", "Services", "Servicegroups", "Problems", "Addons" ]
    for topic in known_topics:
        render_topic(topic, s)

    rest = list(set([ t for (t, _t, _v) in s if t not in known_topics ]))
    rest.sort()
    for topic in rest:
        render_topic(topic, s)


    links = []
    if config.may("edit_views"):
        if config.debug:
            links.append(("EXPORT", "export_views.py"))
        links.append(("EDIT", "edit_views.py"))
        footnotelinks(links)

def render_new_view():
    bulletlink("Host and Service Events","manage_events.py")
    bulletlink("Search Global Logfile","manage_logs.py")

sidebar_snapins["views"] = {
    "title" : "Logs",
    "description" : "Links to all logs.",
    "render" : render_new_view,
    "allowed" : [ "user", "admin", "guest" ],
}

# --------------------------------------------------------------
#    ____                  _                     __
#   / ___|  ___ _ ____   _(_) ___ ___           / /
#   \___ \ / _ \ '__\ \ / / |/ __/ _ \_____    / /
#    ___) |  __/ |   \ V /| | (_|  __/_____|  / /
#   |____/ \___|_|    \_/ |_|\___\___|       /_/
#
#   _   _           _
#  | | | | ___  ___| |_ __ _ _ __ ___  _   _ _ __  ___
#  | |_| |/ _ \/ __| __/ _` | '__/ _ \| | | | '_ \/ __|
#  |  _  | (_) \__ \ || (_| | | | (_) | |_| | |_) \__ \
#  |_| |_|\___/|___/\__\__, |_|  \___/ \__,_| .__/|___/
#                      |___/                |_|
# --------------------------------------------------------------
def render_groups(what):
    data = html.live.query("GET %sgroups\nColumns: name alias\n" % what)
    name_to_alias = dict(data)
    groups = [(name_to_alias[name].lower(), name_to_alias[name], name) for name in name_to_alias.keys()]
    groups.sort() # sort by Alias in lowercase
    target = views.get_context_link(html.req.user, "%sgroup" % what)
    if target:
        html.write('<ul>')
        for alias_lower, alias, name in groups:
            bulletlink(alias, target + "&%sgroup=%s" % (what, htmllib.urlencode(name)))
        html.write('</ul>')

#sidebar_snapins["hostgroups"] = {
#    "title" : "Hostgroups",
#    "description" : "Directs links to all host groups",
#    "author" : "Mathias Kettner",
#    "render" : lambda: render_groups("host"),
#    "allowed" : [ "user", "admin", "guest" ]
#}
#sidebar_snapins["servicegroups"] = {
#    "title" : "Servicegroups",
#    "description" : "Direct links to all service groups",
#    "author" : "Mathias Kettner",
#    "render" : lambda: render_groups("service"),
#    "allowed" : [ "user", "admin", "guest" ]
#}

# --------------------------------------------------------------
#    _   _           _
#   | | | | ___  ___| |_ ___
#   | |_| |/ _ \/ __| __/ __|
#   |  _  | (_) \__ \ |_\__ \
#   |_| |_|\___/|___/\__|___/
#
# --------------------------------------------------------------
def render_hosts(mode):
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: name state worst_service_state\n"
    view = "host"

    if mode == "summary":
        query += "Filter: custom_variable_names >= _REALNAME\n"
    else:
        query += "Filter: custom_variable_names < _REALNAME\n"

    if mode == "problems":
        query += "Filter: state > 0\nFilter: worst_service_state > 0\nOr: 2\n"
        view = "problemsofhost"

    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()

    longestname = 0
    for site, host, state, worstsvc in hosts:
        longestname = max(longestname, len(host))
    if longestname > 15:
        num_columns = 1
    else:
        num_columns = 2

    views.html = html
    views.load_views()
    target = views.get_context_link(html.req.user, view)
    html.write("<table class=allhosts>\n")
    col = 1
    # Open database connection
    db = MySQLdb.connect("localhost","root","root","nms" )

    for site, host, state, worstsvc in hosts:

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = "SELECT COUNT(*) from nms_devices\
               WHERE hostname = '%s' AND created_by = '%s' AND is_deleted = 0" % (host,config.user)
        cursor.execute(sql)
        count_host = cursor.fetchone()[0]
        cursor.close()
        if count_host > 0:
             if col == 1:
                 html.write("<tr>")
             html.write("<td>")

             if state > 0 or worstsvc == 2:
                 statecolor = 2
             elif worstsvc == 1:
                 statecolor = 1
             elif worstsvc == 3:
                 statecolor = 3
             else:
                 statecolor = 0
             html.write('<div class="statebullet state%d">&nbsp;</div> ' % statecolor)
             html.write(link(host, target + ("&host=%s&site=%s" % (htmllib.urlencode(host), htmllib.urlencode(site)))))
             html.write("</td>")
             if col == num_columns:
                 html.write("</tr>\n")
                 col = 1
             else:
                 col += 1
    db.close()
    if col < num_columns:
        html.write("</tr>\n")
    html.write("</table>\n")

snapin_allhosts_styles = """
  .snapin table.allhosts { width: 100%; }
  .snapin table.allhosts td { width: 50%; padding: 0px 0px; }
"""

#sidebar_snapins["hosts"] = {
#    "title" : "All hosts",
#    "description" : "A summary state of each host with a link to the view showing its services",
#    "author" : "Mathias Kettner",
#    "render" : lambda: render_hosts("hosts"),
#    "allowed" : [ "user", "admin", "guest" ],
#    "refresh" : 60,
#    "styles" : snapin_allhosts_styles,
#}

#sidebar_snapins["summary_hosts"] = {
#    "title" : "Summary hosts",
#    "description" : "A summary state of all summary hosts (summary hosts hold aggregated service states and are a feature of Check_MK)",
#    "author" : "Mathias Kettner",
#    "render" : lambda: render_hosts("summary"),
#    "allowed" : [ "user", "admin", "guest" ],
#    "refresh" : 60,
#    "styles" : snapin_allhosts_styles,
#}

#sidebar_snapins["problem_hosts"] = {
#    "title" : "Problem hosts",
#    "description" : "A summary state of all hosts that have problem, with links to problems of those hosts",
#    "author" : "Mathias Kettner",
#    "render" : lambda: render_hosts("problems"),
#    "allowed" : [ "user", "admin", "guest" ],
#    "refresh" : 60,
#    "styles" : snapin_allhosts_styles,
#}

# --------------------------------------------------------------
#    _____          _   _           _                             _
#   |_   _|_ _  ___| |_(_) ___ __ _| |   _____   _____ _ ____   _(_) _____      __
#     | |/ _` |/ __| __| |/ __/ _` | |  / _ \ \ / / _ \ '__\ \ / / |/ _ \ \ /\ / /
#     | | (_| | (__| |_| | (_| (_| | | | (_) \ V /  __/ |   \ V /| |  __/\ V  V /
#     |_|\__,_|\___|\__|_|\___\__,_|_|  \___/ \_/ \___|_|    \_/ |_|\___| \_/\_/
#
# --------------------------------------------------------------
def render_tactical_overview():
    host_query = \
        "GET hosts\n" \
        "Stats: state >= 0\n" \
        "Stats: state > 0\n" \
        "Stats: scheduled_downtime_depth = 0\n" \
        "StatsAnd: 2\n" \
        "Stats: state > 0\n" \
        "Stats: scheduled_downtime_depth = 0\n" \
        "Stats: acknowledged = 0\n" \
        "StatsAnd: 3\n" \
        "Filter: custom_variable_names < _REALNAME\n"

    service_query = \
        "GET services\n" \
        "Stats: state >= 0\n" \
        "Stats: state > 0\n" \
        "Stats: scheduled_downtime_depth = 0\n" \
        "Stats: host_scheduled_downtime_depth = 0\n" \
        "Stats: host_state = 0\n" \
        "StatsAnd: 4\n" \
        "Stats: state > 0\n" \
        "Stats: scheduled_downtime_depth = 0\n" \
        "Stats: host_scheduled_downtime_depth = 0\n" \
        "Stats: acknowledged = 0\n" \
        "Stats: host_state = 0\n" \
        "StatsAnd: 5\n" \
        "Filter: host_custom_variable_names < _REALNAME\n"

    # ACHTUNG: Stats-Filter so anpassen, dass jeder Host gezaehlt wird.

    try:
        hstdata = html.live.query_summed_stats(host_query)
        svcdata = html.live.query_summed_stats(service_query)
    except livestatus.MKLivestatusNotFoundError:
        html.write("<center>No data from any site</center>")
        return
    html.write("<table class=\"content_center tacticaloverview\" cellspacing=2 cellpadding=0 border=0>\n")
    for title, data, view, what in [
            ("Hosts",    hstdata, 'hostproblems', 'host'),
            ("Services", svcdata, 'svcproblems',  'service'),
            ]:
        html.write("<tr><th>%s</th><th>Problems</th><th>Unhandled</th></tr>\n" % title)
        html.write("<tr>")

        html.write('<td class=total><a target="main" href="view.py?view_name=all%ss">%d</a></td>' % (what, data[0]))
        unhandled = False
        for value in data[1:]:
            if value > 0:
                href = "view.py?view_name=" + view
                if unhandled:

                    href += "&is_%s_acknowledged=0" % what
                text = link(str(value), href)
            else:
                text = str(value)
            html.write('<td class="%s">%s</td>' % (value == 0 and " " or "states prob", text))
            unhandled = True
        html.write("</tr>\n")
    html.write("</table>\n")

#sidebar_snapins["tactical_overview"] = {
#    "title" : "Tactical Overview",
#    "description" : "The total number of hosts and service with and without problems",
#    "author" : "Mathias Kettner",
#    "refresh" : 10,
#    "render" : render_tactical_overview,
#    "allowed" : [ "user", "admin", "guest" ],
#    "styles" : """
#table.tacticaloverview {
#   border-collapse: separate;
#   /**
#    * Don't use border-spacing. It is not supported by IE8 with compat mode and older IE versions.
#    * Better set cellspacing in HTML code. This works in all browsers.
#    * border-spacing: 5px 2px;
#    */
#   width: %dpx;
#   margin-top: 0;
#}
#table.tacticaloverview th { font-size: 7pt; text-align: left; font-weight: normal; padding: 0; padding-top: 2px; }
#table.tacticaloverview td { text-align: right; border: 1px solid #444; padding: 0px; }
#table.tacticaloverview td a { display: block; margin-right: 2px; }
#""" % snapin_width
#}
# table.tacticaloverview td.prob { font-weight: bold; }

# --------------------------------------------------------------
#    ____            __
#   |  _ \ ___ _ __ / _| ___  _ __ _ __ ___   __ _ _ __   ___ ___
#   | |_) / _ \ '__| |_ / _ \| '__| '_ ` _ \ / _` | '_ \ / __/ _ \
#   |  __/  __/ |  |  _| (_) | |  | | | | | | (_| | | | | (_|  __/
#   |_|   \___|_|  |_|  \___/|_|  |_| |_| |_|\__,_|_| |_|\___\___|
#
# --------------------------------------------------------------
def render_performance():
    data = html.live.query("GET status\nColumns: service_checks_rate host_checks_rate external_commands_rate connections_rate forks_rate log_messages_rate cached_log_messages\n")
    html.write("<table class=\"content_center performance\">\n")
    for what, col, format in \
        [("Service checks", 0, "%.2f/s"),
        ("Host checks", 1, "%.2f/s"),
        ("External commands", 2, "%.2f/s"),
        ("Livestatus-connections", 3, "%.2f/s"),
        ("Process creations", 4, "%.2f/s"),
        ("New log messages", 5, "%.2f/s"),
        ("Cached log messages", 6, "%d")]:
       html.write(("<tr><td class=left>%s:</td><td class=right><strong>" + format + "</strong></td></tr>\n") % (what, sum([row[col] for row in data])))
    data = html.live.query("GET status\nColumns: external_command_buffer_slots external_command_buffer_max\n")
    size = sum([row[0] for row in data])
    maxx = sum([row[1] for row in data])
    html.write("<tr><td class=left>Com. buf. max/total</td>"
               "<td class=right><strong>%d / %d</strong></td></tr>" % (maxx, size))
    html.write("</table>\n")

#sidebar_snapins["performance"] = {
#    "title" : "Server performance",
#    "description" : "Live monitor of the overall performance of all monitoring servers",
#    "author" : "Mathias Kettner",
#    "refresh" : 10,
#    "render" : render_performance,
#    "allowed" : [ "admin", ],
#    "styles" : """
#table.performance {
#    width: %dpx;
#    -moz-border-radius: 5px;
#    font-size: 8pt;
#    background-color: #589;
#    border-style: solid;
#    border-color: #444 #bbb #eee #666;
#    /* The border needs to be substracted from the width */
#    border-width: 1px;
#}
#table.performance td { padding: 0px; }
#table.Performance td.right { text-align: right; padding: 0px; }
#
#""" % (snapin_width - 2)
#}

# --------------------------------------------------------------
#    ____                           _   _
#   / ___|  ___ _ ____   _____ _ __| |_(_)_ __ ___   ___
#   \___ \ / _ \ '__\ \ / / _ \ '__| __| | '_ ` _ \ / _ \
#    ___) |  __/ |   \ V /  __/ |  | |_| | | | | | |  __/
#   |____/ \___|_|    \_/ \___|_|   \__|_|_| |_| |_|\___|
#
# --------------------------------------------------------------
def render_current_time():
    import time
    html.write("<div class=time>%s</div>" % time.strftime("%h %d - %I:%M %p"))

sidebar_snapins["time"] = {
    "title" : "Server Time",
    "description" : "Clock to display server date-time.",
    "author" : "",
    "refresh" : 30,
    "render" : render_current_time,
    "allowed" : [ "user", "admin", "guest", ],
    "styles" : """
div.time {
   text-align: center;
   font-size: 11pt;
   font-weight: bold;
   /* The border needs to be substracted from the width */
   border: 1px solid #8cc;
   -moz-border-radius: 2px;
   background-color: #588;
   color: #aff;
   width: 210px;
}
"""  #% (snapin_width - 2)
}


# ----------------------------------------------------------------
#   __  __           _                           _             _
#  |  \/  | __ _ ___| |_ ___ _ __ ___ ___  _ __ | |_ _ __ ___ | |
#  | |\/| |/ _` / __| __/ _ \ '__/ __/ _ \| '_ \| __| '__/ _ \| |
#  | |  | | (_| \__ \ ||  __/ | | (_| (_) | | | | |_| | | (_) | |
#  |_|  |_|\__,_|___/\__\___|_|  \___\___/|_| |_|\__|_|  \___/|_|
#
# ----------------------------------------------------------------
def render_master_control():
    items = [
        ( "enable_notifications",     "Notifications", ),
        ( "execute_service_checks",   "Service checks" ),
        ( "execute_host_checks",      "Host checks" ),
        ( "enable_event_handlers",    "Event handlers" ),
        ( "process_performance_data", "Performance data"),
        ]

    html.live.set_prepend_site(True)
    data = html.live.query("GET status\nColumns: %s" % " ".join([ i[0] for i in items ]))
    html.live.set_prepend_site(False)
    html.write("<table class=master_control>\n")
    for siteline in data:
        siteid = siteline[0]
        if siteid:
            sitealias = html.site_status[siteid]["site"]["alias"]
            html.write("<tr><td class=left colspan=2>")
            heading(sitealias)
            html.write("</tr>\n")
        for i, (colname, title) in enumerate(items):
            colvalue = siteline[i + 1]
            url = defaults.url_prefix + ("check_mk/switch_master_state.py?site=%s&switch=%s&state=%d" % (siteid, colname, 1 - colvalue))
            onclick = "get_url('%s', updateContents, 'snapin_master_control')" % url
            enabled = colvalue and "enabled" or "disabled"
            html.write("<tr><td class=left>%s</td><td class=%s><a onclick=\"%s\" href=\"#\">%s</a></td></tr>\n" % (title, enabled, onclick, enabled))
    html.write("</table>")

#sidebar_snapins["master_control"] = {
#    "title" : "Master control",
#    "description" : "Buttons for switching globally states such as enabling checks and notifications",
#    "render" : render_master_control,
#    "allowed" : [ "admin", ],
#    "styles" : """
#div#check_mk_sidebar table.master_control {
#    width: %dpx;
#    margin: 0px;
#    border-spacing: 0px;
#}

#div#check_mk_sidebar table.master_control td {
#    padding: 0px 0px;
#    text-align: right;
#}

#div#check_mk_sidebar table.master_control td a {
#    font-weight: bold;
#    -moz-border-radius: 4px;
#    margin: 0px;
#    padding: 0px 3px;
#    text-align: center;
#    font-size: 7pt;
#    margin-right: 0px;
#    display: block;
#    border: 1px solid black;
#}
#div#check_mk_sidebar table.master_control td.left a {
#    text-align: left;
#    font-size: 8pt;
#    font-weight: normal;
#}

#div#check_mk_sidebar table.master_control td.left {
#    text-align: 

#div#check_mk_sidebar table.master_control td.enabled a {
#    background-color: #4f6;
#    color: #000;
#    border-color: #080;
#}
#div#check_mk_sidebar table.master_control td.disabled a {
#    background-color: #f33;
#    border-color: #c00;
#    color: #fff;
#}
#""" % snapin_width
#}


def ajax_switch_masterstate(h):
    global html
    html = h
    site = html.var("site")
    column = html.var("switch")
    state = int(html.var("state"))
    commands = {
        ( "enable_notifications",     1) : "ENABLE_NOTIFICATIONS",
        ( "enable_notifications",     0) : "DISABLE_NOTIFICATIONS",
        ( "execute_service_checks",   1) : "START_EXECUTING_SVC_CHECKS",
        ( "execute_service_checks",   0) : "STOP_EXECUTING_SVC_CHECKS",
        ( "execute_host_checks",      1) : "START_EXECUTING_HOST_CHECKS",
        ( "execute_host_checks",      0) : "STOP_EXECUTING_HOST_CHECKS",
        ( "process_performance_data", 1) : "ENABLE_PERFORMANCE_DATA",
        ( "process_performance_data", 0) : "DISABLE_PERFORMANCE_DATA",
        ( "enable_event_handlers",    1) : "ENABLE_EVENT_HANDLERS",
        ( "enable_event_handlers",    0) : "DISABLE_EVENT_HANDLERS",
    }

    command = commands.get((column, state))
    if command:
        html.live.command("[%d] %s" % (int(time.time()), command), site)
        html.live.set_only_sites([site])
        html.live.query("GET status\nWaitTrigger: program\nWaitTimeout: 10000\nWaitCondition: %s = %d\nColumns: %s\n" % \
               (column, state, column))
        html.live.set_only_sites()
        render_master_control()
    else:
        html.write("Command %s/%d not found" % (column, state))

# ---------------------------------------------------------
#   ____              _                         _
#  | __ )  ___   ___ | | ___ __ ___   __ _ _ __| | _____
#  |  _ \ / _ \ / _ \| |/ / '_ ` _ \ / _` | '__| |/ / __|
#  | |_) | (_) | (_) |   <| | | | | | (_| | |  |   <\__ \
#  |____/ \___/ \___/|_|\_\_| |_| |_|\__,_|_|  |_|\_\___/
#
# ---------------------------------------------------------
def load_bookmarks():
    path = config.user_confdir + "/bookmarks.mk"
    try:
        return eval(file(path).read())
    except:
        return []

def save_bookmarks(bookmarks):
    config.save_user_file("bookmarks", bookmarks)

def render_bookmarks():
    bookmarks = load_bookmarks()
    n = 0
    for title, href in bookmarks:
        html.write("<div id=\"bookmark_%d\">" % n)
        iconbutton("delete", "del_bookmark.py?num=%d" % n, "side", "updateContents", 'snapin_bookmarks')
        iconbutton("edit", "edit_bookmark.py?num=%d" % n, "main")
        html.write(link(title, href))
        html.write("</div>")
        n += 1

    html.write("<div class=footnotelink><a href=\"#\" onclick=\"addBookmark()\">Add Bookmark</a></div>\n")

def page_edit_bookmark(h):
    global html
    html = h
    html.header("Edit Bookmark")
    n = int(html.var("num"))
    bookmarks = load_bookmarks()
    if n >= len(bookmarks):
        raise MKGeneralException("Unknown bookmark id: %d. This is probably a problem with reload or browser history. Please try again." % n)

    if html.var("save") and html.check_transaction():
        title = html.var("title")
        url = html.var("url")
        bookmarks[n] = (title, url)
        save_bookmarks(bookmarks)
        html.reload_sidebar()

    html.begin_form("edit_bookmark")
    if html.var("save"):
        title = html.var("title")
        url = html.var("url")
        bookmarks[n] = (title, url)
        save_bookmarks(bookmarks)
        html.reload_sidebar()
    else:
        title, url = bookmarks[n]
        html.set_var("title", title)
        html.set_var("url", url)

    html.write("<table class=edit_bookmarks>")
    html.write("<tr><td>Title:</td><td>")
    html.text_input("title", size = 50)
    html.write("</td></tr><tr><td>URL:</td><td>")
    html.text_input("url", size = 50)
    html.write("</td></tr><tr><td></td><td>")
    html.button("save", "Save")
    html.write("</td></tr></table>\n")
    html.hidden_field("num", str(n))
    html.end_form()

    html.footer()

def ajax_del_bookmark(h):
    global html
    html = h
    num = int(html.var("num"))
    bookmarks = load_bookmarks()
    del bookmarks[num]
    save_bookmarks(bookmarks)
    render_bookmarks()

def ajax_add_bookmark(h):
    global html
    html = h
    title = html.var("title")
    href = html.var("href")
    if title and href:
        bookmarks = load_bookmarks()
        bookmarks.append((title, href))
        save_bookmarks(bookmarks)
    render_bookmarks()



# ------------------------------------------------------------
#   ____          _                    _     _       _
#  / ___|   _ ___| |_ ___  _ __ ___   | |   (_)_ __ | | _____
# | |  | | | / __| __/ _ \| '_ ` _ \  | |   | | '_ \| |/ / __|
# | |__| |_| \__ \ || (_) | | | | | | | |___| | | | |   <\__ \
#  \____\__,_|___/\__\___/|_| |_| |_| |_____|_|_| |_|_|\_\___/
#
# ------------------------------------------------------------

def load_customlink_states():
    return config.load_user_file("customlinks", {})

def save_customlink_states(states):
    config.save_user_file("customlinks", states)

def ajax_customlink_openclose(h):
    global html
    html = h

    states = load_customlink_states()
    states[html.var("name")] = html.var("state")
    save_customlink_states(states)

def render_custom_links():
    links = config.custom_links.get(config.role)
    if not links:
        html.write("Please edit <tt>%s</tt> in order to configure which links are shown in this snapin.\n" %
                  (defaults.default_config_dir + "/multisite.mk"))
        return

    def render_list(ids, links):
        states = load_customlink_states()
        n = 0
        for entry in links:
            n += 1
            try:
                if type(entry[1]) == type(True):
                    idss = ids + [str(n)]
                    if states.get(''.join(idss), entry[1] and 'on' or 'off') == 'on': # open
                        display = ""
                        img = "link_folder_open.gif"
                    else:
                        display = "display: none; "
                        img = "link_folder.gif"
                    html.write('<h3 onclick="toggle_folder(this, \'%s\');" ' % ''.join(idss))
                    html.write('onmouseover="this.style.cursor=\'pointer\';" ')
                    html.write('onmouseout="this.style.cursor=\'auto\';">')
                    html.write('<img src="images/%s" align="center" />' % img)
                    html.write("%s</h3>\n" % entry[0])
                    html.write('<div style="%s" class=sublist>' % display)
                    render_list(idss, entry[2])
                    html.write('</div>\n')
                elif type(entry[1]) == str:
                    if len(entry) > 2:
                        html.write('<img src="images/%s">' % entry[2])
                    else:
                        html.write('<img src="images/link_link.gif">')
                    simplelink(entry[0], entry[1])
                else:
                    html.write("Second part of tuple must be list or string, not %s\n" % str(entry[1]))
            except Exception, e:
                html.write("invalid entry %s: %s<br>\n" % (entry, e))

    render_list([], links)

####################################################################################################################
#   Created By: Yogesh Kumar (CSCAPE)
####################################################################################################################

# Bandwidth Management
dic_band={'SWT24':'/cgi-bin/dispatcher.cgi?cmd=4101','IDU4':'/cgi-bin/port_bw.cgi','ODU16':'/tddmac.shtml','ODU100':'/raaccessconfig.shtml','IDU8':'/','SWT8':'/','SWT4':'/'}
def render_bandwidth():
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: name state worst_service_state host_address alias\n"
    view = "host"
    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    sitename = __file__.split("/")[3]
    
    longestname = 0
    for site, host, state, worstsvc, address, alias in hosts:
        longestname = max(longestname, len(host))
    if longestname > 15:
        num_columns = 1
    else:
        num_columns = 2

    views.html = html
    views.load_views()
    target = "http://"
    html.write("<table class=allhosts>\n")
    col = 1
    # Open database connection
    db = MySQLdb.connect("localhost","root","root","nms" )

    for site, host, state, worstsvc, address, alias in hosts:

        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        
        sql = "SELECT username,password,port,devicetype from nms_devices\
               WHERE hostname = '%s' AND created_by = '%s' and (devicetype='ODU16' OR devicetype='IDU4' OR devicetype='ODU100' OR devicetype='IDU8' OR devicetype='SWT4' OR devicetype='SWT8' OR devicetype='SWT24')" % (host,config.user)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
             if col == 1:
                 html.write("<tr>")
             html.write("<td>")

             if state > 0 or worstsvc == 2:
                 statecolor = 2
             elif worstsvc == 1:
                 statecolor = 1
             elif worstsvc == 3:
                 statecolor = 3
             else:
                 statecolor = 0
             html.write('<div class="statebullet state%d">&nbsp;</div> ' % statecolor)        

             port = username = password = device_type = ""
             
             for row in result:
                  username = row[0]
                  password = row[1]
                  port = row[2]
                  device_type=row[3]
             if(username != "" and password != ""):
                  address = username + ":" + password + "@" + address
             if(port.strip() != ""):
                  address = address + ":" + port
             
             html.write(link(host, target + ("%s%s" % (address,dic_band[device_type]))))

             if col == num_columns:
                 html.write("</tr>\n")
                 col = 1
             else:
                 col += 1
    db.close()
    if col < num_columns:
        html.write("</tr>\n")
    html.write("</table>\n")


#sidebar_snapins["configuration"] = {
#    "title" : "Host Configuration",
#    "description" : "Showing all hosts to configure that",
#    "render" : lambda: render_config("hosts"),
#    "allowed" : [ "user", "admin", "guest" ],
#    "refresh" : 60,
#    "styles" : snapin_allhosts_styles,
#}
def render_config(mode):
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: name state worst_service_state host_address alias\n"
    view = "host"

    if mode == "summary":
        query += "Filter: custom_variable_names >= _REALNAME\n"
    else:
        query += "Filter: custom_variable_names < _REALNAME\n"

    if mode == "problems":
        query += "Filter: state > 0\nFilter: worst_service_state > 0\nOr: 2\n"
        view = "problemsofhost"

    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    sitename = __file__.split("/")[3]

    longestname = 0
    for site, host, state, worstsvc, address, alias in hosts:
        longestname = max(longestname, len(host))
    if longestname > 15:
        num_columns = 1
    else:
        num_columns = 2

    views.html = html
    views.load_views()
    target = "http://"
    html.write("<table class=allhosts>\n")
    col = 1
    # Open database connection
    db = MySQLdb.connect("localhost","root","root","nms" )

    for site, host, state, worstsvc, address, alias in hosts:

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = "SELECT username,password,port from nms_devices\
               WHERE hostname = '%s' AND created_by = '%s'" % (host,config.user)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
             if col == 1:
                 html.write("<tr>")
             html.write("<td>")

             if state > 0 or worstsvc == 2:
                 statecolor = 2
             elif worstsvc == 1:
                 statecolor = 1
             elif worstsvc == 3:
                 statecolor = 3
             else:
                 statecolor = 0
             html.write('<div class="statebullet state%d">&nbsp;</div> ' % statecolor)        

             port = username = password = ""

             for row in result:
                  username = row[0]
                  password = row[1]
                  port = row[2]

             if(username != "" and password != ""):
                  address = username + ":" + password + "@" + address
             if(port.strip() != ""):
                  address = address + ":" + port


             html.write(link(host, target + ("%s" % (address))))

             if col == num_columns:
                 html.write("</tr>\n")
                 col = 1
             else:
                 col += 1
    db.close()
    if col < num_columns:
        html.write("</tr>\n")
    html.write("</table>\n")


#sidebar_snapins["configuration"] = {
#    "title" : "Host Configuration",
#    "description" : "Showing all hosts to configure that",
#    "render" : lambda: render_config("hosts"),
#    "allowed" : [ "user", "admin", "guest" ],
#    "refresh" : 60,
#    "styles" : snapin_allhosts_styles,
#}
# function to return XML tag text
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

## MRTG
def render_mrtg():
    html.write("MRTG")
    bulletlink("rlx-linux","http://localhost/rlx-linux/")
    
#sidebar_snapins["MRTG"] = {
#    "title" : "MRTG",
#    "description" : "Bandwidth Usage Graphs",
#    "render" : render_mrtg,
#    "allowed" : [ "admin", "user", "guest" ],
#}

## Network GMAP
def render_gmap():
    html.write("GMAP")
    bulletlink("Live_Map",        "http://maps.google.com")
    
#sidebar_snapins["NGMAP"] = {
#    "title" : "Network GMAP",
#    "description" : "Hostgroups on GMAP",
#    "render" : render_gmap,
#    "allowed" : [ "admin", "user", "guest" ],
#}


## Manage host/service manually
def render_management_of_host_service():
    bulletlink("Manage Host Group","manage_hostgroup.py")
    bulletlink("Manage Service Group","manage_servicegroup.py")
    bulletlink("Manage Host","manage_host.py")
    bulletlink("Manage Service","manage_service.py")
    #bulletlink("Manage Service Template","manage_service_template.py")
    
#sidebar_snapins["ManageHostService"] = {
#    "title" : "Manage Host/Service Manually",
#    "description" : "Manage Host group, Service group, Host and Services.",
#    "render" : render_management_of_host_service,
#    "allowed" : [ "admin", "user", "guest" ],
#}

## Auto Discovery
def render_auto_discovery():
    bulletlink("Auto Discovery","auto_discovery.py")
    
#sidebar_snapins["AutoDiscovery"] = {
#    "title" : "Auto Discovery",
#    "description" : "Auto Discover Host and Service in a particular network range.",
#    "render" : render_auto_discovery,
#    "allowed" : [ "admin", "user", "guest" ],
#}
## User Settings
def render_user_setting():
    bulletlink("Change Password","change_password.py")
    bulletlink("Logout","logout.py")
    
#sidebar_snapins["UserSetting"] = {
#    "title" : "User Settings",
#    "description" : "user can change password and logout.",
#    "render" : render_user_setting,
#    "allowed" : [ "admin", "user", "guest" ],
#}

## Configuration Profile
def render_template_setting():
    bulletlink("Manage Configuration Profile","manage_configuration_template.py")
    bulletlink("Manage Host Configuration","manage_host_configuration.py")
    bulletlink("Update ACL","update_acl.py")
    
#sidebar_snapins["APConfigurationProfile"] = {
#    "title" : "AP Configuration Profile",
#    "description" : "User can manage configuration profile and apply it to hosts.",
#    "render" : render_template_setting,
#    "allowed" : [ "admin" ],
#}


## Scheduling
def render_scheduling():
    bulletlink("Access Point Scheduling","ap_scheduling.py")
    bulletlink("Radio Status","radio_status.py")
    
#sidebar_snapins["APScheduling"] = {
#    "title" : "AP Scheduling",
#    "description" : "User can schedule all the devices.",
#    "render" : render_scheduling,
##    "allowed" : [ "admin" ],
#}

## Dashboard
def render_dashboard():
    bulletlink("Dashboard","nms_dashboard.py")
    bulletlink("AP Dashboard","ap_dashboard.py")
    bulletlink("AP Clients Dashboard","ap_clients_dashboard.py")
    
#sidebar_snapins["Dashboard"] = {
#    "title" : "Dashboard",
#    "description" : "User can view all the Statistics of devices",
#    "render" : render_dashboard,
#    "allowed" : [ "admin","user","guest" ],
#}
## FirmWare Update
##def firmware_update():
  ##  bulletlink("Firmware Update","firmware_update.py")

##sidebar_snapins["Firmware"] = {
  ##    "render" : firmware_update,
    #    "description" : "This Is Used To Update All Shyam Devices",
     #   "allowed" : [ "admin"],
#}

## Performance History
def performance_history():
     bulletlink("Performance History","performance_history.py")
    
#sidebar_snapins["Performance"]={
#        "title" : "Performance History",
#        "render" : performance_history,
#        "description" : "This Is Used To Show the Performance of device",
#        "allowed" : [ "admin"],      
#}

# Bandwidth Management
#sidebar_snapins["bandwidth"] = {
#    "title" : "Bandwidth Management",
#    "description" : "Show Network Bandwidth",
#    "render" : lambda: render_bandwidth(),
#    "allowed" : [ "user", "admin", "guest" ],
#    "refresh" : 60,
#    "styles" : snapin_allhosts_styles,
#}

# Map Generator
def render_nagvis_map():
    bulletlink("Generate Map","nagvis_maps.py")
   
#sidebar_snapins["MAPS"] = {
#    "title" : "Maps Generator",
#    "description" : "It generates all connected hosts map",
#    "render" : render_nagvis_map,
#    "allowed" : [ "admin"],
#}

## ODU Details

#def render_odu():
#    bulletlink("ODU Dashboard","odu_dashboard.py")
    #bulletlink("ODU Profiling","odu_profiling.py")
#    bulletlink("ODU Monitoring","odu_monitor_view.py?host_id=67d558f4-c98d-11e0-8121-e0699562882e")
#    bulletlink("UBR/UBRe Listing","odu_listing.py?device_type=ODU16,odu100,ODU16S&device_list_state=enabled&selected_device_type=''")
#    bulletlink("UBR Common Dashboard","odu_dashboard.py") 
#    bulletlink("UBRe Common Dashboard","odu100_common_dashboard.py")
#    bulletlink("UBR Schdeuling","odu_scheduling.py")
#sidebar_snapins["OduDetail"]={
#    "title":"UBR/UBRe",
#    "description":"It displays all UBR/UBRe device Information.",
#    "render":render_odu,
#    "allowed":["admin","user","guest"],
#}

##Nagvis_map javascript_map
#def render_mapsjavascript():
#    bulletlink("Map","mapsjavascript.py")

#sidebar_snapins["MAPS_NETWORK"] = {
#    "title" : "Network Auto Map",
#    "description" : "It display the all connected host maps in graphical format",
#    "render" : render_mapsjavascript,
#    "allowed" : [ "admin","user","guest" ],
#}

##alarm masking 
def render_alarms():
	bulletlink("Event Details","status_snmptt.py")
	bulletlink("Alarm Masking","alarm_mapping.py")
#	bulletlink("Alarm Events","alarm_masking.py")

sidebar_snapins["Alarm"] = { 
	"title":"Alarms",
	"description":"It display all alarm details, trap information and managing alarm mapping and masking.",
	"render":render_alarms,
	"allowed":["admin","user","guest"],
}


# Google Maps
def render_googlemap():
	bulletlink("Geographical-Map","googlemap.py")
	bulletlink("Topology Map","circle_graph.py")
	bulletlink("Planner","http://rfplanner.codescape.in/v7/NewTransmission/transmission.php")
sidebar_snapins["Network Maps"] = { 
	"title":"Network Maps",
	"description":"It display network maps.",
	"render":render_googlemap,
	"allowed":[ "admin","user","guest"],
}

# idu_dashboard
#def render_idu_dashboard():
#	bulletlink("IDU Dashboard","idu_dashboard.py?host_id=85585ffc-bf60-11e0-af8e-bcaec5e42b00&ip_address=172.22.0.104")

#sidebar_snapins["IDU_dashboard"] = { 
#	"title":"IDU Dashboard",
#	"description":"It display the IDU dashboard.",
#	"render":render_idu_dashboard,
#	"allowed":[ "admin" ],
#}

#Firmware Update
#def render_firmware_update():
#	bulletlink("Firmware Update","firmware_listing.py")

#sidebar_snapins["FirmwareUpdate"]={
#	 "title" : "Firmware Update",
#        "render" : render_firmware_update,
#        "description" : "This is used to update all Shyam devices.",
#        "allowed" : [ "admin","user"],	
#}


# Swtitch Profiling
#def render_swt_profiling():
#	bulletlink("Switch Profiling","swt_profiling.py")
#sidebar_snapins["Switch Profiling"]={
#    "title":"Switch",
#    "description":"It display all Switch Information",
#    "render":render_swt_profiling,
#   "allowed":["admin"],
#}

# Yogesh @ 13 Nov

## Inventory Other
def render_unmp_other():
     bulletlink("Manage Vendors","manage_vendor.py")
     bulletlink("Manage Black List Mac","manage_black_list_mac.py")

#sidebar_snapins["inventory_other"]={
#   "title":"Other",
#   "description":"Here You can manage Inventory's Other Modules",
#   "render":render_unmp_other,
#   "allowed":["admin"],
#}


## User Management
def render_unmp_user_management():
     bulletlink("Manage User","manage_user.py")
     bulletlink("Manage Group","manage_group.py")
     #bulletlink("Group to Hostgroup","group_to_hg_view.py")
     #bulletlink("Hostgroup to Group","hostgroup_group_view.py")
     bulletlink("Manage Session","manage_login.py")
     
     
sidebar_snapins["user_management"]={
   "title":"User Management",
   "description":"Here you can manage user, user session and usergroup.",
   "render":render_unmp_user_management,
   "allowed":["admin"],
}

## Reporting 
def reporting_module():
     bulletlink("Report","main_report.py")
     bulletlink("Analyzed Report","analyzed_report.py")
     bulletlink("Backup & Restore","history_report.py")
     bulletlink("Inventory Report","inventory_report.py")
#     bulletlink("AP Reporting","main_report.py?device_type_user_selected_id=ap25&device_type_user_selected_name=AP25")
     bulletlink("IDU Report","main_report.py?device_type_user_selected_id=idu4&device_type_user_selected_name=IDU4PORT")
     bulletlink("UBR Report","main_report.py?device_type_user_selected_id=odu16&device_type_user_selected_name=UBR")
     bulletlink("UBRe Report","main_report.py?device_type_user_selected_id=odu100&device_type_user_selected_name=UBRe")
     bulletlink("Events Report","trapreport.py")     
#     bulletlink("Network Outage","manage_network_outage_report.py")
#     bulletlink("Trap Report","manage_trap_report.py")
#     bulletlink("Inventory Report","inventory_report.py")
#     bulletlink("UBRe CRC-PHY Error","ubre_manage_crc_phy_report.py")
#     bulletlink("UBRe RSSI Report","ubre_manage_rssi_report.py")
#     bulletlink("UBRe Network Usage","ubre_manage_network_usage_report.py")

sidebar_snapins["reports"]={
   "title":"Reports",
   "description":"Here you can view all reports.",
   "render":reporting_module,
   "allowed":["admin","user","guest"],
}


# delete sampe data
## Reporting 
#def reporting_default_data_delete():
#     bulletlink("Delete Sample Data","default_data_delete.py")
#sidebar_snapins["SampleDelete"]={
#   "title":"Delete Sample Data",
#   "description":"It delete the all sample data from database.",
#   "render":reporting_default_data_delete,
#   "allowed":["admin"],
#}
## scheduling
def scheduling_module():
     bulletlink("Scheduling","odu_scheduling.py")
#     bulletlink("Network Outage","manage_network_outage_report.py")
#     bulletlink("Trap Report","manage_trap_report.py")
#     bulletlink("Inventory Report","inventory_report.py")
#     bulletlink("UBRe CRC-PHY Error","ubre_manage_crc_phy_report.py")
#     bulletlink("UBRe RSSI Report","ubre_manage_rssi_report.py")
#     bulletlink("UBRe Network Usage","ubre_manage_network_usage_report.py")

sidebar_snapins["schedule"]={
   "title":"Scheduling",
   "description":"It schedules all devices.",
   "render":scheduling_module,
   "allowed":["admin","user"],
}


def render_common_listing():
    bulletlink("UBR/UBRe Listing","odu_listing.py?device_type=ODU16,odu100,ODU16S&device_list_state=enabled&selected_device_type=''")
    #bulletlink("AP Listing","ap_listing.py?device_type=ap25&device_list_state=enabled&selected_device_type=''")
    bulletlink("IDU Listing","idu_listing.py?device_type=idu4,idu8&device_list_state=enabled&selected_device_type=''")
    bulletlink("UBR Common Dashboard","odu_dashboard.py") 
    bulletlink("UBRe Common Dashboard","odu100_common_dashboard.py")
    
sidebar_snapins["Listing"]={
    "title":"Listing",
    "description":"It display all device information.",
    "render":render_common_listing,
    "allowed":["admin","user","guest"],
}



## host linkinkg
def host_details():
    global html
    user_id = html.req.session['user_id']
    
    sitename = __file__.split("/")[3]    # get site name of current nms.
    # set parameter and default values
    mysql_host = "localhost"
    mysql_user_name = "root"
    mysql_password = "root"
    mysql_db_schema = "nmsp"
    try:
        # config.xml file path
        xml_config_file = "/omd/sites/%s/share/check_mk/web/htdocs/xml/config.xml" % sitename
        if(os.path.isfile(xml_config_file)):
            dom = xml.dom.minidom.parse(xml_config_file)    # create xml dom object for config.xml file
            mysql_dom = dom.getElementsByTagName("mysql")
            for m in mysql_dom:
                mysql_host = m.getAttribute("hostname")
                mysql_user_name = m.getAttribute("username")
                mysql_password = m.getAttribute("password")
                mysql_db_schema = m.getAttribute("schema")

        db=MySQLdb.connect(mysql_host,mysql_user_name,mysql_password,mysql_db_schema)
        cursor=db.cursor()
    # create the connection
        sel_query = "SELECT DISTINCT h.ip_address,h.host_id FROM users_groups AS ug \
JOIN (SELECT hostgroup_id, group_id FROM hostgroups_groups) AS hg ON ug.group_id = hg.group_id \
JOIN (SELECT host_id, hostgroup_id FROM hosts_hostgroups) AS hh ON hg.hostgroup_id = hh.hostgroup_id \
JOIN (SELECT host_id,ip_address,is_deleted FROM hosts) AS h ON h.host_id = hh.host_id \
WHERE h.is_deleted = 0 AND ug.user_id = '%s' or h.ip_address = 'localhost'"%(user_id)
        #bulletlink("%s"%sel_query,"device_details_example.py?host_id=%s"%mysql_host)
        #sel_query="SELECT hosts.ip_address,hosts.host_id FROM hosts where is_deleted =0"
        cursor.execute(sel_query)  
        host_result=cursor.fetchall()
        cursor.close()
        db.close()      
        if len(host_result) > 0:
            for host in host_result:    
                bulletlink("%s"%host[0],"device_details_example.py?host_id=%s"%host[1])
        else:
            bulletlink("No host exists ","#")    

    except Exception,e:
        bulletlink("No host exists : %s"%str(e),"#")
sidebar_snapins["Hosts"]={
   "title":"Hosts Details",
   "description":"It display all host details.",
   "render":host_details,
   "allowed":["admin","user","guest"],
   "refresh" : 30,
}
## IDU Details

#def render_idu():
#   bulletlink("IDU Listing","idu_listing.py?device_type=idu4,idu8&device_list_state=enabled&selected_device_type=''")
#   bulletlink("IDU4 Common Dashboard","idu4_controller.py")

#sidebar_snapins["IDU"]={
#    "title":"IDU",
#    "description":"It display all IDU information.",
#    "render":render_idu,
#    "allowed":["admin","user","guest"],
#}

# IDU dashboard bullet link start here
#def idu4_controller():
#     bulletlink("IDU4 Dashboard","idu4_controller.py")
#sidebar_snapins["IDU4Dashboard"]={
#   "title":"IDU4 Dashboard",
#   "description":"It display the idu 4 port graphs.",
#   "render":idu4_controller,
#   "allowed":["admin"],
#}
# IDU dashboard bullet link end here

