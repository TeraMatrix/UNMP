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


def r20_listing(h):
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
    javascript_list = ["js/jquery.dataTables.min.js",'js/ccpl_jquery_autocomplete.js',"js/pages/r20_listing.js"]

    #This we import the javascript
    ip_address=""
    mac_address=""
    
    #this is used for storing DeviceTypeList e.g "UBR,odu100"
    device_type = ""
    
    #this is used for storing DeviceListState e.g "enabled
    device_list_state = ""
    
    #this is used for storing SelectedDeviceType e.g. "UBR" 
    selected_device_type = "r20,r220"
    
    #here we check That variable which is returned from page has value None or not
        
    #Here we print the heading of page
    html.new_header("RF Repeater","r20_listing.py","",css_list,javascript_list)
    
    #Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write 
    #we pass parameters 
    #ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
    html.write(str(page_header_search("","","R20,2R20",selected_device_type,"enabled","device_type")))
    
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
                </table></div>\
                <div id=\"iframe_configuration\" style=\"display:none;width:100%;height:100%;\">\
			<div style=\"display:block;position:absolute;top:5px;right:20px;background-color:#EEE;border:1px solid #888;\">\
				<a href=\"javascript:backToListing();\" style=\"color:#555;padding:5px 15px;text-decoration:none;display:block;\">Back</a>\
			</div>\
			<div id=\"edit_configuration\" style=\"display:block;width:100%;height:100%;\">\
		</div>\
        </div>"
    html.write(table_view)
    html.new_footer()
    
    
def _2r20_listing(h):
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
    javascript_list = ["js/jquery.dataTables.min.js",'js/ccpl_jquery_autocomplete.js',"js/pages/2r20_listing.js"]

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
    html.new_header("2R20 Listing","","",css_list,javascript_list)
    
    #Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write 
    #we pass parameters 
    #ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
    html.write(str(page_header_search(ip_address,mac_address,"2R20",selected_device_type,"enabled","device_type")))
    
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
    
def get_r20_details(h):
    global html 
    global sqlalche_obj
    sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    html = h
    userid = html.req.session['user_id']
    r20_details = SystemConfig.get_config_attributes("r20",["alias","hostgroup","ipaddress","macaddress","admin","passwd"],False)
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
    r20_details = []
    if device_type==None or device_type=="":
        device_type1="r20"
        device_type2="r220"
    else:
        if device_type == "r20":
            device_type1 = "r20"
            device_type2 = None
        if device_type == "r220":
            device_type2 = "r220"
            device_type1 = None
        
        #this is the query which returns the multidimensional array of hosts table and store in device_tuple
    
    if device_type1=="r20":
        #this is the query which returns the multidimensional array of hosts table and store in device_tuple
        r20_details = sqlalche_obj.session.query(Hosts.host_id,Hostgroups.hostgroup_name,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type1)),UsersGroups.user_id=='%s'%(userid),\
    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id,Hostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id))\
    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    device_list = []
    if len( r20_details)>0:
        r20_admin_password = sqlalche_obj.session.query(Hosts.http_username,Hosts.http_password).filter(Hosts.host_id==r20_details[0].host_id).all()
        #r20_details = SystemConfig.get_config_attributes("r220",["alias","hostgroup","ipaddress","macaddress","admin","passwd"],False)
        
        for i in range(0,len(r20_details)):
            device_list.append([str(r20_details[i][1]),str(r20_details[i][2]),str(r20_details[i][3]),str(r20_details[i][4]),"R20",\
                "<a target=\"main\" href=\"http://%s:%s@%s/index.html\" class=\"iframe\"><img src=\"images/new/edit.png\" style=\"width:16px;height:16px;\" title=\"Edit Configuration\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/RF_Status.cgi\" class=\"iframe\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Monitor RF Status\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>"\
                %(str((r20_admin_password[0][0]!=None and r20_admin_password[0][0]!="") and  r20_admin_password[0][0] or "admin" ),\
                str((r20_admin_password[0][1]!=None and r20_admin_password[0][1]!="") and  r20_admin_password[0][1] or "pass" ),str(r20_details[i][3]),\
                str((r20_admin_password[0][0]!=None and r20_admin_password[0][0]!="") and  r20_admin_password[0][0] or "admin" ),\
                str((r20_admin_password[0][1]!=None and r20_admin_password[0][1]!="") and  r20_admin_password[0][1] or "pass" ),str(r20_details[i][3]),\
                str(r20_details[i][3])),\
                ])
    # r220
    _2r20_details = []
    if device_type2 == "r220":
        _2r20_details = sqlalche_obj.session.query(Hosts.host_id,Hostgroups.hostgroup_name,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type2)),UsersGroups.user_id=='%s'%(userid),\
    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id,Hostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id))\
    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    if len(_2r20_details)>0:
        _2r20_admin_password = sqlalche_obj.session.query(Hosts.http_username,Hosts.http_password).filter(Hosts.host_id==_2r20_details[0].host_id).all()

        
        for i in range(0,len(_2r20_details)):
            device_list.append([str(_2r20_details[i][1]),str(_2r20_details[i][2]),str(_2r20_details[i][3]),str(_2r20_details[i][4]),"2R20",\
                "<a target=\"main\" href=\"http://%s:%s@%s/index.htm\" class=\"iframe\"><img src=\"images/new/edit.png\" style=\"width:16px;height:16px;\" title=\"Edit Configuration\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/RF_Status.cgi\" class=\"iframe\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Monitor RF Status\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>"\
                %(str((_2r20_admin_password[0][0]!=None and _2r20_admin_password[0][0]!="") and  _2r20_admin_password[0][0] or "admin" ),\
            str((_2r20_admin_password[0][1]!=None and _2r20_admin_password[0][1]!="") and  _2r20_admin_password[0][1] or "pass" ),str(_2r20_details[i][3]),\
                str((_2r20_admin_password[0][0]!=None and _2r20_admin_password[0][0]!="") and  _2r20_admin_password[0][0] or "admin" ),\
            str((_2r20_admin_password[0][1]!=None and _2r20_admin_password[0][1]!="") and  _2r20_admin_password[0][1] or "pass" ),str(_2r20_details[i][3]),\
                str(_2r20_details[i][3])),\
                ])
    #return device_list
    sqlalche_obj.sql_alchemy_db_connection_close()
    result = {'success':0,'result':device_list}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result))) 
    
def get_2r20_details(h):
    global html 
    html = h
    global sqlalche_obj
    sqlalche_obj
    sqlalche_obj.sql_alchemy_db_connection_open()
    device_list = []
    device_type="r220"
    userid = html.req.session['user_id']
    ip_address = ""
    mac_address = ""
        #this is the query which returns the multidimensional array of hosts table and store in device_tuple
##    _2r20_details = sqlalche_obj.session.query(Hosts.host_id,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
##    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
##    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
##    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id))\
##    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    device_list = []
    #_2r20_details = SystemConfig.get_config_attributes("r220",["alias","hostgroup","ipaddress","macaddress","admin","passwd"],False)
    _2r20_details = sqlalche_obj.session.query(Hosts.host_id,Hostgroups.hostgroup_name,Hosts.host_alias,Hosts.ip_address,Hosts.mac_address,Hosts.device_type_id,Hosts.reconcile_health,Hosts.config_profile_id).\
    filter(and_(Hosts.is_deleted == 0,Hosts.ip_address.like('%s%%'%(ip_address)),\
    Hosts.mac_address.like('%s%%'%(mac_address)),Hosts.device_type_id.like('%s%%'%(device_type)),UsersGroups.user_id=='%s'%(userid),\
    UsersGroups.group_id==HostgroupsGroups.group_id,HostsHostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id,Hosts.host_id==HostsHostgroups.host_id,Hostgroups.hostgroup_id==HostgroupsGroups.hostgroup_id))\
    .order_by(Hosts.host_alias).order_by(Hosts.ip_address).all()
    if len(_2r20_details)>0:
        _2r20_admin_password = sqlalche_obj.session.query(Hosts.http_username,Hosts.http_password).filter(Hosts.host_id==_2r20_details[0].host_id).all()

        
        for i in range(0,len(_2r20_details)):
            device_list.append([str(_2r20_details[i][1]),str(_2r20_details[i][2]),str(_2r20_details[i][3]),str(_2r20_details[i][4]),\
                "<a target=\"main\" href=\"http://%s:%s@%s/index.htm\"><img src=\"images/new/edit.png\" style=\"width:16px;height:16px;\" title=\"Edit Configuration\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"http://%s:%s@%s/RF_Status.cgi\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Monitor RF Status\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" title=\"Device Alerts\" class=\"imgbutton imgEditodu16 n-reconcile\"/ ></a>"\
                %(str((_2r20_admin_password[0][0]!=None and _2r20_admin_password[0][0]!="") and  _2r20_admin_password[0][0] or "admin" ),\
            str((_2r20_admin_password[0][1]!=None and _2r20_admin_password[0][1]!="") and  _2r20_admin_password[0][1] or "pass" ),str(_2r20_details[i][3]),\
                str((_2r20_admin_password[0][0]!=None and _2r20_admin_password[0][0]!="") and  _2r20_admin_password[0][0] or "admin" ),\
            str((_2r20_admin_password[0][1]!=None and _2r20_admin_password[0][1]!="") and  _2r20_admin_password[0][1] or "pass" ),str(_2r20_details[i][3]),\
                str(_2r20_details[i][3])),\
                ])
    #return device_list
    sqlalche_obj.sql_alchemy_db_connection_close()
    result = {'success':0,'result':device_list}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result))) 
