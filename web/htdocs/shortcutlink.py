#!/usr/bin/python2.6

import datetime
import os
import subprocess
import time

import MySQLdb
import xml.dom.minidom

from ap_service import *
import config
from lib import *

###################################################################### AUTO DISCOVERY ########################################################################
# function to perform auto discovery in the network


def page_auto_discovery(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    css_list = ["css/style.css"]
    js_list = ["js/unmp/main/autodiscovery.js"]
    html.new_header("Auto Discovery", "", "", css_list, js_list)

    # Add Discovery Form in new Style
    html.write("<div class=\"tab-yo\">")
    html.write("<div class=\"tab-head\">")
    html.write(
        "<a id=\"pingButton\" href=\"#pingDiv\" class=\"tab-active\">Ping")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"snmpButton\" href=\"#snmpDiv\" class=\"tab-button\">Snmp")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"upnpButton\" href=\"#upnpDiv\" class=\"tab-button\">UPnP")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"sdmcButton\" href=\"#sdmcDiv\" class=\"tab-button\">SDM")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write("<h2>Auto Discovery")
    html.write("</h2>")
    html.write("</div>")

    # ping division
    html.write("<div id=\"pingDiv\" class=\"tab-body discoveryDetailsBody\">")
    html.write("<div id=\"form1\">")
    html.write("<div style=\"margin: 20px;\">")
    html.write(
        "<form id=\"autoDiscovery1\" action=\"ajaxcall_autodiscovery_ping.py\">")
    html.write("<table width=\"100%\">")
    html.write(
        "<colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"/></colgroup>")
    html.write(
        "<tr><td>IP Base</td><td><input type='text' name='ipBase1' id='ipBase1' value=''/></td><td class=\"desc\">Enter a class C Network IP base. e.g. 192.168.0</td></tr>")
    html.write(
        "<tr><td>IP Range Start</td><td><input type='text' name='ipRangeStart1' id='ipRangeStart1' value=''/></td><td class=\"desc\">Enter the IP octet of the Class C Network specified above from which NMS shall <b>start</b> discovering new devices.</td></tr>")
    html.write(
        "<tr><td>IP Range End</td><td><input type='text' name='ipRangeEnd1' id='ipRangeEnd1' value=''/></td><td class=\"desc\">Enter the IP octet of the Class C Network specified above at which NMS shall <b>stop</b> discovering new devices.</td></tr>")
    html.write(
        "<tr><td>Time Out</td><td><input type='text' name='timeOut1' id='timeOut1' value=''/></td><td class=\"desc\">Enter a timeout in seconds for the PING request.</td></tr>")
    html.write("<tr><td>Discovery Schedule</td><td>")
    html.write(
        "<select name=\"discoverySchedule1\" id=\"discoverySchedule1\" style=\"width:155px;\">")
    html.write("<option value=\"once\">Once</option>")
    html.write("<option value=\"daily\">Daily</option>")
    html.write("<option value=\"weekly\">Weekly</option>")
    html.write("<option value=\"monthly\">Monthly</option>")
    html.write("<option value=\"yearly\">Yearly</option>")
    html.write("</select>")
    html.write(
        "</td><td class=\"desc\">You can set the auto-discovery to run periodically.</td></tr>")
    html.write("<tr><td>Service Management</td><td>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" checked=\"checked\" value=\"1\" name=\"serviceManagement1\" id=\"serviceAutoScan1\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceAutoScan1\">Automatic Service creation</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input disabled=\"disabled\" type=\"radio\" value=\"2\" name=\"serviceManagement1\" id=\"serviceTemplate1\">")
    html.write(
        "<label style=\"cursor: pointer;color:#666;\" disabled=\"disabled\" for=\"serviceTemplate1\">Automatic Service creation using template(s)</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" value=\"0\" name=\"serviceManagement1\" id=\"serviceNot1\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceNot1\">Do not create Services</label>")
    html.write("</div>")
    html.write(
        "</td><td class=\"desc\">Choose \"Do not create services\" if you want to create and manage services manually. All other settings will scan your network and create the corresponding services. \"Automatic service creation\" is mainly based on Port Scanning, PING, SNMP and UPnP.</td></tr>")
    html.write("<tr><td>Host Group</td><td>" + hostgroup_multiple_select_list("", "HostGroup1") +
               "</td><td class=\"desc\"> Choose Host Group(s) to add new discovered host to</td></tr>")
    html.write("<tr><td class='button' colspan='3'>")
    html.write("<input type=\"submit\" value=\"Discover\" />")
    html.write(
        "<input type='button' value='Cancel' onclick=\"javascript:parent.main.location='main.py';\"/>")
    html.write("</td></tr>")
    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    # end ping division

    # snmp division
    html.write("<div id=\"snmpDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    html.write("<div id=\"form2\">")
    html.write("<div style=\"margin: 20px;\">")
    html.write(
        "<form id=\"autoDiscovery2\" action=\"ajaxcall_autodiscovery_snmp.py\">")
    html.write("<table width=\"100%\">")
    html.write(
        "<colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"/></colgroup>")
    html.write(
        "<tr><td>IP Base</td><td><input type='text' name='ipBase2' id='ipBase2' value=''/></td><td class=\"desc\">Enter a class C Network IP base. e.g. 192.168.0</td></tr>")
    html.write(
        "<tr><td>IP Range Start</td><td><input type='text' name='ipRangeStart2' id='ipRangeStart2' value=''/></td><td class=\"desc\">Enter the IP octet of the Class C Network specified above from which NMS shall <b>start</b> discovering new devices.</td></tr>")
    html.write(
        "<tr><td>IP Range End</td><td><input type='text' name='ipRangeEnd2' id='ipRangeEnd2' value=''/></td><td class=\"desc\">Enter the IP octet of the Class C Network specified above at which NMS shall <b>stop</b> discovering new devices.</td></tr>")
    html.write(
        "<tr><td>Time Out</td><td><input type='text' name='timeOut2' id='timeOut2' value=''/></td><td class=\"desc\">Enter a timeout in seconds for the SNMP request.</td></tr>")
    html.write(
        "<tr><td>Community</td><td><input type='text' name='community2' id='community2' value='public'/></td><td class=\"desc\">Enter community for the SNMP request.</td></tr>")
    html.write(
        "<tr><td>Port</td><td><input type='text' name='port2' id='port2' value='161'/></td><td class=\"desc\">Enter port number for the SNMP request.</td></tr>")
    html.write("<tr><td>SNMP Version</td><td>")
    html.write(
        "<select name=\"version2\" id=\"version2\" style=\"width:155px;\">")
    html.write("<option value=\"1\">v1</option>")
    html.write("<option value=\"2\">v2</option>")
    html.write("<option value=\"3\">v3</option>")
    html.write("</select>")
    html.write("</td><td class=\"desc\">Choose SNMP version.</td></tr>")
    # display if snmp version is v3
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>User Name</td><td><input type='text' name='userName2' id='userName2' value=''/></td><td class=\"desc\">Enter User name for secure authentication.</td></tr>")
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>Password</td><td><input type='text' name='password2' id='password2' value=''/></td><td class=\"desc\">Enter Password for secure authentication.</td></tr>")
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>Authentication Key</td><td><input type='text' name='authKey2' id='authKey2' value=''/></td><td class=\"desc\">Enter Password for secure authentication.</td></tr>")
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>Authentication Protocol</td><td><input type='text' name='authProtocol2' id='authProtocol2' value=''/></td><td class=\"desc\">Enter Authentication Protocol for secure authentication.</td></tr>")
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>Private Password</td><td><input type='text' name='privPassword2' id='privPassword2' value=''/></td><td class=\"desc\">Enter Private Password for secure authentication.</td></tr>")
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>Private Key</td><td><input type='text' name='privKey2' id='privKey2' value=''/></td><td class=\"desc\">Enter Private Key for secure authentication.</td></tr>")
    html.write(
        "<tr class=\"snmpv3Tr\" style=\"display:none;\"><td>Private Protocol</td><td><input type='text' name='privProtocol2' id='privProtocol2' value=''/></td><td class=\"desc\">Enter Private Protocol for secure authentication.</td></tr>")
    # display if snmp version is v3
    html.write("<tr><td>Discovery Schedule</td><td>")
    html.write(
        "<select name=\"discoverySchedule2\" id=\"discoverySchedule2\" style=\"width:155px;\">")
    html.write("<option value=\"once\">Once</option>")
    html.write("<option value=\"daily\">Daily</option>")
    html.write("<option value=\"weekly\">Weekly</option>")
    html.write("<option value=\"monthly\">Monthly</option>")
    html.write("<option value=\"yearly\">Yearly</option>")
    html.write("</select>")
    html.write(
        "</td><td class=\"desc\">You can set the auto-discovery to run periodically.</td></tr>")
    html.write("<tr><td>Service Management</td><td>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" checked=\"checked\" value=\"1\" name=\"serviceManagement2\" id=\"serviceAutoScan2\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceAutoScan2\">Automatic Service creation</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" disabled=\"disabled\" value=\"2\" name=\"serviceManagement2\" id=\"serviceTemplate2\">")
    html.write(
        "<label style=\"cursor: pointer;color:#666;\" disabled=\"disabled\" for=\"serviceTemplate2\">Automatic Service creation using template(s)</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" value=\"0\" name=\"serviceManagement2\" id=\"serviceNot2\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceNot2\">Do not create Services</label>")
    html.write("</div>")
    html.write(
        "</td><td class=\"desc\">Choose \"Do not create services\" if you want to create and manage services manually. All other settings will scan your network and create the corresponding services. \"Automatic service creation\" is mainly based on Port Scanning, PING, SNMP and UPnP.</td></tr>")
    html.write("<tr><td>Host Group</td><td>" + hostgroup_multiple_select_list("", "HostGroup2") +
               "</td><td class=\"desc\"> Choose Host Group(s) to add new discovered host to</td></tr>")
    html.write("<tr><td class='button' colspan='3'>")
    html.write("<input type=\"submit\" value=\"Discover\" />")
    html.write(
        "<input type='button' value='Cancel' onclick=\"javascript:parent.main.location='main.py';\"/>")
    html.write("</td></tr>")
    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    # end snmp division

    # upnp division
    html.write("<div id=\"upnpDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    html.write("<div id=\"form3\">")
    html.write("<div style=\"margin:20px;\">")
    html.write(
        "<form id=\"autoDiscovery3\" action=\"ajaxcall_autodiscovery_upnp.py\">")
    html.write("<table width=\"100%\">")
    html.write(
        "<colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"></colgroup>")
    html.write(
        "<tr><td>Time Out</td><td><input type='text' name='timeOut3' id='timeOut3' value=''/></td><td class=\"desc\">Enter a timeout in seconds for the UPnP request.</td></tr>")
    html.write("<tr><td>Discovery Schedule</td><td>")
    html.write(
        "<select name=\"discoverySchedule3\" id=\"discoverySchedule3\" style=\"width:155px;\">")
    html.write("<option value=\"once\">Once</option>")
    html.write("<option value=\"daily\">Daily</option>")
    html.write("<option value=\"weekly\">Weekly</option>")
    html.write("<option value=\"monthly\">Monthly</option>")
    html.write("<option value=\"yearly\">Yearly</option>")
    html.write("</select>")
    html.write(
        "</td><td class=\"desc\">You can set the auto-discovery to run periodically.</td></tr>")
    html.write("<tr><td>Service Management</td><td>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" checked=\"checked\" value=\"1\" name=\"serviceManagement3\" id=\"serviceAutoScan3\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceAutoScan3\">Automatic Service creation</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" value=\"2\" disabled=\"disabled\" name=\"serviceManagement3\" id=\"serviceTemplate3\">")
    html.write(
        "<label style=\"cursor: pointer;color:#666;\" disabled=\"disabled\" for=\"serviceTemplate3\">Automatic Service creation using template(s)</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" value=\"0\" name=\"serviceManagement3\" id=\"serviceNot3\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceNot3\">Do not create Services</label>")
    html.write("</div>")
    html.write(
        "</td><td class=\"desc\">Choose \"Do not create services\" if you want to create and manage services manually. All other settings will scan your network and create the corresponding services. \"Automatic service creation\" is mainly based on Port Scanning, PING, SNMP and UPnP.</td></tr>")
    html.write("<tr><td>Host Group</td><td>" + hostgroup_multiple_select_list("", "HostGroup3") +
               "</td><td class=\"desc\"> Choose Host Group(s) to add new discovered host to</td></tr>")
    html.write("<tr><td class='button' colspan='3'>")
    html.write("<input type=\"submit\" value=\"Discover\"/>")
    html.write(
        "<input type='button' value='Cancel' onclick=\"javascript:parent.main.location='main.py';\"/>")
    html.write("</td></tr>")
    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    # end upnp division

    # sdmc division
    html.write("<div id=\"sdmcDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    html.write("<div id=\"form4\">")
    html.write("<div style=\"margin:20px;\">")
    html.write(
        "<form id=\"autoDiscovery4\" action=\"ajaxcall_autodiscovery_sdmc.py\">")
    html.write("<table width=\"100%\">")
    html.write(
        "<colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"></colgroup>")
    html.write(
        "<tr><td>Time Out</td><td><input type='text' name='timeOut4' id='timeOut4' value=''/></td><td class=\"desc\">Enter a timeout in seconds for the Shyam device manager (sdm) request.</td></tr>")
    html.write("<tr><td>Discovery Schedule</td><td>")
    html.write(
        "<select name=\"discoverySchedule4\" id=\"discoverySchedule4\" style=\"width:155px;\">")
    html.write("<option value=\"once\">Once</option>")
    html.write("<option value=\"daily\">Daily</option>")
    html.write("<option value=\"weekly\">Weekly</option>")
    html.write("<option value=\"monthly\">Monthly</option>")
    html.write("<option value=\"yearly\">Yearly</option>")
    html.write("</select>")
    html.write(
        "</td><td class=\"desc\">You can set the auto-discovery to run periodically.</td></tr>")
    html.write("<tr><td>Service Management</td><td>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" checked=\"checked\" value=\"1\" name=\"serviceManagement4\" id=\"serviceAutoScan4\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceAutoScan4\">Automatic Service creation</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" value=\"2\" name=\"serviceManagement4\" id=\"serviceTemplate4\">")
    html.write(
        "<label style=\"cursor: pointer;\" for=\"serviceTemplate4\">Automatic Service creation using template(s)</label>")
    html.write("</div>")
    html.write("<div class=\"option-bar\">")
    html.write(
        "<input type=\"radio\" value=\"0\" name=\"serviceManagement4\" id=\"serviceNot4\">")
    html.write("<label style=\"cursor: pointer;\" for=\"serviceNot4\">Do not create Services</label>")
    html.write("</div>")
    html.write(
        "</td><td class=\"desc\">Choose \"Do not create services\" if you want to create and manage services manually. All other settings will scan your network and create the corresponding services. \"Automatic service creation\" is mainly based on Port Scanning, PING, SNMP and UPnP.</td></tr>")
    # choose device type to be search
    html.write("<tr><td>Choose device</td><td>" + shyamDevicesList(sitename) +
               "</td><td class=\"desc\">Choose devices to be search.<br/><br/><label class=\"error\" for=\"deviceList\" style=\"display: none;\">Please select at least one device.</label></td></tr>")
    # end choose device type to be search
    html.write("<tr><td>Host Group</td><td>" + hostgroup_multiple_select_list("", "HostGroup4") +
               "</td><td class=\"desc\"> Choose Host Group(s) to add new discovered host to</td></tr>")
    html.write("<tr><td class='button' colspan='3'>")
    html.write("<input type=\"submit\" value=\"Discover\"/>")
    html.write(
        "<input type='button' value='Cancel' onclick=\"javascript:parent.main.location='main.py';\"/>")
    html.write("</td></tr>")
    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    # end sdmc division

    html.new_footer()
    # discovery loading
    # html.write("<div style=\"position:fixed;width:180px;right:10px; bottom:0; direction:ltr;z-index:200;display:none;\" id=\"loadingDiscovery\" >")
    # html.write("<div class=\"main-title\" style=\"cursor: pointer;\"><span id=\"boxTitle\">Auto Discovery</span></div>")
    # html.write("<div class=\"template-div\" id=\"discoveryMessage\">")
    # html.write("<div class=\"sub-title\"><b>Done: </b><span id=\"result\">100 %</span></div>")
    # html.write("</div>")
    # html.write("</div>")
    # html.write("<div class=\"loading\" ><img src='images/loading.gif' alt=''/></div>")
    # html.write("<input type=\"button\" value=\"Discover\" onclick=\"discovery()\" class=\"sexybutton sexysimple sexysmall\" style=\"width:100px;margin-right:10px;\" />")
    # html.write("<input type='button' value='Cancel'
    # onclick=\"javascript:parent.main.location='main.py';\"
    # class=\"sexybutton sexysimple sexysmall\" style=\"width:100px;margin-
    # right:10px;\"/>")


def shyamDevicesList(sitename):
    """

    @param sitename:
    @return:
    """
    deviceList = "<div class=\"multiSelectList\" style=\"width:430px;\">"
    deviceList += "<div class=\"selected\" style=\"width:100%\">"
    deviceList += "<div class=\"shead\"><div style=\"float:left;width:5%;padding-left:10px; padding-top:1px;\"><input type=\"checkbox\" id=\"allDevices\" name=\"allDevices\" value=\"all\"/></div>"
    deviceList += "<span><label for=\"allDevices\">Shyam Devices</label></span></div>"
    deviceList += "<ul>"

    # load shyam device form syhamdevices.xml file
    shyamDeviceFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/shyamdevices.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString("<shyamDevices><device/></shyamDevices>")
    if (os.path.isfile(shyamDeviceFile)):
        dom = xml.dom.minidom.parse(shyamDeviceFile)
    deviceListXml = dom.getElementsByTagName("device")
    i = 0
    for dev in deviceListXml:
        if dev.getAttribute("hide") == "false":
            i += 1
            deviceList += "<li><div style=\"width: 7%; float: left; height: 20px;\"><input type=\"checkbox\" id=\"" + dev.getAttribute(
                "id") + "\" name=\"deviceList\" value=\"" + dev.getAttribute("sdmcDiscoveryId") + "\"/></div>"
            deviceList += "<div style=\"width: 92%; float: left; overflow: hidden; height: 20px;\"><label for=\"" + dev.getAttribute(
                "id") + "\">" + dev.getAttribute("name") + "</label></div></li>"
    deviceList += "<input type=\"hidden\" id=\"totalShyamDevice\" name=\"totalShyamDevice\" value=\"" + str(
        i) + "\"/>"
    deviceList += "</ul></div></div>"
    return deviceList


def autodiscovery_ping(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    ipBase = html.var("ipBase1")
    ipRangeStart = html.var("ipRangeStart1")
    ipRangeEnd = html.var("ipRangeEnd1")
    timeOut = html.var("timeOut1")
    discoverySchedule = html.var("discoverySchedule1")
    serviceManagement = html.var("serviceManagement1")
    hostGroup = html.var("hdHostGroup1")
    userName = config.user
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % (
        sitename)
    nmsSchedulingXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/nmsScheduling.xml" % (
        sitename)
    checkAutoDiscovery = checkAutoDiscoveryActive(
        hostGroup, ipBase, ipRangeStart, ipRangeEnd, serviceManagement, timeOut, userName, nmsXmlFile, "ping", "", "",
        "", "", "", "", "", "", "", "")
    if checkAutoDiscovery == "1":
        if discoverySchedule != "once":
            # save host configuration page details
            dom = xml.dom.minidom.parseString(
                "<nmsDB><autoDiscoveryScheduling/></nmsDB>")
            if (os.path.isfile(nmsSchedulingXmlFile)):
                dom = xml.dom.minidom.parse(nmsSchedulingXmlFile)

            # Check auto discovery Active or not
            autoDiscoverySchedulingTag = dom.getElementsByTagName(
                "autoDiscoveryScheduling")[0]
            discoverySchedulingDom = dom.createElement("schedule")
            discoverySchedulingDom.setAttribute("ip", ipBase)
            discoverySchedulingDom.setAttribute("start", ipRangeStart)
            discoverySchedulingDom.setAttribute("end", ipRangeEnd)
            discoverySchedulingDom.setAttribute("timeout", timeOut)
            discoverySchedulingDom.setAttribute(
                "scheduling", discoverySchedule)

            discoverySchedulingDom.setAttribute("hostgroup", hostGroup)
            discoverySchedulingDom.setAttribute("username", userName)
            discoverySchedulingDom.setAttribute("service", serviceManagement)
            discoverySchedulingDom.setAttribute("type", "ping")
            if discoverySchedule == "daily":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=1)))
            if discoverySchedule == "weekly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=7)))
            if discoverySchedule == "monthly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=30)))
            if discoverySchedule == "yearly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=365)))
            i = 0
            for discoverySchedulingTag in autoDiscoverySchedulingTag.getElementsByTagName("schedule"):
                if discoverySchedulingTag.getAttribute("type") == "ping" and discoverySchedulingTag.getAttribute(
                        "username") == userName and discoverySchedulingTag.getAttribute("ip") == ipBase:
                    i += 1
                    dom.getElementsByTagName("autoDiscoveryScheduling")[0].replaceChild(
                        discoverySchedulingDom, discoverySchedulingTag)
                    fwxml = open(nmsSchedulingXmlFile, "w")
                    fwxml.write(dom.toxml())
                    fwxml.close()
                    html.write(
                        "2")  # return 2 to start autodiscovery and schudling replaced by existing scheduling.
                    break
            if i == 0:
                dom.getElementsByTagName(
                    "autoDiscoveryScheduling")[0].appendChild(discoverySchedulingDom)
                fwxml = open(nmsSchedulingXmlFile, "w")
                fwxml.write(dom.toxml())
                fwxml.close()
                html.write(
                    "3")        # return 3 to start autodiscovery and add new scheduling details.
        else:
            html.write(checkAutoDiscovery)
            # return 1 to start autodiscovery and no scheduling
            # saved.
    else:
        html.write(checkAutoDiscovery)


def autodiscovery_snmp(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    ipBase = html.var("ipBase2")
    ipRangeStart = html.var("ipRangeStart2")
    ipRangeEnd = html.var("ipRangeEnd2")
    timeOut = html.var("timeOut2")
    discoverySchedule = html.var("discoverySchedule2")
    serviceManagement = html.var("serviceManagement2")
    hostGroup = html.var("hdHostGroup2")
    userName = config.user
    community = html.var("community2")
    port = html.var("port2")
    version = html.var("version2")
    snmpUserName = html.var("userName2")
    snmpPassword = html.var("password2")
    authKey = html.var("authKey2")
    authProtocol = html.var("authProtocol2")
    privPassword = html.var("privPassword2")
    privKey = html.var("privKey2")
    privProtocol = html.var("privProtocol2")
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % (
        sitename)
    nmsSchedulingXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/nmsScheduling.xml" % (
        sitename)
    checkAutoDiscovery = checkAutoDiscoveryActive(
        hostGroup, ipBase, ipRangeStart, ipRangeEnd, serviceManagement, timeOut, userName, nmsXmlFile, "snmp",
        community, port, version, snmpUserName,
        snmpPassword, authKey, authProtocol, privPassword, privKey, privProtocol)
    if checkAutoDiscovery == "1":
        if discoverySchedule != "once":
            # save host configuration page details
            dom = xml.dom.minidom.parseString(
                "<nmsDB><autoDiscoveryScheduling/></nmsDB>")
            if (os.path.isfile(nmsSchedulingXmlFile)):
                dom = xml.dom.minidom.parse(nmsSchedulingXmlFile)

            # Check auto discovery Active or not
            autoDiscoverySchedulingTag = dom.getElementsByTagName(
                "autoDiscoveryScheduling")[0]
            discoverySchedulingDom = dom.createElement("schedule")
            discoverySchedulingDom.setAttribute("ip", ipBase)
            discoverySchedulingDom.setAttribute("start", ipRangeStart)
            discoverySchedulingDom.setAttribute("end", ipRangeEnd)
            discoverySchedulingDom.setAttribute("timeout", timeOut)
            discoverySchedulingDom.setAttribute("community", community)
            discoverySchedulingDom.setAttribute("port", port)
            discoverySchedulingDom.setAttribute("version", version)
            discoverySchedulingDom.setAttribute("snmpUser", snmpUserName)
            discoverySchedulingDom.setAttribute("password", snmpPassword)
            discoverySchedulingDom.setAttribute("authKey", authKey)
            discoverySchedulingDom.setAttribute("authProtocol", authProtocol)
            discoverySchedulingDom.setAttribute("privPassword", privPassword)
            discoverySchedulingDom.setAttribute("privKey", privKey)
            discoverySchedulingDom.setAttribute("privProtocol", privProtocol)
            discoverySchedulingDom.setAttribute(
                "scheduling", discoverySchedule)

            discoverySchedulingDom.setAttribute("hostgroup", hostGroup)
            discoverySchedulingDom.setAttribute("username", userName)
            discoverySchedulingDom.setAttribute("service", serviceManagement)
            discoverySchedulingDom.setAttribute("type", "snmp")
            if discoverySchedule == "daily":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=1)))
            if discoverySchedule == "weekly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=7)))
            if discoverySchedule == "monthly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=30)))
            if discoverySchedule == "yearly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=365)))
            i = 0
            for discoverySchedulingTag in autoDiscoverySchedulingTag.getElementsByTagName("schedule"):
                if discoverySchedulingTag.getAttribute("type") == "snmp" and discoverySchedulingTag.getAttribute(
                        "username") == userName and discoverySchedulingTag.getAttribute("ip") == ipBase:
                    i += 1
                    dom.getElementsByTagName("autoDiscoveryScheduling")[0].replaceChild(
                        discoverySchedulingDom, discoverySchedulingTag)
                    fwxml = open(nmsSchedulingXmlFile, "w")
                    fwxml.write(dom.toxml())
                    fwxml.close()
                    html.write(
                        "2")  # return 2 to start autodiscovery and schudling replaced by existing scheduling.
                    break
            if i == 0:
                dom.getElementsByTagName(
                    "autoDiscoveryScheduling")[0].appendChild(discoverySchedulingDom)
                fwxml = open(nmsSchedulingXmlFile, "w")
                fwxml.write(dom.toxml())
                fwxml.close()
                html.write(
                    "3")        # return 3 to start autodiscovery and add new scheduling details.
        else:
            html.write(checkAutoDiscovery)
            # return 1 to start autodiscovery and no scheduling
            # saved.
    else:
        html.write(checkAutoDiscovery)


def autodiscovery_upnp(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    timeOut = html.var("timeOut3")
    discoverySchedule = html.var("discoverySchedule3")
    serviceManagement = html.var("serviceManagement3")
    hostGroup = html.var("hdHostGroup3")
    userName = config.user
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % (
        sitename)
    nmsSchedulingXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/nmsScheduling.xml" % (
        sitename)
    checkAutoDiscovery = checkAutoDiscoveryActive(
        hostGroup, "", "1", "100", serviceManagement, timeOut, userName, nmsXmlFile, "upnp", "", "", "", "", "", "", "",
        "", "", "")
    if checkAutoDiscovery == "1":
        if discoverySchedule != "once":
            # save host configuration page details
            dom = xml.dom.minidom.parseString(
                "<nmsDB><autoDiscoveryScheduling/></nmsDB>")
            if (os.path.isfile(nmsSchedulingXmlFile)):
                dom = xml.dom.minidom.parse(nmsSchedulingXmlFile)

            # Check auto discovery Active or not
            autoDiscoverySchedulingTag = dom.getElementsByTagName(
                "autoDiscoveryScheduling")[0]
            discoverySchedulingDom = dom.createElement("schedule")
            discoverySchedulingDom.setAttribute("hostgroup", hostGroup)
            discoverySchedulingDom.setAttribute("username", userName)
            discoverySchedulingDom.setAttribute("service", serviceManagement)
            discoverySchedulingDom.setAttribute("timeout", timeOut)
            discoverySchedulingDom.setAttribute("type", "upnp")
            discoverySchedulingDom.setAttribute(
                "scheduling", discoverySchedule)
            if discoverySchedule == "daily":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=1)))
            if discoverySchedule == "weekly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=7)))
            if discoverySchedule == "monthly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=30)))
            if discoverySchedule == "yearly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=365)))
            i = 0
            for discoverySchedulingTag in autoDiscoverySchedulingTag.getElementsByTagName("schedule"):
                if discoverySchedulingTag.getAttribute("type") == "upnp" and discoverySchedulingTag.getAttribute(
                        "username") == userName and discoverySchedulingTag.getAttribute("hostgroup") == hostGroup:
                    i += 1
                    dom.getElementsByTagName("autoDiscoveryScheduling")[0].replaceChild(
                        discoverySchedulingDom, discoverySchedulingTag)
                    fwxml = open(nmsSchedulingXmlFile, "w")
                    fwxml.write(dom.toxml())
                    fwxml.close()
                    html.write(
                        "2")  # return 2 to start autodiscovery and schudling replaced by existing scheduling.
                    break
            if i == 0:
                dom.getElementsByTagName(
                    "autoDiscoveryScheduling")[0].appendChild(discoverySchedulingDom)
                fwxml = open(nmsSchedulingXmlFile, "w")
                fwxml.write(dom.toxml())
                fwxml.close()
                html.write(
                    "3")        # return 3 to start autodiscovery and add new scheduling details.
        else:
            html.write(checkAutoDiscovery)
            # return 1 to start autodiscovery and no scheduling
            # saved.
    else:
        html.write(checkAutoDiscovery)
        # return user name, who is already execute this dicovery

# sdmc utilty discovery start


def autodiscovery_sdmc(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    timeOut = html.var("timeOut4")
    discoverySchedule = html.var("discoverySchedule4")
    serviceManagement = html.var("serviceManagement4")
    hostGroup = html.var("hdHostGroup4")
    selectedDeviceList = html.var("allDeviceList")
    userName = config.user
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % (
        sitename)
    nmsSchedulingXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/nmsScheduling.xml" % (
        sitename)
    checkAutoDiscovery = checkAutoDiscoveryActive(
        hostGroup, selectedDeviceList, "1", "100", serviceManagement, timeOut, userName, nmsXmlFile, "sdmc", "", "", "",
        "", "", "", "", "", "", "")
    if checkAutoDiscovery == "1":
        if discoverySchedule != "once":
            # save host configuration page details
            dom = xml.dom.minidom.parseString(
                "<nmsDB><autoDiscoveryScheduling/></nmsDB>")
            if (os.path.isfile(nmsSchedulingXmlFile)):
                dom = xml.dom.minidom.parse(nmsSchedulingXmlFile)

            # Check auto discovery Active or not
            autoDiscoverySchedulingTag = dom.getElementsByTagName(
                "autoDiscoveryScheduling")[0]
            discoverySchedulingDom = dom.createElement("schedule")
            discoverySchedulingDom.setAttribute("hostgroup", hostGroup)
            discoverySchedulingDom.setAttribute("device", selectedDeviceList)
            discoverySchedulingDom.setAttribute("username", userName)
            discoverySchedulingDom.setAttribute("service", serviceManagement)
            discoverySchedulingDom.setAttribute("timeout", timeOut)
            discoverySchedulingDom.setAttribute("type", "sdmc")
            discoverySchedulingDom.setAttribute(
                "scheduling", discoverySchedule)
            if discoverySchedule == "daily":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=1)))
            if discoverySchedule == "weekly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=7)))
            if discoverySchedule == "monthly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=30)))
            if discoverySchedule == "yearly":
                discoverySchedulingDom.setAttribute("schedulingDateTime", str(
                    datetime.datetime.now() + datetime.timedelta(days=365)))
            i = 0
            for discoverySchedulingTag in autoDiscoverySchedulingTag.getElementsByTagName("schedule"):
                if discoverySchedulingTag.getAttribute("type") == "sdmc" and discoverySchedulingTag.getAttribute(
                        "username") == userName and discoverySchedulingTag.getAttribute("hostgroup") == hostGroup:
                    i += 1
                    dom.getElementsByTagName("autoDiscoveryScheduling")[0].replaceChild(
                        discoverySchedulingDom, discoverySchedulingTag)
                    fwxml = open(nmsSchedulingXmlFile, "w")
                    fwxml.write(dom.toxml())
                    fwxml.close()
                    html.write(
                        "2")  # return 2 to start autodiscovery and schudling replaced by existing scheduling.
                    break
            if i == 0:
                dom.getElementsByTagName(
                    "autoDiscoveryScheduling")[0].appendChild(discoverySchedulingDom)
                fwxml = open(nmsSchedulingXmlFile, "w")
                fwxml.write(dom.toxml())
                fwxml.close()
                html.write(
                    "3")        # return 3 to start autodiscovery and add new scheduling details.
        else:
            html.write(checkAutoDiscovery)
            # return 1 to start autodiscovery and no scheduling
            # saved.
    else:
        html.write(checkAutoDiscovery)
        # return user name, who is already execute this dicovery


# this function check autodiscovery active or not, if it is active then return 'user name' who activate it else make it active and return 1,
# if this autodiscovery parameter doesnot exist in xml then it will add it
# automatically and return 1.
def checkAutoDiscoveryActive(hostGroup, ipBase, start, end, service, timeout, userName, nmsXmlFile, discoveryType,
                             snmpCommunity, snmpPort, snmpVersion, snmpUserName, snmpPasswrod, authKey, authProtocol,
                             privPassword, privKey, privProtocol):
    # save host configuration page details
    """

    @param hostGroup:
    @param ipBase:
    @param start:
    @param end:
    @param service:
    @param timeout:
    @param userName:
    @param nmsXmlFile:
    @param discoveryType:
    @param snmpCommunity:
    @param snmpPort:
    @param snmpVersion:
    @param snmpUserName:
    @param snmpPasswrod:
    @param authKey:
    @param authProtocol:
    @param privPassword:
    @param privKey:
    @param privProtocol:
    @return:
    """
    dom = xml.dom.minidom.parseString(
        "<nmsDB><autoDiscovery/><discoveredHosts/></nmsDB>")
    dom2 = xml.dom.minidom.parseString(
        "<nmsDB><autoDiscovery/><discoveredHosts/></nmsDB>")
    if (os.path.isfile(nmsXmlFile)):
        dom = xml.dom.minidom.parse(nmsXmlFile)

    # Check auto discovery Active or not
    autoDiscoveryTag = dom.getElementsByTagName("autoDiscovery")[0]
    discoveryDom = dom2.createElement("discovery")
    if discoveryType == "ping":
        discoveryDom.setAttribute("hostgroup", hostGroup)
        discoveryDom.setAttribute("username", userName)
        discoveryDom.setAttribute("ip", ipBase)
        discoveryDom.setAttribute("start", start)
        discoveryDom.setAttribute("end", end)
        discoveryDom.setAttribute("current", start)
        discoveryDom.setAttribute("service", service)
        discoveryDom.setAttribute("timeout", timeout)
        discoveryDom.setAttribute("active", "1")
        discoveryDom.setAttribute("complete", "0")
        discoveryDom.setAttribute("type", discoveryType)
    elif discoveryType == "snmp":
        discoveryDom.setAttribute("hostgroup", hostGroup)
        discoveryDom.setAttribute("username", userName)
        discoveryDom.setAttribute("ip", ipBase)
        discoveryDom.setAttribute("start", start)
        discoveryDom.setAttribute("end", end)
        discoveryDom.setAttribute("current", start)
        discoveryDom.setAttribute("service", service)
        discoveryDom.setAttribute("timeout", timeout)
        discoveryDom.setAttribute("active", "1")
        discoveryDom.setAttribute("complete", "0")
        discoveryDom.setAttribute("type", discoveryType)
        discoveryDom.setAttribute("community", snmpCommunity)
        discoveryDom.setAttribute("port", snmpPort)
        discoveryDom.setAttribute("version", snmpVersion)
        discoveryDom.setAttribute("snmpUser", snmpUserName)
        discoveryDom.setAttribute("password", snmpPasswrod)
        discoveryDom.setAttribute("authKey", authKey)
        discoveryDom.setAttribute("authProtocol", authProtocol)
        discoveryDom.setAttribute("privPassword", privPassword)
        discoveryDom.setAttribute("privKey", privKey)
        discoveryDom.setAttribute("privProtocol", privProtocol)
    elif discoveryType == "upnp":
        discoveryDom.setAttribute("hostgroup", hostGroup)
        discoveryDom.setAttribute("username", userName)
        discoveryDom.setAttribute("ip", ipBase)
        discoveryDom.setAttribute("start", start)
        discoveryDom.setAttribute("end", end)
        discoveryDom.setAttribute("current", start)
        discoveryDom.setAttribute("service", service)
        discoveryDom.setAttribute("timeout", timeout)
        discoveryDom.setAttribute("active", "1")
        discoveryDom.setAttribute("complete", "0")
        discoveryDom.setAttribute("type", discoveryType)
    else:
        discoveryDom.setAttribute("hostgroup", hostGroup)
        discoveryDom.setAttribute("username", userName)
        discoveryDom.setAttribute("device", ipBase)
        discoveryDom.setAttribute("start", start)
        discoveryDom.setAttribute("end", end)
        discoveryDom.setAttribute("current", start)
        discoveryDom.setAttribute("service", service)
        discoveryDom.setAttribute("timeout", timeout)
        discoveryDom.setAttribute("active", "1")
        discoveryDom.setAttribute("complete", "0")
        discoveryDom.setAttribute("type", discoveryType)

    i = 0
    for discoveryTag in autoDiscoveryTag.getElementsByTagName("discovery"):
        if discoveryTag.getAttribute("type") == discoveryType:
            i += 1
            if discoveryTag.getAttribute("active") == "1":
                return discoveryTag.getAttribute("username")
            else:
                dom2.getElementsByTagName(
                    "autoDiscovery")[0].appendChild(discoveryDom)
                fwxml = open(nmsXmlFile, "w")
                fwxml.write(dom2.toxml())
                fwxml.close()
                return "1"
    if i == 0:
        dom2.getElementsByTagName("autoDiscovery")[0].appendChild(discoveryDom)

    fwxml = open(nmsXmlFile, "w")
    fwxml.write(dom2.toxml())
    fwxml.close()
    return "1"


def start_autodiscovery_ping(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    ipBase = html.var("ipBase1")
    ipRangeStart = html.var("ipRangeStart1")
    ipRangeEnd = html.var("ipRangeEnd1")
    timeOut = html.var("timeOut1")
    discoverySchedule = html.var("discoverySchedule1")
    serviceManagement = html.var("serviceManagement1")
    hostGroup = html.var("hdHostGroup1")
    userName = config.user
    hostFile = "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % (sitename)
    serviceFile = "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % (sitename)
    hostTemplate = "generic-host"
    serviceTemplate = "generic-service"
    hostCheckCommand = ""
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % (
        sitename)
    perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/pingdiscoverycreatexml.pl" % (
        sitename)
    # nagiosFile = "/omd/sites/%s/share/check_mk/web/htdocs/nagiosfile.pl" %(sitename)
    # portscanFile = "/omd/sites/%s/share/check_mk/web/htdocs/portscan.pl"
    # %(sitename)
    args = [ipBase + "." + ipRangeStart, ipBase + "." + ipRangeEnd,
            timeOut, nmsXmlFile]
    command = [perlFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    html.write(pipe)


def start_autodiscovery_snmp(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    ipBase = html.var("ipBase2")
    ipRangeStart = html.var("ipRangeStart2")
    ipRangeEnd = html.var("ipRangeEnd2")
    timeOut = html.var("timeOut2")
    discoverySchedule = html.var("discoverySchedule2")
    serviceManagement = html.var("serviceManagement2")
    hostGroup = html.var("hdHostGroup2")
    userName = config.user
    community = html.var("community2")
    port = html.var("port2")
    version = html.var("version2")
    snmpUserName = html.var("userName2")
    snmpPassword = html.var("password2")
    authKey = html.var("authKey2")
    authProtocol = html.var("authProtocol2")
    privPassword = html.var("privPassword2")
    privKey = html.var("privKey2")
    privProtocol = html.var("privProtocol2")
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % (
        sitename)
    perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/snmpdiscoverycreatexml.pl" % (
        sitename)
    args = [
        ipBase + "." + ipRangeStart, ipBase + "." +
                                     ipRangeEnd, community, timeOut, version, port,
        snmpUserName, authKey, snmpPassword, authProtocol, privKey, privPassword, privProtocol, nmsXmlFile]
    command = [perlFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    html.write(pipe)


def start_autodiscovery_upnp(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    timeOut = html.var("timeOut3")
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % (
        sitename)
    perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/upnpdiscoverycreatexml.pl" % (
        sitename)
    args = [timeOut, nmsXmlFile]
    command = [perlFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    html.write(pipe)


def start_autodiscovery_sdmc(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]

    # varify the variables
    timeOut = html.var("timeOut4")
    selectedDeviceList = html.var("allDeviceList")
    nmsXmlFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % (
        sitename)
    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)
    args = ["--discovery", "-l", selectedDeviceList, "-o ", timeOut,
            "-P", "54321"]
    command = [sdmcFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]

    #===================================================================================================
    # Output string of sdm utlity
    #     pipe = """
    #	Discovery Time less than or equal to 5 seconds,setting default time 5 seconds
    #
    #
    # DeviceType AP:
    #
    # Sl.No, IPAddress, MacAddress, SSID, HostName, FirmwareVersion, BootloaderVersion
    # 0, 192.168.5.31, 00:50:c2:bc:c8:02, VVDN_AP,11nAP, 1.1.1.0-347, 0.0.4
    #
    #"""
    #=========================================================================

    # get the sdmc string form shyam devices xml file
    DeviceList = selectedDeviceList.split(",")  # [1,2,3,4,5]
    sdmcStringArray = []  # ["AP","CPE","POP"]
    shyamDeviceFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/shyamdevices.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString("<shyamDevices><device/></shyamDevices>")
    if (os.path.isfile(shyamDeviceFile)):
        dom = xml.dom.minidom.parse(shyamDeviceFile)
    deviceListXml = dom.getElementsByTagName("device")

    # create xml object for writing searched device in sdmcDicovery.xml file
    dom2 = xml.dom.minidom.parse(nmsXmlFile)
    autoDiscoveryTag = dom2.getElementsByTagName("autoDiscovery")[0]

    for discoveryTag in autoDiscoveryTag.getElementsByTagName("discovery"):
        discoveryTag.setAttribute("active", "0")
        discoveryTag.setAttribute("complete", "100")
        discoveryTag.setAttribute("current", "100")

    for deviceId in DeviceList:
        tempsdmc = ""
        for dev in deviceListXml:
            if dev.getAttribute("sdmcDiscoveryId") == deviceId:
                tempsdmc = dev.getAttribute("sdmcDiscoveryValue")
                break
        sdmcStringArray.append(tempsdmc)

    outputStringArray = pipe.split("\n")  # split sdmc output string

    for sdmcString in sdmcStringArray:
        i = 0
        for outputString in outputStringArray:
            if outputString.find("DeviceType") >= 0:
                if outputString.find("DeviceType: " + sdmcString) >= 0:
                    i = 1
                else:
                    i = 0
            elif outputString.strip() == "" or outputString.strip() == "Sl.No, IPAddress, MacAddress, SSID, HostName, FirmwareVersion, BootloaderVersion":
                pass
            else:
                if i == 1:
                    # html.write("Device type: " + sdmcString + " Value: "+ outputString + "\n")
                    # Device type: AP Value:
                    # 0,192.168.5.31,00:50:c2:bc:c8:02,VVDN_AP,11nAP,1.1.1.0-347,0.0.4
                    hostDetails = outputString.split(", ")
                    hostDom = dom2.createElement("host")
                    hostDom.setAttribute("name", hostDetails[1].strip())
                    hostDom.setAttribute("alias", hostDetails[4].strip())
                    hostDom.setAttribute("address", hostDetails[1].strip())
                    hostDom.setAttribute("type", sdmcString)
                    dom2.getElementsByTagName(
                        "discoveredHosts")[0].appendChild(hostDom)

    fwxml = open(nmsXmlFile, "w")
    fwxml.write(dom2.toxml())
    fwxml.close()
    # html.write(str(outputStringArray))


def reload_nagios_configfile(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    os.system('kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
    html.write("1")

###################################################################### END

# function to choose option for manage host group, host, service group and
# service manually


def page_manage_host_service(h):
    """

    @param h:
    """
    global html
    html = h
    html.new_header("Manage Host and Service")

    html.write("""
<div class="shortcut-icon-div" style="width:20%;height:30px;clear:both;" onclick="javascript:parent.main.location='manage_hostgroup.py';">
<div><img src="images/button_edit_hi.png" alt=""/></div>
<div style="width:60%;"><b>Manage Host group</b></div>
</div>
<div class="shortcut-icon-div" style="width:20%;height:30px;" onclick="javascript:parent.main.location='manage_servicegroup.py';">
<div><img src="images/button_edit_hi.png" alt=""/></div>
<div style="width:60%;"><b>Manage Service group</b></div>
</div>
<div class="shortcut-icon-div" style="width:20%;height:30px;" onclick="javascript:parent.main.location='manage_host.py';">
<div><img src="images/button_edit_hi.png" alt=""/></div>
<div style="width:60%;"><b>Manage Host</b></div>
</div>
<div class="shortcut-icon-div" style="width:20%;height:30px;clear:both;" onclick="javascript:parent.main.location='manage_service.py';">
<div><img src="images/button_edit_hi.png" alt=""/></div>
<div style="width:60%;"><b>Manage Service</b></div>
</div>
<div class="shortcut-icon-div" style="width:20%;height:30px;" onclick="javascript:parent.main.location='main.py';">
<div><img src="images/button_edit_lo.png" alt=""/></div>
<div style="width:60%;"><b>Back</b></div>
</div>
""")
    html.new_footer()


###################################################################### HOST GROUP ########################################################################
# function to add edit delete host group details manually.
def page_manage_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/hostgroup.js"]
    html.new_header("Manage Host Group", "", "", css_list, js_list)
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt='loading...'/></div>")
    html.write(
        "<div id=\"formDiv\"></div><table class='addform' id='addhosttable' style='margin-bottom:0px;cursor:pointer;'><colgroup><col width='1%'/><col width='99%'/></colgroup><tr><th><img src='images/add16.png' alt='add'/></th><th>Add Host Group</th></tr></table></div>")
    html.write("<div id=\"gridviewDiv\">")
    grid_view_hostgroup(h)
    html.write("</div>")
    html.footer()
    # message and options before delete host group
    html.write(
        "<div style=\"position:fixed;width:400px;left:21%; right:auto; bottom:35%; direction:ltr;z-index:200;display:none;\" id=\"DeleteHostGroupMsg\" >")
    html.write(
        "<div class=\"main-title\" style=\"cursor: pointer;\"><span id=\"boxTitle\">Delete Host Group</span></div>")
    html.write("<div class=\"template-div\">")
    html.write(
        "<div class=\"sub-title\"><input type=\"radio\" id=\"command1\" name=\"command\" value=\"donot delete host\" checked=\"checked\"/><label style=\"vertical-align: bottom;margin-left:3px;\" for=\"command1\">Delete only Host group</label></div>")
    html.write(
        "<div class=\"sub-title\"><input type=\"radio\" id=\"command2\" name=\"command\" value=\"delete host\"/><label style=\"vertical-align: bottom;margin-left:3px;\" for=\"command2\">Delete Host group and Hosts both.</label></div>")
    html.write("<div class=\"row-odd\" style=\"margin: 10px;\">")
    html.write(
        "<input type=\"button\" value=\"Ok\" style=\"width:80px;\" onclick=\"okDelete()\">")
    html.write(
        "<input type=\"button\" value=\"Cancel\" style=\"width:80px;\" onclick=\"cancelDelete()\">")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    html.new_footer()

# function to generate grid view for hostgroup (ajax request).


def grid_view_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        i = 0
        html.live.set_prepend_site(True)
        query = "GET hostgroups\nColumns: hostgroup_name alias\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()

        tabledata = """
<table class='addform'>
<colgroup><col width='30%'/><col width='60%'/><col width='5%'/><col width='5%'/></colgroup>
<tr><th>Host Group Name</th><th>Alias</th><th colspan="2"></th></tr>
"""
        for site, hostgroup, alias in hosts:
            i += 1

            if i % 2 == 0:
                tabledata += "<tr class='even'>"
            else:
                tabledata += "<tr>"

            tabledata += "<td>" + hostgroup + "</td><td><a class=\"newlink\" href=\"view.py?view_name=hostgroup&hostgroup=" + hostgroup + "\" target=\"main\">" + alias + \
                         "</a></td><td><img src='images/edit16.png' alt='edit' title='Edit Host Group' class='imgbutton' onclick='editHostGroup(\"" + hostgroup + "\")'/></td><td><img src='images/delete16.png' alt='delete' title='Delete Host Group' class='imgbutton' onclick='deleteHostGroup(\"" + hostgroup + "\")'/></td></tr>"

        tabledata += "</table><input type=\"hidden\" id=\"totalHostGroup\" name=\"totalHostGroup\" value=\"" + str(
            i) + "\" />"
    except Exception as e:
        html.write("0")  # Some error occur, please Refresh the page
    else:
        html.write(tabledata)

# function to create form for add and edit information of hostgroup.


def form_for_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    html.live.set_prepend_site(True)
    formdata = ""
    _hostGroupName = ""
    _alias = ""
    if html.var("action").strip() == "edit":
        query = "GET hostgroups\nColumns: hostgroup_name alias\nFilter: hostgroup_name = " + \
                html.var("hostGroupName").strip()

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()

        for site, hostgroup, alias in hosts:
            _hostGroupName = hostgroup
            _alias = alias
        formdata += "<form id=\"addHostGroupForm\" action=\"ajaxcall_update_hostgroup.py\"><table class='addform'><colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"/></colgroup><tr><th colspan='3'>Edit Host Group</th></tr><tr><td>Host Group Name</td><td><input type='text' name='hostGroupName' id='hostGroupName' value='" + _hostGroupName + "' class='required' readonly=\"readonly\" maxlength='50'/><input type='hidden' name='oldHostGroupName' id='oldHostGroupName' value='" + _hostGroupName + "' /></td><td class=\"desc\">The name of the Host Group.</td></tr><tr><td>Alias</td><td><input type='text' name='alias' id='alias' value='" + _alias + \
                    "' class='required' maxlength='100'/></td><td class=\"desc\">Alias is a keyword or descriptive term associated with an object as means of classification.</td></tr><tr><td class='button' colspan='3'><input type='submit' value='Update Host Group' /><input type='button' value='Cancel' onclick=\"cancelEditHostGroup()\"/></td></tr></table></form>"

    else:
        formdata += """
         <form id="addHostGroupForm" action="ajaxcall_add_hostgroup.py" method="post">
         <table class='addform'>
         <colgroup><col width='20%'/><col width='40%'/><col width='40%'/></colgroup>
         <tr><th colspan='3'>Add Host Group</th></tr>
         <tr><td>Host Group Name</td><td><input type='text' name='hostGroupName' id='hostGroupName' value='' class='required' maxlength='50' /></td>
         <td class="desc">The name of the Host Group.</td></tr>
         <tr><td>Alias</td><td><input type='text' name='alias' id='alias' value='' class='required' maxlength='100'/></td>
         <td class="desc">Alias is a keyword or descriptive term associated with an object as means of classification.</td></tr>
         <tr><td class='button' colspan='3'><input type='submit' value='submit'/>
         <input type='button' value='Reset' onclick="resetAddHostGroup()"/>
         <input type='button' value='Cancel' onclick="cancelAddHostGroup()"/></td></tr>
         </table>
         </form>
         """
    html.write(formdata)


# function to add new hostgroup (ajax request)
def ajax_add_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h

    if (html.var("hostGroupName").strip() == "" or html.var("alias").strip() == ""):
        html.write(
            "2")  # retuen 2 if hostgroup name and alias both are null or empty
    else:
        sitename = __file__.split("/")[3]
        countHostGroup = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        query = "GET hostgroups\nColumns: hostgroup_name alias\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()

        for site, hostgroup, alias in hosts:
            countHostGroup += 1
            if (hostgroup.strip() == html.var("hostGroupName").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 or countHostGroup == 0):
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename, "a")
            fw.write("\n#hostgroup-" + html.var("hostGroupName"))
            fw.write("\ndefine hostgroup {")
            fw.write("\n\thostgroup_name\t\t" + html.var("hostGroupName"))
            fw.write("\n\talias\t\t\t" + html.var("alias"))
            fw.write("\n}")
            fw.write("\n#endhostgroup-" + html.var("hostGroupName") + "\n")
            fw.close()
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
            html.write("1")  # return 1 if hostgroup added successfully.
        else:
            html.write("0")  # return 0 if hostgroup already exist.

# function to delete hostgroup (ajax request)


def ajax_delete_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    startCheckLine = "#hostgroup-" + html.var("hostGroupName").strip()
    endCheckLine = "#endhostgroup-" + html.var("hostGroupName").strip()
    checkfile = 0
    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename)):
        fr = open(
            "/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename, "r")
        ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
        for line in fr:
            if (line.strip() != startCheckLine.strip() and checkfile == 0):
                ftw.write(line)
            else:
                checkfile = 1
            if (line.strip() == endCheckLine.strip() and checkfile == 1):
                checkfile = 0
        fr.close()
        ftw.close()
        ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
        fw = open(
            "/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename, "w")
        for line in ftr:
            fw.write(line)
        ftr.close()
        fw.close()
        if html.var("command").strip() == "delete host":
            countHost = 0
            html.live.set_prepend_site(True)
            query = "GET hosts\nColumns: host_name\nFilter: host_groups < " + \
                    html.var("hostGroupName").strip()
            hosts = html.live.query(query)
            html.live.set_prepend_site(False)
            hosts.sort()
            for site, hostname in hosts:
                countHost += 1
            if countHost == 0:
                change_hostgroup_from_hosts(
                    html.var("hostGroupName").strip(), "")
            else:
                delete_hosts_of_hostgroup(html.var("hostGroupName").strip())
        else:
            change_hostgroup_from_hosts(html.var("hostGroupName").strip(), "")
        os.system(
            'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
        html.write("1")
    else:
        html.write("0")


def change_hostgroup_from_hosts(oldhostgroup, newhostgroup):
    """

    @param oldhostgroup:
    @param newhostgroup:
    """
    global html
    sitename = __file__.split("/")[3]

    if oldhostgroup != newhostgroup:
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: host_name\nFilter: host_groups >= " + \
                oldhostgroup
        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename)):
            for site, hostname in hosts:
                checkfile = 0
                startCheckLine = "#host-" + hostname
                endCheckLine = "#endhost-" + hostname
                fr = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "r")
                ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                for line in fr:
                    if (line.strip() != startCheckLine.strip() and checkfile == 0):
                        ftw.write(line)
                    else:
                        checkfile = 1
                    if (line.strip() == endCheckLine.strip() and checkfile == 1):
                        checkfile = 0
                fr.close()
                ftw.close()
                ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "w")
                for line in ftr:
                    fw.write(line)
                ftr.close()
                fw.close()
        for site, hostname in hosts:
            html.live.set_prepend_site(True)
            query2 = "GET hosts\nColumns: alias address host_groups parents\nFilter: host_name = " + \
                     hostname
            host = html.live.query(query2)
            html.live.set_prepend_site(False)
            host.sort()
            _alias = ""
            _address = ""
            _hostgroups = []
            _parents = []
            _hostgroupsString = ""
            _parentsString = ""
            for sites, alias, address, hostgroups, parents in host:
                _alias = alias
                _address = address
                _hostgroups = hostgroups
                _parents = parents
            _hostgroups.remove(oldhostgroup.strip())
            if newhostgroup.strip() != "":
                _hostgroups.append(newhostgroup.strip())
            _hostgroupsString = ", ".join(_hostgroups)
            _parentsString = ", ".join(_parents)
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "a")
            fw.write("\n#host-" + hostname)
            fw.write("\ndefine host {")
            fw.write("\n\tuse\t\t\tgeneric-host")
            fw.write("\n\thost_name\t\t" + hostname)
            fw.write("\n\talias\t\t\t" + _alias)
            fw.write("\n\taddress\t\t" + _address)
            if (_hostgroupsString.strip() != ""):
                fw.write("\n\thostgroups\t\t" + _hostgroupsString.strip())
            if (_parentsString.strip() != ""):
                fw.write("\n\tparents\t\t" + _parentsString.strip())
            fw.write("\n}")
            fw.write("\n#endhost-" + hostname)
            fw.close()


def delete_hosts_of_hostgroup(hostgroup):
    """

    @param hostgroup:
    """
    global html
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: host_name\nFilter: host_groups >= " + \
            hostgroup
    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    sitename = __file__.split("/")[3]

    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename)):
        for site, hostname in hosts:
            checkfile = 0
            startCheckLine = "#host-" + hostname
            endCheckLine = "#endhost-" + hostname
            fr = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "r")
            ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
            for line in fr:
                if (line.strip() != startCheckLine.strip() and checkfile == 0):
                    ftw.write(line)
                else:
                    checkfile = 1
                if (line.strip() == endCheckLine.strip() and checkfile == 1):
                    checkfile = 0
            fr.close()
            ftw.close()
            ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "w")
            for line in ftr:
                fw.write(line)
            ftr.close()
            fw.close()
            delete_services_of_host(hostname)
            delete_host_from_database(hostname)

######################################

# function to update hostgroup (ajax request)


def ajax_update_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h

    if (html.var("hostGroupName").strip() == "" or html.var("alias").strip() == ""):
        html.write(
            "2")  # retuen 2 if hostgroup name and alias both are null or empty
    else:
        countHostGroup = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        query = "GET hostgroups\nColumns: hostgroup_name alias\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()

        for site, hostgroup, alias in hosts:
            countHostGroup += 1
            if (hostgroup.strip() == html.var("hostGroupName").strip() and hostgroup.strip() != html.var(
                    "oldHostGroupName").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 and countHostGroup > 0):

            # delete host group
            sitename = __file__.split("/")[3]
            startCheckLine = "#hostgroup-" + html.var(
                "oldHostGroupName").strip()
            endCheckLine = "#endhostgroup-" + html.var(
                "oldHostGroupName").strip()
            checkfile = 0

            if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename)):
                fr = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename, "r")
                ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                for line in fr:
                    if (line.strip() != startCheckLine.strip() and checkfile == 0):
                        ftw.write(line)
                    else:
                        checkfile = 1
                    if (line.strip() == endCheckLine.strip() and checkfile == 1):
                        checkfile = 0
                fr.close()
                ftw.close()
                ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename, "w")
                for line in ftr:
                    fw.write(line)
                ftr.close()
                fw.close()

            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hostgroups.cfg" % sitename, "a")
            fw.write("\n#hostgroup-" + html.var("hostGroupName"))
            fw.write("\ndefine hostgroup {")
            fw.write("\n\thostgroup_name\t\t" + html.var("hostGroupName"))
            fw.write("\n\talias\t\t\t" + html.var("alias"))
            fw.write("\n}")
            fw.write("\n#endhostgroup-" + html.var("hostGroupName") + "\n")
            fw.close()
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
            html.write("1")  # return 1 if hostgroup added successfully.
        else:
            html.write("0")  # return 0 if hostgroup already exist.

###################################################################### END

###################################################################### SERVICE GROUP ########################################################################
# function to add edit delete service group details manually.


def page_manage_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/servicegroup.js"]
    html.new_header("Manage Service Group", "", "", css_list, js_list)
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    html.write(
        "<div id=\"formDiv\"></div><table class='addform' id='addservicetable' style='margin-bottom:0px;cursor:pointer;'><colgroup><col width='1%'/><col width='99%'/></colgroup><tr><th><img src='images/add16.png' alt='add'/></th><th>Add Service Group</th></tr></table></div>")
    html.write("<div id=\"gridviewDiv\">")
    grid_view_servicegroup(h)
    html.write("</div>")
    html.footer()
    # message and options before delete service group
    html.write(
        "<div style=\"position:fixed;width:400px;left:21%; right:auto; bottom:35%; direction:ltr;z-index:200;display:none;\" id=\"DeleteServiceGroupMsg\" >")
    html.write(
        "<div class=\"main-title\" style=\"cursor: pointer;\"><span id=\"boxTitle\">Delete Service Group</span></div>")
    html.write("<div class=\"template-div\">")
    html.write(
        "<div class=\"sub-title\"><input type=\"radio\" id=\"command1\" name=\"command\" value=\"donot delete service\" checked=\"checked\"/><label style=\"vertical-align: bottom;margin-left:3px;\" for=\"command1\">Delete only Service group</label></div>")
    html.write(
        "<div class=\"sub-title\"><input type=\"radio\" id=\"command2\" name=\"command\" value=\"delete service\"/><label style=\"vertical-align: bottom;margin-left:3px;\" for=\"command2\">Delete Service group and Services both.</label></div>")
    html.write("<div class=\"row-odd\" style=\"margin: 10px;\">")
    html.write(
        "<input type=\"button\" value=\"Ok\" style=\"width:80px;\" onclick=\"okDelete()\">")
    html.write(
        "<input type=\"button\" value=\"Cancel\" style=\"width:80px;\" onclick=\"cancelDelete()\">")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    html.new_footer()

# function to generate grid view for servicegroup (ajax request).


def grid_view_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        i = 0
        html.live.set_prepend_site(True)
        query = "GET servicegroups\nColumns: servicegroup_name alias\n"

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        tabledata = """
<table class='addform'>
<colgroup><col width='30%'/><col width='60%'/><col width='5%'/><col width='5%'/></colgroup>
<tr><th>Service Group Name</th><th>Alias</th><th colspan="2"></th></tr>
"""
        for site, servicegroup, alias in services:
            i += 1

            if i % 2 == 0:
                tabledata += "<tr class='even'>"
            else:
                tabledata += "<tr>"

            tabledata += "<td>" + servicegroup + "</td><td><a class=\"newlink\" href=\"view.py?view_name=servicegroup&servicegroup=" + servicegroup + "\" target=\"main\">" + alias + \
                         "</a></td><td><img src='images/edit16.png'\ alt='edit' title='Edit Service Group' class='imgbutton' onclick='editServiceGroup(\"" + servicegroup + "\")'/></td><td><img src='images/delete16.png' alt='delete' title='Delete Service Group' class='imgbutton' onclick='deleteServiceGroup(\"" + \
                         servicegroup + \
                         "\")'/></td></tr>"

        tabledata += "</table><input type=\"hidden\" id=\"totalServiceGroup\" name=\"totalServiceGroup\" value=\"" + str(
            i) + "\" />"
    except Exception as e:
        html.write("0")  # Some error occur, please Refresh the page
    else:
        html.write(tabledata)

# function to create form for add and edit information of servicegroup.


def form_for_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    html.live.set_prepend_site(True)
    formdata = ""
    _serviceGroupName = ""
    _alias = ""
    if html.var("action").strip() == "edit":
        query = "GET servicegroups\nColumns: servicegroup_name alias\nFilter: servicegroup_name = " + \
                html.var("serviceGroupName").strip()

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        for site, servicegroup, alias in services:
            _serviceGroupName = servicegroup
            _alias = alias
        formdata += "<form id=\"addServiceGroupForm\" action=\"ajaxcall_update_servicegroup.py\"><table class='addform'><colgroup><col width='20%'/><col width='40%'/><col width='40%'/></colgroup><tr><th colspan='3'>Edit Service Group</th></tr><tr><td>Service Group Name</td><td><input type='text' name='serviceGroupName' id='serviceGroupName' value='" + _serviceGroupName + "' class='required' readonly = \"readonly\" maxlength='50'/><input type='hidden' name='oldServiceGroupName' id='oldServiceGroupName' value='" + _serviceGroupName + "' /></td><td class=\"desc\">The name of the Service Group.</td></tr><tr><td>Alias</td><td><input type='text' name='alias' id='alias' value='" + _alias + \
                    "' class='required' maxlength='100'/></td><td class=\"desc\">Alias is a keyword or descriptive term associated with an object as means of classification.</td></tr><tr><td class='button' colspan='3'><input type='submit' value='Update Service Group' /><input type='button' value='Cancel' onclick=\"cancelEditServiceGroup()\"/></td></tr></table></form>"

    else:
        formdata += """
         <form id="addServiceGroupForm" action="ajaxcall_add_servicegroup.py" method="post">
         <table class='addform'>
         <colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"/></colgroup>
         <tr><th colspan='3'>Add Service Group</th></tr>
         <tr><td>Service Group Name</td><td><input type='text' name='serviceGroupName' id='serviceGroupName' value='' class='required' maxlength='50' /></td>
         <td class="desc">The name of the Service Group.</td></tr>
         <tr><td>Alias</td><td><input type='text' name='alias' id='alias' value='' class='required' maxlength='100'/></td>
         <td class="desc">Alias is a keyword or descriptive term associated with an object as means of classification.</td></tr>
         <tr><td class='button' colspan='3'><input type='submit' value='submit'/>
         <input type='button' value='Reset' onclick="resetAddServiceGroup()"/>
         <input type='button' value='Cancel' onclick="cancelAddServiceGroup()"/></td></tr>
         </table>
         </form>
         """
    html.write(formdata)


# function to add new servicegroup (ajax request)
def ajax_add_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h

    if (html.var("serviceGroupName").strip() == "" or html.var("alias").strip() == ""):
        html.write(
            "2")  # retuen 2 if servicegroup name and alias both are null or empty
    else:
        sitename = __file__.split("/")[3]
        countServiceGroup = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        query = "GET servicegroups\nColumns: servicegroup_name alias\n"

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        for site, servicegroup, alias in services:
            countServiceGroup += 1
            if (servicegroup.strip() == html.var("serviceGroupName").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 or countServiceGroup == 0):
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename, "a")
            fw.write("\n#servicegroup-" + html.var("serviceGroupName"))
            fw.write("\ndefine servicegroup {")
            fw.write(
                "\n\tservicegroup_name\t\t" + html.var("serviceGroupName"))
            fw.write("\n\talias\t\t\t" + html.var("alias"))
            fw.write("\n}")
            fw.write(
                "\n#endservicegroup-" + html.var("serviceGroupName") + "\n")
            fw.close()
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
            html.write("1")  # return 1 if servicegroup added successfully.
        else:
            html.write("0")  # return 0 if servicegroup already exist.

# function to delete servicegroup (ajax request)


def ajax_delete_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    startCheckLine = "#servicegroup-" + html.var("serviceGroupName").strip()
    endCheckLine = "#endservicegroup-" + html.var("serviceGroupName").strip()
    checkfile = 0
    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename)):
        fr = open(
            "/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename, "r")
        ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
        for line in fr:
            if (line.strip() != startCheckLine.strip() and checkfile == 0):
                ftw.write(line)
            else:
                checkfile = 1
            if (line.strip() == endCheckLine.strip() and checkfile == 1):
                checkfile = 0
        fr.close()
        ftw.close()
        ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
        fw = open(
            "/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename, "w")
        for line in ftr:
            fw.write(line)
        ftr.close()
        fw.close()
        if html.var("command").strip() == "delete service":
            countService = 0
            html.live.set_prepend_site(True)
            query = "GET services\nColumns: host_name\nFilter: service_groups < " + \
                    html.var("serviceGroupName").strip()
            services = html.live.query(query)
            html.live.set_prepend_site(False)
            services.sort()
            for site, hostname in services:
                countService += 1
            if countService == 0:
                change_servicegroup_from_services(
                    html.var("serviceGroupName").strip(), "")
            else:
                delete_services_of_servicegroup(
                    html.var("serviceGroupName").strip())
        os.system(
            'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
        html.write("1")
    else:
        html.write("0")


def change_servicegroup_from_services(oldservicegroup, newservicegroup):
    """

    @param oldservicegroup:
    @param newservicegroup:
    """
    global html
    sitename = __file__.split("/")[3]

    if oldservicegroup != newservicegroup:
        html.live.set_prepend_site(True)
        query = "GET services\nColumns: check_command host_name\nFilter: service_groups >= " + \
                oldservicegroup
        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()
        if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename)):
            for site, command, hostname in services:
                startCheckLine = "#service-" + hostname + "-" + command
                endCheckLine = "#endservice-" + hostname + "-" + command
                checkfile = 0

                fr = open(
                    "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "r")
                ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                for line in fr:
                    if (line.strip() != startCheckLine.strip() and checkfile == 0):
                        ftw.write(line)
                    else:
                        checkfile = 1
                    if (line.strip() == endCheckLine.strip() and checkfile == 1):
                        checkfile = 0
                fr.close()
                ftw.close()
                ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "w")
                for line in ftr:
                    fw.write(line)
                ftr.close()
                fw.close()
            for site, command, hostname in services:
                html.live.set_prepend_site(True)
                query2 = "GET services\nColumns: description service_groups  max_check_attempts notification_interval check_interval retry_interval action_url\nFilter: host_name = " + hostname + \
                         "\nFilter: check_command = " + command
                service = html.live.query(query2)
                html.live.set_prepend_site(False)
                service.sort()
                _description = ""
                _servicegroup = []
                _servicegroupString = ""
                _maxCheckAttempts = 5
                _notificationInverval = 30
                _checkInverval = 5
                _retryInterval = 3
                _useTemplate = "generic-service"
                for sites, description, servicegroup, maxCheckAttempts, notificationInverval, checkInverval, retryInterval, actionUrl in service:
                    _description = description
                    _servicegroup = servicegroup
                    _maxCheckAttempts = maxCheckAttempts
                    _notificationInverval = notificationInverval
                    _checkInverval = checkInverval
                    _retryInterval = retryInterval
                    if str(actionUrl).strip() != "":
                        _useTemplate = "generic-service-perf,generic-service"
                _servicegroup.remove(oldservicegroup.strip())
                if newservicegroup.strip() != "":
                    _servicegroup.append(newservicegroup.strip())
                _servicegroupString = ", ".join(_servicegroup)

                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "a")
                fw.write(
                    "#service-" + hostname.strip() + "-" + command.strip())
                fw.write("\ndefine service {")
                fw.write("\n\tuse\t\t\t" + _useTemplate)
                fw.write("\n\thost_name\t\t" + hostname.strip())
                fw.write("\n\tservice_description\t\t\t" + _description)
                if (str(_maxCheckAttempts) != ""):
                    fw.write(
                        "\n\tmax_check_attempts\t\t" + str(_maxCheckAttempts))
                if (str(_checkInverval) != ""):
                    fw.write(
                        "\n\tnormal_check_interval\t\t" + str(_checkInverval))
                if (str(_retryInterval) != ""):
                    fw.write(
                        "\n\tretry_check_interval\t\t" + str(_retryInterval))
                if (str(_notificationInverval) != ""):
                    fw.write("\n\tnotification_interval\t\t" +
                             str(_notificationInverval))

                if (_servicegroupString.strip() != ""):
                    fw.write(
                        "\n\tservicegroups\t\t" + _servicegroupString.strip())

                if (command.strip() != ""):
                    fw.write("\n\tcheck_command\t\t" + command.strip())
                fw.write("\n}")
                fw.write("\n#endservice-" + hostname.strip(
                ) + "-" + command.strip() + "\n")
                fw.close()

# query_service = "GET services\nColumns: description state check_command
# action_url\nFilter: host_name = " + host


def delete_services_of_servicegroup(servicegroup):
    """

    @param servicegroup:
    """
    global html
    html.live.set_prepend_site(True)
    query = "GET services\nColumns: check_command host_name\nFilter: service_groups >= " + \
            servicegroup
    services = html.live.query(query)
    html.live.set_prepend_site(False)
    services.sort()
    sitename = __file__.split("/")[3]

    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename)):
        for site, command, hostname in services:
            startCheckLine = "#service-" + hostname + "-" + command
            endCheckLine = "#endservice-" + hostname + "-" + command
            checkfile = 0

            fr = open(
                "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "r")
            ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
            for line in fr:
                if (line.strip() != startCheckLine.strip() and checkfile == 0):
                    ftw.write(line)
                else:
                    checkfile = 1
                if (line.strip() == endCheckLine.strip() and checkfile == 1):
                    checkfile = 0
            fr.close()
            ftw.close()
            ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "w")
            for line in ftr:
                fw.write(line)
            ftr.close()
            fw.close()

# function to update servicegroup (ajax request)


def ajax_update_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h

    if (html.var("serviceGroupName").strip() == "" or html.var("alias").strip() == ""):
        html.write(
            "2")  # retuen 2 if servicegroup name and alias both are null or empty
    else:
        countServiceGroup = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        query = "GET servicegroups\nColumns: servicegroup_name alias\n"

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        for site, servicegroup, alias in services:
            countServiceGroup += 1
            if (servicegroup.strip() == html.var("serviceGroupName").strip() and servicegroup.strip() != html.var(
                    "oldServiceGroupName").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 and countServiceGroup > 0):

            # delete service group
            sitename = __file__.split("/")[3]
            startCheckLine = "#servicegroup-" + html.var(
                "oldServiceGroupName").strip()
            endCheckLine = "#endservicegroup-" + html.var(
                "oldServiceGroupName").strip()
            checkfile = 0

            if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename)):
                fr = open(
                    "/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename, "r")
                ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                for line in fr:
                    if (line.strip() != startCheckLine.strip() and checkfile == 0):
                        ftw.write(line)
                    else:
                        checkfile = 1
                    if (line.strip() == endCheckLine.strip() and checkfile == 1):
                        checkfile = 0
                fr.close()
                ftw.close()
                ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename, "w")
                for line in ftr:
                    fw.write(line)
                ftr.close()
                fw.close()

            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/servicegroups.cfg" % sitename, "a")
            fw.write("\n#servicegroup-" + html.var("serviceGroupName"))
            fw.write("\ndefine servicegroup {")
            fw.write(
                "\n\tservicegroup_name\t\t" + html.var("serviceGroupName"))
            fw.write("\n\talias\t\t\t" + html.var("alias"))
            fw.write("\n}")
            fw.write(
                "\n#endservicegroup-" + html.var("serviceGroupName") + "\n")
            fw.close()
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
            html.write("1")  # return 1 if servicegroup added successfully.
        else:
            html.write("0")  # return 0 if servicegroup already exist.


#################################################################### END S

###################################################################### HOST #######################################################################
# function to add edit delete host details manually.
def page_manage_host(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/host.js"]
    html.new_header("Manage Host", "", "", css_list, js_list)
    html.write(
        "<div id=\"formDiv\"></div><table class='addform' id='addhosttable' style='margin-bottom:0px;cursor:pointer;'><colgroup><col width='1%'/><col width='99%'/></colgroup><tr><th><img src='images/add16.png' alt='add'/></th><th>Add Host</th></tr></table></div>")
    html.write("<div id=\"gridviewDiv\">")
    grid_view_host(h)
    html.write("</div>")
    html.footer()
    # message and options before delete host group
    html.write(
        "<div style=\"position:fixed;width:400px;left:21%; right:auto; bottom:35%; direction:ltr;z-index:200;display:none;\" id=\"DeleteHostMsg\" >")
    html.write("<div class=\"main-title\" style=\"cursor: pointer;\"><span id=\"boxTitle\">Delete Host</span></div>")
    html.write("<div class=\"template-div\">")
    html.write(
        "<div class=\"sub-title\"><input type=\"radio\" id=\"command1\" name=\"command\" value=\"donot delete child\" checked=\"checked\"/><label style=\"vertical-align: bottom;margin-left:3px;\" for=\"command1\">Delete only Host</label></div>")
    html.write(
        "<div class=\"sub-title\"><input type=\"radio\" id=\"command2\" name=\"command\" value=\"delete child\"/><label style=\"vertical-align: bottom;margin-left:3px;\" for=\"command2\">Delete Host and child Hosts both.</label></div>")
    html.write("<div class=\"row-odd\" style=\"margin: 10px;\">")
    html.write(
        "<input type=\"button\" value=\"Ok\" style=\"width:80px;\" onclick=\"okDelete()\">")
    html.write(
        "<input type=\"button\" value=\"Cancel\" style=\"width:80px;\" onclick=\"cancelDelete()\">")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    html.new_footer()

# function to generate grid view for host (ajax request).


def grid_view_host(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    try:
        i = 0
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name alias address host_groups parents\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        tabledata = """
<table class='addform'>
<colgroup><col width='15%'/><col width='20%'/><col width='15%'/><col width='15%'/><col width='15%'/><col width='5%'/><col width='5%'/></colgroup>
<tr><th>Host Name</th><th>Alias</th><th>IP Address</th><th>Host Group</th><th>Parent</th><th colspan="2"></th></tr>
"""
        all_i = 0
        for site, host, alias, address, host_groups, parents in hosts:
            i += 1
            port = username = password = ""
            address2 = address

            # Open database connection
            db = MySQLdb.connect("localhost", "root", "root", "nms")

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            sql = "SELECT username,password,port from nms_devices\
                     WHERE hostname = '%s' AND created_by = '%s'" % (host, config.user)
            cursor.execute(sql)
            result = cursor.fetchall()
            sql_i = 0
            for row in result:
                all_i += 1
                sql_i += 1
                username = row[0]
                password = row[1]
                port = row[2]

            if (username.strip() != "" and password != ""):
                address2 = username + ":" + password + "@" + address2
            if (port.strip() != ""):
                address2 = address2 + ":" + port

            if sql_i > 0:
                if all_i % 2 == 0:
                    tabledata += "<tr class='even'>"
                else:
                    tabledata += "<tr>"

                tabledata += "<td>" + host + "</td><td><a class=\"newlink\" href=\"view.py?view_name=host&host=" + host + "\" target=\"main\">" + alias + "</a></td><td><a class=\"newlink\" href=\"http://" + address2 + "\" target=\"main\">" + address + "</td><td>" + (
                ", ".join(host_groups)) + "</td><td>" + (", ".join(
                    parents)) + "</td><td><img src='images/edit16.png' alt='edit' title='Edit Host' class='imgbutton' onclick='editHost(\"" + host + "\")'/></td><td><img src='images/delete16.png' alt='delete' title='Delete Host' class='imgbutton' onclick='deleteHost(\"" + host + "\",\"" + address + "\")'/></td></tr>"
        if all_i == 0:
            tabledata += "<tr><td colspan=\"7\"> No Host Exist </td></tr>"
        tabledata += "</table><input type=\"hidden\" id=\"totalHost\" name=\"totalHost\" value=\"" + \
                     str(i) + "\" />"
    except Exception as e:
        html.write(e)  # Some error occur, please Refresh the page
    else:
        html.write(tabledata)

# function to create form for add and edit information of host.


def form_for_host(h):
    """

    @param h:
    """
    global html
    html = h

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    html.live.set_prepend_site(True)
    formdata = ""
    host = ""
    alias = ""
    port = ""
    username = ""
    password = ""
    hostgroup = []
    parent = []
    address = ""
    deviceType = ""
    if html.var("action").strip() == "edit":
        query = "GET hosts\nColumns: name alias address host_groups parents\nFilter: name = " + \
                html.var("hostName").strip()

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        sitename = __file__.split("/")[3]

        for site, host, alias, address, hostgroup, parent in hosts:
            # Prepare SQL query to INSERT a record into the database.
            sql = "SELECT * FROM nms_devices \
                    WHERE hostname = '%s'" % (host)
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            result = cursor.fetchall()

            for col in result:
                deviceType = col[1]
                username = col[3]
                password = col[4]
                port = col[5]
            formdata += "<form id=\"addHostForm\" action=\"ajaxcall_update_host.py\"><table class='addform'><colgroup><col width='20%'/><col width='40%'/><col width='40%'/></colgroup><tr><th colspan='3'>Edit Host</th></tr><tr><td>Host Name</td><td><input readonly=\"readonly\" type='text' name='hostName' id='hostName' value='" + host + "' class='required' maxlength='50'/><input type='hidden' name='oldHostName' id='oldHostName' value='" + host + "' /></td><td class=\"desc\">The name of the host.</td></tr><tr><td>Alias</td><td><input type='text' name='alias' id='alias' value='" + alias + "' class='required' maxlength='100'/></td><td class=\"desc\">Alias is a keyword or descriptive term associated with an object as means of classification.</td></tr><tr><td>IP Address</td><td><input type='text' name='ipAddress' id='ipAddress' value='" + address + "' class='required'/></td><td class=\"desc\">Enter IP address. (e.g. 192.168.1.1)</td></tr><tr><td>Configuration Port</td><td><input type='text' name='confPort' id='confPort' value='" + port + "' /></td></td><td class=\"desc\">Enter host configuration port number.(if require)</td></tr><tr><td>User Name</td><td><input type='text' name='confUsername' id='confUsername' value='" + username + "' /></td><td class=\"desc\">Enter host configuration username</td></tr><tr><td>Password</td><td><input type='password' name='confPassword' id='confPassword' value='" + password + "' /></td><td class=\"desc\">Enter host configuration password</td></tr><tr><td>Choose Device Type</td><td><select name='deviceType' id='deviceType'> <option value=\"\">-- Select Device Type --</option><option value=\"Unknown\">Unknown Device</option><option value=\"ODU16\">ODU-16Mbps</option><option value=\"ODU100\">ODU-100Mbps</option><option value=\"IDU4\">IDU-4 Port</option><option value=\"IDU8\">IDU-8 Port</option><option value=\"SWT24\">Switch-24 Port</option><option value=\"SWT8\">Switch-8 Port</option><option value=\"SWT4\">Switch-4 Port</option><option value=\"AP\">Access Point</option><option value=\"HG\">Home Gateway</option><option value=\"HG22\">Home Gateway 22dBm</option><option value=\"AP22\">Access Point 22</option><option value=\"CPE\">CPE</option><option value=\"CPE22\">CPE22</option><option value=\"EG\">Enterprise Gateway</option></select></td><td class=\"desc\">Choose type of the device.</td></tr><tr><td style=\"vertical-align: top;\">Host Groups</td><td>" + hostgroup_multiple_select_list(
                (",".join(hostgroup)),
                "HostGroup") + "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose Host Group(s) to add this host to.</td></tr><tr><td style=\"vertical-align: top;\">Parents</td><td>" + _parent_multiple_select_list(
                (",".join(parent)),
                "HostParent") + "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose parent hosts for this host.</td></tr><tr><td class='button' colspan='3'><input type='submit' value='Update Host' /><input type='button' value='Cancel' onclick=\"cancelEditHost()\"/></td></tr></table><input type=\"hidden\" id=\"hdDeviceType\" name=\"hdDeviceType\" value=\"" + deviceType + "\"/><input type=\"hidden\" id=\"hdIpAddress\" name=\"hdIpAddress\" value=\"" + \
                        address + \
                        "\"/></form>"

    else:
        formdata += "<form id=\"addHostForm\" action=\"ajaxcall_add_host.py\" method=\"post\"><table class='addform'><colgroup><col width='20%'/><col width='40%'/><col width='40%'/></colgroup><tr><th colspan='3'>Add Host</th></tr><tr><td>Host Name</td><td><input type='text' name='hostName' id='hostName' value='' class='required' maxlength='50' /></td><td class=\"desc\">The name of the host.</td></tr><tr><td>Alias</td><td><input type='text' name='alias' id='alias' value='' class='required' maxlength='100' /></td><td class=\"desc\">Alias is a keyword or descriptive term associated with an object as means of classification.</td></tr><tr><td>IP Address</td><td><input type='text' name='ipAddress' id='ipAddress' value='' class='required' /></td><td class=\"desc\">Enter IP address. (e.g. 192.168.1.1)</td></tr><tr><td>Configuration Port</td><td><input type='text' name='confPort' id='confPort' value='' /></td><td class=\"desc\">Enter host configuration port number.(if require)</td></tr><tr><td>User Name</td><td><input type='text' name='confUsername' id='confUsername' value='' /></td><td class=\"desc\">Enter host configuration username.</td></tr><tr><td>Password</td><td><input type='password' name='confPassword' id='confPassword' value='' /></td><td class=\"desc\">Enter host configuration password.</td></tr><tr><td>Choose Device Type</td><td><select name='deviceType' id='deviceType'> <option value=\"\">-- Select Device Type --</option><option value=\"Unknown\">Unknown Device</option><option value=\"ODU16\">ODU-16Mbps</option><option value=\"ODU100\">ODU-100Mbps</option><option value=\"IDU4\">IDU-4 Port</option><option value=\"IDU8\">IDU-8 Port</option><option value=\"SWT24\">Switch-24 Port</option><option value=\"SWT8\">Switch-8 Port</option><option value=\"SWT4\">Switch-4 Port</option><option value=\"AP\">Access Point</option><option value=\"HG\">Home Gateway</option><option value=\"HG22\">Home Gateway 22dBm</option><option value=\"AP22\">Access Point 22</option><option value=\"CPE\">CPE</option><option value=\"CPE22\">CPE22</option><option value=\"EG\">Enterprise Gateway</option></select></td><td class=\"desc\">Choose type of the device.</td></tr><tr><td style=\"vertical-align:top;\">Service Management</td><td>" + service_management_option() + "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose \"Services add manually\" if you want to create and manage services manually. Other setting will create services using template.</td></tr><tr><td style=\"vertical-align:top;\">Host Groups</td><td>" + hostgroup_multiple_select_list(
            "",
            "HostGroup") + "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose Host Group(s) to add new host to.</td></tr><tr><td style=\"vertical-align:top;\">Parents</td><td id=\"parentList\">" + _parent_multiple_select_list(
            "", "HostParent") + \
                    "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose parent hosts for this host.</td></tr><tr><td class='button' colspan='3'><input type='submit' value='submit'/><input type='button' value='Reset' onclick=\"resetAddHost()\"/><input type='button' value='Cancel' onclick=\"cancelAddHost()\"/></td></tr></table></form>"

    html.write(formdata)


def service_management_option():
    """


    @return:
    """
    data = "<table class='addform' style='margin-bottom:0px;margin-left:0px;cursor:pointer;width:430px;border:1px solid #6E6C6C;'><colgroup><col width='1%'/><col width='99%'/></colgroup><tr><th><input type=\"radio\" id=\"serviceManagementManual\" name=\"serviceManagement\" value=\"manual\" checked=\"checked\" /></th><th><label for=\"serviceManagementManual\" style='cursor:pointer;'>Services add manually</label></th></tr><tr><th><input type=\"radio\" id=\"serviceManagementUsingTemplate\" name=\"serviceManagement\" value=\"template\" /></th><th><label style='cursor:pointer;' for=\"serviceManagementUsingTemplate\">Services add using template</label></th></tr><tr class=\"trServiceManagement\" style=\"display:none;\"><td colspan=\"2\" style=\"padding:0px;\">" + service_template_form() + "</td></tr></table>"
    return data


def service_template_form():
    """


    @return:
    """
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parseString("<hosts></hosts>")
    if (os.path.isfile("/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % site)):
        dom = xml.dom.minidom.parse(
            "/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % site)
    liList = templateform = ""
    for host in dom.getElementsByTagName("host"):
        hostName = host.getAttribute("name")
        hostId = host.getAttribute("id")
        srvList = ""
        srvCount = 0
        for srv in host.getElementsByTagName("service"):
            argCount = 0
            argList = "<div class=\"serviceArgDiv\">"
            srvCount += 1
            for arg in srv.getElementsByTagName("ARG"):
                argCount += 1
                argList += "<div class=\"argInnerDiv\" style=\"width:70px;\">" + arg.getAttribute(
                    "name") + "</div><div class=\"argInnerDiv\" style=\"padding: 5px 3px 1px 3px;width:110px;\"><input type=\"text\" id=\"arg" + hostId + srv.getAttribute(
                    "id") + str(argCount) + "\" name=\"arg" + hostId + srv.getAttribute(
                    "id") + str(
                    argCount) + "\" value=\"\" /></div><div class=\"argInnerDiv\" style=\"color:#CD5728;width:130px;\">" + getText(
                    arg.childNodes).strip() + "</div>"
            argList += "</div>"

            srvList += "<div style=\"width:10%;float:left;overflow:hidden;height:20px;padding-left:30px;\"><input type=\"checkbox\" id=\"srv" + hostId + str(
                srvCount) + "\" name=\"srv" + hostId + str(srvCount) + "\" value=\"" + srv.getAttribute(
                "id") + "\" checked=\"checked\" /><input type=\"hidden\" id=\"totalArgument" + srv.getAttribute(
                "id") + "\" name=\"totalArgument" + srv.getAttribute("id") + "\" value=\"" + str(
                argCount) + "\" /></div><div style=\"width:80%;float:left;overflow:hidden;height:20px;padding-top:4px;\"><label style='cursor:pointer;' for=\"srv" + hostId + str(
                srvCount) + "\">" + srv.getAttribute("name") + "</label></div>"
            if argCount != 0:
                srvList += argList

        liList += "<li class=\"liHost\" style=\"cursor:pointer;\"><div style=\"width:10%;float:left;overflow:hidden;height:20px;\"><input type=\"radio\" name=\"rdServiceTemplate\" id=\"template" + hostId + "\" value=\"" + hostId + "\" /></div><div style=\"width:85%;float:left;overflow:hidden;height:20px;\"><label style=\"font-weight:bold;cursor:pointer;\" for=\"template" + hostId + "\">" + hostName + "</label><input type=\"hidden\" id=\"totalService" + hostId + "\" name=\"totalService" + \
                  hostId + "\" value=\"" + str(
            srvCount) + "\" /></div></li><div class=\"hostTemplateDiv\" style=\"width:100%;height:auto;display:none;background-color:#FFA35D;overflow:auto;\" id=\"template" + hostId + "Div\">" + \
                  srvList + "</div>"

    templateform += "<div class=\"multiSelectList\" style=\"width:100%;border:0px;\" id=\"multiSelectListForChooseHostTemplate\">"
    templateform += "<div class=\"selected\" style=\"width:100%\">"
    templateform += "<div class=\"shead\"><span>Choose Service Template</span>"
    templateform += "</div>"
    templateform += "<ul>" + liList
    templateform += "</ul>"
    templateform += "</div>"
    templateform += "</div>"
    return templateform

# function to add new host (ajax request)


def ajax_add_host(h):
    """

    @param h:
    """
    global html
    html = h

    if (html.var("hostName").strip() == "" or html.var("alias").strip() == "" or html.var("ipAddress").strip() == ""):
        html.write(
            "2")  # retuen 2 if host name and alias both are null or empty
    else:
        sitename = __file__.split("/")[3]
        countHost = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name alias\nFilter: name = " + \
                html.var("hostName").strip()

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()

        for site, host, alias in hosts:
            countHost += 1
            if (host.strip() == html.var("hostName").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 or countHost == 0):
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "a")
            fw.write("\n#host-" + html.var("hostName"))
            fw.write("\ndefine host {")
            fw.write("\n\tuse\t\t\tgeneric-host")
            fw.write("\n\thost_name\t\t" + html.var("hostName"))
            fw.write("\n\talias\t\t\t" + html.var("alias"))
            fw.write("\n\taddress\t\t" + html.var("ipAddress"))
            if (html.var("hdHostGroup").strip() != ""):
                fw.write("\n\thostgroups\t\t" + html.var("hdHostGroup"))
            if (html.var("hdHostParent").strip() != ""):
                fw.write("\n\tparents\t\t" + html.var("hdHostParent"))
            fw.write("\n}")
            fw.write("\n#endhost-" + html.var("hostName") + "\n")
            fw.close()

            serviceConfig = ""

            # Add Service Using Selected Template
            if (html.var("serviceManagement") == "template"):
                if html.var("rdServiceTemplate") is not None:
                    templateDom = xml.dom.minidom.parseString(
                        "<hosts></hosts>")
                    if (os.path.isfile("/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % sitename)):
                        templateDom = xml.dom.minidom.parse(
                            "/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % sitename)
                    hostTemplateId = html.var("rdServiceTemplate").strip()
                    totalServices = html.var("totalService" + hostTemplateId)

                    for hostTemplate in templateDom.getElementsByTagName("host"):
                        if hostTemplate.getAttribute("id").strip() == hostTemplateId:
                            for x in range(1, int(totalServices) + 1):
                                if html.var("srv" + hostTemplateId + str(x)) is not None:
                                    serviceTemplateId = html.var(
                                        "srv" + hostTemplateId + str(x)).strip()
                                    for serviceTemplate in hostTemplate.getElementsByTagName("service"):
                                        if serviceTemplate.getAttribute("id").strip() == serviceTemplateId:
                                            new_check_command = getText(serviceTemplate.getElementsByTagName(
                                                "check_command")[0].childNodes).strip().replace("$IPADDRESS$", html.var(
                                                "ipAddress").strip())
                                            serviceConfig += "#service-" + html.var(
                                                "hostName").strip() + "-" + new_check_command + "\n"
                                            serviceConfig += "define service {\n"
                                            serviceConfig += "\tuse\t\t\t" + \
                                                             getText(serviceTemplate.getElementsByTagName(
                                                                 "use")[0].childNodes).strip() + "\n"
                                            serviceConfig += "\thost_name\t\t" + \
                                                             html.var(
                                                                 "hostName").strip() + "\n"
                                            serviceConfig += "\tservice_description\t" + getText(
                                                serviceTemplate.getElementsByTagName("service_description")[
                                                    0].childNodes).strip() + "\n"
                                            serviceConfig += "\tmax_check_attempts\t\t\t" + getText(
                                                serviceTemplate.getElementsByTagName("max_check_attempts")[
                                                    0].childNodes).strip() + "\n"
                                            serviceConfig += "\tnormal_check_interval\t\t\t" + getText(
                                                serviceTemplate.getElementsByTagName("normal_check_interval")[
                                                    0].childNodes).strip() + "\n"
                                            serviceConfig += "\tretry_check_interval\t\t\t" + getText(
                                                serviceTemplate.getElementsByTagName("retry_check_interval")[
                                                    0].childNodes).strip() + "\n"
                                            serviceConfig += "\tnotification_interval\t\t\t" + getText(
                                                serviceTemplate.getElementsByTagName("notification_interval")[
                                                    0].childNodes).strip() + "\n"
                                            serviceConfig += "\tcheck_command\t\t\t" + \
                                                             new_check_command + "\n"
                                            serviceConfig += "}\n"
                                            serviceConfig += "#endservice-" + html.var(
                                                "hostName").strip() + "-" + new_check_command + "\n"
                    fsw = open(
                        "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "a")
                    fsw.write(serviceConfig)
                    fsw.close()

            # End Add Service Using Selected Template
            if html.var("deviceType") == "AP":
                create_service_for_graph(
                    html.var("hostName").strip(), "check_ap_bandwidth")
                create_service_for_graph(
                    html.var("hostName").strip(), "check_ap_no_of_user")
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)

            # add the hostIPAddress,username,password,port and type of device in to mysql database
            # Open database connection
            db = MySQLdb.connect("localhost", "root", "root", "nms")
            totalRow = 0
            try:
                # prepare a cursor object using cursor() method
                cursor = db.cursor()
                sql = "SELECT COUNT(*) FROM nms_devices\
                          WHERE hostname = '%s'" % (html.var("hostName"))
                cursor.execute(sql)
                result = cursor.fetchall()
                for col in result:
                    totalRow = col[0]
                if totalRow == 0:
                    sql = "INSERT INTO nms_devices (devicetype,ipaddress,username,password,port,hostname,created_by) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                        html.var("deviceType"), html.var("ipAddress"), html.var("confUsername"),
                        html.var("confPassword"), html.var("confPort"), html.var("hostName"), config.user)
                    cursor.execute(sql)
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
                # disconnect from server
            db.close()

            html.write("1")  # return 1 if host added successfully.
        else:
            html.write("0")  # return 0 if host already exist.

# function to delete host (ajax request)


def ajax_delete_host(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    startCheckLine = "#host-" + html.var("hostName").strip()
    endCheckLine = "#endhost-" + html.var("hostName").strip()
    checkfile = 0
    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename)):
        fr = open("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "r")
        ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
        for line in fr:
            if (line.strip() != startCheckLine.strip() and checkfile == 0):
                ftw.write(line)
            else:
                checkfile = 1
            if (line.strip() == endCheckLine.strip() and checkfile == 1):
                checkfile = 0
        fr.close()
        ftw.close()
        ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
        fw = open("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "w")
        for line in ftr:
            fw.write(line)
        ftr.close()
        fw.close()
        delete_services_of_host(html.var("hostName").strip())
        if html.var("command").strip() == "delete child":
            delete_childhosts_of_host(html.var("hostName").strip())
        else:
            change_host_from_childhosts(html.var("hostName").strip(), "")

        os.system(
            'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
        delete_host_from_database(html.var("hostName"))
        html.write("1")
    else:
        html.write("0")


def delete_host_from_database(hostName):
    # delete host in to mysql database
    # Open database connection
    """

    @param hostName:
    """
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    try:
        cursor = db.cursor()
        apId = 0
        sql = "SELECT id FROM nms_devices \
                     WHERE hostname = '%s'" % (hostName)
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            apId = row[0]

        # prepare a cursor object using cursor() method
        sql = "DELETE FROM nms_devices \
                     WHERE id = %s" % (apId)
        cursor.execute(sql)

        # prepare a cursor object using cursor() method
        sql = "DELETE FROM ap_schedule \
                     WHERE deviceid = %s" % (apId)
        cursor.execute(sql)

        # prepare a cursor object using cursor() method
        sql = "DELETE FROM repeat_ap_schedule \
                     WHERE deviceid = %s" % (apId)
        cursor.execute(sql)

        # prepare a cursor object using cursor() method
        sql = "DELETE FROM nms_devices_connected_user \
                     WHERE deviceid = %s" % (apId)
        cursor.execute(sql)

        # prepare a cursor object using cursor() method
        sql = "DELETE FROM nms_devices_bandwidth \
                     WHERE deviceid = %s" % (apId)
        cursor.execute(sql)

        # prepare a cursor object using cursor() method
        sql = "DELETE FROM nms_devices_uptime \
                     WHERE deviceid = %s" % (apId)
        cursor.execute(sql)

        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        # disconnect from server
    db.close()


def change_host_from_childhosts(oldhost, newhost):
    """

    @param oldhost:
    @param newhost:
    """
    global html
    sitename = __file__.split("/")[3]

    if oldhost != newhost:
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: host_name\nFilter: parents >= " + oldhost
        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename)):
            for site, hostname in hosts:
                checkfile = 0
                startCheckLine = "#host-" + hostname
                endCheckLine = "#endhost-" + hostname
                fr = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "r")
                ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                for line in fr:
                    if (line.strip() != startCheckLine.strip() and checkfile == 0):
                        ftw.write(line)
                    else:
                        checkfile = 1
                    if (line.strip() == endCheckLine.strip() and checkfile == 1):
                        checkfile = 0
                fr.close()
                ftw.close()
                ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "w")
                for line in ftr:
                    fw.write(line)
                ftr.close()
                fw.close()
        for site, hostname in hosts:
            html.live.set_prepend_site(True)
            query2 = "GET hosts\nColumns: alias address host_groups parents\nFilter: host_name = " + \
                     hostname
            host = html.live.query(query2)
            html.live.set_prepend_site(False)
            host.sort()
            _alias = ""
            _address = ""
            _hostgroups = []
            _parents = []
            _hostgroupsString = ""
            _parentsString = ""
            for sites, alias, address, hostgroups, parents in host:
                _alias = alias
                _address = address
                _hostgroups = hostgroups
                _parents = parents
            _parents.remove(oldhost.strip())
            if newhost.strip() != "":
                _parents.append(newhost.strip())
            _hostgroupsString = ", ".join(_hostgroups)
            _parentsString = ", ".join(_parents)
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "a")
            fw.write("\n#host-" + hostname)
            fw.write("\ndefine host {")
            fw.write("\n\tuse\t\t\tgeneric-host")
            fw.write("\n\thost_name\t\t" + hostname)
            fw.write("\n\talias\t\t\t" + _alias)
            fw.write("\n\taddress\t\t" + _address)
            if (_hostgroupsString.strip() != ""):
                fw.write("\n\thostgroups\t\t" + _hostgroupsString.strip())
            if (_parentsString.strip() != ""):
                fw.write("\n\tparents\t\t" + _parentsString.strip())
            fw.write("\n}")
            fw.write("\n#endhost-" + hostname)
            fw.close()


def delete_childhosts_of_host(host):
    """

    @param host:
    """
    global html
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: host_name\nFilter: parents >= " + host
    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    sitename = __file__.split("/")[3]

    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename)):
        for site, hostname in hosts:
            checkfile = 0
            startCheckLine = "#host-" + hostname
            endCheckLine = "#endhost-" + hostname
            fr = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "r")
            ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
            for line in fr:
                if (line.strip() != startCheckLine.strip() and checkfile == 0):
                    ftw.write(line)
                else:
                    checkfile = 1
                if (line.strip() == endCheckLine.strip() and checkfile == 1):
                    checkfile = 0
            fr.close()
            ftw.close()
            ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "w")
            for line in ftr:
                fw.write(line)
            ftr.close()
            fw.close()
            delete_services_of_host(hostname)
            delete_host_from_database(hostName)
            #########################
            delete_childhosts_of_host(hostname)

# function to delete service for a particular host


def delete_services_of_host(host_name):
    """

    @param host_name:
    """
    global html
    html.live.set_prepend_site(True)
    query = "GET services\nColumns: check_command\nFilter: host_name = " + \
            host_name
    services = html.live.query(query)
    html.live.set_prepend_site(False)
    services.sort()

    sitename = __file__.split("/")[3]

    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename)):
        for site, check_command in services:
            startCheckLine = "#service-" + host_name + "-" + check_command
            endCheckLine = "#endservice-" + host_name + "-" + check_command
            checkfile = 0
            fr = open(
                "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "r")
            ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
            for line in fr:
                if (line.strip() != startCheckLine.strip() and checkfile == 0):
                    ftw.write(line)
                else:
                    checkfile = 1
                if (line.strip() == endCheckLine.strip() and checkfile == 1):
                    checkfile = 0
            fr.close()
            ftw.close()
            ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "w")
            for line in ftr:
                fw.write(line)
            ftr.close()
            fw.close()


# function to update host details (ajax request)
def ajax_update_host(h):
    """

    @param h:
    """
    global html
    html = h

    if (html.var("hostName").strip() == "" or html.var("alias").strip() == ""):
        html.write(
            "2")  # retuen 2 if host name and alias both are null or empty
    else:
        countHost = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name alias\nFilter: name = " + \
                html.var("hostName").strip()

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()

        for site, host, alias in hosts:
            countHost += 1
            if (host.strip() != html.var("oldHostName").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 or countHost == 0):

            # delete host
            sitename = __file__.split("/")[3]
            startCheckLine = "#host-" + html.var("oldHostName").strip()
            endCheckLine = "#endhost-" + html.var("oldHostName").strip()
            checkfile = 0

            if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename)):
                fr = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "r")
                ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                for line in fr:
                    if (line.strip() != startCheckLine.strip() and checkfile == 0):
                        ftw.write(line)
                    else:
                        checkfile = 1
                    if (line.strip() == endCheckLine.strip() and checkfile == 1):
                        checkfile = 0
                fr.close()
                ftw.close()
                ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "w")
                for line in ftr:
                    fw.write(line)
                ftr.close()
                fw.close()

            fw = open(
                "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % sitename, "a")
            fw.write("\n#host-" + html.var("hostName"))
            fw.write("\ndefine host {")
            fw.write("\n\tuse\t\t\tgeneric-host")
            fw.write("\n\thost_name\t\t" + html.var("hostName"))
            fw.write("\n\talias\t\t\t" + html.var("alias"))
            fw.write("\n\taddress\t\t" + html.var("ipAddress"))
            if (html.var("hdHostGroup").strip() != ""):
                fw.write("\n\thostgroups\t\t" + html.var("hdHostGroup"))
            if (html.var("hdHostParent").strip() != ""):
                fw.write("\n\tparents\t\t" + html.var("hdHostParent"))
            fw.write("\n}")
            fw.write("\n#endhost-" + html.var("hostName") + "\n")
            fw.close()
            if html.var("hdDeviceType") != html.var("deviceType"):
                if html.var("hdDeviceType") == "AP":
                    delete_service_for_graph(
                        html.var("hostName"), "check_ap_bandwidth")
                    delete_service_for_graph(
                        html.var("hostName"), "check_ap_no_of_user")
                if html.var("deviceType") == "AP":
                    create_service_for_graph(
                        html.var("hostName"), "check_ap_bandwidth")
                    create_service_for_graph(
                        html.var("hostName"), "check_ap_no_of_user")

            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)

            # update the hostIPAddress, username, password, port and type in to mysql database
            # Open database connection
            db = MySQLdb.connect("localhost", "root", "root", "nms")
            totalRow = 0
            try:
                # prepare a cursor object using cursor() method
                cursor = db.cursor()
                sql = "SELECT COUNT(*) FROM nms_devices\
                          WHERE hostname = '%s'" % (html.var("oldHostName"))
                cursor.execute(sql)
                result = cursor.fetchall()
                for col in result:
                    totalRow = col[0]
                if totalRow == 0:
                    sql = "SELECT COUNT(*) FROM nms_devices\
                               WHERE hostname = '%s'" % (html.var("hostName"))
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for col in result:
                        totalRow = col[0]
                    if totalRow == 0:
                        sql = "INSERT INTO nms_devices (devicetype,ipaddress,username,password,port,hostname) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                            html.var("deviceType"), html.var("ipAddress"), html.var("confUsername"),
                            html.var("confPassword"), html.var("confPort"), html.var("hostName"))
                        cursor.execute(sql)
                else:
                    sql = "UPDATE nms_devices SET devicetype = '%s', ipaddress = '%s', username = '%s', password = '%s', port = '%s', hostname = '%s' \
                               WHERE hostname = '%s'" % (
                    html.var("deviceType"), html.var("ipAddress"), html.var("confUsername"), html.var("confPassword"),
                    html.var("confPort"), html.var("hostName"), html.var("oldHostName"))
                    cursor.execute(sql)
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
                # disconnect from server
            db.close()

            html.write("1")  # return 1 if host added successfully.
        else:
            html.write("0")  # return 0 if host already exist.


# function to create multiple selection list for hostgroup
def hostgroup_multiple_select_list(hostGroups, selectListId):
    """

    @param hostGroups:
    @param selectListId:
    @return:
    """
    selectList = ""
    html.live.set_prepend_site(True)
    query = "GET hostgroups\nColumns: hostgroup_name alias\n"

    hostgs = html.live.query(query)
    html.live.set_prepend_site(False)
    hostgs.sort()
    liList = ""
    for site, hostgroup_name, alias in hostgs:
        liList += "<li>" + hostgroup_name + "<img src=\"images/add16.png\" class=\"plus plus" + \
                  selectListId + "\" alt=\"+\" title=\"Add\" id=\"" + \
                  hostgroup_name + "\" /></li>"

    selectList += "<div class=\"multiSelectList\" id=\"multiSelectList" + \
                  selectListId + "\">"
    selectList += "<input type=\"hidden\" id=\"hd" + selectListId + \
                  "\" name=\"hd" + selectListId + "\" value=\"\" />"
    selectList += "<input type=\"hidden\" id=\"hdTemp" + selectListId + "\" name=\"hdTemp" + \
                  selectListId + "\" value=\"" + hostGroups + "\" />"
    selectList += "<div class=\"selected\">"
    selectList += "<div class=\"shead\"><span id=\"count\">0</span><span> Host Group(s)</span><a href=\"#\" id=\"rm" + \
                  selectListId + \
                  "\">Remove all</a>"
    selectList += "</div>"
    selectList += "<ul>"  # <li>asdf<img src=\"images/minus16.png\" class=\"minus\" alt=\"-\" title=\"Remove\" /></li>
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "<div class=\"nonSelected\">"
    selectList += "<div class=\"shead\"><a href=\"#\" id=\"add" + \
                  selectListId + "\">Add all</a>"
    selectList += "</div>"
    selectList += "<ul>" + liList
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "</div>"
    return selectList

# function to create multiple selection list for parents


def _parent_multiple_select_list(hostParents, selectListId):
    selectList = ""
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: name alias\n"

    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    liList = ""
    for site, name, alias in hosts:
        liList += "<li>" + name + "<img src=\"images/add16.png\" class=\"plus plus" + \
                  selectListId + "\" alt=\"+\" title=\"Add\" id=\"" + \
                  name + "\" /></li>"

    selectList += "<div class=\"multiSelectList\" id=\"multiSelectList" + \
                  selectListId + "\">"
    selectList += "<input type=\"hidden\" id=\"hd" + selectListId + \
                  "\" name=\"hd" + selectListId + "\" value=\"\" />"
    selectList += "<input type=\"hidden\" id=\"hdTemp" + selectListId + "\" name=\"hdTemp" + \
                  selectListId + "\" value=\"" + hostParents + "\" />"
    selectList += "<div class=\"selected\">"
    selectList += "<div class=\"shead\"><span id=\"count\">0</span><span> Parent(s)</span><a href=\"#\" id=\"rm" + \
                  selectListId + \
                  "\">Remove all</a>"
    selectList += "</div>"
    selectList += "<ul>"  # <li>asdf<img src=\"images/minus16.png\" class=\"minus\" alt=\"-\" title=\"Remove\" /></li>
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "<div class=\"nonSelected\">"
    selectList += "<div class=\"shead\"><a href=\"#\" id=\"add" + \
                  selectListId + "\">Add all</a>"
    selectList += "</div>"
    selectList += "<ul>" + liList
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "</div>"
    return selectList

# function to create multiple selection list for parents (ajax request)


def parent_multiple_select_list(h):
    """

    @param h:
    """
    global html
    html = h
    hostParents = ""
    selectListId = "HostParent"
    selectList = ""
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: name alias\n"

    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    liList = ""
    for site, name, alias in hosts:
        liList += "<li>" + name + "<img src=\"images/add16.png\" class=\"plus plus" + \
                  selectListId + "\" alt=\"+\" title=\"Add\" id=\"" + \
                  name + "\" /></li>"

    selectList += "<div class=\"multiSelectList\" id=\"multiSelectList" + \
                  selectListId + "\">"
    selectList += "<input type=\"hidden\" id=\"hd" + selectListId + \
                  "\" name=\"hd" + selectListId + "\" value=\"\" />"
    selectList += "<input type=\"hidden\" id=\"hdTemp" + selectListId + "\" name=\"hdTemp" + \
                  selectListId + "\" value=\"" + hostParents + "\" />"
    selectList += "<div class=\"selected\">"
    selectList += "<div class=\"shead\"><span id=\"count\">0</span><span> Parent(s)</span><a href=\"#\" id=\"rm" + \
                  selectListId + \
                  "\">Remove all</a>"
    selectList += "</div>"
    selectList += "<ul>"  # <li>asdf<img src=\"images/minus16.png\" class=\"minus\" alt=\"-\" title=\"Remove\" /></li>
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "<div class=\"nonSelected\">"
    selectList += "<div class=\"shead\"><a href=\"#\" id=\"add" + \
                  selectListId + "\">Add all</a>"
    selectList += "</div>"
    selectList += "<ul>" + liList
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "</div>"
    html.write(selectList)

#################################################################### END H

###################################################################### SERVICE #######################################################################
# function to add edit delete service details manually.


def page_manage_service(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/service.js"]
    html.new_header("Manage Service", "", "", css_list, js_list)
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")
    html.write(
        "<div id=\"formDiv\"></div><table class='addform' id='addservicetable' style='margin-bottom:0px;cursor:pointer;'><colgroup><col width='1%'/><col width='99%'/></colgroup><tr><th><img src='images/add16.png' alt='add'/></th><th>Add Service</th></tr></table></div>")
    html.write("<div id=\"gridviewDiv\">")
    html.write(
        "<div id=\"formDiv\"><table class='addform' id='iconmeaningtable' style='margin-bottom:0px;'><colgroup><col width='auto'/><col width='1%'/><col width='6%'/><col width='1%'/><col width='6%'/><col width='1%'/><col width='6%'/><col width='1%'/><col width='6%'/></colgroup><tr><th></th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-0.png\" alt=\"0\" width=\"10px\"/></th><th>ok</th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-1.png\" alt=\"1\" width=\"10px\"/></th><th>warning</th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-2.png\" alt=\"2\" width=\"10px\"/></th><th>critical</th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-3.png\" alt=\"3\" width=\"10px\"/></th><th>unknown</th></tr></table></div>")
    grid_view_service(h)
    html.write("</div>")
    html.new_footer()

# function to generate grid view for service (ajax request).


def grid_view_service(h):
    """

    @param h:
    """
    global html
    html = h
    try:
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name alias\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        totalService = 0

        # Open database connection
        db = MySQLdb.connect("localhost", "root", "root", "nms")

        all_i = 0

        tabledata = "<table class=\"addform\"><colgroup><col width='2%'/><col width='38%'/><col width='50%'/><col width='5%'/><col width='5%'/></colgroup>"
        for site, host, alias in hosts:
            # Is host bind with current user

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            sql = "SELECT COUNT(*) from nms_devices\
                     WHERE hostname = '%s' AND created_by = '%s'" % (host, config.user)
            cursor.execute(sql)
            count_host = cursor.fetchone()[0]
            cursor.close()

            if count_host > 0:
                all_i += 1
                indx = alias.find(":")
                if indx != -1:
                    alias = alias[:indx]
                tabledata += "<tr><th colspan='2'><a class=\"newlink\" style=\"color:white;\" href=\"view.py?view_name=host&host=" + host + "\" target=\"main\">" + \
                             host + " (" + alias + ")" + \
                             "</a></th><th></th><th colspan=\"2\"></th></tr>"
                query_service = "GET services\nColumns: description state check_command\nFilter: host_name = " + host
                html.live.set_prepend_site(True)
                services = html.live.query(query_service)
                services.sort()
                html.live.set_prepend_site(False)
                i = 0
                for service_site, description, state, command in services:
                    if description != "check_ap_bandwidth" and description != "check_ap_no_of_user":
                        totalService += 1
                        i += 1
                        if i % 2 == 0:
                            tabledata += "<tr class='even'>"
                        else:
                            tabledata += "<tr>"
                        tabledata += "<td style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-" + str(
                            state) + ".png\" alt=\"" + str(
                            state) + "\" width=\"10px\" /></td><td><a class=\"newlink\" href=\"view.py?view_name=service&service=" + description + "&host=" + host + "\" target=\"main\">" + description + \
                                     "</a><td></td><td><img src='images/edit16.png' alt='edit' title='Edit Service' class='imgbutton' onclick='editService(\"" + command + "\",\"" + host + \
                                     "\")'/></td><td><img src='images/delete16.png' alt='delete' title='Delete Service' class='imgbutton' onclick='deleteService(\"" + \
                                     command + \
                                     "\",\"" + \
                                     host + \
                                     "\")'/></td></tr>"

        if all_i == 0:
            tabledata += "<tr><td colspan=\"5\">No Service Exist</td></tr>"
        tabledata += "</table><input type=\"hidden\" id=\"totalService\" name=\"totalService\" value=\"" + str(
            totalService) + "\" />"
        db.close()
    except Exception as e:
        html.write("0")  # Some error occur, please Refresh the page
    else:
        html.write(tabledata)

# function to create form for add and edit information of service.


def form_for_service(h):
    """

    @param h:
    """
    global html
    html = h
    formdata = ""
    if html.var("action").strip() == "edit":
        html.live.set_prepend_site(True)
        query = "GET services\nColumns: description service_groups  max_check_attempts notification_interval check_interval retry_interval\nFilter: host_name = " + html.var(
            "host").strip() + "\nFilter: check_command = " + html.var("checkCommand").strip()

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        for site, description, servicegroup, max_check_attempts, notification_interval, check_interval, retry_interval in services:
            _serviceGroup = servicegroup
            _description = description
            _maxCheckAttempts = max_check_attempts
            _normalCheckInterval = check_interval
            _retryCheckInverval = retry_interval
            _notificationInterval = notification_interval
        serviceName = command = html.var("checkCommand").strip()
        indx = command.find("!")
        if indx != -1:
            serviceName = command[:indx]
        formdata += "<form id=\"addServiceForm\" action=\"ajaxcall_update_service.py\"><table class='addform'><colgroup><col width='20%'/><col width='40%'/><col width='40%'/></colgroup><tr><th colspan='3'>Edit Service</th></tr><tr class='trHost'><td>Host Name</td><td><input type='hidden' id='oldCheckCommand' name='oldCheckCommand' value=\"" + command + "\" /><input type='hidden' id='oldHostName' name='oldHostName' value=\"" + html.var(
            "host").strip() + "\" /><input type=\"text\" id=\"hostName\" name=\"hostName\" readonly=\"readonly\" value=\"" + html.var(
            "host").strip() + "\" /></td><td class=\"desc\"><a style=\"float:right;margin-right:10px;\" href=\"#\" id=\"changeHost\">change</a></td></tr><tr class='trService'><td>Service Name</td><td><input type=\"text\" id=\"serviceName\" name=\"serviceName\" readonly=\"readonly\" value=\"" + serviceName + "\" /></td><td class=\"desc\"><a style=\"float:right;margin-right:10px;\" href=\"#\" id=\"changeService\">change</a></td></tr><tr class='trService'><td>Description</td><td><input type=\"text\" id=\"serviceDescription\" name=\"serviceDescription\" value=\"" + _description + "\" maxlength='150'/></td><td class=\"desc\">Enter service description.</td></tr><tr class='trService'><td>Maximun Check Attempts</td><td><input type=\"text\" id=\"maxCheckAttempts\" name=\"maxCheckAttempts\" value=\"" + str(
            _maxCheckAttempts) + "\" /></td><td class=\"desc\">Enter maximum service check attempts. e.g. 5</td></tr><tr class='trService'><td>Normal Check Interval</td><td><input type=\"text\" id=\"normalCheckInterval\" name=\"normalCheckInterval\" value=\"" + str(
            _normalCheckInterval) + "\" /></td><td class=\"desc\">This is the service check interval (in sec.). (when service check doesn't fail.) e.g. 300 </td></tr><tr class='trService'><td>Retry Check Interval</td><td><input type=\"text\" id=\"retryCheckInterval\" name=\"retryCheckInterval\" value=\"" + str(
            _retryCheckInverval) + "\" /></td><td class=\"desc\">Enter retry check interval (in sec.). If service check fails, it retries with this time interval. if it still fails, send an alert. e.g. 180 </td></tr><tr class='trService'><td>Notification Interval</td><td><input type=\"text\" id=\"notificationInterval\" name=\"notificationInterval\" value=\"" + str(
            _notificationInterval) + "\" /></td><td class=\"desc\">Enter service notification interval (in sec.). e.g. 3600 </td></tr><tr class='trService' style=\"vertical-align: top;\"><td>Service Groups</td><td>" + servicegroup_multiple_select_list(
            ",".join(_serviceGroup),
            "ServiceGroup") + "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose Service Group(s) to add new service to.</td></tr><tr class='trWhite'><td class='button' colspan='3'></td></tr><tr class='trBlack'><th colspan='3'></th></tr><tr class='hostClass'><td style=\"padding: 0px;\" id=\"tdChooseHost\" colspan='3'>"
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name alias\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        liList = ""

        # Open database connection
        db = MySQLdb.connect("localhost", "root", "root", "nms")

        for site, name, alias in hosts:
            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            sql = "SELECT COUNT(*) from nms_devices\
                     WHERE hostname = '%s' AND created_by = '%s'" % (name, config.user)
            cursor.execute(sql)
            count_host = cursor.fetchone()[0]
            cursor.close()

            if count_host > 0:
                indx = alias.find(":")
                if indx != -1:
                    alias = alias[:indx]
                liList += "<li class=\"liHost\" id=\"" + name + "\" style=\"cursor:pointer;\"><div style=\"width:30%;float:left;overflow:hidden;height:20px;\"><b>" + name + \
                          "</b></div><div style=\"width:66%;float:left;overflow:hidden;height:20px;\">" + \
                          alias + "</div></li>"

        db.close()
        formdata += "<div class=\"multiSelectList\" style=\"width:100%; border:0 none;\" id=\"multiSelectListHosts\">"
        formdata += "<div class=\"selected\" style=\"width:100%\">"
        formdata += "<div class=\"shead\"><span>Choose Host</span>"
        formdata += "</div>"
        formdata += "<ul>" + liList
        formdata += "</ul>"
        formdata += "</div>"
        formdata += "</div>"
        formdata += "</td></tr><tr class='even hostClass'><td colspan='3'></td></tr><tr class='hostClass'><td colspan='3' class=\"button\"><input id='btnChooseHost' type='button' disabled='disabled' value='Continue' onclick=\"continueChooseHost()\"/><input type='button' value='Cancel' onclick=\"cancelChooseHostForEditService()\"/></td></tr>"
        formdata += create_service_choose_option("edit")
        formdata += "</table><div id=\"serviceForm\"></div></form>"
        html.write(formdata)
    else:
        formdata += "<form id=\"addServiceForm\" action=\"ajaxcall_add_service.py\"><table class='addform'><colgroup><col width='20%'/><col width='40%'/><col width='40%'/></colgroup><tr><th colspan='3'>Add New Service</th></tr><tr class='trHost'><td>Host Name</td><td><input type='hidden' id='oldCheckCommand' name='oldCheckCommand' value=\"\" /><input type=\"text\" id=\"hostName\" name=\"hostName\" readonly=\"readonly\" /></td><td class=\"desc\"><a style=\"float:right;margin-right:10px;\" href=\"#\" id=\"changeHost\">change</a></td></tr><tr class='trService'><td>Service Name</td><td><input type=\"text\" id=\"serviceName\" name=\"serviceName\" readonly=\"readonly\" /></td><td class=\"desc\"><a style=\"float:right;margin-right:10px;\" href=\"#\" id=\"changeService\">change</a></td></tr><tr class='trService'><td>Description</td><td><input type=\"text\" id=\"serviceDescription\" name=\"serviceDescription\" value=\"\" maxlength='150'/></td><td class=\"desc\">Enter service description.</td></tr><tr class='trService'><td>Maximun Check Attempts</td><td><input type=\"text\" id=\"maxCheckAttempts\" name=\"maxCheckAttempts\" value=\"5\" /></td><td class=\"desc\">Enter maximum service check attempts. e.g. 5</td></tr><tr class='trService'><td>Normal Check Interval</td><td><input type=\"text\" id=\"normalCheckInterval\" name=\"normalCheckInterval\" value=\"300\" /></td><td class=\"desc\">This is the service check interval (in sec.). (when service check doesn't fail.) e.g. 300 </td></tr><tr class='trService'><td>Retry Check Interval</td><td><input type=\"text\" id=\"retryCheckInterval\" name=\"retryCheckInterval\" value=\"180\" /></td><td class=\"desc\">Enter retry check interval (in sec.). If service check fails, it retries with this time interval. if it still fails, send an alert. e.g. 180 </td></tr><tr class='trService'><td>Notification Interval</td><td><input type=\"text\" id=\"notificationInterval\" name=\"notificationInterval\" value=\"3600\" /></td><td class=\"desc\">Enter service notification interval (in sec.). e.g. 3600 </td></tr><tr class='trService'><td style=\"vertical-align: top;\">Service Groups</td><td>" + servicegroup_multiple_select_list(
            "",
            "ServiceGroup") + "</td><td class=\"desc\" style=\"vertical-align: top;\">Choose Service Group(s) to add new service to.</td></tr><tr class='trWhite'><td class='button' colspan='3'></td></tr><tr class='trBlack'><th colspan='3'></th></tr><tr class='hostClass'><td style=\"padding: 0px;\" id=\"tdChooseHost\" colspan='3'>"
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: name alias\n"

        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        liList = ""

        # Open database connection
        db = MySQLdb.connect("localhost", "root", "root", "nms")

        for site, name, alias in hosts:
            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            sql = "SELECT COUNT(*) from nms_devices\
                     WHERE hostname = '%s' AND created_by = '%s'" % (name, config.user)
            cursor.execute(sql)
            count_host = cursor.fetchone()[0]
            cursor.close()

            if count_host > 0:
                indx = alias.find(":")
                if indx != -1:
                    alias = alias[:indx]
                liList += "<li class=\"liHost\" id=\"" + name + "\" style=\"cursor:pointer;\"><div style=\"width:30%;float:left;overflow:hidden;height:20px;\"><b>" + name + \
                          "</b></div><div style=\"width:66%;float:left;overflow:hidden;height:20px;\">" + \
                          alias + "</div></li>"

        db.close()
        formdata += "<div class=\"multiSelectList\" style=\"width:100%; border:0 none;\" id=\"multiSelectListHosts\">"
        formdata += "<div class=\"selected\" style=\"width:100%\">"
        formdata += "<div class=\"shead\"><span>Choose Host</span>"
        formdata += "</div>"
        formdata += "<ul>" + liList
        formdata += "</ul>"
        formdata += "</div>"
        formdata += "</div>"
        formdata += "</td></tr><tr class='even hostClass'><td colspan='3'></td></tr><tr class='hostClass'><td colspan='3' class=\"button\"><input id='btnChooseHost' type='button' disabled='disabled' value='Continue' onclick=\"continueChooseHost()\"/><input type='button' value='Cancel' onclick=\"javascript:cancelChooseHost();\"/></td></tr>"
        formdata += create_service_choose_option("add")
        formdata += "</table><div id=\"serviceForm\"></div></form>"
        html.write(formdata)

# function to create services choose options


def create_service_choose_option(act):
    """

    @param act:
    @return:
    """
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/service.xml" % site)
    services = dom.getElementsByTagName("service")
    servicelist = "<tr class='serviceClass'><td style=\"padding: 0px;\" id=\"tdChooseServices\" colspan='3'>"
    servicelist += "<div class=\"multiSelectList\" style=\"width:100%; border:0 none;\" id=\"multiSelectListService\">"
    servicelist += "<div class=\"selected\" style=\"width:100%\">"
    servicelist += "<div class=\"shead\"><span>Choose Service</span>"
    servicelist += "</div>"
    servicelist += "<ul>" + create_service_buttons(services)
    servicelist += "</ul>"
    servicelist += "</div>"
    servicelist += "</div>"
    if act == "edit":
        servicelist += "</td></tr><tr class='even serviceClass'><td colspan='3'></td></tr><tr class='serviceClass'><td class=\"button\" colspan='3'><input id='btnChooseService' type='button' disabled='disabled' value='Continue' onclick=\"continueChooseService()\"/><input type='button' value='Cancel' onclick=\"cancelChooseHostForEditService()\"/></td></tr>"
    else:
        servicelist += "</td></tr><tr class='even serviceClass'><td colspan='3'></td></tr><tr class='serviceClass'><td class=\"button\" colspan='3'><input id='btnChooseService' type='button' disabled='disabled' value='Continue' onclick=\"continueChooseService()\"/><input type='button' value='Back to choose Host' onclick=\"cancelChooseService()\"/><input type='button' value='Cancel' onclick=\"cancelAddService()\"/></td></tr>"

    return servicelist

# function to return the list of services in html format


def create_service_buttons(services):
    """

    @param services:
    @return:
    """
    liList = ""
    for service in services:
        service_name = service.getAttribute('name')
        service_description = service.getElementsByTagName("description")[0]
        liList += "<li class=\"liService\" id=\"" + service_name + "\" style=\"cursor:pointer;\"><div style=\"width:30%;float:left;overflow:hidden;height:20px;\"><b>" + service_name + \
                  "</b></div><div style=\"width:66%;float:left;overflow:hidden;height:20px;\">" + getText(
            service_description.childNodes) + "</div></li>"
    return liList

# function to return XML tag text


def getText(nodelist):
    """

    @param nodelist:
    @return:
    """
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# create a template for service attributes


def form_for_service_setting(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/service.xml" % site)
    services = dom.getElementsByTagName("service")
    for service in services:
        if (service.getAttribute('name').strip() == html.var("serviceName").strip()):
            create_form_for_basic_service_setting(service.getElementsByTagName("arg"), service.getAttribute(
                'graph').strip(), service.getAttribute('name').strip(), html.var("action").strip())
            break

# function to create a template for the addvance and basic settings


def create_form_for_basic_service_setting(argument, graph, name, action):
    """

    @param argument:
    @param graph:
    @param name:
    @param action:
    """
    paraBasic = 0
    paraAdvance = 0
    serviceOptionTable = "<table class='addform'><colgroup><col width='20%'/><col width='20%'/><col width='60%'/></colgroup>"
    tableStringBasic = "<tr><th colspan='3'>Service Basic Settings</th></tr>"
    tableStringAdvance = "<tr><th colspan='3'>Service Advance Settings</th></tr>"
    for arg in argument:
        if (getText(arg.getElementsByTagName("name")[0].childNodes).strip() == "@#$"):
            for aoarg in arg.getElementsByTagName("aoarg"):
                paraAdvance += 1
                tableStringAdvance += "<tr><td>" + getText(
                    aoarg.getElementsByTagName("name")[0].childNodes).strip() + "</td>"
                tableStringAdvance += "<td><input type='text' id='aoarg" + str(paraAdvance) + "' name='aoarg" + str(
                    paraAdvance) + "' para='" + aoarg.getAttribute('id').strip() + "' value=''/></td>"
                tableStringAdvance += "<td class='desc'>" + getText(
                    aoarg.getElementsByTagName("description")[0].childNodes).strip() + "</td></tr>"
        else:
            paraBasic += 1
            tableStringBasic += "<tr><td>" + getText(arg.getElementsByTagName(
                "name")[0].childNodes).strip() + "</td>"
            tableStringBasic += "<td><input type='text' id='arg" + str(paraBasic) + "' name='arg" + str(
                paraBasic) + "' para='$ARG" + arg.getAttribute(
                'id').strip() + "$' value=''/><label generated=\"false\" for=\"arg" + str(
                paraBasic) + "\" style=\"display:none;color:red;\" id=\"error_arg" + str(
                paraBasic) + "\"> *</label></td>"
            tableStringBasic += "<td class='desc'>" + getText(
                arg.getElementsByTagName("description")[0].childNodes).strip() + "</td></tr>"
    if paraBasic > 0:
        serviceOptionTable += tableStringBasic
    if paraAdvance > 0:
        serviceOptionTable += tableStringAdvance
    if action == "edit":
        serviceOptionTable += "<tr><td class=\"button\" colspan='3'><input type='submit' value='Update Service' /><input type='button' value='Cancel' onclick=\"cancelEditService()\"/><input type='hidden' id='advanceArgument' name='advanceArgument' value='" + str(
            paraAdvance) + "'/><input type='hidden' id='basicArgument' name='basicArgument' value='" + str(
            paraBasic) + "'/><input type='hidden' id='hdGraph' name='hdGraph' value='" + graph + "'/><input type='hidden' id='hdCommand' name='hdCommand' value='" + name + "' /></td></tr></table>"
    else:
        serviceOptionTable += "<tr><td class=\"button\" colspan='3'><input type='submit' value='Add New Service' /><input type='button' value='Back' onclick=\"backToChooseService()\"/><input type='button' value='Cancel' onclick=\"cancelAddService()\"/><input type='hidden' id='advanceArgument' name='advanceArgument' value='" + str(
            paraAdvance) + "'/><input type='hidden' id='basicArgument' name='basicArgument' value='" + str(
            paraBasic) + "'/><input type='hidden' id='hdGraph' name='hdGraph' value='" + graph + "'/><input type='hidden' id='hdCommand' name='hdCommand' value='" + name + "' /></td></tr></table>"
    html.write(serviceOptionTable)

# function to create multiple selection list for servicegroup


def servicegroup_multiple_select_list(serviceGroups, selectListId):
    """

    @param serviceGroups:
    @param selectListId:
    @return:
    """
    selectList = ""
    html.live.set_prepend_site(True)
    query = "GET servicegroups\nColumns: servicegroup_name alias\n"

    servicegs = html.live.query(query)
    html.live.set_prepend_site(False)
    servicegs.sort()
    liList = ""
    for site, servicegroup_name, alias in servicegs:
        liList += "<li>" + servicegroup_name + "<img src=\"images/add16.png\" class=\"plus plus" + \
                  selectListId + "\" alt=\"+\" title=\"Add\" id=\"" + \
                  servicegroup_name + "\" /></li>"

    selectList += "<div class=\"multiSelectList\" id=\"multiSelectList" + \
                  selectListId + "\">"
    selectList += "<input type=\"hidden\" id=\"hd" + selectListId + \
                  "\" name=\"hd" + selectListId + "\" value=\"\" />"
    selectList += "<input type=\"hidden\" id=\"hdTemp" + selectListId + "\" name=\"hdTemp" + \
                  selectListId + "\" value=\"" + serviceGroups + "\" />"
    selectList += "<div class=\"selected\">"
    selectList += "<div class=\"shead\"><span id=\"count\">0</span><span> Service Group(s)</span><a href=\"#\" id=\"rm" + \
                  selectListId + \
                  "\">Remove all</a>"
    selectList += "</div>"
    selectList += "<ul>"  # <li>asdf<img src=\"images/minus16.png\" class=\"minus\" alt=\"-\" title=\"Remove\" /></li>
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "<div class=\"nonSelected\">"
    selectList += "<div class=\"shead\"><a href=\"#\" id=\"add" + \
                  selectListId + "\">Add all</a>"
    selectList += "</div>"
    selectList += "<ul>" + liList
    selectList += "</ul>"
    selectList += "</div>"
    selectList += "</div>"
    return selectList

# function to add new service (ajax request)


def ajax_add_service(h):
    """

    @param h:
    """
    global html
    html = h
    basicPara = int(html.var("basicArgument"))
    advancePara = int(html.var("advanceArgument"))
    checkPara = 1
    for n in range(1, (basicPara + 1)):
        if html.var("arg" + str(n)).strip() == "":
            checkPara = 0
            html.write(str(n))
            break

    if (html.var("serviceName").strip() == "" or html.var("hostName").strip() == "" or html.var(
            "serviceDescription").strip() == "" or checkPara == 0):
        html.write(
            "2")  # retuen 2 if service name and alias both are null or empty
    else:
        sitename = __file__.split("/")[3]
        countService = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        # query = "GET services\nColumns: host_name description check_command
        # max_check_attempts  service_groups\nFilter: host_name = " +
        # html.var("hostName").strip()
        query = "GET services\nColumns: check_command\nFilter: host_name = " + \
                html.var("hostName").strip()

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        for site, command in services:
            countService += 1
            if (command.strip() == html.var("hdCommand").strip()):
                checkfile = 0
                break
            else:
                checkfile = 1

        if (checkfile == 1 or countService == 0):
            countDescription = 0
            html.live.set_prepend_site(True)
            query2 = "GET services\nColumns: description\nFilter: host_name = " + \
                     html.var("hostName").strip()
            serviceDescription = html.live.query(query2)
            html.live.set_prepend_site(False)
            serviceDescription.sort()
            for sites, desc in serviceDescription:
                if desc == html.var("serviceDescription").strip():
                    countDescription += 1
            if countDescription == 0:
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "a")
                fw.write("#service-" + html.var(
                    "hostName").strip() + "-" + html.var("hdCommand").strip())
                fw.write("\ndefine service {")
                fw.write("\n\tuse\t\t\tgeneric-service-perf,generic-service")
                fw.write("\n\thost_name\t\t" + html.var("hostName").strip())
                fw.write("\n\tservice_description\t\t\t" +
                         html.var("serviceDescription").strip())
                if (html.var("maxCheckAttempts").strip() != ""):
                    fw.write("\n\tmax_check_attempts\t\t" +
                             html.var("maxCheckAttempts").strip())
                if (html.var("normalCheckInterval").strip() != ""):
                    fw.write("\n\tnormal_check_interval\t\t" +
                             html.var("normalCheckInterval").strip())
                if (html.var("retryCheckInterval").strip() != ""):
                    fw.write("\n\tretry_check_interval\t\t" +
                             html.var("retryCheckInterval").strip())
                if (html.var("notificationInterval").strip() != ""):
                    fw.write("\n\tnotification_interval\t\t" +
                             html.var("notificationInterval").strip())

                if (html.var("hdServiceGroup").strip() != ""):
                    fw.write(
                        "\n\tservicegroups\t\t" + html.var("hdServiceGroup"))

                if (html.var("hdCommand").strip() != ""):
                    fw.write("\n\tcheck_command\t\t" + html.var("hdCommand"))
                fw.write("\n}")
                fw.write("\n#endservice-" + html.var(
                    "hostName").strip() + "-" + html.var("hdCommand") + "\n")
                fw.close()
                os.system(
                    'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
                html.write("1")  # return 1 if service added successfully.
            else:
                html.write(
                    "2")  # return 2 if service description is already exist.
        else:
            html.write("0")  # return 0 if service already exist.

# function to delete host (ajax request)


def ajax_delete_service(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    startCheckLine = "#service-" + html.var("hostName").strip() + "-" + \
                     html.var("checkCommand")
    endCheckLine = "#endservice-" + html.var("hostName").strip() + "-" + \
                   html.var("checkCommand")
    checkfile = 0
    if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename)):
        fr = open(
            "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "r")
        ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
        for line in fr:
            if (line.strip() != startCheckLine.strip() and checkfile == 0):
                ftw.write(line)
            else:
                checkfile = 1
            if (line.strip() == endCheckLine.strip() and checkfile == 1):
                checkfile = 0
        fr.close()
        ftw.close()
        ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
        fw = open(
            "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "w")
        for line in ftr:
            fw.write(line)
        ftr.close()
        fw.close()
        os.system(
            'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)

        html.write("1")
    else:
        html.write("0")

# function to update host details (ajax request)


def ajax_update_service(h):
    """

    @param h:
    """
    global html
    html = h

    basicPara = int(html.var("basicArgument"))
    advancePara = int(html.var("advanceArgument"))
    checkPara = 1
    for n in range(1, (basicPara + 1)):
        if html.var("arg" + str(n)).strip() == "":
            checkPara = 0
            html.write(str(n))
            break

    if (html.var("serviceName").strip() == "" or html.var("hostName").strip() == "" or html.var(
            "serviceDescription").strip() == "" or checkPara == 0):
        html.write("2")
    else:
        sitename = __file__.split("/")[3]
        countService = 0
        checkfile = 0

        html.live.set_prepend_site(True)
        # query = "GET services\nColumns: host_name description check_command
        # max_check_attempts  service_groups\nFilter: host_name = " +
        # html.var("hostName").strip()
        query = "GET services\nColumns: host_name check_command\nFilter: host_name = " + html.var(
            "hostName").strip() + "\nFilter: check_command = " + html.var("hdCommand").strip()

        services = html.live.query(query)
        html.live.set_prepend_site(False)
        services.sort()

        for site, hostname, command in services:
            countService += 1
            if (hostname.strip() == html.var("oldHostName").strip() and command.strip() == html.var(
                    "oldCheckCommand").strip()):
                checkfile = 1
            else:
                checkfile = 0
                break

        if (checkfile == 1 or countService == 0):
            countDescription = 0
            html.live.set_prepend_site(True)
            query2 = "GET services\nColumns: description check_command\nFilter: host_name = " + html.var(
                "hostName").strip()
            serviceDescription = html.live.query(query2)
            html.live.set_prepend_site(False)
            serviceDescription.sort()
            for sites, desc, comm in serviceDescription:
                if comm != html.var("oldCheckCommand").strip() and desc == html.var("serviceDescription").strip():
                    countDescription += 1
            if countDescription == 0:
                # delete service
                startCheckLine = "#service-" + html.var(
                    "oldHostName").strip() + "-" + html.var("oldCheckCommand")
                endCheckLine = "#endservice-" + html.var(
                    "oldHostName").strip() + "-" + html.var("oldCheckCommand")
                checkfile = 0
                if (os.path.isfile("/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename)):
                    fr = open(
                        "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "r")
                    ftw = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "w")
                    for line in fr:
                        if (line.strip() != startCheckLine.strip() and checkfile == 0):
                            ftw.write(line)
                        else:
                            checkfile = 1
                        if (line.strip() == endCheckLine.strip() and checkfile == 1):
                            checkfile = 0
                    fr.close()
                    ftw.close()
                    ftr = open("/omd/sites/%s/tmp/temp.cfg" % sitename, "r")
                    fw = open(
                        "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "w")
                    for line in ftr:
                        fw.write(line)
                    ftr.close()
                    fw.close()

                # add service
                fw = open(
                    "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % sitename, "a")
                fw.write("#service-" + html.var(
                    "hostName").strip() + "-" + html.var("hdCommand").strip())
                fw.write("\ndefine service {")
                fw.write("\n\tuse\t\t\tgeneric-service-perf,generic-service")
                fw.write("\n\thost_name\t\t" + html.var("hostName").strip())
                fw.write("\n\tservice_description\t\t\t" +
                         html.var("serviceDescription").strip())
                if (html.var("maxCheckAttempts").strip() != ""):
                    fw.write("\n\tmax_check_attempts\t\t" +
                             html.var("maxCheckAttempts").strip())
                if (html.var("normalCheckInterval").strip() != ""):
                    fw.write("\n\tnormal_check_interval\t\t" +
                             html.var("normalCheckInterval").strip())
                if (html.var("retryCheckInterval").strip() != ""):
                    fw.write("\n\tretry_check_interval\t\t" +
                             html.var("retryCheckInterval").strip())
                if (html.var("notificationInterval").strip() != ""):
                    fw.write("\n\tnotification_interval\t\t" +
                             html.var("notificationInterval").strip())

                if (html.var("hdServiceGroup").strip() != ""):
                    fw.write(
                        "\n\tservicegroups\t\t" + html.var("hdServiceGroup"))

                if (html.var("hdCommand").strip() != ""):
                    fw.write("\n\tcheck_command\t\t" + html.var("hdCommand"))
                fw.write("\n}")
                fw.write("\n#endservice-" + html.var(
                    "hostName").strip() + "-" + html.var("hdCommand") + "\n")
                fw.close()
                os.system(
                    'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % sitename)
                html.write("1")  # return 1 if service added successfully.
            else:
                html.write(
                    "2")  # return 2 if service description is already exist.
        else:
            html.write("0")  # return 0 if host already exist.


#################################################################### END S

#################################################################### ALERT

# function to view all the alerts
def page_view_alerts(h):
    """

    @param h:
    """
    global html
    html = h
    html.new_header("Alerts")
    # get alerts
    html.write(problem_host_list())
    html.new_footer()

# function to create host list


def problem_host_list():
    """


    @return:
    """
    global html
    html.live.set_prepend_site(True)
    query = "GET hosts\nColumns: name state worst_service_state\nFilter: state > 0\nFilter: worst_service_state > 0\nOr: 2\n"
    hosts = html.live.query(query)
    html.live.set_prepend_site(False)
    hosts.sort()
    tabledata = "<table class=addform><colgroup><col width=\"2%\"><col width=\"30%\"><col width=\"20%\"><col width=\"38%\"><col width=\"10%\"></colgroup>\n"
    tabledata += "<tr><th colspan=\"2\">Service</th><th>Host</th><th>Status detail</th><th>Age</th></tr>"
    i = 0
    countAlerts = 0
    for site, host, state, worstsvc in hosts:
        query_service = "GET services\nColumns: description state check_command service_plugin_output service_last_state_change service_has_been_checked\nFilter: host_name = " + host + \
                        "\nFilter: state > 0\n"
        html.live.set_prepend_site(True)
        services = html.live.query(query_service)
        services.sort()
        html.live.set_prepend_site(False)
        i += 1
        for service_site, description, state, command, servicedetail, age, checked in services:
            countAlerts += 1
            if i % 2 == 0:
                tabledata += "<tr class='even'>"
            else:
                tabledata += "<tr>"
            tabledata += "<td style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-" + str(
                state) + ".png\" alt=\"" + str(
                state) + "\" width=\"10px\" /></td><td><a class=\"newlink\" href=\"view.py?view_name=service&service=" + description + "&host=" + host + "\" target=\"main\">" + \
                         description + "</a><td>" + \
                         host + "</td><td>" + servicedetail + "</td><td>" + \
                         paint_age(age, checked == 1, 60 * 10) + "</td></tr>"
    tabledata += "<tr><td colspan=\"5\" class='button'><input type='button' value='Back' onclick=\"javascript:parent.main.location='main.py';\"/></td></tr></table>"
    tableHead = "<table class='addform' id='iconmeaningtable' style='margin-bottom:0px;'><colgroup><col width='auto'/><col width='1%'/><col width='6%'/><col width='1%'/><col width='6%'/><col width='1%'/><col width='6%'/><col width='1%'/><col width='6%'/></colgroup><tr><th> Alerts (" + str(
        countAlerts) + ") </th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-0.png\" alt=\"0\" width=\"10px\"/></th><th>ok</th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-1.png\" alt=\"1\" width=\"10px\"/></th><th>warning</th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-2.png\" alt=\"2\" width=\"10px\"/></th><th>critical</th><th style=\"padding:5px 0px 5px 10px;\"><img src=\"images/status-3.png\" alt=\"3\" width=\"10px\"/></th><th>unknown</th></tr></table>"
    return tableHead + tabledata


def paint_age(timestamp, has_been_checked, bold_if_younger_than):
    """

    @param timestamp:
    @param has_been_checked:
    @param bold_if_younger_than:
    @return:
    """
    if not has_been_checked:
        return "age", "-"

    age = time.time() - timestamp
    if age >= 48 * 3600 or age < -48 * 3600:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    # Time delta less than two days => make relative time
    if age < 0:
        age = -age
        prefix = "in "
    else:
        prefix = ""
    if age < bold_if_younger_than:
        age_class = "age recent"
    else:
        age_class = "age"
    return prefix + html.age_text(age)


# function to create link
def link(name, href):
    """

    @param name:
    @param href:
    @return:
    """
    return "<a class='newlink' href='" + href + "' >" + name + "</a>"


#################################################################### END A
