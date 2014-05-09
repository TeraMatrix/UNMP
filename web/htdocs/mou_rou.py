#!/usr/bin/python2.6

####################### import the packages ###################################
import config, htmllib, pprint, sidebar, views, time, defaults, os, xml.dom.minidom, subprocess, datetime, re, tarfile, MySQLdb, urllib2, base64
from lib import *
from mod_python import apache,util
from utility import *
from common_controller import *
from swt4_controller import *
from unmp_config import SystemConfig
from json import JSONEncoder
from unmp_model import *


def mou_listing(h):
    """
    @requires : odu_controller,utility,from common_controller import page_header_search function     
    @author : Anuj Samariya 
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var sitename : this is used to store the site name like nsm,UNMP etc 
    @var css_list : this is used to store the names of all the css files which is used in this function
    @var javascript_list : this is used to store the names of all the javascript files which is used in this function
    @var ip_address : this is used to store the ip address which is on the page
    @var mac_address : this is used to store the mac address which is on the page
    @var device_type : this is used to store the device types i.e UBR,Switch,AP25 etc
    @var device_list_state : this is used to store the select list state i.e. select list is enable or disable.if it's Value is None then it is enable by default 
    @var selected_device_type : this is used to store the device type which selected form the device_type list
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : This function is used for displaying the list of all host in the site and also search the host accrding to IpAddress,MAC Address,and Device Type
           and it write the list of device on the page. 
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    css_list = ["css/custom.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css",'css/ccpl_jquery_combobox.css']
    javascript_list = ["js/jquery.dataTables.min.js",'js/ccpl_jquery_autocomplete.js',"js/pages/mou_listing.js"]

    #This we import the javascript
    ip_address=""
    mac_address=""
    
    #this is used for storing DeviceTypeList e.g "UBR,odu100"
    device_type = ""
    
    #this is used for storing DeviceListState e.g "enabled
    device_list_state = ""
    
    #this is used for storing SelectedDeviceType e.g. "UBR" 
    selected_device_type = ""
    
    #here we check That variable which is returned from page has value None or not
        
    #Here we print the heading of page
    html.new_header("Optical Repeater","mou_listing.py","",css_list,javascript_list)
    
    #Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write 
    #we pass parameters 
    #ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
    html.write(str(page_header_search("","","MOU,ROU","","enabled","device_type")))
    
    #Here we make a div to show the result in datatable
    table_view = "<div id=\"grid_view\">"
    table_view+= "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center\">\
                    <thead>\
                        <tr>\
                            \
                            <th>Host Alias</th>\
                            <th>Host Group</th>\
                            <th>IP Address</th>\
                            <th>MAC Address</th>\
                            <th>Device Type</th>\
                            <th>Actions</th>\
                        </tr>\
                    </thead>\
                </table>\
                </div>\
                <div id=\"iframe_configuration\" style=\"display:none;width:100%;height:100%;\">\
			<div style=\"display:block;position:absolute;top:5px;right:20px;background-color:#EEE;border:1px solid #888;\">\
				<a href=\"javascript:backToListing();\" style=\"color:#555;padding:5px 15px;text-decoration:none;display:block;\">Back</a>\
			</div>\
			<div id=\"edit_configuration\" style=\"display:block;width:100%;height:100%;\">\
		</div>\
        </div>"
    html.write(table_view)
    html.new_footer()
    
    
def rou_listing(h):
    """
    @requires : odu_controller,utility,from common_controller import page_header_search function     
    @author : Anuj Samariya 
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var sitename : this is used to store the site name like nsm,UNMP etc 
    @var css_list : this is used to store the names of all the css files which is used in this function
    @var javascript_list : this is used to store the names of all the javascript files which is used in this function
    @var ip_address : this is used to store the ip address which is on the page
    @var mac_address : this is used to store the mac address which is on the page
    @var device_type : this is used to store the device types i.e UBR,Switch,AP25 etc
    @var device_list_state : this is used to store the select list state i.e. select list is enable or disable.if it's Value is None then it is enable by default 
    @var selected_device_type : this is used to store the device type which selected form the device_type list
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : This function is used for displaying the list of all host in the site and also search the host accrding to IpAddress,MAC Address,and Device Type
           and it write the list of device on the page. 
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    css_list = ["css/custom.css","css/demo_table_jui.css","css/jquery-ui-1.8.4.custom.css",'css/ccpl_jquery_combobox.css']
    javascript_list = ["js/jquery.dataTables.min.js",'js/ccpl_jquery_autocomplete.js',"js/pages/rou_listing.js"]

    #This we import the javascript
    ip_address=""
    mac_address=""
    
    #this is used for storing DeviceTypeList e.g "UBR,odu100"
    device_type = ""
    
    #this is used for storing DeviceListState e.g "enabled
    device_list_state = ""
    
    #this is used for storing SelectedDeviceType e.g. "UBR" 
    selected_device_type = ""
    
    #here we check That variable which is returned from page has value None or not

    #Here we print the heading of page
    html.new_header("ROU Listing","","",css_list,javascript_list)
    
    #Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write 
    #we pass parameters 
    #ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
    html.write(str(page_header_search(ip_address,mac_address,"ROU",selected_device_type,"enabled","device_type")))
    
    #Here we make a div to show the result in datatable
    table_view = "<div>"
    table_view+= "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center\">\
                    <thead>\
                        <tr>\
                            \
                            <th>Host Alias</th>\
                            <th>Host Group</th>\
                            <th>IP Address</th>\
                            <th>MAC Address</th>\
                            <th>Actions</th>\
                        </tr>\
                    </thead>\
                </table></div>\
                <div id=\"status_div\" style=\"position:absolute;display:none\"/>hi\
                </div>"
    html.write(table_view)
    html.new_footer()
    
def get_mou_details(h):
    global html 
    global sqlalche_obj
    sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    html = h
    userid = html.req.session['user_id']
    mou_details = SystemConfig.get_config_attributes("mou",["alias","hostgroup","ipaddress","macaddress","admin","passwd"],False)
    device_list = []
    device_type=""
    device_type1 = None;
    device_type2 = None;
    ip_address = html.var("ip_address")
    if ip_address==None:
        ip_address = ""
    mac_address = html.var("mac_address")
    if mac_address==None:
        mac_address = ""
    device_type = html.var("device_type")
    mou_details = []
    if device_type==None or device_type=="":
        device_type1="mou"
        device_type2="rou"
    else:
        if device_type == "mou":
            device_type1 = "mou"
            device_type2 = None
        if device_type == "rou":
            device_type2 = "rou"
            device_type1 = None
        
        #this is the query which returns the multidimensional array of hosts table and store in device_tuple
        
    if device_type1 == "mou":
        mou_details = sqlalche_obj.session.query(Hosts.host_id,Hostgroups.hostgroup_name,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type1)),UsersGroups.user_id=='%s'%(userid),\
    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id,Hostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id))\
    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    device_list = []
    if len( mou_details)>0:
        mou_admin_password = sqlalche_obj.session.query(Hosts.http_username,Hosts.http_password).filter(Hosts.host_id==mou_details[0].host_id).all()
        #mou_details = SystemConfig.get_config_attributes("rou",["alias","hostgroup","ipaddress","macaddress","admin","passwd"],False)
        
        for i in range(0,len(mou_details)):
            device_list.append([str(mou_details[i][1]),str(mou_details[i][2]),str(mou_details[i][3]),str(mou_details[i][4]),"MOU",\
                "<a target=\"main\" href=\"http://%s:%s@%s/MOUBand_User.cgi\" class=\"iframe\">\
                <img id=\"edit\" src=\"images/new/edit.png\" title=\"Configure RF Parameters\" style=\"width:16px;height:16px;\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/System_Config.htm\" class=\"iframe\"><img src=\"images/new/edit.png\" style=\"width:16px;height:16px;\" title=\"Configure System Parameters\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/mou_status.cgi\" class=\"iframe\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Monitor System Status\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>"\
                %(str((mou_admin_password[0][0]!=None and mou_admin_password[0][0]!="") and  mou_admin_password[0][0] or "admin" ),\
                str((mou_admin_password[0][1]!=None and mou_admin_password[0][1]!="") and  mou_admin_password[0][1] or "pass" ),str(mou_details[i][3]),\
                str((mou_admin_password[0][0]!=None and mou_admin_password[0][0]!="") and  mou_admin_password[0][0] or "admin" ),\
                str((mou_admin_password[0][1]!=None and mou_admin_password[0][1]!="") and  mou_admin_password[0][1] or "pass" ),str(mou_details[i][3]),\
                str((mou_admin_password[0][0]!=None and mou_admin_password[0][0]!="") and  mou_admin_password[0][0] or "admin" ),\
                str((mou_admin_password[0][1]!=None and mou_admin_password[0][1]!="") and  mou_admin_password[0][1] or "pass" ),str(mou_details[i][3]),\
                str(mou_details[i][3])),\
                ])
                
    # rou
    rou_details = []
    if device_type2 == "rou":
        rou_details = sqlalche_obj.session.query(Hosts.host_id,Hostgroups.hostgroup_name,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type2)),UsersGroups.user_id=='%s'%(userid),\
    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id,Hostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id))\
    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    if len(rou_details)>0:
        rou_admin_password = sqlalche_obj.session.query(Hosts.http_username,Hosts.http_password).filter(Hosts.host_id==rou_details[0].host_id).all()

        
        for i in range(0,len(rou_details)):
            device_list.append([str(rou_details[i][1]),str(rou_details[i][2]),str(rou_details[i][3]),str(rou_details[i][4]),"ROU",\
                "<a target=\"main\" href=\"http://%s:%s@%s/ROUBand_User.cgi\" class=\"iframe\"><img src=\"images/new/edit.png\" style=\"width:16px;height:16px;\" title=\"Band Configuration\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/System_Config.htm\" class=\"iframe\">\
                <img id=\"edit\" src=\"images/new/edit.png\" title=\"System Configuration\" style=\"width:16px;height:16px;\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/ROU_Status.cgi\" class=\"iframe\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Monitor System Status\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/Alarms.cgi\" class=\"iframe\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>\
                <!--<a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>-->"\
                %(str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
                str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
                str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
                str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
            str(rou_details[i][3])),\
                ])
    #return device_list
    sqlalche_obj.sql_alchemy_db_connection_close()
    result = {'success':0,'result':device_list}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result))) 
    
def get_rou_details(h):
    global html 
    html = h
    global sqlalche_obj
    sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    device_list = []
    device_type="rou"
    userid = html.req.session['user_id']
    ip_address = ""
    mac_address = ""
        #this is the query which returns the multidimensional array of hosts table and store in device_tuple
##    rou_details = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
##    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
##    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
##    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
##    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    device_list = []
    #rou_details = SystemConfig.get_config_attributes("rou",["alias","hostgroup","ipaddress","macaddress","admin","passwd"],False)
    rou_details = sqlalche_obj.session.query(Hosts.host_id,Hostgroups.hostgroup_name,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id,Hostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id))\
    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    if len(rou_details)>0:
        rou_admin_password = sqlalche_obj.session.query(Hosts.http_username,Hosts.http_password).filter(Hosts.host_id==rou_details[0].host_id).all()

        
        for i in range(0,len(rou_details)):
            device_list.append([str(rou_details[i][1]),str(rou_details[i][2]),str(rou_details[i][3]),str(rou_details[i][4]),\
                "<a target=\"main\" href=\"http://%s:%s@%s/ROUBand_User.cgi\" class=\"iframe\"><img src=\"images/new/edit.png\" style=\"width:16px;height:16px;\" title=\"Band Configuration\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/System_Config.htm\" class=\"iframe\">\
                <img id=\"edit\" src=\"images/new/edit.png\" title=\"System Configuration\" style=\"width:16px;height:16px;\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/ROU_Status.cgi\" class=\"iframe\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Monitor System Status\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/Alarms.cgi\" class=\"iframe\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>\
                <!--<a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>-->"\
                %(str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
                str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
                str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
                str((rou_admin_password[0][0]!=None and rou_admin_password[0][0]!="") and  rou_admin_password[0][0] or "admin" ),\
            str((rou_admin_password[0][1]!=None and rou_admin_password[0][1]!="") and  rou_admin_password[0][1] or "pass" ),str(rou_details[i][3]),\
            str(rou_details[i][3])),\
                ])
    #return device_list
    sqlalche_obj.sql_alchemy_db_connection_close()
    result = {'success':0,'result':device_list}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result))) 
