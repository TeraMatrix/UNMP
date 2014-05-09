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

from datetime import datetime
import MySQLdb
import __builtin__
import defaults
import config
import htmllib
from lib import *
import livestatus
from mod_python import apache, util, Session
import sys
import os
from unmp_config import SystemConfig
import unmp_login
from accessdict import page_access_rights
from common_bll import DB
from common_controller import logme

__builtin__._ = lambda x: x


# @TODO: try to initiate DB in handler
#        handle error with try catch
#        create db connection failed page
db_obj = DB()

TIMEOUT = 5 * 60  # in secs
GRACE_PERIOD = 60  # secs

DEBUG = True
# DEBUG = False
if DEBUG:
    import cgitb
    # cgitb.enable()


pagehandlers = {}
pagehandlers_dir = defaults.web_dir + "/plugins/pages"
for fn in os.listdir(pagehandlers_dir):
    if fn.endswith(".py"):
        execfile(pagehandlers_dir + "/" + fn)

if defaults.omd_root:
    local_module_path = defaults.omd_root + "/local/share/check_mk/web/htdocs"
    if local_module_path not in sys.path:
        sys.path[0:0] = [local_module_path, defaults.web_dir + "/htdocs"]
    local_pagehandlers_dir = defaults.omd_root + \
                             "/local/share/check_mk/web/plugins/pages"
    if os.path.exists(local_pagehandlers_dir):
        for fn in os.listdir(local_pagehandlers_dir):
            if fn.endswith(".py"):
                execfile(local_pagehandlers_dir + "/" + fn)
"""
check the user restriction with userRestrictPages
check the guest restriction with guestRestrictPages / functions
skip the pages / functions for a perticular role


userRestrictPages = [
                        "manage_user",
                        "manage_group",
                        "manage_role"
                    ]
guestRestrictPages = [
                        "manage_host",
                        "manage_hostgroup" ,
                        "manage_login" ,
                        "manage_role" ,
                        "discovery" ,
                        "manage_service" ,
                        "manage_user" ,
                        "manage_group" ,
                        "group_to_hg_view" ,
                        "hostgroup_group_view" ,
                        "default_data_delete" ,
                        "firmware_listing",
                        "daemons_controller"
                    ]
adminRestrictPages = []

li = pagehandlers.keys()
di = {}
for i in li:
    if i in guestRestrictPages:
        di[i] = ['admin','user']
    elif i in userRestrictPages:
        di[i] = ['admin']
    else:
        di[i] = ['admin', 'user', 'guest']

logme("-------------\n")
logme("\n\n      di ="+str(di))
logme("-------------\n")
"""


def read_post_vars(req):
    """

    @param req:
    """
    pass


def read_get_vars(req):

    """

    @param req:
    """
    req.vars = {}
    req.multivars = {}
    if req.args:
        req.rawvars = util.parse_qs(req.args, True)
        for (key, values) in req.rawvars.items():
            if len(values) >= 1:
                req.vars[key] = values[-1]


def connect_to_livestatus(html):
    """

    @param html:
    """
    html.site_status = {}
    # site_status keeps a dictionary for each site with the following
    # keys:
    # "state"              --> "online", "disabled", "down", "unreach", "dead" or "waiting"
    # "exception"          --> An error exception in case of down, unreach, dead or waiting
    # "status_host_state"  --> host state of status host (0, 1, 2 or None)
    # "livestatus_version" --> Version of sites livestatus if "online"
    # "program_version"    --> Version of Nagios if "online"

    # If there is only one site (non-multisite), than
    # user cannot enable/disable.
    if config.is_multisite():
        # do not contact those sites the user has disabled.
        # Also honor HTML-variables for switching off sites
        # right now. This is generally done by the variable
        # _site_switch=sitename1:on,sitename2:off,...
        switch_var = html.var("_site_switch")
        if switch_var:
            for info in switch_var.split(","):
                sitename, onoff = info.split(":")
                d = config.user_siteconf.get(sitename, {})
                if onoff == "on":
                    d["disabled"] = False
                else:
                    d["disabled"] = True
                config.user_siteconf[sitename] = d
            config.save_site_config()

        # Make lists of enabled and disabled sites
        enabled_sites = {}
        disabled_sites = {}

        for sitename, site in config.allsites().items():
            siteconf = config.user_siteconf.get(sitename, {})
            if siteconf.get("disabled", False):
                html.site_status[sitename] = {"state":
                                                  "disabled", "site": site}
                disabled_sites[sitename] = site
            else:
                html.site_status[sitename] = {"state": "dead", "site": site}
                enabled_sites[sitename] = site

        html.live = livestatus.MultiSiteConnection(
            enabled_sites, disabled_sites)

        # Fetch status of sites by querying the version of Nagios and
        # livestatus
        html.live.set_prepend_site(True)
        for sitename, v1, v2 in html.live.query("GET status\nColumns: livestatus_version program_version"):
            html.site_status[sitename].update(
                {"state": "online", "livestatus_version": v1, "program_version": v2})
        html.live.set_prepend_site(False)

        # Get exceptions in case of dead sites
        for sitename, deadinfo in html.live.dead_sites().items():
            html.site_status[sitename]["exception"] = deadinfo["exception"]
            shs = deadinfo.get("status_host_state")
            html.site_status[sitename]["status_host_state"] = shs
            statename = {1: "down", 2: "unreach", 3: "waiting",
            }.get(shs, "unknown")
            html.site_status[sitename]["state"] = statename

    else:
        html.live = livestatus.SingleSiteConnection(
            "unix:" + defaults.livestatus_unix_socket)
        html.site_status = {'': {"state": "dead", "site": config.site('')}}
        v1, v2 = html.live.query_row(
            "GET status\nColumns: livestatus_version program_version")
        html.site_status[''].update({"state": "online", "livestatus_version":
            v1, "program_version": v2})

    # If multiadmin is retricted to data user is a nagios contact for,
    # we need to set an AuthUser: header for livestatus
    if not config.may("see_all"):
        html.live.set_auth_user('read', config.user)
        html.live.set_auth_user('action', config.user)

    # Default auth domain is read. Please set to None to switch off
    # authorization
    html.live.set_auth_domain('read')


def logout_update(username):
    """
    NOT IN USE
    created this function to use as a call back
    with apache when a req session cleanup
    ::
    For this to work you should a modified session.py in mod_python
    ::
    how to use :
    in handler() when creating session from request
    do like this
    req.cleanup_func = logout_update
    sess = Session.FileSession(
            req)  # ,fast_cleanup = True)  #  ,verify_cleanup=False)

    @param username:
    """
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()

        query = " UPDATE `login_info` \
                SET `is_logged_in` = 0 \
                WHERE `user_name` = '%s'" % (
            username)

        cursor.execute(query)
        #db.commit()
        cursor.close()
        db.close()
    except Exception, e:
        logme(" exception logout_update ", str(e))
    finally:
        pass
        # html.req.session.delete()


def handler(req, profiling=False):
    """

    @param req:
    @param profiling:
    @return: @raise:
    """
    is_delete = 1
    is_first_login = 0
    temp_variable = 0
    try:
        sess = Session.FileSession(
            req)  # ,fast_cleanup = True)  #  ,verify_cleanup=False)

    except Exception, e:
        pass

    sess.set_timeout(604800)        # set timeout for 7 days

    if sess.is_new():
        sess["username"] = ""
        sess["role"] = ""
    req.session = sess
    if sess.is_new():
        req.session.save()

    req.content_type = "text/html; charset=UTF-8"
    req.new_header_sent = False
    # All URIs end in .py. We strip away the .py and get the
    # name of the page.
    req.myfile = req.uri.split("/")[-1][:-3]
    # Create an object that contains all data about the request and
    # helper functions for creating valid HTML. Parse URI and
    # store results in the request object for later usage.
    html = htmllib.html(req)
    req.uriinfo = htmllib.uriinfo(req)

    try:
        if profiling:
            read_get_vars(req)
        else:
            """
            This handler is actually an alias to two different handlers.
            When specified in the main config file outside any directory tags,
            it is an alias to PostReadRequestHandler.
            When specified inside directory (where PostReadRequestHandler is not allowed),
            it aliases to PythonHeaderParserHandler.
            """
            read_get_vars(req)

        internal_debug = False
        if html.var('another_debug') and DEBUG:
            internal_debug = True

        not_ajax = 0
        if req.headers_in.get("X-Requested-With", "No Ajax") == "No Ajax":
            # user_trail(req.myfile,req.session["username"])
            not_ajax = 1

        if not_ajax and req.session["username"]:
            check_all_timeouts(req.session["username"])

        if req.myfile == 'server_time' and req.session["username"]:
            check_for_timeout(int(html.var("idle_time")), req.session["username"])

        if req.session["username"]:
            is_delete, is_first_login = delete_sess(req.session["username"])  # delete_login_sess(req)

        # Prepare output format
        output_format = html.var("output_format", "html")
        html.set_output_format(output_format)
        config.load_config()  # load multisite.mk

        if html.var("debug"):  # Debug flag may be set via URL
            config.debug = True

        if DEBUG and profiling:
            import cProfile  # , pstats, sys, StringIO, tempfile
            # the profiler looses the memory about all modules. We need to park
            # the request object in the apache module. This seems to be persistent.
            # Ubuntu: install python-profiler when using this feature
            apache._profiling_req = req
            profilefile = defaults.var_dir + "/web/multisite.profile"
            retcode = cProfile.run(
                "import index; from mod_python import apache; index.handler(apache._profiling_req, False)", profilefile)
            file(profilefile + ".py", "w").write(
                "#!/usr/bin/python\nimport pstats\nstats = pstats.Stats(%r)\nstats.sort_stats('time').print_stats()\n" % profilefile)
            os.chmod(profilefile + ".py", 0755)
            return apache.OK

        if config.check_user(req.session["username"]) == 0:
            #@TODO: do this when method is post for very req
            # the one that include file type object in req
            # should not used util.FieldStorage first
            if req.myfile == 'unmp_login':
                form = util.FieldStorage(html.req)
                html.html_var = form.list.table_dict()
            else:
                html.html_var = {}
            if "username" in html.html_var and "password" in html.html_var:
                if unmp_login.unmp_login_verify(html.html_var["username"], html.html_var["password"]) == 0:
                    req.session["username"] = html.html_var["username"]
                    req.session.save()
                    if config.check_user(req.session["username"]) == 0:
                        temp_variable = -1
                        raise MKConfigLoginBox("You are not Logged in")
                    else:
                        config.user = req.session["username"]
                        check_sess(req)
                else:
                    # raise MKConfigLoginBox("Incorrect login password")
                    pass
            else:
                temp_variable = -2
                raise MKConfigLoginBox("You are not Logged in")
        else:
            if req.myfile == 'unmp_login':
                form = util.FieldStorage(html.req)
                html.html_var = form.list.table_dict()
            config.user = req.session["username"]

            if 'role' in req.session:
                if req.session['role'] == '' and req.myfile != 'unmp_login':
                    raise MKConfigLoginBox("You are not Logged in")
            check_sess(req)
            # if len(req.session) > 2:
            #    check_sess(req)
            # else:
            #    raise MKConfigLoginBox("You are not Logged in")

        config.login(req.session["username"])
        req.session["role"] = config.role
        # Set all permissions, read site config, and similar stuff
        # User allowed to login at all?
        if not config.may("use"):
            reason = "Not Authorized.  You are logged in as <b>%s</b>. " \
                     "Your role is <b>%s</b>:" % (
                         config.user, config.role)
            reason += "If you think this is an error, " \
                      "please ask your administrator to add your login into multisite.mk"
            raise MKAuthException(reason)

        # General access allowed. Now connect to livestatus
        # connect_to_livestatus(html)
        try:
            connect_to_livestatus(html)
        except Exception, e:
            if (req.myfile == "server_time"):
                req.write('{"nagios":"stop"}\n')

        if (req.session["role"] not in page_access_rights(req.myfile)):
            # check the user permission on the pages/function
            # and then grant access if not restricted

            reason = "you dont have permission to view this page"
            raise MKAuthException(reason)

        passReqs = [
            "license_upload",
            "manage_license",
            "unmp_login",
            "unmp_logout",
            "tactical_overview"
        ]

        # param:: skipReqs -

        if (req.myfile in passReqs):
            pass
        else:
            if not_ajax:
                li_value = is_license_valid()
                if li_value == 0:
                    pass
                else:
                    req.myfile = "manage_license"

        # added code to redirect change password screen{
        passReqs = [
            "unmp_logout",
            "save_user_settings_password",
            "check_password",
            "unmp_login",
            "login",
            "help_change_password",
            "server_time",
        ]
        # param:: passReqs- skip the check for first login/
        #         or Password expired of users on these page lists

        # @TODO: should be called when req.myfile is unmp_login
        sess_username = req.session["username"]
        is_password_expired = is_passwd_expired(sess_username)
        if (is_first_login or is_password_expired) and (req.myfile not in passReqs):
            html.req.vars.update({"is_first_login": is_first_login})
            html.req.vars.update({"is_password_expired": is_password_expired})
            if req.myfile != "index":
                # If the request is for index.py file, skip this section and load index.py
                req.myfile = "user_settings"
            # }End added

        time1 = datetime.now()

        if is_delete == 0:
            req.myfile = 'unmp_logout'

        # closed db connection as handler passing req to the perticular function now
        # and ther is no need for db connection in index file
        db_obj.close()

        handler = pagehandlers.get(req.myfile, page_not_found)

        handler(html)
        user_trail(req.myfile, sess_username, not_ajax,
                   time1, datetime.now())

    except MKConfigLoginBox, e:
        temp_variable = 1
        # sess.invalidate()
        handler = pagehandlers.get(
            'login', page_not_found)  # first check 'login' is function or not
        handler(html)
        # unmp_login.login(html)

    except MKLoggedOut, e:
        handler = pagehandlers.get(
            'unmp_logout', page_not_found)
        handler(html)
        handler = pagehandlers.get(
            'login', page_not_found)  # first check 'login' is function or not
        handler(html)

    except MKUserError, e:
        temp_variable = 2
        html.new_header("Invalid User Input")
        html.show_error(str(e))
        html.new_footer()

    except MKAuthException, e:
        temp_variable = 3
        html.new_header("Permission denied")
        html.show_error(str(e))
        html.new_footer()

    except MKConfigError, e:
        temp_variable = 4
        html.new_header("Configuration Error")
        html.show_error(str(e))
        html.new_footer()
        apache.log_error("Configuration error: %s" % (e,), apache.APLOG_ERR)

    except MKGeneralException, e:
        temp_variable = 5
        html.new_header("Error")
        html.show_error(str(e))
        html.new_footer()
        apache.log_error("Error: %s" % (e,), apache.APLOG_ERR)

    except livestatus.MKLivestatusNotFoundError, e:
        temp_variable = 6
        html.new_header("Data not found")
        html.show_error("The following query produced no output:\n<pre>\n%s</pre>\n" %
                        e.query)
        html.new_footer()

    except livestatus.MKLivestatusException, e:
        temp_variable = 7
        # html.new_header("Livestatus problem")
        # html.show_error("Livestatus problem: %s" % e)
        # html.new_header("Please Wait....")
        html.write("Please Wait....")
        html.write("""<script>
setTimeout('location.reload(true)',3000);
</script>""")
        html.new_footer()

    except Exception, e:
        temp_variable = 8
        if config.debug:
            html.live = None
            raise
            # html.new_header("Internal Error")
        if internal_debug:
            html.show_error("Internal error: %s (<div>%s</div>)" %
                            (e, cgitb.html(sys.exc_info(), context=10)))
            # apache.log_error("DEBUG_INTERNAL_ERROR: %s" %
            # (cgitb.text(sys.exc_info(), context=10)), apache.APLOG_ERR)
        elif DEBUG:
            url = html.makeuri([("another_debug", "1")])
            html.show_error(
                "Internal error: %s (<a href=\"%s\" target=\"_blank\">Click to open traceback in new window </a>)" % (
                e, url))
            if not_ajax:
                html.new_footer()
        else:
            html.show_error("Internal error: %s " % (e))
            if not_ajax:
                html.new_footer()

        apache.log_error("Internal error: %s" % (e,), apache.APLOG_ERR)
    finally:
        # Disconnect from livestatus!
        # =============================================================================
        # \n")
        db_obj.close()
        html.live = None
        return apache.OK


def page_not_found(html):
    """

    @param html:
    """
    html.new_header("Page doesn't Exist")
    html.show_error("The page you were looking for could not be found.")
    html.new_footer()


def is_passwd_expired(username):
    """ Check if PASSWORD EXPIRED
        --------------------------
    returns True on PASSWORD EXPIRED and
    auto genrated password service is NOT enabled,
    else returns False

    Password Expiry options are configurable in XML file
    @param username:
    """
    enable, expiry_age, warning_time, auto_password = \
        SystemConfig.get_pwd_expiry_details()
    if ( enable and not auto_password):
        try:# calculate password age
            db_obj.ready()
            query = "SELECT DATEDIFF(CURDATE(), `change_password_date` ) \
                     FROM  `user_login` \
                     WHERE `user_name` = '%s'" % (username)
            rows, res = db_obj.execute(query)
            if (rows > 0) and (int(res[0][0]) >= expiry_age):
                return True
        except Exception, e:
            return False
        finally:
            db_obj.done()
    return False


def check_sess(req):
    """

    @param req:
    """
    try:
        db_obj.ready()
        username = req.session["username"]
        query = "select session_id from login_info where user_name='%s' and is_logged_in=1" % (
            username)
        rows, query_result = db_obj.execute(query)
        if len(query_result) != 0:
            ssid = query_result[0][0]
        else:
            ssid = "0"
        cur_ssid = req.session.id()
        if (cur_ssid != ssid and ssid != "0"):
            try:
                path = os.path.join("/tmp/mp_sess", ssid[0:2])
                filename = os.path.join(path, ssid)
                if os.path.isfile(filename):
                    sess2 = Session.FileSession(
                        req,
                        ssid)  # ,fast_cleanup = True)  # ,verify_cleanup=False)                   # get session object
                    if (sess2 is not None):
                        # sess2.invalidate()
                        sess2.cleanup()
                        sess2.delete()
            except Exception:
                import traceback
                logme(" Exception first checkssess ", traceback.format_exc())

    except Exception:
        import traceback
        logme(" exception second checkssess ", traceback.format_exc())
    finally:
        db_obj.done()


def delete_login_sess(req):
    """

    @param req:
    @return:
    """
    try:
        db_obj.ready()
        query = "select session_id,user_name from login_info where next_time_delete=1 limit 1"
        rows, query_result = db_obj.execute(query)
        if len(query_result) != 0:
            ssid = query_result[0][0]
        else:
            return 1
        if (req.session["username"] != query_result[0][1]):
            try:
                path = os.path.join("/tmp/mp_sess", ssid[0:2])
                filename = os.path.join(path, ssid)
                if os.path.isfile(filename):
                    sess2 = Session.FileSession(
                        req,
                        ssid)  # ,fast_cleanup = True)    # ,verify_cleanup=False)                   # get session object
                    if (sess2 is not None):
                        # sess2.invalidate()
                        sess2.cleanup()
                        sess2.delete()
                        query = "update login_info set is_logged_in='0' where user_name='%s'" % (
                            query_result[0][1])
                        db_obj.execute_dui(query)
                        query = "update login_info set next_time_delete=0 where session_id='%s'" % (ssid)
                        db_obj.execute_dui(query)

            except Exception:
                return 2

    except Exception:
        return 3
    finally:
        db_obj.done()


def delete_sess(username):
    """

    @param username:
    @return: @raise:
    """
    try:
        # db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        # cursor = db.cursor()
        db_obj.ready()
        query = "SELECT `next_time_delete`, `is_first_login` \
        		 FROM `login_info` \
        		 WHERE `user_name` = '%s'" % (
            username)
        rows, query_result = db_obj.execute(query)

        if rows == -1:
            raise db_obj.error

        is_first_login = query_result[0][1]
        if len(query_result) != 0:
            if query_result[0][0]:
                up_query = "UPDATE `login_info` \
                            SET `next_time_delete` = 0 \
                            WHERE `user_name` = '%s'" % (
                    username)
                if db_obj.execute_dui(up_query) == -1:
                    raise db.error
                return (0, is_first_login)
            else:
                return (1, is_first_login)
        else:
            return (1, is_first_login)
    except Exception:
        return (3, 0)
    finally:
        db_obj.done()


def is_license_valid():
    """


    @return:
    """
    try:
        db_obj.ready()
        query = "select is_valid from license_info"
        rows, query_result = db_obj.execute(query)

        if len(query_result) != 0:
            value = query_result[0][0]
            if value == 0:
                return 0
            else:
                return 1
        else:
            return 1

    except Exception:
        return 1
    finally:
        db_obj.done()


def user_trail(link, username, not_ajax=0, time1=0, time2=0):
    """

    @param link:
    @param username:
    @param not_ajax:
    @param time1:
    @param time2:
    @return:
    """
    val = 0
    time_taken = str(
        (time2 - time1).seconds) + "." + str((time2 - time1).microseconds)
    import datetime

    try:
        file_path = "/omd/daemon/configuration_file.unmp"
        if not os.path.isfile(file_path):
            return 0
        file_obj = open(file_path, "r")
        lines = file_obj.readlines()
        file_obj.close()
        for line in lines:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            li = line.split('=')
            if li[0].strip() == "set_user_trail":
                val = li[1].strip()
                break
        if str(val) == "1":
            db_obj.ready()
            query = "INSERT INTO `event_log` (`event_log_id`, `username`, `event_type_id`, `description`, `timestamp`,`level`,`time_taken`) VALUES \
            (NULL,\"%s\",NULL,\"%s\",\"%s\",\"%s\",\"%s\")" % (
            username, "visited link %s.py %s" % (link, "" if not_ajax == 1 else "(AJAX Request)"),
            datetime.datetime.now(), 3, time_taken)

            db_obj.execute_dui(query)
        return 0
    except Exception:
        return 2
    finally:
        db_obj.done()


def check_for_timeout(idle_time, username):
    """

    @param idle_time:
    @param username:
    @raise:
    """
    if idle_time > TIMEOUT:
        raise MKLoggedOut('Session timeout')
    elif idle_time < GRACE_PERIOD:
        try:
            db_obj.ready()
            query = "UPDATE `login_info` \
                    SET `last_accessed_time` = '%s' \
                    WHERE `user_name` = '%s'" % (
                datetime.now(), username)
            db_obj.execute_dui(query)
        finally:
            db_obj.done()


def check_all_timeouts(username):
    """

    @param username:
    @raise:
    """
    raise_logout = False
    try:
        db_obj.ready()
        query = "SELECT last_accessed_time, user_name \
                 FROM `login_info` \
                 WHERE `is_logged_in` = 1"

        rows, query_result = db_obj.execute(query)
        if rows == -1:
            raise db_obj.error

        user_tobe_logout = []
        for tup in query_result:
            if tup[0] and (datetime.now() - tup[0]).seconds > TIMEOUT:
                user_tobe_logout.append(tup[1])
                if username == tup[1]:
                    raise_logout = True

        if user_tobe_logout:
            query = "UPDATE `login_info` \
                SET `is_logged_in` = 0, `next_time_delete` = 1 \
                WHERE `user_name` in (%s) " % str(user_tobe_logout)[1:-1]
            db_obj.execute_dui(query)
    except Exception:
        # Breaking the rule: Errors should never pass silently
        # FIXME
        import traceback
        logme(" Exception check all timeouts ", traceback.format_exc())
    finally:
        db_obj.done()
        if raise_logout:
            raise MKLoggedOut('Session timeout')