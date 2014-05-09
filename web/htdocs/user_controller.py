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
# calling the view for settings
def user_settings(h):
    global html
    html = h
    css_list = []
    js_list = ["js/pages/user_settings.js"]
    html.new_header("User Settings","user_settings","",css_list,js_list)
    html.write(User.create_settings_form())
    usr=User_bll()
    user_id=html.req.session["user_id"]
    res=usr.get_data_for_settings(user_id)
    html.write(User.create_user_settings_form(res[0],res[1],res[2],res[3],res[4],res[5],res[6]))
    res2=usr.get_data_for_settings_password(user_id)
    html.write(User.create_user_settings_password_form(res2[0]))
    html.new_footer()



def get_user_settings(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/user_mgt.js","js/ccpl_utility.js","js/pages/user_settings.js"]
    html.new_header("User Settings","user_settings","",css_list,js_list)
    usr=User_bll()
    user_id=html.req.session["user_id"]
    res=usr.get_data_for_settings(user_id)
    html.write(User.create_user_settings_form(res[0],res[1],res[2],res[3],res[4],res[5],res[6]))
    html.new_footer()

def set_user_settings_personal(h):
    global html
    html = h
    user_id=html.req.session["user_id"]
    first_name=str(html.var("first_name"))
    last_name=str(html.var("last_name"))
    company=str(html.var("company"))
    designation=str(html.var("designation"))
    address=str(html.var("address"))
    mobile=str(html.var("mobile"))
    email_id=str(html.var("email_id"))
    usr=User_bll()
    res=usr.set_data_for_settings(user_id,first_name,last_name,company,designation,address,mobile,email_id)
    return res

def get_user_settings_password(h):
    global html
    html = h
    css_list = ["css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    js_list = ["js/jquery.dataTables.min.js","js/pages/user_mgt.js","js/ccpl_utility.js","js/pages/user_settings.js"]
    html.new_header("User Settings","user_settings","",css_list,js_list)
    user_id=html.req.session["user_id"]
    usr=User_bll()
    res=usr.get_data_for_settings_password(user_id)
    html.write(User.create_user_settings_password_form(res[0]))
    html.new_footer()

def set_user_settings_password(h):
    global html
    html = h
    user_id=html.req.session["user_id"]
    password=str(html.var("confirm_password_1"))
    usr=User_bll()
    res=usr.set_data_for_settings_password(user_id,password)
    return res
