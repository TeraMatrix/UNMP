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
import htmllib
import pprint
import sidebar
import os
from lib import *


def page_manage_user(h):
    global html
    html = h
    if not config.may("manage_user"):
        raise MKAuthException("You are not allowed to manage user.")
    css_list = []
    js_list = ["js/unmp/main/manageuser.js"]
    html.new_header("Manage User", "", "", css_list, js_list)
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    html.write(
        "<div id=\"formDiv\" style=\"display:none;\"></div><div class=\"main-title\" style=\"cursor: pointer;\" id=\"addUserDivButton\" onclick=\"addUser()\"><img alt=\"add\" src=\"images/add16.png\"><span>Add User</span></div>")
    html.write("<div id=\"userListDiv\">")
    html.write("</div>")
    html.new_footer()


def user_grid_view(h):
    global html
    html = h

    htmlString = "<table class=\"addform\"><colgroup><col width=\"30%\" /><col width=\"60%\"<col width=\"5%\" /><col width=\"5%\" /></colgroup>"
    htmlString += "<tr><th>User Name</th><th colspan=\"3\">Role</th></tr>"
    i = 0
    for user in config.get_user_list():
        i += 1
        if i % 2 == 0:
            htmlString += "<tr class=\"even\">"
        else:
            htmlString += "<tr>"
        htmlString += "<td>" + user + "</td><td>" + config.role_of_user(
            user) + "</td><td><img src='images/edit16.png' alt='edit' title='Edit User Details' class='imgbutton' onclick='editUser(\"" + user + \
                      "\")'/></td><td><img src='images/delete16.png' alt='delete' title='Delete User' class='imgbutton' onclick='deleteUser(\"" + \
                      user + \
                      "\")'/></td></tr>"
    htmlString += "</table>"
    html.write(htmlString)


def form_for_user(h):
    global html
    html = h
    formdata = ""
    if html.var("action").strip() == "edit":
        formdata += "<form id=\"userForm\" action=\"update_user.py\" method=\"post\"><table class='addform'><colgroup><col width='20%'/><col width='80%'/></colgroup><tr><th colspan='2'>Edit User</th></tr><tr><td>User Name</td><td><input type='text' name='userName' id='userName' class='required' readonly=\"readonly\" value=\"" + html.var(
            "user") + "\" /></td></tr><tr><td>Password</td><td><input type='password' name='password' id='password' value=''/></td></tr><tr><td>Confirm Password</td><td><input type='password' name='cpassword' id='cpassword' value=''/></td></tr><tr><td>Role</td><td>" + user_roles_select_list(
            config.role_of_user(html.var(
                "user"))) + "</td></tr><tr><td class='button' colspan='2'><input type='submit' value='Update'/><input type='button' value='Cancel' onclick=\"cancelEditUser()\"/></td></tr></table></form>"

    else:
        formdata += "<form id=\"userForm\" action=\"add_user.py\" method=\"post\"><table class='addform'><colgroup><col width='20%'/><col width='80%'/></colgroup><tr><th colspan='2'>Add User</th></tr><tr><td>User Name</td><td><input type='text' name='userName' id='userName' value='' class='required' /></td></tr><tr><td>Password</td><td><input type='password' name='password' id='password' value='' class='required' /></td></tr><tr><td>Confirm Password</td><td><input type='password' name='cpassword' id='cpassword' value='' class='required' /></td></tr><tr><td>Role</td><td>" + \
                    user_roles_select_list(
                        "") + "</td></tr><tr><td class='button' colspan='2'><input type='submit' value='Submit'/><input type='button' value='Reset' onclick=\"resetAddUser()\"/><input type='button' value='Cancel' onclick=\"cancelAddUser()\"/></td></tr></table></form>"
    html.write(formdata)


def page_change_password(h):
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/changepassword.js"]
    html.new_header("Change Password", "", "", css_list, js_list)
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    formdata = "<form id=\"userForm\" action=\"password_changed.py\" method=\"post\"><table class='addform'><colgroup><col width='20%'/><col width='80%'/></colgroup><tr><th colspan='2'>Change Password</th></tr><tr><td>User Name</td><td><input type='text' name='userName' id='userName' class='required' readonly=\"readonly\" value=\"" + config.user + \
               "\" /></td></tr><tr><td>New Password</td><td><input type='password' name='password' id='password' value=''/></td></tr><tr><td>Confirm New Password</td><td><input type='password' name='cpassword' id='cpassword' value=''/></td></tr><tr><td class='button' colspan='2'><input type='submit' value='Update'/><input type='button' value='Cancel' onclick=\"javascript:history.go(-1)\"/></td></tr></table></form>"
    html.write(
        "<div id=\"formDiv\" style=\"display:block;\">" + formdata + "</div>")
    html.new_footer()


def password_changed(h):
    global html
    html = h
    sitename = __file__.split("/")[3]
    if html.var("password").strip() != "":
        os.system("htpasswd -D /omd/sites/%s/etc/htpasswd %s" % (
            sitename, config.user))
        os.system("htpasswd -b /omd/sites/%s/etc/htpasswd %s %s" %
                  (sitename, config.user, html.var("password")))
        html.write("1")
    else:
        html.write("2")


def user_roles_select_list(selectedRole):
    selectString = "<select id=\"userRole\" name=\"userRole\"><option value=\"\" class='required'>-- Select Role --</option>"
    for role in config.get_role_list():
        if selectedRole == role:
            selectString += "<option value=\"" + role + \
                            "\" selected=\"selected\">" + role + "</option>"
        else:
            selectString += "<option value=\"" + role + "\">" + \
                            role + "</option>"
    selectString += "</select>"
    return selectString


def add_user(h):
    global html
    html = h
    sitename = __file__.split("/")[3]
    if config.check_user(html.var("userName").strip()) == 0:
        os.system("htpasswd -b /omd/sites/%s/etc/htpasswd %s %s" % (
            sitename, html.var("userName").strip(), html.var("password")))
        config.add_user(
            html.var("userName").strip(), html.var("userRole").strip())
        html.write("1")
    else:
        html.write("0")


def delete_user(h):
    global html
    html = h
    sitename = __file__.split("/")[3]
    if config.user != html.var("userName").strip():
        if config.check_user(html.var("userName").strip()) == 1:
            os.system("htpasswd -D /omd/sites/%s/etc/htpasswd %s" % (
                sitename, html.var("userName").strip()))
            config.delete_user(html.var("userName").strip())
            html.write("1")
        else:
            html.write("0")
    else:
        html.write("2")


def update_user(h):
    global html
    html = h
    sitename = __file__.split("/")[3]
    if config.user != html.var("userName").strip():
        if config.check_user(html.var("userName").strip()) == 1:
            config.update_user(
                html.var("userName").strip(), html.var("userRole").strip())
            if html.var("password").strip() != "":
                os.system("htpasswd -D /omd/sites/%s/etc/htpasswd %s" % (
                    sitename, html.var("userName").strip()))
                os.system("htpasswd -b /omd/sites/%s/etc/htpasswd %s %s" % (
                    sitename, html.var("userName").strip(), html.var("password")))
            html.write("1")
        else:
            html.write("3")
    else:
        html.write("2")


def logout(h):
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/logout.js"]
    html.new_header("Logout", "", "", css_list, js_list)
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    formdata = "<form id=\"userForm\" action=\"password_changed.py\" method=\"post\"><table class='addform'><colgroup><col width='20%'/><col width='80%'/></colgroup><tr><td colspan='2' class='button'>Do You want to logout?</td></tr><tr><td class='button' colspan='2'><input type='button' onclick=\"return clearAuthData();\" value='Logout'/><input type='button' value='Cancel' onclick=\"javascript:history.go(-1)\"/></td></tr></table></form>"
    html.write(
        "<div id=\"formDiv\" style=\"display:block;\">" + formdata + "</div>")
    html.new_footer()


# Is it possible to create logout for nagios web interface.  As far as I
# understand, it is just matter of resetting the $_REMOTE_USER apache variable.
