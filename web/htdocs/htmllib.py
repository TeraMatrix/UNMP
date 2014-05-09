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
import cgi
import config
import os
import defaults
import pwd
import urllib
from lib import *
from unmp_config import SystemConfig
import __builtin__

# "blue" or "red" theme
__builtin__.theme = "red"
# Python 2.3 does not have 'set' in normal namespace.
# But it can be imported from 'sets'
try:
    set()
except NameError:
    from sets import Set as set

# Sidebar snapin Added By Yogesh Kumar
sidedar_snapins_category = {
    "home": [
        "main"
    ],
    "inventory": [
        "manage_host",
        "manage_hostgroup",
        "discovery",
        "manage_service",
        "ap_listing",
        "idu_listing",
        "odu_listing",
        "odu_dashboard",
        "odu100_common_dashboard",
        "odu_scheduling",
        "googlemap",
        "circle_graph",
        "status_snmptt",
        "alarm_mapping",
        "manage_events",
        "manage_logs",
        "manage_user",
        "manage_group",
        "manage_login",
        "sp_status_profiling"
    ],
    "reports": [
        "main_report",
        "analyzed_report",
        "history_report",
        "main_report_ap25",
        "main_report_idu4",
        "main_report_odu16",
        "main_report_odu100",
        "trapreport"
    ],
    "settings": [
        "daemons_controller",
        "manage_license",
        "user_settings"
    ]
}

sidebar_snapins = {}

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


def link(text, target):
    # Convert relative links into absolute links. We have three kinds
    # of possible links and we change only [3]
    # [1] protocol://hostname/url/link.py
    # [2] /absolute/link.py
    # [3] relative.py
    """

    @param text:
    @param target:
    @return:
    """
    if not (":" in target[:10]) and target[0] != '/':
        target = defaults.url_prefix + "check_mk/" + target
    return "<a target=\"main\" class=link href=\"%s\">%s</a>" % (target, attrencode(text))


def bulletlink(text, target):
    """

    @param text:
    @param target:
    @return:
    """
    return "<li class=sidebar>" + link(text, target) + "</li>\n"


def render_snapin(html, snapin_list, selected_link):
    """

    @param html:
    @param snapin_list:
    @param selected_link:
    """
    state = "closed"
    first_snapin = ""
    remain_snapin = ""
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    if len(snapin_list) == 0:
        for name in sidebar_snapins:
            snapin = sidebar_snapins.get(name)
            if config.role in snapin["allowed"]:
                snapin_links = ""
                try:
                    snapin_links = snapin["render"]()
                except Exception, e:
                    snapin_links = "Links are not defined"

                if selected_link != "" and snapin_links.find(selected_link) != -1:
                    first_snapin += "<div id=\"snapin_container_%s\" class=\"snapin\">\n" % name
                    style = ""
                    headclass = "open"
                    first_snapin += '<div class="head %s" >' % headclass
                    first_snapin += "<b class=\"heading\" >%s</b>" % snapin[
                        "title"]
                    first_snapin += "</div>"
                    first_snapin += "<div id=\"snapin_%s\" class=\"content\"%s>\n" % (
                        name, style)
                    first_snapin += snapin_links
                    first_snapin += '</div></div>'
                else:
                    remain_snapin += "<div id=\"snapin_container_%s\" class=snapin>\n" % name
                    style = ' style=\"display:none\"'
                    headclass = "closed"
                    remain_snapin += '<div class="head %s" >' % headclass
                    remain_snapin += "<b class=\"heading\" >%s</b>" % snapin[
                        "title"]
                    remain_snapin += "</div>"
                    remain_snapin += "<div id=\"snapin_%s\" class=\"content\"%s>\n" % (
                        name, style)
                    remain_snapin += snapin_links
                    remain_snapin += '</div></div>'
    else:
        for name in sidebar_snapins:
            if name in snapin_list:
                snapin = sidebar_snapins.get(name)
                if config.role in snapin["allowed"]:
                    snapin_links = ""
                    try:
                        snapin_links = snapin["render"]()
                    except Exception, e:
                        snapin_links = "Links are not defined"

                    if selected_link != "" and snapin_links.find(selected_link) != -1:
                        first_snapin += "<div id=\"snapin_container_%s\" class=\"snapin\">\n" % name
                        style = ""
                        headclass = "closed"
                        first_snapin += '<div class="head %s" >' % headclass
                        first_snapin += "<b class=\"heading\">%s</b>" % snapin[
                            "title"]
                        first_snapin += "</div>"
                        first_snapin += "<div id=\"snapin_%s\" class=\"content\"%s>\n" % (
                            name, style)
                        first_snapin += snapin_links
                        first_snapin += '</div></div>'
                    else:
                        remain_snapin += "<div id=\"snapin_container_%s\" class=\"snapin\">\n" % name
                        style = ' style=\"display:none\"'
                        headclass = "closed"
                        remain_snapin += '<div class="head %s" >' % headclass
                        remain_snapin += "<b class=\"heading\">%s</b>" % snapin[
                            "title"]
                        remain_snapin += "</div>"
                        remain_snapin += "<div id=\"snapin_%s\" class=\"content\"%s>\n" % (
                            name, style)
                        remain_snapin += snapin_links
                        remain_snapin += '</div></div>'
    html.write("<input type='hidden' id='selected_link' value='%s'/>" %
               selected_link)
    html.write(first_snapin)
    html.write(remain_snapin)


def create_side_bar(html, snapin_list, selected_link):
    """

    @param html:
    @param snapin_list:
    @param selected_link:
    """
    html.write('<div id="side_content" aa="%s">' % len(snapin_list))
    render_snapin(html, snapin_list, selected_link)
    html.write('</div>')


def snapin_exception(e):
    """

    @param e:
    @raise:
    """
    if config.debug:
        raise
    else:
        html.write("<div class=snapinexception>\n"
                   "<h2>Error</h2>\n"
                   "<p>%s</p></div>" % e)

# End Sidebar snapin Added By Yogesh Kumar

company = SystemConfig.get_company_details()
about_us = SystemConfig.get_system_about_us()

# Information about uri


class InvalidUserInput(Exception):
    """

    @param varname:
    @param text:
    """

    def __init__(self, varname, text):
        self.varname = varname
        self.text = text


class uriinfo:
    """

    @param req:
    """

    def __init__(self, req):
        self.req = req

    # URI aus Dateiname und Variablen rekonstruieren
    # TODO: URI-Encode von Variablen!
    def geturi(self):
        """


        @return:
        """
        uri = self.req.myfile + ".py"
        if len(self.req.vars):
            uri += "?" + urlencode(self.req.vars.items())
        return uri

    # [('varname1', value1), ('varname2', value2) ]
    def makeuri(self, addvars):
        """

        @param addvars:
        @return:
        """
        return self.req.myfile + ".py?" + urlencode_vars(self.req.vars.items() + addvars)

    # Liste von Hidden-Felder erzeugen aus aktueller URI
    def hiddenfields(self, omit=[]):
        """

        @param omit:
        @return:
        """
        return ''.join(['<input type=hidden name="%s" value="%s">\n' % i
                        for i in self.req.vars.items()
                        if i[0] not in omit])


def attrencode(value):
    """

    @param value:
    @return:
    """
    if type(value) in [str, unicode]:
        return cgi.escape(value)
    else:
        return cgi.escape(str(value), True)

# This function returns a str object, never unicode!


def urlencode_vars(vars):
    """

    @param vars:
    @return:
    """
    output = ""
    for varname, value in vars:
        if output != "":
            output += "&"

        if type(value) == int:
            value = str(value)
        if type(value) == str:
            value = unicode(value, 'utf-8')

        output += varname
        output += "="
        output += urlencode(value)
    return output


def urlencode(value):
    """

    @param value:
    @return:
    """
    if type(value) == unicode:
        value = value.encode("utf-8")
    ret = ""
    for c in value:
        if c == " ":
            c = "+"
        elif ord(c) <= 32 or ord(c) > 127 or c in ['+', '"', "'", "=", "&", ":", "%"]:
            c = "%%%02x" % ord(c)
        ret += c
    return ret


def urldecode(value):
    """

    @param value:
    @return:
    """
    return urllib.unquote_plus(value)


def u8(c):
    """

    @param c:
    @return:
    """
    if ord(c) > 127:
        return "&#%d;" % ord(c)
    else:
        return c


def utf8_to_entities(text):
    """

    @param text:
    @return:
    """
    if type(text) != unicode:
        return text
    n = ""
    for c in text:
        n += u8(c)
    return n

# remove all HTML-tags


def strip_tags(ht):
    """

    @param ht:
    @return:
    """
    while True:
        x = ht.find('<')
        if x == -1:
            break
        y = ht.find('>')
        ht = ht[0:x] + ht[y + 1:]
    return ht


class html:
    """

    @param req:
    """
    user = ""
    unmp_menu_link = ["main.py", "manage_host.py", "main_report.py",
                      "daemons_controller.py"]
    unmp_menu_name = ["Home", "Inventory", "Reports", "Settings"]
    unmp_sub_menu_link = [
        [],
        [],
        [],
        []
    ]
    unmp_sub_menu_name = [
        [],
        [],
        [],
        []
    ]

    # user
    unmp_menu_link_u = ["main.py", "manage_host.py", "main_report.py"]
    unmp_menu_name_u = ["Home", "Inventory", "Reports"]
    unmp_sub_menu_link_u = [
        [],
        [],
        []
    ]
    unmp_sub_menu_name_u = [
        [],
        [],
        []
    ]

    # guest
    unmp_menu_link_g = ["main.py", "main_report.py"]
    unmp_menu_name_g = ["Home", "Reports"]
    unmp_sub_menu_link_g = [
        [],
        []
    ]
    unmp_sub_menu_name_g = [
        [],
        []
    ]

    def __init__(self, req):
        self.req = req
        self.user_errors = {}
        self.focus_object = None
        self.global_vars = []
        self.browser_reload = 0
        self.browser_redirect = ''
        self.events = set([])  # currently used only for sounds
        self.req.header_sent = False
        self.output_format = "html"

    def set_output_format(self, f):
        """

        @param f:
        """
        self.output_format = f

    def write(self, text):
        """

        @param text:
        """
        if type(text) == unicode:
            text = text.encode("utf-8")
        self.req.write(text)

    def heading(self, text):
        """

        @param text:
        """
        self.write("<h2>%s</h2>\n" % text)

    def rule(self):
        """


        """
        self.write("<hr/>")

    def age_text(self, timedif):
        """

        @param timedif:
        @return:
        """
        timedif = int(timedif)
        if timedif < 120:
            return "%d sec" % timedif

        minutes = timedif / 60
        if minutes < 120:
            return "%d min" % minutes

        hours = minutes / 60
        if hours < 48:
            return "%d hrs" % hours

        days = hours / 24
        return "%d days" % days

    def begin_form(self, name, action=None, method="GET"):
        """

        @param name:
        @param action:
        @param method:
        """
        self.form_vars = []
        if action == None:
            action = self.req.myfile + ".py"
        self.current_form = name
        self.write("<form name=%s class=%s action=\"%s\" method=%s>\n" %
                   (name, name, action, method))
        self.hidden_field("filled_in", "on")
        self.hidden_field("_transid", str(
            self.current_transid(self.req.session["username"])))
        self.hidden_fields(self.global_vars)
        self.form_name = name

    def end_form(self):
        """


        """
        self.write("</form>\n")

    def add_user_error(self, varname, message):
        """

        @param varname:
        @param message:
        """
        if type(varname) == list:
            for v in varname:
                self.add_user_error(v, message)
        else:
            self.user_errors[varname] = message

    def has_users_errors(self):
        """


        @return:
        """
        return len(self.user_errors) > 0

    def hidden_field(self, var, value):
        """

        @param var:
        @param value:
        """
        if value != None:
            self.write("<input type=hidden name=%s value=\"%s\">\n" % (
                var, attrencode(value)))

    def hidden_fields(self, varlist=None, **args):
        """

        @param varlist:
        @param args:
        """
        add_action_vars = args.get("add_action_vars", False)
        if varlist != None:
            for var in varlist:
                value = self.req.vars.get(var, "")
                self.hidden_field(var, value)
        else:  # add *all* get variables, that are not set by any input!
            for var, value in self.req.vars.items():
                if var not in self.form_vars and \
                        (var[0] != "_" or add_action_vars):
                    self.hidden_field(var, value)

    def add_global_vars(self, varnames):
        """

        @param varnames:
        """
        self.global_vars += varnames

    # [('varname1', value1), ('varname2', value2) ]
    def makeuri(self, addvars):
        """

        @param addvars:
        @return:
        """
        vars = [(v, self.var(v))
                for v in self.req.vars if not v.startswith("_")]
        return self.req.myfile + ".py?" + urlencode_vars(vars + addvars)

    def makeuri_contextless(self, vars):
        """

        @param vars:
        @return:
        """
        return self.req.myfile + ".py?" + urlencode_vars(vars)

    def button(self, varname, title, cssclass=""):
        """

        @param varname:
        @param title:
        @param cssclass:
        """
        self.write("<input type=submit name=\"%s\" id=\"%s\" value=\"%s\" class=\"%s\">\n" %
                   (varname, varname, title, cssclass))

    def buttonlink(self, href, text, add_transid=False):
        """

        @param href:
        @param text:
        @param add_transid:
        """
        if add_transid:
            href += "&_transid=%d" % self.current_transid(
                self.req.session["username"])
        self.write("<a href=\"%s\" class=button>%s</a>" % (href, text))

    def begin_context_buttons(self):
        """


        """
        self.write("<table class=contextlinks><tr><td>\n")

    def end_context_buttons(self):
        """


        """
        self.write("</td></tr></table>\n")

    def context_button(self, title, url, hot=False):
        """

        @param title:
        @param url:
        @param hot:
        """
        self.write('<div class="contextlink%s" ' % (hot and " hot" or ""))
        self.write(r'''onmouseover='this.style.backgroundImage="url(\"images/contextlink%s_hi.png\")";' ''' % (
            hot and "_hot" or ""))
        self.write(r'''onmouseout='this.style.backgroundImage="url(\"images/contextlink%s.png\")";' ''' %
                   (hot and "_hot" or ""))
        self.write('>')
        self.write('<a href="%s">%s</a></div>' % (url, title))

    def number_input(self, varname, deflt="", size=8):
        """

        @param varname:
        @param deflt:
        @param size:
        """
        self.text_input(varname, str(deflt), "number", size=size)

    def text_input(self, varname, default_value="", cssclass="text", **args):
        """

        @param varname:
        @param default_value:
        @param cssclass:
        @param args:
        """
        if default_value == None:
            default_value = ""
        addprops = ""
        if "size" in args:
            addprops += " size=%d" % args["size"]

        value = self.req.vars.get(varname, default_value)
        error = self.user_errors.get(varname)
        html = ""
        if error:
            html = "<x class=inputerror>"
        html += "<input type=text class=%s value=\"%s\" name=\"%s\"%s>" % (
            cssclass, attrencode(value), varname, addprops)
        if error:
            html += "</x>"
            self.set_focus(varname)
        self.write(html)
        self.form_vars.append(varname)

    def text_area(self, varname, rows):
        """

        @param varname:
        @param rows:
        """
        value = self.req.vars.get(varname, "")
        self.write("<textarea name=\"%s\">%s</textarea>\n" % (varname, value))
        self.form_vars.append(varname)

    def sorted_select(self, varname, options, deflt="", onchange=None):
        # Sort according to display texts, not keys
        """

        @param varname:
        @param options:
        @param deflt:
        @param onchange:
        """
        swapped = [(disp, key) for key, disp in options]
        swapped.sort()
        swapped = [(key, disp) for disp, key in swapped]
        html.select(self, varname, swapped, deflt, onchange)

    def select(self, varname, options, deflt="", onchange=None):
        """

        @param varname:
        @param options:
        @param deflt:
        @param onchange:
        """
        current = self.var(varname, deflt)
        onchange_code = onchange and " onchange=\"%s\"" % (onchange) or ""
        self.write("<select%s name=\"%s\" id=\"%s\" size=\"1\">\n" % (
            onchange_code, varname, varname))
        for value, text in options:
            if value == None:
                value = ""
            sel = value == current and " selected" or ""
            self.write(
                "<option value=\"%s\"%s>%s</option>\n" % (value, sel, text))
        self.write("</select>\n")
        self.form_vars.append(varname)

    def radiobutton(self, varname, value, checked, text):
        """

        @param varname:
        @param value:
        @param checked:
        @param text:
        """
        checked_text = checked and " checked" or ""
        self.write("<input type=radio name=%s value=\"%s\"%s> %s &nbsp; \n" %
                   (varname, value, checked_text, text))
        self.form_vars.append(varname)

    def checkbox(self, varname, deflt=""):
        """

        @param varname:
        @param deflt:
        """
        value = self.req.vars.get(varname, deflt)
        if value != "" and value != False:
            checked = " CHECKED"
        else:
            checked = ""
        self.write("<input type=checkbox name=\"%s\"%s>" % (
            urlencode(varname), checked))
        self.form_vars.append(varname)

    def datetime_input(self, varname, default_value):
        """

        @param varname:
        @param default_value:
        """
        try:
            t = self.get_datetime_input(varname)
        except:
            t = default_value

        br = time.localtime(t)
        self.date_input(varname + "_date", br.tm_year, br.tm_mon, br.tm_mday)
        self.write(" ")
        self.time_input(varname + "_time", br.tm_hour, br.tm_min)
        self.form_vars.append(varname + "_date")
        self.form_vars.append(varname + "_time")

    def time_input(self, varname, hours, mins):
        """

        @param varname:
        @param hours:
        @param mins:
        """
        error = self.user_errors.get(varname)
        if error:
            self.write("<x class=inputerror>")
        self.write("<input type=text size=5 class=time name=%s value=\"%02d:%02d\">" %
                   (varname, hours, mins))
        if error:
            self.write("</x>")
        self.form_vars.append(varname)

    def date_input(self, varname, year, month, day):
        """

        @param varname:
        @param year:
        @param month:
        @param day:
        """
        error = self.user_errors.get(varname)
        if error:
            self.write("<x class=inputerror>")
        self.write("<input type=text size=10 class=date name=%s value=\"%04d-%02d-%02d\">" %
                   (varname, year, month, day))
        if error:
            self.write("</x>")
        self.form_vars.append(varname)

    def get_datetime_input(self, varname):
        """

        @param varname:
        @return: @raise:
        """
        t = self.var(varname + "_time")
        d = self.var(varname + "_date")
        if not t or not d:
            raise MKUserError([varname + "_date", varname + "_time"],
                              "Please specify a date and time")

        try:
            br = time.strptime(d + " " + t, "%Y-%m-%d %H:%M")
        except:
            raise MKUserError([varname + "_date", varname + "_time"],
                              "Please enter the date/time in the format YYYY-MM-DD HH:MM")
        return int(time.mktime(br))

    def get_time_input(self, varname, what):
        """

        @param varname:
        @param what:
        @return: @raise:
        """
        t = self.var(varname)
        if not t:
            raise MKUserError(varname, "Please specify %s" % what)

        try:
            h, m = t.split(":")
            m = int(m)
            h = int(h)
            if m < 0 or m > 59 or h < 0:
                raise Exception()
        except:
            raise MKUserError(
                varname, "Please enter the time in the format HH:MM")
        return m * 60 + h * 3600

    def html_head(self, title):
        """

        @param title:
        """
        if not self.req.header_sent:
            self.req.write(
                u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                <html><head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>''')
            self.req.write(title.encode("utf-8"))
            self.req.write('''</title>
                <link rel="stylesheet" type="text/css" href="check_mk.css">
		<link rel="stylesheet" type="text/css" href="check_mk.css">''')
            if config.custom_style_sheet:
                self.req.write('                <link rel="stylesheet" type="text/css" href="%s">' %
                               config.custom_style_sheet)
            self.req.write('''
                <script type='text/javascript' src='js/check_mk.js'></script>
                <script type='text/javascript' src='js/hover.js'></script>
            ''')

            if self.browser_reload != 0:
                if self.browser_redirect != '':
                    self.req.write("<script type=\"text/javascript\">setReload(%s, '%s')</script>\n" %
                                   (self.browser_reload, self.browser_redirect))
                else:
                    self.req.write("<script type=\"text/javascript\">setReload(%s)</script>\n" %
                                   self.browser_reload)

            self.req.write("</head>\n")
            self.req.header_sent = True

    def html_foot(self):
        """


        """
        self.write("</html>\n")

    def set_browser_reload(self, secs):
        """

        @param secs:
        """
        self.browser_reload = secs

    def set_browser_redirect(self, secs, url):
        """

        @param secs:
        @param url:
        """
        self.browser_reload = secs
        self.browser_redirect = url

    def header(self, title=''):
        """

        @param title:
        """
        if self.output_format == "html":
            if not self.req.header_sent:
                self.html_head(title)
                self.write("<body class=main>")
                self.req.header_sent = True
                self.top_heading(title)

    def top_heading(self, title):
        """

        @param title:
        """
        if type(self.req.session["username"]) == str:
            login_text = "<b>%s</b> (%s)" % (config.user, config.role)
        else:
            login_text = "not logged in"

    # Edit By Yogesh Kumar
    def page_head(self, title):
        """

        @param title:
        """
        if type(self.req.session["username"]) == str:
            login_text = "<b>%s</b> (%s)" % (config.user, config.role)
        else:
            login_text = "not logged in"
        self.write("<html><head></head><body class=main>")
        self.write("<table class=header><tr><td class=left>%s</td><td class=right>"
                   "%s &nbsp; &nbsp; <b class=headertime>%s</b> <img src=\"images/mk_logo_klein.png\"></td></tr></table>" %
                   (title, login_text, time.strftime("%H:%M")))
        self.write("<hr class=header>\n")
        self.write("</body></html>")

    def new_html_head(self, title, css_list=[], javascript_list=[]):
        """

        @param title:
        @param css_list:
        @param javascript_list:
        """
        if not self.req.header_sent:
            self.req.write(
                u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                <html><head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <meta http-equiv="Cache-Control" content="no-cache"/>
                <meta http-equiv="PRAGMA" content="no-cache"/>
                <meta http-equiv="expires" content="0"/>
            <title>''')
            self.req.write(title.encode("utf-8"))

            self.req.write('''</title>
		<link rel="stylesheet" type="text/css" href="css/{0}/example.css"/>
		<link rel="stylesheet" type="text/css" href="css/colorbox.css"/>
		<link rel="stylesheet" type="text/css" href="css/{0}/impromptu.css"/>
		<link rel="stylesheet" type="text/css" href="css/toastmessage.css"/>
		<!--[if IE]>
		       <link rel="stylesheet" type="text/css" href="css/ie_example.css"/>
		<![endif]-->
		<!--[if IE 8]>
		       <link rel="stylesheet" type="text/css" href="css/ie8.css"/>
		<![endif]-->
		<!--[if IE 7]>
		       <link rel="stylesheet" type="text/css" href="css/{0}/ie7.css"/>
		<![endif]-->
		'''.format(theme))
            for css in css_list:
                if css in ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css", "css/sidepanel.css"]:
                    css = css.replace("/", "/" + theme + "/")
                self.req.write(
                    '<link rel="stylesheet" type="text/css" href="' + css + '"></link>')
            if config.custom_style_sheet:
                self.req.write('<link rel="stylesheet" type="text/css" href="%s"></link>' %
                               config.custom_style_sheet)
            self.req.write('''
                <script type='text/javascript' src='js/check_mk.js'></script>
                <script type='text/javascript' src='js/hover.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery-1.6.1.min.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery-1.4.4.min.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery.validate.min.js'></script>
                <script type='text/javascript' src='js/unmp/main/ccpl_utility.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery.colorbox-min.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery-impromptu.3.1.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery.toastmessage.js'></script>
                <script type='text/javascript' src='js/lib/main/spin.min.js'></script>
                <script type='text/javascript' src='js/lib/main/jquery.tipsy.js'></script>
                <script type='text/javascript' src='js/lib/main/flowplayer.tooltip.tools.min.js'></script>
                <script type='text/javascript' src='js/unmp/main/common.js'></script>
            ''')
            for js in javascript_list:
                self.req.write(
                    '<script type="text/javascript" src="' + js + '"></script>')

            if self.browser_reload != 0:
                if self.browser_redirect != '':
                    self.req.write("<script type=\"text/javascript\">setReload(%s, '%s')</script>\n" %
                                   (self.browser_reload, self.browser_redirect))
                else:
                    self.req.write("<script type=\"text/javascript\">setReload(%s)</script>\n" %
                                   self.browser_reload)

            self.req.write("</head>\n")
            self.req.header_sent = True

    def new_top_heading(self, title, selected_link="", image_btn="", snapin_list=[]):
        """

        @param title:
        @param selected_link:
        @param image_btn:
        @param snapin_list:
        """
        rl = config.role
        if self.req.session["group"].lower() == "superadmin":
            login_text = "<img style=\"width:16px;height:16px;\" src=\"images/new_icons/user.png\" alt=\"\" title=\"User\"/><span><b>%s</b> (%s)</span>" % (
                self.req.session["username"], "SuperAdmin")
        else:
            login_text = "<img style=\"width:16px;height:16px;\" src=\"images/new_icons/user.png\" alt=\"\" title=\"User\"/><span><b>%s</b> (%s)</span>" % (
                self.req.session["username"], rl.title())

        #		<div id="page_title">\
        #			<span> </span>\
        #		</div>\
        # spin loading
        self.req.write(
            "<div id=\"main_loading\" class=\"main_loading\"></div><div class=\"spin-loading\" id=\"spin_loading\"></div>")

        # header menu and sub menu
        menu = ""
        sub_menu = ""
        sub_menu_ = ""
        div_id = ""

        if rl == "user":
            self.unmp_menu_link = self.unmp_menu_link_u
            self.unmp_sub_menu_link = self.unmp_sub_menu_link_u
            self.unmp_sub_menu_name = self.unmp_sub_menu_name_u
            self.unmp_menu_name = self.unmp_menu_name_u

        elif rl == "guest":
            self.unmp_menu_link = self.unmp_menu_link_g
            self.unmp_sub_menu_link = self.unmp_sub_menu_link_g
            self.unmp_sub_menu_name = self.unmp_sub_menu_name_g
            self.unmp_menu_name = self.unmp_menu_name_g

        for menu_link_i in range(len(self.unmp_menu_link) - 1, -1, -1):
            active_menu = ""
            active_sub_menu = ""
            sub_menu_ = ""
            active_css = " style=\"display:none;\""
            for sub_menu_link_i in range(0, len(self.unmp_sub_menu_link[menu_link_i])):
                active_sub_menu = ""
                if selected_link == self.unmp_sub_menu_link[menu_link_i][sub_menu_link_i]:
                    active_menu = " active"
                    active_sub_menu = " menu-link-active"
                    active_css = ""
                sub_menu_ += '<a href="%s" class=\"menu-link%s\">%s</a>' % (
                    self.unmp_sub_menu_link[menu_link_i][sub_menu_link_i], active_sub_menu,
                    self.unmp_sub_menu_name[menu_link_i][sub_menu_link_i])
            div_id_ = self.unmp_menu_link[menu_link_i].split("#")
            if len(div_id_) > 1:
                div_id = div_id_[1]
            else:
                div_id = div_id_[0]
            if selected_link == self.unmp_menu_link[menu_link_i]:
                active_menu = " active"
                active_css = ""

            sub_menu_ = "<div class=\"header2_menu_div\" id=\"%s\"%s>" % (
                div_id, active_css) + sub_menu_ + "</div>"
            sub_menu = sub_menu + sub_menu_
            # new logic for selected menu
            if sidedar_snapins_category[self.unmp_menu_name[menu_link_i].lower()].count(
                    str(selected_link).split(".py")[0]) > 0:
                active_menu = " active"
            else:
                active_menu = ""
                # end new logic for selected menu
            menu += '<div class="icon%s">\
                <a href="%s">%s</a>\
            </div>' % (active_menu, self.unmp_menu_link[menu_link_i], self.unmp_menu_name[menu_link_i])
            # page header 1 and Menu
        self.req.write('\
    <div id="page_header">\
    	<div id=\"logo\"><a href=\"%s\" target=\"main\">%s</a></div>\
        <div id="icons_div">\
            <div id=\"tactical_view\"></div>\
            %s\
        </div>\
    </div>' % (company["website"], company["name"], menu))

        self.req.write('\
    <div id="header2">\
        %s\
        <div id=\"header2_div\" style=\"display:none;\">\
            <div></div>\
            <div class="header-icon">\
                <img src="images/new_icons/alarm.png" class=\"n-tip-image\" original-title="Alarm" width="32">\
            </div>\
            <div class="header-icon">\
                <img src="images/new_icons/doc_new.png" class=\"n-tip-image\" style=\"width:16px;margin:8px;\" original-title="Favourite" width="32">\
            </div>\
            <div class="header-icon">\
                <img src="images/new_icons/bell.png" class=\"n-tip-image\" style=\"width:16px;margin:8px;\" original-title="Alerts/Notifications">\
            </div>\
            <div class="header-icon">\
                <img src="images/%s/wrench.png" class=\"n-tip-image\" style=\"width:16px;margin:8px;\" original-title="User Settings">\
            </div>\
        </div>\
        <div id="login_user">%s</div>\
    </div><div id="user_options"><a href="user_settings.py">Settings</a><a id="logout" href="#">Logout</a></div>\
    <div class=\"sub-sub-menu\" style=\"right:auto;\" id=\"ubr_sub_menu\"><a href=\"manage_crc_phy_report.py\">CRC-PHY Error</a><a href=\"manage_rssi_report.py\">RSSI</a><a href=\"manage_network_usage_report.py\">Network Usage</a></div>\
    <div class=\"sub-sub-menu\" style=\"right:auto;\" id=\"ubre_sub_menu\"><a href=\"ubre_manage_crc_phy_report.py\">CRC-PHY Error</a><a href=\"ubre_manage_rssi_report.py\">RSSI</a><a href=\"ubre_manage_network_usage_report.py\">Network Usage</a></div>\
    <div class=\"sub-sub-menu\" style=\"right:auto;\" id=\"idu_sub_menu\"><a href=\"#\">TDMO IP</a><a href=\"#\">Port Statistic</a><a href=\"#\">Network Usage</a></div>\
' % (sub_menu, theme, login_text)
        )

        self.req.write('\
	<div id="header3">\
		<div id="header3_text">%s</div>\
		<div class="header-icon">\
			<img class=\"n-tip-image\" src="images/%s/info.png" id=\"page_tip\" name=\"page_tip\" style=\"width:16px;height:16px;margin:6px 20px 6px 10px;\" original-title="Page Tip">\
		</div>\
		%s\
	</div>\
        ' % (title, theme, image_btn))
        self.req.write('\
	<div id=\"container\">\
		<div id=\"container_nav\">')
        create_side_bar(self.req, snapin_list, selected_link)
        #  <div id=\"dashboard_submenu\" rel=\"main\">\
        #      <ul>\
        #          <li><a href=\"localhost_dashboard.py\">UNMP System</a></li>\
        #		  <li><a href=\"odu100_common_dashboard.py?device_type=odu100\">UBRe Dashboard</a></li>\
        #		  <li><a href=\"odu_dashboard.py?device_type=odu16\">UBR Dashboard</a></li>\
        #	      </ul>\
        #	  </div>\
        #	  <div id=\"inventory_submenu\" rel=\"manage_host\">\
        #	      <ul>\
        #		<li><a href=\"manage_host.py\">Hosts</a></li>\
        #		<li><a  href=\"manage_hostgroup.py\">Host Groups</a></li>\
        #		<li><a  href=\"discovery.py\">Discovery</a></li>\
        #		<li><a  href=\"manage_service.py\">Services</a></li>\
        #	     </ul>\
        #	  </div>\
        #	  <div id=\"events_submenu\" rel=\"status_snmptt\">\
        #	      <ul>\
        #		<li><a href=\"\">Alarm list</a></li>\
        #		<li><a  href=\"\">Alarm masking</a></li>\
        #	      </ul>\
        #	  </div>\
        #	  <div id=\"reports_submenu\" rel=\"main_report\">\
        #		<ul>\
        #		  <li><a href=\"main_report.py\">General</a></li>\
        #		  <li><a href=\"inventory_report.py\">Inventory</a></li>\
        #		  <li><a href=\"manage_trap_report.py\">Trap</a></li>\
        #		   <li><a href=\"main_report.py?device_type_user_selected_id=ap25&device_type_user_selected_name=AP25\">AP</a></li>\
        #		  <li><a href=\"main_report.py?device_type_user_selected_id=idu4&device_type_user_selected_name=IDU4PORT\">IDU</a></li>\
        #		  <li><a href=\"main_report.py?device_type_user_selected_id=odu16&device_type_user_selected_name=UBR\">UBR</a></li>\
        #		  <li><a href=\"main_report.py?device_type_user_selected_id=odu100&device_type_user_selected_name=UBRe\">UBRE</a></li>\
        #		</ul>\
        #	  </div>\
        #	  <div id=\"devices_submenu\" rel=\"idu_listing\">\
        #		<ul>\
        #		  <li><a href=\"ap_listing.py?device_type=ap25&device_list_state=enabled&selected_device_type=''\">AP</a></li>\
        #		  <li><a href=\"idu_listing.py?device_type=idu4,idu8&device_list_state=enabled&selected_device_type=''\">IDU</a></li>\
        #		  <li><a href=\"odu_listing.py?device_type=ODU16,odu100,ODU16S&device_list_state=enabled&selected_device_type=''\">UBR/UBRE</a></li>\
        #		</ul>\
        #	  </div>\
        #	  <div id=\"user_submenu\" rel=\"manage_user\">\
        #	      <ul>\
        #		<li><a href="manage_login.py">Manage Login</a></li>\
        #		<li><a href="manage_user.py">Manage User</a></li>\
        #		<li><a href="manage_group.py">Manage Group</a></li>\
        #	      </ul>\
        #	  </div>\
        #	  <div id=\"system_submenu\" rel=\"daemons_controller\">\
        #	     <ul>\
        #		<li><a href="daemons_controller.py">Daemon</a></li>\
        #		<li><a href="manage_license.py">License</a></li>\
        #	     </ul>\
        #	  </div>\
        self.req.write('</div>\
	<div id=\"container_body\">\
        ')

    def new_header(self, title='', selected_link='', image_btn='', css_list=[], javascript_list=[], snapin_list=[]):
        """

        @param title:
        @param selected_link:
        @param image_btn:
        @param css_list:
        @param javascript_list:
        @param snapin_list:
        """
        if self.output_format == "html":
            if not self.req.header_sent:
                self.new_html_head(title, css_list, javascript_list)
                self.write("<body>")
                self.req.header_sent = True
                self.new_top_heading(
                    title, selected_link, image_btn, snapin_list)

    def new_sidebar_header(self, title='', css_list=[], javascript_list=[], company_website='', company_name=''):
        """

        @param title:
        @param css_list:
        @param javascript_list:
        @param company_website:
        @param company_name:
        """
        self.new_html_head(title, css_list, javascript_list)
        self.req.write("<body>")
        # spin loading
        self.req.write(
            "<div id=\"main_loading\" class=\"main_loading\"></div><div class=\"spin-loading\" id=\"spin_loading\"></div>")
        logo = '<div id="logo"><a target="main" href="main.py">codescape</a></div>'
        if company_website != '' and company_name != '':
            logo = '<div id="logo"><a target="main" href="%s">%s</a></div>' % (
                company_website, company_name)
        if theme == "red":
            self.req.write('<div id="page_header">%s</div>' % logo)
            self.req.write('<div id="header2"></div>')

    def new_bottom_footer(self):
        """


        """
        self.req.write('</div>\n')
        self.req.write('</div>\n')
        self.req.write('\
        <div id="events_logs_box" style="display: none;">\
            <div id="header">\
                <a class="head-link head-link-active" href="#" id="user_log_a"   onclick="toggle_log_data(1);" >User Log</a>\
                <a class="head-link"		      href="#" id="alarm_log_a"	 onclick="toggle_log_data(2);" >Alarm Log</a>\
                <a style="display:none;" class="head-link" href="#">System Log</a>\
                <a style="display:none;" class="head-link" href="#">Traps</a>\
                <div class="header-icon">\
                    <img id="close_events_logs_box" src="images/{0}/error.png" class=\"s-tip-image\" style=\"width:16px;margin:6px 8px;\" original-title="Close"/>\
                </div>\
            </div>\
		    <div id="body">\
			    <form id="get_current_log_data_form" name="get_current_log_data_form" action="get_current_log_data.py" method="GET">\
			    <div id="log_user" style="z-index:100000;min-height:200px;"></div>\
			    </form>\
		    </div>\
       	    </div>\
        '.format(theme))
        self.req.write('<div id=\"footer\">\
            <div id=\"version_no\" style=\"float:left;margin:10px;color:#FFF;\">%s</div>\
            <div id=\"footer_div\">\
                <div class="footer-icon">\
                    <img id="toggle_events_logs_box" src="images/%s/round_plus.png" class=\"s-tip-image\" style=\"width:16px;margin:6px 8px;\" original-title="Logs"/>\
                </div>\
            </div>\
        </div><div style="clear:both;"></div>' % (about_us["version"], theme))

    def new_body_end(self):
        """


        """
        self.req.write("</body></html>\n")

    def new_footer(self):
        """


        """
        if self.output_format == "html":
            self.new_bottom_footer()
            self.new_body_end()

    def new_sidebar(self, title='', option_list='', css_list=[], javascript_list=[], company_website='',
                    company_name=''):
        """

        @param title:
        @param option_list:
        @param css_list:
        @param javascript_list:
        @param company_website:
        @param company_name:
        """
        self.new_sidebar_header(title, css_list, javascript_list,
                                "http://www.shyamtelecom.com", "SHYAM")
        self.req.write(option_list)
        self.req.write('<div id=\"footer\">\
            <div id=\"footer_div\">\
            </div>\
        </body></html>')

    # End Edit By Yogesh Kumar
    def body_start(self, title=''):
        """

        @param title:
        """
        self.html_head(title)
        self.write("<body class=main>")

    def bottom_focuscode(self):
        """


        """
        if self.focus_object:
            formname, varname = self.focus_object
            obj = formname + "." + varname
            self.req.write("<script language=\"javascript\" type=\"text/javascript\">\n"
                           "<!--\n"
                           "document.%s.focus();\n"
                           "document.%s.select();\n"
                           "// -->\n"
                           "</script>\n" % (obj, obj))

    def bottom_footer(self):
        """


        """
        if self.req.header_sent:
            self.bottom_focuscode()
            corner_text = ""
            if self.browser_reload:
                corner_text += "refresh: %d secs" % self.browser_reload
            self.req.write("<table class=footer><tr>"
                           "<td class=left></td>"
                           "<td class=middle></td>"
                           "<td class=right>%s</td></tr></table>"
                           % (corner_text))

    def body_end(self):
        """


        """
        self.write("</body></html>\n")

    def footer(self):
        """


        """
        if self.output_format == "html":
            self.bottom_footer()
            self.body_end()

    def show_error(self, msg):
        """

        @param msg:
        """
        if self.output_format == "html":
            self.write("<div class=error>%s</div>\n" % msg)
        else:
            self.write("ERROR: ")
            self.write(strip_tags(msg))
            self.write("\n")

    def show_warning(self, msg):
        """

        @param msg:
        """
        if self.output_format == "html":
            self.write("<div class=warning>%s</div>\n" % msg)
        else:
            self.write("WARNING: ")
            self.write(strip_tags(msg))
            self.write("\n")

    def message(self, msg):
        """

        @param msg:
        """
        if self.output_format == "html":
            self.write("<div class=success>%s</div>\n" % msg)
        else:
            self.write("MESSAGE: ")
            self.write(strip_tags(msg))
            self.write("\n")

    def confirm(self, msg):
        """

        @param msg:
        @return:
        """
        if self.var("_do_actions") == "No":
            return # user has pressed "No"
        if not self.has_var("_do_confirm"):
            self.write("<div class=really>%s" % msg)
            self.begin_form("confirm")
            self.hidden_fields(add_action_vars=True)
            self.button("_do_confirm", "Yes!", "really")
            self.button("_do_actions", "No", "")
            self.end_form()
            self.write("</div>")
            return False
        else:
            return self.check_transaction()

    def do_actions(self):
        """


        @return:
        """
        return self.var("_do_actions") not in ["", None, "No"]

    def set_focus(self, varname):
        """

        @param varname:
        """
        self.focus_object = (self.form_name, varname)

    def has_var(self, varname):
        """

        @param varname:
        @return:
        """
        return varname in self.req.vars

    def var(self, varname, deflt=None):
        """

        @param varname:
        @param deflt:
        @return:
        """
        return self.req.vars.get(varname, deflt)

    def multivar(self, varname, deflt=None):
        """

        @param varname:
        @param deflt:
        @return:
        """
        return self.req.multivars.get(varname, deflt)

    def var_utf8(self, varname, deflt=None):
        """

        @param varname:
        @param deflt:
        @return:
        """
        return unicode(self.req.vars.get(varname, deflt), "utf-8")

    def set_var(self, varname, value):
        """

        @param varname:
        @param value:
        """
        self.req.vars[varname] = value

    def del_var(self, varname):
        """

        @param varname:
        """
        del self.req.vars[varname]

    def javascript(self, code):
        """

        @param code:
        """
        self.write("<script language=\"javascript\">\n%s\n</script>\n" % code)

    def reload_sidebar(self):
        """


        """
        self.javascript("parent.frames[0].location.reload();")

    # Get next transaction id for that user
    def current_transid(self, username):
        """

        @param username:
        @return:
        """
        dir = defaults.var_dir + "/web/" + username
        try:
            os.makedirs(dir)
        except:
            pass

        path = dir + "/transid.mk"
        try:
            return int(file(path).read())
        except:
            return 0

    def increase_transid(self, username):
        """

        @param username:
        """
        current = self.current_transid(username)
        config.save_user_file("transid", current + 1)

    # Checks wether the current page is a reload or an original real submit
    def transaction_valid(self):
        """


        @return:
        """
        if not self.var("_transid"):
            return False
        transid = int(self.var("_transid"))
        current = self.current_transid(self.req.session["username"])
        return transid == current or transid == -1

    # called by page functions in order to check, if this was
    # a reload or the original form submission. Increases the
    # transid of the user, if the latter was the case
    def check_transaction(self):
        """


        @return:
        """
        if self.transaction_valid():
            self.increase_transid(self.req.session["username"])
            return True
        else:
            return False

    def register_event(self, name):
        """

        @param name:
        """
        self.events.add(name)

    def has_event(self, name):
        """

        @param name:
        @return:
        """
        return name in self.events

    def play_sound(self, url):
        """

        @param url:
        """
        self.write('<object type="audio/x-wav" data="%s" height="0" width="0">'
                   '<param name="filename" value="%s">'
                   '<param name="autostart" value="true"><param name="playcount" value="1"></object>' % (url, url))
        if config.debug:
            self.write("Booom (%s)" % url)

    def apache_user(self):
        """


        @return:
        """
        return pwd.getpwuid(os.getuid())[0]

    def omd_mode(self):
        # Load mod_python env into regular environment
        """


        @return:
        """
        os.environ.update(self.req.subprocess_env)

        omd_mode = None
        omd_site = None
        if 'OMD_SITE' in os.environ:
            omd_site = os.environ['OMD_SITE']
            omd_mode = 'shared'
            if omd_site == self.apache_user():
                omd_mode = 'own'
        return (omd_mode, omd_site)
