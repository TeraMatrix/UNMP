#!/usr/bin/python2.6

from datetime import datetime
from json import JSONEncoder

from mod_python import util
from common_controller import page_header_search
from firmware_bll import *
from firmware_view import *
from utility import UNMPDeviceType


def firmware_update_device_show(h):
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
    css_list = ['css/ie7.css', 'css/custom.css',
                'css/demo_table_jui.css', 'css/jquery-ui-1.8.4.custom.css']
    jss_list = ['js/lib/main/jquery.dataTables.min.js',
                'js/unmp/main/firmware_updates.js', 'js/lib/main/jquery-ui-personalized-1.6rc2.min.js']

    html.new_header("Firmware Update", "", "", css_list, jss_list)
    # Variable declaration#########################
    # Declare the host id as an empty string
    host_id = ""

    # this is used for storing DeviceTypeList e.g "odu16,odu100"
    device_type = ""

    # this is used for storing DeviceListState e.g "enabled"
    device_list_state = ""
    # this is used for storing the ipaddress,macaddres,hostid and
    # configprofileid which is return form the database
    host_param = []
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
    host_param = device_parameter_bll_obj.get_device_parameter(
        host_id)  # call the idu_profiling_controller function get_device_param returns the list.List Contains ipaddress,macaddress,devicetypeid,config_profile_id
    if isinstance(host_param, list):
        if host_param == [] or host_param == None:
            html.write(page_header_search(
                "", "", "UBR,UBRe", None, "enabled", "device_type"))
            # call the function of common_controller , it is used
            # for listing the Devices based on
            # IPaddress,Macaddress,DeviceTy
        else:
            html.write(page_header_search(host_param[0][0], host_param[0][1],
                                          "UBR,UBRe", device_type, device_list_state, "device_type"))
        html.write((FirmwareUpdateView.firmware_div(host_id, device_type)))
    elif isinstance(host_param, Exception):
        html.write("DataBase Error Occured")
    html.new_footer()


def firmware_master_slave_list(h):
    global html
    html = h
    flag = 0
    obj_bll_get_node_type = FirmwareUpdate()
    firmware_device_list_bll_obj = DeviceParameters()
    ip_address = ""
    mac_address = ""
    selected_device = "odu"
    result = {'site': [], 'success': 0}
    master_slave_list = {}
    master_host_id = []
    final_result = ""
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
        selected_device = "odu"
    else:
        selected_device = html.var("selected_device_type")
    device_list = firmware_device_list_bll_obj.device_list_profiling(
        ip_address, mac_address, selected_device)
    total_record = len(device_list)
    if total_record == 0:
        result = {'msg': 'noProfile', 'success': 1}
    elif total_record > 1:
        result = {'msg': 'moreProfile', 'success': 1}
    else:
        host_id = str(device_list[0][0])
    if host_id == None or host_id == "":
        result = {'msg': 'noHost', 'success': 1}
    else:
        if selected_device == None or selected_device == "":
            result = {'msg': 'missingDeviceType', 'success': 1}
        else:
            node_type = obj_bll_get_node_type.get_node_type(
                host_id, selected_device)
            if len(node_type) > 0 and len(node_type[0]) > 0:
                if node_type[0][0] != 0:
                    master_host_id = obj_bll_get_node_type.get_master_host_id(
                        host_id)
                    if len(master_host_id) > 0 and len(master_host_id[0]) > 0:
                        master_slave_list, final_result = obj_bll_get_node_type.get_master_slave_snmp(
                            str(master_host_id[0][0]), selected_device)
                else:
                    master_slave_list, final_result = obj_bll_get_node_type.get_master_slave_snmp(
                        host_id, selected_device)
            if type(master_slave_list) is list:
                result['site'] = master_slave_list
                result["msg"] = final_result
                result["success"] = 0
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))


def select_firmware_table(h):
    global html
    html = h
    firmware_list = []
    firmware_table = ""
    obj_bll = FirmwareUpdate()
    device_type = html.var("device_type")
    firmware_list = obj_bll.select_firmware_table(device_type)
    firmware_table += "<table class=\"yo-table\" style=\"width:100%%\">\
                            <th>Select Firmware</th>\
                            <th>Firmware File Name</th>\
                            <th>Firmware File Path</th>\
                        "

    if len(firmware_list) > 0:
        for i in range(0, len(firmware_list)):
            firmware_table += "<tr>\
                                <td><input type=\"radio\" name=\"firmware_file\" id=\"%s\"/></td>\
                                <td>%s</td>\
                                <td>%s</td>\
                            </tr>\
                            " % (firmware_list[i][0], firmware_list[i][0], firmware_list[i][1])
    else:
        firmware_table += "<tr>No Data Available</tr>"
    firmware_table += "</table>"

    html.write(str(firmware_table))


def update_firmware_view(h):
    global html
    html = h
    host_id = h.var('host_id')
    device_type = h.var('device_type')
    html.req.session["host_id_session"] = host_id
    html.req.session["device_type"] = device_type
    html.req.session.save()
    upload_form = FirmwareUpdateView.upload_form(host_id, device_type)
    html.write(str(upload_form))


def firmware_file_upload(h):
    global html
    html = h
    objbll = FirmwareUpdate()
    nms_instance = __file__.split(
        "/")[3]       # it gives instance name of nagios system
    flag = 0
    upload_file = {}
    device_type = html.req.session['device_type']
    now = datetime.now()
    form = util.FieldStorage(h.req, keep_blank_values=1)
    upfile = form.getlist('file_uploader')[0]
    filename = upfile.filename
    filedata = upfile.value
    folder_name = ""
    if filename == None or filename == "":
        flag = 1
    else:
        extension = filename.split(".")
        if extension[-1] == "img":
            if device_type == UNMPDeviceType.odu16:
                folder_name = "odu16"
            elif device_type == UNMPDeviceType.odu100:
                folder_name = "odu100"
            file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/firmware_downloads/%s/%s" % (
                nms_instance, folder_name, filename)
            try:
                fobj = open(file_path, 'w')  # 'w' is for 'write'
            except Exception as e:
                flag = 3
            else:
                fobj.write(filedata)
                fobj.close()
                upload_file = objbll.ftp_upload(
                    file_path, device_type, filename)

        else:
            flag = 2
    if flag == 1:
        html.write(
            "<p style=\"font-size:10px;\">Please select a file for Upload<br/><a href=\"javascript:history.go(-1);;\">back</a><p/>")
    elif flag == 2:
        html.write(
            "<p style=\"font-size:10px;\">Only img files are uploaded.Please Choose the correct file<br/><a href=\"javascript:history.go(-1);\">back</a><p/>")
    elif flag == 3:
        html.write(
            "<p style=\"font-size:10px;\">Path not exist for uploading the file.Please contact your administrator<br/></p>")
    else:
        html.write(
            "<p style=\"font-size:10px;\">Firmware Uploading....<br/>Please Wait....<p/>")
        html.write("<p style=\"font-size:10px;\">" + str(upload_file[
            "result"]) + "<br/><p/>")
