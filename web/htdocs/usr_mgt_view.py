#!/usr/bin/python2.6

"""
@author: Rahul Gautam
@note: user Management View
@attention: update: 20/Feb/2011
"""

from htmllib import *
import usr_mgt_bll
from common_bll import EventLog, Essential
from license_bll import LicenseBll

special_check = lambda x:  1 if set("\"\`~!#$%^&*(){}[]+=|?<>:;").intersection(x) else 0
space_check = lambda x:  1 if set(" ").intersection(x) else 0
def validate_name(nm,type):
    if space_check(nm) == 0:
        if type == "user": # user
            result = usr_mgt_bll.check_name(nm,"user")
        elif type == "group": # group
            result = usr_mgt_bll.check_name(nm,"group")
        else:
            result = 1
        if result == 0:         
            return 0
    return 1

def add_users_togroup(h):
    global html
    html = h
    session_user = html.req.session['username']
    grp_name = html.var('grp_name')
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    user_ids = html.var("user_ids")
    users = html.var("users")
    newGroupID = html.var("group_id")
    result,flag = 1,1
    if user_ids != '':
        #user_names_list = users.split(",")
        if users.find(session_user+" ") == -1:
            user_ids_list = user_ids.split(",")
            lb = LicenseBll()
            users_no = lb.check_license_for_useringroup(grp_name)
            if users_no >= len(user_ids_list):
                result = usr_mgt_bll.add_user_in_group(user_ids_list,newGroupID)
            else:
                else_str = "Maximum number of allowed users of a type %s have reached"%(grp_name)
                flag = 0        
        else:
            else_str = "Assigning self to another Usergroup is restricted"
            flag = 0
    else:
        else_str = "Remain Unchanged No User Selected"
        flag = 0

    result_json = {}

    if flag == 0 and result == 1:         
        result_json['success'] = 2
        result_json['result'] = else_str
    elif result == 0:
        result_json['success'] = 0
        users = html.var('users')
        sel_group = html.var('sel_group')
        if sel_group:
            info_str = " Users: %s have been moved from Group: %s to Group: %s"%(users,sel_group,grp_name)            
        else:
            info_str = " Users: %s have been assigned to Group: %s"%(users,grp_name)
        el = EventLog()
        el.log_event(info_str,session_user)
    elif flag == 1 and result == 1:
        result_json['success'] = 1
        result_json['result'] = " Some field contains special characters (like \" \, etc.) "
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "  

    html.write(str(result_json))



def del_users_fromgroup(h):
    global html
    html = h
    session_user = html.req.session['username']
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    users = html.var("users")
    user_ids = html.var("user_ids")
    result,flag = 1,1
    if user_ids != '':
        if users.find(session_user+" ") == -1:
            user_ids_list = user_ids.split(",")
            result = usr_mgt_bll.del_user_from_group(user_ids_list)
        else:
            else_str = "Assigning self to another Usergroup is restricted.\n Deleting form a group moves user to Default system group"
            flag = 0
    else:
        else_str = "Remain Unchanged No User Selected"
        flag = 0

    result_json = {}

    if flag == 0 and result == 1:         
        result_json['success'] = 2
        result_json['result'] = else_str
    elif result == 0:

        result_json['success'] = 0
        users = html.var('users')
        grp_name = html.var('grp_name')
        info_str = " Users: %s have been deleted from Group: %s"%(users,grp_name)
        el = EventLog()
        el.log_event(info_str,session_user)
    elif flag == 1 and result == 1:
        result_json['success'] = 1
        result_json['result'] = " Some field contains special characters (like \" \, etc.) "
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "  

    html.write(str(result_json))



def group_info(h):
    global html
    html = h
    table = usr_mgt_bll.get_group_info(html.var("group_id"))
    group_str = ""
    group_str += "<table cellspacing=\"0\" width=\"100%\" cellpadding=\"0\" class=\"tt-table\" style=\"margin-bottom:0;\">\
                             <tbody><tr style=\"font-weight:bold;\">\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Role Name</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Updated By</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Update Time</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Created By</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Creation Time</td>\
                                     </tr>"
    if table == 1:
        group_str +="<tr> Well, its really embarasing But its seems there is No data availabe. Sorry </tr>"
    else:
        group_str += "<tr>"
        for tup in table:
            group_str += "<td class=\"cell-info1\">%s</td>"%tup
        group_str += "</tr>"
    group_str +="</tbody></table> "
    html.write(group_str)

def group_users(h):
    global html
    html = h
    light_box = html.var("light_box")
    table = usr_mgt_bll.get_group_users(html.var("group_id"))
    if table == 1 :
        html.write("[]")
    else:
        make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
        gpUser_list = []
        for gpUser in table:
            gpUser_list.append(make_list(gpUser))

        html.write(str(gpUser_list))

def user_view(h):
    global html
    html = h
    css_list = ["css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/jquery.dataTables.min.js","js/pages/user_mgt.js","js/ccpl_utility.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addUser();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_user\" name=\"add_user\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add User\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editUser();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_user\" name=\"edit_user\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit User\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delUser();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_user\" name=\"del_user_tip\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete User\"></div>" % theme
    all_btn = del_btn + edit_btn + add_btn
    #all_btn = edit_btn
    html.new_header("User Management","manage_user.py",all_btn,css_list,javascript_list)
    html.write("<div id=\"user_datatable\">\
                    <table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"user_table\" style=\"width:100%;\"></table>\
                </div>\
                <div id=\"user_form\" style=\"display:none;\">\
                    <form action=\"add_user.py\" method=\"get\" id=\"add_user_form\" name=\"add_user_form\">\
                        <div class=\"form-div\">\
				    <table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
				        <tr>\
				            <th class=\"cell-title\">Add User</th>\
				        </tr>\
    				</table>\
                            <div class=\"form-body\">\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"username\">User Name</label>\
                                    <input type=\"text\" id=\"user_name\" name=\"user_name\" title=\"Choose Your Unique User Name. <br/>Must be at least 5 characters.\" onblur=\"name_chk();\" />\
                                    <input type=\"button\" id=\"check_uname\" class=\"yo-button\" name=\"check_uname\" value=\"Check availability\" title=\"Check User Name Availability\" onclick=\"name_chk();\" />\
                                    <label id=\"check_result\" name=\"check_result\" style=\"margin:20px\" for=\"user_name\" ></label>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"password\">Password</label>\
                                    <input type=\"password\" id=\"password\" name=\"password\" title=\"Must be at least 6 characters. \"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"cpassword\">Confirm Password</label>\
                                    <input type=\"password\" id=\"cpassword\" name=\"cpassword\" title=\"Must be same as Password\"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"group\">Select Group</label>" + groups_select_list("","","Default") + "\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"first_name\">First Name</label>\
                                    <input type=\"text\" id=\"first_name\" name=\"first_name\" title=\"Please Enter First name.\"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"last_name\">Last Name</label>\
                                    <input type=\"text\" id=\"last_name\" name=\"last_name\" title=\"Please Enter Last name.\"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"company\">Company</label>\
                                    <input type=\"text\" id=\"company\" name=\"company\" title=\"Please Enter your Company Name.\"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"designation\">Designation</label>\
                                    <input type=\"text\" id=\"designation\" name=\"designation\" title=\"Please Enter your Designation.\"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"address\">Address</label>\
                                    <textarea id=\"address\" name=\"address\" title=\"Please Enter your own Address.\"></textarea>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"mobile\">Mobile Number</label>\
                                    <input type=\"text\" id=\"mobile\" name=\"mobile\" title=\"Please Enter your Mobile Number<br/> Does't include +91 or 0.\"/>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"email_id\">E-Mail ID</label>\
                                    <input type=\"text\" id=\"email_id\" name=\"email_id\" title=\"Please Enter your E-Mail ID.\"/>\
                                </div>\
                            </div>\
                        </div>\
                        <div class=\"form-div-footer\">\
                            <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"add\">Save</span></button>\
                            <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_add_user\"><span class=\"cancel\">Cancel</span></button>\
                        </div>\
                    </form>\
                </div>\
                <div id=\"edit_usr_form\" style=\"display:none;\">\
                </div>")
    html.new_footer()

def add_user(h):
    global html
    html = h
    result_json = {}
    lb = LicenseBll()
    flag = 0
    ugroup = html.var('grp_name')
    lb_result = lb.check_license_for_user(ugroup)
#    html.write(str(lb.check_license_for_user(ugroup))+" : "+str(lb.get_allowed_user(ugroup))+str())
    if lb_result == True:
        var_list = ['user_name','password','first_name','last_name','groups','company','designation','address','mobile','email_id']
        #v_result = validate(html,var_list)
        var_dict_ul = {}
        var_dict = {}
        var_dict_ug = {}
        name_not = 0
        for i in var_list:
            if i == 'user_name' :
                if validate_name(html.var(i),"user") == 0:
                    pass
                else:
                    name_not = 1
                    break

            if i == 'user_name' or i == 'password' or i == 'groups':
                pass
            if special_check(html.var(i)) == 0:
                flag = 0
            else:
                flag = 1
                break
            if i == 'user_name' or i == 'password': 
                var_dict_ul[i] = html.var(i)
            elif i == 'groups':
                var_dict_ug[i] = html.var(i)
            else:
                var_dict[i] = html.var(i)


        if name_not == 1:
            result_json['success'] = 1
            result_json['result'] = " Name Not valid, Choose Unique Name, No space"
        else:

            result = 1
            if flag == 0:         
                result = usr_mgt_bll.add_user(var_dict,var_dict_ul,var_dict_ug)
            else:
                result_json['success'] = 1
                result_json['result'] = " Some field contains special characters (like \" \, etc.) "

            if result == 0:
                result_json['success'] = 0

            elif flag == 0:
                result_json['success'] = 1
                result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "
    elif flag == 1:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code "
    elif lb_result == "groupFlase" :
        result_json['success'] = 1
        result_json['result'] = "Maximum number of allowed users of a type %s have reached"%(ugroup)        
    else:
        result_json['success'] = 1
        result_json['result'] = "Maximum number of allowed users have reached. To Complete this action you need to upgrade your license please contact sales team."

    html.write(str(result_json))




def add_group(h):
    global html
    html = h
    var_list = ['group_id','group_name','description','role']
    var_dict = {}
    name_not = 0 
    for i in var_list:
        if i == 'group_name':
            if validate_name(html.var(i),"group") == 0:
                pass
            else:
                name_not = 1
                break
        if i == 'role_id':
            var_dict[i] = html.var(i)
        else:
            var_dict[i] = html.var(i)

#    st_r = str(var_dict)+" //// "+str(var_dict_ul)
#    html.write(st_r)
    result_json = {}
    lb = LicenseBll()
    if lb.check_license_for_usergroup() == True:
        if name_not == 1:
            result_json['success'] = 1
            result_json['result'] = " Name Not valid, Choose Unique Name, No space"       
        else:
            result = usr_mgt_bll.add_group(var_dict) # modify it it take only one arg

            if result == 0:
                result_json['success'] = 0
            else:
                result_json['success'] = 1
                result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)
    else:
        result_json['success'] = 1
        result_json['result'] = "Maximum number of allowed usergroup have reached. To Complete this action you need to upgrade your license please contact sales team."
    html.write(str(result_json))    


def edit_user_view(h):
    global html
    html = h
    username =  html.req.session['username']
    user_name = html.var('user_name')
    grp_flag = 0
    if username != user_name:
        sess_grp_name = html.req.session['group']                  
        user_id = html.var('user_id')
        if sess_grp_name.lower() != "superadmin":
            grp_name = usr_mgt_bll.get_group_name(user_id)
            if grp_name == "SuperAdmin":
                grp_flag = 1

        if grp_flag == 0:                
            o_dict = {}
            _dict = type(o_dict)  
            user_detail_dict = usr_mgt_bll.edit_user_view(user_id)

            if type(user_detail_dict) == _dict :
                user_detail_dict.update({'group_list':groups_select_list(user_detail_dict['group_name'],"","Default")})
                form_str = "<form action=\"edit_user.py\" method=\"get\" id=\"edit_user_form\" name=\"edit_user_form\">\
                                    <div class=\"form-div\">\
        				<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\">\
        				    <tr>\
        				        <th class=\"cell-title\">Edit User</th>\
        				    </tr>\
        				</table>\
                                        <div class=\"form-body\">\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"username\">User Name</label>\
                                                <input type=\"text\" id=\"user_name\" readonly=\"readonly\" name=\"user_name\" title=\"you can't edit User Name\" value=\"%(user_name)s\" />\
                                                <input type=\"hidden\" id=\"user_id\" name=\"user_id\" value=\"%(user_id)s\" />\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"group\">Select Group</label>%(group_list)s\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"first_name\">First Name</label>\
                                                <input type=\"text\" id=\"first_name\" name=\"first_name\" title=\"Please Enter your First name.\" value=\"%(first_name)s\" />\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"last_name\">Last Name</label>\
                                                <input type=\"text\" id=\"last_name\" name=\"last_name\" title=\"Please Enter your Last name.\" value=\"%(last_name)s\" />\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"company\">Company</label>\
                                                <input type=\"text\" id=\"company\" name=\"company\" title=\"Please Enter your Company Name.\" value=\"%(company)s\" />\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"designation\">Designation</label>\
                                                <input type=\"text\" id=\"designation\" name=\"designation\" title=\"Please Enter your Designation.\" value=\"%(designation)s\" />\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"address\">Address</label>\
                                                <textarea id=\"address\" name=\"address\" title=\"Please Enter your own Address.\" >%(address)s</textarea>\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"mobile\">Mobile Number</label>\
                                                <input type=\"text\" id=\"mobile\" name=\"mobile\" title=\"Please Enter your Mobile Number<br/> Does't include +91 or 0.\"/ value=\"%(mobile)s\" >\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl lbl-big\" for=\"email_id\">E-Mail ID</label>\
                                                <input type=\"text\" id=\"email_id\" name=\"email_id\" title=\"Please Enter your E-Mail ID.\" value=\"%(email_id)s\" />\
                                            </div>\
        				    <div class=\"row-elem\">\
        		                            <label class=\"lbl lbl-big\" for=\"new_password\">New Password</label>\
        		                            <input type=\"password\" id=\"new_password\" name=\"new_password\" title=\"Assign New Password to User OR <br/> leave blank if doesn't want to change it <br/> Must be at least 6 characters. <br/>Must be alphabet + numeric\"/>\
                                            </div>\
                                            <div class=\"row-elem\">\
                	                            <label class=\"lbl lbl-big\" for=\"cpassword\">Confirm Password</label>\
                	                            <input type=\"password\" id=\"cpassword\" name=\"cpassword\" title=\"Must be same as Password\"/>\
                                            </div>\
                                        </div>\
                                    </div>\
                                    <div class=\"form-div-footer\">\
                                            <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"edit\">Save</span></button>\
                                            <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_edit_user\"><span class=\"cancel\">Cancel</span></button>\
                                    </div>\
                                </form>"%user_detail_dict
                html.write(form_str)
            elif user_detail_dict == 11:
                html.write("NOUSERAVAILABLEWITHTHISID")
            else:
                html.write("SOMEERROROCCURMAYBEDBERROR")
        elif grp_flag == 1:
            html.write("SUPERADMINCANNOTEDIT")          
        else:
            html.write("SOMEERROROCCURMAYBEDBERROR")                           
    else:
        html.write("CANNOTEDITYOURSELF")
#    html.write(str(user_detail_dict))


def edit_group_view(h):
    global html
    html = h
    o_dict = {}
    _dict = type(o_dict)  
    group_id = html.var('group_id')
    grp_flag = 0
    grp_name = usr_mgt_bll.get_group_name(group_id,1)
    if grp_name == "SuperAdmin":
        grp_flag = 1

    result_json = {}

    if grp_flag == 0:
        group_detail_dict = usr_mgt_bll.edit_group_view(group_id)

        if type(group_detail_dict) == _dict:
            group_detail_dict.update({'role_list':roles_select_list(group_detail_dict['role_id'])})
            form_str = "<form action=\"edit_group.py\" method=\"get\" id=\"edit_group_form\" name=\"edit_user_form\">\
                                <div class=\"form-div\">\
				        <table cellspacing=\"0\" cellpadding=\"0\" width=\"100%%\" class=\"tt-table\">\
					    <tbody><tr><th class=\"cell-title\" id=\"form_title\">Edit Group</th></tr></tbody>\
				        </table>\
                                        <div class=\"row-elem\">\
                                            <label class=\"lbl lbl-big\" for=\"groupname\">Group Name</label>\
                                            <input type=\"text\" id=\"group_name\" name=\"group_name\" readonly=\"readonly\" title=\"Choose Unique Group Name. <br/>Must be at least 4 characters, No Space.\" value=\"%(group_name)s\" />\
                                            <input type=\"hidden\" id=\"group_id\" name=\"group_id\" value=\"%(group_id)s\" />\
                                        </div>\
                                        <div class=\"row-elem\">\
                                            <label class=\"lbl lbl-big\" for=\"description\">Description</label>\
                                            <textarea id=\"description\" name=\"description\" title=\"Group Description\" >%(description)s</textarea>\
                                        </div>\
                                        <div class=\"row-elem\">\
                                            <label class=\"lbl lbl-big\" for=\"role\" title=\"Select Role\">Select Role</label>%(role_list)s\
                                        </div>\
			         </div>\
                                 <div class=\"form-div-footer\">\
                                        <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"edit\">Edit</span></button>\
                                        <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_edit_group\"><span class=\"cancel\">Cancel</span></button>\
                                 </div>\
                            </form>"%group_detail_dict
            html.write(form_str)
        elif group_detail_dict == 11:
            html.write("NOUSERAVAILABLEWITHTHISID")
        else:
            html.write("SOMEERROROCCURMAYBEDBERROR")
    elif grp_flag == 1:
        html.write("CANNOTEDITSUPERADMIN")
    else:
        html.write("SOMEERROROCCURMAYBEDBERROR")                    


def edit_group(h):
    global html
    html = h
    #var_list = ['group_id','description','role']
    var_list = ['group_id','description']
    #var_dict_ul = {}
    var_dict = {}
    #var_dict_ug = {}
    flag = 1
    for i in var_list:
        if special_check(html.var(i)) == 0:
            flag = 0
            var_dict[i] = html.var(i)
        else:
            flag = 1
            break

    result = 1    
    result_json = {}
    session_user = html.req.session['username']
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    var_dict['session_user'] = session_user    
    if flag == 0:    
        result = usr_mgt_bll.edit_group(var_dict)
    else:
        result_json['success'] = 1
        result_json['result'] = " Some field contains special characters "


    if result == 0:
        result_json['success'] = 0
        info_str = " Group %s has been Updated \n New Details "%html.var('group_name')
        info_str += " role : "+html.var('role_name')
        if html.var('description').strip() != '':
            info_str += ", description : "+html.var('description')
        el = EventLog()
        el.log_event(info_str,session_user)

    elif flag == 0:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)

    html.write(str(result_json))


def check_name(h):
    global html
    html = h
    name = html.var("name")
    type = html.var("type")
    result = 1
    __space = 1
    if space_check(name) == 0:
        __space = 0
    if __space == 0:
        if type == "user": # user
            result = usr_mgt_bll.check_name(name,"user")
        elif type == "group": # group
            result = usr_mgt_bll.check_name(name,"group")
        else:
            result = 1
    else:
        result = 1

    if result == 0:
        result = {'success':0}
    else:
        result = {'success':1}  

    html.write(str(result))  

def show_user_profile(h):
    #same as edit_ser_view but all fields are disabled now 
    pass

def add_useringp_view(h):
    global html
    html = h 
    gp_id = html.var("gp_id")  
    html_str = "<div><div class=\"user-group-th\" id=\"selectGroupDiv\">\
                            Select Group" + groups_select_list("Default",gp_id) + "\
                        </div>\
                        <div id=\"user_ingp_head\" class=\"user-group-th\" >\
                            <Strong>Users In Group</Strong><span id=\"search_user_gp\"> Search: <input type=\"text\" id=\"search_user_gp\" ></span> \
                        </div>\
                        <div id=\"users_in_grp\">\
                        </div>\
                        <div>\
                            <button type=\"submit\" class=\"yo-small yo-button\" onclick=\"boxAddUsers();\"><span class=\"add\" >Add</span></button>\
                            <button type=\"button\" class=\"yo-small yo-button\" id=\"selectAll\" onclick=\"\"><span class=\"ok\" >check all</span></button>\
                        </div>\
                </div>"
    html.write(html_str)



def move_usertogp_view(h):
    global html
    html = h   
    gp_id = html.var("gp_id")
    html_str = "<div><div class=\"user-group-th\" id=\"selectGroupDiv\">\
                            Select Group " + groups_select_list("",gp_id,"Default") + "\
                        </div>\
                        <div>\
                            <button type=\"submit\" class=\"yo-small yo-button\" onclick=\"boxMoveUsers();\"><span class=\"moveto\">Move</span></button>\
                        </div>\
                </div>"
    html.write(html_str)

def edit_user(h):
    global html
    html = h
    lb = LicenseBll()
    ugroup = html.var('grp_name')
    user_id = html.var('user_id')
    result_json = {}
    lb_result = lb.check_license_for_group(ugroup,user_id)
    #html.write(str(lb_result)+str(ugroup))
    if lb_result == True:    
        var_list = ['user_id','first_name','last_name','groups','company','designation','address','mobile','email_id']
        #var_dict_ul = {}
        var_dict = {}
        var_dict_ug = {}
        for i in var_list:
            if i == 'groups':
                var_dict_ug[i] = html.var(i)
            elif i == 'user_id':
                var_dict_ug[i] = html.var(i)
                var_dict[i] = html.var(i)
            else:
                var_dict[i] = html.var(i)

        #html.write(str(var_dict)+str(var_dict_rg))
        if html.var('new_password'):
            passwd_dict = {}
            passwd_dict['passwd'] = html.var('new_password') 
            passwd_dict['user_id'] = html.var('user_id') 
            result = usr_mgt_bll.edit_user(var_dict,var_dict_ug,passwd_dict)
        else:
            result = usr_mgt_bll.edit_user(var_dict,var_dict_ug)

        session_user = html.req.session['username']
        if session_user:
            pass
        else:
            session_user = "NotAvailable"
        if result == 0:
            result_json['success'] = 0
            #f = open("/home/nms/Desktop/event.rg","a")
            #f.write("\nEdit var_dict "+html.var('grp_name')+"\n")
            #f.flush()
            #f.close()
            info_str = " User %s has been Updated \n New Details "%html.var('user_name')
            var_dict.pop('user_id')
            info_str += " group : "+html.var('grp_name')
            for i in var_dict:
                if var_dict[i].strip() != '':
                    info_str += ", "+i
                    info_str += ": "+var_dict[i]
            el = EventLog()
            el.log_event(info_str,session_user)


        else:
            result_json['success'] = 1
            result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)

    else:
        result_json['success'] = 1
        result_json['result'] = "Maximum number of allowed users of a type %s have reached"%(ugroup)

    html.write(str(result_json))


def change_password(h):
    global html
    html = h
    var_tuple = ('user_id','user_name','old_password','password')
    var_dict = []
    for i in var_tuple:
        var_dict[i] = html.var(i)

    result_json = {}

    result = usr_mgt_bll.change_password(var_dict)

    if result == 0:
        result_json['success'] = 0
    elif result == 100:
        result_json['success'] = 1
        result_json['result'] = " Old Password didn't match "
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)

    html.write(str(result_json))

    pass              

def del_user(h):
    global html
    html = h
    user_names = html.var("user_names")
    session_user =  html.req.session['username']  
    result_json = {}
    user_names_list = user_names.split(",")
    grp_flag = 0
    if user_names_list.count(session_user) == 0:
        session_users_list = usr_mgt_bll.is_loggedin_users(user_names_list)
        if isinstance(session_users_list,list):
            result_json['success'] = 1
            result_json['result'] = " User(s) %s logged in. <BR>Deleting of logged in user is restricted"%(''.join(session_users_list))                        
            html.write(str(result_json))            
        else:        
            user_ids = html.var("user_ids")
            user_ids_list = user_ids.split(",")
            sess_grp_name = html.req.session['group']                  
            if sess_grp_name.lower() != "superadmin":
                for user_id in user_ids_list:
                    grp_name = usr_mgt_bll.get_group_name(user_id)
                    if grp_name == "SuperAdmin":
                        grp_flag = 1
                        break

            if grp_flag == 0:                
                result = usr_mgt_bll.del_user(user_ids_list)                   
                if result == 0:
                    result_json['success'] = 0
                    result_json['result'] = str(user_names)+str(session_user)
                    info_str = " User(s) %s has been Deleted"%user_names
                    el = EventLog()
                    el.log_event(info_str,session_user)
                else:
                    result_json['success'] = 1
                    result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)

                html.write(str(result_json))
            elif grp_flag == 1:
                result_json['success'] = 1
                result_json['result'] = " Deleting SuperAdmin type user is not allowed."                        
                html.write(str(result_json))
            else:
                result_json['success'] = 1
                result_json['result'] = " Remain unchanged error code : '%s' "%str(grp_flag)                        
                html.write(str(result_json))                   
    else:
        result_json['success'] = 1
        result_json['result'] = " Self deletion is restricted"
        html.write(str(result_json))



def del_group(h):
    global html
    html = h
    group_id = html.var("group_id")
    #group_ids_list = group_ids.split(",")
    grp_flag = 0
    selfgrp_name = html.req.session["group"]
    grp_name = usr_mgt_bll.get_group_name(group_id,1)

    if grp_name == selfgrp_name:
        grp_flag = 2

    if grp_name == "SuperAdmin":
        grp_flag = 1

    result_json = {}

    if grp_flag == 0:
        result = usr_mgt_bll.del_group(group_id,0) 

        if result == 0:
            result_json['success'] = 0

        else:
            result_json['success'] = 1
            result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)
    elif grp_flag == 1:
        result_json['success'] = 1
        result_json['result'] = " Can not delete SuperAdmin group "                        
    elif grp_flag == 2:
        result_json['success'] = 1
        result_json['result'] = " Can not delete your assigned group "                                
    else:
        result_json['success'] = 1
        result_json['result'] = " Remain unchanged error code : '%s' "%str(grp_flag)              

    html.write(str(result_json))


def user_detail_table(h):
    global html
    html = h
    table = usr_mgt_bll.get_user_details()
    if table == 1:
        table = []
    html.write(str(table))

def group_user_view(h):
    global html
    html = h
    css_list = ["css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/pages/group_mgt.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addGroup();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_group\" name=\"add_group\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Group\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editGroup();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_group\" name=\"edit_group\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Group\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delGroup();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_group\" name=\"del_group\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Group\"></div>" % theme
    #all_btn = del_btn + edit_btn + add_btn
    all_btn = edit_btn
    html.new_header("User Group Management","manage_group.py",all_btn,css_list,javascript_list)
    html.write("\
	<table id=\"group_datatable\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\
		<colgroup>\
			<col width=\"150px\" style=\"width:150px;\"/>\
			<col width=\"auto\" style=\"width:auto;\"/>\
		</colgroup>\
		<tr style=\"background-color:#AAA;height:35px;\">\
			<th align=\"left\" style=\"padding-left:10px;border-right:1px solid #666;border-bottom:1px solid #666;\">\
				Group Name\
			</th>\
			<th align=\"left\" style=\"padding-left:10px;border-bottom:1px solid #666;\">\
				Group Details\
			</th>\
		</tr>\
		<tr>\
			<td rowspan=\"2\">\
				<div style=\"display:block;border-right:1px solid #CCCCCC;background-color:#F1F1F1;font-size:10px;\">\
		                        <div id=\"group_name_div\" style=\"display:bolck;width:100%;\">\
					</div>\
                        	</div>\
			</td>\
			<td>\
				<div id=\"group_info\" style=\"display:block;\">\
	                         </div>\
			</td>\
		</tr>\
		<tr>\
			<td>\
			<div id=\"group_users\" class=\"group-links\" style=\"border-bottom:1px solid #CCCCCC;display:block;\">\
                             <div id=\"user_ingrp_head\" class=\"user-group-th\" >\
                                <Strong>Users in Group</Strong><span id=\"search_user\" style=\"float:right;\"> Search: <input type=\"text\" id=\"search_User\" ></span> \
                            </div>\
                            <div id=\"users_ingrp\">\
                            </div>\
                            <div id=\"status-header\">\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"add_user_to_group\" type=\"button\" onclick=\"addUsrToGrp();\" ><span class=\"add\">Add</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" type=\"button\" onclick=\"delUsrFrmGrp();\" ><span class=\"delete\" >Delete</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"move_user_to_group\" type=\"button\" onclick=\"moveUsrToGrp();\" ><span class=\"moveto\" >Move</span></button>\
                                </div>\
                            </div>\
                         </div>\
			</td>\
		</tr>\
	</table>\
	<div id=\"group_form\" style=\"display:none;\">\
                    <form action=\"add_group.py\" method=\"get\" id=\"add_group_form\" name=\"add_group_form\">\
                        <div class=\"form-div\">\
                            <div class=\"form-body\">\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"groupname\">Group Name</label>\
                                    <input type=\"text\" id=\"group_name\" name=\"group_name\" title=\"Choose Unique Group Name. <br/>Must be at least 4 characters, No Space.\" onblur=\"name_chk();\" />\
                                    <input type=\"button\" id=\"check_gname\" name=\"check_gname\" value=\"Check availability\" title=\"Check Group Name Availablity\" onclick=\"name_chk();\" />\
                                    <label id=\"check_result\" name=\"check_result\" style=\"margin:20px\" for=\"group_name\" ></label>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"description\">Description</label>\
                                    <textarea id=\"description\" name=\"description\" title=\"Group Description\"></textarea>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"role\" title=\"Select Role\" >Select Role</label>" + roles_select_list("") + "\
                                </div>\
                            </div>\
                        </div>\
                        <div class=\"form-div-footer\">\
                            <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"add\">Add</span></button>\
                            <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_add_group\"><span class=\"cancel\">Cancel</span></button>\
                        </div>\
                    </form>\
                </div>\
                <div id=\"edit_grp_form\" style=\"display:none;\">\
                </div>")
    html.new_footer()


def group_table(h):
    global html
    html = h
    group_str = ""
    sess_gp_name = html.req.session['group']   
    if sess_gp_name.lower() != 'superadmin':
        table = usr_mgt_bll.get_group_details()
    else:
        table = usr_mgt_bll.get_group_details(0) # is superadmin
    if table == 1:
        group_str +="<p style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;> Well, its really embarasing But its seems there is No data availabe. Sorry</p>"
    else:
        for tup in table:
            group_str += "<p class=\"gp-name\" style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;\" id=\"%s\" >%s</p>"%tup
    html.write(group_str)


def groups_select_list(selectedGroup,gp_id = "",gp_name = ""):
    global html
    sess_gp_name = html.req.session['group']   
    selectString = "<select id=\"groups\" name=\"groups\" title=\"Select Group\"><option value=\"\" class='required' >-- Select Group --</option>"
    groups_list = usr_mgt_bll.get_group_list()

    if sess_gp_name.lower() != 'superadmin':
        gp_name += ",SuperAdmin"
    gp_name_list = gp_name.split(',')
    if groups_list == 1:
        pass
    else:
        for groupName in groups_list:
            if gp_id == str(groupName[1]):
                pass
            elif gp_name_list.count(str(groupName[0])) > 0:
                pass  
            elif selectedGroup == str(groupName[0]):

                selectString += "<option value=\"" + str(groupName[1]) + "\" selected=\"selected\">" + str(groupName[0]) + "</option>"
            else:

                selectString += "<option value=\"" + str(groupName[1]) + "\">" + str(groupName[0]) + "</option>"
    selectString += "</select>"
    return selectString

def hostgroups_select_list(selectedGroup,gp_id=""):
    global html
    sess_grp_name = html.req.session['group']                  
    hg_ids_list = []
    flag = 0
    if sess_grp_name.lower() != "superadmin":
        flag = 1
        user_id = html.req.session['user_id']                      
        es = Essential()
        hg_ids_list = es.get_hostgroup_ids(user_id)    
        if hg_ids_list.count(gp_id) > 0:
            hg_ids_list.remove(gp_id)
    selectString = "<select id=\"groups\" name=\"groups\" title=\"Select Hostgroup\"><option value=\"\" class='required' >-- Select Hostgroup --</option>"
    groups_list = usr_mgt_bll.get_hostgroup_list()
    if groups_list == 1:
        pass
    else:
        for groupName in groups_list:
            if gp_id == str(groupName[1]):
                pass              
            elif hg_ids_list.count(str(groupName[1])) == 0 and flag == 1:
                pass
            elif selectedGroup == str(groupName[0]):
                selectString += "<option value=\"" + str(groupName[1]) + "\" selected=\"selected\">" + str(groupName[0]) + "</option>"
            else:
                selectString += "<option value=\"" + str(groupName[1]) + "\">" + str(groupName[0]) + "</option>"
    selectString += "</select>"
    return selectString

def roles_select_list(selectedRole):
    selectString = "<select id=\"role\" name=\"role\"  disabled=\"disabled\" onchange=\"this.selectedIndex = 1;\" title=\"Select Role\"><option value=\"\" class='required' >-- Select Role --</option>"
    role_list = usr_mgt_bll.get_role_list()
    #role_list = ['Admin','Operator','Guest']
    if role_list == 1:
        pass
    else:
        for roleName in role_list:
            if selectedRole == str(roleName[1]):
                selectString += "<option value=\"" + str(roleName[1]) + "\" selected=\"selected\">" + str(roleName[0]) + "</option>"
            else:
                selectString += "<option value=\"" + str(roleName[1]) + "\">" + str(roleName[0]) + "</option>"
    selectString += "</select>"
    return selectString


def group_to_hg_view(h):
    global html
    html = h
    css_list = ["css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/pages/group_mgt.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addGroup();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_group\" name=\"add_group\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Group\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editGroup();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_group\" name=\"edit_group\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit Group\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delGroup();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_group\" name=\"del_group\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Group\"></div>" % theme
    #all_btn = del_btn + edit_btn + add_btn
    all_btn = edit_btn
    html.new_header("Group to HostGroup Management","manage_group.py",all_btn,css_list,javascript_list)
    html.write("<table id=\"group_datatable\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\
		<colgroup>\
			<col width=\"150px\" style=\"width:150px;\"/>\
			<col width=\"auto\" style=\"width:auto;\"/>\
		</colgroup>\
		<tr style=\"background-color:#AAA;height:35px;\">\
			<th align=\"left\" style=\"padding-left:10px;border-right:1px solid #666;border-bottom:1px solid #666;\">\
				Group Name\
			</th>\
			<th align=\"left\" style=\"padding-left:10px;border-bottom:1px solid #666;\">\
				Group Details\
			</th>\
		</tr>\
		<tr>\
			<td rowspan=\"2\">\
				<div style=\"display:block;border-right:1px solid #CCCCCC;background-color:#F1F1F1;font-size:10px;\">\
		                        <div id=\"group_name_div\" style=\"display:bolck;width:100%;\">\
					</div>\
                        	</div>\
			</td>\
			<td>\
				<div id=\"group_info\" style=\"display:block;\">\
	                         </div>\
			</td>\
		</tr>\
		<tr>\
			<td>\
<div id=\"group_hostgroups\" class=\"group-links\" style=\"border-bottom:1px solid #CCCCCC;display:block;\">\
                             <div id=\"hg_ingrp_head\" class=\"user-group-th\" >\
                                <Strong>Hostgroups Assign to Group</Strong><span id=\"search_hg_gp\" style=\"float:right;\"> Search: <input type=\"text\" id=\"search_hg_gp\" ></span> \
                            </div>\
                             <div id=\"hg_ingp\" >\
                             </div>\
                             <div id=\"status-header\">\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"add_hg_to_group\" type=\"button\" onclick=\"addHgToGrp();\" ><span class=\"add\">Add</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" type=\"button\" onclick=\"delHgFrmGrp();\" ><span class=\"delete\"  >Delete</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"move_hg_to_group\" type=\"button\" onclick=\"moveHgToGrp();\" ><span class=\"moveto\" >Move</span></button>\
                                </div>\
                            </div>\
                         </div>\
                </td>\
		</tr>\
	</table>\
	<div id=\"group_form\" style=\"display:none;\">\
                    <form action=\"add_group.py\" method=\"get\" id=\"add_group_form\" name=\"add_group_form\">\
                        <div class=\"form-div\">\
                            <div class=\"form-body\">\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"groupname\">Group Name</label>\
                                    <input type=\"text\" id=\"group_name\" name=\"group_name\" title=\"Choose Unique Group Name. <br/>Must be at least 4 characters, No Space.\" onblur=\"name_chk();\" />\
                                    <input type=\"button\" id=\"check_gname\" name=\"check_gname\" value=\"Check availability\" title=\"Check Group Name Availablity\" onclick=\"name_chk();\" />\
                                    <label id=\"check_result\" name=\"check_result\" style=\"margin:20px\" for=\"group_name\"></label>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"description\">Description</label>\
                                    <textarea id=\"description\" name=\"description\" title=\"Group Description\"></textarea>\
                                </div>\
                                <div class=\"row-elem\">\
                                    <label class=\"lbl lbl-big\" for=\"role\" title=\"Select Role\" >Select Role</label>" + roles_select_list("") + "\
                                </div>\
                            </div>\
                        </div>\
                        <div class=\"form-div-footer\">\
                            <button type=\"submit\" class=\"yo-small yo-button\"><span class=\"add\">Add</span></button>\
                            <button type=\"reset\" class=\"yo-small yo-button\" id=\"close_add_group\"><span class=\"cancel\">Cancel</span></button>\
                        </div>\
                    </form>\
                </div>\
                <div id=\"edit_grp_form\" style=\"display:none;\">\
                </div>")
    html.new_footer()


def group_hostgroups1(h):
    global html
    html = h
    light_box = html.var("light_box")
    group_id = html.var("group_id")
    all = html.var("all")
    table = usr_mgt_bll.show_hostgroups(group_id)
    if table == 1 :
        html.write("[]")
    else:
        make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
        gpHG_list = []
        for gpHG in table:
            gpHG_list.append(make_list(gpHG))

        html.write(str(gpHG_list))

def show_hostgroups(h):
    global html
    html = h
    tup__ = ()
    tup__ = type(tup__)
    light_box = html.var("light_box")
    group_id = html.var("group_id")
    all = html.var("all")
    if all == "0": 
        table = usr_mgt_bll.show_hostgroups(group_id,0)
        #html.write(str(table))
    else:
        table = usr_mgt_bll.show_hostgroups(group_id)
        #html.write(str(table))

    if type(table) == tup__:
        if len(table) < 1:
            gpHG_list = []
        else:
            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            gpHG_list = []
            for gpHG in table:
                gpHG_list.append(make_list(gpHG))
    else:
        gpHG_list = table
    html.write(str(gpHG_list))


def add_hgingp_view(h):
    """
        generate view for light box
    """
    global html
    #Select Group" + groups_select_list("") + "<input type=\"button\" value=\"Show All Hostgroup\" onclick=\"show_all_hg();\" />\
    #<div class=\"user-group-th\" id=\"selectGroupDiv\" ><input type=\"button\" value=\"Show All Hostgroup\" onclick=\"show_all_hg();\" /> </div>
    html = h   
    html_str = "<div>\
                        <div id=\"hg_ingrp_head\" class=\"user-group-th\" >\
                        <Strong>Hostgroups Assign to Group</Strong><span id=\"search_hg\" style=\"float:right;\"> Search: <input type=\"text\" id=\"search_hg\" ></span> \
                        </div>\
                        <div id=\"hostgroups_in_grp\">\
                        </div>\
                        <div>\
                            <button type=\"submit\" class=\"yo-small yo-button\" onclick=\"boxAddHg();\"><span class=\"add\" >Add</span></button>\
                            <button type=\"button\" class=\"yo-small yo-button\" id=\"selectAll\" onclick=\"\"><span class=\"ok\" >check all</span></button>\
                        </div>\
                </div>"
    html.write(html_str)


def add_hostgroup_togroup(h):
    global html
    html = h
    hg_ids = html.var("hg_ids")
    newGroupID = html.var("group_id")

    result,flag = 1,1
    if hg_ids != '':
        hg_ids_list = hg_ids.split(",")
        result = usr_mgt_bll.add_hg_togroup(hg_ids_list,newGroupID)
    else:
        else_str = "Remain Unchanged No Hostgroup Selected"
        flag = 0

    result_json = {}
    session_user = html.req.session['username']
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    if flag == 0:         
        result_json['success'] = 0
        result_json['result'] = else_str
    elif result == 0:
        result_json['success'] = 0
        hg_names = html.var('hg_names')
        grp_name = html.var('grp_name')
        info_str = " Hostgroups: %s have been assigned to Group: %s"%(hg_names,grp_name)
        el = EventLog()
        el.log_event(info_str,session_user)
    elif flag == 1 and result == 1:
        result_json['success'] = 1
        result_json['result'] = " Some field contains special characters (like \" \, etc.) "
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "  

    html.write(str(result_json))


def add_group_tohostgroup(h):
    global html
    html = h
    gp_ids = html.var("gp_ids")
    newHgroupID = html.var("hostgroup_id")

    result,flag = 1,1
    if gp_ids != '':
        gp_ids_list = gp_ids.split(",")
        result = usr_mgt_bll.add_gp_tohostgroup(gp_ids_list,newHgroupID)
    else:
        else_str = "Remain Unchanged No Hostgroup Selected"
        flag = 0

    result_json = {}
    session_user = html.req.session['username']
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    if flag == 0:         
        result_json['success'] = 0
        result_json['result'] = else_str
    elif result == 0:
        result_json['success'] = 0
        hg_name = html.var('hg_name')
        grp_names = html.var('grp_names')
        info_str = " Groups: %s have been assigned to Hostroup: %s"%(grp_names,hg_name)
        el = EventLog()
        el.log_event(info_str,session_user)
    elif flag == 1 and result == 1:
        result_json['success'] = 1
        result_json['result'] = " Some field contains special characters (like \" \, etc.) "
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   " +result 

    html.write(str(result_json))

def move_group_tohostgroup(h):
    global html
    html = h
    gp_ids = html.var("gp_ids")
    gp_ids_list = gp_ids.split(",")
    session_group = html.req.session['group']
    grp_flag = 0
    if session_group.lower() != "SuperAdmin".lower():
        for grp_id in gp_ids_list:
            grp_name = usr_mgt_bll.get_group_name(grp_id,1)
            if grp_name == "SuperAdmin":
                grp_flag = 1
                break   
    result_json = {}
    if grp_flag == 0:
        newHgroupID = html.var("hostgroup_id")
        oldHgroupID = html.var("old_hostgroup_id") 
        result,flag = 1,1
        if gp_ids != '':
            gp_ids_list = gp_ids.split(",")
            result = usr_mgt_bll.move_group_tohg(gp_ids_list,newHgroupID,oldHgroupID)
        else:
            else_str = "Remain Unchanged No Hostgroup Selected"
            flag = 0

        result_json = {}
        session_user = html.req.session['username']
        if session_user:
            pass
        else:
            session_user = "NotAvailable"
        if flag == 0:         
            result_json['success'] = 0
            result_json['result'] = else_str
        elif result == 0:
            result_json['success'] = 0
            hg_name = html.var('hg_name')
            grp_names = html.var('grp_names')
            sel_hg = html.var('sel_hg')
            info_str = " Groups: %s have been re-assigned from Hostgroup: %s to Hostgroup: %s"%(grp_names,sel_hg,hg_name)
            el = EventLog()
            el.log_event(info_str,session_user)

        elif flag == 1 and result == 1:
            result_json['success'] = 1
            result_json['result'] = " Some field contains special characters (like \" \, etc.) "
        else:
            result_json['success'] = 1
            result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code  "+result  

    else:
        result_json['success'] = 1
        result_json['result'] = " Can not perform operation on SuperAdmin group "            
    html.write(str(result_json))


def move_hostgroup_togroup(h):
    global html
    html = h
    hg_ids = html.var("hg_ids")
    newGroupID = html.var("group_id")
    oldGroupID = html.var("old_group_id") 
    result,flag = 1,1

    if hg_ids != '':
        hg_ids_list = hg_ids.split(",")
        result = usr_mgt_bll.move_hg_togroup(hg_ids_list,newGroupID,oldGroupID)
    else:
        else_str = "Remain Unchanged No Hostgroup Selected"
        flag = 0

    result_json = {}
    session_user = html.req.session['username']
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    if flag == 0:         
        result_json['success'] = 0
        result_json['result'] = else_str
    elif result == 0:
        result_json['success'] = 0
        hg_names = html.var('hg_names')
        grp_name = html.var('grp_name')
        sel_group = html.var('sel_group')
        info_str = " Hostgroups: %s have been re-assigned from Group: %s to Group: %s"%(hg_names,sel_group,grp_name)
        el = EventLog()
        el.log_event(info_str,session_user)
    elif flag == 1 and result == 1:
        result_json['success'] = 1
        result_json['result'] = " Some field contains special characters (like \" \, etc.) "
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   " +result 

    html.write(str(result_json))


def move_hgtogp_view(h):
    global html
    html = h   
    gp_id = html.var("gp_id")
    html_str = "<div><div class=\"user-group-th\" id=\"selectGroupDiv\">\
                            Select Group" + groups_select_list("",gp_id,"Default") + "\
                        </div>\
                        <div>\
                            <button type=\"submit\" class=\"yo-small yo-button\" onclick=\"boxMoveHg();\"><span class=\"moveto\" >Move</span></button>\
                        </div>\
                </div>"
    html.write(html_str)   



def del_hostgroup_fromgroup(h):
    global html
    html = h
    result_json = {}
    hg_ids = html.var("hg_ids")
    groupID = html.var("group_id")
    hg_ids_list = hg_ids.split(",")
    result = usr_mgt_bll.del_hg_fromgroup(hg_ids_list,groupID)
    session_user = html.req.session['username']
    if session_user:
        pass
    else:
        session_user = "NotAvailable"
    if result == 0:
        result_json['success'] = 0
        hg_names = html.var('hg_names')
        grp_name = html.var('grp_name')
        info_str = " Hostgroups: %s have been removed from Group: %s"%(hg_names,grp_name)
        el = EventLog()
        el.log_event(info_str,session_user)        
    else:
        result_json['success'] = 1
        result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)

    html.write(str(result_json))

def del_group_fromhostgroup(h):
    global html
    html = h
    result_json = {}
    gp_ids = html.var("gp_ids")
    gp_ids_list = gp_ids.split(",")
    session_group = html.req.session['group']
    grp_flag = 0
    if session_group.lower() != "SuperAdmin".lower():
        for grp_id in gp_ids_list:
            grp_name = usr_mgt_bll.get_group_name(grp_id,1)
            if grp_name == "SuperAdmin":
                grp_flag = 1
                break   
    result_json = {}
    if grp_flag == 0:    
        hgroupID = html.var("hostgroup_id")
        result = usr_mgt_bll.del_gp_fromhostgroup(gp_ids_list,hgroupID)
        session_user = html.req.session['username']
        session_group = html.req.session['group']
        if session_user:
            pass
        else:
            session_user = "NotAvailable"
        if result == 0:
            result_json['success'] = 0
            hg_name = html.var('hg_name')
            grp_names = html.var('grp_names')
            info_str = " Groups: %s have been removed from Hostgroup: %s"%(grp_names,hg_name)
            el = EventLog()
            el.log_event(info_str,session_user)        
        else:
            result_json['success'] = 1
            result_json['result'] = " UNMP server has encounterd an error. Please REFRESH your page. still having problem contact support team. code   "+str(result)

    else:
        result_json['success'] = 1
        result_json['result'] = " Can not perform operation on SuperAdmin group "    
    html.write(str(result_json))
#=================================================================

def hostgroup_group_view(h):
    global html
    html = h
    css_list = ["css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/pages/hostgroup_mgt.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addHostGroup();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_hostgroup\" name=\"add_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add HostGroup\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editHostGroup();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_hostgroup\" name=\"edit_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit HostGroup\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delHostGroup();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_hostgroup\" name=\"del_hostgroup\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete HostGroup\"></div>" % theme
    #all_btn = del_btn + edit_btn + add_btn
    all_btn = ""
    html.new_header("HostGroup to Group Management","manage_group.py",all_btn,css_list,javascript_list)
    html.write("<table id=\"hostgroup_table\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\
		<colgroup>\
			<col width=\"150px\" style=\"width:150px;\"/>\
			<col width=\"auto\" style=\"width:auto;\"/>\
		</colgroup>\
		<tr style=\"background-color:#AAA;height:35px;\">\
			<th align=\"left\" style=\"padding-left:10px;border-right:1px solid #666;border-bottom:1px solid #666;\">\
				Hostgroup Name\
			</th>\
			<th align=\"left\" style=\"padding-left:10px;border-bottom:1px solid #666;\">\
				Hostgroup Details\
			</th>\
		</tr>\
		<tr>\
			<td rowspan=\"2\">\
				<div style=\"float:left;width:150px;height:100%;display:block;border-right:1px solid #CCCCCC;background-color:#F1F1F1;position:relative;font-size:10px;\">\
                        <div id=\"hostgroup_name_div\" style=\"display:bolck;width:100%;overflow-x:hidden;overflow-y:auto;\">\</div>\
                        </div>\
			</td>\
			<td>\
				<div id=\"hostgroup_info\" style=\"display:block;\">\
                         </div>\
			</td>\
		</tr>\
<tr>\
			<td>\
<div id=\"hostgroup_groups\" style=\"border-bottom:1px solid #CCCCCC;display:block;\">\
                             <div id=\"grp_inhg_head\" class=\"user-group-th\" >\
                                <Strong>Assign Groups to Hostgroup</Strong> <span id=\"search_grp_hg\" style=\"float:right;\"> Search: <input type=\"text\" id=\"search_grp_hg\" ></span> \
                            </div>\
                            <div id=\"grp_in_hg\" >\
                             </div>\
                             <div id=\"status-header\">\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"add_group_to_hg\" type=\"button\" ><span class=\"add\">Add</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" type=\"button\" onclick=\"delGrpFrmHg();\" ><span class=\"delete\" >Delete</span></button>\
                                </div>\
                                <div class=\"user-header-icon\">\
                                    <button class=\"yo-small yo-button\" id=\"move_group_to_hg\" type=\"button\" onclick=\"moveGrpToHg();\" ><span class=\"moveto\" >Move</span></button>\
                                </div>\
                            </div>\
                         </div>\
</td>\
		</tr>\
	</table>\
")
    html.new_footer()


def hostgroup_table(h):
    global html
    html = h
    hostgroup_str = ""
    table = usr_mgt_bll.get_hostgroup_details()
    if table == 1:
        hostgroup_str +="<p style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;> Well, its really embarasing But its seems there is No data availabe. Sorry</p>"
    else:
        for tup in table:
            hostgroup_str += "<p class=\"hg-name\" style=\"border-bottom:1px solid #DDD;padding:5px 10px;height:18px;\" id=\"%s\" >%s</p>"%tup
    html.write(hostgroup_str)

def hostgroup_info(h):
    global html
    html = h
    table = usr_mgt_bll.get_hostgroup_info(html.var("hostgroup_id"))
    hostgroup_str = ""
    hostgroup_str += "<table cellspacing=\"0\" width=\"100%\" cellpadding=\"0\" class=\"tt-table\" style=\"margin-bottom:0;\">\
                             <tbody><tr>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Alias</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Updated By</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Update Time</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Created By</td>\
                                        <th class=\"cell-title\" style=\"text-align:left;\">Creation Time</td>\
                                     </tr>"

    if table == 1:
        hostgroup_str +="<tr> Well, its really embarrasing But it seems there is No data availabe. Sorry </tr>"
    else:
        hostgroup_str += "<tr>"
        for tup in table:
            hostgroup_str += "<td class=\"cell-info1\">%s</td>"%tup
        hostgroup_str += "</tr>"
    hostgroup_str +="</tbody></table> "
    html.write(hostgroup_str)

def hostgroup_groups(h):
    global html
    html = h
    light_box = html.var("light_box")
    table = usr_mgt_bll.show_groups(html.var("hostgroup_id"))

    hostgroup_str = "<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" class=\"tt-table\"><tbody><tr> <th colspan=\"4\" class=\"user-group-th\"> Groups Assign to Hostgroup <span style=\"float:right;\"> Search: <input type=\"text\"></span></th>  </tr>"
    if table == 1:
        hostgroup_str +="<tr><td colspan=\"4\"> No User In this Group, click on Add for add user </td><tr>"

    else:
        mod = 3-(len(table)%3) 
        devide = (len(table)/3)*3
        i = 0

        if len(table) <= 3:
            mod = 3-len(table)    
        else:

            hostgroup_str += "<tr>"
            for tup in table:
                i += 1
                hostgroup_str += "<td class=\"cell-info1\"><input type=\"checkbox\" name=\"group_check\" value=\"%s\"/> %s </td>"%tup
                if i == devide :
                    hostgroup_str += "</tr>"
                    break
                if i%3 == 0:
                    hostgroup_str += "</tr><tr>"   

        if i < len(table):
            hostgroup_str += "<tr>"
            for j in xrange(i,len(table)):
                hostgroup_str += "<td class=\"cell-info1\"><input type=\"checkbox\" name=\"group_check\" value=\"%s\"/> %s </td>"%table[j]     

            for i in xrange(0,mod):
                hostgroup_str += "<td class=\"cell-info1\"></td>"
            hostgroup_str += "</tr>"

    hostgroup_str +="</tbody></table>"
    if light_box == None:
        hostgroup_str += "<div id=\"status-header\">\
                        <div class=\"user-header-icon\">\
                            <button class=\"yo-small yo-button\" id=\"add_group_to_hg\" type=\"button\" ><span class=\"add\">Add</span></button>\
                        </div>\
                        <div class=\"user-header-icon\">\
                            <button class=\"yo-small yo-button\" type=\"button\" onclick=\"delGrpFrmHg();\" ><span class=\"delete\" >Delete</span></button>\
                        </div>\
                        <div class=\"user-header-icon\">\
                            <button class=\"yo-small yo-button\" id=\"move_group_to_hg\" type=\"button\" onclick=\"moveGrpToHg();\" ><span class=\"moveto\" >Move</span></button>\
                        </div>\
                    </div>"

    html.write(hostgroup_str)


def add_gpinhg_view(h):
    """
        generate view for light box
    """
    global html
    html = h   
    #Select Hostgroup" + hostgroups_select_list("") + "
    html_str = "<div><div id=\"grp_inhg_head\" class=\"user-group-th\" >\
                        <Strong>Assign Groups To Hostgroup</Strong><span id=\"search_grp\" style=\"float:right;\"> Search: <input type=\"text\" id=\"search_grp\" ></span> \
                        </div>\
                        <div id=\"groups_in_hg\">\
                        </div>\
                        <div>\
                            <button type=\"submit\" class=\"yo-small yo-button\" onclick=\"boxAddGrp();\"><span class=\"add\" >Add</span></button>\
                            <button type=\"button\" class=\"yo-small yo-button\" id=\"selectAll\" onclick=\"\"><span class=\"ok\" >check all</span></button>\
                        </div>\
                </div>"
    html.write(html_str)

def show_groups(h):
    global html
    html = h
    grp_value = 0
    sess_grp_name = html.req.session['group']
    if sess_grp_name.lower() == 'superadmin':
        grp_value = 1                      
    tup__ = ()
    tup__ = type(tup__)
    light_box = html.var("light_box")
    group_id = html.var("hostgroup_id")
    all_var = html.var("all")
    if all_var == "0": 
        table = usr_mgt_bll.show_groups(group_id,0,grp_value)
        #html.write(str(table))
    else:
        table = usr_mgt_bll.show_groups(group_id,1,grp_value)
        #html.write(str(table))

    if type(table) == tup__:
        if len(table) < 1:
            gpHG_list = []
        else:
            make_list = lambda x: [" - " if i == None or i == '' else str(i) for i in x]
            gpHG_list = []
            for gpHG in table:
                gpHG_list.append(make_list(gpHG))
    else:
        gpHG_list = table
    html.write(str(gpHG_list))

def move_gptohg_view(h):
    global html
    html = h   
    hg_id = html.var("hg_id")
    html_str = "<div><div class=\"user-group-th\" id=\"selectGroupDiv\">\
                            Select Host Group " + hostgroups_select_list("",hg_id) + "\
                        </div>\
                        <div>\
                            <button type=\"submit\" class=\"yo-small yo-button\" onclick=\"boxMoveGrp();\"><span class=\"moveto\" ></span><strong>Move</strong></button>\
                        </div>\
                </div>"
    html.write(html_str)

def manage_role(h):
    global html
    html = h
    css_list = ["css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/jquery.dataTables.min.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addUser();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_user\" name=\"add_user\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add User\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editUser();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_user\" name=\"edit_user\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit User\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delUser();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_user\" name=\"del_user_tip\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete User\"></div>" % theme
    all_btn = del_btn + edit_btn + add_btn
    all_btn = ""
    html.new_header("Manage Role","manage_role.py",all_btn,css_list,javascript_list)
    html.write("<p style=\"margin:10px;\">Page Under Progress...</p>")
    html.new_footer()

def user_settings(h):
    global html
    html = h
    css_list = ["css/demo_page.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css"]
    javascript_list = ["js/jquery.dataTables.min.js"]
    add_btn = "<div class=\"header-icon\"><img onclick=\"addUser();\" class=\"n-tip-image\" src=\"images/%s/round_plus.png\" id=\"add_user\" name=\"add_user\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add User\"></div>" % theme
    edit_btn = "<div class=\"header-icon\"><img onclick=\"editUser();\" class=\"n-tip-image\" src=\"images/%s/doc_edit.png\" id=\"edit_user\" name=\"edit_user\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Edit User\"></div>" % theme
    del_btn = "<div class=\"header-icon\"><img onclick=\"delUser();\" class=\"n-tip-image\" src=\"images/%s/round_minus.png\" id=\"del_user\" name=\"del_user_tip\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete User\"></div>" % theme
    all_btn = del_btn + edit_btn + add_btn
    all_btn = ""
    html.new_header("User Settings","",all_btn,css_list,javascript_list)
    html.write("<p style=\"margin:10px;\"><strong>User Name: </strong> omdadmin</p>")
    html.write("<p style=\"margin:10px;\"><strong>Role: </strong> Administrator</p>")
    html.new_footer()


def page_tip_user_main(h):
    global html
    html = h
    html_view = "\
        <div id=\"help_container\">\
        <h1>USER MANAGEMENT</h1>\
        <div>This page manages Users.</div>\
        <br/>\
        <div>On this page you can Add ,Edit or Delete Users.</div>\
        <br/>\
        <div><strong>Actions</strong></div>\
        <div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/{0}/round_plus.png\"/></div><div class=\"txt-div\">Add New User </div></div>\
        <div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/{0}/doc_edit.png\"/></div><div class=\"txt-div\">Edit User</div></div>\
        <div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/{0}/round_minus.png\"/></div><div class=\"txt-div\">Delete User</div></div>\
        <br/>\
        </div>".format(theme)
    html.write(str(html_view))


def page_tip_group_user(h):
    global html
    html = h
    html_view = "\
        <div id=\"help_container\">\
        <h1>GROUP MANAGEMENT</h1>\
        <div>This page manages groups and their users.</div>\
        <br/>\
        <div>On this page user can manages Users or Hostgroups releationships</div>\
        <br/>\
        <div><strong>Actions</strong></div>\
        <div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/%s/doc_edit.png\"/></div><div class=\"txt-div\">Edit Group</div></div>\
        <div><strong>Actions on Group</strong></div>\
        <div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"yo-small yo-button\" id=\"add_user_to_group\" type=\"button\"><span class=\"add\">Add</span></button>Add User From another Group.  </div></div></div>\
        <div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"yo-small yo-button\" type=\"button\"><span class=\"delete\"  >Delete</span></button>Delete User from Group</div></div></div>\
        <div class=\"action-tip\"><div class=\"txt-div\"> <div class=\"user-header-icon\"><button class=\"yo-small yo-button\" id=\"move_hg_to_group\" type=\"button\"><span class=\"moveto\" >Move</span></button>Move User to another Group</div></div></div>\
        <br/>\
        </div>" % theme
    html.write(str(html_view))


def page_tip_user_group(h):
    global html
    html = h
    html_view = "\
        <div id=\"help_container\">\
        <h1>GROUP MANAGEMENT</h1>\
        <div>This page manage Groups and their Users </div>\
        <br/>\
        <div>On this page you can Edit group. OR Manage Assigning of Users with selected Group</div>\
        <br/>\
        <div><strong>Actions</strong></div>\
        <div class=\"action-tip\"><div class=\"img-div\"><img style=\"width:16px;height:16px;\" src=\"images/{0}/doc_edit.png\"/></div><div class=\"txt-div\">Edit Group</div></div>\
        <br/>\
        <div><strong>Actions on Group</strong></div>\
        <div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"yo-small yo-button\" id=\"add_user_to_group\" type=\"button\"><span class=\"add\">Add</span></button>Add User From another Group </div></div></div>\
        <div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"yo-small yo-button\" type=\"button\"><span class=\"delete\"  >Delete</span></button>Delete User from Group : these deleted User will be assigned to Default System Group, Can be Re-assign by Add operation </div></div></div>\
        <div class=\"action-tip\"><div class=\"txt-div\"> <div class=\"user-header-icon\"><button class=\"yo-small yo-button\" id=\"move_hg_to_group\" type=\"button\"><span class=\"moveto\" >Move</span></button>Move User to another Group </div></div></div>\
        <br/>\
        </div>".format(theme)
    html.write(str(html_view))


def page_tip_hostgroup_group(h):
    global html
    html = h
    html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>HOSTGROUP MANAGEMENT</h1>"\
        "<div>This page manage HostGroup and their Mappping with Groups.</div>"\
        "<br/>"\
        "<div>On this page you can Assign Groups to Hostgroup.</div>"\
        "<br/>"\
        "<div><strong>Actions</strong></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"yo-small yo-button\" id=\"add_user_to_group\" type=\"button\"><span class=\"add\">Add</span></button>Assign Groups to Hostgroup.  </div></div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"><div class=\"user-header-icon\"><button class=\"yo-small yo-button\" type=\"button\"><span class=\"delete\" >delete</span></button>Remove Group from Hostgroup</div></div></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\"> <div class=\"user-header-icon\"><button class=\"yo-small yo-button\" id=\"move_hg_to_group\" type=\"button\"><span class=\"moveto\" >Move</span></button>Move Group to antoher HostGroup</div></div></div>"\
        "<br/>"\
        "</div>"
    html.write(str(html_view))
