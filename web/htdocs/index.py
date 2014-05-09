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

from mod_python import apache,util,Session
import sys, os, pprint
from lib import *
import livestatus
import defaults, config, htmllib
import unmp_login
import unmp_model
import MySQLdb
from unmp_config import SystemConfig
from datetime import datetime
import cPickle
import __builtin__
__builtin__._ = lambda x: x
# Load page handlers
#import logging
#logging.basicConfig(filename='/omd/daemon/index_unmp.log',format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)
#log = logging.getLogger('Index')
pagehandlers = {}
pagehandlers_dir = defaults.web_dir + "/plugins/pages"
for fn in os.listdir(pagehandlers_dir):
    if fn.endswith(".py"):
        execfile(pagehandlers_dir + "/" + fn)

if defaults.omd_root:
    local_module_path = defaults.omd_root + "/local/share/check_mk/web/htdocs"
    if local_module_path not in sys.path:
        sys.path[0:0] = [ local_module_path, defaults.web_dir + "/htdocs" ]
    local_pagehandlers_dir = defaults.omd_root + "/local/share/check_mk/web/plugins/pages"
    if os.path.exists(local_pagehandlers_dir):
        for fn in os.listdir(local_pagehandlers_dir):
            if fn.endswith(".py"):
                execfile(local_pagehandlers_dir + "/" + fn)


def read_post_vars(req):
    pass
    #form = util.FieldStorage(req)
    #log.info(str('!!!!!!!!!!')+str(form.list.table_dict()))
    #di = {}
    #keys_ = form.keys()
    #for i in keys_:
    #    di[i] = form.get(i,None)
    #log.info(str(' ><><><><><>< ')+str(di))
    #log.info(str(' ><><><><><>< ')+str(dict(form.items())))
    #log.info(str('!!!!!!!!!!')+str(req.header_only))
    #kam ka hailog.info(str('##########')+str(req.headers_in["content-type"]))
    #req_read=req.read()
    #log.info('*****************************')
    #log.info(req_read)
    #if(req_read!=""):
    #    req_list = req_read.split('&')
    #    for i in req_list:
    #        temp_li = i.split("=")
    #        req.vars[temp_li[0]] = temp_li[1]

def read_get_vars(req):
    #def parse_vars(vars):
    #    req.rawvars = util.parse_qs(vars, True)
    #    for (key,values) in req.rawvars.items():
    #        key = htmllib.urldecode(key)
    #        if len(values) >= 1:
    #            req.vars[key] = values[-1]
    #            req.multivars[key] = values

    #req.multivars = {}
    #req.vars = {}
    #if req.args:
    #    parse_vars(req.args)
    #postvars = req.read()
    #if postvars:
    #    parse_vars(postvars)

    req.vars = {}
    req.multivars = {}
    #log.info(str(req.args))
    if req.args:
        req.rawvars = util.parse_qs(req.args, True)
        for (key,values) in req.rawvars.items():
            if len(values) >= 1:
                req.vars[key] = values[-1]
    if req.method.upper() == 'POST':
        read_post_vars(req)




def connect_to_livestatus(html):
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
                html.site_status[sitename] = { "state" : "disabled", "site" : site }
                disabled_sites[sitename] = site
            else:
                html.site_status[sitename] = { "state" : "dead", "site" : site }
                enabled_sites[sitename] = site

        html.live = livestatus.MultiSiteConnection(enabled_sites, disabled_sites)

        # Fetch status of sites by querying the version of Nagios and livestatus
        html.live.set_prepend_site(True)
        for sitename, v1, v2 in html.live.query("GET status\nColumns: livestatus_version program_version"):
            html.site_status[sitename].update({ "state" : "online", "livestatus_version": v1, "program_version" : v2 })
        html.live.set_prepend_site(False)

        # Get exceptions in case of dead sites
        for sitename, deadinfo in html.live.dead_sites().items():
            html.site_status[sitename]["exception"] = deadinfo["exception"]
            shs = deadinfo.get("status_host_state")
            html.site_status[sitename]["status_host_state"] = shs
            statename = { 1:"down", 2:"unreach", 3:"waiting", }.get(shs, "unknown")
            html.site_status[sitename]["state"] = statename

    else:
        html.live = livestatus.SingleSiteConnection("unix:" + defaults.livestatus_unix_socket)
        html.site_status = { '': { "state" : "dead", "site" : config.site('') } }
        v1, v2 = html.live.query_row("GET status\nColumns: livestatus_version program_version")
        html.site_status[''].update({ "state" : "online", "livestatus_version": v1, "program_version" : v2 })

    # If multiadmin is retricted to data user is a nagios contact for,
    # we need to set an AuthUser: header for livestatus
    if not config.may("see_all"):
        html.live.set_auth_user('read',   config.user)
        html.live.set_auth_user('action', config.user)

    # Default auth domain is read. Please set to None to switch off authorization
    html.live.set_auth_domain('read')


def handler(req):
    is_delete = 1
    temp_variable = 0
    ##log.info(" FIRST IN  "+str(req))
    try: 
        sess = Session.FileSession(req) #,fast_cleanup = True)  #  ,verify_cleanup=False)
    except Exception,e:
        pass
        ##log.info(" in except "+str(e)) 

    ##log.info(" in 1 "+str(sess)) 
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

    flag_ajax = 0
    if req.headers_in.get("X-Requested-With","No Ajax")=="No Ajax":
        #user_trail(req.myfile,req.session["username"])        
        flag_ajax = 1

    if not flag_ajax:
        is_delete = delete_sess(req)    #delete_login_sess(req)

    ##log.info("down 1 "+str(sess)+" "+str(req.myfile)) 
    try:

        read_get_vars(req)
        # Prepare output format
        output_format = html.var("output_format", "html")
        html.set_output_format(output_format)
        config.load_config() # load multisite.mk
        if html.var("debug"): # Debug flag may be set via URL
            config.debug = True
        if config.check_user(req.session["username"]) == 0:
            if req.vars.has_key("username") and req.vars.has_key("password"):
                if unmp_login.unmp_login_verify(html)== 0:
                    req.session["username"] = req.vars["username"]
                    req.session.save()
                    if config.check_user(req.session["username"]) == 0:
                        temp_variable = -1
                        raise MKConfigLoginBox("You are not Logged in")
                    else:
                        ##log.info("  ok -1 ")
                        config.user=req.session["username"]
                        if not flag_ajax:
                            check_sess(req)
                else:
                    #raise MKConfigLoginBox("Incorrect login password")
                    pass
            else:
                temp_variable = -2
                raise MKConfigLoginBox("You are not Logged in")
        else:
            config.user=req.session["username"]
            ##log.info("  ok -2 req "+str(req.session))

            if req.session.has_key('role'):
                if req.session['role']=='' and req.myfile != 'unmp_login':
                    ##log.info("  not ok req login")
                    raise MKConfigLoginBox("You are not Logged in")
            if not flag_ajax:
                check_sess(req)
            #if len(req.session) > 2:
            #    check_sess(req)
            #else:
            #    raise MKConfigLoginBox("You are not Logged in")               

        config.login(req.session["username"])
        req.session["role"] = config.role
        # Set all permissions, read site config, and similar stuff
        # User allowed to login at all?
        if not config.may("use"):
            reason = "Not Authorized.  You are logged in as <b>%s</b>. Your role is <b>%s</b>:" % (config.user, config.role)
            reason += "If you think this is an error, " \
                "please ask your administrator to add your login into multisite.mk"
            raise MKAuthException(reason)

        # General access allowed. Now connect to livestatus
        #connect_to_livestatus(html)
        try:
            connect_to_livestatus(html)
        except Exception,e:
            if(req.myfile=="server_time"):
                req.write('{"nagios":"stop"}\n')
                
        if(req.myfile=="manage_host" or req.myfile=="manage_hostgroup" or req.myfile=="manage_login" or req.myfile=="manage_role" or req.myfile=="discovery" or req.myfile=="manage_service" or req.myfile=="manage_user" or req.myfile=="manage_group" or req.myfile=="group_to_hg_view" or req.myfile=="hostgroup_group_view" or req.myfile=="default_data_delete" or req.myfile=="firmware_listing"or req.myfile=="daemons_controller"):
            if(req.session["role"]=="guest"):
                reason="you dont have permission to view this page"
                raise MKAuthException(reason)
        if(req.myfile=="manage_user" or req.myfile=="manage_group" or req.myfile=="manage_role" ):
            if(req.session["role"]=="user"):
                reason="you dont have permission to view this page"
                raise MKAuthException(reason)

        if(req.myfile=="license_upload" or req.myfile == "manage_license" or req.myfile == "unmp_login" or req.myfile == "unmp_logout" or req.myfile == "tactical_overview"):
            pass
        else:
            if not flag_ajax:
                li_value = is_license_valid()
                if li_value == 0:
                    pass
                else:                 
                    req.myfile = "manage_license"

        if is_delete == 0:
            req.myfile = 'unmp_logout'
            
        time1=datetime.now()

        if is_delete == 0:
            req.myfile = 'unmp_logout'
        handler = pagehandlers.get(req.myfile, page_not_found)
        
        ##log.info(" handler is : "+str(req.myfile))
        handler(html)
        user_trail(req.myfile,req.session["username"],flag_ajax,time1,datetime.now())   

    except MKConfigLoginBox, e:
        ##log.info(" login exception "+str(temp_variable)+" "+str(req.myfile))
        temp_variable = 1
        #sess.invalidate()
        handler = pagehandlers.get('login', page_not_found) # first check 'login' is function or not
        handler(html)
        #unmp_login.login(html)

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
        html.show_error("The following query produced no output:\n<pre>\n%s</pre>\n" % \
                        e.query)
        html.new_footer()

    except livestatus.MKLivestatusException, e:
        temp_variable = 7
        #html.new_header("Livestatus problem")
        #html.show_error("Livestatus problem: %s" % e)
        #html.new_header("Please Wait....")
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
        html.new_header("Internal Error")
        url = html.makeuri([("debug", "1")])
        html.show_error("Internal error: %s (<a href=\"%s\">Retry with debug mode</a>)" % (e, url))
        html.new_footer()
        apache.log_error("Internal error: %s" % (e,), apache.APLOG_ERR)
    finally:
        # Disconnect from livestatus!
        ##log.info(" in finally "+str(temp_variable))
        ##log.info(" ============================================================================= \n")
        html.live = None
        return apache.OK

def page_not_found(html):
    html.new_header("Page doesn't Exist")
    html.show_error("The page you were looking for could not be found.")
    html.new_footer()

def check_sess(req):
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        ##log.info("checksess")
        username=req.session["username"]
        query="select session_id from login_info where user_name='%s' and is_logged_in=1" %(username)  
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)!=0: 
            ssid=res[0][0]
        else :
            ssid="0"
        cur_ssid=req.session.id()
        if(cur_ssid!=ssid and ssid!="0"):
            try:
                ##log.info("checksess iner ssid: "+str(ssid)+" cur "+cur_ssid)
                path = os.path.join("/tmp/mp_sess", ssid[0:2])
                filename = os.path.join(path,ssid)
                if os.path.isfile(filename):
                #fp = file(filename,'rb')
                #data = cPickle.load(fp)
                #fp.close()
                    ##log.info("yaha tak aya checksess "+str(filename))
                    sess2 = Session.FileSession(req,ssid)  #,fast_cleanup = True)  # ,verify_cleanup=False)                   # get session object  
                    ##log.info(" sess2 pe bhi aya check_sees"+str(sess2))
                    if(sess2!=None):
                        ##log.critical("check sessdeleting "+str(sess2))
                        #pass
                        #sess2.invalidate()
                        sess2.cleanup()
                        sess2.delete()
            except Exception , e:
                ##log.error("config "+str(e))
            # session doesn't exists
                pass

    except Exception , e:
        pass
    finally:
        db.close()

def delete_login_sess(req):
    try:
        ##log.info("delete")
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        query="select session_id,user_name from login_info where next_time_delete=1 limit 1"   
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)!=0: 
            ssid=res[0][0]
        else :
            return 1
        #query="insert into login_check values('%s')" %(ssid)
        #cursor.execute(query)
        #db.commit()
        if(req.session["username"]!=res[0][1]):
            try:
                path = os.path.join("/tmp/mp_sess", ssid[0:2])
                filename = os.path.join(path,ssid)
                if os.path.isfile(filename):
                    #fp = file(filename,'rb')
                    #data = cPickle.load(fp)
                    #fp.close()
                    sess2 = Session.FileSession(req,ssid)  #,fast_cleanup = True)    # ,verify_cleanup=False)                   # get session object  
                    if(sess2!=None): 
                        ##log.info("deleting")
                        #sess2.invalidate()
                        sess2.cleanup()
                        sess2.delete()
                    #query="insert into login_check values('session deleted')" 
                    #cursor.execute(query)
                    #db.commit()
                        query="update login_info set is_logged_in='0' where user_name='%s'" %(res[0][1])
                        cursor.execute(query)
                        db.commit()
                        query="update login_info set next_time_delete=0 where session_id='%s'" %(ssid)
                        cursor.execute(query)
                        db.commit()

            except Exception , e:
                pass
                ##log.error(str(e))
            # session doesn't exists
                #query="insert into login_check values('%s')" %(str(e))
                #cursor.execute(query)
                #db.commit()
                return 2

    except Exception , e:
        return 3
    finally:
        db.close()

def delete_sess(req):
    try:
        ##log.info("delete")
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        query="select next_time_delete from login_info where user_name = '%s'"%(req.session["username"])   
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)!=0: 
            if res[0][0]:
                up_query="update login_info set next_time_delete = 0 where user_name = '%s'"%(req.session["username"])
                cursor.execute(up_query)   
                db.commit() 
                return 0
            else:
                return 1           
        else :
            return 1
    except Exception , e:
        return 3
    finally:
        cursor.close()
        db.close()


def is_license_valid():
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        query="select is_valid from license_info"  
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)!=0: 
            value=res[0][0]
            if value == 0:
                return 0
            else:
                return 1
        else:
            return 1

    except Exception , e:
        return 1
    finally:
        db.close()		
        

        
def user_trail(link, username,flag_ajax=0,time1=0,time2=0):
    val=0
    time_taken = str((time2-time1).seconds)+"."+str((time2-time1).microseconds)
    import datetime
    try:
        file_path="/omd/daemon/configuration_file.unmp"
        if not os.path.isfile(file_path):
            return 0
        file_obj=open(file_path,"r")
        lines=file_obj.readlines()
        file_obj.close()
        for line in lines:
            line=line.strip()
            if line=="" or line.startswith("#"):
                continue
            li=line.split('=')
            if li[0].strip()=="set_user_trail":
                val=li[1].strip()
                break
        if str(val)=="1":
            db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
            cursor = db.cursor()
            query="INSERT INTO `event_log` (`event_log_id`, `username`, `event_type_id`, `description`, `timestamp`,`level`,`time_taken`) VALUES \
            (NULL,\"%s\",NULL,\"%s\",\"%s\",\"%s\",\"%s\")" %(username, "visited link %s.py %s"%(link,"" if flag_ajax==1 else "(AJAX Request)"),datetime.datetime.now(),3,time_taken)
            cursor.execute(query)
            db.commit()
            db.close()
        return 0
    except Exception,e:
        return 2
