#!/usr/bin/python2.6


##################################################################
#
# Author            :   Yogesh Kumar
# Project           :   UNMP
# Version           :   0.1
# File Name         :   example.py
# Creation Date     :   12-September-2011
# Modify Date       :   12-September-2011
# Purpose           :   Example View
# Require           :   Python 2.6 or Higher Version
# Require Library   :   htmllib.py
# Copyright (c) 2011 Codescape Consultant Private Limited
#
# Second Author 	:   Grijesh Chauhan
# Project           :   TCL UNMP
# Version           :   0.2
# Updation date 	:   8-February-2013
# Purpose           :   security  improvement:
#						Password Complexity and Encryption(SHA)
##################################################################

import config
from htmllib import *
import MySQLdb
import pickle
from datetime import datetime
from unmp_config import SystemConfig
from mod_python import Session
import sha
from common_controller import logme
# import logging
# logging.basicConfig(filename='/omd/daemon/index_unmp.log',format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)
# log = logging.getLogger('Login')


def login(h):
    global html
    html = h
    if theme == "blue":
        login_box = '<form  id=\"login_form\" name=\"login_form\" action=\"unmp_login.py\" method=\"get\">\
	    <h1><div id=\"logo\" style=\"position:static;\"><a href=\"#\" target=\"main\"></a></div></h1>\
	    <fieldset id=\"inputs\">\
		<input type=\"text\" required=\"\" autofocus=\"\" placeholder=\"Username\" id=\"username\" name=\"username\">\
		<input type="password" required="" placeholder="Password" id="password" name=\"password\">\
	    </fieldset>\
	    <fieldset id=\"actions\">\
		<input type=\"submit\" value=\"Log in\" id=\"submit\" class="yo-small yo-button" style=\"margin-top:0px\">\
	       </fieldset>\
	  </form>'
        html.new_sidebar_header("Login", [], ["js/login.js"], "#", "Nocout")
        html.write(login_box)
    else:
        login_box = '<div id=\"login_box\">\
	    <h1>Login</h1>\
	    </script>\
	    <form action=\"unmp_login.py\" method=\"post\" id=\"login_form\" name=\"login_form\">\
		<div class=\"form-div\" style=\"min-width:100%;margin-bottom:0px;position:inherit;\">\
		    <div class=\"form-body\" style=\"position:absolute;top:33px;left:0;\">\
		        <div class=\"row-elem\">\
		            <label class=\"lbl\" for=\"username\">Username</label>\
		            <input type=\"text\" id=\"username\" name=\"username\" title=\"Enter Your User Name\" value=\"\" />\
		        </div>\
		        <div class=\"row-elem\">\
		            <label class=\"lbl\" for=\"password\">Password</label>\
		            <input type=\"password\" id=\"password\" name=\"password\" title=\"Enter Your Password\" value=\"\" />\
		        </div>'

    #                <div class=\"row-elem\">\
    #                    <label class=\"lbl\">&nbsp;</label>\
    #                    <input type=\"checkbox\" id=\"remamber_me\" name=\"remamber_me\" />\
    #                    <label class=\"sub-lbl\" for=\"remamber_me\">[Remember Me]</label>\
    #                    <input type=\"hidden\" id=\"check_session\" name=\"check_session\" />\
    #                </div>\
        login_box += '        </div>\
		    <div class=\"form-div-footer\" style=\"background-color:#FFF;position:absolute;bottom:0;\">\
		        <button class="yo-small yo-button" type="submit"><span class="key">Login</span></button>\
		    </div>\
		</div>\
	    </form>\
	    </div>'
        html.new_sidebar_header("Login", [], ["js/login.js"],
                                "http://www.shyamtelecom.com", "SHYAM")
        html.write(login_box)
        html.write('<div id=\"footer\">\
		<div id=\"footer_div\">\
		</div>\
	    </div>')

def license_check(db):
    cursor = db.cursor()
    query = "SELECT `is_valid`, `minutes`, `last_check_date` \
    		 FROM `license_info` "
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) > 0:
        is_valid, minutes, last_check_date = res[0]
        if is_valid == 0:
            curr_date = datetime.now()
            if curr_date > last_check_date:
                dtdelta = curr_date - last_check_date
                mins = divmod(dtdelta.days * 86400 + dtdelta.seconds, 60)
                if mins[0] >= 0:
                    mindelta = minutes - mins[0]
                    if mindelta > 0:
                        query = "UPDATE `license_info` \
                        		 SET `minutes` = '%s', `last_check_date` = '%s' " \
                        		 						% (mindelta,curr_date)
                    else:
                        query = "UPDATE `license_info` \
                        		 SET `is_valid` = '1', `minutes` = '0', \
                        		  `last_check_date` = '%s' " % (curr_date)
                else:
                    query = "UPDATE `license_info` SET `last_check_date` = '%s'" % (
                        curr_date)
            else:
                query = "UPDATE `license_info` SET `last_check_date` = '%s'" % (
                    curr_date)

            cursor.execute(query)
            db.commit()
    cursor.close()

	# Edit start :
	# Redmine Issue: Features
 	# 730: "Password Storage in Encrypted Form"
    # 890: "Notifying User That They Entered Old Password"
 	# Description:
	# Password Authentication in SHA format
	# By: Grijesh Chauhan, Date: 7, Feb 2013, 12, March 2013
def str2bool(v):
    '''
     return bool for string object
    '''
    return v.lower() in ("yes", "true", "t", "1")

def unmp_login(h):
    global html
    html = h
    enable = 0
    expiry_age = 1
    warning_time = 2
    auto_password = 3
    try:
        password_expiry = SystemConfig.get_config_attributes(
                    "password_expiry",
                    ["enable", "expiry_age", "warning_time", "auto_password"],
                    False)[0]
        enable = str2bool(password_expiry[enable])
        auto_password = str2bool(password_expiry[auto_password])
        expiry_age = int(password_expiry[expiry_age])
        warning_time = int(password_expiry[warning_time])

        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        # username = html.var("username")
        # password = html.var("password")
        username = html.html_var.get("username")
        password = html.html_var.get("password")
        pwd = db.escape_string(password)
        query="SELECT `user_name`, \
                      `user_id`, \
                      `password`, \
                      `old_password`, \
                      DATEDIFF(CURDATE(), `change_password_date` ) \
               FROM  `user_login` \
               WHERE `user_name` ='%s' AND ( `password` = SHA('%s') OR \
                                            `old_password` =  SHA('%s') )"\
                                        %  (username, pwd, pwd)
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 1:
            user_id = str(res[0][1])
            sha_pwd = str(res[0][2])
            sha_old_pwd = str(res[0][3])
            pwd_age = int(res[0][4])
            if(sha.sha(password).hexdigest() == sha_pwd):
                query="	SELECT `roles`.`role_name`, `groups`.`group_name` \
    				 	FROM `roles` \
    					  JOIN (	SELECT `group_id`, `role_id`, `group_name` \
    								FROM `groups`) AS groups  \
    					  ON `groups`.`role_id`= `roles`.`role_id` \
            			  JOIN (	SELECT `user_id`, `group_id` \
            						FROM `users_groups` ) AS `users_groups` \
              			  ON `groups`.`group_id`= `users_groups`.`group_id` \
           							WHERE `user_id`='%s' " % (user_id)

                cursor.execute(query)
                res = cursor.fetchall()
                html.req.session["role"] = str(res[0][0]).lower()
                html.req.session["group"] = str(res[0][1])
                html.req.session["user_id"] = str(user_id)
                html.req.session.save()
                sr = check_db_session(username)

                if(sr == 0):
                    html_str = str(
                        {"success": 2, "result": "Error While Logging in"})
                else:
                    if (enable and   # if password_expiry feature enable
                            (   (expiry_age > pwd_age) # and password yet not expired
                                and
                                ((expiry_age-pwd_age) <=  warning_time) # but seemes to be expired
                            )
                        ):
                        html_str = str(
                            {"success": 4, "result": "Your password will expire in %d days" % (expiry_age-pwd_age)})
                    else:
                        html_str = str(
                            {"success": 0, "result": ["side.py", "main.py"]})
                update_session(html.req.session["username"], html.req.session.id())
                html.write(html_str)
            elif(sha.sha(password).hexdigest() == sha_old_pwd):
                html.req.session.delete()
                html.write(str({"success": 3, "result":
                       "<br/>Sorry! You Entered An Old Password"}))
        else:
            html.req.session.delete()
            html.write(str({"success": 1, "result":
                       "Please Enter Valid Username and Password"}))
    except Exception, e:
        import traceback
        logme("unmp_login", traceback.format_exc())
        html.write(str({"success": 1, "result":
                   "Please Enter Valid Username and Password"}))

    finally:
        license_check(db)
        cursor.close()
        db.close()


def unmp_logout(h):
    global html
    html = h
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()

        query="	UPDATE `login_info` \
        		SET `is_logged_in` = 0 \
        		WHERE `user_name` = '%s'" %(
        				html.req.session["username"])

        cursor.execute(query)
        db.commit()
    except Exception, e:
        html.write("0")
    finally:
        # html.req.session.delete()
        html.req.session.invalidate()
        cursor.close()
        db.close()


def update_session(username, ssid):
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        query="SELECT  `user_name` \
        	   FROM `login_info` \
        	   WHERE `user_name` = '%s' " %(username)
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res)!=0:
            query="	UPDATE `login_info` \
            		SET `session_id` = '%s', `login_time` = '%s', `is_logged_in` = 1, `last_accessed_time` = '%s' \
            		WHERE `user_name` = '%s' " %(
                        ssid, datetime.now(), datetime.now(), username)
        else :
            query="	INSERT INTO `login_info` \
            		VALUES ('%s', 1, '%s', '%s', 0, 1, '%s') " %(
            					username,ssid,datetime.now(), datetime.now())

        cursor.execute(query)
        db.commit()
    except Exception, e:
        pass
    finally:
        db.close()


def check_db_session(username):
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()

        query="SELECT `session_id` \
               FROM  `login_info` \
               WHERE  `user_name`='%s' AND `is_logged_in` = 1" %(username)

        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 0:
            return 1
        else:
            return 0
    except Exception, e:
        return 1
    finally:
        db.close()


def unmp_login_verify(username, password):
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        pwd = db.escape_string(password)

        query="SELECT `user_name`, `user_id` \
        	   FROM  `user_login` \
        	   WHERE `user_name` = '%s' AND `password` =SHA('%s') " %(
        	   										username,pwd)
        cursor.execute(query)
        res = cursor.fetchall()

        if len(res) == 1:
            return 0
        else:
            return 1
    except Exception, e:
        return 1
    finally:
        db.close()

#End Edit
