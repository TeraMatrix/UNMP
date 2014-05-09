#!/usr/bin/python2.6

""" 
@author:Anuj Samariya 
@since: 27 June 2011
@version: 0.0
@date: 27 June 2011
@note: In this file there are many classes and functions which create forms of Profiling and shows the forms on page,
       there is a functions which shows list of devices which are available on site and functions which take values of page
       and call the controller functions and pass the page values on that function and according to response it shows the 
       profiling page values are set or not set.
@organisation: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
"""

####################### import the packages ###################################
#import config,htmllib,pprint,sidebar,views,time,defaults,os,xml.dom.minidom,subprocess,datetime,re,tarfile,MySQLdb,urllib2,base64
#from lib import *
#from mod_python import apache,util
from odu_controller import *
#import unmp_model
from utility import Validation
from common_controller import page_header_search
from json import JSONEncoder
import traceback
from common_bll import Essential
from datetime import datetime
from idu_profiling_bll import IduGetData
###############################################################################
obj_essential = Essential ()
host_status_dic = {0:'No operation', 1:'Firmware download', 2:'Firmware upgrade', 3:'Restore default config', 4:'Flash commit', 5:'Reboot', 6:'Site survey', 7:'Calculate BW', 8:'Uptime service', 9:'Statistics gathering', 10:'Reconciliation', 11:'Table reconciliation', 12:'Set operation', 13:'Live monitoring', 14:'Status capturing', 15:'Refreshing Site Survey', '16':'Refreshing RA Channel List'}
#Device is busy, Device <> is in progress. please wait ...
def odu_dashboard(h):
    """
    @requires:     
    @return: 
    @rtype: 
    @author:
    @since: 
    @version: 
    @date: 
    @note: 
    @organisation: Codescape Consultants Pvt. Ltd.
    @copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    html.new_header("UBR Dashboard");
    html.new_footer()

def odu_listing(h):
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
    css_list = ["css/demo_table_jui.css", "css/jquery-ui-1.8.4.custom.css", 'css/ccpl_jquery_combobox.css']
    javascript_list = ["js/jquery.dataTables.min.js", 'js/ccpl_jquery_autocomplete.js', "js/odu_listing.js"]

    #This we import the javascript
    ip_address = ""
    mac_address = ""

    #this is used for storing DeviceTypeList e.g "UBR,odu100"
    device_type = ""

    #this is used for storing DeviceListState e.g "enabled
    device_list_state = ""

    #this is used for storing SelectedDeviceType e.g. "UBR" 
    selected_device_type = ""

    #here we check That variable which is returned from page has value None or not
    if html.var("device_type") != None: #we get the variable of page through html.var
        device_type = html.var("device_type")
    if html.var("device_list_state") != None:
        device_list_state = html.var("device_list_state")
    if html.var("selected_device_type") != None:
        selected_device_type = html.var("selected_device_type")
    if html.var("ip_address") != None:
        ip_address = html.var("ip_address")
    if html.var("mac_address") != None:
        mac_address = html.var("mac_address")

    snapin_list = ["reports", "views", "Alarm", "Inventory", "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    #Here we print the heading of page
    html.new_header("RM18/RM Listing", "odu_listing.py", "", css_list, javascript_list, snapin_list)

    #Here we call the function pageheadersearch of common_controller which return the string in html format and we write it on page through html.write 
    #we pass parameters 
    #ipaddress,macaddress,devicelist,selectedDevice,devicestate,selectdeviceid
    html.write(str(page_header_search(ip_address, mac_address, "RM18,RM,IDU,Access Point,CCU", selected_device_type, "enabled", "device_type")))

    #Here we make a div to show the result in datatable
    table_view = "<div>"
    table_view += "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" class=\"display\" id=\"device_data_table\" style=\"text-align:center\">\
                    <thead>\
                        <tr>\
                            <th>Device Status</th>\
                            <th>Host Alias</th>\
                            <th>Host Group</th>\
                            <th>IP Address</th>\
                            <th>MAC (eth)</th>\
                            <th>MAC (Radio)</th>\
                            <th>Device Type</th>\
                            <th>Slave Of</th>\
                            <th>Admin State</th>\
                            <th>Actions</th>\
                            <th>OP State</th>\
                        </tr>\
                    </thead>\
                </table>\
                <input name='device_type' id='device_type' value='%s' type='hidden'/>\
                </div>\
                <div id=\"status_div\" style=\"position:absolute;display:none\"/>hi\
                </div>" % (device_type)
    html.write(table_view)
    html.new_footer()

def page_tip_odu_listing(h):
    """
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @since : 12 December 2011
    @version :0.0 
    @date : 12 December 2011
    @note : This function is used for diplaying the help of odu Listing page.Every link help.Every button Help.What output display.Every Image description.
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>RM/RM18 Listing</h1>"\
        "<div><strong>RM18/RM Listing</strong> has shown all RM18/RM Type Devices.On This Page You Can see Various Options</div>"\
        "<br/>"\
        "<div>On this page you can Edit Configuration, Update Firmware,See Graph and Events for Monitoring of Devices and also make Reconciliation of Devices.</div>"\
        "<br/>"\
        "<div><strong>Actions</strong></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/edit.png\"/></div><div class=\"txt-div\">Edit Configuration</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/graph.png\"/></div><div class=\"txt-div\">Device Monitoring</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/alert.png\"/></div><div class=\"txt-div\">Device Events</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/update.png\"/></div><div class=\"txt-div\">Firmware Upgrade</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-green.png\"/></div><div class=\"txt-div\">Reconciliation done 100%</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-black.png\"/></div><div class=\"txt-div\">Reconciliation done in between 36% and less than 90%</div></div>"\
        "<div class=\"action-tip\"><div class=\"img-div img-div2\"><img style=\"width:16px;height:16px;\" src=\"images/new/r-red.png\"/></div><div class=\"txt-div\">Reconciliation done in between 0% and 35%</div></div>"\
        "<br/>"\
        "<div><strong>Note:</strong>After Reconciliation The Reconciliation Image changes according to Reconciliation Percentage.\
    The Reconiliation Images turns Red when Reconciliation done Between 0 to 35%\
    The Reconiliation Images turns Black when Reconciliation done Between 0 to less than 90%\
    The Reconiliation Images turns Green when Reconciliation Percentage Greater Than and Equal To 90%\
    </div>"\
        "</div>"
    html.write(str(html_view))

def page_tip_odu_profiling(h):
    """
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var html_view : this is used to store the html content which is write on page
    @since : 12 December 2011
    @version :0.0 
    @date : 12 December 2011
    @note : This function is used for diplaying the help of odu Profiling page.Every link help.Every Tab Help.What output display.Every Image description.How Forms works
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    html_view = ""\
        "<div id=\"help_container\">"\
        "<h1>RM/RM18 Profiling</h1>"\
        "<div><strong>RM18/RM</strong> Profiling of (Device). You can edit the profiling of individual device.</div>"\
        "<br/>"\
        "<div><strong><u>Serach Profile</u></strong>At the top there is Ip Address,MAC Address,and Device Type.By All Of that you can select an individual profile.If more than one device is come in search result then you can move to UBR Listing page</div>"\
        "<br/>"\
        "<div><strong><u>Radio Unit</u></strong> On this tab you can manage the channel bandwidth and country code.</div>"\
        "<br/>"\
        "<div><strong><u>UNMP</u></strong> On this tab you can manage the UNMP IP Address and Periodic Stats Timer.</div>"\
        "<br/>"\
        "<div><strong><u>UNMP Resgistration</u></strong> On this tab You can manage the address,contact person,mobile,alternate contact and email</div>"\
        "<br/>"\
        "<div><strong><u>Synchronization</u></strong> On this tab You can manage the Raster Time,Number of slaves,SyncLossThreshold,LeakyBucketTimer,SyncLossTimeOut,SyncTimerAdjust</div>"\
        "<br/>"\
        "<div><strong><u>ACL</u></strong> On this tab you can manage ACL Mode and MAC Addresses</div>"\
        "<br/>"\
        "<div><strong><u>Radio Frequency</u></strong> On this tab you can manage RF Frequency,RF Coding,MAC tx Power,Max Crc Errors,Leaky Bucket timer</div>"\
        "<br/>"\
        "<div><strong><u>Peer MAC</u></strong> On this tab we can manage the Number of slaves and Mac Addresses.</div>"\
        "<br/>"\
        "<div><strong><u>Commit To Flash</u></strong> This is a button on the bottom of Page.It save all your page data on device permanently</div>"\
        "<br/>"\
        "<div><strong><u>Reboot</u></strong> This is a button on the bottom of Page.It Reboots the devive.When you press reboot there is a loading spin on you page and it stops spinning when deviceis reachable again after reboot.If device is not reachable after 100 sec then loading  automatically hides and show you the message</div>"\
        "<br/>"\
        "<div><strong><u>Reconciliation</u></strong> This is a button on the bottom of Page.It save all device data on data storage and show on your page</div>"\
        "<br/>"\
        "<div><strong><u>Site Survey Result</u></strong> This is a button on the bottom of Page.It gives a pop up after runs successfully.It takes time to run.</div>"\
        "<br/>"\
        "<div><strong><u>BW Calculator</u></strong> This is a button on the bottom of Page.It gives a pop up after click on button.In this pop window there is TX Rate,TX Time and TX BW.TX Rate,TX Time are entered by you and bandwidth is calculated according to that</div>"\
        "<br/>"\
        "<div><strong><u>Form Working Description</u></strong> After Click On Save Button Of form.All The values given in form are going to set on the device.If All Values are set then \
    there is a <img src=\"images/done.png\"/> image is display after every Field.And OK button is display instead of save.After click on ok.the form is display with updated values.\
    If values are not set then the <img src=\"images/alert_restart.png\"/> image is display after fields which are not set.if No one field are set then it display after Every field on form .\
    By clicking on retry image after fields ,the value of that field is again going to retry.When retry image is displayed then there are two buttons are also\
    displayed Retry and Cancel button.When Click on retry button all fields are again going to set in which retry image is diplayed.On click on cancel button \
    the form is displayed with the updated values which are set and the retry values are discarded and the old values are displayed in that fileds\
    </div>"\
        "<br/>"\
        "</div>"
    html.write(str(html_view))


def form_box(filter_class, a_class, a_href, a_id, a_text, header_text, data_id, width_size = '375px'):

    tab_str = ""
    for yo in range(0, len(a_href)):
        tab_str += "<a class=\"tab-profile %s\" href=\"%s\" id=\"%s\">%s<span class=\"\"></span></a>" % (a_class[yo], a_href[yo], a_id[yo], a_text[yo])
    str_form = "<li class=\"%s\" data-id=\"%s\" >\
                <div class=\"widget-head\">\
                    %s\
                    <h3>%s</h3>\
                </div>\
                <div class=\"widget-content\" style=\"width:%s\">" % (filter_class, data_id, tab_str, header_text, width_size)
    return str_form

def odu_profiling(h):
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
    global obj_essential
    html = h
    ################### Javascript files declaration ##########################
    # Here we declare all the javascripts file which we usedin this file


    ###########################################################################

    ################### Css files declaration #################################
    # Declare path of all the css file which we used in this file


    ###########################################################################

    ##################### Header Declaration ##################################
    # Define the page header e.g Odu Profiling
    css_list = ['css/demo_table_jui.css', 'css/jquery-ui-1.8.4.custom.css', 'css/ccpl_jquery_combobox.css']
    jss_list = ['js/jquery.dataTables.min.js', 'js/ccpl_jquery_autocomplete.js', 'js/odu_controller.js', 'js/jquery-ui-personalized-1.6rc2.min.js']

    ##############################Variable declaration#########################
    # Declare the host id as an empty string 
    host_id = ""

    #this is used for storing DeviceTypeList e.g "odu16,odu100"
    device_type = ""

    #this is used for storing DeviceListState e.g "enabled"
    device_list_state = ""
    # this is used for storing the ipaddress,macaddres,hostid and configprofileid which is return form the database
    device_list_param = []
    ###########################################################################
    ru_op_state = 1
    ra_op_state = 1
    sync_op_state = 1
    #we get the variable of page through html.var
    host_id = html.var("host_id")
    global host_status_dic
    if html.var("device_type") != None: 
        device_type = html.var("device_type")
    if html.var("device_list_state") != None:
        device_list_state = html.var("device_list_state")    
    if host_id == None:
        host_id = ""
    obj_data = IduGetData()
    device_list_param = get_device_param(host_id)# call the odu_controller function get_device_param returns the tuple.tuple consist ipaddress,macaddress,devicetypeid,config_profile_id
    if device_list_param == [] or device_list_param == None:
        html.write(page_header_search("", "", "RM18,RM,IDU,Access Point,CCU", None, "enabled", "device_type"))#call the function of common_controller , it is used for listing the Devices based on IPaddress,Macaddress,DeviceTy
    else:
        snapin_list = ["reports", "views", "Alarm", "Inventory", "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
        html.new_header("%s %s Configuration" % ("RM18" if device_type == "odu16" else "RM", device_list_param[0][0]), "odu_listing.py", "", css_list, jss_list, snapin_list)

        html.write(page_header_search(device_list_param[0][0], device_list_param[0][1], "RM18,RM,IDU,Access Point,CCU", device_type, device_list_state, "device_type"))
    # if host_id is None or empty then returns that no profiling exist
    # else the forms of that selected profiling diplays on page
    if host_id == "" or host_id == "None":
        val = ""
        html.write("<div id=\"odu16_form_div\" class=\"form-div\">There is no profile selected</div>")
    else:
        obj_get_data = IduGetData()
        if device_type == "odu16":
            ru_data = obj_get_data.common_get_data('SetOdu16RUConfTable', host_id)
            ra_data = obj_get_data.common_get_data('SetOdu16RAConfTable', host_id)
            sync_data = obj_get_data.common_get_data('SetOdu16SyncConfigTable', host_id)
        else:
            ru_data = obj_get_data.common_get_data('Odu100RuConfTable', host_id)
            ra_data = obj_get_data.common_get_data('Odu100RaConfTable', host_id)
            sync_data = obj_get_data.common_get_data('Odu100SyncConfigTable', host_id)
            ru_status = odu100_get_status(host_id, "Odu100RuStatusTable")
            ra_status = odu100_get_status(host_id, "Odu100RaStatusTable", 1)
            sync_status = odu100_get_status(host_id, "Odu100SynchStatusTable", 1)
            if len(ru_status) > 0:
                if ru_status[0].ruoperationalState == None:
                    ru_op_state = 1
                else:
                    ru_op_state = ru_status[0].ruoperationalState
            else:
                ru_op_state = 1

            if len(ra_status) > 0:
                if ra_status[0].raoperationalState == None:
                    ra_op_state = 1
                else:
                    ra_op_state = ra_status[0].raoperationalState
            else:
                ra_op_state = 1

            if len(sync_status) > 0:
                if sync_status[0].syncoperationalState == None:
                    sync_op_state = 1
                else:
                    sync_op_state = sync_status[0].syncoperationalState
            else:
                sync_op_state = 1



        if device_type == "odu16":
            if int(ru_data[0].adminstate) == 0:
                ru_state = 0
                image_ru_title = "RU State Locked"            
            else:
                ru_state = 1
                image_ru_title = "RU State UnLocked"

            if int(ra_data[0].raAdminState) == 0:
                ra_state = 0
                image_ra_title = "RA State Locked"
            else:
                ra_state = 1
                image_ra_title = "RA State Unlocked"            

            if int(sync_data[0].adminStatus) == 0:
                sync_state = 0
                image_sync_title = "SYNC State Locked"
            else:
                sync_state = 1
                image_sync_title = " SYNC State Unlocked"


            html.write("<div id=\"odu16_form_div\" class=\"form-div\" style=\"margin-top: 56px;\">")
            odu_profiling_form(h, host_id)# function call , it is used to make a form of selected profiling
            html.write("</div>")
            html.write("<div class=\"form-div-footer\">\
            <div id=\"adminDiv\" style=\"float: left;margin-left:15px\">\
                <ul class=\"button_group\" style=\" margin:10px 0 0 10px !important;\">\
                    <li>\
                        <a class=\"%s n-reconcile\" id=\"ru.ruConfTable.adminstate\" name=\"ru.ruConfTable.adminstate\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','ru.ruConfTable.adminstate')\">Radio Unit %s</a>\
                    </li>\
                    <li>\
                        <a class=\"%s n-reconcile\" id=\"ru.syncClock.syncConfigTable.adminStatus\" name=\"ru.syncClock.syncConfigTable.adminStatus\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','ru.syncClock.syncConfigTable.adminStatus')\">SYN %s</a>\
                    </li>\
                    <li>\
                        <a class=\"%s n-reconcile\" id=\"ru.ra.raConfTable.raAdminState\" name=\"ru.ra.raConfTable.raAdminState\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','ru.ra.raConfTable.raAdminState')\">Radio Access %s</a>\
                    </li>\
                </ul>\
            </div>\
            <div id=\"operationDiv\" style=\"float:right;margin-right:100px;\">\
                <input type=\"button\" id=\"RU.RUOMOperationsTable.omOperationsReq\" name=\"odu16_commit_to_flash\" value=\"Commit To Flash\" class=\"yo-small yo-button\"/>\
                <input type=\"button\" id=\"odu16_reconcile\" name=\"odu16_reconcile\" value=\"Reconciliation\" class=\"yo-small yo-button\"/>\
                <!--<input type=\"button\" id=\"site_survey_btn\" name=\"site_survey_btn\" value=\"Site Survey Results\" class=\"yo-small yo-button\" onClick=\"siteSurvey();\"/>-->\
            </div>\
            </div>" % ("red" if ru_state == 0 else "green", ru_state, device_list_param[0][2], "Locked" if ru_state == 0 else "Unlocked", \
                     "red" if sync_state == 0 else "green", sync_state, device_list_param[0][2], "Locked" if sync_state == 0 else "Unlocked", \
                     "red" if ra_state == 0 else "green", ra_state, device_list_param[0][2], "Locked" if ra_state == 0 else "Unlocked"))

        else:
            if len(ru_data) > 0:
                if ru_data[0].adminstate == None:                    
                    ru_state = 1
                    image_ru_title = "RU State UnLocked"
                else:
                    if int(ru_data[0].adminstate) == 0:
                        ru_state = 0
                        image_ru_title = "RU State Locked"
                    else:
                        if int(ru_op_state) == 0:
                            ru_state = 0
                            image_ru_title = "RU State UnLocked"
                        else:
                            ru_state = 1
                            image_ru_title = "RU State UnLocked"
            else:
                ru_state = 1
                image_ru_title = "RU State UnLocked"

            if len(ra_data) > 0:
                if ra_data[0].raAdminState == None:
                    ra_state = 1
                    image_ra_title = "RA State Unlocked"

                else:
                    if int(ra_data[0].raAdminState) == 0:
                        ra_state = 0
                        image_ra_title = "RA State Locked"

                    else:
                        if int(ra_op_state) == 0:
                            ra_state = 0
                            image_ra_title = "RA State Unlocked"
                        else:
                            ra_state = 1
                            image_ra_title = "RA State Unlocked"
            else:
                ra_state = 1
                image_ra_title = "RA State Unlocked"

            if len(sync_data) > 0:
                if sync_data[0].adminStatus == None:
                    sync_state = 1
                    image_sync_title = " SYNC State Unlocked"

                else:
                    if int(sync_data[0].adminStatus) == 0:
                        sync_state = 0
                        image_sync_title = "SYNC State Locked"

                    else:
                        if int(sync_op_state) == 0:
                            sync_state = 0
                            image_sync_title = " SYNC State Unlocked"
                        else:
                            sync_state = 1
                            image_sync_title = " SYNC State Unlocked"
            else:
                sync_state = 1
                image_sync_title = " SYNC State Unlocked"



            op_status = obj_essential.get_hoststatus(host_id)
            if op_status == None:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[0]
            elif op_status == 0:
                op_img = "images/host_status0.png"
                op_title = host_status_dic[op_status]
            else:
                op_img = "images/host_status1.png"
                op_title = host_status_dic[op_status]
            html.write("<div id=\"odu16_form_div\" class=\"form-div\" style=\"margin-top: 56px;\"></div>")
            html.write("<div class=\"form-div-footer\">\
                <div id=\"adminDiv\" style=\"float: left;margin-left:15px\">\
                    <ul class=\"button_group\" style=\"margin:10px 0 0 10px !important;\">\
                        <li>\
                            <a class=\"%s n-reconcile\" id=\"ru.ruConfTable.adminstate\" name=\"ru.ruConfTable.adminstate\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','ru.ruConfTable.adminstate')\">Radio Unit %s</a>\
                        </li>\
                        <li>\
                            <a class=\"%s n-reconcile\" id=\"ru.syncClock.syncConfigTable.adminStatus\" name=\"ru.syncClock.syncConfigTable.adminStatus\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','ru.syncClock.syncConfigTable.adminStatus')\">SYN %s</a>\
                        </li>\
                        <li>\
                            <a class=\"%s n-reconcile\" id=\"ru.ra.raConfTable.raAdminState\" name=\"ru.ra.raConfTable.raAdminState\" title=\"%s\" state=\"%s\" onclick=\"adminStateCheck(event,this,'%s','ru.ra.raConfTable.raAdminState')\">Radio Access %s</a>\
                        </li>\
                    </ul>\
                </div>\
                <div id=\"operation_status\" style=\"float: left; margin-top: 12px; margin-left: 15px;vertical-align: middle;\">\
                    <span>Operation Status </span>&nbsp;&nbsp;&nbsp;<img class=\"n-reconcile\" id=\"operation_status\" name=\"operation_status\" src=\"%s\" title=\"%s\" style=\"width:14px;height:14px;vertical-align: middle;\"class=\"imgbutton n-reconcile\"/></center>&nbsp;&nbsp;\
                </div>\
                <div id=\"operationDiv\" style=\"float:right;margin-right:10px;\">\
                    <input type=\"button\" id=\"RU.RUOMOperationsTable.omOperationsReq\" name=\"odu16_commit_to_flash\" value=\"Commit To Flash\" class=\"yo-small yo-button\" host_id=\"%s\"/>\
                    <input type=\"button\" id=\"odu_reboot\" name=\"odu_reboot\" value=\"Reboot\" class=\"yo-small yo-button\"/>\
                    <input type=\"button\" id=\"odu16_reconcile\" name=\"odu16_reconcile\" value=\"Reconciliation\"  class=\"yo-small yo-button\"/>\
                    <input type=\"button\" id=\"site_survey_btn\" name=\"site_survey_btn\" value=\"Site Survey Results\" class=\"yo-small yo-button\" onClick=\"siteSurvey();\" />\
                    <input type=\"button\" id=\"bw_calculator_form\" name=\"bw_calculator_form\" value=\"BW Calculator\" class=\"yo-small yo-button\" />\
\
                </div>\
            </div>" % ("red" if ru_state == 0 else "green", image_ru_title, ru_state, device_list_param[0][2], "Locked" if ru_state == 0 else "Unlocked", \
                     "red" if sync_state == 0 else "green", image_sync_title, sync_state, device_list_param[0][2], "Locked" if sync_state == 0 else "Unlocked", \
                     "red" if ra_state == 0 else "green", image_ra_title, ra_state, device_list_param[0][2], "Locked" if ra_state == 0 else "Unlocked", op_img, op_title, host_id))
        html.write("<input type=\"hidden\" name=\"device_type\" id=\"device_type\" value=%s>" % (device_type))
            #odu100_profiling_form(h)# function call , it is used to make a form of selected profiling


    html.new_footer()    
def odu_profiling_form(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var host_id : this is used to store the Host Id which is come from the page
    @device_list_param : this is used to store all the details of device 
    @tab_str : this is used to store the form string  
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to write the forms of odu16 on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """

    if host_id == None:
        host_id = html.var("host_id")
    device_list_param = get_device_param(host_id)
    if device_list_param[0][3] == None or device_list_param[0][3] == "":
        html.write("No Configuration Profile Exist")

    else:
# This makes the filter buttons and a commit to flash button and writes on page  
        tab_str = ''
        tab_str += "<div class=\"yo-tabs\" id=\"config_tabs\" style=\"display:block\">\
                        <ul>\
                            <li><a class=\"active\" href=\"#content_1\">Radio Unit</a></li>\
                            <!--<li><a href=\"#content_3\">UNMP Registration</a></li>-->\
                            <li><a href=\"#content_8\">LLC Configuration</a></li>\
                            <li><a href=\"#content_4\">Synchronization</a></li>\
                            <li><a href=\"#content_5\">ACL</a></li>\
                            <li><a href=\"#content_6\">Radio Frequency</a></li>\
                            <li><a href=\"#content_7\">Peer MAC</a></li>\
                            <li><a href=\"#content_2\">UNMP</a></li>\
                        </ul>\
                        <div id=\"content_1\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\" id=\'hh\'>\
                            %s\
                            </div>\
                            <div id=\"result_ru_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_8\" class=\"tab-content form-div\" style=\"display:block;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                            <div id=\"result_llc_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_2\" class=\"tab-content form-div\" style=\"display:none;margin-bottom:0;margin-top:26px\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                            <div id=\"result_omc_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_3\" class=\"tab-content form-div\" style=\"display:none;margin-bottom:0;margin-top:26px\">\
                            %s\
                            <div id=\"result_sys_omc_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_4\" class=\"tab-content form-div\" style=\"display:none;margin-bottom:0;margin-top:26px\">\
                            %s\
                            <div id=\"result_syn_omc_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_5\" class=\"tab-content form-div\" style=\"display:none;margin-bottom:0;margin-top:26px\">\
                            %s\
                            <div id=\"result_acl_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_6\" class=\"tab-content form-div\" style=\"display:none;margin-bottom:0;margin-top:26px\">\
                            %s\
                            <div id=\"tdd_mac_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <div id=\"content_7\" class=\"tab-content form-div\" style=\"display:none;margin-bottom:0;margin-top:26px\">\
                            %s\
                            <div id=\"peer_mac_config\" style=\"margin-top:10px\">\
                            </div>\
                        </div>\
                        <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                        <input type=\"hidden\" name=\"mac_address\" value=\"%s\"/>\
                    </div>" % (RU_Configuration(h, host_id), Llc_Configuration(h, host_id), Omc_Config(h, host_id), SysOmc_Registration_Configuration(h, host_id), \
                             Syn_Omc_Registration_Configuration(h, host_id), Acl_Configuration(h, host_id), Tdd_Mac_Configuration(h, host_id), Peer_mac(h, host_id), \
                             device_list_param[0][0], device_list_param[0][1])
        html.write(tab_str)


def odu100_profiling_form(host_id, selected_device):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var host_id : this is used to store the Host Id which is come from the page
    @device_list_param : this is used to store all the details of device 
    @tab_str : this is used to store the form string
    @var odu_configuration_object : this is used to store the object of class OduConfiguration  
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to write the forms of odu100 on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    firmware_result=get_firmware_version(host_id)
    if firmware_result['success']==0:
        firmware_version=firmware_result['output']
    else:
        firmware_version='7.2.20'
    
    device_list_param = get_device_param(host_id)
    if device_list_param[0][3] == None or device_list_param[0][3] == "":
        html.write("No Configuration Profile Exist")
    else:
        odu_configuration_object = OduConfiguration()
        tab_str = ''
        tab_str += "<div class=\"yo-tabs\" id=\"config_tabs\" style=\"display:block\">\
                        <ul>\
                            <li><a class=\"active\" href=\"#content_1\">Radio Unit</a></li>\
                            <li><a href=\"#content_3\">LLC Configuration</a></li>\
                            <li><a href=\"#content_4\">Synchronization</a></li>\
                            <li><a href=\"#content_5\">ACL</a></li>\
                            <li><a href=\"#content_6\">Radio Access</a></li>\
                            <li><a href=\"#content_7\">Peer MAC</a></li>\
                            <li><a href=\"#content_8\">Preferred Channel List</a></li>\
                            <li><a href=\"#content_2\">UNMP</a></li>\
                            <li %s><a href=\"#content_9\">Packet Filter</a></li>\
                        </ul>\
                        <div id=\"content_1\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_2\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            <div style=\"position: relative;margin-bottom:0px\" class=\"form-div\">\
                            %s\
                            </div>\
                        </div>\
                        <div id=\"content_3\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            %s\
                        </div>\
                        <div id=\"content_4\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            %s\
                        </div>\
                        <div id=\"content_5\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            %s\
                        </div>\
                        <div id=\"content_6\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            %s\
                        </div>\
                        <div id=\"content_7\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            %s\
                        </div>\
                        <div id=\"content_8\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            %s\
                        </div>\
                            %s\
                        <input type=\"hidden\" name=\"ip_address\" value=\"%s\"/>\
                        <input type=\"hidden\" name=\"mac_address\" value=\"%s\"/>\
                    </div>" % ( "style=\"display:none;\"" if firmware_version == '7.2.20' else "",\
                             odu_configuration_object.odu100_ru_configuration(host_id, selected_device), \
                             odu_configuration_object.odu100_omc_configuration(host_id, selected_device), \
                             odu_configuration_object.llc_config(host_id, selected_device), \
                             odu_configuration_object.odu100_sync_configuration(host_id, selected_device), \
                             odu_configuration_object.odu100_acl_configuration(host_id, selected_device), \
                             odu_configuration_object.odu100_ra_configuration(host_id, selected_device), \
                             odu_configuration_object.odu100_peer_configuration(host_id, selected_device), \
                             odu_configuration_object.odu100_channel_configuration(host_id, selected_device, 0), \
                             "" if firmware_version == '7.2.20' else odu_configuration_object.odu100_packet_filter(host_id, selected_device),\
                             device_list_param[0][0], device_list_param[0][1])
        html.write(tab_str)


def RU_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var ru_config_get : this is used to store the ru configuration form details as a list
    @var ru_config_odu16_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the Radio Unit configuration forms of odu16 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function ru_config_table_get(host_id) ##################################
    #ru_config_get Values------------------------------------------------------
    ru_config_get, ru_config_odu16_profile_id = ru_config_table_get(host_id)#This is the odu_controller function.It returns the ruconfiguration form parameters and  onfig profile id
    #--------------------------------------------------------------------------

#this is string in which form is define
    str_form += "<form action=\"ru_configuration.py\" method=\"get\" id=\"ru_configuration_form\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\">Channel Bandwidth **</label>\
                                <Select id=\"RU.RUConfTable.channelBandwidth\" name=\"RU.RUConfTable.channelBandwidth\" fact=\".1.3.6.1.4.1.26149.2.2.1.1.7.1\" val=\"Integer\" value=\"%s\" tablename=\"SetOdu16RUConfTable\" field=\"channel_bandwidth\">Mhz\
                                    <option value=\"0\">5</option>\
                                    <option value=\"1\">10</option>\
                                    <option value=\"2\">20</option>\
                                </Select>\
                                <input name=\"channelBandwidth\" type=\"hidden\" value=\"%s\"/>\
                                <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                 <label class=\"lbl lbl-big\">Sync Source</label>\
                                    <Select id=\"RU.RUConfTable.synchSource\" disabled=\"disabled\" name=\"RU.RUConfTable.synchSource\" fact=\".1.3.6.1.4.1.26149.2.2.1.1.8.1\" val=\"Integer\" tablename=\"SetOdu16RUConfTable\" field=\"sysnch_source\">\
                                        <option value=\"0\" disabled=\"disabled\">Internal Clock</option>\
                                        <option value=\"1\" disabled=\"disabled\">Radio</option>\
                                        <option value=\"2\" disabled=\"disabled\">Radio</option>\
                                    </Select>\
                                    <input name=\"synchSource\" disabled=\"disabled\" type=\"hidden\" value=\"\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\">Country Code **</label>\
                                    <Select id=\"RU.RUConfTable.countryCode\" name=\"RU.RUConfTable.countryCode\" fact=\".1.3.6.1.4.1.26149.2.2.1.1.9.1\" val=\"Unsigned\" value=\"%s\" tablename=\"SetOdu16RUConfTable\" field=\"country_code\">\
                                        <option value=\"356\">India</option>\
                                        <option value=\"208\">Denmark</option>\
                                        <option value=\"752\">Sweden</option>\
                                    </Select>\
                                    <input name=\"countryCode\" type=\"hidden\" value=\"%s\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                    <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/><br/><br/>\
                                    <span  style=\"font-size: 11px;\" class=\"note\">** Change for all these values will cause reboot</span>\
                                    \
                            </div>\
                        </form>" % ("" if ru_config_get[0][0] == None else ru_config_get[0][0], "" if ru_config_get[0][0] == None else ru_config_get[0][0], "" if host_id == None else host_id\
                                   , "" if ru_config_get[0][2] == None else ru_config_get[0][2], "" if ru_config_get[0][2] == None else ru_config_get[0][2])
    return str_form


def RU_Cancel_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var ru_config_get : this is used to store the ru configuration form details as a list
    @var ru_config_odu16_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the Radio Unit configuration forms of odu16 device and call on cancel buuton
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function ru_config_table_get(host_id) ##################################
    #ru_config_get Values------------------------------------------------------
    ru_config_get, ru_config_odu16_profile_id = ru_config_table_get(host_id)#This is the odu_controller function.It returns the ruconfiguration form parameters and  onfig profile id
    #--------------------------------------------------------------------------

#this is string in which form is define
    str_form += "<form action=\"ru_configuration.py\" method=\"get\" id=\"ru_configuration_form\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\">Channel Bandwidth</label>\
                                <Select id=\"RU.RUConfTable.channelBandwidth\" name=\"RU.RUConfTable.channelBandwidth\" fact=\".1.3.6.1.4.1.26149.2.2.1.1.7.1\" val=\"Integer\" value=\"%s\" tablename=\"SetOdu16RUConfTable\" field=\"channel_bandwidth\">\
                                    <option value=\"0\">5 Mhz</option>\
                                    <option value=\"1\">10Mhz</option>\
                                    <option value=\"2\">20Mhz</option>\
                                </Select>\
                                <label class=\"lbl lbl-big\" style=\"font-size:9px;float:none;display:inline\">change of this will cause a reboot</label>\
                                <input name=\"channelBandwidth\" type=\"hidden\" value=\"%s\"/>\
                                <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                 <label class=\"lbl lbl-big\">Sync Source</label>\
                                    <Select id=\"RU.RUConfTable.synchSource\" disabled=\"disabled\" name=\"RU.RUConfTable.synchSource\" fact=\".1.3.6.1.4.1.26149.2.2.1.1.8.1\" val=\"Integer\" tablename=\"SetOdu16RUConfTable\" field=\"sysnch_source\">\
                                        <option value=\"0\" disabled=\"disabled\">Internal Clock</option>\
                                        <option value=\"1\" disabled=\"disabled\">Radio</option>\
                                        <option value=\"2\" disabled=\"disabled\">Radio</option>\
                                    </Select>\
                                    <input name=\"synchSource\" disabled=\"disabled\" type=\"hidden\" value=\"\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\">Country Code</label>\
                                    <Select id=\"RU.RUConfTable.countryCode\" name=\"RU.RUConfTable.countryCode\" fact=\".1.3.6.1.4.1.26149.2.2.1.1.9.1\" val=\"Unsigned\" value=\"%s\" tablename=\"SetOdu16RUConfTable\" field=\"country_code\">\
                                        <option value=\"356\">India</option>\
                                        <option value=\"208\">Denmark</option>\
                                        <option value=\"752\">Sweden</option>\
                                    </Select>\
                                    <label class=\"lbl lbl-big\" style=\"font-size:9px;float:none;display:inline\">change of this will cause a reboot</label>\
                                    <input name=\"countryCode\" type=\"hidden\" value=\"%s\"/>\
                            </div>\
                            <div class=\"row-elem\">\
                                    <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                    <span  style=\"font-size: 11px;\" class=\"note\">** Change for all these values will cause reboot</span>\
                                    \
                            </div>\
                        </form>" % ("" if ru_config_get[0][0] == None else ru_config_get[0][0], "" if ru_config_get[0][0] == None else ru_config_get[0][0], "" if host_id == None else host_id\
                                   , "" if ru_config_get[0][2] == None else ru_config_get[0][2], "" if ru_config_get[0][2] == None else ru_config_get[0][2])
    html.write(str(str_form))



### Author - Anuj Samariya
### This function is displaying form of RU Date Time 
### h -  is used for request
### host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
### it displays the forms on page 
##def RU_Date_Time(h,host_id):
##    """
##    @author : Anuj Samariya 
##    @param h : html Class Object
##    @param host_id : in this the host id is stored for access of particular host
##    @var html : this is html Class Object defined globally 
##    @var str_form : this is used to store the html form string 
##    @var ru_date_time : this is used to store the ru date time configuration form details as a list
##    @var ru_config_profile_id : this is used to store the configuration id for odu16 device 
##    @tab_str : this is used to store the form string
##    @since : 20 August 2011
##    @version :0.0 
##    @date : 20 Augugst 2011
##    @note : this function is used to make the Radio Unit Date Time configuration forms of odu16 device
##    @organisation : Codescape Consultants Pvt. Ltd.
##    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    @return : retrun the form string in html
##    @rtype : string
##    """
##    global html
##    html=h
##    str_form=""
##    ############### Values get from the database by calling the function ru_date_time_table_get(host_id) ##################################
##    #host_id = html.var("host_id") 
##    # RU Date Time Configuration ---------------------------------------------------
##    ru_date_time=[]
##    ru_date_time,ru_config_profile_id=ru_date_time_table_get(host_id)#This is the odu_controller function.It returns the ru date time form parameters and  onfig profile id
##    #--------------------------------------------------------------------------
##    str_form+="<form action=\"ru_date_time_table.py\" method=\"get\" id=\"odu_ru_date_time_form\">\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Year:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Year\" id=\"RU.RUDateTimeTable.Year\" fact=\".1.3.6.1.4.1.26149.2.2.2.1.2.1\" val=\"Integer\" field=\"year\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Month:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Month\" id=\"RU.RUDateTimeTable.Month\" fact=\".1.3.6.1.4.1.26149.2.2.2.1.3.1\" val=\"Integer\" field=\"month\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Day:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Day\" id=\"RU.RUDateTimeTable.Day\" fact=\".1.3.6.1.4.1.26149.2.2.2.1.4.1\" val=\"Integer\" field=\"day\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Hour:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Hour\" id=\"RU.RUDateTimeTable.Hour\" fact=\"1.3.6.1.4.1.26149.2.2.2.1.5.1\"/ val=\"Integer\" field=\"hour\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Minute:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Minutes\" id=\"RU.RUDateTimeTable.Minutes\" fact=\"1.3.6.1.4.1.26149.2.2.2.1.6.1\" val=\"Integer\" field=\"min\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Second:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Seconds\" id=\"RU.RUDateTimeTable.Seconds\" fact=\"1.3.6.1.4.1.26149.2.2.2.1.7.1\" val=\"Integer\" field=\"sec\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
##                    </div>\
##                </form>" %("" if ru_date_time[0][0]==None else ru_date_time[0][0],"" if host_id==None else host_id,\
##           "" if ru_date_time[0][1]==None else ru_date_time[0][1],"" if ru_date_time[0][2]==None else ru_date_time[0][2],"" if ru_date_time[0][3]==None else ru_date_time[0][3],\
##            "" if ru_date_time[0][4]==None else ru_date_time[0][4],"" if ru_date_time[0][5]==None else ru_date_time[0][5])
##    return str_form
##
##
### Author - Anuj Samariya
### This function is displaying form of RU Date Time 
### h -  is used for request
### host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
### it displays the forms on page 
##def RU_Cancel_Date_Time(h,host_id):
##    """
##    @author : Anuj Samariya 
##    @param h : html Class Object
##    @param host_id : in this the host id is stored for access of particular host
##    @var html : this is html Class Object defined globally 
##    @var str_form : this is used to store the html form string 
##    @var ru_date_time : this is used to store the ru date time configuration form details as a list
##    @var ru_config_profile_id : this is used to store the configuration id for odu16 device 
##    @tab_str : this is used to store the form string
##    @since : 20 August 2011
##    @version :0.0 
##    @date : 20 Augugst 2011
##    @note : this function is used to make the Radio Unit Date Time configuration forms of odu16 device on cancel button and write on page
##    @organisation : Codescape Consultants Pvt. Ltd.
##    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    @return : retrun the form string in html
##    @rtype : string
##    """
##    global html
##    html=h
##    str_form=""
##    ############### Values get from the database by calling the function ru_date_time_table_get(host_id) ##################################
##    #host_id = html.var("host_id") 
##    # RU Date Time Configuration ---------------------------------------------------
##    ru_date_time=[]
##    ru_date_time,ru_config_profile_id=ru_date_time_table_get(host_id)#This is the odu_controller function.It returns the ru date time form parameters and  onfig profile id
##    #--------------------------------------------------------------------------
##    str_form+="<form action=\"ru_date_time_table.py\" method=\"get\" id=\"odu_ru_date_time_form\">\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Year:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Year\" id=\"RU.RUDateTimeTable.Year\" fact=\".1.3.6.1.4.1.26149.2.2.2.1.2.1\" val=\"Integer\" field=\"year\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Month:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Month\" id=\"RU.RUDateTimeTable.Month\" fact=\".1.3.6.1.4.1.26149.2.2.2.1.3.1\" val=\"Integer\" field=\"month\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Day:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Day\" id=\"RU.RUDateTimeTable.Day\" fact=\".1.3.6.1.4.1.26149.2.2.2.1.4.1\" val=\"Integer\" field=\"day\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Hour:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Hour\" id=\"RU.RUDateTimeTable.Hour\" fact=\"1.3.6.1.4.1.26149.2.2.2.1.5.1\"/ val=\"Integer\" field=\"hour\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Minute:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Minutes\" id=\"RU.RUDateTimeTable.Minutes\" fact=\"1.3.6.1.4.1.26149.2.2.2.1.6.1\" val=\"Integer\" field=\"min\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <label class=\"lbl lbl-big\">Second:</label>\
##                        <input type=\"text\" name=\"RU.RUDateTimeTable.Seconds\" id=\"RU.RUDateTimeTable.Seconds\" fact=\"1.3.6.1.4.1.26149.2.2.2.1.7.1\" val=\"Integer\" field=\"sec\" value=\"%s\" tablename=\"SetOdu16RUDateTimeTable\"/>\
##                    </div>\
##                    <div class=\"row-elem\">\
##                        <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
##                    </div>\
##                </form>" %("" if ru_date_time[0][0]==None else ru_date_time[0][0],"" if host_id==None else host_id,\
##           "" if ru_date_time[0][1]==None else ru_date_time[0][1],"" if ru_date_time[0][2]==None else ru_date_time[0][2],"" if ru_date_time[0][3]==None else ru_date_time[0][3],\
##            "" if ru_date_time[0][4]==None else ru_date_time[0][4],"" if ru_date_time[0][5]==None else ru_date_time[0][5])
##    html.write(str(str_form))


def Omc_Config(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var omc_config : this is used to store the configuration form details as a list
    @var omc_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the UNMP form of odu16 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    #host_id = html.var("host_id")
    str_form = ""
############### Values get from the database by calling the function omc_conf_table_get(host_id) ##################################
#omc get values-------------------------------------------------------------
    omc_config = []
    omc_config, omc_profile_id = omc_conf_table_get(host_id)#This is the odu_controller function.It returns the omcconfiguration form parameters and  onfig profile id
#--------------------------------------------------------------------------
    str_form += "\
                <form action=\"omc_config_detail.py\" method=\"get\" id=\"omc_configuration_form\">\
                    <div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\">UNMP IP</label>\
                        <input type=\"text\" name=\"RU.OMCConfTable.omcIPAddress\" id=\"RU.OMCConfTable.omcIPAddress\" fact=\".1.3.6.1.4.1.26149.2.2.7.1.2.1\" val=\"ip\" field=\"omc_ip_address\" value=\"%s\" tablename=\"SetOdu16OmcConfTable\"/> \
                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                    </div>\
                    <div class=\"row-elem\" style=\"display:none\">\
                        <label class=\"lbl lbl-big\">Periodic Statistics Timer</label>\
                        <input type=\"text\" name=\"RU.OMCConfTable.periodicStatisticsTimer\" id=\"RU.OMCConfTable.periodicStatisticsTimer\" fact=\".1.3.6.1.4.1.26149.2.2.7.1.3.1\" val=\"Integer\" field=\"periodic_stats_timer\" value=\"%s\" tablename=\"SetOdu16OmcConfTable\"/>\
                    </div>\
                    <div class=\"row-elem\">\
                            <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/><br/><br/>\
                            <span  style=\"font-size: 11px;\" class=\"note\">**UNMP IP - Configuring UNMP IP is important for capturing and monitoring the device alarms</span>\
                    </div>\
                </form>\
           " % ("" if omc_config[0].omc_ip_address == None else omc_config[0].omc_ip_address, "" if host_id == None else host_id, "" if omc_config[0].periodic_stats_timer == None else omc_config[0].periodic_stats_timer)
    return str(str_form)

##--------------------..............................its jugad...........................---------------------------
def omc_config_form(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var omc_config : this is used to store the configuration form details as a list
    @var omc_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the omc configuration forms of odu16 device on cancel button and write on page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    #host_id = html.var("host_id")
    str_form = ""
#omc get values-------------------------------------------------------------
    omc_config = []
    omc_config, omc_profile_id = omc_conf_table_get(host_id)
#--------------------------------------------------------------------------
    str_form += "\
                    <form action=\"omc_config_detail.py\" method=\"get\" id=\"omc_configuration_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">UNMP IP</label>\
                            <input type=\"text\" name=\"RU.OMCConfTable.omcIPAddress\" id=\"RU.OMCConfTable.omcIPAddress\" fact=\".1.3.6.1.4.1.26149.2.2.7.1.2.1\" val=\"ip\" field=\"omc_ip_address\" value=\"%s\" tablename=\"SetOdu16OmcConfTable\"/> \
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\" style=\"display:none\">\
                            <label class=\"lbl lbl-big\">Periodic Statistics Timer</label>\
                            <input type=\"text\" name=\"RU.OMCConfTable.periodicStatisticsTimer\" id=\"RU.OMCConfTable.periodicStatisticsTimer\" fact=\".1.3.6.1.4.1.26149.2.2.7.1.3.1\" val=\"Integer\" field=\"periodic_stats_timer\" value=\"%s\" tablename=\"SetOdu16OmcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                            <span  style=\"font-size: 11px;\" class=\"note\">**UNMP IP - Configuring UNMP IP is important for capturing and monitoring the device alarms</span>\
                        </div>\
                    </form>" % ("" if omc_config[0].omc_ip_address == None else omc_config[0].omc_ip_address, "" if host_id == None else host_id, "" if omc_config[0].periodic_stats_timer == None else omc_config[0].periodic_stats_timer)
    html.write(str(str_form))
##-------------------------------------------------------------------------------------------------------------------------


def SysOmc_Registration_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var sys_omc_registration_table : this is used to store the configuration form details as a list
    @var sys_omc_config_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the UNMP Registration forms of odu16 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    #host_id = html.var("host_id")
    str_form = ""
############### Values get from the database by calling the function sys_omc_registration_table_get(host_id) ##################################
    #sys_omc_registration_table----------------------------------------------------
    sys_omc_registration_table = []
    sys_omc_registration_table, sys_omc_config_profile_id = sys_omc_registration_table_get(host_id)#This is the odu_controller function.It returns the sys registration form parameters and  onfig profile id
    #--------------------------------------------------------------------------
    str_form += "\
                    <form action=\"omc_registration_configuration.py\" method=\"get\" id=\"omc_registration_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Address</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.2.1\" maxlength=\"20\" val=\"string\" field=\"sys_omc_register_contact_addr\" value=\"%s\" tablename=\"SetOdu16SysOmcRegistrationTable\"/>\
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Person</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.3.1\" val=\"string\" value=\"%s\" field=\"sys_omc_register_contact_person\" maxlength=\"20\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Number</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.4.1\" field=\"sys_omc_register_contact_mobile\"  val=\"string\" value=\"%s\" maxlength=\"10\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Alternate Contact Number</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont\" id=\"RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.5.1\" val=\"string\" value=\"%s\" maxlength=\"20\" field=\"sys_omc_register_alternate_contact\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Email</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail\" field=\"sys_omc_register_contact_email\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.6.1\" val=\"string\" value=\"%s\" maxlength=\"20\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if sys_omc_registration_table[0].sys_omc_register_contact_addr == None else sys_omc_registration_table[0].sys_omc_register_contact_addr, "" if host_id == None else host_id, \
                              "" if sys_omc_registration_table[0].sys_omc_register_contact_person == None else sys_omc_registration_table[0].sys_omc_register_contact_person, \
                              "" if sys_omc_registration_table[0].sys_omc_register_contact_mobile == None else sys_omc_registration_table[0].sys_omc_register_contact_mobile, \
                              "" if sys_omc_registration_table[0].sys_omc_register_alternate_contact == None else sys_omc_registration_table[0].sys_omc_register_alternate_contact, \
                              "" if sys_omc_registration_table[0].sys_omc_register_contact_email == None else sys_omc_registration_table[0].sys_omc_register_contact_email)
    return str_form


######################################## ITs jugad##############################################
def sys_registration_form(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var sys_omc_registration_table : this is used to store the configuration form details as a list
    @var sys_omc_config_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the UNMP Registration forms of odu16 device on cancel button and write on page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function sys_omc_registration_table_get(host_id) ##################################
    #sys_omc_registration_table----------------------------------------------------
    sys_omc_registration_table = []
    sys_omc_registration_table, sys_omc_config_profile_id = sys_omc_registration_table_get(host_id)
    str_form += "<form action=\"omc_registration_configuration.py\" method=\"get\" id=\"omc_registration_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Address</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.2.1\" maxlength=\"20\" val=\"string\" field=\"sys_omc_register_contact_addr\" value=\"%s\" tablename=\"SetOdu16SysOmcRegistrationTable\"/>\
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Person</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.3.1\" val=\"string\" value=\"%s\" field=\"sys_omc_register_contact_person\" maxlength=\"20\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Number</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.4.1\" field=\"sys_omc_register_contact_mobile\"  val=\"string\" value=\"%s\" maxlength=\"10\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Alternate Contact Number</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont\" id=\"RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.5.1\" val=\"string\" value=\"%s\" maxlength=\"20\" field=\"sys_omc_register_alternate_contact\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Email</label>\
                            <input type=\"text\" name=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail\" id=\"RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail\" field=\"sys_omc_register_contact_email\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.6.1\" val=\"string\" value=\"%s\" maxlength=\"20\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if sys_omc_registration_table[0].sys_omc_register_contact_addr == None else sys_omc_registration_table[0].sys_omc_register_contact_addr, "" if host_id == None else host_id, \
                              "" if sys_omc_registration_table[0].sys_omc_register_contact_person == None else sys_omc_registration_table[0].sys_omc_register_contact_person, \
                              "" if sys_omc_registration_table[0].sys_omc_register_contact_mobile == None else sys_omc_registration_table[0].sys_omc_register_contact_mobile, \
                              "" if sys_omc_registration_table[0].sys_omc_register_alternate_contact == None else sys_omc_registration_table[0].sys_omc_register_alternate_contact, \
                              "" if sys_omc_registration_table[0].sys_omc_register_contact_email == None else sys_omc_registration_table[0].sys_omc_register_contact_email)
    html.write(str(str_form))

################################################################################################

# Author - Anuj Samariya
# This function is displaying form of SYN OMC Registration Configuration 
# h -  is used for request
# host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
# it displays the forms on page 
def Syn_Omc_Registration_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var sync_config_table : this is used to store the configuration form details as a list
    @var sync_config_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version : 0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the synchronization forms of odu16 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function sync_config_table_get(host_id) ##################################
    # syn_configuration get Method-------------------------------------------------
    sync_config_table, sync_config_profile_id = sync_config_table_get(host_id)#This is the odu_controller function.It returns the synomcregistration form parameters and  onfig profile id
    #--------------------------------------------------------------------------
    str_form += "<form action=\"syn_configuration.py\" method=\"get\" id=\"syn_configuration_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Raster Time</label>\
                            <Select id=\"RU.SyncClock.SyncConfigTable.rasterTime\" name=\"RU.SyncClock.SyncConfigTable.rasterTime\" fact=\".1.3.6.1.4.1.26149.2.2.13.4.1.5.1\" val=\"Integer\" tablename=\"SetOdu16SyncConfigTable\" field=\"raster_time\">\
                                <option value=\"0\">0</option>\
                                <option value=\"2\">2</option>\
                                <option value=\"4\">4</option>\
                                <option value=\"8\">8</option>\
                            </Select>\
                            <input name=\"raster_time\" type=\"hidden\" value=\"%s\"/>\
                           <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Number of Slaves</label>\
                            <Select id=\"RU.SyncClock.SyncConfigTable.numSlaves\" name=\"RU.SyncClock.SyncConfigTable.numSlaves\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.5.1\" val=\"Integer\" tablename=\"SetOdu16SyncConfigTable\" field=\"num_slaves\">\
                                <option value=\"1\">1 Timeslot(T1/T2)</option>\
                                <option value=\"2\">2 Timeslot(T2)</option>\
                                <option value=\"3\">3 Timeslot(T2)</option>\
                                <option value=\"4\">4 Timeslot(T2)</option>\
                                <option value=\"5\">5 Timeslot(T2)</option>\
                                <option value=\"6\">6 Timeslot(T2)</option>\
                                <option value=\"7\">7 Timeslot(T2)</option>\
                                <option value=\"8\">8 Timeslot(T2)</option>\
                            </Select>\
                            <input name=\"slaves\" type=\"hidden\" value=\"%s\"/>\
                            <input id=\"database_slaves\" name=\"database_slaves\" type=\"hidden\" value=\"%s\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">SyncLossThreshold</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.syncLossThreshold\" id=\"RU.SyncClock.SyncConfigTable.syncLossThreshold\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.6.1\" val=\"Integer\" value=\"%s\" field=\"sync_loss_threshold\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.leakyBucketTimer\" id=\"RU.SyncClock.SyncConfigTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.7.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Sync Loss Time Out</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.syncLostTimeout\" id=\"RU.SyncClock.SyncConfigTable.syncLostTimeout\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.8.1\" val=\"Integer\" value=\"%s\" field=\"sync_lost_timeout\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Sync Timer Adjust</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.timerAdjust\" id=\"RU.SyncClock.SyncConfigTable.timerAdjust\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.9.1\" val=\"Integer\" value=\"%s\" field=\"sync_config_time_adjust\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if sync_config_table[0][0] == None else sync_config_table[0][0], "" if host_id == None else host_id, \
                               "" if sync_config_table[0][1] == None else sync_config_table[0][1], "" if sync_config_table[0][1] == None else sync_config_table[0][1], \
                               "" if sync_config_table[0][2] == None else sync_config_table[0][2], "" if sync_config_table[0][3] == None else sync_config_table[0][3], \
                               "" if sync_config_table[0][4] == None else sync_config_table[0][4], \
                               "" if sync_config_table[0][5] == None else sync_config_table[0][5])
    return str_form


def Syn_Cancel_Omc_Registration_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var sync_config_table : this is used to store the configuration form details as a list
    @var sync_config_profile_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the Synchronization forms of odu16 device on cancel button and write on page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function sync_config_table_get(host_id) ##################################
    # syn_configuration get Method-------------------------------------------------
    sync_config_table, sync_config_profile_id = sync_config_table_get(host_id)#This is the odu_controller function.It returns the synomcregistration form parameters and  onfig profile id
    #--------------------------------------------------------------------------
    str_form += "<form action=\"syn_configuration.py\" method=\"get\" id=\"syn_configuration_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Raster Time</label>\
                            <Select id=\"RU.SyncClock.SyncConfigTable.rasterTime\" name=\"RU.SyncClock.SyncConfigTable.rasterTime\" fact=\".1.3.6.1.4.1.26149.2.2.13.4.1.5.1\" val=\"Integer\" tablename=\"SetOdu16SyncConfigTable\" field=\"raster_time\">\
                                <option value=\"0\">0</option>\
                                <option value=\"2\">2</option>\
                                <option value=\"4\">4</option>\
                                <option value=\"8\">8</option>\
                            </Select>\
                            <input name=\"raster_time\" type=\"hidden\" value=\"%s\"/>\
                           <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Number of Slaves</label>\
                            <Select id=\"RU.SyncClock.SyncConfigTable.numSlaves\" name=\"RU.SyncClock.SyncConfigTable.numSlaves\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.5.1\" val=\"Integer\" tablename=\"SetOdu16SyncConfigTable\" field=\"num_slaves\">\
                                <option value=\"1\">1 Timeslot(T1/T2)</option>\
                                <option value=\"2\">2 Timeslot(T2)</option>\
                                <option value=\"3\">3 Timeslot(T2)</option>\
                                <option value=\"4\">4 Timeslot(T2)</option>\
                                <option value=\"5\">5 Timeslot(T2)</option>\
                                <option value=\"6\">6 Timeslot(T2)</option>\
                                <option value=\"7\">7 Timeslot(T2)</option>\
                                <option value=\"8\">8 Timeslot(T2)</option>\
                            </Select>\
                            <input name=\"slaves\" type=\"hidden\" value=\"%s\"/>\
                            <input id=\"database_slaves\" name=\"database_slaves\" type=\"hidden\" value=\"%s\">\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">SyncLossThreshold</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.syncLossThreshold\" id=\"RU.SyncClock.SyncConfigTable.syncLossThreshold\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.6.1\" val=\"Integer\" value=\"%s\" field=\"sync_loss_threshold\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.leakyBucketTimer\" id=\"RU.SyncClock.SyncConfigTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.7.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Sync Loss Time Out</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.syncLostTimeout\" id=\"RU.SyncClock.SyncConfigTable.syncLostTimeout\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.8.1\" val=\"Integer\" value=\"%s\" field=\"sync_lost_timeout\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Sync Timer Adjust</label>\
                            <input type=\"text\" name=\"RU.SyncClock.SyncConfigTable.timerAdjust\" id=\"RU.SyncClock.SyncConfigTable.timerAdjust\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.9.1\" val=\"Integer\" value=\"%s\" field=\"sync_config_time_adjust\" tablename=\"SetOdu16SyncConfigTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if sync_config_table[0][0] == None else sync_config_table[0][0], "" if host_id == None else host_id, \
                               "" if sync_config_table[0][1] == None else sync_config_table[0][1], "" if sync_config_table[0][1] == None else sync_config_table[0][1], \
                               "" if sync_config_table[0][2] == None else sync_config_table[0][2], "" if sync_config_table[0][3] == None else sync_config_table[0][3], \
                               "" if sync_config_table[0][4] == None else sync_config_table[0][4], \
                               "" if sync_config_table[0][5] == None else sync_config_table[0][5])
    html.write(str(str_form))


# Author - Anuj Samariya
# This function is displaying form of LLC Configuration 
# h -  is used for request
# host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
# it displays the forms on page 
def Llc_Configuration(h, host_id):
    """
    Author - Anuj Samariya
    This function is displaying form of LLC Configuration 
    h -  is used for request
    host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
    it displays the forms on page
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function ra_llc_conf_table_get(host_id) ##################################
# RaLlc Configuration get Method-----------------------------------------------
    ra_llc_config = []
    ra_llc_config, ra_llc_config_id = ra_llc_conf_table_get(host_id)#This is the odu_controller function.It returns the llcconfiguration form parameters and  onfig profile id
#--------------------------------------------------------------------------
    str_form += "<form action=\"ra_llc_configuration.py\" method=\"get\" id=\"ra_llc_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">ARQ Mode</label>\
                            <Select id=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" name=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1\" val=\"Integer\" value=\"%s\" field=\"llc_arq_enable\" tablename=\"SetOdu16RALlcConfTable\">\
                                <option value=\"0\">Disabled(0)</option>\
                                <option value=\"1\">Enabled(1)</option>\
                            </Select>\
                        <input name=\"llcArqEnable\" type=\"hidden\" value=\"%s\"/>\
                        \
                        \
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">ArqWin(Retransmit Window Size)</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" id=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1\" val=\"Integer\" value=\"%s\" field=\"arq_win\" tablename=\"SetOdu16RALlcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Frame Loss Threshold</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_threshold \" tablename=\"SetOdu16RALlcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Leaky Bucket Timer</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" id=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer_val\" tablename=\"SetOdu16RALlcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl\">Frame Loss Time Out</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_timeout\" tablename=\"SetOdu16RALlcConfTable\"/>\
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if ra_llc_config[0][0] == None else ra_llc_config[0][0], \
                               "" if ra_llc_config[0][0] == None else ra_llc_config[0][0], "" if ra_llc_config[0][1] == None else ra_llc_config[0][1], \
                               "" if ra_llc_config[0][2] == None else ra_llc_config[0][2], "" if ra_llc_config[0][3] == None else ra_llc_config[0][3], \
                               "" if ra_llc_config[0][4] == None else ra_llc_config[0][4], "" if host_id == None else host_id)
    return str_form

# Author - Anuj Samariya
# This function is displaying form of LLC Configuration 
# h -  is used for request
# host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
# it displays the forms on page 
def Llc_Cancel_Configuration(h, host_id):
    """
    Author - Anuj Samariya
    This function is displaying form of LLC Configuration 
    h -  is used for request
    host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
    it displays the forms on page
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function ra_llc_conf_table_get(host_id) ##################################
# RaLlc Configuration get Method-----------------------------------------------
    ra_llc_config = []
    ra_llc_config, ra_llc_config_id = ra_llc_conf_table_get(host_id)#This is the odu_controller function.It returns the llcconfiguration form parameters and  onfig profile id
#--------------------------------------------------------------------------
    str_form += "<form action=\"ra_llc_configuration.py\" method=\"get\" id=\"ra_llc_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">ARQ Mode</label>\
                            <Select id=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" name=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1\" val=\"Integer\" value=\"%s\" field=\"llc_arq_enable\" tablename=\"SetOdu16RALlcConfTable\">\
                                <option value=\"0\">Disabled(0)</option>\
                                <option value=\"1\">Enabled(1)</option>\
                            </Select>\
                        <input name=\"llcArqEnable\" type=\"hidden\" value=\"%s\"/>\
                        \
                        \
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">ArqWin(Retransmit Window Size)</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" id=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1\" val=\"Integer\" value=\"%s\" field=\"arq_win\" tablename=\"SetOdu16RALlcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Frame Loss Threshold</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_threshold \" tablename=\"SetOdu16RALlcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" id=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer_val\" tablename=\"SetOdu16RALlcConfTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Frame Loss Time Out</label>\
                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_timeout\" tablename=\"SetOdu16RALlcConfTable\"/>\
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if ra_llc_config[0][0] == None else ra_llc_config[0][0], \
                               "" if ra_llc_config[0][0] == None else ra_llc_config[0][0], "" if ra_llc_config[0][1] == None else ra_llc_config[0][1], \
                               "" if ra_llc_config[0][2] == None else ra_llc_config[0][2], "" if ra_llc_config[0][3] == None else ra_llc_config[0][3], \
                               "" if ra_llc_config[0][4] == None else ra_llc_config[0][3], "" if host_id == None else host_id)
    html.write(str(str_form))

def Acl_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var str_mac : this is used to store the html of mac address and its labels
    @var ru_acl_config : this is used to store the configuration form details as a list
    @var ra_acl_config_profile_id : this is used to store the configuration id for odu16 device 
    @var ra_conf :  this is used to store the ACL configuration form details as a list
    @var count : this is used to count the total number of acl rows
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the ACL forms of odu16 device 
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function ra_acl_config_table_get(host_id) ##################################
#ra_conf_table_get():------------------------------------------------------
    #ra_conf_table,ra_conf_profile_id = ra_conf_table_get(host_id)#This is the odu_controller function.It returns the aclconfiguration form parameters and  onfig profile id
#--------------------------------------------------------------------------

#ru acl configuration get--------------------------------------------------
    ra_acl_config = []
    ra_acl_config, ra_acl_config_profile_id, ra_conf = ra_acl_config_table_get(host_id)
#--------------------------------------------------------------------------
#########################################################################################################################################
    global mac
    #indexmac = ra_acl_config[0][1]
    strmac = ""
    ra_acl_val = ""
    count = len(ra_acl_config)
    if len(ra_acl_config) == 0:
        count = 10

    for i in range(0, 10 if len(ra_acl_config) == 0 else len(ra_acl_config)):
        if i < 10:


            strmac += "<div class=\"row-elem\" id=\"acl_row_element_%s\">\
                   <label class=\"lbl lbl-big\">MAC Address %s</label>\
                        <input type=\"text\" name=\"RU.RA.1.RAACLConfig.%s.macAddress\" id=\"RU.RA.1.RAACLConfig.%s.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s\" val=\"string\" value=\'%s\' field=\"mac_address\" tablename=\"SetOdu16RAAclConfigTable\" index=\"%s\"/>\
                </div>" % (i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1, ("" if len(ra_acl_config) == 0 else "" if ra_acl_config[i][0] == None else ra_acl_config[i][0].replace('"', '').replace(" ", "")), i + 1)
        else:

            strmac += "<div class=\"row-elem\" id=\"acl_row_element_%s\">\
                   <label class=\"lbl lbl-big\">MAC Address %s</label>\
                        <input type=\"text\" name=\"RU.RA.1.RAACLConfig.%s.macAddress\" id=\"RU.RA.1.RAACLConfig.%s.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s\" val=\"string\" value=\"%s\" field=\"mac_address\" tablename=\"SetOdu16RAAclConfigTable\" index=\"%s\"/>\
                        <img src=\"images/delete16.png\" alt=\"Delete\" title=\"Delete\" class=\"imgbutton\" onclick=\"deleteAclConfigMacAddress(%s)\" />\
                </div>" % (ra_acl_config[i][1], ra_acl_config[i][1], ra_acl_config[i][1], ra_acl_config[i][1], i + 1, (ra_acl_config[i][0].replace('"', '').replace(" ", "") if ra_acl_config[i][0] != None else ""), i + 1, ra_acl_config[i][1])

    str_form += "<form action=\"acl_config.py\" method=\"get\" id=\"acl_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">ACL Mode</label>\
                            <Select id=\"RU.RA.1.RAConfTable.aclMode\" name=\"RU.RA.1.RAConfTable.aclMode\" fact=\".1.3.6.1.4.1.26149.2.2.13.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"acl_mode\" tablename=\"SetOdu16RAConfTable\">\
                                <option value=\"0\">Disabled</option>\
                                <option value=\"1\">Accept</option>\
                                <option value=\"2\">Deny</option>\
                            </Select>\
                           \
                            <input name=\"aclmode\" type=\"hidden\" value=\"%s\"/>\
                            <input id=\"acl_count\" name=\"acl_count\" type=\"hidden\" value=\"%s\"/>\
                            \
                        </div>\
                        %s\
                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        <div class=\"row-elem\">\
                                <a href=\"#\"/ id=\"aclAddMore\">Add More</a>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" value=\"ACL Reconcilation\" class=\"yo-small yo-button\" id=\"reconcileAcl\"/>\
                        </div>\
                        \
                    </form>" % ("" if ra_conf[0][0] == None else ra_conf[0][0], "" if ra_conf[0][0] == None else ra_conf[0][0], "" if count == None else count, "" if strmac == None else strmac, "" if host_id == None else host_id)
    return str_form


def Acl_Cancel_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var str_mac : this is used to store the html of mac address and its labels
    @var ra_acl_config : this is used to store the configuration form details as a list
    @var ra_acl_config_profile_id : this is used to store the configuration id for odu16 device 
    @var ra_conf :  this is used to store the ACL form details as a list
    @var count : this is used to count the total number of acl rows
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the ACL forms of odu16 device on cancel button and write on page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    str_form = ""
############### Values get from the database by calling the function ra_acl_config_table_get(host_id) ##################################
#ra_conf_table_get():------------------------------------------------------
    #ra_conf_table,ra_conf_profile_id = ra_conf_table_get(host_id)#This is the odu_controller function.It returns the aclconfiguration form parameters and  onfig profile id
#--------------------------------------------------------------------------

#ru acl configuration get--------------------------------------------------
    ra_acl_config = []
    ra_acl_config, ra_acl_config_profile_id, ra_conf = ra_acl_config_table_get(host_id)
#--------------------------------------------------------------------------
#########################################################################################################################################
    global mac
    #indexmac = ra_acl_config[0][1]
    strmac = ""
    ra_acl_val = ""
    count = len(ra_acl_config)
    if len(ra_acl_config) == 0:
        count = 10

    for i in range(0, 10 if len(ra_acl_config) == 0 else len(ra_acl_config)):
        if i < 10:
            strmac += "<div class=\"row-elem\" id=\"acl_row_element_%s\">\
                   <label class=\"lbl lbl-big\">MAC Address %s</label>\
                        <input type=\"text\" name=\"RU.RA.1.RAACLConfig.%s.macAddress\" id=\"RU.RA.1.RAACLConfig.%s.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s\" val=\"string\" value=\'%s\' field=\"mac_address\" tablename=\"SetOdu16RAAclConfigTable\" index=\"%s\"/>\
                </div>" % (i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1 if len(ra_acl_config) == 0 else "" if ra_acl_config[i][1] == None else ra_acl_config[i][1], \
                         i + 1, ("" if len(ra_acl_config) == 0 else "" if ra_acl_config[i][0] == None else ra_acl_config[i][0].replace('"', '')), i + 1)
        else:

            strmac += "<div class=\"row-elem\" id=\"acl_row_element_%s\">\
                   <label class=\"lbl lbl-big\">Mac Address %s</label>\
                        <input type=\"text\" name=\"RU.RA.1.RAACLConfig.%s.macAddress\" id=\"RU.RA.1.RAACLConfig.%s.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.5.1.2.1.%s\" val=\"string\" value=\"%s\" field=\"mac_address\" tablename=\"SetOdu16RAAclConfigTable\" index=\"%s\"/>\
                        <img src=\"images/delete16.png\" alt=\"Delete\" title=\"Delete\" class=\"imgbutton\" onclick=\"deleteAclConfigMacAddress(%s)\" />\
                </div>" % (ra_acl_config[i][1], ra_acl_config[i][1], ra_acl_config[i][1], ra_acl_config[i][1], i + 1, (ra_acl_config[i][0].replace('"', '') if ra_acl_config[i][0] != None else ""), i + 1, ra_acl_config[i][1])

    str_form += "<form action=\"acl_config.py\" method=\"get\" id=\"acl_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">ACL Mode</label>\
                            <Select id=\"RU.RA.1.RAConfTable.aclMode\" name=\"RU.RA.1.RAConfTable.aclMode\" fact=\".1.3.6.1.4.1.26149.2.2.13.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"acl_mode\" tablename=\"SetOdu16RAConfTable\">\
                                <option value=\"0\">Disabled</option>\
                                <option value=\"1\">Accept</option>\
                                <option value=\"2\">Deny</option>\
                            </Select>\
                           \
                            <input name=\"aclmode\" type=\"hidden\" value=\"%s\"/>\
                            <input id=\"acl_count\" name=\"acl_count\" type=\"hidden\" value=\"%s\"/>\
                            \
                        </div>\
                        %s\
                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        <div class=\"row-elem\">\
                                <a href=\"#\"/ id=\"aclAddMore\">Add More</a>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                <input type=\"button\" value=\"ACL Reconcilation\" class=\"yo-small yo-button\" id=\"reconcileAcl\"/>\
                                \
                        </div>\
                        \
                    </form>" % ("" if ra_conf[0][0] == None else ra_conf[0][0], "" if ra_conf[0][0] == None else ra_conf[0][0], "" if count == None else count, "" if strmac == None else strmac, "" if host_id == None else host_id)
    html.write(str(str_form))



### Author - Anuj Samariya
### This function is displaying form of LLC Configuration 
### h -  is used for request
### host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
### it displays the forms on page 
##def Llc_Configuration(h,host_id):
##    """
##    @requires:     
##    @return: 
##    @rtype: 
##    @author:Anuj Samariya 
##    @since: 
##    @version: 
##    @date: 
##    @note: 
##    @organisation: Codescape Consultants Pvt. Ltd.
##    @copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    """
##    global html
##    html=h
##    str_form=""
################# Values get from the database by calling the function ra_llc_conf_table_get(host_id) ##################################
### RaLlc Configuration get Method-----------------------------------------------
##    ra_llc_config=[]
##    ra_llc_config,ra_llc_config_id=ra_llc_conf_table_get(host_id)#This is the odu_controller function.It returns the llcconfiguration form parameters and  onfig profile id
###--------------------------------------------------------------------------
##    str_form+="<form action=\"ra_llc_configuration.py\" method=\"get\" id=\"ra_llc_config_form\">\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">ARQ Mode</label>\
##                            <Select id=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" name=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1\" val=\"Integer\" value=\"%s\" field=\"llc_arq_enable\" tablename=\"SetOdu16RALlcConfTable\">\
##                                <option value=\"0\">Disabled(0)</option>\
##                                <option value=\"1\">Enabled(1)</option>\
##                            </Select>\
##                        <input name=\"llcArqEnable\" type=\"hidden\" value=\"%s\"/>\
##                        \
##                        \
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">ArqWin(Retransmit Window Size)</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" id=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1\" val=\"Integer\" value=\"%s\" field=\"arq_win\" tablename=\"SetOdu16RALlcConfTable\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">Frame Loss Threshold</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_threshold \" tablename=\"SetOdu16RALlcConfTable\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" id=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer_val\" tablename=\"SetOdu16RALlcConfTable\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">Frame Loss Time Out</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_timeout\" tablename=\"SetOdu16RALlcConfTable\"/>\
##                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
##                                \
##                        </div>\
##                    </form>" %("" if ra_llc_config[0][0]==None else ra_llc_config[0][0],\
##            "" if ra_llc_config[0][0]==None else ra_llc_config[0][0],"" if ra_llc_config[0][1]==None else ra_llc_config[0][1],\
##            "" if ra_llc_config[0][2]== None else ra_llc_config[0][2],"" if ra_llc_config[0][3]==None else ra_llc_config[0][3],\
##            "" if ra_llc_config[0][4]==None else ra_llc_config[0][3],"" if host_id==None else host_id)
##    return str_form
##
##
### Author - Anuj Samariya
### This function is displaying form of LLC Configuration 
### h -  is used for request
### host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
### it displays the forms on page 
##def Llc_Cancel_Configuration(h,host_id):
##    """
##    @requires:     
##    @return: 
##    @rtype: 
##    @author:Anuj Samariya 
##    @since: 
##    @version: 
##    @date: 
##    @note: 
##    @organisation: Codescape Consultants Pvt. Ltd.
##    @copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    """
##    global html
##    html=h
##    str_form=""
################# Values get from the database by calling the function ra_llc_conf_table_get(host_id) ##################################
### RaLlc Configuration get Method-----------------------------------------------
##    ra_llc_config=[]
##    ra_llc_config,ra_llc_config_id=ra_llc_conf_table_get(host_id)#This is the odu_controller function.It returns the llcconfiguration form parameters and  onfig profile id
###--------------------------------------------------------------------------
##    str_form+="<form action=\"ra_llc_configuration.py\" method=\"get\" id=\"ra_llc_config_form\">\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">ARQ Mode</label>\
##                            <Select id=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" name=\"RU.RA.1.LLC.RALLCConfTable.llcArqEnable\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1\" val=\"Integer\" value=\"%s\" field=\"llc_arq_enable\" tablename=\"SetOdu16RALlcConfTable\">\
##                                <option value=\"0\">Disabled(0)</option>\
##                                <option value=\"1\">Enabled(1)</option>\
##                            </Select>\
##                        <input name=\"llcArqEnable\" type=\"hidden\" value=\"%s\"/>\
##                        \
##                        \
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">ArqWin(Retransmit Window Size)</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" id=\"RU.RA.1.LLC.RALLCConfTable.arqWin\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.2.1\" val=\"Integer\" value=\"%s\" field=\"arq_win\" tablename=\"SetOdu16RALlcConfTable\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">Frame Loss Threshold</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossThreshold\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.3.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_threshold \" tablename=\"SetOdu16RALlcConfTable\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" id=\"RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer_val\" tablename=\"SetOdu16RALlcConfTable\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                            <label class=\"lbl lbl-big\">Frame Loss Time Out</label>\
##                            <input type=\"text\" name=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" id=\"RU.RA.1.LLC.RALLCConfTable.frameLossTimeout\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.5.1\" val=\"Integer\" value=\"%s\" field=\"frame_loss_timeout\" tablename=\"SetOdu16RALlcConfTable\"/>\
##                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
##                        </div>\
##                        <div class=\"row-elem\">\
##                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
##                                \
##                        </div>\
##                    </form>" %("" if ra_llc_config[0][0]==None else ra_llc_config[0][0],\
##            "" if ra_llc_config[0][0]==None else ra_llc_config[0][0],"" if ra_llc_config[0][1]==None else ra_llc_config[0][1],\
##            "" if ra_llc_config[0][2]== None else ra_llc_config[0][2],"" if ra_llc_config[0][3]==None else ra_llc_config[0][3],\
##            "" if ra_llc_config[0][4]==None else ra_llc_config[0][3],"" if host_id==None else host_id)
##    html.write(str(str_form))

# Author - Anuj Samariya
# This function is displaying form of TDD MAC Configuration 
# h -  is used for request
# host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
# it displays the forms on page 
def Tdd_Mac_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var ra_tdd_mac_config : this is used to store the configuration form details as a list
    @var ra_tdd_mac_config_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the Radio Frequency form of  odu16 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
############### Values get from the database by calling the function ra_tdd_mac_config_get(host_id) ##################################
    str_form = ""
#RaTdd Mac Configuration get Method--------------------------------------------
    ra_tdd_mac_config, ra_tdd_mac_config_id = ra_tdd_mac_config_get(host_id)#This is the odu_controller function.It returns the tddmacconfiguration form parameters and  onfig profile id
#------------------------------------------------------------------------------

    str_form += "<form action=\"tdd_mac_config.py\" method=\"get\" id=\"tdd_mac_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TDD MAC RF</label>\
                            <Select id=\"ru.np.ra.1.tddmac.rfChannel\" name=\"ru.np.ra.1.tddmac.rfChannel\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1\" val=\"Integer\" value=\"%s\" field=\"rf_channel_frequency\" tablename=\"SetOdu16RATddMacConfig\">\
                                <option value=\"5180\">5180 Mhz</option>\
                                <option value=\"5190\">5190 Mhz</option>\
                                <option value=\"5200\">5200 Mhz</option>\
                                <option value=\"5210\">5210 Mhz</option>\
                                <option value=\"5220\">5220 Mhz</option>\
                                <option value=\"5230\">5230 Mhz</option>\
                                <option value=\"5240\">5240 Mhz</option>\
                                <option value=\"5260\">5260 Mhz</option>\
                                <option value=\"5270\">5270 Mhz</option>\
                                <option value=\"5280\">5280 Mhz</option>\
                                <option value=\"5290\">5290 Mhz</option>\
                                <option value=\"5300\">5300 Mhz</option>\
                                <option value=\"5310\">5310 Mhz</option>\
                                <option value=\"5320\">5320 Mhz</option>\
                                <option value=\"5745\">5745 Mhz</option>\
                                <option value=\"5755\">5755 Mhz</option>\
                                <option value=\"5765\">5765 Mhz</option>\
                                <option value=\"5775\">5775 Mhz</option>\
                                <option value=\"5785\">5785 Mhz</option>\
                                <option value=\"5795\">5795 Mhz</option>\
                                <option value=\"5805\">5805 Mhz</option>\
                                <option value=\"5815\">5815 Mhz</option>\
                                <option value=\"5825\">5825 Mhz</option>\
                                <option value=\"5835\">5835 Mhz</option>\
                                <option value=\"5845\">5845 Mhz</option>\
                                <option value=\"5855\">5855 Mhz</option>\
                                <option value=\"5865\">5865 Mhz</option>\
                            </Select>\
                            <input type=\"hidden\" value=\"%s\" id=\"rfchannel\" name=\"rfchannel\" /> \
                           \
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TDD MAC RF Coding</label>\
                            <Select id=\"ru.np.ra.1.tddmac.rfCoding\" name=\"ru.np.ra.1.tddmac.rfCoding\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1\" val=\"Integer\" value=\"%s\" field=\"rfcoding\" tablename=\"SetOdu16RATddMacConfig\">\
                                <option value=\"1\">16 QAM</option>\
                                <option value=\"2\">64 QAM</option>\
                            </Select>\
                            \
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TDD MAC TX Power</label>\
                            \
                            <input type=\"text\" name=\"ru.np.ra.1.tddmac.txPower\" id=\"ru.np.ra.1.tddmac.txPower\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"tx_power\" tablename=\"SetOdu16RATddMacConfig\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Pass Phrase</label>\
                            <input type=\"text\" name=\"RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase\" id=\"RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1\" val=\"Integer\" value=\"%s\" field=\"pass_phrase\" tablename=\"SetOdu16RATddMacConfig\" />\
                        </div>\
                        \
                        \
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Max CRC Errors</label>\
                            <input type=\"text\" name=\"RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors\" id=\"RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1\" val=\"Integer\" value=\"%s\" field=\"max_crc_errors\" tablename=\"SetOdu16RATddMacConfig\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
                            <input type=\"text\" name=\"RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer\" id=\"RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer_value \" tablename=\"SetOdu16RATddMacConfig\" />\
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if ra_tdd_mac_config[0][0] == None else ra_tdd_mac_config[0][0], "" if ra_tdd_mac_config[0][0] == None else ra_tdd_mac_config[0][0], \
                               "" if ra_tdd_mac_config[0][2] == None else ra_tdd_mac_config[0][2], "" if ra_tdd_mac_config[0][3] == None else ra_tdd_mac_config[0][3], \
                               "" if ra_tdd_mac_config[0][1] == None else ra_tdd_mac_config[0][1], "" if ra_tdd_mac_config[0][4] == None else ra_tdd_mac_config[0][4], \
                               "" if ra_tdd_mac_config[0][5] == None else ra_tdd_mac_config[0][5], "" if host_id == None else host_id)
    return str_form


def Tdd_Mac_Cancel_Configuration(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var ra_tdd_mac_config : this is used to store the configuration form details as a list
    @var ra_tdd_mac_config_id : this is used to store the configuration id for odu16 device 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the Radio Frequency form of odu16 device on cancel button and write on page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
############### Values get from the database by calling the function ra_tdd_mac_config_get(host_id) ##################################
    str_form = ""
#RaTdd Mac Configuration get Method--------------------------------------------
    ra_tdd_mac_config, ra_tdd_mac_config_id = ra_tdd_mac_config_get(host_id)#This is the odu_controller function.It returns the tddmacconfiguration form parameters and  onfig profile id
#------------------------------------------------------------------------------

    str_form += "<form action=\"tdd_mac_config.py\" method=\"get\" id=\"tdd_mac_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TDD1 MAC RF Frequency</label>\
                            <Select id=\"ru.np.ra.1.tddmac.rfChannel\" name=\"ru.np.ra.1.tddmac.rfChannel\" fact=\".1.3.6.1.4.1.26149.2.2.13.6.1.1.1.1\" val=\"Integer\" value=\"%s\" field=\"rf_channel_frequency\" tablename=\"SetOdu16RATddMacConfig\">\
                                <option value=\"5180\">5180 Mhz</option>\
                                <option value=\"5190\">5190 Mhz</option>\
                                <option value=\"5200\">5200 Mhz</option>\
                                <option value=\"5210\">5210 Mhz</option>\
                                <option value=\"5220\">5220 Mhz</option>\
                                <option value=\"5230\">5230 Mhz</option>\
                                <option value=\"5240\">5240 Mhz</option>\
                                <option value=\"5260\">5260 Mhz</option>\
                                <option value=\"5270\">5270 Mhz</option>\
                                <option value=\"5280\">5280 Mhz</option>\
                                <option value=\"5290\">5290 Mhz</option>\
                                <option value=\"5300\">5300 Mhz</option>\
                                <option value=\"5310\">5310 Mhz</option>\
                                <option value=\"5320\">5320 Mhz</option>\
                                <option value=\"5745\">5745 Mhz</option>\
                                <option value=\"5755\">5755 Mhz</option>\
                                <option value=\"5765\">5765 Mhz</option>\
                                <option value=\"5775\">5775 Mhz</option>\
                                <option value=\"5785\">5785 Mhz</option>\
                                <option value=\"5795\">5795 Mhz</option>\
                                <option value=\"5805\">5805 Mhz</option>\
                                <option value=\"5815\">5815 Mhz</option>\
                                <option value=\"5825\">5825 Mhz</option>\
                                <option value=\"5835\">5835 Mhz</option>\
                                <option value=\"5845\">5845 Mhz</option>\
                                <option value=\"5855\">5855 Mhz</option>\
                                <option value=\"5865\">5865 Mhz</option>\
                            </Select>\
                            <input type=\"hidden\" value=\"%s\" id=\"rfchannel\" name=\"rfchannel\" /> \
                           \
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Pass phrase (RW_LO:RA1)</label>\
                            <input type=\"text\" name=\"RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase\" id=\"RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.2.1\" val=\"Integer\" value=\"%s\" field=\"pass_phrase\" tablename=\"SetOdu16RATddMacConfig\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TDD 1 MAC RF Coding</label>\
                            <Select id=\"ru.np.ra.1.tddmac.rfCoding\" name=\"ru.np.ra.1.tddmac.rfCoding\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.3.1\" val=\"Integer\" value=\"%s\" field=\"rfcoding\" tablename=\"SetOdu16RATddMacConfig\">\
                                <option value=\"1\">16 QAM</option>\
                                <option value=\"2\">64 QAM</option>\
                            </Select>\
                            \
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TDD 1 MAC TX Power</label>\
                            \
                            <input type=\"text\" name=\"ru.np.ra.1.tddmac.txPower\" id=\"ru.np.ra.1.tddmac.txPower\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.4.1\" val=\"Integer\" value=\"%s\" field=\"tx_power\" tablename=\"SetOdu16RATddMacConfig\"/>\
                        </div>\
                        \
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Max CRC Errors</label>\
                            <input type=\"text\" name=\"RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors\" id=\"RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.6.1\" val=\"Integer\" value=\"%s\" field=\"max_crc_errors\" tablename=\"SetOdu16RATddMacConfig\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Leaky Bucket Timer</label>\
                            <input type=\"text\" name=\"RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer\" id=\"RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer\" fact=\".1.3.6.1.4.1.26149.2.2.13.7.1.1.7.1\" val=\"Integer\" value=\"%s\" field=\"leaky_bucket_timer_value \" tablename=\"SetOdu16RATddMacConfig\" />\
                            <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                                <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                                \
                        </div>\
                    </form>" % ("" if ra_tdd_mac_config[0][0] == None else ra_tdd_mac_config[0][0], "" if ra_tdd_mac_config[0][0] == None else ra_tdd_mac_config[0][0], \
                               "" if ra_tdd_mac_config[0][1] == None else ra_tdd_mac_config[0][1], "" if ra_tdd_mac_config[0][2] == None else ra_tdd_mac_config[0][2], \
                               "" if ra_tdd_mac_config[0][3] == None else ra_tdd_mac_config[0][3], "" if ra_tdd_mac_config[0][4] == None else ra_tdd_mac_config[0][4], \
                               "" if ra_tdd_mac_config[0][5] == None else ra_tdd_mac_config[0][5], "" if host_id == None else host_id)
    html.write(str(str_form))


def Peer_mac(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var peer_config_table : this is used to store the configuration form details as a list
    @var peer_config_table_id : this is used to store the configuration id for odu16 device 
    @var sync_config_table : this is used to store the synchronization configuration form details as a list
    @var sync_config_table_id : this is used to store the Synchronization configuration id for odu16 device
    @var peermac : this is used to store the total mac address in the form
    @var peer_count : this is used to store the length of peer mac come from database
    @var strpeermac : this is used to store the html of peer mac and ite labels 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the form Peer Mac of odu16 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
############### Values get from the database by calling the function peer_config_table_get(host_id) ##################################
    str_form = ""
#peer_config_table_get--------------------------------------------------------
    peer_config_table = []
    peer_config_table, peer_config_profile_id = peer_config_table_get(host_id)#This is the odu_controller function.It returns the peermacconfiguration form parameters and config profile id
    # syn_configuration get Method-------------------------------------------------
    sync_config_table, sync_config_profile_id = sync_config_table_get(host_id)#This is the odu_controller function.It returns the synconfiguration form parameters and  onfig profile id
#------------------------------------------------------------------------------
    peermac = 8
    peer_count = len(peer_config_table)
    strpeermac = ""
    peer_val = ""
    for i in range(peermac):
        if peer_count > 0:
            strpeermac += "<div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\">Timeslot %s MAC Address</label>\
                            <input type=\"text\" name=\"ru.np.ra.1.peer.%s.config.macAddress\" id=\"ru.np.ra.1.peer.%s.config.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s\" val=\"string\" value=\"%s\" field=\"peer_mac_address\" tablename=\"SetOdu16PeerConfigTable\" index=\"%s\"/>\
                    </div>" % (i + 1, i + 1, i + 1, i + 1, "" if peer_config_table[i][0] == None else peer_config_table[i][0].replace('"', ''), i + 1)
            peer_count = peer_count - 1
        else:
            strpeermac += "<div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\">Timeslot %s Mac Address</label>\
                            <input type=\"text\" name=\"ru.np.ra.1.peer.%s.config.macAddress\" id=\"ru.np.ra.1.peer.%s.config.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s\" val=\"string\" value=\"%s\" field=\"peer_mac_address\" tablename=\"SetOdu16PeerConfigTable\" index=\"%s\"/>\
                    </div>" % (i + 1, i + 1, i + 1, i + 1, peer_val, i + 1)
#------------------------------------------------------------------------------
    str_form += "<form action=\"peer_config.py\" method=\"get\" id=\"peer_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Number of Slaves</label>\
                            <Select id=\"RU.SyncClock.SyncConfigTable.numSlaves\" name=\"RU.SyncClock.SyncConfigTable.numSlaves\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.5.1\" val=\"Integer\" value=\"%s\" field=\"num_slaves\" tablename=\"SetOdu16SyncConfigTable\" >\
                                <option value=\"1\">1 Timeslot(T1/T2)</option>\
                                <option value=\"2\">2 Timeslot(T2)</option>\
                                <option value=\"3\">3 Timeslot(T2)</option>\
                                <option value=\"4\">4 Timeslot(T2)</option>\
                                <option value=\"5\">5 Timeslot(T2)</option>\
                                <option value=\"6\">6 Timeslot(T2)</option>\
                                <option value=\"7\">7 Timeslot(T2)</option>\
                                <option value=\"8\">8 Timeslot(T2)</option>\
                            </Select>\
                            <input name=\"slaves\" type=\"hidden\" value=\"%s\"/>\
                            \
                        </div>\
                        %s\
                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                            \
                        </div></form>" % ("" if sync_config_table[0][1] == None else sync_config_table[0][1], \
                                         "" if sync_config_table[0][1] == None else sync_config_table[0][1], "" if strpeermac == None else strpeermac, "" if host_id == None else host_id)
    return str_form



def Peer_mac_Cancel(h, host_id):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @param host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var str_form : this is used to store the html form string 
    @var peer_config_table : this is used to store the configuration form details as a list
    @var peer_config_table_id : this is used to store the configuration id for odu16 device 
    @var sync_config_table : this is used to store the synchronization configuration form details as a list
    @var sync_config_table_id : this is used to store the Synchronization configuration id for odu16 device
    @var peermac : this is used to store the total mac address in the form
    @var peer_count : this is used to store the length of peer mac come from database
    @var strpeermac : this is used to store the html of peer mac and ite labels 
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to make the form Peer Mac of odu16 device on cancel button and write on page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """

    global html
    html = h
############### Values get from the database by calling the function peer_config_table_get(host_id) ##################################
    str_form = ""
#peer_config_table_get--------------------------------------------------------
    peer_config_table = []
    peer_config_table, peer_config_profile_id = peer_config_table_get(host_id)#This is the odu_controller function.It returns the peermacconfiguration form parameters and config profile id
    # syn_configuration get Method-------------------------------------------------
    sync_config_table, sync_config_profile_id = sync_config_table_get(host_id)#This is the odu_controller function.It returns the synconfiguration form parameters and  onfig profile id
#------------------------------------------------------------------------------
    peermac = 8
    peer_count = len(peer_config_table)
    strpeermac = ""
    peer_val = ""
    for i in range(peermac):
        if peer_count > 0:
            strpeermac += "<div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\">Timeslot %s MAC Address</label>\
                            <input type=\"text\" name=\"ru.np.ra.1.peer.%s.config.macAddress\" id=\"ru.np.ra.1.peer.%s.config.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s\" val=\"string\" value=\"%s\" field=\"peer_mac_address\" tablename=\"SetOdu16PeerConfigTable\" index=\"%s\"/>\
                    </div>" % (i + 1, i + 1, i + 1, i + 1, "" if peer_config_table[i][0] == None else peer_config_table[i][0].replace('"', ''), i + 1)
            peer_count = peer_count - 1
        else:
            strpeermac += "<div class=\"row-elem\">\
                        <label class=\"lbl lbl-big\">Timeslot %s Mac Address</label>\
                            <input type=\"text\" name=\"ru.np.ra.1.peer.%s.config.macAddress\" id=\"ru.np.ra.1.peer.%s.config.macAddress\" fact=\".1.3.6.1.4.1.26149.2.2.13.9.1.1.2.1.%s\" val=\"string\" value=\"%s\" field=\"peer_mac_address\" tablename=\"SetOdu16PeerConfigTable\" index=\"%s\"/>\
                    </div>" % (i + 1, i + 1, i + 1, i + 1, peer_val, i + 1)
#------------------------------------------------------------------------------
    str_form += "<form action=\"peer_config.py\" method=\"get\" id=\"peer_config_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Number of Slaves</label>\
                            <Select id=\"RU.SyncClock.SyncConfigTable.numSlaves\" name=\"RU.SyncClock.SyncConfigTable.numSlaves\" fact=\".1.3.6.1.4.1.26149.2.2.11.1.1.5.1\" val=\"Integer\" value=\"%s\" field=\"num_slaves\" tablename=\"SetOdu16SyncConfigTable\" >\
                                <option value=\"1\">1 Timeslot(T1/T2)</option>\
                                <option value=\"2\">2 Timeslot(T2)</option>\
                                <option value=\"3\">3 Timeslot(T2)</option>\
                                <option value=\"4\">4 Timeslot(T2)</option>\
                                <option value=\"5\">5 Timeslot(T2)</option>\
                                <option value=\"6\">6 Timeslot(T2)</option>\
                                <option value=\"7\">7 Timeslot(T2)</option>\
                                <option value=\"8\">8 Timeslot(T2)</option>\
                            </Select>\
                            <input name=\"slaves\" type=\"hidden\" value=\"%s\"/>\
                            \
                        </div>\
                        %s\
                        <input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"/>\
                        <div class=\"row-elem\">\
                            <input type=\"submit\" value=\"Save\" class=\"yo-small yo-button\"/>\
                            \
                        </div></form>" % ("" if sync_config_table[0][1] == None else sync_config_table[0][1], \
                                         "" if sync_config_table[0][1] == None else sync_config_table[0][1], "" if strpeermac == None else strpeermac, "" if host_id == None else host_id)
    html.write(str(str_form))



def cancel_odu_form(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var action : this is used to store the action of form
    @var host_id : in this the host id is stored for access of particular host
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used for calling form on cancel button of each form
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    @return : retrun the form string in html
    @rtype : string
    """
    global html
    html = h
    action = str(html.var("action_name")).split(".")[0]
    host_id = html.var("host_id")
    exec(action + "(h,host_id)") ## this function is used to execute the string 


def omc_config_detail(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var omc_config : this is used to store the values of fields on page like text boxes,select boxes etc
    @var omc_fields : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of UNMP which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    omc_config = []
    omc_fields = []
    omc_fields.append('RU.OMCConfTable.omcIPAddress')
    omc_fields.append('RU.OMCConfTable.periodicStatisticsTimer')
    omc_config.append(html.var('RU.OMCConfTable.omcIPAddress'))
    omc_config.append(html.var('RU.OMCConfTable.periodicStatisticsTimer'))
    result = omc_conf_set(host_id, omc_fields, omc_config, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))


def ru_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var ru_config_param : this is used to store the values of fields on page like text boxes,select boxes etc
    @var ru_config_fields : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of Radio Unit Configuration which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page and it main
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    ru_config_fields = []
    ru_config_param = []
    ru_config_fields.append('RU.RUConfTable.channelBandwidth')
    #ru_config_fields.append('RU.RUConfTable.synchSource')
    ru_config_fields.append('RU.RUConfTable.countryCode')
    ru_config_param.append(html.var('RU.RUConfTable.channelBandwidth'))
    #u_config_param.append(html.var('RU.RUConfTable.synchSource'))
    ru_config_param.append(html.var('RU.RUConfTable.countryCode'))
    result = ru_config_table_set(host_id, ru_config_fields, ru_config_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))


##def ru_date_time_table(h):
##    """
##    @requires:     
##    @return: 
##    @rtype: 
##    @author:Anuj Samariya 
##    @since: 
##    @version: 
##    @date: 
##    @note: 
##    @organisation: Codescape Consultants Pvt. Ltd.
##    @copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    """
##    
##    global html
##    html=h
##    host_id = html.var("host_id")
##    user_name =  html.req.session['username']
##    if user_name==None:
##        user_name = ""
##    date_time_fields=[]
##    date_time_param=[]
##    date_time_fields.append('RU.RUDateTimeTable.Year')
##    date_time_fields.append('RU.RUDateTimeTable.Month')
##    date_time_fields.append('RU.RUDateTimeTable.Day')
##    date_time_fields.append('RU.RUDateTimeTable.Hour')
##    date_time_fields.append('RU.RUDateTimeTable.Minutes')
##    date_time_fields.append('RU.RUDateTimeTable.Seconds')
##    date_time_param.append(html.var('RU.RUDateTimeTable.Year'))
##    date_time_param.append(html.var('RU.RUDateTimeTable.Month'))
##    date_time_param.append(html.var('RU.RUDateTimeTable.Day'))
##    date_time_param.append(html.var('RU.RUDateTimeTable.Hour'))
##    date_time_param.append(html.var('RU.RUDateTimeTable.Minutes'))
##    date_time_param.append(html.var('RU.RUDateTimeTable.Seconds'))
##    result=ru_date_time_table_set(host_id,date_time_fields,date_time_param,user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
##    html.write(str(result))

##def network_interface_config(h):
##    """
##    @requires:     
##    @return: 
##    @rtype: 
##    @author:Anuj Samariya 
##    @since: 
##    @version: 
##    @date: 
##    @note: 
##    @organisation: Codescape Consultants Pvt. Ltd.
##    @copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    """
##    global html
##    global arr
##    html=h
##    host_id = html.var("host_id")
##    user_name =  html.req.session['username']
##    if user_name==None:
##        user_name = ""
##    network_interface_config_fields=[]
##    network_interface_config_param=[]
##    for i in range(len(arr)):
##        count=i+1
##        network_interface_config_fields.append('RU.NetworkInterface.%s.NetworkInterfaceConfigTable.ssId' %(count))
##        network_interface_config_param.append(html.var('RU.NetworkInterface.%s.NetworkInterfaceConfigTable.ssId'%(count)))
##    result=network_interface_config_set(host_id,network_interface_config_fields,network_interface_config_param,user_name)
##    html.write(str(result))


def tdd_mac_config(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var tdd_mac_config_param : this is used to store the values of fields on page like text boxes,select boxes etc
    @var tdd_mac_config_fields : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of Radio Frequency Configuration which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    tdd_mac_config_fields = []
    tdd_mac_config_param = []
    tdd_mac_config_fields.append('ru.np.ra.1.tddmac.rfChannel')
    tdd_mac_config_fields.append('RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase')
    tdd_mac_config_fields.append('ru.np.ra.1.tddmac.rfCoding')
    tdd_mac_config_fields.append('ru.np.ra.1.tddmac.txPower')
    tdd_mac_config_fields.append('RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors')
    tdd_mac_config_fields.append('RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer')
    tdd_mac_config_param.append(html.var('ru.np.ra.1.tddmac.rfChannel'))
    tdd_mac_config_param.append(html.var('RU.RA.1.TddMac.RATDDMACConfigTable.passPhrase'))
    tdd_mac_config_param.append(html.var('ru.np.ra.1.tddmac.rfCoding'))
    tdd_mac_config_param.append(html.var('ru.np.ra.1.tddmac.txPower'))
    tdd_mac_config_param.append(html.var('RU.RA.1.TddMac.RATDDMACConfigTable.maxCrcErrors'))
    tdd_mac_config_param.append(html.var('RU.RA.1.TddMac.RATDDMACConfigTable.leakyBucketTimer'))
    result = ra_tdd_mac_config_set(host_id, tdd_mac_config_fields, tdd_mac_config_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))

def ra_llc_configuration(h):
    """
    Author - Anuj Samariya
    this function is used to take values of llc_config form from page and send to the function ra_llc_configuration_set of odu_controller function
    this function returns the result in which diplays which values are set or which are not set
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    llc_configuration_fields = []
    llc_configuration_param = []
    llc_configuration_fields.append('RU.RA.1.LLC.RALLCConfTable.llcArqEnable')
    llc_configuration_fields.append('RU.RA.1.LLC.RALLCConfTable.arqWin')
    llc_configuration_fields.append('RU.RA.1.LLC.RALLCConfTable.frameLossThreshold')
    llc_configuration_fields.append('RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer')
    llc_configuration_fields.append('RU.RA.1.LLC.RALLCConfTable.frameLossTimeout')
    llc_configuration_param.append(html.var('RU.RA.1.LLC.RALLCConfTable.llcArqEnable'))
    llc_configuration_param.append(html.var('RU.RA.1.LLC.RALLCConfTable.arqWin'))
    llc_configuration_param.append(html.var('RU.RA.1.LLC.RALLCConfTable.frameLossThreshold'))
    llc_configuration_param.append(html.var('RU.RA.1.LLC.RALLCConfTable.leakyBucketTimer'))
    llc_configuration_param.append(html.var('RU.RA.1.LLC.RALLCConfTable.frameLossTimeout'))
    result = ra_llc_configuration_set(host_id, llc_configuration_fields, llc_configuration_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))


def omc_registration_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var omc_registration_fields : this is used to store the values of fields on page like text boxes,select boxes etc
    @var omc_registration_param : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of UNMP registration form which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    omc_registration_fields = []
    omc_registration_param = []
    omc_registration_fields.append('RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr')
    omc_registration_fields.append('RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson')
    omc_registration_fields.append('RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile')
    omc_registration_fields.append('RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont')
    omc_registration_fields.append('RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail')
    omc_registration_param.append(html.var('RU.SysOmcRegistrationTable.sysOmcRegistercontactAddr'))
    omc_registration_param.append(html.var('RU.SysOmcRegistrationTable.sysOmcRegistercontactPerson'))
    omc_registration_param.append(html.var('RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile'))
    omc_registration_param.append(html.var('RU.SysOmcRegistrationTable.sysOmcRegisteralternateCont'))
    omc_registration_param.append(html.var('RU.SysOmcRegistrationTable.sysOmcRegistercontactEmail'))
    result = omc_registration_configuration_set(host_id, omc_registration_fields, omc_registration_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))



def syn_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var syn_configuration_fields : this is used to store the values of fields on page like text boxes,select boxes etc
    @var syn_configuration_param : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of Synchronization Configuration form which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    syn_configuration_fields = []
    syn_configuration_param = []
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.rasterTime')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.numSlaves')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.syncLossThreshold')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.leakyBucketTimer')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.syncLostTimeout')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.timerAdjust')
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.rasterTime'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.numSlaves'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.syncLossThreshold'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.leakyBucketTimer'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.syncLostTimeout'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.timerAdjust'))
    result = syn_configuration_set(host_id, syn_configuration_fields, syn_configuration_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))



def ra_config(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var ra_config_fields : this is used to store the values of fields on page like text boxes,select boxes etc
    @var ra_config_param : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of Radio Access Configuration form which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    ra_config_fields = []
    ra_config_param = []
    ra_config_fields.append('RU.RA.1.RAConfTable.aclMode')
    ra_config_fields.append('RU.RA.1.RAConfTable.ssId')
    ra_config_param.append(html.var('RU.RA.1.RAConfTable.aclMode'))
    ra_config_param.append(html.var('RU.RA.1.RAConfTable.ssId'))
    result = ra_config_set(host_id, ra_config_fields, ra_config_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))


def peer_config(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var peer_config_fields : this is used to store the values of fields on page like text boxes,select boxes etc
    @var peer_config_param : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var time_slot_param : this is used to store the field name of timeslot
    @var count : this is used to store the count of timeslot and use in giving number to peer mac fields
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of Peer MAC Configuration form which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    peermac = 8
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    peer_config_fields = []
    peer_config_param = []
    time_slot_param = ''
    status = 0
    count = 0
    time_slot_param = html.var('RU.SyncClock.SyncConfigTable.numSlaves')
    for i in range(0, int(time_slot_param)):
        peer_config_fields.append('ru.np.ra.1.peer.%s.config.macAddress' % (i + 1))
        peer_config_param.append(html.var('ru.np.ra.1.peer.%s.config.macAddress' % (i + 1)))
    for i in range(int(time_slot_param), peermac):
        count = i + 1
        param = html.var('ru.np.ra.1.peer.%s.config.macAddress' % (count))
        if param != "":
            status = 1
            break
    result = peer_config_set(host_id, status, peer_config_fields, peer_config_param, time_slot_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))

def peer_delete_slaves(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var sync_configuration_fields : this is used to store the values of fields on page like text boxes,select boxes etc
    @var sync_configuration_param : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var time_slot_param : this is used to store the field name of timeslot
    @var count : this is used to store the count of timeslot and use in giving number to peer mac fields
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to empty the peer mac addresses if the number of slaves is smaller than the peer mac addresses and user want to continue to set the timeslot
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    peermac = 8
    html = h
    host_id = html.var("host_id")
    syn_configuration_fields = []
    syn_configuration_param = []
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.rasterTime')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.numSlaves')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.syncLossThreshold')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.leakyBucketTimer')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.syncLostTimeout')
    syn_configuration_fields.append('RU.SyncClock.SyncConfigTable.timerAdjust')
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.rasterTime'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.numSlaves'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.syncLossThreshold'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.leakyBucketTimer'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.syncLostTimeout'))
    syn_configuration_param.append(html.var('RU.SyncClock.SyncConfigTable.timerAdjust'))
    result = peer_slaves(host_id, peermac, syn_configuration_fields, syn_configuration_param)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))


def acl_config(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var acl_config_fields : this is used to store the values of fields on page like text boxes,select boxes etc
    @var acl_config_param : this is used to store name of html elements on the page like textboxes name ,select boxes etc
    @var acl_mode : this is used to store the value of acl mode on the page
    @var acl-count : this is used to store the total number of acl mac addresses on the page
    @var time_slot_param : this is used to store the field name of timeslot
    @var count : this is used to store the count of timeslot and use in giving number to peer mac fields
    @var result : this is used to store result of form values which are set or which are not set in dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to get all the field values and field names on form of ACL Configuration form which are going to set by user and 
            pass it to the controller function and controller return the result, this function get the result and write on to the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    count = 0
    acl_config_fields = []
    acl_config_param = []
    acl_mode_field = 'RU.RA.1.RAConfTable.aclMode'
    acl_mode = html.var('RU.RA.1.RAConfTable.aclMode')
    acl_count = int(html.var('acl_count'))
    while acl_count > 10:
        if html.var('RU.RA.1.RAACLConfig.%s.macAddress' % (acl_count)) == None or html.var('RU.RA.1.RAACLConfig.%s.macAddress' % (acl_count)) == '':
            acl_count = acl_count - 1
        else:
            break
    for i in range(0, int(acl_count)):
        count = i + 1
        acl_config_fields.append('RU.RA.1.RAACLConfig.%s.macAddress' % (count))
        acl_config_param.append(html.var('RU.RA.1.RAACLConfig.%s.macAddress' % (count)))
    result = acl_config_set(host_id, acl_mode_field, acl_mode, acl_config_fields, acl_config_param, user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))

def acl_reconciliation(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type_id : this is used to store the device type id i.e. odu16,odu00
    @var table_prefix : this is used to store the table prefix according to device type and according to table name in database eg odu16_get_ru_conifg 
                        in this "odu16_" is the table prefix and "odu16" is the device_type_id and "odu16_get_ru_conifg " is the table name
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to reconciliation the acl mac addresses
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    table_prefix = "odu16_"
    insert_update = True
    result = acl_reconcile(host_id, device_type_id, table_prefix, insert_update)
    html.write(str(result))


def retry_set_for_odu16(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var device_type_id : this is used to store the device type id i.e. odu16,odu00
    @var table_name : this is used to store the table name
    @var textbox : this is used to store the textbox name on the page
    @var textbox_value : this is used to store the textbox value on the page
    @var textbox_field : this is used to store the textbox field name on the page like "periodic_stats_timer" i.e. the field which we want to update in the database
    @index_val : this is used to store the index value in case of aclmac and peer mac otherwise it is empty
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to retry the single value
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    table_name = html.var("table_name")
    textbox = html.var("textbox")
    textbox_value = html.var("textbox_value")
    textbox_field = html.var("textbox_field")
    index_value = html.var('index')
    host_id = html.var("host_id")
    result = retry_set_one(host_id, table_name, textbox, textbox_value, textbox_field, index_value, user_name)# this funtion takes the host_id ,table name,textbox name,textbox value,textbox field,index value 
    html.write(str(result))


def retry_set_all_for_odu16(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var device_type_id : this is used to store the device type id i.e. odu16,odu00
    @var table_name : this is used to store the table name
    @var textbox : this is used to store the textbox name on the page
    @var textbox_value : this is used to store the textbox value on the page
    @var textbox_field : this is used to store the textbox field name on the page like "periodic_stats_timer" i.e. the field which we want to update in the database
    @textbox_value_list: this is used to store the list of textbox value name 
    @textbox_field_list: this is used to store the list of textbox field name 
    @table_name_list : this is used to store the list of tablename 
    @index_value_list : this is used to store the list of indexes in case of aclmac and peer mac otherwise it is empty
    @index_val : this is used to store the index value in case of aclmac and peer mac otherwise it is empty
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to retry all the values on the form
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    table_name = html.var("table_name")
    textbox = html.var("textbox_name")
    textbox_value = html.var("textbox_value")
    textbox_field = html.var("textbox_field")
    index_value = html.var("index")
    host_id = html.var("host_id") 
    table_name_list = []
    textbox_list = []
    textbox_value_list = []
    textbox_field_list = []
    index_value_list = []
    if table_name != None and textbox != None and textbox_value != None and textbox_field != None:
        table_name_list = table_name.split(",")
        textbox_list = textbox.split(",")
        textbox_value_list = textbox_value.split(",")
        textbox_field_list = textbox_field.split(",")
        if index_value is None:
            index_value_list = [1]
        else:
            index_value_list = index_value.split(",")
    result = retry_set_for_all_odu16(host_id, table_name_list, textbox_list, textbox_field_list, textbox_value_list, index_value_list, user_name)# this funtion takes the host_id ,table name,textbox name,textbox value,textbox field,index value 
    html.write(str(result))

def commit_flash(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var user_name : this is used to store the name of user who is logged in
    @var device_type_id : this is used to store the device type id i.e. odu16,odu00
    @var result : this is used to store the result come form controller
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to commit all the data on device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    host_id = html.var("host_id")
    device_type_id = html.var("device_type_id")
    try:
        if device_type_id == "odu100":
            host_op_status = obj_essential.get_hoststatus(host_id)
            if host_op_status == None or host_op_status == 0:
                obj_essential.host_status(host_id, 4)
                result = commit_to_flash(host_id, 'RU.RUOMOperationsTable.omOperationsReq', user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
                html.write(str(result))
            else:
                result = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
                html.write(str(result))

        else:
            result = commit_to_flash(host_id, 'RU.RUOMOperationsTable.omOperationsReq', user_name)# this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
            html.write(str(result))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))

    finally:        
        obj_essential.host_status(host_id, 0, None, 4)
    # this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not



def get_device_data_table(h):
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

    global html
    html = h
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
    #this is the result which we show on the page
    result = ""
    userid = html.req.session['user_id']
    #take value of IPaddress from the page through html.var
    #check that value is None Then It takes the empty string
    if html.var("ip_address") == None:
        ip_address = ""
    else:
        ip_address = html.var("ip_address")

    #take value of MACAddress from the page through html.var
    #check that value is None Then It takes the empty string
    if html.var("mac_address") == None:
        mac_address = ""
    else:
        mac_address = html.var("mac_address")

    #take value of SelectedDevice from the page through html.var
    #check that value is None Then It takes the empty string
    if html.var("device_type") == None:
        selected_device = "odu"
    else:
        selected_device = html.var("device_type")

    #call the function get_odu_list of odu-controller which return us the list of devices in two dimensional list according to IPAddress,MACaddress,SelectedDevice
    if html.req.session["role"] == "admin" or html.req.session["role"] == "user":
        result = get_device_list(ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_req)#sSortDir_0,iSortCol_0,
    else:
        result = get_device_list_guest(ip_address, mac_address, selected_device, i_display_start, i_display_length, s_search, sEcho, sSortDir_0, iSortCol_0, userid, html_req)#sSortDir_0,iSortCol_0,
    # display the result on page
    #html.write(str(result))
    #html.write(table_view)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result))) 

def get_device_list_odu(h):
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
    @note : this function is used to select the from function according to device type means which device configuration shows on page is decided with this function
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """

    try:
        global html
        html = h

        #this is the result which we show on the page
        result = ""
        ip_address = ""
        mac_address = ""
        selected_device = "odu16"
        #take value of IPaddress from the page through html.var
        #check that value is None Then It takes the empty string
        if html.var("ip_address") == None:
            ip_address = ""
        else:
            ip_address = html.var("ip_address")

        #take value of MACAddress from the page through html.var
        #check that value is None Then It takes the empty string
        if html.var("mac_address") == None:
            mac_address = ""
        else:
            mac_address = html.var("mac_address")
        #take value of SelectedDevice from the page through html.var
        #check that value is None Then It takes the empty string
        if html.var("selected_device_type") == None:
            selected_device = "odu16"
        else:
            selected_device = html.var("selected_device_type")

        #call the function get_odu_list of odu-controller which return us the list of devices in two dimensional list according to IPAddress,MACaddress,SelectedDevice

        result = get_device_list_odu_profiling(ip_address, mac_address, selected_device)
        if result == 0 or result == 1 or result == 2:
            html.write(str(result))
        else:
            if selected_device == "odu16":
                odu_profiling_form(h, result)
            else:

                odu100_profiling_form(result, selected_device)
    except Exception as e:
        html.write(str(e[-1]))

############################################Classes Structure For Odu Profiling###########################################################


class OduConfiguration():
    """
    @author : Anuj Samariya 
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this class is used to create the configuration forms of odu100 device
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    def __init__(self):
        self.odu100_select_list_object = MakeOdu100SelectListWithDic()

    def odu16_profiling(self):
        """
        Author - Anuj Samariya
        This function is used to call all functions which make forms of odu16
        h - request object
        This returns the string in html form
        """
        pass


    def odu100_profiling(self, host_id, selected_device):

        global html
        #This the main div container for all the forms of odu100
        html.write("<div id = \"odu100_main_form_container\" name=\"odu100_main_form_container\">")

        #This closes the main div container of forms


    def odu100_ru_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 Radio Unit
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        #This variable is used for storing html form which is in string form [type - string]
        odu100_ru_config = ""
        global html        
        ru_config_table_data = odu100_get_ruconfigtable(host_id)
        ru_status_obj = IduGetData()
        ru_status_data = ru_status_obj.common_get_data_by_host('Odu100RuStatusTable', host_id)
        firmware_result=get_firmware_version(host_id)
        if firmware_result['success']==0:
            firmware_version=firmware_result['output']
        else:
            firmware_version='7.2.20'
        if len(ru_status_data) > 0:
            if ru_status_data[0].cpuId == None:
                cpuid = 6
            else:
                cpuid = ru_status_data[0].cpuId
        else:
            cpuid = 6
        ru_configuration = ru_config_table_data["result"]        
        if len(ru_configuration) > 0:
            odu100_ru_config_form = "\
                                        <form id = \"odu100_ru_configuration_form\" name=\"odu100_ru_configuration_form\" action=\"odu100_ru_configuration.py\" method=\"get\">\
                                            <div id=\"odu100_ru_configuration_form_parmeters_container\" name=\"odu100_ru_configuration_form_parmeters_container\">\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Channel Bandwidth **</label>\
                                                    %s<span>&nbsp;&nbsp;MHz</span>\
                                                </div>\
                                                <div class=\"row-elem\" style=\"display:none\">\
                                                    <label class=\"lbl\">Sync Source</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Country Code **</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\"  style=\"%s\">\
                                                    <label class=\"lbl\">POE State</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Alignment Control</label>\
                                                    <input type = \"text\" id =\"RU.RUConfTable.alignmentControl\" name = \"RU.RUConfTable.alignmentControl\" value = \"%s\" />\
                                                    <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 300</span>\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                    <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\"/>\
                                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\"/>\
                                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\" /><br/><br/>\
                                                    <span  style=\"font-size: 11px;\" class=\"note\">** Change for all these values will cause reboot</span>\
                                                    <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                                    <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                    <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_ru_configuration\" tablename=\"ruConfTable\"/>\
                                                </div>\
                                            </div>\
                                        </form>\
                                " % \
                                  (self.odu100_select_list_object.channel_bandwidth_select_list(str("" if ru_configuration[0][0] == None else ru_configuration[0][0]), "enabled", "ru.ruConfTable.channelBandwidth", "false", "Channel Bandwidth"), \
                                   self.odu100_select_list_object.sync_source_select_list((0 if ru_configuration[0][5] == None else "0" if ru_configuration[0][5] == 0 or ru_configuration[0][5] == 2 else str("" if ru_configuration[0][5] == None else ru_configuration[0][5])), \
                                                                                          ("disabled" if ru_configuration[0][5] == None else "disabled" if ru_configuration[0][5] == 0 or ru_configuration[0][5] == 2 else "enabled"), "ru.ruConfTable.synchSource", "false", "Sync Source"), \
                                   self.odu100_select_list_object.country_code_select_list(str("" if ru_configuration[0][2] == None else str("" if ru_configuration[0][2] == None else ru_configuration[0][2])), "enabled", "ru.ruConfTable.countryCode", "false", "Country Code"), \
                                   "" if firmware_version=="7.2.20" else "display:none",\
                                   "" if firmware_version=="7.2.25" else self.odu100_select_list_object.poe_state_select_list_cpu(str("" if ru_configuration[0][3] == None else ru_configuration[0][3]),"enabled", "ru.ruConfTable.poeState", "false", "Poe State") if int(cpuid) == 1 or int(cpuid) == 5 else self.odu100_select_list_object.poe_state_select_list(str("" if ru_configuration[0][3] == None else ru_configuration[0][3]), "enabled", "ru.ruConfTable.poeState", "false", "Poe State"),\
                                   "" if ru_configuration[0][4] == None else ru_configuration[0][4],host_id, selected_device)
                                   

        else:
            if ru_config_table_data["success"] == 1:
                self.flag = 1
                odu100_ru_config_form = "\
                                            <form id = \"odu100_ru_configuration_form\" name=\"odu100_ru_configuration_form\" action=\"odu100_ru_configuration.py\" method=\"get\">\
                                                <div id=\"odu100_ru_configuration_form_parmeters_container\" name=\"odu100_ru_configuration_form_parmeters_container\">\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Channel Bandwidth</label>\
                                                        %s\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Sync Source</label>\
                                                        %s\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Country Code</label>\
                                                        %s\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">POE State</label>\
                                                        %s\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Alignment Control</label>\
                                                        <input type = \"text\" id =\"RU.RUConfTable.alignmentControl\" name = \"RU.RUConfTable.alignmentControl\" value = \"\"/>\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\" \>\
                                                        <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100RuConfigFormSubmitCheck('odu100_ru_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                        <span  style=\"font-size: 11px;\">** Change these values will cause reboot</span>\
                                                        <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                        <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                        <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_ru_configuration\" tablename=\"ruConfTable\"/>\
                                                    </div>\
                                                </div>\
                                            </form>\
                                    " % \
                                      (self.odu100_select_list_object.channel_bandwidth_select_list("", "enabled", "ru.ruConfTable.channelBandwidth", "false", "Channel Bandwidth"), \
                                       self.odu100_select_list_object.sync_source_select_list("", "enable", "ru.ruConfTable.synchSource", "false", "Sync Source"), \
                                       self.odu100_select_list_object.country_code_select_list("", "enabled", "ru.ruConfTable.countryCode", "false", "Country Code"), \
                                       self.odu100_select_list_object.poe_state_select_list("", "enabled", "ru.ruConfTable.poeState", "false", "Poe State"), \
                                       host_id, selected_device
                                       )

        return str(odu100_ru_config_form)

    def  odu100_ra_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 Radio Access
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        #This variable is used for storing html form which is in string form [type - string]
        odu100_ra_config = ""
        global html
        ra_config_table_data = odu100_get_raconfigtable(host_id)
        tddmac_config_table_data = odu100_get_tddmacconfigtable(host_id)
        ru_config_table_data = odu100_get_ruconfigtable(host_id)
        ru_configuration = ru_config_table_data["result"]
        tddmac_configuration = tddmac_config_table_data["result"]
        ra_configuration = ra_config_table_data["result"]
        firmware_result=get_firmware_version(host_id)
        if firmware_result['success']==0:
            firmware_version=firmware_result['output']
        else:
            firmware_version='7.2.20'
        
        odu100_ra_config_form = ""   
        anc_div = ""
        anc_div = "<div class=\"row-elem\" style=\"%s\">\
	                <label class=\"lbl\">ANC</label>\
	                %s\
	            </div> "%("" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none",
	            self.odu100_select_list_object.ans_select_list(str("" if ra_configuration[0][10] == None else ra_configuration[0][10]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.anc", "false", "ANC"))
                                    
                                                                                    
        if len(ra_configuration) > 0 and len(tddmac_configuration) > 0 and len(ru_configuration) > 0:
            odu100_ra_config_form = "\
                                    <form id=\"odu100_ra_configuration_form\" name=\"odu100_ra_configuration_form\" action=\"odu100_ra_configuration.py\" method=\"get\">\
                                        <div id=\"odu100_ra_configuration_form_parmeters_container\" name=\"odu100_ra_configuration_form_parmeters_container\">\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">Number Of Slaves</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">SSID</label>\
                                                <input type = \"text\" id =\"ru.ra.raConfTable.ssID\" name = \"ru.ra.raConfTable.ssID\" value = \"%s\" maxlength = \"32\" />\
                                                <span style=\"font-size:9px\">&nbsp;&nbsp;Upto 32 characters allowed</span>\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Encryption Type</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Pass Phrase</label>\
                                                <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.passPhrase\" name = \"ru.ra.tddMac.raTddMacConfigTable.passPhrase\" value=\"%s\" maxlength = \"64\"/>\
                                                <span style=\"font-size:9px\">&nbsp;&nbsp;Upto 64 characters allowed</span>\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">TX Power <span style=\"font-size:9px\">(dBm)</span></label>\
                                                <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.txPower\" name = \"ru.ra.tddMac.raTddMacConfigTable.txPower\" value = \"%s\"/>\
                                                <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 30</span>\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Max CRC Errors</label>\
                                                <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors\" name = \"ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors\" value = \"%s\" maxlength = \"15\">\
                                                <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 50000</span>\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Leaky Bucket Timer</label>\
                                                <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue\" name = \"ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue\"\" value = \"%s\" maxlength = \"15\">\
                                                <span style=\"font-size:9px\">&nbsp;&nbsp;1 - 60</span>\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">ACM</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">DBA</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">Guaranteed Broadcast </label>\
                                                <input type = \"text\" id=\"ru.ra.raConfTable.guaranteedBroadcastBW\" name=\"ru.ra.raConfTable.guaranteedBroadcastBW\" value=\"%s\" maxlength=\"15\" \>\
                                                <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 10000</span>\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">ACS</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">DFS</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Antenna Port</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\" style=\"%s\">\
                                                <label class=\"lbl\">Link Distance</label>\
                                                %s\
                                            </div>\
						%s\
                                            <div class=\"row-elem\">\
                                                <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                <input type = \"hidden\" name=\"node_type\" value=\"%s\" />\
                                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_ra_configuration\" tablename=\"raConfTable,raTddMacConfigTable\"/>\
                                            </div>\
                                        </div>\
                                    </form>\
                                " % ("" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    self.odu100_select_list_object.timeslot_select_list(int(0 if ra_configuration[0][0] == None else ra_configuration[0][0]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.numSlaves", "false", "TimeSlot"), \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    "" if ra_configuration[0][1] == None else ra_configuration[0][1],
                                    self.odu100_select_list_object.encryption_type_select_list(str(tddmac_configuration[0][0] if str(tddmac_configuration[0][0]) != None else ""), "enabled", "ru.ra.tddMac.raTddMacConfigTable.encryptionType", "false", "Encryption Type"), \
                                    (tddmac_configuration[0][1] if  tddmac_configuration[0][1] != None else ""), "" if tddmac_configuration[0][2] == None else tddmac_configuration[0][2], "" if tddmac_configuration[0][3] == None else tddmac_configuration[0][3], "" if tddmac_configuration[0][4] == None else tddmac_configuration[0][4], \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    self.odu100_select_list_object.acm_select_list(str("" if ra_configuration[0][2] == None else ra_configuration[0][2]), "disabled" if ru_configuration[0].defaultNodeType == None else "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.acm", "false", "ACM"), \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    self.odu100_select_list_object.dba_select_list(str("" if ra_configuration[0][3] == None else ra_configuration[0][3]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.dba", "false", "DBA"), \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    "" if ra_configuration[0][4] == None else ra_configuration[0][4], \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    self.odu100_select_list_object.acs_select_list(str("" if ra_configuration[0][5] == None else ra_configuration[0][5]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.acs", "false", "ACS"), \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    self.odu100_select_list_object.dfs_select_list(str("" if ra_configuration[0][6] == None else ra_configuration[0][6]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.dfs", "false", "DFS"), \
                                    self.odu100_select_list_object.antenna_port_select_list(str("" if ra_configuration[0][8] == None else ra_configuration[0][8]), "enabled", "ru.ra.raConfTable.antennaPort", "false", "Antenna Port"), \
                                    "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                    self.odu100_select_list_object.link_distance_select_list(str("" if ra_configuration[0][9] == None else ra_configuration[0][9]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.ra.raConfTable.linkDistance", "false", "Link Distance"), \
                                    "" if firmware_version=="7.2.20" else anc_div ,\
                                    host_id, selected_device, ru_configuration[0].defaultNodeType)
# Change ra_configuration[0][5] valuue to ra_configuration[0][10] after new db updated
        else:
            if tddmac_config_table_data["success"] == 1 or ra_config_table_data["success"] == 1:
                anc_div = "<div class=\"row-elem\">\
                            <label class=\"lbl\">ANC</label>\
                            %s\
                        </div>"%(self.odu100_select_list_object.ans_select_list(str(""), "enabled", "ru.ra.raConfTable.anc", "false", "ANC"))

                self.flag = 1
                odu100_ra_config_form = "\
                                        <form id=\"odu100_ra_configuration_form\" name=\"odu100_ra_configuration_form\" action=\"odu100_ra_configuration.py\" method=\"get\">\
                                            <div id=\"odu100_ra_configuration_form_parmeters_container\" name=\"odu100_ra_configuration_form_parmeters_container\">\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Number Of Slaves</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">SSID</label>\
                                                    <input type = \"text\" id =\"ru.ra.raConfTable.ssID\" name = \"ru.ra.raConfTable.ssID\" value = \"\" maxlength = \"32\"/>\
                                                    <span style=\"font-size:9px\">&nbsp;&nbsp;Upto 32 characters allowed</span>\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Encryption Type</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Pass Phrase</label>\
                                                    <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.passPhrase\" name = \"ru.ra.tddMac.raTddMacConfigTable.passPhrase\" value=\"\"/>\
                                                    <span style=\"font-size:9px\">&nbsp;&nbsp;Upto 32 characters allowed</span>\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Tx Power</label>\
                                                    <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.txPower\" name = \"ru.ra.tddMac.raTddMacConfigTable.txPower\" value = \"\"/>\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Max Crc Errors</label>\
                                                    <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors\" name = \"ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors\" value = \"\" maxlength = \"15\">\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Leaky Bucket Timer</label>\
                                                    <input type = \"text\" id =\"ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue\" name = \"ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue\" value = \"\" maxlength = \"15\">\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">ACM</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">DBA</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Guaranteed Broadcast </label>\
                                                    <input type = \"text\" id =\"ru.ra.raConfTable.guaranteedBroadcastBW\" name = \"ru.ra.raConfTable.guaranteedBroadcastBW\" value = \"\" maxlength = \"15\" disabled=\"disabled\">\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">ACS</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">DFS</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Antenna Port</label>\
                                                    %s\
                                                </div>\
                                                <div class=\"row-elem\">\
                                                    <label class=\"lbl\">Link Distance</label>\
                                                    %s\
                                                </div>\
                                                %s\
                                                <div class=\"row-elem\">\
                                                    <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                    <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_ra_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                    <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                    <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                    <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_ra_configuration\" tablename=\"'raConfTable,raTddMacConfigTable'\"/>\
                                                </div>\
                                            </div>\
                                            <div id=\"ra_config_form_result\" name=\"ra_config_form_result\">\
                                            </div>\
                                        </form>\
                                    " % (self.odu100_select_list_object.timeslot_select_list(str(""), "disabled", "ru.ra.raConfTable.numSlaves", "false", "TimeSlot"), \
                                        self.odu100_select_list_object.encryption_type_select_list(str(""), "enabled", "ru.ra.tddMac.raTddMacConfigTable.encryptionType", "false", "Encryption Type"), \
                                        self.odu100_select_list_object.acm_select_list(str(""), "enabled", "ru.ra.raConfTable.acm", "false", "ACM"), \
                                        self.odu100_select_list_object.dba_select_list(str(""), "disabled", "ru.ra.raConfTable.dba", "false", "DBA"), \
                                        self.odu100_select_list_object.acs_select_list(str(""), "enabled", "ru.ra.raConfTable.acs", "false", "ACS"), \
                                        self.odu100_select_list_object.dfs_select_list(str(""), "enabled", "ru.ra.raConfTable.dfs", "false", "DFS"), \
                                        self.odu100_select_list_object.antenna_port_select_list(str(""), "enabled", "ru.ra.raConfTable.antennaPort", "false", "Antenna Port"), \
                                        self.odu100_select_list_object.link_distance_select_list(str(""), "enabled", "ru.ra.raConfTable.linkDistance", "false", "Link Distance"), \
                                        "" if firmware_version=="7.2.20" else anc_div ,\
                                        host_id, selected_device)                        

        return str(odu100_ra_config_form)

    def odu100_peer_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 Peer Configuration
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        #This variable is used for storing html form which is in string form [type - string]
        odu100_ra_config_form = ""
        global html
        peer_config_table_data = odu100_get_peerconfigtable(host_id)
        ra_conf_result = odu100_get_raconfigtable(host_id)
        ra_configuration = ra_conf_result["result"]
        if len(ra_configuration) > 0:
            antenna_port = 1 if ra_configuration[0].antennaPort == None else ra_configuration[0].antennaPort
        ru_config_table_data = odu100_get_ruconfigtable(host_id)
        ru_configuration = ru_config_table_data["result"]
        peer_configuration = peer_config_table_data["result"]
        if len(peer_configuration) > 0:
            odu100_peer_config_form = "\
                                    <form id = \"odu100_peer_configuration_form\" name=\"odu100_peer_configuration_form\" action=\"odu100_peer_configuration.py\" method=\"get\">\
                                        <div id=\"odu100_peer_configuration_form_parmeters_container\" name=\"odu100_peer_configuration_form_parmeters_container\" style=\"width: 1230px;\" >\
                                            <div class=\"row-elem\" style=\"width: 1230px;\">\
                                                <label class=\"lbl\" style=\"width: 114px;\">MAC</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 35px;\" >Guaranteed Uplink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Guaranteed Downlink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Maximum Downlink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Maximum Uplink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Basic Rate MCS Index</label>\
                                                <input type=\"hidden\" id=\"timeslot_val\" name=\"timeslot_val\" value=\"\"/>\
                                                <input type=\"hidden\" id=\"acl_val\" name=\"acl_val\" value=\"\"/>\
                                            </div>"
            #for i in range(0,len(peer_configuration)):
            for i in range(0, 16):
                if len(peer_configuration) > i:
                    odu100_peer_config_form += "<div class=\"row-elem\" style=\"width:1230px\">\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" name = \"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" value = \"%s\" maxlength=\"18\" style=\"width:100px;\"/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" value = \"%s\" style=\"width:61px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" value = \"%s\"  style=\"width:61px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" name=\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" value = \"%s\" style=\"width:61px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" value = \"%s\"  style=\"width:61px;\" %s/>\
                                                    %s\
                                                </div>" % (i + 1, i + 1, \
                                                         "" if peer_configuration[i].peerMacAddress == None else peer_configuration[i].peerMacAddress, \
                                                         i + 1, i + 1, \
                                                         "512" if peer_configuration[i].guaranteedUplinkBW == None else peer_configuration[i].guaranteedUplinkBW, "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                         i + 1, i + 1, \
                                                         "512" if peer_configuration[i].guaranteedDownlinkBW == None else peer_configuration[i].guaranteedDownlinkBW, "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                         i + 1, i + 1, "100000" if peer_configuration[i].maxDownlinkBW == None else peer_configuration[i].maxDownlinkBW, \
                                                         "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                         i + 1, i + 1, "100000" if peer_configuration[i].maxUplinkBW == None else peer_configuration[i].maxUplinkBW, \
                                                         "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                         self.odu100_select_list_object.mcs_index_select_list("-1" if peer_configuration[i].basicrateMCSIndex == None or peer_configuration[i].basicrateMCSIndex == "" else peer_configuration[i].basicrateMCSIndex, \
                                                                                                              "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1), False, "MCS Index", {'style':'width:118px'}) if int(antenna_port) == 1 or int(antenna_port) == 2 else self.odu100_select_list_object.mcs_index_select_list_mimo("-1" if peer_configuration[i].basicrateMCSIndex == None or peer_configuration[i].basicrateMCSIndex == "" else peer_configuration[i].basicrateMCSIndex, \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1), False, "MCS Index", {'style':'width:118px'}))

                else:
                    odu100_peer_config_form += "<div class=\"row-elem\" style=\"width:1230px;display:none\">\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" name = \"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" value = \"%s\" maxlength=\"18\" style=\"width:100px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" value = \"%s\" style=\"width:61px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" value = \"%s\"  style=\"width:61px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" name=\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" value = \"100000\" style=\"width:61px;\" %s/>\
                                                    <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" value = \"100000\" style=\"width:61px;\" %s/>\
                                                    %s\
                                                </div>" % (i + 1, i + 1, "", "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                         i + 1, i + 1, "512", "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                         i + 1, i + 1, "512", "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled"\
                                                         , i + 1, i + 1, "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", \
                                                         i + 1, i + 1, "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", \
                                                         self.odu100_select_list_object.mcs_index_select_list(-1, \
                                                                                                              "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1), False, "MCS Index", {'style':'width:118px'})if int(antenna_port) == 1 or int(antenna_port) == 2 else self.odu100_select_list_object.mcs_index_select_list_mimo(-1, \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1), False, "MCS Index", {'style':'width:118px'}))

            #%("" if peer_configuration[i][0]==None else peer_configuration[i][0],"" if peer_configuration[i][1]==None else peer_configuration[i][1],"" if peer_configuration[i][2]==None else peer_configuration[i][2],"" if peer_configuration[i][3]==None else peer_configuration[i][3])                            
            odu100_peer_config_form += " <div class=\"row-elem\">\
                                            <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\"  />\
                                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type=\"button\" name=\"modulation_rate_table\" id=\"modulation_rate_table\" value=\"View Modulation Rates\" class=\"yo-small yo-button\" onclick=\"viewModulationRate();\" />\
                                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                            <input type = \"hidden\" name = \"ch_bw\" value=\"%s\" />\
                                            <input type = \"hidden\" name = \"ra_port\" value=\"%s\" />\
                                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_peer_configuration\" tablename=\"peerConfigTable\"/>\
                                        </div>\
                                    </div>\
                                        <div id=\"peer_config_form_result\" name=\"peer_config_form_result\">\
                                        </div>\
                                    </form>\
                                " % (host_id, selected_device, "" if ru_configuration[0][0] == None else ru_configuration[0][0] if len(ru_configuration) > 0 else 0, \
                                   "" if ra_configuration[0][8] == None else ra_configuration[0][8] if len(ra_configuration) > 0 else 1)
        else:
            if peer_config_table_data["success"] == 1:
                self.flag = 1
                odu100_peer_config_form = "\
                                        <form id = \"odu100_peer_configuration_form\" name=\"odu100_peer_configuration_form\" action=\"odu100_peer_configuration.py\" method=\"get\">\
                                            <div id=\"odu100_peer_configuration_form_parmeters_container\" name=\"odu100_peer_configuration_form_parmeters_container\">\
                                                <div class=\"row-elem\" style=\"width: 830px;\">\
                                                <label class=\"lbl\" style=\"width: 114px;\">MAC</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 35px;\" >Guaranteed Uplink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Guaranteed Downlink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Maximum Downlink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Maximum Uplink BW (kbps)</label>\
                                                <label class=\"lbl\" style=\"width: 75px; height: 30px;\">Basic Rate MCS Index</label>\
                                                <input type=\"hidden\" id=\"timeslot_val\" name=\"timeslot_val\" value=\"\"/>\
                                                <input type=\"hidden\" id=\"acl_val\" name=\"acl_val\" value=\"\"/>\
                                            </div>"
                for i in range(0, 16):
                    if len(peer_configuration) > i:
                        odu100_peer_config_form += "<div class=\"row-elem\" style=\"width:1230px;display:none\">\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" name = \"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" value = \"%s\" maxlength=\"18\" />\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" value = \"%s\" %s/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" value = \"%s\"  %s/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" name=\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" value = \"\" %s/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" value = \"\" %s/>\
                                                        %s\
                                                    </div>" % (i + 1, i + 1, \
                                                             "" if peer_configuration[i].peerMacAddress == None else peer_configuration[i].peerMacAddress, \
                                                             i + 1, i + 1, \
                                                             "512" if peer_configuration[i].guaranteedUplinkBW == None else peer_configuration[i].guaranteedUplinkBW, \
                                                             "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             i + 1, i + 1, \
                                                             "512" if peer_configuration[i].guaranteedDownlinkBW == None else peer_configuration[i].guaranteedDownlinkBW, \
                                                             "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             i + 1, i + 1, "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             i + 1, i + 1, "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             self.odu100_select_list_object.mcs_index_select_list("-1" if peer_configuration[i].basicrateMCSIndex == None or peer_configuration[i].basicrateMCSIndex == "" else peer_configuration[i].basicrateMCSIndex, \
                                                                                                                  "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1), False, "MCS Index", {'style':'width:118px'}))

                    else:
                        odu100_peer_config_form += "<div class=\"row-elem\" style=\"width:1230px;display:none\">\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" name = \"ru.ra.peerNode.peerConfigTable.peerMacAddress.%s\" value = \"%s\" maxlength=\"18\" style=\"width:100px;\"/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s\" value=\"%s\" style=\"width:61px;\" %s/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s\" value = \"%s\"  style=\"width:61px;\" %s/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" name=\"ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s\" value = \"\" style=\"width:61px;\" %s/>\
                                                        <input type = \"text\" id =\"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" name = \"ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s\" value = \"\" style=\"width:61px;\" %s/>\
                                                        %s\
                                                    </div>" % (i + 1, i + 1, "", \
                                                             i + 1, i + 1, "512", \
                                                             "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             i + 1, i + 1, "512", \
                                                             "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             i + 1, i + 1, "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             i + 1, i + 1, "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                                             self.odu100_select_list_object.mcs_index_select_list(-1, \
                                                                                                                  "" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", 'ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s' % (i + 1), False, "MCS Index", {'style':'width:118px'}))
                odu100_peer_config_form += " <div class=\"row-elem\">\
                                                <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100PeerForm('odu100_peer_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type=\"button\" name=\"modulation_rate_table\" id=\"modulation_rate_table\" value=\"View Modulation Rates\" class=\"yo-small yo-button\" onclick=\"viewModulationRate();\" />\
                                                <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_peer_configuration\" tablename=\"peerConfigTable\"/>\
                                            </div>\
                                        </div>\
                                            <div id=\"peer_config_form_result\" name=\"peer_config_form_result\">\
                                            </div>\
                                        </form>\
                                    " % (host_id, selected_device)
        #html.write(str(odu100_peer_config_form ))
        return str(odu100_peer_config_form)
##        
##    # Author - Anuj Samariya
##    # This function is used to make form of odu100_prefferd_channellist_configuration
##    # h - request object
##    # This returns the html form in string
##    def odu100_preffered_channellist_configuration(self,h):
##        """
##        Author - Anuj Samariya
##        This function is used to make form of odu100_preffered_channellist_configuration
##        h - request object
##        This returns the string in html form
##        """
##        #This variable is used for storing html form which is in string form [type - string]
##        odu100_preffered_channel_list_config_form = ""
##        global html
##        html = h
##        odu100_preffered_channel_list_config_form = "<div id =\"preffered_channellist_config_form_container\" name=\"preffered_channellist_config_form_container\">\
##                                <form id = \"odu100_preffered_channellist_config_form\" name = \"odu100_preffered_channellist_config_form\" action = \"odu100_preffered_channellist_config\">\
##                                    <div id=\"odu100_preffered_channellist_form_parmeters_container\" name=\"odu100_preffered_channellist_form_parmeters_container\">\
##                                        <div class=\"row-elem\">\
##                                            <label class=\"lbl\">Frequency</label>\
##                                        <div>"
##        for i in range(0,10):
##            odu100_preffered_channel_list_config_form += "<div class=\"row-elem\">\
##                                                                %s\
##                                                            </div>" %(self.odu100_select_list_object.preffered_channel_select_list("","enabled",,is_readonly,select_list_initial_msg))
##        odu100_preffered_channel_list_config_form += " <div class=\"row-elem\">\
##                                    <input type=\"submit\" value=\"Save\"/>\
##                                </div>\
##                                </div>\
##                                    <div id=\"preffered_channellist_config_form_result\" name=\"preffered_channellist_config_form_result\">\
##                                    </div>\
##                                </form>\
##                            </div>"
##        html.write(odu100_preffered_channel_list_config_form)
##        

    def odu100_sync_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 Synchronization configuration
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        #This variable is used for storing html form which is in string form [type - string]
        odu100_sync_config_form = ""
        global html
        sync_config_table_data = odu100_get_syncconfigtable(host_id)
        sync_configuration = sync_config_table_data["result"]
        ru_config_table_data = odu100_get_ruconfigtable(host_id)
        ru_configuration = ru_config_table_data["result"]
        if len(sync_configuration) > 0 and len(ru_configuration) > 0:
            odu100_sync_config_form = "\
                                            <form id = \"odu100_sync_config_form\" name = \"odu100_sync_config_form\" action = \"odu100_sync_config.py\" method=\"get\">\
                                                <div id=\"odu100_sync_form_parmeters_container\" name=\"odu100_sync_form_parmeters_container\">\
                                                    <div class=\"row-elem\" style=\"%s\">\
                                                        <label class=\"lbl\">Raster Time</label>\
                                                        %s\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Sync Loss Threshold</label>\
                                                        <input type = \"text\" id =\"ru.syncClock.syncConfigTable.syncLossThreshold\" name = \"ru.syncClock.syncConfigTable.syncLossThreshold\" value = \"%s\" maxlength = \"15\"/>\
                                                        <span style=\"font-size:9px\">&nbsp;&nbsp;1 to 100</span>\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Leaky Bucket Timer</label>\
                                                        <input type = \"text\" id =\"ru.syncClock.syncConfigTable.leakyBucketTimer\" name = \"ru.syncClock.syncConfigTable.leakyBucketTimer\" value = \"%s\" maxlength = \"15\"/>\
                                                        <span style=\"font-size:9px\">&nbsp;&nbsp;1 to 60</span>\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">Sync Loss Timeout</label>\
                                                        <input type = \"text\" id =\"ru.syncClock.syncConfigTable.syncLostTimeout\" name = \"ru.syncClock.syncConfigTable.syncLostTimeout\" value = \"%s\" maxlength = \"15\"/>\
                                                        <span style=\"font-size:9px\">&nbsp;&nbsp;30 to 600</span>\
                                                    </div>\
                                                    <div class=\"row-elem\" style=\"%s\">\
                                                        <label class=\"lbl\">Sync Timer Adjust</label>\
                                                        <input type = \"text\" id =\"ru.syncClock.syncConfigTable.syncConfigTimerAdjust\" name = \"ru.syncClock.syncConfigTable.syncConfigTimerAdjust\" value = \"%s\" maxlength = \"15\" \"%s\"/>\
                                                        <span style=\"font-size:9px\">&nbsp;&nbsp;-127 to 127</span>\
                                                    </div>\
                                                    <div class=\"row-elem\" style=\"%s\">\
                                                        <label class=\"lbl\">Percentage Downlink Transmit Time</label>\
                                                        <input type = \"text\" id =\"ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime\" name = \"ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime\" value = \"%s\" maxlength = \"15\" \"%s\"/>\
                                                        <span style=\"font-size:9px\">&nbsp;&nbsp;20 to 80</span>\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <input type=\"submit\" name=\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name=\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name=\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name=\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type = \"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                        <input type = \"hidden\" name=\"device_type\" value=\"%s\" />\
                                                        <input type = \"hidden\" name=\"node_type\" value=\"%s\" />\
                                                        <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_sync_configuration\" tablename=\"syncConfigTable\"/>\
                                                    </div>\
                                                </div>\
                                                <div id=\"sync_config_form_result\" name=\"sync_config_form_result\">\
                                                </div>\
                                            </form>\
                                        " % ("" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                            self.odu100_select_list_object.raster_time_select_list(str("" if sync_configuration[0][0] == None else sync_configuration[0][0]), "disabled" if ru_configuration[0].defaultNodeType == None else "enabled" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled", "ru.syncClock.syncConfigTable.rasterTime", "false", "Raster Time")\
                                            , "" if sync_configuration[0][1] == None else sync_configuration[0][1], "" if sync_configuration[0][2] == None else sync_configuration[0][2], \
                                            "" if sync_configuration[0][3] == None else sync_configuration[0][3], \
                                            "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                            "" if sync_configuration[0][4] == None else sync_configuration[0][4], "disabled=disabled" if ru_configuration[0].defaultNodeType == None else "" if int(ru_configuration[0].defaultNodeType) == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", \
                                            "" if ru_configuration[0].defaultNodeType == None else "" if ru_configuration[0].defaultNodeType == 0 or ru_configuration[0].defaultNodeType == 2 else "display:none", \
                                            sync_configuration[0][5], "disabled" if ru_configuration[0].defaultNodeType == None else "" if int(ru_configuration[0].defaultNodeType) == 0 or ru_configuration[0].defaultNodeType == 2 else "disabled=disabled", host_id, selected_device, ru_configuration[0].defaultNodeType)
        else:
            if sync_config_table_data["success"] == 1:
                self.flag = 1
                odu100_sync_config_form = "\
                                                <form id = \"odu100_sync_config_form\" name = \"odu100_sync_config_form\" action = \"odu100_sync_config.py\" method=\"get\">\
                                                    <div id=\"odu100_sync_form_parmeters_container\" name=\"odu100_sync_form_parmeters_container\">\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">Raster Time</label>\
                                                            %s\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">Sync Loss Threshold</label>\
                                                            <input type = \"text\" id =\"ru.syncClock.syncConfigTable.syncLossThreshold\" name = \"ru.syncClock.syncConfigTable.syncLossThreshold\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">Leaky Bucket Timer</label>\
                                                            <input type = \"text\" id =\"ru.syncClock.syncConfigTable.leakyBucketTimer\" name = \"ru.syncClock.syncConfigTable.leakyBucketTimer\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">Sync Loss Timeout</label>\
                                                            <input type = \"text\" id =\"ru.syncClock.syncConfigTable.syncLostTimeout\" name = \"ru.syncClock.syncConfigTable.syncLostTimeout\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">Sync Timer Adjust</label>\
                                                            <input type = \"text\" id =\"ru.syncClock.syncConfigTable.syncConfigTimerAdjust\" name = \"ru.syncClock.syncConfigTable.syncConfigTimerAdjust\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">Percentage Downlink Transmit Time</label>\
                                                            <input type = \"text\" id =\"ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime\" name = \"ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_sync_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_sync_configuration\" tablename=\"syncConfigTable\"/>\
                                                        </div>\
                                                    </div>\
                                                    <div id=\"sync_config_form_result\" name=\"sync_config_form_result\">\
                                                    </div>\
                                                </form>\
                                            " % (self.odu100_select_list_object.raster_time_select_list(str(""), "enabled", "ru.syncClock.syncConfigTable.rasterTime", "false", "Raster Time")\
                                                , host_id, selected_device)
        return str((odu100_sync_config_form))


    def odu100_ip_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 Ip Configuration
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """

        #This variable is used for storing html form which is in string form [type - string]
        odu100_ip_config_form = ""
        global html
        ip_config_table_data = odu100_get_ipconfigtable(host_id)
        ip_configuration = ip_config_table_data["result"]
        if len(ip_configuration) > 0:
            odu100_ip_config_form = "\
                                            <form id = \"odu100_ip_config_form\" name = \"odu100_ip_config_form\" action=\"odu100_ip_config.py\" method =\"get\">\
                                                <div id=\"ip_config_form_parmeters_container\" name=\"ip_config_form_parmeters_container\">\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">IP Address</label>\
                                                        <input type = \"text\" id =\"ru.ipConfigTable.ipAddress\" name = \"ru.ipConfigTable.ipAddress\" value = \"%s\" maxlength = \"15\" disabled=\"disabled\"/>\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">IP Netmask</label>\
                                                        <input type = \"text\" id =\"ru.ipConfigTable.ipNetworkMask\" name = \"ru.ipConfigTable.ipNetworkMask\" value = \"%s\" maxlength = \"15\"/>\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <label class=\"lbl\">IP Default Gateway</label>\
                                                        <input type = \"text\" id =\"ru.ipConfigTable.ipDefaultGateway\" name = \"ru.ipConfigTable.ipDefaultGateway\" value = \"%s\" maxlength = \"15\"/>\
                                                    </div>\
                                                    <div class=\"row-elem\" style=\"diplay:none\">\
                                                        <label class=\"lbl\">DHCP state</label>\
                                                        %s\
                                                    </div>\
                                                    <div class=\"row-elem\">\
                                                        <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                        <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                        <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                    </div>\
                                                </div>\
                                                <div id=\"odu100_ip_config_form_result\" name=\"odu100_ip_config_form_result\" >\
                                                </div>\
                                            </form>\
                                        " % ("" if ip_configuration[0][0] == None else ip_configuration[0][0], "" if ip_configuration[0][1] == None else ip_configuration[0][1], "" if ip_configuration[0][2] == None else ip_configuration[0][2], self.odu100_select_list_object.dhcp_select_list(str("" if ip_configuration[0][3] == None else ip_configuration[0][3]), "enabled", "ru.ipConfigTable.autoIpConfig", "false", "DHCP State"), host_id, selected_device)
        else:
            if ip_config_table_data["success"] == 1:
                self.flag = 1
                odu100_ip_config_form = "\
                                                <form id = \"odu100_ip_config_form\" name = \"odu100_ip_config_form\" action=\"odu100_ip_config.py\" method =\"get\">\
                                                    <div id=\"ip_config_form_parmeters_container\" name=\"ip_config_form_parmeters_container\">\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">IP Address</label>\
                                                            <input type = \"text\" id =\"ru.ipConfigTable.ipAddress\" name = \"ru.ipConfigTable.ipAddress\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">IP Netmask</label>\
                                                            <input type = \"text\" id =\"ru.ipConfigTable.ipNetworkMask\" name = \"ru.ipConfigTable.ipNetworkMask\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">IP Default Gateway</label>\
                                                            <input type = \"text\" id =\"ru.ipConfigTable.ipDefaultGateway\" name = \"ru.ipConfigTable.ipDefaultGateway\" value = \"\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">DHCP state</label>\
                                                            %s\
                                                        </div>\
                                                        <div class=\"row-elem\">\
                                                            <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\"/ style=\"Display:None\" onClick=\"return odu100IpConfigFormSubmitCheck('odu100_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                        </div>\
                                                    </div>\
                                                    <div id=\"odu100_ip_config_form_result\" name=\"odu100_ip_config_form_result\">\
                                                    </div>\
                                                </form>\
                                            " % (self.odu100_select_list_object.dhcp_select_list(str(""), "enabled", "ru.ipConfigTable.autoIpConfig", "false", "DHCP State"), host_id, selected_device)
        return str(odu100_ip_config_form)

    def odu100_omc_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 OMC Configuration
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        #This variable is used for storing html form which is in string form[type - string]
        try:
            global html
            odu100_omc_config_form = ""
            omc_config_table_data = odu100_get_omcconfigtable(host_id)
            omc_configuration = omc_config_table_data["result"]
            if len(omc_configuration) > 0:
                odu100_omc_config_form = "\
                                                <form id=\"odu100_omc_config_form\" name=\"odu100_omc_config_form\" action=\"odu100_omc_config.py\" method=\"get\">\
                                                    <div class=\"omc_config_form_parmeters_container\" name=\"omc_config_form_parmeters_container\">\
                                                        <div class=\"row-elem\">\
                                                            <label class=\"lbl\">UNMP IP **</label>\
                                                            <input type=\"text\" id=\"ru.omcConfTable.omcIpAddress\" name=\"ru.omcConfTable.omcIpAddress\" value=\"%s\" maxlength=\"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\" style=\"display:none\">\
                                                            <label class=\"lbl\">Periodic Statistics Timer</label>\
                                                            <input type = \"text\" id =\"ru.omcConfTable.periodicStatsTimer\" name = \"ru.omcConfTable.periodicStatsTimer\" value = \"%s\" maxlength = \"15\"/>\
                                                        </div>\
                                                        <div class=\"row-elem\" style=\"width: 600px;\">\
                                                            <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\"/>\
                                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\"/>\
                                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" /><br/><br/>\
                                                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_omc_configuration\" tablename=\"omcConfTable\"/>\
                                                            <span  style=\"font-size: 11px;\" class=\"note\">** UNMP IP - Configuring UNMP IP is important for capturing and monitoring the device alarms</span>\
                                                        </div>\
                                                    </div>\
                                                    <div id=\"odu100_omc_config_form_result\" name=\"odu100_omc_config_form_result\">\
                                                    </div>\
                                                </form>\
                                            " % ("" if omc_configuration[0][0] == None else omc_configuration[0][0], "" if omc_configuration[0][1] == None else omc_configuration[0][1], host_id, selected_device)
            else:
                if omc_config_table_data["success"] == 1:
                    self.flag = 1
                    odu100_omc_config_form = "\
                                                    <form id=\"odu100_omc_config_form\" name=\"odu100_omc_config_form\" action=\"odu100_omc_config.py\" method=\"get\">\
                                                        <div class=\"omc_config_form_parmeters_container\" name=\"omc_config_form_parmeters_container\">\
                                                            <div class=\"row-elem\">\
                                                                <label class=\"lbl\">UNMP IP</label>\
                                                                <input type=\"text\" id=\"ru.omcConfTable.omcIpAddress\" name=\"ru.omcConfTable.omcIpAddress\" value=\"\" maxlength=\"15\"/>\
                                                            </div>\
                                                            <div class=\"row-elem\" style=\"display:none\">\
                                                                <label class=\"lbl\">Periodic Statistics Timer</label>\
                                                                <input type = \"text\" id =\"ru.omcConfTable.periodicStatsTimer\" name = \"ru.omcConfTable.periodicStatsTimer\" value=\"\" maxlength = \"15\"/>\
                                                            </div>\
                                                            <div class=\"row-elem\">\
                                                                <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_omc_config_form',this)\" class=\"yo-small yo-button\" /><br/><br/>\
                                                                <span  style=\"font-size: 11px;\">**UNMP IP - Configuring UNMP IP is important for capturing and monitoring the device alarms</span>\
                                                                <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_omc_configuration\" tablename=\"omcConfTable\"/>\
                                                            </div>\
                                                        </div>\
                                                        <div id=\"odu100_omc_config_form_result\" name=\"odu100_omc_config_form_result\">\
                                                        </div>\
                                                    </form>\
                                                " % (host_id, selected_device)
            return str(odu100_omc_config_form)
        except Exception as e:
            return str(e)

    def odu100_acl_configuration(self, host_id, selected_device):
        """
        @author : Anuj Samariya 
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to create the configuration forms of odu100 ACL Configuration
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        #This variable is used for storing html form which is in string form [type - string]
        global html
        acl_config_table_data = odu100_get_aclconfigtable(host_id)
        ra_config_table_data = odu100_get_raconfigtable(host_id)
        ra_configuration = ra_config_table_data["result"]
        acl_configuration = acl_config_table_data["result"]
        if len(acl_configuration) > 0:
            odu100_acl_config_form = "\
                                        \
                                        <fieldset>\
                                            <legend> ACL </legend>\
                                                <form id = \"odu100_acl_add_mac_config_form\" name = \"odu100_acl_add_mac_config_form\" action=\"odu100_acl_add_mac_config.py\" method=\"get\">\
                                                "

            odu100_acl_config_form += "<div class=\"row-elem\">\
                                            <label class=\"lbl\">Index</label>\
                                            %s\
                                        </div>\
                                        <div class=\"row-elem\">\
                                            <label class=\"lbl\">MAC Address</label>\
                                            <input type = \"text\" id =\"ru.ra.raAclConfigTable.macaddress\" name = \"ru.ra.raAclConfigTable.macaddress\" value = \"%s\"/>\
                                        </div>\
                                        <div class=\"row-elem\">\
                                            <input type=\"submit\" name =\"odu100_submit\" value=\"Add\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type=\"button\" name =\"odu100_acl_reconcile\" value=\"ACL Reconciliation\" id=\"odu100_acl_reconcile\" onClick=\"return odu100AclConfig('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type = \"hidden\" name = \"raacl_index\" value=\"%s\" style=\"display:None\"/>\
                                            <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"display:None\"/>\
                                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                            <input type = \"hidden\" name = \"total_rows\" value=\"%s\" id=\"total_rows\"/>\
                                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_acl_configuration\" tablename=\"raLlcConfTable\"/>\
                                        </div>" % (self.odu100_select_list_object.acl_index_select_list("" if acl_configuration[0][0] == None else acl_configuration[0][0], "enabled", "aclindex", "false", "Index",host_id), \
                                                 "" if acl_configuration[0][1] == None else acl_configuration[0][1], "" if acl_configuration[0][3] == None else acl_configuration[0][3], host_id, selected_device, len(acl_configuration))


            odu100_acl_config_form += "\
                                        \
                                    </form>\
                                    </fieldset>\
                                    <fieldset>\
                                        <legend>ACL Mode</legend>\
                                        <form id =\"odu100_acl_mode_form\" name = \"odu100_acl_mode_form\" action=\"odu100_acl_mode.py\" method=\"get\">\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">ACL Mode</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                <input type = \"hidden\" name = \"total_rows\" value=\"%s\" id=\"total_rows\"/>\
                                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_acl_configuration\" tablename=\"raLlcConfTable\"/>\
                                            </div>\
                                        </form>\
                                        </legend></fieldset>\
                                \
                            " % (self.odu100_select_list_object.acl_select_list(str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), "enabled", "ru.ra.raConfTable.aclMode", "false", "ACL Mode"), host_id, selected_device, len(acl_configuration))

            odu100_acl_config_form += "\
                                            \
                                                \
                                                    <div class=\"tableDiv\" id=\"tableDiv\">\
                                                        <table id=\"show_mac_edit_delete\" class =\"show_mac_edit_delete display\" width=\"100%\" cellpadding=0 cellspacing=0 style=\"text-align:center;\">\
                                                            <thead>\
                                                            <tr>\
                                                                <th>Index</th>\
                                                                <th>MAC Address</th>\
                                                                <th></th>\
                                                                \
                                                            </tr>\
                                                            </thead>\
                                                            <tbody>"

            # This variable is used for storing total number of records of database table [type - int]
            for i in range(0, len(acl_configuration)):
                odu100_acl_config_form += "<tr>\
                                                <td>%s</td>\
                                                <td>%s</td>\
                                                <td><a href=\"javascript:editMac('%s','0','%s',this,'%s','%s','%s');\" class=\"acl_edit_anchor\"><img src = \"images/edit16.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton\"/></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src = \"images/delete16.png\" title=\"Delete Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton\" onclick=\"editMac('%s','1','%s',this,'%s','%s','%s');\"/></td>\
                                                \
                                           </tr>" % (str("" if acl_configuration[i][0] == None else acl_configuration[i][0]), "" if acl_configuration[i][1] == None else acl_configuration[i][1], "" if acl_configuration[i][2] == None else acl_configuration[i][2], host_id, str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), len(acl_configuration), "" if acl_configuration[i][1] == None else acl_configuration[i][1], "" if acl_configuration[i][2] == None else acl_configuration[i][2], host_id, str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), len(acl_configuration), "" if acl_configuration[i][1] == None else acl_configuration[i][1])

            odu100_acl_config_form += "</tbody></table>\
                                    </div>\
                                \
                            \
                        \
                    "
        else:
            if ra_config_table_data["success"] == 1 or acl_config_table_data["success"] == 1:
                self.flag = 1
                odu100_acl_config_form = "\
                                        \
                                        <fieldset>\
                                            <legend> ACL </legend>\
                                                <form id = \"odu100_acl_add_mac_config_form\" name = \"odu100_acl_add_mac_config_form\" action=\"odu100_acl_add_mac_config.py\" method=\"get\">\
                                                "

                odu100_acl_config_form += "<div class=\"row-elem\">\
                                                <label class=\"lbl\">Index</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Mac Address</label>\
                                                <input type = \"text\" id =\"ru.ra.raAclConfigTable.macaddress\" name = \"ru.ra.raAclConfigTable.macaddress\" value = \"%s\"/>\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <input type=\"submit\" name =\"odu100_submit\" value=\"Add\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type=\"button\" name =\"odu100_acl_reconcile\" value=\"ACL Reconciliation\" id=\"odu100_acl_reconcile\" onClick=\"return odu100AclConfig('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_add_mac_config_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type = \"hidden\" name = \"raacl_index\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                <input type = \"hidden\" name = \"total_rows\" value=\"%s\" id=\"total_rows\"/>\
                                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_acl_configuration\" tablename=\"raLlcConfTable\"/>\
                                                </div>" % (self.odu100_select_list_object.acl_index_select_list("", "enabled", "aclindex", "false", "Index",host_id), \
                                                     "", \
                                                     1, host_id, selected_device, len(acl_configuration))

                odu100_acl_config_form += "\
                                        \
                                    </form>\
                                    </fieldset>\
                                    <fieldset>\
                                        <legend>ACL Mode</legend>\
                                        <form id =\"odu100_acl_mode_form\" name = \"odu100_acl_mode_form\" action=\"odu100_acl_mode.py\" method=\"get\">\
                                            <div class=\"row-elem\">\
                                                <label class=\"lbl\">Acl Mode</label>\
                                                %s\
                                            </div>\
                                            <div class=\"row-elem\">\
                                                <input type=\"submit\" name =\"odu100_submit\" value=\"Save\" id=\"id_omc_submit_save\" onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('odu100_acl_mode_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type = \"hidden\" name = \"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                                <input type = \"hidden\" name = \"total_rows\" value=\"%s\" id=\"total_rows\"/>\
                                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_acl_configuration\" tablename=\"raLlcConfTable\"/>\
                                            </div>\
                                        </form>\
                                        </legend></fieldset>\
                                \
                            " % (self.odu100_select_list_object.acl_select_list(str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), "enabled", "ru.ra.raConfTable.aclMode", "false", "ACL Mode"), host_id, selected_device, len(acl_configuration))


                odu100_acl_config_form += "\
                                                \
                                                    \
                                                        <div class=\"tableDiv\" id=\"tableDiv\">\
                                                        <table id=\"show_mac_edit_delete\" class =\"show_mac_edit_delete display\" width=\"100%\" cellpadding=0 cellspacing=0>\
                                                            <thead>\
                                                            <tr>\
                                                                <th>Index</th>\
                                                                <th>Mac Address</th>\
                                                                <th></th>\
                                                                \
                                                            </tr>\
                                                            </thead>\
                                                            <tbody>"

                # This variable is used for storing total number of records of database table [type - int]
                if (acl_configuration) == 0:
                    odu100_acl_config_form += "<tr>\
                                                <td>No Data Exist</td>\
                                           </tr>"

                else:
                    for i in range(0, len(acl_configuration)):
                        odu100_acl_config_form += "<tr>\
                                                    <td>%s</td>\
                                                    <td>%s</td>\
                                                    <td><a href=\"javascript:editMac('%s','0','%s',this,'%s','%s','%s');\" class=\"acl_edit_anchor\"><img src = \"images/edit16.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton\"/></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src = \"images/delete16.png\" title=\"Delete Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton\" onclick=\"editMac('%s','1','%s',this,'%s','%s','%s');\"/></td>\
                                                    <td></td>\
                                               </tr>" % (str("" if acl_configuration[i][0] == None else acl_configuration[i][0]), "" if acl_configuration[i][1] == None else acl_configuration[i][1], "" if acl_configuration[i][2] == None else acl_configuration[i][2], host_id, str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), len(acl_configuration), "" if acl_configuration[i][1] == None else acl_configuration[i][1], "" if acl_configuration[i][2] == None else acl_configuration[i][2], host_id, str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), len(acl_configuration), "" if acl_configuration[i][1] == None else acl_configuration[i][1])

                odu100_acl_config_form += "</tbody></table>\
                                    </div>\
                                    \
                                \
                           \
                       "
        return str(odu100_acl_config_form)

    def odu100_sys_omc_registration(self, host_id, selected_device):
        sys_registration = []
        sys_registration_data = []
        sys_registration = odu100_get_sysconfigtable(host_id)
        sys_registration_data = sys_registration["result"]
        str_form = ""
        str_form += "\
                    <form action=\"sys_registration_configuration.py\" method=\"get\" id=\"omc_registration_form\" name=\"omc_registration_form\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Address</label>\
                            <input type=\"text\" name=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr\" id=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.2.1\" maxlength=\"20\" val=\"string\" field=\"sys_omc_register_contact_addr\" value=\"%s\" tablename=\"SetOdu16SysOmcRegistrationTable\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Person</label>\
                            <input type=\"text\" name=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson\" id=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.3.1\" val=\"string\" value=\"%s\" field=\"sys_omc_register_contact_person\" maxlength=\"20\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Contact Number</label>\
                            <input type=\"text\" name=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile\" id=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.4.1\" field=\"sys_omc_register_contact_mobile\"  val=\"string\" value=\"%s\" maxlength=\"10\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Alternate Contact Number</label>\
                            <input type=\"text\" name=\"ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact\" id=\"ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.5.1\" val=\"string\" value=\"%s\" maxlength=\"20\" field=\"sys_omc_register_alternate_contact\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">Email</label>\
                            <input type=\"text\" name=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail\" id=\"ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail\" field=\"sys_omc_register_contact_email\" fact=\".1.3.6.1.4.1.26149.2.2.8.1.6.1\" val=\"string\" value=\"%s\" maxlength=\"20\" tablename=\"SetOdu16SysOmcRegistrationTable\" />\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('omc_registration_form',this)\" class=\"yo-small yo-button\"/>\
                            <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"odu100CommonFormSubmit('omc_registration_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"odu100CommonFormSubmit('omc_registration_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('omc_registration_form',this)\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                        </div>\
                    </form>" % (sys_registration_data[0].sysOmcRegisterContactAddr if len(sys_registration_data) > 0 else "", \
                              sys_registration_data[0].sysOmcRegisterContactPerson if len(sys_registration_data) > 0 else "", \
                              sys_registration_data[0].sysOmcRegisterContactMobile if len(sys_registration_data) > 0 else ""\
                              , sys_registration_data[0].sysOmcRegisterAlternateContact if len(sys_registration_data) > 0 else "", \
                              sys_registration_data[0].sysOmcRegisterContactEmail if len(sys_registration_data) > 0 else "", \
                              host_id, selected_device)
        return str_form


    def odu100_packet_filter(self,host_id,selected_device):
        """
        @author : Anuj Samariya 
        @param h : html Class Object
        @var html : this is html Class Object defined globally 
        @var host_id : this is used to store the Host Id which is come from the page
        @device_list_param : this is used to store all the details of device 
        @tab_str : this is used to store the form string
        @var odu_configuration_object : this is used to store the object of class OduConfiguration  
        @since : 20 August 2011
        @version :0.0 
        @date : 20 Augugst 2011
        @note : this function is used to write the forms of odu100 on the page
        @organisation : Codescape Consultants Pvt. Ltd.
        @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
        """
        ip_filter_table=odu100_ip_packet_table(host_id)
        ip_filter_data= ip_filter_table['result'] if ip_filter_table['success'] == 0 and len(ip_filter_table['result']) > 0 else []
        mac_filter_table=odu100_mac_packet_table(host_id)
        mac_filter_data= mac_filter_table['result'] if mac_filter_table['success'] == 0 and len(mac_filter_table['result']) > 0 else []
        filter_status_result = odu100_get_ruconfigtable(host_id)
        filter_status_field = filter_status_result['result'] if filter_status_result['success'] == 0 and len(filter_status_result['result']) > 0 else []
        
        tab_str = ''
        tab_str += "<div id=\"content_9\" class=\"tab-content form-div\" style=\"margin-bottom: 0px; margin-top: 26px; display: block;\">\
                            <div class=\"yo-tabs\" id=\"sub_config_tabs\" style=\"margin:10px 0\">\
                                <ul>\
                                    <li><a href=\"#content9_1\">IP Filter</a></li>\
                                    <li><a href=\"#content9_2\">MAC Filter</a></li>\
                                    <li><a href=\"#content9_3\">Filter Mode</a></li>\
                                </ul>\
                        <div id=\"content9_1\" class=\"tab-content\">\
                        <div style=\"width:auto;\">"
        tab_str+="<form action=\"ip_packet_filter.py\" method=\"get\" id=\"ip_packet_filter_form\" name=\"ip_packet_filter_form\">\
                    <div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl-small\">Index</label><label class=\"lbl\">IP Address</label><label class=\"lbl\">NetMask Address</label>\
                        </div>"
        for i in xrange(1, 9):
            tab_str += "\
                            <div class=\"row-elem\">\
                                <label class=\"lbl-small\">%i</label>\
                                <input type=\"text\" name=\"ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s\" id=\"ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s\" field=\"sys_omc_register_contact_email\" value=\"%s\" style=\"width: 100px;\" />\
                                <input type=\"text\" name=\"ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s\" id=\"ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s\" field=\"sys_omc_register_contact_email\" value=\"%s\" style=\"width: 100px;\"/>\
                            </div>" % (i,i,i,ip_filter_data[i-1].ipFilterIpAddress if len(ip_filter_data) > 0 else "", 
                                  i,i,ip_filter_data[i-1].ipFilterNetworkMask if len(ip_filter_data) > 0 else "")
        tab_str += "\
                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('ip_packet_filter_form',this)\" class=\"yo-small yo-button\"/>\
                                <input type =\"button\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"odu100CommonFormSubmit('ip_packet_filter_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"button\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"odu100CommonFormSubmit('ip_packet_filter_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('ip_packet_filter_form',this)\" class=\"yo-small yo-button\" />\
                                <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_packet_filter\" tablename=\"ipFilterTable,macFilterTable,ruConfTable\"/>\
                                </div>\
                            </form>\
                        </div>\
                    </div>"%(host_id,selected_device)
        tab_str+="<div id=\"content9_2\" class=\"tab-content\">\
                        <div style=\"width:auto;\">\
                    <form action=\"mac_packet_filter.py\" method=\"get\" id=\"mac_packet_filter_form\" name=\"mac_packet_filter_form\">\
                        <div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl-small\">Index</label><label class=\"lbl\">MAC Address</label>\
                        </div>"
        for i in xrange(1, 9):
            tab_str += "\
                            <div class=\"row-elem\">\
                                <label class=\"lbl-small\">%i</label>\
                                <input type=\"text\" name=\"ru.packetFilters.macFilterTable.filterMacAddress.%s\" id=\"ru.packetFilters.macFilterTable.filterMacAddress.%s\" field=\"sys_omc_register_contact_email\" value=\"%s\" style=\"width: 100px;\"/>\
                            </div>" % (i,i,i,mac_filter_data[i-1].filterMacAddress if len(mac_filter_data) > 0 else "")
        tab_str += "\
                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('mac_packet_filter_form',this)\" class=\"yo-small yo-button\"/>\
                                <input type =\"button\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"odu100CommonFormSubmit('mac_packet_filter_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"button\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"odu100CommonFormSubmit('mac_packet_filter_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('mac_packet_filter_form',this)\" class=\"yo-small yo-button\" />\
                                <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_packet_filter\" tablename=\"ipFilterTable,macFilterTable,ruConfTable\"/>\
                                </div>\
                            </form>\
                        </div>\
                    </div>\
                    <div id=\"content9_3\" class=\"tab-content\">\
                        <div>\
                        <form action=\"packet_filter_mode.py\" method=\"get\" id=\"packet_filter_mode_form\" name=\"packet_filter_mode_form\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl lbl-big\">Filter Mode</label>\
                                %s\
                            </div>\
                            <div class=\"row-elem\">\
                                <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('packet_filter_mode_form',this)\" class=\"yo-small yo-button\"/>\
                                <input type =\"button\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"odu100CommonFormSubmit('packet_filter_mode_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"button\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"odu100CommonFormSubmit('packet_filter_mode_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('packet_filter_mode_form',this)\" class=\"yo-small yo-button\" />\
                                <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_packet_filter\" tablename=\"ipFilterTable,macFilterTable,ruConfTable\"/>\
                            </div>\
                        </form>\
                       </div>\
                    </div>\
               </div>\
            </div>"%(host_id,selected_device,self.odu100_select_list_object.packet_filter_select_list(str(0 if filter_status_field[0][6] == None else filter_status_field[0][6]), "enabled", "ru.ruConfTable.ethFiltering", "false", "Filter Mode"),host_id,selected_device)
        return tab_str
    
    
    def odu100_channel_configuration(self, host_id, selected_device, i = 0):
        global html
        obj_get_data = IduGetData()
        channel_config_table_data = odu100_get_channelConfig(host_id)
        ru_config_table_data = odu100_get_ruconfigtable(host_id)
        ru_configuration = ru_config_table_data["result"]
        channel_configuration = channel_config_table_data["result"]     
        ra_channel_list = []
        ra_channel_list = obj_get_data.common_get_data_by_host('Odu100RaChannelListTable', host_id)
        str_form = ""        
        if len(ra_channel_list) == 0 and i == 0 or i == 2:
            str_form += "\
                    <form action=\"channel_configuration.py\" method=\"get\" id=\"channel_configuration_form\">"
            for j in range(0, 10):
                str_form += "<div class=\"row-elem\" style=\"align:center\">\
                                    \
                                    %s\
                                </div>" % (self.odu100_select_list_object.preffered_channel_select_list((0 if channel_configuration[j].rafrequency == None or channel_configuration[j].rafrequency == "" else channel_configuration[j].rafrequency), "disabled" if i == 2 or len(ra_channel_list) == 0 else "enabled", 'RU.RA.PrefRfChanFreq.frequency.%s' % (j + 1), "false", "Channel list", host_id, selected_device))
            str_form += "<div class=\"row-elem\">\
                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" disabled=\"disabled\"/>\
                            <input type =\"button\" name =\"refresh_channel\" id=\"refresh_channel\" value=\"Channel List Reconciliation\"  onClick=\"refreshchannelList();\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                            <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                            <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                            <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                            <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_channel_configuration\" tablename=\"raPreferredRFChannelTable\"/>\
                    </div>\
                        </form>" % (host_id, selected_device)
        else:
            bw = 0

            str_form += "\
                        <form action=\"channel_configuration.py\" method=\"get\" id=\"channel_configuration_form\">"
            if int(i) == 1:
                result = refresh_channel_freq_list_table(host_id, selected_device)
                #html.write(str(result))
                #return str(result)
                if result['success'] == 1:
                    for j in range(0, 10):
                        str_form += "<div class=\"row-elem\" style=\"align:center\">\
                                            \
                                            %s\
                                        </div>" % (self.odu100_select_list_object.default_preffered_channel_select_list(0, "disabled", 'RU.RA.PrefRfChanFreq.frequency.%s' % (j + 1), "false", "Channel List"))
                    str_form += "<div class=\"row-elem\">\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" disabled=\"disabled\"/>\
                                    <input type =\"button\" name =\"refresh_channel\" id=\"refresh_channel\" value=\"Channel List Reconciliation\"  onClick=\"refreshchannelList()\" class=\"yo-small yo-button\" />\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                    <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                    <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                    <input type = \"hidden\" name = \"status_msg\" value=\"1\" />\
                                    <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_channel_configuration\" tablename=\"raPreferredRFChannelTable\"/>\
                            </div>\
                                </form>" % (host_id, selected_device)
##                    if len(ru_configuration)>0:
##                        if int(ru_configuration[0].channelBandwidth) ==0 or int(ru_configuration[0].channelBandwidth) == 1 or int(ru_configuration[0].channelBandwidth) ==2:
##                            bw = 1
##                        else:
##                            bw = 2
##                    if len(channel_configuration)>0:
##                        for i in range(0,10):
##                            str_form+="<div class=\"row-elem\" style=\"align:center\">\
##                                            \
##                                            %s\
##                                        </div>"%(self.odu100_select_list_object.preffered_channel_select_list10((0 if channel_configuration[i].rafrequency==None or channel_configuration[i].rafrequency=="" else channel_configuration[i].rafrequency),"enabled",'RU.RA.PrefRfChanFreq.frequency.%s'%(i+1),"false","Channel list") if bw==1 else self.odu100_select_list_object.preffered_channel_select_list40((0 if channel_configuration[i].rafrequency==None else channel_configuration[i].rafrequency),"enabled",'RU.RA.PrefRfChanFreq.frequency.%s'%(i+1),"false","Channel List"))            
##                        str_form+="<div class=\"row-elem\">\
##                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\"/>\
##                                        <input type =\"submit\" name =\"refresh_channel\" id=\"refresh_channel\" value=\"Channel List Reconciliation\"  onClick=\"return refreshchannelList()\" class=\"yo-small yo-button\" />\
##                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
##                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
##                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
##                                        <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
##                                        <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
##                                </div>\
##                                    </form>"%(host_id,selected_device)
##                       
##                    else:
##                        for i in range(0,10):
##                            str_form+="<div class=\"row-elem\">\
##                                            <label class=\"lbl lbl-big\">%s</label>\
##                                            %s\
##                                        </div>"%(i+1,self.odu100_select_list_object.preffered_channel_select_list((0,"enabled",'RU.RA.PrefRfChanFreq.frequency.%s'%(i+1),"false","Channel List")))            
##                        str_form+="<div class=\"row-elem\">\
##                                        <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\"/>\
##                                        <input type =\"submit\" name =\"refresh_channel\" id=\"refresh_channel\" value=\"Channel List Reconciliation\"  onClick=\"return refreshchannelList()\" class=\"yo-small yo-button\" />\
##                                        <input type =\"submit\" name =\"odu100_submit\"  id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
##                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
##                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
##                                        <input type = \"hidden\" name = \"raacl_index\" value=\"%s\" style=\"Display:None\"/>\
##                                        <input type = \"hidden\" name = \"host_id\" value=\"\" style=\"Display:None\"/>\
##                                        <input type = \"hidden\" name = \"device_type\" value=\"\" />\
##                                        <input type = \"hidden\" name = \"total_rows\" value=\"%s\" id=\"total_rows\"/>\
##                                </div>\
##                                    </form>"%(host_id,selected_device)
                else:              
                    for j in range(0, 10):
                        str_form += "<div class=\"row-elem\" style=\"align:center\">\
                                            \
                                            %s\
                                        </div>" % (self.odu100_select_list_object.preffered_channel_select_list_snmp((0 if channel_configuration[j].rafrequency == None or channel_configuration[j].rafrequency == "" or int(channel_configuration[j].rafrequency) == 0 else str(channel_configuration[j].rafrequency)), "disabled" if len(ra_channel_list) == 0 else "enabled", 'RU.RA.PrefRfChanFreq.frequency.%s' % (j + 1), "false", "Channel list"))             
                    str_form += "<div class=\"row-elem\">\
                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\"/>\
                                        <input type =\"button\" name =\"refresh_channel\" id=\"refresh_channel\" value=\"Channel List Reconciliation\"  onClick=\"refreshchannelList()\" class=\"yo-small yo-button\" />\
                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                        <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                        <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                        <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                        <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_channel_configuration\" tablename=\"raPreferredRFChannelTable\"/>\
                                </div>\
                                    </form>" % (host_id, selected_device)
            else:
                for j in range(0, 10):
                    str_form += "<div class=\"row-elem\" style=\"align:center\">\
                                        \
                                        %s\
                                    </div>" % (self.odu100_select_list_object.preffered_channel_select_list((0 if channel_configuration[j].rafrequency == None or channel_configuration[j].rafrequency == "" else channel_configuration[j].rafrequency), "disabled" if len(ra_channel_list) == 0 else "enabled", 'RU.RA.PrefRfChanFreq.frequency.%s' % (j + 1), "false", "Channel list", host_id, selected_device))             
                str_form += "<div class=\"row-elem\">\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\"/>\
                                    <input type =\"button\" name =\"refresh_channel\" id=\"refresh_channel\" value=\"Channel List Reconciliation\"  onClick=\"refreshchannelList()\" class=\"yo-small yo-button\" />\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                    <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('channel_configuration_form',this)\" class=\"yo-small yo-button\" />\
                                    <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                    <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                    <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"odu100_channel_configuration\" tablename=\"raPreferredRFChannelTable\"/>\
                            </div>\
                                </form>" % (host_id, selected_device)
        return str_form#####################################################################################################################################

    def site_survey_form(self, site_survey_record):
        form_str = ""
        form_str += "<div id=\"site_survey_result\">\
                        <table id=\"site_survey_table\" name=\"site_survey_table\" class=\"yo-table\" style=\"width:100%\" cellspacing=\"0\" cellpadding=\"0\">\
                        <tr>\
                            <th>ScanIndex</th>\
                            <th>RF Channel Frequency</th>\
                            <th>Avg Num CRC Errors</th>\
                            <th>Max RSL CRC Errors</th>\
                            <th>Avg Num PHY Errors</th>\
                            <th>Max RSL PHY Errors</th>\
                            <th>Max RSL Valid Frames</th>\
                            <th>Channel Number</th>\
                            <th>Noise Floor</th>\
                        </tr>\
                    "
        if len(site_survey_record) > 0 or site_survey_record != []:
            for i in range(0, len(site_survey_record)):
                form_str += "<tr>\
                                \
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                            </tr>" % (site_survey_record[i].scanIndex, site_survey_record[i].rfChannelFrequency, \
                                    site_survey_record[i].numCrcErrors, site_survey_record[i].maxRslCrcError, site_survey_record[i].numPhyErrors, \
                                    site_survey_record[i].maxRslPhyError, \
                                    site_survey_record[i].maxRslValidFrames, site_survey_record[i].channelnumber, site_survey_record[i].noiseFloor)
        else:
            form_str += "<tr>\
                            <td colspan=\"9\">No Data Exist</td>\
                        </tr>"

        form_str += "</table></div>"
        return str(form_str)


    def bw_form(self, host_id, device_type):
        str_form = ""
        tx_rate = ""
        tx_time = ""
        tx_bw = ""
        bw_result = bw_get_value(host_id, device_type)
        if bw_result['success'] == 0:
            if bw_result['result'] == {}:
                pass
            else:
                tx_rate = bw_result['result']['tx_rate']
                tx_time = bw_result['result']['tx_time']
                tx_bw = bw_result['result']['tx_bw']

        str_form += "\
                    <form action=\"bw_action.py\" method=\"get\" id=\"bw_action_form\" name=\"bw_action_form\" style=\"overflow:hidden;\">\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TX Rate(kbps)</label>\
                            <input type=\"text\" name=\"tx_rate\" id=\"tx_rate\" value=\"%s\"/>\
                            <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 300000</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TX Time(usec)</label>\
                            <input type=\"text\" name=\"tx_time\" id=\"tx_time\" value=\"%s\"/>\
                            <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 4000</span>\
                        </div>\
                        <div class=\"row-elem\">\
                            <label class=\"lbl lbl-big\">TX BW(kbps)</label>\
                            <input type=\"text\" name=\"tx_bw\" id=\"tx_bw\" readonly=\"readonly\" value=\"%s\"/>\
                        </div>\
                        <div class=\"row-elem\">\
                            <input type =\"submit\" name =\"odu100_bw_submit\"  id=\"odu100_bw_submit_save\" value=\"BW Calculator\" onClick=\"return odu100BWCalc('bw_action_form','%s','%s')\" class=\"yo-small yo-button\"/>\
                        </div>\
                    </form>" % (tx_rate, tx_time, tx_bw, host_id, device_type)
        return str_form


    def llc_config(self, host_id, device_type):
        """
        Author - Anuj Samariya
        This function is displaying form of LLC Configuration 
        h -  is used for request
        host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
        it displays the forms on page
        """
        str_form = ""
    ############### Values get from the database by calling the function ra_llc_conf_table_get(host_id) ##################################
    # RaLlc Configuration get Method-----------------------------------------------
        odu100_llc_config_form = ""
        llc_config_table_data = odu100_get_llcconfigtable(host_id)
        ra_llc_config = llc_config_table_data["result"]
    #--------------------------------------------------------------------------
        str_form += "<form action=\"llc_configuration.py\" method=\"get\" id=\"llc_config_form\" name=\"llc_config_form\">\
                        <div id=\"llc_config_form_parmeters_container\" name=\"llc_config_form_parmeters_container\">\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Retransmit Window Size(High)</label>\
                                <input type=\"text\" name=\"ru.ra.llc.raLlcConfTable.arqWinHigh\" id=\"ru.ra.llc.raLlcConfTable.arqWinHigh\" value=\"%s\"/>\
                                <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 5</span>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Retransmit Window Size(Low)</label>\
                                <input type=\"text\" name=\"ru.ra.llc.raLlcConfTable.arqWinLow\" id=\"ru.ra.llc.raLlcConfTable.arqWinLow\" value=\"%s\"/>\
                                <span style=\"font-size:9px\">&nbsp;&nbsp;0 to 5</span>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Frame Loss Threshold</label>\
                                <input type=\"text\" name=\"ru.ra.llc.raLlcConfTable.frameLossThreshold\" id=\"ru.ra.llc.raLlcConfTable.frameLossThreshold\" value=\"%s\"/>\
                                <span style=\"font-size:9px\">&nbsp;&nbsp;1 to 429497295</span>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Leaky Bucket Timer</label>\
                                <input type=\"text\" name=\"ru.ra.llc.raLlcConfTable.leakyBucketTimerVal\" id=\"ru.ra.llc.raLlcConfTable.leakyBucketTimerVal\" value=\"%s\"/>\
                                <span style=\"font-size:9px\">&nbsp;&nbsp;1 to 60</span>\
                            </div>\
                            <div class=\"row-elem\">\
                                <label class=\"lbl\">Frame Loss Timeout</label>\
                                <input type=\"text\" name=\"ru.ra.llc.raLlcConfTable.frameLossTimeout\" id=\"ru.ra.llc.raLlcConfTable.frameLossTimeout\" value=\"%s\"/>\
                                <span style=\"font-size:9px\">&nbsp;&nbsp;30 to 600</span>\
                            </div>\
                            <div class=\"row-elem\">\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_submit_save\" value=\"Save\" onClick=\"return odu100CommonFormSubmit('llc_config_form',this)\" class=\"yo-small yo-button\"/>\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('llc_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_cancel\" value=\"Cancel\" style=\"Display:None\"  onClick=\"return odu100CommonFormSubmit('llc_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type =\"submit\" name =\"odu100_submit\" id=\"id_omc_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return odu100CommonFormSubmit('llc_config_form',this)\" class=\"yo-small yo-button\" />\
                                <input type = \"hidden\" name = \"host_id\" value=\"%s\"/>\
                                <input type = \"hidden\" name = \"device_type\" value=\"%s\" />\
                                <input type = \"hidden\" id=\"common_rec\" name=\"common_rec\" form_name=\"llc_config\" tablename=\"raLlcConfTable\"/>\
                            </div>\
                        </div>\
                    </form>" % ("" if len(ra_llc_config) == 0 else "" if ra_llc_config[0].arqWinHigh == None else ra_llc_config[0].arqWinHigh, \
                              "" if len(ra_llc_config) == 0 else "" if ra_llc_config[0].arqWinLow == None else ra_llc_config[0].arqWinLow, \
                              "" if len(ra_llc_config) == 0 else "" if ra_llc_config[0].frameLossThreshold == None else ra_llc_config[0].frameLossThreshold, \
                              "" if len(ra_llc_config) == 0 else "" if ra_llc_config[0].leakyBucketTimerVal == None else ra_llc_config[0].leakyBucketTimerVal, \
                              "" if len(ra_llc_config) == 0 else "" if ra_llc_config[0].frameLossTimeout == None else ra_llc_config[0].frameLossTimeout, \
                              "" if host_id == None else host_id, "" if device_type == None else device_type)
        return str_form






######################################Actions of Forms For odu100 forms #############################################################

def bw_action(h):
    global html, host_status_dic, obj_essential
    html = h
    dic_result = {'success':0, 'result':{}}
    flag = 0
    host_id = html.var("hostId")
    device_type = html.var("deviceType")
    try:
        host_op_status = obj_essential.get_hoststatus(host_id)
        #
        if host_op_status == None or host_op_status == 0:
            if host_id == None or device_type == None:
                dic_result['success'] = 1
                dic_result['result'] = "Host Not Exist"
                flag = 1
            else:
                obj_essential.host_status(host_id, 7)
                if html.var("tx_rate") != None:
                    if Validation.is_required(html.var("tx_rate")):
                        if Validation.is_number(html.var("tx_rate")):
                            if int(html.var("tx_rate")) >= 0 and int(html.var("tx_rate")) <= 300000:
                                dic_result["tx_rate"] = html.var("tx_rate")
                            else:
                                flag = 1
                                dic_result["result"] = "TX Rate must be in between 0 and 300000"
                        else:
                            flag = 1
                            dic_result["result"] = "TX Rate must be number"
                    else:
                        flag = 1
                        dic_result["result"] = "TX Rate is required"
                if html.var("tx_time") != None:
                    if Validation.is_required(html.var("tx_time")):
                        if Validation.is_number(html.var("tx_time")):
                            if int(html.var("tx_time")) >= 0 and int(html.var("tx_time")) <= 4000:
                                dic_result["tx_time"] = html.var("tx_time")
                            else:
                                flag = 1
                                dic_result["result"] = "TX Time must be in between 0 and 4000"
                        else:
                            flag = 1
                            dic_result["result"] = "TX Time must be number"
                    else:
                        flag = 1
                        dic_result["result"] = "TX Time is required"

            if flag == 1:
                dic_result['success'] = 1
                html.req.content_type = 'application/json'
                html.req.write(str(JSONEncoder().encode(dic_result)))

            else:
                result = bw_calc(host_id, device_type, dic_result)        
                html.req.content_type = 'application/json'
                html.req.write(str(JSONEncoder().encode(result)))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))

    finally:        
        obj_essential.host_status(host_id, 0, None, 7)

def sys_registration_configuration(h):
    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 12)
            if html.var("odu100_submit") == "Save" or html.var("odu100_submit") == "Retry" or html.var("odu100_submit") == "":
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["result"] = "Host does not exist"
                    flag = 1
                else:
                    if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr") != None:
                        if Validation.is_required(html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr")):
                            dic_result["ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr")
                        else:
                            flag = 1
                            dic_result["result"] = "Address is required field"
                    if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson") != None:
                        if Validation.is_required(html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson")):
                            dic_result["ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson")
                        else:
                            flag = 1
                            dic_result["result"] = "Contact Person is required field"
                    if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile") != None:
                        if Validation.is_required(html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile")):
                            dic_result["ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile")
                        else:
                            flag = 1
                            dic_result["result"] = "Mobile is required field"
                    if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact") != None:
                        if Validation.is_required(html.var("ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact")):
                            dic_result["ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact")
                        else:
                            flag = 1
                            dic_result["result"] = "Alternate Contact is required field"
                    if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail") != None:
                        if Validation.is_required(html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail")):
                            dic_result["ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail")
                        else:
                            flag = 1
                            dic_result["result"] = "Email is required field"
                    if flag == 1:
                        dic_result["success"] = 1
                        html.write(str(dic_result))
                    else:
                        dic_result["success"] = 0

                        result = controller_validation(host_id, device_type_id, dic_result)
                        html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr") != None:
                    dic_result["result"]["ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactAddr")
                if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson") != None:
                    dic_result["result"]["ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactPerson")
                if html.var("RU.SysOmcRegistrationTable.sysOmcRegistercontactMobile") != None:
                    dic_result["result"]["ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile")
                if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactMobile") != None:
                    dic_result["result"]["ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact")
                if html.var("ru.sysOmcRegistrationTable.sysOmcRegisterAlternateContact") != None:
                    dic_result["result"]["ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail"] = html.var("ru.sysOmcRegistrationTable.sysOmcRegisterContactEmail")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Ok":
                html.write("ok")
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def odu100_omc_config(h):

    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """

    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            if html.var("odu100_submit") == "Save":
                obj_essential.host_status(host_id, 12)
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["host_id"] = "Host does not exist"
                    flag = 1
                else:                    
                    if Validation.is_required(html.var("ru.omcConfTable.periodicStatsTimer")):
                        if Validation.is_number(html.var("ru.omcConfTable.periodicStatsTimer")):
                            dic_result["ru.omcConfTable.periodicStatsTimer"] = html.var("ru.omcConfTable.periodicStatsTimer")
                        else:
                            flag = 1 
                            dic_result["Periodic Stats Timer"] = "It Must be Integer"
                    else:
                        dic_result["Periodic Stats Timer"] = "Periodic stats timer is required"
                        flag = 1
                    if Validation.is_required(html.var("ru.omcConfTable.omcIpAddress")):
                        if Validation.is_valid_ip(html.var("ru.omcConfTable.omcIpAddress")):
                            dic_result["ru.omcConfTable.omcIpAddress"] = html.var("ru.omcConfTable.omcIpAddress")
                        else: 
                            flag = 1
                            dic_result["Unmp Ip Address"] = "Ip is not valid IP"
                    else:
                        flag = 1
                        dic_result["Unmp Ip Address"] = "Ip value is required"
                    if flag == 1:
                        dic_result["success"] = 1
                        html.write(str(dic_result))
                    else:
                        dic_result["success"] = 0
                        result = controller_validation(host_id, device_type_id, dic_result)
                        html.write(str(result))
            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "":
                obj_essential.host_status(host_id, 12) 
                if html.var("ru.omcConfTable.periodicStatsTimer") != None:
                    dic_result["ru.omcConfTable.periodicStatsTimer"] = html.var("ru.omcConfTable.periodicStatsTimer")
                if html.var("ru.omcConfTable.omcIpAddress") != None:
                    dic_result["ru.omcConfTable.omcIpAddress"] = html.var("ru.omcConfTable.omcIpAddress")
                dic_result["success"] = 0
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                if html.var("ru.omcConfTable.periodicStatsTimer") != None:
                    dic_result["result"]["ru.omcConfTable.periodicStatsTimer"] = html.var("ru.omcConfTable.periodicStatsTimer")
                if html.var("ru.omcConfTable.omcIpAddress") != None:
                    dic_result["result"]["ru.omcConfTable.omcIpAddress"] = html.var("ru.omcConfTable.omcIpAddress")


                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Ok":
                html.write("ok")
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))

    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def odu100_sync_config(h):    
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            if html.var("odu100_submit") == "Save":
                obj_essential.host_status(host_id, 12)
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["host_id"] = "Host does not exist"
                    flag = 1
                else:
                    if html.var("ru.syncClock.syncConfigTable.rasterTime") != None:
                        if Validation.is_required(html.var("ru.syncClock.syncConfigTable.rasterTime")):
                            dic_result["ru.syncClock.syncConfigTable.rasterTime"] = html.var("ru.syncClock.syncConfigTable.rasterTime")
                        else:
                            dic_result["Raster Time"] = "Please Select a value in Raster time"
                            flag = 1
                    if Validation.is_required(html.var("ru.syncClock.syncConfigTable.syncLossThreshold")):
                        if Validation.is_number(html.var("ru.syncClock.syncConfigTable.syncLossThreshold")):
                            dic_result["ru.syncClock.syncConfigTable.syncLossThreshold"] = html.var("ru.syncClock.syncConfigTable.syncLossThreshold")
                        else:
                            flag = 1 
                            dic_result["Sync Loss Threshold"] = "It Must be Integer"
                    else:
                        dic_result["Sync Loss Threshold"] = "Sync Loss Threshold is required"
                        flag = 1    
                    if Validation.is_required(html.var("ru.syncClock.syncConfigTable.leakyBucketTimer")):
                        if Validation.is_number(html.var("ru.syncClock.syncConfigTable.leakyBucketTimer")):
                            dic_result["ru.syncClock.syncConfigTable.leakyBucketTimer"] = html.var("ru.syncClock.syncConfigTable.leakyBucketTimer")
                        else:
                            flag = 1 
                            dic_result["Leaky bucket Timer"] = "It Must be Integer"
                    else:
                        dic_result["Leaky bucket Timer"] = "Sync Loss Threshold is required"
                        flag = 1    

                    if Validation.is_required(html.var("ru.syncClock.syncConfigTable.syncLostTimeout")):
                        if Validation.is_number(html.var("ru.syncClock.syncConfigTable.syncLostTimeout")):
                            dic_result["ru.syncClock.syncConfigTable.syncLostTimeout"] = html.var("ru.syncClock.syncConfigTable.syncLostTimeout")
                        else:
                            flag = 1 
                            dic_result["Sync Loss Timeout"] = "Sync Lost Timeout Must be Integer"
                    else:
                        dic_result["Sync Loss Timeout"] = "Sync Loss Timeout is required"
                        flag = 1    
                    if html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust") != None:
                        if Validation.is_required(html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust")):
                            if Validation.is_number(html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust")):
                                dic_result["ru.syncClock.syncConfigTable.syncConfigTimerAdjust"] = html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust")
                            else:
                                flag = 1 
                                dic_result["Sync Timer Adjust"] = "Sync Timer Adjust Must be Integer"
                        else:
                            dic_result["Sync Timer Adjust"] = "Sync Timer Adjust is required"
                            flag = 1    
                    if html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime") != None:
                        if Validation.is_required(html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime")):
                            if Validation.is_number(html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime")):
                                dic_result["ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime"] = html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime")
                            else:
                                flag = 1 
                                dic_result["Percentage Downlink"] = "Percentage Downlink Must be Integer"
                        else:
                            dic_result["Percentage Downlink"] = "Sync timer Adjust is required"
                            flag = 1    
                    if flag == 1:
                        dic_result["success"] = 1
                        html.write(str(dic_result))
                    else:
                        dic_result["success"] = 0
                        result = controller_validation(host_id, device_type_id, dic_result)
                        html.write(str(result))
                        #html.write(str(dic_result))

            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "": 
                obj_essential.host_status(host_id, 12)
                if html.var("ru.syncClock.syncConfigTable.rasterTime") != None:
                    dic_result["ru.syncClock.syncConfigTable.rasterTime"] = html.var("ru.syncClock.syncConfigTable.rasterTime")
                if html.var("ru.syncClock.syncConfigTable.syncLossThreshold") != None:
                    dic_result["ru.syncClock.syncConfigTable.syncLossThreshold"] = html.var("ru.syncClock.syncConfigTable.syncLossThreshold")
                if html.var("ru.syncClock.syncConfigTable.leakyBucketTimer") != None:
                    dic_result["ru.syncClock.syncConfigTable.leakyBucketTimer"] = html.var("ru.syncClock.syncConfigTable.leakyBucketTimer")
                if html.var("ru.syncClock.syncConfigTable.syncLostTimeout") != None:
                    dic_result["ru.syncClock.syncConfigTable.syncLostTimeout"] = html.var("ru.syncClock.syncConfigTable.syncLostTimeout")
                if html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust") != None:
                    dic_result["ru.syncClock.syncConfigTable.syncConfigTimerAdjust"] = html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust")
                if html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime") != None:
                    dic_result["ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime"] = html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime")
                dic_result["success"] = 0
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                dic_result["result"]["ru.syncClock.syncConfigTable.rasterTime"] = html.var("ru.syncClock.syncConfigTable.rasterTime")
                dic_result["result"]["ru.syncClock.syncConfigTable.syncLossThreshold"] = html.var("ru.syncClock.syncConfigTable.syncLossThreshold")
                dic_result["result"]["ru.syncClock.syncConfigTable.leakyBucketTimer"] = html.var("ru.syncClock.syncConfigTable.leakyBucketTimer")
                dic_result["result"]["ru.syncClock.syncConfigTable.syncLostTimeout"] = html.var("ru.syncClock.syncConfigTable.syncLostTimeout")
                dic_result["result"]["ru.syncClock.syncConfigTable.syncConfigTimerAdjust"] = html.var("ru.syncClock.syncConfigTable.syncConfigTimerAdjust")
                dic_result["result"]["ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime"] = html.var("ru.syncClock.syncConfigTable.percentageDownlinkTransmitTime")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))
            elif html.var("odu100_submit") == "Ok":
                html.write("ok")
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)
def odu100_ip_config(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html
        html = h
        dic_result = {}
        flag = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        if html.var("odu100_submit") == "Save":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["host_id"] = "Host does not exist"
                flag = 1
            else:
                if html.var("ru.ipConfigTable.ipAddress") != None:
                    if Validation.is_required(html.var("ru.ipConfigTable.ipAddress")):
                        if Validation.is_valid_ip(html.var("ru.ipConfigTable.ipAddress")):
                            dic_result["ru.ipConfigTable.ipAddress"] = html.var("ru.ipConfigTable.ipAddress")
                        else: 
                            flag = 1
                            dic_result["IpAddress"] = "IpAddress is not valid"
                    else:
                        flag = 1
                        dic_result["IpAddress"] = "IpAddress is required"
                if Validation.is_required(html.var("ru.ipConfigTable.ipNetworkMask")):
                    if Validation.is_valid_ip(html.var("ru.ipConfigTable.ipNetworkMask")):
                        dic_result["ru.ipConfigTable.ipNetworkMask"] = html.var("ru.ipConfigTable.ipNetworkMask")
                    else: 
                        flag = 1
                        dic_result["IpNetworkmask"] = "IpNetworkMask is not valid"
                else:
                    flag = 1
                    dic_result["IpNetworkmask"] = "IpNetworkMask required"
                if Validation.is_required(html.var("ru.ipConfigTable.ipDefaultGateway")):
                    if Validation.is_valid_ip(html.var("ru.ipConfigTable.ipDefaultGateway")):
                        dic_result["ru.ipConfigTable.ipDefaultGateway"] = html.var("ru.ipConfigTable.ipDefaultGateway")
                    else: 
                        flag = 1
                        dic_result["IpDefaultGateway"] = "IpDefault Gateway is not valid"
                else:
                    flag = 1
                    dic_result["IpDefaultGateway"] = "IpDefault Gateway is required"
                if html.var("ru.ipConfigTable.autoIpConfig") != None:
                    if Validation.is_required(html.var("ru.ipConfigTable.autoIpConfig")):
                        dic_result["ru.ipConfigTable.autoIpConfig"] = html.var("ru.ipConfigTable.autoIpConfig")
                    else:
                        flag = 1
                        dic_result["DHCP"] = "DHCP is required"
            if flag == 1:
                dic_result["success"] = 1
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))    
        elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "": 
            if html.var("ru.ipConfigTable.ipAddress") != None:
                dic_result["ru.ipConfigTable.ipAddress"] = html.var("ru.ipConfigTable.ipAddress")
            if html.var("ru.ipConfigTable.ipNetworkMask") != None:
                dic_result["ru.ipConfigTable.ipNetworkMask"] = html.var("ru.ipConfigTable.ipNetworkMask")
            if html.var("ru.ipConfigTable.ipDefaultGateway") != None:
                dic_result["ru.ipConfigTable.ipDefaultGateway"] = html.var("ru.ipConfigTable.ipDefaultGateway")
            if html.var("ru.ipConfigTable.autoIpConfig") != None:
                dic_result["ru.ipConfigTable.autoIpConfig"] = html.var("ru.ipConfigTable.autoIpConfig")
            dic_result["success"] = 0
            result = controller_validation(host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("odu100_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = {}
            if html.var("ru.ipConfigTable.ipAddress") != None:
                dic_result["result"]["ru.ipConfigTable.ipAddress"] = html.var("ru.ipConfigTable.ipAddress")
            dic_result["result"]["ru.ipConfigTable.ipNetworkMask"] = html.var("ru.ipConfigTable.ipNetworkMask")
            dic_result["result"]["ru.ipConfigTable.ipDefaultGateway"] = html.var("ru.ipConfigTable.ipDefaultGateway")
            dic_result["result"]["ru.ipConfigTable.autoIpConfig"] = html.var("ru.ipConfigTable.autoIpConfig")
            result = odu100_common_cancel(host_id, device_type_id, dic_result)
            html.write(str(result))
        elif html.var("odu100_submit") == "Ok":
            html.write("ok")

    except Exception as e:
        html.write(str(e[-1]))

def odu100_ra_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        timeslot_chk = 0
        timeslot = 0
        indicate = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            if html.var("odu100_submit") == "Save":
                obj_essential.host_status(host_id, 12)
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["host_id"] = "Host does not exist"
                    flag = 1
                else:
                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.numSlaves") != None:
                            if Validation.is_required(html.var("ru.ra.raConfTable.numSlaves")):
                                if int(html.var("ru.ra.raConfTable.numSlaves")) == 1:
                                    if html.var("ru.ra.raConfTable.guaranteedBroadcastBW") != None:
                                        if int(html.var("ru.ra.raConfTable.guaranteedBroadcastBW")) > 0:
                                            indicate = 1
                                            dic_result["result"] = "Number of slaves one is not valid if guranteedBroadcastBandwidth is non-zero"
##                                    if html.var("ru.ra.raConfTable.dba")!=None:
##                                        if int(html.var("ru.ra.raConfTable.dba"))==1:
##                                            indicate = 1
##                                            dic_result["result"] = "Number of slaves one is not valid if DBA enabled"
                                    if indicate == 0 or indicate == "0":
                                        dic_result["ru.ra.raConfTable.numSlaves"] = html.var("ru.ra.raConfTable.numSlaves")
                                else:
                                    if str(check_timeslot(host_id, int(html.var("ru.ra.raConfTable.numSlaves")))) == '0' or check_timeslot(host_id, int(html.var("ru.ra.raConfTable.numSlaves"))) == '0':
                                        dic_result["ru.ra.raConfTable.numSlaves"] = html.var("ru.ra.raConfTable.numSlaves")
                                    else:
                                        timeslot_chk = 1
                                        timeslot = check_timeslot(host_id, int(html.var("ru.ra.raConfTable.numSlaves")))
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select Number of Slaves"
                        else:
                            flag = 1
                            dic_result["ru.ra.raConfTable.numSlaves"] = "Please Select Number of Slaves"

                    if html.var("ru.ra.raConfTable.ssID") == None:    
                        dic_result["ru.ra.raConfTable.ssID"] = ""
                    else:
                        if len(html.var("ru.ra.raConfTable.ssID"))>=0 and len(html.var("ru.ra.raConfTable.ssID"))<33:
                            dic_result["ru.ra.raConfTable.ssID"]=html.var("ru.ra.raConfTable.ssID")
                        else:
                            flag = 1
                            dic_result["result"]="ssID must be in 0 to 32 character"
                        
                    if html.var("ru.ra.tddMac.raTddMacConfigTable.encryptionType") != None:
                        if Validation.is_required(html.var("ru.ra.tddMac.raTddMacConfigTable.encryptionType")):
                            dic_result["ru.ra.tddMac.raTddMacConfigTable.encryptionType"] = html.var("ru.ra.tddMac.raTddMacConfigTable.encryptionType")
                        else:
                            flag = 1
                            dic_result["result"] = "Please Select Encryption"
                    if html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase") != None:
                        if len(html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase"))>=0 and len(html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase"))<65:
                            dic_result["ru.ra.tddMac.raTddMacConfigTable.passPhrase"]=html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase")
                        else:
                            flag = 1
                            dic_result["result"]="Pass Phrase must be in upto 64 character"
                    else:
                        dic_result["ru.ra.tddMac.raTddMacConfigTable.passPhrase"] = ""
                    if html.var("ru.ra.tddMac.raTddMacConfigTable.txPower") != None:
                        if Validation.is_required(html.var("ru.ra.tddMac.raTddMacConfigTable.txPower")):

                            if Validation.is_number(html.var("ru.ra.tddMac.raTddMacConfigTable.txPower")):
                                dic_result["ru.ra.tddMac.raTddMacConfigTable.txPower"] = html.var("ru.ra.tddMac.raTddMacConfigTable.txPower")
                            else:
                                flag = 1 
                                dic_result["result"] = "Tx Power Must be Integer"
                        else:
                            flag = 1
                            dic_result["Tx Power"] = "Tx power is required"
                    if html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors") != None:    
                        if Validation.is_required(html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors")):
                            if Validation.is_number(html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors")):
                                dic_result["ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors"] = html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors")
                            else:
                                flag = 1 
                                dic_result["result"] = "Max Crc Error Must be Integer"
                        else:
                            flag = 1
                            dic_result["result"] = "Max Crc Error is required"

                    if html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue") != None: 
                        if Validation.is_required(html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue")):
                            if Validation.is_number(html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue")):
                                dic_result["ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue"] = html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue")
                            else:
                                flag = 1 
                                dic_result["result"] = "Leaky Bucket Timer Must be Integer"
                        else:
                            flag = 1
                            dic_result["result"] = "Leaky Bucket Timer is required"
                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.acm") != None:    
                            if Validation.is_required(html.var("ru.ra.raConfTable.acm")):
                                dic_result["ru.ra.raConfTable.acm"] = html.var("ru.ra.raConfTable.acm")
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select ACM "

                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.dba") != None:
                            if Validation.is_required(html.var("ru.ra.raConfTable.dba")):
                                dic_result["ru.ra.raConfTable.dba"] = html.var("ru.ra.raConfTable.dba")
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select DBA "
##                    if int(html.var("node_type"))==0 or int(html.var("node_type"))==2:
##                        if html.var("ru.ra.raConfTable.dba")!=None:
##                            if Validation.is_required(html.var("ru.ra.raConfTable.dba")):
##                                if html.var("ru.ra.raConfTable.numSlaves")!=None:
##                                    if Validation.is_required(html.var("ru.ra.raConfTable.numSlaves")):
##                                        if int(html.var("ru.ra.raConfTable.numSlaves"))==1:
##                                            if int(html.var("ru.ra.raConfTable.dba"))==1:
##                                                flag = 1
##                                                dic_result["result"]="DBA can not be enabled if number of slaves is one" 
##                                            else:
##                                                dic_result["ru.ra.raConfTable.dba"] = html.var("ru.ra.raConfTable.dba")
##                                        else:
##                                            dic_result["ru.ra.raConfTable.dba"] = html.var("ru.ra.raConfTable.dba")
##                                    else:
##                                        flag = 1
##                                         
##                            else:
##                                flag = 1
##                                dic_result["DBA"] = "Please Select DBA "                            

                    if html.var("ru.ra.raConfTable.guaranteedBroadcastBW") != None:
                        if Validation.is_required(html.var("ru.ra.raConfTable.guaranteedBroadcastBW")):
                            if Validation.is_number(html.var("ru.ra.raConfTable.guaranteedBroadcastBW")):
                                if html.var("ru.ra.raConfTable.numSlaves") != None:
                                    if Validation.is_required(html.var("ru.ra.raConfTable.numSlaves")):
                                        if int(html.var("ru.ra.raConfTable.numSlaves")) == 1:
                                            if int(html.var("ru.ra.raConfTable.numSlaves")) == 1 and int(html.var("ru.ra.raConfTable.guaranteedBroadcastBW")) == 0:
                                                dic_result["ru.ra.raConfTable.guaranteedBroadcastBW"] = html.var("ru.ra.raConfTable.guaranteedBroadcastBW")
                                            else:
                                                flag = 1
                                                dic_result["result"] = "Gauranteed Broadcast can not be greater than zero if number of slaves is one"
                                        else:
                                            if int(html.var("ru.ra.raConfTable.numSlaves")) > 1 and int(html.var("ru.ra.raConfTable.guaranteedBroadcastBW")) > 0:
                                                dic_result["ru.ra.raConfTable.guaranteedBroadcastBW"] = html.var("ru.ra.raConfTable.guaranteedBroadcastBW")
                                            else:
                                                flag = 1
                                                dic_result["result"] = "If number of slaves more than one, guaranteed broadcast Bandwidth cant be zero"
                                    else:
                                        flag = 1
                                else:
                                    dic_result["ru.ra.raConfTable.guaranteedBroadcastBW"] = html.var("ru.ra.raConfTable.guaranteedBroadcastBW")
                            else:
                                flag = 1 
                                dic_result["result"] = "GuaranteedBroadcastBW Must be Integer"                       
                        else:
                            flag = 1
                            dic_result["result"] = "GuaranteedBroadcast is required"
                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.acs") != None:
                            if Validation.is_required(html.var("ru.ra.raConfTable.acs")):
                                dic_result["ru.ra.raConfTable.acs"] = html.var("ru.ra.raConfTable.acs")
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select ACS"
                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.dfs") != None:
                            if Validation.is_required(html.var("ru.ra.raConfTable.dfs")):
                                dic_result["ru.ra.raConfTable.dfs"] = html.var("ru.ra.raConfTable.dfs")
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select DFS"   
                    if html.var("ru.ra.raConfTable.antennaPort") != None:
                        if Validation.is_required(html.var("ru.ra.raConfTable.antennaPort")):
                            dic_result["ru.ra.raConfTable.antennaPort"] = html.var("ru.ra.raConfTable.antennaPort")
                        else:
                            flag = 1
                            dic_result["result"] = "Please Select Antenna Port"    
                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.linkDistance") != None:
                            if Validation.is_required(html.var("ru.ra.raConfTable.linkDistance")):
                                dic_result["ru.ra.raConfTable.linkDistance"] = html.var("ru.ra.raConfTable.linkDistance")
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select Link Distance"   

                    if int(html.var("node_type")) == 0 or int(html.var("node_type")) == 2:
                        if html.var("ru.ra.raConfTable.anc") != None:
                            if Validation.is_required(html.var("ru.ra.raConfTable.anc")):
                                dic_result["ru.ra.raConfTable.anc"] = html.var("ru.ra.raConfTable.anc")
                            else:
                                flag = 1
                                dic_result["result"] = "Please Select ANC"

                if flag == 1:
                    dic_result["success"] = 1
                    html.write(str(dic_result))
                elif timeslot_chk == 1 or timeslot_chk == '1':
                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "Remove any pre-configured links on the Removed timeslots. One such exists on Timeslot[%s]" % (timeslot)
                    html.write(str(dic_result))
                else:
                    #html.write(str(dic_result))
                    dic_result["success"] = '0'
                    result = controller_validation(host_id, device_type_id, dic_result)
                    html.write(str(result))
                    

            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "": 
                obj_essential.host_status(host_id, 12)
                if html.var("ru.ra.raConfTable.numSlaves") != None:
                    dic_result["ru.ra.raConfTable.numSlaves"] = html.var("ru.ra.raConfTable.numSlaves")
                if html.var("ru.ra.raConfTable.ssID") != None:
                    dic_result["ru.ra.raConfTable.ssID"] = html.var("ru.ra.raConfTable.ssID")
                if html.var("ru.ra.tddMac.raTddMacConfigTable.encryptionType") != None:
                    dic_result["ru.ra.tddMac.raTddMacConfigTable.encryptionType"] = html.var("ru.ra.tddMac.raTddMacConfigTable.encryptionType")
                if html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase") != None:
                    dic_result["ru.ra.tddMac.raTddMacConfigTable.passPhrase"] = html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase")
                if html.var("ru.ra.tddMac.raTddMacConfigTable.txPower") != None:
                    dic_result["ru.ra.tddMac.raTddMacConfigTable.txPower"] = html.var("ru.ra.tddMac.raTddMacConfigTable.txPower")
                if html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors") != None:
                    dic_result["ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors"] = html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors")
                if html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue") != None:
                    dic_result["ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue"] = html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue")
                if html.var("ru.ra.raConfTable.acm") != None:
                    dic_result["ru.ra.raConfTable.acm"] = html.var("ru.ra.raConfTable.acm")
                if html.var("ru.ra.raConfTable.dba") != None:
                    dic_result["ru.ra.raConfTable.dba"] = html.var("ru.ra.raConfTable.dba")
                if html.var("ru.ra.raConfTable.guaranteedBroadcastBW") != None:
                    dic_result["ru.ra.raConfTable.guaranteedBroadcastBW"] = html.var("ru.ra.raConfTable.guaranteedBroadcastBW")
                if html.var("ru.ra.raConfTable.acs") != None:
                    dic_result["ru.ra.raConfTable.acs"] = html.var("ru.ra.raConfTable.acs")
                if html.var("ru.ra.raConfTable.dfs") != None:
                    dic_result["ru.ra.raConfTable.dfs"] = html.var("ru.ra.raConfTable.dfs")
                dic_result["success"] = 0
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                if html.var("ru.ra.raConfTable.numSlaves") != None:
                    dic_result["result"]["ru.ra.raConfTable.numSlaves"] = html.var("ru.ra.raConfTable.numSlaves")
                dic_result["result"]["ru.ra.raConfTable.ssID"] = html.var("ru.ra.raConfTable.ssID")
                dic_result["result"]["ru.ra.tddMac.raTddMacConfigTable.encryptionType"] = html.var("ru.ra.tddMac.raTddMacConfigTable.encryptionType")
                dic_result["result"]["ru.ra.tddMac.raTddMacConfigTable.passPhrase"] = html.var("ru.ra.tddMac.raTddMacConfigTable.passPhrase")
                dic_result["result"]["ru.ra.tddMac.raTddMacConfigTable.txPower"] = html.var("ru.ra.tddMac.raTddMacConfigTable.txPower")
                dic_result["result"]["ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors"] = html.var("ru.ra.tddMac.raTddMacConfigTable.maxCrcErrors")
                dic_result["result"]["ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue"] = html.var("ru.ra.tddMac.raTddMacConfigTable.leakyBucketTimerValue")
                if html.var("ru.ra.raConfTable.acm") != None:
                    dic_result["result"]["ru.ra.raConfTable.acm"] = html.var("ru.ra.raConfTable.acm")
                if html.var("ru.ra.raConfTable.dba") != None:
                    dic_result["result"]["ru.ra.raConfTable.dba"] = html.var("ru.ra.raConfTable.dba")
                if html.var("ru.ra.raConfTable.guaranteedBroadcastBW") != None:
                    dic_result["result"]["ru.ra.raConfTable.guaranteedBroadcastBW"] = html.var("ru.ra.raConfTable.guaranteedBroadcastBW")
                if html.var("ru.ra.raConfTable.dfs") != None:
                    dic_result["result"]["ru.ra.raConfTable.dfs"] = html.var("ru.ra.raConfTable.dfs")
                dic_result["result"]["ru.ra.raConfTable.dfs"] = html.var("ru.ra.raConfTable.dfs")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Ok":
                html.write("ok")
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(dic_result))
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def odu100_ru_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            if html.var("odu100_submit") == "Save":
                obj_essential.host_status(host_id, 12)
                if Validation.is_required(html.var("ru.ruConfTable.channelBandwidth")):
                    dic_result["ru.ruConfTable.channelBandwidth"] = html.var("ru.ruConfTable.channelBandwidth")
                else:
                    flag = 1
                    dic_result["result"] = "Please Select Channel Bandwidth "

                if html.var("ru.ruConfTable.synchSource") != None:
                    if Validation.is_required(html.var("ru.ruConfTable.synchSource")):
                        dic_result["ru.ruConfTable.synchSource"] = html.var("ru.ruConfTable.synchSource")
                    else:
                        flag = 1
                        dic_result["result"] = "Please Select SynchSource"

                if Validation.is_required(html.var("ru.ruConfTable.countryCode")):
                    dic_result["ru.ruConfTable.countryCode"] = html.var("ru.ruConfTable.countryCode")
                else:
                    flag = 1
                    dic_result["result"] = "Please Select Country Code"
                if html.var("ru.ruConfTable.poeState")!=None:
                    if Validation.is_required(html.var("ru.ruConfTable.poeState")):
                        dic_result["ru.ruConfTable.poeState"] = html.var("ru.ruConfTable.poeState")
                    else:
                        flag = 1
                        dic_result["result"] = "Please Select PoeState"

                if html.var("RU.RUConfTable.alignmentControl") != None:
                    if Validation.is_required(html.var("RU.RUConfTable.alignmentControl")):
                        if Validation.is_number(html.var("RU.RUConfTable.alignmentControl")):
                            dic_result["RU.RUConfTable.alignmentControl"] = html.var("RU.RUConfTable.alignmentControl")
                        else:
                            dic_result["result"] = "Alignment Control should be Number"
                    else:
                        dic_result["result"] = "Alignment Control is required"                

                if flag == 1:
                    dic_result["success"] = 1
                    html.write(str(dic_result))
                else:
                    dic_result["success"] = 0
                    result = controller_validation(host_id, device_type_id, dic_result)
                    html.write(str(result))
                    #html.write(str(dic_result))    

            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "": 
                obj_essential.host_status(host_id, 12)
                if html.var("ru.ruConfTable.channelBandwidth") != None:
                    dic_result["ru.ruConfTable.channelBandwidth"] = html.var("ru.ruConfTable.channelBandwidth")
                if html.var("ru.ruConfTable.synchSource") != None:
                    dic_result["ru.ruConfTable.synchSource"] = html.var("ru.ruConfTable.synchSource")
                if html.var("ru.ruConfTable.countryCode") != None:
                    dic_result["ru.ruConfTable.countryCode"] = html.var("ru.ruConfTable.countryCode")
                if html.var("ru.ruConfTable.poeState") != None:
                    dic_result["ru.ruConfTable.poeState"] = html.var("ru.ruConfTable.poeState")
                if html.var("RU.RUConfTable.alignmentControl") != None:
                    dic_result["RU.RUConfTable.alignmentControl"] = html.var("RU.RUConfTable.alignmentControl")
                dic_result["success"] = 0
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                dic_result["result"]["ru.ruConfTable.channelBandwidth"] = html.var("ru.ruConfTable.channelBandwidth")
                dic_result["result"]["ru.ruConfTable.synchSource"] = html.var("ru.ruConfTable.synchSource")
                dic_result["result"]["ru.ruConfTable.countryCode"] = html.var("ru.ruConfTable.countryCode")
                dic_result["result"]["ru.ruConfTable.poeState"] = html.var("ru.ruConfTable.poeState")
                dic_result["result"]["RU.RUConfTable.alignmentControl"] = html.var("RU.RUConfTable.alignmentControl")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))
            elif html.var("odu100_submit") == "Ok":
                html.write("ok")
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))

    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def odu100_peer_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        timeslot_val = 0
        mac_duplicate_list = []
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        mac_list = []
        mac_accept = 0
        mac_deny = 0
        duplicate = 0
        host_op_status = obj_essential.get_hoststatus(host_id)
        if html.var("odu100_submit") == "Save" :
            if host_op_status == None or host_op_status == 0:
                obj_essential.host_status(host_id, 12)
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["result"] = "Host does not exist"
                    dic_result["success"] = 1
                else:
                    if html.var("timeslot_val") != None:
                        timeslot_val = int(html.var("timeslot_val"))

                        for i in range(0, (timeslot_val)):

                            if html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)) != None:
                                if html.var("acl_val") != None:
                                    if int(html.var("acl_val")) == 1 or int(html.var("acl_val")) == 2:
                                        mac_list.append(html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)))
                                mac_duplicate_list.append(html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)))
                                dic_result["ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1))

                            if html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1)) != None:
                                if Validation.is_required(html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1))):
                                    if Validation.is_number(html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1))):
                                        dic_result["ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1))
                                    else:
                                        flag = 1
                                        dic_result["result"] = "GuaranteedUplinkBW must be number"
                                else:
                                    flag = 1
                                    dic_result["result"] = "GuaranteedUplinkBW is required"
                            if html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1)) != None:
                                if Validation.is_required(html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1))):
                                    if Validation.is_number(html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1))):
                                        dic_result["ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1))
                                    else:
                                        flag = 1
                                        dic_result["result"] = "GuaranteedDownlinkBW must be number"
                                else:
                                    flag = 1
                                    dic_result["result"] = "GuaranteedDownlinkBW is required"
                            if html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1)) != None:
                                if Validation.is_required(html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1))):
                                    if Validation.is_number(html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1))):
                                        dic_result["ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1))
                                    else:
                                        flag = 1
                                        dic_result["result"] = "BasicRateMCSIndex must be number"
                                else:
                                    flag = 1
                                    dic_result["result"] = "BasicRateMCSIndex is required"
                            if html.var("ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1)) != None:
                                if Validation.is_required(html.var("ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1))):
                                    if Validation.is_number(html.var("ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1))):
                                        dic_result["ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1))
                                    else:
                                        flag = 1
                                        dic_result["result"] = "Maximum Uplink must be number"
                                else:
                                    flag = 1
                                    dic_result["result"] = "Maximum Uplink is required"
                            if html.var("ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1)) != None:
                                if Validation.is_required(html.var("ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1))):
                                    if Validation.is_number(html.var("ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1))):
                                        dic_result["ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1))
                                    else:
                                        flag = 1
                                        dic_result["result"] = "Maximum Downlink must be number"
                                else:
                                    flag = 1
                                    dic_result["result"] = "Maximum Downlink is required"
                        if flag == 1:
                            dic_result["success"] = 1
                            html.write(str(dic_result))                
                        else:
                            if chk_mac_duplicacy(mac_duplicate_list) == 0:
                                if int(html.var("acl_val")) == 1:
                                    mac_accept = mac_chk_accept(host_id, mac_list)
                                elif int(html.var("acl_val")) == 2:
                                    mac_deny = mac_chk_deny(host_id, mac_list)
                                    #html.write(str(mac_deny))
                                if mac_accept == 0 and mac_deny == 0 or mac_deny == 2:
                                    dic_result["success"] = 0
                                    #html.write(str(dic_result))
                                    result = peer_set(host_id, device_type_id, timeslot_val, dic_result, 1)
                                    html.write(str(result))
                                    #html.write(str(dic_result)+str(timeslot_val))
                                else:
                                    dic_result = {}
                                    if mac_accept == 1:
                                        dic_result["success"] = 1
                                        dic_result["result"] = "ACL ACCEPT mode PEER MAC should be same as in ACL MAC list"
                                    if mac_deny == 1:
                                        dic_result["success"] = 1
                                        dic_result["result"] = "ACL DENY mode PEER MAC should be different from ACL MAC list"
                                    html.write(str(dic_result))
                            else:
                                duplicate = 1
                            if duplicate == 1:
                                dic_result["success"] = 1
                                dic_result["result"] = "Same MAC Address are not allowed"
                                html.write(str(dic_result))
                    else:
                        dic_result["result"] = "Timeslot Value is not set"
                        dic_result["success"] = 1
                        html.write(str(dic_result))
            else:
                dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..."
                dic_result['success'] = 1
                html.write(str(dic_result))
        elif html.var("odu100_submit") == "Retry" or html.var("odu100_submit") == "":
            if host_op_status == None or host_op_status == 0:
                obj_essential.host_status(host_id, 12)
                if html.var("timeslot_val") != None:
                    timeslot_val = int(html.var("timeslot_val"))
                    for i in range(0, (timeslot_val)):
                        if html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)) != None:
                            if html.var("acl_val") != None:
                                if int(html.var("acl_val")) == 1 or int(html.var("acl_val")) == 2:
                                    mac_list.append(html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)))
                            dic_result["ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1))
                        if html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1)) != None:
                            dic_result["ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1))
                        if html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1)) != None:
                            dic_result["ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1))
                        if html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1)) != None:
                            dic_result["ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1))
                        if html.var("ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1)) != None:
                            dic_result["ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.maxDownlinkBW.%s" % (i + 1))
                        if html.var("ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1)) != None:
                            dic_result["ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.maxUplinkBW.%s" % (i + 1))

                    if int(html.var("acl_val")) == 1:
                        mac_chk_accept(host_id, mac_list)
                    elif int(html.var("acl_val")) == 2:
                        mac_chk_deny(host_id, mac_list)

                    if mac_accept == 0 or mac_deny == 0:
                        dic_result["success"] = 0
                        result = peer_set(host_id, device_type_id, timeslot_val, dic_result, 2)
                        html.write(str(result))
                    else:
                        if mac_accept == 1:
                            dic_result["success"] = 1
                            dic_result["result"] = "ACL ACCEPT mode PEER MAC should be same as in ACL MAC list"
                        if mac_deny == 1:
                            dic_result["success"] = 1
                            dic_result["result"] = "ACL DENY mode PEER MAC should be different from ACL MAC list"
                        html.write(str(dic_result))
                else:
                    dic_result["result"] = "Timeslot Value is not set"
                    dic_result["success"] = 1
                    html.write(str(dic_result))
            else:
                dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..."
                dic_result['success'] = 1
                html.write(str(dic_result))
        if html.var("odu100_submit") == "Cancel":
            for i in range(0, (timeslot_val)):
                if html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)) != None:
                    dic_result["ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.peerMacAddress.%s" % (i + 1))
                if html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1)) != None:
                    dic_result["ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.guaranteedUplinkBW.%s" % (i + 1))
                if html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1)) != None:
                    dic_result["ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.guaranteedDownlinkBW.%s" % (i + 1))
                if html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1)) != None:
                    dic_result["ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1)] = html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex.%s" % (i + 1))
            dic_result["success"] = 0
            #result = odu100_common_cancel(host_id,device_type_id,dic_result)
            html.write(str(dic_result))
        elif html.var("odu100_submit") == "Ok":
            html.write("ok")


    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def llc_configuration(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    try:
        global html, host_status_dic, obj_essential
        html = h
        dic_result = {}
        flag = 0
        host_id = html.var("host_id")
        device_type_id = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            if html.var("odu100_submit") == "Save":
                obj_essential.host_status(host_id, 12)
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["host_id"] = "Host does not exist"
                    flag = 1
                else:
                    if html.var("ru.ra.llc.raLlcConfTable.arqWinHigh") != None:
                        if Validation.is_required(html.var("ru.ra.llc.raLlcConfTable.arqWinHigh")):
                            if Validation.is_number(html.var("ru.ra.llc.raLlcConfTable.arqWinHigh")):
                                dic_result["ru.ra.llc.raLlcConfTable.arqWinHigh"] = html.var("ru.ra.llc.raLlcConfTable.arqWinHigh")
                            else:
                                dic_result["result"] = "Retransmit Window Size(High) must be number"
                                flag = 1
                        else:
                            dic_result["result"] = "Retransmit Window Size(High) is required"
                            flag = 1
                    if html.var("ru.ra.llc.raLlcConfTable.arqWinLow") != None:
                        if Validation.is_required(html.var("ru.ra.llc.raLlcConfTable.arqWinLow")):
                            if Validation.is_number(html.var("ru.ra.llc.raLlcConfTable.arqWinLow")):
                                dic_result["ru.ra.llc.raLlcConfTable.arqWinLow"] = html.var("ru.ra.llc.raLlcConfTable.arqWinLow")
                            else:
                                dic_result["result"] = "Retransmit Window Size(Low) must be number"
                                flag = 1
                        else:
                            dic_result["result"] = "Retransmit Window Size(Low) is required"
                            flag = 1
                    if html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold") != None:
                        if Validation.is_required(html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold")):
                            if Validation.is_number(html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold")):
                                dic_result["ru.ra.llc.raLlcConfTable.frameLossThreshold"] = html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold")
                            else:
                                dic_result["result"] = "FrameLoss Threshold must be number must be number"
                                flag = 1
                        else:
                            dic_result["result"] = "FrameLoss Threshold is required"
                            flag = 1
                    if html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal") != None:
                        if Validation.is_required(html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal")):
                            if Validation.is_number(html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal")):
                                dic_result["ru.ra.llc.raLlcConfTable.leakyBucketTimerVal"] = html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal")
                            else:
                                dic_result["result"] = "Leaky Bucket Timer must be number"
                                flag = 1
                        else:
                            dic_result["result"] = "Leaky Bucket Timer is required"
                            flag = 1    
                    if html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout") != None:
                        if Validation.is_required(html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout")):
                            if Validation.is_number(html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout")):
                                dic_result["ru.ra.llc.raLlcConfTable.frameLossTimeout"] = html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout")
                            else:
                                dic_result["result"] = "Frame Loss Timeout must be number"
                                flag = 1
                        else:
                            dic_result["result"] = "Frame Loss Timeout is required"
                            flag = 1    

                if flag == 1:
                    dic_result["success"] = 1
                    html.write(str(dic_result))
                else:
                    #html.write(str(dic_result))
                    dic_result["success"] = 0
                    result = controller_validation(host_id, device_type_id, dic_result)
                    html.write(str(result))
                    

            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "":
                obj_essential.host_status(host_id, 12) 
                if html.var("ru.ra.llc.raLlcConfTable.arqWinHigh") != None:
                    dic_result["ru.ra.llc.raLlcConfTable.arqWinHigh"] = html.var("ru.ra.llc.raLlcConfTable.arqWinHigh")
                if html.var("ru.ra.llc.raLlcConfTable.arqWinLow") != None:
                    dic_result["ru.ra.llc.raLlcConfTable.arqWinLow"] = html.var("ru.ra.llc.raLlcConfTable.arqWinLow")
                if html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold") != None:
                    dic_result["ru.ra.llc.raLlcConfTable.frameLossThreshold"] = html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold")
                if html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal") != None:
                    dic_result["ru.ra.llc.raLlcConfTable.leakyBucketTimerVal"] = html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal")
                if html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout") != None:
                    dic_result["ru.ra.llc.raLlcConfTable.frameLossTimeout"] = html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout")
                dic_result["success"] = 0
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                dic_result["result"]["ru.ra.llc.raLlcConfTable.arqWinHigh"] = html.var("ru.ra.llc.raLlcConfTable.arqWinHigh")
                dic_result["result"]["ru.ra.llc.raLlcConfTable.arqWinLow"] = html.var("ru.ra.llc.raLlcConfTable.arqWinLow")
                dic_result["result"]["ru.ra.llc.raLlcConfTable.frameLossThreshold"] = html.var("ru.ra.llc.raLlcConfTable.frameLossThreshold")
                dic_result["result"]["ru.ra.llc.raLlcConfTable.leakyBucketTimerVal"] = html.var("ru.ra.llc.raLlcConfTable.leakyBucketTimerVal")
                dic_result["result"]["ru.ra.llc.raLlcConfTable.frameLossTimeout"] = html.var("ru.ra.llc.raLlcConfTable.frameLossTimeout")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))
            elif html.var("odu100_submit") == "Ok":
                html.write("ok")
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def channel_configuration(h):
    global html, host_status_dic, obj_essential
    html = h
    dic_result = {}
    flag = 1
    channel_config = 10
    select_list = []
    flag = 0
    host_id = html.var("host_id")
    result = {}
    device_type_id = html.var("device_type")
    try:
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            if html.var("odu100_submit") == "Save" or html.var("odu100_submit") == "Retry" or html.var("odu100_submit") == "":
                obj_essential.host_status(host_id, 12)
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["result"] = "Host does not exist"
                    dic_result["success"] = 1
                else:
                    for i in range(0, channel_config):
                        if html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1)) != None and html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1)) != "":
                            dic_result['RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1)] = html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1))

                            if int(html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1))) != 0:
                                select_list.append(html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1)))
                            if len(select_list) != 0:
                                if chk_list(select_list) == 0:
                                    flag = 0
                                else:
                                    flag = 1
                if flag == 1:
                    dic_result["success"] = 1
                    dic_result["result"] = "Dupliacte Frequency Used"
                    html.write(str(dic_result))
                else:
                    #html.write(str(dic_result))
                    result = channel_config_set(host_id, device_type_id, dic_result)
                    html.write(str(result))
            elif html.var("odu100_submit") == "Cancel":
                for i in range(0, channel_config):
                    if html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1)) != None:
                        dic_result['RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1)] = html.var('RU.RA.PrefRfChanFreq.frequency.%s' % (i + 1))
                dic_result["success"] = 0
                #result = odu100_common_cancel(host_id,device_type_id,dic_result)
                html.write(str(dic_result))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)


def ip_packet_filter(h):
    global html, host_status_dic, obj_essential
    html = h
    dic_result = {}
    ip_range = 9
    select_list = []
    flag = 0
    host_id = html.var("host_id")
    result = {}
    device_type_id = html.var("device_type")
    try:
        host_op_status = obj_essential.host_status(host_id, 12)
        if host_op_status == 0 :
            if html.var("odu100_submit") == "Save" or html.var("odu100_submit") == "Retry" or html.var("odu100_submit") == "":
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["result"] = "Host does not exist"
                    dic_result["success"] = 1
                else:
                    for i in range(1, ip_range):
                        if html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)) != None:
                            if html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)) != "":
                                if Validation.is_valid_ip(html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i))) and int(html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)).split('.')[0]) not in [0,255] and int(html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)).split('.')[-1]) not in [0,255]:
                                    if html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)) not in  dic_result.values():
                                        dic_result['ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)] = html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i))
                                    else :
                                        flag = 1
                                        dic_result["result"] = "Dupliacte IP Address used of index no %s "%(i)
                                else:
                                    flag = 1
                                    dic_result["result"] = "Please Enter a Valid Ip Address of index no %s "%(i)
                            else:
                                dic_result['ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)] = ""

                                
                        if html.var('ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i)) != None :
                            if html.var('ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i)) != "":
                                if Validation.is_valid_ip(html.var('ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i))):
                                    dic_result['ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i)] = html.var('ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i))
                                else:
                                    flag = 1
                                    dic_result["result"] = "Please Enter a Valid Net Mask Address of index no %s "%(i)
                            else:
                                flag = 1
                                dic_result["result"] = "Net-Mask should be a valid IP Address of index no %s "%(i)

                if flag == 1:
                    dic_result["success"] = 1
                    html.write(str(dic_result))
                else:
                    #html.write(str(dic_result))
                    result = packet_filter_set(host_id, device_type_id , 0 , dic_result)
                    html.write(str(result))
            elif html.var("odu100_submit") == "Cancel":
                for i in range(1, ip_range):
                    if html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i)) != None:
                        dic_result['ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (1)] = html.var('ru.packetFilters.ipFilterTable.ipFilterIpAddress.%s' % (i))
                    if html.var('ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i)) != None:
                        dic_result['ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (1)] = html.var('ru.packetFilters.ipFilterTable.ipFilterNetworkMask.%s' % (i))
                dic_result["success"] = 0
                #result = odu100_common_cancel(host_id,device_type_id,dic_result)
                html.write(str(dic_result))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)


def mac_packet_filter(h):
    global html, host_status_dic, obj_essential
    html = h
    dic_result = {}
    ip_range = 9
    select_list = []
    flag = 0
    host_id = html.var("host_id")
    result = {}
    device_type_id = html.var("device_type")
    try:
        host_op_status = obj_essential.host_status(host_id, 12)
        if host_op_status == 0 :
            if html.var("odu100_submit") == "Save" or html.var("odu100_submit") == "Retry" or html.var("odu100_submit") == "":
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["result"] = "Host does not exist"
                    dic_result["success"] = 1
                else:
                    for i in range(1, ip_range):
                        if html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)) != None:
                            if html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)) != "":
                                if Validation.is_valid_mac(html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)).strip()):
                                    if html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)) not in  dic_result.values():
                                        dic_result['ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)] = html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i))
                                    else :
                                        flag = 1
                                        dic_result["result"] = "Dupliacte MAC Address of index no %s"%i
                                else :
                                    flag = 1
                                    dic_result["result"] = "Please Enter a Valid MAC Address of index no %s "%(i)
                            else:
                                dic_result['ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)] = ""
                if flag == 1:
                    dic_result["success"] = 1
                    html.write(str(dic_result))
                else:
                    #html.write(str(dic_result))
                    result = packet_filter_set(host_id, device_type_id,1 ,dic_result)
                    html.write(str(result))
            elif html.var("odu100_submit") == "Cancel":
                for i in range(1, ip_range):
                    if html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i)) != None:
                        dic_result['ru.packetFilters.macFilterTable.filterMacAddress.%s' % (1)] = html.var('ru.packetFilters.macFilterTable.filterMacAddress.%s' % (i))
                dic_result["success"] = 0
                #result = odu100_common_cancel(host_id,device_type_id,dic_result)
                html.write(str(dic_result))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)



def packet_filter_mode(h):

    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """

    global html, host_status_dic, obj_essential
    html = h
    dic_result = {}
    ip_range = 9
    select_list = []
    flag = 0
    host_id = html.var("host_id")
    result = {}
    device_type_id = html.var("device_type")
    try:
    	filter_result = totalPacketIpMAC(host_id)
        host_op_status = obj_essential.host_status(host_id, 12)
        if host_op_status == 0 :
            if html.var("odu100_submit") == "Save" or html.var("odu100_submit") == "Retry" or html.var("odu100_submit") == "":
                if html.var("host_id") == "" or html.var("host_id") == None:
                    dic_result["result"] = "Host does not exist"
                    dic_result["success"] = 1
                    flag = 1
                else:
                    if html.var('ru.ruConfTable.ethFiltering') != None and html.var('ru.ruConfTable.ethFiltering') != "":
                        if filter_result['success'] == 0:
                            if int(html.var('ru.ruConfTable.ethFiltering')) == 1 :
                                flag = 2 if filter_result['ip_result'] != None and filter_result['ip_result'] == [] else 0
                            elif int(html.var('ru.ruConfTable.ethFiltering')) == 2 :
                                flag = 3 if filter_result['mac_result'] != None and filter_result['mac_result'] == [] else 0
                            else:
                                dic_result['ru.ruConfTable.ethFiltering'] = html.var('ru.ruConfTable.ethFiltering')
                        else:
                            dic_result['ru.ruConfTable.ethFiltering'] = html.var('ru.ruConfTable.ethFiltering')
                        
		if flag == 2:
                    dic_result["success"] = 1
                    dic_result["result"] =  "Can not enable IP filtering if there are no entries in IP filter config table"
                    html.write(str(dic_result))
		elif flag == 3 :
                    dic_result["success"] = 1
                    dic_result["result"] =  "Can not enable MAC filtering if there are no entries in MAC filter config table"
                    html.write(str(dic_result))
                else:
                    if flag == 0:
                        dic_result['ru.ruConfTable.ethFiltering'] = html.var('ru.ruConfTable.ethFiltering')
                    dic_result["success"] = 0
                    result = controller_validation(host_id, device_type_id, dic_result)
                    html.write(str(result))
            elif html.var("odu100_submit") == "Cancel":
                for i in range(1, ip_range):
                    if html.var('ru.ruConfTable.ethFiltering') != None:
                        dic_result['ru.ruConfTable.ethFiltering'] = html.var('ru.ruConfTable.ethFiltering')
                dic_result["success"] = 0
                result = odu100_common_cancel(host_id,device_type_id,dic_result)
                html.write(str(dic_result))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        html.write(str(e[-1]))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)


def acl_data_bind(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var id : this is used to give the id of a particular index of acl which is used to edit
    @var data : this is used to give data of a particular index of a particular id
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to edit the acl mac values
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    dic_result = {}
    flag = 0
    id = html.var("uuid")
    if id == "" or id == None:
        flag = 1
    elif flag == 1:
        html.write("Row not exist")
    else:
        data = acl_edit_bind(id)
        html.write(str(data))

def acl_delete(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var id : this is used to give the id of a particular index of acl which is used to edit
    @var data : this is used to give data of a particular index of a particular id
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this function is used to edit the acl mac values
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html, host_status_dic, obj_essential
    html = h
    uuid = ""
    dic_result = {}
    flag = 0
    mac_exist = 0
    uuid = html.var("uuid")
    host_id = html.var("host_id")
    acl_mode = html.var("aclMode")
    acl_len = html.var("aclLen")
    mac_address = html.var("macAddress")
    host_op_status = obj_essential.get_hoststatus(host_id)
    try:
        if host_op_status == None or host_op_status == 0:
            if uuid == "" or uuid == None:
                flag = 1
            if host_id == "" or host_id == None:
                flag = 1 
            if acl_mode == '1' or acl_mode == 1:
                mac_exist = chk_peer_mac(host_id, mac_address)
            if mac_exist == 1:
                dic_result["success"] = 1
                dic_result["result"] = "Mac Present in PeerMac Address"
                html.write(str(dic_result))
            else:    
                if int(acl_len) == 1 and int(acl_mode) == 1:
                    dic_result["success"] = 1
                    dic_result["result"] = "Last mac address cant be removed if ACL mode is ACCEPT"
                    html.write(str(dic_result))
                else:
                    if (acl_len == 1 and acl_mode == 1) or (acl_len == '1' and acl_mode == '1'):
                        flag = 1
                    if flag == 1:
                        dic_result["success"] = 1
                        html.write(str(dic_result))
                    else:
                        data = acl_delete_bind(uuid, host_id)
                        html.write(str(data))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))

    finally:        
        obj_essential.host_status(host_id, 0, None, 12)

def odu100_acl_add_mac_config(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html, host_status_dic, obj_essential
    html = h
    dic_result = {}
    flag = 0
    mac_flag = 0
    mac_acl_flag = 0
    mac_acl_accept = 0
    mac_acl_deny = 0
    acl_accept = 0
    acl_deny = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    submit_btn_name = html.var("odu100_submit")
    host_op_status = obj_essential.get_hoststatus(host_id)
    try:
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 12)
            if html.var("odu100_submit") == "Add" or html.var("odu100_submit") == "Edit":
                if html.var("aclindex") == "" or html.var("aclindex") == None:
                    flag = 1
                    dic_result["result"] = "Index is not selected"
                else:
                    dic_result["aclindex"] = html.var("aclindex")
        ##        if html.var("ru.ra.raConfTable.aclMode") == None or html.var("ru.ra.raConfTable.aclMode") == "":
        ##            flag = 1
        ##            dic_result["ru.ra.raConfTable.aclMode"] = "ACL mode is not selected"
        ##        else:
        ##            if html.var("ru.ra.raConfTable.aclMode") == 1 or html.var("ru.ra.raConfTable.aclMode") == "1":
        ##                acl_accept = check_acl_accept(host_id,html.var("ru.ra.raAclConfigTable.macaddress"),html.var("ru.ra.raConfTable.aclMode"))
        ##                if acl_accept == 0:
        ##                    dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
        ##                    
        ##            elif html.var("ru.ra.raConfTable.aclMode") == 2 or html.var("ru.ra.raConfTable.aclMode") == "2":
        ##                if check_acl_deny(host_id,html.var("ru.ra.raAclConfigTable.macaddress"),html.var("ru.ra.raConfTable.aclMode"))==0:
        ##                    dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
        ##                else:
        ##                    acl_deny = 1
        ##            else:
        ##                dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                if html.var("ru.ra.raAclConfigTable.macaddress") == "" or html.var("ru.ra.raAclConfigTable.macaddress") == None: 
                    flag = 1
                    dic_result["result"] = "MAC Address is Empty"
                else :
                    if check_mac(host_id, html.var("ru.ra.raAclConfigTable.macaddress"), html.var("ru.ra.raConfTable.aclMode"),submit_btn_name,html.var("aclindex")) == 1:
                        mac_flag = 1
                        dic_result["ru.ra.raAclConfigTable.macaddress"] = "MAC Address Already Exist in Peer Mac.Please Enter the Another One"
                    elif check_acl_mac(host_id, html.var("ru.ra.raAclConfigTable.macaddress")) == 1:
                        mac_acl_flag = 1
                    elif check_acl_mac_accept(host_id, html.var("ru.ra.raAclConfigTable.macaddress")) == 1:
                        mac_acl_accept = 1
                    elif check_acl_mac_deny(host_id, html.var("ru.ra.raAclConfigTable.macaddress")) == 1:
                        mac_acl_deny = 1
                    else:
                        dic_result["ru.ra.raAclConfigTable.macaddress"] = html.var("ru.ra.raAclConfigTable.macaddress")
                if html.var("raacl_index") == "" or html.var("raacl_index") == None:
                    raindex = ""
                else:
                    raindex = html.var("raacl_index")
                if flag == 1:
                    dic_result["success"] = 1 
                    html.write(str(dic_result))
                elif mac_flag == 1:
                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "Mac Address already in use"
                    html.write(str(dic_result))
                elif mac_acl_flag == 1:
                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "Mac Address Present in PeerMac Address"
                    html.write(str(dic_result))
                elif mac_acl_accept == 1:
                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "ACL ACCEPT mode PEER MAC should be same as in ACL MAC list"
                    html.write(str(dic_result))
                elif mac_acl_deny == 1:
                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "ACL DENY mode PEER MAC should be different from ACL MAC list"
                    html.write(str(dic_result))
        ##        elif acl_accept == 1:
        ##            dic_result = {}
        ##            dic_result["success"] = 1
        ##            dic_result["result"] = "ACL ACCEPT mode PEER MAC should be same as in ACL MAC list"
        ##            html.write(str(dic_result))
        ##        elif acl_accept == 2:
        ##            dic_result = {}
        ##            dic_result["success"] = 1
        ##            dic_result["result"] = "ACL Mode cannot be ACCEPT if the ACL MAC list is empty"
        ##            html.write(str(dic_result))
        ##        elif acl_deny == 1:
        ##            dic_result = {}
        ##            dic_result["success"] = 1
        ##            dic_result["result"] = "ACL DENY mode PEER MAC should be different from ACL MAC list"
        ##            html.write(str(dic_result))
                else:
                    dic_result["success"] = 0
                    result = acl_controller_add_edit(host_id, device_type_id, dic_result, raindex)
                    html.write(str(result))

            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "": 
                if html.var("aclindex") != None:
                    dic_result["aclindex"] = html.var("aclindex")
    ##            if html.var("ru.ra.raConfTable.aclMode") != None:
    ##                dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                if html.var("ru.ra.raAclConfigTable.macaddress") != None:
                    dic_result["ru.ra.raAclConfigTable.macaddress"] = html.var("ru.ra.raAclConfigTable.macaddress")
                dic_result["success"] = 0
                html.write(str('raju'))
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))

            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                dic_result["result"]["aclindex"] = html.var("aclindex")
                dic_result["result"]["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                dic_result["result"]["ru.ra.raAclConfigTable.macaddress"] = html.var("ru.ra.raAclConfigTable.macaddress")
        ##            dic_result["result"]["ru.ra.peerNode.peerConfigTable.basicRateMCSIndex"] = html.var("ru.ra.peerNode.peerConfigTable.basicRateMCSIndex")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))
            elif html.var("odu100_submit") == "Ok":
                odu_class_obj = OduConfiguration()
                odu_class_obj.odu100_acl_configuration(host_id, device_type_id)
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))        #html.write("ok")
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))
    finally:        
        obj_essential.host_status(host_id, 0, None, 12)    

def odu100_acl_mode(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var flag : this is used to store the 0 or 1 for error handling.If there is error then flag values's 1 otherwise it is 0
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html, host_status_dic, obj_essential
    html = h
    dic_result = {}
    flag = 0
    acl_accept = 0
    acl_deny = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    try:
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 12)
            if html.var("odu100_submit") == "Save" :
                if html.var("ru.ra.raConfTable.aclMode") == None or html.var("ru.ra.raConfTable.aclMode") == "":
                    flag = 1
                    dic_result["result"] = "Please Select Acl Mode"
                else:

                    if html.var("ru.ra.raConfTable.aclMode") == 1 or html.var("ru.ra.raConfTable.aclMode") == "1":
                        acl_accept = check_acl_accept(host_id, "" if html.var("ru.ra.raAclConfigTable.macaddress") == None else html.var("ru.ra.raAclConfigTable.macaddress") , html.var("ru.ra.raConfTable.aclMode"))
                        if acl_accept == 0:
                            dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")

                    elif html.var("ru.ra.raConfTable.aclMode") == 2 or html.var("ru.ra.raConfTable.aclMode") == "2":

                        if check_acl_deny(host_id, "" if html.var("ru.ra.raAclConfigTable.macaddress") == None else html.var("ru.ra.raAclConfigTable.macaddress") , html.var("ru.ra.raConfTable.aclMode")) == 0:
                            dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                        else:
                            acl_deny = 1
                    else:

                        dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                if flag == 1:

                    dic_result["success"] = 1 
                    html.write(str(dic_result))
                elif acl_accept == 1:

                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "ACL ACCEPT mode PEER MAC should be same as in ACL MAC list"
                    html.write(str(dic_result))
                elif acl_accept == 2:

                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "ACL Mode cannot be ACCEPT if the ACL MAC list is empty"
                    html.write(str(dic_result))
                elif acl_deny == 1:

                    dic_result = {}
                    dic_result["success"] = 1
                    dic_result["result"] = "ACL DENY mode PEER MAC should be different from ACL MAC list"
                    html.write(str(dic_result))
                else:

                    dic_result["success"] = 0
                    result = controller_validation(host_id, device_type_id, dic_result)
                    html.write(str(result))
            elif html.var("odu100_submit") == "Retry" or  html.var("odu100_submit") == "": 
                if html.var("ru.ra.raConfTable.aclMode") != None:
                    dic_result["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                result = controller_validation(host_id, device_type_id, dic_result)
                html.write(str(result))
            elif html.var("odu100_submit") == "Cancel":
                dic_result["success"] = 0
                dic_result["result"] = {}
                dic_result["result"]["ru.ra.raConfTable.aclMode"] = html.var("ru.ra.raConfTable.aclMode")
                result = odu100_common_cancel(host_id, device_type_id, dic_result)
                html.write(str(result))
            elif html.var("odu100_submit") == "Ok":
                odu_class_obj = OduConfiguration()
                odu_class_obj.odu100_acl_configuration(host_id, device_type_id)
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.write(str(dic_result))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))

    finally:        
        obj_essential.host_status(host_id, 0, None, 12)
def update_mac_list(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var device_type : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var odu100_acl_config_form : this is used to save the html string
    @var acl_config_table_data : this is used to store the acl configuration data in dictionary format
    @var acl_configuration : this is used to store the data of acl macaddresses come form databse through controller function 
    @var dic_result : this is used to store the page values in a dictionary format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to give all the page values of form and give the controller function according to submit action which process these values and give the result 
            and this result is write on the page
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    if host_id == "" or host_id == None:
        host_id = ""
    odu100_acl_config_form = ""
    ra_config_table_data = odu100_get_raconfigtable(host_id)
    ra_configuration = ra_config_table_data["result"]
    acl_config_table_data = odu100_get_aclconfigtable(host_id)
    acl_configuration = acl_config_table_data["result"]
    if len(acl_configuration) > 0:
        odu100_acl_config_form += "<div class=\"tableDiv\" id=\"tableDiv\">\
                                    <table id=\"show_mac_edit_delete\" class =\"show_mac_edit_delete display\" width=\"100%\" cellpadding=0 cellspacing=0>\
                                        <thead>\
                                            <tr>\
                                                <th>Index</th>\
                                                <th>Mac Address</th>\
                                                <th></th>\
                                                \
                                            </tr>\
                                        </thead>\
                                        <tbody>"

        # This variable is used for storing total number of records of database table [type - int]
        for i in range(0, len(acl_configuration)):
            odu100_acl_config_form += "<tr>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td><a href=\"javascript:editMac('%s','0','%s',this,'%s','%s','%s');\" class=\"acl_edit_anchor\"><img src = \"images/edit16.png\" title=\"Edit Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton\"/></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src = \"images/delete16.png\" title=\"Delete Profile\" style=\"width:16px;height:16px;\" class=\"imgbutton\" onclick=\"editMac('%s','1','%s',this,'%s','%s','%s');\"/></td>\
                                                \
                                           </tr>" % (str("" if acl_configuration[i][0] == None else acl_configuration[i][0]), "" if acl_configuration[i][1] == None else acl_configuration[i][1], "" if acl_configuration[i][2] == None else acl_configuration[i][2], host_id, str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), len(acl_configuration), "" if acl_configuration[i][1] == None else acl_configuration[i][1], "" if acl_configuration[i][2] == None else acl_configuration[i][2], host_id, str("" if ra_configuration[0][7] == None else ra_configuration[0][7]), len(acl_configuration), "" if acl_configuration[i][1] == None else acl_configuration[i][1])
        odu100_acl_config_form += "</tbody></table>\
                                    </div>"
    else:
        if acl_config_table_data["success"] == 1:
            odu100_acl_config_form += "<div class=\"tableDiv\" id=\"tableDiv\">\
                                        <table id=\"show_mac_edit_delete\" class =\"show_mac_edit_delete display\" width=\"100%\" cellpadding=0 cellspacing=0>\
                                            <thead>\
                                                <tr>\
                                                    <th>Index</th>\
                                                    <th>Mac Address</th>\
                                                    <th></th>\
                                                    \
                                                </tr>\
                                            </thead>\
                                        </table>\
                                    </div>"
    html.write(str(odu100_acl_config_form))    

#def check_mac(macaddress):


def odu100_commit_to_flash(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var device_type_id : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var dic_result : this is used to store the page values in a dictionary format
    @var result : this is used to store the result of the function to write on the page
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to commit all the data of forms on the device    
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    dic_result = {}
    flash_reboot = html.var("ru.ruOmOperationsTable.omOperationReq")
    if flash_reboot != None:
        if flash_reboot == "Reboot":
            dic_result["ru.ruOmOperationsTable.omOperationReq"] = 5
        else:
            dic_result["ru.ruOmOperationsTable.omOperationReq"] = 4
    dic_result["success"] = 0
    host_id = html.var("host_id")
    device_type_id = html.var("device_type")
    result = commit_reboot_flash(host_id, device_type_id, dic_result)
    html.write(str(result))

    #html.write(str(flash_reboot))

def odu16_reconcilation(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var html : this is html Class Object defined globally 
    @var device_type_id : this is used to store the device type id i.e UBR,Switch,AP25 etc
    @var user_name : this is used to store the name of user who is logged in
    @var obj_reconciliation : this is object of OduReconciliation class
    @var table_prefix : this is used to sotre the table prefix for eg if table name is odu16_get_ru_details then table prefix is odu16_
    @var result : this is used to store the result of the function to write on the page
    @since : 20 August 2011
    @version :0.0 
    @date : 20 Augugst 2011
    @note : this is used to commit all the data of forms on the device    
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    user_name = html.req.session['username']
    if user_name == None:
        user_name = ""
    device_type_id = "odu16"

    if html.var("insert_update") == None:
        insert_update = True
    else:
        insert_update = html.var("insert_update")
    table_prefix = "odu16_"
    device_type_id = html.var("device_type_id")
    obj_reconcilation = OduReconcilation()
    if device_type_id == "odu16":
        result = obj_reconcilation.odu16_reconcilation_controller_update(host_id, device_type_id, table_prefix, insert_update, user_name)
    else:
        result = obj_reconcilation.update_reconcilation_controller(host_id, device_type_id, "odu100_", datetime.now(), user_name)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))

##def reconcilation(h):
##    """
##    @requires:     
##    @return: 
##    @rtype: 
##    @author:Anuj Samariya 
##    @since: 
##    @version: 
##    @date: 
##    @note: 
##    @organisation: Codescape Consultants Pvt. Ltd.
##    @copyright: 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    """
##    global html
##    html = h
##    host_id = html.var("host_id")
##    device_type_id = html.var("device_type_id")
##    table_prefix = html.var("table_prefix")
##    insert_update = html.var("insert_update")
##    obj_reconcilation = OduReconcilation()
##    #result = obj_reconcilation.reconcilation_controller(host_id,device_type_id,table_prefix,insert_update)
##    html.write(str(result))

def chk_reconcilation_status(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var obj_reconciliation : this is object of OduReconciliation class
    @var result : this is used to store the result which is in string format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 August 2011
    @note : this function is used to check the status of reconciliation that the device reconciliation is completed or not
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj_reconcilation = OduReconcilation()
    result = obj_reconcilation.reconcilation_chk_status(host_id)
    html.write(str(result))

##def reconcilation_status_chk(h):
##    """
##    @author : Anuj Samariya 
##    @param h : html Class Object
##    @var host_id : in this the host id is stored for access of particular host
##    @var html : this is html Class Object defined globally 
##    @var obj_reconciliation : this is object of OduReconciliation class
##    @var result : this is used to store the result which is in string format
##    @since : 20 August 2011
##    @version :0.0 
##    @date : 20 August 2011
##    @note : this function is used to check the status of reconciliation that the device reconciliation is completed or not
##    @organisation : Codescape Consultants Pvt. Ltd.
##    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
##    """
##    global html
##    html = h
##    host_id = html.var("host_id")
##    obj_reconcilation = OduReconcilation()
##    result = obj_reconcilation.reconcilation_chk_status(host_id)
##    html.write(str(result))

def reconcilation_list(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var obj_reconciliation : this is object of OduReconciliation class
    @var result : this is used to store the result which is in string format
    @since : 20 August 2011
    @version :0.0 
    @date : 20 August 2011
    @note : this function is used to give the list of devices whose reconciliation is in under process
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    obj_reconcilation = OduReconcilation()
    result = obj_reconcilation.list_reconciliation()
    html.write(str(result))

def odu100_acl_reconcile(h):
    global html, host_status_dic, obj_essential
    try:
        html = h

        if html.var("host_id") != None:
            host_id = html.var("host_id")
        if html.var("device_type") != None:
            device_type = html.var("device_type")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 11)
            obj_reconcilation = OduReconcilation()
            result = obj_reconcilation.odu100_acl_reconciliation(host_id, device_type)
        else:
            result = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 

        html.write(str(result))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))
    finally:        
        obj_essential.host_status(host_id, 0, None, 11)

def reboot_odu(h):
    global html, host_status_dic, obj_essential
    html = h
    host_id = html.var("host_id")
    dic_result = {}
    try:
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 5)
            bll_rec_obj = OduReconcilation()
            if host_id == "":
                result = {"success":1, "result":"Host Not Exist"}
            device_type_id = html.var("device_type_id")
            if device_type_id == "":
                result = {"success":1, "result":"No device Exist"}
            result = bll_rec_obj.reboot(host_id, device_type_id)
            if int(result['flag']) == 0:
                if 53 in result["result"]:
                    result["success"] = 0
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(result)))
        else:
            dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            dic_result['success'] = 1
            html.req.content_type = 'application/json'
            html.req.write(str(JSONEncoder().encode(dic_result)))
    except Exception as e:
        dic_result["success"] = 1
        dic_result["result"] = str(e[-1])
        html.write(str(dic_result))

    finally:        
        obj_essential.host_status(host_id, 0, None, 5)
def ping_chk(h):
    """
    @author : Anuj Samariya 
    @param h : html Class Object
    @var host_id : in this the host id is stored for access of particular host
    @var html : this is html Class Object defined globally 
    @var obj_reconciliation : this is object of OduReconciliation class
    @var result : this is used to store the result which is in integer number 0 that is device is ping otherwise device is not ping
    @since : 20 August 2011
    @version :0.0 
    @date : 20 August 2011
    @note : this function is used to check that the device is ping or not
    @organisation : Codescape Consultants Pvt. Ltd.
    @copyright : 2011 Anuj Samariya from Codescape Consultants Pvt. Ltd.
    """
    global html
    html = h
    host_id = html.var("host_id")
    obj_reconcilation = OduReconcilation()
    result = obj_reconcilation.chk_ping(host_id)
    html.write(str(result))

def refresh_channel_list(h):
    global html
    html = h
    time.sleep(2)
    host_id = html.var("host_id")
    device_type = html.var("selected_device")
    refresh = html.var("refresh")
    ra_list_refresh = html.var("ra_list_refresh")
    obj = OduConfiguration()
    if int(refresh) == 0 or int(refresh) == 2:
        if int(ra_list_refresh) == 0:
            pass
        else:
            delete_ra_channel_list(host_id)
        result = obj.odu100_channel_configuration(host_id, device_type, 2 if int(refresh) == 2 else 0)
    else:
        result = obj.odu100_channel_configuration(host_id, device_type, 1)
    html.write(str(result))

def ra_channel_list_table(h):
    global html
    html = h
    host_id = html.var("host_id")
    obj_get_channel_list = IduGetData()
    channel_list = obj_get_channel_list.common_get_data_by_host('Odu100RaChannelListTable', host_id)    
    table_str = ""
    table_str += "<input type=\"button\" name=\"refresh_channel_list\" id=\"refresh_channel_list\" value=\"Refresh Channel List\" class=\"yo-small yo-button\"/><br/><br/>"

    if len(channel_list) > 0:
        table_str += "<table class=\"display\" style=\"width:100%;height:100%\"><th class=\"center ui-state-default\" style=\"height:20px\">S.No</th>\
                <th class=\"center ui-state-default\" style=\"height:10px\">Channel Number</th>\
                <th class=\"center ui-state-default\" style=\"height:10px\">Frequency</th>\
                "
        for i in range(0, len(channel_list)):
            table_str += "<tr>\
                        <td style=\"text-align:center\">%s</td>\
                        <td style=\"text-align:center\">%s</td>\
                        <td style=\"text-align:center\">%s</td>\
                    </tr>" % (channel_list[i].raChanIndex, channel_list[i].channelNumber, channel_list[i].frequency)

        table_str += "</table>"
    else:
        table_str += "<table style=\"width:100%;height:100%\"><th class=\"center ui-state-default\" style=\"height:20px\">S.No</th>\
                <th class=\"center ui-state-default\" style=\"height:10px\">Channel Number</th>\
                <th class=\"center ui-state-default\" style=\"height:10px\">Frequency</th>\
                "
        table_str += "<tr>\
                        <td colspan=3 style=\"text-align:center;\">No Data Available</td>\
                    </tr>"
        table_str += "</table>"
    html.write(str(table_str))

def refresh_channel_freq_list(h):
    global html, host_status_dic, obj_essential
    html = h
    host_id = html.var("host_id")
    device_type = html.var("selected_device")
    dic_result = {}
    host_op_status = obj_essential.get_hoststatus(host_id)
    if host_op_status == None or host_op_status == 0:
        obj_essential.host_status(host_id, 16)
        result = channel_list_refresh(host_id, device_type)
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))
        obj_essential.host_status(host_id, 0, None, 16)
    else:
        dic_result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
        dic_result['success'] = 1
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(dic_result)))


def refresh_peer_form(h):
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("selected_device")
    obj = OduConfiguration()
    result = obj.odu100_peer_configuration(host_id, device_type)
    html.write(str(result))

def view_modulation_rate(h):
    global html
    html = h    
    table_str = ""
    table_str += "<table class=\"display\" style=\"width:100%;height:100%\"><th class=\"center ui-state-default\" style=\"height:20px\">MCS Index</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Spatial Streams</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Modulation Type</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Coding Rate</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Rate(kbps)</th>\
                "
    modulation_type = {1:"BPSK", 2:"QPSK", 3:"QAM16", 4:"QAM64"}
    coding_rate = {1:"1/2", 2:"2/3", 3:"3/4", 4:"5/6"}
    host_id = html.var('host_id')
##    ra_conf_result = odu100_get_raconfigtable(host_id)
##    ra_configuration = ra_conf_result["result"]
    view_modulation_rate = get_modulation_rate(host_id)    
    if view_modulation_rate['success'] == 0:
        for i in view_modulation_rate['result']:
            table_str += "<tr>\
                        <td>%s</td>\
                        <td>%s</td>\
                        <td>%s</td>\
                        <td>%s</td>\
                        <td>%s</td>\
                    </tr>" % (int(view_modulation_rate['result'][i][1]) - 1, view_modulation_rate['result'][i][2], modulation_type[int(view_modulation_rate['result'][i][3])], \
                            coding_rate[int(view_modulation_rate['result'][i][4])], view_modulation_rate['result'][i][5])
        table_str += "</table>"
    else:
        table_str = "<table style=\"width:100%;height:100%\"><th class=\"center ui-state-default\" style=\"height:20px\">MCS Index</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Spatial Streams</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Modulation Type</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Coding Rate</th>\
                <th class=\"center ui-state-default\" style=\"height:20px\">Rate(kbps)</th>\
                "
        table_str += "<tr>\
                        <td colspan=5 style=\"text-align:center;\">%s</td>\
                    </tr>" % (view_modulation_rate['result'])
        table_str += "</table>"
    html.write(str(table_str))

def site_survey_data(h):
    global html, host_status_dic, obj_essential
    html = h
    host_id = html.var("host_id")
    form_str = ""
    obj_site_survey_data = IduGetData()
    obj = SiteSurvey()
    site_survey_record = []
    host_op_status = obj_essential.get_hoststatus(host_id)
    if host_op_status == None or host_op_status == 0:
        site_survey_status = obj.chk_site_survey_status(host_id)
        if int(site_survey_status) == 0:
            html.write(str(2))    
        if int(site_survey_status) == 2:
            site_survey_record = obj_site_survey_data.common_get_data_by_host('Odu100RaSiteSurveyResultTable', host_id)
            if len(site_survey_record) > 0 or site_survey_record != []:
                html.write(str(0))
            else:
                html.write(str(1))
        else:
            html.write(str(site_survey_status))
    else:
        html.write(str(host_op_status))

def site_survey_result(h):
    global html
    html = h
    host_id = html.var("host_id")
    form_str = ""
    site_survey_record = []
    obj_site_survey_data = IduGetData()
    site_survey_record = obj_site_survey_data.common_get_data_by_host('Odu100RaSiteSurveyResultTable', host_id)
    obj_site_survey_form = OduConfiguration()
    #if len(site_survey_record)>0 or  site_survey_record != [] :
    form_str = obj_site_survey_form.site_survey_form(site_survey_record)
    html.write("<br/><br/>List Of Channels : <div id=\"ru_value\"> <input type=\"text\" name=\"listOfChannels\" id=\"listOfChannels\" /></div>")
    html.write("<input type=\"button\" name=\"refresh_scan_list\" id=\"refresh_scan_list\" value=\"Calculate\" class=\"yo-small yo-button\"/>")
    html.write("<input type=\"button\" name=\"get_scan_list\" id=\"get_scan_list\" value=\"Refresh Site Survey\" class=\"yo-small yo-button\"/><br/><br/>")
    html.write(form_str)
#    else:
#       html.write("true")

def site_survey_snmp(h):
    try:
        global html, host_status_dic, obj_essential
        html = h
        result = {'success':0, 'result':''}
        node_type = html.var("node_type")
        host_id = html.var("host_id")
        list_of_channels = html.var("listOfChannels")

        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 6)
            obj = SiteSurvey()
            result = obj.site_survey(host_id, node_type, list_of_channels)
        else:
            result['success'] = 1
            result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))
    except Exception as e:
        result = {'success':1, 'result':str(e)}
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))
    finally:        
        obj_essential.host_status(host_id, 0, None, 6)

def get_site_survey(h):
    global html, host_status_dic, obj_essential
    html = h
    result = {}
    try:
        host_id = html.var("host_id")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 15)
            result = get_site_survey_bll(host_id)
        else:
            result['success'] = 1
            result['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..."
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))
    except Exception as e:
        result = {'success':1, 'result':str(e)}
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result)))

    finally:        
        obj_essential.host_status(host_id, 0, None, 15)

def hw_sw_frequency_status(h):
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj = OduStatus()
    result_dic = obj.hw_sw_frequecy_status_chk(host_id, device_type)
    html_str = ""
    html_str += "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1\">"
    if int(result_dic['success']) == 0:
        html_str += "<tr><th>S/W Version<th><td>%s</td></tr>" % ("-" if result_dic['result']['sw_status'] == None else result_dic['result']['sw_status'])
        html_str += "<tr><th>H/W Serial Number<th><td>%s</td></tr>" % ("-" if result_dic['result']['hw_serail_number'] == None else result_dic['result']['hw_serail_number'])
        if device_type == "odu100":
            html_str += "<tr><th>Channel List<th><td>\
                        <table><th>Channel Number</th><th>Frequency</th>"
            if len(result_dic['result']['channel_list']) > 0:

                for i in result_dic['result']['channel_list']:
                    html_str += "<tr>\
                                <td>%s</td>\
                                <td>%s</td>\
                            </tr>" % (0 if i == None else i, result_dic['result']['channel_list'][i])
        else:
            html_str += "<tr><th>Frequency<th><td>%s</td></tr>" % ("-" if result_dic['result']['frequency'] == None else result_dic['result']['frequency'])
        html_str += "</table></td></tr>"    
    html_str += "</table>"
    html.write(str(html_str))

def show_peer_status(h):
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj = OduStatus()
    #{'sucess': 0, 'result': {'timeslot1': {'signalstrength': -38L, 'timestamp': '05-Apr-2012 07:50:10 PM', 'mac_address': '00:80:48:71:86:92,'}}}
    result_dic = obj.peer_status_chk(host_id, device_type)
    html_str = ""
    html_str += "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1\">"
    html_str += "<th>MacAddress</th><th>Signal Strength</th><th>Time</th>"
    if int(result_dic['success']) == 0:
        if len(result_dic['result']) > 0:
            for i in result_dic['result']:
                html_str += "<tr>"
                if int(result_dic['result'][i]['signalstrength']) == 1 or result_dic['result'][i]['signalstrength'] == None:
                    html_str += "<td colspan=\"3\">Device Unreachable</td>"
                else:
                    html_str += "<td>%s</td><td>%s</td><td>%s</td>" % ("-" if result_dic['result'][i]['mac_address'] == None else result_dic['result'][i]['mac_address'][1:-1], \
                                                                   "-" if result_dic['result'][i]['signalstrength'] == None else result_dic['result'][i]['signalstrength'], \
                                                                   "-" if result_dic['result'][i]['timestamp'] == None else result_dic['result'][i]['timestamp'])
                html_str += "</tr>"
        else:
            html_str += "<tr><td colspan=3>No Peer connected</td></tr>"

    html_str += "</table>"
    html.write(html_str)

def admin_state_show(h):
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type_id")
    obj = OduStatus()
    result_dic = obj.admin_states_data(host_id, device_type)
    html_str = ""
    admin_states = "ru.syncClock.syncConfigTable.adminStatus,ru.ra.raConfTable.raAdminState,ru.ruConfTable.adminstate"
    if result_dic['success'] == 0:
        html_str += "<table class=\"yo-table\" id=\"table_status\" style=\"border:2px;border-style:solid;border-color:#6b6969;z-index:1\">"
        html_str += "<tr><th>RU Admin State</th>"
        html_str += "<td><img class=\"n-reconcile\" title=\"RU Admin State\" src=\"%s\" id=\"ru.ruConfTable.adminstate\" name=\"ru.ruConfTable.adminstate\" style=\"width:10px;height:10px;\" state=\"%s\" \
        onClick=\"adminStateCheck(event,this,'%s','%s','ru.ruConfTable.adminstate');\"/></div></td></tr>"\
            % ("images/temp/green_dot.png" if result_dic['ru_admin'] == 1 else "images/temp/red_dot.png", \
              1 if result_dic['ru_admin'] == 1 else 0, host_id, device_type)
        html_str += "<tr><th>RA Admin State</th>"
        html_str += "<td><img class=\"n-reconcile\" title=\"RA Admin State\" src=\"%s\" id=\"ru.ra.raConfTable.raAdminState\" name=\"ru.ra.raConfTable.raAdminState\" style=\"width:10px;height:10px;\" state=\"%s\" \
        onClick=\"adminStateCheck(event,this,'%s','%s','ru.ra.raConfTable.raAdminState');\" /></td></tr>" % ("images/temp/green_dot.png" if result_dic['ra_admin'] == 1 else "images/temp/red_dot.png", 1 if result_dic['ra_admin'] == 1 else 0, host_id, device_type)
        html_str += "<tr><th>Sync Admin State</th>"
        html_str += "<td><img class=\"n-reconcile\" title=\"Sync Admin State\" src=\"%s\" id=\"ru.syncClock.syncConfigTable.adminStatus\" name=\"ru.syncClock.syncConfigTable.adminStatus\" style=\"width:10px;height:10px;\" state=\"%s\" onClick=\"adminStateCheck(event,this,'%s','%s','ru.syncClock.syncConfigTable.adminStatus');\"/></td></tr>" % ("images/temp/green_dot.png" if result_dic['sync_admin'] == 1 else "images/temp/red_dot.png", 1 if result_dic['sync_admin'] == 1 else 0 , host_id, device_type)
        html_str += "<tr><td><input type=\"radio\" class=\"n-reconcile\" title=\"Locked All Admin State\" id=\"lock\" name=\"lock_unlock\" onClick=\"lock_unlock_check(event,this,'%s','%s','%s',0);\"/>Lock All\
        </td><td><input type=\"radio\" id=\"unlock\" class=\"n-reconcile\" title=\"Unlocked All Admin State\" name=\"lock_unlock\" onClick=\"lock_unlock_check(event,this,'%s','%s','%s',1);\"/>Unlock All</td></tr>"\
            % (host_id, device_type, admin_states, host_id, device_type, admin_states)
        html_str += "</table>"
    html.write(html_str)

def change_admin_state(h):
    global html, host_status_dic, obj_essential
    html = h
    try:
        result_dic = {'success':0, 'result':""}
        host_id = html.var("host_id")
        device_type = html.var("device_type_id")
        admin_state_name = html.var("admin_state_name")
        state = html.var("state")
        host_op_status = obj_essential.get_hoststatus(host_id)
        if host_op_status == None or host_op_status == 0:
            obj_essential.host_status(host_id, 12)
            obj = OduStatus()
            result_dic = obj.admin_state_change(host_id, device_type, admin_state_name, state)
        else:
            result_dic['result'] = "Device is busy, Device " + str(host_status_dic[host_op_status]) + " is in progress. please wait ..." 
            result_dic['success'] = 1
        html.req.content_type = 'application/json'
        html.req.write(str(JSONEncoder().encode(result_dic)))
    except Exception as e:
        result_dic["success"] = 1
        result_dic["result"] = str(e[-1])
        html.write(str(result_dic))

    finally:        
        obj_essential.host_status(host_id, 0, None, 12)


def all_lock_unlock(h):
    global html
    html = h
    host_id = html.var("host_id")
    device_type = html.var("device_type")
    admin_state_name = html.var("admin_state_names")
    state = html.var("state")
    obj = OduStatus()
    result_dic = obj.all_lock_unlocked(host_id, device_type, admin_state_name, state)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result_dic)))


def global_admin_status(h):
    global html
    html = h
    host_id = html.var("host_id")
    obj = OduStatus()
    result = obj.global_admin_request(host_id)
    html.req.content_type = 'application/json'
    html.req.write(str(JSONEncoder().encode(result)))

def bw_calculate_form(h):
    global html
    html = h
    host_id = html.var("hostId")
    device_type = html.var("device_type")
    obj = OduConfiguration()
    result = obj.bw_form(host_id, device_type)
    html.write(result)



def odu_form_reconcile(h):
    global html
    html = h
    if html.var("host_id") != None:
        host_id = html.var("host_id")

    if html.var("formName") != None:
        formname = html.var("formName")    
    if html.var("device_type") != None:
        device_type = html.var("device_type")
    obj_form = OduConfiguration()
    result = eval("obj_form.%s(%s,'%s')" % (formname, host_id, device_type))
    html.write(str(result))
