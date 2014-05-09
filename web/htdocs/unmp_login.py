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
##################################################################

import config
from htmllib import *
import MySQLdb
import pickle 
from datetime import datetime
from unmp_config import SystemConfig
from mod_python import Session
#import logging
#logging.basicConfig(filename='/omd/daemon/index_unmp.log',format='%(levelname)s: %(asctime)s >> %(message)s', level=logging.DEBUG)
#log = logging.getLogger('Login')


def login(h):
    global html
    html = h
    login_box = '<div id=\"login_box\">\
    <h1>Login</h1>\
    </script>\
    <form action=\"unmp_login.py\" method=\"get\" id=\"login_form\" name=\"login_form\">\
        <div class=\"form-div\" style=\"min-width:100%;margin-bottom:0px;position:inherit;\">\
            <div class=\"form-body\" style=\"position:absolute;top:33px;left:0;\">\
                <div class=\"row-elem\">\
                    <label class=\"lbl\" for=\"username\">Username</label>\
                    <input type=\"text\" id=\"username\" name=\"username\" title=\"Enter Your User Name\"/>\
                </div>\
                <div class=\"row-elem\">\
                    <label class=\"lbl\" for=\"password\">Password</label>\
                    <input type=\"password\" id=\"password\" name=\"password\" title=\"Enter Your Password\"/>\
                </div>'

#                <div class=\"row-elem\">\
#                    <label class=\"lbl\">&nbsp;</label>\
#                    <input type=\"checkbox\" id=\"remamber_me\" name=\"remamber_me\" />\
#                    <label class=\"sub-lbl\" for=\"remamber_me\">[Remember Me]</label>\
#                    <input type=\"hidden\" id=\"check_session\" name=\"check_session\" />\
#                </div>\
    login_box+='        </div>\
            <div class=\"form-div-footer\" style=\"background-color:#FFF;position:absolute;bottom:0;\">\
                <button class="yo-small yo-button" type="submit"><span class="key">Login</span></button>\
            </div>\
        </div>\
    </form>\
    </div>'
    html.new_sidebar_header("Login",[],["js/login.js"],"http://www.shyamtelecom.com","SHYAM");
    html.write(login_box)
    html.write('<div id=\"footer\">\
        <div id=\"footer_div\">\
        </div>\
    </div>')
     
def license_check(db):    
    cursor = db.cursor()
    query = "select is_valid,minutes,last_check_date from license_info"
    cursor.execute(query)
    res=cursor.fetchall()
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
                        query = "update license_info set minutes= '%s', last_check_date = '%s'"%(mindelta,curr_date)
                    else:
                        query = "update license_info set is_valid= '1', minutes= '0', last_check_date = '%s'"%(curr_date)
                else:
                    query = "update license_info set last_check_date = '%s'"%(curr_date)             
            else:
                query = "update license_info set last_check_date = '%s'"%(curr_date)             
            
            cursor.execute(query)
            db.commit()
    cursor.close()           
            
                 
def unmp_login(h):
    global html
    html = h
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        username=html.var("username")
        password=html.var("password")
        pwd = db.escape_string(password)
        #check=html.var("check_session")
        query="select user_name,user_id from user_login where user_name='%s' and password='%s' " %(username,pwd)
        
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)==1:
            user_id=str(res[0][1])
            query="SELECT roles.role_name,groups.group_name from roles join ( select group_id,role_id, group_name FROM groups) as groups  on groups.role_id=roles.role_id \
            join (select user_id,group_id from users_groups ) as users_groups on groups.group_id=users_groups.group_id \
            where user_id='%s' " %(user_id)
            cursor.execute(query)
            res=cursor.fetchall()
            html.req.session["role"]=str(res[0][0]).lower()
            html.req.session["group"]=str(res[0][1])
            html.req.session["user_id"]=str(user_id)
            html.req.session.save()
            sr=check_db_session(username)
            if(sr==0):
                html_str = str({"success":2,"result":"Error While Logging in"})
            else:
                html_str = str({"success":0,"result":["side.py","main.py"]})
            update_session(html.req.session["username"],html.req.session.id())
            html.write(html_str)
        else:
            req.session.delete()
            html.write(str({"success":1,"result":"Please Enter Valid Username and Password"}))

    except Exception,e:
        html.write(str({"success":1,"result":"Please Enter Valid Username and Password"}))
        #pass
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
        query="update login_info set is_logged_in=0 where user_name='%s'" %(html.req.session["username"])
        cursor.execute(query)
        db.commit()

    except Exception,e:
        html.write("0")
    finally:
        #html.req.session.delete()
        html.req.session.invalidate()
        cursor.close()
        db.close()



def update_session(username,ssid):
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
    	query="select user_name from login_info where user_name='%s' " %(username)
    	cursor.execute(query)
    	res=cursor.fetchall()
    	if len(res)!=0:
    	    query="update login_info set session_id='%s',login_time='%s',is_logged_in=1 where user_name='%s' " %(ssid,datetime.now(),username)  
    	else :
    	    query="insert into login_info values('%s',1,'%s','%s',0) " %(username,ssid,datetime.now())                        
        cursor.execute(query)
        db.commit()
    except Exception ,e:
        pass
    finally:
        db.close()


def check_db_session(username):
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        query="select session_id from login_info where user_name='%s' and is_logged_in=1" %(username)  
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)==0: 
            return 1
        else :
            return 0
    except Exception ,e:
        return 1
    finally:   
        db.close()
        
def unmp_login_verify(h):
    global html
    html = h
    try:
        db = MySQLdb.connect(*SystemConfig.get_mysql_credentials())
        cursor = db.cursor()
        username=html.var("username")
        password=html.var("password")
        pwd = db.escape_string(password)
        #check=html.var("check_session")
        query="select user_name,user_id from user_login where user_name='%s' and password='%s' " %(username,pwd)
        cursor.execute(query)
        res=cursor.fetchall()
        if len(res)==1:
            return 0
        else :
            return 1
    except Exception , e:
        return 1
    finally:
        db.close()
        
