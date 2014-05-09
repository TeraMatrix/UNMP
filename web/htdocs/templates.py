#!/usr/bin/python2.6

import os
import xml.dom.minidom
from lib import *

################################# Manage Service Template ################


def page_manage_service_template(h):
    global html
    html = h
    css_list = []
    js_list = ["js/unmp/main/templates.js"]
    html.new_header("Manage Service Template", "", "", css_list, js_list)
    html.write(
        "<div class=\"main-title\" style=\"cursor: pointer;\" id=\"createTemplateDiv\" onclick=\"createTemplate()\"><img alt=\"add\" src=\"images/add16.png\"><span>Create Template</span></div>")
    html.write("<div class=\"template-div\" id=\"templateDiv\">")
    html.write(template_services_list())
    html.write("</div>")
    html.write(
        "<div class=\"main-title\" id=\"addTemplateDiv\"><img alt=\"\" src=\"images/add16.png\"><span>Add Template</span></div>")
    html.write("<div class=\"template-div\" id=\"addTemplateForm\">")
    html.write(add_template())
    html.write("</div>")
    html.write(
        "<div class=\"main-title\" id=\"editTemplateDiv\"><img alt=\"\" src=\"images/edit16.png\"><span>Edit Template</span></div>")
    html.write("<div class=\"template-div\" id=\"editTemplateForm\">")
    html.write(edit_template())
    html.write("</div>")
    html.write(
        "<div class=\"main-title\" style=\"cursor: pointer;\" id=\"addService\" onclick=\"addService()\"><img alt=\"add\" src=\"images/add16.png\"><span>Add Service</span></div>")
    html.write("<div class=\"template-div\" id=\"templateServiceList\">")
    html.write("</div>")
    html.new_footer()


def template_services_list():
    site = __file__.split("/")[3]
    dom = xml.dom.minidom.parseString("<hosts></hosts>")
    if (os.path.isfile("/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % site)):
        dom = xml.dom.minidom.parse(
            "/omd/sites/%s/share/check_mk/web/htdocs/xml/service_template.xml" % site)
    htmlString = ""
    for host in dom.getElementsByTagName("host"):
        hostName = host.getAttribute("name").strip()
        hostId = host.getAttribute("id").strip()
        srvList = "<div class=\"service-list-div\" id=\"serviceListDiv" + \
                  hostId + "\">"
        srvCount = 0
        for srv in host.getElementsByTagName("service"):
            srvCount += 1
            if srvCount % 2 == 0:
                srvList += "<div class=\"row-even\">" + \
                           srv.getAttribute("name") + "</div>"
            else:
                srvList += "<div class=\"row-even\">" + \
                           srv.getAttribute("name") + "</div>"
        srvList += "</div>"
        htmlString += "<div class=\"sub-title\"><span class=\"span-button\" onclick=\"hostServiceShowHide(this,'" + hostId + "')\">" + \
                      hostName + "</span>"
        htmlString += "<img onclick=\"editTemplate('" + hostId + \
                      "')\" class=\"delete-button\" title=\"Delete Template\" alt=\"delete\" src=\"images/delete16.png\"/>"
        htmlString += "<img onclick=\"deleteTemplate('" + hostId + \
                      "')\" class=\"edit-button\" title=\"Edit Template\" alt=\"edit\" src=\"images/edit16.png\"/>"
        htmlString += "</div>"
        htmlString += srvList

    return htmlString


def add_template():
    htmlString = "<div class=\"row-odd\"><div style=\"float:left; line-height: 20px;\">Template Name</div>"
    htmlString += "<div style=\"float:left;margin-left:20px;\"><input type=\"text\" name=\"addTemplateName\" id=\"addTemplateName\" value=\"\" /></div>"
    htmlString += "<div style=\"float:left;margin-left:5px;\"><input type=\"button\" value=\"Add Template\" onclick=\"addTemplate();\" /></div>"
    htmlString += "<div style=\"float:left;margin-left:5px;\"><input type=\"button\" value=\"Cancel\" onclick=\"cancelAddTemplate();\" /></div>"
    htmlString += "</div>"
    return htmlString


def edit_template():
    htmlString = "<div class=\"row-odd\"><div style=\"float:left; line-height: 20px;\">Template Name</div>"
    htmlString += "<div style=\"float:left;margin-left:20px;\"><input type=\"text\" name=\"updateTemplateName\" id=\"updateTemplateName\" value=\"\" /></div>"
    htmlString += "<div style=\"float:left;margin-left:5px;\"><input type=\"button\" value=\"Update Template\" onclick=\"updateTemplate();\" /></div>"
    htmlString += "<div style=\"float:left;margin-left:5px;\"><input type=\"button\" value=\"Cancel\" onclick=\"cancelUpdateTemplate();\" /></div>"
    htmlString += "</div>"
    return htmlString

################################# Update Service Template ################

################################# Delete Service Template ################

################################## View Service Template #################
