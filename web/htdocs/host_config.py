#!/usr/bin/python2.6
import base64
import datetime
import os
import re
import subprocess
import tarfile
import time
import urllib2

import MySQLdb
from mod_python import apache, util
import xml.dom.minidom

from lib import *

############################################### Manage Template ##########


def manage_configuration_template(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    html.new_header("Manage Configuration Profile")
    html.write(
        "<script type=\"text/javascript\" src=\"js/unmp/main/configScripts.js\"></script>\n")
    html.write(
        "<script type=\"text/javascript\" src=\"js/unmp/main/manage_configuration_template.js\"></script>\n")
    html.write(
        "<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\n")

    # create tabs for manage configuration
    html.write("<div class=\"tab-yo\">")
    html.write("<div class=\"tab-head main-head\">")
    html.write("<a id=\"addButton\" href=\"#addDiv\" class=\"tab-button\">Add")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"editButton\" href=\"#editDiv\" class=\"tab-button\" style=\"display:none;\">Edit")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"viewButton\" href=\"#viewDiv\" class=\"tab-active\">View")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write("<h2>Configuration Profile")
    html.write("</h2>")
    html.write("</div>")
    addDeviceButtonHover(h)
    html.write(
        "<div id=\"addDiv\" class=\"tab-body\" style=\"display:none;\">")
    # dicoveredHostDetailsForPing(h)
    html.write("</div>")
    html.write(
        "<div id=\"editDiv\" class=\"tab-body\" style=\"display:none;\">")
    # dicoveredHostDetailsForSnmp(h)
    html.write("</div>")
    html.write(
        "<div id=\"viewDiv\" class=\"tab-body\" style=\"display:block;\">")
    view_configuration_template(h)
    html.write("</div>")
    html.write("</div>")
    html.footer()
    html.write(
        "<div class=\"loading\"><img src='images/loading.gif' alt=''/></div>")


def view_configuration_template(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    configTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplate.xml" % (
        site)
    dom = xml.dom.minidom.parseString(
        "<configurationTemplate></configurationTemplate>")
    if (os.path.isfile(configTemplateFile)):
        dom = xml.dom.minidom.parse(configTemplateFile)
    templateDom = dom.getElementsByTagName("template")
    i = 0
    tableString = "<table style=\"width:100%;padding:20px;\">"
    tableString += "<colgroup><col width='5%'/><col width='25%'/><col width='60%'/><col width='5%'/><col width='5%'/></colgroup>"
    tableString += "<tr><th align=\"left\">S.No</th><th align=\"left\">Device Name</th><th align=\"left\">Profile Name</th><th colspan=\"2\"></th></tr>"
    for tDom in templateDom:
        i += 1
        tableString += "<tr><td>" + str(i) + "</td><td>" + tDom.getAttribute(
            "deviceName") + "</td><td>" + tDom.getAttribute(
            "name") + "</td><td><img onclick=\"editConfigurationProfile('" + tDom.getAttribute("id") + \
                       "')\" class=\"imgbutton\" title=\"Edit Configuration Profile\" alt=\"edit\" src=\"images/edit16.png\"></td><td><img onclick=\"deleteConfigurationProfile('" + tDom.getAttribute(
            "id") + "')\" class=\"imgbutton\" title=\"Delete Configuration Profile\" alt=\"delete\" src=\"images/delete16.png\"></td></tr>"
    tableString += "</table>"
    if i == 0:
        html.write(
            "<div style=\"display:block;width:100%; text-align:center;margin:10px;\">No Configuration Profile</div>")
    else:
        html.write(tableString)


def addDeviceButtonHover(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    # load shyam device form syhamdevices.xml file
    shyamDeviceFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/shyamdevices.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString("<shyamDevices></shyamDevices>")
    if (os.path.isfile(shyamDeviceFile)):
        dom = xml.dom.minidom.parse(shyamDeviceFile)
    deviceListXml = dom.getElementsByTagName("device")
    i = 0
    deviceListHoverMenu = "<div id=\"addDivHover\" class=\"device-hover-menu\">"
    for dev in deviceListXml:
        if dev.getAttribute("hide") == "false":
            i += 1
            deviceListHoverMenu += "<a href=\"#\" id=\"" + dev.getAttribute(
                "id") + "\" name=\"" + dev.getAttribute("sdmcDiscoveryId") + "\" sdmc=\"" + dev.getAttribute(
                "sdmcDiscoveryValue") + "\">" + dev.getAttribute("name") + "</a>"

    if i == 0:
        deviceListHoverMenu += "<div style=\"padding: 10px 20px 10px 20px;color:#FFF;\">No Shyam Device Exist</div></div>"
    else:
        deviceListHoverMenu += "</div>"

    html.write(deviceListHoverMenu)


def add_configuration_template(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    deviceId = html.var("deviceId")
    deviceName = html.var("deviceName")
    templateString = ""

    # load device configuration template form configurationTemplateDefault.xml
    # file
    deviceTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplateDefault.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString(
        "<configurationTemplate></configurationTemplate>")
    if (os.path.isfile(deviceTemplateFile)):
        dom = xml.dom.minidom.parse(deviceTemplateFile)
    defaultTemplateDom = dom.getElementsByTagName("defaultTemplate")
    i = 0
    for tDom in defaultTemplateDom:
        if tDom.getAttribute("deviceId") == deviceId:
            i += 1
            templateString += "<div style=\"margin: 20px;\"><form action=\"create_config_tamplate.py\" method=\"post\" id=\"createTemplate\">"
            templateString += "<table width=\"100%\">"
            templateString += "<colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"></colgroup>"
            templateString += "<tr><td>Device Name</td><td><input type=\"text\" id=\"deviceName\" name=\"deviceName\" value=\"" + deviceName + \
                              "\" readonly=\"readonly\" /></td><td><input type=\"hidden\" id=\"deviceId\" name=\"deviceId\" value=\"" + deviceId + \
                              "\"/><input type=\"hidden\" id=\"templateId\" name=\"templateId\" value=\"0\"/></td></tr>"
            templateString += "<tr><td>Profile Name</td><td><input type=\"text\" id=\"templateName\" name=\"templateName\" value=\"" + \
                              deviceName + " Profile" + "\"/></td><td></td></tr>"
            templateString += "</table>"
            ################################## Tamplate Tabs #########################
            templateString += "<div class=\"tab-yo\" style=\"margin:10px 0px 15px;\">"
            templateString += "<div class=\"tab-head\">"
            templateString += "<a id=\"networkButton\" href=\"#networkDiv\" class=\"tab-active\" vap=\"0\">Network"
            templateString += "</a>"
            templateString += "<a id=\"radioButton\" href=\"#radioDiv\" class=\"tab-button\" vap=\"0\">Radio"
            templateString += "</a>"
            templateString += "<a id=\"vapButton\" href=\"#vapDiv\" class=\"tab-button\" vap=\"1\">VAP Config"
            templateString += "</a>"
            templateString += "<a id=\"aclButton\" href=\"#aclDiv\" class=\"tab-button\" vap=\"1\">ACL"
            templateString += "</a>"
            templateString += "<a id=\"servicesButton\" href=\"#servicesDiv\" class=\"tab-button\" vap=\"0\">Services"
            templateString += "</a>"
            templateString += "<h2>"
            templateString += "</h2>"
            templateString += "</div>"
            templateString += "<div id=\"networkDiv\" class=\"tab-body\" style=\"display:block;\">"
            templateString += apNetworkTab(
                tDom.getElementsByTagName("network")[0])
            templateString += "</div>"
            templateString += "<div id=\"radioDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apRadioTab(tDom.getElementsByTagName("radio")[0])
            templateString += "</div>"
            templateString += "<div id=\"vapDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apVapTab(tDom.getElementsByTagName("vap")[0])
            templateString += "</div>"
            templateString += "<div id=\"aclDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apAclTab(tDom.getElementsByTagName("acl")[0])
            templateString += "</div>"
            templateString += "<div id=\"servicesDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apServicesTab(
                tDom.getElementsByTagName("services")[0])
            templateString += "</div>"
            templateString += "<div id=\"msgDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += "<div style=\"padding:20px; width:100%; text-align:center;\"> Please select any Startup Mode under Radio tab.</div>"
            templateString += "</div>"
            templateString += "</div>"
            templateString += "<div style=\"padding:10px 20px 10px 0px;\"><input type=\"submit\" value=\"Add Profile\"/> <input type=\"button\" value=\"Cancel\" onclick=\"cancelAddProfile();\" /></div>"
            ################################ End Tamplate Tabs #######################
            templateString += "</form></div>"
    if i == 0:
        templateString = "<div style=\"display:block;width:100%; text-align:center;margin:10px;\">No Configuration Profile for this device</div>"
    html.write(templateString)


def edit_configuration_template(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    templateId = html.var("templateId")

    # load device configuration template form configurationTemplate.xml file
    deviceTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplate.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString(
        "<configurationTemplate></configurationTemplate>")
    if (os.path.isfile(deviceTemplateFile)):
        dom = xml.dom.minidom.parse(deviceTemplateFile)
    templateDom = dom.getElementsByTagName("template")
    templateString = ""
    for tDom in templateDom:
        if tDom.getAttribute("id") == templateId:
            templateString += "<div style=\"margin: 20px;\"><form action=\"create_config_tamplate.py\" method=\"post\" id=\"createTemplate\">"
            templateString += "<table width=\"100%\">"
            templateString += "<colgroup><col width='20%'/><col width='40%'/><col width=\"40%\"></colgroup>"
            templateString += "<tr><td>Device Name</td><td><input type=\"text\" id=\"deviceName\" name=\"deviceName\" value=\"" + tDom.getAttribute(
                "deviceName") + "\" readonly=\"readonly\" /></td><td><input type=\"hidden\" id=\"templateId\" name=\"templateId\" value=\"" + tDom.getAttribute(
                "id") + "\"/><input type=\"hidden\" id=\"deviceId\" name=\"deviceId\" value=\"" + tDom.getAttribute(
                "deviceId") + "\"/></td></tr>"
            templateString += "<tr><td>Profile Name</td><td><input type=\"text\" id=\"templateName\" name=\"templateName\" value=\"" + \
                              tDom.getAttribute("name") + "\"/></td><td></td></tr>"
            templateString += "</table>"
            ################################## Tamplate Tabs #########################
            templateString += "<div class=\"tab-yo\" style=\"margin:10px 0px 15px;\">"
            templateString += "<div class=\"tab-head\">"
            templateString += "<a id=\"networkButton\" href=\"#networkDiv\" class=\"tab-active\" vap=\"0\">Network"
            templateString += "</a>"
            templateString += "<a id=\"radioButton\" href=\"#radioDiv\" class=\"tab-button\" vap=\"0\">Radio"
            templateString += "</a>"
            templateString += "<a id=\"vapButton\" href=\"#vapDiv\" class=\"tab-button\" vap=\"1\">VAP Config"
            templateString += "</a>"
            templateString += "<a id=\"aclButton\" href=\"#aclDiv\" class=\"tab-button\" vap=\"1\">ACL"
            templateString += "</a>"
            templateString += "<a id=\"servicesButton\" href=\"#servicesDiv\" class=\"tab-button\" vap=\"0\">Services"
            templateString += "</a>"
            templateString += "<h2>"
            templateString += "</h2>"
            templateString += "</div>"
            templateString += "<div id=\"networkDiv\" class=\"tab-body\" style=\"display:block;\">"
            templateString += apNetworkTab(
                tDom.getElementsByTagName("network")[0])
            templateString += "</div>"
            templateString += "<div id=\"radioDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apRadioTab(tDom.getElementsByTagName("radio")[0])
            templateString += "</div>"
            templateString += "<div id=\"vapDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apVapTab(tDom.getElementsByTagName("vap")[0])
            templateString += "</div>"
            templateString += "<div id=\"aclDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apAclTab(tDom.getElementsByTagName("acl")[0])
            templateString += "</div>"
            templateString += "<div id=\"servicesDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += apServicesTab(
                tDom.getElementsByTagName("services")[0])
            templateString += "</div>"
            templateString += "<div id=\"msgDiv\" class=\"tab-body\" style=\"display:none;\">"
            templateString += "<div style=\"padding:20px; width:100%; text-align:center;\"> Please select any Startup Mode under Radio tab.</div>"
            templateString += "</div>"
            templateString += "</div>"
            templateString += "<div style=\"padding:10px 20px 10px 0px;\"><input type=\"submit\" value=\"Edit Profile\"/> <input type=\"button\" value=\"Cancel\" onclick=\"cancelEditProfile();\" /></div>"
            ################################ End Tamplate Tabs #######################
            templateString += "</form></div>"
    html.write(templateString)


def delete_configuration_template(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    templateId = html.var("templateId")

    # load device configuration template form configurationTemplate.xml file
    deviceTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplate.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString(
        "<configurationTemplate></configurationTemplate>")
    if (os.path.isfile(deviceTemplateFile)):
        dom = xml.dom.minidom.parse(deviceTemplateFile)
    templateDom = dom.getElementsByTagName("template")
    for tDom in templateDom:
        if tDom.getAttribute("id") == templateId:
            dom.getElementsByTagName(
                "configurationTemplate")[0].removeChild(tDom)
            break
    fwxml = open(deviceTemplateFile, "w")
    fwxml.write(dom.toxml())
    fwxml.close()
    html.write("0")


def apNetworkTab(networkDom):
    """

    @param networkDom:
    @return:
    """
    AP_HOSTNAME = networkDom.getAttribute("AP_HOSTNAME")
    AP_NETMASK = networkDom.getAttribute("AP_NETMASK")
    WAN_MODE = networkDom.getAttribute("WAN_MODE")
    IPGW = networkDom.getAttribute("IPGW")
    PRIDNS = networkDom.getAttribute("PRIDNS")
    SECDNS = networkDom.getAttribute("SECDNS")
    tableString = """<table style=\"padding:20px;width:100%\">
			<colgroup><col width='20%'/><col width='80%'/></colgroup>
			<tbody>
				<tr>
					<td>AP Host Name</td>
					<td><input type="text" value=\"""" + AP_HOSTNAME + """\" maxlength="16" name="AP_HOSTNAME" id="AP_HOSTNAME"></td>
				</tr>
				<tr><td colspan="2">&nbsp;</td></tr>
				<tr><td colspan="2"><b>Local Area Network  settings</b></td></tr>
				<tr style="display:none;">
					<td>Local IP Addr</td>
					<td><input type="text" maxlength="16" name="AP_IPADDR" id="AP_IPADDR"> </td>
				</tr>
				<tr>
					<td>Local Netmask</td>
					<td><input type="text" value=\"""" + AP_NETMASK + """\" maxlength="16" name="AP_NETMASK" id="AP_NETMASK" onkeypress="return IPKeyCheck(event)" onblur="checkIp(2,'AP_NETMASK','Netmask')"></td>
					<input type="hidden" value=\"""" + WAN_MODE + """\" id="WAN_MODE" name="WAN_MODE" />
				</tr>
				<tr>
					<td>Gateway IP</td>
					<td><input type="text" value=\"""" + IPGW + """\" maxlength="16" name="IPGW" id="IPGW" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(1,'IPGW','GatewayIP')"></td>
				</tr>
				<tr>
					<td>Primary DNS</td>
					<td><input type="text" value=\"""" + PRIDNS + """\" maxlength="16" name="PRIDNS" id="PRIDNS" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(3,'PRIDNS','PrimaryDNS')"></td>
				</tr>
				<tr>
					<td>Secondary DNS</td>
					<td><input type="text" value=\"""" + SECDNS + """\" maxlength="16" name="SECDNS" id="SECDNS" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(3,'SECDNS','SecondaryDNS')"></td>
				</tr>
			</tbody>
	</table>"""
    return tableString


def apRadioTab(radioDom):
    """

    @param radioDom:
    @return:
    """
    tableString = """
	<table style=\"padding:20px;width:100%\">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>Startup Mode<input type="hidden" id="startmode_hd" name="startmode_hd" value=\"""" + radioDom.getAttribute(
        "AP_STARTMODE") + """\" /></td>
				<td>
<input type="radio" id="startup_standard" onclick="ToggleMVlan(false)" value="standard" name="AP_STARTMODE"> Standard&nbsp;
<input type="radio" id="startup_rootap" onclick="ToggleMVlan(false)" value="rootap" name="AP_STARTMODE"> RootAP&nbsp;
<input type="radio" id="startup_repeater" onclick="ToggleMVlan(false)" value="repeater" name="AP_STARTMODE"> Repeater&nbsp;
<input type="radio" id="startup_client" onclick="ToggleMVlan(false)" value="client" name="AP_STARTMODE"> Client&nbsp;
<input type="radio" id="startup_multi" onclick="ToggleMVlan(false)" value="multi" name="AP_STARTMODE"> Multi AP&nbsp;
<input type="radio" id="startup_multivlan" onclick="ToggleMVlan(true)" value="multivlan" name="AP_STARTMODE"> Multi VLAN
				</td>
			</tr>
			<tr>
				<td colspan="2">
<div style="display: none; border: 2px solid grey; padding-left: 10px;" id="ManageVlan_tr">
	Management Vlan<input type="hidden" id="mngmtvlan_hd" name="mngmtvlan_hd" value=\"""" + radioDom.getAttribute(
        "MANAGEMENTVLAN") + """\" />
	<span style="padding-left: 30px;">
		<input type="radio" name="MANAGEMENTVLAN" checked="checked" value="1" onclick="ManageVlanPrompt(true)" id="Enbl_mngmtvlan"/>Enable
		<input type="radio" name="MANAGEMENTVLAN" value="0" onclick="ManageVlanPrompt(false)" id="Dsbl_mngmtvlan">Disable
		<br>
		<span style="color: black; font-size: 14px;">[
			<span style="color: red;">Caution:</span>
			If you Enable the Management VLAN You may lose the connectivity to Access Point throught ethernet.
			<br>
			Verify that packet coming from ethernet has same managment tag for connectivity.]
		</span>
	</span>
</div>
				</td>
			</tr>
			<tr>
				<td>Country <input type="hidden" id="countrycode_hd" name="countrycode_hd" value=\"""" + radioDom.getAttribute(
        "ATH_countrycode") + """\" /></td>
				<td>
					<select id="ATH_countrycode" name="ATH_countrycode">
						<option value="NA">DEFAULT </option>
						<option value="DB">DEBUG</option>
						<option value="AL">ALBANIA </option>
						<option value="DZ ">ALGERIA</option>
						<option value="AR">ARGENTINA</option>
						<option value="AM">ARMENIA</option>
						<option value="AU">AUSTRALIA</option>
						<option value="AT">AUSTRIA</option>
						<option value="AZ">AZERBAIJAN</option>
						<option value="BH">BAHRAIN</option>
						<option value="BY">BELARUS </option>
						<option value="BE">BELGIUM</option>
						<option value="BZ">BELIZE</option>
						<option value="BO">BOLIVIA</option>
						<option value="BA">BOSNIA_HERZEGOWINA </option>
						<option value="BR">BRAZIL</option>
						<option value="BN">BRUNEI_DARUSSALAM</option>
						<option value="BG">BULGARIA </option>
						<option value="CA">CANADA</option>
						<option value="CL">CHILE</option>
						<option value="CN">CHINA</option>
						<option value="CO">COLOMBIA</option>
						<option value="CR">COSTA_RICA</option>
						<option value="HR">CROATIA</option>
						<option value="CY">CYPRUS</option>
						<option value="CZ">CZECH</option>
						<option value="DK ">DENMARK</option>
						<option value="DO">DOMINICAN REPUBLIC </option>
						<option value="EC">ECUADOR</option>
						<option value="EG">EGYPT</option>
						<option value="SV">EL_SALVADOR</option>
						<option value="EE">ESTONIA</option>
						<option value="">FAEROE_ISLANDS</option>
						<option value="FI">FINLAND</option>
						<option value="FR">FRANCE</option>
						<option value="GE">GEORGIA</option>
						<option value="DE">GERMANY</option>
						<option value="GR">GREECE</option>
						<option value="GT">GUATEMALA</option>
						<option value="HN">HONDURAS</option>
						<option value="HK">HONG KONG</option>
						<option value="HU">HUNGARY</option>
						<option value="IS">ICELAND</option>
						<option value="IN">INDIA</option>
						<option value="ID">INDONESIA</option>
						<option value="IR">IRAN</option>
						<option value="">IRAQ</option>
						<option value="IE">IRELAND</option>
						<option value="IL">ISRAEL</option>
						<option value="IT">ITALY</option>
						<option value="">JAMAICA</option>
						<option value="JP">JAPAN</option>
						<option value="JO">JORDAN</option>
						<option value="KZ">KAZAKHSTAN</option>
						<option value="KE">KENYA</option>
						<option value="KP">KOREA NORTH</option>
						<option value="KW">KUWAIT</option>
						<option value="LV">LATVIA</option>
						<option value="LB">LEBANON</option>
						<option value="LI">LIECHTENSTEIN</option>
						<option value="LT">LITHUANIA</option>
						<option value="LU">LUXEMBOURG</option>
						<option value="MO">MACAU</option>
						<option value="MK">MACEDONIA</option>
						<option value="MY">MALAYSIA</option>
						<option value="">MALTA</option>
						<option value="MX">MEXICO</option>
						<option value="MC">MONACO</option>
						<option value="MA">MOROCCO</option>
						<option value="NL">NETHERLANDS</option>
						<option value="NZ">NEW ZEALAND</option>
						<option value="">NICARAGUA</option>
						<option value="NO">NORWAY</option>
						<option value="OM">OMAN</option>
						<option value="PK">PAKISTAN</option>
						<option value="PA">PANAMA</option>
						<option value="">PARAGUAY</option>
						<option value="PE">PERU</option>
						<option value="PH">PHILIPPINES</option>
						<option value="PL">POLAND</option>
						<option value="PT">PORTUGAL</option>
						<option value="PR">PUERTO_RICO</option>
						<option value="QA">QATAR</option>
						<option value="RO">ROMANIA</option>
						<option value="RU">RUSSIA</option>
						<option value="SA">SAUDI ARABIA</option>
						<option value="">SERBIA MONTENEGRO</option>
						<option value="SG">SINGAPORE</option>
						<option value="SK">SLOVAKIA</option>
						<option value="SI">SLOVENIA</option>
						<option value="ZA">SOUTH AFRICA</option>
						<option value="ES">SPAIN</option>
						<option value="LK">SRI LANKA</option>
						<option value="SE">SWEDEN</option>
						<option value="CH">SWITZERLAND</option>
						<option value="SY">SYRIA</option>
						<option value="TW">TAIWAN</option>
						<option value="TH">THAILAND</option>
						<option value="TT">TRINIDAD Y TOBAGO</option>
						<option value="TN">TUNISIA</option>
						<option value="TR">TURKEY</option>
						<option value="AE">UAE</option>
						<option value="UA">UKRAINE</option>
						<option value="GB">UNITED KINGDOM</option>
						<option value="US">UNITED STATES</option>
						<option value="UY">URUGUAY</option>
						<option value="UZ">UZBEKISTAN</option>
						<option value="VE">VENEZUELA</option>
						<option value="VN">VIET NAM</option>
						<option value="YE">YEMEN</option>
						<option value="ZW">ZIMBABWE</option>
					</select>
				</td>
			</tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr><td colspan="2"><b>Radio 1 (2.4 GHz)</b></td></tr>
			<tr>
				<td>Number of VAP's</td>
				<td>
					<input type="hidden" id="HID_AP_MAX_VAP" name="HID_AP_MAX_VAP" value=\"""" + radioDom.getAttribute(
        "AP_MAX_VAP") + """\"/>
					<select id="NoofVaps" name="AP_MAX_VAP" class="text2" disabled="" onchange="selectNoOfVap()">
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
						<option value="4">4</option>
						<option value="5">5</option>
						<option value="6">6</option>
						<option value="7">7</option>
						<option value="8">8</option>
					</select>
				</td>
			</tr>
			<tr>
				<td>Channel<input type="hidden" id="HID_AP_Channel" name="HID_AP_Channel" value=\"""" + radioDom.getAttribute(
        "AP_PRIMARY_CH") + """\"/></td>
				<td>
					<select id="AP_Channel" name="AP_PRIMARY_CH">
						<option value="1">Channel-1:2.412GHz</option>
						<option value="2">Channel-2:2.417GHz</option>
						<option value="3">Channel-3:2.422GHz</option>
						<option value="4">Channel-4:2.427GHz</option>
						<option value="5">Channel-5:2.432GHz</option>
						<option value="6">Channel-6:2.437GHz</option>
						<option value="7">Channel-7:2.442GHz</option>
						<option value="8">Channel-8:2.447GHz</option>
						<option value="9">Channel-9:2.452GHz</option>
						<option value="10">Channel-10:2.457GHz</option>
						<option value="11">Channel-11:2.462GHz</option>
						<option value="12">Channel-12:2.467GHz</option>
						<option value="13">Channel-13:2.472GHz</option>
					</select>
				</td>
			</tr>
			<tr>
				<td>Mode<input type="hidden" id="HID_AP_CHMODE" name="HID_AP_CHMODE" value=\"""" + radioDom.getAttribute(
        "AP_CHMODE") + """\"/></td>
				<td>
					<select id="AP_CHMODE" name="AP_CHMODE" class="text2">
						<option value="11G">WiFi 11g</option>
						<option value="11NGHT20">WiFi 11gn HT20</option>
						<option value="11NGHT40PLUS">WiFi 11gn HT40+</option>
						<option value="11NGHT40MINUS">WiFi 11gn HT40-</option>
					</select>
				</td>
			</tr>
			<tr>
				<td>Tx Power<input type="hidden" id="HID_AP_TXPOWER" name="HID_AP_TXPOWER" value=\"""" + radioDom.getAttribute(
        "AP_TXPOWER") + """\"/></td>
				<td>
					<select id="AP_TXPOWER" name="AP_TXPOWER" class="text2">
						<option value="">Default</option>
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
						<option value="4">4</option>
						<option value="5">5</option>
						<option value="6">6</option>
						<option value="7">7</option>
						<option value="8">8</option>
						<option value="9">9</option>
						<option value="10">10</option>
						<option value="11">11</option>
						<option value="12">12</option>
						<option value="13">13</option>
						<option value="14">14</option>
						<option value="15">15</option>
						<option value="16">16</option>
						<option value="17">17</option>
						<option value="18">18</option>
						<option value="19">19</option>
						<option value="20">20</option>
						<option value="21">21</option>
						<option value="22">22</option>
						<option value="23">23</option>
						<option value="24">24</option>
						<option value="25">25</option>
						<option value="26">26</option>
						<option value="27">27</option>
						<option value="28">28</option>
						<option value="29">29</option>
						<option value="30">30</option>
					</select>dBm
				</td>
			</tr>
			<tr>
				<td colspan="2">
				   <div id="Distance_auto" style="display: none;">
					Distance
					<span style="padding-left: 120px;"></span>
					<input type="text" class="text2" id="Distance" name="AP_DISTANCE" value=\"""" + radioDom.getAttribute(
        "AP_DISTANCE") + """\" /> &nbsp;&nbsp;
				   </div>
				   <div id="Distance_manual" style="display: none;">
					Slot Time
					<span style="padding-left: 110px;"></span>
					<input class="text2" value=\"""" + radioDom.getAttribute("AP_SLOTTIME") + """\" name="AP_SLOTTIME" tpe="text"/>
					<br>
					ACK Timeout
					<span style="padding-left: 92px;"></span>
					<input type="text" class="text2" value=\"""" + radioDom.getAttribute("AP_ACKTIMEOUT") + """\" name="AP_ACKTIMEOUT"/>
					<br>
					CTS TimeOut<span style="padding-left: 92px;"></span>
					<input type="text" class="text2" value=\"""" + radioDom.getAttribute("AP_CTSTIMEOUT") + """\" name="AP_CTSTIMEOUT">
					<br>
				   <div>
				</td>
			</tr>
			<tr>
				<td>Gating Index<input type="hidden" id="HID_SHORTGI" name="HID_SHORTGI" value=\"""" + radioDom.getAttribute(
        "SHORTGI") + """\"/></td>
				<td>
					<input type="radio" id="SHORTGI_1" value="1" name="SHORTGI"> Half&nbsp;
					<input type="radio" id="SHORTGI_0" value="0" name="SHORTGI"> Full&nbsp;
				</td>
			</tr>
			<tr>
				<td>Aggregation<input type="hidden" id="HID_AMPDUENABLE" name="HID_AMPDUENABLE" value=\"""" + radioDom.getAttribute(
        "AMPDUENABLE") + """\"/></td>
				<td>
					<input type="radio" onclick="SwapAggregation(true)" id="chk_AMPDU_Enable" value="1" name="AMPDUENABLE"> Enabled&nbsp;
					<input type="radio" onclick="SwapAggregation(false)" id="chk_AMPDU_Disable" value="0" name="AMPDUENABLE"> Disabled&nbsp;
				</td>
			</tr>
			<tr>
				<td>Agg Frames</td>
				<td>
					<input type="text" value=\"""" + radioDom.getAttribute("AMPDUFRAMES") + """\" maxlength="16" name="AMPDUFRAMES" id="AMPDUFRAMES" onkeypress="return numCheck(event)" >
				</td>
			</tr>
			<tr>
				<td>Agg Size</td>
				<td>
					<input type="text" value=\"""" + radioDom.getAttribute("AMPDULIMIT") + """\" maxlength="16" name="AMPDULIMIT" id="AMPDULIMIT" onkeypress="return numCheck(event)" >
				</td>
			</tr>
			<tr>
				<td>Agg Min Size</td>
				<td>
					<input type="text" value=\"""" + radioDom.getAttribute("AMPDUMIN") + """\" maxlength="16" name="AMPDUMIN" id="AMPDUMIN" onkeypress="return numCheck(event)" >
				</td>
			</tr>
			<tr>
				<td>Channel Width<input type="hidden" id="HID_CWMMODE" name="HID_CWMMODE" value=\"""" + radioDom.getAttribute(
        "CWMMODE") + """\"/></td>
				<td>
					<input type="radio" id="CWMMODE_0" value="0" name="CWMMODE"> HT20&nbsp;
					<input type="radio" id="CWMMODE_1" value="1" name="CWMMODE"> HT20/40&nbsp;
				</td>
			</tr>
			<tr>
				<td>TX ChainMask<input type="hidden" id="HID_TX_CHAINMASK" name="HID_TX_CHAINMASK" value=\"""" + radioDom.getAttribute(
        "TX_CHAINMASK") + """\"/></td>
				<td>
					<input type="radio" value="1" name="TX_CHAINMASK" id="TX_CHAINMASK_1"> 1 Chain
					<input type="radio" value="3" name="TX_CHAINMASK" id="TX_CHAINMASK_3"> 2 Chain
					<input type="radio" value="0" name="TX_CHAINMASK" id="TX_CHAINMASK_0"> EEPROM
				</td>
			</tr>
			<tr>
				<td>RX ChainMask<input type="hidden" id="HID_RX_CHAINMASK" name="HID_RX_CHAINMASK" value=\"""" + radioDom.getAttribute(
        "RX_CHAINMASK") + """\"/></td>
				<td>
					<input type="radio" value="1" id="RX_CHAINMASK_1" name="RX_CHAINMASK"> 1 Chain
					<input type="radio" value="3" id="RX_CHAINMASK_3" name="RX_CHAINMASK"> 2 Chain
					<input type="radio" value="0" id="RX_CHAINMASK_0" name="RX_CHAINMASK"> EEPROM

					<input type="hidden" name="AP_LONGDISTANCE"  value=\"""" + radioDom.getAttribute(
        "AP_LONGDISTANCE") + """\" >
					<input type="hidden" name="WLAN_ON_BOOT"  value=\"""" + radioDom.getAttribute("WLAN_ON_BOOT") + """\" >
					<input type="hidden" name="AP_RADIO_ID"  value=\"""" + radioDom.getAttribute("AP_RADIO_ID") + """\" >
					<input type="hidden" name="PUREG"  value=\"""" + radioDom.getAttribute("PUREG") + """\" >
					<input type="hidden" name="PUREN"  value=\"""" + radioDom.getAttribute("PUREN") + """\" >
					<input type="hidden" name="TXQUEUELEN"  value=\"""" + radioDom.getAttribute("TXQUEUELEN") + """\" >
					<input type="hidden" name="RATECTL"  value=\"""" + radioDom.getAttribute("RATECTL") + """\" >
					<input type="hidden" name="MANRATE"  value=\"""" + radioDom.getAttribute("MANRATE") + """\" >
					<input type="hidden" name="MANRETRIES"  value=\"""" + radioDom.getAttribute("MANRETRIES") + """\" >
					<input type="hidden" name="AP_BEAC_INT"  value=\"""" + radioDom.getAttribute("AP_BEAC_INT") + """\" >
					<input type="hidden" name="APM_Enable"  value=\"""" + radioDom.getAttribute("APM_Enable") + """\" >
				</td>
			</tr>
		</tbody>
	</table>"""
    return tableString


def apVapTab(vapDom):
    """

    @param vapDom:
    @return:
    """
    tableString = """
	<table style="padding: 20px 20px 0px 20px; width: 100%;">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>Select VAP</td>
				<td>
					<select id="vap_vap" name="vap_vap" onchange="vapVap()">
						<option value="1">VAP 1</option>
						<option value="2">VAP 2</option>
						<option value="3">VAP 3</option>
						<option value="4">VAP 4</option>
						<option value="5">VAP 5</option>
						<option value="6">VAP 6</option>
						<option value="7">VAP 7</option>
						<option value="8">VAP 8</option>
					</select>
				</td>
			</tr>
			<tr>
				<td colspan="2" id="vapMsg" style="font-weight:bold;"></td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_1" value=\"""" + vapDom.getAttribute("AP_MODE") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;" id="vap_vap1_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID") + """\" maxlength="32" name="AP_SSID" id="AP_SSID_1">&nbsp;&nbsp;
					<span id="hidessid_div_1">Hide Essid <input type="checkbox" onclick="Toggle_ssid('1')" id="HIDE_SSID_1" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID") + """\"></span>
					<input type="hidden" name="HIDE_SSID" id="hdn_ssid_1" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_1">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN") + """\" maxlength="5" name="AP_VLAN" id="AP_VLAN_1" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI") + """\" maxlength="1" name="VLAN_PRI" id="VLAN_PRI_1" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_1">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE" id="ap_mode_ap_1">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE" id="ap_mode_ap_wds_1">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div style="display: none;" id="Mac_opt">Root AP Mac Address&nbsp;&nbsp;
						<input type="text" maxlength="32" name="ROOTAP_MAC" id="ROOTAP_MAC" value=\"""" + vapDom.getAttribute(
        "ROOTAP_MAC") + """\">
					</div>
				</td>
			</tr>
			<tr>
				<td>Enable Dynamic Vlan </td>
				<td>
					<input type="checkbox" onclick="Toggle_Dynvlan()" id="chk_dyn_vlan">
					(Dymamic VLAN can be Enabled in RootAP,Standard mode With Enterprise/Radius Support.)
					<input type="hidden" value=\"""" + vapDom.getAttribute("AP_DYN_VLAN") + """\" id="dyn_vlan" name="AP_DYN_VLAN">
				</td>
			</tr>

			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode1" onchange="modeChange('rts',1)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr1" onblur="checkThr('rts',1)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR" id="hdn_rts_thr1" value=\"""" + vapDom.getAttribute("AP_RTS_THR") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode1" onchange="modeChange('frag',1)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr1" onblur="checkThr('frag',1)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR" id="hdn_frag_thr1" value=\"""" + vapDom.getAttribute("AP_FRAG_THR") + """\" type="hidden">
				</td>
			</tr>

			<tr id="beacon_row">
				<td>Beacon Interval</td>
				<td>
					<input name="AP_BEAC_INT" id="beacon_int" value=\"""" + vapDom.getAttribute("AP_BEAC_INT") + """\" onkeypress="return numCheck(event)" style="width: 65px;" type="text">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_2" value=\"""" + vapDom.getAttribute("AP_MODE_2") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap2_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" maxlength="32" name="AP_SSID_2" id="AP_SSID_2" value=\"""" + vapDom.getAttribute(
        "AP_SSID_2") + """\">&nbsp;&nbsp;
					<span id="hidessid_div_2">Hide Essid <input type="checkbox" onclick="Toggle_ssid('2')" id="HIDE_SSID_2"></span>
					<input type="hidden" name="HIDE_SSID_2" id="hdn_ssid_2" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_2") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_2">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_2") + """\" maxlength="5" name="AP_VLAN_2" id="AP_VLAN_2" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_2") + """\" maxlength="1" name="VLAN_PRI_2" id="VLAN_PRI_2" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_2">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_2" id="ap_mode_ap_2">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_2" id="ap_mode_ap_wds_2">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div style="display: none;" id="Mac_opt2">
					</div>
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode2" onchange="modeChange('rts',2)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr2" onblur="checkThr('rts',2)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_2" id="hdn_rts_thr2" value=\"""" + vapDom.getAttribute("AP_RTS_THR_2") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode2" onchange="modeChange('frag',2)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr2" onblur="checkThr('frag',2)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_2" id="hdn_frag_thr2" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_2") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_3" value=\"""" + vapDom.getAttribute("AP_MODE_3") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap3_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID_3") + """\" maxlength="32" name="AP_SSID_3" id="AP_SSID_3">&nbsp;&nbsp;
					Hide Essid <input type="checkbox" onclick="Toggle_ssid('3')" id="HIDE_SSID_3">
					<input type="hidden" name="HIDE_SSID_3" id="hdn_ssid_3" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_3") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_3">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_3") + """\" maxlength="5" name="AP_VLAN_3" id="AP_VLAN_3" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_3") + """\" maxlength="1" name="VLAN_PRI_3" id="VLAN_PRI_3" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_3">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_3" id="ap_mode_ap_3">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_3" id="ap_mode_ap_wds_3">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode3" onchange="modeChange('rts',3)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr3" onblur="checkThr('rts',3)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_3" id="hdn_rts_thr3" value=\"""" + vapDom.getAttribute("AP_RTS_THR_3") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode3" onchange="modeChange('frag',3)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr3" onblur="checkThr('frag',3)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_3" id="hdn_frag_thr3" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_3") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_4" value=\"""" + vapDom.getAttribute("AP_MODE_4") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap4_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID_4") + """\" maxlength="32" name="AP_SSID_4" id="AP_SSID_4">&nbsp;&nbsp;
					Hide Essid <input type="checkbox" onclick="Toggle_ssid('4')" id="HIDE_SSID_4">
					<input type="hidden" name="HIDE_SSID_4" id="hdn_ssid_4" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_4") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_4">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_4") + """\" maxlength="5" name="AP_VLAN_4" id="AP_VLAN_4" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_4") + """\" maxlength="1" name="VLAN_PRI_4" id="VLAN_PRI_4" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_4">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_4" id="ap_mode_ap_4">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_4" id="ap_mode_ap_wds_4">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode4" onchange="modeChange('rts',4)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr4" onblur="checkThr('rts',4)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_4" id="hdn_rts_thr4" value=\"""" + vapDom.getAttribute("AP_RTS_THR_4") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode4" onchange="modeChange('frag',4)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr4" onblur="checkThr('frag',4)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_4" id="hdn_frag_thr4" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_4") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_5" value=\"""" + vapDom.getAttribute("AP_MODE_5") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap5_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID_5") + """\" maxlength="32" name="AP_SSID_5" id="AP_SSID_5">&nbsp;&nbsp;
					Hide Essid <input type="checkbox" onclick="Toggle_ssid('5')" id="HIDE_SSID_5">
					<input type="hidden" name="HIDE_SSID_5" id="hdn_ssid_5" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_5") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_5">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_5") + """\" maxlength="5" name="AP_VLAN_5" id="AP_VLAN_5" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_5") + """\" maxlength="1" name="VLAN_PRI_5" id="VLAN_PRI_5" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_5">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_5" id="ap_mode_ap_5">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_5" id="ap_mode_ap_wds_5">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode5" onchange="modeChange('rts',5)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr5" onblur="checkThr('rts',5)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_5" id="hdn_rts_thr5" value=\"""" + vapDom.getAttribute("AP_RTS_THR_5") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode5" onchange="modeChange('frag',5)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr5" onblur="checkThr('frag',5)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_5" id="hdn_frag_thr5" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_5") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_6" value=\"""" + vapDom.getAttribute("AP_MODE_6") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap6_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID_6") + """\" maxlength="32" name="AP_SSID_6" id="AP_SSID_6">&nbsp;&nbsp;
					Hide Essid <input type="checkbox" onclick="Toggle_ssid('6')" id="HIDE_SSID_6">
					<input type="hidden" name="HIDE_SSID_6" id="hdn_ssid_6" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_6") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_6">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_6") + """\" maxlength="5" name="AP_VLAN_6" id="AP_VLAN_6" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_6") + """\" maxlength="1" name="VLAN_PRI_6" id="VLAN_PRI_6" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_6">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_6" id="ap_mode_ap_6">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_6" id="ap_mode_ap_wds_6">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode6" onchange="modeChange('rts',6)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr6" onblur="checkThr('rts',6)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_6" id="hdn_rts_thr6" value=\"""" + vapDom.getAttribute("AP_RTS_THR_6") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode6" onchange="modeChange('frag',6)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr6" onblur="checkThr('frag',6)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_6" id="hdn_frag_thr6" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_6") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_7" value=\"""" + vapDom.getAttribute("AP_MODE_7") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap7_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID_7") + """\" maxlength="32" name="AP_SSID_7" id="AP_SSID_7">&nbsp;&nbsp;
					Hide Essid <input type="checkbox" onclick="Toggle_ssid('7')" id="HIDE_SSID_7">
					<input type="hidden" name="HIDE_SSID_7" id="hdn_ssid_7" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_7") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_7">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_7") + """\" maxlength="5" name="AP_VLAN_7" id="AP_VLAN_7" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_7") + """\" maxlength="1" name="VLAN_PRI_7" id="VLAN_PRI_7" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_7">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_7" id="ap_mode_ap_7">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_7" id="ap_mode_ap_wds_7">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode7" onchange="modeChange('rts',7)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr7" onblur="checkThr('rts',7)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_7" id="hdn_rts_thr7" value=\"""" + vapDom.getAttribute("AP_RTS_THR_7") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode7" onchange="modeChange('frag',7)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr7" onblur="checkThr('frag',7)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_7" id="hdn_frag_thr7" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_7") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>

	<input type="hidden" id="HID_AP_MODE_8" value=\"""" + vapDom.getAttribute("AP_MODE_8") + """\">

	<table style="padding: 0px 20px 20px 20px; width: 100%;display:none;" id="vap_vap8_table1" class="vap-table">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td>ESSID String</td>
				<td>
					<input type="text" value=\"""" + vapDom.getAttribute("AP_SSID_8") + """\" maxlength="32" name="AP_SSID_8" id="AP_SSID_8">&nbsp;&nbsp;
					Hide Essid <input type="checkbox" onclick="Toggle_ssid('8')" id="HIDE_SSID_8">
					<input type="hidden" name="HIDE_SSID_8" id="hdn_ssid_8" value=\"""" + vapDom.getAttribute(
        "HIDE_SSID_8") + """\">
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<div id="MultiVlan_opt_8">
						VLAN ID
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("AP_VLAN_8") + """\" maxlength="5" name="AP_VLAN_8" id="AP_VLAN_8" onkeypress="return numCheck(event)">
						&nbsp;&nbsp;&nbsp;
						VLAN PRIORITY
						&nbsp;&nbsp;&nbsp;
						<input type="text" value=\"""" + vapDom.getAttribute("VLAN_PRI_8") + """\" maxlength="1" name="VLAN_PRI_8" id="VLAN_PRI_8" onkeypress="return numCheck(event)">
					</div>
				</td>
			</tr>
			<tr id="MultiVapmod_opt_8">
				<td>VAP Mode</td>
				<td>
					<input type="radio" value="ap" checked="checked" name="AP_MODE_8" id="ap_mode_ap_8">Access Point&nbsp;
					<input type="radio" value="ap-wds" name="AP_MODE_8" id="ap_mode_ap_wds_8">WDS Access Point&nbsp;
				</td>
			</tr>
			<tr>
				<td>RTS Threshold</td>
				<td>
					<select id="rts_mode8" onchange="modeChange('rts',8)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display: none; width: 80px;" id="txt_rts_thr8" onblur="checkThr('rts',8)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_RTS_THR_8" id="hdn_rts_thr8" value=\"""" + vapDom.getAttribute("AP_RTS_THR_8") + """\" type="hidden">
				</td>
			</tr>
			<tr>
				<td>Fragmenation Threshold</td>
				<td>
					<select id="frag_mode8" onchange="modeChange('frag',8)">
						<option value="0">Off</option>
						<!--<option value='1'>Auto</option> -->
						<option value="2">Fixed</option>
					</select> &nbsp;
					<input style="display:none; width: 80px;" id="txt_frag_thr8" onblur="checkThr('frag',8)" onkeypress="return numCheck(event)" type="text">
					<input name="AP_FRAG_THR_8" id="hdn_frag_thr8" value=\"""" + vapDom.getAttribute("AP_FRAG_THR_8") + """\" type="hidden">
				</td>
			</tr>
		</tbody>
	</table>


	<!-- vap 1 table 2 -->
	<input type="hidden" id="HID_AP_SECMODE_1" value=\"""" + vapDom.getAttribute("AP_SECMODE") + """\">
	<input type="hidden" id="HID_AP_WEP_MODE_0" value=\"""" + vapDom.getAttribute("AP_WEP_MODE_0") + """\">
	<input type="hidden" id="HID_WEPKEY_1" value=\"""" + vapDom.getAttribute("WEPKEY_1") + """\">
	<input type="hidden" id="HID_WEPKEY_2" value=\"""" + vapDom.getAttribute("WEPKEY_2") + """\">
	<input type="hidden" id="HID_WEPKEY_3" value=\"""" + vapDom.getAttribute("WEPKEY_3") + """\">
	<input type="hidden" id="HID_WEPKEY_4" value=\"""" + vapDom.getAttribute("WEPKEY_4") + """\">
	<input type="hidden" id="HID_AP_PRIMARY_KEY_0" value=\"""" + vapDom.getAttribute("AP_PRIMARY_KEY_0") + """\">
	<input type="hidden" id="HID_AP_WPA_1" value=\"""" + vapDom.getAttribute("AP_WPA") + """\">
	<input type="hidden" id="HID_AP_CYPHER_1" value=\"""" + vapDom.getAttribute("AP_CYPHER") + """\">
	<input type="hidden" id="HID_AP_SECFILE_1" value=\"""" + vapDom.getAttribute("AP_SECFILE") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_1" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH") + """\">

	<table style="padding: 20px; width: 100%;"  id="vap_vap1_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_1" onclick="displayData(1,'1')" value="None" name="AP_SECMODE">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div class="hide" id="open_div_1" style="display: none;">
						<span style="padding-left: 65px;" class="headerBLK">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="display: block;" id="wepdiv_1">
						<input type="radio" id="sec_wep_1" onclick="displayData(2,'1')" value="WEP" name="AP_SECMODE">
						WEP
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: none;" class="hide" id="WEP_div_1">

					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_1" onclick="displayData(3,'1')" value="WPA" checked="checked" name="AP_SECMODE">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" class="hide" id="WPA_div_1">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_1" onclick="EnableEnterprise('1')" value="0" name="AP_WPA"> 										802.1x&nbsp;
										<input type="radio" id="secwpa_1" onclick="AlterEnterprise('1')" value="1" name="AP_WPA">WPA&nbsp;
										<input type="radio" id="secwpa2_1" onclick="AlterEnterprise('1')" value="2" name="AP_WPA">WPA 2&nbsp;
										<input type="radio" id="secauto_1" onclick="AlterEnterprise('1')" value="3" name="AP_WPA"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_1" value="CCMP" checked="checked" name="AP_CYPHER">CCMP
										<span id="span_cypher_1" style="display: none;">
											<input type="radio" id="cypher_tkip_1" value="TKIP" name="AP_CYPHER">TKIP
											<input type="radio" id="cypher_tkip_ccmp_1" value="TKIP CCMP" name="AP_CYPHER">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY" id="AP_WPA_GROUP_REKEY_1">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY") + """\" maxlength="16" name="AP_WPA_GMK_REKEY" id="AP_WPA_GMK_REKEY_1">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY" id="AP_WEP_REKEY_1" value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('1')" id="chk_PersonalKey_1" value="PSK" checked="checked" name="AP_SECFILE" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('1')" value=\"""" + vapDom.getAttribute("PSK_KEY") + """\" maxlength="64" size="70" class="text2" name="PSK_KEY" id="PSK_KEY_1" disabled="">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('1')" id="chk_EnterpriseKey_1" value="EAP" name="AP_SECFILE">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_1" value="0" name="AP_RSN_ENA_PREAUTH">Disable
	<input type="radio" id="interface_enb_1" value="1" name="AP_RSN_ENA_PREAUTH">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF" id="AP_WPA_PREAUTH_IF_1" value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER" id="AP_EAP_REAUTH_PER_1" value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_1','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER" id="AP_AUTH_SERVER_1" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT" id="AP_AUTH_PORT_1" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET" id="AP_AUTH_SECRET_1" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>



	<!-- vap 2 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_2" value=\"""" + vapDom.getAttribute("AP_SECMODE_2") + """\">
	<input type="hidden" id="HID_AP_WPA_2" value=\"""" + vapDom.getAttribute("AP_WPA_2") + """\">
	<input type="hidden" id="HID_AP_CYPHER_2" value=\"""" + vapDom.getAttribute("AP_CYPHER_2") + """\">
	<input type="hidden" id="HID_AP_SECFILE_2" value=\"""" + vapDom.getAttribute("AP_SECFILE_2") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_2" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_2") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap2_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_2" onclick="displayData(1,'2')" value="None" name="AP_SECMODE_2">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div class="hide" id="open_div_2" style="display: none;">
						<span style="padding-left: 65px;" class="headerBLK">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="display: block;" id="wepdiv_2">
						<input type="radio" id="sec_wep_2" onclick="displayData(2,'2')" value="WEP" name="AP_SECMODE_2">
						WEP
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: none;" class="hide" id="WEP_div_2">

					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_2" onclick="displayData(3,'2')" value="WPA" checked="checked" name="AP_SECMODE_2">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_2">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_2" onclick="EnableEnterprise('2')" value="0" name="AP_WPA_2">802.1x&nbsp;
										<input type="radio" id="secwpa_2" onclick="AlterEnterprise('2')" value="1" checked="checked" name="AP_WPA_2">WPA&nbsp;
										<input type="radio" id="secwpa2_2" onclick="AlterEnterprise('2')" value="2" name="AP_WPA_2">WPA 2&nbsp;
										<input type="radio" id="secauto_2" onclick="AlterEnterprise('2')" value="3" name="AP_WPA_2"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_2" value="CCMP" checked="checked" name="AP_CYPHER_2">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_2" value="TKIP" name="AP_CYPHER_2">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_2" name="AP_CYPHER_2">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_2") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_2" id="AP_WPA_GROUP_REKEY_2">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_2") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_2" id="AP_WPA_GMK_REKEY_2">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_2" id="AP_WEP_REKEY_2" value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_2") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('2')" id="chk_PersonalKey_2" value="PSK" checked="checked" name="AP_SECFILE_2" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('2')" maxlength="64" name="PSK_KEY_2" id="PSK_KEY_2" disabled="" value=\"""" + vapDom.getAttribute(
        "PSK_KEY_2") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('2')" id="chk_EnterpriseKey_2" value="EAP" name="AP_SECFILE_2">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_2" value="0" name="AP_RSN_ENA_PREAUTH_2">Disable
	<input type="radio" id="interface_enb_2" value="1" name="AP_RSN_ENA_PREAUTH_2">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_2" id="AP_WPA_PREAUTH_IF_2" value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_2") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_2" id="AP_EAP_REAUTH_PER_2" value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_2") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_2','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_2" id="AP_AUTH_SERVER_2" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_2") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_2" id="AP_AUTH_PORT_2" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_2") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_2" id="AP_AUTH_SECRET_2" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_2") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

	<!-- vap 3 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_3" value=\"""" + vapDom.getAttribute("AP_SECMODE_3") + """\">
	<input type="hidden" id="HID_AP_WPA_3" value=\"""" + vapDom.getAttribute("AP_WPA_3") + """\">
	<input type="hidden" id="HID_AP_CYPHER_3" value=\"""" + vapDom.getAttribute("AP_CYPHER_3") + """\">
	<input type="hidden" id="HID_AP_SECFILE_3" value=\"""" + vapDom.getAttribute("AP_SECFILE_3") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_3" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_3") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap3_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_3" onclick="displayData(1,'3')" value="None" name="AP_SECMODE_3">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div class="hide" id="open_div_3" style="display: none;">
						<span style="padding-left: 65px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_3" onclick="displayData(3,'3')" value="WPA" checked="checked" name="AP_SECMODE_3">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_3">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_3" onclick="EnableEnterprise('3')" value="0" name="AP_WPA_3">802.1x&nbsp;
										<input type="radio" id="secwpa_3" onclick="AlterEnterprise('3')" value="1" checked="checked" name="AP_WPA_3">WPA&nbsp;
										<input type="radio" id="secwpa2_3" onclick="AlterEnterprise('3')" value="2" name="AP_WPA_3">WPA 2&nbsp;
										<input type="radio" id="secauto_3" onclick="AlterEnterprise('3')" value="3" name="AP_WPA_3"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_3" value="CCMP" checked="checked" name="AP_CYPHER_3">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_3" value="TKIP" name="AP_CYPHER_3">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_3" name="AP_CYPHER_3">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_3") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_3" id="AP_WPA_GROUP_REKEY_3">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_3") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_3" id="AP_WPA_GMK_REKEY_3">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_3" id="AP_WEP_REKEY_3" value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_3") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('3')" id="chk_PersonalKey_3" value="PSK" checked="checked" name="AP_SECFILE_3" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('3')" maxlength="64" name="PSK_KEY_3" id="PSK_KEY_3" disabled="" value=\"""" + vapDom.getAttribute(
        "PSK_KEY_3") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('3')" id="chk_EnterpriseKey_3" value="EAP" name="AP_SECFILE_3">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_3" value="0" name="AP_RSN_ENA_PREAUTH_3">Disable
	<input type="radio" id="interface_enb_3" value="1" name="AP_RSN_ENA_PREAUTH_3">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_3" id="AP_WPA_PREAUTH_IF_3" value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_3") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_3" id="AP_EAP_REAUTH_PER_3" value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_3") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_3','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_3" id="AP_AUTH_SERVER_3" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_3") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_3" id="AP_AUTH_PORT_3" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_3") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_3" id="AP_AUTH_SECRET_3" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_3") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

	<!-- vap 4 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_4" value=\"""" + vapDom.getAttribute("AP_SECMODE_4") + """\">
	<input type="hidden" id="HID_AP_WPA_4" value=\"""" + vapDom.getAttribute("AP_WPA_4") + """\">
	<input type="hidden" id="HID_AP_CYPHER_4" value=\"""" + vapDom.getAttribute("AP_CYPHER_4") + """\">
	<input type="hidden" id="HID_AP_SECFILE_4" value=\"""" + vapDom.getAttribute("AP_SECFILE_4") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_4" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_4") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap4_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_4" onclick="displayData(1,'4')" value="None" name="AP_SECMODE_4">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div id="open_div_4" style="display: none;">
						<span style="padding-left: 65px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_4" onclick="displayData(3,'4')" value="WPA" checked="checked" name="AP_SECMODE_4">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_4">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_4" onclick="EnableEnterprise('4')" value="0" name="AP_WPA_4">802.1x&nbsp;
										<input type="radio" id="secwpa_4" onclick="AlterEnterprise('4')" value="1" checked="checked" name="AP_WPA_4">WPA&nbsp;
										<input type="radio" id="secwpa2_4" onclick="AlterEnterprise('4')" value="2" name="AP_WPA_4">WPA 2&nbsp;
										<input type="radio" id="secauto_4" onclick="AlterEnterprise('4')" value="3" name="AP_WPA_4"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_4" value="CCMP" checked="checked" name="AP_CYPHER_4">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_4" value="TKIP" name="AP_CYPHER_4">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_4" name="AP_CYPHER_4">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)"  value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_4") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_4" id="AP_WPA_GROUP_REKEY_4">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)"  value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_4") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_4" id="AP_WPA_GMK_REKEY_4">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_4" id="AP_WEP_REKEY_4"  value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_4") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('4')" id="chk_PersonalKey_4" value="PSK" checked="checked" name="AP_SECFILE_4" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('4')" maxlength="64" name="PSK_KEY_4" id="PSK_KEY_4" disabled=""  value=\"""" + vapDom.getAttribute(
        "PSK_KEY_4") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('4')" id="chk_EnterpriseKey_4" value="EAP" name="AP_SECFILE_4">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_4" value="0" name="AP_RSN_ENA_PREAUTH_4">Disable
	<input type="radio" id="interface_enb_4" value="1" name="AP_RSN_ENA_PREAUTH_4">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_4" id="AP_WPA_PREAUTH_IF_4"  value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_4") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_4" id="AP_EAP_REAUTH_PER_4"  value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_4") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_4','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_4" id="AP_AUTH_SERVER_4"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_4") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_4" id="AP_AUTH_PORT_4"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_4") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_4" id="AP_AUTH_SECRET_4"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_4") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

	<!-- vap 5 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_5" value=\"""" + vapDom.getAttribute("AP_SECMODE_5") + """\">
	<input type="hidden" id="HID_AP_WPA_5" value=\"""" + vapDom.getAttribute("AP_WPA_5") + """\">
	<input type="hidden" id="HID_AP_CYPHER_5" value=\"""" + vapDom.getAttribute("AP_CYPHER_5") + """\">
	<input type="hidden" id="HID_AP_SECFILE_5" value=\"""" + vapDom.getAttribute("AP_SECFILE_5") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_5" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_5") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap5_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_5" onclick="displayData(1,'5')" value="None" name="AP_SECMODE_5">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div id="open_div_5" style="display: none;">
						<span style="padding-left: 65px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_5" onclick="displayData(3,'5')" value="WPA" checked="checked" name="AP_SECMODE_5">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_5">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_5" onclick="EnableEnterprise('5')" value="0" name="AP_WPA_5">802.1x&nbsp;
										<input type="radio" id="secwpa_5" onclick="AlterEnterprise('5')" value="1" checked="checked" name="AP_WPA_5">WPA&nbsp;
										<input type="radio" id="secwpa2_5" onclick="AlterEnterprise('5')" value="2" name="AP_WPA_5">WPA 2&nbsp;
										<input type="radio" id="secauto_5" onclick="AlterEnterprise('5')" value="3" name="AP_WPA_5"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_5" value="CCMP" checked="checked" name="AP_CYPHER_5">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_5" value="TKIP" name="AP_CYPHER_5">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_5" name="AP_CYPHER_5">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_5") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_5" id="AP_WPA_GROUP_REKEY_5">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)"  value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_5") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_5" id="AP_WPA_GMK_REKEY_5">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_5" id="AP_WEP_REKEY_5"  value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_5") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('5')" id="chk_PersonalKey_5" value="PSK" checked="checked" name="AP_SECFILE_5" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('5')" maxlength="64" name="PSK_KEY_5" id="PSK_KEY_5" disabled=""  value=\"""" + vapDom.getAttribute(
        "PSK_KEY_5") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('5')" id="chk_EnterpriseKey_5" value="EAP" name="AP_SECFILE_5">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_5" value="0" name="AP_RSN_ENA_PREAUTH_5">Disable
	<input type="radio" id="interface_enb_5" value="1" name="AP_RSN_ENA_PREAUTH_5">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_5" id="AP_WPA_PREAUTH_IF_5"  value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_5") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_5" id="AP_EAP_REAUTH_PER_5"  value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_5") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_5','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_5" id="AP_AUTH_SERVER_5"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_5") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_5" id="AP_AUTH_PORT_5"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_5") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_5" id="AP_AUTH_SECRET_5"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_5") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

	<!-- vap 6 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_6" value=\"""" + vapDom.getAttribute("AP_SECMODE_6") + """\">
	<input type="hidden" id="HID_AP_WPA_6" value=\"""" + vapDom.getAttribute("AP_WPA_6") + """\">
	<input type="hidden" id="HID_AP_CYPHER_6" value=\"""" + vapDom.getAttribute("AP_CYPHER_6") + """\">
	<input type="hidden" id="HID_AP_SECFILE_6" value=\"""" + vapDom.getAttribute("AP_SECFILE_6") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_6" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_6") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap6_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_6" onclick="displayData(1,'6')" value="None" name="AP_SECMODE_6">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div id="open_div_6" style="display: none;">
						<span style="padding-left: 65px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_6" onclick="displayData(3,'6')" value="WPA" checked="checked" name="AP_SECMODE_6">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_6">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_6" onclick="EnableEnterprise('6')" value="0" name="AP_WPA_6">802.1x&nbsp;
										<input type="radio" id="secwpa_6" onclick="AlterEnterprise('6')" value="1" checked="checked" name="AP_WPA_6">WPA&nbsp;
										<input type="radio" id="secwpa2_6" onclick="AlterEnterprise('6')" value="2" name="AP_WPA_6">WPA 2&nbsp;
										<input type="radio" id="secauto_6" onclick="AlterEnterprise('6')" value="3" name="AP_WPA_6"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_6" value="CCMP" checked="checked" name="AP_CYPHER_6">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_6" value="TKIP" name="AP_CYPHER_6">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_6" name="AP_CYPHER_6">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)"  value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_6") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_6" id="AP_WPA_GROUP_REKEY_6">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)"  value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_6") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_6" id="AP_WPA_GMK_REKEY_6">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_6" id="AP_WEP_REKEY_6"  value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_6") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('6')" id="chk_PersonalKey_6" value="PSK" checked="checked" name="AP_SECFILE_6" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('6')" maxlength="64" name="PSK_KEY_6" id="PSK_KEY_6" disabled=""  value=\"""" + vapDom.getAttribute(
        "PSK_KEY_6") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('6')" id="chk_EnterpriseKey_6" value="EAP" name="AP_SECFILE_6">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_6" value="0" name="AP_RSN_ENA_PREAUTH_6">Disable
	<input type="radio" id="interface_enb_6" value="1" name="AP_RSN_ENA_PREAUTH_6">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_6" id="AP_WPA_PREAUTH_IF_6" value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_6") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_6" id="AP_EAP_REAUTH_PER_6" value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_6") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_6','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_6" id="AP_AUTH_SERVER_6"  value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_6") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_6" id="AP_AUTH_PORT_6" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_6") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_6" id="AP_AUTH_SECRET_6" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_6") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

	<!-- vap 7 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_7" value=\"""" + vapDom.getAttribute("AP_SECMODE_7") + """\">
	<input type="hidden" id="HID_AP_WPA_7" value=\"""" + vapDom.getAttribute("AP_WPA_7") + """\">
	<input type="hidden" id="HID_AP_CYPHER_7" value=\"""" + vapDom.getAttribute("AP_CYPHER_7") + """\">
	<input type="hidden" id="HID_AP_SECFILE_7" value=\"""" + vapDom.getAttribute("AP_SECFILE_7") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_7" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_7") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap7_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_7" onclick="displayData(1,'7')" value="None" name="AP_SECMODE_7">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div id="open_div_7" style="display: none;">
						<span style="padding-left: 65px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_7" onclick="displayData(3,'7')" value="WPA" checked="checked" name="AP_SECMODE_7">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_7">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_7" onclick="EnableEnterprise('7')" value="0" name="AP_WPA_7">802.1x&nbsp;
										<input type="radio" id="secwpa_7" onclick="AlterEnterprise('7')" value="1" checked="checked" name="AP_WPA_7">WPA&nbsp;
										<input type="radio" id="secwpa2_7" onclick="AlterEnterprise('7')" value="2" name="AP_WPA_7">WPA 2&nbsp;
										<input type="radio" id="secauto_7" onclick="AlterEnterprise('7')" value="3" name="AP_WPA_7"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_7" value="CCMP" checked="checked" name="AP_CYPHER_7">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_7" value="TKIP" name="AP_CYPHER_7">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_7" name="AP_CYPHER_7">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_7") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_7" id="AP_WPA_GROUP_REKEY_7">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_7") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_7" id="AP_WPA_GMK_REKEY_7">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_7" id="AP_WEP_REKEY_7" value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_7") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('7')" id="chk_PersonalKey_7" value="PSK" checked="checked" name="AP_SECFILE_7" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('7')" maxlength="64" name="PSK_KEY_7" id="PSK_KEY_7" disabled="" value=\"""" + vapDom.getAttribute(
        "PSK_KEY_7") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('7')" id="chk_EnterpriseKey_7" value="EAP" name="AP_SECFILE_7">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_7" value="0" name="AP_RSN_ENA_PREAUTH_7">Disable
	<input type="radio" id="interface_enb_7" value="1" name="AP_RSN_ENA_PREAUTH_7">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_7" id="AP_WPA_PREAUTH_IF_7" value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_7") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_7" id="AP_EAP_REAUTH_PER_7"  value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_7") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_7','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_7" id="AP_AUTH_SERVER_7" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_7") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_7" id="AP_AUTH_PORT_7" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_7") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_7" id="AP_AUTH_SECRET_7" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_7") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

	<!-- vap 8 table 2 -->

	<input type="hidden" id="HID_AP_SECMODE_8" value=\"""" + vapDom.getAttribute("AP_SECMODE_8") + """\">
	<input type="hidden" id="HID_AP_WPA_8" value=\"""" + vapDom.getAttribute("AP_WPA_8") + """\">
	<input type="hidden" id="HID_AP_CYPHER_8" value=\"""" + vapDom.getAttribute("AP_CYPHER_8") + """\">
	<input type="hidden" id="HID_AP_SECFILE_8" value=\"""" + vapDom.getAttribute("AP_SECFILE_8") + """\">
	<input type="hidden" id="HID_AP_RSN_ENA_PREAUTH_8" value=\"""" + vapDom.getAttribute("AP_RSN_ENA_PREAUTH_8") + """\">

	<table style="padding: 20px; width: 100%;display:none;"  id="vap_vap8_table2" class="vap-table">
		<tbody>
			<tr><td><b>Security Setting</b></td></tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_open_8" onclick="displayData(1,'8')" value="None" name="AP_SECMODE_8">
						Open
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div id="open_div_8" style="display: none;">
						<span style="padding-left: 65px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;No Security Applied</span>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div>
						<input type="radio" id="sec_wpa_8" onclick="displayData(3,'8')" value="WPA" checked="checked" name="AP_SECMODE_8">WPA
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div style="padding-left: 65px; display: block;" id="WPA_div_8">
						<table>
							<tbody>
								<tr><td colspan="2">Enhanced Security for Personal/Enterprise</td></tr>
								<tr>
									<td>
										<input type="radio" id="sec_802_8" onclick="EnableEnterprise('8')" value="0" name="AP_WPA_8">802.1x&nbsp;
										<input type="radio" id="secwpa_8" onclick="AlterEnterprise('8')" value="1" checked="checked" name="AP_WPA_8">WPA&nbsp;
										<input type="radio" id="secwpa2_8" onclick="AlterEnterprise('8')" value="2" name="AP_WPA_8">WPA 2&nbsp;
										<input type="radio" id="secauto_8" onclick="AlterEnterprise('8')" value="3" name="AP_WPA_8"> Auto&nbsp;
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CYPHER:</td>
									<td>
										<input type="radio" id="cypher_CCMP_8" value="CCMP" checked="checked" name="AP_CYPHER_8">CCMP
										<span id="span_cypher" style="display: none;">
											<input type="radio" id="cypher_tkip_8" value="TKIP" name="AP_CYPHER_8">TKIP
											<input type="radio" value="TKIP CCMP" id="cypher_tkip_ccmp_8" name="AP_CYPHER_8">Auto&nbsp;
										</span>
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WPA Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GROUP_REKEY_8") + """\" maxlength="16"  name="AP_WPA_GROUP_REKEY_8" id="AP_WPA_GROUP_REKEY_8">&nbsp;&nbsp;WPA Master Rekey:
	<input type="text" onkeypress="return  numCheck(event)" value=\"""" + vapDom.getAttribute("AP_WPA_GMK_REKEY_8") + """\" maxlength="16" name="AP_WPA_GMK_REKEY_8" id="AP_WPA_GMK_REKEY_8">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WEP Rekey Int:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_WEP_REKEY_8" id="AP_WEP_REKEY_8" value=\"""" + vapDom.getAttribute(
        "AP_WEP_REKEY_8") + """\">(802.1x mode only)
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_clearEnt('8')" id="chk_PersonalKey_8" value="PSK" checked="checked" name="AP_SECFILE_8" disabled="">Personal Shared Key
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PSK KEY</td>
									<td>
	<input type="password" onblur="keylen_check('8')" maxlength="64" name="PSK_KEY_8" id="PSK_KEY_8" disabled="" value=\"""" + vapDom.getAttribute(
        "PSK_KEY_8") + """\">
									</td>
								</tr>
								<tr>
									<td colspan="2">
	<input type="radio" onclick="default_fillEnt('8')" id="chk_EnterpriseKey_8" value="EAP" name="AP_SECFILE_8">Enterprise/RADIUS support
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSN Preauth</td>
									<td>
	<input type="radio" id="interface_dis_8" value="0" name="AP_RSN_ENA_PREAUTH_8">Disable
	<input type="radio" id="interface_enb_8" value="1" name="AP_RSN_ENA_PREAUTH_8">Enable
	&nbsp;&nbsp;Interface:
	<input type="text" maxlength="16" name="AP_WPA_PREAUTH_IF_8" id="AP_WPA_PREAUTH_IF_8" value=\"""" + vapDom.getAttribute(
        "AP_WPA_PREAUTH_IF_8") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EAP Reauth Period:</td>
									<td>
	<input type="text" onkeypress="return  numCheck(event)" maxlength="16" name="AP_EAP_REAUTH_PER_8" id="AP_EAP_REAUTH_PER_8" value=\"""" + vapDom.getAttribute(
        "AP_EAP_REAUTH_PER_8") + """\">Seconds
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auth Server IP:</td>
									<td>
	<input type="text" onblur="checkIp(1,'AP_AUTH_SERVER_8','IPaddress')" onkeypress="return  IPKeyCheck(event)" maxlength="16" name="AP_AUTH_SERVER_8" id="AP_AUTH_SERVER_8" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SERVER_8") + """\">
	&nbsp;&nbsp;&nbsp;&nbsp; Port: <input type="text" onkeypress="return  numCheck(event)" maxlength="6" name="AP_AUTH_PORT_8" id="AP_AUTH_PORT_8" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_PORT_8") + """\">
									</td>
								</tr>
								<tr>
									<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shared Secret:</td>
									<td>
	&nbsp;&nbsp;&nbsp;<input type="password" value="" maxlength="64" name="AP_AUTH_SECRET_8" id="AP_AUTH_SECRET_8" value=\"""" + vapDom.getAttribute(
        "AP_AUTH_SECRET_8") + """\">
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>

"""
    return tableString


def apAclTab(aclDom):
    """

    @param aclDom:
    @return:
    """
    tableString = """
	<table style="padding:20px 20px 0px 20px; width:100%;">
		<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr>
				<td colspan="2"><b>Access Control List</b></td>
			</tr>
			<tr>
				<td>Select VAP</td>
				<td>
					<select id="acl_vap" name="acl_vap" onchange="aclVap()">
						<option value="1">VAP 1</option>
						<option value="2">VAP 2</option>
						<option value="3">VAP 3</option>
						<option value="4">VAP 4</option>
						<option value="5">VAP 5</option>
						<option value="6">VAP 6</option>
						<option value="7">VAP 7</option>
						<option value="8">VAP 8</option>
					</select>
				</td>
			</tr>
			<tr>
			     <td colspan="2">
				<table style="width:100%;" id="acl_vap1_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr >
							<td>ACL<input type="hidden" id="acl_vap1_hd" name="acl_vap1_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP") + """\" /></td>
							<td>
							    <input type="radio" id="acl_vap1_enabled" onclick="ToggleACL(true,'1')" value="1" name="ACL_VAP">Enable
							    <input type="radio" id="acl_vap1_disabled" onclick="ToggleACL(false,'1')" value="0" name="ACL_VAP">Disable
							</td>
						</tr>
						<tr id="acl_vap1_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap1_hd" name="acltype_vap1_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap1_allow\" name=\"ACLTYPE_VAP\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap1_deny\" name=\"ACLTYPE_VAP\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST\" name=\"MAC_LIST\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist1")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap2_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap2_hd" name="acl_vap2_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_2") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap2_enabled" onclick="ToggleACL(true,'2')" value="1" name="ACL_VAP_2">Enable
							   <input type="radio" id="acl_vap2_disabled" onclick="ToggleACL(false,'2')" value="0" name="ACL_VAP_2">Disable
							</td>
						</tr>
						<tr id="acl_vap2_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap2_hd" name="acltype_vap2_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_2") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap2_allow\" name=\"ACLTYPE_VAP_2\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap2_deny\" name=\"ACLTYPE_VAP_2\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_2\" name=\"MAC_LIST_2\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist2")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap3_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap3_hd" name="acl_vap3_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_3") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap3_enabled" onclick="ToggleACL(true,'3')" value="1" name="ACL_VAP_3">Enable
							   <input type="radio" id="acl_vap3_disabled" onclick="ToggleACL(false,'3')" value="0" name="ACL_VAP_3">Disable
							</td>
						</tr>
						<tr id="acl_vap3_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap3_hd" name="acltype_vap3_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_3") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap3_allow\" name=\"ACLTYPE_VAP_3\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap3_deny\" name=\"ACLTYPE_VAP_3\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_3\" name=\"MAC_LIST_3\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist3")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap4_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap4_hd" name="acl_vap4_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_4") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap4_enabled" onclick="ToggleACL(true,'4')" value="1" name="ACL_VAP_4">Enable
							   <input type="radio" id="acl_vap4_disabled" onclick="ToggleACL(false,'4')" value="0" name="ACL_VAP_4">Disable
							</td>
						</tr>
						<tr id="acl_vap4_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap4_hd" name="acltype_vap4_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_4") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap4_allow\" name=\"ACLTYPE_VAP_4\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap4_deny\" name=\"ACLTYPE_VAP_4\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_4\" name=\"MAC_LIST_4\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist4")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap5_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap5_hd" name="acl_vap5_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_5") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap5_enabled" onclick="ToggleACL(true,'5')" value="1" name="ACL_VAP_5">Enable
							   <input type="radio" id="acl_vap5_disabled" onclick="ToggleACL(false,'5')" value="0" name="ACL_VAP_5">Disable
							</td>
						</tr>
						<tr id="acl_vap5_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap5_hd" name="acltype_vap5_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_5") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap5_allow\" name=\"ACLTYPE_VAP_5\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap5_deny\" name=\"ACLTYPE_VAP_5\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_5\" name=\"MAC_LIST_5\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist5")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap6_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap6_hd" name="acl_vap6_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_6") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap6_enabled" onclick="ToggleACL(true,'6')" value="1" name="ACL_VAP_6">Enable
							   <input type="radio" id="acl_vap6_disabled" onclick="ToggleACL(false,'6')" value="0" name="ACL_VAP_6">Disable
							</td>
						</tr>
						<tr id="acl_vap6_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap6_hd" name="acltype_vap6_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_6") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap6_allow\" name=\"ACLTYPE_VAP_6\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap6_deny\" name=\"ACLTYPE_VAP_6\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_6\" name=\"MAC_LIST_6\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist6")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap7_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap7_hd" name="acl_vap7_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_7") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap7_enabled" onclick="ToggleACL(true,'7')" value="1" name="ACL_VAP_7">Enable
							   <input type="radio" id="acl_vap7_disabled" onclick="ToggleACL(false,'7')" value="0" name="ACL_VAP_7">Disable
							</td>
						</tr>
						<tr id="acl_vap7_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap7_hd" name="acltype_vap7_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_7") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap7_allow\" name=\"ACLTYPE_VAP_7\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap7_deny\" name=\"ACLTYPE_VAP_7\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_7\" name=\"MAC_LIST_7\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist7")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
				<table style="width:100%;display:none;" id="acl_vap8_table" class="acl-table">
					<colgroup><col width='20%'/><col width='80%'/></colgroup>
					<tbody>
						<tr>
							<td>ACL<input type="hidden" id="acl_vap8_hd" name="acl_vap8_hd" value=\"""" + aclDom.getAttribute(
        "ACL_VAP_8") + """\" /></td>
							<td>
							   <input type="radio" id="acl_vap8_enabled" onclick="ToggleACL(true,'8')" value="1" name="ACL_VAP_8">Enable
							   <input type="radio" id="acl_vap8_disabled" onclick="ToggleACL(false,'8')" value="0" name="ACL_VAP_8">Disable
							</td>
						</tr>
						<tr id="acl_vap8_tr" style="width:100%;display:none;">
							<td>MAC Address List<input type="hidden" id="acltype_vap8_hd" name="acltype_vap8_hd" value=\"""" + aclDom.getAttribute(
        "ACLTYPE_VAP_8") + """\" /></td>
							<td>
								<input type=\"radio\" id=\"acltype_vap8_allow\" name=\"ACLTYPE_VAP_8\" value=\"1\"> Allow
								<input type=\"radio\" id=\"acltype_vap8_deny\" name=\"ACLTYPE_VAP_8\" value=\"0\"> Deny <br/>
								<textarea id=\"MAC_LIST_8\" name=\"MAC_LIST_8\" style=\"width:300px;height:150px;\">""" + getText(
        aclDom.getElementsByTagName("maclist8")[0].childNodes) + """</textarea><br/><span style=\"color:#555;font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span>
							</td>
						</tr>
					</tbody>
				</table>
			     </td>
			</tr>
		</tbody>
	</table>
"""
    return tableString


def apServicesTab(servicesDom):
    """

    @param servicesDom:
    @return:
    """
    tableString = """
<table style="padding:20px;width:100%;">
	<colgroup><col width='20%'/><col width='80%'/></colgroup>
		<tbody>
			<tr><td colspan="2"><b>UPnP Server</b><input type="hidden" id="upnpHidden" name="upnpHidden" value=\"""" + servicesDom.getAttribute(
        "AP_UPNP") + """\" /></td></tr>
			<tr>
				<td>UPnP</td>
				<td>
					<input id="upnp_enable" name="AP_UPNP" value="Enable" type="radio">Enable&nbsp;&nbsp;
					<input id="upnp_disable" name="AP_UPNP" value="Disable" type="radio">Disable
				</td>
			</tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr><td colspan="2"><b>System Log</b><input type="hidden" id="sysLogHidden" name="sysLogHidden" value=\"""" + servicesDom.getAttribute(
        "AP_SYSLOG") + """\" /></td></tr>
			<tr>
				<td>System Log</td>
				<td>
					<input name="AP_SYSLOG" value="Enable" onclick="ServiceState('Syslog',true)" id="syslog_enable" type="radio">Enable&nbsp;&nbsp;
					<input name="AP_SYSLOG" value="Disable" onclick="ServiceState('Syslog',false)" id="syslog_disable" type="radio">Disable
				</td>
			</tr>
			<tr>
				<td>Logging IP Address</td>
				<td>
<input id="syslog_ip" name="AP_SYSLOG_IP" style="width: 150px;" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(1,'syslog_ip','IPAddress')" type="text" value=\"""" + servicesDom.getAttribute(
        "AP_SYSLOG_IP") + """\" >
				</td>
			</tr>
			<tr>
				<td>Logging Port</td>
				<td>
<input style="width: 50px;" maxlength="5" id="syslog_port" value="514" name="SYSLOG_PORT" onkeypress="return  numCheck(event)" type="text" value=\"""" + servicesDom.getAttribute(
        "SYSLOG_PORT") + """\" >
				</td>
			</tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr>
				<td colspan="2"><b>SNMP Server</b><input type="hidden" id="snmpHidden" name="snmpHidden" value=\"""" + servicesDom.getAttribute(
        "SNMP_Enable") + """\" /></td>
			</tr>
			<tr>
				<td>SNMP</td>
				<td>
<input name="SNMP_Enable" value="Enable" onclick="ServiceState('Snmp',true)" id="snmp_enable" type="radio">Enable&nbsp;&nbsp;
<input name="SNMP_Enable" value="Disable" onclick="ServiceState('Snmp',false)" id="snmp_disable" type="radio">Disable
				</td>
			</tr>
			<tr>
				<td>Read Only Community</td>
				<td><input id="snmp_comm" name="SNMP_Comm" type="text" value=\"""" + servicesDom.getAttribute(
        "SNMP_Comm") + """\" ></td>
			</tr>
			<tr>
				<td>System Location</td>
				<td><input id="snmp_location" name="SNMP_Location" type="text" value=\"""" + servicesDom.getAttribute(
        "SNMP_Location") + """\" ></td>
			</tr>
			<tr>
				<td>System Contact</td>
				<td><input id="snmp_contact" name="SNMP_Contact" type="text" value=\"""" + servicesDom.getAttribute(
        "SNMP_Contact") + """\" /></td>
			</tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr><td colspan="2"><b>DHCP Server Settings</b><input type="hidden" id="dhcpHidden" name="dhcpHidden" value=\"""" + servicesDom.getAttribute(
        "DHCP_SER") + """\" /></td></tr>
				<tr>
					<td>DHCP Server</td>
					<td><input type="radio" onclick="dhcpState(true)" value="Enable" id="DHCP_SER_EN" name="DHCP_SER">Enable &nbsp; &nbsp;
					<input type="radio" onclick="dhcpState(false)" value="Disable" id="DHCP_SER_DS" name="DHCP_SER">Disable
					</td>
				</tr>
				<tr>
					<td>DHCP Start IP</td>
					<td><input type="text" maxlength="16" name="DHCP_SIP" id="DHCP_SIP" value=\"""" + servicesDom.getAttribute(
        "DHCP_SIP") + """\" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(1,'DHCP_SIP','StartIP')"></td>
				</tr>
				<tr>
					<td>DHCP End IP</td>
					<td><input type="text" maxlength="16" name="DHCP_EIP" id="DHCP_EIP" value=\"""" + servicesDom.getAttribute(
        "DHCP_EIP") + """\" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(1,'DHCP_EIP','EndIP')"></td>
				</tr>
				<tr>
					<td>Network Mask</td>
					<td><input type="text" maxlength="16" name="DHCP_NM" id="DHCP_NM" value=\"""" + servicesDom.getAttribute(
        "DHCP_NM") + """\" onkeypress="return  IPKeyCheck(event)" onblur="checkIp(2,'DHCP_NM','NetworkMask')"></td>
				</tr>
				<tr>
					<td>DHCP Lease Time</td>
					<td><input type="text" onkeypress="return numCheck(event)" name="DHCP_LEASE" id="DHCP_LEASE" value=\"""" + servicesDom.getAttribute(
        "DHCP_LEASE") + """\" > Minutes</td>
				</tr>
				<tr><td colspan="2">&nbsp;</td></tr>
				<tr>
					<td colspan="2">
						<div id="timeeditor">
							Time Zone :<input type="hidden" id="timeZoneHidden" name="timeZoneHidden" value=\"""" + servicesDom.getAttribute(
        "TimeZone") + """\" />
							<select name="TimeZone" id="DropDownTimezone">
							      <option value="HMT-12">(GMT -12:00) Eniwetok, Kwajalein</option>
							      <option value="SST11">(GMT -11:00) Midway Island, Samoa</option>
							      <option value="HST10">(GMT -10:00) Hawaii</option>
							      <option value="AKST9AKDT">(GMT -9:00) Alaska</option>
							      <option value="PST8PDT">(GMT -8:00) Pacific Time (US &amp; Canada)</option>
							      <option value="MST7MDT">(GMT -7:00) Mountain Time (US &amp; Canada)</option>
							      <option value="CST6CDT">(GMT -6:00) Central Time (US &amp; Canada), Mexico City</option>
							      <option value="EST5EDT">(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima</option>
 							      <option value="AST4ADT">(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz</option>
							      <option value="NST3:30NDT">(GMT -3:30) Newfoundland</option>
							      <option value="ART3ARST">(GMT -3:00) Brazil, Buenos Aires, Georgetown</option>
							      <option value="GST2">(GMT -2:00) Mid-Atlantic</option>
							      <option value="AZOT1AZOST">(GMT -1:00 hour) Azores, Cape Verde Islands</option>
							      <option value="GMT0BST">(GMT) Western Europe Time, London, Lisbon, Casablanca</option>
							      <option value="CET-1CEST">(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris</option>
							      <option value="EET-2EEST">(GMT +2:00) Kaliningrad, South Africa</option>
							      <option value="AST-3">(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg</option>
							      <option value="UCT-3:30">(GMT +3:30) Tehran</option>
							      <option value="GST-4:00">(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi</option>
							      <option value="AFT-4:30">(GMT +4:30) Kabul</option>
							      <option value="PKT-5:00">(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent</option>
							      <option value="IST-5:30">(GMT +5:30) Bombay, Calcutta, Madras, New Delhi</option>
							      <option value="NPT-5:45">(GMT +5:45) Kathmandu</option>
							      <option value="BDT-6">(GMT +6:00) Almaty, Dhaka, Colombo</option>
							      <option value="ICT-7">(GMT +7:00) Bangkok, Hanoi, Jakarta</option>
							      <option value="SGT-8">(GMT +8:00) Beijing, Perth, Singapore, Hong Kong</option>
							      <option value="JST-9">(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk</option>
							      <option value="CST-9:30CST">(GMT +9:30) Adelaide, Darwin</option>
							      <option value="ChST-10">(GMT +10:00) Eastern Australia, Guam, Vladivostok</option>
							      <option value="MAGT-11MAGST">(GMT +11:00) Magadan, Solomon Islands, New Caledonia</option>
							      <option value="FJT-12">(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka</option>
							</select>
							<br><br>
							Configuration :<input type="hidden" id="ntpHidden" name="ntpHidden" value=\"""" + servicesDom.getAttribute(
        "NTP_Enable") + """\" />
							<select onchange="AlterTimeSettings()" name="NTP_Enable" id="NTP_Enable">
								<option value="Disable">Manual</option>
								<option value="Enable">Automatic</option>
							</select>
							<br><br>
							<table id="Time_Manual" style="display: none;">
								<tbody>
									<tr>
										<td>Date :</td>
										<td>
										<input id="txt_date" maxlength="25" size="10" onkeypress="return false;" type="Text">
										</td>
									</tr>
									<tr>
										<td>Time :</td>
										<td>
				<input size="1" onblur="checktime('hour')" id="txt_hour" onkeypress="return numCheck(event)" type="text"> :
				<input size="1" onblur="checktime('minute')" id="txt_minute" onkeypress="return numCheck(event)" type="text"> :
				<input size="1" onblur="checktime('second')" id="txt_second" onkeypress="return numCheck(event)" type="text">
				<input value="Copy Computer Date&amp;Time" onclick="GetSystemTime(1)" id="btn_getTime" type="button">
										</td>
									</tr>
								</tbody>
							</table>
							<table id="Time_NTP" style="display: none;">
								<tbody>
									<tr><td>NTP ServerIP :  </td><td> </td></tr>
									<tr>
										<td>
				<input id="NTPServer_txt" value=\"""" + servicesDom.getAttribute("NTPSERVERIP") + """\" name="NTPSERVERIP" onkeypress="return  IPKeyCheck(event)" type="text">
										</td>
										<td>
											<select id="NTPServer_list" onchange="change_Ntpserver()">
												<option value="" selected="selected">Select Time Server</option>
												<option value="192.5.41.41">192.5.41.41 -North America</option>
												<option value="192.5.41.209">192.5.41.209 -North America</option>
												<option value="208.184.49.9">208.184.49.9 -North America</option>
												<option value="131.188.3.220">131.188.3.220 -Europe</option>
												<option value="130.149.17.8">130.149.17.8 -Europe</option>
												<option value="203.60.1.2">203.60.1.2 -Australia</option>
												<option value="203.117.180.36">203.117.180.36 -Asia Pacific</option>
											</select>
										</td>
									</tr>
							</tbody>
						</table>
					</div>
				</td>
			</tr>
		</tbody>
	</table>"""
    return tableString


def create_config_tamplate(h):
    """

    @param h:
    """
    global html
    html = h
    site = __file__.split("/")[3]
    configurationTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplate.xml" % site
    # create service template dom
    configTemplateDom = xml.dom.minidom.parseString(
        "<configurationTemplate></configurationTemplate>")
    if (os.path.isfile(configurationTemplateFile)):
        configTemplateDom = xml.dom.minidom.parse(configurationTemplateFile)

    # create new tamplate element
    templateDom = configTemplateDom.createElement("template")
    templateDom.setAttribute("deviceName", html.var("deviceName"))
    templateDom.setAttribute("deviceId", html.var("deviceId"))
    templateDom.setAttribute("name", html.var("templateName"))
    templateDom.setAttribute("id", str(datetime.datetime.now()))

    # create new network element
    networkDom = configTemplateDom.createElement("network")
    if html.var("AP_HOSTNAME") is not None:
        if html.var("AP_HOSTNAME").strip() != "":
            networkDom.setAttribute("AP_HOSTNAME", html.var("AP_HOSTNAME"))
        else:
            networkDom.setAttribute("AP_HOSTNAME", "11nAP")
    else:
        networkDom.setAttribute("AP_HOSTNAME", "11nAP")

    if html.var("AP_NETMASK") is not None:
        if html.var("AP_NETMASK").strip() != "":
            networkDom.setAttribute("AP_NETMASK", html.var("AP_NETMASK"))
        else:
            networkDom.setAttribute("AP_NETMASK", "255.255.255.0")
    else:
        networkDom.setAttribute("AP_NETMASK", "255.255.255.0")

    if html.var("IPGW") is not None:
        if html.var("IPGW") is not None:
            networkDom.setAttribute("IPGW", html.var("IPGW"))
        else:
            networkDom.setAttribute("IPGW", "192.168.1.1")
    else:
        networkDom.setAttribute("IPGW", "192.168.1.1")

    if html.var("PRIDNS") is not None:
        if html.var("PRIDNS").strip() != "":
            networkDom.setAttribute("PRIDNS", html.var("PRIDNS"))
    if html.var("SECDNS") is not None:
        if html.var("SECDNS").strip() != "":
            networkDom.setAttribute("SECDNS", html.var("SECDNS"))
    if html.var("WAN_MODE") is not None:
        networkDom.setAttribute("WAN_MODE", html.var("WAN_MODE"))
    else:
        networkDom.setAttribute("WAN_MODE", "bridged")

    templateDom.appendChild(networkDom)

    # create new radio element
    radioDom = configTemplateDom.createElement("radio")
    if html.var("AP_STARTMODE") is not None:
        radioDom.setAttribute("AP_STARTMODE", html.var("AP_STARTMODE"))
    else:
        radioDom.setAttribute("AP_STARTMODE", "standard")

    if html.var("MANAGEMENTVLAN") is not None:
        radioDom.setAttribute("MANAGEMENTVLAN", html.var("MANAGEMENTVLAN"))
    else:
        radioDom.setAttribute("MANAGEMENTVLAN", "0")

    if html.var("ATH_countrycode") is not None:
        radioDom.setAttribute("ATH_countrycode", html.var("ATH_countrycode"))
    else:
        radioDom.setAttribute("ATH_countrycode", "IN")

    if html.var("HID_AP_MAX_VAP") is not None:
        radioDom.setAttribute("AP_MAX_VAP", html.var("HID_AP_MAX_VAP"))
    else:
        radioDom.setAttribute("AP_MAX_VAP", "1")

    if html.var("AP_PRIMARY_CH") is not None:
        radioDom.setAttribute("AP_PRIMARY_CH", html.var("AP_PRIMARY_CH"))
    else:
        radioDom.setAttribute("AP_PRIMARY_CH", "6")

    if html.var("AP_CHMODE") is not None:
        radioDom.setAttribute("AP_CHMODE", html.var("AP_CHMODE"))
    else:
        radioDom.setAttribute("AP_CHMODE", "11NGHT20")

    if html.var("AP_TXPOWER") is not None:
        if html.var("AP_TXPOWER") != "":
            radioDom.setAttribute("AP_TXPOWER", html.var("AP_TXPOWER"))

    if html.var("AP_DISTANCE") is not None:
        if html.var("AP_DISTANCE").strip() != "":
            radioDom.setAttribute("AP_DISTANCE", html.var("AP_DISTANCE"))
        else:
            radioDom.setAttribute("AP_DISTANCE", "0")
    else:
        radioDom.setAttribute("AP_DISTANCE", "0")

    if html.var("AP_SLOTTIME") is not None:
        if html.var("AP_SLOTTIME").strip() != "":
            radioDom.setAttribute("AP_SLOTTIME", html.var("AP_SLOTTIME"))
        else:
            radioDom.setAttribute("AP_SLOTTIME", "9")
    else:
        radioDom.setAttribute("AP_SLOTTIME", "9")

    if html.var("AP_ACKTIMEOUT") is not None:
        if html.var("AP_ACKTIMEOUT").strip() != "":
            radioDom.setAttribute("AP_ACKTIMEOUT", html.var("AP_ACKTIMEOUT"))
        else:
            radioDom.setAttribute("AP_ACKTIMEOUT", "25")
    else:
        radioDom.setAttribute("AP_ACKTIMEOUT", "25")

    if html.var("AP_CTSTIMEOUT") is not None:
        if html.var("AP_CTSTIMEOUT").strip() != "":
            radioDom.setAttribute("AP_CTSTIMEOUT", html.var("AP_CTSTIMEOUT"))
        else:
            radioDom.setAttribute("AP_CTSTIMEOUT", "25")
    else:
        radioDom.setAttribute("AP_CTSTIMEOUT", "25")

    if html.var("SHORTGI") is not None:
        radioDom.setAttribute("SHORTGI", html.var("SHORTGI"))
    else:
        radioDom.setAttribute("SHORTGI", "1")

    if html.var("AMPDUENABLE") is not None:
        radioDom.setAttribute("AMPDUENABLE", html.var("AMPDUENABLE"))
    else:
        radioDom.setAttribute("AMPDUENABLE", "0")

    if html.var("AMPDUFRAMES") is not None:
        if html.var("AMPDUFRAMES").strip() != "":
            radioDom.setAttribute("AMPDUFRAMES", html.var("AMPDUFRAMES"))
        else:
            radioDom.setAttribute("AMPDUFRAMES", "32")
    else:
        radioDom.setAttribute("AMPDUFRAMES", "32")

    if html.var("AMPDULIMIT") is not None:
        if html.var("AMPDULIMIT").strip() != "":
            radioDom.setAttribute("AMPDULIMIT", html.var("AMPDULIMIT"))
        else:
            radioDom.setAttribute("AMPDULIMIT", "50000")
    else:
        radioDom.setAttribute("AMPDULIMIT", "50000")

    if html.var("AMPDUMIN") is not None:
        if html.var("AMPDUMIN").strip() != "":
            radioDom.setAttribute("AMPDUMIN", html.var("AMPDUMIN"))
        else:
            radioDom.setAttribute("AMPDUMIN", "32768")
    else:
        radioDom.setAttribute("AMPDUMIN", "32768")

    if html.var("CWMMODE") is not None:
        radioDom.setAttribute("CWMMODE", html.var("CWMMODE"))
    else:
        radioDom.setAttribute("CWMMODE", "1")

    if html.var("TX_CHAINMASK") is not None:
        radioDom.setAttribute("TX_CHAINMASK", html.var("TX_CHAINMASK"))
    else:
        radioDom.setAttribute("TX_CHAINMASK", "0")

    if html.var("RX_CHAINMASK") is not None:
        radioDom.setAttribute("RX_CHAINMASK", html.var("RX_CHAINMASK"))
    else:
        radioDom.setAttribute("RX_CHAINMASK", "0")

    if html.var("AP_LONGDISTANCE") is not None:
        radioDom.setAttribute("AP_LONGDISTANCE", html.var("AP_LONGDISTANCE"))
    else:
        radioDom.setAttribute("AP_LONGDISTANCE", "0")

    if html.var("WLAN_ON_BOOT") is not None:
        radioDom.setAttribute("WLAN_ON_BOOT", html.var("WLAN_ON_BOOT"))
    else:
        radioDom.setAttribute("WLAN_ON_BOOT", "y")

    if html.var("AP_RADIO_ID") is not None:
        radioDom.setAttribute("AP_RADIO_ID", html.var("AP_RADIO_ID"))
    else:
        radioDom.setAttribute("AP_RADIO_ID", "0")

    if html.var("PUREG") is not None:
        radioDom.setAttribute("PUREG", html.var("PUREG"))
    else:
        radioDom.setAttribute("PUREG", "0")

    if html.var("PUREN") is not None:
        radioDom.setAttribute("PUREN", html.var("PUREN"))
    else:
        radioDom.setAttribute("PUREN", "0")

    if html.var("TXQUEUELEN") is not None:
        radioDom.setAttribute("TXQUEUELEN", html.var("TXQUEUELEN"))
    else:
        radioDom.setAttribute("TXQUEUELEN", "1000")

    if html.var("RATECTL") is not None:
        radioDom.setAttribute("RATECTL", html.var("RATECTL"))
    else:
        radioDom.setAttribute("RATECTL", "auto")

    if html.var("MANRATE") is not None:
        radioDom.setAttribute("MANRATE", html.var("MANRATE"))
    else:
        radioDom.setAttribute("MANRATE", "0x8c8c8c8c")

    if html.var("MANRETRIES") is not None:
        radioDom.setAttribute("MANRETRIES", html.var("MANRETRIES"))
    else:
        radioDom.setAttribute("MANRETRIES", "0x04040404")

    if html.var("AP_BEAC_INT") is not None:
        radioDom.setAttribute("AP_BEAC_INT", html.var("AP_BEAC_INT"))
    else:
        radioDom.setAttribute("AP_BEAC_INT", "100")

    if html.var("APM_Enable") is not None:
        radioDom.setAttribute("APM_Enable", html.var("APM_Enable"))
    else:
        radioDom.setAttribute("APM_Enable", "Enable")

    templateDom.appendChild(radioDom)

    # create new vap element    and int(html.var("HID_AP_MAX_VAP")) > 1
    vapDom = configTemplateDom.createElement("vap")
    if html.var("AP_PRIMARY_KEY_0") is not None:
        vapDom.setAttribute("AP_PRIMARY_KEY_0", html.var("AP_PRIMARY_KEY_0"))
    else:
        vapDom.setAttribute("AP_PRIMARY_KEY_0", "1")

    if html.var("AP_WEP_MODE_0") is not None:
        vapDom.setAttribute("AP_WEP_MODE_0", html.var("AP_WEP_MODE_0"))
    else:
        vapDom.setAttribute("AP_WEP_MODE_0", "1")

    if html.var("AP_DYN_VLAN") is not None:
        vapDom.setAttribute("AP_DYN_VLAN", html.var("AP_DYN_VLAN"))
    else:
        vapDom.setAttribute("AP_DYN_VLAN", "0")

    if html.var("WEPKEY_1") is not None:
        if html.var("WEPKEY_1").strip() != "":
            vapDom.setAttribute("WEPKEY_1", html.var("WEPKEY_1"))
    if html.var("WEPKEY_2") is not None:
        if html.var("WEPKEY_2").strip() != "":
            vapDom.setAttribute("WEPKEY_2", html.var("WEPKEY_2"))
    if html.var("WEPKEY_3") is not None:
        if html.var("WEPKEY_3").strip() != "":
            vapDom.setAttribute("WEPKEY_3", html.var("WEPKEY_3"))
    if html.var("WEPKEY_4") is not None:
        if html.var("WEPKEY_4").strip() != "":
            vapDom.setAttribute("WEPKEY_4", html.var("WEPKEY_4"))

    if html.var("ROOTAP_MAC") is not None:
        if html.var("ROOTAP_MAC").strip() != "":
            vapDom.setAttribute("ROOTAP_MAC", html.var("ROOTAP_MAC"))

    # For VAP 1:
    if int(html.var("HID_AP_MAX_VAP")) > 0:
        # AP_SSID
        if html.var("AP_SSID") is not None:
            if html.var("AP_SSID").strip() != "":
                vapDom.setAttribute("AP_SSID", html.var("AP_SSID"))
            else:
                vapDom.setAttribute("AP_SSID", "SHYAM_2G")
        else:
            vapDom.setAttribute("AP_SSID", "SHYAM_2G")

        # HIDE_SSID
        if html.var("HIDE_SSID") is not None:
            if html.var("HIDE_SSID").strip() != "":
                vapDom.setAttribute("HIDE_SSID", html.var("HIDE_SSID"))
            else:
                vapDom.setAttribute("HIDE_SSID", "0")
        else:
            vapDom.setAttribute("HIDE_SSID", "0")

        # AP_VLAN
        if html.var("AP_VLAN") is not None:
            if html.var("AP_VLAN").strip() != "":
                vapDom.setAttribute("AP_VLAN", html.var("AP_VLAN"))
            else:
                vapDom.setAttribute("AP_VLAN", "2")
        else:
            vapDom.setAttribute("AP_VLAN", "2")

        # VLAN_PRI
        if html.var("VLAN_PRI") is not None:
            if html.var("VLAN_PRI").strip() != "":
                vapDom.setAttribute("VLAN_PRI", html.var("VLAN_PRI"))
            else:
                vapDom.setAttribute("VLAN_PRI", "0")
        else:
            vapDom.setAttribute("VLAN_PRI", "0")

        # AP_MODE
        if html.var("AP_MODE") is not None:
            if html.var("AP_MODE").strip() != "":
                vapDom.setAttribute("AP_MODE", html.var("AP_MODE"))
            else:
                vapDom.setAttribute("AP_MODE", "ap")
        else:
            vapDom.setAttribute("AP_MODE", "ap")

        # AP_SECMODE
        if html.var("AP_SECMODE") is not None:
            if html.var("AP_SECMODE").strip() != "":
                vapDom.setAttribute("AP_SECMODE", html.var("AP_SECMODE"))
            else:
                vapDom.setAttribute("AP_SECMODE", "None")
        else:
            vapDom.setAttribute("AP_SECMODE", "None")

        # AP_SECFILE
        if html.var("AP_SECFILE") is not None:
            if html.var("AP_SECFILE").strip() != "":
                vapDom.setAttribute("AP_SECFILE", html.var("AP_SECFILE"))
            else:
                vapDom.setAttribute("AP_SECFILE", "PSK")
        else:
            vapDom.setAttribute("AP_SECFILE", "PSK")

        # AP_BEAC_INT
        if html.var("AP_BEAC_INT") is not None:
            if html.var("AP_BEAC_INT").strip() != "":
                vapDom.setAttribute("AP_BEAC_INT", html.var("AP_BEAC_INT"))
            else:
                vapDom.setAttribute("AP_BEAC_INT", "100")
        else:
            vapDom.setAttribute("AP_BEAC_INT", "100")

        # AP_RTS_THR
        if html.var("AP_RTS_THR") is not None:
            if html.var("AP_RTS_THR").strip() != "":
                vapDom.setAttribute("AP_RTS_THR", html.var("AP_RTS_THR"))
            else:
                vapDom.setAttribute("AP_RTS_THR", "off")
        else:
            vapDom.setAttribute("AP_RTS_THR", "off")

        # AP_FRAG_THR
        if html.var("AP_FRAG_THR") is not None:
            if html.var("AP_FRAG_THR").strip() != "":
                vapDom.setAttribute("AP_FRAG_THR", html.var("AP_FRAG_THR"))
            else:
                vapDom.setAttribute("AP_FRAG_THR", "off")
        else:
            vapDom.setAttribute("AP_FRAG_THR", "off")

        # AP_WPA
        if html.var("AP_WPA") is not None:
            vapDom.setAttribute("AP_WPA", html.var("AP_WPA"))

        # AP_CYPHER
        if html.var("AP_CYPHER") is not None:
            vapDom.setAttribute("AP_CYPHER", html.var("AP_CYPHER"))

        # AP_WPA_GROUP_REKEY
        if html.var("AP_WPA_GROUP_REKEY") is not None:
            if html.var("AP_WPA_GROUP_REKEY").strip() != "":
                vapDom.setAttribute(
                    "AP_WPA_GROUP_REKEY", html.var("AP_WPA_GROUP_REKEY"))

        # AP_WPA_GMK_REKEY
        if html.var("AP_WPA_GMK_REKEY") is not None:
            if html.var("AP_WPA_GMK_REKEY").strip() != "":
                vapDom.setAttribute(
                    "AP_WPA_GMK_REKEY", html.var("AP_WPA_GMK_REKEY"))

        # AP_WEP_REKEY
        if html.var("AP_WEP_REKEY") is not None:
            if html.var("AP_WEP_REKEY").strip() != "":
                vapDom.setAttribute("AP_WEP_REKEY", html.var("AP_WEP_REKEY"))

        # PSK_KEY
        if html.var("PSK_KEY") is not None:
            if html.var("PSK_KEY").strip() != "":
                vapDom.setAttribute("PSK_KEY", html.var("PSK_KEY"))
            # AP_RSN_ENA_PREAUTH
        if html.var("AP_RSN_ENA_PREAUTH") is not None:
            vapDom.setAttribute(
                "AP_RSN_ENA_PREAUTH", html.var("AP_RSN_ENA_PREAUTH"))

        # AP_WPA_PREAUTH_IF
        if html.var("AP_WPA_PREAUTH_IF") is not None:
            vapDom.setAttribute(
                "AP_WPA_PREAUTH_IF", html.var("AP_WPA_PREAUTH_IF"))

        # AP_EAP_REAUTH_PER
        if html.var("AP_EAP_REAUTH_PER") is not None:
            vapDom.setAttribute(
                "AP_EAP_REAUTH_PER", html.var("AP_EAP_REAUTH_PER"))

        # AP_AUTH_SERVER
        if html.var("AP_AUTH_SERVER") is not None:
            vapDom.setAttribute("AP_AUTH_SERVER", html.var("AP_AUTH_SERVER"))

        # AP_AUTH_PORT
        if html.var("AP_AUTH_PORT") is not None:
            vapDom.setAttribute("AP_AUTH_PORT", html.var("AP_AUTH_PORT"))

        # AP_AUTH_SECRET
        if html.var("AP_AUTH_SECRET") is not None:
            vapDom.setAttribute("AP_AUTH_SECRET", html.var("AP_AUTH_SECRET"))

    # For VAP: 2 3 4 5 6 7 8
    for j in range(2, 9):
        # AP_SSID
        if html.var("AP_SSID_" + str(j)) is not None:
            if html.var("AP_SSID_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "AP_SSID_" + str(j), html.var("AP_SSID_" + str(j)))
            else:
                vapDom.setAttribute("AP_SSID_" + str(j), "SHYAM_2G")
        else:
            vapDom.setAttribute("AP_SSID_" + str(j), "SHYAM_2G")

        # HIDE_SSID
        if html.var("HIDE_SSID_" + str(j)) is not None:
            if html.var("HIDE_SSID_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "HIDE_SSID_" + str(j), html.var("HIDE_SSID_" + str(j)))
            else:
                vapDom.setAttribute("HIDE_SSID_" + str(j), "0")
        else:
            vapDom.setAttribute("HIDE_SSID_" + str(j), "0")

        # AP_VLAN
        if html.var("AP_VLAN_" + str(j)) is not None:
            if html.var("AP_VLAN_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "AP_VLAN_" + str(j), html.var("AP_VLAN_" + str(j)))
            else:
                vapDom.setAttribute("AP_VLAN_" + str(j), "2")
        else:
            vapDom.setAttribute("AP_VLAN_" + str(j), "2")

        # VLAN_PRI
        if html.var("VLAN_PRI_" + str(j)) is not None:
            if html.var("VLAN_PRI_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "VLAN_PRI_" + str(j), html.var("VLAN_PRI_" + str(j)))
            else:
                vapDom.setAttribute("VLAN_PRI_" + str(j), "0")
        else:
            vapDom.setAttribute("VLAN_PRI_" + str(j), "0")

        # AP_MODE
        if html.var("AP_MODE_" + str(j)) is not None:
            if html.var("AP_MODE_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "AP_MODE_" + str(j), html.var("AP_MODE_" + str(j)))
            else:
                vapDom.setAttribute("AP_MODE_" + str(j), "ap")
        else:
            vapDom.setAttribute("AP_MODE_" + str(j), "ap")

        # AP_SECMODE
        if html.var("AP_SECMODE_" + str(j)) is not None:
            if html.var("AP_SECMODE_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "AP_SECMODE_" + str(j), html.var("AP_SECMODE_" + str(j)))
            else:
                vapDom.setAttribute("AP_SECMODE_" + str(j), "None")
        else:
            vapDom.setAttribute("AP_SECMODE_" + str(j), "None")

        # AP_SECFILE
        if html.var("AP_SECFILE_" + str(j)) is not None:
            if html.var("AP_SECFILE_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "AP_SECFILE_" + str(j), html.var("AP_SECFILE_" + str(j)))
            else:
                vapDom.setAttribute("AP_SECFILE_" + str(j), "PSK")
        else:
            vapDom.setAttribute("AP_SECFILE_" + str(j), "PSK")

        # AP_RTS_THR
        if html.var("AP_RTS_THR_" + str(j)) is not None:
            if html.var("AP_RTS_THR_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "AP_RTS_THR_" + str(j), html.var("AP_RTS_THR_" + str(j)))
            else:
                vapDom.setAttribute("AP_RTS_THR_" + str(j), "off")
        else:
            vapDom.setAttribute("AP_RTS_THR_" + str(j), "off")

        # AP_FRAG_THR
        if html.var("AP_FRAG_THR_" + str(j)) is not None:
            if html.var("AP_FRAG_THR_" + str(j)).strip() != "":
                vapDom.setAttribute("AP_FRAG_THR_" + str(
                    j), html.var("AP_FRAG_THR_" + str(j)))
            else:
                vapDom.setAttribute("AP_FRAG_THR_" + str(j), "off")
        else:
            vapDom.setAttribute("AP_FRAG_THR_" + str(j), "off")

        # AP_WPA
        if html.var("AP_WPA_" + str(j)) is not None:
            vapDom.setAttribute(
                "AP_WPA_" + str(j), html.var("AP_WPA_" + str(j)))

        # AP_CYPHER
        if html.var("AP_CYPHER_" + str(j)) is not None:
            vapDom.setAttribute(
                "AP_CYPHER_" + str(j), html.var("AP_CYPHER_" + str(j)))

        # AP_WPA_GROUP_REKEY
        if html.var("AP_WPA_GROUP_REKEY_" + str(j)) is not None:
            if html.var("AP_WPA_GROUP_REKEY_" + str(j)).strip() != "":
                vapDom.setAttribute("AP_WPA_GROUP_REKEY_" + str(
                    j), html.var("AP_WPA_GROUP_REKEY_" + str(j)))

        # AP_WPA_GMK_REKEY
        if html.var("AP_WPA_GMK_REKEY_" + str(j)) is not None:
            if html.var("AP_WPA_GMK_REKEY_" + str(j)).strip() != "":
                vapDom.setAttribute("AP_WPA_GMK_REKEY_" + str(
                    j), html.var("AP_WPA_GMK_REKEY_" + str(j)))

        # AP_WEP_REKEY
        if html.var("AP_WEP_REKEY_" + str(j)) is not None:
            if html.var("AP_WEP_REKEY_" + str(j)).strip() != "":
                vapDom.setAttribute("AP_WEP_REKEY_" + str(
                    j), html.var("AP_WEP_REKEY_" + str(j)))

        # PSK_KEY
        if html.var("PSK_KEY_" + str(j)) is not None:
            if html.var("PSK_KEY_" + str(j)).strip() != "":
                vapDom.setAttribute(
                    "PSK_KEY_" + str(j), html.var("PSK_KEY_" + str(j)))
            # AP_RSN_ENA_PREAUTH
        if html.var("AP_RSN_ENA_PREAUTH_" + str(j)) is not None:
            vapDom.setAttribute("AP_RSN_ENA_PREAUTH_" + str(
                j), html.var("AP_RSN_ENA_PREAUTH_" + str(j)))

        # AP_WPA_PREAUTH_IF
        if html.var("AP_WPA_PREAUTH_IF_" + str(j)) is not None:
            vapDom.setAttribute("AP_WPA_PREAUTH_IF_" + str(
                j), html.var("AP_WPA_PREAUTH_IF_" + str(j)))

        # AP_EAP_REAUTH_PER
        if html.var("AP_EAP_REAUTH_PER_" + str(j)) is not None:
            vapDom.setAttribute("AP_EAP_REAUTH_PER_" + str(
                j), html.var("AP_EAP_REAUTH_PER_" + str(j)))

        # AP_AUTH_SERVER
        if html.var("AP_AUTH_SERVER_" + str(j)) is not None:
            vapDom.setAttribute("AP_AUTH_SERVER_" + str(j),
                                html.var("AP_AUTH_SERVER_" + str(j)))

        # AP_AUTH_PORT
        if html.var("AP_AUTH_PORT_" + str(j)) is not None:
            vapDom.setAttribute(
                "AP_AUTH_PORT_" + str(j), html.var("AP_AUTH_PORT_" + str(j)))

        # AP_AUTH_SECRET
        if html.var("AP_AUTH_SECRET_" + str(j)) is not None:
            vapDom.setAttribute("AP_AUTH_SECRET_" + str(j),
                                html.var("AP_AUTH_SECRET_" + str(j)))

    templateDom.appendChild(vapDom)

    # create new acl element
    aclDom = configTemplateDom.createElement("acl")
    if html.var("ACL_VAP") is not None:
        aclDom.setAttribute("ACL_VAP", html.var("ACL_VAP"))
        if html.var("ACL_VAP") == "1":
            aclDom.setAttribute("ACLTYPE_VAP", html.var("ACLTYPE_VAP"))
    else:
        aclDom.setAttribute("ACL_VAP", "0")

    maclist = configTemplateDom.createElement("maclist1")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_2") is not None and int(html.var("HID_AP_MAX_VAP")) > 1:
        aclDom.setAttribute("ACL_VAP_2", html.var("ACL_VAP_2"))
        if html.var("ACL_VAP_2") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_2", html.var("ACLTYPE_VAP_2"))
    else:
        aclDom.setAttribute("ACL_VAP_2", "0")

    maclist = configTemplateDom.createElement("maclist2")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_2"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_3") is not None and int(html.var("HID_AP_MAX_VAP")) > 2:
        aclDom.setAttribute("ACL_VAP_3", html.var("ACL_VAP_3"))
        if html.var("ACL_VAP_3") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_3", html.var("ACLTYPE_VAP_3"))
    else:
        aclDom.setAttribute("ACL_VAP_3", "0")

    maclist = configTemplateDom.createElement("maclist3")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_3"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_4") is not None and int(html.var("HID_AP_MAX_VAP")) > 3:
        aclDom.setAttribute("ACL_VAP_4", html.var("ACL_VAP_4"))
        if html.var("ACL_VAP_4") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_4", html.var("ACLTYPE_VAP_4"))
    else:
        aclDom.setAttribute("ACL_VAP_4", "0")

    maclist = configTemplateDom.createElement("maclist4")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_4"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_5") is not None and int(html.var("HID_AP_MAX_VAP")) > 4:
        aclDom.setAttribute("ACL_VAP_5", html.var("ACL_VAP_5"))
        if html.var("ACL_VAP_5") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_5", html.var("ACLTYPE_VAP_5"))
    else:
        aclDom.setAttribute("ACL_VAP_5", "0")

    maclist = configTemplateDom.createElement("maclist5")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_5"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_6") is not None and int(html.var("HID_AP_MAX_VAP")) > 5:
        aclDom.setAttribute("ACL_VAP_6", html.var("ACL_VAP_6"))
        if html.var("ACL_VAP_6") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_6", html.var("ACLTYPE_VAP_6"))
    else:
        aclDom.setAttribute("ACL_VAP_6", "0")

    maclist = configTemplateDom.createElement("maclist6")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_6"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_7") is not None and int(html.var("HID_AP_MAX_VAP")) > 6:
        aclDom.setAttribute("ACL_VAP_7", html.var("ACL_VAP_7"))
        if html.var("ACL_VAP_7") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_7", html.var("ACLTYPE_VAP_7"))
    else:
        aclDom.setAttribute("ACL_VAP_7", "0")

    maclist = configTemplateDom.createElement("maclist7")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_7"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    if html.var("ACL_VAP_8") is not None and int(html.var("HID_AP_MAX_VAP")) > 7:
        aclDom.setAttribute("ACL_VAP_8", html.var("ACL_VAP_8"))
        if html.var("ACL_VAP_8") == "1":
            aclDom.setAttribute("ACLTYPE_VAP_8", html.var("ACLTYPE_VAP_8"))
    else:
        aclDom.setAttribute("ACL_VAP_8", "0")

    maclist = configTemplateDom.createElement("maclist8")
    maclisttext = configTemplateDom.createTextNode(html.var("MAC_LIST_8"))
    maclist.appendChild(maclisttext)
    aclDom.appendChild(maclist)

    templateDom.appendChild(aclDom)

    # create new services element
    servicesDom = configTemplateDom.createElement("services")
    if html.var("AP_UPNP") is not None:
        servicesDom.setAttribute("AP_UPNP", html.var("AP_UPNP"))
    else:
        servicesDom.setAttribute("AP_UPNP", "Enable")

    if html.var("AP_SYSLOG") is not None:
        servicesDom.setAttribute("AP_SYSLOG", html.var("AP_SYSLOG"))
    else:
        servicesDom.setAttribute("AP_SYSLOG", "Disable")

    if html.var("AP_SYSLOG_IP") is not None:
        if html.var("AP_SYSLOG_IP").strip() != "":
            servicesDom.setAttribute("AP_SYSLOG_IP", html.var("AP_SYSLOG_IP"))
    if html.var("SYSLOG_PORT") is not None:
        if html.var("SYSLOG_PORT").strip() != "":
            servicesDom.setAttribute("SYSLOG_PORT", html.var("SYSLOG_PORT"))
        else:
            servicesDom.setAttribute("SYSLOG_PORT", "514")
    else:
        servicesDom.setAttribute("SYSLOG_PORT", "514")

    if html.var("SNMP_Enable") is not None:
        servicesDom.setAttribute("SNMP_Enable", html.var("SNMP_Enable"))
    else:
        servicesDom.setAttribute("SNMP_Enable", "Enable")

    if html.var("SNMP_Comm") is not None:
        if html.var("SNMP_Comm").strip() != "":
            servicesDom.setAttribute("SNMP_Comm", html.var("SNMP_Comm"))
        else:
            servicesDom.setAttribute("SNMP_Comm", "public")
    else:
        servicesDom.setAttribute("SNMP_Comm", "public")

    if html.var("SNMP_Location") is not None:
        if html.var("SNMP_Location").strip() != "":
            servicesDom.setAttribute(
                "SNMP_Location", html.var("SNMP_Location"))
        else:
            servicesDom.setAttribute(
                "SNMP_Location", "Gurgaon, Haryana, India")
    else:
        servicesDom.setAttribute("SNMP_Location", "Gurgaon, Haryana, India")

    if html.var("SNMP_Contact") is not None:
        if html.var("SNMP_Contact").strip() != "":
            servicesDom.setAttribute("SNMP_Contact", html.var("SNMP_Contact"))
        else:
            servicesDom.setAttribute(
                "SNMP_Contact", "contact@shyamtelecom.com")
    else:
        servicesDom.setAttribute("SNMP_Contact", "contact@shyamtelecom.com")

    if html.var("DHCP_SER") is not None:
        servicesDom.setAttribute("DHCP_SER_EN", html.var("DHCP_SER"))
    else:
        servicesDom.setAttribute("DHCP_SER_EN", "Disable")

    if html.var("DHCP_SIP") is not None:
        if html.var("DHCP_SIP").strip() != "":
            servicesDom.setAttribute("DHCP_SIP", html.var("DHCP_SIP"))
        else:
            servicesDom.setAttribute("DHCP_SIP", "192.168.1.20")
    else:
        servicesDom.setAttribute("DHCP_SIP", "192.168.1.20")

    if html.var("DHCP_EIP") is not None:
        if html.var("DHCP_EIP").strip() != "":
            servicesDom.setAttribute("DHCP_EIP", html.var("DHCP_EIP"))
        else:
            servicesDom.setAttribute("DHCP_EIP", "192.168.1.254")
    else:
        servicesDom.setAttribute("DHCP_EIP", "192.168.1.254")

    if html.var("DHCP_NM") is not None:
        if html.var("DHCP_NM").strip() != "":
            servicesDom.setAttribute("DHCP_NM", html.var("DHCP_NM"))
        else:
            servicesDom.setAttribute("DHCP_NM", "255.255.255.0")
    else:
        servicesDom.setAttribute("DHCP_NM", "255.255.255.0")

    if html.var("DHCP_LEASE") is not None:
        if html.var("DHCP_LEASE").strip() != "":
            servicesDom.setAttribute("DHCP_LEASE", html.var("DHCP_LEASE"))
        else:
            servicesDom.setAttribute("DHCP_LEASE", "86400")
    else:
        servicesDom.setAttribute("DHCP_LEASE", "86400")

    if html.var("TimeZone") is not None:
        servicesDom.setAttribute("TimeZone", html.var("TimeZone"))
    else:
        servicesDom.setAttribute("TimeZone", "IST-5:30")

    if html.var("NTP_Enable") is not None:
        servicesDom.setAttribute("NTP_Enable", html.var("NTP_Enable"))
    else:
        servicesDom.setAttribute("NTP_Enable", "Disable")

    if html.var("NTPSERVERIP") is not None:
        if html.var("NTPSERVERIP").strip() != "":
            servicesDom.setAttribute("NTPSERVERIP", html.var("NTPSERVERIP"))
        else:
            servicesDom.setAttribute("NTPSERVERIP", "120.88.46.10")
    else:
        servicesDom.setAttribute("NTPSERVERIP", "120.88.46.10")

    templateDom.appendChild(servicesDom)

    templateId = "0"
    if html.var("templateId") is not None:
        templateId = html.var("templateId")

    if templateId == "0":
        configTemplateDom.getElementsByTagName(
            "configurationTemplate")[0].appendChild(templateDom)
    else:
        templateDom2 = configTemplateDom.getElementsByTagName("template")
        for tDom in templateDom2:
            if tDom.getAttribute("id") == templateId:
                configTemplateDom.getElementsByTagName(
                    "configurationTemplate")[0].replaceChild(templateDom, tDom)
                break

    fwxml = open(configurationTemplateFile, "w")
    fwxml.write(configTemplateDom.toxml())
    fwxml.close()
    html.write("0")

############################################### End Manage Template ######

############################################### Manage Configuration #####


def manage_host_configuration(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    html.new_header("Manage Host Configuration")
    html.write("<script type=\"text/javascript\" src=\"js/unmp/main/manage_host_configuration.js\"></script>\n")
    html.write(
        "<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\n")

    # create tabs for manage configuration
    html.write("<div class=\"tab-yo\">")
    html.write("<div class=\"tab-head\">")
    html.write(
        "<a id=\"chooseButton\" href=\"#addDiv\" class=\"tab-button\">Choose Device")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"settingButton\" href=\"#settingsDiv\" class=\"tab-disable\">Setting")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write(
        "<a id=\"chooseTButton\" href=\"#chooseTemplate\" class=\"tab-disable\">Choose Profile")
    html.write("<span class=\"\"></span>")
    html.write("</a>")
    html.write("<h2>Manage Configuration")
    html.write("</h2>")
    html.write("</div>")
    addDeviceButtonHover(h)
    addTemplateButtonHover(h)
    html.write(
        "<div id=\"settingsDiv\" class=\"tab-body\" style=\"display:block;margin:10px;\">")
    html.write(
        "<div style=\"display:block;width:100%; text-align:center;\">Please choose device to manage configuration</div>")
    html.write("</div>")
    html.write("</div>")
    html.footer()

    # image uploader div
    html.write("<div class=\"loading\"></div>")
    html.write(
        "<div id=\"imageUploadDiv\" style=\"width:400px;height:200px;z-index:2000;position:absolute;top:200px; left:25%;display:none;\" ><form id=\"imageUploadForm\" enctype=\"multipart/form-data\" method=\"post\" action=\"image_upload.py\"><table class=\"addform\">")
    html.write("<tr><th colspan=\"2\">Upload Image File<th></tr>")
    html.write(
        "<tr><td>select file</td><td><input type=\"file\" id=\"uploader\" name=\"file\"><label id=\"uploadError\" style=\"color:red;display:none;\"> *</label> </td></tr>")
    html.write(
        "<tr><td colspan=\"2\"><input type=\"submit\" onclick=\"return uploadImageFileCheck();\" id=\"imageUploader\" name=\"imageUploader\" value=\"Upload\" /><input type=\"button\" onclick=\"cancelUpload();\" value=\"Cancel\"/><input type=\"hidden\" id=\"deviceTy\" name=\"deviceTy\" value=\"\"/><input type=\"hidden\" id=\"deviceMac\" name=\"deviceMac\" value=\"\"/></td></tr>")
    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.new_footer()


def discoverDevices(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    deviceType = html.var("deviceType")
    timeOut = "5"
    sdmcString = html.var("sdmcString")

    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)
    args = ["--discovery", "-l", deviceType, "-o", timeOut, "-P", "54321"]
    command = [sdmcFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]

    #===================================================================================================
    # Output string of sdm utlity
    #     pipe = """
    #	Discovery Time less than or equal to 5 seconds,setting default time 5 seconds

    # DeviceType: AP
    # Sl.No, IPAddress, MacAddress, SSID, HostName, FirmwareVersion, BootloaderVersion
    # 0, 192.168.5.31, 00:50:c2:bc:c8:02, VVDN_AP, 11nAP, 1.1.1.0-347, 0.0.4
    # 0, 192.168.5.33, 00:50:c2:bc:c8:03, VVDN_AP, 12nAP, 1.1.1.0-347, 0.0.4
    #"""
    #=========================================================================
    outputStringArray = pipe.split("\n")  # split sdmc output string
    tableString = """
<table width=\"100%\" class=\"host-table\">
	<tbody>
		<tr>
			<td colspan=\"8\" align=\"left\" style=\"padding:5px;\">
				<table width=\"60%\">
					<colgroup><col width='30%'/><col width='70%'/></colgroup>
					<tr>
						<td>Selected Profile</td>
						<td>
							<input type=\"text\" id=\"templateName\" name=\"templateName\" value=\"None\" readonly=\"readonly\" />
							<input type=\"hidden\" id=\"templateId\" name=\"templateId\" value=\"\"/>
						</td>
					</tr>
					<tr>
						<td>Local Netmask</td>
						<td>
							<input type=\"text\" id=\"localNetmask\" name=\"localNetmask\"/>
							<label style=\"color:red;display:none;\" id=\"localNetmaskError\"> *</label>
						</td>
					</tr>
					<tr>
						<td>Gateway IP</td>
						<td>
							<input type=\"text\" id=\"gatewayIp\" name=\"gatewayIp\"/>
							<label style=\"color:red;display:none;\" id=\"gatewayIpError\"> *</label>
						</td>
					</tr>
				</table>
			</td>
		</tr>
		<tr>
			<th align=\"left\">
				<input type=\"checkbox\" id=\"allChecked\" name=\"allChecked\" value=\"all\"/>
			</th>
			<th align=\"left\">Host Address</th>
			<th align=\"left\">Host Name</th>
			<th align=\"left\">SSID</th>
			<th align=\"left\">Firmware Version</th>
			<th align=\"left\">Device Type</th>
			<th></th>
			<th></th>
		</tr>
"""
    i = 0
    totalHost = 0
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
                totalHost += 1
                # html.write("Device type: " + sdmcString + " Value: "+ outputString + "\n")
                # Device type: AP Value:
                # 0,192.168.5.31,00:50:c2:bc:c8:02,VVDN_AP,11nAP,1.1.1.0-347,0.0.4
                hostDetails = outputString.split(", ")
                tableString += "<tr>"
                tableString += "<td><input type=\"checkbox\" deviceType=\"" + deviceType + \
                               "\" id=\"" + hostDetails[2] + \
                               "\" name=\"host\" value=\"" + \
                               hostDetails[1] + "\"/></td>"
                tableString += "<td><input type=\"text\" readonly=\"readonly\" name=\"address\" value=\"" + \
                               hostDetails[1] + "\"/></td>"
                tableString += "<td>" + hostDetails[4] + "</td>"
                tableString += "<td>" + hostDetails[3] + "</td>"
                tableString += "<td>" + hostDetails[5] + "</td>"
                tableString += "<td>" + sdmcString + "</td>"
                tableString += "<td></td>"  # <input type=\"button\" name=\"ipSet\" value=\"IP set\"/>
                tableString += "<td><input type=\"button\" deviceType=\"" + deviceType + \
                               "\" mac=\"" + hostDetails[2] + \
                               "\" name=\"factoryReset\" value=\"Factory Reset\"/></td>"
                tableString += "</tr>"

    if totalHost == 0:
        tableString = "<table width=\"100%\"><tbody><tr><td align=\"center\">No Device Exist</td></tr>"
    else:
        tableString += "<tr><td colspan=\"8\" align=\"left\" style=\"padding:5px;\"><input type=\"button\" onclick=\"setIp();\" id=\"SetIp\" name=\"SetIp\" value=\"Set Ip\"/> <input type=\"button\" onclick=\"configSubmit();\" id=\"configSubmit\" name=\"configSubmit\" value=\"Apply Config Profile\" /> <input type=\"button\" onclick=\"imageUploadCheck();\" id=\"imageUpload\" name=\"imageUpload\" value=\"Image Upload\" /></td></tr><tr><td colspan=\"8\" style=\"font-size:9px;color:#555;\"> Please check the Configuration Profile before apply.</td></tr>"

    tableString += "<input type=\"hidden\" name=\"totalHost\" value=\"" + str(
        totalHost) + "\"/></tbody></table>"
    html.write(tableString)


def addTemplateButtonHover(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    # load shyam device form syhamdevices.xml file
    configTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplate.xml" % (
        sitename)
    dom = xml.dom.minidom.parseString(
        "<configurationTemplate><device/></configurationTemplate>")
    if (os.path.isfile(configTemplateFile)):
        dom = xml.dom.minidom.parse(configTemplateFile)
    configTemplateDom = dom.getElementsByTagName("template")
    i = 0
    templateHoverMenu = "<div id=\"chooseTemplateHover\" class=\"device-hover-menu\">"
    for tDom in configTemplateDom:
        i += 1
        templateHoverMenu += "<a href=\"#\" id=\"template" + str(
            i) + "\" name=\"" + tDom.getAttribute("id") + "\">" + tDom.getAttribute("name") + "</a>"

    if i == 0:
        templateHoverMenu += "<div style=\"padding: 10px 20px 10px 20px;color:#FFF;\">No Configuration Profile exist, Please add a profile first</div></div>"
    else:
        templateHoverMenu += "</div>"
    html.write(templateHoverMenu)


def apply_config_template(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    ipAddress = html.var("ipAddress").split(",")
    macAddress = html.var("macAddress").split(",")
    templateId = html.var("templateId")
    deviceType = html.var("deviceType").split(",")
    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)
    configString = ""
    aclVap1 = ""
    aclVap2 = ""
    aclVap3 = ""
    aclVap4 = ""
    aclVap5 = ""
    aclVap6 = ""
    aclVap7 = ""
    aclVap8 = ""
    if len(ipAddress) == len(macAddress) == len(deviceType):
        # create config file
        configurationTemplateFile = "/omd/sites/%s/share/check_mk/web/htdocs/xml/configurationTemplate.xml" % sitename
        configurationFile = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/config" % sitename
        acl1File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath0" % sitename
        acl2File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath1" % sitename
        acl3File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath2" % sitename
        acl4File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath3" % sitename
        acl5File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath4" % sitename
        acl6File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath5" % sitename
        acl7File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath6" % sitename
        acl8File = "/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig/acl/acl_ath7" % sitename

        apcfg = "/omd/sites/%s/share/check_mk/web/htdocs/download/apcfg" % sitename
        configTemplateDom = xml.dom.minidom.parseString(
            "<configurationTemplate></configurationTemplate>")
        if (os.path.isfile(configurationTemplateFile)):
            configTemplateDom = xml.dom.minidom.parse(
                configurationTemplateFile)
        templateDom = configTemplateDom.getElementsByTagName("template")
        for tDom in templateDom:
            if tDom.getAttribute("id") == templateId:
                # network
                network = tDom.getElementsByTagName("network")[0]
                if network.getAttribute("AP_HOSTNAME").strip() != "":
                    configString += "cfg -a AP_HOSTNAME=" + \
                                    network.getAttribute("AP_HOSTNAME") + "\n"

                if network.getAttribute("AP_NETMASK").strip() != "":
                    configString += "cfg -a AP_NETMASK=\"" + \
                                    network.getAttribute("AP_NETMASK") + "\"\n"

                if network.getAttribute("WAN_MODE").strip() != "":
                    configString += "cfg -a WAN_MODE=" + \
                                    network.getAttribute("WAN_MODE") + "\n"

                if network.getAttribute("IPGW").strip() != "":
                    configString += "cfg -a IPGW=\"" + \
                                    network.getAttribute("IPGW") + "\"\n"

                if network.getAttribute("PRIDNS").strip() != "":
                    configString += "cfg -a PRIDNS=\"" + \
                                    network.getAttribute("PRIDNS") + "\"\n"

                if network.getAttribute("SECDNS").strip() != "":
                    configString += "cfg -a SECDNS=\"" + \
                                    network.getAttribute("SECDNS") + "\"\n"

                # radio
                radio = tDom.getElementsByTagName("radio")[0]
                if radio.getAttribute("AP_STARTMODE").strip() != "":
                    configString += "cfg -a AP_STARTMODE=" + \
                                    radio.getAttribute("AP_STARTMODE") + "\n"

                if radio.getAttribute("MANAGEMENTVLAN").strip() != "":
                    configString += "cfg -a MANAGEMENTVLAN=" + \
                                    radio.getAttribute("MANAGEMENTVLAN") + "\n"

                if radio.getAttribute("ATH_countrycode").strip() != "":
                    configString += "cfg -a ATH_countrycode=" + \
                                    radio.getAttribute("ATH_countrycode") + "\n"

                if radio.getAttribute("AP_MAX_VAP").strip() != "":
                    configString += "cfg -a AP_MAX_VAP=" + \
                                    radio.getAttribute("AP_MAX_VAP") + "\n"

                if radio.getAttribute("AP_PRIMARY_CH").strip() != "":
                    configString += "cfg -a AP_PRIMARY_CH=" + \
                                    radio.getAttribute("AP_PRIMARY_CH") + "\n"

                if radio.getAttribute("AP_CHMODE").strip() != "":
                    configString += "cfg -a AP_CHMODE=" + \
                                    radio.getAttribute("AP_CHMODE") + "\n"

                if radio.getAttribute("AP_TXPOWER").strip() != "":
                    configString += "cfg -a AP_TXPOWER=" + \
                                    radio.getAttribute("AP_TXPOWER") + "\n"

                if radio.getAttribute("AP_DISTANCE").strip() != "":
                    configString += "cfg -a AP_DISTANCE=" + \
                                    radio.getAttribute("AP_DISTANCE") + "\n"

                if radio.getAttribute("AP_SLOTTIME").strip() != "":
                    configString += "cfg -a AP_SLOTTIME=" + \
                                    radio.getAttribute("AP_SLOTTIME") + "\n"

                if radio.getAttribute("AP_ACKTIMEOUT").strip() != "":
                    configString += "cfg -a AP_ACKTIMEOUT=" + \
                                    radio.getAttribute("AP_ACKTIMEOUT") + "\n"

                if radio.getAttribute("AP_CTSTIMEOUT").strip() != "":
                    configString += "cfg -a AP_CTSTIMEOUT=" + \
                                    radio.getAttribute("AP_CTSTIMEOUT") + "\n"

                if radio.getAttribute("SHORTGI").strip() != "":
                    configString += "cfg -a SHORTGI=" + \
                                    radio.getAttribute("SHORTGI") + "\n"

                if radio.getAttribute("AMPDUENABLE").strip() != "":
                    configString += "cfg -a AMPDUENABLE=" + \
                                    radio.getAttribute("AMPDUENABLE") + "\n"

                if radio.getAttribute("AMPDUFRAMES").strip() != "":
                    configString += "cfg -a AMPDUFRAMES=" + \
                                    radio.getAttribute("AMPDUFRAMES") + "\n"

                if radio.getAttribute("AMPDULIMIT").strip() != "":
                    configString += "cfg -a AMPDULIMIT=" + \
                                    radio.getAttribute("AMPDULIMIT") + "\n"

                if radio.getAttribute("AMPDUMIN").strip() != "":
                    configString += "cfg -a AMPDUMIN=" + \
                                    radio.getAttribute("AMPDUMIN") + "\n"

                if radio.getAttribute("CWMMODE").strip() != "":
                    configString += "cfg -a CWMMODE=" + \
                                    radio.getAttribute("CWMMODE") + "\n"

                if radio.getAttribute("TX_CHAINMASK").strip() != "":
                    configString += "cfg -a TX_CHAINMASK=" + \
                                    radio.getAttribute("TX_CHAINMASK") + "\n"

                if radio.getAttribute("RX_CHAINMASK").strip() != "":
                    configString += "cfg -a RX_CHAINMASK=" + \
                                    radio.getAttribute("RX_CHAINMASK") + "\n"

                if radio.getAttribute("AP_LONGDISTANCE").strip() != "":
                    configString += "cfg -a AP_LONGDISTANCE=" + \
                                    radio.getAttribute("AP_LONGDISTANCE") + "\n"

                if radio.getAttribute("WLAN_ON_BOOT").strip() != "":
                    configString += "cfg -a WLAN_ON_BOOT=" + \
                                    radio.getAttribute("WLAN_ON_BOOT") + "\n"

                if radio.getAttribute("AP_RADIO_ID").strip() != "":
                    configString += "cfg -a AP_RADIO_ID=" + \
                                    radio.getAttribute("AP_RADIO_ID") + "\n"

                if radio.getAttribute("PUREG").strip() != "":
                    configString += "cfg -a PUREG=" + \
                                    radio.getAttribute("PUREG") + "\n"

                if radio.getAttribute("PUREN").strip() != "":
                    configString += "cfg -a PUREN=" + \
                                    radio.getAttribute("PUREN") + "\n"

                if radio.getAttribute("TXQUEUELEN").strip() != "":
                    configString += "cfg -a TXQUEUELEN=" + \
                                    radio.getAttribute("TXQUEUELEN") + "\n"

                if radio.getAttribute("RATECTL").strip() != "":
                    configString += "cfg -a RATECTL=" + \
                                    radio.getAttribute("RATECTL") + "\n"

                if radio.getAttribute("MANRATE").strip() != "":
                    configString += "cfg -a MANRATE=" + \
                                    radio.getAttribute("MANRATE") + "\n"

                if radio.getAttribute("MANRETRIES").strip() != "":
                    configString += "cfg -a MANRETRIES=" + \
                                    radio.getAttribute("MANRETRIES") + "\n"

                if radio.getAttribute("AP_BEAC_INT").strip() != "":
                    configString += "cfg -a AP_BEAC_INT=" + \
                                    radio.getAttribute("AP_BEAC_INT") + "\n"

                if radio.getAttribute("APM_Enable").strip() != "":
                    configString += "cfg -a APM_Enable=" + \
                                    radio.getAttribute("APM_Enable") + "\n"
                    # vap
                vap = tDom.getElementsByTagName("vap")[0]

                if vap.getAttribute("AP_PRIMARY_KEY_0").strip() != "":
                    configString += "cfg -a AP_PRIMARY_KEY_0=" + \
                                    vap.getAttribute("AP_PRIMARY_KEY_0") + "\n"

                if vap.getAttribute("AP_WEP_MODE_0").strip() != "":
                    configString += "cfg -a AP_WEP_MODE_0=" + \
                                    vap.getAttribute("AP_WEP_MODE_0") + "\n"

                if vap.getAttribute("AP_DYN_VLAN").strip() != "":
                    configString += "cfg -a AP_DYN_VLAN=" + \
                                    vap.getAttribute("AP_DYN_VLAN") + "\n"

                if vap.getAttribute("WEPKEY_1").strip() != "":
                    configString += "cfg -a WEPKEY_1=" + \
                                    vap.getAttribute("WEPKEY_1") + "\n"

                if vap.getAttribute("WEPKEY_2").strip() != "":
                    configString += "cfg -a WEPKEY_2=" + \
                                    vap.getAttribute("WEPKEY_2") + "\n"

                if vap.getAttribute("WEPKEY_3").strip() != "":
                    configString += "cfg -a WEPKEY_3=" + \
                                    vap.getAttribute("WEPKEY_3") + "\n"

                if vap.getAttribute("WEPKEY_4").strip() != "":
                    configString += "cfg -a WEPKEY_4=" + \
                                    vap.getAttribute("WEPKEY_4") + "\n"

                if vap.getAttribute("ROOTAP_MAC").strip() != "":
                    configString += "cfg -a ROOTAP_MAC=\"" + \
                                    vap.getAttribute("ROOTAP_MAC") + "\"\n"

                # vap 1
                if vap.getAttribute("AP_SSID").strip() != "":
                    configString += "cfg -a AP_SSID=\"" + \
                                    vap.getAttribute("AP_SSID") + "\"\n"

                if vap.getAttribute("HIDE_SSID").strip() != "":
                    configString += "cfg -a HIDE_SSID=" + \
                                    vap.getAttribute("HIDE_SSID") + "\n"

                if vap.getAttribute("AP_VLAN").strip() != "":
                    configString += "cfg -a AP_VLAN=" + \
                                    vap.getAttribute("AP_VLAN") + "\n"

                if vap.getAttribute("VLAN_PRI").strip() != "":
                    configString += "cfg -a VLAN_PRI=" + \
                                    vap.getAttribute("VLAN_PRI") + "\n"

                if vap.getAttribute("AP_MODE").strip() != "":
                    configString += "cfg -a AP_MODE=" + \
                                    vap.getAttribute("AP_MODE") + "\n"

                if vap.getAttribute("AP_SECMODE").strip() != "":
                    configString += "cfg -a AP_SECMODE=" + \
                                    vap.getAttribute("AP_SECMODE") + "\n"

                if vap.getAttribute("AP_SECFILE").strip() != "":
                    configString += "cfg -a AP_SECFILE=" + \
                                    vap.getAttribute("AP_SECFILE") + "\n"

                if vap.getAttribute("AP_BEAC_INT").strip() != "":
                    configString += "cfg -a AP_BEAC_INT=" + \
                                    vap.getAttribute("AP_BEAC_INT") + "\n"

                if vap.getAttribute("AP_RTS_THR").strip() != "":
                    configString += "cfg -a AP_RTS_THR=" + \
                                    vap.getAttribute("AP_RTS_THR") + "\n"

                if vap.getAttribute("AP_FRAG_THR").strip() != "":
                    configString += "cfg -a AP_FRAG_THR=" + \
                                    vap.getAttribute("AP_FRAG_THR") + "\n"

                if vap.getAttribute("AP_WPA").strip() != "":
                    configString += "cfg -a AP_WPA=" + \
                                    vap.getAttribute("AP_WPA") + "\n"

                if vap.getAttribute("AP_CYPHER").strip() != "":
                    configString += "cfg -a AP_CYPHER=" + \
                                    vap.getAttribute("AP_CYPHER") + "\n"

                if vap.getAttribute("AP_WPA_GROUP_REKEY").strip() != "":
                    configString += "cfg -a AP_WPA_GROUP_REKEY=" + \
                                    vap.getAttribute("AP_WPA_GROUP_REKEY") + "\n"

                if vap.getAttribute("AP_WPA_GMK_REKEY").strip() != "":
                    configString += "cfg -a AP_WPA_GMK_REKEY=" + \
                                    vap.getAttribute("AP_WPA_GMK_REKEY") + "\n"

                if vap.getAttribute("AP_WEP_REKEY").strip() != "":
                    configString += "cfg -a AP_WEP_REKEY=" + \
                                    vap.getAttribute("AP_WEP_REKEY") + "\n"

                if vap.getAttribute("PSK_KEY").strip() != "":
                    configString += "cfg -a PSK_KEY=" + \
                                    vap.getAttribute("PSK_KEY") + "\n"

                if vap.getAttribute("AP_RSN_ENA_PREAUTH").strip() != "":
                    configString += "cfg -a AP_RSN_ENA_PREAUTH=" + \
                                    vap.getAttribute("AP_RSN_ENA_PREAUTH") + "\n"

                if vap.getAttribute("AP_WPA_PREAUTH_IF").strip() != "":
                    configString += "cfg -a AP_WPA_PREAUTH_IF=" + \
                                    vap.getAttribute("AP_WPA_PREAUTH_IF") + "\n"

                if vap.getAttribute("AP_EAP_REAUTH_PER").strip() != "":
                    configString += "cfg -a AP_EAP_REAUTH_PER=" + \
                                    vap.getAttribute("AP_EAP_REAUTH_PER") + "\n"

                if vap.getAttribute("AP_AUTH_SERVER").strip() != "":
                    configString += "cfg -a AP_AUTH_SERVER=" + \
                                    vap.getAttribute("AP_AUTH_SERVER") + "\n"

                if vap.getAttribute("AP_AUTH_PORT").strip() != "":
                    configString += "cfg -a AP_AUTH_PORT=" + \
                                    vap.getAttribute("AP_AUTH_PORT") + "\n"

                if vap.getAttribute("AP_AUTH_SECRET").strip() != "":
                    configString += "cfg -a AP_AUTH_SECRET=" + \
                                    vap.getAttribute("AP_AUTH_SECRET") + "\n"

                # vap 2,3,4,5,5,6,7,8
                for j in range(2, 9):
                    if vap.getAttribute("AP_SSID_" + str(j)).strip() != "":
                        configString += "cfg -a AP_SSID_" + str(
                            j) + "=\"" + vap.getAttribute("AP_SSID_" + str(j)) + "\"\n"

                    if vap.getAttribute("HIDE_SSID_" + str(j)).strip() != "":
                        configString += "cfg -a HIDE_SSID_" + str(
                            j) + "=" + vap.getAttribute("HIDE_SSID_" + str(j)) + "\n"

                    if vap.getAttribute("AP_VLAN_" + str(j)).strip() != "":
                        configString += "cfg -a AP_VLAN_" + str(
                            j) + "=" + vap.getAttribute("AP_VLAN_" + str(j)) + "\n"

                    if vap.getAttribute("VLAN_PRI_" + str(j)).strip() != "":
                        configString += "cfg -a VLAN_PRI_" + str(
                            j) + "=" + vap.getAttribute("VLAN_PRI_" + str(j)) + "\n"

                    if vap.getAttribute("AP_MODE_" + str(j)).strip() != "":
                        configString += "cfg -a AP_MODE_" + str(
                            j) + "=" + vap.getAttribute("AP_MODE_" + str(j)) + "\n"

                    if vap.getAttribute("AP_SECMODE_" + str(j)).strip() != "":
                        configString += "cfg -a AP_SECMODE_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_SECMODE_" + str(j)) + "\n"

                    if vap.getAttribute("AP_SECFILE_" + str(j)).strip() != "":
                        configString += "cfg -a AP_SECFILE_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_SECFILE_" + str(j)) + "\n"

                    if vap.getAttribute("AP_RTS_THR_" + str(j)).strip() != "":
                        configString += "cfg -a AP_RTS_THR_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_RTS_THR_" + str(j)) + "\n"

                    if vap.getAttribute("AP_FRAG_THR_" + str(j)).strip() != "":
                        configString += "cfg -a AP_FRAG_THR_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_FRAG_THR_" + str(j)) + "\n"

                    if vap.getAttribute("AP_WPA_" + str(j)).strip() != "":
                        configString += "cfg -a AP_WPA_" + str(
                            j) + "=" + vap.getAttribute("AP_WPA_" + str(j)) + "\n"

                    if vap.getAttribute("AP_CYPHER_" + str(j)).strip() != "":
                        configString += "cfg -a AP_CYPHER_" + str(
                            j) + "=" + vap.getAttribute("AP_CYPHER_" + str(j)) + "\n"

                    if vap.getAttribute("AP_WPA_GROUP_REKEY_" + str(j)).strip() != "":
                        configString += "cfg -a AP_WPA_GROUP_REKEY_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_WPA_GROUP_REKEY_" + str(j)) + "\n"

                    if vap.getAttribute("AP_WPA_GMK_REKEY_" + str(j)).strip() != "":
                        configString += "cfg -a AP_WPA_GMK_REKEY_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_WPA_GMK_REKEY_" + str(j)) + "\n"

                    if vap.getAttribute("AP_WEP_REKEY_" + str(j)).strip() != "":
                        configString += "cfg -a AP_WEP_REKEY_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_WEP_REKEY_" + str(j)) + "\n"

                    if vap.getAttribute("PSK_KEY_" + str(j)).strip() != "":
                        configString += "cfg -a PSK_KEY_" + str(
                            j) + "=" + vap.getAttribute("PSK_KEY_" + str(j)) + "\n"

                    if vap.getAttribute("AP_RSN_ENA_PREAUTH_" + str(j)).strip() != "":
                        configString += "cfg -a AP_RSN_ENA_PREAUTH_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_RSN_ENA_PREAUTH_" + str(j)) + "\n"

                    if vap.getAttribute("AP_WPA_PREAUTH_IF_" + str(j)).strip() != "":
                        configString += "cfg -a AP_WPA_PREAUTH_IF_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_WPA_PREAUTH_IF_" + str(j)) + "\n"

                    if vap.getAttribute("AP_EAP_REAUTH_PER_" + str(j)).strip() != "":
                        configString += "cfg -a AP_EAP_REAUTH_PER_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_EAP_REAUTH_PER_" + str(j)) + "\n"

                    if vap.getAttribute("AP_AUTH_SERVER_" + str(j)).strip() != "":
                        configString += "cfg -a AP_AUTH_SERVER_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_AUTH_SERVER_" + str(j)) + "\n"

                    if vap.getAttribute("AP_AUTH_PORT_" + str(j)).strip() != "":
                        configString += "cfg -a AP_AUTH_PORT_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_AUTH_PORT_" + str(j)) + "\n"

                    if vap.getAttribute("AP_AUTH_SECRET_" + str(j)).strip() != "":
                        configString += "cfg -a AP_AUTH_SECRET_" + \
                                        str(j) + "=" + vap.getAttribute(
                            "AP_AUTH_SECRET_" + str(j)) + "\n"

                # acl
                acl = tDom.getElementsByTagName("acl")[0]
                if acl.getAttribute("ACL_VAP").strip() != "":
                    configString += "cfg -a ACL_VAP=" + \
                                    acl.getAttribute("ACL_VAP") + "\n"

                if acl.getAttribute("ACLTYPE_VAP").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP=" + \
                                    acl.getAttribute("ACLTYPE_VAP") + "\n"

                if acl.getAttribute("ACL_VAP_2").strip() != "":
                    configString += "cfg -a ACL_VAP_2=" + \
                                    acl.getAttribute("ACL_VAP_2") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_2").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_2=" + \
                                    acl.getAttribute("ACLTYPE_VAP_2") + "\n"

                if acl.getAttribute("ACL_VAP_3").strip() != "":
                    configString += "cfg -a ACL_VAP_3=" + \
                                    acl.getAttribute("ACL_VAP_3") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_3").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_3=" + \
                                    acl.getAttribute("ACLTYPE_VAP_3") + "\n"

                if acl.getAttribute("ACL_VAP_4").strip() != "":
                    configString += "cfg -a ACL_VAP_4=" + \
                                    acl.getAttribute("ACL_VAP_4") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_4").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_4=" + \
                                    acl.getAttribute("ACLTYPE_VAP_4") + "\n"

                if acl.getAttribute("ACL_VAP_5").strip() != "":
                    configString += "cfg -a ACL_VAP_5=" + \
                                    acl.getAttribute("ACL_VAP_5") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_5").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_5=" + \
                                    acl.getAttribute("ACLTYPE_VAP_5") + "\n"

                if acl.getAttribute("ACL_VAP_6").strip() != "":
                    configString += "cfg -a ACL_VAP_6=" + \
                                    acl.getAttribute("ACL_VAP_6") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_6").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_6=" + \
                                    acl.getAttribute("ACLTYPE_VAP_6") + "\n"

                if acl.getAttribute("ACL_VAP_7").strip() != "":
                    configString += "cfg -a ACL_VAP_7=" + \
                                    acl.getAttribute("ACL_VAP_7") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_7").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_7=" + \
                                    acl.getAttribute("ACLTYPE_VAP_7") + "\n"

                if acl.getAttribute("ACL_VAP_8").strip() != "":
                    configString += "cfg -a ACL_VAP_8=" + \
                                    acl.getAttribute("ACL_VAP_8") + "\n"

                if acl.getAttribute("ACLTYPE_VAP_8").strip() != "":
                    configString += "cfg -a ACLTYPE_VAP_8=" + \
                                    acl.getAttribute("ACLTYPE_VAP_8") + "\n"

                aclmac1 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist1")[0].childNodes))
                aclVap1 = "\n".join(aclmac1)
                aclmac2 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist2")[0].childNodes))
                aclVap2 = "\n".join(aclmac2)
                aclmac3 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist3")[0].childNodes))
                aclVap3 = "\n".join(aclmac3)
                aclmac4 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist4")[0].childNodes))
                aclVap4 = "\n".join(aclmac4)
                aclmac5 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist5")[0].childNodes))
                aclVap5 = "\n".join(aclmac5)
                aclmac6 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist6")[0].childNodes))
                aclVap6 = "\n".join(aclmac6)
                aclmac7 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist7")[0].childNodes))
                aclVap7 = "\n".join(aclmac7)
                aclmac8 = re.split("[,\n ]", getText(
                    acl.getElementsByTagName("maclist8")[0].childNodes))
                aclVap8 = "\n".join(aclmac8)

                # services
                services = tDom.getElementsByTagName("services")[0]

                if services.getAttribute("AP_UPNP").strip() != "":
                    configString += "cfg -a AP_UPNP=" + \
                                    services.getAttribute("AP_UPNP") + "\n"

                if services.getAttribute("AP_SYSLOG").strip() != "":
                    configString += "cfg -a AP_SYSLOG=" + \
                                    services.getAttribute("AP_SYSLOG") + "\n"

                if services.getAttribute("AP_SYSLOG_IP").strip() != "":
                    configString += "cfg -a AP_SYSLOG_IP=\"" + \
                                    services.getAttribute("AP_SYSLOG_IP") + "\"\n"

                if services.getAttribute("SYSLOG_PORT").strip() != "":
                    configString += "cfg -a SYSLOG_PORT=" + \
                                    services.getAttribute("SYSLOG_PORT") + "\n"

                if services.getAttribute("SNMP_Enable").strip() != "":
                    configString += "cfg -a SNMP_Enable=" + \
                                    services.getAttribute("SNMP_Enable") + "\n"

                if services.getAttribute("SNMP_Comm").strip() != "":
                    configString += "cfg -a SNMP_Comm=" + \
                                    services.getAttribute("SNMP_Comm") + "\n"

                if services.getAttribute("SNMP_Location").strip() != "":
                    configString += "cfg -a SNMP_Location=\"" + \
                                    services.getAttribute("SNMP_Location") + "\"\n"

                if services.getAttribute("SNMP_Contact").strip() != "":
                    configString += "cfg -a SNMP_Contact=\"" + \
                                    services.getAttribute("SNMP_Contact") + "\"\n"

                if services.getAttribute("DHCP_SER").strip() != "":
                    configString += "cfg -a DHCP_SER=" + \
                                    services.getAttribute("DHCP_SER") + "\n"

                if services.getAttribute("DHCP_SIP").strip() != "":
                    configString += "cfg -a DHCP_SIP=\"" + \
                                    services.getAttribute("DHCP_SIP") + "\"\n"

                if services.getAttribute("DHCP_EIP").strip() != "":
                    configString += "cfg -a DHCP_EIP=\"" + \
                                    services.getAttribute("DHCP_EIP") + "\"\n"

                if services.getAttribute("DHCP_NM").strip() != "":
                    configString += "cfg -a DHCP_NM=\"" + \
                                    services.getAttribute("DHCP_NM") + "\"\n"

                if services.getAttribute("DHCP_LEASE").strip() != "":
                    configString += "cfg -a DHCP_LEASE=" + \
                                    services.getAttribute("DHCP_LEASE") + "\n"

                if services.getAttribute("TimeZone").strip() != "":
                    configString += "cfg -a TimeZone=\"" + \
                                    services.getAttribute("TimeZone") + "\"\n"

                if services.getAttribute("NTP_Enable").strip() != "":
                    configString += "cfg -a NTP_Enable=" + \
                                    services.getAttribute("NTP_Enable") + "\n"

                if services.getAttribute("NTPSERVERIP").strip() != "":
                    configString += "cfg -a NTPSERVERIP=\"" + \
                                    services.getAttribute("NTPSERVERIP") + "\"\n"
                break

        acl1obj = open(acl1File, "w")
        acl1obj.write(aclVap1)
        acl1obj.close()
        acl2obj = open(acl2File, "w")
        acl2obj.write(aclVap2)
        acl2obj.close()
        acl3obj = open(acl3File, "w")
        acl3obj.write(aclVap3)
        acl3obj.close()
        acl4obj = open(acl4File, "w")
        acl4obj.write(aclVap4)
        acl4obj.close()
        acl5obj = open(acl5File, "w")
        acl5obj.write(aclVap5)
        acl5obj.close()
        acl6obj = open(acl6File, "w")
        acl6obj.write(aclVap6)
        acl6obj.close()
        acl7obj = open(acl7File, "w")
        acl7obj.write(aclVap7)
        acl7obj.close()
        acl8obj = open(acl8File, "w")
        acl8obj.write(aclVap8)
        acl8obj.close()

        for i in range(0, len(ipAddress)):
            fobj = open(configurationFile, "w")
            fobj.write(
                configString + "cfg -a MACADD=\"" + macAddress[i] + "\"")
            fobj.close()

            tar = tarfile.open(apcfg, "w")
            tar.add("/omd/sites/%s/share/check_mk/web/htdocs/download/11nconfig" %
                    sitename, arcname="11nconfig")
            tar.close()
            args = ["-l", deviceType[i], "-f", "2", "-a", "0",
                    "-m", macAddress[i], "-t", apcfg, "-P", "54321"]
            command = [sdmcFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]
        html.write("0")
    else:
        html.write("1")


def factory_reset(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    deviceType = html.var("deviceType")
    mac = html.var("mac")
    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)
    args = ["-l", deviceType, "-r", "-m", mac, "-P", "54321"]
    command = [sdmcFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    html.write("0")


def set_ip(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    oldIpAddress = html.var("oldIpAddress").split(",")
    newIpAddress = html.var("newIpAddress").split(",")
    macAddress = html.var("macAddress").split(",")
    deviceType = html.var("deviceType").split(",")
    localNetmask = html.var("localNetmask")
    gatewayIp = html.var("gatewayIp")
    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)

    if len(oldIpAddress) == len(newIpAddress) == len(macAddress) == len(deviceType):
        for i in range(0, len(oldIpAddress)):
            if oldIpAddress[i] != newIpAddress[i]:
                args = ["-l", deviceType[i], "-c", "-m", macAddress[i], "-i",
                        newIpAddress[i], "-n", localNetmask, "-g", gatewayIp, "-P", "54321"]
                command = [sdmcFile]
                command.extend(args)
                pipe = subprocess.Popen(
                    command, stdout=subprocess.PIPE).communicate()[0]
        html.write("0")
    else:
        html.write("1")

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


def image_upload(req):
    """

    @param req:
    @return:
    """
    global html
    html = req
    sitename = __file__.split("/")[3]
    filePath = "/omd/sites/%s/share/check_mk/web/htdocs/download/image.img" % (
        sitename)
    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)
    form = util.FieldStorage(req.req, keep_blank_values=1)
    upfile = form.getlist('file')[0]
    filename = upfile.filename
    filedata = upfile.value
    fobj = open(filePath, 'w')  # 'w' is for 'write'
    fobj.write(filedata)
    fobj.close()
    deviceMac = form.get("deviceMac", "")
    deviceTy = form.get("deviceTy", "")
    mac = deviceMac.split(",")
    ty = deviceTy.split(",")
    time.sleep(10)
    # html.write(",".join(mac))
    # html.write(",".join(ty))
    if len(mac) == len(ty):
        for i in range(0, len(mac)):
            args = ["-l", ty[i], "-f", "0", "-a", "0", "-m",
                    mac[i], "-t", filePath, "-P", "54321"]
            command = [sdmcFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]
            html.write("<p style=\"font-size:12px;color:#111;width:95%;\">Device " + str(
                i + 1) + ": " + pipe + "</p>")
            time.sleep(5)
        html.write(
            "<script type=\"text/javascript\">alert(\"Image Uploaded successfully. please wait for 5 min device is rebooting.\"); window.location=\"manage_host_configuration.py\";</script>")
    else:
        html.write(
            "<script type=\"text/javascript\">alert(\"There is some error, Please try again.\");window.location=\"manage_host_configuration.py\";</script>")
    return apache.OK

############################################### End Manage Configuration #

############################################### Update ACL ###############


def update_acl(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    html.new_header("Update ACL")
    html.write(
        "<script type=\"text/javascript\" src=\"js/unmp/main/update_acl.js\"></script>\n")
    html.write(
        "<script type=\"text/javascript\" src=\"facebox/facebox.js\"></script>\n")
    html.write(
        "<link type=\"text/css\" href=\"css/style.css\" rel=\"stylesheet\"></link>\n")
    html.write(
        "<link type=\"text/css\" href=\"facebox/facebox.css\" rel=\"stylesheet\"></link>\n")

    # create tabs for manage configuration
    html.write("<div class=\"tab-yo\">")
    html.write("<div class=\"tab-head\">")
    html.write("<h2>Update ACL")
    html.write("</h2>")
    html.write("</div>")

    # acl division
    html.write("<div id=\"aclDiv\" class=\"tab-body discoveryDetailsBody\">")
    html.write("<div id=\"form1\">")
    html.write("<div style=\"margin: 20px;\">")
    html.write(
        "<form id=\"aclForm\" enctype=\"multipart/form-data\" method=\"post\" action=\"upload_mac_address_file.py\">")
    html.write("<table width=\"100%\">")
    html.write("<colgroup><col width='20%'/><col width='80%'/></colgroup>")
    html.write(
        "<tr><td>Add a MAC Address</td><td><input type='text' name='mac' id='mac' value='' onkeypress=\"return macCheck(event)\"/> <input type=\"button\" onclick=\"addMacAddress()\" value=\"Add\"/></td></tr>")
    html.write(
        "<tr><td>MAC Address File</td><td><input type='file' name='macFile' id='macFile'/> <input type=\"submit\" value=\"Upload\"/><br/><span style=\"color:#555; font-size:9px;\">(Use blankspace or comma or newline as seperator between MACs)</span></td></tr>")
    html.write("</table>")
    html.write("</form>")
    html.write("</div>")
    html.write("<div style=\"margin-top: 20px;\" id=\"macGrid\">")
    html.write("</div>")
    html.write("</div>")
    html.write("</div>")
    # end acl division

    html.write("</div>")
    html.footer()

    # image uploader div
    html.write("<div class=\"loading\"></div>")
    html.write(
        "<div id=\"selectApDiv\" style=\"min-width:500px;height:400px;z-index:2000;position:absolute;top:100px; left:10%;display:none;overflow-x:hidden;overflow-y:auto;\" >")
    html.write("</div>")


def list_of_mac_address(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    i = 0
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # prepare SQL query to get Mac Address
    sql = "SELECT * FROM macaddress"

    cursor.execute(sql)
    macList = cursor.fetchall()
    db.close()

    tableString = "<div><table class=\"addform\">"
    tableString += "<colgroup><col width='3%'/><col width='90%'/><col width='5%'/></colgroup><tbody>"
    tableString += "<tr><th align=\"left\"><input type=\"checkbox\" id=\"allMac\" name=\"allMac\"/></th><th align=\"left\">Mac Address</th><th align=\"left\">Delete</th></tr>"
    for mac in macList:
        i += 1
        tableString += "<tr><td><input type=\"checkbox\" mac=\"" + mac[1] + "\" id=\"macAddressValue" + str(
            i) + "\" name=\"macAddressValue\"/></td><td style=\"vertical-align:middle;\">" + mac[
                           1] + "</td><td align=\"center\"><img onclick=\"deleteMacAddress('" + mac[
                           1] + "')\" class=\"imgbutton\" title=\"Delete Mac Address\" alt=\"delete\" src=\"images/delete16.png\"></td></tr>"
    if i == 0:
        tableString = "<table class=\"addform\"><tr><td><b> No Mac Address in the List</b></td></tr></table>"
    else:
        tableString += "<tr><td colspan=\"3\"> &nbsp;</td></tr><tr><td colspan=\"3\"><input type=\"button\" onclick=\"selectApToApply();\" value=\"Select AP's to Apply\"/><input type=\"hidden\" id=\"totalMac\" name=\"totalMac\" value=\"" + str(
            i) + \
                       "\"/></td></tr></tbody></table></div>"
    html.write(tableString)


def delete_mac_address(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    mac = html.var("mac")
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")

    try:
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # prepare SQL query to delete Mac Address
        sql = "DELETE FROM macaddress WHERE address = '%s'" % (mac)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    html.write("0")


def add_mac_address(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    macAdd = html.var("mac").strip()
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")

    totalMac = 0
    try:
        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # prepare SQL query to add Mac Address
        sql = "SELECT COUNT(*) FROM macaddress WHERE address = '%s'" % (macAdd)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            totalMac = row[0]

        if totalMac != 0:
            html.write("1")
        else:
            # prepare SQL query to add Mac Address
            sql = "INSERT INTO macaddress (address) VALUES('%s')" % (macAdd)
            cursor.execute(sql)
            db.commit()
            html.write("0")
    except:
        db.rollback()
        html.write("2")


def upload_mac_address_file(req):
    """

    @param req:
    """
    sitename = __file__.split("/")[3]
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "root", "nms")

    form = util.FieldStorage(req.req, keep_blank_values=1)
    upfile = form.getlist('macFile')[0]
    filename = upfile.filename
    filedata = re.split("[,\n ]", upfile.value)
    try:
        for macAdd in filedata:
            macAdd = macAdd.strip().upper()
            if validate_mac_address(macAdd) == 0:
                totalMac = 0
                # prepare a cursor object using cursor() method
                cursor = db.cursor()

                # prepare SQL query to add Mac Address
                sql = "SELECT COUNT(*) FROM macaddress WHERE address = '%s'" % (
                    macAdd)
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    totalMac = row[0]

                if totalMac == 0:
                    # prepare SQL query to add Mac Address
                    sql = "INSERT INTO macaddress (address) VALUES('%s')" % (
                        macAdd)
                    cursor.execute(sql)
                    db.commit()
    except:
        db.rollback()
    req.write(
        "<script type=\"text/javascript\">window.location=\"update_acl.py\";</script>")


def validate_mac_address(mac):
    """

    @param mac:
    @return:
    """
    mac = mac.upper()
    macArray = mac.split(":")
    if mac != "":
        if mac == "FF:FF:FF:FF:FF:FF" or mac == "00:00:00:00:00:00":
            return 1
        else:
            if len(macArray) != 6:
                return 1
            else:
                for j in range(0, 6):
                    if len(macArray[j]) != 2:
                        return 1
                return 0
    else:
        return 1


def select_ap_to_apply_mac(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    deviceType = "1"
    timeOut = "5"
    sdmcString = "AP"

    sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (sitename)
    args = ["--discovery", "-l", deviceType, "-o", timeOut, "-P", "54321"]
    command = [sdmcFile]
    command.extend(args)
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]

    #===================================================================================================
    # Output string of sdm utlity
    #     pipe = """
    #	Discovery Time less than or equal to 5 seconds,setting default time 5 seconds
    #
    #
    # DeviceType: AP
    #
    # Sl.No, IPAddress, MacAddress, SSID, HostName, FirmwareVersion, BootloaderVersion
    # 0, 192.168.5.31, 00:50:c2:bc:c8:02, VVDN_AP, 11nAP, 1.1.1.0-347, 0.0.4
    # 0, 192.168.5.33, 00:50:c2:bc:c8:03, VVDN_AP, 12nAP, 1.1.1.0-347, 0.0.4
    #"""
    #=========================================================================
    outputStringArray = pipe.split("\n")  # split sdmc output string
    tableString = """
<div><table width=\"100%\" class=\"addform\">
	<tbody>
<tr><th colspan=\"3\"> Choose Access Points</th><th colspan=\"2\"><input checked=\"checked\" type=\"checkbox\" id=\"sameUnP\" name=\"sameUnP\"/> User name and Password same for all</th></tr>

		<tr>
			<th>
				<input type=\"checkbox\" id=\"allAP\" name=\"allAP\" value=\"all\" style=\"margin-left:10px;\"/>
			</th>
			<th>IP Address</th>
			<th>Name</th>
			<th>Username</th>
			<th>Password</th>
		</tr>
"""
    i = 0
    totalHost = 0
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
                totalHost += 1
                # html.write("Device type: " + sdmcString + " Value: "+ outputString + "\n")
                # Device type: AP Value:
                # 0,192.168.5.31,00:50:c2:bc:c8:02,VVDN_AP,11nAP,1.1.1.0-347,0.0.4
                hostDetails = outputString.split(", ")
                tableString += "<tr>"
                tableString += "<td><input type=\"checkbox\" id=\"" + hostDetails[2] + \
                               "\" ip=\"" + hostDetails[1] + \
                               "\" name=\"host\" value=\"" + \
                               hostDetails[1] + "\"/></td>"
                tableString += "<td>" + hostDetails[1] + "</td>"
                tableString += "<td>" + hostDetails[4] + "</td>"
                tableString += "<td><input type=\"text\" name=\"hostUsername\" value=\"admin\" ip=\"" + hostDetails[
                    1] + "_user\"/></td>"
                tableString += "<td><input type=\"password\" name=\"hostPassword\" value=\"password\" ip=\"" + \
                               hostDetails[1] + "_pass\"/></td>"
                tableString += "</tr>"

    if totalHost == 0:
        tableString = "<table width=\"100%\" class=\"addform\"><tbody><tr><th> Choose Access Point</th></tr><tr><td>No Device Exist</td></tr><tr><td><input type=\"button\" value=\"Cancel\" onclick=\"applyCancel()\"/></td></tr>"
    else:
        tableString += """<tr><td colspan=\"5\"><input type=\"checkbox\" checked=\"checked\" id=\"vap1\" name=\"vapnum\" value=\"1\"/> vap1 <input type=\"checkbox\" id=\"vap2\" name=\"vapnum\" value=\"2\"/>vap2 <input type=\"checkbox\" id=\"vap3\" name=\"vapnum\" value=\"3\"/>vap3 <input type=\"checkbox\" id=\"vap4\" name=\"vapnum\" value=\"4\"/>vap4 <input type=\"checkbox\" id=\"vap5\" name=\"vapnum\" value=\"5\"/>vap5 <input type=\"checkbox\" id=\"vap6\" name=\"vapnum\" value=\"6\"/>vap6 <input type=\"checkbox\" id=\"vap7\" name=\"vapnum\" value=\"7\"/>vap7 <input type=\"checkbox\" id=\"vap8\" name=\"vapnum\" value=\"8\"/>vap8 </td></tr>

<tr><td colspan=\"5\" align=\"left\" style=\"padding:5px;\"><input type=\"radio\" name=\"ACLTYPE_VAP\" id=\"nochange\" value=\"-1\" checked /> <label for=\"nochange\">No Change</label><input type=\"radio\" name=\"ACLTYPE_VAP\" id=\"allow\" value=\"1\" /> <label for=\"allow\">Allow</label> <input type=\"radio\" name=\"ACLTYPE_VAP\" id=\"deny\" value=\"0\"/><label for=\"deny\">Deny</label></td></tr>

<tr><td colspan=\"5\" align=\"left\" style=\"padding:5px;\"><input type=\"radio\" name=\"actionForMac\" id=\"appendmac\" value=\"append\" checked /> <label for=\"appendmac\">Append MacAddress</label> <input type=\"radio\" name=\"actionForMac\" id=\"replacemac\" value=\"replace\"/><label for=\"replacemac\"> Replace MacAddress</label></td></tr><tr><td colspan=\"5\" align=\"left\" style=\"padding:5px;\"><input type=\"button\" onclick=\"applyAP();\" value=\"Add Selected MacAddress\"/> <input type=\"button\" onclick=\"deleteMacFromAP();\" value=\"Delete Selected MacAddress\"/> <input type=\"button\" value=\"Cancel\" onclick=\"applyCancel()\"/></td></tr>"""

    tableString += "<input type=\"hidden\" name=\"totalHost\" value=\"" + str(
        totalHost) + "\"/></tbody></table></div>"
    html.write(tableString)


def http_request_for_ap(h):
    """

    @param h:
    """
    global html
    html = h
    sitename = __file__.split("/")[3]
    username = html.var("username")
    password = html.var("password")
    url = html.var("url")
    ap = html.var("ap")
    para = html.var("para").split(",")
    arg = html.var("arg").split(",")
    acltype = html.var("acltype")
    restart = html.var("restart")
    deviceType = "1"
    tempUrl = "?"
    i = 0
    for i in range(0, len(para)):
        if i > 0:
            tempUrl += "&"
        tempUrl += para[i] + "=" + arg[i]
    i += 1
    for j in range(i, len(arg)):
        tempUrl += "," + arg[j]

    apurl = "http://" + ap + url + tempUrl

    try:
        req = urllib2.Request(apurl)
        auth_string = base64.encodestring("%s:%s" % (username, password))
        req.add_header("Authorization", "Basic %s" % auth_string)
        f = urllib2.urlopen(req)
        response = f.read()
        acl_vap = "ACL_VAP"
        acl_type = "ACLTYPE_VAP"
        if acltype != "-1":
            if int(arg[1]) > 1:
                acl_vap += "_" + arg[1]
                acl_type += "_" + arg[1]
            sdmcFile = "/omd/sites/%s/share/check_mk/web/htdocs/sdm" % (
                sitename)
            args = ["-l", deviceType, "-e", "0", "-a", "1",
                    "-i", ap, "-N", acl_vap, "-V", "1"]
            command = [sdmcFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]

            args = ["-l", deviceType, "-e", "0", "-a", "1",
                    "-i", ap, "-N", acl_type, "-V", acltype]
            command = [sdmcFile]
            command.extend(args)
            pipe = subprocess.Popen(
                command, stdout=subprocess.PIPE).communicate()[0]

            if restart == "1":
                args = ["-l", deviceType, "-e", "1", "-a",
                        "1", "-i", ap, "-N", "acl_cmd -c"]
                command = [sdmcFile]
                command.extend(args)
                pipe = subprocess.Popen(
                    command, stdout=subprocess.PIPE).communicate()[0]

                args = ["-l", deviceType, "-e", "1", "-a",
                        "1", "-i", ap, "-N", "reboot"]
                command = [sdmcFile]
                command.extend(args)
                pipe = subprocess.Popen(
                    command, stdout=subprocess.PIPE).communicate()[0]
        if str(response).find("error") != -1:
            html.write("-1")
        else:
            html.write("0")
    # except urllib2.URLError, e:
    #     html.write("-1")	# no network connection
    except urllib2.HTTPError, e:
        html.write(str(e.code))  # send http error code

#    100: ('Continue', 'Request received, please continue'),
#    101: ('Switching Protocols',
#          'Switching to new protocol; obey Upgrade header'),
#
#    200: ('OK', 'Request fulfilled, document follows'),
#    201: ('Created', 'Document created, URL follows'),
#    202: ('Accepted',
#          'Request accepted, processing continues off-line'),
#    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
#    204: ('No Content', 'Request fulfilled, nothing follows'),
#    205: ('Reset Content', 'Clear input form for further input.'),
#    206: ('Partial Content', 'Partial content follows.'),
#    300: ('Multiple Choices',
#          'Object has several resources -- see URI list'),
#    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
#    302: ('Found', 'Object moved temporarily -- see URI list'),
#    303: ('See Other', 'Object moved -- see Method and URL list'),
#    304: ('Not Modified',
#          'Document has not changed since given time'),
#    305: ('Use Proxy',
#          'You must use proxy specified in Location to access this '
#          'resource.'),
#    307: ('Temporary Redirect',
#          'Object moved temporarily -- see URI list'),
#    400: ('Bad Request',
#          'Bad request syntax or unsupported method'),
#    401: ('Unauthorized',
#          'No permission -- see authorization schemes'),
#    402: ('Payment Required',
#          'No payment -- see charging schemes'),
#    403: ('Forbidden',
#          'Request forbidden -- authorization will not help'),
#    404: ('Not Found', 'Nothing matches the given URI'),
#    405: ('Method Not Allowed',
#          'Specified method is invalid for this server.'),
#    406: ('Not Acceptable', 'URI not available in preferred format.'),
#    407: ('Proxy Authentication Required', 'You must authenticate with '
#          'this proxy before proceeding.'),
#    408: ('Request Timeout', 'Request timed out; try again later.'),
#    409: ('Conflict', 'Request conflict.'),
#    410: ('Gone',
#          'URI no longer exists and has been permanently removed.'),
#    411: ('Length Required', 'Client must specify Content-Length.'),
#    412: ('Precondition Failed', 'Precondition in headers is false.'),
#    413: ('Request Entity Too Large', 'Entity is too large.'),
#    414: ('Request-URI Too Long', 'URI is too long.'),
#    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
#    416: ('Requested Range Not Satisfiable',
#          'Cannot satisfy request range.'),
#    417: ('Expectation Failed',
#          'Expect condition could not be satisfied.'),
#    500: ('Internal Server Error', 'Server got itself in trouble'),
#    501: ('Not Implemented',
#          'Server does not support this operation'),
#    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
#    503: ('Service Unavailable',
#          'The server cannot process the request due to a high load'),
#    504: ('Gateway Timeout',
#          'The gateway server did not receive a timely response'),
#    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),


############################################# End Update ACL #############
