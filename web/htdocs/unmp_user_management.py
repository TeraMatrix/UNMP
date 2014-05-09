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


def login(h):
    """

    @param h:
    """
    global html
    html = h
    login_box = '<div id=\"login_box\">\
    <h1>Login</h1>\
    <form action=\"unmp_login.py\" method=\"post\" id=\"login_form\" name=\"login_form\">\
        <div class=\"form-div\" style=\"min-width:100%;margin-bottom:0px;position:inherit;\">\
            <div class=\"form-body\">\
                <div class=\"row-elem\">\
                    <label class=\"lbl\" for=\"username\">Username</label>\
                    <input type=\"text\" id=\"username\" name=\"username\" title=\"Enter Your User Name\"/>\
                </div>\
                <div class=\"row-elem\">\
                    <label class=\"lbl\" for=\"password\">Password</label>\
                    <input type=\"password\" id=\"password\" name=\"password\" title=\"Enter Your Password\"/>\
                </div>\
                <div class=\"row-elem\">\
                </div>\
            </div>\
            <div class=\"form-div-footer\">\
                <button class="yo-small yo-button" type="submit"><span class="key">Login</span></button>\
            </div>\
        </div>\
    </form>\
    </div>'
    css_list = ["css/style.css"]
    js_list = ["js/unmp/main/login.js"]
    html.new_header("Login", "", "", css_list, js_list)
    html.write(login_box)
    html.new_footer()


def unmp_login(h):
    """

    @param h:
    """
    global html
    html = h
    if config.check_user(html.req.session["username"]) > 0:
        html.write(str({"success": 0, "result": ["side.py", "main.py"]}))
    else:
        html.write(str({"success": 1, "result": "Worng Username or Password"}))


def unmp_logout(h):
    """

    @param h:
    """
    global html
    html = h
    html.req.session.delete()
    html.write("0")
