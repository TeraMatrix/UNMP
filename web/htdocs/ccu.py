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
from ccu_view import CCUProfiling
from ccu_profiling_bll import CCUDeviceList, CcuCommonSetValidation, CCUReconcilation
from idu_profiling_bll import *
from json import JSONEncoder
from utility import Validation
from time import sleep
from datetime import datetime

ccu_bll_obj = CcuCommonSetValidation()


def ccu_listing(h):
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
        css_list = ["css/custom.css", "css/demo_table_jui.css",
                    "css/jquery-ui-1.8.4.custom.css", 'css/ccpl_jquery_combobox.css']
        javascript_list = ["js/lib/main/jquery.dataTables.min.js",
                           'js/unmp/main/ccpl_jquery_autocomplete.js', "js/unmp/main/ccu_listing.js"]

        # This we import the javascript
        ip_address = ""
        mac_address = ""

        # this is used for storing DeviceTypeList e.g "UBR,odu100"
        device_type = ""

        # this is used for storing DeviceListState e.g "enabled
        device_list_state = ""

        # this is used for storing SelectedDeviceType e.g. "UBR"
        selected_device_type = "ccu"

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
        html.new_header(
            "CCU Listing", "ccu_listing.py", "", css_list, javascript_list)

        # Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write
        # we pass parameters
        # ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
        html.write(str(page_header_search(ip_address, mac_address,
                                          "RM18,RM,Access Point,IDU,CCU", selected_device_type, "enabled",
                                          "device_type")))

        # Here we make a div to show the result in datatable
        html.write(CCUProfiling.ccu_listing())
        html.new_footer()
    except Exception as e:
        html.write(str(e))


def ccu_profiling(h):
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
        'js/unmp/main/ccu_controller.js', 'js/lib/main/jquery-ui-personalized-1.6rc2.min.js']
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
                "", "", "RM18,RM,Access Point,IDU,CCU", None, "enabled", "device_type"))
            # call the function of common_controller , it is used
            # for listing the Devices based on
            # IPaddress,Macaddress,DeviceTy
        else:
            html.new_header("%s %s Configuration" % ("CCU", device_list_parameter[0]
            .ip_address), "ccu_listing.py", "", css_list, jss_list, snapin_list)
            html.write(page_header_search(device_list_parameter[0][0], device_list_parameter[0][
                1], "RM18,RM,Access Point,IDU,CCU", device_type, device_list_state, "device_type"))
            html.write(CCUProfiling.ccu_div(device_list_parameter[0][0],
                                            device_list_parameter[0][1], host_id))
    elif isinstance(device_list_parameter, Exception):
        html.write("DataBase Error Occured")
    html.new_footer()


def ccu_device_listing_table(h):
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
    ccu_device_list_bll_obj = CCUDeviceList()
    obj_get_data = IduGetData()
    obj_link_count = IduLinkCount()
    result_device_list = []
    device_list = []
    device_dict = {}
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
        selected_device = "ccu"
    else:
        selected_device = html.var("device_type")
        # call the function get_odu_list of odu-controller which return us the
    # list of devices in two dimensional list according to
    # IPAddress,MACaddress,SelectedDevice
    if html.req.session["role"] == "admin" or html.req.session["role"] == "user" or True:
        device_dict = ccu_device_list_bll_obj.ccu_device_list(
            ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0,
            iSortCol_0, userid, html_req)
        device_list = device_dict["aaData"]
        index = int(device_dict["i_display_start"])
        # display the result on page
    # This is a empty list variable used for storing the device list
    if isinstance(device_list, list):
        # html.write(str(device_list))
        for i in range(0, len(device_list)):
        # html.write(str(i))
        # monitoring_status = "<a target=\"main\" <!--
        # href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"--><img
        # src=\"images/new/info1.png\" style=\"width:16px;height:16px;\"
        # title=\"Current Device Status\" class=\"imgbutton n-reconcile
        # w-reconcile\"/></a>"%('sp_status_profiling.py',\device_list[i][0],device_list[i][5],device_list_state)

            monitoring_status = ""

            ccu_real_data = obj_get_data.common_get_data_by_host(
                'CcuRealTimeStatusTable', device_list[i][0])
            if i == len(device_list) - 1:
                device_status_host_id += str(device_list[i][0])
            else:
                device_status_host_id += str(device_list[i][0]) + ","

            if device_list[i][6] <= 35:
                images = 'images/new/r-red.png'
            elif device_list[i][6] <= 90:
                images = 'images/new/r-black.png'
            else:
                images = 'images/new/r-green.png'

            if html.req.session["role"] == "admin" or html.req.session["role"] == "user":
                result_device_list.append(
                    [str(
                        device_list[i][1]), str(
                        device_list[i][2]), str(
                        device_list[i][3]), str(device_list[i][4]),
                     str(ccu_real_data[0].ccuRTSSystemVoltage if len(
                         ccu_real_data) > 0 and str(
                         ccu_real_data[
                             0].ccuRTSSystemVoltage) != '1111111' else "Device Unreachable"),
                     str(ccu_real_data[0].ccuRTSSolarCurrent if len(
                         ccu_real_data) > 0 and str(
                         ccu_real_data[
                             0].ccuRTSSolarCurrent) != '1111111' else "Device Unreachable"),
                     str(ccu_real_data[0].ccuRTSInternalTemperature if len(
                         ccu_real_data) > 0 and str(
                         ccu_real_data[
                             0].ccuRTSInternalTemperature) != '1111111' else "Device Unreachable"),
                     "<a target=\"main\" href=\"ccu_profiling.py?host_id=%s&device_type=%s&device_list_state=%s\">\
                <img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\">\
                <img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\">\
                <img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton n-reconcile\"/></a>&nbsp;&nbsp;\
                %s&nbsp;&nbsp;<img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" onclick=\"ccuReconcile(this,'%s','%s');\" state_rec=\"0\"/>\
                %s"
                     % (
                         device_list[i][
                             0], device_list[
                             i][
                             5], device_list_state, device_list[i][0],
                         'sp_dashboard_profiling.py' if device_list[
                                                            i][
                                                            5] == "ccu" else 'sp_dashboard_profiling.py',
                         device_list[i][0], device_list[i][5], device_list_state, device_list[
                             i][
                             3], monitoring_status, images, device_list[
                             i][
                             6], device_list[
                             i][0], device_list[i][5],
                         "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (
                         device_status_host_id) if i == len(device_list) - 1 else "")])
            else:
            # monitoring_status = "<a target=\"main\" <!--
            # href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\"--><img
            # src=\"images/new/info1.png\" style=\"width:16px;height:16px;\"
            # title=\"Current Device Status\" class=\"imgbutton n-reconcile
            # w-reconcile\"/></a>"%('sp_status_profiling.py',device_list[i][0],device_list[i][5],device_list_state)
                monitoring_status = ""

                result_device_list.append(
                    [str(
                        device_list[i][1]), str(
                        device_list[i][2]), str(
                        device_list[i][3]), str(device_list[i][4]),
                     str(ccu_real_data[0].ccuRTSSystemVoltage if len(
                         ccu_real_data) > 0 else "-"),
                     str(ccu_real_data[0].ccuRTSSolarCurrent if len(
                         ccu_real_data) > 0 else "-"),
                     str(ccu_real_data[0]
                     .ccuRTSInternalTemperature if len(
                         ccu_real_data) > 0 else "-"),
                     "<a target=\"main\" href=\"#\">\
                <a><img id=\"%s\" src=\"images/new/edit.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\" n-reconcile\"/></a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"%s?host_id=%s&device_type=%s&device_list_state=%s\">\
                <img src=\"images/new/graph.png\" style=\"width:16px;height:16px;\" title=\"Performance Monitoring\" class=\"imgbutton imgEditodu16 n-reconcile\"/>\
                </a>&nbsp;&nbsp;\
                <a target=\"main\" href=\"status_snmptt.py?ip_address=%s-\">\
                <img src=\"images/new/alert.png\" style=\"width:16px;height:16px;\" title=\"Device Alarms\" class=\"imgbutton imgEditodu16 n-reconcile\"/>\
                </a>&nbsp;&nbsp;\
                %s<img src=\"%s\" title=\"Reconciliation %s%% Done\" style=\"width:16px;height:16px;\" class=\"imgbutton n-reconcile imgEditodu16\" \
                state_rec=\"0\"/>%s" % (device_list[i][0],
                                        'sp_dashboard_profiling.py' if device_list[
                                                                           i][
                                                                           5] == "ccu" else 'sp_dashboard_profiling.py',
                                        device_list[i][0], device_list[i][
                         5], device_list_state, device_list[
                                            i][
                                            3], monitoring_status, images, device_list[i][6],
                                        "<input type=\"hidden\" value=\"%s\" name=\"host_id\" id=\"host_id\" />" % (
                                        device_status_host_id) if i == len(device_list) - 1 else "")])
        html.req.content_type = 'application/json'
        device_dict["aaData"] = result_device_list
        html.req.write(str(JSONEncoder().encode(device_dict)))


def get_device_list_ccu_profiling(h):
    """

    @param h:
    """
    try:
        global html
        html = h
        ccu_device_list_bll_obj = CCUDeviceList()
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

        device_list = ccu_device_list_bll_obj.ccu_device_list_profiling(
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
            device_list_parameter = ccu_device_list_bll_obj.get_device_parameter(
                result)  # call the idu_profiling_controller function get_device_param returns the list.List Contains ipaddress,macaddress,devicetypeid,config_profile_id
            # html.write(str(device_list_parameter))
            html.write(CCUProfiling.ccu_profile_call(
                result, selected_device, device_list_parameter))
    except Exception as e:
        html.write(str(e[-1]))


def battery_panel_action(h):
    """

    @param h:
    """
    global html, ccu_bll_obj
    html = h
    count = 0
    dic_result = {"success": 0}
    result = {}
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = CcuCommonSetValidation()
    if html.var("host_id") == "" or html.var("host_id") == None or html.var("host_id") == 'undefined':
        dic_result["success"] = 1
        dic_result["result"] = "Host Not Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None or html.var("device_type") == 'undefined':
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Missed"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ccu_common_submit") == "Save" or html.var("ccu_common_submit") == "Retry" or html.var(
            "ccu_common_submit") == "":
        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity") != None:
            if Validation.is_required(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity")):
                if Validation.is_number(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity")):
                    dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity"] = html.var(
                        "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Battery capacity field must be interger."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Battery capacity field is required."

        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP") != None:
            if Validation.is_required(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP")):
                if Validation.is_number(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP")):
                    dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP"] = html.var(
                        "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Solar Panel field must be integer."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Solar Panel field is required."

        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount") != None:
            if Validation.is_required(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount")):
                if Validation.is_number(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount")):
                    dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount"] = html.var(
                        "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Solar panel count must be integer."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Solar panel count field is required."

        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate") != None:
            if Validation.is_required(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate")):
                if Validation.is_string(html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate")):
                    dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate"] = html.var(
                        "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Please fill the correct date."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Date field is required."
        if flag == 1:
            if count > 1:
                dic_result["result"] = "All fields are required."
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            result = ccu_bll_obj.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ccu_common_submit") == "Cancel":
        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity") != None:
            dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity"] = html.var(
                "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteBatteryCapacity")
        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP") != None:
            dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP"] = html.var(
                "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelwP")
        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount") != None:
            dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount"] = html.var(
                "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCSiteSolarPanelCount")
        if html.var("ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate") != None:
            dic_result["ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate"] = html.var(
                "ccuOAM.ccuBatteryPanelConfigTable.ccuBPCNewBatteryInstallationDate")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def alarm_threshold_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    count = 0
    flag = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = CcuCommonSetValidation()
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

    elif html.var("ccu_common_submit") == "Save" or html.var("ccu_common_submit") == "Retry" or html.var(
            "ccu_common_submit") == "":
        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm")):
                if Validation.is_number(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm")):
                    dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm"] = html.var(
                        "ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Temperature alarm field must be interger."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Temperature alarm field is required."

        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest")):
                if Validation.is_number(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest")):
                    dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest"] = html.var(
                        "ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "PSM request field must be integer."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "PSM request field is required."

        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit")):
                if Validation.is_number(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit")):
                    dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit"] = html.var(
                        "ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "SMPS Max current field must be integer."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "SMPS Max current field is required."

        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent")):
                if Validation.is_string(html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent")):
                    dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent"] = html.var(
                        "ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Peak load current field must be integer."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Peak load current field is required."
        if flag == 1:
            if count > 1:
                dic_result["result"] = "All fields are required."
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ccu_common_submit") == "Cancel":
        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm") != None:
            dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm"] = html.var(
                "ccuOAM.ccuAlarmAndThresholdTable.ccuATHighTemperatureAlarm")
        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest") != None:
            dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest"] = html.var(
                "ccuOAM.ccuAlarmAndThresholdTable.ccuATPSMRequest")
        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit") != None:
            dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit"] = html.var(
                "ccuOAM.ccuAlarmAndThresholdTable.ccuATSMPSMaxCurrentLimit")
        if html.var("ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent") != None:
            dic_result["ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent"] = html.var(
                "ccuOAM.ccuAlarmAndThresholdTable.ccuATPeakLoadCurrent")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def peer_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    flag = 0
    count = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = CcuCommonSetValidation()
    if html.var("host_id") == "" or html.var("host_id") == None:
        dic_result["success"] = 1
        dic_result["result"] = "No Such Host Exist"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))
    elif html.var("device_type") == "" or html.var("device_type") == None:
        dic_result["success"] = 1
        dic_result["result"] = "Device Type Not Found"
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))

    elif html.var("ccu_common_submit") == "Save" or html.var("ccu_common_submit") == "Retry" or html.var(
            "ccu_common_submit") == "":
        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID") != None:
            if Validation.is_required(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID")):
                if Validation.is_valid_mac(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID")):
                    dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID"] = html.var(
                        "ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Peer 1 MAC is incorrect."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Peer 1 MAC field is required."

        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID") != None:
            if Validation.is_required(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID")):
                if Validation.is_valid_mac(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID")):
                    dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID"] = html.var(
                        "ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Peer 2 MAC is incorrect."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Peer 2 MAC field is required."

        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID") != None:
            if Validation.is_required(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID")):
                if Validation.is_valid_mac(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID")):
                    dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID"] = html.var(
                        "ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Peer 3 MAC is incorrect."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Peer 3 MAC field is required."

        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID") != None:
            if Validation.is_required(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID")):
                if Validation.is_valid_mac(html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID")):
                    dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID"] = html.var(
                        "ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result["result"] = "Peer 4 MAC is incorrect."
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "Peer 4 MAC field is required."
        if flag == 1:
            if count > 1:
                dic_result["result"] = "All fields are required."
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ccu_common_submit") == "Cancel":
        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID") != None:
            dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID"] = html.var(
                "ccuOAM.ccuPeerInformationTable.ccuPIPeer1MACID")
        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID") != None:
            dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID"] = html.var(
                "ccuOAM.ccuPeerInformationTable.ccuPIPeer2MACID")
        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID") != None:
            dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID"] = html.var(
                "ccuOAM.ccuPeerInformationTable.ccuPIPeer3MACID")
        if html.var("ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID") != None:
            dic_result["ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID"] = html.var(
                "ccuOAM.ccuPeerInformationTable.ccuPIPeer4MACID")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ccu_ip_action(h):
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
    obj_bll_set_valid = CcuCommonSetValidation()
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

    elif html.var("ccu_common_submit") == "Save" or html.var("ccu_common_submit") == "Retry" or html.var(
            "ccu_common_submit") == "":
        if html.var("ccuOAM.ccuSiteInformationTable.ccuSITSiteName") != None:
            if Validation.is_required(html.var("ccuOAM.ccuSiteInformationTable.ccuSITSiteName")):
                if Validation.is_string(html.var("ccuOAM.ccuSiteInformationTable.ccuSITSiteName")):
                    dic_result["ccuOAM.ccuSiteInformationTable.ccuSITSiteName"] = html.var(
                        "ccuOAM.ccuSiteInformationTable.ccuSITSiteName")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Site name field must be String Type."
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Site name field is required."
        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ccu_common_submit") == "Cancel":
        if html.var("ccuOAM.ccuSiteInformationTable.ccuSITSiteName") != None:
            dic_result["ccuOAM.ccuSiteInformationTable.ccuSITSiteName"] = html.var(
                "ccuOAM.ccuSiteInformationTable.ccuSITSiteName")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def aux_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {"success": 0}
    result = {}
    flag = 0
    count = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    obj_bll_set_valid = CcuCommonSetValidation()
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

    elif html.var("ccu_common_submit") == "Save" or html.var("ccu_common_submit") == "Retry" or html.var(
            "ccu_common_submit") == "":
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1")):
                dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1"] = html.var(
                    "ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1")
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "External output 1 field is required."

        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2")):
                dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2"] = html.var(
                    "ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2")
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "External output 2 field is required."

        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3")):
                dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3"] = html.var(
                    "ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3")
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "External output 3 field is required."

        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput1AlarmType") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput1AlarmType")):
                dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalInput1AlarmType"] = html.var(
                    "ccuOAM.ccuAuxIOTable.ccuAIExternalInput1AlarmType")
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "External input 1 field is required."
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput2AlarmType") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput2AlarmType")):
                dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalInput2AlarmType"] = html.var(
                    "ccuOAM.ccuAuxIOTable.ccuAIExternalInput2AlarmType")
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "External input 2 field is required."
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput3AlarmType") != None:
            if Validation.is_required(html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput3AlarmType")):
                dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalInput3AlarmType"] = html.var(
                    "ccuOAM.ccuAuxIOTable.ccuAIExternalInput3AlarmType")
            else:
                flag = 1
                count += 1
                dic_result["success"] = 1
                dic_result["result"] = "External input 3 field is required."

        if flag == 1:
            if count > 1:
                dic_result["result"] = "All fields are required."
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ccu_common_submit") == "Cancel":
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1") != None:
            dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1"] = html.var(
                "ccuOAM.ccuAuxIOTable.ccuAIExternalOutput1")
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2") != None:
            dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2"] = html.var(
                "ccuOAM.ccuAuxIOTable.ccuAIExternalOutput2")
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3") != None:
            dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3"] = html.var(
                "ccuOAM.ccuAuxIOTable.ccuAIExternalOutput3")
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput1") != None:
            dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalInput1"] = html.var(
                "ccuOAM.ccuAuxIOTable.ccuAIExternalInput1")
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput2") != None:
            dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalInput2"] = html.var(
                "ccuOAM.ccuAuxIOTable.ccuAIExternalInput2")
        if html.var("ccuOAM.ccuAuxIOTable.ccuAIExternalInput3") != None:
            dic_result["ccuOAM.ccuAuxIOTable.ccuAIExternalInput3"] = html.var(
                "ccuOAM.ccuAuxIOTable.ccuAIExternalInput3")

        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ccu_control_form(h):
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
    obj_bll_set_valid = CcuCommonSetValidation()
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

    elif html.var("ccu_common_submit") == "Save" or html.var("ccu_common_submit") == "Retry" or html.var(
            "ccu_common_submit") == "":
        if html.var("ccuOAM.ccuControlTable.ccuCTLoadTurnOff") != None:
            if Validation.is_required(html.var("ccuOAM.ccuControlTable.ccuCTLoadTurnOff")):
                if Validation.is_number(html.var("ccuOAM.ccuControlTable.ccuCTLoadTurnOff")):
                    dic_result["ccuOAM.ccuControlTable.ccuCTLoadTurnOff"] = html.var(
                        "ccuOAM.ccuControlTable.ccuCTLoadTurnOff")
                else:
                    flag = 1
                    dic_result["success"] = 1
                    dic_result[
                        "result"] = "Load turn Off field must be number."
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "Load Trun Off field is required."
            if Validation.is_required(html.var("ccuOAM.ccuControlTable.ccuCTSMPSCharging")):
                dic_result["ccuOAM.ccuControlTable.ccuCTSMPSCharging"] = html.var(
                    "ccuOAM.ccuControlTable.ccuCTSMPSCharging")
            else:
                flag = 1
                dic_result["success"] = 1
                dic_result["result"] = "SMPS Charging field is required."
        if flag == 1:
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
        else:
            # html.write(str(dic_result))
            result = obj_bll_set_valid.common_validation(
                host_id, device_type_id, dic_result)
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))

    elif html.var("ccu_common_submit") == "Cancel":
        if html.var("ccuOAM.ccuControlTable.ccuCTLoadTurnOff") != None:
            dic_result["ccuOAM.ccuControlTable.ccuCTLoadTurnOff"] = html.var(
                "ccuOAM.ccuControlTable.ccuCTLoadTurnOff")
        if html.var("ccuOAM.ccuControlTable.ccuCTSMPSCharging") != None:
            dic_result["ccuOAM.ccuControlTable.ccuCTSMPSCharging"] = html.var(
                "ccuOAM.ccuControlTable.ccuCTSMPSCharging")
        result = obj_bll_set_valid.ap_cancel_form(
            host_id, device_type_id, dic_result)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))


def ccu_reconciliation(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type")
    user_name = html.req.session['username']
    obj = CCUReconcilation()
    result = obj.update_reconcilation_controller(
        host_id, device_type, "ccu_", datetime.now(), user_name)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


# def page_tip_ccu_listing(h):
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_ccu_listing.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))
