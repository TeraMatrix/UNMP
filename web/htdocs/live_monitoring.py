#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 23-Oct-2011
@version: 0.1
@note: All Views Related with Inventory.
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''


class LiveMonitoring(object):
    @staticmethod
    def header_buttons():
        add_btn = "<div class=\"header-icon\"><img onclick=\"liveSettings();\" class=\"n-tip-image\" src=\"images/%s/wrench.png\" id=\"add_host\" style=\"width: 16px; height: 16px; margin: 6px 20px 6px 10px;\" original-title=\"Settings\"></div>" % theme
        header_btn = add_btn
        return header_btn

    @staticmethod
    def live_monitring(host_id):
        return "<input type=\"hidden\" id=\"host_id\" name=\"host_id\" value=\"%s\"><div id=\"host_details\"></div><div id=\"live_monitoring\"></div><div id=\"live_monitoring_setting_div\" style=\"display:none;\"></div>" % host_id

    # @staticmethod
    # def page_tip_live_monitoring():
    #     import defaults
    #     f = open(defaults.web_dir + "/htdocs/locale/page_tip_live_monitoring.html", "r")
    #     html_view = f.read()
    #     f.close()
    #     return str(html_view)

    @staticmethod
    def settings_live_monitoring(device_type_select_list, protocol_select_list, dataset_select_list,
                                 ds_show_select_list, refresh_rate_select_list):
        html_view = "" \
                    "<div action=\"#\" id=\"form_settings_live_monitoring\" method=\"get\"> " \
                    "<div class=\"form-div\">" \
                    "<table class=\"tt-table\" cellspacing=\"0\" cellpadding=\"0\" width=\"100%\">" \
                    "<tr>" \
                    "<th id=\"form_title\" class=\"cell-title\"> Settings <img class=\"img-link\" src=\"images/new/close.png\" style=\"float: right; margin-right: 10px;\" original-title=\"Close\" id=\"close\"/></th>" \
                    "</tr>" \
                    "</table>" \
                    "<div class=\"row-elem\">" \
                    "<label class=\"lbl lbl-big\" for=\"device_type\">Device Type</label>" \
                    "" + device_type_select_list + "" \
                                                   "</div>" \
                                                   "<div class=\"row-elem\">" \
                                                   "<label class=\"lbl lbl-big\" for=\"rrd_step\">Refresh Rate</label>" \
                                                   "" + refresh_rate_select_list + "" \
                                                                                   "</div>" \
                                                                                   "<div class=\"row-elem\">" \
                                                                                   "<label class=\"lbl lbl-big\" for=\"name\">Graph Name</label>" \
                                                                                   "<div id=\"graph_name_div\"></div>" \
                                                                                   "</div>" \
                                                                                   "<div class=\"row-elem\">" \
                                                                                   "<label class=\"lbl lbl-big\" for=\"desc\">Graph Description</label>" \
                                                                                   "<textarea id=\"desc\" name=\"desc\" title=\"Enter Graph Description\" ></textarea>" \
                                                                                   "</div>" \
                                                                                   "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                   "<label class=\"lbl lbl-big\" for=\"is_localhost\">Is UNMP System</label>" \
                                                                                   "<input type=\"checkbox\" id=\"is_localhost\" name=\"is_localhost\" title=\"Check it if this graph for UNMP System \" />" \
                                                                                   "</div>" \
                                                                                   "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                   "<label class=\"lbl lbl-big\" for=\"is_snmp\">Protocol</label>" \
                                                                                   "" + protocol_select_list + "" \
                                                                                                               "</div>" \
                                                                                                               "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                               "<label class=\"lbl lbl-big\" for=\"oid_table\">Table OID</label>" \
                                                                                                               "<input type=\"text\" id=\"oid_table\" name=\"oid_table\" title=\"Enter Table Object ID\" />" \
                                                                                                               "</div>" \
                                                                                                               "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                               "<label class=\"lbl lbl-big\" for=\"row_index\">Table Row X Column</label>" \
                                                                                                               "<input type=\"text\" id=\"row\" name=\"row\" style=\"width:20px;\" value=\"0\" onkeypress=\"return isNumberKey(event);\" />" \
                                                                                                               " x " \
                                                                                                               "<input type=\"text\" id=\"column\" name=\"column\" style=\"width:20px;\" value=\"0\" onkeypress=\"return isNumberKey(event);\"/>" \
                                                                                                               "</div>" \
                                                                                                               "<div class=\"row-elem\" id=\"rrd_table_div\" style=\"display:none;\">" \
                                                                                                               "<label class=\"lbl lbl-big\" for=\"\">Dataset</label>" \
                                                                                                               "<table class=\"yo-table\" style=\"width:400px;border:1px solid #AAA;float:left\">" \
                                                                                                               "<tr class=\"yo-table-head\">" \
                                                                                                               "<th>Row Index</th>" \
                                                                                                               "<th>Column Index</th>" \
                                                                                                               "<th>Dataset Name</th>" \
                                                                                                               "</tr>" \
                                                                                                               "<tr>" \
                                                                                                               "<td colspan=\"3\"> No row exist </td>" \
                                                                                                               "</tr>" \
                                                                                                               "</table>" \
                                                                                                               "</div>" \
                                                                                                               "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                               "<label class=\"lbl lbl-big\" for=\"ds_type\">Dataset Type</label>" \
                                                                                                               "" + dataset_select_list + "" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"ds_heartbeat\">Dataset HeartBeat</label>" \
                                                                                                                                          "<input type=\"text\" id=\"ds_heartbeat\" name=\"ds_heartbeat\" title=\"Enter Dataset Heartbeat\" onkeypress=\"return isNumberKey(event);\" />" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"ds_lower_limit\">Dataset Lower Limit</label>" \
                                                                                                                                          "<input type=\"text\" id=\"ds_lower_limit\" name=\"ds_lower_limit\" title=\"Enter Dataset Lower Limit\" />" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"ds_upper_limit\">Dataset Upper Limit</label>" \
                                                                                                                                          "<input type=\"text\" id=\"ds_upper_limit\" name=\"ds_upper_limit\" title=\"Enter Dataset Upper Limit\" />" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"unit\">Unit</label>" \
                                                                                                                                          "<input type=\"text\" id=\"unit\" name=\"unit\" title=\"Enter Unit Name\" />" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"rrd_file_name\">RRD File Name</label>" \
                                                                                                                                          "<input type=\"text\" id=\"rrd_file_name\" name=\"rrd_file_name\" title=\"Enter RRD File Name\" />" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"timestamp\">Timestamps</label>" \
                                                                                                                                          "<input type=\"text\" id=\"timestamp\" name=\"timestamp\" title=\"Enter RRD File Name\" value=\"N\" />" \
                                                                                                                                          "</div>" \
                                                                                                                                          "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                          "<label class=\"lbl lbl-big\" for=\"show_ds\">show Dataset</label>" \
                                                                                                                                          "" + ds_show_select_list + "" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"dyn_ds_name\">Dataset Dynamic</label>" \
                                                                                                                                                                     "<input type=\"checkbox\" id=\"dyn_ds_name\" name=\"dyn_ds_name\" title=\"Check it if graph show dynamic name for datasets\" />" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"get_dyn_name\">Function for Dataset Dynamic</label>" \
                                                                                                                                                                     "<input type=\"text\" id=\"get_dyn_name\" name=\"get_dyn_name\" title=\"Enter Function to graph show dynamic name for datasets\" />" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"unreachable_value\">Unreachable Value</label>" \
                                                                                                                                                                     "<input type=\"text\" id=\"unreachable_value\" name=\"unreachable_value\" title=\"Enter value for unreachable device\" />" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"row-elem\" style=\"display:none;\">" \
                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"rrd_size\">Database Size</label>" \
                                                                                                                                                                     "<input type=\"text\" id=\"rrd_size\" name=\"rrd_size\" style=\"width:20px;\" title=\"Enter Execution Timout\" value=\"24\" onkeypress=\"return isNumberKey(event);\" /> (in hours)" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"row-elem\">" \
                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"total_rra\">Total Archive</label>" \
                                                                                                                                                                     "<input type=\"text\" id=\"total_rra\" name=\"total_rra\" style=\"width:20px;\" title=\"Enter Total Round Robin Archive\" value=\"0\" onkeypress=\"return isNumberKey(event);\" />" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"row-elem\" id=\"rra_table_div\">" \
                                                                                                                                                                     "<label class=\"lbl lbl-big\" for=\"\">Archive Details</label>" \
                                                                                                                                                                     "<table class=\"yo-table\" style=\"width:400px;border:1px solid #AAA;float:left\">" \
                                                                                                                                                                     "<tr class=\"yo-table-head\">" \
                                                                                                                                                                     "<th>Function</th>" \
                                                                                                                                                                     "<th>Total Dataset</th>" \
                                                                                                                                                                     "</tr>" \
                                                                                                                                                                     "<tr>" \
                                                                                                                                                                     "<td colspan=\"2\"> No Archive exist </td>" \
                                                                                                                                                                     "</tr>" \
                                                                                                                                                                     "</table>" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "<div class=\"form-div-footer\">" \
                                                                                                                                                                     "<button type=\"buttom\" class=\"yo-small yo-button\" id=\"save\"><span class=\"ok\">Save</span></button>" \
                                                                                                                                                                     "<button type=\"button\" class=\"yo-small yo-button\" id=\"cancel\"><span class=\"cancel\">Cancel</span></button>" \
                                                                                                                                                                     "</div>" \
                                                                                                                                                                     "</div>"
        return html_view
