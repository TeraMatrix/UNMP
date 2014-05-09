#!/usr/bin/python2.6
from lib import *
from nms_config import *
from manage_login_view import ManageLogin
from manage_login_bll import ManageLoginBll


def get_data(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/lib/main/jquery.dataTables.min.js", "js/unmp/main/manage_login.js"]
    html.new_header("Manage Login-Session of Users", "manage_login.py",
                    "", css_list, js_list)
    html.write(ManageLogin.create_form())
    html.new_footer()


def get_login_data(h):
    '''
    @author			: Mahipal Choudhary
    @since			: 07-Dec-2011
    @requires			: html object h
    @param h			: html object from request
    @var html			: global object html
    @var lb			: object of class Log_bll
    @var result			: string containing the result after calling the BLL function for logs
    @note			: This is the controller function to get complete data for all logs
    '''
    global html
    html = h
    mlb_obj = ManageLoginBll()
    user_id = html.req.session["user_id"]
    username = html.req.session["username"]
    result = mlb_obj.get_login_data(user_id, username)
    html.write(str(result))


def delete_login_data(h):
    '''
    @author			: Mahipal Choudhary
    @since			: 07-Dec-2011
    @requires			: html object h
    @param h			: html object from request
    @var html			: global object html
    @var lb			: object of class Log_bll
    @var result			: string containing the result after calling the BLL function for logs
    @note			: This is the controller function to get complete data for all logs
    '''
    global html
    html = h
    mlb_obj = ManageLoginBll()
    user_id = str(html.var("user_id"))
    result1 = mlb_obj.set_session_delete(user_id)
    # result2= mlb_obj.update_login(user_id)
    html.write(str(result1))


# def view_page_tip_manage_login(h):
#     global html
#     html = h
#     html.write(ManageLogin.view_page_tip_manage_login())
