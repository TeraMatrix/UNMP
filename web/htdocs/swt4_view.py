#!/usr/bin/python2.6

####################### import the packages ###################################

from lib import *
from utility import *
from common_controller import *
from swt4_controller import *
###############################################################################

#-------------------------Author and file Information--------------------------

###############################################################################
"""
Odu View : This is used for displaying the forms of Switch 4 port

Author : Anuj Samariya

(CodeScape Consultants Pvt. Ltd.)

"""

###############################################################################
##                                                                           ##
##                     Author- Anuj Samariya                                 ##
##                                                                           ##
##                         Switch 4 Port                                     ##
##                                                                           ##
##                 CodeScape Consultants Pvt. Ltd.                           ##
##                                                                           ##
##                     Dated:23 October 2011                                 ##
##                                                                           ##
###############################################################################

###############################################################################


def form_box(filter_class, a_class, a_href, a_id, a_text, header_text, data_id):
    """
    Author - Anuj Samariya
    This function is used for forming a form on page
    filter_class - This is used to filter the forms according to the button on forms e.g Radio Unit,Radio Access
    a_class - This is used for giving the class on tab in a form
    a_href - This is the link location of anchor
    a_id -  This is the anchor id
    a_text - This is the text view on the anchor e.g Configuration
    header_text - This is the header of form e.g RU Date Time,RU prfile
    data_id - This is the id for filter class.
    this returns the string in html format
    @param filter_class:
    @param a_class:
    @param a_href:
    @param a_id:
    @param a_text:
    @param header_text:
    @param data_id:
    """
    tab_str = ""
    for yo in range(0, len(a_href)):
        tab_str += "<a class=\"tab-profile %s\" href=\"%s\" id=\"%s\">%s<span class=\"\"></span></a>" % (
            a_class[yo], a_href[yo], a_id[yo], a_text[yo])
    str_form = "<li class=\"%s\" data-id=\"%s\" >\
                <div class=\"widget-head\">\
                    %s\
                    <h3>%s</h3>\
                </div>\
                <div class=\"widget-content\">" % (filter_class, data_id, tab_str, header_text)
    return str_form

# Author - Anuj Samariya
# This function is defined the path of forms javascripts and css files and call the odu_profiling_form
# h - is used for request
# prints the forms and display on page


def swt_profiling(h):
    """
    Author - Anuj Samariya
    This function is defined the path of forms javascripts and css files and call the odu_profiling_form
    h - is used for request
    prints the forms and display on page
    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    sitename = __file__.split("/")[3]
    # This we import the stylesheet

##    html.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"css/custom.css\" />\n")
##    html.write("<style type=\"text/css\" title=\"currentStyle\">\
##    		@import \"css/demo_page.css\";\
##            @import \"css/demo_table_jui.css\";\
##            @import \"css/jquery-ui-1.8.4.custom.css\";\
##            @import \"css/main2.css\";\
##        </style>")

    # Define the page header e.g Odu Profiling
    css_list = ['css/ie7.css', 'css/custom.css']
    jss_list = ['js/unmp/main/switch.js', 'js/lib/main/jquery-ui-personalized-1.6rc2.min.js']
    html.new_header("Switch Profiling", "", "", css_list, jss_list)

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

    connect_chk = check_connection()
    if connect_chk == 0 or connect_chk == "0":
        html.write(str(page_header_search(ip_address, mac_address, "Switch4",
                   selected_device_type, "enabled", "device_type")))
        html.write("<br/><br/>")
        html.write(
            "<div id=\"swt4_form_div\" style=\"margin-left:10px\"></div>")
    else:
        html.write("<div id=\"swt4_form_div\" style=\"margin-left:10px\">")
        html.write("There is Some DataBase Problem.Contact Administrator")
        html.write("</div")
    html.new_footer()

# Author - Anuj Samariya
# This function is displaying form of odu16 profiling
# h -  is used for request
# host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
# it displays the forms on page


def swt4_profiling_form(host_id, selected_device):
    """
    Author - Anuj Samariya
    This function is displaying form of odu16 profiling
    h -  is used for request
    host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
    it displays the forms on page
    @param host_id:
    @param selected_device:
    """

# This makes the filter buttons and a commit to flash button and writes on page

##    connect_chk = check_connection()
    """
    Author - Anuj Samariya
    This function is displaying form of Switch4 profiling
    h -  is used for request
    host_id - it is come with request and used to find the ip_address,mac_address,device_id of particular device
    it displays the forms on page
    """
    msg_str = ""
    swt4_storm_str = ""
    # connect_chk = check_connection()
    swt4_obj = SwtFormProfiling()
    ip_form = swt4_obj.swt4_ip_configuration(host_id, selected_device)
    ip_port_str = swt4_obj.swt4_port_settings(host_id, selected_device)
    swt4_vlan_str = swt4_obj.swt4_vlan_settings(host_id, selected_device)
    swt4_bandwidth_str = swt4_obj.swt4_bandwidth_control_settings(
        host_id, selected_device)
    swt4_storm_str = swt4_obj.swt4_storm_control(host_id, selected_device)
    swt4_port_priority_str = swt4_obj.swt4_port_priority(
        host_id, selected_device)
    swt4_dscp_priority_str = swt4_obj.swt4_dscp_priority(
        host_id, selected_device)
    swt4_802_priority_str = swt4_obj.swt4_802_priority(
        host_id, selected_device)
    swt4_ip_priority_str = swt4_obj.swt4_ip_base_priority(
        host_id, selected_device)
    swt4_queue_priority_str = swt4_obj.swt4_queue_priority(
        host_id, selected_device)
    swt4_queue_weight_str = swt4_obj.swt4_queue_weight(
        host_id, selected_device)
    swt4_qos_abstraction_str = swt4_obj.swt4_qos_abstraction(
        host_id, selected_device)
    # swt4_1p_remarking_str = swt4_obj.swt4_1p_remarking(host_id,selected_device)
    # if connect_chk==0 or connect_chk=="0":
    html.write("<div>\
                    <br/><br/>\
                    <ul class=\"splitter\" style=\"margin-right:-30px;\">\
                        <li>Filter by type:\
                            <ul>\
                                <li class=\"segment-1\"><a href=\"#\" data-value=\"all\"><button class=\"filterBtn yo-small yo-button\" id=\"everyThingFilter\" >Everything</button></a></li>\
                                \
                                <li class=\"segment-0\"><a href=\"#\" data-value=\"Configuration\"><button class=\"filterBtn yo-small yo-button\" id=\"configfiler\" >Configuration</button></a></li>\
                                <li class=\"segment-0\"><a href=\"#\" data-value=\"QoS\"><button class=\"filterBtn yo-small yo-button\" id=\"qosFilter\" >QoS</button></a></li>\
                                \
                               \
                            </ul>\
                        </li>\
                    </ul>\
                    <div style=\"margin-left:10px;\">\
                        <input type = \"hidden\" name=\"host_id\" id=\"host_id\" value=\"%s\"  />\
                        <input type=\"button\" id=\"commit_flash_btn\" name=\"commit_flash_btn\" value=\"Commit To Flash\" class=\"yo-small yo-button\" />\
                        <input type=\"button\" id=\"reboot_btn\" name=\"reboot_btn\" value=\"Reboot\" class=\"yo-small yo-button\"/>\
                    </div>\
                </div>" % (host_id))
##    if odu_configuration_object.flag == 1:
##        html.write(msg_str)

    html.write("<div id=\"Columns\">\
    <ul id=\"list\" class=\"column\" >")
    html.write(form_box("Configuration", ["tab-active"], ["#viewDiv"],
               ["viewButton"], ["Configuration"], "IP", "id-1"))
    html.write(str(ip_form))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")
    html.write(form_box("Configuration", ["tab-active", "tab-button"], ["#swt4_port_form_container", "#swt_port_get_div"], ["viewPortButton", "viewPortButton2"], [
               "Configuration", "Port Details"], "Port Settings", "id-1"))
    html.write(str(ip_port_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(form_box("Configuration", ["tab-active", "tab-button"], ["#swt4_vlan_form_container", "#swt_vlan_get_div"], ["viewVlanButton", "viewVlanButton2"], [
               "Configuration", "VLAN Settings"], "VLAN Settings", "id-1"))
    html.write(str(swt4_vlan_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(form_box("Configuration", ["tab-active", "tab-button"], ["#swt_bandwidth_form_container", "#swt_bandwidth_get_div"], ["viewBandwidthButton", "viewBandwidthButton2"], [
               "Configuration", "Bandwidth Details"], "Bandwidth Settings", "id-1"))
    html.write(str(swt4_bandwidth_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")
    ##########################################################################
    html.write(
        form_box(
            "QoS", ["tab-active", "tab-button"], ["#swt4_port_priority_form_container", "#swt4_port_priority_get_div"], ["viewPortPriorityButton",
                                                                                                                         "viewPortPriorityButton2"], ["Configuration", "Port Priority"], "Port Priority", "id-1"))
    html.write(str(swt4_port_priority_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(form_box("QoS", ["tab-active", "tab-button"], ["#swt4_dscp_priority_form_container", "#swt4_dscp_priority_get_div"], ["viewDscpButton", "viewDscpButton2"], [
               "Configuration", "DSCP Priority"], "DSCP Priority", "id-1"))
    html.write(str(swt4_dscp_priority_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(form_box("QoS", ["tab-active", "tab-button"], ["#swt4_802_priority_form_container", "#swt4_802_priority_get_div"], ["view802Button", "view802Button2"], [
               "Configuration", "802p Priority"], "802p Priority", "id-1"))
    html.write(str(swt4_802_priority_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(
        form_box(
            "QoS", ["tab-active", "tab-button"], ["#swt4_ip_base_priority_form_container", "#swt4_ip_base_priority_get_div"], ["viewIpPriorityButton",
                                                                                                                               "viewIpPriorityButton2"], ["Configuration", "Ip Priority"], "Ip Priority", "id-1"))
    html.write(str(swt4_ip_priority_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(
        form_box(
            "QoS", ["tab-active", "tab-button"], ["#swt4_queue_priority_form_container", "#swt4_queue_priority_get_div"], ["viewQueuePriorityButton",
                                                                                                                           "viewQueuePriorityButton2"], ["Configuration", "Queue Priority"], "Queue Priority", "id-1"))
    html.write(str(swt4_queue_priority_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(
        form_box(
            "QoS", ["tab-active", "tab-button"], ["#swt4_queue_weight_form_container", "#swt4_queue_weight_get_div"], ["viewQueueWeightButton",
                                                                                                                       "viewQueueWeightButton2"], ["Configuration", "Queue Weight"], "Queue Weight", "id-1"))
    html.write(str(swt4_queue_weight_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write(
        form_box(
            "QoS", ["tab-active", "tab-button"], ["#swt4_qos_abstraction_form_container", "#swt4_qos_abstraction_get_div"], ["viewQosAbstractionButton",
                                                                                                                             "viewQosAbstractionButton2"], ["Configuration", "Qos Abstraction"], "Qos Abstraction", "id-1"))
    html.write(str(swt4_qos_abstraction_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

##    html.write(form_box("QoS",["tab-active","tab-button"],["#swt4_1p_remarking_form_container","#swt4_1p_remarking_get_div"],["view1PRemarkingButton","view1PRemarkingButton2"],["Configuration","1P Remarking"],"1P Remarking","id-1"))
##    html.write(str(swt4_1p_remarking_str))
##    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
##                </div></li>")

    ##########################################################################

    html.write(form_box("Storm Control", ["tab-active", "tab-button"], ["#swt_storm_form_container", "#swt_storm_get_div"], ["viewStormButton", "viewStormButton2"], [
               "Configuration", "Storm Details"], "Storm Control", "id-1"))
    html.write(str(swt4_storm_str))
    html.write("<div class=\"box-loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>\
                </div></li>")

    html.write("</ul>")
    html.write("</div>")
    html.write(
        "<div class=\"loading\" id=\"main_loading\"><img alt=\"\" src=\"images/loading.gif\"/></div>")
               # this is the main div of loading which is shown on commit to
               # flash

    # html.write("</div>")

##    else:
##        html.write("There is Some DataBase Problem.Contact Administrator")


class SwtFormProfiling(object):
    """
    Author- Anuj Samariya
    This class is used to make forms of Switch
    """

    # Author - Anuj Samariya
    # This function is used to call all functions which make forms of Switch
    # h - request object
    # This returns the string in html format

    swt_select_list_obj = MakeSwtSelectListWithDic()

    # Author - Anuj Samariya
    # This function is used to make form of swt4_ip_configuration
    # h - request object
    # This returns the html form in string
    def swt4_ip_configuration(self, host_id, selected_device):  # host_id,selected_device):
        """
        Author - Anuj Samariya
        This function is used to make form of odu100_ip_configuration
        h - request object
        This returns the string in html form
        @param host_id:
        @param selected_device:
        """

        # This variable is used for storing html form which is in string form
        # [type - string]
        swt_ip_dic = swt4_get_ip(host_id)
        swt_ip_list = swt_ip_dic["result"]
        swt4_ip_config_form = "<div id =\"ip_config_form_container\" name=\"ip_config_form_container\">\
                                    <form id = \"swt_ip_config_form\" name = \"swt_ip_config_form\" action=\"swt_ip_config_form_action.py\" method =\"get\">\
                                        <div id=\"ip_config_form_parmeters_container\" name=\"ip_config_form_parmeters_container\">\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">Mode</label>\
                                                %s\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">IP Address</label>\
                                                <input type = \"text\" id =\"swt4_ip_address\" name=\"swt4_ip_address\" value = \"%s\" maxsize = \"15\"/>\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">SubNetmask</label>\
                                                <input type = \"text\" id =\"swt4_subnet_mask\" name=\"swt4_subnet_mask\" value = \"%s\" maxsize = \"15\"/>\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">Gateway</label>\
                                                <input type = \"text\" id =\"swt4_gateway\" name=\"swt4_gateway\" value = \"%s\" maxsize = \"15\"/>\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_ip_config_form',this)\" class=\"yo-small yo-button\"/>\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_ip_config_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type = \"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type = \"hidden\" name=\"device_type\" value=\"%s\" />\
                                            </div>\
                                        </div>\
                                        \
                                    </form>\
                                </div>" % (self.swt_select_list_obj.ip_mode_select_list(str(swt_ip_list[0][0]), "enabled", "swt_ip_mode_selection", "false", "IP Mode"),
                                           swt_ip_list[0][1], swt_ip_list[0][2], swt_ip_list[0][3], host_id, selected_device)
        return str(swt4_ip_config_form)

    def swt4_port_settings(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_port_list = swt4_get_port_data(host_id)
        swt4_port_data = swt4_port_list["result"]
        swt4_port_str = ""
        speed = ""
        swt4_port_str = "<div id=\"swt4_port_setting\" name=\"swt4_port_setting\">\
                                <form id=\"swt4_port_setting_form\" name=\"swt4_port_setting_form\" action=\"swt4_port_setting_form_action.py\" method=\"get\" tab=\"1\" div_id=\"swt_port_get_div\" div_action=\"update_port_settings.py\">\
                                    <div id=\"swt4_port_form_container\" name=\"swt4_port_form_container\" class=\"form-div\">\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">Link Fault Pass Through</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">Port</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">State</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">Speed/duplex</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">Flow Control</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_port_setting_form',this)\" class=\"yo-small yo-button\">\
                                            <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_port_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_port_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_port_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                            <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                        </div>\
                                    </div>\
                                </form>\
                        " % (self.swt_select_list_obj.link_fault_pass_through_select_list(str("" if swt4_port_data[0][0] == None or swt4_port_data[0][0] == "" else swt4_port_data[0][0]), 'enabled', 'swt_link_fault_selection', 'false', 'Link Fault Pass Through'),
                             self.swt_select_list_obj.port_select_list(str("" if swt4_port_data[0][1] == None or swt4_port_data[0][1]
                                                                           == "" else swt4_port_data[0][1]), 'enabled', 'port_select_list_id', 'false', 'Port'),
                             self.swt_select_list_obj.state_select_list(str("" if swt4_port_data[0][2] == None or swt4_port_data[0][2]
                                                                            == "" else swt4_port_data[0][2]), 'enabled', 'state_select_list_id', 'false', 'State'),
                             self.swt_select_list_obj.speed_duplex_select_list(str("" if swt4_port_data[0][3] == None or swt4_port_data[0][3]
                                                                                   == "" else swt4_port_data[0][3]), 'enabled', 'speed_duplex_list_id', 'false', 'Speed Duplex'),
                             self.swt_select_list_obj.flow_control_select_list(str("" if swt4_port_data[0][4] == None or swt4_port_data[0][4] == "" else swt4_port_data[0][4]), 'enabled', 'flow_control_select_list', 'false', 'Flow Control'), host_id, selected_device)
        swt4_port_str += "<div id=\"swt_port_get_div\" name=\"swt_port_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                        <table cellpadding=\"10\" cellspacing=\"10\" style=\"font-size:12px;\">\
                                            <tr align=\"left\">\
                                                \
                                                <th>Port</th>\
                                                <th>State</th>\
                                                <th>Speed/Duplex</th>\
                                                <th>Flow Control</th>\
                                            </tr>"
        for i in range(0, len(swt4_port_data)):
            if swt4_port_data[i][3] == 0:
                speed = "Auto"
            elif swt4_port_data[i][3] == 1:
                speed = "10M/Half"
            elif swt4_port_data[i][3] == 2:
                speed = "10M/Full"
            elif swt4_port_data[i][3] == 3:
                speed = "100M/Half"
            elif swt4_port_data[i][3] == 4:
                speed = "100M/Full"
            swt4_port_str += "<tr align=\"left\">\
                                    \
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                </tr>" % ("Port" + str(i + 1), "Disabled" if swt4_port_data[i][2] == 0 else "Enabled", str(speed), "Off" if swt4_port_data[i][4] == 0 else "on")
        swt4_port_str += "</table>\
                            </div>\
                        </div>"
        return str(swt4_port_str)

    def swt4_vlan_settings(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt_vlan_dic = swt4_get_vlan_data(host_id)
        swt_vlan_list = swt_vlan_dic["result"]
        swt_vlan_str = ""
        swt_vlan_str += "<div id=\"swt4_vlan_setting\" name=\"swt4_vlan_setting\">\
                                <form id=\"swt4_vlan_setting_form\" name=\"swt4_vlan_setting_form\" action=\"swt4_vlan_setting_form_action.py\" method=\"get\" tab=\"1\" div_id=\"swt_vlan_get_div\" div_action=\"update_vlan.py\">\
                                    <div id=\"swt4_vlan_form_container\" name=\"swt4_vlan_form_container\" class=\"form-div\">\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">VLAN Ingress Filter</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">VLAN Pass All</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">VLAN Port</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">PVID</label>\
                                            <input type = \"text\" id =\"pvid\" name=\"pvid\" value = \"%s\" maxsize = \"15\"/>\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <label class=\"lbl\">Mode</label>\
                                                %s\
                                        </div>\
                                        <div class=\"rowElem\">\
                                            <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_vlan_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_vlan_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_vlan_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_vlan_setting_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"hidden\" name=\"host_id\" value=\"%s\" id=\"host_id\"/>\
                                            <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                        </div>\
                                    </div>\
                                </form>\
                       \
                        " % (self.swt_select_list_obj.vlan_ingress_filter_select_list(str("" if swt_vlan_list[0][0] == None else swt_vlan_list[0][0]), 'enabled', 'vlan_ingress_filter_id', 'false', 'VLAN Ingress Filter'),
                             self.swt_select_list_obj.vlan_pass_all_select_list(
                             str(
                             "" if swt_vlan_list[0][1] == None else swt_vlan_list[0][1]), 'enabled', 'vlan_pass_all_id', 'false', 'VLAN Pass All'),
                             self.swt_select_list_obj.vlan_port_select_list(
                             str(
                             "" if swt_vlan_list[0][2] == None else swt_vlan_list[0][2]), 'enabled', 'vlan_port_id', 'false', 'VLAN Port'),
                             str("" if swt_vlan_list[
                                 0][3] == None else swt_vlan_list[0][3]),
                             self.swt_select_list_obj.vlan_mode_select_list(str("" if swt_vlan_list[0][4] == None else swt_vlan_list[0][4]), 'enabled', 'vlan_mode_id', 'false', 'VLAN Mode'), host_id, selected_device)
        swt_vlan_str += "<div id=\"swt_vlan_get_div\" name=\"swt_vlan_get_div\" class=\"form-div\" style=\"display:none;width:345px\" class=\"form-div\">\
                                        <table style=\"font-size:12px\" cellspacing=\"15\" cellpadding=\"10\">\
                                            <tr align=\"left\">\
                                                \
                                                <th>Port</th>\
                                                <th>PVID</th>\
                                                <th>Mode</th>\
                                                \
                                            </tr>"
        for i in range(0, len(swt_vlan_list)):
            swt_vlan_str += "<tr align=\"left\">\
                                    \
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    <td>%s</td>\
                                    \
                                </tr>" % ("Port" + str(i + 1), swt_vlan_list[i][3], "Original" if swt_vlan_list[i][4] == 0 else "Keep Format")
        swt_vlan_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt_vlan_str))

    def swt4_bandwidth_control_settings(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt_bandwidth_str = ""
        swt4_bandwidth_data = swt4_get_bandwidth_control(host_id)
        swt4_bandwidth = swt4_bandwidth_data["result"]
        if len(swt4_bandwidth) > 0:
            swt_bandwidth_str += "<div id=\"swt_bandwidth\" name=\"swt_bandwidth\">\
                                    <form id=\"swt_bandwidth_form\" name=\"swt_bandwidth_form\" action=\"swt_bandwidth_form_action.py\" method=\"get\" tab=\"1\" div_id=\"swt_bandwidth_get_div\" div_action=\"update_bandwidth.py\">\
                                        <div id=\"swt_bandwidth_form_container\" name=\"swt_bandwidth_form_container\" class=\"form-div\">\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">Cpu Protect</label>\
                                                    %s\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">Port</label>\
                                                    %s\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">Type</label>\
                                                    %s\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">State</label>\
                                                    %s\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <label class=\"lbl\">Rate</label>\
                                                <input type = \"text\" id =\"bandwidth_rate_id\" name=\"bandwidth_rate_id\" value = \"%s\" maxsize = \"15\"/>\
                                            </div>\
                                            <div class=\"rowElem\">\
                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_bandwidth_form',this)\" class=\"yo-small yo-button\" />\
                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                            </div>\
                                        </div>\
                                    </form>\
                                    \
                            " % (self.swt_select_list_obj.bandwidth_cpu_protect_select_list(str("" if swt4_bandwidth[0][0] == None or swt4_bandwidth[0][0] == "" else swt4_bandwidth[0][0]), 'enabled', 'bandwidth_cpu_protect_id', 'false', 'CPU Protect'),
                                 self.swt_select_list_obj.bandwidth_port_select_list(str("" if swt4_bandwidth[0][1] == None or swt4_bandwidth[0][1]
                                                                                         == "" else swt4_bandwidth[0][1]), 'enabled', 'bandwidth_port_select_list_id', 'false', 'Port'),
                                 self.swt_select_list_obj.bandwidth_type_select_list(str("" if swt4_bandwidth[0][2] == None or swt4_bandwidth[0][2]
                                                                                         == "" else swt4_bandwidth[0][2]), 'enabled', 'bandwidth_type_select_list_id', 'false', 'Type'),
                                 self.swt_select_list_obj.bandwidth_state_select_list(str("" if swt4_bandwidth[0][3] == None or swt4_bandwidth[0][3]
                                                                                          == "" else swt4_bandwidth[0][3]), 'enabled', 'bandwidth_state_select_list_id', 'false', 'State'),
                                 "Unlimited" if swt4_bandwidth[0][4] == 0 else swt4_bandwidth[0][4], host_id, selected_device)

            swt_bandwidth_str += "<div id=\"swt_bandwidth_get_div\" name=\"swt_bandwidth_get_div\" class=\"form-div\" style=\"display:none;width:345px\">\
                                        <table style=\"font-size:12px\" cellspacing=\"10\" cellpadding=\"10\">\
                                            <tr align=\"left\">\
                                                \
                                                <th>Port</th>\
                                                <th>Type</th>\
                                                <th>State</th>\
                                                <th>Rate</th>\
                                            </tr>"
            for i in range(0, len(swt4_bandwidth)):
                swt_bandwidth_str += "<tr align=\"left\">\
                                        \
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                    </tr>" % ("Port" + str(i + 1), "Ingress" if swt4_bandwidth[i][2] == 0 else "Egress", "Disable" if swt4_bandwidth[i][3] == 0 else "Enable", "Unlimited" if swt4_bandwidth[i][4] == 0 else swt4_bandwidth[i][4])
            swt_bandwidth_str += "</table>\
                                </div>\
                            </div>"

        return(str(swt_bandwidth_str))

    def swt4_storm_control(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_storm_list = swt4_get_storm_control(host_id)
        swt4_storm_data = swt4_storm_list["result"]
        swt4_storm_str = ""
        swt4_storm_str += "<div id=\"swt_storm\" name=\"swt_storm\">\
                                                <form id=\"swt_storm_form\" name=\"swt_storm_form\" action=\"swt_storm_form_action.py\" method=\"get\" tab=\"1\" div_id=\"swt_storm_get_div\" div_action=\"update_storm.py\">\
                                                    <div id=\"swt_storm_form_container\" name=\"swt_storm_form_container\" class=\"form-div\">\
                                                        <div class=\"rowElem\">\
                                                            <label class=\"lbl\">Storm-type</label>\
                                                                %s\
                                                        </div>\
                                                        <div class=\"rowElem\">\
                                                            <label class=\"lbl\">State</label>\
                                                                %s\
                                                        </div>\
                                                        <div class=\"rowElem\">\
                                                            <label class=\"lbl\">Rate</label>\
                                                                %s\
                                                        </div>\
                                                        <div class=\"rowElem\">\
                                                            <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt_storm_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_storm_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_storm_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt_storm_form',this)\" class=\"yo-small yo-button\" />\
                                                            <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                            <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                        </div>\
                                                    </div>\
                                                </form>\
                                           \
                                            " % (self.swt_select_list_obj.storm_type_select_list(str("" if swt4_storm_data[0][0] == None else swt4_storm_data[0][0]), 'enabled', 'storm_type_id', 'false', 'Storm-Type'),
                                                 self.swt_select_list_obj.storm_state_select_list(str(
                                                                                                  "" if swt4_storm_data[0][1] == None else swt4_storm_data[0][1]), 'enabled', 'storm_state_id', 'false', 'State'),
                                                 self.swt_select_list_obj.storm_rate_select_list(str("" if swt4_storm_data[0][2] == None else swt4_storm_data[0][2]), 'enabled', 'storm_rate_id', 'false', 'Rate(pps)'), host_id, selected_device)

        swt4_storm_str += "<div id=\"swt_storm_get_div\" name=\"swt_storm_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                        <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                            <tr align=\"left\">\
                                                \
                                                <th>Storm-Type</th>\
                                                <th>State</th>\
                                                <th>Rate</th>\
                                                \
                                            </tr>"
        for i in range(0, len(swt4_storm_data)):
            if swt4_storm_data[i][0] == 0:
                storm_type = "Broadcast"
            elif swt4_storm_data[i][0] == 1:
                storm_type = "Multicast"
            elif swt4_storm_data[i][0] == 2:
                storm_type = "UDA"
            swt4_storm_str += "<tr align=\"left\">\
                                        \
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        <td>%s</td>\
                                        \
                                    </tr>" % (str(storm_type), "Off" if swt4_storm_data[i][1] == 0 else "On", "Off" if swt4_storm_data[i][2] == 0 else str(swt4_storm_data[i][2]))
        swt4_storm_str += "</table>\
                            </div>\
                        </div>"
        return(str(swt4_storm_str))

    def swt4_port_priority(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_port_priority_list = swt4_get_port_priority(host_id)
        swt4_port_priority_data = swt4_port_priority_list["result"]
        swt4_port_priority_str = ""
        swt4_port_priority_str += "<div id=\"swt4_port_priority_main_div\" name=\"swt4_port_priority_main_div\">\
                                                    <form id=\"swt4_port_priority_form\" name=\"swt4_port_priority_form\" action=\"swt4_port_priority_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_port_priority_get_div\" div_action=\"update_port_priority.py\">\
                                                        <div id=\"swt4_port_priority_form_container\" name=\"swt4_port_priority_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Port-Based Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Port</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_port_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_port_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_port_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_port_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_enable_disable_select_list('0', 'enabled', 'port_base_priority_id', 'false', 'Port Priority'), self.swt_select_list_obj.common_port_select_list(str("" if swt4_port_priority_data[0][0] == None else swt4_port_priority_data[0][0]), 'enabled', 'port_id', 'false', 'Port'), self.swt_select_list_obj.common_priority_select_list(str("" if swt4_port_priority_data[0][1] == None else swt4_port_priority_data[0][1]), 'enabled', 'priority_id', 'false', 'Priority'), host_id, selected_device)

        swt4_port_priority_str += "<div id=\"swt4_port_priority_get_div\" name=\"swt4_port_priority_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"10\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>Port</th>\
                                                    <th>Priority</th>\
                                                    \
                                                    \
                                                </tr>"
        port = ""

        for i in range(0, len(swt4_port_priority_data)):
            if swt4_port_priority_data[i][0] == '0' or swt4_port_priority_data[i][0] == 0:
                port = "Port 1"
            elif swt4_port_priority_data[i][0] == '1' or swt4_port_priority_data[i][0] == 1:
                port = "Port 2"
            elif swt4_port_priority_data[i][0] == '2' or swt4_port_priority_data[i][0] == 2:
                port = "Port 3"
            elif swt4_port_priority_data[i][0] == '3' or swt4_port_priority_data[i][0] == 3:
                port = "Port 4"
            elif swt4_port_priority_data[i][0] == '4' or swt4_port_priority_data[i][0] == 4:
                port = "Port 5"
            swt4_port_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                           \
                                            \
                                        </tr>" % (port, swt4_port_priority_data[i][1])
        swt4_port_priority_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_port_priority_str))

    def swt4_dscp_priority(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_dscp_priority_list = swt4_get_dscp_priority(host_id)
        swt4_dscp_priority_data = swt4_dscp_priority_list["result"]
        swt4_dscp_priority_str = ""
        swt4_dscp_priority_str += "<div id=\"swt4_dscp_priority_main_div\" name=\"swt4_dscp_priority_main_div\">\
                                                    <form id=\"swt4_dscp_priority_form\" name=\"swt4_dscp_priority_form\" action=\"swt4_dscp_priority_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_dscp_priority_get_div\" div_action=\"update_dscp_priority.py\">\
                                                        <div id=\"swt4_dscp_priority_form_container\" name=\"swt4_dscp_priority_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">DSCP-Based Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">DSCP</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_dscp_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_dscp_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_dscp_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_dscp_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_enable_disable_select_list('0', 'enabled', 'dscp_port_priority_id', 'false', 'DSCP Priority'),
                                                     self.swt_select_list_obj.dscp_select_list(str("" if swt4_dscp_priority_data[0][0]
                                                                                                   == "" else swt4_dscp_priority_data[0][0]), 'enabled', 'dscp_id', 'false', 'DSCP'),
                                                     self.swt_select_list_obj.common_priority_select_list(str("" if swt4_dscp_priority_data[0][1] == None else swt4_dscp_priority_data[0][1]
                                                                                                              ), 'enabled', 'dscp_priority_id', 'false', 'Priority'),
                                                     host_id, selected_device)

        swt4_dscp_priority_str += "<div id=\"swt4_dscp_priority_get_div\" name=\"swt4_dscp_priority_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"15\" cellspacing=\"10\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>DSCP</th>\
                                                    <th>Priority</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_dscp_priority_data)):
            swt4_dscp_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_dscp_priority_data[i][0].upper(), swt4_dscp_priority_data[i][1])
        swt4_dscp_priority_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_dscp_priority_str))

    def swt4_802_priority(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_802_priority_list = swt4_get_801_priority(host_id)
        swt4_802_priority_data = []
        swt4_802_priority_data = swt4_802_priority_list["result"]
        swt4_802_priority_str = ""
        swt4_802_priority_str += "<div id=\"swt4_802_priority_main_div\" name=\"swt4_802_priority_main_div\">\
                                                    <form id=\"swt4_802_priority_form\" name=\"swt4_802_priority_form\" action=\"swt4_802_priority_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_802_priority_get_div\" div_action=\"update_802_priority.py\">\
                                                        <div id=\"swt4_802_priority_form_container\" name=\"swt4_802_priority_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">802.1p-based Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">802.1p</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_802_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_802_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_802_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_802_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_enable_disable_select_list('0', 'enabled', '802p_priority', 'false', 'Priority'),
                                                     self.swt_select_list_obj.select_list_802p(str('' if swt4_802_priority_data[0][0]
                                                                                                   == None else swt4_802_priority_data[
                                                                                                   0][0]), 'enabled', '802p_id', 'false', '802.1p'),
                                                     self.swt_select_list_obj.common_priority_select_list(str("" if swt4_802_priority_data[0][1] == None else swt4_802_priority_data[0][
                                                                                                              1]), 'enabled', '802p_priority_id', 'false', 'Priority'),
                                                     host_id, selected_device)

        swt4_802_priority_str += "<div id=\"swt4_802_priority_get_div\" name=\"swt4_802_priority_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>802.1p</th>\
                                                    <th>Priority</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_802_priority_data)):
            swt4_802_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_802_priority_data[i][0], swt4_802_priority_data[i][1])
        swt4_802_priority_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_802_priority_str))

    def swt4_ip_base_priority(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_ip_priority_list = swt4_get_ip_base_priority(host_id)
        swt4_ip_priority_data = swt4_ip_priority_list["result"]
        swt4_ip_priority_str = ""
        swt4_ip_priority_str += "<div id=\"swt4_ip_base_priority_main_div\" name=\"swt4_ip_base_priority_main_div\">\
                                                    <form id=\"swt4_ip_base_priority_form\" name=\"swt4_ip_base_priority_form\" action=\"swt4_ip_base_priority_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_ip_base_priority_get_div\" div_action=\"update_ip_base_priority.py\">\
                                                        <div id=\"swt4_ip_base_priority_form_container\" name=\"swt4_ip_base_priority_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Ip-Based Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Ip Type</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Ip Address</label>\
                                                                <input type = \"text\" id =\"ip_priority_address\" name=\"ip_priority_address\" value = \"%s\" maxsize = \"15\"/>\
                                                            </div>\
                                                             <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Network Mask</label>\
                                                                <input type = \"text\" id =\"ip_priority_net_mask\" name=\"ip_priority_net_mask\" value = \"%s\" maxsize = \"15\"/>\
                                                            </div>\
                                                             <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_ip_base_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_ip_base_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_ip_base_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_ip_base_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_enable_disable_select_list(str("" if swt4_ip_priority_data[0][0] == None else swt4_ip_priority_data[0][0]), 'enabled', 'ip_priority', 'false', 'Priority'),
                                                     self.swt_select_list_obj.ip_type_select_list(str("" if swt4_ip_priority_data[0][1] == None else swt4_ip_priority_data[
                                                                                                      0][1]), "enabled", "ip_type_id", "false", "IP Type"),
                                                     str(swt4_ip_priority_data[0][2]
                                                         ), str(
                                                     swt4_ip_priority_data[
                                                         0][3]),
                                                   self.swt_select_list_obj.common_priority_select_list(str(
                                                       "" if swt4_ip_priority_data[0][4] == None else swt4_ip_priority_data[0][4]), 'enabled', 'ip_priority_id', 'false', 'Priority'),
                                                   host_id, selected_device)

        swt4_ip_priority_str += "<div id=\"swt4_ip_base_priority_get_div\" name=\"swt4_ip_base_priority_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"8\" cellspacing=\"8\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>Ip Type</th>\
                                                    <th>Ip Address</th>\
                                                    <th>Network Mask</th>\
                                                    <th>Priority</th>\
                                                    <th>Status</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_ip_priority_data)):
            swt4_ip_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % ("Group A" if swt4_ip_priority_data[i][1] == 0 else "Group B", swt4_ip_priority_data[i][2], swt4_ip_priority_data[i][3], swt4_ip_priority_data[i][4], "Disabled" if swt4_ip_priority_data[i][0] == 0 else "Enabled")
        swt4_ip_priority_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_ip_priority_str))

    def swt4_queue_priority(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_queue_priority_list = swt4_get_queue_prority(host_id)
        swt4_queue_priority_data = swt4_queue_priority_list["result"]
        swt4_queue_priority_str = ""
        swt4_queue_priority_str += "<div id=\"swt4_queue_priority_main_div\" name=\"swt4_queue_priority_main_div\">\
                                                    <form id=\"swt4_queue_priority_form\" name=\"swt4_queue_priority_form\" action=\"swt4_queue_priority_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_queue_priority_get_div\" div_action=\"update_queue_priority.py\">\
                                                        <div id=\"swt4_queue_priority_form_container\" name=\"swt4_queue_priority_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">QID Map</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            \
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_queue_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_queue_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_queue_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_queue_priority_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_priority_select_list(str("" if swt4_queue_priority_data[0][0] == None else swt4_queue_priority_data[0][0]), 'enabled', 'qid_map_id', 'false', 'QID MAP'),
                                                   self.swt_select_list_obj.common_priority_select_list(str("" if swt4_queue_priority_data[0][1] == None else swt4_queue_priority_data[
                                                                                                        0][1]), 'enabled', 'qid_map_priority_id', 'false', 'Priority'),
                                                   host_id, selected_device)

        swt4_queue_priority_str += "<div id=\"swt4_queue_priority_get_div\" name=\"swt4_queue_priority_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>QID MAP</th>\
                                                    <th>Priority</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_queue_priority_data)):
            swt4_queue_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_queue_priority_data[i][0], swt4_queue_priority_data[i][1])
        swt4_queue_priority_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_queue_priority_str))

    def swt4_queue_weight(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_queue_weight_list = swt4_get_queue_weight(host_id)
        swt4_queue_weight_data = swt4_queue_weight_list["result"]
        swt4_queue_weight_str = ""
        swt4_queue_weight_str += "<div id=\"swt4_queue_weight_main_div\" name=\"swt4_queue_weight_main_div\">\
                                                    <form id=\"swt4_queue_weight_form\" name=\"swt4_queue_weight_form\" action=\"swt4_queue_weight_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_queue_weight_get_div\" div_action=\"update_queue_weight.py\">\
                                                        <div id=\"swt4_queue_weight_form_container\" name=\"swt4_queue_weight_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Queue</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Weight</label>\
                                                                    %s\
                                                            </div>\
                                                            \
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_queue_weight_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_queue_weight_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_queue_weight_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_queue_weight_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_priority_select_list(str("" if swt4_queue_weight_data[0][0] == None else swt4_queue_weight_data[0][0]), 'enabled', 'queue_id', 'false', 'Queue'),
                                                   self.swt_select_list_obj.queue_weight_select_list(str("" if swt4_queue_weight_data[0][1] == None else swt4_queue_weight_data[
                                                                                                     0][1]), 'enabled', 'qid_weight_id', 'false', 'Weight'),
                                                   host_id, selected_device)

        swt4_queue_weight_str += "<div id=\"swt4_queue_weight_get_div\" name=\"swt4_queue_weight_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>Queue</th>\
                                                    <th>Weight</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_queue_weight_data)):
            swt4_queue_weight_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_queue_weight_data[i][0], swt4_queue_weight_data[i][1])
        swt4_queue_weight_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_queue_weight_str))

    def swt4_qos_abstraction(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_qos_abstraction_list = swt4_get_qos_abstraction(host_id)
        swt4_qos_abstraction_data = swt4_qos_abstraction_list["result"]
        swt4_qos_abstraction_str = ""
        swt4_qos_abstraction_str += "<div id=\"swt4_qos_abstraction_main_div\" name=\"swt4_qos_abstraction_main_div\">\
                                                    <form id=\"swt4_qos_abstraction_form\" name=\"swt4_qos_abstraction_form\" action=\"swt4_qos_abstraction_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_qos_abstraction_get_div\" div_action=\"update_qos_abstraction.py\">\
                                                        <div id=\"swt4_qos_abstraction_form_container\" name=\"swt4_qos_abstraction_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">Level</label>\
                                                                    %s\
                                                            </div>\
                                                            \
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_qos_abstraction_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_qos_abstraction_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_qos_abstraction_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_qos_abstraction_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.qos_abstaction_priority_select_list(str("" if swt4_qos_abstraction_data[0][0] == None else swt4_qos_abstraction_data[0][0]), 'enabled', 'qos_priority_id', 'false', 'Priorty'),
                                                   self.swt_select_list_obj.qos_abstaction_level_select_list(str(
                                                       "" if swt4_qos_abstraction_data[0][1] == None else swt4_qos_abstraction_data[0][1]), 'enabled', 'qos_level_id', 'false', 'Level'),
                                                   host_id, selected_device)

        swt4_qos_abstraction_str += "<div id=\"swt4_qos_abstraction_get_div\" name=\"swt4_qos_abstraction_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>Priority</th>\
                                                    <th>Level</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_qos_abstraction_data)):
            swt4_qos_abstraction_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_qos_abstraction_data[i][0], swt4_qos_abstraction_data[i][1])
        swt4_qos_abstraction_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_qos_abstraction_str))

    def swt4_1p_remarking(self, host_id, selected_device):
        """

        @param host_id:
        @param selected_device:
        @return:
        """
        swt4_1p_remarking_list = swt4_get_1p_remarking(host_id)
        swt4_1p_remarking_data = swt4_1p_remarking_list["result"]
        swt4_1p_remarking_str = ""
        swt4_1p_remarking_str += "<div id=\"swt4_1p_remarking_main_div\" name=\"swt4_1p_remarking_main_div\">\
                                                    <form id=\"swt4_1p_remarking_form\" name=\"swt4_1p_remarking_form\" action=\"swt4_1p_remarking_action.py\" method=\"get\" tab=\"1\" div_id=\"swt4_1p_remarking_get_div\" div_action=\"update_1p_remarking.py\">\
                                                        <div id=\"swt4_1p_remarking_form_container\" name=\"swt4_1p_remarking_form_container\" class=\"form-div\">\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">1P Remarking</label>\
                                                                    %s\
                                                            </div>\
                                                            <div class=\"rowElem\">\
                                                                <label class=\"lbl\">802.1P Priority</label>\
                                                                    %s\
                                                            </div>\
                                                            \
                                                            <div class=\"rowElem\">\
                                                                <input type=\"submit\" name=\"swt_submit\" value=\"Save\" id=\"id_swt_submit_save\" onClick=\"return swt4CommonFormSubmit('swt4_1p_remarking_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\"  id=\"id_swt_button_retry_all\" value=\"Retry\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_1p_remarking_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_cancel\" value=\"Cancel\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_1p_remarking_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"submit\" name=\"swt_submit\" id=\"id_swt_button_ok\" value=\"Ok\" style=\"Display:None\" onClick=\"return swt4CommonFormSubmit('swt4_1p_remarking_form',this)\" class=\"yo-small yo-button\" />\
                                                                <input type =\"hidden\" name=\"host_id\" value=\"%s\" style=\"Display:None\"/>\
                                                                <input type =\"hidden\" name=\"device_type\" value=\"%s\" />\
                                                            </div>\
                                                        </div>\
                                                    </form>\
                                               \
                                                " % (self.swt_select_list_obj.common_priority_select_list(str("" if swt4_1p_remarking_data[0][0] == None else swt4_1p_remarking_data[0][0]), 'enabled', '1p_remarking_id', 'false', '1P Remarking'),
                                                   self.swt_select_list_obj.select_list_802p(str('' if swt4_1p_remarking_data[0][1] == None else swt4_1p_remarking_data[0][1]),
                                                                                             'enabled', '1p_remarking_priority', 'false', 'Priority'),
                                                   host_id, selected_device)

        swt4_1p_remarking_str += "<div id=\"swt4_1p_remarking_get_div\" name=\"swt4_1p_remarking_get_div\" class=\"form-div\" style=\"display:none;width:345px;\">\
                                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                                <tr align=\"left\">\
                                                    \
                                                    <th>1P Remarkin</th>\
                                                    <th>802.1P Priority</th>\
                                                    \
                                                    \
                                                </tr>"
        for i in range(0, len(swt4_1p_remarking_data)):
            swt4_1p_remarking_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_1p_remarking_data[i][0], swt4_1p_remarking_data[i][1])
        swt4_1p_remarking_str += "</table>\
                                </div>\
                            </div>"
        return(str(swt4_1p_remarking_str))


def swt_ip_config_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")

    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:

                if Validation.is_required(html.var("swt_ip_mode_selection")):
                    dic_result["result"]["swt_ip_mode_selection"] = html.var(
                        "swt_ip_mode_selection")
                else:
                    flag = 1
                    dic_result["result"][
                        "swt4_ip_address"] = "Select the mode of Ip"
                if Validation.is_required(html.var("swt4_ip_address")):
                    if Validation.is_valid_ip(html.var("swt4_ip_address")):
                        dic_result["result"][
                            "swt4_ip_address"] = html.var("swt4_ip_address")
                    else:
                        flag = 1
                        dic_result["result"][
                            "swt4_ip_address"] = "Ip Address is not valid"
                else:
                    flag = 1
                    dic_result["result"][
                        "swt4_ip_address"] = "Ip Address is Required"

                if Validation.is_required(html.var("swt4_subnet_mask")):
                    if Validation.is_valid_ip(html.var("swt4_subnet_mask")):
                        dic_result["result"][
                            "swt4_subnet_mask"] = html.var("swt4_subnet_mask")
                    else:
                        flag = 1
                        dic_result["result"][
                            "swt4_subnet_mask"] = "Subnet Mask is not valid"
                else:
                    flag = 1
                    dic_result["result"][
                        "swt4_subnet_mask"] = "Subnet Mask is Required"

                if Validation.is_required(html.var("swt4_gateway")):
                    if Validation.is_valid_ip(html.var("swt4_gateway")):
                        dic_result["result"][
                            "swt4_gateway"] = html.var("swt4_gateway")
                    else:
                        flag = 1
                        dic_result["result"][
                            "swt4_gateway"] = "Gateway Format is not valid"
                else:
                    flag = 1
                    dic_result["result"][
                        "swt4_gateway"] = "Gateway Address is Required"
            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_ip_set(host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(
                ["swt_ip_mode_selection", html.var("swt_ip_mode_selection")])
            dic_result["result"].append(
                ["swt4_ip_address", html.var("swt4_ip_address")])
            dic_result["result"].append(
                ["swt4_subnet_mask", html.var("swt4_subnet_mask")])
            dic_result["result"].append(["swt4_gateway",
                                        html.var("swt4_gateway")])
            result = swt4_ip_cancel(host_id, device_type_id, dic_result)
            html.write(str(dic_result))
        elif html.var("swt_submit") == "Ok":
            html.write("ok")

    except Exception as e:
        html.write(str(e[-1]))


def swt4_port_setting_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("swt_link_fault_selection")):
                    dic_result["result"]["swt_link_fault_selection"] = html.var(
                        "swt_link_fault_selection")
                else:
                    flag = 1
                    dic_result["result"][
                        "swt_link_fault_selection"] = "Select the Switch Link Fault Selection"
                if Validation.is_required(html.var("port_select_list_id")):
                    dic_result["result"]["port_select_list_id"] = html.var(
                        "port_select_list_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "port_select_list_id"] = "Select the Port"
                if Validation.is_required(html.var("state_select_list_id")):
                    dic_result["result"]["state_select_list_id"] = html.var(
                        "state_select_list_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "state_select_list_id"] = "Select the state"
                if Validation.is_required(html.var("speed_duplex_list_id")):
                    dic_result["result"]["speed_duplex_list_id"] = html.var(
                        "speed_duplex_list_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "speed_duplex_list_id"] = "Select the Speed duplex"
                if Validation.is_required(html.var("flow_control_select_list")):
                    dic_result["result"]["flow_control_select_list"] = html.var(
                        "flow_control_select_list")
                else:
                    flag = 1
                    dic_result["result"][
                        "flow_control_select_list"] = "Select the Flow Control"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_port_setting_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["swt_link_fault_selection",
                                        html.var("swt_link_fault_selection")])
            dic_result["result"].append(
                ["port_select_list_id", html.var("port_select_list_id")])
            dic_result["result"].append(
                ["state_select_list_id", html.var("state_select_list_id")])
            dic_result["result"].append(["flow_control_select_list", html.var(
                "flow_control_select_list")])
            result = swt4_port_cancel(host_id, device_type_id, dic_result)
            html.write(str(result))
        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e[-1]))


def swt4_vlan_setting_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("vlan_ingress_filter_id")):
                    dic_result["result"]["vlan_ingress_filter_id"] = html.var(
                        "vlan_ingress_filter_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "vlan_ingress_filter_id"] = "Select the VLAN Ingress Filter"
                if Validation.is_required(html.var("vlan_pass_all_id")):
                    dic_result["result"][
                        "vlan_pass_all_id"] = html.var("vlan_pass_all_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "vlan_pass_all_id"] = "Select the VLAN Pass All"
                if Validation.is_required(html.var("vlan_port_id")):
                    dic_result["result"][
                        "vlan_port_id"] = html.var("vlan_port_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "vlan_port_id"] = "Select the VLAN Port"
                if Validation.is_required(html.var("pvid")):
                    if Validation.is_number(html.var("pvid")):
                        dic_result["result"]["pvid"] = html.var("pvid")
                    else:
                        flag = 1
                        dic_result["result"]["pvid"] = "Number is required"
                else:
                    flag = 1
                    dic_result["result"]["pvid"] = "PVID is required"
                if Validation.is_required(html.var("vlan_mode_id")):
                    dic_result["result"][
                        "vlan_mode_id"] = html.var("vlan_mode_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "vlan_mode_id"] = "Select the VLAN Mode"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_vlan_setting_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["vlan_ingress_filter_id",
                                        html.var("vlan_ingress_filter_id")])
            dic_result["result"].append(
                ["vlan_pass_all_id", html.var("vlan_pass_all_id")])
            dic_result["result"].append(["vlan_port_id",
                                        html.var("vlan_port_id")])
            dic_result["result"].append(["pvid", html.var("pvid")])
            dic_result["result"].append(["vlan_mode_id",
                                        html.var("vlan_mode_id")])
            result = swt4_vlan_cancel(host_id, device_type_id, dic_result)
            html.write(str(result))
        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e[-1]))


def swt_bandwidth_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")

    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("bandwidth_cpu_protect_id")):
                    dic_result["result"]["bandwidth_cpu_protect_id"] = html.var(
                        "bandwidth_cpu_protect_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "bandwidth_cpu_protect_id"] = "Select the Cpu Protect"
                if Validation.is_required(html.var("bandwidth_port_select_list_id")):
                    dic_result["result"]["bandwidth_port_select_list_id"] = html.var(
                        "bandwidth_port_select_list_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "bandwidth_port_select_list_id"] = "Select the Port"
                if Validation.is_required(html.var("bandwidth_type_select_list_id")):
                    dic_result["result"]["bandwidth_type_select_list_id"] = html.var(
                        "bandwidth_type_select_list_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "bandwidth_type_select_list_id"] = "Select the Type"

                if Validation.is_required(html.var("bandwidth_state_select_list_id")):
                    dic_result["result"]["bandwidth_state_select_list_id"] = html.var(
                        "bandwidth_state_select_list_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "bandwidth_state_select_list_id"] = "Select the State"
                if html.var("bandwidth_rate_id") == None:
                    dic_result["result"]["bandwidth_rate_id"] = "Unlimited"
                elif html.var("bandwidth_rate_id") == "Unlimited":
                    dic_result["result"]["bandwidth_rate_id"] = 0
                else:
                    if Validation.is_required(html.var("bandwidth_rate_id")):
                        if Validation.is_number(html.var("bandwidth_rate_id")):
                            dic_result["result"][
                                "bandwidth_rate_id"] = html.var("bandwidth_rate_id")
                        else:
                            flag = 1
                            dic_result["result"][
                                "bandwidth_rate_id"] = "Number is required"
                    else:
                        flag = 1
                        dic_result["result"][
                            "bandwidth_rate_id"] = "Bandwidth Rate is required"
            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_bandwidth_setting_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["bandwidth_cpu_protect_id",
                                        html.var("bandwidth_cpu_protect_id")])
            dic_result["result"].append(["bandwidth_port_select_list_id",
                                        html.var("bandwidth_port_select_list_id")])
            dic_result["result"].append(["bandwidth_type_select_list_id",
                                        html.var("bandwidth_type_select_list_id")])
            dic_result["result"].append(["bandwidth_state_select_list_id",
                                        html.var("bandwidth_state_select_list_id")])
            dic_result["result"].append(
                ["bandwidth_rate_id", html.var("bandwidth_rate_id")])
            result = swt4_bandwidth_cancel(host_id, device_type_id, dic_result)
            html.write(str(result))
        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e[-1]))


def swt_storm_form_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("storm_type_id")):
                    dic_result["result"][
                        "storm_type_id"] = html.var("storm_type_id")
                else:
                    flag = 1
                    dic_result["result"]["storm_type_id"] = "Select the Type"
                if Validation.is_required(html.var("storm_state_id")):
                    dic_result["result"][
                        "storm_state_id"] = html.var("storm_state_id")
                else:
                    flag = 1
                    dic_result["result"]["storm_state_id"] = "Select the State"
                if html.var("storm_rate_id") != None:
                    if Validation.is_required(html.var("storm_rate_id")):
                        dic_result["result"][
                            "storm_rate_id"] = html.var("storm_rate_id")
                    else:
                        flag = 1
                        dic_result["result"][
                            "storm_rate_id"] = "Select The Rate"
                else:
                    dic_result["result"]["storm_rate_id"] = 0
            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_storm_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["storm_type_id",
                                        html.var("storm_type_id")])
            dic_result["result"].append(
                ["storm_state_id", html.var("storm_state_id")])
            if html.var("storm_rate_id") != None:
                dic_result["result"].append(
                    ["storm_rate_id", html.var("storm_rate_id")])
            else:
                dic_result["result"].append(["storm_rate_id", 0])
            result = swt4_storm_cancel(host_id, device_type_id, dic_result)
            html.write(str(result))
        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_port_priority_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("port_id")):
                    dic_result["result"]["port_id"] = html.var("port_id")
                else:
                    flag = 1
                    dic_result["result"]["port_id"] = "Select the Port"

                if Validation.is_required(html.var("priority_id")):
                    dic_result["result"][
                        "priority_id"] = html.var("priority_id")
                else:
                    flag = 1
                    dic_result["result"]["priority_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_port_priority_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["port_id", html.var("port_id")])
            dic_result["result"].append(["priority_id",
                                        html.var("priority_id")])
            result = swt4_port_priority_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_dscp_priority_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("dscp_id")):
                    dic_result["result"]["dscp_id"] = html.var("dscp_id")
                else:
                    flag = 1
                    dic_result["result"]["dscp_id"] = "Select the Port"

                if Validation.is_required(html.var("dscp_priority_id")):
                    dic_result["result"][
                        "dscp_priority_id"] = html.var("dscp_priority_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "dscp_priority_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_dscp_priority_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["dscp_id", html.var("dscp_id")])
            dic_result["result"].append(
                ["dscp_priority_id", html.var("dscp_priority_id")])
            result = swt4_dscp_priority_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_802_priority_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("802p_id")):
                    dic_result["result"]["802p_id"] = html.var("802p_id")
                else:
                    flag = 1
                    dic_result["result"]["802p_id"] = "Select the Port"

                if Validation.is_required(html.var("802p_priority_id")):
                    dic_result["result"][
                        "802p_priority_id"] = html.var("802p_priority_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "802p_priority_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_802_priority_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["802p_id", html.var("802p_id")])
            dic_result["result"].append(
                ["802p_priority_id", html.var("802p_priority_id")])
            result = swt4_802_priority_controller(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_ip_base_priority_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("ip_priority")):
                    dic_result["result"][
                        "ip_priority"] = html.var("ip_priority")
                else:
                    flag = 1
                    dic_result["result"]["ip_priority"] = "Select the Port"

                if Validation.is_required(html.var("ip_type_id")):
                    dic_result["result"]["ip_type_id"] = html.var("ip_type_id")
                else:
                    flag = 1
                    dic_result["result"]["ip_type_id"] = "Select the Priority"

                if Validation.is_required(html.var("ip_priority_address")):
                    if Validation.is_valid_ip(html.var("ip_priority_address")):
                        dic_result["result"]["ip_priority_address"] = html.var(
                            "ip_priority_address")
                    else:
                        flag = 1
                        dic_result["result"][
                            "ip_priority_address"] = "Ip Address is not valid"
                else:
                    flag = 1
                    dic_result["result"][
                        "ip_priority_address"] = "Ip Address is Required"

                if Validation.is_required(html.var("ip_priority_net_mask")):
                    if Validation.is_valid_ip(html.var("ip_priority_net_mask")):
                        dic_result["result"][
                            "ip_priority_net_mask"] = html.var("ip_priority_net_mask")
                    else:
                        flag = 1
                        dic_result["result"][
                            "ip_priority_net_mask"] = "Subnet Mask is not valid"
                else:
                    flag = 1
                    dic_result["result"][
                        "ip_priority_net_mask"] = "Subnet Mask is Required"

                if Validation.is_required(html.var("ip_priority_id")):
                    dic_result["result"][
                        "ip_priority_id"] = html.var("ip_priority_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "ip_priority_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_ip_priority_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(
                ["ip_priority", str(html.var("ip_priority"))])
            dic_result["result"].append(["ip_type_id", str(
                html.var("ip_type_id"))])
            dic_result["result"].append(
                ["ip_priority_address", str(html.var("ip_priority_address"))])
            dic_result["result"].append(["ip_priority_net_mask", str(
                html.var("ip_priority_net_mask"))])
            dic_result["result"].append(
                ["ip_priority_id", str(html.var("ip_priority_id"))])
            result = swt4_ip_priority_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_queue_priority_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("qid_map_id")):
                    dic_result["result"]["qid_map_id"] = html.var("qid_map_id")
                else:
                    flag = 1
                    dic_result["result"]["qid_map_id"] = "Select the Port"

                if Validation.is_required(html.var("qid_map_priority_id")):
                    dic_result["result"]["qid_map_priority_id"] = html.var(
                        "qid_map_priority_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "qid_map_priority_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_queue_priority_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["qid_map_id", html.var("qid_map_id")])
            dic_result["result"].append(
                ["qid_map_priority_id", html.var("qid_map_priority_id")])
            result = swt4_queue_priority_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_queue_weight_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("queue_id")):
                    dic_result["result"]["queue_id"] = html.var("queue_id")
                else:
                    flag = 1
                    dic_result["result"]["queue_id"] = "Select the Port"

                if Validation.is_required(html.var("qid_weight_id")):
                    dic_result["result"][
                        "qid_weight_id"] = html.var("qid_weight_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "qid_weight_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_queue_weight_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(["queue_id", html.var("queue_id")])
            dic_result["result"].append(["qid_weight_id",
                                        html.var("qid_weight_id")])
            result = swt4_queue_weight_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_qos_abstraction_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("qos_priority_id")):
                    dic_result["result"][
                        "qos_priority_id"] = html.var("qos_priority_id")
                else:
                    flag = 1
                    dic_result["result"]["qos_priority_id"] = "Select the Port"

                if Validation.is_required(html.var("qos_level_id")):
                    dic_result["result"][
                        "qos_level_id"] = html.var("qos_level_id")
                else:
                    flag = 1
                    dic_result["result"][
                        "qos_level_id"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_qos_abstraction_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(
                ["qos_priority_id", html.var("qos_priority_id")])
            dic_result["result"].append(["qos_level_id",
                                        html.var("qos_level_id")])
            result = swt4_qos_abstraction_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def swt4_1p_remarking_action(h):
    """

    @param h:
    """
    global html
    html = h
    dic_result = {'result': {}, 'success': 0}
    host_id = html.var("host_id")
    flag = 0
    device_type_id = html.var("device_type")
    try:
        if html.var("swt_submit") == "Save" or html.var("swt_submit") == "Retry":
            if html.var("host_id") == "" or html.var("host_id") == None:
                dic_result["result"]["host_id"] = "Host Does not Exist"
                flag = 1
            else:
                if Validation.is_required(html.var("1p_remarking_id")):
                    dic_result["result"][
                        "1p_remarking_id"] = html.var("1p_remarking_id")
                else:
                    flag = 1
                    dic_result["result"]["1p_remarking_id"] = "Select the Port"

                if Validation.is_required(html.var("1p_remarking_priority")):
                    dic_result["result"]["1p_remarking_priority"] = html.var(
                        "1p_remarking_priority")
                else:
                    flag = 1
                    dic_result["result"][
                        "1p_remarking_priority"] = "Select the Priority"

            if flag == 1:
                dic_result["success"] = 0
                html.write(str(dic_result))
            else:
                dic_result["success"] = 0
                result = swt4_1p_remarking_controller(
                    host_id, device_type_id, dic_result)
                html.write(str(result))

        elif html.var("swt_submit") == "Cancel":
            dic_result["success"] = 0
            dic_result["result"] = []
            dic_result["result"].append(
                ["1p_remarking_id", html.var("1p_remarking_id")])
            dic_result["result"].append(
                ["1p_remarking_priority", html.var("1p_remarking_priority")])
            result = swt4_1p_remarking_cancel(
                host_id, device_type_id, dic_result)
            html.write(str(result))

        elif html.var("swt_submit") == "Ok":
            html.write("ok")
    except Exception as e:
        html.write(str(e))


def update_bandwidth(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    result = swt4_get_bandwidth_control(host_id)
    swt4_bandwidth = result["result"]
    bandwidth_str = ""
    bandwidth_str += "<table style=\"font-size:12px\" cellspacing=\"20\">\
                                            <tr>\
                                                <th>Port</th>\
                                                <th>Type</th>\
                                                <th>State</th>\
                                                <th>Rate</th>\
                                            </tr>"
    for i in range(0, len(swt4_bandwidth)):
        bandwidth_str += "<tr>\
                                \
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                            </tr>" % ("Port" + str(i + 1), "Ingress" if swt4_bandwidth[i][2] == 0 else "Egress", "Disable" if swt4_bandwidth[i][3] == 0 else "Enable", swt4_bandwidth[i][4])
    bandwidth_str += "</table>"
    html.write(str(bandwidth_str))


def update_port_settings(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    result = swt4_get_port_data(host_id)
    swt4_port_details = result["result"]
    swt4_port_str = ""
    speed = ""
    swt4_port_str += "<table style=\"font-size:12px\" cellspacing=\"20\">\
                                            <tr>\
                                               \
                                                <th>Port</th>\
                                                <th>State</th>\
                                                <th>Speed/Duplex</th>\
                                                <th>Flow Control</th>\
                                            </tr>"
    for i in range(0, len(swt4_port_details)):
        if swt4_port_details[i][3] == 0:
            speed = "Auto"
        elif swt4_port_details[i][3] == 1:
            speed = "10M/Half"
        elif swt4_port_details[i][3] == 2:
            speed = "10M/Full"
        elif swt4_port_details[i][3] == 3:
            speed = "100M/Half"
        elif swt4_port_details[i][3] == 4:
            speed = "100M/Full"
        swt4_port_str += "<tr>\
                                \
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                            </tr>" % ("Port" + str(i + 1), "Disabled" if swt4_port_details[i][2] == 0 else "Enabled", str(speed), "Off" if swt4_port_details[i][4] == 0 else "On")
    swt4_port_str += "</table>"
    html.write(str(swt4_port_str))


def update_storm(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_storm_list = swt4_get_storm_control(host_id)
    swt4_storm_data = swt4_storm_list["result"]
    swt4_storm_str = ""
    swt4_storm_str += "\
                        <table style=style=\"font-size:12px;cellspacing:32 \">\
                            <tr>\
                                \
                                <th>Storm-Type</th>\
                                <th>State</th>\
                                <th>Rate</th>\
                                \
                            </tr>"
    for i in range(0, len(swt4_storm_data)):
        if swt4_storm_data[i][0] == 0:
            storm_type = "Broadcast"
        elif swt4_storm_data[i][0] == 1:
            storm_type = "Multicast"
        elif swt4_storm_data[i][0] == 2:
            storm_type = "UDA"
        swt4_storm_str += "<tr>\
                            \
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                            \
                            </tr>" % (str(storm_type), "Off" if swt4_storm_data[i][1] == 0 else "On", "Off" if swt4_storm_data[i][2] == 0 else str(swt4_storm_data[i][2]))
    swt4_storm_str += "</table>"
    html.write(str(swt4_storm_str))


def update_vlan(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt_vlan_dic = swt4_get_vlan_data(host_id)
    swt_vlan_list = swt_vlan_dic["result"]
    swt_vlan_str = ""
    swt_vlan_str += "\
                    <table style=\"font-size:12px\" cellspacing=\"15\" cellpadding=\"10\">\
                        <tr align=\"left\">\
                            \
                            <th>Port</th>\
                            <th>PVID</th>\
                            <th>Mode</th>\
                            \
                        </tr>"
    for i in range(0, len(swt_vlan_list)):
        swt_vlan_str += "<tr align=\"left\">\
                                \
                                <td>%s</td>\
                                <td>%s</td>\
                                <td>%s</td>\
                                \
                            </tr>" % ("Port" + str(i + 1), swt_vlan_list[i][3], "Original" if swt_vlan_list[i][4] == 0 else "Keep Format")
    swt_vlan_str += "</table>"
    html.write(str(swt_vlan_str))


def update_port_priority(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_port_priority_list = swt4_get_port_priority(host_id)
    swt4_port_priority_data = swt4_port_priority_list["result"]
    swt4_port_priority_str = ""
    swt4_port_priority_str += "\
                                <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                    <tr align=\"left\">\
                                        \
                                        <th>Port</th>\
                                        <th>Priority</th>\
                                        \
                                        \
                                    </tr>"
    for i in range(0, len(swt4_port_priority_data)):
        if swt4_port_priority_data[i][0] == '0' or swt4_port_priority_data[i][0] == 0:
            port = "Port 1"
        elif swt4_port_priority_data[i][0] == '1' or swt4_port_priority_data[i][0] == 1:
            port = "Port 2"
        elif swt4_port_priority_data[i][0] == '2' or swt4_port_priority_data[i][0] == 2:
            port = "Port 3"
        elif swt4_port_priority_data[i][0] == '3' or swt4_port_priority_data[i][0] == 3:
            port = "Port 4"
        elif swt4_port_priority_data[i][0] == '4' or swt4_port_priority_data[i][0] == 4:
            port = "Port 5"
        swt4_port_priority_str += "<tr align=\"left\">\
                                    \
                                    <td>%s</td>\
                                    <td>%s</td>\
                                   \
                                    \
                                </tr>" % (port, swt4_port_priority_data[i][1])
    swt4_port_priority_str += "</table>"
    html.write(str(swt4_port_priority_str))


def update_dscp_priority(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_dscp_priority_list = swt4_get_dscp_priority(host_id)
    swt4_dscp_priority_data = swt4_dscp_priority_list["result"]
    swt4_dscp_priority_str = ""
    swt4_dscp_priority_str += "\
                                <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                    <tr align=\"left\">\
                                        \
                                        <th>DSCP</th>\
                                        <th>Priority</th>\
                                        \
                                        \
                                    </tr>"
    for i in range(0, len(swt4_dscp_priority_data)):
        swt4_dscp_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_dscp_priority_data[i][0].upper(), swt4_dscp_priority_data[i][1])
    swt4_dscp_priority_str += "</table>"
    html.write(str(swt4_dscp_priority_str))


def update_802_priority(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_802_priority_list = swt4_get_801_priority(host_id)
    swt4_802_priority_data = swt4_802_priority_list["result"]
    swt4_802_priority_str = ""
    swt4_802_priority_str += "\
                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                <tr align=\"left\">\
                                    \
                                    <th>802.1p</th>\
                                    <th>Priority</th>\
                                    \
                                    \
                                </tr>"
    for i in range(0, len(swt4_802_priority_data)):
        swt4_802_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_802_priority_data[i][0], swt4_802_priority_data[i][1])
    swt4_802_priority_str += "</table>"
    html.write(str(swt4_802_priority_str))


def update_ip_base_priority(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_ip_priority_list = swt4_get_ip_base_priority(host_id)
    swt4_ip_priority_data = swt4_ip_priority_list["result"]
    swt4_ip_priority_str = ""
    swt4_ip_priority_str += "\
                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                <tr align=\"left\">\
                                    \
                                    <th>Ip Type</th>\
                                    <th>Ip Address</th>\
                                    <th>Network Mask</th>\
                                    <th>Priority</th>\
                                    <th>Status</th>\
                                    \
                                    \
                                </tr>"
    for i in range(0, len(swt4_ip_priority_data)):
        swt4_ip_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % ("Group A" if swt4_ip_priority_data[i][1] == 0 else "Group B", swt4_ip_priority_data[i][2], swt4_ip_priority_data[i][3], swt4_ip_priority_data[i][4], "Disabled" if swt4_ip_priority_data[i][0] == 0 else "Enabled")
    swt4_ip_priority_str += "</table>"
    html.write(str(swt4_ip_priority_str))


def update_queue_priority(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_queue_priority_list = swt4_get_queue_prority(host_id)
    swt4_queue_priority_data = swt4_queue_priority_list["result"]
    swt4_queue_priority_str = ""
    swt4_queue_priority_str += "\
                                <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                    <tr align=\"left\">\
                                        \
                                        <th>QID MAP</th>\
                                        <th>Priority</th>\
                                        \
                                        \
                                    </tr>"
    for i in range(0, len(swt4_queue_priority_data)):
        swt4_queue_priority_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_queue_priority_data[i][0], swt4_queue_priority_data[i][1])
    swt4_queue_priority_str += "</table>"
    html.write(str(swt4_queue_priority_str))


def update_queue_weight(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_queue_weight_list = swt4_get_queue_weight(host_id)
    swt4_queue_weight_data = swt4_queue_weight_list["result"]
    swt4_queue_weight_str = ""
    swt4_queue_weight_str += "\
                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                <tr align=\"left\">\
                                    \
                                    <th>Queue</th>\
                                    <th>Weight</th>\
                                    \
                                    \
                                </tr>"
    for i in range(0, len(swt4_queue_weight_data)):
        swt4_queue_weight_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_queue_weight_data[i][0], swt4_queue_weight_data[i][1])
    swt4_queue_weight_str += "</table>"
    html.write(str(swt4_queue_weight_str))


def update_qos_abstraction(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_qos_abstraction_list = swt4_get_qos_abstraction(host_id)
    swt4_qos_abstraction_data = swt4_qos_abstraction_list["result"]
    swt4_qos_abstraction_str = ""
    swt4_qos_abstraction_str += "\
                                <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                    <tr align=\"left\">\
                                        \
                                        <th>Priority</th>\
                                        <th>Level</th>\
                                        \
                                        \
                                    </tr>"
    for i in range(0, len(swt4_qos_abstraction_data)):
        swt4_qos_abstraction_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_qos_abstraction_data[i][0], swt4_qos_abstraction_data[i][1])
    swt4_qos_abstraction_str += "</table>\
                        </div>\
                    </div>"
    html.write(str(swt4_qos_abstraction_str))


def update_1p_remarking(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    swt4_1p_remarking_list = swt4_get_1p_remarking(host_id)
    swt4_1p_remarking_data = swt4_1p_remarking_list["result"]
    swt4_1p_remarking_str = ""
    swt4_1p_remarking_str += "\
                            <table cellpadding=\"15\" cellspacing=\"15\" style=\"font-size:12px;\">\
                                <tr align=\"left\">\
                                    \
                                    <th>1P Remarkin</th>\
                                    <th>802.1P Priority</th>\
                                    \
                                    \
                                </tr>"
    for i in range(0, len(swt4_1p_remarking_data)):
        swt4_1p_remarking_str += "<tr align=\"left\">\
                                            \
                                            <td>%s</td>\
                                            <td>%s</td>\
                                            \
                                            \
                                        </tr>" % (swt4_1p_remarking_data[i][0], swt4_1p_remarking_data[i][1])
    swt4_1p_remarking_str += "</table>\
                        </div>\
                    </div>"
    html.write(str(swt4_1p_remarking_str))


def swt4_commit_flash(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    result = commit_to_flash(
        host_id)  # this funtion takes the host_id ,form names,forms parameters and return the dcitionary that the values are set or not
    html.write(str(result))


def reboot(h):
    """

    @param h:
    """
    global html
    html = h
    reboot_str = ""
    reboot_str += "<div>\
                        <form id=\"reboot_form\" name=\"reboot_form\">\
                            <div class=\"rowElem\">\
                                <label class=\"lbl\">Select Firmware</label>\
                                    <input type=\"radio\" name=\"firmwarebtngroup\" id=\"firmwarebtngroup\" value=\"1\"/>Primary\
                                    <input type=\"radio\" name=\"firmwarebtngroup\" id=\"firmwarebtngroup\" value=\"2\"/>Secondary\
                            </div>\
                            <div class=\"rowElem\">\
                                <input type=\"submit\" name=\"id_swt_submit_reboot\" value=\"Reboot\" id=\"id_swt_submit_reboot\">\
                            </div>\
                        </form>\
                </div>"
    html.write(reboot_str)


def reboot_final(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    firmware = html.var("firmware");
    result = reboot_final_controller(host_id, firmware)
    html.write(str(result))


def get_device_list(h):
    """
    Author- Anuj Samariya
    This function is used to get the list of Devices based on IPaddress,Macaddress,DeviceTypes
    ip_address - This is the IP Address of device e.g 192.168.0.1
    mac_address - This is the Mac Address of device e.g aa:bb:cc:dd:ee:ff
    selected_device - This is the selected device types from the drop down menu of devices e.g "odu16"
    @param h:
    """
    try:
        global html
        html = h
        # this is the result which we show on the page
        result = ""
        ip_address = ""
        mac_address = ""
        selected_device = "swt4"
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
            selected_device = "swt4"
        else:
            selected_device = html.var("selected_device_type")

        # call the function get_odu_list of odu-controller which return us the
        # list of devices in two dimensional list according to
        # IPAddress,MACaddress,SelectedDevice

        result = get_device_list_swt_profiling(
            ip_address, mac_address, selected_device)
        if result == 0 or result == 1 or result == 2:
            html.write(str(result))
        else:
            if result == None or result == "":
                html.write(str(result))
            else:
                swt4_profiling_form(result, selected_device)

    except Exception as e:
        html.write(str(e))
