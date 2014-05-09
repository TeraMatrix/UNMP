#!/usr/bin/python2.6

'''
@author: Mahipal Choudhary
@since: 14-Nov-2011
@version: 0.1
@note: All functions Related with user settings.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

# Import modules that contain the function and libraries
from user_bll import User_bll
from user import User
from json import JSONEncoder

# calling the view for settings
def user_settings(h):
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/user_settings.js"]
    html.new_header("User Settings", "user_settings", "", css_list, js_list)

    is_first_login = html.var('is_first_login')
    is_password_expired = html.var('is_password_expired')
    if is_first_login or is_password_expired:
        html.write(User.change_password(is_first_login, is_password_expired))
    else:
        html.write(User.create_settings_form())
        usr = User_bll()
        user_id = html.req.session["user_id"]
        res = usr.get_data_for_settings(user_id)
        html.write(User.create_user_settings_form(res[0], res[1], res[2], res[3], res[4], res[5], res[6]))

    html.write(User.create_user_settings_password_form())
    html.write('</div></div>')
    html.new_footer()


def get_user_settings(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/lib/main/jquery.dataTables.min.js", "js/unmp/main/user_mgt.js",
               "js/unmp/main/user_settings.js"]
    html.new_header("User Settings", "user_settings", "", css_list, js_list)
    usr = User_bll()
    user_id = html.req.session["user_id"]
    res = usr.get_data_for_settings(user_id)
    html.write(User.create_user_settings_form(res[0], res[1], res[2], res[3], res[4], res[5], res[6]))
    html.new_footer()


def set_user_settings_personal(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    first_name = str(html.var("first_name"))
    last_name = str(html.var("last_name"))
    company = str(html.var("company"))
    designation = str(html.var("designation"))
    address = str(html.var("address"))
    mobile = str(html.var("mobile"))
    email_id = str(html.var("email_id"))
    usr = User_bll()
    res = usr.set_data_for_settings(user_id, first_name, last_name, company,
                                    designation, address, mobile, email_id)
    return res


def get_user_settings_password(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/lib/main/jquery.dataTables.min.js", "js/unmp/main/user_mgt.js",
               "js/unmp/main/user_settings.js"]
    html.new_header("User Settings", "user_settings", "", css_list, js_list)
    #user_id = html.req.session["user_id"]
    #usr = User_bll()
    #res = usr.get_data_for_settings_password(user_id)
    #html.write(User.create_user_settings_password_form(res[0]))
    html.write(User.create_user_settings_password_form())
    html.new_footer()

#from common_controller import logme
from usr_mgt_view import is_valid_passwd


def set_user_settings_password(h):
    global html
    html = h
    user_id = html.req.session["user_id"]
    old_password = html.var("password")
    password = html.var("confirm_password_1")
    #logme('i m in '+str(old_password))
    return_json = {'success': 1, 'msg': 'no '}
    if old_password is not None and password is not None:
        if old_password == password:
            return_json = {'success': 1, 'msg': 'New Password can\'t be same as Old password'}
        else:
            if User_bll.check_password(user_id, old_password):
                return_json = {'success': 1, 'msg': 'Old Password doesn\'t Match'}
            else:
                if is_valid_passwd(password):
                    usr = User_bll()
                    if usr.set_data_for_settings_password(user_id, password):
                        return_json = {'success': 1, 'msg': 'Password couldn\'t save, Try again'}
                    else:
                        verify_first_login(html)
                        return_json = {'success': 0, 'msg': ''}
                else:
                    return_json = {'success': 1, 'msg': ' Password should consist of 2 numeric, 2 alpha, 2 special'}
    else:
        return_json = {'success': 1, 'msg': 'All fields are required'}
    html.req.content_type = 'application/json'
    html.write(str(JSONEncoder().encode(return_json)))


def verify_first_login(h):
    global html
    html = h
    username = html.req.session["username"]
    usr = User_bll()
    res = usr.verify_first_login(username)
    return res

# added by Grijesh on 7, Feb 2013
def check_password(h):
    pwd = h.var('pwd')
    user_id = h.req.session['user_id']
    if pwd is not None and user_id is not None:
        result = User_bll.check_password(user_id, pwd)
        if result == 0:
            result = {'success': 0}
        else:
            result = {'success': 1}
    else:
        result = {'success': 1}

    h.req.content_type = 'application/json'
    h.req.write(str(JSONEncoder().encode(result)))
