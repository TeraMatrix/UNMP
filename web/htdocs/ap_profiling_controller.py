#!/usr/bin/python2.6

"""
@author:Anuj Samariya
@since: 23 January 2012
@version: 0.0
@date: 23 January 2012
@note: In this file there are many classes and functions which create forms of AP Profiling and shows the forms on page,
       there is a functions which shows list of devices which are available on site and functions which take values of page
       and call the controller functions and pass the page values on that function and according to response it shows the
       profiling page values are set or not set.
@organisation: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
"""
from utility import ErrorMessages
from common_controller import page_header_search, DeviceStatus
from common_bll import EventLog, Essential, agent_start
from idu_profiling_bll import IduGetData
from ap_profiling import *
from ap_profiling_bll import *
from json import JSONEncoder
from utility import Validation
from time import sleep
import traceback
import time

essential_obj = Essential()


def ap_listing(h):
    """

    @param h:
    """
    try:
        """
        @requires : ap_profiling_controller,utility,from common_controller import page_header_search function
        @author : Anuj Samariya
        @param h : html Class Object
        @var html : this is html Class Object defined globally
        @var sitename : this is used to store the site name like nsm,UNMP etc
        @var css_list : this is used to store the names of all the css files which is used in this function
        @var javascript_list : this is used to store the names of all the javascript files which is used in this function
        @var ip_address : this is used to store the ip address which is on the page
        @var mac_address : this is used to store the mac address which is on the page
        @var device_type : this is used to store the device types i.e AP25 etc
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
        css_list = ["css/demo_table_jui.css",
                    "css/jquery-ui-1.8.4.custom.css", 'css/ccpl_jquery_combobox.css']
        javascript_list = ["js/lib/main/jquery.dataTables.min.js",
                           'js/unmp/main/ccpl_jquery_autocomplete.js', "js/unmp/main/ap_listing.js"]

        # This we import the javascript
        ip_address = ""
        mac_address = ""

        # this is used for storing DeviceTypeList e.g "UBR,odu100"
        device_type = ""

        # this is used for storing DeviceListState e.g "enabled
        device_list_state = ""

        # this is used for storing SelectedDeviceType e.g. "UBR"
        selected_device_type = ""

        # here we check That variable which is returned from page has value
        # None or not
        if html.var("device_type") != None:  # we get the variable of page through html.var
            device_type = html.var("device_type")
        if html.var("device_list_state") != None:
            device_list_state = html.var("device_list_state")
        if html.var("selected_device_type") != None:
            selected_device_type = html.var("selected_device_type")
        if html.var("ip_address") != None:
            ip_address = html.var("ip_address")
        if html.var("mac_address") != None:
            mac_address = html.var("mac_address")

        # Here we print the heading of page
        snapin_list = ["reports", "views", "Alarm", "Inventory", "Settings",
                       "NetworkMaps", "user_management", "schedule", "Listing"]
        add_btn = "<div class=\"header-icon\"><img onclick=\"addClientListing();\" class=\"n-tip-image\" src=\"images/new_icons/user.png\" id=\"ap_client\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"AP Client Listing\"></div>"
        add_btn += "<div class=\"header-icon\"><img onclick=\"apListing();\" class=\"n-tip-image\" src=\"images/new_icons/doc_new.png\" id=\"ap_listing\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;display:none\" original-title=\"AP Listing\"></div>"

        html.new_header(
            "AP Listing", "ap_listing.py", add_btn, css_list, javascript_list)

        # Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write
        # we pass parameters
        # ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
        html.write(str(page_header_search(ip_address, mac_address,
                                          "RM18,RM,IDU,Access Point,CCU", selected_device_type, "enabled",
                                          "device_type")))

        # Here we make a div to show the result in datatable

        html.write(APProfiling.ap_listing())
        html.new_footer()
    except Exception as e:
        html.write(str(e))


def get_client_data_table(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var html : this is html Class Object defined globally
    @var css_list : this is used to store the names of all the css files which is used in this function
    @var javascript_list : this is used to store the names of all the javascript files which is used in this function
    @var host_id : this is used to store the Host Id which is come from the page
    @var device_type : this is used to store the device types i.e UBR,Switch,AP25 etc
    @var device_list_state : this is used to store the select list state i.e. select list is enable or disable.if it's Value is None then it is enable by default
    @var device_list_param : this is used to store all the host details accoding to host-id like host ip address,host mac address,host device type,host configuration id
    @since : 20 August 2011
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to write the search bar in which user search the device according to ipaddress, macaddress, device type and show the configuration forms of device
            according to search
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    req_vars = html.req.vars
    ap_device_list_bll_obj = APDeviceList()
    i_display_start = str(html.var("iDisplayStart"))
    i_display_length = str(html.var("iDisplayLength"))
    s_search = str(html.var("sSearch"))
    sEcho = str(html.var("sEcho"))
    # client_list = ap_device_list_bll_obj.ap_client_list()
    client_list = ap_device_list_bll_obj.pagination_create_table(
        i_display_start, i_display_length, s_search, sEcho, req_vars)
    html.req.content_type = 'application/json'
    html.req.write(JSONEncoder().encode(client_list))


def ap_profiling(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var html : this is html Class Object defined globally
    @var css_list : this is used to store the names of all the css files which is used in this function
    @var javascript_list : this is used to store the names of all the javascript files which is used in this function
    @var host_id : this is used to store the Host Id which is come from the page
    @var device_type : this is used to store the device types i.e UBR,Switch,AP25 etc
    @var device_list_state : this is used to store the select list state i.e. select list is enable or disable.if it's Value is None then it is enable by default
    @var device_list_param : this is used to store all the host details accoding to host-id like host ip address,host mac address,host device type,host configuration id
    @since : 20 August 2011
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to write the search bar in which user search the device according to ipaddress, macaddress, device type and show the configuration forms of device
            according to search
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    ################### Javascript files declaration ##########################
    # Here we declare all the javascripts file which we usedin this file

    ###########################################################################
    ################### Css files declaration #################################
    # Declare path of all the css file which we used in this file
    ###########################################################################
    ##################### Header Declaration ##################################
    # Define the page header e.g Odu Profiling
    css_list = ['css/demo_table_jui.css',
                'css/jquery-ui-1.8.4.custom.css', 'css/ccpl_jquery_combobox.css']
    jss_list = [
        'js/lib/main/jquery.dataTables.min.js', 'js/unmp/main/ccpl_jquery_autocomplete.js',
        'js/unmp/main/ap_controller.js', 'js/lib/main/jquery-ui-personalized-1.6rc2.min.js']
    snapin_list = ["reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    # Variable declaration#########################
    # Declare the host id as an empty string
    host_id = ""

    # this is used for storing DeviceTypeList e.g "odu16,odu100"
    device_type = ""

    # this is used for storing DeviceListState e.g "enabled"
    device_list_state = ""
    # this is used for storing the ipaddress,macaddres,hostid and
    # configprofileid which is return form the database
    device_list_param = []
    ###########################################################################
    # we get the variable of page through html.var
    if html.var("host_id") != None:
        host_id = html.var("host_id")
    if html.var("device_type") != None:
        device_type = html.var("device_type")
    if html.var("device_list_state") != None:
        device_list_state = html.var("device_list_state")
    if host_id == None:
        host_id = ""
    device_parameter_bll_obj = DeviceParameters()
    device_list_parameter = device_parameter_bll_obj.get_device_parameter(
        host_id)  # call the idu_profiling_controller function get_device_param returns the list.List Contains ipaddress,macaddress,devicetypeid,config_profile_id
    if isinstance(device_list_parameter, list):
        html.new_header("%s %s Configuration" % ("AP", device_list_parameter[0]
        .ip_address), "ap_listing.py", "", css_list, jss_list, snapin_list)
        if device_list_parameter == [] or device_list_parameter == None:
            html.write(page_header_search(
                "", "", "RM18,RM,IDU,Access Point,CCU", None, "enabled", "device_type"))
            # call the function of common_controller , it is used
            # for listing the Devices based on
            # IPaddress,Macaddress,DeviceTy
        else:
            html.write(page_header_search(device_list_parameter[0][0], device_list_parameter[0][
                1], "RM18,RM,IDU,Access Point,CCU", device_type, device_list_state, "device_type"))
            html.write(APProfiling.ap_div(device_list_parameter[0][0],
                                          device_list_parameter[0][1], host_id))

    elif isinstance(device_list_parameter, Exception):
        html.write("DataBase Error Occured")
    html.new_footer()


# def page_tip_ap_listing(h):
#     global html
#     html = h
#     html.write(str(APProfiling.page_tip_ap_listing()))


def edit_ap_client(h):
    """

    @param h:
    """
    global html
    html = h
    client_id = html.var("client_id")
    result = APConnectedClients().client_details(client_id)
    group_name = html.req.session['group']
    if result["success"] == 0 and type(result["result"]) == dict:
        html.write(APForms().edit_client_form(result["result"], group_name))
    else:
        html.write(result["result"])


def edit_ap_client_details(h):
    """

    @param h:
    """
    global html
    html = h
    client_id = html.var("client_id")
    client_name = html.var("client_name")
    client_ip = html.var("client_ip")
    result = APConnectedClients(
    ).edit_ap_client_details(client_id, client_name, client_ip)
    html.req.content_type = 'application/json'
    html.write(JSONEncoder().encode(result))


def ap_device_listing_table(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally
    @var ip_address : this is used to store the ip address
    @var mac_address : this is used to store the mac address
    @var selected_device : this is used to store the device type id i.e. ap25,ap25
    @var result : this is used to store the result which is a list of devices according to the search criteria
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to give the list of selected device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        ap_device_list_bll_obj = APDeviceList()
        result_device_list = []
        device_list_state = "enabled"
        global html, essential_obj
        html = h
        device_dict = {}
        # this is the result which we show on the page
        result = ""
        userid = html.req.session['user_id']
        device_status_host_id = ""
        obj_get_data = IduGetData()
        obj_device_status = DeviceStatus()
        ## Mahipal data table
        i_display_start = str(html.var("iDisplayStart"))
        i_display_length = str(html.var("iDisplayLength"))
        s_search = str(html.var("sSearch"))
        sEcho = str(html.var("sEcho"))
        s_search = str(html.var("sSearch"))
        sSortDir_0 = str(html.var("sSortDir_0"))
        iSortCol_0 = str(html.var("iSortCol_0"))
        html_req = html.req.vars
        connected_clients = 0
        obj_clients_connected = APConnectedClients()
        obj_status = APRadioState()
        ###########################
        ap_mode = {0: 'Standard', 1: 'Root AP', 2: 'Repeater', 3:
            'Client', 4: 'Multi AP', 5: 'Multi VLAN', 6: 'Dynamic VLAN'}
        # take value of IPaddress from the page through html.var
        # check that value is None Then It takes the empty string
        if html.var("ip_address") == None:
            ip_address = ""
        else:
            ip_address = html.var("ip_address")

        # take value of MACAddress from the page through html.var
        # check that value is None Then It takes the empty string
        if html.var("mac_address") == None:
            mac_address = ""
        else:
            mac_address = html.var("mac_address")

        # take value of SelectedDevice from the page through html.var
        # check that value is None Then It takes the empty string
        if html.var("device_type") == None or html.var("device_type") == "":
            selected_device = "ap25"
        else:
            selected_device = html.var("device_type")
            # call the function get_odu_list of odu-controller which return us the
        # list of devices in two dimensional list according to
        # IPAddress,MACaddress,SelectedDevice

        device_dict = ap_device_list_bll_obj.ap_device_list(
            ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0,
            iSortCol_0, userid, html_req)

        # display the result on page
        # This is a empty list variable used for storing the device list
        device_list = device_dict["aaData"]
        # html.write(str(device_list))
        index = int(device_dict["i_display_start"])

        if isinstance(device_list, list):
            for i in range(0, len(device_list)):

                op_status = essential_obj.get_hoststatus(
                    device_list[i][0])  # Get the host status and this code use for op state status
                if op_status == None:
                    op_img = "images/host_status0.png"
                    op_title = host_status_dic[0]
                elif op_status == 0:
                    op_img = "images/host_status0.png"
                    op_title = host_status_dic[op_status]
                else:
                    op_img = "images/host_status1.png"
                    op_title = host_status_dic[op_status]

                if device_list[i][6] <= 35:
                    images = 'images/new/r-red.png'
                elif device_list[i][6] <= 90:
                    images = 'images/new/r-black.png'
                else:
                    images = 'images/new/r-green.png'

                snmp_up_time_data = obj_device_status.common_list_device_status(
                    device_list[i][0])
                device_status = snmp_up_time_data['result']['device_status'][0]
                device_status_image_path = snmp_up_time_data[
                    'result']['device_status'][1]
                chk_status = obj_status.chk_radio_status(
                    str(device_list[i][0]))
                if chk_status['success'] == 0:
                    # html.write(str(chk_status))
                    for j in chk_status['result']:
                        admin_mode = chk_status['result'][j][0]
                        radio_ap_mode = chk_status['result'][j][1]

                else:
                    admin_mode = 0
                    radio_ap_mode = 0

                if admin_mode == None:
                    image_class = "red"
                    state = 0
                    title = "Radio Disabled"
                elif admin_mode == 0:
                    image_class = "red"
                    state = 0
                    title = "Radio Disabled"
                else:
                    image_class = "green"
                    state = 1
                    title = "Radio Enabled"

                total_clients_connected = obj_clients_connected.total_connected_clients(
                    device_list[i][0])
                if total_clients_connected['success'] == 0:
                    connected_clients = total_clients_connected['result'][0]
                else:
                    connected_clients = 0
                if i == len(device_list) - 1:
                    device_status_host_id += str(device_list[i][0])
                else:
                    device_status_host_id += str(device_list[i][0]) + ","
                live_monitoring = "&nbsp;&nbsp;<a target=\"main\" href=\"live_monitoring.py?host_id=%s&device_type=%s\"><img src=\"images/new/star-empty.png\" title=\"Live Monitoring\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" /></a>" % (
                    device_list[i][0], device_list[i][5])

                # monitoring_status = "<img src=\"images/new/info1.png\"
                # style=\"width:16px;height:16px;\" title=\"Current Device
                # Status\" class=\" n-reconcile\"/>" if
                # device_list[i][5]=="ap25" else "<img
                # src=\"images/new/info1.png\"
                # style=\"width:16px;height:16px;\" title=\"Current Device
                # Status\" class=\"imgbutton n-reconcile\"/>"
                monitoring_status = ""
                if html.req.session["role"] == "admin" or html.req.session["role"] == "user":
                    result_device_list.append([
                        "<center><a href=\"#\"onclick=\"viewServiceDetails(%s)\"> <img id=\"ap_device_status\" name=\"ap_device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton n-reconcile imgEditodu16\" /></a></center>"
                        % (device_list[i][0], device_status_image_path, device_status), device_list[i][1],
                        device_list[i][2], device_list[i][3], device_list[i][4], connected_clients,
                        ap_mode[radio_ap_mode],
                        "<ul class=\"button_group\" style=\"width:30px\"><li><a class=\"%s n-reconcile imgEditodu16\" state=\"%s\" title=\"%s\" onclick=\"radio_enable_disable(event,this,'%s','radioSetup.radioState');\"/>AP</a></li></ul>"
                        % (image_class, state, title, device_list[i][0]),
                        "<div class=\"listing-icon\"><img src=\"images/new/wifi.png\" title=\"Wireless\" style=\"width:16px;height:16px;display:none;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"wirelessStatus(event,this,'%s','%s');\"/></div>&nbsp;\
<a target=\"main\" href=\"ap_profiling.py?host_id=%s&device_type=%s&device_list_state=%s\"><img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
<a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
<a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
<a target=\"main\" href=\"javascript:apFormwareUpdate('%s','%s','%s');\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
<img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"imgReconcile(this,'%s','%s'); state_rec=0\"/>\
%s&nbsp;&nbsp;%s\
%s"
                        % (
                            device_list[
                                i][0], device_list[i][5],
                            device_list[i][0], device_list[
                                i][
                                5], device_list_state,
                            device_list[i][0], 'sp_dashboard_profiling.py' if device_list[i][
                                                                                  5] == "ap25" else 'sp_dashboard_profiling.py',
                            device_list[i][0], device_list[i][5], device_list_state,
                            device_list[i][3],
                            device_list[i][0], device_list[
                                i][
                                5], device_list_state,
                            images, device_list[i][6], device_list[i][
                                0], device_list[
                                i][
                                5], live_monitoring, monitoring_status,
                            "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (
                            device_status_host_id) if i == len(device_list) - 1 else ""),
                        "<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\" class=\"n-reconcile\"/></center>&nbsp;&nbsp;" % (
                        op_img, op_title)])
                else:
                    result_device_list.append([
                        "<center><a href=\"#\"onclick=\"viewServiceDetails(%s)\"> <img id=\"ap_device_status\" name=\"ap_device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton n-reconcile imgEditodu16\" /></a></center>"
                        % (device_list[i][0], device_status_image_path, device_status), device_list[i][1],
                        device_list[i][2], device_list[i][3], device_list[i][4], connected_clients,
                        ap_mode[radio_ap_mode],
                        "<ul class=\"button_group\" style=\"width:30px\"><li><a class=\"%s n-reconcile imgEditodu16\" state=\"%s\" title=\"%s\"/>AP</a></li></ul>"
                        % (image_class, state, title),
                        "<div class=\"listing-icon\"><img src=\"images/new/wifi.png\" title=\"Wireless\" style=\"width:16px;height:16px;display:none;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"wirelessStatus(event,this,'%s','%s');\"/></div>&nbsp;\
<a target=\"main\" href=\"ap_profiling.py?host_id=%s&device_type=%s&device_list_state=%s\"><img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
<a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
<a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
<a target=\"main\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
<img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" state_rec=0\"/>\
%s&nbsp;&nbsp;%s\
%s"
                        % (
                            device_list[
                                i][0], device_list[i][5],
                            device_list[i][0], device_list[
                                i][
                                5], device_list_state,
                            device_list[i][0], 'sp_dashboard_profiling.py' if device_list[i][
                                                                                  5] == "ap25" else 'sp_dashboard_profiling.py',
                            device_list[i][0], device_list[i][5], device_list_state,
                            device_list[i][3],
                            images, device_list[i][
                                6], live_monitoring, monitoring_status,
                            "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (
                            device_status_host_id) if i == len(device_list) - 1 else ""),
                        "<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\" class=\"n-reconcile\"/></center>&nbsp;&nbsp;" % (
                        op_img, op_title)])

                #                    result_device_list.append(["<center><a href=\"#\"onclick=\"viewServiceDetails(%s)\"> <img id=\"ap_device_status\" name=\"ap_device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton n-reconcile imgEditodu16\" /></a></center>"\
                #                    %((device_status_host_id) if i==len(device_list)-1 else "",device_status_image_path,device_status)\
                #                    ,device_list[i][1],device_list[i][2],device_list[i][3],device_list[i][4],ap_mode[int(device_list[i][8])],\
                #                    "<ul class=\"button_group\" style=\"width:30px\"><li><a class=\"%s n-reconcile imgEditodu16\" state=\"%s\" title=\"%s\" onclick=\"radio_enable_disable(event,this,'%s','radioSetup.radioState');\"/>AP</a></li></ul>"
                #                    %(image_class,state,title,device_list[i][0]),\
                #                    "<div class=\"listing-icon\"><img src=\"images/new/wifi.png\" title=\"Wireless\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\" onclick=\"wirelessStatus(event,this,'%s','%s');\"/></div>&nbsp;\
                #                    <a target=\"main\" ><img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
                #                    <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
                #                    <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\"><img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton  n-reconcile\"/></a>&nbsp;&nbsp;\
                #                    <a target=\"main\" ><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
                #                    <img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" state_rec=0\"/>\
                #                    &nbsp;&nbsp;%s\
                #                   %s"
                #                   %(device_list[i][0],device_list[i][5],\
                #                   device_list[i][0],'sp_dashboard_profiling.py' if device_list[i][5] == "ap25" else 'sp_dashboard_profiling.py',device_list[i][0],device_list[i][5],device_list_state,\
                #                   device_list[i][3],\
                #                   images,device_list[i][6],monitoring_status,\
                #                   "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />"%(device_status_host_id) if i==len(device_list)-1 else ""),"<center><img id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:12px;height:12px;\" class=\"imgbutton n-reconcile\"/></center>&nbsp;&nbsp;"%(op_img,op_title)
                #                   ])
            html.req.content_type = 'application/json'
            device_dict["aaData"] = result_device_list
            html.req.write(str(JSONEncoder().encode(device_dict)))
    except Exception as e:
        output2 = {
            "sEcho": 1,
            "iTotalRecords": 10,
            "iTotalDisplayRecords": 10,
            "aaData": [],
            "query": str(e)
        }
        html.req.write(str(JSONEncoder().encode(output2)))


def get_device_list_ap_profiling(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        ap_device_list_bll_obj = APDeviceList()
        # this is the result which we show on the page
        result = ""
        ip_address = ""
        mac_address = ""
        selected_device = "ap25"
        # take value of IPaddress from the page through html.var
        # check that value is None Then It takes the empty string
        if html.var("ip_address") == None:
            ip_address = ""
        else:
            ip_address = html.var("ip_address")

        # take value of MACAddress from the page through html.var
        # check that value is None Then It takes the empty string
        if html.var("mac_address") == None:
            mac_address = ""
        else:
            mac_address = html.var("mac_address")
            # take value of SelectedDevice from the page through html.var
        # check that value is None Then It takes the empty string
        if html.var("selected_device_type") == None:
            selected_device = "ap25"
        else:
            selected_device = html.var("selected_device_type")

        # call the function get_odu_list of odu-controller which return us the
        # list of devices in two dimensional list according to
        # IPAddress,MACaddress,SelectedDevice

        device_list = ap_device_list_bll_obj.ap_device_list_profiling(
            ip_address, mac_address, selected_device)
        # html.write(str(device_list))
        total_record = len(device_list)
        if total_record == 0:
            result = 0
        elif total_record > 1:
            result = 1
        else:
            result = str(device_list[0][0])
            # html.write(str(result))
        if result == 0 or result == 1 or result == 2:
            # html.write("hello")
            html.write(str(result))
        else:
            # html.write("hiiiiiiii")
            device_parameter_bll_obj = DeviceParameters()
            device_list_parameter = device_parameter_bll_obj.get_device_parameter(
                result)  # call the ap_profiling_controller function get_device_param returns the list.List Contains ipaddress,macaddress,devicetypeid,config_profile_id
            # html.write(str(device_list_parameter))
            group_name = html.req.session['group']
            html.write(APProfiling.ap_profile_call(
                group_name, result, selected_device, device_list_parameter))

    except Exception as e:
        html.write(str(e[-1]))


def commit_to_flash(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    bll_commit_obj = APCommitToFlash()
    if host_id == "":
        result = {"success": 1, "result": "Host Not Exist"}
    result = bll_commit_obj.commit_to_flash(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def acl_add_form(h):
    """

    @param h:
    """
    global html
    html = h
    html.write(str(APForms.acl_add_form()))


def acl_upload_form(h):
    """

    @param h:
    """
    global html
    html = h
    html.write(str(APForms.acl_upload_form()))


def update_reconciliation(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_reconcilation = Reconciliation()
    table_prefix = "ap25_"
    current_time = datetime.now()
    username = html.req.session["username"]
    if username == None:
        username = ""
    result = obj_reconcilation.update_configuration(
        host_id, device_type, table_prefix, current_time, username)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def reconciliation_status(h):
    """

    @param h:
    """
    global html
    html = h
    bll_rec_obj = Reconciliation()
    result = bll_rec_obj.reconciliation_status()
    if result == None:
        result = []
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def chk_reconciliation_status(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj_reconcilation = Reconciliation()
    result = obj_reconcilation.reconciliation_chk_status(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def ap25_reconcilation(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_reconcilation = Reconciliation()
    table_prefix = "ap25_"
    current_time = datetime.now()
    username = html.req.session["username"]
    if username == None:
        username = ""
    result = obj_reconcilation.update_configuration(
        host_id, device_type, table_prefix, current_time, username)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def ap25_reboot(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj_reconcilation = Reconciliation()
    result = obj_reconcilation.reboot(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def ap_dhcp_client_information(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var('host_id')
    calculate = html.var('calculate')
    obj_dhcp_client = DHCPClientInformation()
    result = obj_dhcp_client.ap_dhcp_client_information(host_id, calculate)

    # html.write(str(result))
    ap_dhcp_client_table = '<div><button type=\"submit\" id=\"client_calculate\" class=\"yo-button\" style=\"margin-top:5px;margin-bottom:10px;\" onclick="dhcpClientInformationCalculate();"><span>Calculate</span></button></div>'
    ap_dhcp_client_table += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                            <th>\
                                Serial No.\
                            </th>\
                            <th>\
                                DHCP Client Mac Address\
                            </th>\
                            <th>\
                                DHCP Client IP Address\
                            </th>\
                            <th>\
                                DHCP Client Expiretion\
                            </th>\
                            <th>\
                                Timestamp\
                            </th>\
                            "
    if result["success"] == 0:
        if len(result["result"]) > 0:
            k = 1
            for i in result["result"]:
                ap_dhcp_client_table += "<tr><td>%s</td>" % k
                for j in result["result"][i]:
                    ap_dhcp_client_table += "<td>%s</td>" % (str(
                        j) if str(j).find("\n") == -1 else "" if str(j) == "\n" else str(j)[0:-1])
                k += 1
                ap_dhcp_client_table += "</tr>"
        else:
            ap_dhcp_client_table += "<tr><td colspan=\"5\">No Data Exists.</tr>"
    else:
        ap_dhcp_client_table += "<tr><td colspan=\"5\">%s</td></tr>" % (
            result["result"])
    ap_dhcp_client_table += "</table>"
    html.write(str(ap_dhcp_client_table))


def ap_scan(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var('host_id')
    calculate = html.var('calculate')
    obj_ap_scan = APScan()
    result = obj_ap_scan.ap_scan(host_id, calculate)
    ap_scan_table = '<div><button type=\"submit\" id=\"ap_scan_calculate\" class=\"yo-button\" style=\"margin-top:5px;margin-bottom:10px;\" onclick="apScanCalculate();"><span>Calculate</span></button></div>'
    ap_scan_table += " <table class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\"> \
                            <th>\
                                Serial No.\
                            </th>\
                            <th>\
                                Mac Address\
                            </th>\
                            <th>\
                                Essid\
                            </th>\
                            <th>\
                                Frequency\
                            </th>\
                            <th>\
                                Quality\
                            </th>\
                            <th>\
                                Signal Level\
                            </th>\
                            <th>\
                                Noise Level\
                            </th>\
                            <th>\
                                Beacon Interval\
                            </th>\
                            <th>\
                                Tiemstamp\
                            </th>\
                            "
    if result["success"] == 0:
        if len(result["result"]) > 0:
            for i in result["result"]:
                ap_scan_table += "<tr>"
                for j in result["result"][i]:
                    ap_scan_table += "<td>%s</td>" % (j if j.find(
                        "\n") == -1 else "" if j == "\n" else j[0:-1])
                ap_scan_table += "</tr>"
        else:
            ap_scan_table += "<tr><td colspan=\"9\">No Data Exists.</tr>"
    else:
        ap_scan_table += "<tr><td colspan=\"9\">%s</td></tr>" % (
            result["result"])
    ap_scan_table += "</table>"
    html.write(str(ap_scan_table))


def ap_radio_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = APCommonSetValidation()
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ap_common_submit") == "Save" or html.var("ap_common_submit") == "Retry" or html.var(
            "ap_common_submit") == "":
        if html.var("radioSetup.radioState") != None:
            if Validation.is_required(html.var("radioSetup.radioState")):
                dic_result["radioSetup.radioState"] = html.var(
                    "radioSetup.radioState")
                if int(html.var("radioSetup.radioState")) == 1:
                    dic_result["radioSetup.numberofVAPs"] = 1
                elif int(html.var("radioSetup.radioState")) == 2:
                    dic_result["radioSetup.numberofVAPs"] = 1
                elif int(html.var("radioSetup.radioState")) == 3:
                    dic_result["radioSetup.numberofVAPs"] = 2
                elif int(html.var("radioSetup.radioState")) == 4:
                    dic_result["radioSetup.numberofVAPs"] = 1
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Radio State is required"

        if html.var("radioSetup.radioAPmode") != None:
            if Validation.is_required(html.var("radioSetup.radioAPmode")):
                dic_result["radioSetup.radioAPmode"] = html.var(
                    "radioSetup.radioAPmode")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Start Up Mode is required"

        if html.var("radioSetup.radioManagementVLANstate") != None:
            if Validation.is_required(html.var("radioSetup.radioManagementVLANstate")):
                dic_result["radioSetup.radioManagementVLANstate"] = html.var(
                    "radioSetup.radioManagementVLANstate")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Radio State is required"

        if html.var("radioSetup.radioCountryCode") != None:
            if Validation.is_required(html.var("radioSetup.radioCountryCode")):
                dic_result["radioSetup.radioCountryCode"] = html.var(
                    "radioSetup.radioCountryCode")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Country code is required"

        if html.var("radioSetup.numberofVAPs") != None:
            if Validation.is_required(html.var("radioSetup.numberofVAPs")):
                dic_result["radioSetup.numberofVAPs"] = html.var(
                    "radioSetup.numberofVAPs")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Number of VAP's is required"

        if html.var("radioSetup.radioChannel") != None:
            if Validation.is_required(html.var("radioSetup.radioChannel")):
                dic_result["radioSetup.radioChannel"] = html.var(
                    "radioSetup.radioChannel")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Radio Channel Frequency is required"

        if html.var("radioSetup.wifiMode") != None:
            if Validation.is_required(html.var("radioSetup.wifiMode")):
                dic_result[
                    "radioSetup.wifiMode"] = html.var("radioSetup.wifiMode")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Radio Wifi Mode is required"

        if html.var("radioSetup.radioTxPower") != None:
            if Validation.is_required(html.var("radioSetup.radioTxPower")):
                dic_result["radioSetup.radioTxPower"] = html.var(
                    "radioSetup.radioTxPower")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Tx Power is required"

        if html.var("radioSetup.radioGatingIndex") != None:
            if Validation.is_required(html.var("radioSetup.radioGatingIndex")):
                dic_result["radioSetup.radioGatingIndex"] = html.var(
                    "radioSetup.radioGatingIndex")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Gating Index is required"
        if html.var("radioSetup.radioAggregation") != None:
            if Validation.is_required(html.var("radioSetup.radioAggregation")):
                if int(html.var("radioSetup.radioAggregation")) == 1 or True:
                    dic_result["radioSetup.radioAggregation"] = html.var(
                        "radioSetup.radioAggregation")
                    if html.var("radioSetup.radioAggFrames") != None:
                        if Validation.is_required(html.var("radioSetup.radioAggFrames")):
                            if Validation.is_number(html.var("radioSetup.radioAggFrames")):
                                dic_result["radioSetup.radioAggFrames"] = html.var(
                                    "radioSetup.radioAggFrames")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result["result"] = "The value is not a number.Please Enter a Number in aggframes"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "Aggregation Frame is required"

                    if html.var("radioSetup.radioAggSize") != None:
                        if Validation.is_required(html.var("radioSetup.radioAggSize")):
                            if Validation.is_number(html.var("radioSetup.radioAggSize")):
                                dic_result["radioSetup.radioAggSize"] = html.var(
                                    "radioSetup.radioAggSize")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "The value is not a number.Please Enter a Number in Aggsize"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "Aggregation Size is required"

                    if html.var("radioSetup.radioAggMinSize") != None:
                        if Validation.is_required(html.var("radioSetup.radioAggMinSize")):
                            if Validation.is_number(html.var("radioSetup.radioAggMinSize")):
                                dic_result["radioSetup.radioAggMinSize"] = html.var(
                                    "radioSetup.radioAggMinSize")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "The value is not a number.Please Enter a Number in minsize"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "Aggregation Minimum Size is required"
                elif int(html.var("radioSetup.radioAggregation")) == 0:
                    dic_result["radioSetup.radioAggregation"] = html.var(
                        "radioSetup.radioAggregation")

            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Aggregation is required"

        if html.var("radioSetup.radioChannelWidth") != None:
            if Validation.is_required(html.var("radioSetup.radioChannelWidth")):
                dic_result["radioSetup.radioChannelWidth"] = html.var(
                    "radioSetup.radioChannelWidth")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Channel Width is required"

        if html.var("radioSetup.radioTXChainMask") != None:
            if Validation.is_required(html.var("radioSetup.radioTXChainMask")):
                dic_result["radioSetup.radioTXChainMask"] = html.var(
                    "radioSetup.radioTXChainMask")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Tx Chain Mask is required"

        if html.var("radioSetup.radioRXChainMask") != None:
            if Validation.is_required(html.var("radioSetup.radioRXChainMask")):
                dic_result["radioSetup.radioRXChainMask"] = html.var(
                    "radioSetup.radioRXChainMask")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Rx Chain Mask is required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            time.sleep(2)
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ap_common_submit") == "Cancel":
        if html.var("radioSetup.radioState") != None:
            dic_result["radioSetup.radioState"] = html.var(
                "radioSetup.radioState")
        if html.var("radioSetup.radioAPmode") != None:
            dic_result["radioSetup.radioAPmode"] = html.var(
                "radioSetup.radioAPmode")
        if html.var("radioSetup.radioManagementVLANstate") != None:
            dic_result["radioSetup.radioManagementVLANstate"] = html.var(
                "radioSetup.radioManagementVLANstate")
        if html.var("radioSetup.radioCountryCode") != None:
            dic_result["radioSetup.radioCountryCode"] = html.var(
                "radioSetup.radioCountryCode")
        if html.var("radioSetup.numberofVAPs") != None:
            dic_result["radioSetup.numberofVAPs"] = html.var(
                "radioSetup.numberofVAPs")
        if html.var("radioSetup.radioChannel") != None:
            dic_result["radioSetup.radioChannel"] = html.var(
                "radioSetup.radioChannel")
        if html.var("radioSetup.wifiMode") != None:
            dic_result["radioSetup.wifiMode"] = html.var("radioSetup.wifiMode")
        if html.var("radioSetup.radioTxPower") != None:
            dic_result["radioSetup.radioTxPower"] = html.var(
                "radioSetup.radioTxPower")
        if html.var("radioSetup.radioGatingIndex") != None:
            dic_result["radioSetup.radioGatingIndex"] = html.var(
                "radioSetup.radioGatingIndex")
        if html.var("radioSetup.radioAggregation") != None:
            dic_result["radioSetup.radioAggregation"] = html.var(
                "radioSetup.radioAggregation")
        if html.var("radioSetup.radioAggFrames") != None:
            dic_result["radioSetup.radioAggFrames"] = html.var(
                "radioSetup.radioAggFrames")
        if html.var("radioSetup.radioAggSize") != None:
            dic_result["radioSetup.radioAggSize"] = html.var(
                "radioSetup.radioAggSize")
        if html.var("radioSetup.radioAggMinSize") != None:
            dic_result["radioSetup.radioAggMinSize"] = html.var(
                "radioSetup.radioAggMinSize")
        if html.var("radioSetup.radioChannelWidth") != None:
            dic_result["radioSetup.radioChannelWidth"] = html.var(
                "radioSetup.radioChannelWidth")
        if html.var("radioSetup.radioTXChainMask") != None:
            dic_result["radioSetup.radioTXChainMask"] = html.var(
                "radioSetup.radioTXChainMask")
        if html.var("radioSetup.radioRXChainMask") != None:
            dic_result["radioSetup.radioRXChainMask"] = html.var(
                "radioSetup.radioRXChainMask")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ap_service_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = APCommonSetValidation()
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ap_common_submit") == "Save" or html.var("ap_common_submit") == "Retry" or html.var(
            "ap_common_submit") == "":
        if html.var("services.upnpServerStatus") != None:
            if Validation.is_required(html.var("services.upnpServerStatus")):
                dic_result["services.upnpServerStatus"] = html.var(
                    "services.upnpServerStatus")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "UNMP Server Status is required"

        if html.var("services.systemLogStatus") != None:
            if Validation.is_required(html.var("services.systemLogStatus")):
                dic_result["services.systemLogStatus"] = html.var(
                    "services.systemLogStatus")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Log Status is required"

        if html.var("services.systemLogIP") != None:
            if Validation.is_required(html.var("services.systemLogIP")):
                if Validation.is_valid_ip(html.var("services.systemLogIP")) and int(
                        html.var("services.systemLogIP").split('.')[0]) not in [0, 255] and int(
                        html.var("services.systemLogIP").split('.')[-1]) not in [0, 255]:
                    dic_result["services.systemLogIP"] = html.var(
                        "services.systemLogIP")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Please Enter a Valid Ip Address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "System Log IP is required"

        if html.var("services.systemLogPort") != None:
            if Validation.is_required(html.var("services.systemLogPort")):
                if Validation.is_number(html.var("services.systemLogPort")):
                    if int(html.var("services.systemLogPort")) >= 1 and int(
                            html.var("services.systemLogPort")) <= 65535:
                        dic_result["services.systemLogPort"] = html.var(
                            "services.systemLogPort")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Log Port Number should be 1 to 65535"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Log Port Number is required"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Log Port is required"
        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            time.sleep(2)
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ap_common_submit") == "Cancel":
        if html.var("services.upnpServerStatus") != None:
            dic_result["services.upnpServerStatus"] = html.var(
                "services.upnpServerStatus")
        if html.var("services.systemLogStatus") != None:
            dic_result["services.systemLogStatus"] = html.var(
                "services.systemLogStatus")
        if html.var("services.systemLogIP") != None:
            dic_result["services.systemLogIP"] = html.var(
                "services.systemLogIP")
        if html.var("services.systemLogPort") != None:
            dic_result["services.systemLogPort"] = html.var(
                "services.systemLogPort")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ap_dhcp_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = APCommonSetValidation()
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ap_common_submit") == "Save" or html.var("ap_common_submit") == "Retry" or html.var(
            "ap_common_submit") == "":
        device_obj = DeviceParameters()
        ip_address_result = device_obj.get_device_parameter(host_id)
        if len(ip_address_result) > 0:
            ip_address = ip_address_result[0].ip_address
        if html.var("dhcpServer.dhcpServerStatus") != None:
            if Validation.is_required(html.var("dhcpServer.dhcpServerStatus")):
                dic_result["dhcpServer.dhcpServerStatus"] = html.var(
                    "dhcpServer.dhcpServerStatus")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "DHCP Server Status is required"

        if html.var("dhcpServer.dhcpStartIPaddress") != None:
            if Validation.is_required(html.var("dhcpServer.dhcpStartIPaddress")):
                if Validation.is_valid_ip(html.var("dhcpServer.dhcpStartIPaddress")) and int(
                        html.var("dhcpServer.dhcpStartIPaddress").split('.')[0]) not in [0, 255] and int(
                        html.var("dhcpServer.dhcpStartIPaddress").split('.')[-1]) not in [0, 255]:
                    dic_result["dhcpServer.dhcpStartIPaddress"] = html.var(
                        "dhcpServer.dhcpStartIPaddress")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter the valid DHCP start IP Address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "DHCP Start IP Address is required"

        if html.var("dhcpServer.dhcpEndIPaddress") != None:
            if Validation.is_required(html.var("dhcpServer.dhcpEndIPaddress")):
                if Validation.is_valid_ip(html.var("dhcpServer.dhcpEndIPaddress")) and int(
                        html.var("dhcpServer.dhcpEndIPaddress").split('.')[0]) not in [0, 255] and int(
                        html.var("dhcpServer.dhcpEndIPaddress").split('.')[-1]) not in [0, 255]:
                    dic_result["dhcpServer.dhcpEndIPaddress"] = html.var(
                        "dhcpServer.dhcpEndIPaddress")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter the valid DHCP end IP Address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "DHCP End IP Address is required"

        if dic_result["success"] == 0 and html.var("dhcpServer.dhcpStartIPaddress") != None and html.var(
                "dhcpServer.dhcpEndIPaddress") != None:
            if dic_result["dhcpServer.dhcpStartIPaddress"] > dic_result["dhcpServer.dhcpEndIPaddress"]:
                flag = 1
                dic_result["success"] = 1
                dic_result[
                    "result"] = "Start DHCP IP Address can't be greater than end DHCP IP Address"
            elif int(dic_result["dhcpServer.dhcpStartIPaddress"].split('.')[0]) != int(ip_address.split('.')[0]):
                flag = 1
                dic_result["success"] = 1
                dic_result[
                    "result"] = "Please check the domain of start DHCP IP Address"
            elif int(dic_result["dhcpServer.dhcpEndIPaddress"].split('.')[0]) != int(ip_address.split('.')[0]):
                flag = 1
                dic_result["success"] = 1
                dic_result[
                    "result"] = "Please check the domain of end DHCP IP Address"
            elif dic_result["dhcpServer.dhcpStartIPaddress"] <= ip_address and ip_address <= dic_result[
                "dhcpServer.dhcpEndIPaddress"]:
                flag = 1
                dic_result["success"] = 1
                dic_result[
                    "result"] = "Device IP address can't be exists in DHCP IP range"

        if html.var("dhcpServer.dhcpSubnetMask") != None:
            if Validation.is_required(html.var("dhcpServer.dhcpSubnetMask")):
                if Validation.is_valid_ip(html.var("dhcpServer.dhcpSubnetMask")) and int(
                        html.var("dhcpServer.dhcpSubnetMask").split('.')[0]) not in [0]:
                    dic_result["dhcpServer.dhcpSubnetMask"] = html.var(
                        "dhcpServer.dhcpSubnetMask")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter the valid DHCP subnet Mask IP Address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result[
                    "result"] = "DHCP Network Mask IP Address is required"

        if html.var("dhcpServer.dhcpClientLeaseTime") != None:
            if Validation.is_required(html.var("dhcpServer.dhcpClientLeaseTime")):
                if Validation.is_positive_number(html.var("dhcpServer.dhcpClientLeaseTime")):
                    if int(html.var("dhcpServer.dhcpClientLeaseTime")) >= 10 and int(
                            html.var("dhcpServer.dhcpClientLeaseTime")) <= 6000:
                        dic_result["dhcpServer.dhcpClientLeaseTime"] = html.var(
                            "dhcpServer.dhcpClientLeaseTime")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Lease Time must be in 10 to 6000"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Lease Time only number is required"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Lease Time is required"
        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            time.sleep(2)
            result = obj_bll_set_valid.common_set_config(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ap_common_submit") == "Cancel":
        if html.var("dhcpServer.dhcpServerStatus") != None:
            dic_result["dhcpServer.dhcpServerStatus"] = html.var(
                "dhcpServer.dhcpServerStatus")
        if html.var("dhcpServer.dhcpStartIPaddress") != None:
            dic_result["dhcpServer.dhcpStartIPaddress"] = html.var(
                "dhcpServer.dhcpStartIPaddress")
        if html.var("dhcpServer.dhcpEndIPaddress") != None:
            dic_result["dhcpServer.dhcpEndIPaddress"] = html.var(
                "dhcpServer.dhcpEndIPaddress")
        if html.var("dhcpServer.dhcpSubnetMask") != None:
            dic_result["dhcpServer.dhcpSubnetMask"] = html.var(
                "dhcpServer.dhcpSubnetMask")
        if html.var("dhcpServer.dhcpClientLeaseTime") != None:
            dic_result["dhcpServer.dhcpClientLeaseTime"] = html.var(
                "dhcpServer.dhcpClientLeaseTime")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def selectVap(h):
    """

    @param h:
    """
    global html
    obj_bll_select_vap = SelectVap()
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type")
    result = obj_bll_select_vap.select_vap_vap(host_id, device_type)
    html.write(str(result))


def vap_vap_select(h):
    """

    @param h:
    """
    global html
    obj_bll_select_vap = SelectVap()
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type")
    result = obj_bll_select_vap.select_vap_change(host_id, device_type)
    html.write(str(result))


def select_vap_acl(h):
    """

    @param h:
    """
    global html
    obj_bll_select_vap = SelectVap()
    html = h
    vap_select_id = html.var("vap_select_id")
    result = obj_bll_select_vap.select_mac(vap_select_id)
    mac_table = ""
    mac_table += "<table id=\"showmac\" style=\"width: 100%;\" class=\"display\">\
                    <thead>\
                        <tr>\
                            <th>Select</th>\
                            <th>Serial No.</th>\
                            <th>MAC Address</th>\
                        </tr>\
                    </thead><tbody>"
    if len(result) > 0:
        for i in range(0, len(result)):
            mac_table += "<tr>\
                            <td><input type=\"checkbox\" name=\"mac_chk\" id=\"mac_chk\" value=\"%s\"/>\
                            <td>%s</td>\
                            <td>%s</td>\
                        </tr>" % (result[i].macaddress, i + 1, result[i].macaddress)
    mac_table += "</tbody></table>"
    html.write(str(mac_table))


def ap_acl_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = APCommonSetValidation()

    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ap_common_submit") == "Save" or html.var("ap_common_submit") == "Retry" or html.var(
            "ap_common_submit") == "":
        if html.var("vapSelection.selectVap") != None:
            if Validation.is_required(html.var("vapSelection.selectVap")):
                dic_result["vapSelection.selectVap"] = html.var(
                    "vapSelection.selectVap")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please Select a vap"
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Please Select a vap"

        if html.var("basicACLconfigTable.aclState") != None:
            dic_result["basicACLconfigTable.aclState"] = html.var(
                "basicACLconfigTable.aclState")
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result[
                "result"] = "You can not do this operation because ACL Mode is disable."

        if html.var("basicACLconfigTable.aclMode") != None:
            dic_result["basicACLconfigTable.aclMode"] = html.var(
                "basicACLconfigTable.aclMode")

        if html.var("vap_selection_id") != None:
            dic_result["vap_selection_id"] = html.var("vap_selection_id")
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Problem occured in UNMP.Please Shut Down The UNMP.Contact Administartor"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            time.sleep(2)
            result = obj_bll_set_valid.basic_acl_set(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ap_common_submit") == "Cancel":
        if html.var("vapSelection.selectVap") != None:
            dic_result["vapSelection.selectVap"] = html.var(
                "vapSelection.selectVap")
        if html.var("vapWPAsecuritySetup.aclState") != None:
            dic_result["vapWPAsecuritySetup.aclState"] = html.var(
                "vapWPAsecuritySetup.aclState")
        if html.var("vapWPAsecuritySetup.aclMode") != None:
            dic_result["vapWPAsecuritySetup.aclMode"] = html.var(
                "vapWPAsecuritySetup.aclMode")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def acl_add_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    obj_bll_mac_operations = MacOperations()
    dic_result = {"success": 0}
    result = {}
    flag = 0
    valid = 0
    duplicate = 0
    mac_add = []
    final_mac_list = []
    strip_macaddress = ""
    mac_duplicate = []
    duplicate_mac = 1
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("ap_common_submit") == "Add":
        vap_selection_id = html.var("vap_selection_id")
        if vap_selection_id == None:
            flag = 1
            dic_result["success"] = 1
            dic_result[
                "result"] = "Unmp has Encountered an Error.Please Reconcile the device"

        selected_vap = html.var("selected_vap")
        if selected_vap == None:
            flag = 1
            dic_result["success"] = 1
            dic_result[
                "result"] = "Unmp has Encountered an error.Please reconcile the device"
        if html.var("mac_add") != None:
            if html.var("mac_text") != None:
                if Validation.is_required(html.var("mac_text")):
                    mac_add = html.var("mac_text").split(",")
                    if len(mac_add) == 0:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result["result"] = "Please Enter the Mac"
                    elif len(mac_add) == 1:
                        if Validation.is_valid_mac(mac_add[0]):
                            if obj_bll_mac_operations.chk_mac_duplicate(mac_add[0], vap_selection_id) == 0:
                                strip_macaddress = mac_add[0].strip()
                                mac_add = []
                                mac_add.append(strip_macaddress)
                                dic_result["mac_add"] = mac_add
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result["result"] = "Mac Already Exist"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result["result"] = "Please Enter the Valid Mac"
                    else:
                        for i in range(0, len(mac_add)):
                            if Validation.is_valid_mac(mac_add[i].strip()):
                                valid = 0
                                if mac_add[i].strip() in mac_duplicate:
                                    duplicate_mac = 1
                                else:
                                    mac_duplicate.append(mac_add[i])
                                    if obj_bll_mac_operations.chk_mac_duplicate(mac_add[i].strip(),
                                                                                vap_selection_id) == 0:
                                        final_mac_list.append(
                                            mac_add[i].strip())
                                    else:
                                        duplicate = 1
                            else:
                                valid = 1
                        if len(final_mac_list) > 0:
                            dic_result["mac_add"] = final_mac_list
                        else:
                            if valid == 1:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "Please Enter the valid mac addresses"
                            elif duplicate == 1:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "Mac Addresses Already Exists"
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "You entered the duplicate mac"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Please Enter the mac address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please Enter the mac address"
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result[
                "result"] = "Please Choose Option of single and multiple added"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))

        else:
            time.sleep(2)
            result = obj_bll_mac_operations.add_acl(
                host_id, device_type_id, dic_result, vap_selection_id, selected_vap)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))
            # html.req.write(str(JSONEncoder().encode(dic_result)))


def delete_all_mac(h):
    """

    @param h:
    """
    global html
    html = h
    obj_bll_mac_operations = MacOperations()
    dic_result = {"success": 0}
    result = {}
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    vap_selection_id = html.var("vap_selection_id")
    if vap_selection_id == None:
        flag = 1
        dic_result["success"] = 1
        dic_result[
            "result"] = "Unmp has Encountered an Error.Please Reconcile the device"

    selected_vap = html.var("selected_vap")
    if selected_vap == None:
        flag = 1
        dic_result["success"] = 1
        dic_result[
            "result"] = "Unmp has Encountered an error.Please reconcile the device"

    if flag == 1:
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    else:
        result = obj_bll_mac_operations.delete_all_mac(
            host_id, device_type_id, selected_vap, vap_selection_id)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def delete_single_mac(h):
    """

    @param h:
    """
    global html
    html = h
    obj_bll_mac_operations = MacOperations()
    dic_result = {"success": 0}
    result = {}
    flag = 0
    mac_add = []
    final_mac_list = []
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    selected_vap = html.var("selected_vap")
    vap_selection_id = html.var("vap_selection_id")
    if vap_selection_id == None:
        flag = 1
        dic_result["success"] = 1
        dic_result[
            "result"] = "Unmp has Encountered an Error.Please Reconcile the device"

    if selected_vap == None:
        flag = 1
        dic_result["success"] = 1
        dic_result[
            "result"] = "Unmp has Encountered an error.Please reconcile the device"
    if html.var("mac_text") != None:
        mac_add = html.var("mac_text").split(",")
        for i in range(0, len(mac_add)):
            final_mac_list.append(mac_add[i].strip())
        if len(final_mac_list) > 0:
            dic_result["mac_add"] = final_mac_list
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Please Select the mac address to delete"
    else:
        flag = 1
        dic_result["success"] = 1
        dic_result["result"] = "Please Select the mac address to delete"

    if flag == 1:
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    else:
        time.sleep(2)
        result = obj_bll_mac_operations.delete_acl(
            host_id, device_type_id, dic_result, selected_vap, vap_selection_id)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ap_vap_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    wep_flag = 0
    wep_flag_error = 0
    wep_field_flag = 0
    device_type = html.var("device_type")
    dic_result = {"success": 0}
    flag = 0
    result = {}
    obj_bll_set_valid = APCommonSetValidation()
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ap_common_submit") == "Save" or html.var("ap_common_submit") == "Retry" or html.var(
            "ap_common_submit") == "":

        if html.var("vapselectionid") != None:
            if Validation.is_required(html.var("vapselectionid")):
                selectedvap = html.var("vapselectionid")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please Select a vap"
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Please Select a vap"

        if html.var("selectionvap_id") != None:
            vap_id = html.var("selectionvap_id")
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Problem occured in UNMP.Please Shut Down The UNMP.Contact Administartor"
            # html.write(str(html.var("vap_selection_id")))

        if html.var("basicVAPconfigTable.vapESSID") != None:
            if Validation.is_required(html.var("basicVAPconfigTable.vapESSID")):
                if len(html.var("basicVAPconfigTable.vapESSID")) >= 0 and len(
                        html.var("basicVAPconfigTable.vapESSID")) < 33:
                    dic_result["basicVAPconfigTable.vapESSID"] = html.var(
                        "basicVAPconfigTable.vapESSID")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Essid must be in 0 to 32 character"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Essid is required"

        if html.var("essid") != None:
            dic_result[
                "basicVAPconfigTable.vapHiddenESSIDstate"] = html.var("essid")

        if html.var("basicVAPconfigTable.vlanId") != None:
            if Validation.is_required(html.var("basicVAPconfigTable.vlanId")):
                if Validation.is_number(html.var("basicVAPconfigTable.vlanId")):
                    if int(html.var("basicVAPconfigTable.vlanId")) > 0 and int(
                            html.var("basicVAPconfigTable.vlanId")) < 4096:
                        dic_result["basicVAPconfigTable.vlanId"] = html.var(
                            "basicVAPconfigTable.vlanId")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result["result"] = "VLAN Id must be in 1 to 4095"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "VLAN Id must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "VLAN Id is required"

        if html.var("basicVAPconfigTable.vlanPriority") != None:
            if Validation.is_required(html.var("basicVAPconfigTable.vlanPriority")):
                if Validation.is_number(html.var("basicVAPconfigTable.vlanPriority")):
                    if int(html.var("basicVAPconfigTable.vlanPriority")) >= 0 and int(
                            html.var("basicVAPconfigTable.vlanPriority")) < 8:
                        dic_result["basicVAPconfigTable.vlanPriority"] = html.var(
                            "basicVAPconfigTable.vlanPriority")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "VLAN Priority must be in 0 to 7"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "VLAN Priority must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "VLAN Priority is required"

        if html.var("basicVAPconfigTable.vapRadioMac") != None:
            if Validation.is_required(html.var("basicVAPconfigTable.vapRadioMac")):
                if Validation.is_valid_mac(html.var("basicVAPconfigTable.vapRadioMac")):
                    dic_result["basicVAPconfigTable.vapRadioMac"] = html.var(
                        "basicVAPconfigTable.vapRadioMac")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Root MAC Address not correct"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Root MAC Address is required"

        if html.var("basicVAPconfigTable.vapMode") != None:
            if Validation.is_required(html.var("basicVAPconfigTable.vapMode")):
                dic_result["basicVAPconfigTable.vapMode"] = html.var(
                    "basicVAPconfigTable.vapMode")

        if html.var("rts_mode") != None:
            if Validation.is_required(html.var("rts_mode")):
                if int(html.var("rts_mode")) == 1:
                    if html.var("basicVAPconfigTable.vapRTSthresholdValue") != None:
                        if Validation.is_required(html.var("basicVAPconfigTable.vapRTSthresholdValue")):
                            if Validation.is_number(html.var("basicVAPconfigTable.vapRTSthresholdValue")):
                                if int(html.var("basicVAPconfigTable.vapRTSthresholdValue")) >= 256 and int(
                                        html.var("basicVAPconfigTable.vapRTSthresholdValue")) <= 2346:
                                    dic_result["basicVAPconfigTable.vapRTSthresholdValue"] = html.var(
                                        "basicVAPconfigTable.vapRTSthresholdValue")
                                else:
                                    flag = 1
                                    dic_result["success"] = 1
                                    dic_result[
                                        "result"] = "RTS Threshold should be between 256 to 2346"

                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "RTS Threshold must be number"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result["result"] = "RTS Threshold is required"
                else:
                    dic_result["basicVAPconfigTable.vapRTSthresholdValue"] = 0
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please Select The RTS Mode"
        if html.var("frag_mode") != None:
            if Validation.is_required(html.var("frag_mode")):
                if int(html.var("frag_mode")) == 1:
                    if html.var("basicVAPconfigTable.vapFragmentationThresholdValue") != None:
                        if Validation.is_required(html.var("basicVAPconfigTable.vapFragmentationThresholdValue")):
                            if Validation.is_number(html.var("basicVAPconfigTable.vapFragmentationThresholdValue")):
                                if int(html.var("basicVAPconfigTable.vapFragmentationThresholdValue")) >= 256 and int(
                                        html.var("basicVAPconfigTable.vapFragmentationThresholdValue")) <= 2346:
                                    dic_result["basicVAPconfigTable.vapFragmentationThresholdValue"] = html.var(
                                        "basicVAPconfigTable.vapFragmentationThresholdValue")
                                else:
                                    flag = 1
                                    dic_result["success"] = 1
                                    dic_result["result"] = "Fragmentation Threshold should be between 256 to 2346"
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "Fragmentation threshold must be number"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "Fragmentation Threshold is required"
                else:
                    dic_result[
                        "basicVAPconfigTable.vapFragmentationThresholdValue"] = 0
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please Select The Fragmentation Mode"
        if html.var("basicVAPconfigTable.vapBeaconInterval") != None:
            if Validation.is_required(html.var("basicVAPconfigTable.vapBeaconInterval")):
                if Validation.is_number(html.var("basicVAPconfigTable.vapBeaconInterval")):
                    if int(html.var("basicVAPconfigTable.vapBeaconInterval")) >= 40 and int(
                            html.var("basicVAPconfigTable.vapBeaconInterval")) <= 1000:
                        dic_result["basicVAPconfigTable.vapBeaconInterval"] = html.var(
                            "basicVAPconfigTable.vapBeaconInterval")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Beacon Interval must be in Between 40 and 1000"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Beacon Interval must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Beacon Interval is required"

        if html.var("basicVAPconfigTable.vapSecurityMode") != None:
            if int(html.var("basicVAPconfigTable.vapSecurityMode")) == 0:

                dic_result["basicVAPconfigTable.vapSecurityMode"] = html.var(
                    "basicVAPconfigTable.vapSecurityMode")
            elif int(html.var("basicVAPconfigTable.vapSecurityMode")) == 1:

                dic_result["basicVAPconfigTable.vapSecurityMode"] = html.var(
                    "basicVAPconfigTable.vapSecurityMode")
                if html.var("vapWEPsecurityConfigTable.vapWEPmode") != None:
                    dic_result["vapWEPsecurityConfigTable.vapWEPmode"] = html.var(
                        "vapWEPsecurityConfigTable.vapWEPmode")

                if html.var("vapWEPsecurityConfigTable.vapWEPprimaryKey") != None:
                    if int(html.var("vapWEPsecurityConfigTable.vapWEPprimaryKey")) == 1:
                        if html.var("vapWEPsecurityConfigTable.vapWEPkey1") != None:
                            if Validation.is_required(html.var("vapWEPsecurityConfigTable.vapWEPkey1")):
                                if (len(html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 5 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 13 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 16):
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey1"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey1")
                                    wep_flag = 1
                                elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 10 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 26 or len(html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey1")) == 32) and Validation.is_hex_number(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey1")):
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey1"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey1")
                                    wep_flag = 1
                                else:
                                    # flag = 1
                                    # dic_result["success"]=1
                                    # dic_result["result"] = "WEP key1 must be
                                    # the length of 5,13 or 16"
                                    wep_field_flag = 1
                            else:
                                wep_flag_error = 1
                                # flag = 1
                                # dic_result["success"] = 1
                                # dic_result["result"]="WEP Key1 is required"

                    elif int(html.var("vapWEPsecurityConfigTable.vapWEPprimaryKey")) == 2:
                        if html.var("vapWEPsecurityConfigTable.vapWEPkey2") != None:
                            if Validation.is_required(html.var("vapWEPsecurityConfigTable.vapWEPkey2")):
                                if len(html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 5 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 13 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 16:
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey2"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey2")
                                    wep_flag = 2
                                elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 10 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 26 or len(html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey2")) == 32) and Validation.is_hex_number(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey2")):
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey2"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey2")
                                    wep_flag = 1
                                else:
                                    wep_field_flag = 2
                                    # flag = 1
                                    # dic_result["success"]=1
                                    # ic_result["result"] = "WEP key2 must be
                                    # the length of 5,13 or 16"
                            else:
                                wep_flag_error = 2
                                # flag = 1
                                # dic_result["success"] = 1
                                # dic_result["result"]="WEP Key2 is required"

                    elif int(html.var("vapWEPsecurityConfigTable.vapWEPprimaryKey")) == 3:
                        if html.var("vapWEPsecurityConfigTable.vapWEPkey3") != None:
                            if Validation.is_required(html.var("vapWEPsecurityConfigTable.vapWEPkey3")):
                                if len(html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 5 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 13 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 16:
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey3"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey3")
                                    wep_flag = 3
                                elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 10 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 26 or len(html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey3")) == 32) and Validation.is_hex_number(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey3")):
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey3"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey3")
                                    wep_flag = 1
                                else:
                                    wep_field_flag = 3
                                    # flag = 1
                                    # dic_result["success"]=1
                                    # dic_result["result"] = "WEP key3 must be
                                    # the length of 5,13 or 16"
                            else:
                                wep_flag_error = 3
                                # flag = 1
                                # dic_result["success"] = 1
                                # dic_result["result"]="WEP Key3 is required"

                    else:
                        if html.var("vapWEPsecurityConfigTable.vapWEPkey4") != None:
                            if Validation.is_required(html.var("vapWEPsecurityConfigTable.vapWEPkey4")):
                                if len(html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 5 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 13 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 16:
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey4"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey4")
                                    wep_flag = 4
                                elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 10 or len(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 26 or len(html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey4")) == 32) and Validation.is_hex_number(
                                        html.var("vapWEPsecurityConfigTable.vapWEPkey4")):
                                    dic_result["vapWEPsecurityConfigTable.vapWEPkey4"] = html.var(
                                        "vapWEPsecurityConfigTable.vapWEPkey4")
                                    wep_flag = 1
                                else:
                                    wep_field_flag = 4
                                    # flag = 1
                                    # ic_result["success"]=1
                                    # dic_result["result"] = "WEP key4 must be
                                    # the length of 5,13 or 16"
                            else:
                                wep_flag_error = 4
                                # flag = 1
                                # dic_result["success"] = 1
                                # dic_result["result"]="WEP Key4 is required"

                    if html.var("vapWEPsecurityConfigTable.vapWEPkey1") != None and len(
                            html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 0:
                        dic_result["vapWEPsecurityConfigTable.vapWEPkey1"] = ""
                    else:
                        if (len(html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 5 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 13 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 16):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey1"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey1")
                            wep_flag = 1
                        elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 10 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 26 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey1")) == 32) and Validation.is_hex_number(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey1")):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey1"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey1")
                            wep_flag = 1
                        else:
                            wep_field_flag = 1
                    if html.var("vapWEPsecurityConfigTable.vapWEPkey2") != None and len(
                            html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 0:
                        dic_result["vapWEPsecurityConfigTable.vapWEPkey2"] = ""
                    else:
                        if (len(html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 5 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 13 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 16):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey2"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey2")
                            wep_flag = 2
                        elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 10 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 26 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey2")) == 32) and Validation.is_hex_number(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey2")):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey2"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey2")
                            wep_flag = 1
                        else:
                            wep_field_flag = 2

                    if html.var("vapWEPsecurityConfigTable.vapWEPkey3") != None and len(
                            html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 0:
                        dic_result["vapWEPsecurityConfigTable.vapWEPkey3"] = ""
                    else:
                        if (len(html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 5 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 13 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 16):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey3"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey3")
                            wep_flag = 3
                        elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 10 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 26 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey3")) == 32) and Validation.is_hex_number(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey3")):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey3"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey3")
                            wep_flag = 1
                        else:
                            wep_field_flag = 3
                    if html.var("vapWEPsecurityConfigTable.vapWEPkey4") != None and len(
                            html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 0:
                        dic_result["vapWEPsecurityConfigTable.vapWEPkey4"] = ""
                    else:
                        if (len(html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 5 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 13 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 16):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey4"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey4")
                            wep_flag = 4
                        elif (len(html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 10 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 26 or len(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey4")) == 32) and Validation.is_hex_number(
                                html.var("vapWEPsecurityConfigTable.vapWEPkey4")):
                            dic_result["vapWEPsecurityConfigTable.vapWEPkey4"] = html.var(
                                "vapWEPsecurityConfigTable.vapWEPkey4")
                            wep_flag = 1
                        else:
                            wep_field_flag = 4

                    # this for the wep
                    if wep_flag > 0 and wep_field_flag > 0:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "WEP key%s Length can be 5,13,16 for ASCII and 10,26,32 for HEX" % wep_field_flag
                    elif wep_flag == 0 and wep_field_flag > 0:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "WEP key%s Length can be 5,13,16 for ASCII and 10,26,32 for HEX" % wep_field_flag
                    elif wep_flag > 0 and wep_field_flag == 0:
                        pass
                    elif wep_flag == 0 and wep_field_flag == 0:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result["result"] = "WEP key%s is required" % html.var(
                            "vapWEPsecurityConfigTable.vapWEPprimaryKey")

                    dic_result["vapWEPsecurityConfigTable.vapWEPprimaryKey"] = html.var(
                        "vapWEPsecurityConfigTable.vapWEPprimaryKey")
            else:

                dic_result["basicVAPconfigTable.vapSecurityMode"] = html.var(
                    "basicVAPconfigTable.vapSecurityMode")
                if html.var("vapWPAsecurityConfigTable.vapWPAmode") != None:
                    dic_result["vapWPAsecurityConfigTable.vapWPAmode"] = html.var(
                        "vapWPAsecurityConfigTable.vapWPAmode")

                if html.var("vapWPAsecurityConfigTable.vapWPAcypher") != None:
                    dic_result["vapWPAsecurityConfigTable.vapWPAcypher"] = html.var(
                        "vapWPAsecurityConfigTable.vapWPAcypher")

                if html.var("vapWPAsecurityConfigTable.vapWPArekeyInterval") != None:
                    if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPArekeyInterval")):
                        if Validation.is_number(html.var("vapWPAsecurityConfigTable.vapWPArekeyInterval")):
                            dic_result["vapWPAsecurityConfigTable.vapWPArekeyInterval"] = html.var(
                                "vapWPAsecurityConfigTable.vapWPArekeyInterval")
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Rekey Interval must be number"
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result["result"] = "WPA Rekey Interval is required"

                if html.var("vapWPAsecurityConfigTable.vapWPAmasterReKey") != None:
                    if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPAmasterReKey")):
                        if Validation.is_number(html.var("vapWPAsecurityConfigTable.vapWPAmasterReKey")):
                            dic_result["vapWPAsecurityConfigTable.vapWPAmasterReKey"] = html.var(
                                "vapWPAsecurityConfigTable.vapWPAmasterReKey")
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Master Rekey Interval must be number"
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "WPA Master Rekey Interval is required"

                if html.var("vapWPAsecurityConfigTable.vapWPAmode") == '0' or int(
                                html.var("vapWPAsecurityConfigTable.vapWPAmode") == 0):
                    if html.var("vapWPAsecurityConfigTable.vapWEPrekeyInt") != None:
                        if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWEPrekeyInt")):
                            if Validation.is_number(html.var("vapWPAsecurityConfigTable.vapWEPrekeyInt")):
                                dic_result["vapWPAsecurityConfigTable.vapWEPrekeyInt"] = html.var(
                                    "vapWPAsecurityConfigTable.vapWEPrekeyInt")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "WPA Pre Key Interval must be number"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Master Rekey Interval is required"
                else:
                    if html.var("vapWPAsecurityConfigTable.vapWEPrekeyInt") != None:
                        if Validation.is_number(html.var("vapWPAsecurityConfigTable.vapWEPrekeyInt")):
                            dic_result[
                                "vapWPAsecurityConfigTable.vapWEPrekeyInt"] = 600
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Pre Key Interval must be number"
                    else:
                        dic_result["vapWPAsecurityConfigTable.vapWEPrekeyInt"] = html.var(
                            "vapWPAsecurityConfigTable.vapWEPrekeyInt")

                if html.var("vapWPAsecurityConfigTable.vapWPAkeyMode") != None:

                    if int(html.var("vapWPAsecurityConfigTable.vapWPAkeyMode")) == 0:
                        dic_result["vapWPAsecurityConfigTable.vapWPAkeyMode"] = html.var(
                            "vapWPAsecurityConfigTable.vapWPAkeyMode")
                        if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPAkeyMode")):
                            if int(len(html.var("vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase"))) >= 8 and int(
                                    len(html.var("vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase"))) <= 32:
                                dic_result["vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase"] = html.var(
                                    "vapWPAsecurityConfigTable.vapWPAconfigPSKPassPhrase")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "Key length should be in 8 to 32 characters"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result["result"] = "Pass Phrase is required"
                    else:
                        dic_result["vapWPAsecurityConfigTable.vapWPAkeyMode"] = html.var(
                            "vapWPAsecurityConfigTable.vapWPAkeyMode")
                        if html.var("vapWPAsecurityConfigTable.vapWPArsnPreAuth") != None:
                            dic_result["vapWPAsecurityConfigTable.vapWPArsnPreAuth"] = html.var(
                                "vapWPAsecurityConfigTable.vapWPArsnPreAuth")
                        if html.var("vapWPAsecurityConfigTable.vapWPArsnPreAuthInterface") != None:
                            dic_result["vapWPAsecurityConfigTable.vapWPArsnPreAuthInterface"] = html.var(
                                "vapWPAsecurityConfigTable.vapWPArsnPreAuthInterface")

                        if html.var("vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod") != None:
                            if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod")):
                                if Validation.is_number(html.var("vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod")):
                                    dic_result["vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod"] = html.var(
                                        "vapWPAsecurityConfigTable.vapWPAeapReAuthPeriod")
                                else:
                                    flag = 1
                                    dic_result["success"] = 1
                                    dic_result[
                                        "result"] = "WPA Reauth period must be number"
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "WPA Reauth period is required"

                    if html.var("vapWPAsecurityConfigTable.vapWPAserverIP") != None:
                        if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPAserverIP")):
                            if Validation.is_valid_ip(
                                    html.var("vapWPAsecurityConfigTable.vapWPAserverIP")) and html.var(
                                    "vapWPAsecurityConfigTable.vapWPAserverIP") not in ["0.0.0.0"] and int(
                                    html.var("vapWPAsecurityConfigTable.vapWPAserverIP").split('.')[-1]) not in [0,
                                                                                                                 255]:
                                dic_result["vapWPAsecurityConfigTable.vapWPAserverIP"] = html.var(
                                    "vapWPAsecurityConfigTable.vapWPAserverIP")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "Invalid WPA Server IPAddress"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Server IPAddress is required"

                    if html.var("vapWPAsecurityConfigTable.vapWPAserverPort") != None:
                        if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPAserverPort")):
                            if Validation.is_number(html.var("vapWPAsecurityConfigTable.vapWPAserverPort")):
                                dic_result["vapWPAsecurityConfigTable.vapWPAserverPort"] = html.var(
                                    "vapWPAsecurityConfigTable.vapWPAserverPort")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result[
                                    "result"] = "WPA Server Port must be number"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Server Port is required"

                    if html.var("vapWPAsecurityConfigTable.vapWPAsharedSecret") != None:
                        if Validation.is_required(html.var("vapWPAsecurityConfigTable.vapWPAsharedSecret")):
                            dic_result["vapWPAsecurityConfigTable.vapWPAsharedSecret"] = html.var(
                                "vapWPAsecurityConfigTable.vapWPAsharedSecret")
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "WPA Shared Secret is required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))

        else:

            time.sleep(2)
            # html.write(str(dic_result)+str(selectedvap)+(vap_id))
            result = obj_bll_set_valid.vap_set(
                host_id, device_type, dic_result, selectedvap, vap_id)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ap_common_submit") == "Cancel":
        if html.var("vapSelection.selectVap") != None:
            dic_result["vapSelection.selectVap"] = html.var(
                "vapSelection.selectVap")
        if html.var("vapWPAsecuritySetup.aclState") != None:
            dic_result["vapWPAsecuritySetup.aclState"] = html.var(
                "vapWPAsecuritySetup.aclState")
        if html.var("vapWPAsecuritySetup.aclMode") != None:
            dic_result["vapWPAsecuritySetup.aclMode"] = html.var(
                "vapWPAsecuritySetup.aclMode")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ip_mac_search(h):
    # pass
    """

    @param h:
    """
    global html
    html = h
    ip_mac_list = []
    final_result = {}
    search_value = html.var("s")
    total_records = html.var("totalRecord")
    obj = IpMacSearch()
    ##    device_type = html.var("device_type")
    ##    if device_type == "None":
    ##        device_type = ""
    device_type = ""
    user_id = html.req.session['user_id']
    ip_mac_search = html.var("ip_mac_search")
    result = obj.ip_search(device_type, search_value, user_id, ip_mac_search)
    if len(result) != []:
        for i in range(0, len(result)):
            ip_mac_list.append({'Name': result[i][0], 'Hidden': ""})
    final_result = {'items': ip_mac_list}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(final_result)))


def show_wireless_status(h):
    """

    @param h:
    """
    global html
    html = h
    wifi_mode = {0: 'wifi11g', 1: 'wifi11gnHT20', 2:
        'wifi11gnHT40plus', 3: 'wifi11gnHT40minus'}
    wap_security = {0: 'Open', 1: 'WEP', 2: 'WPA'}
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_ap_data = IduGetData()

    result_dic = {'success': 0, 'result': {}}
    vap_data = {}
    wireless_data = obj_ap_data.common_get_data('Ap25RadioSetup', host_id)
    basic_vap_data = obj_ap_data.common_get_data(
        'Ap25BasicVAPconfigTable', host_id)
    basic_vap_security_data = obj_ap_data.common_get_data(
        'Ap25BasicVAPsecurity', host_id)
    html_str = ""
    if len(wireless_data) > 0:
        result_dic['result'].update({'channel': "-" if wireless_data[0]
                                                       .radioChannel == None else wireless_data[0].radioChannel})
        result_dic['result'].update(
            {'wifimode': "-" if wireless_data[0].wifiMode == None else wifi_mode[int(wireless_data[0].wifiMode)]})
        result_dic['result'].update({'txpower': "-" if wireless_data[0]
                                                       .radioTxPower == None else wireless_data[0].radioTxPower})
        result_dic['result'].update({'txrxchain': "-" if wireless_data[0].radioTXChainMask == None and wireless_data[
            0].radioRXChainMask == None else str(wireless_data[
            0].radioTXChainMask) + "x" + str(wireless_data[0].radioRXChainMask)})

        if wireless_data[0].radioAPmode != None:
            if int(wireless_data[0].radioAPmode) == 1 or int(wireless_data[0].radioAPmode) == 3:
                activevap = 1
            elif int(wireless_data[0].radioAPmode) == 2:
                activevap = 2
            else:
                activevap = 0 if wireless_data[
                                     0].numberOfVAPs == None else wireless_data[0].numberOfVAPs
        else:
            activevap = 0

        for i in range(0, activevap):
            if len(basic_vap_data) > 0 and len(basic_vap_security_data) > 0:
                vap_data.update(
                    {'ssid%s' % (i): "-" if basic_vap_data[i].vapESSID == None else basic_vap_data[i].vapESSID,
                     'security%s' % (i): "-" if basic_vap_security_data[i].vapSecurityMode == None else wap_security[
                         int(basic_vap_security_data[i].vapSecurityMode)]})
        result_dic['result'].update({'vapstats': vap_data})

    html_str += "<table id=\"table_status\" name=\"table_status\" class=\"yo-table\"  style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    ##    #html_str+="<tr><th>Channel</th>\
    ##    #            <td>%s</td></tr>"%(result_dic['result']['channel'])
    ##    html_str+="<tr><th>Wifimode</th>\
    ##                <td>%s</td></tr>"%(result_dic['result']['wifimode'])
    ##    html_str+="<tr><th>Tx Power</th>\
    ##                <td>%s</td></tr>"%(result_dic['result']['txpower'])
    ##    html_str+="<tr><th>Tx & Rx Chain</th>\
    ##                <td>%s</td></tr>"%(result_dic['result']['txrxchain'])

    html_str += "<tr><th colspan=2>Active VAPs</th></tr>"
    html_str += "<tr><th>SSID</th>\
                <th>Security</th></tr>"
    for i in range(0, activevap):
        html_str += "<tr><td>%s</td>\
                <td>%s</td></tr>" % (
        result_dic['result']['vapstats']['ssid%s' % i], result_dic['result']['vapstats']['security%s' % i])

    html_str += "</table>"
    html.write(str(html_str))


def service_status(h):
    """

    @param h:
    """
    global html
    html = h
    status = {0: 'Disabled', 1: 'Enabled'}
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_ap_data = IduGetData()
    dhcp_data = obj_ap_data.common_get_data('Ap25DhcpServer', host_id)
    service_data = obj_ap_data.common_get_data('Ap25Services', host_id)
    html_str = ""
    html_str += "<table id=\"table_status\" name=\"table_status\" class=\"yo-table\"  style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    if len(dhcp_data) > 0:
        html_str += "<tr><th>DHCP Server</th>\
                <td>%s</td></tr>" % (
        "-" if dhcp_data[0].dhcpServerStatus == None else status[dhcp_data[0].dhcpServerStatus])
    if len(service_data) > 0:
        html_str += "<tr><th>UPnP Server</th>\
                <td>%s</td></tr>" % (
        "-" if service_data[0].upnpServerStatus == None else status[service_data[0].upnpServerStatus])
        html_str += "<tr><th>System Log</th>\
                <td>%s</td></tr>" % (
        "-" if service_data[0].systemLogStatus == None else status[service_data[0].systemLogStatus])
    else:
        html_str += "<tr><td>No Data Available</td></tr>"

    html.write(html_str)


def system_info(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_ap_data = IduGetData()
    system_data = obj_ap_data.common_get_data_by_host('Ap25Versions', host_id)
    ip_setting_data = obj_ap_data.common_get_data(
        'Ap25AccesspointIPsettings', host_id)
    html_str = ""
    html_str += "<table id=\"table_status\" name=\"table_status\" class=\"yo-table\"  style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    if len(system_data) > 0:
        html_str += "<tr><th>Hardware Version</th>\
                <td>%s</td></tr>" % (
        "-" if system_data[0].hardwareVersion == None or system_data[0].hardwareVersion == "" else system_data[
            0].hardwareVersion)
        html_str += "<tr><th>Software Version</th>\
                <td>%s</td></tr>" % (
        "-" if system_data[0].softwareVersion == None or system_data[0].softwareVersion == "" else system_data[
            0].softwareVersion)
    if len(ip_setting_data) > 0:
        html_str += "<tr><th>Primary DNS</th>\
        <td>%s</td></tr>" % (
        "-" if ip_setting_data[0].lanPrimaryDNS == None or ip_setting_data[0].lanPrimaryDNS == "" else ip_setting_data[
            0].lanPrimaryDNS)
        html_str += "<tr><th>Secondary DNS</th>\
                <td>%s</td></tr>" % (
        "-" if ip_setting_data[0].lanSecondaryDNS == None or ip_setting_data[0].lanSecondaryDNS == "" else
        ip_setting_data[0].lanSecondaryDNS)

    else:
        html_str += "<tr><td>No Data Available</td></tr>"
    html.write(html_str)


def show_radio_admin(h):
    """

    @param h:
    """
    global html
    html = h
    html_str = ""
    obj_idu_get_data = IduGetData()
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    main_admin_list = obj_idu_get_data.common_get_data(
        'Ap25RadioSetup', host_id)
    html_str = "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    html_str += "<th>Radio State</th>"
    if len(main_admin_list) > 0:
        for i in range(0, len(main_admin_list)):
            html_str += "<td><img src=\"%s\" class=\"n-reconcile\" title=\"%s\" id=\"main_admin\" name=\"main_admin\" style=\"width:10px;height:10px;\" state=\"%s\" onClick=\"radio_enable_disable(event,this,'%s','radioSetup.radioState');\"/></td></tr>" \
                        % (
                "images/temp/green_dot.png" if int(
                    main_admin_list[
                        i].radioState) == 1 else "images/temp/red_dot.png",
                "Radio Enable" if int(
                    main_admin_list[
                        i].radioState) == 1 else "Radio Disable",
                1 if int(main_admin_list[i].radioState) == 1 else 0,
                host_id)
    else:
        html_str += "<tr><td colspan=2>No Data Available</td></tr>"
    html_str += "</table>"
    html.write(html_str)


def disable_enable_radio(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    admin_state_name = html.var("admin_state_name")
    state = html.var("state")
    obj = APRadioState()
    result_dic = obj.radio_enable_disable(
        host_id, admin_state_name, int(state))
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def chk_radio_state(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj = APRadioState()
    result = obj.chk_radio_status(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def connected_clients(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj = APConnectedClients()
    result = obj.total_connected_clients(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def ap_form_reconcile(h):
    """

    @param h:
    """
    global html
    html = h
    if html.var("host_id") != None:
        host_id = html.var("host_id")
    if html.var("formName") != None:
        formname = html.var("formName")
    if html.var("device_type") != None:
        device_type = html.var("device_type")
        # obj_form = OduConfiguration()
    result = eval("APForms.%s(%s,'%s')" % (formname, host_id, device_type))
    html.write(str(result))
