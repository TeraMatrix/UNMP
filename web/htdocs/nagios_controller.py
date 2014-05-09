#!/usr/bin/python2.6

"""
@author: Mahipal Choudhary
@since: 07-Nov-2011
@version: 0.1
@note: All Controller functions Related with Reporting.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Mahipal Choudhary for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
"""

# Import modules that contain the function and libraries
from json import JSONEncoder

from nagios import Nagios
from nagios_bll import NagiosBll

########### hosts
## inventory


def advanced_host_settings_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    host_id = html.var("host_id")
    if (host_id != "" and host_id is None):
        n_bll = NagiosBll()
        result = n_bll.get_advanced_host_settings_nagios(host_id)
    else:
        result = {}
    html.write(Nagios.advanced_host_settings(result))


def apply_advanced_host_settings_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    n_bll = NagiosBll()
    result = n_bll.apply_advanced_host_settings_nagios(req_vars)
    html.write(result)


def nagios_load(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_load.py", header_btn, css_list,
                    js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu())
    html.new_footer()


def get_host_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data(req_vars)
    html.write(result)


def edit_nagios_host_from_inventory(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    host_id = html.var("host_id")
    n_bll = NagiosBll()
    host_name = n_bll.get_host_name_from_host_id(host_id)
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    html.new_header(
        "Edit host", "manage_host.py", "", css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]

    result = n_bll.get_nagios_host_by_name(host_name)
    selected_columns = result["data"].get("use", "").split(",")
    non_selected_columns = [i[0] for i in result["options"].get(
        "use", [[]]) if i[0] not in selected_columns and i[0] != ""]
    result["html"] = Nagios.get_columns(
        selected_columns, non_selected_columns, " Select Host templates ")
    # html.write(result)
    # html.write(JSONEncoder().encode(result))
    html.write('<input type=\"text\" id=\"host_name_nagios\" value=\"%s\" style=\"display:none\"/>' % (host_name) +
               Nagios.main_menu_host_inventory())
    html.new_footer()


def edit_nagios_host(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    host_name = html.var("host_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_host_by_name(host_name)
    selected_columns = result["data"].get("use", "").split(",")
    non_selected_columns = [i[0] for i in result["options"].get(
        "use", [[]]) if i[0] not in selected_columns and i[0] != ""]
    result["html"] = Nagios.get_columns(
        selected_columns, non_selected_columns, " Select Host templates ")
    # html.write(result)
    html.write(JSONEncoder().encode(result))


def save_nagios_edit_host(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_host(req_vars)
    html.write(result)

########### host templates


def nagios_load_host_template(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>\
    <div class=\"header-icon\"><img onclick=\"delHostTemplate();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_host_template\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Host Template\"></div>\
    <div class=\"header-icon\"><img onclick=\"addHostTemplate();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_host_template\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Host Template\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_host_template.py", header_btn,
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_host_template())
    html.new_footer()


def get_host_template_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_host_template(req_vars)
    html.write(result)


def edit_nagios_host_template(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    host_template_name = html.var("host_template_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_host_template_by_name(host_template_name)
    # html.write(result)
    selected_columns = result["data"].get("use", "").split(",")
    non_selected_columns = [i[0] for i in result["options"].get(
        "use", [[]]) if i[0] not in selected_columns and i[0] != ""]
    result["html"] = Nagios.get_columns(
        selected_columns, non_selected_columns, " Select Host templates ")
    # html.write(result)
    html.write(JSONEncoder().encode(result))


def save_nagios_edit_host_template(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_host_template(req_vars)
    html.write(result)


def nagios_delete_host_template(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.nagios_delete_host_template(req_vars)
    html.write(result)

########### services


def nagios_service(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>\
    <div class=\"header-icon\"><img onclick=\"delService();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_service\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Service\"></div>\
    <div class=\"header-icon\"><img onclick=\"addService();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_service\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Service\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_service.py", header_btn,
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_service())
    html.new_footer()


def get_service_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_service(req_vars)
    html.write(result)


def edit_nagios_service(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    service_unique_key = html.var("service_unique_key")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_service_by_name(service_unique_key)
    # html.write(result)
    selected_columns = result["data"].get("use", "").split(",")
    non_selected_columns = [i[0] for i in result["options"].get(
        "use", [[]]) if i[0] not in selected_columns and i[0] != ""]
    result["html"] = Nagios.get_columns(
        selected_columns, non_selected_columns, " Select Service templates ")
    # html.write(result)
    html.write(JSONEncoder().encode(result))


def save_nagios_edit_service(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_service(req_vars)
    html.write(result)


def nagios_delete_service(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.nagios_delete_service(req_vars)
    html.write(result)


########### service templates
def nagios_service_template(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/new_icons/{0}\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>\
    <div class=\"header-icon\"><img onclick=\"delServiceTemplate();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_service_template\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Service Template\"></div>\
    <div class=\"header-icon\"><img onclick=\"addServiceTemplate();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_service_template\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Service Template\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_service_template.py", header_btn,
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_service_template())
    html.new_footer()


def get_service_template_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_service_template(req_vars)
    html.write(result)


def edit_nagios_service_template(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    service_unique_key = html.var("service_unique_key")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_service_template_by_name(service_unique_key)
    # html.write(result)
    selected_columns = result["data"].get("use", "").split(",")
    non_selected_columns = [i[0] for i in result["options"].get(
        "use", [[]]) if i[0] not in selected_columns and i[0] != ""]
    result["html"] = Nagios.get_columns(
        selected_columns, non_selected_columns, " Select Service templates ")
    # html.write(result)
    html.write(JSONEncoder().encode(result))


def save_nagios_edit_service_template(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_service_template(req_vars)
    html.write(result)


def nagios_delete_service_template(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.nagios_delete_service_template(req_vars)
    html.write(result)


########### hostgroups
def nagios_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/new_icons/{0}\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_hostgroup_load.py", header_btn,
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_hostgroup())
    html.new_footer()


def get_hostgroup_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_hostgroup(req_vars)
    html.write(result)


def edit_nagios_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    host_name = html.var("hostgroup_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_hostgroup_by_name(host_name)
    html.write(result)


def edit_nagios_hostgroup_from_inventory(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    hostgroup_id = html.var("hostgroup_id")
    n_bll = NagiosBll()
    hostgroup_name = n_bll.get_hostgroup_name_from_hostgroup_id(hostgroup_id)

    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    html.new_header("Edit hostgroup", "manage_hostgroup.py", "",
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(
        '<input type=\"text\" id=\"hostgroup_name_nagios\" value=\"%s\" style=\"display:none\"/>' % (hostgroup_name) +
        Nagios.main_menu_hostgroup_inventory())
    html.new_footer()

#


def edit_nagios_hostgroup_inventory(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    hostgroup_name = html.var("hostgroup_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_hostgroup_inventory(hostgroup_name)
    html.write(result)


def save_nagios_hostgroup_inventory(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_hostgroup_inventory(req_vars)
    html.write(result)


def save_nagios_edit_hostgroup(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_hostgroup(req_vars)
    html.write(result)


########### servicegroup
def nagios_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_servicegroup_load.py",
                    header_btn, css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_servicegroup())
    html.new_footer()


def get_servicegroup_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_servicegroup(req_vars)
    html.write(result)


def edit_nagios_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    servicegroup_name = html.var("servicegroup_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_servicegroup_by_name(host_name)
    html.write(result)


def save_nagios_edit_servicegroup(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_servicegroup(req_vars)
    html.write(result)


########### commands
def nagios_command(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>\
    <div class=\"header-icon\"><img onclick=\"delCommand();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_command\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Command\"></div>\
    <div class=\"header-icon\"><img onclick=\"addCommand();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_command\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Command\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_command_load.py", header_btn,
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_command())
    html.new_footer()


def get_command_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_command(req_vars)
    html.write(result)


def edit_nagios_command(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    command_name = html.var("command_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_command_by_name(command_name)
    html.write(result)


def save_nagios_edit_command(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_command(req_vars)
    html.write(result)


def nagios_delete_command(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.nagios_delete_command(req_vars)
    html.write(result)

########### hostdependency


def nagios_hostdependency(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js", "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>\
    <div class=\"header-icon\"><img onclick=\"delHostDependency();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_hostdependency\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Host Dependency\"></div>\
    <div class=\"header-icon\"><img onclick=\"addHostdependency();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_hostdependency\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Host Dependency\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_hostdependency.py", header_btn,
                    css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_hostdependency())
    html.new_footer()


def get_hostdependency_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_hostdependency(req_vars)
    html.write(result)


def edit_nagios_hostdependency(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    hostdependency_name = html.var("hostdependency_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_hostdependency_by_name(hostdependency_name)
    html.write(result)


def save_nagios_edit_hostdependency(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_hostdependency(req_vars)
    html.write(result)


def nagios_delete_host_dependency(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.nagios_delete_hostdependency(req_vars)
    html.write(result)

########### servicedependency


def nagios_servicedependency(h):
    """

    @param h:
    """
    global html
    html = h
    css_list = ["css/demo_table_jui.css", "css/jquery.multiselect.css",
                "css/jquery.multiselect.filter.css", "css/jquery-ui-1.8.4.custom.css", "css/demo_page.css"]
    js_list = [
        "js/lib/main/jquery-ui-1.8.6.custom.min.js", "js/lib/main/jquery.multiselect.min.js",
        "js/lib/main/jquery.multiselect.filter.js",
        "js/lib/main/jquery.dataTables.min.js", "js/unmp/main/nagios.js"]
    snapin_list = ["Nagios", "reports", "views", "Alarm", "Inventory",
                   "Settings", "NetworkMaps", "user_management", "schedule", "Listing"]
    header_btn = "<div class=\"header-icon\"><img onclick=\"nagiosSettings();\" class=\"n-tip-image\" src=\"images/{0}/wrench.png\" id=\"settings_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\">\
    <img onclick=\"verifyConfiguration();\" class=\"n-tip-image\" src=\"images/{0}/checkbox_checked.png\" id=\"verify_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Verify Configuration\">\
    <img onclick=\"backupRestore();\" class=\"n-tip-image\" src=\"images/{0}/mail.png\" id=\"restore_configuration_btn\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Restore Configuration\"></div>\
    <div class=\"header-icon\"><img onclick=\"delServiceDependency();\" class=\"n-tip-image\" src=\"images/{0}/round_minus.png\" id=\"del_servicedependency\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Delete Service Dependency\"></div>\
    <div class=\"header-icon\"><img onclick=\"addServicedependency();\" class=\"n-tip-image\" src=\"images/{0}/round_plus.png\" id=\"add_servicedependency\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Add Service Dependency\"></div>".format(
        theme)
    html.new_header("Nagios", "nagios_servicedependency.py",
                    header_btn, css_list, js_list, snapin_list)
    # user_id=html.req.session["user_id"]
    html.write(Nagios.main_menu_servicedependency())
    html.new_footer()


def get_servicedependency_data_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    req_vars = html.req.vars
    result = n_bll.get_log_data_servicedependency(req_vars)
    html.write(result)


def edit_nagios_servicedependency(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    servicedependency_name = html.var("servicedependency_name")
    n_bll = NagiosBll()
    result = n_bll.get_nagios_servicedependency_by_name(servicedependency_name)
    html.write(result)


def save_nagios_edit_servicedependency(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.save_nagios_edit_servicedependency(req_vars)
    html.write(result)


def nagios_delete_service_dependency(h):
    """

    @param h:
    """
    global html
    html = h
    req_vars = html.req.vars
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    result = n_bll.nagios_delete_servicedependency(req_vars)
    html.write(result)


############ settings
def settings_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    n_bll = NagiosBll()
    result = n_bll.get_nagios_status()
    html.write(str(Nagios.settings_nagios(result)))


def nagios_force_sync(h):
    """

    @param h:
    """
    global html
    html = h
    n_bll = NagiosBll()
    result = n_bll.nagios_force_sync()
    html.write(result)


def do_action_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    n_bll = NagiosBll()
    action = html.var("action")
    result = n_bll.do_action_nagios(action)
    result_after_action = n_bll.get_nagios_status()
    if result_after_action == "Nagios is running":
        result = {"success": 0}
    else:
        result = {"success": 1}
    html.write(JSONEncoder().encode(result))


def do_verify_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    n_bll = NagiosBll()
    action = html.var("action")
    result = n_bll.do_verify_nagios(action)
    html.write(result)

########### page tips

#
# def view_page_tip_nagios_host(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_host())
#
#
# def view_page_tip_nagios_host_template(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_host_template())
#
#
# def view_page_tip_nagios_service(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_service())
#
#
# def view_page_tip_nagios_service_template(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_service_template())
#
#
# def view_page_tip_nagios_hostgroup(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_hostgroup())
#
#
# def view_page_tip_nagios_servicegroup(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_servicegroup())
#
#
# def view_page_tip_nagios_command(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_command())
#
#
# def view_page_tip_nagios_hostdependency(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_hostdependency())
#
#
# def view_page_tip_nagios_servicedependency(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_servicedependency())
#
#
# def view_page_tip_nagios_inventory_hosts(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_inventory_hosts())
#
#
# def view_page_tip_nagios_inventory_hostgroups(h):
#     global html
#     html = h
#     html.write(Nagios.view_page_tip_nagios_inventory_hostgroups())


def restore_config_nagios(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    backup_dict = n_bll.restore_config_nagios()
    result = Nagios.restore_config_nagios(backup_dict)
    html.write(result)


def restore_config_nagios_selected(h):
    """

    @param h:
    """
    global html
    html = h
    # user_id=html.req.session["user_id"]
    n_bll = NagiosBll()
    file_name = html.var("file_name")
    result = n_bll.restore_config_nagios_selected(file_name)
    html.write(result)
