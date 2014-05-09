#!/usr/bin/python2.6

import os
import subprocess

import MySQLdb
import xml.dom.minidom

from ap_service import *
import config
from lib import *



############################################ Network Overview ############


def network_overview(h):
    """

    @param h:
    """
    global hrml
    html = h
    css_list = ["css/style.css"]
    js_list = ["js/unmp/main/overview.js"]
    html.new_header("Host Inventory", "", "", css_list, js_list)
    html.write("<div class=\"tab-yo\">")
    html.write("<div class=\"tab-head\">")
    html.write(
        "<a id=\"pingButton\" href=\"#pingDiv\" class=\"tab-button\">Ping")
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
    html.write("<h2>Discovery")
    html.write("</h2>")
    html.write(
        "<a id=\"optionMenuButton\" href=\"#\" class=\"tab-button\" style=\"float:right;\">")
    html.write("<span class=\"tab-img-button\">")
    html.write("</span>")
    html.write("</a>")
    html.write("</div>")
    html.write("<div id=\"pingDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    dicoveredHostDetailsForPing(h)
    html.write("</div>")
    html.write("<div id=\"snmpDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    dicoveredHostDetailsForSnmp(h)
    html.write("</div>")
    html.write("<div id=\"upnpDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    dicoveredHostDetailsForUPnP(h)
    html.write("</div>")
    html.write("<div id=\"sdmcDiv\" class=\"tab-body discoveryDetailsBody\" style=\"display:none;\">")
    dicoveredHostDetailsForSDMC(h)
    html.write("</div>")
    html.write("<div id=\"allDiv\" class=\"tab-body\">")
    discoveredHostDetailsForAll(h)
    html.write("</div>")
    html.write("</div>")

    # discovery option menu
    html.write("""<div id="optionMenu" class="jstree-default-context">
	<ul>
		<li class="">
			<ins>&nbsp;</ins>
			<a rel="start" href="#">Start</a>
		</li>
		<li class="vakata-separator vakata-separator-after"></li>
		<li class="">
			<ins>&nbsp;</ins>
			<a rel="stop" href="#">Stop</a>
		</li>
		<li class="vakata-separator vakata-separator-before"></li>
		<li class="">
			<ins>&nbsp;</ins>
			<a rel="viewDetails" href="#">View Details</a>
		</li>
		<li class="">
			<ins>&nbsp;</ins>
			<a rel="discoveredHostDetails" href="#">Hide View Details</a>
		</li>
	</ul>
</div>""")
    # end discovery option menu
    html.write("<div id=\"nmsDetail\">")
    # discoveryAndNetworkDetails(h)
    html.write("</div>")
    html.footer()
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")

########################################## End Network Overview ##########


def list_search(list_, value):
    """

    @param list_:
    @param value:
    @return:
    """
    i = -1
    try:
        i = list_.index(value)
        return i
    except:
        return i


def discoveredHostDetailsForAll(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    checkboxState = ""
    host_list = []
    dom_sdm = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site)
    dom_snmp = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site)
    dom_upnp = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site)
    dom_ping = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site)
    discovery = dom_sdm.getElementsByTagName("discovery")
    for dis in discovery:
        if int(dis.getAttribute("active").strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
    discovery = dom_snmp.getElementsByTagName("discovery")
    for dis in discovery:
        if int(dis.getAttribute("active").strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
    discovery = dom_upnp.getElementsByTagName("discovery")
    for dis in discovery:
        if int(dis.getAttribute("active").strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
    discovery = dom_ping.getElementsByTagName("discovery")
    for dis in discovery:
        if int(dis.getAttribute("active").strip()) == 1:
            checkboxState = " disabled=\"disabled\" "

    discoveredHostsString = "<div><table width=\"60%\" class=\"host-table\"><tbody><tr><th align=\"left\"><input type=\"checkbox\" id=\"allChecked\" name=\"allChecked\" value=\"all\"" + checkboxState + \
                            "/></th><th align=\"left\">Host Name</th><th align=\"left\">Host Alias</th><th align=\"left\">Host Address</th><th align=\"left\">Device Type</th></tr>"
    discoveredHosts = dom_sdm.getElementsByTagName("host")
    i = 0
    for host in discoveredHosts:
        if list_search(host_list, host.getAttribute("address")) == -1:
            i += 1
            discoveredHostsString += "<tr><td><input type=\"checkbox\" class=\"sdm\" id=\"host" + str(
                i) + "\" name=\"host\" value=\"" + host.getAttribute(
                "name") + "\" " + checkboxState + "/></td><td>" + host.getAttribute(
                "name") + "</td><td>" + host.getAttribute("alias") + "</td><td>" + host.getAttribute(
                "address") + "</td><td>" + deviceTypeOption(host.getAttribute("type"), i) + "</td></tr>"
            host_list.append(host.getAttribute("address"))
        else:
            dom_sdm.getElementsByTagName(
                "discoveredHosts")[0].removeChild(host)
            fwxml = open(
                "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site, "w")
            fwxml.write(dom_sdm.toxml())
            fwxml.close()

    discoveredHosts = dom_snmp.getElementsByTagName("host")
    for host in discoveredHosts:
        if list_search(host_list, host.getAttribute("address")) == -1:
            i += 1
            discoveredHostsString += "<tr><td><input type=\"checkbox\" class=\"snmp\" id=\"host" + str(
                i) + "\" name=\"host\" value=\"" + host.getAttribute(
                "name") + "\" " + checkboxState + "/></td><td>" + host.getAttribute(
                "name") + "</td><td>" + host.getAttribute("alias") + "</td><td>" + host.getAttribute(
                "address") + "</td><td>" + deviceTypeOption(host.getAttribute("type"), i) + "</td></tr>"
            host_list.append(host.getAttribute("address"))
        else:
            dom_snmp.getElementsByTagName(
                "discoveredHosts")[0].removeChild(host)
            fwxml = open(
                "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site, "w")
            fwxml.write(dom_snmp.toxml())
            fwxml.close()

    discoveredHosts = dom_upnp.getElementsByTagName("host")
    for host in discoveredHosts:
        if list_search(host_list, host.getAttribute("address")) == -1:
            i += 1
            discoveredHostsString += "<tr><td><input type=\"checkbox\" class=\"upnp\" id=\"host" + str(
                i) + "\" name=\"host\" value=\"" + host.getAttribute(
                "name") + "\" " + checkboxState + "/></td><td>" + host.getAttribute(
                "name") + "</td><td>" + host.getAttribute("alias") + "</td><td>" + host.getAttribute(
                "address") + "</td><td>" + deviceTypeOption(host.getAttribute("type"), i) + "</td></tr>"
            host_list.append(host.getAttribute("address"))
        else:
            dom_upnp.getElementsByTagName(
                "discoveredHosts")[0].removeChild(host)
            fwxml = open(
                "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site, "w")
            fwxml.write(dom_upnp.toxml())
            fwxml.close()

    discoveredHosts = dom_ping.getElementsByTagName("host")
    for host in discoveredHosts:
        if list_search(host_list, host.getAttribute("address")) == -1:
            i += 1
            discoveredHostsString += "<tr><td><input type=\"checkbox\" class=\"ping\" id=\"host" + str(
                i) + "\" name=\"host\" value=\"" + host.getAttribute(
                "name") + "\" " + checkboxState + "/></td><td>" + host.getAttribute(
                "name") + "</td><td>" + host.getAttribute("alias") + "</td><td>" + host.getAttribute(
                "address") + "</td><td>" + deviceTypeOption(host.getAttribute("type"), i) + "</td></tr>"
            host_list.append(host.getAttribute("address"))
        else:
            dom_ping.getElementsByTagName(
                "discoveredHosts")[0].removeChild(host)
            fwxml = open(
                "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site, "w")
            fwxml.write(dom_ping.toxml())
            fwxml.close()

    if i == 0:
        discoveredHostsString = "<table width=\"60%\"><tr><th align=\"left\" style=\"padding-left:10px;\"> No Host Discovered</th></tr>"
    else:
        discoveredHostsString += "<tr><td colspan=\"5\" align=\"left\" style=\"padding:5px;\"><input type=\"button\" onclick=\"allSubmit();\" id=\"allSubmit\" name=\"allSubmit\" value=\"Submit\"" + checkboxState + "/></td></tr>"
    discoveredHostsString += "<input type=\"hidden\" name=\"totalHost\" value=\"" + \
                             str(i) + "\"/></tbody></table></div>"
    html.write(discoveredHostsString)


def dicoveredHostDetailsForPing(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site)
    discoveryString = "<div>"
    discovery = dom.getElementsByTagName("discovery")
    discoveredHosts = dom.getElementsByTagName("host")
    checkboxState = ""
    i = 0
    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"100\"/>"
    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"0\"/>"
    html.write(discoveryString + "</div>")


def dicoveredHostDetailsForSnmp(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site)
    discoveryString = "<div>"
    discovery = dom.getElementsByTagName("discovery")
    discoveredHosts = dom.getElementsByTagName("host")
    checkboxState = ""
    i = 0
    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"100\"/>"
    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"0\"/>"
    html.write(discoveryString + "</div>")


def dicoveredHostDetailsForUPnP(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site)
    discoveryString = "<div>"
    discovery = dom.getElementsByTagName("discovery")
    discoveredHosts = dom.getElementsByTagName("host")
    checkboxState = ""
    i = 0
    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"100\"/>"
    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"0\"/>"
    html.write(discoveryString + "</div>")


def dicoveredHostDetailsForSDMC(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site)
    discoveryString = "<div>"
    discovery = dom.getElementsByTagName("discovery")
    discoveredHosts = dom.getElementsByTagName("host")
    checkboxState = ""
    i = 0
    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            checkboxState = " disabled=\"disabled\" "
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"100\"/>"
    html.write(discoveryString + "</div>")


def discoveryDetailsForPing(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site)
    discoveryString = ""
    discoveryDetailString = ""
    discovery = dom.getElementsByTagName("discovery")

    i = 0
    discoveryDetailString = "<table width=\"60%\" style=\"margin-left:10px;\"><tr><th align=\"left\" colspan=\"2\">Discovery Details</th></tr>"

    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"100\"/>"
        discoveryDetailString += "<tr><td>Start IP Range <td/><td>" + dis.getAttribute(
            'ip') + "." + dis.getAttribute('start') + "</td></tr>"
        discoveryDetailString += "<tr><td>End IP Range <td/><td>" + dis.getAttribute(
            'ip') + "." + dis.getAttribute('end') + "</td></tr>"
        discoveryDetailString += "<tr><td>Timeout<td/><td>" + \
                                 dis.getAttribute('timeout') + " sec.</td></tr>"
        discoveryDetailString += "<tr><td>Hostgroups<td/><td>" + \
                                 dis.getAttribute('hostgroup') + "</td></tr>"
        if int(dis.getAttribute('service')) == 1:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using port scanning</td></tr>"
        elif int(dis.getAttribute('service')) == 2:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using service template</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Service<td/><td>Do not create service</td></tr>"
        discoveryDetailString += "<tr><td>User <span style=\"font-size:9px;\">(who set the details)</span><td/><td>" + \
                                 dis.getAttribute(
                                     'username') + "</td></tr>"
        if int(dis.getAttribute('active')) == 1:
            discoveryDetailString += "<tr><td>Status<td/><td>Active</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Status<td/><td>Inactive</td></tr>"

    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"pingStatus\" name=\"pingStatus\" value=\"0\"/>"
        discoveryDetailString = "<table width=\"60%\"><tr><th align=\"left\" style=\"padding-left:10px;\"> No Details</th></tr>"
    discoveryString += "</table>"
    html.write(discoveryString + discoveryDetailString)


def discoveryDetailsForSnmp(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site)
    discoveryString = ""
    discoveryDetailString = ""
    discovery = dom.getElementsByTagName("discovery")

    i = 0
    discoveryDetailString = "<table width=\"60%\" style=\"margin-left:10px;\"><tr><th align=\"left\" colspan=\"2\">Discovery Details</th></tr>"

    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"100\"/>"
        discoveryDetailString += "<tr><td>Start IP Range <td/><td>" + dis.getAttribute(
            'ip') + "." + dis.getAttribute('start') + "</td></tr>"
        discoveryDetailString += "<tr><td>End IP Range <td/><td>" + dis.getAttribute(
            'ip') + "." + dis.getAttribute('end') + "</td></tr>"
        discoveryDetailString += "<tr><td>Community<td/><td>" + \
                                 dis.getAttribute('community') + "</td></tr>"
        discoveryDetailString += "<tr><td>Port<td/><td>" + \
                                 dis.getAttribute('port') + "</td></tr>"
        discoveryDetailString += "<tr><td>Version<td/><td>" + \
                                 dis.getAttribute('version') + "</td></tr>"
        discoveryDetailString += "<tr><td>Timeout<td/><td>" + \
                                 dis.getAttribute('timeout') + " sec.</td></tr>"
        discoveryDetailString += "<tr><td>Hostgroups<td/><td>" + \
                                 dis.getAttribute('hostgroup') + "</td></tr>"
        if int(dis.getAttribute('service')) == 1:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using port scanning</td></tr>"
        elif int(dis.getAttribute('service')) == 2:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using service template</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Service<td/><td>Do not create service</td></tr>"
        discoveryDetailString += "<tr><td>User <span style=\"font-size:9px;\">(who set the details)</span><td/><td>" + \
                                 dis.getAttribute(
                                     'username') + "</td></tr>"
        if int(dis.getAttribute('active')) == 1:
            discoveryDetailString += "<tr><td>Status<td/><td>Active</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Status<td/><td>Inactive</td></tr>"

    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"snmpStatus\" name=\"snmpStatus\" value=\"0\"/>"
        discoveryDetailString = "<table width=\"60%\"><tr><th align=\"left\" style=\"padding-left:10px;\"> No Details</th></tr>"
    discoveryString += "</table>"
    html.write(discoveryString + discoveryDetailString)


def discoveryDetailsForUPnP(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site)
    discoveryString = ""
    discoveryDetailString = ""
    discovery = dom.getElementsByTagName("discovery")

    i = 0
    discoveryDetailString = "<table width=\"60%\" style=\"margin-left:10px;\"><tr><th align=\"left\" colspan=\"2\">Discovery Details</th></tr>"

    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"100\"/>"
        discoveryDetailString += "<tr><td>Timeout<td/><td>" + \
                                 dis.getAttribute('timeout') + " sec.</td></tr>"
        discoveryDetailString += "<tr><td>Hostgroups<td/><td>" + \
                                 dis.getAttribute('hostgroup') + "</td></tr>"
        if int(dis.getAttribute('service')) == 1:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using port scanning</td></tr>"
        elif int(dis.getAttribute('service')) == 2:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using service template</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Service<td/><td>Do not create service</td></tr>"
        discoveryDetailString += "<tr><td>User <span style=\"font-size:9px;\">(who set the details)</span><td/><td>" + \
                                 dis.getAttribute(
                                     'username') + "</td></tr>"
        if int(dis.getAttribute('active')) == 1:
            discoveryDetailString += "<tr><td>Status<td/><td>Active</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Status<td/><td>Inactive</td></tr>"

    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"upnpStatus\" name=\"upnpStatus\" value=\"0\"/>"
        discoveryDetailString = "<table width=\"60%\"><tr><th align=\"left\" style=\"padding-left:10px;\"> No Details</th></tr>"
    discoveryString += "</table>"
    html.write(discoveryString + discoveryDetailString)


def discoveryDetailsForSDMC(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parse(
        "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site)
    discoveryString = ""
    discoveryDetailString = ""
    discovery = dom.getElementsByTagName("discovery")

    i = 0
    discoveryDetailString = "<table width=\"60%\" style=\"margin-left:10px;\"><tr><th align=\"left\" colspan=\"2\">Discovery Details</th></tr>"

    for dis in discovery:
        i += 1
        if int(dis.getAttribute('active').strip()) == 1:
            discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                'complete') + "% Completed...</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"1\"/>"
        else:
            if float(dis.getAttribute('complete')) < 100:
                discoveryString += "<div class=\"msg-head\"><img src=\"images/loading-small-stop.gif\" alt=\"\" style=\"vertical-align: middle;\" /><span> Discovery " + dis.getAttribute(
                    'complete') + "% Completed... [stopped]</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"0\"/>"
            else:
                discoveryString += "<div class=\"msg-head\"><span>Discovery 100% done</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"100\"/>"
        discoveryDetailString += "<tr><td>Timeout<td/><td>" + \
                                 dis.getAttribute('timeout') + " sec.</td></tr>"
        discoveryDetailString += "<tr><td>Hostgroups<td/><td>" + \
                                 dis.getAttribute('hostgroup') + "</td></tr>"
        discoveryDetailString += "<tr><td>Selected Device<td/><td>" + \
                                 dis.getAttribute('device') + "</td></tr>"
        if int(dis.getAttribute('service')) == 1:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using port scanning</td></tr>"
        elif int(dis.getAttribute('service')) == 2:
            discoveryDetailString += "<tr><td>Service<td/><td>Create service using service template</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Service<td/><td>Do not create service</td></tr>"
        discoveryDetailString += "<tr><td>User <span style=\"font-size:9px;\">(who set the details)</span><td/><td>" + \
                                 dis.getAttribute(
                                     'username') + "</td></tr>"
        if int(dis.getAttribute('active')) == 1:
            discoveryDetailString += "<tr><td>Status<td/><td>Active</td></tr>"
        else:
            discoveryDetailString += "<tr><td>Status<td/><td>Inactive</td></tr>"

    if i == 0:
        discoveryString += "<div class=\"msg-head\"><span>No Discovery details</span></div><input type=\"hidden\" id=\"sdmcStatus\" name=\"sdmcStatus\" value=\"0\"/>"
        discoveryDetailString = "<table width=\"60%\"><tr><th align=\"left\" style=\"padding-left:10px;\"> No Details</th></tr>"
    discoveryString += "</table>"
    html.write(discoveryString + discoveryDetailString)


def startDiscovery(h):
    """

    @param h:
    """
    global html
    html = h
    discoveryType = html.var("type")
    site = __file__.split("/")[3]
    discoveryXmlFilePath = ""
    ipBase = ""
    ipRangeStart = ""
    ipRangeEnd = ""
    timeOut = ""
    perlFile = ""
    community = ""
    version = ""
    port = ""
    snmpUserName = ""
    authKey = ""
    snmpPassword = ""
    authProtocol = ""
    privKey = ""
    privPassword = ""
    privProtocol = ""

    if discoveryType == "ping":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site
        perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/pingdiscoverycreatexml.pl" % site
    elif discoveryType == "snmp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site
        perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/snmpdiscoverycreatexml.pl" % site
    elif discoveryType == "upnp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site
        perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/upnpdiscoverycreatexml.pl" % site
    if discoveryXmlFilePath != "":
        dom = xml.dom.minidom.parse(discoveryXmlFilePath)
        discovery = dom.getElementsByTagName("discovery")
        for dis in discovery:
            if discoveryType == "ping":
                ipBase = dis.getAttribute("ip")
                ipRangeStart = dis.getAttribute("current")
                ipRangeEnd = dis.getAttribute("end")
                timeOut = dis.getAttribute("timeout")
            elif discoveryType == "snmp":
                ipBase = dis.getAttribute("ip")
                ipRangeStart = dis.getAttribute("current")
                ipRangeEnd = dis.getAttribute("end")
                timeOut = dis.getAttribute("timeout")
                community = dis.getAttribute("community")
                version = dis.getAttribute("version")
                port = dis.getAttribute("port")
                snmpUserName = dis.getAttribute("snmpUser")
                authKey = dis.getAttribute("authKey")
                snmpPassword = dis.getAttribute("password")
                authProtocol = dis.getAttribute("authProtocol")
                privKey = dis.getAttribute("privKey")
                privPassword = dis.getAttribute("privPassword")
                privProtocol = dis.getAttribute("privProtocol")
            elif discoveryType == "upnp":
                timeOut = dis.getAttribute("timeout")
        if discoveryType == "ping":
            args = [ipBase + "." + ipRangeStart, ipBase + "." +
                                                 ipRangeEnd, timeOut, discoveryXmlFilePath]
            command = [perlFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]
        elif discoveryType == "snmp":
            args = [
                ipBase + "." + ipRangeStart, ipBase + "." +
                                             ipRangeEnd, community, timeOut, version, port,
                snmpUserName, authKey, snmpPassword, authProtocol, privKey, privPassword, privProtocol,
                discoveryXmlFilePath]
            command = [perlFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]
        elif discoveryType == "upnp":
            # delete all host from xml file
            host = dom.getElementsByTagName("host")
            for hos in host:
                dom.getElementsByTagName("discoveredHosts")[0].removeChild(hos)
            fwxml = open(discoveryXmlFilePath, "w")
            fwxml.write(dom.toxml())
            fwxml.close()
            args = [timeOut, discoveryXmlFilePath]
            command = [perlFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]
        html.write("0")
    else:
        html.write("1")


def stopStartDiscovery(h):
    """

    @param h:
    """
    global html
    html = h
    action = html.var("action")
    discoveryType = html.var("type")
    site = __file__.split("/")[3]
    discoveryXmlFilePath = ""

    if discoveryType == "ping":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site
    elif discoveryType == "snmp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site
    elif discoveryType == "upnp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site
    if discoveryXmlFilePath != "":
        dom = xml.dom.minidom.parse(discoveryXmlFilePath)
        discovery = dom.getElementsByTagName("discovery")
        for dis in discovery:
            if action == "stop":
                dis.setAttribute("active", "0")
            else:
                dis.setAttribute("active", "1")
        fwxml = open(discoveryXmlFilePath, "w")
        fwxml.write(dom.toxml())
        fwxml.close()
        html.write("0")
    else:
        html.write("1")


def discoveryAndNetworkDetails(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    html.write(
        "<div class=\"demo jstree jstree-0 jstree-default jstree-focused\" id=\"demo\"><ul><li id=\"node_2\" rel=\"drive\" class=\"jstree-last  jstree-open\"><ins class=\"jstree-icon\">&nbsp;</ins><a href=\"#\" class=\"jstree-clicked\"><ins class=\"jstree-icon\">&nbsp;</ins>NMS</a><ul style=\"\">")

    nmsTree = ""
    html.live.set_prepend_site(True)
    query = "GET hostgroups\nColumns: hostgroup_name alias\n"
    hostgroups = html.live.query(query)
    html.live.set_prepend_site(False)
    hostgroups.sort()
    hostgroup_i = 0
    for site, hostgroup, alias in hostgroups:
        hostgroup_i += 1
        nmsTree += "<li id=\"" + hostgroup + "\" rel=\"folder\" class=\"jstree-open\"><ins class=\"jstree-icon\">&nbsp;</ins><a href=\"#\" class=\"\" style=\"-moz-user-select: none;\"><ins class=\"jstree-icon\">&nbsp;</ins>" + alias + \
                   "</a><ul style=\"\">"
        html.live.set_prepend_site(True)
        query = "GET hosts\nColumns: host_name alias\nFilter: host_groups >= " + \
                hostgroup
        hosts = html.live.query(query)
        html.live.set_prepend_site(False)
        hosts.sort()
        host_i = 0
        for host_site, host, alias in hosts:
            host_i += 1
            nmsTree += "<li id=\"" + host + "\" rel=\"folder\" class=\"jstree-open\"><ins class=\"jstree-icon\">&nbsp;</ins><a href=\"#\" class=\"\" style=\"-moz-user-select: none;\"><ins class=\"jstree-icon\">&nbsp;</ins>" + alias + "</a><ul style=\"\">"
            html.live.set_prepend_site(True)
            query = "GET services\nColumns: description state check_command\nFilter: host_name = " + host
            services = html.live.query(query)
            html.live.set_prepend_site(False)
            services.sort()
            for service_site, description, state, command in services:
                service_i = 0
                nmsTree += "<li id=\"" + host + "_service_" + str(
                    service_i) + "\" rel=\"default\" class=\"jstree-leaf\"><ins class=\"jstree-icon\">&nbsp;</ins><a href=\"#\" class=\"\" style=\"-moz-user-select: none;\"><ins class=\"jstree-icon\">&nbsp;</ins>" + \
                           description + \
                           "</a></li>"
            nmsTree += "</ul></li>"

        nmsTree += "</ul></li>"
    nmsTree += "</ul></div>"
    html.write(nmsTree)


def discoveryStatus(h):
    """

    @param h:
    """
    global html
    html = h
    status = "0"
    discoveryType = html.var("type")
    site = __file__.split("/")[3]
    discoveryXmlFilePath = ""
    if discoveryType == "ping":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site
    elif discoveryType == "snmp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site
    elif discoveryType == "upnp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site
    elif discoveryType == "sdmc":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site
    if discoveryXmlFilePath != "":
        dom = xml.dom.minidom.parse(discoveryXmlFilePath)
        discovery = dom.getElementsByTagName("discovery")
        for dis in discovery:
            if int(dis.getAttribute('active').strip()) == 1:
                status = "1"
            else:
                if float(dis.getAttribute('complete')) < 100:
                    status = "0"
                else:
                    status = "100"
    html.write(status)


def createHostConfiguration(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    discoveryType = html.var("type")
    discoveryXmlFilePath = ""
    if discoveryType == "ping":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site
    elif discoveryType == "snmp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site
    elif discoveryType == "upnp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site
    elif discoveryType == "sdmc":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site
    hostList = html.var("hostList")
    hosts = hostList.split(",")
    deviceType = html.var("deviceType").split(",")

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    totalRow = 0
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    ind = 0
    hostFile = "/omd/sites/%s/etc/nagios/conf.d/hosts.cfg" % site
    hostGroup = ""
    serviceManagement = "0"
    hostTemplate = "generic-host"
    dom = xml.dom.minidom.parseString(
        "<nmsDB><autoDiscovery><discovery/></autoDiscovery><discoveredHosts></discoveredHosts></nmsDB>")
    if discoveryXmlFilePath != "":
        dom = xml.dom.minidom.parse(discoveryXmlFilePath)
    hostDom = dom.getElementsByTagName("host")
    discoveryDom = dom.getElementsByTagName("discovery")
    for dis in discoveryDom:
        hostGroup = dis.getAttribute("hostgroup")
        serviceManagement = dis.getAttribute("service")

    # create host in configuration file
    try:
        for host in hosts:
            countHost = 0
            checkfile = 0
            alias = "alias"
            address = "0.0.0.0"
            for hDom in hostDom:
                if hDom.getAttribute("name").strip() == host:
                    alias = hDom.getAttribute("alias").strip()
                    address = hDom.getAttribute("address").strip()
                    dom.getElementsByTagName(
                        "discoveredHosts")[0].removeChild(hDom)
                    break
            html.live.set_prepend_site(True)
            query = "GET hosts\nColumns: name\nFilter: name = " + host
            hostQueryResult = html.live.query(query)
            html.live.set_prepend_site(False)
            hostQueryResult.sort()

            for siteName, hostName in hostQueryResult:
                countHost += 1
                if (hostName.strip() == host):
                    checkfile = 0
                    break
                else:
                    checkfile = 1

            if (checkfile == 1 or countHost == 0):
                fw = open(hostFile, "a")
                fw.write("\n#host-" + host)
                fw.write("\ndefine host {")
                fw.write("\n\tuse\t\t\t" + hostTemplate)
                fw.write("\n\thost_name\t\t" + host)
                fw.write("\n\talias\t\t\t" + alias)
                fw.write("\n\taddress\t\t" + address)
                if (hostGroup != ""):
                    fw.write("\n\thostgroups\t\t" + hostGroup)
                fw.write("\n}")
                fw.write("\n#endhost-" + host + "\n")
                fw.close()

                # add graph service if this device AP type device
                if deviceType[ind].strip() == "AP":
                    create_service_for_graph(
                        html.var("hostName").strip(), "check_ap_bandwidth")
                    create_service_for_graph(
                        html.var("hostName").strip(), "check_ap_no_of_user")

                # insert the host details in database
                sql = "SELECT COUNT(*) FROM nms_devices\
                           WHERE hostname = '%s'" % (host)
                cursor.execute(sql)
                result = cursor.fetchall()
                totalRow = 0
                for col in result:
                    totalRow = col[0]
                if totalRow == 0:
                    sql = "INSERT INTO nms_devices (devicetype,ipaddress,username,password,port,hostname,created_by) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                        deviceType[ind], address, "", "", "", host, config.user)
                    cursor.execute(sql)
                    db.commit()
            ind += 1
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()
    os.system('kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % site)

    if str(serviceManagement) == "0" or str(serviceManagement) == "1":
        fwxml = open(discoveryXmlFilePath, "w")
        fwxml.write(dom.toxml())
        fwxml.close()
    html.write(str(serviceManagement))


def createSeviceConfiguration(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    discoveryType = html.var("type")
    discoveryXmlFilePath = ""
    if discoveryType == "ping":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/pingDiscovery.xml" % site
    elif discoveryType == "snmp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/snmpDiscovery.xml" % site
    elif discoveryType == "upnp":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/upnpDiscovery.xml" % site
    elif discoveryType == "sdmc":
        discoveryXmlFilePath = "/omd/sites/%s/share/check_mk/web/htdocs/xml/sdmcDiscovery.xml" % site
    hostList = html.var("hostList")
    serviceManagement = html.var("service")
    serviceTemplate = "generic-service"
    serviceFile = "/omd/sites/%s/etc/nagios/conf.d/services.cfg" % site
    perlFile = "/omd/sites/%s/share/check_mk/web/htdocs/portscan.pl" % site
    hosts = hostList.split(",")
    dom = xml.dom.minidom.parseString(
        "<nmsDB><autoDiscovery><discovery/></autoDiscovery><discoveredHosts></discoveredHosts></nmsDB>")
    if discoveryXmlFilePath != "":
        dom = xml.dom.minidom.parse(discoveryXmlFilePath)
    hostDom = dom.getElementsByTagName("host")

    if serviceManagement.strip() == "1":
        args = [discoveryType, hostList, serviceFile, serviceTemplate]
        command = [perlFile]
        command.extend(args)
        pipe = subprocess.Popen(
            command, stdout=subprocess.PIPE).communicate()[0]
        if str(pipe) == "0":
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % site)
        html.write(pipe)
    elif serviceManagement.strip() == "2":
        if discoveryType == "sdmc":
            hostType = ""
            serviceTemplateId = ""

            # create service template dom
            shyamDevicesDom = xml.dom.minidom.parseString(
                "<shyamDevices></shyamDevices>")
            if (os.path.isfile("/omd/sites/%s/share/check_mk/web/htdocs/xml/shyamdevices.xml" % site)):
                shyamDevicesDom = xml.dom.minidom.parse(
                    "/omd/sites/%s/share/check_mk/web/htdocs/xml/shyamdevices.xml" % site)

            # create service template dom
            templateDom = xml.dom.minidom.parseString("<hosts></hosts>")
            if (os.path.isfile("/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % site)):
                templateDom = xml.dom.minidom.parse(
                    "/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % site)

            for host in hosts:
                countService = 0
                checkfile = 0
                serviceConfig = ""

                html.live.set_prepend_site(True)
                query = "GET services\nColumns: check_command description\nFilter: host_name = " + \
                        host
                serviceQueryResult = html.live.query(query)
                html.live.set_prepend_site(False)
                serviceQueryResult.sort()

                for hDom in hostDom:
                    if hDom.getAttribute("name").strip() == host:
                        hostType = hDom.getAttribute("type")
                        dom.getElementsByTagName(
                            "discoveredHosts")[0].removeChild(hDom)
                        break
                for sdDom in shyamDevicesDom.getElementsByTagName("device"):
                    if sdDom.getAttribute("sdmcDiscoveryValue").strip() == hostType:
                        serviceTemplateId = sdDom.getAttribute(
                            "applyedServiceTemplate")
                        break
                for tDom in templateDom.getElementsByTagName("host"):
                    if tDom.getAttribute("id").strip() == serviceTemplateId:
                        for stDom in tDom.getElementsByTagName("service"):
                            new_check_command = getText(stDom.getElementsByTagName(
                                "check_command")[0].childNodes).strip().replace("$IPADDRESS$", host)
                            # check service existence
                            for siteName, command, desc in serviceQueryResult:
                                countService += 1
                                if (command == new_check_command or desc == getText(
                                        stDom.getElementsByTagName("service_description")[0].childNodes).strip()):
                                    checkfile = 0
                                    break
                                else:
                                    checkfile = 1

                            if (checkfile == 1 or countService == 0):
                                serviceConfig += "\n#service-" + \
                                                 host + "-" + new_check_command + "\n"
                                serviceConfig += "define service {\n"
                                serviceConfig += "\tuse\t\t\t" + getText(
                                    stDom.getElementsByTagName("use")[0].childNodes).strip() + "\n"
                                serviceConfig += "\thost_name\t\t" + \
                                                 host + "\n"
                                serviceConfig += "\tservice_description\t" + getText(
                                    stDom.getElementsByTagName("service_description")[0].childNodes).strip() + "\n"
                                serviceConfig += "\tmax_check_attempts\t\t\t" + getText(
                                    stDom.getElementsByTagName("max_check_attempts")[0].childNodes).strip() + "\n"
                                serviceConfig += "\tnormal_check_interval\t\t\t" + getText(
                                    stDom.getElementsByTagName("normal_check_interval")[0].childNodes).strip() + "\n"
                                serviceConfig += "\tretry_check_interval\t\t\t" + getText(
                                    stDom.getElementsByTagName("retry_check_interval")[0].childNodes).strip() + "\n"
                                serviceConfig += "\tnotification_interval\t\t\t" + getText(
                                    stDom.getElementsByTagName("notification_interval")[0].childNodes).strip() + "\n"
                                serviceConfig += "\tcheck_command\t\t\t" + \
                                                 new_check_command + "\n"
                                serviceConfig += "}\n"
                                serviceConfig += "#endservice-" + \
                                                 host + "-" + new_check_command + "\n"
                        break

                fsw = open(serviceFile, "a")
                fsw.write(serviceConfig)
                fsw.close()
            os.system(
                'kill -HUP `cat /omd/sites/%s/tmp/lock/nagios.lock`' % site)
            fwxml = open(discoveryXmlFilePath, "w")
            fwxml.write(dom.toxml())
            fwxml.close()
        html.write("0")

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

# function to create device type option


def deviceTypeOption(dtype, dtypeId):
    """

    @param dtype:
    @param dtypeId:
    @return:
    """
    strDeviceType = "<select name='deviceType' id='deviceType" + str(
        dtypeId) + "'>"

    if dtype == "Unknown":
        strDeviceType += "<option value=\"Unknown\" selected=\"selected\">Unknown Device</option>"
    else:
        strDeviceType += "<option value=\"Unknown\">Unknown Device</option>"

    if dtype == "ODU16":
        strDeviceType += "<option value=\"ODU16\" selected=\"selected\">ODU-16Mbps</option>"
    else:
        strDeviceType += "<option value=\"ODU16\">ODU-16Mbps</option>"

    if dtype == "ODU100":
        strDeviceType += "<option value=\"ODU100\" selected=\"selected\">ODU-100Mbps</option>"
    else:
        strDeviceType += "<option value=\"ODU100\">ODU-100Mbps</option>"

    if dtype == "IDU4":
        strDeviceType += "<option value=\"IDU4\" selected=\"selected\">IDU-4 Port</option>"
    else:
        strDeviceType += "<option value=\"IDU4\">IDU-4 Port</option>"

    if dtype == "IDU8":
        strDeviceType += "<option value=\"IDU8\" selected=\"selected\">IDU-8 Port</option>"
    else:
        strDeviceType += "<option value=\"IDU8\">IDU-8 Port</option>"

    if dtype == "SWT24":
        strDeviceType += "<option value=\"SWT24\" selected=\"selected\">Switch-24 Port</option>"
    else:
        strDeviceType += "<option value=\"SWT24\">Switch-24 Port</option>"

    if dtype == "SWT8":
        strDeviceType += "<option value=\"SWT8\" selected=\"selected\">Switch-8 Port</option>"
    else:
        strDeviceType += "<option value=\"SWT8\">Switch-8 Port</option>"

    if dtype == "SWT4":
        strDeviceType += "<option value=\"SWT4\" selected=\"selected\">Switch-4 Port</option>"
    else:
        strDeviceType += "<option value=\"SWT4\">Switch-4 Port</option>"

    if dtype == "AP":
        strDeviceType += "<option value=\"AP\" selected=\"selected\">Access Point</option>"
    else:
        strDeviceType += "<option value=\"AP\">Access Point</option>"

    if dtype == "HG":
        strDeviceType += "<option value=\"HG\" selected=\"selected\">Home Gateway</option>"
    else:
        strDeviceType += "<option value=\"HG\">Home Gateway</option>"

    if dtype == "HG22":
        strDeviceType += "<option value=\"HG22\" selected=\"selected\">Home Gateway 22dBm</option>"
    else:
        strDeviceType += "<option value=\"HG22\">Home Gateway 22dBm</option>"

    if dtype == "AP22":
        strDeviceType += "<option value=\"AP22\" selected=\"selected\">Access Point 22</option>"
    else:
        strDeviceType += "<option value=\"AP22\">Access Point 22</option>"

    if dtype == "CPE":
        strDeviceType += "<option value=\"CPE\" selected=\"selected\">CPE</option>"
    else:
        strDeviceType += "<option value=\"CPE\">CPE</option>"

    if dtype == "CPE22":
        strDeviceType += "<option value=\"CPE22\" selected=\"selected\">CPE22</option>"
    else:
        strDeviceType += "<option value=\"CPE22\">CPE22</option>"

    if dtype == "EG":
        strDeviceType += "<option value=\"EG\" selected=\"selected\">Enterprise Gateway</option>"
    else:
        strDeviceType += "<option value=\"EG\">Enterprise Gateway</option>"

    strDeviceType += "</select>"
    return strDeviceType
