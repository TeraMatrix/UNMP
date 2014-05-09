#!/usr/bin/python2.6

"""
@author : Anuj Samariya
@since : 27 June 2011
@version : 0.0
@date : 27 June 2011
@note : In this file there are many functions which create table of master and its related slaves and give the option button with them to select the firmware
        upgrade for that device
@organisation: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
"""

from odu_controller import get_device_param, \
    get_device_list_odu_profiling, check_connection
from common_controller import page_header_search
import pycurl
#import MySQLdb
from mod_python import util
from mysql_collection import mysql_connection
import StringIO
from datetime import datetime
import time


def common_firrmware_controller(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var html : this is html Class Object defined globally
    @since : 20 August 2011
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to make the design of firmware upgrade function like make div,,ake buttons of page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    html.write(
        "<div class=\"form-div\" id=\"odu16_form_div\" style=\"position: relative;\">")
    html.write("</div>")
    html.write("<div id=\"firmware-update\" class=\"form-div-footer\">")
    html.write("<div style=\"position:relative;float:left\"><label class=\"lbl\" style=\"margin: 14px 14px 0px;\">Choose Firmware</label><input id=\"firmware_file\" type=\"file\" name=\"firmware\">\
                <label class=\"error file-error\" style=\"display: none;\">Please Choose Firmware file</label></div>")
    html.write(
        "<div id=\"firmware-update-child-div\" style=\"position:relative;float:left\"><input type=\"button\" value=\"Update Firmware\" id=\"firmware\" class=\"yo-small yo-button\"/></div>")
    html.write(
        "<div id=\"result-div\" style=\"margin:14px 30px 0px;position:relative;float:left;font-size:10px;\"></div>")
    html.write("</div>")


def firmware_listing(h):
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
    @var selected_device_type : this is used to store the device type id whihc is selected on the page
    @var connect_chk : this is used to store a integer value 0 or 1.0 for connection is establish and 1 connection is not established
    @since : 20 August 2011
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to write the search bar in which user search the device according to ipaddress, macaddress, device type
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    sitename = __file__.split("/")[3]
    # This we import the stylesheet
    # This we import the javascript

    # html.write("<script type=\"text/javascript\"
    # src=\"js/unmp/main/firmware_update.js\"></script>\n")
    css_list = ['css/custom.css']
    js_list = ['js/unmp/main/firmware_update.js']
    html.new_header("Firmware Update", "", "", css_list, js_list)
    ip_address = ""
    mac_address = ""

    # this is used for storing DeviceTypeList e.g "odu16,odu100"
    device_type = ""

    # this is used for storing DeviceListState e.g "enabled
    device_list_state = ""

    # this is used for storing SelectedDeviceType e.g. "odu16"
    selected_device_type = ""

    # here we check That variable which is returned from page has value None
    # or not
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

    # Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write
    # we pass parameters
    # ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
    connect_chk = check_connection(
    )  # used to check that the database connection is available or not
    host_id = html.var("host_id")
    if connect_chk == 0 or connect_chk == "0":
        if host_id == None or host_id == "":
            html.write(str(page_header_search(ip_address, mac_address,
                                              "UBR,UBRe", selected_device_type, "enabled", "device_type")))
        else:
            device_list_param = get_device_param(host_id)
            html.write(str(page_header_search(device_list_param[0][0],
                                              device_list_param[0][1], "UBR,UBRe", device_type, "enabled",
                                              "device_type")))
        common_firrmware_controller(h)
    else:
        html.write("<div id=\"odu16_form_div\" style=\"margin:10px\">")
        html.write("UNMP Server unable to connect to UNMP Database.")
        html.write("</div>")

    html.new_footer()


### verify 1 list should not be none , index out of range

def firmware_process(host_id, selected_device):
    """


    @param host_id:
    @param selected_device:
    @author : Anuj Samariya
    @param h : html Class Object
    @var html : this is html Class Object defined globally
    @var host_id : this is used to store the Host Id which is come from the page
    @var master : this is used to store the master's list
    @var slaves : this is used to store the slave's list
    @var result : this is used to store integer type value like 0,1 0 for master and 1 for not master
    @var firmware_result : this is a list which store slave information,master information
    @var selected_device : this is used to store the device type id whihc is selected on the page
    @var table_str : this is used to store the html string
    @var result_final : this is used to store the integer value which identify that the firmware is in progress or done
    @since : 20 August 2011
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to store the list of master and slave and show it as a table on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html
        slaves = []
        master = []
        result = firmware_device_check_controller(
            host_id, selected_device)  # check that the device is master or not
        # html.write(str(result))
        if str(result) == "0" or str(result) == 0:
            firmware_result = firmware_process_controller(
                host_id, selected_device)  # used to count the number of slaves connected to a master
            # html.write(str(firmware_result))
            table_str = "<table class=\"yo-table\" cellspacing=\"0\" cellpadding=\"0\" id=\"firmware_table\" width=\"100%\">\
                            <tr>\
                                <th align=\"left\">Select Master</th>\
                                <th align=\"left\">Master</th>\
                                <th align=\"left\">Slave</th>\
                            </tr>\
                        "
            # html.write(str(firmware_result))
            if firmware_result == 8:
                html.write("No Data Regarding This Host")

            elif firmware_result == 4:
                html.write("No Data Regarding This Host")

            elif len(firmware_result) > 0:
                if firmware_result[2] == 0:
                    result_final = firmware_refresh(firmware_result, 0)
                    html.write("<input type=\"hidden\" id=\"result_final\" name=\"result_final\" value=\"%s\"/>" %
                               (str(result_final[0])))
                    html.write(
                        "<input type=\"hidden\" id=\"result_msg\" name=\"result_msg\" value=\"%s\"/>" % (
                        str(result_final[1])))
                    if result_final[0] == 0:
                        if len(firmware_result[1]) > 0:
                            master.append({'tr_master': firmware_result[1][0][0] if (firmware_result[0])
                                                                                    == 7 or (
                            firmware_result[0]) == 6 else firmware_result[0][0][0]})
                            table_str += "<tr style=\"background-color:#EEE\" slave_value=\"[]\" >\
                                                <td><input type=\"radio\" id=\"selct_master_tr\" name=\"\"/></td>\
                                                <td id=tr_master master_value=\"[{'tr_master':'%s'}]\" >%s(%s)</td>\
                                                <td id=\"tr_0\" class=\"loadingimage\" style=\"width:500px\">No One Slave Connected To this Device\
                                                <input class=\"img-loader\" title=\"loading\" style=\"float: right;\"></td>\
                                                \
                                            </tr>" % (
                            firmware_result[1][0][0] if (firmware_result[0]) == 7 or (firmware_result[0]) == 6 else
                            firmware_result[0][0][0],
                            firmware_result[1][0][1] if (firmware_result[0]) == 7 or (firmware_result[0]) == 6 else
                            firmware_result[0][0][1],
                            firmware_result[1][0][3] if (firmware_result[0]) == 7 or (firmware_result[0]) == 6 else
                            firmware_result[0][0][3])
                            table_str += "</table>\
                                            <input type=\"hidden\" value=\"\" id=\"master\" id=\"master_value\"/>\
                                            <input type=\"hidden\" value=\"\" name=\"slave\" id=\"slave_value\"/>\
                                            <input type=\"hidden\" value=\"%s\" name=\"device_type\" id=\"device_type\"/>" % (
                            selected_device)
                            html.write(str(table_str))
                    else:
                        if len(firmware_result[1]) > 0:
                            master.append({'tr_master': firmware_result[1][0][0] if (firmware_result[0])
                                                                                    == 7 or (
                            firmware_result[0]) == 6 else firmware_result[0][0][0]})
                            table_str += "<tr slave_value=\"[]\">\
                                                <td><input type=\"radio\" id=\"selct_master_tr\" name=\"select_master\"/></td>\
                                                <td id=tr_master master_value=\"[{'tr_master':'%s'}]\">%s(%s)</td>\
                                                <td id=\"tr_0\" class=\"loadingimage\" style=\"width:500px\">No One Slave Connected To this Device</td>\
                                               \
                                            </tr>" % (
                            firmware_result[1][0][0] if (firmware_result[0]) == 7 or (firmware_result[0]) == 6 else
                            firmware_result[0][0][0],
                            firmware_result[1][0][1] if (firmware_result[0]) == 7 or (firmware_result[0]) == 6 else
                            firmware_result[0][0][1],
                            firmware_result[1][0][3] if (firmware_result[0]) == 7 or (firmware_result[0]) == 6 else
                            firmware_result[0][0][3])
                            table_str += "</table>\
                                            <input type=\"hidden\" value=\"\" name=\"master\" id=\"master_value\"/>\
                                            <input type=\"hidden\" value=\"\" name=\"slave\" id=\"slave_value\"/>\
                                            <input type=\"hidden\" value=\"%s\" name=\"device_type\" id=\"device_type\"/>" % (
                            selected_device)
                            html.write(str(table_str))
                else:

                    result_final = firmware_refresh(firmware_result, 1)
                    html.write("<input type=\"hidden\" id=\"result_final\" name=\"result_final\" value=\"%s\"/>" %
                               (str(result_final[0])))
                    html.write(
                        "<input type=\"hidden\" id=\"result_msg\" name=\"result_msg\" value=\"%s\"/>" % (
                        str(result_final[1])))
                    if result_final[0] == 0:
                        for i in range(0, firmware_result[2]):
                            slaves.append(
                                {"tr_%s" % (i): firmware_result[1][0][i][0]})
                            if i == 0:
                                table_str += "<tr style=\"background-color:#EEE\" slave_value=%s>\
                                                    <td rowspan=\"%s\"><input type=\"radio\" id=\"selct_master_tr\" name=\"select_master\"/></td>\
                                                    <td rowspan=\"%s\" id=\"tr_master\" master_value=\"[{'tr_master':'%s'}]\">%s(%s)</td>\
                                                    <td id=\"tr_%s\" class=\"loadingimage\" style=\"width:500px\">%s(%s)\
                                                    <input class=\"img-loader\" title=\"loading\" style=\"float: right;\" type=\"image\"></td>\
                                                </tr>" % (
                                ("".join(str(slaves).split())), firmware_result[2], firmware_result[2],
                                firmware_result[0][0][0],
                                "Master" if firmware_result[0][0][1] == None or firmware_result[0][0][1] == "" else str(
                                    firmware_result[0][0][1]),
                                "IP Address" if firmware_result[0][0][
                                                    3] == None or firmware_result[0][0][3] == "" else
                                firmware_result[0][0][3],
                                i, firmware_result[1][0][i][5], firmware_result[1][0][i][2])
                            if i >= 1:
                                table_str += "<tr>\
                                                    <td id=\"tr_%s\" class=\"loadingimage\">%s(%s)\
                                                    \
                                                    <input class=\"img-loader\" title=\"loading\" style=\"float: right;\"></td>\
                                                </tr>" % (i, firmware_result[1][0][i][5], firmware_result[1][0][i][2])
                        master.append({"tr_master": firmware_result[0][0][0]})
                        table_str += "</table>\
                                        <input type=\"hidden\" value=\"\" name=\"master\" id=\"master_value\"/>\
                                        <input type=\"hidden\" value=\"\" name=\"slave\" id=\"slave_value\"/>\
                                        <input type=\"hidden\" value=\"%s\" name=\"device_type\" id=\"device_type\"/>" % (
                        selected_device)
                        html.write(str(table_str))
                    else:
                        for i in range(0, firmware_result[2]):
                            slaves.append({"tr_%s" % (
                                i): firmware_result[1][0][i][0]})
                            if i == 0:
                                table_str += "<tr slave_value=%s>\
                                                    <td rowspan=\%s\"><input type=\"radio\" id=\"selct_master_tr\" name=\"select_master\"/></td>\
                                                    <td rowspan=\"%s\" id=\"tr_master\" master_value=\"[{'tr_master':'%s'}]\" >%s(%s)</td>\
                                                    <td id=\"tr_%s\" class=\"loadingimage\" style=\"width:500px\">%s(%s)</td>\
                                                </tr>" % (
                                ("".join(str(slaves).split())), firmware_result[2], firmware_result[2],
                                firmware_result[0][0][0],
                                "Master" if firmware_result[0][0][1] == None or firmware_result[0][0][1] == "" else str(
                                    firmware_result[0][0][1]),
                                "IP Address" if firmware_result[0][0][
                                                    3] == None or firmware_result[0][0][3] == "" else
                                firmware_result[0][0][3],
                                i, firmware_result[1][0][i][5], firmware_result[1][0][i][2])

                            if i >= 1:
                                table_str += "<tr>\
                                                    <td id=\"tr_%s\" class=\"loadingimage\">%s(%s)</td>\
                                                </tr>" % (i, firmware_result[1][0][i][5], firmware_result[1][0][i][2])
                        table_str += "</table>\
                                        <input type=\"hidden\" value=\"\" name=\"master\" id=\"master_value\"/>\
                                        <input type=\"hidden\" value=\"\" name=\"slave\" id=\"slave_value\"/>\
                                        <input type=\"hidden\" value=\"%s\" name=\"device_type\" id=\"device_type\"/>" % (
                        selected_device)
                        html.write(str(table_str))
            elif int(firmware_result[0]) == 7 or int(firmware_result[0]) == 6:
                if len(firmware_result[1]) > 0:
                    master.append({'tr_master': firmware_result[1][0]})
                    table_str += "<tr>\
                                    <td id=tr_master>%s(%s)</td>\
                                    <td>No Connected Slaves Found</td>\
                                </tr>" % (firmware_result[1][1], firmware_result[1][3])
                    table_str += "</table>\
                                <input type=\"hidden\" value=\"%s\" name=\"master\" id=\"master_value\"/>\
                                <input type=\"hidden\" value=\"%s\" name=\"slave\" id=\"slave_value\"/>\
                                <input type=\"hidden\" value=\"%s\" name=\"device_type\" id=\"device_type\"/>" % (
                    master, [], selected_device)
                    html.write(table_str)
        elif result == -1:
            html.write("Device Unresponsive. Please try again later.")
        elif result == 1:
            html.write(
                "The Selected Device is of type Slave.Please Select The Master Device For Firemware Upgrade")

        elif result == 2:
            html.write("No Data Regarding This Device.")

        elif result == 3:
            html.write("No Configuration Exist For this Device.")

        elif result == 4:
            html.write("Host Doesn't exist")

        elif result == 5:
            html.write("Page Can't be Displayed.")
    except Exception as e:
        html.write(str(e[-1]))


def update_firmware_result(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var html : this is html Class Object defined globally
    @var master_id : this is used to store the database id of master it is in string format
    @var master : this is used to store the master id in a list format
    @var result : this is used to store the result of firmware progress in 0 or 1 form, 1 means done or 0 means in progress
    @since : 20 August 2011
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to update the result of firmware progress and write it on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    master_id = html.var(("master"))
    master = eval(master_id)
    result = firmware_update_result(master[0]["tr_master"])
    # html.write(str(master[0]["tr_master"]))
    html.write(str(result))


def get_device_list_for_firmware(h):
    """"
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
    @note : this function is used to select the from function according to device type means which device configuration shows on page is decided with this function
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html
        html = h

        # this is the result which we show on the page
        result = ""
        ip_address = ""
        mac_address = ""
        selected_device = "ODU16"
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
            selected_device = ""
        else:
            selected_device = html.var("selected_device_type")

        # call the function get_odu_list of odu-controller which return us the
        # list of devices in two dimensional list according to
        # IPAddress,MACaddress,SelectedDevice

        result = get_device_list_odu_profiling(
            ip_address, mac_address, selected_device)
        if result == 0 or result == 1 or result == 2:
            html.write(str(result))
        else:
            if result == None or result == "":
                html.write(str("Empty Set Returned."))
            else:
                # html.write(str(result+selected_device))
                firmware_process(result, selected_device)
    except Exception as e:
        html.write(str(e))


def firmware_update_set(h):
    """
    @author : Anuj Samariya
    @param h : html Class Object
    @var html : this is html Class Object defined globally
    @var master : thsi is used to store the master's list
    @var slave_value : this is used to store the slave list
    @var filenameval : this is used to store the full file path
    @var file_name : this is used to store the filename splitting from the full filenameval path
    @var result : this is used to store the result of firmware upgrade
    @version :0.0
    @date : 20 Augugst 2011
    @note : this function is used to make a list of master and its slaves and give it to the controller function,controller function set the firmware upgrade
            with snmp set and return the result back to this funtion
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """

    from datetime import datetime

    global html
    html = h
    master = []
    slave_value = ""
    filenameval = ""
    file_name = ""
    current_datetime = datetime.now()
    if html.var("master") == None or html.var("master") == [] or html.var("master") == "":
        master = []
    else:
        master = html.var("master")
    if html.var("device_type") == None or html.var("device_type") == [] or html.var("device_type") == "":
        device_type = ""
    else:
        device_type = html.var("device_type")
    if html.var("slave") == None or html.var("slave") == [] or html.var("slave") == "":
        slave_value = []
    else:
        slave_value = html.var("slave")
    if html.var("filename") == None or html.var("filename") == "":
        file_name = "1"
    else:
        filenameval = html.var("filename")
        filenameval = filenameval.split("\\")
        file_name = filenameval[-1]
        # slaves = list_convert(slave_value)
    # html.write(str(eval(slave_value)))
    if device_type != "":
        result = firmware_final_set(eval(master), eval(
            slave_value), current_datetime, device_type, file_name)
    else:
        result = "False"
    html.write(str(result))


# def page_tip_firmware_update(h):
#     """
#     @author : Anuj Samariya
#     @param h : html Class Object
#     @var html : this is html Class Object defined globally
#     @var html_view : this is used to store the html string
#     @version :0.0
#     @date : 20 Augugst 2011
#     @note : this function is used to make a page tip and show it on the page
#     @organisation : Codescape Consultants Pvt. Ltd.
#     @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
#     """
#     global html
#     html = h
#     import defaults
#     f = open(defaults.web_dir + "/htdocs/locale/page_tip_firmware_update.html", "r")
#     html_view = f.read()
#     f.close()
#     html.write(str(html_view))


def firmware_file_upload(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h

    try:
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/image.img" % (
            nms_instance)
        form = util.FieldStorage(h.req, keep_blank_values=1)
        upfile = form.getlist('file_uploader')[0]
        filename = upfile.filename
        filedata = upfile.value
        fobj = open(file_path, 'w')  # 'w' is for 'write'
        fobj.write(filedata)
        fobj.close()
        password = ''
        user_name = ''

        if filename == None or filename == "":
            html.write(
                "<p style=\"font-size:10px;\">Please Choose the file for Upgrade<br/><br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
        else:
            db, cursor = mysql_connection('midnms')
            if db == 1:
                raise SelfException(cursor)

                # get the ip address of ap correspondence
            sel_query = "SELECT ip_address,http_username,http_password FROM hosts WHERE host_id='%s'" % (
                html.req.session["host_id_session"])
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                ip_address = result[0][0]
                user_name = '' if result[0][1] == None else result[0][1]
                password = '' if result[0][2] == None else result[0][2]
                c = pycurl.Curl()
                b = StringIO.StringIO()
                file = file_path
                values = [('image', (c.FORM_FILE, file))]
                c.setopt(pycurl.URL,
                         "http://%s/cgi-bin/FirmwareUpgrade" % ip_address)
                # c.setopt(pycurl.HTTPHEADER, ['Accept:
                # application/json'])http://172.22.0.101/cgi-
                # bin/FirmwareUpgrade
                c.setopt(c.HTTPPOST, values)
                c.setopt(pycurl.VERBOSE, 0)
                c.setopt(pycurl.USERPWD, user_name + ':' + password)
                c.setopt(c.WRITEFUNCTION, b.write)
                c.perform()
                responseCode = c.getinfo(pycurl.RESPONSE_CODE)
                responseString = b.getvalue()
                c.close()

                if int(responseCode) == 404:
                    html.write(
                        "<p style=\"font-size:10px;font-wight:bold;\">The path of firmware upload is not correct.<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
                elif int(responseCode) == 401:
                    html.write(
                        "<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
                elif int(responseCode) == 200:
                    result = responseString.find(
                        "Firmware image has bad magic number")
                    if result != -1:
                        html.write(
                            "<p style=\"font-size:10px;font-wight:bold;\">Wrong File is Uploaded<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
                    result = responseString.find("Firmware upgrade complete")
                    if result != -1:
                        html.write(
                            "<p style=\"font-size:10px;font-wight:bold;\">Firmware Uploaded Successfully. Device will Reboot now.</p>")
                    result = responseString.find(
                        "Device is now being automatically rebooted")
                    if result != -1:
                        html.write(
                            "<p style=\"font-size:10px;font-wight:bold;\">Firmware Updated Successfully</p>")

                else:
                    html.write(
                        "<p style=\"font-size:10px;font-wight:bold;\">Host does not exists so check the host and try again.</p>")
            db.close()
    except pycurl.error, e:
        if int(e[0]) == 7:
            html.write(
                "<p style=\"font-size:10px;font-wight:bold;\">Device is not Connected.</p>")
        elif int(e[0]) == 26:
            html.write(
                "<p style=\"font-size:10px;font-wight:bold;\">The Firmware file is missing.</p>")
        else:
            html.write("Unkown Problem Occured")
    except Exception, e:
        html.write(
            "<p style=\"font-size:10px;font-wight:bold;\">Firmware update not done.Please try again...</p>")

#    finally:
#        if isinstance(db,MySQLdb.connection):
#            if db.open:
#                db.close()


def ap_firmware_view(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = h.var('host_id')
    device_type = h.var('device_type')
    device_list_state = h.var('device_list_state')
    html.req.session["host_id_session"] = host_id
    html.req.session.save()

    html.write(
        "<form method=\"post\" enctype=\"multipart/form-data\" action=\"firmware_file_upload.py\" style=\"font-size:10px;\"><input type=\"hidden\" name=\"host_id\" value=\"%s\"/><input type=\"hidden\" name=\"device_type\" value=\"%s\"/><input type=\"hidden\" name=\"device_list_state\" value=\"%s\"/><label style=\"margin-top: 15px;margin-right: 25px;\" class=\"lbl\">Firmware File</label><input style=\"font-size:10px;\" type=\"file\" name=\"file_uploader\" id=\"file_uploader\"><button name=\"button_uploader\" id=\"button_uploader\" type=\"file\" style=\"font-size:10px;\" class=\"yo-button yo-small\"><span class=\"upload\">Upload</span></button></form>" % (
        host_id, device_type, device_list_state))


def odu_firmware_view(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = h.var('host_id')
    device_type = h.var('device_type')
    device_list_state = h.var('device_list_state')
    html.req.session["host_id_session"] = host_id
    html.req.session.save()

    html.write(
        "<form method=\"post\" enctype=\"multipart/form-data\" action=\"odu_firmware_file_upload.py\" style=\"font-size:10px;\"><input type=\"hidden\" name=\"host_id\" value=\"%s\"/><input type=\"hidden\" name=\"device_type\" value=\"%s\"/><input type=\"hidden\" name=\"device_list_state\" value=\"%s\"/><label style=\"margin-top: 15px;margin-right: 25px;\" class=\"lbl\">Firmware File</label><input style=\"font-size:10px;\" type=\"file\" name=\"file_uploader\" id=\"file_uploader\"><button name=\"button_uploader\" id=\"button_uploader\" type=\"file\" style=\"font-size:10px;\" class=\"yo-button yo-small\"><span class=\"upload\">Upload</span></button></form>" % (
        host_id, device_type, device_list_state))


def odu_firmware_file_upload(h):
    """

    @param h:
    @raise:
    """
    global html
    html = h

    try:
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/image.img" % (
            nms_instance)
        form = util.FieldStorage(h.req, keep_blank_values=1)
        upfile = form.getlist('file_uploader')[0]
        filename = upfile.filename
        filedata = upfile.value
        fobj = open(file_path, 'w')  # 'w' is for 'write'
        fobj.write(filedata)
        fobj.close()
        password = ''
        user_name = ''

        if filename == None or filename == "":
            html.write(
                "<p style=\"font-size:10px;\">Please Choose the file for Upgrade<br/><br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
        else:
            db, cursor = mysql_connection('midnms')
            if db == 1:
                raise SelfException(cursor)

                # get the ip address of ap correspondence
            sel_query = "SELECT ip_address,http_username,http_password FROM hosts WHERE host_id='%s'" % (
                html.req.session["host_id_session"])
            cursor.execute(sel_query)
            result = cursor.fetchall()
            if len(result) > 0:
                ip_address = result[0][0]
                user_name = '' if result[0][1] == None else result[0][1]
                password = '' if result[0][2] == None else result[0][2]
                c = pycurl.Curl()
                b = StringIO.StringIO()
                file = file_path
                values = [('image', (c.FORM_FILE, file))]
                c.setopt(pycurl.URL, "http://%s/cgi-bin/index" % ip_address)
                # c.setopt(pycurl.HTTPHEADER, ['Accept:
                # application/json'])http://172.22.0.101/cgi-
                # bin/FirmwareUpgrade
                c.setopt(c.HTTPPOST, values)
                c.setopt(pycurl.VERBOSE, 0)
                c.setopt(pycurl.USERPWD, user_name + ':' + password)
                c.setopt(c.WRITEFUNCTION, b.write)
                c.perform()
                responseCode = c.getinfo(pycurl.RESPONSE_CODE)
                responseString = b.getvalue()
                c.close()

                if int(responseCode) == 404:
                    html.write(
                        "<p style=\"font-size:10px;font-wight:bold;\">Page not found<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
                elif int(responseCode) == 401:
                    html.write(
                        "<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
                elif int(responseCode) == 200:
                    result = responseString.find(
                        "Firmware image has bad magic number")
                    if result != -1:
                        html.write(
                            "<p style=\"font-size:10px;font-wight:bold;\">Wrong File is Uploaded<br/><a href=\"javascript:history.go(-1)\">Back</a><p/>")
                    result = responseString.find("Firmware upgrade complete")
                    result1 = responseString.find(
                        "Device is now being automatically rebooted")
                    if result != -1 or result1 != -1:
                        html.write(
                            "<p style=\"font-size:10px;font-wight:bold;\">Firmware Update Successfully.Device is now being automatically rebooted.</p>")
                        if filename.find("7.2.25") >= 0:
                            sel_query = "update hosts set firmware_mapping_id = '%s' where host_id = '%s'" % (
                                "7.2.25", html.req.session["host_id_session"])
                        else:
                            sel_query = "update hosts set firmware_mapping_id = '%s' where host_id = '%s'" % (
                                "7.2.20", html.req.session["host_id_session"])
                        cursor.execute(sel_query)
                        del_query = "TRUNCATE TABLE  odu100_raAclConfigTable"  # empty the ACL table when firmware will update.
                        cursor.execute(del_query)
                        db.commit()
                else:
                    html.write(
                        "<p style=\"font-size:10px;font-wight:bold;\">Host does not exists so check the host and try again.</p>")
            db.close()
    except pycurl.error, e:
        if int(e[0]) == 7:
            html.write(
                "<p style=\"font-size:10px;font-wight:bold;\">Device is not Connected.</p>")
        elif int(e[0]) == 26:
            html.write(
                "<p style=\"font-size:10px;font-wight:bold;\">The Firmware file is missing.</p>")
        else:
            html.write("Unkown Problem Occured")
    except Exception, e:
        html.write(
            "<p style=\"font-size:10px;font-wight:bold;\">Firmware update not done.Please try again...</p>")


def idu_firmware_file_upload(h):
    """

    @param h:
    @return: @raise:
    """
    global html
    html = h

    try:
        nms_instance = __file__.split(
            "/")[3]       # it gives instance name of nagios system
        flag = 0
        activate = 0
        idu_reboot = 0
        current_time = datetime.now()
        form = util.FieldStorage(h.req, keep_blank_values=1)
        upfile = form.getlist('fufile')[0]
        filename = upfile.filename
        filedata = upfile.value
        file_path = "/omd/sites/%s/share/check_mk/web/htdocs/download/%s" % (
            nms_instance, filename)
        fobj = open(file_path, 'w')  # 'w' is for 'write'
        fobj.write(filedata)
        fobj.close()
        password = ''
        user_name = ''
        cgi_result = ""
        i = 0
        j = 0
        if filename == None or filename == "":
            html.write(
                "<p style=\"font-size:10px;\">Please Choose the file for Upgrade<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
            return
        else:
            db, cursor = mysql_connection('midnms')
            if db == 1:
                raise SelfException(cursor)

        # get the ip address of ap correspondence
        sel_query = "SELECT ip_address,http_username,http_password,http_port FROM hosts WHERE host_id='%s'" % (
            html.req.session["host_id_session"])
        cursor.execute(sel_query)
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
            ip_address = result[0][0]
            user_name = '' if result[0][1] == None else result[0][1]
            password = '' if result[0][2] == None else result[0][2]
            port = result[0][3]
            c = pycurl.Curl()
            b = StringIO.StringIO()
            file = file_path
            values = [('fufile', (c.FORM_FILE, file))]
            c.setopt(pycurl.URL,
                     "http://%s:%s/cgi-bin/uploadfile.cgi" % (ip_address, port))

            c.setopt(c.HTTPPOST, values)
            c.setopt(pycurl.VERBOSE, 0)
            c.setopt(pycurl.USERPWD, user_name + ':' + password)
            c.setopt(c.WRITEFUNCTION, b.write)
            c.perform()
            responseCode = c.getinfo(pycurl.RESPONSE_CODE)
            responseString = b.getvalue()
            c.close()
            if int(responseCode) == 404:
                html.write(
                    "<p style=\"font-size:10px;font-wight:bold;\">Page not found.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
            elif int(responseCode) == 401:
                html.write(
                    "<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
            elif int(responseCode) == 200:
                if responseString.find("File Transfer Complete") != -1:
                    html.write(
                        "<p style=\"font-size:10px;\">File Transfer Complete.Please wait while system Saves the file.<br/>Activating the new image file.Please Wait...</p>")

                    while (1):
                        db, cursor = mysql_connection('midnms')
                        query = "select trap_event_id,description,timestamp from midnms.trap_alarms where trap_event_id = '%s' and agent_id = '%s' and timestamp>='%s'" % (
                            '4', str(ip_address), str(current_time)[:19])
                        cursor.execute(query)
                        cgi_result = cursor.fetchall()
                        cursor.close()
                        if i < 10:
                            if len(cgi_result) > 0:
                                current_time = cgi_result[0][2]
                                flag = 0
                                break
                            else:
                                i = i + 1
                                time.sleep(15)
                                flag = 1
                                continue
                        else:
                            break

                    if flag == 0:
                        if cgi_result[0][1] == "Image Upgrade Failure":
                            html.write(
                                "<p style=\"font-size:10px;\">Image Upload Failed.Please try again with right image<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                        elif cgi_result[0][1] == "New Image Upgrade Success":
                            html.write(
                                "<p style=\"font-size:10px;\">Image Upload Successfully.Plase wait for activating the image</p>")
                            c = pycurl.Curl()
                            b = StringIO.StringIO()
                            values = [('activate', 'Activate')]
                            c.setopt(pycurl.URL,
                                     "http://%s:%s/cgi-bin/activateimage.cgi" % (ip_address, port))
                            c.setopt(c.HTTPPOST, values)
                            c.setopt(pycurl.VERBOSE, 0)
                            c.setopt(
                                pycurl.USERPWD, user_name + ':' + password)
                            c.setopt(c.WRITEFUNCTION, b.write)
                            c.perform()
                            responseCode = c.getinfo(pycurl.RESPONSE_CODE)
                            responseString = b.getvalue()
                            c.close()
                            if int(responseCode) == 404:
                                html.write(
                                    "<p style=\"font-size:10px;font-wight:bold;\">The path of firmware upload is not correct.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                            elif int(responseCode) == 401:
                                html.write(
                                    "<p style=\"font-size:10px;font-wight:bold;\">Username and Password are wrong.<br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                            elif int(responseCode) == 200:
                                while (1):
                                    db, cursor = mysql_connection('midnms')
                                    query = "select trap_event_id,description,timestamp from midnms.trap_alarms where trap_event_id in ('%s','%s') and agent_id = '%s' and timestamp>'%s'" % (
                                        '7', '67', str(ip_address), str(current_time))
                                    cursor.execute(query)
                                    cgi_final_result = cursor.fetchall()
                                    cursor.close()
                                    j = 0
                                    if j < 20:
                                        if len(cgi_final_result) > 0:
                                            current_time = cgi_final_result[
                                                0][2]
                                            if activate == 0:
                                                if cgi_final_result[0][1].find("Activating passive image") != -1:
                                                    html.write(
                                                        "<p style=\"font-size:10px;font-wight:bold;\">Activating image.<br/></p>")
                                                    html.write(
                                                        "<p style=\"font-size:10px;font-wight:bold;\">Device is rebooting.Please wait.....<br/></p>")
                                                    activate = 1
                                            if idu_reboot == 0:
                                                if cgi_final_result[0][1].find("IDU started") != -1:
                                                    idu_reboot = 1
                                            if cgi_final_result[0][1].find(
                                                    "Image passed approval period. Image activation success") != -1:
                                                html.write(
                                                    "<p style=\"font-size:10px;font-wight:bold;\">Firmware upgrade successfully.<br/></p>")
                                                flag = 0
                                                break
                                        else:
                                            j = j + 1
                                            time.sleep(30)
                                            flag = 1
                                            continue
                                    else:
                                        flag = 1
                                        break
                            if flag == 0:
                                if idu_reboot == 1:
                                    html.write(
                                        "<p style=\"font-size:10px;\">Device rebooted successfully</p>")
                            else:
                                html.write(
                                    "<p style=\"font-size:10px;\">Image Activation Failed.Please Try again<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
                        else:
                            html.write(
                                "<p style=\"font-size:10px;\">Host Not Exist<br/><br/><a href=\"javascript:history.go(-1)\">Back</a></p>")
        db.close()
    except pycurl.error, e:
        if int(e[0]) == 7:
            html.write(
                "<p style=\"font-size:10px;font-wight:bold;\">Device is not Connected.</p>")
        elif int(e[0]) == 26:
            html.write(
                "<p style=\"font-size:10px;font-wight:bold;\">The Firmware file is missing.</p>")
        else:
            html.write("Unkown Problem Occured")
    except Exception, e:
        html.write(str(e))
        html.write(
            "<p style=\"font-size:10px;font-wight:bold;\">Firmware update not done.Please try again...</p>")


def idu_firmware_view(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = h.var('host_id')
    device_type = h.var('device_type')
    device_list_state = h.var('device_list_state')
    html.req.session["host_id_session"] = host_id
    html.req.session.save()

    html.write(
        "<form method=\"post\" enctype=\"multipart/form-data\" name=\"main_form\" action=\"idu_firmware_file_upload.py\" style=\"font-size:10px;\"><input type=\"hidden\" name=\"host_id\" value=\"%s\"/><input type=\"hidden\" name=\"device_type\" value=\"%s\"/><input type=\"hidden\" name=\"device_list_state\" value=\"%s\"/><input type=\"hidden\" name=\"current_date_time\" value=\"%s\"/><label style=\"margin-top: 15px;margin-right: 25px;\" class=\"lbl\">Firmware File</label><input style=\"font-size:10px;\" type=\"file\" name=\"fufile\" id=\"fufile\"><button name=\"button_uploader\" id=\"button_uploader\" type=\"submit\" style=\"font-size:10px;\" class=\"yo-button yo-small\"><span class=\"upload\">Upload</span></button></form>" % (
        host_id, device_type, device_list_state, datetime.now()))
