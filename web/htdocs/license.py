#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 04-Nov-2011
@version: 0.1
@note: All Views That are use in License. 
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

class License(object):
    @staticmethod
    def manage_license(company="",date="",host=[0,0,0],hostgroup=[0,0,0],user=[0,0,0],usergroup=[0,0,0],host_device_type_list=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],user_type_list=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]):
        
        host_device_type = License.device_type(*tuple(host_device_type_list))
        user_type = License.user_type(*tuple(user_type_list))
        html_str = '\
        <div class="form-div">\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <thead>\
            <tr>\
            <th class="cell-title" colspan="2">\
                License Information\
            </th>\
            </tr>\
        </thead>\
        <tbody>\
            <tr>\
              <td class="cell-label">\
                Company Name\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
            </tr>\
            <tr>\
              <td class="cell-label">\
                Expires in\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
            </tr>\
        </tbody>\
        </table>\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <thead>\
            <tr>\
            <th class="cell-title cell-title2">\
                System Object\
            </th>\
            <th class="cell-title cell-title2">\
                 Allowed\
            </th>\
            <th class="cell-title cell-title2">\
                Used\
            </th>\
            <th class="cell-title cell-title2">\
                Remaining\
            </th>\
            </tr>\
        </thead>\
        <tbody>\
            <tr>\
              <td class="cell-label cell-label2" id="host" style="cursor:pointer;">\
                <span class="nxt" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">Host</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
            %s\
            <tr>\
              <td class="cell-label cell-label2" style="cursor:pointer;">\
                <span class="" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">Host Group</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
            <tr>\
              <td class="cell-label cell-label2" id="user" style="cursor:pointer;">\
                <span class="nxt" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">User</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
            %s\
            <tr>\
              <td class="cell-label cell-label2" style="cursor:pointer;">\
                <span class="" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">User Group</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
        </tbody>\
        </table>\
        </div>\
        <div class="form-div-footer">\
            <form action="license_upload.py" enctype=\"multipart/form-data\" method=\"post\">\
             <label class="lbl" style="margin-top:15px;">License File</label>\
             <input type="file" id="file_uploader" name="file_uploader" />\
             <button class="yo-button yo-small" type="file" id="button_uploader" name="button_uploader"><span class="upload">Upload</span></button>\
            </form>\
        </div>' % (company,date,host[0],host[1],host[2],host_device_type,hostgroup[0],hostgroup[1],hostgroup[2],user[0],user[1],user[2],user_type,usergroup[0],usergroup[1],usergroup[2])
        return html_str
    
    @staticmethod
    def license_toast_msg(msg_type,msg_text):
        type = {"success":"showSuccessToast","error":"showErrorToast","warning":"showWarningToast"}
        msg = "<script type=\"text/javascript\">\
                $().toastmessage('%s', '%s');\
            </script>" % (type[msg_type],msg_text)
        return msg
        
    @staticmethod
    def page_tip_license():
        html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>License</h1>"\
        "<div><strong>License</strong>  required for managing complete UNMP Server . </div>"\
        "<br/>"\
        "<div><strong><u>License Information</u></strong> consists of company name which has this license and expiry date.</div>"\
        "<div><strong><u>System Object</u></strong> are host, hostgroup, user and usergroup. This page displays current system object details like  Allowed user, Used and Remaining Objects</div>"\
        "<br/>"\
        "<div><strong>Actions</strong></div>"\
        "<div class=\"action-tip\"><div class=\"txt-div\">User can upload new license to renew it.</div></div>"\
        "<br/>"\
        "</div>"
        return html_view
    
    @staticmethod
    def device_type(ap25=[0,0,0],idu4=[0,0,0],ubr=[0,0,0],ubre=[0,0,0],unknown=[0,0,0]):
        html_view = '\
            <tr class="host_p">\
            <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">Access Point</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="host_p">\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">IDU</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="host_p">\
            <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">RM18</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="host_p">\
            <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">RM</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="host_p">\
            <td class="cell-info cell-info1 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">Generic</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info3">\
		%s\
              </td>\
            </tr>' % (tuple(ap25 + idu4 + ubr + ubre + unknown))
        return html_view

    @staticmethod
    def user_type(super_admin=[0,0,0],admin=[0,0,0],operator=[0,0,0],guest=[0,0,0]):
        html_view = '\
            <tr class="user_p">\
            <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">Super Admin</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="user_p">\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">Admin</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="user_p">\
            <td class="cell-info cell-info1 cell-info2 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">Operator</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info2 cell-info3">\
		%s\
              </td>\
            </tr>\
            <tr class="user_p">\
            <td class="cell-info cell-info1 cell-info3">\
		<span style="display:block;float:left;margin:4px 0px 4px 35px;">Guest</span>\
              </td>\
              <td class="cell-info cell-info1 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info3">\
		%s\
              </td>\
              <td class="cell-info cell-info1 cell-info3">\
		%s\
              </td>\
            </tr>' % (tuple(super_admin + admin + operator + guest))
        return html_view
    
    @staticmethod
    def invalid_license(host=[0,0,0],hostgroup=[0,0,0],user=[0,0,0],usergroup=[0,0,0],host_device_type_list=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],user_type_list=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]):
        
        host_device_type = License.device_type(*tuple(host_device_type_list))
        user_type = License.user_type(*tuple(user_type_list))
        html_str = '\
        <div>\
        <table class="tt-table" cellspacing="0" cellpadding="0" width="100%%">\
        <thead>\
            <tr>\
            <th class="cell-title cell-title2">\
                System Object\
            </th>\
            <th class="cell-title cell-title2">\
                Allowed\
            </th>\
            <th class="cell-title cell-title2">\
                Used\
            </th>\
            <th class="cell-title cell-title2">\
                Remaining\
            </th>\
            </tr>\
        </thead>\
        <tbody>\
            <tr>\
              <td class="cell-label cell-label2" id="host" style="cursor:pointer;">\
                <span class="nxt" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">HOST</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
            %s\
            <tr>\
              <td class="cell-label cell-label2" style="cursor:pointer;">\
                <span class="" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">HOSTGROUP</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
            <tr>\
              <td class="cell-label cell-label2" id="user" style="cursor:pointer;">\
                <span class="nxt" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">USER</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
            %s\
            <tr>\
              <td class="cell-label cell-label2" style="cursor:pointer;">\
                <span class="" style="height:16px;width:16px;display:block;float:left;"></span><span style="display:block;float:left;margin:4px 10px;">USERGROUP</span>\
              </td>\
              <td class="cell-info">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
              <td class="cell-info cell-info1">\
		%s\
              </td>\
            </tr>\
        </tbody>\
        </table>\
        </div>' % (host[0],host[1],host[2],host_device_type,hostgroup[0],hostgroup[1],hostgroup[2],user[0],user[1],user[2],user_type,usergroup[0],usergroup[1],usergroup[2])
        return html_str    
        
    @staticmethod
    def license_colorbox(msg_type,msg_text,html_str):
        type = {"success":"showSuccessToast","error":"showErrorToast","warning":"showWarningToast"}
        #msg = "<script type=\"text/javascript\">$().colorbox({html:'<p>Hello</p>'});</script>"
        msg = "<script type=\"text/javascript\">\
                $().toastmessage('%s','%s',{sticky: true});\
                $.colorbox({html:'%s'});\
            </script>" % (type[msg_type],html_str,html_str)
        return msg        
