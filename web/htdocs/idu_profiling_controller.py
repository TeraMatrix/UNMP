#!/usr/bin/python2.6

"""
@author:Anuj Samariya
@since: 27 June 2011
@version: 0.0
@date: 27 June 2011
@note: In this file there are many classes and functions which create forms of idu Profiling and shows the forms on page,
       there is a functions which shows list of devices which are available on site and functions which take values of page
       and call the controller functions and pass the page values on that function and according to response it shows the
       profiling page values are set or not set.
@organisation: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
"""

from utility import ErrorMessages
from common_controller import page_header_search, DeviceStatus
from idu_profiling import IduProfiling, IduForms
from idu_profiling_bll import *
from json import JSONEncoder
from utility import Validation
from time import sleep


def idu_listing(h):
    """

    @param h:
    """
    try:
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
        css_list = ["css/demo_table_jui.css",
                    "css/jquery-ui-1.8.4.custom.css", 'css/ccpl_jquery_combobox.css']
        javascript_list = ["js/lib/main/jquery.dataTables.min.js",
                           'js/unmp/main/ccpl_jquery_autocomplete.js', "js/unmp/main/idu_listing.js"]
        snapin_list = ["reports", "views", "Alarm", "Inventory", "Settings",
                       "NetworkMaps", "user_management", "schedule", "Listing"]
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
        html.new_header("IDU Listing", "idu_listing.py", "",
                        css_list, javascript_list, snapin_list)

        # Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write
        # we pass parameters
        # ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
        html.write(str(page_header_search(ip_address, mac_address,
                                          "RM18,RM,IDU,Access Point,CCU", selected_device_type, "enabled",
                                          "device_type")))

        # Here we make a div to show the result in datatable
        html.write(IduProfiling.idu_listing())
        html.new_footer()
    except Exception as e:
        html.write(str(e))


def idu_profiling(h):
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
                "css/jquery.multiselect.css", "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css",
                'css/ccpl_jquery_combobox.css']
    jss_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", 'js/lib/main/jquery.dataTables.min.js', 'js/unmp/main/ccpl_jquery_autocomplete.js',
        'js/unmp/main/idu_controller.js', 'js/lib/main/jquery-ui-personalized-1.6rc2.min.js']
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
        if device_list_parameter == [] or device_list_parameter == None:
            html.write(page_header_search(
                "", "", "RM18,RM,IDU,CCU", None, "enabled", "device_type"))
            # call the function of common_controller , it is used
            # for listing the Devices based on
            # IPaddress,Macaddress,DeviceTy
        else:
            html.new_header("%s %s Configuration" % ("IDU", device_list_parameter[0]
            .ip_address), "idu_listing.py", "", css_list, jss_list, snapin_list)
            html.write(
                page_header_search(
                    device_list_parameter[0][
                        0], device_list_parameter[0][1], "RM18,RM,IDU,CCU",
                    device_type, device_list_state, "device_type"))
            html.write(IduProfiling.idu_div(device_list_parameter[0][0],
                                            device_list_parameter[0][1], host_id))
    elif isinstance(device_list_parameter, Exception):
        html.write("DataBase Error Occured")
    html.new_footer()


# def page_tip_idu_listing(h):
#     global html
#     html = h
#     html.write(str(IduProfiling.page_tip_idu_listing()))
#
#
# def page_tip_idu_profiling(h):
#     global html
#     html = h
#     html.write(str(IduProfiling.page_tip_idu_profiling()))


def idu_device_listing_table(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally
    @var ip_address : this is used to store the ip address
    @var mac_address : this is used to store the mac address
    @var selected_device : this is used to store the device type id i.e. odu16,odu00
    @var result : this is used to store the result which is a list of devices according to the search criteria
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to give the list of selected device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    idu_device_list_bll_obj = IduDeviceList()
    obj_get_data = IduGetData()
    obj_link_count = IduLinkCount()
    result_device_list = []
    device_list_state = "enabled"
    global html
    html = h
    obj_device_status = DeviceStatus()
    # this is the result which we show on the page
    result = ""
    userid = html.req.session['user_id']
    device_status_host_id = ""
    ## Mahipal data table
    i_display_start = str(html.var("iDisplayStart"))
    i_display_length = str(html.var("iDisplayLength"))
    s_search = str(html.var("sSearch"))
    sEcho = str(html.var("sEcho"))
    s_search = str(html.var("sSearch"))
    sSortDir_0 = str(html.var("sSortDir_0"))
    iSortCol_0 = str(html.var("iSortCol_0"))
    html_req = html.req.vars
    ###########################

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
        selected_device = "idu4"
    else:
        selected_device = html.var("device_type")
        # call the function get_odu_list of odu-controller which return us the
    # list of devices in two dimensional list according to
    # IPAddress,MACaddress,SelectedDevice

    device_dict = idu_device_list_bll_obj.idu_device_list(
        ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0,
        iSortCol_0, userid, html_req)
    #[1, "172.22.0.120", "Default", "172.22.0.120",
    device_list = device_dict["aaData"]
    index = int(device_dict["i_display_start"])
    # display the result on page
    # This is a empty list variable used for storing the device list
    if isinstance(device_list, list):
        for i in range(0, len(device_list)):
            if device_list[i][8] <= 35:
                images = 'images/new/r-red.png'
            elif device_list[i][8] <= 90:
                images = 'images/new/r-black.png'
            else:
                images = 'images/new/r-green.png'

            snmp_up_time_data = obj_device_status.common_list_device_status(
                device_list[i][0])

            device_status = snmp_up_time_data['result']['device_status'][0]
            device_status_image_path = snmp_up_time_data[
                'result']['device_status'][1]
            e1_port_list = obj_get_data.common_get_data(
                'IduE1PortConfigurationTable', device_list[i][0])
            main_admin_state_list = obj_get_data.common_get_data(
                'IduIduAdminStateTable', device_list[i][0])
            main_admin_image_class = "red"
            main_admin_title = "IDU Admin Unlocked"
            if len(main_admin_state_list) > 0:
                if int(main_admin_state_list[0].adminstate) == 1:
                    main_admin_image_class = "green"
                    main_admin_title = "IDU Admin Unlocked"
                else:
                    main_admin_image_class = "red"
                    main_admin_title = "IDU Admin Locked"
            else:
                main_admin_image_path = "images/temp/red_dot.png"

            link_port_dic = obj_link_count.link_count(device_list[i][0])
            if link_port_dic['success'] == 0:
                if int(link_port_dic['result']) <= 35:
                    link_image_class = "red"
                elif int(link_port_dic['result']) <= 90:
                    link_image_class = "yellow"
                else:
                    link_image_class = "green"
                link_title = str(link_port_dic['result']) + "% Links Unlocked"
            else:
                link_image_class = "red"
                link_title = "No Link Exists"
            if i == len(device_list) - 1:
                device_status_host_id += str(device_list[i][0])
            else:
                device_status_host_id += str(device_list[i][0]) + ","
            temp_list = []
            monitoring_status = "<a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"><img src=\"images/new/info.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile\"/></a>" % (
            'sp_status_profiling.py',
            device_list[i][0], device_list[i][7], device_list_state) if device_list[i][
                                                                            7] == "idu4" else "<img src=\"images/new/info.png\" style=\"width:16px;height:16px;\" title=\"Current Device Status\" class=\"imgbutton n-reconcile\"/>"
            if html.req.session["role"] == "admin" or html.req.session["role"] == "user":
                result_device_list.append([
                    "<center><img id=\"device_status\" name=\"device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton w-reconcile\" /></center>"
                    % (device_status_image_path, device_status),
                    device_list[i][1], device_list[i][2], device_list[i][3], device_list[i][4],
                    "" if device_list[i][5] == None else device_list[i][5],
                    "-" if device_list[i][6] == None else "Slave IDU" if int(device_list[i][6]) == 1 else "Master IDU"])
                temp_list.append(
                    "<ul class=\"button_group\" style=\"width: 113px;\">")
                for j in range(0, len(e1_port_list)):
                    temp_list.append("<li><a class=\"%s imgEditodu16 n-reconcile\" title=\"E1 Port%s %s\" id=\"e1_admin_state_%s\" name=\"admin_state_%s\" state=\"%s\" \
                    onClick=\"idu_admin_state_change(event,this,'%s','%s','%s','iduConfiguration.e1PortConfigurationTable.adminState',0);\">E1</a></li>"
                                     % (
                        "green" if int(e1_port_list[j].adminState) == 1 else "red", str(
                            e1_port_list[j].portNumber),
                        "Unlocked" if int(e1_port_list[j].adminState) == 1 else "Locked",
                        e1_port_list[j].portNumber, e1_port_list[
                            j].portNumber,
                        1 if int(e1_port_list[
                            j].adminState) == 1 else 0,
                        device_list[i][0], e1_port_list[j].idu_e1PortConfigurationTable_id, e1_port_list[j].portNumber))

                temp_list.append(
                    '<li><a class=\"%s n-reconcile imgEditodu16\" title=\"%s\" onclick=\"main_admin_state_change(event,this,\'%s\',\'iduinfo.iduAdminStateTable.adminstate\'); \"/>A</a></li>' % (
                    main_admin_image_class, main_admin_title,
                    device_list[i][0]))
                temp_list.append(
                    '<li><a class=\"%s n-reconcile imgEditodu16\" title=\"%s\" onclick=\"show_link_admin_state(event,this,\'%s\',\'%s\');\"/>L</a></li>' %
                    (link_image_class, link_title, device_list[i][0], device_list[i][7]))
                temp_list.append("</ul>")
                result_device_list[i].append("".join(temp_list))
                temp_list = []
                temp_list.append("<a target=\"main\" href=\"idu_profiling.py?host_id=%s&device_type=%s&device_list_state=%s\">\
                <img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\">\
                <img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\">\
                <img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"javascript:iduFirmwareUpdate('%s','%s','%s');\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"imgReconcile(this,'%s','%s','idu_','True'); state_rec=0\"/>\
                &nbsp;&nbsp;%s%s"
                                 % (
                    device_list[i][0], device_list[i][
                        7], device_list_state, device_list[
                        i][0],
                    'sp_dashboard_profiling.py' if device_list[i][
                                                       7] == "idu4" else 'sp_dashboard_profiling.py',
                    device_list[i][0], device_list[i][
                        7], device_list_state, device_list[
                        i][
                        3], device_list[
                        i][0], device_list[i][7],
                    device_list_state, images, device_list[i][
                        8], device_list[
                        i][
                        0], device_list[
                        i][7], monitoring_status,
                    "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (
                    device_status_host_id) if i == len(device_list) - 1 else ""))
                result_device_list[i].append(" ".join(temp_list))
            else:
                result_device_list.append([
                    "<center><img id=\"device_status\" name=\"device_status\" src=\"%s\" title=\"%s\" style=\"width:8px;height:8px;\" class=\"imgbutton w-reconcile\" /></center>"
                    % (device_status_image_path, device_status),
                    device_list[i][1], device_list[i][2], device_list[i][3], device_list[i][4], device_list[i][5],
                    "Slave IDU" if int(device_list[i][6]) == 1 else "Master IDU"])
                temp_list.append(
                    "<ul class=\"button_group\" style=\"width: 170px;\">")
                for j in range(0, len(e1_port_list)):
                    temp_list.append("<li><a class=\"%s imgEditodu16 n-reconcile\" title=\"E1 Port%s %s\" id=\"e1_admin_state_%s\" name=\"admin_state_%s\" state=\"%s\" \
                    onClick=\"idu_admin_state_change(event,this,'%s','%s','%s','iduConfiguration.e1PortConfigurationTable.adminState',0);\">E1</a></li>"
                                     % (
                        "green" if int(e1_port_list[j].adminState) == 1 else "red", str(
                            e1_port_list[j].portNumber),
                        "Unlocked" if int(e1_port_list[j].adminState) == 1 else "Locked",
                        e1_port_list[j].portNumber, e1_port_list[
                            j].portNumber,
                        1 if int(e1_port_list[
                            j].adminState) == 1 else 0,
                        device_list[i][0], e1_port_list[j].idu_e1PortConfigurationTable_id, e1_port_list[j].portNumber))

                temp_list.append(
                    '<li><a class=\"%s n-reconcile imgEditodu16\" title=\"%s\" onclick=\"main_admin_state_change(event,this,\'%s\',\'iduinfo.iduAdminStateTable.adminstate\'); \"/>A</a></li>' % (
                    main_admin_image_class, main_admin_title,
                    device_list[i][0]))
                temp_list.append(
                    '<li><a class=\"%s n-reconcile imgEditodu16\" title=\"%s\" onclick=\"show_link_admin_state(event,this,\'%s\',\'%s\');\"/>L</a></li>' %
                    (link_image_class, link_title, device_list[i][0], device_list[i][7]))
                temp_list.append("</ul>")
                result_device_list[i].append("".join(temp_list))
                temp_list = []
                temp_list.append("<a target=\"main\">\
                <img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\">\
                <img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\">\
                <img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\"><img src=\"images/new/update.png\" title=\"Firmware Upgrade\" class=\"imgbutton imgEditodu16 n-reconcile\"/></a>&nbsp;&nbsp;\
                <img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" state_rec=\"0\"/>\
                &nbsp;&nbsp;%s%s"
                                 % (device_list[i][0],
                                    'sp_dashboard_profiling.py' if device_list[i][
                                                                       7] == "idu4" else 'sp_dashboard_profiling.py',
                                    device_list[i][0], device_list[i][
                    7], device_list_state, device_list[
                                        i][
                                        3], images, device_list[
                                        i][8], monitoring_status,
                                    "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (
                                    device_status_host_id) if i == len(device_list) - 1 else ""))
                result_device_list[i].append(" ".join(temp_list))
    html.req.content_type = 'application/json'
    device_dict["aaData"] = result_device_list
    html.req.write(str(JSONEncoder().encode(device_dict)))


def get_device_list_idu_profiling(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        idu_device_list_bll_obj = IduDeviceList()
        # this is the result which we show on the page
        result = ""
        ip_address = ""
        mac_address = ""
        selected_device = "idu4"
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
            selected_device = "idu4"
        else:
            selected_device = html.var("selected_device_type")

        # call the function get_odu_list of odu-controller which return us the
        # list of devices in two dimensional list according to
        # IPAddress,MACaddress,SelectedDevice

        device_list = idu_device_list_bll_obj.idu_device_list_profiling(
            ip_address, mac_address, selected_device)
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
                result)  # call the idu_profiling_controller function get_device_param returns the list.List Contains ipaddress,macaddress,devicetypeid,config_profile_id
            # html.write(str(device_list_parameter))
            html.write(IduProfiling.idu_profile_call(
                result, selected_device, device_list_parameter))
    except Exception as e:
        html.write(str(e[-1]))


def alarm_port_form(h):
    """

    @param h:
    """
    global html
    html = h
    alarm_port_list = []
    idu_get_database_obj = IduGetDatabase()
    alarm_port_id = html.var("alarmPortId")
    alarm_port_list = idu_get_database_obj.alarm_get_list(alarm_port_id)
    if isinstance(alarm_port_list, list):
        html.write(IduForms.alarm_port_form(alarm_port_list))
    elif isinstance(alarm_port_list, Exception):
        html.write(str(e))


def port_configuration_form(h):
    """

    @param h:
    """
    global html
    html = h
    port_configuration_list = []
    idu_get_database_obj = IduGetDatabase()
    port_configuration_id = html.var("portConfigurationId")
    host_id = html.var("hostId")
    id_name = html.var("idName")
    class_name = html.var("className")
    selected_device = html.var("selected_device")
    port_configuration_list = idu_get_database_obj.common_get_data_by_id(
        port_configuration_id, host_id, id_name, class_name)
    if isinstance(port_configuration_list, list):
        html.write(IduForms.port_configuration_form(port_configuration_list,
                                                    host_id, selected_device, port_configuration_id))
    elif isinstance(port_configuration_list, Exception):
        html.write(str(e))


def port_bandwidth_form(h):
    """

    @param h:
    """
    global html
    html = h
    port_bandwidth_list = []
    idu_get_database_obj = IduGetDatabase()
    port_bandwidth_id = html.var("portBandwidthId")
    host_id = html.var("hostId")
    id_name = html.var("idName")
    class_name = html.var("className")
    selected_device = html.var("selected_device")
    # index = html.var("index")
    port_bandwidth_list = idu_get_database_obj.common_get_data_by_id(
        port_bandwidth_id, host_id, id_name, class_name)
    if isinstance(port_bandwidth_list, list):
        html.write(str(IduForms.port_bandwidth_form(port_bandwidth_list,
                                                    host_id, selected_device, port_bandwidth_id)))
    elif isinstance(port_bandwidth_list, Exception):
        html.write(str(e))


def port_QinQ_form(h):
    """

    @param h:
    """
    global html
    html = h
    port_bandwidth_list = []
    idu_get_database_obj = IduGetDatabase()
    port_bandwidth_id = html.var("portQinQId")
    host_id = html.var("hostId")
    id_name = html.var("idName")
    class_name = html.var("className")
    selected_device = html.var("selected_device")
    # index = html.var("index")
    port_bandwidth_list = idu_get_database_obj.common_get_data_by_id(
        port_bandwidth_id, host_id, id_name, class_name)
    if isinstance(port_bandwidth_list, list):
        html.write(str(IduForms.port_QinQ_form(port_bandwidth_list,
                                               host_id, selected_device, port_bandwidth_id)))
    elif isinstance(port_bandwidth_list, Exception):
        html.write(str(e))


def e1_port(h):
    """

    @param h:
    """
    global html
    html = h
    port_e1_list = []
    idu_get_database_obj = IduGetDatabase()
    port_e1_id = html.var("porte1Id")
    host_id = html.var("hostId")
    id_name = html.var("idName")
    class_name = html.var("className")
    selected_device = html.var("selected_device")
    # index = html.var("index")
    port_e1_list = idu_get_database_obj.common_get_data_by_id(
        port_e1_id, host_id, id_name, class_name)
    if isinstance(port_e1_list, list):
        html.write(str(IduForms.form_e1_port(
            port_e1_list, host_id, selected_device, port_e1_id)))
    elif isinstance(port_e1_list, Exception):
        html.write(str(e))


def update_e1_port_table(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        idu_get_database_obj = IduGetDatabase()
        host_id = html.var("host_id")
        selected_device = html.var("selected_device")
        html.write(str(IduForms.table_e1_port(host_id, selected_device)))
    except Exception as e:
        html.write(str(e))


def e1_port_form_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    id = None
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("e1_port_id") != None:
            if obj_bll_cancel_set_valid.chk_link_e1_port(host_id, int(html.var("e1_port_id"))) == 0:
                id = html.var("e1_port_id")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result[
                    "result"] = "Delete all link in this port before applying this change"
        if html.var("index_id") != None:
            index = html.var("index_id")
        if html.var("iduConfiguration.e1PortConfigurationTable.clockSource") != None:
            if Validation.is_required(html.var("iduConfiguration.e1PortConfigurationTable.clockSource")):
                dic_result["iduConfiguration.e1PortConfigurationTable.clockSource"] = html.var(
                    "iduConfiguration.e1PortConfigurationTable.clockSource")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Clock source is required"

        if html.var("iduConfiguration.e1PortConfigurationTable.lineType") != None:
            if Validation.is_required(html.var("iduConfiguration.e1PortConfigurationTable.lineType")):
                dic_result["iduConfiguration.e1PortConfigurationTable.lineType"] = html.var(
                    "iduConfiguration.e1PortConfigurationTable.lineType")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Link Type is required"

            ##        if html.var("iduConfiguration.e1PortConfigurationTable.lineCode")!=None:
            ##            if Validation.is_required(html.var("iduConfiguration.e1PortConfigurationTable.lineCode")):
            ##                dic_result["iduConfiguration.e1PortConfigurationTable.lineCode"]=html.var("iduConfiguration.e1PortConfigurationTable.lineCode")
            ##            else:
            ##                flag = 1
            ##                dic_result["success"] = 1
            ##                dic_result["result"] = "Line code is required"

            ##        if html.var("adminState")!=None:
            ##            if Validation.is_required(html.var("adminState")):
            ##                dic_result["adminState"]=html.var("adminState")

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(str(host_id)+str(device_type_id)+str(dic_result)+str(id)+str(index)))
            result = obj_bll_cancel_set_valid.e1_port_set(
                host_id, device_type_id, dic_result, id, index)
            # time.sleep(7)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))
            # html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("e1_port_id") != None:
            id = html.var("e1_port_id")
        if html.var("iduConfiguration.e1PortConfigurationTable.clockSource") != None:
            dic_result["iduConfiguration.e1PortConfigurationTable.clockSource"] = html.var(
                "iduConfiguration.e1PortConfigurationTable.clockSource")
        if html.var("iduConfiguration.e1PortConfigurationTable.lineType") != None:
            dic_result["iduConfiguration.e1PortConfigurationTable.lineType"] = html.var(
                "iduConfiguration.e1PortConfigurationTable.lineType")
        if html.var("iduConfiguration.e1PortConfigurationTable.lineCode") != None:
            dic_result["iduConfiguration.e1PortConfigurationTable.lineCode"] = html.var(
                "iduConfiguration.e1PortConfigurationTable.lineCode")
        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def port_ATU_form(h):
    """

    @param h:
    """
    global html
    html = h
    port_ATU_list = []
    idu_get_database_obj = IduGetDatabase()
    port_ATU_id = html.var("portQinQId")
    port_ATU_list = idu_get_database_obj.port_ATU_get_list(port_ATU_id)
    if isinstance(port_ATU_list, list):
        html.write(IduForms.port_ATU_form(port_ATU_list))
    elif isinstance(port_ATU_list, Exception):
        html.write(str(e))


def port_vlan_add_form(h):
    """

    @param h:
    """
    global html
    html = h
    port_vlan_list = []
    idu_get_database_obj = IduGetDatabase()
    port_vlan_id = html.var("portVlanId")
    host_id = html.var("hostId")
    id_name = html.var("idName")
    class_name = html.var("className")
    selected_device = html.var("selected_device")
    addEdit = html.var("addEdit")
    vlanId = html.var("vlanId")
    # index = html.var("index")
    if int(addEdit) == 1:
        port_vlan_list = idu_get_database_obj.common_get_data_by_id(
            port_vlan_id, host_id, id_name, class_name)

    if isinstance(port_vlan_list, list):
        html.write(str(IduForms.port_vlan_form(port_vlan_list,
                                               host_id, selected_device, port_vlan_id, addEdit, vlanId)))
    elif isinstance(port_vlan_list, Exception):
        html.write(str(e))


def vlan_form_action(h):
    """

    @param h:
    """
    try:
        obj_bll_cancel_set_valid = IduCommonSetValidation()
        global html
        html = h
        host_id = html.var("host_id")
        dic_result = {"success": 0}
        result = {}
        flag = 0
        index = 0
        id = None
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

        elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var(
                "common_submit") == "":
            if html.var("vlan_id") != None:
                id = html.var("vlan_id")
            if html.var("index_id") != None:
                index = html.var("index_id")

            if html.var("addEdit") != None:
                addEdit = html.var("addEdit")
            if html.var("switch.vlanconfigTable.vlanname") != None:
                if Validation.is_required(html.var("switch.vlanconfigTable.vlanname")):
                    if obj_bll_cancel_set_valid.check_vlan_name(html.var("switch.vlanconfigTable.vlanname"),
                                                                host_id) == 0:
                        dic_result["switch.vlanconfigTable.vlanname"] = html.var(
                            "switch.vlanconfigTable.vlanname")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Vlan Name already exist.Please enter different vlan name"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Vlan Name is required"

            if html.var("switch.vlanconfigTable.vlantag") != None:
                if Validation.is_required(html.var("switch.vlanconfigTable.vlantag")):
                    if Validation.is_number(html.var("switch.vlanconfigTable.vlantag")):
                        if int(html.var("switch.vlanconfigTable.vlantag")) > 0 and int(
                                html.var("switch.vlanconfigTable.vlantag")) < 4096:
                            if obj_bll_cancel_set_valid.check_vlan_tag(html.var("switch.vlanconfigTable.vlantag"),
                                                                       host_id) == 0:
                                dic_result["switch.vlanconfigTable.vlantag"] = html.var(
                                    "switch.vlanconfigTable.vlantag")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result["result"] = "Vlan tag already exist.Please enter different vlan tag"
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result[
                                "result"] = "Vlan Tag is between 1 and 4095"
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result["result"] = "Vlan Tag is number"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Vlan Tag is required"

            dic_result[
                "switch.vlanconfigTable.memberports"] = html.var("number")

            if flag == 1:
                html.req.content_type = 'application/json'
                html.req.write(str(JSONEncoder().encode(dic_result)))
            else:
                # html.write(str(str(host_id)+str(device_type_id)+str(dic_result)+str(id)+str(index)))
                result = obj_bll_cancel_set_valid.vlan_set(
                    host_id, device_type_id, dic_result, addEdit, id, index)
                html.req.content_type = 'application/json'
                html.req.write(str(JSONEncoder().encode(result)))

                # html.req.write(str(JSONEncoder().encode(dic_result)))

        elif html.var("common_submit") == "Cancel":
            dic_result["success"] = 0
            if html.var("switch.vlanconfigTable.vlanname") != None:
                dic_result["switch.vlanconfigTable.vlanname"] = html.var(
                    "switch.vlanconfigTable.vlanname")
            if html.var("switch.vlanconfigTable.vlantag") != None:
                dic_result["switch.vlanconfigTable.vlantag"] = html.var(
                    "switch.vlanconfigTable.vlantag")
            dic_result[
                "switch.vlanconfigTable.memberports"] = html.var("number")

            result = obj_bll_cancel_set_valid.idu_cancel_form(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))
    except Exception as e:
        dic_result = {"success": 1, "result": str(e)}
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def update_vlan_port_form(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        idu_get_database_obj = IduGetDatabase()
        host_id = html.var("host_id")
        selected_device = html.var("selected_device")
        html.write(str(IduForms.table_port_Vlan(host_id, selected_device)))
    except Exception as e:
        html.write(str(e))


def device_update_reconciliation(h):
    """

    @param h:
    """
    global html
    html = h
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    bll_rec_obj = IduReconcilation()
    host_id = html.var("host_id")
    if host_id == None:
        host_id = ""
    device_type_id = html.var("device_type_id")
    if device_type_id == "":
        device_type_id = "idu4"
    table_prefix = html.var("table_prefix")
    if table_prefix == None:
        table_prefix = "idu_"
    insert_update = html.var("insert_update")
    if insert_update == None:
        insert_update = True
    result = bll_rec_obj.update_device_reconcilation_controller(
        host_id, device_type_id, table_prefix, insert_update, user_name)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def reconciliation_status_idu(h):
    """

    @param h:
    """
    global html
    html = h
    bll_rec_obj = IduReconcilation()
    result = bll_rec_obj.reconciliation_status()
    if result == None:
        result = []
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def commit_to_flash(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    bll_rec_obj = IduReconcilation()
    if host_id == "":
        result = {"success": 1, "result": "Host Not Exist"}
    device_type_id = html.var("device_type_id")
    if device_type_id == "":
        result = {"success": 1, "result": "No device Exist"}
    result = bll_rec_obj.commit_to_flash(host_id, device_type_id)
    if 53 in result["result"] or '53' in result["result"]:
        result = {"success": 1, "result": "Device Unresponsive"}
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def reboot(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    bll_rec_obj = IduReconcilation()
    if host_id == "":
        result = {"success": 1, "result": "Host Not Exist"}
    device_type_id = html.var("device_type_id")
    if device_type_id == "":
        result = {"success": 1, "result": "No device Exist"}
    result = bll_rec_obj.reboot(host_id, device_type_id)
    if int(result['flag']) == 0:
        if 53 in result["result"]:
            result["success"] = 0
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def ping_check(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    bll_rec_obj = IduReconcilation()
    if host_id == "":
        result = 2
    result = bll_rec_obj.chk_ping(host_id)
    html.write(str(result))


def temperature_form_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    temp_min = 0
    temp_max = 0
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":

        if html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMin") != None:
            if Validation.is_required(html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMin")):
                if Validation.is_number(html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMin")):
                    dic_result["iduConfiguration.temperatureSensorConfigurationTable.tempMin"] = html.var(
                        "iduConfiguration.temperatureSensorConfigurationTable.tempMin")
                    temp_min = int(html.var(
                        "iduConfiguration.temperatureSensorConfigurationTable.tempMin"))
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Lower Threshhold must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Lower Threshhold is required"

        if html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMax") != None:
            if Validation.is_required(html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMax")):
                if Validation.is_number(html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMax")):
                    temp_max = int(html.var(
                        "iduConfiguration.temperatureSensorConfigurationTable.tempMax"))
                    dic_result["iduConfiguration.temperatureSensorConfigurationTable.tempMax"] = html.var(
                        "iduConfiguration.temperatureSensorConfigurationTable.tempMax")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Upper Threshhold must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Upper Threshhold is required"

        if temp_min == temp_max:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Invalid temperature thresholds.Both thresholds should not be same"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMin") != None:
            dic_result["iduConfiguration.temperatureSensorConfigurationTable.tempMin"] = html.var(
                "iduConfiguration.temperatureSensorConfigurationTable.tempMin")
        if html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMax") != None:
            dic_result["iduConfiguration.temperatureSensorConfigurationTable.tempMax"] = html.var(
                "iduConfiguration.temperatureSensorConfigurationTable.tempMax")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def date_time_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("iduConfiguration.rtcConfigurationTable.year") != None:
            if Validation.is_required(html.var("iduConfiguration.rtcConfigurationTable.year")):
                if Validation.is_number(html.var("iduConfiguration.rtcConfigurationTable.year")):
                    dic_result["iduConfiguration.rtcConfigurationTable.year"] = html.var(
                        "iduConfiguration.rtcConfigurationTable.year")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Year must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Year is required"

        if html.var("iduConfiguration.rtcConfigurationTable.month") != None:
            if Validation.is_required(html.var("iduConfiguration.rtcConfigurationTable.month")):
                if Validation.is_number(html.var("iduConfiguration.rtcConfigurationTable.month")):
                    dic_result["iduConfiguration.rtcConfigurationTable.month"] = html.var(
                        "iduConfiguration.rtcConfigurationTable.month")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Month must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Month is required"
        if html.var("iduConfiguration.rtcConfigurationTable.day") != None:
            if Validation.is_required(html.var("iduConfiguration.rtcConfigurationTable.day")):
                if Validation.is_number(html.var("iduConfiguration.rtcConfigurationTable.day")):
                    dic_result["iduConfiguration.rtcConfigurationTable.day"] = html.var(
                        "iduConfiguration.rtcConfigurationTable.day")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Day must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Day is required"

        if html.var("iduConfiguration.rtcConfigurationTable.hour") != None:
            if Validation.is_required(html.var("iduConfiguration.rtcConfigurationTable.hour")):
                if Validation.is_number(html.var("iduConfiguration.rtcConfigurationTable.hour")):
                    dic_result["iduConfiguration.rtcConfigurationTable.hour"] = html.var(
                        "iduConfiguration.rtcConfigurationTable.hour")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Hour must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Hour is required"

        if html.var("iduConfiguration.rtcConfigurationTable.min") != None:
            if Validation.is_required(html.var("iduConfiguration.rtcConfigurationTable.min")):
                if Validation.is_number(html.var("iduConfiguration.rtcConfigurationTable.min")):
                    dic_result["iduConfiguration.rtcConfigurationTable.min"] = html.var(
                        "iduConfiguration.rtcConfigurationTable.min")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Minute must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Minute is required"

        if html.var("iduConfiguration.rtcConfigurationTable.sec") != None:
            if Validation.is_required(html.var("iduConfiguration.rtcConfigurationTable.sec")):
                if Validation.is_number(html.var("iduConfiguration.rtcConfigurationTable.sec")):
                    dic_result["iduConfiguration.rtcConfigurationTable.sec"] = html.var(
                        "iduConfiguration.rtcConfigurationTable.sec")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Seconds must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Seconds is required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMin") != None:
            dic_result["iduConfiguration.temperatureSensorConfigurationTable.tempMin"] = html.var(
                "iduConfiguration.temperatureSensorConfigurationTable.tempMin")
        if html.var("iduConfiguration.temperatureSensorConfigurationTable.tempMax") != None:
            dic_result["iduConfiguration.temperatureSensorConfigurationTable.tempMax"] = html.var(
                "iduConfiguration.temperatureSensorConfigurationTable.tempMax")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def poe_form_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if Validation.is_required(html.var("iduConfiguration.poeConfigurationTable.poeAdminStatus")):
            if html.var("iduConfiguration.poeConfigurationTable.poeAdminStatus") != None:
                dic_result["iduConfiguration.poeConfigurationTable.poeAdminStatus"] = html.var(
                    "iduConfiguration.poeConfigurationTable.poeAdminStatus")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Admin State is Required"
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Admin State is Required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("iduConfiguration.poeConfigurationTable.poeAdminStatus") != None:
            dic_result["iduConfiguration.poeConfigurationTable.poeAdminStatus"] = html.var(
                "iduConfiguration.poeConfigurationTable.poeAdminStatus")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def swt_port_config_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    id = None
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("port_config_id") != None:
            id = html.var("port_config_id")
        if html.var("index_id") != None:
            index = html.var("index_id")
        if html.var("switch.switchPortconfigTable.swadminState") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.swadminState")):
                dic_result["switch.switchPortconfigTable.swadminState"] = html.var(
                    "switch.switchPortconfigTable.swadminState")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Admin State is required"

        if html.var("switch.switchPortconfigTable.swlinkMode") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.swlinkMode")):
                dic_result["switch.switchPortconfigTable.swlinkMode"] = html.var(
                    "switch.switchPortconfigTable.swlinkMode")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Link Mode is required"

        if html.var("switch.switchPortconfigTable.portvid") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.portvid")):
                if Validation.is_number(html.var("switch.switchPortconfigTable.portvid")):
                    dic_result["switch.switchPortconfigTable.portvid"] = html.var(
                        "switch.switchPortconfigTable.portvid")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "PortVid must be number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Port Vid is required"

        if html.var("switch.switchPortconfigTable.macauthState") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.macauthState")):
                dic_result["switch.switchPortconfigTable.macauthState"] = html.var(
                    "switch.switchPortconfigTable.macauthState")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Mac Auth State is required"

        if html.var("switch.switchPortconfigTable.mirroringdirection") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.mirroringdirection")):
                dic_result["switch.switchPortconfigTable.mirroringdirection"] = html.var(
                    "switch.switchPortconfigTable.mirroringdirection")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Mirroring Direction is required"

        if html.var("switch.switchPortconfigTable.macflowcontrol") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.macflowcontrol")):
                dic_result["switch.switchPortconfigTable.macflowcontrol"] = html.var(
                    "switch.switchPortconfigTable.macflowcontrol")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Mac Flow Control is required"

        if html.var("switch.switchPortconfigTable.portdotqmode") != None:
            if Validation.is_required(html.var("switch.switchPortconfigTable.portdotqmode")):
                dic_result["switch.switchPortconfigTable.portdotqmode"] = html.var(
                    "switch.switchPortconfigTable.portdotqmode")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Dotq Mode is required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(str(host_id)+str(device_type_id)+str(dic_result)+str(id)+str(index)))
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result, id, index)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))
            # html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("switch.portBwTable.ingressbwvalue") != None:
            dic_result["switch.portBwTable.ingressbwvalue"] = html.var(
                "switch.portBwTable.ingressbwvalue")
        if html.var("switch.portBwTable.ingressbwvalue") != None:
            dic_result["switch.portBwTable.ingressbwvalue"] = html.var(
                "switch.portBwTable.ingressbwvalue")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def update_swt_port_form(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        idu_get_database_obj = IduGetDatabase()
        host_id = html.var("host_id")
        selected_device = html.var("selected_device")
        html.write(
            str(IduForms.table_port_configuration(host_id, selected_device)))
    except Exception as e:
        html.write(str(e))


def swt_bw_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    id = None
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("bw_id") != None:
            id = html.var("bw_id")
        if html.var("index_id") != None:
            index = html.var("index_id")
        if html.var("switch.portBwTable.ingressbwvalue") != None:
            if Validation.is_required(html.var("switch.portBwTable.ingressbwvalue")):
                dic_result["switch.portBwTable.ingressbwvalue"] = html.var(
                    "switch.portBwTable.ingressbwvalue")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Ingress Value is Required"

        if html.var("switch.portBwTable.egressbwvalue") != None:
            if Validation.is_required(html.var("switch.portBwTable.egressbwvalue")):
                dic_result["switch.portBwTable.egressbwvalue"] = html.var(
                    "switch.portBwTable.egressbwvalue")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Egress value is Required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(str(host_id)+str(device_type_id)+str(dic_result)+str(id)+str(index)))
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result, id, index)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))
            # html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("switch.portBwTable.ingressbwvalue") != None:
            dic_result["switch.portBwTable.ingressbwvalue"] = html.var(
                "switch.portBwTable.ingressbwvalue")
        if html.var("switch.portBwTable.ingressbwvalue") != None:
            dic_result["switch.portBwTable.ingressbwvalue"] = html.var(
                "switch.portBwTable.ingressbwvalue")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def mirror_port_form_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    special_case = 0
    id = None
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("special_case") != None:
            special_case = html.var("special_case")
        if html.var("switch.mirroringportTable.mirroringport") != None:
            if Validation.is_required(html.var("switch.mirroringportTable.mirroringport")):
                dic_result["switch.mirroringportTable.mirroringport"] = html.var(
                    "switch.mirroringportTable.mirroringport")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please select Mirroring port"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result, None, 0, special_case)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("switch.mirroringportTable.mirroringport") != None:
            dic_result["switch.mirroringportTable.mirroringport"] = html.var(
                "switch.mirroringportTable.mirroringport")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def unmp_ip_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    special_case = 0
    id = None
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("special_case") != None:
            special_case = html.var("special_case")
        if html.var("iduConfiguration.omcConfigurationTable.omcIpAddress") != None:
            if Validation.is_required(html.var("iduConfiguration.omcConfigurationTable.omcIpAddress")):
                if Validation.is_valid_ip(html.var("iduConfiguration.omcConfigurationTable.omcIpAddress")):
                    dic_result["iduConfiguration.omcConfigurationTable.omcIpAddress"] = html.var(
                        "iduConfiguration.omcConfigurationTable.omcIpAddress")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Invalid IP Address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "IP Address is required"
        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result, None, 0, special_case)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("iduConfiguration.omcConfigurationTable.omcIpAddress") != None:
            dic_result["iduConfiguration.omcConfigurationTable.omcIpAddress"] = html.var(
                "iduConfiguration.omcConfigurationTable.omcIpAddress")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def update_bw_form(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        idu_get_database_obj = IduGetDatabase()
        host_id = html.var("host_id")
        selected_device = html.var("selected_device")
        html.write(
            str(IduForms.port_bandwidth_show_table(host_id, selected_device)))
    except Exception as e:
        html.write(str(e))


def update_qinq_form(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        idu_get_database_obj = IduGetDatabase()
        host_id = html.var("host_id")
        selected_device = html.var("selected_device")
        html.write(
            str(IduForms.port_QinQ_show_table(host_id, selected_device)))
    except Exception as e:
        html.write(str(e))


def qinq_form_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    id = None
    actual_value = ""
    number = []
    total_len = 0
    actual_number = 0
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("qinq_id") != None:
            id = html.var("qinq_id")
        if html.var("index_id") != None:
            index = html.var("index_id")
        if html.var("switch.portqinqTable.portqinqstate") != None:
            if Validation.is_required(html.var("switch.portqinqTable.portqinqstate")):
                dic_result["switch.portqinqTable.portqinqstate"] = html.var(
                    "switch.portqinqTable.portqinqstate")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Port Qinq state is required"

        if html.var("switch.portqinqTable.providertag") != None:
            if Validation.is_required(html.var("switch.portqinqTable.providertag")):
                if Validation.is_number(html.var("switch.portqinqTable.providertag")):
                    actual_value = html.var("switch.portqinqTable.providertag")
                    number = list(actual_value)
                    total_len = 4 - len(number)
                    for i in range(0, total_len):
                        number.insert(0, 0)
                    actual_number = 0
                    actual_number += int(number[0]) * 4096
                    actual_number += int(number[1]) * 256
                    actual_number += int(number[2]) * 16
                    actual_number += int(number[3])
                    dic_result[
                        "switch.portqinqTable.providertag"] = actual_number

            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Provider Tag is only Number"
        else:
            flag = 1
            dic_result["success"] = 1
            dic_result["result"] = "Provider Tag is Required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(index))
            result = obj_bll_cancel_set_valid.common_validation(
                host_id, device_type_id, dic_result, id, index)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("switch.portqinqTable.portqinqstate") != None:
            dic_result["switch.portqinqTable.portqinqstate"] = html.var(
                "switch.portqinqTable.portqinqstate")
        if html.var("switch.portqinqTable.providertag") != None:
            dic_result["switch.portqinqTable.providertag"] = html.var(
                "switch.portqinqTable.providertag")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def port_link_form(h):
    """

    @param h:
    """
    global html
    html = h
    port_link_list = []
    idu_get_database_obj = IduGetDatabase()
    addEdit = html.var("addEdit")
    port_num = html.var("portnum")
    link_num = html.var("linknum")
    class_name = html.var("tablename")
    id_name = html.var("tableId")
    port_link_id = html.var("tableidvalue")
    host_id = html.var("host_id")
    selected_device = html.var("selected_device")
    # index = html.var("index")
    if int(addEdit) == 1:
        port_link_list = idu_get_database_obj.common_get_data_by_id(
            port_link_id, host_id, id_name, class_name)
    if isinstance(port_link_list, list):
        html.write(str(IduForms.port_link_form(port_link_list, host_id,
                                               selected_device, port_link_id, port_num, link_num, addEdit)))
    elif isinstance(port_link_list, Exception):
        html.write(str(e))


def link_port_delete(h):
    """

    @param h:
    """
    global html
    html = h
    obj = LinkConfiguration()
    id = html.var("portid")
    port_number = html.var("portnumber")
    link_number = html.var("bundleNumber")
    host_id = html.var("host_id")
    result = obj.delete_link_port(host_id, id, port_number, link_number)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def vlan_port_delete(h):
    """

    @param h:
    """
    global html
    html = h
    obj = IduCommonSetValidation()
    id = html.var("vlanid")
    host_id = html.var("host_id")
    result = obj.delete_vlan_port(host_id, id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def update_link_port_table(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        idu_get_database_obj = IduGetDatabase()
        host_id = html.var("host_id")
        selected_device = html.var("selected_device")
        html.write(str(IduForms.table_link_port(host_id, selected_device)))
    except Exception as e:
        html.write(str(e))


def link_form_action(h):
    """

    @param h:
    """
    obj_bll_cancel_set_valid = IduCommonSetValidation()
    obj_link = LinkConfiguration()
    global html
    html = h
    host_id = html.var("host_id")
    dic_result = {"success": 0}
    result = {}
    flag = 0
    index = 0
    id = None
    actual_value = ""
    number = []
    total_len = 0
    actual_number = 0
    device_type_id = html.var("device_type")
    port_num = ""
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

    elif html.var("common_submit") == "Save" or html.var("common_submit") == "Retry" or html.var("common_submit") == "":
        if html.var("addEdit") != None:
            addEdit = html.var("addEdit")

        if html.var("port_number") != None:
            if Validation.is_required(html.var("port_number")):
                port_num = html.var("port_number")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please select E1 Port number"

        if html.var("e1_port_num") != None:
            index = html.var("e1_port_num")

        if html.var("link_number") != None:
            id = html.var("link_number")

        if html.var("bundle_id") != None:
            if Validation.is_required(html.var("bundle_id")):
                if Validation.is_number(html.var("bundle_id")):
                    if int(html.var("bundle_id")) >= 0 and int(html.var("bundle_id")) <= 63:
                        if int(addEdit) == 0:
                            if obj_link.link_chk(host_id, int(html.var("bundle_id"))) == 0:
                                bundle_id = html.var("bundle_id")
                            else:
                                flag = 1
                                dic_result["success"] = 1
                                dic_result["result"] = "Link already exist"
                        else:
                            bundle_id = html.var("bundle_id")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Link Number must be in between 0 and 63"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Please enter number in Link Number"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Link Number is required"

        if html.var("iduConfiguration.linkConfigurationTable.dstIPAddr") != None:
            if Validation.is_required(html.var("iduConfiguration.linkConfigurationTable.dstIPAddr")):
                if Validation.is_valid_ip(html.var("iduConfiguration.linkConfigurationTable.dstIPAddr")):
                    dic_result["iduConfiguration.linkConfigurationTable.dstIPAddr"] = html.var(
                        "iduConfiguration.linkConfigurationTable.dstIPAddr")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Please enter valid ip address"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Ip Address is required"

        if html.var("iduConfiguration.linkConfigurationTable.srcBundleID") != None:
            if Validation.is_required(html.var("iduConfiguration.linkConfigurationTable.srcBundleID")):
                if Validation.is_number(html.var("iduConfiguration.linkConfigurationTable.srcBundleID")):
                    if int(html.var("iduConfiguration.linkConfigurationTable.srcBundleID")) >= 0 and int(
                            html.var("iduConfiguration.linkConfigurationTable.srcBundleID")) <= 63:
                        if obj_link.src_bundle_chk(host_id,
                                                   int(html.var("iduConfiguration.linkConfigurationTable.srcBundleID")),
                                                   html.var("bundle_id") if int(addEdit) == 0 else id,
                                                   port_num if int(addEdit) == 0 else index) == 0:
                            dic_result["iduConfiguration.linkConfigurationTable.srcBundleID"] = html.var(
                                "iduConfiguration.linkConfigurationTable.srcBundleID")
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result["result"] = "Source Bundle is busy"

                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Source Link Id must be in between 0 and 63"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter number in Source Link Id"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Source Link Id is required"

        if html.var("iduConfiguration.linkConfigurationTable.dstBundleID") != None:
            if Validation.is_required(html.var("iduConfiguration.linkConfigurationTable.dstBundleID")):
                if Validation.is_number(html.var("iduConfiguration.linkConfigurationTable.dstBundleID")):
                    if int(html.var("iduConfiguration.linkConfigurationTable.dstBundleID")) >= 0 and int(
                            html.var("iduConfiguration.linkConfigurationTable.dstBundleID")) <= 63:
                        if obj_link.destination_bundle_chk(host_id, int(
                                html.var("iduConfiguration.linkConfigurationTable.dstBundleID")),
                                                           html.var("bundle_id") if int(addEdit) == 0 else id,
                                                           port_num if int(addEdit) == 0 else index) == 0:
                            dic_result["iduConfiguration.linkConfigurationTable.dstBundleID"] = html.var(
                                "iduConfiguration.linkConfigurationTable.dstBundleID")
                        else:
                            flag = 1
                            dic_result["success"] = 1
                            dic_result["result"] = "Destination Bundle is busy"
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Destination Link Id must be in between 0 and 63"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter number in Destination Link Id"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Destination Link Id is required"

        if html.var("iduConfiguration_linkConfigurationTable_tsaAssign") != None:
            if Validation.is_required(html.var("iduConfiguration_linkConfigurationTable_tsaAssign")):
                timeslot = ""
                timeslot_str = html.var(
                    "iduConfiguration_linkConfigurationTable_tsaAssign")
                timeslot_list = timeslot_str.split(",")
                for i in range(0, 32):
                    if str(i) in timeslot_list:
                        timeslot += "1"
                    else:
                        timeslot += "0"
                dic_result[
                    "iduConfiguration_linkConfigurationTable_tsaAssign"] = timeslot
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Please select Timeslot"

        if html.var("iduConfiguration.linkConfigurationTable.bundleSize") != None:
            if Validation.is_required(html.var("iduConfiguration.linkConfigurationTable.bundleSize")):
                if Validation.is_number(html.var("iduConfiguration.linkConfigurationTable.bundleSize")):
                    if int(html.var("iduConfiguration.linkConfigurationTable.bundleSize")) >= 1 and int(
                            html.var("iduConfiguration.linkConfigurationTable.bundleSize")) <= 99:
                        dic_result["iduConfiguration.linkConfigurationTable.bundleSize"] = html.var(
                            "iduConfiguration.linkConfigurationTable.bundleSize")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Payload must be in between 1 and 99"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter number in Payload size"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Payload size is required"

        if html.var("iduConfiguration.linkConfigurationTable.bufferSize") != None:
            if Validation.is_required(html.var("iduConfiguration.linkConfigurationTable.bufferSize")):
                if Validation.is_number(html.var("iduConfiguration.linkConfigurationTable.bufferSize")):
                    if int(html.var("iduConfiguration.linkConfigurationTable.bufferSize")) >= 1000 and int(
                            html.var("iduConfiguration.linkConfigurationTable.bufferSize")) <= 25000:
                        dic_result["iduConfiguration.linkConfigurationTable.bufferSize"] = html.var(
                            "iduConfiguration.linkConfigurationTable.bufferSize")
                    else:
                        flag = 1
                        dic_result["success"] = 1
                        dic_result[
                            "result"] = "Jitter buffer must be in between 1000 and 25000"
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Please enter number in Jitter buffer"
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Jitter Buffer is required"
        if html.var("iduConfiguration_linkConfigurationTable_clockRecovery") != None:
            if Validation.is_required(html.var("iduConfiguration_linkConfigurationTable_clockRecovery")):
                dic_result["iduConfiguration_linkConfigurationTable_clockRecovery"] = html.var(
                    "iduConfiguration_linkConfigurationTable_clockRecovery")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Clock Recovery is required"

        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(id+">>>"+index+">>>>"+">>>>"+addEdit+">>>>"+port_num+">>>>"+bundle_id))
            # html.write(str(dic_result))
            # html.write(str(bundle_id))
            # html.write(str(port_num))
            result = obj_bll_cancel_set_valid.set_link_port(host_id, device_type_id, dic_result, bundle_id if int(
                addEdit) == 0 else id, port_num if int(addEdit) == 0 else index, int(addEdit))
            # html.write(str(result))
            # time.sleep(30)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("common_submit") == "Cancel":
        dic_result["success"] = 0
        if html.var("switch.portqinqTable.portqinqstate") != None:
            dic_result["switch.portqinqTable.portqinqstate"] = html.var(
                "switch.portqinqTable.portqinqstate")
        if html.var("switch.portqinqTable.providertag") != None:
            dic_result["switch.portqinqTable.providertag"] = html.var(
                "switch.portqinqTable.providertag")

        result = obj_bll_cancel_set_valid.idu_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def get_selected_timeslot(h):
    """

    @param h:
    """
    global html
    html = h
    link_obj = LinkConfiguration()
    if html.var("host_id") != "" or html.var("host_id") != None:
        host_id = html.var("host_id")
    if html.var("portNum") != None:
        port_num = html.var("portNum")
    else:
        port_num = ""
    result = link_obj.selected_timeslot(host_id, port_num)
    select_list_html = ""
    pos = [0]
    if len(result) > 0:
        for k in range(0, len(result)):
            if int(result[k]) == 1:
                pos.append(k)
        for row in range(0, 32):
            if row == 0:
                select_list_html += "<option value=\"%s\" disabled=\"disabled\"> %s </option>" % (
                    row, row)
            else:
                if len(pos) > 0:
                    if row in pos:
                        select_list_html += "<option value=\"%s\" disabled=\"disabled\"> %s </option>" % (
                            row, row)
                    else:
                        select_list_html += "<option value=\"%s\"> %s </option>" % (
                            row, row)
                else:
                    select_list_html += "<option value=\"%s\"> %s </option>" % (
                        row, row)
    else:
        for row in range(0, 32):
            if row == 0:
                select_list_html += "<option value=\"%s\" disabled=\"disabled\"> %s </option>" % (
                    row, row)
            else:
                select_list_html += "<option value=\"%s\"> %s </option>" % (
                    row, row)

    html.write(str(select_list_html))


class IduStatus(object):
    """
    Device IDU related status class
    """
    def idu_hw_sw_temperature_status(self, host_id, device_type):
        """

        @param host_id:
        @param device_type:
        @return:
        """
        hw_sw_temperature_dic = {'success': 0, 'result': {}}
        try:
            obj_idu_get_data = IduGetData()
            sw_status_list = obj_idu_get_data.common_get_data_by_host(
                'IduSwStatusTable', host_id)
            hw_temperature_list = obj_idu_get_data.common_get_data_by_host(
                'IduIduInfoTable', host_id)
            temp_dic = {}

            temp_dic.update(
                {'active_version': sw_status_list[0].activeVersion if len(sw_status_list) > 0 else "-",
                 'hw_serial_number': hw_temperature_list[0].hwSerialNumber if len(hw_temperature_list) > 0 else "-",
                 'temperature': str(hw_temperature_list[0].currentTemperature) if len(
                     hw_temperature_list) > 0 else "-"})
            hw_sw_temperature_dic['result'] = temp_dic
        except Exception, e:
            hw_sw_temperature_dic['success'] = 1
            hw_sw_temperature_dic['result'] = str(e)
        finally:
            sqlalche_obj.sql_alchemy_db_connection_close()
            return hw_sw_temperature_dic


def idu_listing_status(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj = IduStatus()
    result_dic = obj.idu_hw_sw_temperature_status(host_id, device_type)
    html_str = ""
    html_str += "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    html_str += "<th>S/W Version</th><th>H/W Serial Number</th><th>Temperature</th>"
    #{'result': {'hw_serial_number': 'IDU21FE10270048', 'active_version': '-', 'temperature': '42'}, 'success': 0}

    if int(result_dic['success']) == 0:
        html_str += "<tr>"
        html_str += "<td>%s</td><td>%s</td><td>%s</td>" % (
        "-" if result_dic['result']['active_version'] == None else result_dic['result']['active_version'],
        "-" if result_dic['result'][
                   'hw_serial_number'] == None else result_dic['result']['hw_serial_number'],
        "-" if result_dic['result']['temperature'] == None else result_dic['result']['temperature'])

        html_str += "</tr>"
    else:
        html_str += "<tr>"
        html_str += "<td colspan=\"3\">No Data Available</td>"
        html_str += "</tr>"
    html_str += "</table>"
    html.write(str(html_str))


def e1_admin_state_show(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_idu_get_data = IduGetData()
    e1_port_list = obj_idu_get_data.common_get_data(
        'IduE1PortConfigurationTable', host_id)
    html_str = "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    html_str += "<th>E1 Port Number</th>"
    html_str += "<th>Admin State</th>"

    if len(e1_port_list) > 0:
        for i in range(0, len(e1_port_list)):
            html_str += "<tr><td>%s</td>" % (e1_port_list[i].portNumber)
            html_str += "<td><img src=\"%s\" class=\"n-reconcile\" title=\"%s Port Admin State\" id=\"admin_state_%s\" name=\"admin_state_%s\" style=\"width:10px;height:10px;\" state=\"%s\" onClick=\"idu_admin_state_change(event,this,'%s','%s','%s','iduConfiguration.e1PortConfigurationTable.adminState',0);\"/></td></tr>" \
                        % (
                "images/temp/green_dot.png" if int(
                    e1_port_list[i].adminState) == 1 else "images/temp/red_dot.png",
                "E" + str(e1_port_list[i].portNumber),
                e1_port_list[i].portNumber, e1_port_list[i].portNumber,
                1 if int(e1_port_list[i].adminState) == 1 else 0,
                host_id, e1_port_list[i].idu_e1PortConfigurationTable_id, e1_port_list[i].portNumber)
        html_str += "<tr><td><input type=\"radio\" class=\"n-reconcile\" title=\"Lock All Admin State\" id=\"lock_all\" name=\"unlock_lock_all\" onClick=\"lock_unlock_admin(event,this,'%s','iduConfiguration.e1PortConfigurationTable.adminState',0);\"/>Lock All</td>\
        <td><input type=\"radio\" id=\"unlock_all\" class=\"n-reconcile\" title=\"UnLock All Admin State\" name=\"unlock_lock_all\" onClick=\"lock_unlock_admin(event,this,'%s','iduConfiguration.e1PortConfigurationTable.adminState',1);\"/>Unlock All</td></tr>" % (
        host_id, host_id)
    else:
        html_str += "<tr><td colspan=2>No E1 Port Exist</td></tr>"
    html_str += "</table>"
    html.write(html_str)


def link_admin_state_show(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_idu_get_data = IduGetData()
    link_port_list = obj_idu_get_data.common_get_data(
        'IduLinkConfigurationTable', host_id)
    html_str = "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    html_str += "<!--<th></th>-->"
    html_str += "<th colspan=2>Link Admin State</th>"
    if len(link_port_list) > 0:
        for i in range(0, len(link_port_list)):
            html_str += "<tr><!--<td>%s</td>-->" % (
                link_port_list[i].portNumber)
            html_str += "<td colspan=2><ul class=\"button_group\" style=\"width:40px;\"><li><a class=\"%s n-reconcile\" title=\"Link %s\" id=\"admin_state_%s\" name=\"admin_state_%s\" state=\"%s\" bundle_num=\"%s\" onClick=\"idu_admin_state_change(event,this,'%s','%s','%s','iduConfiguration.linkConfigurationTable.adminStatus',1);\">L %s</a></li></td></tr>" \
                        % (
                "green" if int(
                    link_port_list[i].adminStatus) == 1 else "red",
                str(link_port_list[i].portNumber) + " Unlocked" if int(link_port_list[i]
                .adminStatus) == 1 else str(
                    link_port_list[i].portNumber) + " Locked",
                link_port_list[i].portNumber, link_port_list[i].portNumber,
                1 if int(link_port_list[i].adminStatus) == 1 else 0,
                link_port_list[i].bundleNumber,
                host_id, link_port_list[i].idu_linkConfigurationTable_id, link_port_list[i].portNumber,
                link_port_list[i].portNumber)
        html_str += "<tr><td><input type=\"radio\" class=\"n-reconcile\" title=\"Lock All Link State\" id=\"link_lock_all\" name=\"link_unlock_lock_all\" onClick=\"link_lock_unlock_admin(event,this,'%s','iduConfiguration.linkConfigurationTable.adminStatus',0);\"/>Lock All</td>\
        <td><input type=\"radio\" class=\"n-reconcile\" title=\"Unlock All Link State\" id=\"link_unlock_all\" name=\"link_unlock_lock_all\" onClick=\"link_lock_unlock_admin(event,this,'%s','iduConfiguration.linkConfigurationTable.adminStatus',1);\"/>Unlock All</td></tr>" % (
        host_id, host_id)
    else:
        html_str += "<tr><td colspan=2>No Link Exist</td></tr>"
    html_str += "</table>"
    html.write(html_str)


def main_admin_state_show(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj_idu_get_data = IduGetData()
    main_admin_list = obj_idu_get_data.common_get_data(
        'IduIduAdminStateTable', host_id)
    html_str = "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1px\">"
    html_str += "<th>System Admin State</th>"
    if len(main_admin_list) > 0:
        for i in range(0, len(main_admin_list)):
            html_str += "<td><img src=\"%s\" class=\"n-reconcile\" title=\"System Admin State\" id=\"main_admin\" name=\"main_admin\" style=\"width:10px;height:10px;\" state=\"%s\" onClick=\"main_admin_state_change(event,this,'%s','iduinfo.iduAdminStateTable.adminstate');\"/></td></tr>" \
                        % (
                "images/temp/green_dot.png" if int(
                    main_admin_list[
                        i].adminstate) == 1 else "images/temp/red_dot.png",
                1 if int(main_admin_list[i].adminstate) == 1 else 0,
                host_id)
    else:
        html_str += "<tr><td colspan=2>No Data Available</td></tr>"
    html_str += "</table>"
    html.write(html_str)


def e1_admin_parameters(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    primary_id = html.var("primary_id")
    port_num = html.var("port_num")
    admin_state_name = html.var("admin_state_name")
    state = html.var("state")
    obj = IduAdminStateChange()
    result_dic = obj.e1_port_admin_change(
        host_id, int(primary_id), int(port_num), admin_state_name, int(state))
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def link_admin_parameters(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    primary_id = html.var("primary_id")
    port_num = html.var("port_num")
    bundle_num = html.var("bundle_num")
    admin_state_name = html.var("admin_state_name")
    state = html.var("state")
    obj = IduAdminStateChange()
    result_dic = obj.link_port_admin_change(host_id, int(primary_id), int(
        port_num), int(bundle_num), admin_state_name, int(state))
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def main_admin_parameters(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    admin_state_name = html.var("admin_state_name")
    state = html.var("state")
    obj = IduAdminStateChange()
    result_dic = obj.main_admin_change(host_id, admin_state_name, int(state))
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def all_locked_unlocked(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    admin_state_name = html.var("admin_state_name")
    state = html.var("state")
    obj_idu_get_data = IduGetData()
    e1_port_list = obj_idu_get_data.common_get_data(
        'IduE1PortConfigurationTable', host_id)
    port_str = ""
    primary_ids = ""
    if len(e1_port_list) > 0:
        for i in range(0, len(e1_port_list)):
            if i == len(e1_port_list) - 1:
                port_str += str(e1_port_list[i].portNumber)
                primary_ids += str(
                    e1_port_list[i].idu_e1PortConfigurationTable_id)
            else:
                port_str += str(e1_port_list[i].portNumber) + ","
                primary_ids += str(
                    e1_port_list[i].idu_e1PortConfigurationTable_id) + ","
    obj = IduAdminStateChange()
    result_dic = obj.locked_unlocked_all(
        host_id, port_str, primary_ids, admin_state_name, state)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def link_all_locked_unlocked(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    admin_state_name = html.var("admin_state_name")
    state = html.var("state")
    obj_idu_get_data = IduGetData()
    link_port_list = obj_idu_get_data.common_get_data(
        'IduLinkConfigurationTable', host_id)
    port_str = ""
    primary_ids = ""
    bundle_num = ""
    if len(link_port_list) > 0:
        for i in range(0, len(link_port_list)):
            if i == len(link_port_list) - 1:
                port_str += str(link_port_list[i].portNumber)
                primary_ids += str(
                    link_port_list[i].idu_linkConfigurationTable_id)
                bundle_num += str(link_port_list[i].bundleNumber)
            else:
                port_str += str(link_port_list[i].portNumber) + ","
                primary_ids += str(
                    link_port_list[i].idu_linkConfigurationTable_id) + ","
                bundle_num += str(link_port_list[i].bundleNumber) + ","
    obj = IduAdminStateChange()
    result_dic = obj.link_locked_unlocked_all(
        host_id, port_str, primary_ids, bundle_num, admin_state_name, state)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def link_status_count(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj = IduLinkCount()
    result = obj.link_count(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def global_admin_request(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj = IduLinkCount()
    result = obj.global_admin_change(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def global_admin(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj = IduLinkCount()
    result = obj.global_admin_request(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))

# obj = IduStatus()
# print obj.idu_hw_sw_temperature_status(60,'idu4')


def idu_form_reconcile(h):
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
    result = eval("IduForms.%s(%s,'%s')" % (formname, host_id, device_type))
    html.write(str(result))
